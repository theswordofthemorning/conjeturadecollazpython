import PerdicesSemilla

/-! # Perdices: novena raíz por la exclusión de múltiplos de tres.

Una órbita tiene a lo sumo una entrada impar divisible por tres. El lema
finito utiliza además entradas distintas y al menos tres. FugaPura aporta
esas dos hipótesis; no se afirma que exista una fuga pura.
-/

namespace PerdicesNovena

open Ocelotas CasaPlano CasaRetrato PerdicesEstela PerdicesTamano PerdicesSexta
open PerdicesCruce
open scoped BigOperators

set_option exponentiation.threshold 2048

theorem impar_aparta_tres {x : ℕ} (hx : x % 2 = 1) : T x % 3 ≠ 0 := by
  have h := T_impar hx
  omega

theorem conserva_no_tres {x : ℕ} (hx : x % 3 ≠ 0) : T x % 3 ≠ 0 := by
  by_cases he : x % 2 = 0
  · have h := T_par he; omega
  · exact impar_aparta_tres (by omega)

theorem iter_no_tres {x : ℕ} (hx : x % 3 ≠ 0) (k : ℕ) : T^[k] x % 3 ≠ 0 := by
  induction k with
  | zero => exact hx
  | succ k ih => rw [Function.iterate_succ_apply']; exact conserva_no_tres ih

theorem despues_de_impar {n i j : ℕ} (hi : T^[i] n % 2 = 1) (hij : i < j) :
    T^[j] n % 3 ≠ 0 := by
  have hj : j = (j - (i + 1)) + (i + 1) := by omega
  rw [hj, Function.iterate_add_apply, Function.iterate_succ_apply']
  exact iter_no_tres (impar_aparta_tres hi) _

theorem excepcion_orbital (n k : ℕ) : ∃ b : ℕ,
    ∀ x ∈ (subidas k n).image (fun j => T^[j] n), x ≠ b → x % 3 ≠ 0 := by
  classical
  by_cases he : ∃ i ∈ subidas k n, T^[i] n % 3 = 0
  · obtain ⟨i, hi, htres⟩ := he
    refine ⟨T^[i] n, ?_⟩
    intro x hx hxb
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hx
    have hne : j ≠ i := by intro h; exact hxb (congrArg (fun z => T^[z] n) h)
    rcases lt_or_gt_of_ne hne with hji | hij
    · exact False.elim ((despues_de_impar (Finset.mem_filter.1 hj).2 hji) htres)
    · exact despues_de_impar (Finset.mem_filter.1 hi).2 hij
  · refine ⟨0, ?_⟩
    intro x hx _ hzero
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.1 hx
    exact he ⟨i, hi, hzero⟩

theorem impar_mayor_sin_tres {A : Finset ℕ} {a : ℕ} (ha : a ∈ A)
    (hmax : ∀ x ∈ A, x ≤ a)
    (hb : ∀ x ∈ A, x % 2 = 1 ∧ 3 ≤ x ∧ x % 3 ≠ 0) : 3 * A.card + 1 ≤ a := by
  have hc : A.card ≤ (Finset.Icc 1 ((a - 1) / 3)).card := by
    apply Finset.card_le_card_of_injOn (fun x => (x - 1) / 3)
    · intro x hx
      have h1 := hb x hx
      have h2 := hmax x hx
      simp only [Finset.coe_Icc, Set.mem_Icc]
      have h3 : x % 3 = 1 ∨ x % 3 = 2 := by omega
      rcases h3 with h3 | h3 <;> omega
    · intro x hx y hy hxy
      have h1 := hb x hx
      have h2 := hb y hy
      simp only at hxy
      have h3 : x % 3 = 1 ∨ x % 3 = 2 := by omega
      have h4 : y % 3 = 1 ∨ y % 3 = 2 := by omega
      rcases h3 with h3 | h3 <;> rcases h4 with h4 | h4 <;> omega
  rw [Nat.card_Icc] at hc
  have := hb a ha
  omega

theorem factor_novena (r : ℕ) :
    (2 * r + 1) * (9 * r + 13) ^ 9 ≤ (2 * r + 3) * (9 * r + 12) ^ 9 := by
  calc
    _ ≤ (2 * r + 1) * (9 * r + 13) ^ 9 +
      (4874841683 + 27521925685 * r + 67990638762 * r ^ 2 +
       95996425860 * r ^ 3 + 84725547858 * r ^ 4 + 47865946086 * r ^ 5 +
       16904075328 * r ^ 6 + 3411851220 * r ^ 7 + 301327047 * r ^ 8) :=
      Nat.le_add_right _ _
    _ = _ := by ring

theorem producto_novena (A : Finset ℕ) :
    (∀ x ∈ A, x % 2 = 1 ∧ 3 ≤ x ∧ x % 3 ≠ 0) →
      (∏ x ∈ A, (1 + 1 / (3 * (x : ℝ)))) ^ 9 ≤ 2 * A.card + 1 := by
  induction A using Finset.induction_on_max with
  | empty => intro _; simp
  | insert a s hlt ih =>
    intro hb
    have has : a ∉ s := fun h => lt_irrefl a (hlt a h)
    have hp := ih fun x hx => hb x (Finset.mem_insert_of_mem hx)
    have hbig : 3 * (insert a s).card + 1 ≤ a :=
      impar_mayor_sin_tres (Finset.mem_insert_self a s)
        (fun x hx => by
          rcases Finset.mem_insert.1 hx with rfl | hx
          · exact le_rfl
          · exact (hlt x hx).le) hb
    rw [Finset.card_insert_of_notMem has] at hbig ⊢
    rw [Finset.prod_insert has, mul_pow]
    have hra : 3 * ((s.card : ℝ) + 1) + 1 ≤ (a : ℝ) := by exact_mod_cast hbig
    have hf : 1 + 1 / (3 * (a : ℝ)) ≤ (9 * s.card + 13) / (9 * s.card + 12) := by
      have h1 : 1 / (3 * (a : ℝ)) ≤ 1 / (9 * s.card + 12) :=
        one_div_le_one_div_of_le (by positivity) (by linarith)
      have h2 : (9 * (s.card : ℝ) + 13) / (9 * s.card + 12) =
          1 + 1 / (9 * s.card + 12) := by field_simp; ring
      linarith
    have hf9 := pow_le_pow_left₀ (by positivity : (0 : ℝ) ≤ 1 + 1 / (3 * (a : ℝ))) hf 9
    have hfac : ((9 * (s.card : ℝ) + 13) / (9 * s.card + 12)) ^ 9 *
        (2 * s.card + 1) ≤ 2 * s.card + 3 := by
      have hn : (2 * (s.card : ℝ) + 1) * (9 * s.card + 13) ^ 9 ≤
          (2 * s.card + 3) * (9 * s.card + 12) ^ 9 := by exact_mod_cast factor_novena s.card
      rw [div_pow, div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
      linarith
    calc
      _ ≤ ((9 * (s.card : ℝ) + 13) / (9 * s.card + 12)) ^ 9 * (2 * s.card + 1) :=
        mul_le_mul hf9 hp (by positivity) (by positivity)
      _ ≤ 2 * s.card + 3 := hfac
      _ = _ := by push_cast; ring

theorem factor_excepcional {b : ℕ} (hb : 3 ≤ b) :
    (1 + 1 / (3 * (b : ℝ))) ^ 9 ≤ 3 := by
  have hr : (3 : ℝ) ≤ b := by exact_mod_cast hb
  have hf : (1 : ℝ) + 1 / (3 * b) ≤ 10 / 9 := by
    have := one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 9)
      (show (9 : ℝ) ≤ 3 * b by linarith)
    linarith
  have h9 := pow_le_pow_left₀ (by positivity : (0 : ℝ) ≤ 1 + 1 / (3 * (b : ℝ))) hf 9
  exact h9.trans (by norm_num)

theorem producto_novena_excepcion (A : Finset ℕ) (b : ℕ)
    (himp : ∀ x ∈ A, x % 2 = 1 ∧ 3 ≤ x)
    (hb : ∀ x ∈ A, x ≠ b → x % 3 ≠ 0) :
    (∏ x ∈ A, (1 + 1 / (3 * (x : ℝ)))) ^ 9 ≤ 3 * (2 * A.card + 1) := by
  classical
  by_cases hmem : b ∈ A
  · have hg := producto_novena (A.erase b) (fun x hx =>
      ⟨(himp x (Finset.mem_of_mem_erase hx)).1,
       (himp x (Finset.mem_of_mem_erase hx)).2,
       hb x (Finset.mem_of_mem_erase hx) (Finset.mem_erase.1 hx).1⟩)
    have hf := factor_excepcional (himp b hmem).2
    have heq : (∏ x ∈ A, (1 + 1 / (3 * (x : ℝ)))) =
        (1 + 1 / (3 * (b : ℝ))) * ∏ x ∈ A.erase b, (1 + 1 / (3 * (x : ℝ))) := by
      conv_lhs => rw [← Finset.insert_erase hmem, Finset.prod_insert (by simp)]
    rw [heq, mul_pow]
    calc
      _ ≤ (3 : ℝ) * (2 * ((A.erase b).card : ℝ) + 1) :=
        mul_le_mul hf hg (by positivity) (by positivity)
      _ ≤ (3 : ℝ) * (2 * (A.card : ℝ) + 1) := by
        have hh : ((A.erase b).card : ℝ) ≤ A.card := by
          exact_mod_cast Finset.card_le_card (Finset.erase_subset b A)
        linarith
  · have hg := producto_novena A (fun x hx =>
      ⟨(himp x hx).1, (himp x hx).2, hb x hx (by intro h; exact hmem (h ▸ hx))⟩)
    nlinarith only [hg, Nat.cast_nonneg (α := ℝ) A.card]

theorem novena_raiz_general {n k : ℕ} (hn : 0 < n)
    (hiny : Set.InjOn (fun j => T^[j] n) (subidas k n))
    (htres : ∀ j ∈ subidas k n, 3 ≤ T^[j] n) :
    normalizado n k ^ 9 ≤ 3 * (n : ℝ) ^ 9 * (2 * S k n + 1) := by
  have hprod : (∏ j ∈ Finset.range k,
      (if T^[j] n % 2 = 1 then 1 + 1 / (3 * (T^[j] n : ℝ)) else 1)) =
      ∏ x ∈ (subidas k n).image (fun j => T^[j] n), (1 + 1 / (3 * (x : ℝ))) := by
    rw [Finset.prod_image hiny, subidas, Finset.prod_filter]
  have hA : ∀ x ∈ (subidas k n).image (fun j => T^[j] n), x % 2 = 1 ∧ 3 ≤ x := by
    intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hx
    exact ⟨(Finset.mem_filter.1 hj).2, htres j hj⟩
  have hc : ((subidas k n).image (fun j => T^[j] n)).card = S k n := by
    rw [Finset.card_image_of_injOn hiny, card_subidas]
  obtain ⟨b, hb⟩ := excepcion_orbital n k
  have h9 := producto_novena_excepcion _ b hA hb
  rw [hc] at h9
  rw [identidad_producto hn, hprod, mul_pow]
  have hh := mul_le_mul_of_nonneg_left h9 (show (0 : ℝ) ≤ (n : ℝ) ^ 9 by positivity)
  nlinarith only [hh]

theorem novena_raiz {n : ℕ} (h : FugaPura n) (k : ℕ) :
    normalizado n k ^ 9 ≤ 3 * (n : ℝ) ^ 9 * (2 * S k n + 1) := by
  have hn := fuga_pura_dos h
  apply novena_raiz_general (by omega)
  · intro i _ j _ hij; exact rasgo_inyectiva h hij
  · intro j hj
    have hodd := (Finset.mem_filter.1 hj).2
    have hge := fuga_pura_no_baja h j
    omega

theorem novena_raiz_nat {n : ℕ} (h : FugaPura n) (k : ℕ) :
    (2 ^ k * T^[k] n) ^ 9 ≤ (3 ^ S k n) ^ 9 * (3 * n ^ 9 * (2 * S k n + 1)) := by
  have hr := novena_raiz h k
  unfold normalizado inverso at hr
  rw [div_mul_eq_mul_div, div_pow, div_le_iff₀ (by positivity)] at hr
  have hc : (((2 ^ k * T^[k] n) ^ 9 : ℕ) : ℝ) ≤
      (((3 ^ S k n) ^ 9 * (3 * n ^ 9 * (2 * S k n + 1)) : ℕ) : ℝ) := by
    push_cast
    nlinarith only [hr]
  exact_mod_cast hc

theorem regreso_novena {n k c : ℕ} (h : FugaPura n) (hk : 3 ^ S k n ≤ c * 2 ^ k) :
    (T^[k] n) ^ 9 ≤ 3 * c ^ 9 * n ^ 9 * (2 * S k n + 1) := by
  have h1 := novena_raiz_nat h k
  have h2 := Nat.pow_le_pow_left hk 9
  have h3 : (2 ^ k) ^ 9 * (T^[k] n) ^ 9 ≤
      (2 ^ k) ^ 9 * (3 * c ^ 9 * n ^ 9 * (2 * S k n + 1)) := by
    calc
      _ = (2 ^ k * T^[k] n) ^ 9 := by ring
      _ ≤ (3 ^ S k n) ^ 9 * (3 * n ^ 9 * (2 * S k n + 1)) := h1
      _ ≤ (c * 2 ^ k) ^ 9 * (3 * n ^ 9 * (2 * S k n + 1)) := Nat.mul_le_mul_right _ h2
      _ = _ := by ring
  exact Nat.le_of_mul_le_mul_left h3 (by positivity)

theorem radio_novena (Q : ℕ) : ∃ X : ℕ, X ^ 9 ≤ Q ∧ Q < (X + 1) ^ 9 := by
  have he : ∃ X : ℕ, Q < (X + 1) ^ 9 :=
    ⟨Q, lt_of_lt_of_le (by omega) (le_self_pow₀ (by omega) (by decide))⟩
  refine ⟨Nat.find he, ?_, Nat.find_spec he⟩
  by_cases hz : Nat.find he = 0
  · simp [hz]
  · have hh := Nat.find_min he (show Nat.find he - 1 < Nat.find he by omega)
    rw [Nat.sub_add_cancel (by omega : 1 ≤ Nat.find he)] at hh
    omega

theorem regreso_intervalo_novena {n c K X j : ℕ} (h : FugaPura n)
    (hX : 6 * (3 ^ c * n) ^ 9 * K < (X + 1) ^ 9)
    (hj : j < K) (hb : 3 ^ S j n ≤ 3 ^ c * 2 ^ j) : T^[j] n ≤ X := by
  have hS : 2 * S j n + 1 ≤ 2 * K := by have := S_le_pasos j n; omega
  have hval : (T^[j] n) ^ 9 ≤ 6 * (3 ^ c * n) ^ 9 * K := by
    calc
      _ ≤ 3 * (3 ^ c) ^ 9 * n ^ 9 * (2 * S j n + 1) := regreso_novena h hb
      _ ≤ 3 * (3 ^ c) ^ 9 * n ^ 9 * (2 * K) := Nat.mul_le_mul_left _ hS
      _ = _ := by ring
  have hh : T^[j] n < X + 1 := (Nat.pow_lt_pow_iff_left (by decide : 9 ≠ 0)).1 (hval.trans_lt hX)
  omega

open Classical in
theorem cuenta_mixta_novena {n c K X : ℕ} (h : FugaPura n)
    (hX : 6 * (3 ^ c * n) ^ 9 * K < (X + 1) ^ 9) (m : ℕ) :
    regresos n c K ≤ ((X + 1) / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m)) := by
  refine le_trans ?_ (cuenta_casi_fugas (X + 1) m c)
  unfold regresos
  refine Finset.card_le_card_of_injOn (fun j => T^[j] n) ?_ ?_
  · intro j hj
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hj ⊢
    exact ⟨by have := regreso_intervalo_novena h hX hj.1 hj.2; omega, casi_fuga_de_bajo h hj.2⟩
  · intro i _ j _ hij; exact rasgo_inyectiva h hij

theorem cuenta_potencia_novena {n c K X : ℕ} (h : FugaPura n)
    (hX : 6 * (3 ^ c * n) ^ 9 * K < (X + 1) ^ 9) :
    (regresos n c K) ^ 25 ≤ 2 ^ (25 * c + 125) * (X + 1) ^ 24 := by
  exact cota_espacial (by omega) (fun m => quitar_division (cuenta_mixta_novena h hX m))

theorem exponente_temporal_novena {n : ℕ} (h : FugaPura n) (c K : ℕ) :
    (regresos n c K) ^ 225 ≤
      2 ^ (225 * c + 1341) * 6 ^ 24 * (3 ^ c * n) ^ 216 * K ^ 24 := by
  by_cases hK : K = 0
  · simp [hK, regresos]
  obtain ⟨X, hXlo, hXhi⟩ := radio_novena (6 * (3 ^ c * n) ^ 9 * K)
  have hn := fuga_pura_dos h
  have hQ : 0 < 6 * (3 ^ c * n) ^ 9 * K := by positivity
  have hX : 1 ≤ X := by
    by_contra hh
    have hz : X = 0 := by omega
    simp only [hz, Nat.zero_add, one_pow] at hXhi
    omega
  have hN : (X + 1) ^ 9 ≤ 2 ^ 9 * (6 * (3 ^ c * n) ^ 9 * K) := by
    calc
      _ ≤ (2 * X) ^ 9 := Nat.pow_le_pow_left (by omega) 9
      _ = 2 ^ 9 * X ^ 9 := by ring
      _ ≤ _ := Nat.mul_le_mul_left _ hXlo
  have hq := Nat.pow_le_pow_left (cuenta_potencia_novena h hXhi) 9
  calc
    (regresos n c K) ^ 225 ≤ 2 ^ ((25 * c + 125) * 9) * ((X + 1) ^ 9) ^ 24 := by
      simpa only [mul_pow, ← pow_mul] using hq
    _ ≤ 2 ^ ((25 * c + 125) * 9) * (2 ^ 9 * (6 * (3 ^ c * n) ^ 9 * K)) ^ 24 :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hN 24)
    _ = _ := by ring

theorem entrada_novena {n c u : ℕ} (h : FugaPura n)
    (hu : PerdicesExcursiones.Bajo n c u) :
    (T^[u] n + 1) ^ 9 ≤ 3072 * (3 ^ c * n) ^ 9 * (u + 1) := by
  have hp : 1 ≤ T^[u] n := iter_pos (by have := fuga_pura_dos h; omega) u
  have hx : T^[u] n + 1 ≤ 2 * T^[u] n := by omega
  have hs : 2 * S u n + 1 ≤ 2 * (u + 1) := by have := S_le_pasos u n; omega
  calc
    _ ≤ (2 * T^[u] n) ^ 9 := Nat.pow_le_pow_left hx 9
    _ = 512 * (T^[u] n) ^ 9 := by ring
    _ ≤ 512 * (3 * (3 ^ c) ^ 9 * n ^ 9 * (2 * S u n + 1)) :=
      Nat.mul_le_mul_left _ (regreso_novena h hu)
    _ ≤ 512 * (3 * (3 ^ c) ^ 9 * n ^ 9 * (2 * (u + 1))) :=
      Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ hs)
    _ = _ := by ring

@[irreducible] def constante_novena (n c : ℕ) : ℕ :=
  2 ^ (225 * c + 1341) * 6 ^ 24 * (3 ^ c * n) ^ 216

theorem tiempo_por_indice_novena {n c r : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i ≤ r, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) :
    (r + 1) ^ 225 ≤ constante_novena n c * (t r + 1) ^ 24 := by
  simpa only [constante_novena] using
    (Nat.pow_le_pow_left (PerdicesSeparacion.cuenta_lista ht hb) 225).trans
      (exponente_temporal_novena h c _)

theorem reloj_noveno_imposible {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (ht : StrictMono t) (hb : ∀ i, 3 ^ S (t i) n ≤ 3 ^ c * 2 ^ t i) (B : ℕ) :
    ¬ ∀ r, t r + 1 ≤ B * (r + 1) ^ 9 := by
  intro hr
  let M := constante_novena n c * B ^ 24
  have hp := tiempo_por_indice_novena h ht (r := M) (fun i _ => hb i)
  have hc : (M + 1) ^ 9 * (M + 1) ^ 216 ≤ M * (M + 1) ^ 216 := by
    calc
      _ = (M + 1) ^ 225 := by rw [← pow_add]
      _ ≤ constante_novena n c * (t M + 1) ^ 24 := hp
      _ ≤ constante_novena n c * (B * (M + 1) ^ 9) ^ 24 :=
        Nat.mul_le_mul_left _ (Nat.pow_le_pow_left (hr M) 24)
      _ = _ := by rw [mul_pow, ← pow_mul]; exact (Nat.mul_assoc _ _ _).symm
  have hh : (M + 1) ^ 9 ≤ M :=
    Nat.le_of_mul_le_mul_right hc (Nat.pow_pos (by omega : 0 < M + 1))
  have hl : M + 1 ≤ (M + 1) ^ 9 := le_self_pow₀ (by omega) (by decide)
  omega

theorem reloj_noveno {t : ℕ → ℕ} (ht : Monotone t) {D : ℕ}
    (hs : ∀ i, (t (i + 1) - t i) ^ 9 ≤ D * (t i + 1) ^ 8) :
    ∀ i, t i + 1 ≤ (D + t 0 + 1) * (i + 1) ^ 9 := by
  generalize hB : D + t 0 + 1 = B
  have hDB : D ≤ B := by omega
  have h0 : t 0 + 1 ≤ B := by omega
  intro i
  induction i with
  | zero => simpa using h0
  | succ i ih =>
    have hg : (t (i + 1) - t i) ^ 9 ≤ (B * (i + 1) ^ 8) ^ 9 := by
      calc
        _ ≤ D * (t i + 1) ^ 8 := hs i
        _ ≤ B * (B * (i + 1) ^ 9) ^ 8 := Nat.mul_le_mul hDB (Nat.pow_le_pow_left ih 8)
        _ = _ := by ring
    have hd := (Nat.pow_le_pow_iff_left (by decide : 9 ≠ 0)).1 hg
    have hm := ht (Nat.le_succ i)
    have hstep : (i + 1) ^ 9 + (i + 1) ^ 8 ≤ (i + 1 + 1) ^ 9 := by
      calc
        _ = (i + 1) ^ 8 * (i + 1 + 1) := by ring
        _ ≤ (i + 1 + 1) ^ 8 * (i + 1 + 1) :=
          Nat.mul_le_mul_right _ (Nat.pow_le_pow_left (Nat.le_succ (i + 1)) 8)
        _ = _ := (pow_succ _ 8).symm
    calc
      _ = (t i + 1) + (t (i + 1) - t i) := by
        rw [Nat.add_right_comm, Nat.add_sub_of_le hm]
      _ ≤ B * (i + 1) ^ 9 + B * (i + 1) ^ 8 := Nat.add_le_add ih hd
      _ = B * ((i + 1) ^ 9 + (i + 1) ^ 8) := by ring
      _ ≤ _ := Nat.mul_le_mul_left _ hstep

theorem cota_octava_novena {n c u v H : ℕ} (h : FugaPura n)
    (he : PerdicesExcursiones.Consecutivos n c u v)
    (hd : v - u ≤ H * (T^[u] n + 1) ^ 8) :
    (v - u) ^ 9 ≤ (H ^ 9 * (3072 * (3 ^ c * n) ^ 9) ^ 8) * (u + 1) ^ 8 := by
  have hx := entrada_novena h he.2.1
  calc
    _ ≤ (H * (T^[u] n + 1) ^ 8) ^ 9 := Nat.pow_le_pow_left hd 9
    _ = H ^ 9 * ((T^[u] n + 1) ^ 9) ^ 8 := by ring
    _ ≤ H ^ 9 * (3072 * (3 ^ c * n) ^ 9 * (u + 1)) ^ 8 :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hx 8)
    _ = _ := by ring

theorem infinitos_exigen_octava {n c : ℕ} (h : FugaPura n)
    (hi : PerdicesExcursiones.InfinitosRegresos n c) (H U : ℕ) :
    ∃ u v, U < u ∧ PerdicesExcursiones.Consecutivos n c u v ∧
      H * (T^[u] n + 1) ^ 8 < v - u := by
  obtain ⟨t, hU, he⟩ := PerdicesRitmo.enumerar_regresos hi U
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have hx : ∃ i, H * (T^[t i] n + 1) ^ 8 < t (i + 1) - t i := by
    by_contra hh
    have hd : ∀ i, t (i + 1) - t i ≤ H * (T^[t i] n + 1) ^ 8 := by simpa using hh
    have hclock := reloj_noveno ht.monotone (fun i => cota_octava_novena h (he i) (hd i))
    exact reloj_noveno_imposible h ht (fun i => (he i).2.1)
      (H ^ 9 * (3072 * (3 ^ c * n) ^ 9) ^ 8 + t 0 + 1) hclock
  obtain ⟨i, hir⟩ := hx
  have h0 := ht.monotone (Nat.zero_le i)
  exact ⟨t i, t (i + 1), by omega, he i, hir⟩

theorem cota_octava_excluye_regresos {n c H U : ℕ} (h : FugaPura n)
    (hc : ∀ u v, U < u → PerdicesExcursiones.Consecutivos n c u v →
      v - u ≤ H * (T^[u] n + 1) ^ 8) : ¬ PerdicesExcursiones.InfinitosRegresos n c := by
  intro hi
  obtain ⟨u, v, hu, he, hd⟩ := infinitos_exigen_octava h hi H U
  exact (not_lt_of_ge (hc u v hu he)) hd

end PerdicesNovena

#print axioms PerdicesNovena.impar_aparta_tres
#print axioms PerdicesNovena.conserva_no_tres
#print axioms PerdicesNovena.iter_no_tres
#print axioms PerdicesNovena.despues_de_impar
#print axioms PerdicesNovena.excepcion_orbital
#print axioms PerdicesNovena.impar_mayor_sin_tres
#print axioms PerdicesNovena.factor_novena
#print axioms PerdicesNovena.producto_novena
#print axioms PerdicesNovena.factor_excepcional
#print axioms PerdicesNovena.producto_novena_excepcion
#print axioms PerdicesNovena.novena_raiz_general
#print axioms PerdicesNovena.novena_raiz
#print axioms PerdicesNovena.novena_raiz_nat
#print axioms PerdicesNovena.regreso_novena
#print axioms PerdicesNovena.radio_novena
#print axioms PerdicesNovena.regreso_intervalo_novena
#print axioms PerdicesNovena.cuenta_mixta_novena
#print axioms PerdicesNovena.cuenta_potencia_novena
#print axioms PerdicesNovena.exponente_temporal_novena
#print axioms PerdicesNovena.entrada_novena
#print axioms PerdicesNovena.tiempo_por_indice_novena
#print axioms PerdicesNovena.reloj_noveno_imposible
#print axioms PerdicesNovena.reloj_noveno
#print axioms PerdicesNovena.cota_octava_novena
#print axioms PerdicesNovena.infinitos_exigen_octava
#print axioms PerdicesNovena.cota_octava_excluye_regresos
