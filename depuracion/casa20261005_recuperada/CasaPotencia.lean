import CasaCasiTodos

/-! # Ahorro de potencia: los que nunca bajan son a lo sumo `N^0,97`

Ruta B, 05-10-2026, sin hipótesis externas. La misma cota de Chernoff con `√3` que da la
densidad cero da también una potencia menor que `N`:

* `fugitivos_en_sinCruce`: si `N ≤ 2^K`, todo fugitivo menor que `N` es un residuo sin
  cruce a los `K` pasos;
* `fugitivos_potencia`: `#fugitivos(N)^20 < (2N)^19` para `N ≥ 2`; es decir, menos de
  `(2N)^0,95` números menores que `N` son fugitivos;
* `potencia_de_bloques`: para toda propiedad *bloqueable* (si `n ≥ 3^J` la tiene, su
  pronóstico no cruza en el paso `J`), `#{n < N : P n}^32 < 5^32 · 3^31 · N^31` para
  `N ≥ 2`, con `bloque_paso` y `bloques_tres` (`5 (3ρ)^J`, `3ρ ≈ 2,898`) por el camino;
* `noDescienden_potencia`: menos de `14,5 N^(31/32)` números menores que `N` nunca bajan de
  sí mismos;
* `fallasCST_potencia`: la conjetura CST de Terras falla en menos de `14,5 N^(31/32)`
  números menores que `N` (`fallasCST_iff` identifica las fallas).

El menor contraejemplo de Collatz, si existe, está en ese conjunto
(`contraejemplo_minimo_no_baja`). No se afirma que el conjunto sea vacío ni finito.

Compilación: `comprobar_fugitivo.py`, en esta carpeta. -/

namespace CasaPotencia

open Ocelotas OcelotasContador CasaPlano CasaFugitivo CasaCasiTodos

/-! ## Constantes -/

theorem raiz_tres_cota : Real.sqrt 3 < 17320509 / 10000000 := by
  have h3 := Real.sq_sqrt (show (0 : ℝ) ≤ 3 by norm_num)
  have h3p := Real.sqrt_nonneg 3
  nlinarith

theorem cuadrado_razon : ((1 + Real.sqrt 3) / Real.sqrt 2) ^ 2 = 2 + Real.sqrt 3 := by
  have h3 := Real.sq_sqrt (show (0 : ℝ) ≤ 3 by norm_num)
  have h1 : (1 + Real.sqrt 3) ^ 2 = 2 * (2 + Real.sqrt 3) := by
    have h : (1 + Real.sqrt 3) ^ 2 = 1 + 2 * Real.sqrt 3 + Real.sqrt 3 ^ 2 := by ring
    rw [h, h3]
    ring
  rw [div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2), h1]
  ring

/-- `((1 + √3)/√2)^20 < 2^19`: el exponente `log₂((1 + √3)/√2) ≈ 0,94998` es menor que
    `0,95`. -/
theorem razon_fugitivos : ((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20 < 2 ^ 19 := by
  have hs := raiz_tres_cota
  calc ((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20
      = (((1 + Real.sqrt 3) / Real.sqrt 2) ^ 2) ^ 10 := by rw [← pow_mul]
    _ = (2 + Real.sqrt 3) ^ 10 := by rw [cuadrado_razon]
    _ < (2 + 17320509 / 10000000) ^ 10 :=
        pow_lt_pow_left₀ (by linarith) (by positivity) (by norm_num)
    _ < 2 ^ 19 := by norm_num

/-- `3ρ ≥ 11/5`, con `ρ = (1 + √3)/(2√2)`. -/
theorem razon_tres_grande : (11 : ℝ) / 5 ≤ 3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) := by
  have h3 := Real.sq_sqrt (show (0 : ℝ) ≤ 3 by norm_num)
  have h2 := Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
  have h3p := Real.sqrt_nonneg 3
  have h2p := Real.sqrt_nonneg 2
  have hs3 : (17 : ℝ) / 10 < Real.sqrt 3 := by nlinarith
  have hs2 : Real.sqrt 2 < 3 / 2 := by nlinarith
  have hpos : (0 : ℝ) < Real.sqrt 2 * 2 := by positivity
  rw [div_div, mul_div_assoc', le_div_iff₀ hpos]
  linarith

/-- `(3ρ)^32 < 3^31`: el exponente `1 + log₃ ρ ≈ 0,9685` es menor que `31/32`. -/
theorem razon_potencia : (3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2)) ^ 32 < 3 ^ 31 := by
  have hs := raiz_tres_cota
  have hsq : (3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2)) ^ 2 = 9 * (2 + Real.sqrt 3) / 4 := by
    rw [mul_pow, div_pow, cuadrado_razon]
    ring
  calc (3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2)) ^ 32
      = ((3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2)) ^ 2) ^ 16 := by rw [← pow_mul]
    _ = (9 * (2 + Real.sqrt 3) / 4) ^ 16 := by rw [hsq]
    _ < (9 * (2 + 17320509 / 10000000) / 4) ^ 16 :=
        pow_lt_pow_left₀ (by linarith) (by positivity) (by norm_num)
    _ < 3 ^ 31 := by norm_num

/-- Escala: si `N ≥ 2`, con `K = log₂(N − 1) + 1` se tiene `2^(K−1) < N ≤ 2^K`. -/
theorem escala {b N : ℕ} (hb : 1 < b) (hN : 2 ≤ N) :
    ∃ K, 1 ≤ K ∧ b ^ (K - 1) < N ∧ N ≤ b ^ K := by
  refine ⟨Nat.log b (N - 1) + 1, by omega, ?_, ?_⟩
  · rw [Nat.add_sub_cancel]
    have := Nat.pow_log_le_self b (show N - 1 ≠ 0 by omega)
    omega
  · have := Nat.lt_pow_succ_log_self hb (N - 1)
    rw [Nat.succ_eq_add_one] at this
    omega

/-! ## Los fugitivos -/

theorem fugitivos_en_sinCruce {N K : ℕ} (hN : N ≤ 2 ^ K) : fugitivos N ⊆ sinCruce K := by
  classical
  intro n hn
  have hn' : n < N ∧ FugaPura n := by simpa [fugitivos] using hn
  exact Finset.mem_filter.2 ⟨Finset.mem_range.2 (lt_of_lt_of_le hn'.1 hN), fugitivo_sube hn'.2 K⟩

/-- **Fugitivos, con ahorro de potencia.** Para `N ≥ 2`, `#fugitivos(N)^20 < (2N)^19`: hay
    menos de `(2N)^0,95` fugitivos menores que `N`. -/
theorem fugitivos_potencia {N : ℕ} (hN : 2 ≤ N) :
    ((fugitivos N).card : ℝ) ^ 20 < (2 * N) ^ 19 := by
  obtain ⟨K, hK1, hlow, hhigh⟩ := escala (show 1 < 2 by norm_num) hN
  have hc : ((fugitivos N).card : ℝ) ≤ ((1 + Real.sqrt 3) / Real.sqrt 2) ^ K :=
    le_trans (by exact_mod_cast Finset.card_le_card (fugitivos_en_sinCruce hhigh))
      (cota_sinCruce K)
  have h2K : (2 : ℝ) ^ K < 2 * N := by
    have : 2 ^ K = 2 * 2 ^ (K - 1) := by
      rw [← pow_succ']
      congr 1
      omega
    have h' : 2 ^ K < 2 * N := by omega
    exact_mod_cast h'
  calc ((fugitivos N).card : ℝ) ^ 20
      ≤ (((1 + Real.sqrt 3) / Real.sqrt 2) ^ K) ^ 20 :=
        pow_le_pow_left₀ (by positivity) hc 20
    _ = (((1 + Real.sqrt 3) / Real.sqrt 2) ^ 20) ^ K := by rw [← pow_mul, ← pow_mul, mul_comm]
    _ < ((2 : ℝ) ^ 19) ^ K := pow_lt_pow_left₀ razon_fugitivos (by positivity) (by omega)
    _ = ((2 : ℝ) ^ K) ^ 19 := by rw [← pow_mul, ← pow_mul, mul_comm]
    _ ≤ (2 * N) ^ 19 := pow_le_pow_left₀ (by positivity) h2K.le 19

/-! ## Los que nunca bajan de sí mismos -/

/-- El menor contraejemplo de Collatz (con el atajo), si existe, nunca baja de sí mismo. -/
theorem contraejemplo_minimo_no_baja {n : ℕ} (hn : 2 ≤ n) (h : ¬ LlegaT n)
    (hmin : ∀ m, 1 ≤ m → m < n → LlegaT m) : ¬ Desciende n := by
  rintro ⟨k, -, hk⟩
  obtain ⟨j, hj⟩ := hmin (T^[k] n) (iter_pos (by omega) k) hk
  exact h ⟨j + k, by rw [Function.iterate_add_apply, hj]⟩

/-- Una propiedad es **bloqueable** si todo `n ≥ 3^J` que la tiene conserva el pronóstico
    sin cruce en el paso `J`. -/
def Bloqueable (P : ℕ → Prop) : Prop := ∀ n J, P n → 3 ^ J ≤ n → 2 ^ J ≤ 3 ^ S J n

/-- El bloque `[3^J, 3^(J+1))` aporta a lo sumo `(3^(J+1)/2^J + 1) c_J`. -/
theorem bloque_paso (P : ℕ → Prop) [DecidablePred P] (hP : Bloqueable P) (J : ℕ) :
    ((Finset.range (3 ^ (J + 1))).filter P).card ≤
      ((Finset.range (3 ^ J)).filter P).card + (3 ^ (J + 1) / 2 ^ J + 1) * (sinCruce J).card := by
  have hsub : (Finset.range (3 ^ (J + 1))).filter P ⊆ (Finset.range (3 ^ J)).filter P ∪
      (Finset.range (3 ^ (J + 1))).filter fun n => 2 ^ J ≤ 3 ^ S J n := by
    intro n hn
    rw [Finset.mem_filter, Finset.mem_range] at hn
    rw [Finset.mem_union, Finset.mem_filter, Finset.mem_filter, Finset.mem_range,
      Finset.mem_range]
    by_cases hk : n < 3 ^ J
    · exact Or.inl ⟨hk, hn.2⟩
    · exact Or.inr ⟨hn.1, hP n J hn.2 (not_lt.mp hk)⟩
  calc ((Finset.range (3 ^ (J + 1))).filter P).card
      ≤ ((Finset.range (3 ^ J)).filter P ∪
          (Finset.range (3 ^ (J + 1))).filter fun n => 2 ^ J ≤ 3 ^ S J n).card :=
        Finset.card_le_card hsub
    _ ≤ ((Finset.range (3 ^ J)).filter P).card +
          ((Finset.range (3 ^ (J + 1))).filter fun n => 2 ^ J ≤ 3 ^ S J n).card :=
        Finset.card_union_le _ _
    _ ≤ _ := Nat.add_le_add_left (filtro_por_residuos _ J) _

/-- `#{n < 3^J : P n} ≤ 5 (3ρ)^J` para toda propiedad bloqueable. -/
theorem bloques_tres (P : ℕ → Prop) [DecidablePred P] (hP : Bloqueable P) (J : ℕ) :
    (((Finset.range (3 ^ J)).filter P).card : ℝ) ≤
      5 * (3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2)) ^ J := by
  obtain ⟨ρ, hρ⟩ : ∃ ρ : ℝ, ρ = (1 + Real.sqrt 3) / Real.sqrt 2 / 2 := ⟨_, rfl⟩
  rw [← hρ]
  have hx : (11 : ℝ) / 5 ≤ 3 * ρ := by rw [hρ]; exact razon_tres_grande
  induction J with
  | zero =>
    have h : ((Finset.range (3 ^ 0)).filter P).card ≤ 1 :=
      le_trans (Finset.card_filter_le _ _) (by simp)
    have h' : (((Finset.range (3 ^ 0)).filter P).card : ℝ) ≤ 1 := by exact_mod_cast h
    simp only [pow_zero, mul_one] at h' ⊢
    linarith
  | succ J ih =>
    have hpaso : (((Finset.range (3 ^ (J + 1))).filter P).card : ℝ) ≤
        ((Finset.range (3 ^ J)).filter P).card +
          (((3 ^ (J + 1) / 2 ^ J : ℕ) : ℝ) + 1) * (sinCruce J).card := by
      exact_mod_cast bloque_paso P hP J
    have h23 : 2 ^ J ≤ 3 ^ (J + 1) :=
      le_trans (Nat.pow_le_pow_left (by norm_num) J) (Nat.pow_le_pow_right (by norm_num) (by omega))
    have hb := cota_bloques h23
    rw [← hρ] at hb
    have hb' : (((3 ^ (J + 1) / 2 ^ J : ℕ) : ℝ) + 1) * (sinCruce J).card ≤
        6 * (3 * ρ) ^ J := by
      calc (((3 ^ (J + 1) / 2 ^ J : ℕ) : ℝ) + 1) * (sinCruce J).card
          ≤ 2 * ρ ^ J * ((3 ^ (J + 1) : ℕ) : ℝ) := hb
        _ = 6 * (3 * ρ) ^ J := by push_cast; ring
    have hpow : (0 : ℝ) ≤ (3 * ρ) ^ J := pow_nonneg (by linarith) J
    calc (((Finset.range (3 ^ (J + 1))).filter P).card : ℝ)
        ≤ 5 * (3 * ρ) ^ J + 6 * (3 * ρ) ^ J := by linarith
      _ = 11 * (3 * ρ) ^ J := by ring
      _ ≤ 5 * (3 * ρ) * (3 * ρ) ^ J := by nlinarith
      _ = 5 * (3 * ρ) ^ (J + 1) := by ring

/-- **Ahorro de potencia por bloques.** Para toda propiedad bloqueable y `N ≥ 2`,
    `#{n < N : P n}^32 < 5^32 · 3^31 · N^31`. -/
theorem potencia_de_bloques (P : ℕ → Prop) [DecidablePred P] (hP : Bloqueable P) {N : ℕ}
    (hN : 2 ≤ N) : (((Finset.range N).filter P).card : ℝ) ^ 32 < 5 ^ 32 * 3 ^ 31 * N ^ 31 := by
  set x := 3 * ((1 + Real.sqrt 3) / Real.sqrt 2 / 2) with hx
  obtain ⟨J, hJ1, hlow, hhigh⟩ := escala (show 1 < 3 by norm_num) hN
  have hmono : (Finset.range N).filter P ⊆ (Finset.range (3 ^ J)).filter P :=
    Finset.filter_subset_filter P (Finset.range_subset_range.2 hhigh)
  have hc : (((Finset.range N).filter P).card : ℝ) ≤ 5 * x ^ J :=
    le_trans (by exact_mod_cast Finset.card_le_card hmono) (bloques_tres P hP J)
  have hx0 : (0 : ℝ) ≤ x := by positivity
  have hlowr : (3 : ℝ) ^ (J - 1) < N := by exact_mod_cast hlow
  calc (((Finset.range N).filter P).card : ℝ) ^ 32
      ≤ (5 * x ^ J) ^ 32 := pow_le_pow_left₀ (by positivity) hc 32
    _ = 5 ^ 32 * (x ^ 32) ^ J := by rw [mul_pow, ← pow_mul, ← pow_mul, mul_comm J]
    _ < 5 ^ 32 * ((3 : ℝ) ^ 31) ^ J := by
        have h : (x ^ 32) ^ J < ((3 : ℝ) ^ 31) ^ J :=
          pow_lt_pow_left₀ razon_potencia (by positivity) (show J ≠ 0 by omega)
        exact mul_lt_mul_of_pos_left h (by positivity)
    _ = 5 ^ 32 * 3 ^ 31 * ((3 : ℝ) ^ (J - 1)) ^ 31 := by
        rw [← pow_mul, ← pow_mul, mul_assoc, ← pow_add]
        congr 2
        omega
    _ ≤ 5 ^ 32 * 3 ^ 31 * N ^ 31 := by
        have := pow_le_pow_left₀ (by positivity) hlowr.le 31
        nlinarith

/-- No bajar nunca de sí mismo es bloqueable. -/
theorem noDesciende_bloqueable : Bloqueable fun n => ¬ Desciende n := by
  intro n J hn hJ
  by_contra hc
  exact hn (desciende_de_grande (not_le.mp hc) hJ)

/-- **Los que nunca bajan, con ahorro de potencia.** Para `N ≥ 2`,
    `#noDescienden(N)^32 < 5^32 · 3^31 · N^31`: menos de `14,5 N^(31/32)` números menores
    que `N` nunca bajan de sí mismos. -/
theorem noDescienden_potencia {N : ℕ} (hN : 2 ≤ N) :
    ((noDescienden N).card : ℝ) ^ 32 < 5 ^ 32 * 3 ^ 31 * N ^ 31 := by
  classical
  exact potencia_de_bloques _ noDesciende_bloqueable hN

open Classical in
/-- Números menores que `N` en los que falla la conjetura CST: tienen primer cruce `k`, pero
    no bajan de sí mismos en el paso `k`. -/
noncomputable def fallasCST (N : ℕ) : Finset ℕ :=
  (Finset.range N).filter fun n => ∃ k, PrimerCruce n k ∧ n ≤ T^[k] n

/-- Fallar en CST es bloqueable: el primer cruce de una falla `n ≥ 3^J` es posterior a `J`. -/
theorem fallaCST_bloqueable : Bloqueable fun n => ∃ k, PrimerCruce n k ∧ n ≤ T^[k] n := by
  rintro n J ⟨k, ⟨hpre, hc⟩, hge⟩ hJ
  by_cases hJk : J < k
  · rcases Nat.eq_zero_or_pos J with h0 | h0
    · subst h0
      simp [S]
    · exact hpre J hJk h0
  · exfalso
    have h3 : 3 ^ k ≤ n := le_trans (Nat.pow_le_pow_right (by norm_num) (not_lt.mp hJk)) hJ
    have := desciende_de_cruce_grande hc h3
    omega

/-- **CST casi siempre, con ahorro de potencia.** Para `N ≥ 2`, la conjetura CST de Terras
    falla en menos de `14,5 N^(31/32)` números menores que `N`. -/
theorem fallasCST_potencia {N : ℕ} (hN : 2 ≤ N) :
    ((fallasCST N).card : ℝ) ^ 32 < 5 ^ 32 * 3 ^ 31 * N ^ 31 := by
  classical
  exact potencia_de_bloques _ fallaCST_bloqueable hN

/-- Las fallas de CST son exactamente los `n` donde no vale su enunciado puntual. -/
theorem fallasCST_iff {N n : ℕ} :
    n ∈ fallasCST N ↔ n < N ∧ ¬ ∀ k, PrimerCruce n k → T^[k] n < n := by
  classical
  simp only [fallasCST, Finset.mem_filter, Finset.mem_range, not_forall, not_lt, exists_prop]

end CasaPotencia

#print axioms CasaPotencia.razon_fugitivos
#print axioms CasaPotencia.razon_potencia
#print axioms CasaPotencia.fugitivos_en_sinCruce
#print axioms CasaPotencia.fugitivos_potencia
#print axioms CasaPotencia.contraejemplo_minimo_no_baja
#print axioms CasaPotencia.bloque_paso
#print axioms CasaPotencia.bloques_tres
#print axioms CasaPotencia.potencia_de_bloques
#print axioms CasaPotencia.noDescienden_potencia
#print axioms CasaPotencia.fallaCST_bloqueable
#print axioms CasaPotencia.fallasCST_potencia
#print axioms CasaPotencia.fallasCST_iff
