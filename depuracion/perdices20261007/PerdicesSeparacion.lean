import PerdicesCruce

/-! # Perdices: lo que una cota superior exige a los tiempos de regreso.

La semilla y el techo se conservan. Una lista estrictamente creciente
de visitas puede ser incompleta; para interpretar sus saltos como huecos
sin visitas intermedias debe enumerar todos los regresos.
-/

namespace PerdicesSeparacion

open Ocelotas CasaPlano CasaRetrato PerdicesCruce OcelotasTrayectorias

@[irreducible] def constante (n c : ℕ) : ℕ := 2 ^ (150 * c + 894) * (3 ^ c * n) ^ 144

open Classical in
theorem cuenta_lista {n c r : ℕ} {t : ℕ → ℕ} (ht : StrictMono t)
    (hb : ∀ i ≤ r, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) :
    r + 1 ≤ regresos n c (t r + 1) := by
  rw [← Finset.card_range (r + 1)]
  unfold regresos
  refine Finset.card_le_card_of_injOn t ?_ ?_
  · intro i hi
    simp only [Finset.mem_coe, Finset.mem_range, Finset.mem_filter] at hi ⊢
    exact ⟨by have := ht.monotone (show i ≤ r by omega); omega, hb i (by omega)⟩
  · intro i _ j _ hij
    exact ht.injective hij

theorem tiempo_por_indice {n c r : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i ≤ r, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) :
    (r + 1) ^ 150 ≤ constante n c * (t r + 1) ^ 24 := by
  simpa only [constante] using
    (Nat.pow_le_pow_left (cuenta_lista ht hb) 150).trans (exponente_temporal h c _)

theorem tiempo_de_saltos {t : ℕ → ℕ} {r D : ℕ}
    (hs : ∀ i < r, t (i + 1) ≤ t i + D) : t r ≤ t 0 + D * r := by
  induction r with
  | zero => simp
  | succ r ih =>
    have hr := ih (fun i hi => hs i (by omega))
    have hh := hs r (by omega)
    rw [Nat.mul_succ]
    omega

theorem presupuesto_saltos {n c r D : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i ≤ r, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i)
    (hs : ∀ i < r, t (i + 1) ≤ t i + D) :
    (r + 1) ^ 126 ≤ constante n c * (t 0 + D + 1) ^ 24 := by
  have hp := tiempo_por_indice h ht hb
  have hr := tiempo_de_saltos hs
  have htr : t r + 1 ≤ (t 0 + D + 1) * (r + 1) := by nlinarith
  have hc : (r + 1) ^ 126 * (r + 1) ^ 24 ≤
      (constante n c * (t 0 + D + 1) ^ 24) * (r + 1) ^ 24 := by
    calc
      _ = (r + 1) ^ 150 := by rw [← pow_add]
      _ ≤ constante n c * (t r + 1) ^ 24 := hp
      _ ≤ constante n c * ((t 0 + D + 1) * (r + 1)) ^ 24 :=
        Nat.mul_le_mul_left _ (Nat.pow_le_pow_left htr 24)
      _ = _ := by rw [mul_pow]; exact (Nat.mul_assoc _ _ _).symm
  exact Nat.le_of_mul_le_mul_right hc (Nat.pow_pos (by omega : 0 < r + 1))

theorem existe_salto_grande {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) (D : ℕ) :
    ∃ i, t i + D < t (i + 1) := by
  by_contra hh
  have hs : ∀ i, t (i + 1) ≤ t i + D := by simpa using hh
  let B := constante n c * (t 0 + D + 1) ^ 24
  have hp : (B + 1) ^ 126 ≤ B := presupuesto_saltos h ht (fun i _ => hb i) (fun i _ => hs i)
  have hl : B + 1 ≤ (B + 1) ^ 126 := le_self_pow₀ (by omega) (by decide)
  omega

theorem saltos_grandes_tarde {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) (D a : ℕ) :
    ∃ i, a ≤ i ∧ t i + D < t (i + 1) := by
  have hm : StrictMono (fun i => t (a + i)) := fun i j hij => ht (by omega)
  obtain ⟨i, hi⟩ := existe_salto_grande h hm (fun i => hb (a + i)) D
  exact ⟨a + i, by omega, by simpa [Nat.add_assoc] using hi⟩

theorem reloj_sextico_imposible {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) (B : ℕ) :
    ¬ ∀ r, t r + 1 ≤ B * (r + 1) ^ 6 := by
  intro hr
  let M := constante n c * B ^ 24
  have hp := tiempo_por_indice h ht (r := M) (fun i _ => hb i)
  have hc : (M + 1) ^ 6 * (M + 1) ^ 144 ≤ M * (M + 1) ^ 144 := by
    calc
      _ = (M + 1) ^ 150 := by rw [← pow_add]
      _ ≤ constante n c * (t M + 1) ^ 24 := hp
      _ ≤ constante n c * (B * (M + 1) ^ 6) ^ 24 :=
        Nat.mul_le_mul_left _ (Nat.pow_le_pow_left (hr M) 24)
      _ = _ := by rw [mul_pow, ← pow_mul]; exact (Nat.mul_assoc _ _ _).symm
  have hh : (M + 1) ^ 6 ≤ M :=
    Nat.le_of_mul_le_mul_right hc (Nat.pow_pos (by omega : 0 < M + 1))
  have hl : M + 1 ≤ (M + 1) ^ 6 := le_self_pow₀ (by omega) (by decide)
  omega

theorem impares_por_rachas {x r L : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hx : x + 1 ≤ 2 ^ L) :
    acumulados a r + L ≤ 2 ^ r * L := by
  have hpaso : ∀ i < r, acumulados a (i + 1) ≤ L + 2 * acumulados a i := by
    intro i hi
    have hc := congruencias_acumuladas hw i hi
    have htres : 3 ^ acumulados a i ≤ 2 ^ (2 * acumulados a i) := by
      simpa only [pow_mul] using Nat.pow_le_pow_left (by decide : 3 ≤ 2 ^ 2) (acumulados a i)
    have hh : 2 ^ acumulados a (i + 1) ≤ 2 ^ (L + 2 * acumulados a i) := by
      calc
        _ ≤ (x + 1) * 3 ^ acumulados a i := hc
        _ ≤ 2 ^ L * 2 ^ (2 * acumulados a i) := Nat.mul_le_mul hx htres
        _ = _ := (pow_add _ _ _).symm
    exact (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 hh
  have htotal : ∀ i ≤ r, acumulados a i + L ≤ 2 ^ i * L := by
    intro i
    induction i with
    | zero => intro _; simp [acumulados]
    | succ i ih =>
      intro hi
      have h1 := ih (by omega)
      have h2 := hpaso i (by omega)
      rw [pow_succ]
      nlinarith
  exact htotal r le_rfl

theorem duracion_por_rachas {x r L c : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hx : x + 1 ≤ 2 ^ L)
    (hp : 2 ^ tiempo a b r ≤ 3 ^ c * 3 ^ S (tiempo a b r) x) :
    tiempo a b r ≤ 2 * ((2 ^ r - 1) * L + c) := by
  have hs := impares_por_rachas hw hx
  have hi := cuenta_impares hw r le_rfl
  have he : 2 ^ r * L = (2 ^ r - 1) * L + L := by
    have ht := Nat.one_le_two_pow (n := r)
    rw [Nat.sub_mul]
    omega
  have hfin : acumulados a r ≤ (2 ^ r - 1) * L := by omega
  have hpow : 2 ^ tiempo a b r ≤ 2 ^ (2 * (c + acumulados a r)) := by
    calc
      _ ≤ 3 ^ c * 3 ^ S (tiempo a b r) x := hp
      _ = 3 ^ (c + acumulados a r) := by rw [hi, pow_add]
      _ ≤ (2 ^ 2) ^ (c + acumulados a r) :=
        Nat.pow_le_pow_left (by decide) _
      _ = _ := (pow_mul _ _ _).symm
  have hd := (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 hpow
  omega

theorem tramo_desde_regreso {n u c r L : ℕ} {a b : ℕ → ℕ} (h : FugaPura n)
    (hu : 3 ^ S u n ≤ 3 ^ c * 2 ^ u)
    (hw : Palabra (T^[u] n) a b r) (hx : T^[u] n + 1 ≤ 2 ^ L) :
    tiempo a b r ≤ 2 * ((2 ^ r - 1) * L + c) := by
  exact duracion_por_rachas hw hx (PerdicesEstela.casi_fuga_de_bajo h hu _)

end PerdicesSeparacion

#print axioms PerdicesSeparacion.cuenta_lista
#print axioms PerdicesSeparacion.tiempo_por_indice
#print axioms PerdicesSeparacion.tiempo_de_saltos
#print axioms PerdicesSeparacion.presupuesto_saltos
#print axioms PerdicesSeparacion.existe_salto_grande
#print axioms PerdicesSeparacion.saltos_grandes_tarde
#print axioms PerdicesSeparacion.reloj_sextico_imposible
#print axioms PerdicesSeparacion.impares_por_rachas
#print axioms PerdicesSeparacion.duracion_por_rachas
#print axioms PerdicesSeparacion.tramo_desde_regreso
