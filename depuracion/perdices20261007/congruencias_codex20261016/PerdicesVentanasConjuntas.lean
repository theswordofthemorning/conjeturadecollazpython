import PerdicesCongruenciasOrbitales
import Mathlib.Data.Nat.ModEq

/-! Dos partes compartidas consecutivas no pueden alcanzar ambas el
mínimo residual. Certificado finito con periodos comprobados en el núcleo. -/

set_option maxRecDepth 100000
set_option maxHeartbeats 800000
set_option Elab.async false

namespace PerdicesVentanasConjuntas

open PerdicesCongruencias PerdicesCongruenciasOrbitales PerdicesTransporteImpar

abbrev Terna := ℕ × ℕ × ℕ

def compatible (m b c d : ℕ) : Prop :=
  (9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1)) % m =
    (8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1)) % m

def tabla12 : List Terna :=
  [(0, 0, 0), (5, 1, 3), (11, 2, 1), (3, 6, 7), (1, 10, 9)]

def tabla36 : List Terna := [(0, 0, 0), (35, 2, 1)]

def tabla108 : List Terna :=
  [(0, 0, 0), (0, 0, 36), (0, 0, 72),
   (107, 2, 1), (107, 2, 37), (107, 2, 73)]

def tabla324 : List Terna :=
  [(0, 0, 0), (108, 0, 216), (216, 0, 108), (323, 2, 1), (0, 216, 36)]

theorem tabla_inicial : ∀ b c d : Fin 12,
    compatible 455 b c d → (b.val, c.val, d.val) ∈ tabla12 := by
  unfold compatible
  decide +kernel

def certificado (p m : ℕ) (antes despues : List Terna) : Prop :=
  ∀ t ∈ antes, ∀ i j k : Fin 3,
    compatible m (t.1 + p * i) (t.2.1 + p * j) (t.2.2 + p * k) →
      (t.1 + p * i.val, t.2.1 + p * j.val, t.2.2 + p * k.val) ∈ despues

theorem tabla_segunda : certificado 12 23350145 tabla12 tabla36 := by
  unfold certificado compatible tabla12
  decide +kernel
theorem tabla_tercera : certificado 36 2545165805 tabla36 tabla108 := by
  unfold certificado compatible tabla36
  decide +kernel
theorem tabla_cuarta : certificado 108 414862026215 tabla108 tabla324 := by
  unfold certificado compatible tabla108
  decide +kernel

theorem levantar {p m b c d : ℕ} {antes despues : List Terna}
    (hp : 0 < p) (hb : b < 3 * p) (hc : c < 3 * p) (hd : d < 3 * p)
    (ht : (b % p, c % p, d % p) ∈ antes)
    (he : compatible m b c d) (hf : certificado p m antes despues) :
    (b, c, d) ∈ despues := by
  have hb' : b / p < 3 := (Nat.div_lt_iff_lt_mul hp).mpr (by omega)
  have hc' : c / p < 3 := (Nat.div_lt_iff_lt_mul hp).mpr (by omega)
  have hd' : d / p < 3 := (Nat.div_lt_iff_lt_mul hp).mpr (by omega)
  have h := hf _ ht ⟨b / p, hb'⟩ ⟨c / p, hc'⟩ ⟨d / p, hd'⟩
  simp only [Nat.mod_add_div] at h
  exact h he

theorem reducir {m p b c d : ℕ} (hp : 6 ∣ p)
    (h2 : 2 ^ p % m = 1) (h3 : 3 ^ p % m = 1)
    (h8 : 8 ^ p % m = 1) (h9 : 9 ^ p % m = 1)
    (he : 9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1) =
      8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1)) :
    compatible m (b % p) (c % p) (d % p) := by
  have hb : b % p % 6 = b % 6 := Nat.mod_mod_of_dvd b hp
  have hd : d % p % 6 = d % 6 := Nat.mod_mod_of_dvd d hp
  have hl : Nat.ModEq m
      (9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1))
      (9 ^ (c % p) * (3 ^ (b % p) * minimoResiduo (b % 6) + 1)) :=
    Nat.ModEq.mul (potencia_periodica h9 c)
      (Nat.ModEq.add (Nat.ModEq.mul (potencia_periodica h3 b) (Nat.ModEq.refl _)) (Nat.ModEq.refl _))
  have hr : Nat.ModEq m
      (8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1))
      (8 ^ (c % p) * (2 ^ (d % p) * minimoResiduo (d % 6) + 1)) :=
    Nat.ModEq.mul (potencia_periodica h8 c)
      (Nat.ModEq.add (Nat.ModEq.mul (potencia_periodica h2 d) (Nat.ModEq.refl _)) (Nat.ModEq.refl _))
  rw [he] at hl
  unfold compatible
  rw [hb, hd]
  exact hl.symm.trans hr

theorem candidatos {b c d : ℕ}
    (he : 9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1) =
      8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1)) :
    (b % 324, c % 324, d % 324) ∈ tabla324 := by
  have h12 := reducir (m := 455) (p := 12) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t12 := tabla_inicial ⟨b % 12, Nat.mod_lt _ (by omega)⟩
    ⟨c % 12, Nat.mod_lt _ (by omega)⟩ ⟨d % 12, Nat.mod_lt _ (by omega)⟩ h12
  have h36 := reducir (m := 23350145) (p := 36) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t36 : (b % 36, c % 36, d % 36) ∈ tabla36 := by
    apply levantar (p := 12) (by omega) (Nat.mod_lt _ (by omega))
      (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h36 tabla_segunda
    simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 12 ∣ 36)] using t12
  have h108 := reducir (m := 2545165805) (p := 108) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t108 : (b % 108, c % 108, d % 108) ∈ tabla108 := by
    apply levantar (p := 36) (by omega) (Nat.mod_lt _ (by omega))
      (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h108 tabla_tercera
    simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 36 ∣ 108)] using t36
  have h324 := reducir (m := 414862026215) (p := 324) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  apply levantar (p := 108) (by omega) (Nat.mod_lt _ (by omega))
    (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h324 tabla_cuarta
  simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 108 ∣ 324)] using t108

theorem descartar_cero {b c d : ℕ} (hc : 2 ≤ c)
    (hb4 : b % 4 = 0) (hb6 : b % 6 = 0)
    (he : 9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1) =
      8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1)) : False := by
  have hd : 16 ∣ 8 ^ c := (by decide +kernel : 16 ∣ 8 ^ 2).trans (pow_dvd_pow 8 hc)
  have hz := Nat.mod_eq_zero_of_dvd (dvd_mul_of_dvd_left hd
    (2 ^ d * minimoResiduo (d % 6) + 1))
  rw [← he] at hz
  have h3 := potencia_periodica (a := 3) (m := 16) (k := 4) (by decide +kernel) b
  have h9 := potencia_periodica (a := 9) (m := 16) (k := 2) (by decide +kernel) c
  have hp : (3 ^ b * 71 + 1) % 16 = 8 := by
    rw [Nat.add_mod, Nat.mul_mod, h3, hb4]
    norm_num
  rw [hb6] at hz
  change (9 ^ c * (3 ^ b * 71 + 1)) % 16 = 0 at hz
  rw [Nat.mul_mod, h9, hp] at hz
  have : c % 2 < 2 := Nat.mod_lt _ (by omega)
  interval_cases j : c % 2 <;> norm_num [j, minimoResiduo] at hz

theorem descartar_uno {b c d : ℕ} (hc : 2 ≤ c) (hd54 : d % 54 = 1)
    (he : 9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1) =
      8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1)) : False := by
  have hd : 81 ∣ 9 ^ c := (by decide +kernel : 81 ∣ 9 ^ 2).trans (pow_dvd_pow 9 hc)
  have hz : 81 ∣ 2 ^ d * minimoResiduo (d % 6) + 1 := by
    apply ((by decide +kernel : Nat.Coprime 81 8).pow_right c).dvd_of_dvd_mul_left
    rw [← he]
    exact dvd_mul_of_dvd_left hd _
  have h2 := potencia_periodica (a := 2) (m := 81) (k := 54) (by decide +kernel) d
  have hd6 : d % 6 = 1 := by
    have h := Nat.mod_mod_of_dvd d (by decide +kernel : 6 ∣ 54)
    omega
  have h := Nat.mod_eq_zero_of_dvd hz
  rw [Nat.add_mod, Nat.mul_mod, h2, hd54, hd6] at h
  norm_num [minimoResiduo] at h

theorem minimos_incompatibles {b c d : ℕ} (hc : 1 ≤ c) :
    9 ^ c * (3 ^ b * minimoResiduo (b % 6) + 1) ≠
      8 ^ c * (2 ^ d * minimoResiduo (d % 6) + 1) := by
  intro he
  have ht := candidatos he
  simp only [tabla324, List.mem_cons, Prod.mk.injEq, List.not_mem_nil, or_false] at ht
  rcases ht with h | h | h | h | h
  · apply descartar_cero (b := b) (c := c) (d := d) (by omega) _ _ he
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 4 ∣ 324); omega
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 6 ∣ 324); omega
  · apply descartar_cero (b := b) (c := c) (d := d) (by omega) _ _ he
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 4 ∣ 324); omega
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 6 ∣ 324); omega
  · apply descartar_cero (b := b) (c := c) (d := d) (by omega) _ _ he
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 4 ∣ 324); omega
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 6 ∣ 324); omega
  · apply descartar_uno (b := b) (c := c) (d := d) (by omega) _ he
    have := Nat.mod_mod_of_dvd d (by decide +kernel : 54 ∣ 324); omega
  · apply descartar_cero (b := b) (c := c) (d := d) (by omega) _ _ he
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 4 ∣ 324); omega
    · have := Nat.mod_mod_of_dvd b (by decide +kernel : 6 ∣ 324); omega

theorem exceso_pareja {b c d r v : ℕ} (hc : 1 ≤ c)
    (hr : r % 72 = minimoResiduo (b % 6))
    (hv : v % 72 = minimoResiduo (d % 6))
    (he : 9 ^ c * (3 ^ b * r + 1) = 8 ^ c * (2 ^ d * v + 1)) :
    minimoResiduo (b % 6) + minimoResiduo (d % 6) + 72 ≤ r + v := by
  have hn := minimos_incompatibles (b := b) (d := d) hc
  have hrd := Nat.mod_add_div r 72
  have hvd := Nat.mod_add_div v 72
  by_contra h
  have hrr : r = minimoResiduo (b % 6) := by omega
  have hvv : v = minimoResiduo (d % 6) := by omega
  exact hn (by simpa only [hrr, hvv] using he)

theorem enlace_compartido {b c d y z t r v : ℕ}
    (ha : Camino (List.replicate b .a) y z)
    (hb : Camino (List.replicate c .b) z t)
    (hr : y + 1 = 2 ^ (b + 2) * r)
    (hv : t + 1 = 2 ^ (d + 2) * v) :
    9 ^ c * (3 ^ b * r + 1) = 8 ^ c * (2 ^ d * v + 1) := by
  have h₁ := racha_a ha
  have h₂ := racha_b hb
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  have hz : z + 1 = 4 * 3 ^ b * r := by
    rw [hr, pow_add] at h₁
    norm_num at h₁
    nlinarith
  rw [pow_add] at hv
  norm_num at hv
  nlinarith [congrArg (fun x => 9 ^ c * x) hz,
    congrArg (fun x => 8 ^ c * x) hv]

theorem pareja_orbital {a b c d e f n y z t u w x : ℕ}
    (ha : 1 ≤ a) (hc : 1 ≤ c) (he : 1 ≤ e)
    (h₁ : Camino (List.replicate a .b) n y)
    (h₂ : Camino (List.replicate b .a) y z)
    (h₃ : Camino (List.replicate c .b) z t)
    (h₄ : Camino (List.replicate d .a) t u)
    (h₅ : Camino (List.replicate e .b) u w)
    (h₆ : Camino (List.replicate f .a) w x) (hx : x % 8 = 3) :
    ∃ r v, y + 1 = 2 ^ (b + 2) * r ∧ t + 1 = 2 ^ (d + 2) * v ∧
      r % 72 = minimoResiduo (b % 6) ∧ v % 72 = minimoResiduo (d % 6) ∧
      minimoResiduo (b % 6) + minimoResiduo (d % 6) + 72 ≤ r + v := by
  obtain ⟨r, hr, hr9, hr8, _⟩ := fronteras ha hc h₁ h₂ h₃ h₄ (entrada_racha_b he h₅)
  obtain ⟨v, hv, hv9, hv8, _⟩ := fronteras hc he h₃ h₄ h₅ h₆ hx
  have rr := tabla_compartida hr9 hr8
  have rv := tabla_compartida hv9 hv8
  exact ⟨r, v, hr, hv, rr, rv,
    exceso_pareja hc rr rv (enlace_compartido h₂ h₃ hr hv)⟩

theorem banda_con_exceso {n b r : ℕ}
    (hr : minimoResiduo (b % 6) + 72 ≤ r)
    (he : 9 * (n + 5) = 32 * (2 ^ b * r + 1)) :
    b + 9 ≤ Nat.clog 2 (n + 5) := by
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  have hmin : 13 ≤ minimoResiduo (b % 6) := by
    interval_cases j : b % 6 <;> norm_num [j, minimoResiduo]
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  have hg : 2 ^ (b + 8) < n + 5 := by
    rw [pow_add]
    norm_num
    nlinarith [Nat.mul_le_mul_left (2 ^ b) (show 85 ≤ r by omega)]
  have := (Nat.lt_clog_iff_pow_lt (by omega : 1 < 2)).mpr hg
  omega

def SinCerosVecinos : List ℕ → Prop
  | [] => True
  | [_] => True
  | a :: b :: resto => 1 ≤ a + b ∧ SinCerosVecinos (b :: resto)

theorem exceso_cadena (cargas : List ℕ) (h : SinCerosVecinos cargas) :
    cargas.length / 2 ≤ cargas.sum := by
  match cargas with
  | [] => simp
  | [a] => simp
  | a :: b :: resto =>
    have hr : SinCerosVecinos resto := by
      cases resto with
      | nil => trivial
      | cons x xs => exact h.2.2
    have hi := exceso_cadena resto hr
    have hab := h.1
    simp only [List.length_cons, List.sum_cons]
    omega
termination_by cargas.length

end PerdicesVentanasConjuntas

#print axioms PerdicesVentanasConjuntas.tabla_inicial
#print axioms PerdicesVentanasConjuntas.tabla_segunda
#print axioms PerdicesVentanasConjuntas.tabla_tercera
#print axioms PerdicesVentanasConjuntas.tabla_cuarta
#print axioms PerdicesVentanasConjuntas.levantar
#print axioms PerdicesVentanasConjuntas.reducir
#print axioms PerdicesVentanasConjuntas.candidatos
#print axioms PerdicesVentanasConjuntas.descartar_cero
#print axioms PerdicesVentanasConjuntas.descartar_uno
#print axioms PerdicesVentanasConjuntas.minimos_incompatibles
#print axioms PerdicesVentanasConjuntas.exceso_pareja
#print axioms PerdicesVentanasConjuntas.enlace_compartido
#print axioms PerdicesVentanasConjuntas.pareja_orbital
#print axioms PerdicesVentanasConjuntas.banda_con_exceso
#print axioms PerdicesVentanasConjuntas.exceso_cadena
