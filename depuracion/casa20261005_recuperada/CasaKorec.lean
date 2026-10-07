import CasaCasiTodos
import Mathlib.Data.Nat.Log

/-! # Korec (1994): casi todo número baja por debajo de `n^c` si `c > log 3 / log 4`

Ruta B, 05-10-2026, sin hipótesis externas. Con `k ≈ log₂ n` pasos, un número típico
tiene cerca de `k/2` subidas, y la cota superior de Terras da
`T^k(n) ≲ 3^(k/2) n / 2^k ≈ n^(log 3 / log 4)`. Aquí se demuestra con enteros:

* `suma_transferencia`: sumar una función de las subidas sobre los residuos módulo
  `2^(K+1)` es sumarla sobre los residuos módulo `2^K`, con y sin una subida más;
* `momento_dos`: `∑_{r < 2^K} (2 S_K(r) − K)² = K 2^K` (varianza binomial);
* `cota_chebyshev`: hay a lo sumo `K 2^K / (2t)²` residuos con `2 S_K(r) ≥ K + 2t`;
* `baja_de_potencia`: si `S_k(n) ≤ s`, `n ≥ 3^(k−s)` y `2^q 3^(s q) n^(q−p) ≤ 2^(k q)`,
  entonces `T^k(n)^q < n^p`;
* `korec`: si `3^q < 4^p` y `p ≤ q`, la proporción de `n < N` cuya órbita nunca baja de
  `n^(p/q)` tiende a 0;
* `korec_cuatro_quintos`, `korec_cerca_del_umbral` y `allouche`: los casos `c = 0,8`,
  `c = 191/241 ≈ 0,79253` (a menos de una diezmilésima del umbral) y `c = 0,87`.

Como `3^q < 4^p` equivale a `p/q > log 3 / log 4` y entre dos reales siempre hay un
racional, `korec` cubre todo exponente real `c > log 3 / log 4`; el enunciado con
potencias reales no se escribe aquí porque los módulos de logaritmos de Mathlib no
están compilados en esta instalación.

Allouche (1979) lo había probado para `c > 3/2 − log 2 / log 3 ≈ 0,869`; queda incluido.
No es Wu 1: bajar de `n^c` una vez no garantiza llegar a 1.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaKorec

open Ocelotas OcelotasContador CasaPlano CasaFugitivo CasaCasiTodos

/-! ## La distribución de las subidas -/

/-- Transferencia de un paso: los residuos módulo `2^(K+1)` son `2s` (sin subida) y
    `2s+1` (una subida y después `3s+2`, que recorre todos los residuos módulo `2^K`). -/
theorem suma_transferencia (f : ℕ → ℝ) (K : ℕ) :
    ∑ r ∈ Finset.range (2 ^ (K + 1)), f (S (K + 1) r) =
      ∑ r ∈ Finset.range (2 ^ K), (f (S K r) + f (S K r + 1)) := by
  have hpar : ∀ s, S (K + 1) (2 * s) = S K s := by
    intro s
    show (2 * s) % 2 + S K (T (2 * s)) = S K s
    rw [T_dos]
    omega
  have himp : ∀ s, S (K + 1) (2 * s + 1) = S K (3 * s + 2) + 1 := by
    intro s
    show (2 * s + 1) % 2 + S K (T (2 * s + 1)) = S K (3 * s + 2) + 1
    rw [T_dos_uno]
    omega
  rw [pow_succ', suma_pares_impares]
  simp only [hpar, himp]
  rw [suma_permutada K (fun r => f (S K r + 1))
    (fun a b hab => by rw [S_congr K a b hab]), Finset.sum_add_distrib]

/-- Segundo momento de las subidas: `∑_{r < 2^K} (2 S_K(r) − K)² = K 2^K`. -/
theorem momento_dos (K : ℕ) :
    ∑ r ∈ Finset.range (2 ^ K), (2 * (S K r : ℝ) - K) ^ 2 = (K : ℝ) * 2 ^ K := by
  induction K with
  | zero => simp [S]
  | succ K ih =>
    calc ∑ r ∈ Finset.range (2 ^ (K + 1)), (2 * (S (K + 1) r : ℝ) - ((K + 1 : ℕ) : ℝ)) ^ 2
        = ∑ r ∈ Finset.range (2 ^ K), ((2 * (S K r : ℝ) - ((K + 1 : ℕ) : ℝ)) ^ 2 +
            (2 * ((S K r + 1 : ℕ) : ℝ) - ((K + 1 : ℕ) : ℝ)) ^ 2) :=
          suma_transferencia (fun i => (2 * (i : ℝ) - ((K + 1 : ℕ) : ℝ)) ^ 2) K
      _ = ∑ r ∈ Finset.range (2 ^ K), (2 * (2 * (S K r : ℝ) - K) ^ 2 + 2) :=
          Finset.sum_congr rfl fun r _ => by push_cast; ring
      _ = 2 * ∑ r ∈ Finset.range (2 ^ K), (2 * (S K r : ℝ) - K) ^ 2 + 2 * 2 ^ K := by
          rw [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_range,
            nsmul_eq_mul]
          push_cast
          ring
      _ = ((K + 1 : ℕ) : ℝ) * 2 ^ (K + 1) := by
          rw [ih]
          push_cast
          ring

/-- Chebyshev: a lo sumo `K 2^K / (2t)²` residuos tienen `2 S_K(r) ≥ K + 2t`. -/
theorem cota_chebyshev (K t : ℕ) :
    (((Finset.range (2 ^ K)).filter fun r => K + 2 * t ≤ 2 * S K r).card : ℝ) * (2 * t) ^ 2 ≤
      K * 2 ^ K := by
  rw [← momento_dos K]
  calc (((Finset.range (2 ^ K)).filter fun r => K + 2 * t ≤ 2 * S K r).card : ℝ) * (2 * t) ^ 2
      = ∑ r ∈ (Finset.range (2 ^ K)).filter (fun r => K + 2 * t ≤ 2 * S K r),
          (2 * (t : ℝ)) ^ 2 := by
        rw [Finset.sum_const, nsmul_eq_mul]
    _ ≤ ∑ r ∈ (Finset.range (2 ^ K)).filter (fun r => K + 2 * t ≤ 2 * S K r),
          (2 * (S K r : ℝ) - K) ^ 2 := by
        apply Finset.sum_le_sum
        intro r hr
        have h : (K : ℝ) + 2 * t ≤ 2 * S K r := by exact_mod_cast (Finset.mem_filter.1 hr).2
        have h0 : (0 : ℝ) ≤ 2 * t := by positivity
        nlinarith
    _ ≤ ∑ r ∈ Finset.range (2 ^ K), (2 * (S K r : ℝ) - K) ^ 2 :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          fun _ _ _ => sq_nonneg _

/-- Residuos módulo `2^k` con más de `s` subidas en `k` pasos. -/
def muchasSubidas (k s : ℕ) : Finset ℕ := (Finset.range (2 ^ k)).filter fun r => s < S k r

/-- Contar con residuos: `#{n < N : S_k(n) > s} ≤ (N / 2^k + 1) · #muchasSubidas k s`. -/
theorem muchas_por_residuos (N k s : ℕ) :
    ((Finset.range N).filter fun n => s < S k n).card ≤
      (N / 2 ^ k + 1) * (muchasSubidas k s).card := by
  rw [← Finset.card_range (N / 2 ^ k + 1), ← Finset.card_product]
  apply Finset.card_le_card_of_injOn (fun n => (n / 2 ^ k, n % 2 ^ k))
  · intro n hn
    have hn' : n < N ∧ s < S k n := by simpa using hn
    simp only [Finset.coe_product, Set.mem_prod, Finset.mem_coe, Finset.mem_range,
      muchasSubidas, Finset.mem_filter]
    refine ⟨Nat.lt_succ_of_le (Nat.div_le_div_right hn'.1.le), Nat.mod_lt _ (by positivity),
      ?_⟩
    rw [S_congr k _ n (Nat.mod_modEq _ _)]
    exact hn'.2
  · intro a _ b _ hab
    simp only [Prod.mk.injEq] at hab
    rw [← Nat.div_add_mod a (2 ^ k), ← Nat.div_add_mod b (2 ^ k), hab.1, hab.2]

/-- Con `k = 2 (E+1) m` pasos y umbral `s ≥ (E+2) m − 1`: `2 m · #muchasSubidas ≤ (E+1) 2^k`. -/
theorem cota_muchas {k s m E : ℕ} (hm : 1 ≤ m) (hk : k = 2 * (E + 1) * m)
    (hs : k + 2 * m ≤ 2 * s + 2) :
    2 * m * (muchasSubidas k s).card ≤ (E + 1) * 2 ^ k := by
  have hsub : muchasSubidas k s ⊆
      (Finset.range (2 ^ k)).filter fun r => k + 2 * m ≤ 2 * S k r := by
    intro r hr
    rw [muchasSubidas, Finset.mem_filter] at hr
    rw [Finset.mem_filter]
    exact ⟨hr.1, by omega⟩
  have hc : ((Finset.range (2 ^ k)).filter fun r => k + 2 * m ≤ 2 * S k r).card * (2 * m) ^ 2 ≤
      k * 2 ^ k := by
    exact_mod_cast cota_chebyshev k m
  have h1 := le_trans (Nat.mul_le_mul_right ((2 * m) ^ 2) (Finset.card_le_card hsub)) hc
  generalize (muchasSubidas k s).card = c at h1 ⊢
  generalize 2 ^ k = P at h1 ⊢
  subst hk
  have hpos : 0 < 2 * m := by omega
  refine Nat.le_of_mul_le_mul_left ?_ hpos
  calc 2 * m * (2 * m * c) = c * (2 * m) ^ 2 := by ring
    _ ≤ 2 * (E + 1) * m * P := h1
    _ = 2 * m * ((E + 1) * P) := by ring

/-! ## Bajar por debajo de una potencia -/

/-- Si `S_k(n) ≤ s ≤ k`, `n ≥ 3^(k−s)` y `2^q 3^(s q) n^(q−p) ≤ 2^(k q)`, entonces
    `T^k(n)^q < n^p`. -/
theorem baja_de_potencia {n k s p q : ℕ} (hs : S k n ≤ s) (hsk : s ≤ k)
    (hn : 3 ^ (k - s) ≤ n) (hpq : p ≤ q) (hq : q ≠ 0)
    (h : 2 ^ q * 3 ^ (s * q) * n ^ (q - p) ≤ 2 ^ (k * q)) :
    (T^[k] n) ^ q < n ^ p := by
  have hc := cota_superior n k
  have h3 : 3 ^ S k n * n ≤ 3 ^ s * n :=
    Nat.mul_le_mul_right n (Nat.pow_le_pow_right (by norm_num) hs)
  have h3k : 3 ^ k ≤ 3 ^ s * n := by
    calc 3 ^ k = 3 ^ s * 3 ^ (k - s) := by rw [← pow_add, Nat.add_sub_cancel' hsk]
      _ ≤ 3 ^ s * n := Nat.mul_le_mul_left _ hn
  have hp2 : 0 < 2 ^ k := by positivity
  have h1 : 2 ^ k * T^[k] n < 2 * 3 ^ s * n := by
    have : 2 * 3 ^ s * n = 3 ^ s * n + 3 ^ s * n := by ring
    omega
  have h2 := Nat.pow_lt_pow_left h1 hq
  have hnq : n ^ q = n ^ (q - p) * n ^ p := by rw [← pow_add, Nat.sub_add_cancel hpq]
  rw [mul_pow, mul_pow, mul_pow, ← pow_mul, ← pow_mul, hnq] at h2
  have h4 : 2 ^ (k * q) * (T^[k] n) ^ q < 2 ^ (k * q) * n ^ p := by
    calc 2 ^ (k * q) * (T^[k] n) ^ q < 2 ^ q * 3 ^ (s * q) * (n ^ (q - p) * n ^ p) := h2
      _ = 2 ^ q * 3 ^ (s * q) * n ^ (q - p) * n ^ p := by ring
      _ ≤ 2 ^ (k * q) * n ^ p := Nat.mul_le_mul_right _ h
  exact Nat.lt_of_mul_lt_mul_left h4

open Classical in
/-- Números menores que `N` cuya órbita nunca baja de `n^(p/q)`: `n^p ≤ T^j(n)^q` para todo
    `j`. -/
noncomputable def altos (p q N : ℕ) : Finset ℕ :=
  (Finset.range N).filter fun n => ∀ j, n ^ p ≤ (T^[j] n) ^ q

theorem altos_por_residuos {p q N k s : ℕ} (hsk : s ≤ k) (hpq : p ≤ q) (hq : q ≠ 0)
    (h : 2 ^ q * 3 ^ (s * q) * N ^ (q - p) ≤ 2 ^ (k * q)) :
    (altos p q N).card ≤ 3 ^ (k - s) + (N / 2 ^ k + 1) * (muchasSubidas k s).card := by
  classical
  have hsub : altos p q N ⊆ Finset.range (3 ^ (k - s)) ∪
      (Finset.range N).filter fun n => s < S k n := by
    intro n hn
    have hn' : n < N ∧ ∀ j, n ^ p ≤ (T^[j] n) ^ q := by simpa [altos] using hn
    rw [Finset.mem_union, Finset.mem_range, Finset.mem_filter, Finset.mem_range]
    by_cases hk : n < 3 ^ (k - s)
    · exact Or.inl hk
    · refine Or.inr ⟨hn'.1, ?_⟩
      by_contra hS
      have hn2 : 2 ^ q * 3 ^ (s * q) * n ^ (q - p) ≤ 2 ^ (k * q) :=
        le_trans (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hn'.1.le _)) h
      exact absurd (hn'.2 k)
        (not_le.mpr (baja_de_potencia (not_lt.mp hS) hsk (not_lt.mp hk) hpq hq hn2))
  calc (altos p q N).card
      ≤ (Finset.range (3 ^ (k - s)) ∪ (Finset.range N).filter fun n => s < S k n).card :=
        Finset.card_le_card hsub
    _ ≤ (Finset.range (3 ^ (k - s))).card +
          ((Finset.range N).filter fun n => s < S k n).card :=
        Finset.card_union_le _ _
    _ ≤ 3 ^ (k - s) + (N / 2 ^ k + 1) * (muchasSubidas k s).card := by
        rw [Finset.card_range]
        exact Nat.add_le_add_left (muchas_por_residuos N k s) _

/-- La cuenta de Korec: con `k = 2 (E+1) m` pasos y umbral `(E+2) m`,
    `m · #altos ≤ (E+2) N`. -/
theorem korec_cota {p q N E m : ℕ} (hpq : p ≤ q) (hq : q ≠ 0) (hm : 1 ≤ m)
    (hN : 2 ^ (2 * (E + 1) * m) ≤ N)
    (h : 2 ^ q * 3 ^ ((E + 2) * m * q) * N ^ (q - p) ≤ 2 ^ (2 * (E + 1) * m * q)) :
    m * (altos p q N).card ≤ (E + 2) * N := by
  have hks : 2 * (E + 1) * m = (E + 2) * m + E * m := by ring
  have hs2 : (E + 2) * m = E * m + 2 * m := by ring
  have hsk : (E + 2) * m ≤ 2 * (E + 1) * m := by omega
  have hsub : 2 * (E + 1) * m - (E + 2) * m = E * m := by omega
  have hcont := altos_por_residuos hsk hpq hq h
  rw [hsub] at hcont
  have hmuch := cota_muchas (k := 2 * (E + 1) * m) (s := (E + 2) * m) (E := E) hm rfl
    (by omega)
  have hsmall : m * 3 ^ (E * m) ≤ N := by
    have h4 : 2 ^ (2 * (E + 1) * m) = 4 ^ m * 4 ^ (E * m) := by
      rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul, ← pow_mul, ← pow_add]
      congr 1
      ring
    have hm4 : m ≤ 4 ^ m := (Nat.lt_pow_self (by norm_num)).le
    have h34 : 3 ^ (E * m) ≤ 4 ^ (E * m) := Nat.pow_le_pow_left (by norm_num) _
    calc m * 3 ^ (E * m) ≤ 4 ^ m * 4 ^ (E * m) := Nat.mul_le_mul hm4 h34
      _ = 2 ^ (2 * (E + 1) * m) := h4.symm
      _ ≤ N := hN
  generalize 2 * (E + 1) * m = k at hN hcont hmuch
  generalize (muchasSubidas k ((E + 2) * m)).card = c at hcont hmuch
  have hblock : (N / 2 ^ k + 1) * 2 ^ k ≤ 2 * N := by
    have h1 := Nat.div_mul_le_self N (2 ^ k)
    rw [Nat.add_mul, one_mul]
    omega
  have hbad : m * ((N / 2 ^ k + 1) * c) ≤ (E + 1) * N := by
    have h1 : 2 * (m * ((N / 2 ^ k + 1) * c)) ≤ 2 * ((E + 1) * N) := by
      calc 2 * (m * ((N / 2 ^ k + 1) * c)) = (N / 2 ^ k + 1) * (2 * m * c) := by ring
        _ ≤ (N / 2 ^ k + 1) * ((E + 1) * 2 ^ k) := Nat.mul_le_mul_left _ hmuch
        _ = (E + 1) * ((N / 2 ^ k + 1) * 2 ^ k) := by ring
        _ ≤ (E + 1) * (2 * N) := Nat.mul_le_mul_left _ hblock
        _ = 2 * ((E + 1) * N) := by ring
    omega
  calc m * (altos p q N).card ≤ m * (3 ^ (E * m) + (N / 2 ^ k + 1) * c) :=
        Nat.mul_le_mul_left _ hcont
    _ = m * 3 ^ (E * m) + m * ((N / 2 ^ k + 1) * c) := by ring
    _ ≤ N + (E + 1) * N := Nat.add_le_add hsmall hbad
    _ = (E + 2) * N := by ring

/-- Si `A < B`, entonces `C A^m < B^m` para todo `m` suficientemente grande. -/
theorem potencias_ganan {A B : ℕ} (C : ℕ) (h : A < B) :
    ∃ M, ∀ m, M ≤ m → C * A ^ m < B ^ m := by
  have hB : (0 : ℝ) < B := by exact_mod_cast Nat.zero_lt_of_lt h
  have hy0 : (0 : ℝ) ≤ A / B := by positivity
  have hy1 : (A : ℝ) / B < 1 := by
    rw [div_lt_one hB]
    exact_mod_cast h
  obtain ⟨M, hM⟩ := exists_pow_lt_of_lt_one (show (0 : ℝ) < 1 / (C + 1) by positivity) hy1
  refine ⟨M, fun m hm => ?_⟩
  have h1 : ((A : ℝ) / B) ^ m < 1 / (C + 1) :=
    lt_of_le_of_lt (pow_le_pow_of_le_one hy0 hy1.le hm) hM
  have hBm : (0 : ℝ) < (B : ℝ) ^ m := by positivity
  rw [div_pow, div_lt_div_iff₀ hBm (by positivity)] at h1
  have hAm : (0 : ℝ) ≤ (A : ℝ) ^ m := by positivity
  have h2 : ((C * A ^ m : ℕ) : ℝ) < ((B ^ m : ℕ) : ℝ) := by
    push_cast
    nlinarith
  exact_mod_cast h2

/-- La condición de potencias que pide `korec_cota`, a partir de `N < 2^(2(E+1)(m+1))`. -/
theorem condicion {p q E m N : ℕ} (hpq : p ≤ q) (hN : N < 2 ^ (2 * (E + 1) * (m + 1)))
    (hC : 2 ^ q * 2 ^ (2 * (E + 1) * (q - p)) * (3 ^ ((E + 2) * q)) ^ m ≤
      (2 ^ (2 * (E + 1) * p)) ^ m) :
    2 ^ q * 3 ^ ((E + 2) * m * q) * N ^ (q - p) ≤ 2 ^ (2 * (E + 1) * m * q) := by
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le hpq
  rw [Nat.add_sub_cancel_left] at hC ⊢
  have hX : N ^ r ≤ 2 ^ (2 * (E + 1) * r) * 2 ^ (2 * (E + 1) * m * r) := by
    calc N ^ r ≤ (2 ^ (2 * (E + 1) * (m + 1))) ^ r := Nat.pow_le_pow_left hN.le r
      _ = 2 ^ (2 * (E + 1) * r) * 2 ^ (2 * (E + 1) * m * r) := by
          rw [← pow_mul, ← pow_add]
          congr 1
          ring
  have h3 : 3 ^ ((E + 2) * m * (p + r)) = (3 ^ ((E + 2) * (p + r))) ^ m := by
    rw [← pow_mul]
    congr 1
    ring
  have h2 : 2 ^ (2 * (E + 1) * m * (p + r)) =
      (2 ^ (2 * (E + 1) * p)) ^ m * 2 ^ (2 * (E + 1) * m * r) := by
    rw [← pow_mul, ← pow_add]
    congr 1
    ring
  rw [h3, h2]
  calc 2 ^ (p + r) * (3 ^ ((E + 2) * (p + r))) ^ m * N ^ r
      ≤ 2 ^ (p + r) * (3 ^ ((E + 2) * (p + r))) ^ m *
          (2 ^ (2 * (E + 1) * r) * 2 ^ (2 * (E + 1) * m * r)) := Nat.mul_le_mul_left _ hX
    _ = 2 ^ (p + r) * 2 ^ (2 * (E + 1) * r) * (3 ^ ((E + 2) * (p + r))) ^ m *
          2 ^ (2 * (E + 1) * m * r) := by ring
    _ ≤ (2 ^ (2 * (E + 1) * p)) ^ m * 2 ^ (2 * (E + 1) * m * r) := Nat.mul_le_mul_right _ hC

/-- **Korec (1994).** Si `3^q < 4^p` (es decir, `p/q > log 3 / log 4`) y `p ≤ q`, la
    proporción de `n < N` cuya órbita nunca baja de `n^(p/q)` tiende a 0. -/
theorem korec {p q : ℕ} (h34 : 3 ^ q < 4 ^ p) (hpq : p ≤ q) :
    Filter.Tendsto (fun N : ℕ => ((altos p q N).card : ℝ) / N) Filter.atTop (nhds 0) := by
  have hq : q ≠ 0 := by
    rintro rfl
    have hp0 : p = 0 := by omega
    rw [hp0] at h34
    norm_num at h34
  obtain ⟨E0, hE0⟩ := potencias_ganan (3 ^ q) h34
  have hA : 3 ^ ((E0 + 2) * q) < 2 ^ (2 * (E0 + 1) * p) := by
    calc 3 ^ ((E0 + 2) * q) = 3 ^ q * (3 ^ q) ^ (E0 + 1) := by
          rw [← pow_mul, ← pow_add]
          congr 1
          ring
      _ < (4 ^ p) ^ (E0 + 1) := hE0 (E0 + 1) (by omega)
      _ = 2 ^ (2 * (E0 + 1) * p) := by
          rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul, ← pow_mul]
          congr 1
          ring
  obtain ⟨M, hM⟩ := potencias_ganan (2 ^ q * 2 ^ (2 * (E0 + 1) * (q - p))) hA
  have hb1 : 1 < 2 ^ (2 * (E0 + 1)) := Nat.one_lt_two_pow (by omega)
  rw [tendsto_order]
  refine ⟨fun a ha => Filter.Eventually.of_forall fun N => lt_of_lt_of_le ha (by positivity),
    fun a ha => ?_⟩
  obtain ⟨m0, hm0⟩ := exists_nat_gt (((E0 + 2 : ℕ) : ℝ) / a)
  rw [Filter.eventually_atTop]
  refine ⟨(2 ^ (2 * (E0 + 1))) ^ (m0 + M + 1), fun N hN => ?_⟩
  have hN0 : N ≠ 0 := by
    have := Nat.one_le_pow (m0 + M + 1) (2 ^ (2 * (E0 + 1))) (by omega)
    omega
  have hmge : m0 + M + 1 ≤ Nat.log (2 ^ (2 * (E0 + 1))) N := Nat.le_log_of_pow_le hb1 hN
  have hlow : 2 ^ (2 * (E0 + 1) * Nat.log (2 ^ (2 * (E0 + 1))) N) ≤ N := by
    rw [pow_mul]
    exact Nat.pow_log_le_self _ hN0
  have hhigh : N < 2 ^ (2 * (E0 + 1) * (Nat.log (2 ^ (2 * (E0 + 1))) N + 1)) := by
    rw [pow_mul]
    exact Nat.lt_pow_succ_log_self hb1 N
  generalize Nat.log (2 ^ (2 * (E0 + 1))) N = m at hmge hlow hhigh
  have hcond := condicion hpq hhigh (hM m (by omega)).le
  have hcota := korec_cota hpq hq (by omega) hlow hcond
  have hNpos : (0 : ℝ) < N := by exact_mod_cast Nat.pos_of_ne_zero hN0
  have hmpos : (0 : ℝ) < m := by exact_mod_cast (show 0 < m by omega)
  have hmr : ((E0 + 2 : ℕ) : ℝ) / a < m :=
    lt_of_lt_of_le hm0 (by exact_mod_cast (show m0 ≤ m by omega))
  have h1 : ((E0 + 2 : ℕ) : ℝ) < m * a := (div_lt_iff₀ ha).1 hmr
  have hcr : (m : ℝ) * (altos p q N).card ≤ ((E0 + 2 : ℕ) : ℝ) * N := by
    exact_mod_cast hcota
  rw [div_lt_iff₀ hNpos]
  by_contra hcon
  have h2 := mul_le_mul_of_nonneg_left (not_lt.mp hcon) hmpos.le
  have h3 := mul_lt_mul_of_pos_right h1 hNpos
  nlinarith

/-- Korec con `c = 4/5`: casi todo número baja por debajo de `n^0,8` (`3^5 < 4^4`). -/
theorem korec_cuatro_quintos :
    Filter.Tendsto (fun N : ℕ => ((altos 4 5 N).card : ℝ) / N) Filter.atTop (nhds 0) :=
  korec (by norm_num) (by norm_num)

/-- Korec con `c = 191/241 ≈ 0,79253`, a menos de una diezmilésima del umbral
    `log 3 / log 4 ≈ 0,79248` (`3^241 < 4^191`). -/
theorem korec_cerca_del_umbral :
    Filter.Tendsto (fun N : ℕ => ((altos 191 241 N).card : ℝ) / N) Filter.atTop (nhds 0) :=
  korec (by norm_num) (by norm_num)

/-- Allouche (1979), con `c = 87/100 > 0,869` (`3^100 < 4^87`). -/
theorem allouche :
    Filter.Tendsto (fun N : ℕ => ((altos 87 100 N).card : ℝ) / N) Filter.atTop (nhds 0) :=
  korec (by norm_num) (by norm_num)

end CasaKorec

#print axioms CasaKorec.suma_transferencia
#print axioms CasaKorec.momento_dos
#print axioms CasaKorec.cota_chebyshev
#print axioms CasaKorec.baja_de_potencia
#print axioms CasaKorec.korec_cota
#print axioms CasaKorec.korec
#print axioms CasaKorec.korec_cuatro_quintos
#print axioms CasaKorec.korec_cerca_del_umbral
#print axioms CasaKorec.allouche
