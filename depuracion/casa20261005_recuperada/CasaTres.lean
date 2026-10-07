import CasaFugitivo

/-! # El lado 3-ádico de la órbita: primer paso hacia Tao (2019)

Ruta B, 05-10-2026, sin hipótesis externas. La barrera de Korec viene de mirar sólo la
información 2-ádica (`n mod 2^k`). Tao (2019) la salta mirando además `T^k(n) mod 3^j`.
Aquí, la estructura exacta que conecta los dos lados:

* `T_progresion`: `T(c + 2u) = T(c) + 3^(c mod 2) u`;
* `iter_afin`: **identidad afín**, `T^k(r + 2^k t) = T^k(r) + 3^(S_k(r)) t`;
* `tres_determinado`: el residuo de `T^k(n)` módulo `3^(S_k(n))` queda fijado por
  `n mod 2^k`;
* `fibra_inyectiva`: dentro de una clase módulo `2^k`, los `t < 3^(j − S)` dan valores de
  `T^k` distintos módulo `3^j`: la clase recorre sin repetir su fibra 3-ádica;
* `paridad_independiente`: si `m ≤ S_k(r)`, las dos subclases de `r mod 2^k` dan el mismo
  `T^k` módulo `3^m` y paridades opuestas; con `T_mod_tres`, `T^k(r) mod 3^m` sigue una
  cadena de Markov en `ℤ/3^m`;
* `sin_multiplos_de_tres`: después de la primera subida, la órbita nunca vuelve a un
  múltiplo de 3 (`T_impar_mod_tres`: tras una subida el valor es `≡ 2 (mod 3)`).

Lo que falta para Tao es la mezcla fina: que el desplazamiento `T^k(r) mod 3^S`, con `r`
uniforme módulo `2^k`, se reparta casi uniformemente en las fibras. Ver `PERDICES.md`.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaTres

open Ocelotas OcelotasContador CasaPlano CasaFugitivo

/-- Un paso del atajo sobre una progresión de razón par. -/
theorem T_progresion (c u : ℕ) : T (c + 2 * u) = T c + 3 ^ (c % 2) * u := by
  rcases Nat.mod_two_eq_zero_or_one c with h | h
  · have h1 : (c + 2 * u) % 2 = 0 := by omega
    have e1 := T_par h1
    have e2 := T_par h
    rw [h, pow_zero, one_mul]
    omega
  · have h1 : (c + 2 * u) % 2 = 1 := by omega
    have e1 := T_impar h1
    have e2 := T_impar h
    rw [h, pow_one]
    omega

/-- **Identidad afín.** `T^k(r + 2^k t) = T^k(r) + 3^(S_k(r)) t`. -/
theorem iter_afin : ∀ k r t, T^[k] (r + 2 ^ k * t) = T^[k] r + 3 ^ S k r * t
  | 0, r, t => by simp [S]
  | k + 1, r, t => by
    rw [Function.iterate_succ_apply, Function.iterate_succ_apply,
      show r + 2 ^ (k + 1) * t = r + 2 * (2 ^ k * t) by ring, T_progresion,
      show 3 ^ (r % 2) * (2 ^ k * t) = 2 ^ k * (3 ^ (r % 2) * t) by ring, iter_afin k (T r)]
    show T^[k] (T r) + 3 ^ S k (T r) * (3 ^ (r % 2) * t) =
      T^[k] (T r) + 3 ^ (r % 2 + S k (T r)) * t
    rw [pow_add]
    ring

/-- Las subidas no cambian a lo largo de la progresión. -/
theorem S_afin (k r t : ℕ) : S k (r + 2 ^ k * t) = S k r :=
  S_congr k _ _ (Nat.add_mul_mod_self_left r (2 ^ k) t)

/-- **El residuo 3-ádico queda fijado por el 2-ádico.**
    `T^k(n) ≡ T^k(n mod 2^k) (mod 3^(S_k(n)))`. -/
theorem tres_determinado (k n : ℕ) :
    T^[k] n % 3 ^ S k n = T^[k] (n % 2 ^ k) % 3 ^ S k n := by
  have h := iter_afin k (n % 2 ^ k) (n / 2 ^ k)
  rw [Nat.mod_add_div] at h
  rw [h, S_congr k n (n % 2 ^ k) (Nat.mod_modEq n _).symm, Nat.add_mul_mod_self_left]

/-- **La clase recorre su fibra sin repetir.** Si `S_k(r) ≤ j` y `t₁, t₂ < 3^(j − S_k(r))`
    dan el mismo valor de `T^k` módulo `3^j`, entonces `t₁ = t₂`. -/
theorem fibra_inyectiva {k r j t₁ t₂ : ℕ} (hj : S k r ≤ j) (h₁ : t₁ < 3 ^ (j - S k r))
    (h₂ : t₂ < 3 ^ (j - S k r))
    (h : T^[k] (r + 2 ^ k * t₁) % 3 ^ j = T^[k] (r + 2 ^ k * t₂) % 3 ^ j) : t₁ = t₂ := by
  rw [iter_afin, iter_afin] at h
  have hj' : 3 ^ j = 3 ^ S k r * 3 ^ (j - S k r) := by
    rw [← pow_add, Nat.add_sub_cancel' hj]
  have hc : 3 ^ S k r * t₁ ≡ 3 ^ S k r * t₂ [MOD 3 ^ S k r * 3 ^ (j - S k r)] := by
    rw [← hj']
    exact Nat.ModEq.add_left_cancel' _ h
  have hpos : 0 < 3 ^ S k r := by positivity
  have ht := Nat.ModEq.mul_left_cancel' hpos.ne' hc
  unfold Nat.ModEq at ht
  rwa [Nat.mod_eq_of_lt h₁, Nat.mod_eq_of_lt h₂] at ht

/-- Toda la clase cae en la misma fibra módulo `3^(S_k(r))`. -/
theorem fibra_contenida (k r t : ℕ) :
    T^[k] (r + 2 ^ k * t) % 3 ^ S k r = T^[k] r % 3 ^ S k r := by
  rw [iter_afin, Nat.add_mul_mod_self_left]

/-- **Paridad independiente del residuo 3-ádico.** Si `m ≤ S_k(r)`, las dos subclases
    `r` y `r + 2^k` de la clase `r mod 2^k` dan el mismo `T^k` módulo `3^m` y paridades
    opuestas. Por eso, con `r` uniforme, `T^k(r) mod 3^m` sigue la cadena
    `X ↦ X/2` o `X ↦ (3X+1)/2` en `ℤ/3^m` con monedas justas. -/
theorem paridad_independiente {k r m : ℕ} (hm : m ≤ S k r) :
    T^[k] (r + 2 ^ k) % 3 ^ m = T^[k] r % 3 ^ m ∧
      T^[k] (r + 2 ^ k) % 2 ≠ T^[k] r % 2 := by
  have h := iter_afin k r 1
  rw [mul_one, mul_one] at h
  rw [h]
  have hd : 3 ^ m ∣ 3 ^ S k r := pow_dvd_pow 3 hm
  have hodd : 3 ^ S k r % 2 = 1 := Nat.pow_mod 3 (S k r) 2 ▸ by norm_num
  refine ⟨?_, ?_⟩
  · obtain ⟨c, hc⟩ := hd
    rw [hc, Nat.add_mul_mod_self_left]
  · omega

/-- El paso del atajo en `ℤ/3^m`: `2 T(x) ≡ x` o `3x + 1` según la paridad de `x`. -/
theorem T_mod_tres (x m : ℕ) :
    2 * T x % 3 ^ m = (if x % 2 = 0 then x else 3 * x + 1) % 3 ^ m := by
  split
  · rw [T_par (by assumption)]
  · rw [T_impar (by omega)]

/-- Tras una subida, el valor es `≡ 2 (mod 3)`. -/
theorem T_impar_mod_tres {n : ℕ} (h : n % 2 = 1) : T n % 3 = 2 := by
  have := T_impar h
  omega

/-- Sin subidas, `k` pasos sólo dividen por `2^k`. -/
theorem todo_par : ∀ k m, S k m = 0 → 2 ^ k * T^[k] m = m
  | 0, m, _ => by simp
  | k + 1, m, h => by
    have h' : m % 2 + S k (T m) = 0 := h
    have hm : m % 2 = 0 := by omega
    have hk := todo_par k (T m) (by omega)
    have e := T_par hm
    rw [Function.iterate_succ_apply, pow_succ]
    calc 2 ^ k * 2 * T^[k] (T m) = 2 * (2 ^ k * T^[k] (T m)) := by ring
      _ = m := by rw [hk, e]

/-- Dividir por 2 no crea múltiplos de 3. -/
theorem no_tres_de_todo_par {k m : ℕ} (hS : S k m = 0) (hm : m % 3 ≠ 0) :
    T^[k] m % 3 ≠ 0 := by
  intro h3
  have he := todo_par k m hS
  have hdvd : 3 ∣ 2 ^ k * T^[k] m := Dvd.dvd.mul_left (Nat.dvd_of_mod_eq_zero h3) _
  rw [he] at hdvd
  exact hm (Nat.mod_eq_zero_of_dvd hdvd)

/-- **Después de la primera subida, la órbita nunca vuelve a un múltiplo de 3.** -/
theorem sin_multiplos_de_tres : ∀ k n, 1 ≤ S k n → T^[k] n % 3 ≠ 0
  | 0, n, h => by simp [S] at h
  | k + 1, n, h => by
    have h' : n % 2 + S k (T n) ≥ 1 := h
    rw [Function.iterate_succ_apply]
    by_cases hS : 1 ≤ S k (T n)
    · exact sin_multiplos_de_tres k (T n) hS
    · have hS0 : S k (T n) = 0 := by omega
      have hn : n % 2 = 1 := by omega
      exact no_tres_de_todo_par hS0 (by rw [T_impar_mod_tres hn]; norm_num)

end CasaTres

#print axioms CasaTres.T_progresion
#print axioms CasaTres.iter_afin
#print axioms CasaTres.S_afin
#print axioms CasaTres.tres_determinado
#print axioms CasaTres.fibra_inyectiva
#print axioms CasaTres.fibra_contenida
#print axioms CasaTres.paridad_independiente
#print axioms CasaTres.T_mod_tres
#print axioms CasaTres.T_impar_mod_tres
#print axioms CasaTres.todo_par
#print axioms CasaTres.sin_multiplos_de_tres
