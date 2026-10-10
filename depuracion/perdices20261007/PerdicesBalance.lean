import PerdicesRitmo

/-! # Perdices: balance par y exclusión de excursiones interiores 110.

Las cotas de bloques se expresan con enteros. Las excursiones regulares
pueden tener tantas rachas como se quiera; sólo sus bloques interiores
se restringen a 110, con una última racha par de longitud libre.
-/

namespace PerdicesBalance

open Ocelotas CasaPlano CasaRetrato OcelotasTrayectorias OcelotasContador
open PerdicesSeparacion PerdicesExcursiones PerdicesRitmo

theorem balance_bloque {x r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hi : i < r) :
    2 ^ (a i + b i) * (T^[tiempo a b (i + 1)] x + 1) + 2 ^ a i =
      3 ^ a i * (T^[tiempo a b i] x + 1) + 2 ^ (a i + b i) := by
  have he := congrArg (fun z : ℕ => 2 ^ a i * z) (identidad_par hw hi)
  have ho := identidad_impar hw hi
  rw [pow_add]
  nlinarith only [he, ho]

theorem tiempo_descompuesto (a b : ℕ → ℕ) (i : ℕ) :
    tiempo a b i = acumulados a i + acumulados b i := by
  induction i with
  | zero => rfl
  | succ i ih => simp only [tiempo, acumulados, ih]; omega

theorem balance_prefijo {x r k : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hk : k ≤ r)
    (hp : ∀ i ≤ k, 2 ^ tiempo a b i ≤ 3 ^ acumulados a i) :
    2 ^ tiempo a b k * (T^[tiempo a b k] x + 1) ≤
      3 ^ acumulados a k * (x + 1 + k) := by
  induction k with
  | zero => simp [tiempo, acumulados]
  | succ k ih =>
    have hprev := ih (by omega) (fun i hi => hp i (by omega))
    have hbal := congrArg (fun z : ℕ => 2 ^ tiempo a b k * z) (balance_bloque hw (by omega : k < r))
    have hmul := Nat.mul_le_mul_left (3 ^ a k) hprev
    have hfin := hp (k + 1) le_rfl
    simp only [tiempo, acumulados, pow_add] at hbal hfin ⊢
    nlinarith only [hbal, hmul, hfin,
      Nat.zero_le (2 ^ tiempo a b k * 2 ^ a k)]

theorem presupuesto_par {x r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hi : i < r)
    (hp : ∀ j ≤ i, 2 ^ tiempo a b j ≤ 3 ^ acumulados a j) :
    2 ^ (acumulados a (i + 1) + acumulados b i) ≤
      3 ^ acumulados a i * (x + 1 + i) := by
  have hc := Nat.le_of_dvd (by omega : 0 < T^[tiempo a b i] x + 1)
    (congruencia_racha hw hi)
  have hh := Nat.mul_le_mul_left (2 ^ tiempo a b i) hc
  have hb := balance_prefijo hw (by omega) hp
  have he : tiempo a b i + a i = acumulados a (i + 1) + acumulados b i := by
    rw [tiempo_descompuesto, acumulados]; omega
  rw [← pow_add, he] at hh
  exact hh.trans hb

theorem interior_sin_cruce {n c u v j : ℕ}
    (he : Consecutivos n c u v) (hj : j < v - u) :
    2 ^ j ≤ 3 ^ S j (T^[u] n) := by
  by_cases h0 : j = 0
  · simp [h0, S]
  have hinter := he.2.2.2 (u + j) (by omega) (by omega : u + j < v)
  have hu := he.2.1
  unfold Bajo at hu hinter
  rw [S_add, pow_add, pow_add] at hinter
  by_contra hh
  have hle : 3 ^ S j (T^[u] n) ≤ 2 ^ j := by omega
  exact hinter (by simpa only [Nat.mul_assoc] using Nat.mul_le_mul hu hle)

theorem presupuesto_excursion {n c u v r i : ℕ} {a b : ℕ → ℕ}
    (he : Consecutivos n c u v)
    (hw : Palabra (T^[u] n) a b r) (hfin : tiempo a b r = v - u)
    (hi : i < r) :
    2 ^ (acumulados a (i + 1) + acumulados b i) ≤
      3 ^ acumulados a i * (T^[u] n + 1 + i) := by
  apply presupuesto_par hw hi
  intro j hj
  have hjr : j < r := by omega
  have ht := tiempo_lt hw hjr
  rw [hfin] at ht
  have hp := interior_sin_cruce he ht
  rwa [cuenta_impares hw j (by omega)] at hp

/-- Una cadena afín trasladada conserva su identidad multiplicativa. -/
theorem cadena_trasladada {A M r : ℕ} {z : ℕ → ℕ}
    (hz : ∀ i < r, M * z (i + 1) = A * z i) : M ^ r * z r = A ^ r * z 0 := by
  induction r with
  | zero => simp
  | succ r ih =>
    have hprev := ih (fun i hi => hz i (by omega))
    have hpaso := congrArg (fun z : ℕ => M ^ r * z) (hz r (by omega))
    have hprev := congrArg (fun z : ℕ => A * z) hprev
    simp only [pow_succ]
    nlinarith only [hpaso, hprev]

theorem divisibilidad_trasladada {A M r : ℕ} {z : ℕ → ℕ}
    (hc : Nat.Coprime M A) (hz : ∀ i < r, M * z (i + 1) = A * z i) :
    M ^ r ∣ z 0 := by
  apply (hc.pow r r).dvd_of_dvd_mul_left
  exact ⟨z r, (cadena_trasladada hz).symm⟩

theorem bloque_110 {x r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hi : i < r) (ha : a i = 2) (hb : b i = 1) :
    8 * (T^[tiempo a b (i + 1)] x + 5) =
      9 * (T^[tiempo a b i] x + 5) := by
  have hh := balance_bloque hw hi
  rw [ha, hb] at hh
  norm_num at hh
  omega

theorem rachas_regulares {x r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (ha : ∀ i < r, a i = 2)
    (hb : ∀ i, i + 1 < r → b i = 1) : r ≤ x + 5 := by
  by_cases hr : r = 0
  · omega
  have hd : 8 ^ (r - 1) ∣ x + 5 := by
    have hh := divisibilidad_trasladada (z := fun i => T^[tiempo a b i] x + 5)
      (by decide : Nat.Coprime 8 9) (r := r - 1)
      (fun i hi => bloque_110 hw (by omega) (ha i (by omega)) (hb i (by omega)))
    simpa only [tiempo, Function.iterate_zero_apply] using hh
  have hp := Nat.le_of_dvd (by omega : 0 < x + 5) hd
  have h2 : 2 ^ (r - 1) ≤ 8 ^ (r - 1) := Nat.pow_le_pow_left (by decide) _
  have hh : r - 1 < 2 ^ (r - 1) := Nat.lt_two_pow_self
  omega

def Regular (x d : ℕ) : Prop :=
  d = 1 ∨ ∃ r a b, Palabra x a b r ∧ tiempo a b r = d ∧
    (∀ i < r, a i = 2) ∧ (∀ i, i + 1 < r → b i = 1)

theorem duracion_regular {n c u v : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v) (hr : Regular (T^[u] n) (v - u)) :
    v - u ≤ (24 + 2 * c) * T^[u] n := by
  have hx : 1 ≤ T^[u] n := iter_pos (by have := fuga_pura_dos h; omega) u
  rcases hr with hd | ⟨r, a, b, hw, ht, ha, hb⟩
  · rw [hd]; nlinarith
  · have hs : ∀ i ≤ r, acumulados a i = 2 * i := by
      intro i
      induction i with
      | zero => intro _; rfl
      | succ i ih => intro hi; rw [acumulados, ha i (by omega), ih (by omega)]; omega
    have hp := PerdicesEstela.casi_fuga_de_bajo h he.2.1 (tiempo a b r)
    rw [cuenta_impares hw r le_rfl, hs r le_rfl, ← pow_add] at hp
    have hp2 : 3 ^ (c + 2 * r) ≤ 2 ^ (2 * (c + 2 * r)) := by
      simpa only [← pow_mul] using Nat.pow_le_pow_left (by decide : 3 ≤ 2 ^ 2) (c + 2 * r)
    have hd := (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 (hp.trans hp2)
    have hr := rachas_regulares hw ha hb
    rw [ht] at hd
    nlinarith

theorem regular_cuadrado {n c u v : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v) (hr : Regular (T^[u] n) (v - u)) :
    (v - u) ^ 2 ≤ (24 + 2 * c) ^ 2 * ((3 ^ c) ^ 6 * n ^ 6) * (u + 1) := by
  have hx : 1 ≤ T^[u] n := iter_pos (by have := fuga_pura_dos h; omega) u
  have h6 := PerdicesSexta.regreso_sexta h he.2.1
  have hs := PerdicesEstela.S_le_pasos u n
  have h2 : (T^[u] n) ^ 2 ≤ (3 ^ c) ^ 6 * n ^ 6 * (u + 1) :=
    (Nat.pow_le_pow_right hx (by decide : 2 ≤ 6)).trans
      (h6.trans (Nat.mul_le_mul_left _ (by omega)))
  have hd := Nat.pow_le_pow_left (duracion_regular h he hr) 2
  rw [mul_pow] at hd
  exact hd.trans (by simpa only [Nat.mul_assoc] using Nat.mul_le_mul_left ((24 + 2 * c) ^ 2) h2)

theorem infinitos_exigen_irregulares {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (U : ℕ) :
    ∃ u v, U < u ∧ Consecutivos n c u v ∧ ¬ Regular (T^[u] n) (v - u) := by
  obtain ⟨t, hU, he⟩ := enumerar_regresos hi U
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have hx : ∃ i, ¬ Regular (T^[t i] n) (t (i + 1) - t i) := by
    by_contra hh
    have hr : ∀ i, Regular (T^[t i] n) (t (i + 1) - t i) := by simpa using hh
    have hclock := reloj_cuadratico ht.monotone (fun i => regular_cuadrado h (he i) (hr i))
    apply reloj_sextico_imposible h ht (fun i => (he i).2.1)
      ((24 + 2 * c) ^ 2 * ((3 ^ c) ^ 6 * n ^ 6) + t 0 + 1)
    intro i
    exact (hclock i).trans (Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by omega) (by decide)))
  obtain ⟨i, hir⟩ := hx
  have h0 := ht.monotone (Nat.zero_le i)
  exact ⟨t i, t (i + 1), by omega, he i, hir⟩

end PerdicesBalance

#print axioms PerdicesBalance.balance_bloque
#print axioms PerdicesBalance.tiempo_descompuesto
#print axioms PerdicesBalance.balance_prefijo
#print axioms PerdicesBalance.presupuesto_par
#print axioms PerdicesBalance.interior_sin_cruce
#print axioms PerdicesBalance.presupuesto_excursion
#print axioms PerdicesBalance.cadena_trasladada
#print axioms PerdicesBalance.divisibilidad_trasladada
#print axioms PerdicesBalance.bloque_110
#print axioms PerdicesBalance.rachas_regulares
#print axioms PerdicesBalance.duracion_regular
#print axioms PerdicesBalance.regular_cuadrado
#print axioms PerdicesBalance.infinitos_exigen_irregulares
