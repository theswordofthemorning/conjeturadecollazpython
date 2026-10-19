import PerdicesRelojTerminal
import PerdicesDosCambios

/-! Cotas de reloj con un numero fijado de rachas. La relajacion lineal
conserva el crecimiento del prefijo, pero no certifica un reloj uniforme. -/

namespace PerdicesRelojRachas

open PerdicesTransporteImpar PerdicesRelojTerminal

theorem balance_racha {p : Bloque} {k x y : ℕ}
    (h : Camino (List.replicate k p) x y) :
    2 ^ (duracion p * k) * (y + constante p) = D p ^ k * (x + constante p) := by
  induction k generalizing x with
  | zero => cases h; simp
  | succ k ih =>
    cases h with
    | @cons _ _ _ z _ hp ht =>
      have he := ih ht
      have hb : 2 ^ duracion p * (z + constante p) = D p * (x + constante p) := by
        cases p <;> simp_all only [Paso, N, D, E, duracion, constante] <;> omega
      rw [Nat.mul_succ, pow_add, pow_succ]
      nlinarith [congrArg (fun t => 2 ^ duracion p * t) he,
        congrArg (fun t => D p ^ k * t) hb]

theorem consumo_racha {p : Bloque} {k x y : ℕ}
    (h : Camino (List.replicate k p) x y) :
    duracion p * k + orden (y + constante p) = orden (x + constante p) := by
  have he := balance_racha h
  cases p
  · simp only [duracion, constante, D] at he ⊢
    exact PerdicesDosCambios.consumo he (by omega) (by omega)
  · simp only [duracion, constante, D] at he ⊢
    have ht : 2 ^ (3 * k) * (y + 5) = 3 ^ (2 * k) * (x + 5) := by
      simpa [pow_mul] using he
    exact PerdicesDosCambios.consumo ht (by omega) (by omega)

theorem cota_racha_prefijo {ps : List Bloque} {n x y k : ℕ} {p : Bloque}
    (hp : Camino ps n x) (hr : Camino (List.replicate k p) x y) :
    17 * (largo ps + duracion p * k + orden (y + constante p)) ≤
      27 * impares ps + 17 * ell n := by
  have hc : 1 ≤ constante p ∧ constante p ≤ 5 := by cases p <;> simp [constante]
  have he := (encaje_potencial hp hc).2
  have hv : 2 ^ orden (x + constante p) ≤ x + constante p :=
    Nat.le_of_dvd (by omega) pow_padicValNat_dvd
  have ht := PerdicesDosCambios.cota_orden he (Nat.le_pow_clog (by omega : 1 < 2) (n + 5)) hv
  rw [← consumo_racha hr] at ht
  simpa [ell, Nat.add_assoc] using ht

theorem impares_concatenar (us vs : List Bloque) :
    impares (us ++ vs) = impares us + impares vs := by
  induction us with
  | nil => simp [impares]
  | cons p us ih => cases p <;> simp [impares, ih, Nat.add_assoc]

theorem impares_racha (p : Bloque) (k : ℕ) :
    impares (List.replicate k p) = (match p with | .a => 1 | .b => 2) * k := by
  induction k with
  | zero => simp [impares]
  | succ k ih => cases p <;> simp [List.replicate_succ, impares] at * <;> omega

theorem reloj_aba {a b c n x y z : ℕ}
    (h1 : Camino (List.replicate a .a) n x)
    (h2 : Camino (List.replicate b .b) x y)
    (h3 : Camino (List.replicate c .a) y z) :
    289 * (a + 3*b + c + orden (z + 1)) ≤ 1234 * ell n := by
  have ha := cota_racha_prefijo (Camino.nil n) h1
  have hb := cota_racha_prefijo h1 h2
  have hc := cota_racha_prefijo (concatenar h1 h2) h3
  simp only [largo, impares, largo_racha, impares_racha, largo_concatenar,
    impares_concatenar, duracion, constante, one_mul] at ha hb hc
  omega

theorem reloj_bab {a b c n x y z : ℕ}
    (h1 : Camino (List.replicate a .b) n x)
    (h2 : Camino (List.replicate b .a) x y)
    (h3 : Camino (List.replicate c .b) y z) :
    289 * (3*a + b + 3*c + orden (z + 5)) ≤ 1081 * ell n := by
  have ha := cota_racha_prefijo (Camino.nil n) h1
  have hb := cota_racha_prefijo h1 h2
  have hc := cota_racha_prefijo (concatenar h1 h2) h3
  simp only [largo, impares, largo_racha, impares_racha, largo_concatenar,
    impares_concatenar, duracion, constante, one_mul] at ha hb hc
  omega

theorem reloj_abab {a b c d n x y z w : ℕ}
    (h1 : Camino (List.replicate a .a) n x)
    (h2 : Camino (List.replicate b .b) x y)
    (h3 : Camino (List.replicate c .a) y z)
    (h4 : Camino (List.replicate d .b) z w) :
    4913 * (a + 3*b + c + 3*d + orden (w + 5)) ≤ 34100 * ell n := by
  have ha := cota_racha_prefijo (Camino.nil n) h1
  have hb := cota_racha_prefijo h1 h2
  have hc := cota_racha_prefijo (concatenar h1 h2) h3
  have hd := cota_racha_prefijo (concatenar (concatenar h1 h2) h3) h4
  simp only [largo, impares, largo_racha, impares_racha, largo_concatenar,
    impares_concatenar, duracion, constante, one_mul] at ha hb hc hd
  omega

theorem reloj_baba {a b c d n x y z w : ℕ}
    (h1 : Camino (List.replicate a .b) n x)
    (h2 : Camino (List.replicate b .a) x y)
    (h3 : Camino (List.replicate c .b) y z)
    (h4 : Camino (List.replicate d .a) z w) :
    4913 * (3*a + b + 3*c + d + orden (w + 1)) ≤ 27125 * ell n := by
  have ha := cota_racha_prefijo (Camino.nil n) h1
  have hb := cota_racha_prefijo h1 h2
  have hc := cota_racha_prefijo (concatenar h1 h2) h3
  have hd := cota_racha_prefijo (concatenar (concatenar h1 h2) h3) h4
  simp only [largo, impares, largo_racha, impares_racha, largo_concatenar,
    impares_concatenar, duracion, constante, one_mul] at ha hb hc hd
  omega

def gamma : Bloque → ℚ | .a => 10/17 | .b => 1/17

def coeficiente : List Bloque → ℚ
  | [] => 0
  | p :: ps => 1 + (1 + gamma p) * coeficiente ps

def coste : List (Bloque × ℚ) → ℚ
  | [] => 0
  | (_, d) :: rs => d + coste rs

def Admisible : ℚ → List (Bloque × ℚ) → Prop
  | _, [] => True
  | h, (p, d) :: rs => 0 ≤ d ∧ d ≤ h ∧ Admisible (h + gamma p * d) rs

theorem coeficiente_no_negativo (ps : List Bloque) : 0 ≤ coeficiente ps := by
  induction ps with
  | nil => simp [coeficiente]
  | cons p ps ih => cases p <;> simp [coeficiente, gamma] <;> linarith

theorem cota_relajacion {rs : List (Bloque × ℚ)} {h : ℚ}
    (hh : 0 ≤ h) (hr : Admisible h rs) :
    coste rs ≤ coeficiente (rs.map Prod.fst) * h := by
  induction rs generalizing h with
  | nil => simp [coste, coeficiente]
  | cons r rs ih =>
    obtain ⟨p, d⟩ := r
    obtain ⟨hd, hdh, ht⟩ := hr
    have hg : 0 ≤ gamma p := by cases p <;> norm_num [gamma]
    have hi := ih (by nlinarith : 0 ≤ h + gamma p * d) ht
    have hc := coeficiente_no_negativo (rs.map Prod.fst)
    simp only [coste, List.map_cons, coeficiente] at *
    nlinarith [mul_nonneg hc (mul_nonneg hg (sub_nonneg.mpr hdh))]

def saturada : ℚ → List Bloque → List (Bloque × ℚ)
  | _, [] => []
  | h, p :: ps => (p, h) :: saturada ((1 + gamma p) * h) ps

theorem saturada_admisible (ps : List Bloque) {h : ℚ} (hh : 0 ≤ h) :
    Admisible h (saturada h ps) := by
  induction ps generalizing h with
  | nil => trivial
  | cons p ps ih =>
    have hg : 0 ≤ gamma p := by cases p <;> norm_num [gamma]
    refine ⟨hh, le_rfl, ?_⟩
    rw [show h + gamma p * h = (1 + gamma p) * h by ring]
    exact ih (by nlinarith : 0 ≤ (1 + gamma p) * h)

theorem coste_saturada (ps : List Bloque) (h : ℚ) :
    coste (saturada h ps) = coeficiente ps * h := by
  induction ps generalizing h with
  | nil => simp [saturada, coste, coeficiente]
  | cons p ps ih => simp only [saturada, coste, coeficiente, ih]; ring

theorem coeficiente_ge_longitud (ps : List Bloque) :
    (ps.length : ℚ) ≤ coeficiente ps := by
  induction ps with
  | nil => simp [coeficiente]
  | cons p ps ih =>
    have hc := coeficiente_no_negativo ps
    have hg : 0 ≤ gamma p := by cases p <;> norm_num [gamma]
    simp only [List.length_cons, Nat.cast_add, Nat.cast_one, coeficiente]
    nlinarith

def descuento : ℚ → List (Bloque × ℚ) → ℚ
  | _, [] => 0
  | h, (p, d) :: rs =>
      (1 + gamma p * coeficiente (rs.map Prod.fst)) * (h - d) +
        descuento (h + gamma p * d) rs

theorem identidad_defectos (rs : List (Bloque × ℚ)) (h : ℚ) :
    coste rs + descuento h rs = coeficiente (rs.map Prod.fst) * h := by
  induction rs generalizing h with
  | nil => simp [coste, descuento, coeficiente]
  | cons r rs ih =>
    obtain ⟨p, d⟩ := r
    have ht := ih (h + gamma p * d)
    simp only [coste, descuento, List.map_cons, coeficiente]
    nlinarith only [ht]

def Reserva : ℚ → ℚ → List (Bloque × ℚ) → Prop
  | _, _, [] => True
  | k, h, (p, d) :: rs =>
      0 ≤ d ∧ d + k = h ∧ Reserva k (h + gamma p * d) rs

theorem reserva_constante (ps : List Bloque) {h k : ℚ} (hh : k ≤ h) :
    Reserva k h (saturada (h - k) ps) := by
  induction ps generalizing h with
  | nil => trivial
  | cons p ps ih =>
    have hg : 0 ≤ gamma p := by cases p <;> norm_num [gamma]
    change 0 ≤ h - k ∧ h - k + k = h ∧
      Reserva k (h + gamma p * (h - k)) (saturada ((1 + gamma p) * (h - k)) ps)
    refine ⟨sub_nonneg.mpr hh, by ring, ?_⟩
    have ht := ih (h := h + gamma p * (h - k)) (by nlinarith)
    rw [show (1 + gamma p) * (h - k) = (h + gamma p * (h - k)) - k by ring]
    exact ht

end PerdicesRelojRachas

#print axioms PerdicesRelojRachas.balance_racha
#print axioms PerdicesRelojRachas.consumo_racha
#print axioms PerdicesRelojRachas.cota_racha_prefijo
#print axioms PerdicesRelojRachas.impares_concatenar
#print axioms PerdicesRelojRachas.impares_racha
#print axioms PerdicesRelojRachas.reloj_aba
#print axioms PerdicesRelojRachas.reloj_bab
#print axioms PerdicesRelojRachas.reloj_abab
#print axioms PerdicesRelojRachas.reloj_baba
#print axioms PerdicesRelojRachas.coeficiente_no_negativo
#print axioms PerdicesRelojRachas.cota_relajacion
#print axioms PerdicesRelojRachas.saturada_admisible
#print axioms PerdicesRelojRachas.coste_saturada
#print axioms PerdicesRelojRachas.coeficiente_ge_longitud
#print axioms PerdicesRelojRachas.identidad_defectos
#print axioms PerdicesRelojRachas.reserva_constante
