import CasaVentana

/-! # El teorema de Korec, completo

07-10-2026. Explicación en `LEEME.md` de esta carpeta, sección «Una ventana: Korec».

Korec (*A density estimate for the 3x+1 problem*, Math. Slovaca 44, 1994) probó que, para todo
exponente θ mayor que log 3/log 4 ≈ 0,7925, casi todo número `n` baja alguna vez por debajo de
`n^θ`. `CasaVentana` lo prueba para θ = 0,8 con constantes escritas; este archivo lo prueba para
todo θ, con bloques de largo `2c` y umbral de `c + 1` subidas, donde `c` crece cuando θ se acerca
a log 3/log 4:

* `entropia_real`, `margen_entropia`: con pesos `c + 1` y `c`, los patrones de largo `2c` con al
  menos `c + 1` subidas son menos que `4^c`: `(2c+1)^(2c) < 4^c·(c+1)^(c+1)·c^(c−1)`;
* `baja_param`: si `2^(2cm) ≤ n < 2^((2c+1)m)` y en sus primeros `2cm` pasos el número sube menos
  de `(c+1)m` veces, termina por debajo de `n^(u/v)`, siempre que el bloque cumpla dos márgenes;
* `cuenta_param`, `cuenta_param_bloque`: la cuenta de los que quedan fuera;
* `existe_potencia`, `margenes_como_potencias`, `existe_bloque`: si `3^v < 4^u` y `u < v`, hay un
  bloque que cumple los dos márgenes;
* `korec_param`, `korec`: **para todo exponente racional `u/v` con `3^v < 4^u` y `u < v`, casi
  toda órbita baja por debajo de `n^(u/v)` en a lo sumo `log₂ n` pasos**;
* `korec_real`: **lo mismo para todo exponente real θ > log 3/log 4**;
* `margen_6309`, `margen_pesos_lagarias`, `subidas_lagarias`, `rareza_lagarias`: con la misma
  cuenta y pesos 6309 y 3691, **la rareza de las fugas puras al nivel de Lagarias**: por debajo
  de `x = 2^(10000m)`, a lo sumo `2·x^0,95` (su teorema F, 1985, para el primer cruce).

Es una ventana: dice «casi todos». Sin hipótesis externas. Compilación: `comprobar_casa.py`, en
esta carpeta. -/

namespace CasaKorec

open Ocelotas OcelotasContador CasaPlano CasaRetrato CasaTablero CasaPlaneador CasaGrieta
  CasaVentana

/-- **Entropía, en reales**: con `Y = 4c(c+1)`, `(1 + 1/Y)^c · c < c + 1`. -/
theorem entropia_real {c : ℕ} (hc : 1 ≤ c) :
    (1 + 1 / (4 * (c : ℝ) * (c + 1))) ^ c * c < c + 1 := by
  have hcR : (1 : ℝ) ≤ c := by exact_mod_cast hc
  set Y : ℝ := 4 * (c : ℝ) * (c + 1) with hY
  have hYpos : 0 < Y := by positivity
  -- (1 + 1/Y)^c ≤ exp(c/Y)
  have h1 : (1 + 1 / Y) ^ c ≤ Real.exp (c / Y) := by
    have h2 : 1 + 1 / Y ≤ Real.exp (1 / Y) := by linarith [Real.add_one_le_exp (1 / Y)]
    calc (1 + 1 / Y) ^ c ≤ (Real.exp (1 / Y)) ^ c :=
          pow_le_pow_left₀ (by positivity) h2 c
      _ = Real.exp (c / Y) := by
          rw [← Real.exp_nat_mul]
          congr 1
          field_simp
  -- exp(c/Y)·(1 - c/Y) ≤ 1
  have h3 : Real.exp (c / Y) * (1 - c / Y) ≤ 1 := by
    have h4 : 1 - c / Y ≤ Real.exp (-(c / Y)) := by linarith [Real.add_one_le_exp (-(c / Y))]
    calc Real.exp (c / Y) * (1 - c / Y) ≤ Real.exp (c / Y) * Real.exp (-(c / Y)) :=
          mul_le_mul_of_nonneg_left h4 (Real.exp_pos _).le
      _ = 1 := by rw [← Real.exp_add]; simp
  -- c/Y = 1/(4(c+1))
  have hcY : (c : ℝ) / Y = 1 / (4 * (c + 1)) := by
    rw [hY]
    field_simp
  have h6 : 0 ≤ 1 - (c : ℝ) / Y := by
    rw [hcY, sub_nonneg, div_le_one (by positivity)]
    linarith
  have h5 : (1 + 1 / Y) ^ c * (1 - (c : ℝ) / Y) ≤ 1 :=
    le_trans (mul_le_mul_of_nonneg_right h1 h6) h3
  have h8 : (1 + 1 / Y) ^ c * (4 * c + 3) ≤ 4 * (c + 1) := by
    have e : (1 : ℝ) - 1 / (4 * (c + 1)) = (4 * c + 3) / (4 * (c + 1)) := by
      field_simp
      ring
    rw [hcY, e, mul_div_assoc', div_le_one (by positivity)] at h5
    exact h5
  have hP : 0 ≤ (1 + 1 / Y) ^ c := by positivity
  nlinarith [mul_le_mul_of_nonneg_left h8 (by positivity : (0 : ℝ) ≤ c)]

/-- **Entropía, en naturales**: `(2c+1)^(2c) < 4^c·(c+1)^(c+1)·c^(c−1)`. Con pesos `c+1` y `c`,
    los patrones de largo `2c` con al menos `c+1` subidas son menos que `4^c`. -/
theorem margen_entropia {c : ℕ} (hc : 1 ≤ c) :
    (2 * c + 1) ^ (2 * c) < 4 ^ c * ((c + 1) ^ (c + 1) * c ^ (c - 1)) := by
  have h := entropia_real hc
  have hcR : (1 : ℝ) ≤ c := by exact_mod_cast hc
  set Y : ℝ := 4 * (c : ℝ) * (c + 1) with hY
  have hYpos : 0 < Y := by positivity
  -- (Y+1)^c·c < Y^c·(c+1)
  have h1 : (Y + 1) ^ c * c < Y ^ c * (c + 1) := by
    have e : (Y + 1) ^ c = Y ^ c * (1 + 1 / Y) ^ c := by
      rw [← mul_pow]
      congr 1
      field_simp
    rw [e]
    have hYc : 0 < Y ^ c := by positivity
    calc Y ^ c * (1 + 1 / Y) ^ c * c = Y ^ c * ((1 + 1 / Y) ^ c * c) := by ring
      _ < Y ^ c * (c + 1) := mul_lt_mul_of_pos_left h hYc
  -- pasar a naturales
  have h2 : (4 * c * (c + 1) + 1) ^ c * c < (4 * c * (c + 1)) ^ c * (c + 1) := by
    have : ((4 * c * (c + 1) + 1 : ℕ) : ℝ) ^ c * (c : ℝ) <
        ((4 * c * (c + 1) : ℕ) : ℝ) ^ c * ((c + 1 : ℕ) : ℝ) := by
      push_cast
      exact h1
    exact_mod_cast this
  have e1 : 4 * c * (c + 1) + 1 = (2 * c + 1) ^ 2 := by ring
  have e2 : (4 * c * (c + 1)) ^ c * (c + 1) = 4 ^ c * ((c + 1) ^ (c + 1) * c ^ (c - 1)) * c := by
    obtain ⟨d, rfl⟩ : ∃ d, c = d + 1 := ⟨c - 1, by omega⟩
    rw [show d + 1 - 1 = d by omega]
    rw [mul_pow, mul_pow]
    ring
  rw [e1, e2, ← pow_mul] at h2
  exact Nat.lt_of_mul_lt_mul_right h2

/-! ## El descenso y la cuenta, con parámetros -/

/-- **Bajar por debajo de `n^(u/v)`, con parámetros.** Con bloques de `2c` pasos: si
    `2^(2cm) ≤ n < 2^((2c+1)m)`, con `m ≥ 1`, y en sus primeros `2cm` pasos el número sube
    menos de `(c+1)m` veces, termina por debajo de `n^(u/v)`: `T^(2cm)(n)^v < n^u`. Pide dos
    márgenes por bloque, `hK1` (el del pronóstico) y `hK2` (el del viento). -/
theorem baja_param {u v c m n : ℕ} (huv : u < v) (hm : 1 ≤ m)
    (hK1 : 2 ^ v * (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u))) ≤ 2 ^ (2 * c * v))
    (hK2 : 2 ^ v * 3 ^ (2 * c * v) < 2 ^ (2 * c * (u + v)))
    (h1 : 2 ^ (2 * c * m) ≤ n) (h2 : n < 2 ^ ((2 * c + 1) * m))
    (hS : S (2 * c * m) n < (c + 1) * m) : (T^[2 * c * m] n) ^ v < n ^ u := by
  have hv : v ≠ 0 := by omega
  have ht := tamano_general n (2 * c * m)
  have h3S : 3 ^ S (2 * c * m) n ≤ 3 ^ ((c + 1) * m) :=
    Nat.pow_le_pow_right (by norm_num) hS.le
  have hT : 2 ^ (2 * c * m) * T^[2 * c * m] n < 3 ^ ((c + 1) * m) * n + 3 ^ (2 * c * m) := by
    have h4 : 3 ^ S (2 * c * m) n * n ≤ 3 ^ ((c + 1) * m) * n := Nat.mul_le_mul_right _ h3S
    have h5 : 0 < 2 ^ (2 * c * m) := by positivity
    omega
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
  -- el término del pronóstico
  have hX : (2 * (3 ^ ((c + 1) * (j + 1)) * n)) ^ v ≤ (2 ^ (2 * c * (j + 1))) ^ v * n ^ u := by
    have hnv : n ^ v = n ^ (v - u) * n ^ u := by rw [← pow_add, Nat.sub_add_cancel huv.le]
    have hn : n ^ (v - u) ≤ (2 ^ ((2 * c + 1) * (v - u))) ^ (j + 1) := by
      rw [← pow_mul, show (2 * c + 1) * (v - u) * (j + 1) = (2 * c + 1) * (j + 1) * (v - u) by ring,
        pow_mul 2 ((2 * c + 1) * (j + 1)) (v - u)]
      exact Nat.pow_le_pow_left h2.le _
    have hXY : 3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u)) ≤ 2 ^ (2 * c * v) :=
      le_trans (Nat.le_mul_of_pos_left _ (by positivity)) hK1
    have key : 2 ^ v * ((3 ^ ((c + 1) * v)) ^ (j + 1) * (2 ^ ((2 * c + 1) * (v - u))) ^ (j + 1)) ≤
        (2 ^ (2 * c * v)) ^ (j + 1) := by
      calc 2 ^ v * ((3 ^ ((c + 1) * v)) ^ (j + 1) * (2 ^ ((2 * c + 1) * (v - u))) ^ (j + 1))
          = (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u))) ^ j *
              (2 ^ v * (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u)))) := by
            rw [← mul_pow, pow_succ]
            ring
        _ ≤ (2 ^ (2 * c * v)) ^ j * 2 ^ (2 * c * v) :=
            Nat.mul_le_mul (Nat.pow_le_pow_left hXY j) hK1
        _ = (2 ^ (2 * c * v)) ^ (j + 1) := by rw [pow_succ]
    have e1 : (3 ^ ((c + 1) * (j + 1))) ^ v = (3 ^ ((c + 1) * v)) ^ (j + 1) := by
      rw [← pow_mul, ← pow_mul, show (c + 1) * (j + 1) * v = (c + 1) * v * (j + 1) by ring]
    have e2 : (2 ^ (2 * c * v)) ^ (j + 1) = (2 ^ (2 * c * (j + 1))) ^ v := by
      rw [← pow_mul, ← pow_mul, show 2 * c * v * (j + 1) = 2 * c * (j + 1) * v by ring]
    calc (2 * (3 ^ ((c + 1) * (j + 1)) * n)) ^ v
        = 2 ^ v * (3 ^ ((c + 1) * (j + 1))) ^ v * n ^ v := by rw [mul_pow, mul_pow, Nat.mul_assoc]
      _ = 2 ^ v * (3 ^ ((c + 1) * v)) ^ (j + 1) * (n ^ (v - u) * n ^ u) := by rw [e1, hnv]
      _ ≤ 2 ^ v * (3 ^ ((c + 1) * v)) ^ (j + 1) *
            ((2 ^ ((2 * c + 1) * (v - u))) ^ (j + 1) * n ^ u) :=
          Nat.mul_le_mul_left _ (Nat.mul_le_mul_right _ hn)
      _ = 2 ^ v * ((3 ^ ((c + 1) * v)) ^ (j + 1) * (2 ^ ((2 * c + 1) * (v - u))) ^ (j + 1)) *
            n ^ u := by ring
      _ ≤ (2 ^ (2 * c * v)) ^ (j + 1) * n ^ u := Nat.mul_le_mul_right _ key
      _ = (2 ^ (2 * c * (j + 1))) ^ v * n ^ u := by rw [e2]
  -- el término del viento
  have hY : (2 * 3 ^ (2 * c * (j + 1))) ^ v < (2 ^ (2 * c * (j + 1))) ^ v * n ^ u := by
    have hnu : (2 ^ (2 * c * (j + 1))) ^ u ≤ n ^ u := Nat.pow_le_pow_left h1 u
    have hK2' : 3 ^ (2 * c * v) ≤ 2 ^ (2 * c * (u + v)) :=
      le_trans (Nat.le_mul_of_pos_left _ (by positivity)) hK2.le
    have e1 : (2 * 3 ^ (2 * c * (j + 1))) ^ v = (3 ^ (2 * c * v)) ^ j * (2 ^ v * 3 ^ (2 * c * v)) := by
      rw [mul_pow, ← pow_mul, show 2 * c * (j + 1) * v = 2 * c * v * j + 2 * c * v by ring,
        pow_add 3 (2 * c * v * j) (2 * c * v), pow_mul 3 (2 * c * v) j]
      ring
    have e2 : (2 ^ (2 * c * (u + v))) ^ j * 2 ^ (2 * c * (u + v)) =
        (2 ^ (2 * c * (j + 1))) ^ v * (2 ^ (2 * c * (j + 1))) ^ u := by
      rw [← pow_mul, ← pow_add, ← pow_mul, ← pow_mul, ← pow_add]
      congr 1
      ring
    calc (2 * 3 ^ (2 * c * (j + 1))) ^ v = (3 ^ (2 * c * v)) ^ j * (2 ^ v * 3 ^ (2 * c * v)) := e1
      _ < (3 ^ (2 * c * v)) ^ j * 2 ^ (2 * c * (u + v)) :=
          Nat.mul_lt_mul_of_pos_left hK2 (by positivity)
      _ ≤ (2 ^ (2 * c * (u + v))) ^ j * 2 ^ (2 * c * (u + v)) :=
          Nat.mul_le_mul_right _ (Nat.pow_le_pow_left hK2' j)
      _ = (2 ^ (2 * c * (j + 1))) ^ v * (2 ^ (2 * c * (j + 1))) ^ u := e2
      _ ≤ (2 ^ (2 * c * (j + 1))) ^ v * n ^ u := Nat.mul_le_mul_left _ hnu
  -- juntar los dos
  have hsum : 3 ^ ((c + 1) * (j + 1)) * n + 3 ^ (2 * c * (j + 1)) ≤
      2 * max (3 ^ ((c + 1) * (j + 1)) * n) (3 ^ (2 * c * (j + 1))) := by
    have := le_max_left (3 ^ ((c + 1) * (j + 1)) * n) (3 ^ (2 * c * (j + 1)))
    have := le_max_right (3 ^ ((c + 1) * (j + 1)) * n) (3 ^ (2 * c * (j + 1)))
    omega
  have hZ : (2 * max (3 ^ ((c + 1) * (j + 1)) * n) (3 ^ (2 * c * (j + 1)))) ^ v ≤
      (2 ^ (2 * c * (j + 1))) ^ v * n ^ u := by
    rcases le_total (3 ^ ((c + 1) * (j + 1)) * n) (3 ^ (2 * c * (j + 1))) with h | h
    · rw [max_eq_right h]
      exact hY.le
    · rw [max_eq_left h]
      exact hX
  have h5 : (2 ^ (2 * c * (j + 1)) * T^[2 * c * (j + 1)] n) ^ v <
      (2 ^ (2 * c * (j + 1))) ^ v * n ^ u :=
    calc (2 ^ (2 * c * (j + 1)) * T^[2 * c * (j + 1)] n) ^ v
        < (3 ^ ((c + 1) * (j + 1)) * n + 3 ^ (2 * c * (j + 1))) ^ v := Nat.pow_lt_pow_left hT hv
      _ ≤ (2 * max (3 ^ ((c + 1) * (j + 1)) * n) (3 ^ (2 * c * (j + 1)))) ^ v :=
          Nat.pow_le_pow_left hsum v
      _ ≤ (2 ^ (2 * c * (j + 1))) ^ v * n ^ u := hZ
  rw [mul_pow] at h5
  exact Nat.lt_of_mul_lt_mul_left h5

open Classical in
/-- Entre 0 y N−1, los números con al menos `(c+1)m` subidas en sus primeros `2cm` pasos, por
    `((c+1)^(c+1)·c^(c−1))^m`, no pasan de `(N/2^(2cm) + 1)·((2c+1)^(2c))^m`. -/
theorem cuenta_param (N c m : ℕ) (hc : 1 ≤ c) :
    ((Finset.range N).filter fun n => (c + 1) * m ≤ S (2 * c * m) n).card *
        ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m ≤
      (N / 2 ^ (2 * c * m) + 1) * ((2 * c + 1) ^ (2 * c)) ^ m := by
  have h1 := cuenta_por_bloques N (2 * c * m) (fun s => (c + 1) * m ≤ s)
  have h2 := pocos_patrones_pesos (2 * c * m) ((c + 1) * m) (c + 1) c (by omega)
  have hsub : 2 * c * m - (c + 1) * m = (c - 1) * m := by
    obtain ⟨d, rfl⟩ : ∃ d, c = d + 1 := ⟨c - 1, by omega⟩
    rw [Nat.add_sub_cancel]
    apply Nat.sub_eq_of_eq_add
    ring
  have e1 : (c + 1) ^ ((c + 1) * m) * c ^ (2 * c * m - (c + 1) * m) =
      ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m := by
    rw [hsub, mul_pow, ← pow_mul, ← pow_mul]
  have e2 : (c + 1 + c) ^ (2 * c * m) = ((2 * c + 1) ^ (2 * c)) ^ m := by
    rw [show c + 1 + c = 2 * c + 1 by ring, ← pow_mul]
  rw [e1, e2] at h2
  calc ((Finset.range N).filter fun n => (c + 1) * m ≤ S (2 * c * m) n).card *
        ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m
      ≤ ((N / 2 ^ (2 * c * m) + 1) *
          ((Finset.range (2 * c * m)).powerset.filter fun A => (c + 1) * m ≤ A.card).card) *
          ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m := Nat.mul_le_mul_right _ h1
    _ = (N / 2 ^ (2 * c * m) + 1) *
          (((Finset.range (2 * c * m)).powerset.filter fun A => (c + 1) * m ≤ A.card).card *
            ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m) := by rw [Nat.mul_assoc]
    _ ≤ (N / 2 ^ (2 * c * m) + 1) * ((2 * c + 1) ^ (2 * c)) ^ m := Nat.mul_le_mul_left _ h2

open Classical in
/-- **Korec en cifras, con parámetros**: por debajo de `2^((2c+1)m)`, los números que no bajan
    por debajo de `n^(u/v)` en a lo sumo `log₂ n` pasos, por `((c+1)^(c+1)·c^(c−1))^m`, no pasan
    de `2^(2cm)·((c+1)^(c+1)·c^(c−1))^m + (2^m + 1)·((2c+1)^(2c))^m`. -/
theorem cuenta_param_bloque {u v c m : ℕ} (huv : u < v) (hc : 1 ≤ c) (hm : 1 ≤ m)
    (hK1 : 2 ^ v * (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u))) ≤ 2 ^ (2 * c * v))
    (hK2 : 2 ^ v * 3 ^ (2 * c * v) < 2 ^ (2 * c * (u + v))) :
    ((Finset.range (2 ^ ((2 * c + 1) * m))).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u).card *
        ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m ≤
      2 ^ (2 * c * m) * ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m +
        (2 ^ m + 1) * ((2 * c + 1) ^ (2 * c)) ^ m := by
  have hsub : ((Finset.range (2 ^ ((2 * c + 1) * m))).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u) ⊆
      Finset.range (2 ^ (2 * c * m)) ∪
        (Finset.range (2 ^ ((2 * c + 1) * m))).filter fun n => (c + 1) * m ≤ S (2 * c * m) n := by
    intro n hn
    rw [Finset.mem_filter, Finset.mem_range] at hn
    rw [Finset.mem_union, Finset.mem_range, Finset.mem_filter, Finset.mem_range]
    by_cases h1 : n < 2 ^ (2 * c * m)
    · exact Or.inl h1
    · right
      refine ⟨hn.1, ?_⟩
      by_contra hS
      push Not at hS h1
      exact hn.2 ⟨2 * c * m, Nat.le_log_of_pow_le (by norm_num) h1,
        baja_param huv hm hK1 hK2 h1 hn.1 hS⟩
  have hdiv : 2 ^ ((2 * c + 1) * m) / 2 ^ (2 * c * m) = 2 ^ m := by
    rw [Nat.pow_div (Nat.mul_le_mul_right _ (by omega)) (by norm_num)]
    congr 1
    rw [show (2 * c + 1) * m = 2 * c * m + m by ring, Nat.add_sub_cancel_left]
  have hc' := cuenta_param (2 ^ ((2 * c + 1) * m)) c m hc
  rw [hdiv] at hc'
  calc ((Finset.range (2 ^ ((2 * c + 1) * m))).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u).card *
        ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m
      ≤ (Finset.range (2 ^ (2 * c * m)) ∪ (Finset.range (2 ^ ((2 * c + 1) * m))).filter
          fun n => (c + 1) * m ≤ S (2 * c * m) n).card * ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m :=
        Nat.mul_le_mul_right _ (Finset.card_le_card hsub)
    _ ≤ ((Finset.range (2 ^ (2 * c * m))).card + ((Finset.range (2 ^ ((2 * c + 1) * m))).filter
          fun n => (c + 1) * m ≤ S (2 * c * m) n).card) * ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m :=
        Nat.mul_le_mul_right _ (Finset.card_union_le _ _)
    _ = 2 ^ (2 * c * m) * ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m +
          ((Finset.range (2 ^ ((2 * c + 1) * m))).filter
            fun n => (c + 1) * m ≤ S (2 * c * m) n).card * ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m := by
        rw [Finset.card_range, Nat.add_mul]
    _ ≤ 2 ^ (2 * c * m) * ((c + 1) ^ (c + 1) * c ^ (c - 1)) ^ m +
          (2 ^ m + 1) * ((2 * c + 1) ^ (2 * c)) ^ m := Nat.add_le_add_left hc' _

/-! ## La elección del bloque -/

/-- Si `A < B`, para todo `C` hay un `c₀` desde el que `C·A^c < B^c`. -/
theorem existe_potencia {A B : ℕ} (C : ℕ) (hAB : A < B) :
    ∃ c₀, ∀ c, c₀ ≤ c → C * A ^ c < B ^ c := by
  have hB : (0 : ℝ) < B := by exact_mod_cast (lt_of_le_of_lt (Nat.zero_le A) hAB)
  set r : ℝ := (A : ℝ) / B with hr
  have hr0 : 0 ≤ r := div_nonneg (Nat.cast_nonneg A) hB.le
  have hr1 : r < 1 := by
    rw [hr, div_lt_one hB]
    exact_mod_cast hAB
  have hC1 : (0 : ℝ) < (C : ℝ) + 1 := by positivity
  obtain ⟨c₀, hc₀⟩ := exists_pow_lt_of_lt_one (div_pos one_pos hC1) hr1
  refine ⟨c₀, fun c hc => ?_⟩
  have h1 : r ^ c ≤ r ^ c₀ := pow_le_pow_of_le_one hr0 hr1.le hc
  have h2 : r ^ c < 1 / ((C : ℝ) + 1) := lt_of_le_of_lt h1 hc₀
  have hBc : (0 : ℝ) < (B : ℝ) ^ c := pow_pos hB c
  have e : (A : ℝ) ^ c = r ^ c * (B : ℝ) ^ c := by
    rw [hr, div_pow]
    field_simp
  have h4 : ((C : ℝ) + 1) * r ^ c < 1 := by
    have h5 := mul_lt_mul_of_pos_left h2 hC1
    rwa [mul_one_div_cancel hC1.ne'] at h5
  have hrc : 0 ≤ r ^ c := pow_nonneg hr0 c
  have h3 : (C : ℝ) * (A : ℝ) ^ c < (B : ℝ) ^ c := by
    rw [e]
    nlinarith
  exact_mod_cast h3

/-- Los dos márgenes por bloque, escritos como potencias `c`-ésimas. -/
theorem margenes_como_potencias (u v c : ℕ) :
    2 ^ v * (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u))) =
        (2 ^ v * 3 ^ v * 2 ^ (v - u)) * (3 ^ v * 4 ^ (v - u)) ^ c ∧
      2 ^ (2 * c * v) = (4 ^ v) ^ c ∧
      2 ^ v * 3 ^ (2 * c * v) = 2 ^ v * (9 ^ v) ^ c ∧
      2 ^ (2 * c * (u + v)) = (4 ^ (u + v)) ^ c := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [show (c + 1) * v = v * c + v by ring,
      show (2 * c + 1) * (v - u) = 2 * ((v - u) * c) + (v - u) by ring,
      pow_add 3 (v * c) v, pow_add 2 (2 * ((v - u) * c)) (v - u), pow_mul 3 v c,
      pow_mul 2 2 ((v - u) * c), pow_mul (2 ^ 2) (v - u) c,
      show (2 : ℕ) ^ 2 = 4 by norm_num, mul_pow]
    ring
  · rw [show 2 * c * v = 2 * (v * c) by ring, pow_mul 2 2 (v * c), pow_mul (2 ^ 2) v c,
      show (2 : ℕ) ^ 2 = 4 by norm_num]
  · rw [show 2 * c * v = 2 * (v * c) by ring, pow_mul 3 2 (v * c), pow_mul (3 ^ 2) v c,
      show (3 : ℕ) ^ 2 = 9 by norm_num]
  · rw [show 2 * c * (u + v) = 2 * ((u + v) * c) by ring, pow_mul 2 2 ((u + v) * c),
      pow_mul (2 ^ 2) (u + v) c, show (2 : ℕ) ^ 2 = 4 by norm_num]

/-- **Hay bloque**: si `3^v < 4^u` y `u < v`, hay un `c ≥ 1` con los dos márgenes por bloque. -/
theorem existe_bloque {u v : ℕ} (h : 3 ^ v < 4 ^ u) (huv : u < v) :
    ∃ c, 1 ≤ c ∧
      2 ^ v * (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u))) ≤ 2 ^ (2 * c * v) ∧
      2 ^ v * 3 ^ (2 * c * v) < 2 ^ (2 * c * (u + v)) := by
  have hA1 : 3 ^ v * 4 ^ (v - u) < 4 ^ v := by
    have e : 4 ^ v = 4 ^ u * 4 ^ (v - u) := by rw [← pow_add, Nat.add_sub_cancel' huv.le]
    rw [e]
    exact Nat.mul_lt_mul_of_pos_right h (by positivity)
  have hA2 : 9 ^ v < 4 ^ (u + v) := by
    have e1 : (9 : ℕ) ^ v = 3 ^ v * 3 ^ v := by
      rw [← mul_pow]
      norm_num
    have e2 : (4 : ℕ) ^ (u + v) = 4 ^ u * 4 ^ v := pow_add 4 u v
    have h3 : (4 : ℕ) ^ u ≤ 4 ^ v := Nat.pow_le_pow_right (by norm_num) huv.le
    rw [e1, e2]
    calc 3 ^ v * 3 ^ v < 4 ^ u * 4 ^ u := Nat.mul_lt_mul'' h h
      _ ≤ 4 ^ u * 4 ^ v := Nat.mul_le_mul_left _ h3
  obtain ⟨c₁, hc₁⟩ := existe_potencia (2 ^ v * 3 ^ v * 2 ^ (v - u)) hA1
  obtain ⟨c₂, hc₂⟩ := existe_potencia (2 ^ v) hA2
  refine ⟨c₁ + c₂ + 1, by omega, ?_, ?_⟩
  · obtain ⟨e1, e2, -, -⟩ := margenes_como_potencias u v (c₁ + c₂ + 1)
    rw [e1, e2]
    exact (hc₁ _ (by omega)).le
  · obtain ⟨-, -, e3, e4⟩ := margenes_como_potencias u v (c₁ + c₂ + 1)
    rw [e3, e4]
    exact hc₂ _ (by omega)

/-! ## De los bloques a la densidad -/

open Classical in
/-- **Korec con parámetros**: con un bloque que cumpla los dos márgenes, casi toda órbita baja
    por debajo de `n^(u/v)` en a lo sumo `log₂ n` pasos. -/
theorem korec_param {u v c : ℕ} (huv : u < v) (hc : 1 ≤ c)
    (hK1 : 2 ^ v * (3 ^ ((c + 1) * v) * 2 ^ ((2 * c + 1) * (v - u))) ≤ 2 ^ (2 * c * v))
    (hK2 : 2 ^ v * 3 ^ (2 * c * v) < 2 ^ (2 * c * (u + v))) {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N →
      (((Finset.range N).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u).card : ℝ) ≤ ε * N := by
  set E : ℕ → ℕ := fun N => ((Finset.range N).filter fun n =>
    ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u).card with hEdef
  have hE : Monotone E := by
    intro a b hab
    exact Finset.card_le_card (Finset.filter_subset_filter _ (Finset.range_mono hab))
  set K : ℕ := (c + 1) ^ (c + 1) * c ^ (c - 1) with hK
  set R : ℕ := (2 * c + 1) ^ (2 * c) with hR
  set Q : ℕ := 4 ^ c with hQ
  have hC1 : R < Q * K := margen_entropia hc
  have hQpos : 0 < Q := by positivity
  have hKpos : 0 < K := by positivity
  have hQR : (0 : ℝ) < Q := by exact_mod_cast hQpos
  have hKR : (0 : ℝ) < K := by exact_mod_cast hKpos
  have hQKR : (0 : ℝ) < (Q : ℝ) * K := mul_pos hQR hKR
  set ρ : ℝ := (R : ℝ) / ((Q : ℝ) * K) with hρ
  have hρ0 : 0 ≤ ρ := div_nonneg (Nat.cast_nonneg R) hQKR.le
  have hρ1 : ρ < 1 := by
    rw [hρ, div_lt_one hQKR]
    exact_mod_cast hC1
  set f : ℕ → ℝ := fun m => ((1 : ℝ) / 2) ^ m + 2 * ρ ^ m with hfdef
  have hf : ∀ δ : ℝ, 0 < δ → ∃ m₀, ∀ m, m₀ ≤ m → f m ≤ δ := by
    intro δ hδ
    obtain ⟨a, ha⟩ := exists_pow_lt_of_lt_one (div_pos hδ (by norm_num) : (0 : ℝ) < δ / 3) hρ1
    obtain ⟨b, hb⟩ := exists_pow_lt_of_lt_one (div_pos hδ (by norm_num) : (0 : ℝ) < δ / 3)
      (by norm_num : (1 / 2 : ℝ) < 1)
    refine ⟨a + b, fun m hm => ?_⟩
    have h1 : ((1 : ℝ) / 2) ^ m ≤ (1 / 2) ^ b :=
      pow_le_pow_of_le_one (by norm_num) (by norm_num) (by omega)
    have h2 : ρ ^ m ≤ ρ ^ a := pow_le_pow_of_le_one hρ0 hρ1.le (by omega)
    simp only [hfdef]
    linarith
  have hB2 : 2 ≤ 2 ^ (2 * c + 1) := by
    calc 2 = 2 ^ 1 := by norm_num
      _ ≤ 2 ^ (2 * c + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
  have hcota : ∀ m, 2 ≤ m → (E ((2 ^ (2 * c + 1)) ^ m) : ℝ) ≤ f m * ((2 ^ (2 * c + 1) : ℕ) : ℝ) ^ m := by
    intro m hm
    have hblock := cuenta_param_bloque (m := m) huv hc (by omega) hK1 hK2
    have e1 : (2 : ℕ) ^ ((2 * c + 1) * m) = (2 ^ (2 * c + 1)) ^ m := by rw [← pow_mul]
    have e2 : (2 : ℕ) ^ (2 * c * m) = Q ^ m := by
      rw [hQ, ← pow_mul, show 2 * c * m = 2 * (c * m) by ring, pow_mul 2 2 (c * m)]
      norm_num
    rw [e1, e2] at hblock
    have hblockR : (E ((2 ^ (2 * c + 1)) ^ m) : ℝ) * (K : ℝ) ^ m ≤
        (Q : ℝ) ^ m * (K : ℝ) ^ m + ((2 : ℝ) ^ m + 1) * (R : ℝ) ^ m := by
      exact_mod_cast hblock
    have hRm : (R : ℝ) ^ m = (Q : ℝ) ^ m * (K : ℝ) ^ m * ρ ^ m := by
      rw [hρ, div_pow, mul_pow]
      field_simp
    have hKm : (0 : ℝ) < (K : ℝ) ^ m := pow_pos hKR m
    have hQm : (0 : ℝ) ≤ (Q : ℝ) ^ m := (pow_pos hQR m).le
    have hρm : (0 : ℝ) ≤ ρ ^ m := pow_nonneg hρ0 m
    have h1m : (1 : ℝ) ≤ (2 : ℝ) ^ m := one_le_pow₀ (by norm_num)
    have hE1 : (E ((2 ^ (2 * c + 1)) ^ m) : ℝ) ≤
        (Q : ℝ) ^ m + ((2 : ℝ) ^ m + 1) * ((Q : ℝ) ^ m * ρ ^ m) := by
      rw [hRm] at hblockR
      have h6 : (E ((2 ^ (2 * c + 1)) ^ m) : ℝ) * (K : ℝ) ^ m ≤
          ((Q : ℝ) ^ m + ((2 : ℝ) ^ m + 1) * ((Q : ℝ) ^ m * ρ ^ m)) * (K : ℝ) ^ m := by
        linarith [hblockR]
      exact le_of_mul_le_mul_right h6 hKm
    have hBm : ((2 ^ (2 * c + 1) : ℕ) : ℝ) ^ m = (Q : ℝ) ^ m * (2 : ℝ) ^ m := by
      have e3 : (2 : ℕ) ^ (2 * c + 1) = Q * 2 := by
        rw [hQ, pow_succ, show 2 * c = 2 * c by rfl, pow_mul 2 2 c]
        norm_num
      rw [e3]
      push_cast
      rw [mul_pow]
    have hmedio : ((1 : ℝ) / 2) ^ m * (2 : ℝ) ^ m = 1 := by
      rw [← mul_pow]
      norm_num
    have e4 : f m * ((2 ^ (2 * c + 1) : ℕ) : ℝ) ^ m =
        (Q : ℝ) ^ m + 2 * ((2 : ℝ) ^ m * ((Q : ℝ) ^ m * ρ ^ m)) := by
      rw [hBm]
      simp only [hfdef]
      linear_combination (Q : ℝ) ^ m * hmedio
    rw [e4]
    have h7 : ((2 : ℝ) ^ m + 1) * ((Q : ℝ) ^ m * ρ ^ m) ≤
        2 * ((2 : ℝ) ^ m * ((Q : ℝ) ^ m * ρ ^ m)) := by
      have h8 : (0 : ℝ) ≤ (Q : ℝ) ^ m * ρ ^ m := mul_nonneg hQm hρm
      nlinarith
    linarith
  exact densidad_de_bloques E hE (2 ^ (2 * c + 1)) hB2 f hf hcota hε

open Classical in
/-- **El teorema de Korec (1994)**, para todo exponente racional `u/v` entre `log 3/log 4` y 1:
    si `3^v < 4^u` y `u < v`, casi toda órbita baja por debajo de `n^(u/v)` en a lo sumo `log₂ n`
    pasos. Como entre `log 3/log 4 ≈ 0,7925` y cualquier exponente mayor hay un racional, vale
    para todo exponente mayor que `log 3/log 4`. -/
theorem korec {u v : ℕ} (h : 3 ^ v < 4 ^ u) (huv : u < v) {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N →
      (((Finset.range N).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u).card : ℝ) ≤ ε * N := by
  obtain ⟨c, hc, hK1, hK2⟩ := existe_bloque h huv
  exact korec_param huv hc hK1 hK2 hε

open Classical in
/-- **El teorema de Korec (1994), con exponente real**: para todo `θ > log 3/log 4 ≈ 0,7925`,
    casi toda órbita baja por debajo de `n^θ` en a lo sumo `log₂ n` pasos. -/
theorem korec_real {θ : ℝ} (hθ : Real.log 3 / Real.log 4 < θ) {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N →
      (((Finset.range N).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ ((T^[k] n : ℕ) : ℝ) < (n : ℝ) ^ θ).card : ℝ) ≤ ε * N := by
  have hlog3 : 0 < Real.log 3 := Real.log_pos (by norm_num)
  have hlog4 : 0 < Real.log 4 := Real.log_pos (by norm_num)
  have h34 : Real.log 3 / Real.log 4 < 1 := by
    rw [div_lt_one hlog4]
    exact Real.log_lt_log (by norm_num) (by norm_num)
  -- un racional q con log 3/log 4 < q < min θ 1
  obtain ⟨q, hq1, hq2⟩ := exists_rat_btwn (lt_min hθ h34)
  have hq0 : (0 : ℝ) < q := lt_trans (div_pos hlog3 hlog4) hq1
  have hqθ : (q : ℝ) ≤ θ := le_trans hq2.le (min_le_left _ _)
  have hq1' : (q : ℝ) < 1 := lt_of_lt_of_le hq2 (min_le_right _ _)
  have hnum : 0 < q.num := Rat.num_pos.2 (by exact_mod_cast hq0)
  set u : ℕ := q.num.toNat with hu
  set v : ℕ := q.den with hv
  have hvpos : 0 < v := q.den_pos
  have hvR : (0 : ℝ) < v := by exact_mod_cast hvpos
  have hqR : (q : ℝ) = (u : ℝ) / v := by
    have h1 : ((u : ℤ) : ℝ) = (q.num : ℝ) := by
      rw [hu, Int.toNat_of_nonneg hnum.le]
    have h2 := Rat.num_div_den q
    have h3 : (q : ℝ) = (q.num : ℝ) / (q.den : ℝ) := by
      conv_lhs => rw [← h2]
      push_cast
      ring
    rw [h3, ← h1]
    push_cast
    rfl
  -- 3^v < 4^u y u < v
  have hupos : 0 < u := by
    have : (0 : ℝ) < (u : ℝ) / v := by rw [← hqR]; exact hq0
    have h4 : (0 : ℝ) < u := by
      by_contra h5
      push Not at h5
      have : (u : ℝ) / v ≤ 0 := div_nonpos_of_nonpos_of_nonneg h5 hvR.le
      linarith
    exact_mod_cast h4
  have huv : u < v := by
    have : (u : ℝ) / v < 1 := by rw [← hqR]; exact hq1'
    rw [div_lt_one hvR] at this
    exact_mod_cast this
  have h34' : 3 ^ v < 4 ^ u := by
    have h5 : Real.log 3 / Real.log 4 < (u : ℝ) / v := by rw [← hqR]; exact hq1
    rw [div_lt_div_iff₀ hlog4 hvR] at h5
    have h6 : Real.log ((3 : ℝ) ^ v) < Real.log ((4 : ℝ) ^ u) := by
      rw [Real.log_pow, Real.log_pow]
      linarith
    have h7 : ((3 : ℝ) ^ v) < (4 : ℝ) ^ u :=
      (Real.log_lt_log_iff (by positivity) (by positivity)).1 h6
    exact_mod_cast h7
  -- los que no bajan por debajo de n^θ no bajan por debajo de n^(u/v)
  obtain ⟨N₀, hN₀⟩ := korec h34' huv hε
  refine ⟨N₀, fun N hN => le_trans ?_ (hN₀ N hN)⟩
  have hsub : ((Finset.range N).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ ((T^[k] n : ℕ) : ℝ) < (n : ℝ) ^ θ) ⊆
      ((Finset.range N).filter fun n =>
        ¬ ∃ k, k ≤ Nat.log 2 n ∧ (T^[k] n) ^ v < n ^ u) := by
    intro n hn
    rw [Finset.mem_filter] at hn ⊢
    refine ⟨hn.1, ?_⟩
    rintro ⟨k, hk, hlt⟩
    apply hn.2
    refine ⟨k, hk, ?_⟩
    -- n ≥ 1, porque n^u > 0
    have hn1 : 1 ≤ n := by
      rcases Nat.eq_zero_or_pos n with h0 | h0
      · rw [h0, zero_pow (by omega)] at hlt
        exact absurd hlt (Nat.not_lt_zero _)
      · exact h0
    have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn1
    have hltR : ((T^[k] n : ℕ) : ℝ) ^ v < (n : ℝ) ^ u := by exact_mod_cast hlt
    have hT0 : (0 : ℝ) ≤ ((T^[k] n : ℕ) : ℝ) := Nat.cast_nonneg _
    have hvne : v ≠ 0 := by omega
    -- raíz v-ésima
    have h8 : ((T^[k] n : ℕ) : ℝ) < ((n : ℝ) ^ u) ^ ((v : ℝ)⁻¹) := by
      have h9 := Real.rpow_lt_rpow (pow_nonneg hT0 v) hltR (inv_pos.2 hvR)
      rwa [Real.pow_rpow_inv_natCast hT0 hvne] at h9
    have h10 : ((n : ℝ) ^ u) ^ ((v : ℝ)⁻¹) = (n : ℝ) ^ ((u : ℝ) / v) := by
      rw [← Real.rpow_natCast, ← Real.rpow_mul (by positivity), div_eq_mul_inv]
    have h11 : (n : ℝ) ^ ((u : ℝ) / v) ≤ (n : ℝ) ^ θ := by
      apply Real.rpow_le_rpow_of_exponent_le hnR
      rw [← hqR]
      exact hqθ
    rw [h10] at h8
    exact lt_of_lt_of_le h8 h11
  exact_mod_cast Finset.card_le_card hsub

/-! ## La rareza con el exponente de Lagarias -/

/-- `3^6309 < 2^10000`. -/
theorem margen_6309 : (3 : ℕ) ^ 6309 < 2 ^ 10000 := by decide +kernel

/-- Margen de los pesos de la rareza: `10000^10000 ≤ 2^9500·6309^6309·3691^3691`. -/
theorem margen_pesos_lagarias : (10000 : ℕ) ^ 10000 ≤ 2 ^ 9500 * (6309 ^ 6309 * 3691 ^ 3691) := by
  decide +kernel

/-- Si el pronóstico a los `10000m` pasos no bajó de 1, hubo al menos `6309m` subidas. -/
theorem subidas_lagarias {m s : ℕ} (h : 2 ^ (10000 * m) ≤ 3 ^ s) : 6309 * m ≤ s := by
  by_contra hlt
  push Not at hlt
  have h1 : 3 ^ s < 3 ^ (6309 * m) := Nat.pow_lt_pow_right (by norm_num) hlt
  have h2 : (3 : ℕ) ^ (6309 * m) ≤ 2 ^ (10000 * m) := by
    rw [pow_mul 3 6309 m, pow_mul 2 10000 m]
    exact Nat.pow_le_pow_left margen_6309.le m
  omega

open Classical in
/-- **Rareza con el exponente de Lagarias** (su teorema F, 1985, para el primer cruce): entre 0 y
    N−1 hay a lo sumo `(N/2^(10000m) + 1)·2^(9500m)` fugas puras. Por debajo de
    `x = 2^(10000m)` son a lo sumo `2·x^0,95`, frente a las `x^0,96` de `rasgo_pocos`. -/
theorem rareza_lagarias (N m : ℕ) :
    ((Finset.range N).filter FugaPura).card ≤ (N / 2 ^ (10000 * m) + 1) * 2 ^ (9500 * m) := by
  have hsub : (Finset.range N).filter FugaPura ⊆
      (Finset.range N).filter fun n => 6309 * m ≤ S (10000 * m) n := by
    intro n hn
    rw [Finset.mem_filter] at hn ⊢
    exact ⟨hn.1, subidas_lagarias (nunca_cruza hn.2 _)⟩
  have h1 := cuenta_por_bloques N (10000 * m) (fun s => 6309 * m ≤ s)
  have h2 := pocos_patrones_pesos (10000 * m) (6309 * m) 6309 3691 (by norm_num)
  have e1 : (6309 : ℕ) ^ (6309 * m) * 3691 ^ (10000 * m - 6309 * m) =
      (6309 ^ 6309 * 3691 ^ 3691) ^ m := by
    rw [show 10000 * m - 6309 * m = 3691 * m by omega, mul_pow, ← pow_mul, ← pow_mul]
  have e2 : ((6309 : ℕ) + 3691) ^ (10000 * m) = (10000 ^ 10000) ^ m := by
    rw [show (6309 : ℕ) + 3691 = 10000 by norm_num, ← pow_mul]
  rw [e1, e2] at h2
  have h4 : (10000 ^ 10000 : ℕ) ^ m ≤ 2 ^ (9500 * m) * (6309 ^ 6309 * 3691 ^ 3691) ^ m := by
    rw [pow_mul 2 9500 m, ← mul_pow]
    exact Nat.pow_le_pow_left margen_pesos_lagarias m
  have h3 : ((Finset.range (10000 * m)).powerset.filter fun A => 6309 * m ≤ A.card).card ≤
      2 ^ (9500 * m) := by
    have h5 : ((Finset.range (10000 * m)).powerset.filter fun A => 6309 * m ≤ A.card).card *
        (6309 ^ 6309 * 3691 ^ 3691) ^ m ≤ 2 ^ (9500 * m) * (6309 ^ 6309 * 3691 ^ 3691) ^ m :=
      le_trans h2 h4
    exact Nat.le_of_mul_le_mul_right h5 (by positivity)
  calc ((Finset.range N).filter FugaPura).card
      ≤ ((Finset.range N).filter fun n => 6309 * m ≤ S (10000 * m) n).card :=
        Finset.card_le_card hsub
    _ ≤ (N / 2 ^ (10000 * m) + 1) *
          ((Finset.range (10000 * m)).powerset.filter fun A => 6309 * m ≤ A.card).card := h1
    _ ≤ (N / 2 ^ (10000 * m) + 1) * 2 ^ (9500 * m) := Nat.mul_le_mul_left _ h3

end CasaKorec

#print axioms CasaKorec.entropia_real
#print axioms CasaKorec.margen_entropia
#print axioms CasaKorec.baja_param
#print axioms CasaKorec.cuenta_param
#print axioms CasaKorec.cuenta_param_bloque
#print axioms CasaKorec.existe_potencia
#print axioms CasaKorec.margenes_como_potencias
#print axioms CasaKorec.existe_bloque
#print axioms CasaKorec.korec_param
#print axioms CasaKorec.korec
#print axioms CasaKorec.korec_real
#print axioms CasaKorec.margen_6309
#print axioms CasaKorec.margen_pesos_lagarias
#print axioms CasaKorec.subidas_lagarias
#print axioms CasaKorec.rareza_lagarias
