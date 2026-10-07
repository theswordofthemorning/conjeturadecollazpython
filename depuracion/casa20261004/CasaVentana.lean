import CasaGrieta

/-! # Una ventana: casi toda órbita baja por debajo de n^0,8

07-10-2026. Explicación en `LEEME.md` de esta carpeta, sección «Una ventana: Korec».

Terras (1976) probó que casi todo número baja alguna vez de sí mismo (`casi_todo_desciende`).
Korec (1994) probó mucho más: para todo exponente θ mayor que log 3/log 4 ≈ 0,7925, casi todo
número `n` baja alguna vez por debajo de `n^θ`. Aquí está en Lean el caso θ = 0,8, con las
constantes escritas:

* `tamano_general`: para cualquier número y cualquier camino,
  `2^k·T^k(n) + 2^k ≤ 3^S·n + 3^k`;
* `pocos_patrones_pesos`: con pesos `q ≤ p`, los patrones de largo `L` con al menos `a`
  subidas, por `p^a·q^(L−a)`, no pasan de `(p+q)^L`; con 503 y 497 (`margen_pesos`), los
  patrones de largo 1000 con al menos 503 subidas son menos que `2^1000`;
* `baja_korec`: si `2^(1000m) ≤ n < 2^(1010m)`, con `m ≥ 2`, y en sus primeros `1000m` pasos
  el número sube menos de `503m` veces, termina por debajo de `n^0,8`: `T^(1000m)(n)^5 < n^4`;
* `cuenta_korec_bloque`: por debajo de `2^(1010m)` quedan pocos números que no bajen así;
* `densidad_de_bloques`, `casi_todo_baja_08`: **casi toda órbita baja por debajo de `n^0,8`
  en a lo sumo `log₂ n` pasos**;
* `cuenta_sin_cst_bloques`, `densidad_de_cuenta`, `casi_todo_cst`: otra ventana, del muro A:
  **casi todo número cumple CST**, es decir, baja de sí mismo justo en su primer cruce
  (Terras, 1976).

Es una ventana: dice «casi todos», y el fugitivo y la grieta viven en el conjunto de densidad
cero. Las cuentas con números enormes (`margen_pronostico`, `margen_viento`,
`margen_viento_debil`, `margen_pesos`) se comprueban con `decide +kernel`, en el núcleo de Lean;
en la prueba de densidad esas constantes quedan como números opacos (`korec_opaco`).

Sin hipótesis externas. Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaVentana

open Ocelotas OcelotasContador CasaPlano CasaRetrato CasaTablero CasaPlaneador CasaGrieta

/-- **El tamaño con el viento**, para cualquier número y cualquier camino:
    `2^k·T^k(n) + 2^k ≤ 3^S·n + 3^k`. -/
theorem tamano_general (n : ℕ) : ∀ k, 2 ^ k * T^[k] n + 2 ^ k ≤ 3 ^ S k n * n + 3 ^ k := by
  intro k
  induction k with
  | zero => simp [S]
  | succ k ih =>
    have hS : S (k + 1) n = S k n + T^[k] n % 2 := by
      rw [S_add]
      simp [S]
    rw [Function.iterate_succ_apply', hS]
    rcases Nat.mod_two_eq_zero_or_one (T^[k] n) with hp | hp
    · rw [hp, Nat.add_zero]
      have he := T_par hp
      have h23 : 2 ^ k ≤ 2 * 3 ^ k := by
        have := Nat.pow_le_pow_left (show 2 ≤ 3 by norm_num) k
        omega
      calc 2 ^ (k + 1) * T (T^[k] n) + 2 ^ (k + 1)
          = 2 ^ k * (2 * T (T^[k] n)) + 2 ^ k + 2 ^ k := by ring
        _ = 2 ^ k * T^[k] n + 2 ^ k + 2 ^ k := by rw [he]
        _ ≤ 3 ^ S k n * n + 3 ^ k + 2 ^ k := by omega
        _ ≤ 3 ^ S k n * n + 3 ^ (k + 1) := by rw [pow_succ 3 k]; omega
    · rw [hp]
      have he := T_impar hp
      calc 2 ^ (k + 1) * T (T^[k] n) + 2 ^ (k + 1)
          = 2 ^ k * (2 * T (T^[k] n)) + 2 * 2 ^ k := by ring
        _ = 3 * (2 ^ k * T^[k] n + 2 ^ k) := by rw [he]; ring
        _ ≤ 3 * (3 ^ S k n * n + 3 ^ k) := Nat.mul_le_mul_left 3 ih
        _ = 3 ^ (S k n + 1) * n + 3 ^ (k + 1) := by ring

/-- **Pocos patrones con muchas subidas**, con pesos `q ≤ p`: los subconjuntos de
    `{0, …, L−1}` con al menos `a` elementos, por `p^a·q^(L−a)`, no pasan de `(p+q)^L`. -/
theorem pocos_patrones_pesos (L a p q : ℕ) (hqp : q ≤ p) :
    ((Finset.range L).powerset.filter fun A => a ≤ A.card).card * (p ^ a * q ^ (L - a)) ≤
      (p + q) ^ L := by
  set B := (Finset.range L).powerset.filter fun A => a ≤ A.card
  have hsuma : ∑ A ∈ (Finset.range L).powerset, p ^ A.card * q ^ (L - A.card) = (p + q) ^ L := by
    have := Finset.sum_pow_mul_eq_add_pow p q (Finset.range L)
    simpa using this
  have hcada : ∀ A ∈ B, p ^ a * q ^ (L - a) ≤ p ^ A.card * q ^ (L - A.card) := by
    intro A hA
    rw [Finset.mem_filter, Finset.mem_powerset] at hA
    have hAL : A.card ≤ L := by
      have := Finset.card_le_card hA.1
      simpa using this
    obtain ⟨j, hj⟩ : ∃ j, A.card = a + j := ⟨A.card - a, by omega⟩
    have e : L - a = j + (L - A.card) := by omega
    rw [e, hj, pow_add, pow_add]
    have hj' : q ^ j ≤ p ^ j := Nat.pow_le_pow_left hqp j
    calc p ^ a * (q ^ j * q ^ (L - (a + j))) ≤ p ^ a * (p ^ j * q ^ (L - (a + j))) :=
          Nat.mul_le_mul_left _ (Nat.mul_le_mul_right _ hj')
      _ = p ^ a * p ^ j * q ^ (L - (a + j)) := by rw [Nat.mul_assoc]
  calc B.card * (p ^ a * q ^ (L - a)) = ∑ A ∈ B, p ^ a * q ^ (L - a) := by
        rw [Finset.sum_const, smul_eq_mul]
    _ ≤ ∑ A ∈ B, p ^ A.card * q ^ (L - A.card) := Finset.sum_le_sum hcada
    _ ≤ ∑ A ∈ (Finset.range L).powerset, p ^ A.card * q ^ (L - A.card) :=
        Finset.sum_le_sum_of_subset (Finset.filter_subset _ _)
    _ = (p + q) ^ L := hsuma

/-- Entre 0 y N−1, los números con al menos `503m` subidas en sus primeros `1000m` pasos, por
    `(503^503·497^497)^m`, no pasan de `(N/2^(1000m) + 1)·1000^(1000m)`. -/
theorem cuenta_korec (N m : ℕ) :
    ((Finset.range N).filter fun n => 503 * m ≤ S (1000 * m) n).card *
        (503 ^ 503 * 497 ^ 497) ^ m ≤ (N / 2 ^ (1000 * m) + 1) * 1000 ^ (1000 * m) := by
  have h1 := cuenta_por_bloques N (1000 * m) (fun s => 503 * m ≤ s)
  have h2 := pocos_patrones_pesos (1000 * m) (503 * m) 503 497 (by norm_num)
  have e1 : (503 : ℕ) ^ (503 * m) * 497 ^ (1000 * m - 503 * m) =
      (503 ^ 503 * 497 ^ 497) ^ m := by
    rw [show 1000 * m - 503 * m = 497 * m by omega, mul_pow, ← pow_mul, ← pow_mul]
  have e2 : ((503 : ℕ) + 497) ^ (1000 * m) = 1000 ^ (1000 * m) := by norm_num
  rw [e1, e2] at h2
  calc ((Finset.range N).filter fun n => 503 * m ≤ S (1000 * m) n).card *
        (503 ^ 503 * 497 ^ 497) ^ m
      ≤ ((N / 2 ^ (1000 * m) + 1) *
          ((Finset.range (1000 * m)).powerset.filter fun A => 503 * m ≤ A.card).card) *
          (503 ^ 503 * 497 ^ 497) ^ m := Nat.mul_le_mul_right _ h1
    _ = (N / 2 ^ (1000 * m) + 1) *
          (((Finset.range (1000 * m)).powerset.filter fun A => 503 * m ≤ A.card).card *
            (503 ^ 503 * 497 ^ 497) ^ m) := by rw [Nat.mul_assoc]
    _ ≤ (N / 2 ^ (1000 * m) + 1) * 1000 ^ (1000 * m) := Nat.mul_le_mul_left _ h2

/-- Margen del pronóstico: `8·3^2515·2^1010 ≤ 2^5000`. -/
theorem margen_pronostico : 8 * (3 ^ 2515 * 2 ^ 1010) ≤ (2 : ℕ) ^ 5000 := by decide +kernel

/-- Margen del viento: `32·3^5000 < 2^9000`. -/
theorem margen_viento : 32 * 3 ^ 5000 < (2 : ℕ) ^ 9000 := by decide +kernel

/-- `3^5000 ≤ 2^9000`. -/
theorem margen_viento_debil : (3 : ℕ) ^ 5000 ≤ 2 ^ 9000 := by decide +kernel

/-- Margen de los pesos: `1000^1000 < 2^1000·503^503·497^497`, es decir, con pesos 503 y 497 los
    patrones de largo 1000 con al menos 503 subidas son menos que `2^1000`. -/
theorem margen_pesos : (1000 : ℕ) ^ 1000 < 2 ^ 1000 * (503 ^ 503 * 497 ^ 497) := by
  decide +kernel

/-- **Bajar por debajo de `n^0,8`.** Si `2^(1000m) ≤ n < 2^(1010m)`, con `m ≥ 2`, y en sus
    primeros `1000m` pasos el número sube menos de `503m` veces, al final de esos pasos vale
    menos que `n^0,8`: `T^(1000m)(n)^5 < n^4`. -/
theorem baja_korec {m n : ℕ} (hm : 2 ≤ m) (h1 : 2 ^ (1000 * m) ≤ n) (h2 : n < 2 ^ (1010 * m))
    (hS : S (1000 * m) n < 503 * m) : (T^[1000 * m] n) ^ 5 < n ^ 4 := by
  have ht := tamano_general n (1000 * m)
  have h3S : 3 ^ S (1000 * m) n ≤ 3 ^ (503 * m) := Nat.pow_le_pow_right (by norm_num) hS.le
  have hT : 2 ^ (1000 * m) * T^[1000 * m] n < 3 ^ (503 * m) * n + 3 ^ (1000 * m) := by
    have h4 : 3 ^ S (1000 * m) n * n ≤ 3 ^ (503 * m) * n := Nat.mul_le_mul_right _ h3S
    have h5 : 0 < 2 ^ (1000 * m) := by positivity
    omega
  -- el término del pronóstico
  have hX : (2 * (3 ^ (503 * m) * n)) ^ 5 ≤ (2 ^ (1000 * m)) ^ 5 * n ^ 4 := by
    have hc := margen_pronostico
    have h8 : 32 ≤ 8 ^ m := le_trans (by norm_num) (Nat.pow_le_pow_right (by norm_num) hm)
    have key : 32 * (3 ^ 2515) ^ m * (2 ^ 1010) ^ m ≤ (2 ^ 5000) ^ m :=
      calc 32 * (3 ^ 2515) ^ m * (2 ^ 1010) ^ m = 32 * (3 ^ 2515 * 2 ^ 1010) ^ m := by
            rw [mul_pow, Nat.mul_assoc]
        _ ≤ 8 ^ m * (3 ^ 2515 * 2 ^ 1010) ^ m := Nat.mul_le_mul_right _ h8
        _ = (8 * (3 ^ 2515 * 2 ^ 1010)) ^ m := (mul_pow _ _ _).symm
        _ ≤ (2 ^ 5000) ^ m := Nat.pow_le_pow_left hc m
    have hn : n ≤ (2 ^ 1010) ^ m := by
      rw [← pow_mul]
      exact h2.le
    have e1 : (2 * (3 ^ (503 * m) * n)) ^ 5 = 32 * (3 ^ 2515) ^ m * n * n ^ 4 := by
      rw [mul_pow, mul_pow, ← pow_mul, show 503 * m * 5 = 2515 * m by ring, pow_mul]
      generalize (3 : ℕ) ^ 2515 = C
      ring
    have e2 : (2 ^ (1000 * m)) ^ 5 * n ^ 4 = (2 ^ 5000) ^ m * n ^ 4 := by
      rw [← pow_mul, show 1000 * m * 5 = 5000 * m by ring, pow_mul]
    rw [e1, e2]
    apply Nat.mul_le_mul_right
    calc 32 * (3 ^ 2515) ^ m * n ≤ 32 * (3 ^ 2515) ^ m * (2 ^ 1010) ^ m :=
          Nat.mul_le_mul_left _ hn
      _ ≤ (2 ^ 5000) ^ m := key
  -- el término del viento
  have hY : (2 * 3 ^ (1000 * m)) ^ 5 < (2 ^ (1000 * m)) ^ 5 * n ^ 4 := by
    have hn4 : (2 ^ (1000 * m)) ^ 4 ≤ n ^ 4 := Nat.pow_le_pow_left h1 4
    have hc2 := margen_viento
    have hc3 := margen_viento_debil
    obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
    have e1 : (2 * 3 ^ (1000 * (j + 1))) ^ 5 = (3 ^ 5000) ^ j * (32 * 3 ^ 5000) := by
      rw [mul_pow, ← pow_mul, show 1000 * (j + 1) * 5 = 5000 * j + 5000 by ring, pow_add,
        pow_mul]
      generalize (3 : ℕ) ^ 5000 = C
      ring
    have e2 : (2 ^ (1000 * (j + 1))) ^ 5 * (2 ^ (1000 * (j + 1))) ^ 4 =
        (2 ^ 9000) ^ j * 2 ^ 9000 := by
      rw [← pow_mul, ← pow_mul, ← pow_add, show 1000 * (j + 1) * 5 + 1000 * (j + 1) * 4 =
        9000 * j + 9000 by ring, pow_add, pow_mul]
    calc (2 * 3 ^ (1000 * (j + 1))) ^ 5 = (3 ^ 5000) ^ j * (32 * 3 ^ 5000) := e1
      _ < (3 ^ 5000) ^ j * 2 ^ 9000 := Nat.mul_lt_mul_of_pos_left hc2 (by positivity)
      _ ≤ (2 ^ 9000) ^ j * 2 ^ 9000 := Nat.mul_le_mul_right _ (Nat.pow_le_pow_left hc3 j)
      _ = (2 ^ (1000 * (j + 1))) ^ 5 * (2 ^ (1000 * (j + 1))) ^ 4 := e2.symm
      _ ≤ (2 ^ (1000 * (j + 1))) ^ 5 * n ^ 4 := Nat.mul_le_mul_left _ hn4
  -- juntar los dos
  have hsum : 3 ^ (503 * m) * n + 3 ^ (1000 * m) ≤
      2 * max (3 ^ (503 * m) * n) (3 ^ (1000 * m)) := by
    have := le_max_left (3 ^ (503 * m) * n) (3 ^ (1000 * m))
    have := le_max_right (3 ^ (503 * m) * n) (3 ^ (1000 * m))
    omega
  have hZ5 : (2 * max (3 ^ (503 * m) * n) (3 ^ (1000 * m))) ^ 5 ≤
      (2 ^ (1000 * m)) ^ 5 * n ^ 4 := by
    rcases le_total (3 ^ (503 * m) * n) (3 ^ (1000 * m)) with h | h
    · rw [max_eq_right h]
      exact hY.le
    · rw [max_eq_left h]
      exact hX
  have h5 : (2 ^ (1000 * m) * T^[1000 * m] n) ^ 5 < (2 ^ (1000 * m)) ^ 5 * n ^ 4 :=
    calc (2 ^ (1000 * m) * T^[1000 * m] n) ^ 5
        < (3 ^ (503 * m) * n + 3 ^ (1000 * m)) ^ 5 := Nat.pow_lt_pow_left hT (by norm_num)
      _ ≤ (2 * max (3 ^ (503 * m) * n) (3 ^ (1000 * m))) ^ 5 := Nat.pow_le_pow_left hsum 5
      _ ≤ (2 ^ (1000 * m)) ^ 5 * n ^ 4 := hZ5
  rw [mul_pow] at h5
  exact Nat.lt_of_mul_lt_mul_left h5

open Classical in
/-- **Korec en cifras**: por debajo de `2^(1010m)`, con `m ≥ 2`, los números que no bajan por
    debajo de `n^0,8` en a lo sumo `log₂ n` pasos, por `(503^503·497^497)^m`, no pasan de
    `2^(1000m)·(503^503·497^497)^m + (2^(10m) + 1)·1000^(1000m)`. -/
theorem cuenta_korec_bloque {m : ℕ} (hm : 2 ≤ m) :
    ((Finset.range (2 ^ (1010 * m))).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4).card * (503 ^ 503 * 497 ^ 497) ^ m ≤
      2 ^ (1000 * m) * (503 ^ 503 * 497 ^ 497) ^ m +
        (2 ^ (10 * m) + 1) * 1000 ^ (1000 * m) := by
  have hsub : ((Finset.range (2 ^ (1010 * m))).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4) ⊆
      Finset.range (2 ^ (1000 * m)) ∪
        (Finset.range (2 ^ (1010 * m))).filter fun n => 503 * m ≤ S (1000 * m) n := by
    intro n hn
    rw [Finset.mem_filter, Finset.mem_range] at hn
    rw [Finset.mem_union, Finset.mem_range, Finset.mem_filter, Finset.mem_range]
    by_cases h1 : n < 2 ^ (1000 * m)
    · exact Or.inl h1
    · right
      refine ⟨hn.1, ?_⟩
      by_contra hS
      push Not at hS h1
      exact hn.2 ⟨1000 * m, Nat.le_log_of_pow_le (by norm_num) h1, baja_korec hm h1 hn.1 hS⟩
  have hdiv : 2 ^ (1010 * m) / 2 ^ (1000 * m) = 2 ^ (10 * m) := by
    rw [Nat.pow_div (by omega) (by norm_num)]
    congr 1
    omega
  have hc := cuenta_korec (2 ^ (1010 * m)) m
  rw [hdiv] at hc
  calc ((Finset.range (2 ^ (1010 * m))).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4).card * (503 ^ 503 * 497 ^ 497) ^ m
      ≤ (Finset.range (2 ^ (1000 * m)) ∪ (Finset.range (2 ^ (1010 * m))).filter
          fun n => 503 * m ≤ S (1000 * m) n).card * (503 ^ 503 * 497 ^ 497) ^ m :=
        Nat.mul_le_mul_right _ (Finset.card_le_card hsub)
    _ ≤ ((Finset.range (2 ^ (1000 * m))).card + ((Finset.range (2 ^ (1010 * m))).filter
          fun n => 503 * m ≤ S (1000 * m) n).card) * (503 ^ 503 * 497 ^ 497) ^ m :=
        Nat.mul_le_mul_right _ (Finset.card_union_le _ _)
    _ = 2 ^ (1000 * m) * (503 ^ 503 * 497 ^ 497) ^ m + ((Finset.range (2 ^ (1010 * m))).filter
          fun n => 503 * m ≤ S (1000 * m) n).card * (503 ^ 503 * 497 ^ 497) ^ m := by
        rw [Finset.card_range, Nat.add_mul]
    _ ≤ 2 ^ (1000 * m) * (503 ^ 503 * 497 ^ 497) ^ m +
          (2 ^ (10 * m) + 1) * 1000 ^ (1000 * m) := Nat.add_le_add_left hc _

/-- **De los bloques a la densidad.** Si una cuenta creciente `E` cumple
    `E(B^m) ≤ f(m)·B^m` desde `m = 2`, con `f(m)` tan chico como se quiera para `m` grande,
    entonces `E(N) ≤ ε·N` desde cierto `N₀`. -/
theorem densidad_de_bloques (E : ℕ → ℕ) (hE : Monotone E) (B : ℕ) (hB : 2 ≤ B)
    (f : ℕ → ℝ) (hf : ∀ δ : ℝ, 0 < δ → ∃ m₀, ∀ m, m₀ ≤ m → f m ≤ δ)
    (hcota : ∀ m, 2 ≤ m → (E (B ^ m) : ℝ) ≤ f m * (B : ℝ) ^ m) {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N → (E N : ℝ) ≤ ε * N := by
  have hBpos : (0 : ℝ) < B := by exact_mod_cast (by omega : 0 < B)
  obtain ⟨m₀, hm₀⟩ := hf (ε / B) (by positivity)
  refine ⟨B ^ (m₀ + 2), fun N hN => ?_⟩
  have hN0 : N ≠ 0 := by
    have : 0 < B ^ (m₀ + 2) := by positivity
    omega
  have hℓ1 : B ^ Nat.log B N ≤ N := Nat.pow_log_le_self B hN0
  have hℓ2 : N < B ^ (Nat.log B N + 1) := Nat.lt_pow_succ_log_self (by omega) N
  have hℓ3 : m₀ + 2 ≤ Nat.log B N := Nat.le_log_of_pow_le (by omega) hN
  set ℓ := Nat.log B N
  have h1 : (E N : ℝ) ≤ E (B ^ (ℓ + 1)) := by exact_mod_cast hE hℓ2.le
  have h2 := hcota (ℓ + 1) (by omega)
  have h3 : f (ℓ + 1) ≤ ε / B := hm₀ (ℓ + 1) (by omega)
  have h4 : (B : ℝ) ^ (ℓ + 1) ≤ B * N := by
    have h5 : (B : ℝ) ^ ℓ ≤ N := by exact_mod_cast hℓ1
    rw [pow_succ, mul_comm]
    exact mul_le_mul_of_nonneg_left h5 hBpos.le
  calc (E N : ℝ) ≤ E (B ^ (ℓ + 1)) := h1
    _ ≤ f (ℓ + 1) * (B : ℝ) ^ (ℓ + 1) := h2
    _ ≤ (ε / B) * (B : ℝ) ^ (ℓ + 1) := mul_le_mul_of_nonneg_right h3 (by positivity)
    _ ≤ (ε / B) * (B * N) := mul_le_mul_of_nonneg_left h4 (by positivity)
    _ = ε * N := by field_simp

open Classical in
/-- La cuenta de `cuenta_korec_bloque`, escrita con potencias `m`-ésimas de constantes fijas. -/
theorem cuenta_korec_potencias {m : ℕ} (hm : 2 ≤ m) :
    ((Finset.range ((2 ^ 1000 * 1024) ^ m)).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4).card * (503 ^ 503 * 497 ^ 497) ^ m ≤
      (2 ^ 1000) ^ m * (503 ^ 503 * 497 ^ 497) ^ m + (1024 ^ m + 1) * (1000 ^ 1000) ^ m := by
  have h := cuenta_korec_bloque hm
  have e10 : (1024 : ℕ) ^ m = 2 ^ (10 * m) := by
    rw [pow_mul]
    norm_num
  have e1 : (2 : ℕ) ^ (1010 * m) = (2 ^ 1000 * 1024) ^ m := by
    rw [mul_pow, ← pow_mul, e10, ← pow_add]
    congr 1
    omega
  have e2 : (2 : ℕ) ^ (1000 * m) = (2 ^ 1000) ^ m := by rw [← pow_mul]
  have e4 : (1000 : ℕ) ^ (1000 * m) = (1000 ^ 1000) ^ m := by rw [← pow_mul]
  rw [e1, e2, ← e10, e4] at h
  exact h

open Classical in
/-- `cuenta_korec_potencias` y `margen_pesos` con las constantes como variables. -/
theorem korec_opaco (K Q R : ℕ) (hK : K = 503 ^ 503 * 497 ^ 497) (hQ : Q = 2 ^ 1000)
    (hR : R = 1000 ^ 1000) :
    R < Q * K ∧ ∀ m, 2 ≤ m →
      ((Finset.range ((Q * 1024) ^ m)).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4).card * K ^ m ≤
      Q ^ m * K ^ m + (1024 ^ m + 1) * R ^ m := by
  rw [hK, hQ, hR]
  exact ⟨margen_pesos, fun m hm => cuenta_korec_potencias hm⟩

open Classical in
/-- **Una ventana: casi toda órbita baja por debajo de `n^0,8`** (Korec, 1994, lo prueba para
    todo exponente mayor que log 3/log 4 ≈ 0,7925; aquí, 0,8). Para todo ε > 0, desde cierto
    N₀, entre 0 y N−1 hay a lo sumo ε·N números que no bajan por debajo de `n^0,8` en a lo
    sumo `log₂ n` pasos. -/
theorem casi_todo_baja_08 {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N →
      (((Finset.range N).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4).card : ℝ) ≤ ε * N := by
  set E : ℕ → ℕ := fun N => ((Finset.range N).filter fun n =>
    ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ 5 < n ^ 4).card with hEdef
  have hE : Monotone E := by
    intro a b hab
    exact Finset.card_le_card (Finset.filter_subset_filter _ (Finset.range_mono hab))
  -- las constantes gigantes, como números opacos
  obtain ⟨K, hK⟩ : ∃ K : ℕ, K = 503 ^ 503 * 497 ^ 497 := ⟨_, rfl⟩
  obtain ⟨Q, hQ⟩ : ∃ Q : ℕ, Q = 2 ^ 1000 := ⟨_, rfl⟩
  obtain ⟨R, hR⟩ : ∃ R : ℕ, R = 1000 ^ 1000 := ⟨_, rfl⟩
  obtain ⟨hC1, hbl⟩ := korec_opaco K Q R hK hQ hR
  clear hK hQ hR
  have hQK : 0 < Q * K := lt_of_le_of_lt (Nat.zero_le R) hC1
  have hQpos : 0 < Q := by
    rcases Nat.eq_zero_or_pos Q with h | h
    · rw [h, Nat.zero_mul] at hQK
      exact absurd hQK (lt_irrefl 0)
    · exact h
  have hKpos : 0 < K := by
    rcases Nat.eq_zero_or_pos K with h | h
    · rw [h, Nat.mul_zero] at hQK
      exact absurd hQK (lt_irrefl 0)
    · exact h
  have hQR : (0 : ℝ) < Q := by exact_mod_cast hQpos
  have hKR : (0 : ℝ) < K := by exact_mod_cast hKpos
  have hQKR : (0 : ℝ) < (Q : ℝ) * K := mul_pos hQR hKR
  set ρ : ℝ := (R : ℝ) / ((Q : ℝ) * K) with hρ
  have hρ0 : 0 ≤ ρ := div_nonneg (Nat.cast_nonneg R) hQKR.le
  have hρ1 : ρ < 1 := by
    rw [hρ, div_lt_one hQKR]
    exact_mod_cast hC1
  set f : ℕ → ℝ := fun m => ((1 : ℝ) / 1024) ^ m + 2 * ρ ^ m with hfdef
  have hf : ∀ δ : ℝ, 0 < δ → ∃ m₀, ∀ m, m₀ ≤ m → f m ≤ δ := by
    intro δ hδ
    obtain ⟨a, ha⟩ := exists_pow_lt_of_lt_one (div_pos hδ (by norm_num) : (0 : ℝ) < δ / 3) hρ1
    obtain ⟨b, hb⟩ := exists_pow_lt_of_lt_one (div_pos hδ (by norm_num) : (0 : ℝ) < δ / 3)
      (by norm_num : (1 / 1024 : ℝ) < 1)
    refine ⟨a + b, fun m hm => ?_⟩
    have h1 : ((1 : ℝ) / 1024) ^ m ≤ (1 / 1024) ^ b :=
      pow_le_pow_of_le_one (by norm_num) (by norm_num) (by omega)
    have h2 : ρ ^ m ≤ ρ ^ a := pow_le_pow_of_le_one hρ0 hρ1.le (by omega)
    simp only [hfdef]
    linarith
  have hB2 : 2 ≤ Q * 1024 := by omega
  have hcota : ∀ m, 2 ≤ m → (E ((Q * 1024) ^ m) : ℝ) ≤ f m * ((Q * 1024 : ℕ) : ℝ) ^ m := by
    intro m hm
    have hblockR : (E ((Q * 1024) ^ m) : ℝ) * (K : ℝ) ^ m ≤
        (Q : ℝ) ^ m * (K : ℝ) ^ m + ((1024 : ℝ) ^ m + 1) * (R : ℝ) ^ m := by
      exact_mod_cast hbl m hm
    have hRm : (R : ℝ) ^ m = (Q : ℝ) ^ m * (K : ℝ) ^ m * ρ ^ m := by
      rw [hρ, div_pow, mul_pow]
      field_simp
    have hKm : (0 : ℝ) < (K : ℝ) ^ m := pow_pos hKR m
    have hQm : (0 : ℝ) ≤ (Q : ℝ) ^ m := (pow_pos hQR m).le
    have hρm : (0 : ℝ) ≤ ρ ^ m := pow_nonneg hρ0 m
    have h1m : (1 : ℝ) ≤ (1024 : ℝ) ^ m := one_le_pow₀ (by norm_num)
    have hE1 : (E ((Q * 1024) ^ m) : ℝ) ≤
        (Q : ℝ) ^ m + ((1024 : ℝ) ^ m + 1) * ((Q : ℝ) ^ m * ρ ^ m) := by
      rw [hRm] at hblockR
      have h6 : (E ((Q * 1024) ^ m) : ℝ) * (K : ℝ) ^ m ≤
          ((Q : ℝ) ^ m + ((1024 : ℝ) ^ m + 1) * ((Q : ℝ) ^ m * ρ ^ m)) * (K : ℝ) ^ m := by
        linarith [hblockR]
      exact le_of_mul_le_mul_right h6 hKm
    have hBm : ((Q * 1024 : ℕ) : ℝ) ^ m = (Q : ℝ) ^ m * (1024 : ℝ) ^ m := by
      push_cast
      rw [mul_pow]
    have hmil : ((1 : ℝ) / 1024) ^ m * (1024 : ℝ) ^ m = 1 := by
      rw [← mul_pow]
      norm_num
    have e4 : f m * ((Q * 1024 : ℕ) : ℝ) ^ m =
        (Q : ℝ) ^ m + 2 * ((1024 : ℝ) ^ m * ((Q : ℝ) ^ m * ρ ^ m)) := by
      rw [hBm]
      simp only [hfdef]
      linear_combination (Q : ℝ) ^ m * hmil
    rw [e4]
    have h7 : ((1024 : ℝ) ^ m + 1) * ((Q : ℝ) ^ m * ρ ^ m) ≤
        2 * ((1024 : ℝ) ^ m * ((Q : ℝ) ^ m * ρ ^ m)) := by
      have h8 : (0 : ℝ) ≤ (Q : ℝ) ^ m * ρ ^ m := mul_nonneg hQm hρm
      nlinarith
    linarith
  exact densidad_de_bloques E hE (Q * 1024) hB2 f hf hcota hε

/-! ## Otra ventana: CST para casi todo número -/

/-- **De la cuenta de Terras a la densidad.** Si una cuenta cumple
    `E(N) ≤ (N/2^(100m) + 1)·2^(96m) + 100m·2^(100m)` para todo `m`, tiene densidad cero. -/
theorem densidad_de_cuenta (E : ℕ → ℕ)
    (h : ∀ N m, E N ≤ (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m))
    {ε : ℝ} (hε : 0 < ε) : ∃ N₀ : ℕ, ∀ N, N₀ ≤ N → (E N : ℝ) ≤ ε * N := by
  obtain ⟨m, hm⟩ := pow_unbounded_of_one_lt (2 / ε) (by norm_num : (1 : ℝ) < 16)
  set R : ℕ := 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m) with hR
  refine ⟨⌈2 * (R : ℝ) / ε⌉₊, fun N hN => ?_⟩
  have h1 := h N m
  have e : 2 ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h2 : N / 2 ^ (100 * m) * 2 ^ (96 * m) ≤ N / 16 ^ m := by
    rw [e, ← Nat.div_div_eq_div_mul]
    exact Nat.div_mul_le_self _ _
  have h3 : E N ≤ N / 16 ^ m + R := by
    have e4 : (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) =
        N / 2 ^ (100 * m) * 2 ^ (96 * m) + 2 ^ (96 * m) := by ring
    rw [hR]
    omega
  have h4 : (E N : ℝ) ≤ ((N / 16 ^ m : ℕ) : ℝ) + R := by
    exact_mod_cast h3
  have h16 : (0 : ℝ) < 16 ^ m := by positivity
  have h5 : ((N / 16 ^ m : ℕ) : ℝ) ≤ (N : ℝ) / 16 ^ m := by
    rw [le_div_iff₀ h16]
    exact_mod_cast Nat.div_mul_le_self N (16 ^ m)
  have h6 : (N : ℝ) / 16 ^ m ≤ ε * N / 2 := by
    rw [div_le_iff₀ h16]
    have h7 : 2 < 16 ^ m * ε := (div_lt_iff₀ hε).1 hm
    nlinarith [Nat.cast_nonneg (α := ℝ) N]
  have h8 : (R : ℝ) ≤ ε * N / 2 := by
    have h9 : 2 * (R : ℝ) / ε ≤ (N : ℝ) := (Nat.le_ceil _).trans (by exact_mod_cast hN)
    rw [div_le_iff₀ hε] at h9
    linarith
  linarith

open Classical in
/-- **Cuenta de los que no cumplen CST.** Entre 0 y N−1, los números que no bajan justo en su
    primer cruce son a lo sumo los que aguantan `100m` pasos sin cruzar más los menores que
    `100m·2^(100m)`. -/
theorem cuenta_sin_cst_bloques (N m : ℕ) :
    ((Finset.range N).filter fun n => ¬ ∃ k, PrimerCruce n k ∧ T^[k] n < n).card ≤
      (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m) := by
  have hsub : (Finset.range N).filter (fun n => ¬ ∃ k, PrimerCruce n k ∧ T^[k] n < n) ⊆
      (Finset.range N).filter (fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n) ∪
        Finset.range (100 * m * 2 ^ (100 * m)) := by
    intro n hn
    rw [Finset.mem_filter] at hn
    rw [Finset.mem_union, Finset.mem_filter, Finset.mem_range, Finset.mem_range]
    by_cases h : 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n
    · exact Or.inl ⟨Finset.mem_range.1 hn.1, h⟩
    · right
      push Not at h
      obtain ⟨k, hkj, hk⟩ := primer_cruce_antes h
      have h1 : 3 * n < k * 2 ^ k := by
        by_contra h2
        push Not at h2
        exact hn.2 ⟨k, hk, desciende_si_grande hk h2⟩
      have h2 : k * 2 ^ k ≤ 100 * m * 2 ^ (100 * m) :=
        Nat.mul_le_mul hkj (Nat.pow_le_pow_right (by norm_num) hkj)
      omega
  calc ((Finset.range N).filter fun n => ¬ ∃ k, PrimerCruce n k ∧ T^[k] n < n).card
      ≤ ((Finset.range N).filter (fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n) ∪
          Finset.range (100 * m * 2 ^ (100 * m))).card := Finset.card_le_card hsub
    _ ≤ ((Finset.range N).filter (fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n)).card +
          (Finset.range (100 * m * 2 ^ (100 * m))).card := Finset.card_union_le _ _
    _ ≤ (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) + 100 * m * 2 ^ (100 * m) := by
      rw [Finset.card_range]
      exact Nat.add_le_add_right (cuenta_sin_cruce N m) _

open Classical in
/-- **CST para casi todo número** (Terras, 1976): casi todo número baja de sí mismo justo en su
    primer cruce. Los que no tienen densidad cero. Es la forma reforzada del muro A, para casi
    todos y no para todos. -/
theorem casi_todo_cst {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N →
      (((Finset.range N).filter fun n => ¬ ∃ k, PrimerCruce n k ∧ T^[k] n < n).card : ℝ) ≤
        ε * N :=
  densidad_de_cuenta _ cuenta_sin_cst_bloques hε

end CasaVentana

#print axioms CasaVentana.tamano_general
#print axioms CasaVentana.pocos_patrones_pesos
#print axioms CasaVentana.cuenta_korec
#print axioms CasaVentana.margen_pronostico
#print axioms CasaVentana.margen_viento
#print axioms CasaVentana.margen_viento_debil
#print axioms CasaVentana.margen_pesos
#print axioms CasaVentana.baja_korec
#print axioms CasaVentana.cuenta_korec_bloque
#print axioms CasaVentana.cuenta_korec_potencias
#print axioms CasaVentana.densidad_de_bloques
#print axioms CasaVentana.korec_opaco
#print axioms CasaVentana.casi_todo_baja_08
#print axioms CasaVentana.densidad_de_cuenta
#print axioms CasaVentana.cuenta_sin_cst_bloques
#print axioms CasaVentana.casi_todo_cst
