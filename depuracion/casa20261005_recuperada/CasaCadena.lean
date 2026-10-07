import CasaTres

/-! # La ley exacta de `T^k(r) mod 3^m`: una cadena de Markov en `ℤ/3^m`

Ruta B, 05-10-2026, sin hipótesis externas. Completa el puente 3-ádico de `CasaTres`
(nota `PERDICES.md`) con el enunciado exacto que allí estaba sólo en palabras:

* `cadena_correcta`: `T^k(n) mod 3^m` es la cadena `X ↦ X/2` o `X ↦ (3X+1)/2` en `ℤ/3^m`
  (dividir por 2 es multiplicar por `(3^m+1)/2`), seguida a lo largo de la palabra de
  paridades de `n` y empezada en `n mod 3^m`;
* `palabra_congr`, `congr_de_palabra`, `palabra_sobre`: la palabra de los `k` primeros
  pasos depende sólo de `n mod 2^k`, la determina, y toda palabra de longitud `k` aparece:
  `c ↦ palabra k c` es una biyección de `[0, 2^k)` en las palabras de longitud `k`;
* `ley_de_la_cadena`: para `r` uniforme en `[0, 2^k 3^m)`, `T^k(r) mod 3^m` tiene
  exactamente la ley de la cadena con palabra uniforme y punto de partida uniforme.

Lo que falta para Tao es la mezcla fina de esa cadena (`PERDICES.md`).

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaCadena

open Ocelotas OcelotasContador CasaPlano CasaFugitivo CasaTres

/-- Inverso de 2 módulo `3^m`. -/
def medio (m : ℕ) : ℕ := (3 ^ m + 1) / 2

theorem dos_medio (m : ℕ) : 2 * medio m = 3 ^ m + 1 := by
  have h : 3 ^ m % 2 = 1 := by
    rw [Nat.pow_mod]
    norm_num
  unfold medio
  omega

/-- Un paso de la cadena en `ℤ/3^m`: `x/2` con el bit falso, `(3x+1)/2` con el verdadero. -/
def paso (m : ℕ) (b : Bool) (x : ℕ) : ℕ := (if b then 3 * x + 1 else x) * medio m % 3 ^ m

/-- La cadena que sigue una palabra de bits. -/
def cadena (m : ℕ) : List Bool → ℕ → ℕ
  | [], x => x % 3 ^ m
  | b :: w, x => cadena m w (paso m b x)

/-- La palabra de paridades de los `k` primeros pasos de `n`. -/
def palabra : ℕ → ℕ → List Bool
  | 0, _ => []
  | k + 1, n => decide (n % 2 = 1) :: palabra k (T n)

theorem palabra_longitud : ∀ k n, (palabra k n).length = k
  | 0, _ => rfl
  | k + 1, n => by simp [palabra, palabra_longitud k (T n)]

theorem paso_T (m n : ℕ) : paso m (decide (n % 2 = 1)) n = T n % 3 ^ m := by
  have h2 : (if decide (n % 2 = 1) then 3 * n + 1 else n) = 2 * T n := by
    rcases Nat.mod_two_eq_zero_or_one n with h | h
    · rw [T_par h]
      simp [h]
    · rw [T_impar h]
      simp [h]
  unfold paso
  rw [h2]
  calc 2 * T n * medio m % 3 ^ m = (T n + 3 ^ m * T n) % 3 ^ m := by
        congr 1
        rw [mul_comm 2 (T n), mul_assoc, dos_medio]
        ring
    _ = T n % 3 ^ m := Nat.add_mul_mod_self_left _ _ _

theorem paso_mod (m : ℕ) (b : Bool) (x : ℕ) : paso m b (x % 3 ^ m) = paso m b x := by
  have hx : x % 3 ^ m ≡ x [MOD 3 ^ m] := Nat.mod_modEq x _
  cases b
  · exact hx.mul_right (medio m)
  · exact ((hx.mul_left 3).add_right 1).mul_right (medio m)

theorem cadena_mod (m : ℕ) : ∀ (w : List Bool) (x : ℕ), cadena m w (x % 3 ^ m) = cadena m w x
  | [], x => Nat.mod_mod _ _
  | b :: w, x => by
    show cadena m w (paso m b (x % 3 ^ m)) = cadena m w (paso m b x)
    rw [paso_mod]

/-- **La cadena describe la órbita módulo `3^m`.** -/
theorem cadena_correcta (m : ℕ) : ∀ k n, T^[k] n % 3 ^ m = cadena m (palabra k n) n
  | 0, _ => rfl
  | k + 1, n => by
    rw [Function.iterate_succ_apply, cadena_correcta m k (T n)]
    show cadena m (palabra k (T n)) (T n) =
      cadena m (palabra k (T n)) (paso m (decide (n % 2 = 1)) n)
    rw [paso_T, cadena_mod]

/-- La palabra depende sólo de `n mod 2^k`. -/
theorem palabra_congr : ∀ k x y, x ≡ y [MOD 2 ^ k] → palabra k x = palabra k y
  | 0, _, _, _ => rfl
  | k + 1, x, y, h => by
    obtain ⟨h1, h2⟩ := T_congr h
    show decide (x % 2 = 1) :: palabra k (T x) = decide (y % 2 = 1) :: palabra k (T y)
    rw [h2, palabra_congr k _ _ h1]

/-- La palabra determina `n mod 2^k`. -/
theorem congr_de_palabra : ∀ k x y, palabra k x = palabra k y → x ≡ y [MOD 2 ^ k]
  | 0, _, _, _ => by simp [Nat.ModEq, Nat.mod_one]
  | k + 1, x, y, h => by
    have h' : decide (x % 2 = 1) :: palabra k (T x) =
        decide (y % 2 = 1) :: palabra k (T y) := h
    obtain ⟨h0, hw⟩ := List.cons.inj h'
    have hT := congr_de_palabra k (T x) (T y) hw
    have hp : x % 2 = y % 2 := by
      rcases Nat.mod_two_eq_zero_or_one x with hx | hx <;>
        rcases Nat.mod_two_eq_zero_or_one y with hy | hy <;> simp_all
    have h2 : 2 * T x ≡ 2 * T y [MOD 2 ^ (k + 1)] := by
      have := Nat.ModEq.mul_left' 2 hT
      rwa [show 2 * 2 ^ k = 2 ^ (k + 1) by ring] at this
    rcases Nat.mod_two_eq_zero_or_one x with hx | hx
    · have hy : y % 2 = 0 := by omega
      rwa [T_par hx, T_par hy] at h2
    · have hy : y % 2 = 1 := by omega
      rw [T_impar hx, T_impar hy] at h2
      exact Nat.ModEq.cancel_left_of_coprime (coprimo_tres (k + 1))
        (Nat.ModEq.add_right_cancel' 1 h2)

/-- `s ↦ 3s + 2` recorre todos los residuos módulo `2^k`. -/
theorem tres_mas_dos_sobre (k c : ℕ) (hc : c < 2 ^ k) : ∃ s, s < 2 ^ k ∧ (3 * s + 2) % 2 ^ k = c := by
  have hN : 0 < 2 ^ k := by positivity
  have hinj : Set.InjOn (fun s => (3 * s + 2) % 2 ^ k) ↑(Finset.range (2 ^ k)) := by
    intro a ha b hb hab
    simp only [Finset.coe_range, Set.mem_Iio] at ha hb
    have h1 : 3 * a + 2 ≡ 3 * b + 2 [MOD 2 ^ k] := hab
    have h3 : a ≡ b [MOD 2 ^ k] :=
      Nat.ModEq.cancel_left_of_coprime (coprimo_tres k) (Nat.ModEq.add_right_cancel' 2 h1)
    unfold Nat.ModEq at h3
    rwa [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at h3
  have himg : (Finset.range (2 ^ k)).image (fun s => (3 * s + 2) % 2 ^ k) =
      Finset.range (2 ^ k) := by
    apply Finset.eq_of_subset_of_card_le
    · intro y hy
      simp only [Finset.mem_image] at hy
      obtain ⟨s, -, rfl⟩ := hy
      exact Finset.mem_range.2 (Nat.mod_lt _ hN)
    · rw [Finset.card_image_of_injOn hinj]
  have hmem : c ∈ (Finset.range (2 ^ k)).image (fun s => (3 * s + 2) % 2 ^ k) := by
    rw [himg]
    exact Finset.mem_range.2 hc
  obtain ⟨s, hs, hsc⟩ := Finset.mem_image.1 hmem
  exact ⟨s, Finset.mem_range.1 hs, hsc⟩

/-- **Toda palabra aparece.** Para cada palabra `w` de longitud `k` hay `c < 2^k` con
    `palabra k c = w`. -/
theorem palabra_sobre : ∀ (k : ℕ) (w : List Bool), w.length = k → ∃ c, c < 2 ^ k ∧ palabra k c = w
  | 0, w, h => ⟨0, by norm_num, by rw [List.length_eq_zero_iff.1 h]; rfl⟩
  | k + 1, [], h => by simp at h
  | k + 1, b :: w, h => by
    have hw : w.length = k := by simpa using h
    obtain ⟨c', hc', hpal⟩ := palabra_sobre k w hw
    cases b
    · refine ⟨2 * c', by rw [pow_succ]; omega, ?_⟩
      show decide ((2 * c') % 2 = 1) :: palabra k (T (2 * c')) = false :: w
      rw [T_dos, hpal]
      simp
    · obtain ⟨s, hs, hsc⟩ := tres_mas_dos_sobre k c' hc'
      refine ⟨2 * s + 1, by rw [pow_succ]; omega, ?_⟩
      show decide ((2 * s + 1) % 2 = 1) :: palabra k (T (2 * s + 1)) = true :: w
      rw [T_dos_uno, palabra_congr k (3 * s + 2) c' (by
        unfold Nat.ModEq
        rw [hsc, Nat.mod_eq_of_lt hc']), hpal]
      simp

/-- La palabra es inyectiva en `[0, 2^k)`. -/
theorem palabra_inyectiva {k x y : ℕ} (hx : x < 2 ^ k) (hy : y < 2 ^ k)
    (h : palabra k x = palabra k y) : x = y := by
  have := congr_de_palabra k x y h
  unfold Nat.ModEq at this
  rwa [Nat.mod_eq_of_lt hx, Nat.mod_eq_of_lt hy] at this

/-- Coordenadas 2-ádica y 3-ádica de `r`. -/
def coordenadas (k m r : ℕ) : ℕ × ℕ := (r % 2 ^ k, r % 3 ^ m)

theorem coordenadas_inyectivas (k m : ℕ) :
    Set.InjOn (coordenadas k m) ↑(Finset.range (2 ^ k * 3 ^ m)) := by
  intro a ha b hb hab
  simp only [Finset.coe_range, Set.mem_Iio] at ha hb
  have h1 : a % 2 ^ k = b % 2 ^ k := congrArg Prod.fst hab
  have h2 : a % 3 ^ m = b % 3 ^ m := congrArg Prod.snd hab
  have hcop : Nat.Coprime (2 ^ k) (3 ^ m) := Nat.Coprime.pow k m (by decide)
  have h3 : a ≡ b [MOD 2 ^ k * 3 ^ m] :=
    (Nat.modEq_and_modEq_iff_modEq_mul hcop).1 ⟨h1, h2⟩
  unfold Nat.ModEq at h3
  rwa [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at h3

/-- **Ley exacta de la cadena.** Para `r` uniforme en `[0, 2^k 3^m)`, `T^k(r) mod 3^m` tiene
    la ley de `cadena m (palabra k c) x` con `(c, x)` uniforme en `[0, 2^k) × [0, 3^m)`;
    por `palabra_sobre` y `palabra_inyectiva`, la palabra `palabra k c` es uniforme entre
    las `2^k` palabras de longitud `k`. -/
theorem ley_de_la_cadena (k m y : ℕ) :
    ((Finset.range (2 ^ k * 3 ^ m)).filter fun r => T^[k] r % 3 ^ m = y).card =
      ((Finset.range (2 ^ k) ×ˢ Finset.range (3 ^ m)).filter
        fun p => cadena m (palabra k p.1) p.2 = y).card := by
  have hinj := coordenadas_inyectivas k m
  have himg : (Finset.range (2 ^ k * 3 ^ m)).image (coordenadas k m) =
      Finset.range (2 ^ k) ×ˢ Finset.range (3 ^ m) := by
    apply Finset.eq_of_subset_of_card_le
    · intro p hp
      simp only [Finset.mem_image] at hp
      obtain ⟨r, -, rfl⟩ := hp
      simp only [coordenadas, Finset.mem_product, Finset.mem_range]
      exact ⟨Nat.mod_lt _ (by positivity), Nat.mod_lt _ (by positivity)⟩
    · rw [Finset.card_image_of_injOn hinj, Finset.card_product, Finset.card_range,
        Finset.card_range, Finset.card_range]
  have hP : ∀ r ∈ Finset.range (2 ^ k * 3 ^ m), (T^[k] r % 3 ^ m = y) ↔
      (cadena m (palabra k (coordenadas k m r).1) (coordenadas k m r).2 = y) := by
    intro r _
    show (T^[k] r % 3 ^ m = y) ↔ (cadena m (palabra k (r % 2 ^ k)) (r % 3 ^ m) = y)
    rw [cadena_correcta, cadena_mod, palabra_congr k (r % 2 ^ k) r (Nat.mod_modEq r _)]
  rw [← himg, Finset.filter_image,
    Finset.card_image_of_injOn (hinj.mono (Finset.coe_subset.2 (Finset.filter_subset _ _)))]
  exact congrArg Finset.card (Finset.filter_congr hP)

end CasaCadena

#print axioms CasaCadena.dos_medio
#print axioms CasaCadena.paso_T
#print axioms CasaCadena.cadena_mod
#print axioms CasaCadena.cadena_correcta
#print axioms CasaCadena.palabra_congr
#print axioms CasaCadena.congr_de_palabra
#print axioms CasaCadena.palabra_sobre
#print axioms CasaCadena.palabra_inyectiva
#print axioms CasaCadena.coordenadas_inyectivas
#print axioms CasaCadena.ley_de_la_cadena
