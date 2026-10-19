import PerdicesRelojTerminal
import Mathlib.Algebra.Order.Archimedean.Real.Basic

/-! Una familia positiva real descarta L ≤ ell(n) + D para todo D fijo.
No descarta pendientes mayores que uno ni el reloj uniforme buscado. -/

namespace PerdicesPendienteUno

open PerdicesTransporteImpar PerdicesRelojTerminal

theorem potencia_con_cociente (k : ℕ) :
    ∃ q : ℕ, 3 ^ (k + 2) * q + 1 = 2 ^ (6 * 3 ^ k) := by
  induction k with
  | zero => exact ⟨7, by norm_num⟩
  | succ k ih =>
    obtain ⟨q, hq⟩ := ih
    refine ⟨q + 3 ^ (k + 2) * q ^ 2 + 3 * (3 ^ (k + 1)) ^ 2 * q ^ 3, ?_⟩
    have he : 2 ^ (6 * 3 ^ (k + 1)) = (2 ^ (6 * 3 ^ k)) ^ 3 := by
      rw [← pow_mul]
      congr 1
      simp [pow_succ, Nat.mul_assoc]
    rw [he, ← hq]
    simp only [pow_succ]
    ring

def palabra (a b : ℕ) : List Bloque :=
  (List.replicate a .a ++ List.replicate b .b) ++ List.replicate 2 .a

theorem largo_palabra (a b : ℕ) : largo (palabra a b) = a + 3 * b + 2 := by
  simp [palabra, largo_concatenar, largo_racha, duracion, largo, Nat.add_assoc]

theorem familia_real {a b q : ℕ} (hb : 0 < b)
    (hq : 3 ^ a * q + 1 = 2 ^ (3 * b)) :
    let n := 2 ^ (a + 2) * q - 1
    0 < n ∧ ∃ y, Camino (palabra a b) n y := by
  have hqpos : 0 < q := by
    have hp : 1 < 2 ^ (3 * b) := one_lt_pow₀ (by norm_num) (by omega)
    by_contra hn
    have : q = 0 := by omega
    simp [this] at hq
    omega
  dsimp only
  let n := 2 ^ (a + 2) * q - 1
  have hn : n + 1 = 2 ^ (a + 2) * q := by
    dsimp [n]
    have : 0 < 2 ^ (a + 2) * q := by positivity
    omega
  have hnpos : 0 < n := by
    have hp : 1 ≤ 2 ^ a := Nat.one_le_pow a 2 (by omega)
    rw [pow_add] at hn
    norm_num at hn
    nlinarith
  refine ⟨hnpos, ?_⟩
  have ha : 2 ^ (duracion .a * a) ∣ n + constante .a := by
    simp only [duracion, constante, one_mul, hn, pow_add]
    exact ⟨2 ^ 2 * q, by ring⟩
  obtain ⟨z, hz, hza⟩ := continuar_racha .a a n ha
  simp only [duracion, constante, D, one_mul] at hza
  have hz1 : z + 1 = 4 * 3 ^ a * q := by
    apply Nat.eq_of_mul_eq_mul_left (pow_pos (by omega : 0 < 2) a)
    rw [hza, hn, pow_add]
    ring
  have hz5 : z + 5 = 2 ^ (3 * b) * 4 := by nlinarith [hq]
  have hbb : 2 ^ (duracion .b * b) ∣ z + constante .b := by
    simp only [duracion, constante, hz5]
    exact dvd_mul_right _ _
  obtain ⟨t, ht, htb⟩ := continuar_racha .b b z hbb
  simp only [duracion, constante, D] at htb
  have ht5 : t + 5 = 4 * 9 ^ b := by
    apply Nat.eq_of_mul_eq_mul_left (pow_pos (by omega : 0 < 2) (3 * b))
    rw [htb, hz5]
    ring
  have ht1 : 4 ∣ t + 1 := by
    have hd : 4 ∣ t + 5 := by rw [ht5]; exact dvd_mul_right _ _
    have hs := Nat.dvd_sub hd (dvd_refl 4)
    simpa using hs
  obtain ⟨y, hy, _⟩ := continuar_racha .a 2 t (by simpa [duracion, constante] using ht1)
  exact ⟨y, concatenar (concatenar hz ht) hy⟩

theorem familia_altura {a b q : ℕ} (hqpos : 0 < q)
    (hq : 3 ^ a * q + 1 = 2 ^ (3 * b)) :
    ell (2 ^ (a + 2) * q - 1) ≤ 3 * b + 2 := by
  apply Nat.clog_le_of_le_pow
  have hn : 2 ^ (a + 2) * q - 1 + 5 = 4 * 2 ^ a * q + 4 := by
    have hp : 0 < 2 ^ (a + 2) * q := by positivity
    calc
      _ = 2 ^ (a + 2) * q + 4 := by omega
      _ = 4 * 2 ^ a * q + 4 := by rw [pow_add]; ring
  rw [hn, pow_add]
  norm_num
  have hp : 2 ^ a * q ≤ 3 ^ a * q :=
    Nat.mul_le_mul_right q (Nat.pow_le_pow_left (by omega : 2 ≤ 3) a)
  nlinarith

theorem exceso_arbitrario (k : ℕ) :
    ∃ n y : ℕ, 0 < n ∧ Camino (palabra (k + 2) (2 * 3 ^ k)) n y ∧
      ell n + (k + 2) ≤ largo (palabra (k + 2) (2 * 3 ^ k)) := by
  obtain ⟨q, hq⟩ := potencia_con_cociente k
  have he : 3 * (2 * 3 ^ k) = 6 * 3 ^ k := by ring
  have hb : 0 < 2 * 3 ^ k := by positivity
  have hc : 3 ^ (k + 2) * q + 1 = 2 ^ (3 * (2 * 3 ^ k)) := by rwa [he]
  obtain ⟨hn, y, hy⟩ := familia_real hb hc
  have hqpos : 0 < q := by
    by_contra h
    have : q = 0 := by omega
    simp [this] at hn
  have hh := familia_altura hqpos hc
  refine ⟨_, y, hn, hy, ?_⟩
  rw [largo_palabra]
  omega

theorem sin_reloj_pendiente_uno (D : ℝ) :
    ¬ (∀ n : ℕ, 0 < n → Reloj n ((ell n : ℝ) + D)) := by
  intro h
  obtain ⟨k, hk⟩ := exists_nat_gt D
  obtain ⟨n, y, hn, hy, hl⟩ := exceso_arbitrario k
  have hr := h n hn _ y hy
  have hc : (ell n : ℝ) + (k + 2 : ℕ) ≤ largo (palabra (k + 2) (2 * 3 ^ k)) := by
    exact_mod_cast hl
  push_cast at hc
  linarith

theorem pendiente_necesariamente_mayor_uno {C D : ℝ}
    (h : ∀ n : ℕ, 0 < n → Reloj n (C * ell n + D)) : 1 < C := by
  by_contra hc
  have hc1 : C ≤ 1 := by linarith
  apply sin_reloj_pendiente_uno D
  intro n hn ps y hy
  have hr := h n hn ps y hy
  have hm := mul_le_mul_of_nonneg_right hc1 (Nat.cast_nonneg (ell n) : (0 : ℝ) ≤ ell n)
  linarith

end PerdicesPendienteUno

#print axioms PerdicesPendienteUno.potencia_con_cociente
#print axioms PerdicesPendienteUno.largo_palabra
#print axioms PerdicesPendienteUno.familia_real
#print axioms PerdicesPendienteUno.familia_altura
#print axioms PerdicesPendienteUno.exceso_arbitrario
#print axioms PerdicesPendienteUno.sin_reloj_pendiente_uno
#print axioms PerdicesPendienteUno.pendiente_necesariamente_mayor_uno
