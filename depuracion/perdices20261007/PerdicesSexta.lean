import PerdicesTamano
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-! # Perdices: la sexta raíz y el techo que sube

Atajo T de Ocelotas: `T(x) = x/2` si x es par y `(3x+1)/2` si es impar. `S k n` cuenta
las subidas (entradas impares) antes del instante k y el pronóstico es `P_k = 3^S/2^k`.
`normalizado n k = T^k(n)/P_k` es el tamaño normalizado `R_k` de `PerdicesTamano`.

Este archivo completa en Lean la prueba escrita de TAMANO.md («Segunda vía»):

* `impar_mayor`: entre q impares distintos, todos al menos 3, el mayor vale al menos 2q+1;
* `producto_sexta`: para esos impares, `(∏ (1 + 1/(3a)))^6 ≤ q + 1`; inducción quitando
  el mayor, con `factor_sexta` como paso del telescopio;
* `sexta_raiz_general`: `R_k^6 ≤ n^6 (S_k + 1)` si las entradas impares de los k primeros
  pasos son distintas y al menos 3; `sexta_raiz`: lo mismo para toda fuga pura;
* `sexta_raiz_nat`: la misma cota en naturales, `(2^k T^k(n))^6 ≤ (3^S)^6 n^6 (S_k + 1)`;
* `regreso_sexta`: si `P_k ≤ c`, entonces `T^k(n)^6 ≤ c^6 n^6 (S_k + 1)`;
* `cuenta_regresos`: hay a lo sumo `c n K^(1/6)` tiempos `j < K` con `P_j ≤ c`
  (enunciado elevado a la sexta);
* `regreso_sexta_real`, `cuenta_regresos_real` y `cuenta_regresos_raiz`: lo mismo con
  un techo real `C ≥ 0`; la última da a lo sumo `⌊C n K^(1/6)⌋` regresos;
* `techo_sube` (rasgo 9): en algún instante `j < K`, el pronóstico de una fuga pura
  vale al menos `K^(5/6)/n`; `techo_sube_real` lo enuncia con la raíz.

Sin hipótesis analíticas adicionales. Véase TAMANO.md.
-/

namespace PerdicesSexta

open Ocelotas CasaPlano CasaRetrato PerdicesEstela PerdicesTamano
open scoped BigOperators

/-! ## El lema finito -/

/-- Entre `q` impares distintos, todos al menos 3, el mayor vale al menos `2q + 1`. -/
theorem impar_mayor {A : Finset ℕ} {a : ℕ} (ha : a ∈ A) (hmax : ∀ x ∈ A, x ≤ a)
    (himp : ∀ x ∈ A, x % 2 = 1 ∧ 3 ≤ x) : 2 * A.card + 1 ≤ a := by
  have hc : A.card ≤ (Finset.Icc 1 (a / 2)).card := by
    apply Finset.card_le_card_of_injOn (fun x => x / 2)
    · intro x hx
      have h1 := himp x hx
      have h2 := hmax x hx
      simp only [Finset.coe_Icc, Set.mem_Icc]
      omega
    · intro x hx y hy hxy
      have h1 := (himp x hx).1
      have h2 := (himp y hy).1
      simp only at hxy
      omega
  rw [Nat.card_Icc] at hc
  have := (himp a ha).1
  omega

/-- **Telescopio.** Para impares distintos, todos al menos 3,
    `(∏ (1 + 1/(3a)))^6 ≤ q + 1`, con `q` la cantidad. Inducción quitando el mayor. -/
theorem producto_sexta (A : Finset ℕ) :
    (∀ x ∈ A, x % 2 = 1 ∧ 3 ≤ x) →
      (∏ x ∈ A, (1 + 1 / (3 * (x : ℝ)))) ^ 6 ≤ A.card + 1 := by
  induction A using Finset.induction_on_max with
  | empty => intro _; simp
  | insert a s hlt ih =>
    intro himp
    have has : a ∉ s := fun h => lt_irrefl a (hlt a h)
    have hP := ih fun x hx => himp x (Finset.mem_insert_of_mem hx)
    have hbig : 2 * (insert a s).card + 1 ≤ a :=
      impar_mayor (Finset.mem_insert_self a s)
        (fun x hx => by
          rcases Finset.mem_insert.1 hx with rfl | hx
          · exact le_rfl
          · exact (hlt x hx).le)
        himp
    rw [Finset.card_insert_of_notMem has] at hbig ⊢
    rw [Finset.prod_insert has, mul_pow]
    set r := s.card + 1 with hr
    have hra : (2 * (r : ℝ) + 1) ≤ (a : ℝ) := by exact_mod_cast hbig
    have hpos : (0 : ℝ) < 6 * r + 3 := by positivity
    have hf : 1 + 1 / (3 * (a : ℝ)) ≤ (6 * r + 4) / (6 * r + 3) := by
      have h1 : 1 / (3 * (a : ℝ)) ≤ 1 / (6 * r + 3) :=
        one_div_le_one_div_of_le hpos (by linarith)
      have h2 : (6 * (r : ℝ) + 4) / (6 * r + 3) = 1 + 1 / (6 * r + 3) := by
        field_simp
        ring
      linarith
    have hf6 : (1 + 1 / (3 * (a : ℝ))) ^ 6 ≤ ((6 * r + 4) / (6 * r + 3)) ^ 6 :=
      pow_le_pow_left₀ (by positivity) hf 6
    have hfac : ((6 * (r : ℝ) + 4) / (6 * r + 3)) ^ 6 * r ≤ r + 1 := by
      have hn : (r : ℝ) * (6 * r + 4) ^ 6 ≤ (r + 1) * (6 * r + 3) ^ 6 := by
        exact_mod_cast factor_sexta r
      rw [div_pow, div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
      linarith
    have hPr : (∏ x ∈ s, (1 + 1 / (3 * (x : ℝ)))) ^ 6 ≤ r := by
      rw [hr]
      push_cast
      exact hP
    calc (1 + 1 / (3 * (a : ℝ))) ^ 6 * (∏ x ∈ s, (1 + 1 / (3 * (x : ℝ)))) ^ 6
        ≤ ((6 * r + 4) / (6 * r + 3)) ^ 6 * r :=
          mul_le_mul hf6 hPr (by positivity) (by positivity)
      _ ≤ r + 1 := hfac

/-! ## La sexta raíz -/

/-- **Sexta raíz, versión general.** Si las entradas impares de los `k` primeros pasos son
    distintas y todas al menos 3, entonces `R_k^6 ≤ n^6 (S_k + 1)`. -/
theorem sexta_raiz_general {n k : ℕ} (hn : 0 < n)
    (hiny : Set.InjOn (fun j => T^[j] n) (subidas k n))
    (htres : ∀ j ∈ subidas k n, 3 ≤ T^[j] n) :
    normalizado n k ^ 6 ≤ (n : ℝ) ^ 6 * (S k n + 1) := by
  have hprod : (∏ j ∈ Finset.range k,
      (if T^[j] n % 2 = 1 then 1 + 1 / (3 * (T^[j] n : ℝ)) else 1)) =
      ∏ x ∈ (subidas k n).image (fun j => T^[j] n), (1 + 1 / (3 * (x : ℝ))) := by
    rw [Finset.prod_image hiny, subidas, Finset.prod_filter]
  have hA : ∀ x ∈ (subidas k n).image (fun j => T^[j] n), x % 2 = 1 ∧ 3 ≤ x := by
    intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hx
    exact ⟨(Finset.mem_filter.1 hj).2, htres j hj⟩
  have hcard : ((subidas k n).image (fun j => T^[j] n)).card = S k n := by
    rw [Finset.card_image_of_injOn hiny, card_subidas]
  have h6 := producto_sexta _ hA
  rw [hcard] at h6
  rw [identidad_producto hn, hprod, mul_pow]
  exact mul_le_mul_of_nonneg_left h6 (by positivity)

/-- **Sexta raíz de una fuga pura:** `R_k^6 ≤ n^6 (S_k + 1)` en todo instante. -/
theorem sexta_raiz {n : ℕ} (h : FugaPura n) (k : ℕ) :
    normalizado n k ^ 6 ≤ (n : ℝ) ^ 6 * (S k n + 1) := by
  have hn2 := fuga_pura_dos h
  apply sexta_raiz_general (by omega)
  · intro i _ j _ hij
    exact rasgo_inyectiva h hij
  · intro j hj
    have hodd := (Finset.mem_filter.1 hj).2
    have hge := fuga_pura_no_baja h j
    omega

/-- La sexta raíz en naturales: `(2^k T^k(n))^6 ≤ (3^S)^6 n^6 (S_k + 1)`. -/
theorem sexta_raiz_nat {n : ℕ} (h : FugaPura n) (k : ℕ) :
    (2 ^ k * T^[k] n) ^ 6 ≤ (3 ^ S k n) ^ 6 * (n ^ 6 * (S k n + 1)) := by
  have hr := sexta_raiz h k
  unfold normalizado inverso at hr
  rw [div_mul_eq_mul_div, div_pow, div_le_iff₀ (by positivity)] at hr
  have hc : (((2 ^ k * T^[k] n) ^ 6 : ℕ) : ℝ) ≤
      (((3 ^ S k n) ^ 6 * (n ^ 6 * (S k n + 1)) : ℕ) : ℝ) := by
    push_cast
    linarith
  exact_mod_cast hc

/-! ## Regresos y techo -/

/-- **Regresos.** Si `3^S ≤ c·2^k` (pronóstico a lo sumo `c`), entonces
    `T^k(n)^6 ≤ c^6 n^6 (S_k + 1)`. -/
theorem regreso_sexta {n k c : ℕ} (h : FugaPura n) (hk : 3 ^ S k n ≤ c * 2 ^ k) :
    (T^[k] n) ^ 6 ≤ c ^ 6 * n ^ 6 * (S k n + 1) := by
  have h1 := sexta_raiz_nat h k
  have h2 : (3 ^ S k n) ^ 6 ≤ (c * 2 ^ k) ^ 6 := Nat.pow_le_pow_left hk 6
  have h3 : (2 ^ k) ^ 6 * (T^[k] n) ^ 6 ≤ (2 ^ k) ^ 6 * (c ^ 6 * n ^ 6 * (S k n + 1)) := by
    calc (2 ^ k) ^ 6 * (T^[k] n) ^ 6 = (2 ^ k * T^[k] n) ^ 6 := by ring
      _ ≤ (3 ^ S k n) ^ 6 * (n ^ 6 * (S k n + 1)) := h1
      _ ≤ (c * 2 ^ k) ^ 6 * (n ^ 6 * (S k n + 1)) := Nat.mul_le_mul_right _ h2
      _ = (2 ^ k) ^ 6 * (c ^ 6 * n ^ 6 * (S k n + 1)) := by ring
  exact Nat.le_of_mul_le_mul_left h3 (by positivity)

/-- Entre `N` naturales distintos, todos al menos 1, alguno vale al menos `N`. -/
theorem existe_grande {B : Finset ℕ} (hB : B.Nonempty) (h1 : ∀ x ∈ B, 1 ≤ x) :
    ∃ v ∈ B, B.card ≤ v := by
  refine ⟨B.max' hB, B.max'_mem hB, ?_⟩
  have hsub : B ⊆ Finset.Icc 1 (B.max' hB) := by
    intro x hx
    rw [Finset.mem_Icc]
    exact ⟨h1 x hx, B.le_max' x hx⟩
  have hc := Finset.card_le_card hsub
  rw [Nat.card_Icc] at hc
  omega

/-- **Cuenta de regresos.** Hay a lo sumo `c n K^(1/6)` tiempos `j < K` con pronóstico a lo
    sumo `c`; aquí, elevado a la sexta. -/
theorem cuenta_regresos {n : ℕ} (h : FugaPura n) (c K : ℕ) :
    ((Finset.range K).filter fun j => 3 ^ S j n ≤ c * 2 ^ j).card ^ 6 ≤
      c ^ 6 * n ^ 6 * K := by
  rcases ((Finset.range K).filter fun j => 3 ^ S j n ≤ c * 2 ^ j).eq_empty_or_nonempty
    with h0 | hne
  · rw [h0]
    simp
  · have hiny : Set.InjOn (fun j => T^[j] n)
        ((Finset.range K).filter fun j => 3 ^ S j n ≤ c * 2 ^ j) :=
      fun i _ j _ hij => rasgo_inyectiva h hij
    have hn2 := fuga_pura_dos h
    obtain ⟨v, hv, hcard⟩ := existe_grande (hne.image (fun j => T^[j] n))
      (fun x hx => by
        obtain ⟨j, -, rfl⟩ := Finset.mem_image.1 hx
        have := fuga_pura_no_baja h j
        omega)
    rw [Finset.card_image_of_injOn hiny] at hcard
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hv
    have hj' := Finset.mem_filter.1 hj
    have hjK := Finset.mem_range.1 hj'.1
    have hS : S j n + 1 ≤ K := by
      have := S_le_pasos j n
      omega
    calc ((Finset.range K).filter fun j => 3 ^ S j n ≤ c * 2 ^ j).card ^ 6
        ≤ (T^[j] n) ^ 6 := Nat.pow_le_pow_left hcard 6
      _ ≤ c ^ 6 * n ^ 6 * (S j n + 1) := regreso_sexta h hj'.2
      _ ≤ c ^ 6 * n ^ 6 * K := Nat.mul_le_mul_left _ hS

/-- **Rasgo 9: el techo sube.** Antes del tiempo `K`, el pronóstico de una fuga pura
    alcanzó al menos `K^(5/6)/n`: hay `j < K` con `K^5 · 2^(6j) ≤ n^6 · 3^(6 S_j)`. -/
theorem techo_sube {n K : ℕ} (h : FugaPura n) (hK : 1 ≤ K) :
    ∃ j < K, K ^ 5 * 2 ^ (6 * j) ≤ n ^ 6 * 3 ^ (6 * S j n) := by
  have hn2 := fuga_pura_dos h
  have hiny : Set.InjOn (fun j => T^[j] n) (Finset.range K) :=
    fun i _ j _ hij => rasgo_inyectiva h hij
  have hne : (Finset.range K).Nonempty := Finset.nonempty_range_iff.2 (by omega)
  obtain ⟨v, hv, hcard⟩ := existe_grande (hne.image (fun j => T^[j] n))
    (fun x hx => by
      obtain ⟨j, -, rfl⟩ := Finset.mem_image.1 hx
      have := fuga_pura_no_baja h j
      omega)
  rw [Finset.card_image_of_injOn hiny, Finset.card_range] at hcard
  obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hv
  have hjK := Finset.mem_range.1 hj
  refine ⟨j, hjK, ?_⟩
  have h1 := sexta_raiz_nat h j
  have hS : S j n + 1 ≤ K := by
    have := S_le_pasos j n
    omega
  have h2 : (2 ^ j * K) ^ 6 ≤ (2 ^ j * T^[j] n) ^ 6 :=
    Nat.pow_le_pow_left (Nat.mul_le_mul_left _ hcard) 6
  have h3 : K * (K ^ 5 * 2 ^ (6 * j)) ≤ K * (n ^ 6 * 3 ^ (6 * S j n)) := by
    calc K * (K ^ 5 * 2 ^ (6 * j)) = (2 ^ j * K) ^ 6 := by ring
      _ ≤ (2 ^ j * T^[j] n) ^ 6 := h2
      _ ≤ (3 ^ S j n) ^ 6 * (n ^ 6 * (S j n + 1)) := h1
      _ ≤ (3 ^ S j n) ^ 6 * (n ^ 6 * K) := by gcongr
      _ = K * (n ^ 6 * 3 ^ (6 * S j n)) := by ring
  exact Nat.le_of_mul_le_mul_left h3 (by omega)

/-- El rasgo 9 con la raíz: antes del tiempo `K`, el pronóstico `3^S/2^j` alcanzó al
    menos `K^(5/6)/n`. -/
theorem techo_sube_real {n K : ℕ} (h : FugaPura n) (hK : 1 ≤ K) :
    ∃ j < K, (K : ℝ) ^ ((5 : ℝ) / 6) / n ≤ (3 : ℝ) ^ S j n / 2 ^ j := by
  obtain ⟨j, hj, hle⟩ := techo_sube h hK
  refine ⟨j, hj, ?_⟩
  have hn : (0 : ℝ) < n := by
    have := fuga_pura_dos h
    exact_mod_cast (show 0 < n by omega)
  have h5 : ((K : ℝ) ^ ((5 : ℝ) / 6)) ^ 6 = (K : ℝ) ^ 5 := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by positivity)]
    norm_num
  have hc : ((K ^ 5 * 2 ^ (6 * j) : ℕ) : ℝ) ≤ ((n ^ 6 * 3 ^ (6 * S j n) : ℕ) : ℝ) := by
    exact_mod_cast hle
  have h6 : ((K : ℝ) ^ ((5 : ℝ) / 6) * 2 ^ j) ^ 6 ≤ ((3 : ℝ) ^ S j n * n) ^ 6 := by
    rw [mul_pow, mul_pow, h5, ← pow_mul, ← pow_mul]
    push_cast at hc
    rw [mul_comm j 6, mul_comm (S j n) 6]
    linarith
  rw [div_le_div_iff₀ hn (by positivity)]
  exact (pow_le_pow_iff_left₀ (by positivity) (by positivity) (by norm_num)).1 h6


/-! ## Techo real -/

/-- **Regresos con techo real.** Si `3^S ≤ C·2^k`, es decir `P_k ≤ C`, entonces
    `T^k(n)^6 ≤ C^6 n^6 (S_k + 1)`. -/
theorem regreso_sexta_real {n k : ℕ} {C : ℝ} (h : FugaPura n)
    (hk : (3 : ℝ) ^ S k n ≤ C * 2 ^ k) :
    (T^[k] n : ℝ) ^ 6 ≤ C ^ 6 * n ^ 6 * (S k n + 1) := by
  have hr := sexta_raiz h k
  have hP : (0 : ℝ) ≤ (3 : ℝ) ^ S k n / 2 ^ k := by positivity
  have hPC : (3 : ℝ) ^ S k n / 2 ^ k ≤ C := by
    rw [div_le_iff₀ (by positivity)]
    exact hk
  have hx : (T^[k] n : ℝ) = (3 : ℝ) ^ S k n / 2 ^ k * normalizado n k := by
    unfold normalizado inverso
    field_simp
  rw [hx, mul_pow]
  calc ((3 : ℝ) ^ S k n / 2 ^ k) ^ 6 * normalizado n k ^ 6
      ≤ C ^ 6 * ((n : ℝ) ^ 6 * (S k n + 1)) :=
        mul_le_mul (pow_le_pow_left₀ hP hPC 6) hr (by positivity) (by positivity)
    _ = C ^ 6 * n ^ 6 * (S k n + 1) := by ring

/-- La cuenta de regresos con techo real `C`, elevada a la sexta. -/
theorem cuenta_regresos_real {n : ℕ} (h : FugaPura n) (C : ℝ) (K : ℕ) :
    (((Finset.range K).filter fun j => (3 : ℝ) ^ S j n ≤ C * 2 ^ j).card : ℝ) ^ 6 ≤
      C ^ 6 * n ^ 6 * K := by
  rcases ((Finset.range K).filter fun j => (3 : ℝ) ^ S j n ≤ C * 2 ^ j).eq_empty_or_nonempty
    with h0 | hne
  · rw [h0]
    simp only [Finset.card_empty, Nat.cast_zero]
    norm_num
    positivity
  · have hiny : Set.InjOn (fun j => T^[j] n)
        ((Finset.range K).filter fun j => (3 : ℝ) ^ S j n ≤ C * 2 ^ j) :=
      fun i _ j _ hij => rasgo_inyectiva h hij
    have hn2 := fuga_pura_dos h
    obtain ⟨v, hv, hcard⟩ := existe_grande (hne.image (fun j => T^[j] n))
      (fun x hx => by
        obtain ⟨j, -, rfl⟩ := Finset.mem_image.1 hx
        have := fuga_pura_no_baja h j
        omega)
    rw [Finset.card_image_of_injOn hiny] at hcard
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hv
    have hj' := Finset.mem_filter.1 hj
    have hjK := Finset.mem_range.1 hj'.1
    have hS : ((S j n : ℕ) : ℝ) + 1 ≤ K := by
      have := S_le_pasos j n
      have h1 : S j n + 1 ≤ K := by omega
      exact_mod_cast h1
    have hc : (((Finset.range K).filter fun j => (3 : ℝ) ^ S j n ≤ C * 2 ^ j).card : ℝ) ≤
        (T^[j] n : ℝ) := by exact_mod_cast hcard
    calc (((Finset.range K).filter fun j => (3 : ℝ) ^ S j n ≤ C * 2 ^ j).card : ℝ) ^ 6
        ≤ (T^[j] n : ℝ) ^ 6 := pow_le_pow_left₀ (by positivity) hc 6
      _ ≤ C ^ 6 * n ^ 6 * (S j n + 1) := regreso_sexta_real h hj'.2
      _ ≤ C ^ 6 * n ^ 6 * K := mul_le_mul_of_nonneg_left hS (by positivity)

/-- **La cuenta de regresos con la raíz:** si `C ≥ 0`, hay a lo sumo `⌊C·n·K^(1/6)⌋`
    tiempos `j < K` con pronóstico a lo sumo `C`. -/
theorem cuenta_regresos_raiz {n : ℕ} (h : FugaPura n) {C : ℝ} (hC : 0 ≤ C) (K : ℕ) :
    ((Finset.range K).filter fun j => (3 : ℝ) ^ S j n ≤ C * 2 ^ j).card ≤
      ⌊C * n * (K : ℝ) ^ ((1 : ℝ) / 6)⌋₊ := by
  apply Nat.le_floor
  have h6 := cuenta_regresos_real h C K
  have hK : ((K : ℝ) ^ ((1 : ℝ) / 6)) ^ 6 = K := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by positivity)]
    norm_num
  have hr : (C * n * (K : ℝ) ^ ((1 : ℝ) / 6)) ^ 6 = C ^ 6 * n ^ 6 * K := by
    rw [mul_pow, mul_pow, hK]
  rw [← hr] at h6
  exact (pow_le_pow_iff_left₀ (by positivity) (by positivity) (by norm_num)).1 h6

end PerdicesSexta

#print axioms PerdicesSexta.impar_mayor
#print axioms PerdicesSexta.producto_sexta
#print axioms PerdicesSexta.sexta_raiz_general
#print axioms PerdicesSexta.sexta_raiz
#print axioms PerdicesSexta.sexta_raiz_nat
#print axioms PerdicesSexta.regreso_sexta
#print axioms PerdicesSexta.existe_grande
#print axioms PerdicesSexta.cuenta_regresos
#print axioms PerdicesSexta.techo_sube
#print axioms PerdicesSexta.techo_sube_real
#print axioms PerdicesSexta.regreso_sexta_real
#print axioms PerdicesSexta.cuenta_regresos_real
#print axioms PerdicesSexta.cuenta_regresos_raiz
