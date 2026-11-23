import Mathlib

/-!
# Juguete: Collatz sin acarreos en F2[x]

Mapa de Hicks–Mullen–Yucas–Zavislak (Amer. Math. Monthly 115, 2008):
`T f = f / X` si `X ∣ f`, y `T f = (X + 1) * f + 1` si no. Codificado en
binario, multiplicar por `X + 1` es `n XOR 2n`: es 3n+1 sin acarreos.

Teorema `llega_a_uno`: todo `f ≠ 0` llega a 1 en a lo sumo
`d^2 + 2d` pasos, con `d = natDegree f` (la cota publicada).

La prueba usa dos lemas, separados a propósito:
* `dos_pasos` (racha impar): `T (T (X*h+1)) = (X+1)*h + 1`. Su análogo
  entero, `T n + 1 = 3 (n+1) / 2` para n impar, se transporta sin cambios.
* `natDegree_dos_pasos` (tamaño): el par de pasos impar conserva el grado.
  Aquí está la ausencia de acarreos: en Z, 3 es más grande que 2.
`natDegree_dos_pasos_siete` muestra que con multiplicador `X^2+X+1`
ese mismo par de pasos sube el grado, que es donde la prueba deja de valer.
-/

open Polynomial

namespace JugueteF2x

/-- El mapa de Collatz sin acarreos sobre `F2[x]`. -/
noncomputable def T (f : (ZMod 2)[X]) : (ZMod 2)[X] :=
  if f.coeff 0 = 0 then f.divX else (X + 1) * f + 1

lemma dos_eq_cero : (2 : (ZMod 2)[X]) = 0 := CharTwo.two_eq_zero

lemma uno_de_ne_cero {a : ZMod 2} (h : a ≠ 0) : a = 1 := by
  revert a; decide

lemma T_par {f : (ZMod 2)[X]} (h : f.coeff 0 = 0) : T f = f.divX := by
  simp [T, h]

lemma T_impar {f : (ZMod 2)[X]} (h : f.coeff 0 ≠ 0) : T f = (X + 1) * f + 1 := by
  simp [T, h]

lemma divX_X_mul' (p : (ZMod 2)[X]) : (X * p).divX = p := by
  ext n
  simp [coeff_divX, coeff_X_mul]

/-- Descomposición de un polinomio impar: `f = X * divX f + 1`. -/
lemma impar_eq {f : (ZMod 2)[X]} (h : f.coeff 0 ≠ 0) : f = X * f.divX + 1 := by
  have := divX_mul_X_add f
  rw [uno_de_ne_cero h, C_1, mul_comm] at this
  exact this.symm

/-- Descomposición de un polinomio par: `f = X * divX f`. -/
lemma par_eq {f : (ZMod 2)[X]} (h : f.coeff 0 = 0) : f = X * f.divX := by
  have := divX_mul_X_add f
  rw [h, C_0, add_zero, mul_comm] at this
  exact this.symm

/-- (L1) Racha impar: dos pasos sobre `X*h+1` dan `(X+1)*h+1`. -/
lemma dos_pasos (h : (ZMod 2)[X]) : T (T (X * h + 1)) = (X + 1) * h + 1 := by
  have h1 : (X * h + 1).coeff 0 ≠ 0 := by simp
  have e : (X + 1) * (X * h + 1) + 1 = X * ((X + 1) * h + 1) := by
    linear_combination dos_eq_cero
  rw [T_impar h1, e]
  have h2 : (X * ((X + 1) * h + 1)).coeff 0 = 0 := by simp
  rw [T_par h2, divX_X_mul']

lemma natDegree_X_add_uno : (X + 1 : (ZMod 2)[X]).natDegree = 1 := by
  rw [show (X + 1 : (ZMod 2)[X]) = X + C 1 by simp]
  exact natDegree_X_add_C 1

lemma X_add_uno_ne_cero : (X + 1 : (ZMod 2)[X]) ≠ 0 := by
  intro h
  have := natDegree_X_add_uno
  rw [h, natDegree_zero] at this
  exact absurd this (by norm_num)

/-- (L2) Tamaño: `(X+1)*h+1` tiene grado `natDegree h + 1`. -/
lemma natDegree_dos_pasos {h : (ZMod 2)[X]} (hh : h ≠ 0) :
    ((X + 1) * h + 1).natDegree = h.natDegree + 1 := by
  have hm : ((X + 1) * h).natDegree = h.natDegree + 1 := by
    rw [natDegree_mul X_add_uno_ne_cero hh, natDegree_X_add_uno, add_comm]
  rw [natDegree_add_eq_left_of_natDegree_lt (by rw [hm, natDegree_one]; omega), hm]

lemma divX_ne_cero {p : (ZMod 2)[X]} (hp : 1 ≤ p.natDegree) : p.divX ≠ 0 := by
  intro h
  have := natDegree_divX_eq_natDegree_tsub_one (p := p)
  rw [h, natDegree_zero] at this
  have hc : p = C (p.coeff 0) := by
    have := divX_mul_X_add p
    rw [h, zero_mul, zero_add] at this
    exact this.symm
  rw [hc, natDegree_C] at hp
  omega

lemma coeff_cero_ne_de_trailing {h : (ZMod 2)[X]} (hh : h ≠ 0)
    (ht : h.natTrailingDegree = 0) : h.coeff 0 ≠ 0 := by
  have := trailingCoeff_nonzero_iff_nonzero.mpr hh
  rwa [trailingCoeff, ht] at this

/-- La racha impar termina: desde `X*h+1` se llega, en a lo sumo
`2 * natTrailingDegree h + 3` pasos, a un polinomio no nulo de grado
`natDegree h`, uno menos que el de partida. -/
lemma corrida : ∀ n (h : (ZMod 2)[X]), h ≠ 0 → h.natTrailingDegree = n →
    ∃ j ≤ 2 * n + 3, T^[j] (X * h + 1) ≠ 0 ∧
      (T^[j] (X * h + 1)).natDegree = h.natDegree := by
  intro n
  induction n with
  | zero =>
    intro h hh ht
    have hc := coeff_cero_ne_de_trailing hh ht
    set p := (X + 1) * h + 1 with hp
    have hp0 : p.coeff 0 = 0 := by
      simp only [hp, coeff_add, mul_coeff_zero, coeff_one_zero, coeff_X_zero,
        zero_add, one_mul, uno_de_ne_cero hc]
      decide
    have hdeg : p.natDegree = h.natDegree + 1 := natDegree_dos_pasos hh
    refine ⟨3, le_refl _, ?_, ?_⟩
    · rw [show (3 : ℕ) = 1 + 2 from rfl, Function.iterate_add_apply]
      simp only [Function.iterate_succ, Function.iterate_zero, Function.comp_apply,
        id_eq, dos_pasos, ← hp, T_par hp0]
      exact divX_ne_cero (by omega)
    · rw [show (3 : ℕ) = 1 + 2 from rfl, Function.iterate_add_apply]
      simp only [Function.iterate_succ, Function.iterate_zero, Function.comp_apply,
        id_eq, dos_pasos, ← hp, T_par hp0]
      rw [natDegree_divX_eq_natDegree_tsub_one, hdeg]
      omega
  | succ n ih =>
    intro h hh ht
    have hc : h.coeff 0 = 0 := by
      by_contra hc
      have : h.natTrailingDegree = 0 :=
        natTrailingDegree_eq_zero.mpr (Or.inr hc)
      omega
    set h₁ := h.divX with hh₁
    have eh : h = X * h₁ := par_eq hc
    have h₁0 : h₁ ≠ 0 := by
      intro e
      rw [e, mul_zero] at eh
      exact hh eh
    set g := (X + 1) * h₁ with hg
    have g0 : g ≠ 0 := mul_ne_zero X_add_uno_ne_cero h₁0
    have tg : g.natTrailingDegree = n := by
      have t1 : h.natTrailingDegree = h₁.natTrailingDegree + 1 := by
        rw [eh, natTrailingDegree_mul X_ne_zero h₁0, natTrailingDegree_X, add_comm]
      have t2 : g.natTrailingDegree = h₁.natTrailingDegree := by
        rw [hg, natTrailingDegree_mul X_add_uno_ne_cero h₁0,
          natTrailingDegree_eq_zero.mpr (Or.inr (by simp)), zero_add]
      omega
    have dg : g.natDegree = h.natDegree := by
      rw [eh, hg, natDegree_mul X_add_uno_ne_cero h₁0, natDegree_mul X_ne_zero h₁0,
        natDegree_X_add_uno, natDegree_X]
    have e2 : T^[2] (X * h + 1) = X * g + 1 := by
      simp only [Function.iterate_succ, Function.iterate_zero, Function.comp_apply,
        id_eq, dos_pasos]
      rw [eh, hg]
      ring
    obtain ⟨j, hj, hne, hdeg⟩ := ih g g0 tg
    refine ⟨j + 2, by omega, ?_, ?_⟩
    · rwa [Function.iterate_add_apply, e2]
    · rw [Function.iterate_add_apply, e2, hdeg, dg]

/-- Desde un polinomio no nulo de grado `d+1` se baja a grado `d` en a lo
sumo `2d + 3` pasos. -/
lemma baja (d : ℕ) (f : (ZMod 2)[X]) (hd : f.natDegree = d + 1) :
    ∃ j ≤ 2 * d + 3, T^[j] f ≠ 0 ∧ (T^[j] f).natDegree = d := by
  by_cases hc : f.coeff 0 = 0
  · refine ⟨1, by omega, ?_, ?_⟩
    · simp only [Function.iterate_one, T_par hc]
      exact divX_ne_cero (by omega)
    · simp only [Function.iterate_one, T_par hc]
      rw [natDegree_divX_eq_natDegree_tsub_one, hd]
      rfl
  · have ef := impar_eq hc
    set h := f.divX with hh
    have dh : h.natDegree = d := by
      rw [hh, natDegree_divX_eq_natDegree_tsub_one, hd]
      rfl
    have h0 : h ≠ 0 := divX_ne_cero (by omega)
    obtain ⟨j, hj, hne, hdeg⟩ := corrida _ h h0 rfl
    have ht : h.natTrailingDegree ≤ d := dh ▸ natTrailingDegree_le_natDegree h
    refine ⟨j, by omega, ?_, ?_⟩
    · rwa [ef]
    · rw [ef, hdeg, dh]

lemma grado_cero {f : (ZMod 2)[X]} (hf : f ≠ 0) (hd : f.natDegree = 0) : f = 1 := by
  rw [eq_C_of_natDegree_eq_zero hd]
  have hc : f.coeff 0 ≠ 0 := by
    intro h
    apply hf
    rw [eq_C_of_natDegree_eq_zero hd, h, C_0]
  rw [uno_de_ne_cero hc, C_1]

/-- **Teorema del juguete.** Todo polinomio no nulo de `F2[x]` llega a 1
bajo `T`, en a lo sumo `d^2 + 2d` pasos, con `d` su grado. -/
theorem llega_a_uno (f : (ZMod 2)[X]) (hf : f ≠ 0) :
    ∃ k ≤ f.natDegree ^ 2 + 2 * f.natDegree, T^[k] f = 1 := by
  suffices H : ∀ d (f : (ZMod 2)[X]), f ≠ 0 → f.natDegree = d →
      ∃ k ≤ d ^ 2 + 2 * d, T^[k] f = 1 from H _ f hf rfl
  intro d
  induction d with
  | zero =>
    intro f hf hd
    exact ⟨0, le_refl _, grado_cero hf hd⟩
  | succ d ih =>
    intro f hf hd
    obtain ⟨j, hj, hne, hdeg⟩ := baja d f hd
    obtain ⟨k, hk, hk1⟩ := ih _ hne hdeg
    refine ⟨k + j, by nlinarith, ?_⟩
    rw [Function.iterate_add_apply, hk1]

/-! ## Dónde deja de valer: multiplicador `X^2 + X + 1` (7n sin acarreos) -/

/-- Mapa con multiplicador `X^2 + X + 1`. -/
noncomputable def T7 (f : (ZMod 2)[X]) : (ZMod 2)[X] :=
  if f.coeff 0 = 0 then f.divX else (X ^ 2 + X + 1) * f + 1

lemma natDegree_X2_X_uno : (X ^ 2 + X + 1 : (ZMod 2)[X]).natDegree = 2 := by
  compute_degree!

/-- Con `X^2+X+1`, el par de pasos impar sube el grado en uno: el análogo
de `L2` falla, y con él la prueba. -/
lemma natDegree_dos_pasos_siete {f : (ZMod 2)[X]} (hf : f.coeff 0 ≠ 0) :
    (T7 (T7 f)).natDegree = f.natDegree + 1 := by
  have f0 : f ≠ 0 := fun e => hf (by rw [e, coeff_zero])
  have m0 : (X ^ 2 + X + 1 : (ZMod 2)[X]) ≠ 0 := by
    intro e
    have := natDegree_X2_X_uno
    rw [e, natDegree_zero] at this
    exact absurd this (by norm_num)
  set p := (X ^ 2 + X + 1) * f + 1 with hp
  have h1 : T7 f = p := by simp [T7, hf, hp]
  have hm : ((X ^ 2 + X + 1) * f).natDegree = f.natDegree + 2 := by
    rw [natDegree_mul m0 f0, natDegree_X2_X_uno, add_comm]
  have dp : p.natDegree = f.natDegree + 2 := by
    rw [hp, natDegree_add_eq_left_of_natDegree_lt (by rw [hm, natDegree_one]; omega), hm]
  have p0 : p.coeff 0 = 0 := by
    simp only [hp, coeff_add, mul_coeff_zero, coeff_one_zero, coeff_X_zero,
      coeff_X_pow, coeff_add, uno_de_ne_cero hf]
    decide
  rw [h1]
  simp only [T7, p0, if_true]
  rw [natDegree_divX_eq_natDegree_tsub_one, dp]
  omega

/-! ## L1 en los enteros: la racha impar se transporta

Atajo clásico `Tz n = n/2` o `(3n+1)/2`. La racha desde `2^k a - 1` es la
misma que desde `X^k a + 1` en F2[x]; la diferencia es el tamaño final:
`3^k a` frente a `(X+1)^k a`, que tiene el grado de `X^k a`. -/

/-- Atajo de Collatz en los naturales. -/
def Tz (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

lemma Tz_impar {m : ℕ} (hm : 1 ≤ m) : Tz (2 * m - 1) = 3 * m - 1 := by
  unfold Tz
  split_ifs with h <;> omega

lemma racha_entera : ∀ k a : ℕ, 1 ≤ a → Tz^[k] (2 ^ k * a - 1) + 1 = 3 ^ k * a := by
  intro k
  induction k with
  | zero => intro a ha; simp; omega
  | succ k ih =>
    intro a ha
    have hpos : 1 ≤ 2 ^ k * a := Nat.one_le_iff_ne_zero.mpr (by positivity)
    rw [Function.iterate_succ_apply, pow_succ, mul_comm (2 ^ k) 2, mul_assoc,
      Tz_impar hpos, show 3 * (2 ^ k * a) = 2 ^ k * (3 * a) by ring,
      ih (3 * a) (by omega), pow_succ]
    ring

end JugueteF2x

#print axioms JugueteF2x.llega_a_uno
#print axioms JugueteF2x.natDegree_dos_pasos_siete
#print axioms JugueteF2x.racha_entera
