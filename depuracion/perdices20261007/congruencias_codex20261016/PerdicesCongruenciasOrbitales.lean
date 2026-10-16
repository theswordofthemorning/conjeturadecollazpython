import PerdicesTransporteImpar
import PerdicesCongruencias
import Mathlib.Data.Nat.Log

/-! Enlace desde caminos reales A/B, sin suponer las congruencias de
las fronteras. No afirma el presupuesto global de recargas. -/

namespace PerdicesCongruenciasOrbitales

open PerdicesTransporteImpar PerdicesCongruencias

theorem separar {xs ys : List Bloque} {n z : ℕ}
    (h : Camino (xs ++ ys) n z) :
    ∃ y, Camino xs n y ∧ Camino ys y z := by
  induction xs generalizing n with
  | nil => exact ⟨n, Camino.nil n, h⟩
  | cons p ps ih =>
    cases h with
    | cons hp hs =>
      obtain ⟨y, h₁, h₂⟩ := ih hs
      exact ⟨y, Camino.cons hp h₁, h₂⟩

theorem racha_a {b x y : ℕ} (h : Camino (List.replicate b .a) x y) :
    2 ^ b * (y + 1) = 3 ^ b * (x + 1) := by
  induction b generalizing x with
  | zero => cases h; simp
  | succ b ih =>
    rw [List.replicate_succ] at h
    cases h with
    | @cons _ _ _ z _ hp hs =>
      have hi := ih hs
      have he : 2 * (z + 1) = 3 * (x + 1) := by
        simp only [Paso, N, D, E] at hp
        omega
      simp only [pow_succ]
      nlinarith [congrArg (fun u => 3 ^ b * u) he]

theorem racha_b {c x y : ℕ} (h : Camino (List.replicate c .b) x y) :
    8 ^ c * (y + 5) = 9 ^ c * (x + 5) := by
  induction c generalizing x with
  | zero => cases h; simp
  | succ c ih =>
    rw [List.replicate_succ] at h
    cases h with
    | @cons _ _ _ z _ hp hs =>
      have hi := ih hs
      have he : 8 * (z + 5) = 9 * (x + 5) := by
        simp only [Paso, N, D, E] at hp
        omega
      simp only [pow_succ]
      nlinarith [congrArg (fun u => 9 ^ c * u) he]

theorem entrada_b {ps : List Bloque} {x y : ℕ}
    (h : Camino (.b :: ps) x y) : x % 8 = 3 := by
  cases h with
  | cons hp _ =>
    simp only [Paso, N, D, E] at hp
    omega

theorem parte_compartida {b x y : ℕ}
    (h : Camino (List.replicate b .a) x y) (hy : y % 8 = 3) :
    ∃ r, x + 1 = 2 ^ (b + 2) * r ∧ y + 1 = 4 * 3 ^ b * r := by
  have he := racha_a h
  have hd : 2 ^ (b + 2) ∣ 3 ^ b * (x + 1) := by
    rw [← he, pow_add]
    obtain ⟨k, hk⟩ : 4 ∣ y + 1 := by omega
    refine ⟨k, ?_⟩
    rw [hk]
    ring
  have hc : Nat.Coprime (2 ^ (b + 2)) (3 ^ b) :=
    ((by decide : Nat.Coprime 2 3).pow_left _).pow_right _
  obtain ⟨r, hr⟩ := hc.dvd_of_dvd_mul_left hd
  refine ⟨r, hr, ?_⟩
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  rw [hr, pow_add] at he
  norm_num at he
  nlinarith [he]

theorem entrada_racha_b {c x y : ℕ} (hc : 1 ≤ c)
    (h : Camino (List.replicate c .b) x y) : x % 8 = 3 := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : c ≠ 0)
  rw [List.replicate_succ] at h
  exact entrada_b h

theorem salida_racha_b {a x y : ℕ} (ha : 1 ≤ a)
    (h : Camino (List.replicate a .b) x y) : 9 ∣ y + 5 := by
  have he := racha_b h
  have hd : 9 ∣ 8 ^ a * (y + 5) := by
    rw [he]
    exact dvd_mul_of_dvd_left (dvd_pow_self 9 (by omega : a ≠ 0)) _
  exact ((by decide : Nat.Coprime 9 8).pow_right _).dvd_of_dvd_mul_left hd

theorem carga_entrada_b {c x y : ℕ} (hc : 1 ≤ c)
    (h : Camino (List.replicate c .b) x y) (hy : 4 ∣ y + 5) :
    32 ∣ x + 5 := by
  have he := racha_b h
  obtain ⟨k, hk⟩ := hy
  obtain ⟨j, hj⟩ : 8 ∣ 8 ^ c := dvd_pow_self 8 (by omega : c ≠ 0)
  have hd : 32 ∣ 9 ^ c * (x + 5) := by
    rw [← he, hk, hj]
    exact ⟨j * k, by ring⟩
  exact ((by decide : Nat.Coprime 32 9).pow_right _).dvd_of_dvd_mul_left hd

theorem fronteras {a b c d n y z t u : ℕ}
    (ha : 1 ≤ a) (hc : 1 ≤ c)
    (h₁ : Camino (List.replicate a .b) n y)
    (h₂ : Camino (List.replicate b .a) y z)
    (h₃ : Camino (List.replicate c .b) z t)
    (h₄ : Camino (List.replicate d .a) t u) (hu : u % 8 = 3) :
    ∃ r, y + 1 = 2 ^ (b + 2) * r ∧
      (2 ^ b * r + 1) % 9 = 0 ∧ (3 ^ b * r + 1) % 8 = 0 ∧
      9 ^ a * (n + 5) = 4 * 8 ^ a * (2 ^ b * r + 1) := by
  obtain ⟨r, hr, hz⟩ := parte_compartida h₂ (entrada_racha_b hc h₃)
  obtain ⟨v, hv, _⟩ := parte_compartida h₄ hu
  have hy9 := salida_racha_b ha h₁
  have ht4 : 4 ∣ t + 5 := by
    refine ⟨2 ^ d * v + 1, ?_⟩
    rw [pow_add] at hv
    norm_num at hv
    nlinarith [hv]
  have hz32 := carga_entrada_b hc h₃ ht4
  have hr9 : (2 ^ b * r + 1) % 9 = 0 := by
    have hy : y + 5 = 4 * (2 ^ b * r + 1) := by
      rw [pow_add] at hr
      norm_num at hr
      nlinarith
    rw [hy] at hy9
    exact Nat.mod_eq_zero_of_dvd
      ((by decide : Nat.Coprime 9 4).dvd_of_dvd_mul_left hy9)
  have hr8 : (3 ^ b * r + 1) % 8 = 0 := by
    obtain ⟨k, hk⟩ := hz32
    have : 3 ^ b * r + 1 = 8 * k := by nlinarith [hz, hk]
    omega
  refine ⟨r, hr, hr9, hr8, ?_⟩
  have he := racha_b h₁
  rw [pow_add] at hr
  norm_num at hr
  nlinarith [congrArg (fun w => 8 ^ a * w) hr]

theorem desde_palabra {a b c d n fin : ℕ} {cola : List Bloque}
    (ha : 1 ≤ a) (hc : 1 ≤ c)
    (h : Camino (List.replicate a .b ++ (List.replicate b .a ++
      (List.replicate c .b ++ (List.replicate d .a ++ (.b :: cola))))) n fin) :
    ∃ r, r % 72 = minimoResiduo (b % 6) ∧
      9 ^ a * (n + 5) = 4 * 8 ^ a * (2 ^ b * r + 1) := by
  obtain ⟨y, h₁, hresto⟩ := separar h
  obtain ⟨z, h₂, hresto⟩ := separar hresto
  obtain ⟨t, h₃, hresto⟩ := separar hresto
  obtain ⟨u, h₄, hresto⟩ := separar hresto
  obtain ⟨r, _, hr9, hr8, he⟩ := fronteras ha hc h₁ h₂ h₃ h₄ (entrada_b hresto)
  exact ⟨r, tabla_compartida hr9 hr8, he⟩

theorem banda_entera {b c d n fin : ℕ} {cola : List Bloque}
    (hc : 1 ≤ c)
    (h : Camino (List.replicate 1 .b ++ (List.replicate b .a ++
      (List.replicate c .b ++ (List.replicate d .a ++ (.b :: cola))))) n fin) :
    2 ^ b * 2 ^ (sobrecoste (b % 6) - 1) < n + 5 := by
  obtain ⟨r, hr, he⟩ := desde_palabra (by omega) hc h
  have hm : minimoResiduo (b % 6) ≤ r := hr ▸ Nat.mod_le r 72
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  norm_num at he
  interval_cases j : b % 6 <;>
    norm_num [j, minimoResiduo, sobrecoste] at hm ⊢ <;> nlinarith

theorem banda_logaritmica {b c d n fin : ℕ} {cola : List Bloque}
    (hc : 1 ≤ c)
    (h : Camino (List.replicate 1 .b ++ (List.replicate b .a ++
      (List.replicate c .b ++ (List.replicate d .a ++ (.b :: cola))))) n fin) :
    b + sobrecoste (b % 6) ≤ Nat.clog 2 (n + 5) := by
  have he := banda_entera hc h
  rw [← pow_add] at he
  have hi := (Nat.lt_clog_iff_pow_lt (by omega : 1 < 2)).mpr he
  have hs : 1 ≤ sobrecoste (b % 6) := by
    unfold sobrecoste
    split <;> omega
  omega

theorem ventana_desde_semilla {b c d n fin : ℕ} {prefijo cola : List Bloque}
    (hc : 1 ≤ c)
    (h : Camino (prefijo ++ (List.replicate 1 .b ++ (List.replicate b .a ++
      (List.replicate c .b ++ (List.replicate d .a ++ (.b :: cola)))))) n fin) :
    2 ^ (largo prefijo + b + (sobrecoste (b % 6) - 1)) <
      3 ^ impares prefijo * (n + 5) := by
  obtain ⟨x, hp, hv⟩ := separar h
  have he := banda_entera hc hv
  have ht := (encaje hp).2
  have hpos : 0 < (2 : ℕ) ^ largo prefijo := pow_pos (by omega) _
  have hm := Nat.mul_lt_mul_of_pos_left he hpos
  rw [pow_add, pow_add]
  nlinarith [hm, ht]

end PerdicesCongruenciasOrbitales

#print axioms PerdicesCongruenciasOrbitales.separar
#print axioms PerdicesCongruenciasOrbitales.racha_a
#print axioms PerdicesCongruenciasOrbitales.racha_b
#print axioms PerdicesCongruenciasOrbitales.entrada_b
#print axioms PerdicesCongruenciasOrbitales.parte_compartida
#print axioms PerdicesCongruenciasOrbitales.entrada_racha_b
#print axioms PerdicesCongruenciasOrbitales.salida_racha_b
#print axioms PerdicesCongruenciasOrbitales.carga_entrada_b
#print axioms PerdicesCongruenciasOrbitales.fronteras
#print axioms PerdicesCongruenciasOrbitales.desde_palabra
#print axioms PerdicesCongruenciasOrbitales.banda_entera
#print axioms PerdicesCongruenciasOrbitales.banda_logaritmica
#print axioms PerdicesCongruenciasOrbitales.ventana_desde_semilla
