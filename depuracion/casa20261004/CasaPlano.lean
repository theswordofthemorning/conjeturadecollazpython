import OcelotasContador

/-! # Plano de la casa: las piezas de una prueba de Collatz

Ruta B, 04-10-2026. Inventario en `LEEME.md` de esta carpeta.

Se usa el atajo `T(n) = n/2` (par), `(3n+1)/2` (impar) de `Ocelotas`, y el mapa clásico
`C`. El pronóstico de `n` a los `k` pasos es `3^S k n / 2^k`, donde `S k n` cuenta las
subidas (pasos impares).

* `Cruza n`: el pronóstico baja de 1 alguna vez; es decir, τ(n) es finito.
* `Desciende n`: la órbita baja alguna vez de su punto de partida; σ(n) es finito.
* `MuroA`: para `n ≥ 2`, si `Cruza n` entonces `Desciende n`.
* `MuroB`: para `n ≥ 2`, `Cruza n`.

Teoremas principales:
* `collatz_iff_muros`: la conjetura de Collatz equivale a tener los dos muros;
* `techo`: con los dos muros, todo número llega a 1;
* `dos_fallas`: una órbita que no llega a 1 es un circuito o una fuga;
* `muroA_sin_circuitos`: el muro A, por sí solo, excluye los circuitos;
* `muroA_de_cst` y `muroA_de_tramos`: la conjetura CST, o todos los tramos por número
  de picos, levantan el muro A.

No hay hipótesis externas. Los muros que faltan son definiciones (`Prop`), no axiomas:
nada aquí afirma que se cumplan.

Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaPlano

open Ocelotas OcelotasContador

/-! ## Las definiciones -/

/-- Mapa clásico de Collatz. -/
def C (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- La conjetura de Collatz, con el mapa clásico. -/
def Collatz : Prop := ∀ n, 1 ≤ n → ∃ h, C^[h] n = 1

/-- `n` llega a 1 con el atajo. -/
def LlegaT (n : ℕ) : Prop := ∃ k, T^[k] n = 1

/-- El pronóstico llega a decir «abajo»: el primer cruce τ(n) es finito. -/
def Cruza (n : ℕ) : Prop := ∃ k, 3 ^ S k n < 2 ^ k

/-- La órbita baja alguna vez de su punto de partida: σ(n) es finito. -/
def Desciende (n : ℕ) : Prop := ∃ k, 1 ≤ k ∧ T^[k] n < n

/-- Muro A: si el pronóstico dice «abajo», el número termina bajando. -/
def MuroA : Prop := ∀ n, 2 ≤ n → Cruza n → Desciende n

/-- Muro B: el pronóstico siempre llega a decir «abajo». -/
def MuroB : Prop := ∀ n, 2 ≤ n → Cruza n

/-- Conjetura CST de Terras: el descenso ocurre justo en el primer cruce. -/
def CST : Prop := ∀ n k, 2 ≤ n → PrimerCruce n k → T^[k] n < n

/-- Tramo del muro A: números con a lo sumo `R` rachas (picos) hasta el primer cruce. -/
def MuroAHasta (R : ℕ) : Prop :=
  ∀ n k, 2 ≤ n → PrimerCruce n k → rachas n k ≤ R → Desciende n

/-- Circuito distinto de `1 → 2 → 1`: un valor positivo que vuelve a sí mismo y cuya
    órbita nunca pasa por 1. -/
def Circuito (x : ℕ) : Prop :=
  1 ≤ x ∧ (∃ p, 1 ≤ p ∧ T^[p] x = x) ∧ ∀ k, T^[k] x ≠ 1

/-- Fuga: la órbita supera cualquier cota. -/
def Fuga (n : ℕ) : Prop := ∀ M, ∃ k, M < T^[k] n

/-- Fuga pura: el pronóstico nunca llega a decir «abajo». -/
def FugaPura (n : ℕ) : Prop := ¬ Cruza n

/-! ## El radier: hechos básicos del atajo -/

theorem T_pos {n : ℕ} (h : 1 ≤ n) : 1 ≤ T n := by
  unfold T
  split_ifs <;> omega

theorem iter_pos {n : ℕ} (h : 1 ≤ n) (k : ℕ) : 1 ≤ T^[k] n := by
  induction k with
  | zero => simpa using h
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    exact T_pos ih

theorem iterT_succ (k n : ℕ) : T^[k + 1] n = T^[k] (T n) :=
  Function.iterate_succ_apply T k n

theorem iterC_succ (h n : ℕ) : C^[h + 1] n = C^[h] (C n) :=
  Function.iterate_succ_apply C h n

/-- La órbita de 1 es `1, 2, 1, 2, …`. -/
theorem iter_uno (i : ℕ) : T^[i] 1 ≤ 2 := by
  have h : ∀ i, T^[i] 1 = 1 ∨ T^[i] 1 = 2 := by
    intro i
    induction i with
    | zero => left; rfl
    | succ i ih =>
      rw [Function.iterate_succ_apply']
      rcases ih with h | h <;> rw [h] <;> decide
  rcases h i with h | h <;> omega

/-- Mientras el pronóstico no baja de 1, la órbita no baja de su punto de partida. -/
theorem no_baja {n k : ℕ} (hc : 2 ^ k ≤ 3 ^ S k n) : n ≤ T^[k] n := by
  have hp := Nat.mul_le_mul_right n hc
  have hc2 := cota_inferior n k
  have hpos : 0 < 2 ^ k := by positivity
  nlinarith

/-! ## El mapa clásico y el atajo dicen lo mismo -/

theorem C_par {n : ℕ} (h : n % 2 = 0) : C n = T n := by
  unfold C T
  rw [if_pos h, if_pos h]

theorem C_impar {n : ℕ} (h : n % 2 = 1) : C (C n) = T n := by
  have h1 : C n = 3 * n + 1 := by
    unfold C
    rw [if_neg (by omega)]
  rw [h1]
  unfold C T
  rw [if_pos (by omega), if_neg (by omega)]

/-- Cada valor de la órbita del atajo aparece en la órbita clásica. -/
theorem clasico_alcanza : ∀ k n, ∃ h, C^[h] n = T^[k] n := by
  intro k
  induction k with
  | zero => intro n; exact ⟨0, rfl⟩
  | succ k ih =>
    intro n
    obtain ⟨h, hh⟩ := ih (T n)
    rcases Nat.mod_two_eq_zero_or_one n with hp | hp
    · exact ⟨h + 1, by rw [iterC_succ, C_par hp, hh, iterT_succ]⟩
    · exact ⟨h + 1 + 1, by rw [iterC_succ, iterC_succ, C_impar hp, hh, iterT_succ]⟩

/-- Si la órbita clásica llega a 1, la del atajo también. -/
theorem atajo_alcanza : ∀ h n, C^[h] n = 1 → ∃ k, T^[k] n = 1 := by
  intro h
  induction h using Nat.strong_induction_on with
  | _ h ih =>
    intro n hn
    by_cases h1 : n = 1
    · exact ⟨0, by simp [h1]⟩
    have hh0 : h ≠ 0 := by
      rintro rfl
      simp at hn
      exact h1 hn
    obtain ⟨g, rfl⟩ : ∃ g, h = g + 1 := ⟨h - 1, by omega⟩
    rcases Nat.mod_two_eq_zero_or_one n with hp | hp
    · rw [iterC_succ, C_par hp] at hn
      obtain ⟨k, hk⟩ := ih g (by omega) (T n) hn
      exact ⟨k + 1, by rw [iterT_succ, hk]⟩
    · have hg0 : g ≠ 0 := by
        rintro rfl
        rw [iterC_succ] at hn
        simp only [Function.iterate_zero, id_eq] at hn
        unfold C at hn
        rw [if_neg (by omega)] at hn
        omega
      obtain ⟨f, rfl⟩ : ∃ f, g = f + 1 := ⟨g - 1, by omega⟩
      rw [iterC_succ, iterC_succ, C_impar hp] at hn
      obtain ⟨k, hk⟩ := ih f (by omega) (T n) hn
      exact ⟨k + 1, by rw [iterT_succ, hk]⟩

theorem llega_iff (n : ℕ) : (∃ h, C^[h] n = 1) ↔ LlegaT n := by
  constructor
  · rintro ⟨h, hh⟩
    exact atajo_alcanza h n hh
  · rintro ⟨k, hk⟩
    obtain ⟨h, hh⟩ := clasico_alcanza k n
    exact ⟨h, hh.trans hk⟩

theorem collatz_iff_atajo : Collatz ↔ ∀ n, 1 ≤ n → LlegaT n := by
  unfold Collatz
  constructor
  · intro h n hn
    exact (llega_iff n).1 (h n hn)
  · intro h n hn
    exact (llega_iff n).2 (h n hn)

/-! ## El techo: los dos muros bastan -/

/-- Si todo `n ≥ 2` baja alguna vez de sí mismo, todo número positivo llega a 1. -/
theorem llega_de_descensos (hD : ∀ n, 2 ≤ n → Desciende n) :
    ∀ n, 1 ≤ n → LlegaT n := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro hn
    by_cases h1 : n = 1
    · exact ⟨0, by simp [h1]⟩
    obtain ⟨k, -, hk⟩ := hD n (by omega)
    obtain ⟨j, hj⟩ := ih (T^[k] n) hk (iter_pos hn k)
    exact ⟨j + k, by rw [Function.iterate_add_apply, hj]⟩

/-- El techo: con el muro A y el muro B, todo número llega a 1. -/
theorem techo (hA : MuroA) (hB : MuroB) : Collatz :=
  collatz_iff_atajo.2 (llega_de_descensos fun n hn => hA n hn (hB n hn))

/-! ## Los dos muros son necesarios -/

/-- Antes de bajar de sí mismo, el pronóstico ya bajó de 1 (τ ≤ σ). -/
theorem cruza_de_desciende {n : ℕ} (h : Desciende n) : Cruza n := by
  obtain ⟨k, -, hk⟩ := h
  refine ⟨k, ?_⟩
  by_contra hc
  have := no_baja (not_lt.mp hc)
  omega

theorem desciende_de_llega {n : ℕ} (hn : 2 ≤ n) (h : LlegaT n) : Desciende n := by
  obtain ⟨k, hk⟩ := h
  refine ⟨k, ?_, by omega⟩
  rcases Nat.eq_zero_or_pos k with h0 | h0
  · subst h0
    simp at hk
    omega
  · exact h0

theorem muros_de_collatz (h : Collatz) : MuroA ∧ MuroB := by
  have hL := collatz_iff_atajo.1 h
  have hD : ∀ n, 2 ≤ n → Desciende n :=
    fun n hn => desciende_de_llega hn (hL n (by omega))
  exact ⟨fun n hn _ => hD n hn, fun n hn => cruza_de_desciende (hD n hn)⟩

/-- **La norma de la casa.** Collatz equivale a tener los dos muros. -/
theorem collatz_iff_muros : Collatz ↔ MuroA ∧ MuroB :=
  ⟨muros_de_collatz, fun h => techo h.1 h.2⟩

/-! ## Sólo hay dos maneras de fallar -/

theorem circuito_de_repeticion {n i j : ℕ} (hn : 1 ≤ n) (h : ¬ LlegaT n) (hlt : i < j)
    (heq : T^[i] n = T^[j] n) : Circuito (T^[i] n) := by
  refine ⟨iter_pos hn i, ⟨j - i, by omega, ?_⟩, ?_⟩
  · rw [← Function.iterate_add_apply, Nat.sub_add_cancel hlt.le, heq]
  · intro k hk
    exact h ⟨k + i, by rw [Function.iterate_add_apply, hk]⟩

/-- Una órbita que no llega a 1 contiene un circuito o es una fuga. -/
theorem dos_fallas {n : ℕ} (hn : 1 ≤ n) (h : ¬ LlegaT n) :
    (∃ i, Circuito (T^[i] n)) ∨ Fuga n := by
  classical
  by_cases hf : Fuga n
  · exact Or.inr hf
  left
  simp only [Fuga, not_forall, not_exists, not_lt] at hf
  obtain ⟨M, hM⟩ := hf
  have hmaps : Set.MapsTo (fun k => T^[k] n) (↑(Finset.range (M + 2)) : Set ℕ)
      (↑(Finset.range (M + 1)) : Set ℕ) := by
    intro k _
    simp only [Finset.mem_coe, Finset.mem_range]
    exact Nat.lt_succ_of_le (hM k)
  obtain ⟨i, -, j, -, hij, heq⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to (by simp) hmaps
  rcases lt_or_gt_of_ne hij with hlt | hlt
  · exact ⟨i, circuito_de_repeticion hn h hlt heq⟩
  · exact ⟨j, circuito_de_repeticion hn h hlt heq.symm⟩

/-- Una órbita que llega a 1 queda acotada: no es una fuga. -/
theorem llega_no_fuga {n : ℕ} (h : LlegaT n) : ¬ Fuga n := by
  obtain ⟨k, hk⟩ := h
  intro hf
  obtain ⟨j, hj⟩ := hf ((Finset.range (k + 1)).sum (fun i => T^[i] n) + 2)
  rcases le_or_gt j k with hjk | hjk
  · have hs : T^[j] n ≤ (Finset.range (k + 1)).sum (fun i => T^[i] n) :=
      Finset.single_le_sum (f := fun i => T^[i] n) (fun i _ => Nat.zero_le _)
        (Finset.mem_range.2 (by omega))
    omega
  · have he : T^[j] n = T^[j - k] 1 := by
      rw [← hk, ← Function.iterate_add_apply, Nat.sub_add_cancel hjk.le]
    have := iter_uno (j - k)
    omega

/-! ## Qué frena cada muro -/

/-- Si el pronóstico baja de 1 alguna vez, hay un primer cruce. -/
theorem primerCruce_de_cruza {n : ℕ} (h : Cruza n) : ∃ k, PrimerCruce n k := by
  classical
  refine ⟨Nat.find h, ?_, Nat.find_spec h⟩
  intro j hj _
  exact not_lt.mp (Nat.find_min h hj)

theorem primerCruce_pos {n k : ℕ} (hk : PrimerCruce n k) : 1 ≤ k := by
  rcases Nat.eq_zero_or_pos k with h0 | h0
  · subst h0
    have h2 := hk.2
    simp [S] at h2
  · exact h0

/-- 3^a nunca es igual a 2^p con p ≥ 1. -/
theorem tres_ne_dos {a p : ℕ} (hp : 1 ≤ p) : 3 ^ a ≠ 2 ^ p := by
  have h3 : 3 ^ a % 2 = 1 := by
    rw [Nat.pow_mod]
    norm_num
  have h2 : 2 ^ p % 2 = 0 := by
    obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
    rw [pow_succ]
    simp
  omega

/-- El muro A, por sí solo, excluye los circuitos: el menor valor de un circuito tiene
    pronóstico que baja de 1 en un periodo, pero nunca baja de sí mismo. -/
theorem muroA_sin_circuitos (hA : MuroA) (x : ℕ) : ¬ Circuito x := by
  classical
  rintro ⟨hx1, ⟨p, hp1, hpx⟩, hno1⟩
  have hex : ∃ v, ∃ j, T^[j] x = v := ⟨x, 0, rfl⟩
  obtain ⟨j0, hj0⟩ := Nat.find_spec hex
  have hmin : ∀ j, Nat.find hex ≤ T^[j] x := fun j => Nat.find_min' hex ⟨j, rfl⟩
  generalize Nat.find hex = m at hj0 hmin
  have hm1 : 1 ≤ m := hj0 ▸ iter_pos hx1 j0
  have hm2 : 2 ≤ m := by
    have := hno1 j0
    omega
  have horb : ∀ k, m ≤ T^[k] m := by
    intro k
    have h := hmin (k + j0)
    rwa [Function.iterate_add_apply, hj0] at h
  have hmp : T^[p] m = m := by
    rw [← hj0, ← Function.iterate_add_apply, add_comm, Function.iterate_add_apply, hpx]
  have hle : 3 ^ S p m ≤ 2 ^ p := by
    have h := cota_inferior m p
    rw [hmp] at h
    exact Nat.le_of_mul_le_mul_right h (by omega)
  have hcz : Cruza m := ⟨p, lt_of_le_of_ne hle (tres_ne_dos hp1)⟩
  obtain ⟨k, -, hk⟩ := hA m hm2 hcz
  have := horb k
  omega

/-- Una fuga pura nunca baja de su punto de partida. -/
theorem fuga_pura_no_baja {n : ℕ} (h : FugaPura n) (k : ℕ) : n ≤ T^[k] n := by
  apply no_baja
  by_contra hc
  exact h ⟨k, not_le.mp hc⟩

theorem fuga_pura_no_llega {n : ℕ} (hn : 2 ≤ n) (h : FugaPura n) : ¬ LlegaT n := by
  rintro ⟨k, hk⟩
  have := fuga_pura_no_baja h k
  omega

/-- El muro B dice exactamente que no hay fugas puras. -/
theorem muroB_iff : MuroB ↔ ∀ n, 2 ≤ n → ¬ FugaPura n := by
  unfold MuroB FugaPura
  constructor
  · intro h n hn hf
    exact hf (h n hn)
  · intro h n hn
    by_contra hc
    exact h n hn hc

/-- Con los dos muros no queda ni circuito ni fuga. -/
theorem casa_sin_fallas (hA : MuroA) (hB : MuroB) :
    (∀ x, ¬ Circuito x) ∧ ∀ n, ¬ Fuga n := by
  refine ⟨muroA_sin_circuitos hA, fun n hf => ?_⟩
  rcases Nat.eq_zero_or_pos n with h0 | h0
  · subst h0
    obtain ⟨k, hk⟩ := hf 0
    have h00 : T^[k] 0 = 0 := Function.iterate_fixed (by decide) k
    omega
  · exact llega_no_fuga ((collatz_iff_atajo.1 (techo hA hB)) n h0) hf

/-! ## Cómo se levanta el muro A -/

/-- La conjetura CST de Terras levanta el muro A. -/
theorem muroA_de_cst (h : CST) : MuroA := by
  intro n hn hc
  obtain ⟨k, hk⟩ := primerCruce_de_cruza hc
  exact ⟨k, primerCruce_pos hk, h n k hn hk⟩

/-- Un tramo del muro A sale de CST restringida a palabras con a lo sumo `R` rachas. -/
theorem tramo_de_descenso {R : ℕ}
    (h : ∀ n k, 2 ≤ n → PrimerCruce n k → rachas n k ≤ R → T^[k] n < n) :
    MuroAHasta R :=
  fun n k hn hk hr => ⟨k, primerCruce_pos hk, h n k hn hk hr⟩

/-- Todos los tramos juntos levantan el muro A (el «dominó» que falta). -/
theorem muroA_de_tramos (h : ∀ R, MuroAHasta R) : MuroA := by
  intro n hn hc
  obtain ⟨k, hk⟩ := primerCruce_de_cruza hc
  exact h (rachas n k) n k hn hk le_rfl

end CasaPlano

#print axioms CasaPlano.iter_uno
#print axioms CasaPlano.no_baja
#print axioms CasaPlano.llega_iff
#print axioms CasaPlano.collatz_iff_atajo
#print axioms CasaPlano.techo
#print axioms CasaPlano.muros_de_collatz
#print axioms CasaPlano.collatz_iff_muros
#print axioms CasaPlano.dos_fallas
#print axioms CasaPlano.llega_no_fuga
#print axioms CasaPlano.primerCruce_de_cruza
#print axioms CasaPlano.muroA_sin_circuitos
#print axioms CasaPlano.fuga_pura_no_llega
#print axioms CasaPlano.muroB_iff
#print axioms CasaPlano.casa_sin_fallas
#print axioms CasaPlano.muroA_de_cst
#print axioms CasaPlano.tramo_de_descenso
#print axioms CasaPlano.muroA_de_tramos
