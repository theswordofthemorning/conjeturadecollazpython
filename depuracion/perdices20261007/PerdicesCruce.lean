import PerdicesSexta
import Mathlib.Data.Nat.Log
import Mathlib.Data.Nat.Find

/-! # Perdices: sexta raíz y cuenta de casi fugitivos

Todas las cotas orbitales reciben FugaPura n; no se prueba que exista.
Los techos son 3^c, c natural, y se conserva la misma semilla n.
-/

namespace PerdicesCruce

set_option exponentiation.threshold 2048

open Ocelotas CasaPlano CasaRetrato PerdicesEstela PerdicesSexta

open Classical in
noncomputable def regresos (n c K : ℕ) : ℕ :=
  ((Finset.range K).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card

theorem radio_existe (Q : ℕ) : ∃ X : ℕ, X ^ 6 ≤ Q ∧ Q < (X + 1) ^ 6 := by
  have he : ∃ X : ℕ, Q < (X + 1) ^ 6 :=
    ⟨Q, lt_of_lt_of_le (by omega) (le_self_pow₀ (by omega) (by decide))⟩
  refine ⟨Nat.find he, ?_, Nat.find_spec he⟩
  by_cases hz : Nat.find he = 0
  · simp [hz]
  · have hh := Nat.find_min he (show Nat.find he - 1 < Nat.find he by omega)
    rw [Nat.sub_add_cancel (by omega : 1 ≤ Nat.find he)] at hh
    omega

theorem regreso_intervalo {n c K X j : ℕ} (h : FugaPura n)
    (hX : (3 ^ c * n) ^ 6 * K < (X + 1) ^ 6)
    (hj : j < K) (hb : 3 ^ S j n ≤ 3 ^ c * 2 ^ j) : T^[j] n ≤ X := by
  have hS : S j n + 1 ≤ K := by have := S_le_pasos j n; omega
  have hy : (T^[j] n) ^ 6 < (X + 1) ^ 6 :=
    lt_of_le_of_lt ((regreso_sexta h hb).trans (by
      rw [mul_pow]
      exact Nat.mul_le_mul_left _ hS)) hX
  have : T^[j] n < X + 1 := (Nat.pow_lt_pow_iff_left (by decide : 6 ≠ 0)).1 hy
  omega

open Classical in
theorem cuenta_mixta {n c K X : ℕ} (h : FugaPura n)
    (hX : (3 ^ c * n) ^ 6 * K < (X + 1) ^ 6) (m : ℕ) :
    regresos n c K ≤ ((X + 1) / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m)) := by
  refine le_trans ?_ (cuenta_casi_fugas (X + 1) m c)
  unfold regresos
  refine Finset.card_le_card_of_injOn (fun j => T^[j] n) ?_ ?_
  · intro j hj
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hj ⊢
    exact ⟨by have := regreso_intervalo h hX hj.1 hj.2; omega,
      casi_fuga_de_bajo h hj.2⟩
  · intro i _ j _ hij
    exact rasgo_inyectiva h hij

theorem quitar_division {q N c m : ℕ}
    (h : q ≤ (N / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m))) :
    q * 16 ^ m ≤ (N + 2 ^ (100 * m)) * 2 ^ c := by
  have he : 2 ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by omega, pow_add, pow_mul]
    norm_num
  have hd : (N / 2 ^ (100 * m) + 1) * 2 ^ (100 * m) ≤ N + 2 ^ (100 * m) := by
    rw [Nat.add_mul, one_mul]
    exact Nat.add_le_add_right (Nat.div_mul_le_self _ _) _
  have hh : (q * 16 ^ m) * 2 ^ (96 * m) ≤
      ((N + 2 ^ (100 * m)) * 2 ^ c) * 2 ^ (96 * m) := by
    calc
      _ = q * 2 ^ (100 * m) := by rw [he]; ring
      _ ≤ ((N / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m))) * 2 ^ (100 * m) :=
        Nat.mul_le_mul_right _ h
      _ = ((N / 2 ^ (100 * m) + 1) * 2 ^ (100 * m)) * (2 ^ c * 2 ^ (96 * m)) := by ring
      _ ≤ (N + 2 ^ (100 * m)) * (2 ^ c * 2 ^ (96 * m)) := Nat.mul_le_mul_right _ hd
      _ = _ := by ring
  exact Nat.le_of_mul_le_mul_right hh (by positivity)

theorem escala_existe {N : ℕ} (hN : 0 < N) :
    ∃ m : ℕ, 2 ^ (100 * m) ≤ N ∧ N < 2 ^ 100 * 2 ^ (100 * m) := by
  refine ⟨Nat.log (2 ^ 100) N, ?_, ?_⟩
  · rw [pow_mul]
    exact Nat.pow_log_le_self (2 ^ 100) (by omega : N ≠ 0)
  · have hh := Nat.lt_pow_succ_log_self (b := 2 ^ 100) (by norm_num) N
    rw [pow_succ, ← pow_mul] at hh
    exact hh.trans_eq (Nat.mul_comm _ _)

theorem cota_espacial {q N c : ℕ} (hN : 0 < N)
    (h : ∀ m, q * 16 ^ m ≤ (N + 2 ^ (100 * m)) * 2 ^ c) :
    q ^ 25 ≤ 2 ^ (25 * c + 125) * N ^ 24 := by
  obtain ⟨m, hlo, hhi⟩ := escala_existe hN
  have hq : q * 16 ^ m ≤ 2 ^ (c + 1) * N := by
    calc
      _ ≤ (N + 2 ^ (100 * m)) * 2 ^ c := h m
      _ ≤ (N + N) * 2 ^ c := Nat.mul_le_mul_right _ (Nat.add_le_add_left hlo N)
      _ = _ := by rw [pow_succ]; ring
  have he : (16 ^ m) ^ 25 = (2 : ℕ) ^ (100 * m) := by
    rw [show (16 : ℕ) = 2 ^ 4 by norm_num, ← pow_mul, ← pow_mul]
    congr 1
    omega
  have hp : q ^ 25 * 2 ^ (100 * m) ≤ (2 ^ (c + 1)) ^ 25 * N ^ 25 := by
    simpa only [mul_pow, he] using Nat.pow_le_pow_left hq 25
  have hc : 2 ^ 100 * (2 ^ (c + 1)) ^ 25 = (2 : ℕ) ^ (25 * c + 125) := by
    rw [← pow_mul, ← pow_add]
    congr 1
    omega
  have hcancel : q ^ 25 * N ≤ (2 ^ (25 * c + 125) * N ^ 24) * N := by
    calc
      _ ≤ q ^ 25 * (2 ^ 100 * 2 ^ (100 * m)) := Nat.mul_le_mul_left _ (Nat.le_of_lt hhi)
      _ = 2 ^ 100 * (q ^ 25 * 2 ^ (100 * m)) := by ring
      _ ≤ 2 ^ 100 * ((2 ^ (c + 1)) ^ 25 * N ^ 25) := Nat.mul_le_mul_left _ hp
      _ = _ := by rw [← Nat.mul_assoc, hc]; ring
  exact Nat.le_of_mul_le_mul_right hcancel hN

theorem cuenta_potencia {n c K X : ℕ} (h : FugaPura n)
    (hX : (3 ^ c * n) ^ 6 * K < (X + 1) ^ 6) :
    (regresos n c K) ^ 25 ≤ 2 ^ (25 * c + 125) * (X + 1) ^ 24 := by
  exact cota_espacial (by omega) (fun m => quitar_division (cuenta_mixta h hX m))

open Classical in
theorem cuenta_combinada {n c K X : ℕ} (h : FugaPura n)
    (hX : (3 ^ c * n) ^ 6 * K < (X + 1) ^ 6) (m : ℕ) :
    regresos n c K ≤ min K (min X
      (((X + 1) / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m)))) := by
  have hk : regresos n c K ≤ K := by
    unfold regresos
    simpa using Finset.card_le_card (Finset.filter_subset
      (fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j) (Finset.range K))
  have hq : (regresos n c K) ^ 6 < (X + 1) ^ 6 := by
    apply lt_of_le_of_lt (cuenta_regresos h (3 ^ c) K)
    simpa [mul_pow, Nat.mul_assoc] using hX
  have hx : regresos n c K ≤ X := by
    have := (Nat.pow_lt_pow_iff_left (by decide : 6 ≠ 0)).1 hq
    omega
  exact le_min hk (le_min hx (cuenta_mixta h hX m))

theorem exponente_temporal {n : ℕ} (h : FugaPura n) (c K : ℕ) :
    (regresos n c K) ^ 150 ≤
      2 ^ (150 * c + 894) * (3 ^ c * n) ^ 144 * K ^ 24 := by
  by_cases hK : K = 0
  · simp [hK, regresos]
  obtain ⟨X, hXlo, hXhi⟩ := radio_existe ((3 ^ c * n) ^ 6 * K)
  have hn := fuga_pura_dos h
  have hQ : 0 < (3 ^ c * n) ^ 6 * K := by positivity
  have hX : 1 ≤ X := by
    by_contra hh
    have hz : X = 0 := by omega
    simp only [hz, Nat.zero_add, one_pow] at hXhi
    omega
  have hN : (X + 1) ^ 6 ≤ 2 ^ 6 * ((3 ^ c * n) ^ 6 * K) := by
    calc
      _ ≤ (2 * X) ^ 6 := Nat.pow_le_pow_left (by omega) 6
      _ = 2 ^ 6 * X ^ 6 := by ring
      _ ≤ _ := Nat.mul_le_mul_left _ hXlo
  have hq := Nat.pow_le_pow_left (cuenta_potencia h hXhi) 6
  calc
    (regresos n c K) ^ 150 ≤
        2 ^ ((25 * c + 125) * 6) * ((X + 1) ^ 6) ^ 24 := by
      simpa only [mul_pow, ← pow_mul] using hq
    _ ≤ 2 ^ ((25 * c + 125) * 6) * (2 ^ 6 * ((3 ^ c * n) ^ 6 * K)) ^ 24 :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hN 24)
    _ = _ := by ring

end PerdicesCruce

#print axioms PerdicesCruce.radio_existe
#print axioms PerdicesCruce.regreso_intervalo
#print axioms PerdicesCruce.cuenta_mixta
#print axioms PerdicesCruce.quitar_division
#print axioms PerdicesCruce.escala_existe
#print axioms PerdicesCruce.cota_espacial
#print axioms PerdicesCruce.cuenta_potencia
#print axioms PerdicesCruce.cuenta_combinada
#print axioms PerdicesCruce.exponente_temporal
