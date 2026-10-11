import PerdicesMinimos

/-! # Perdices: presupuesto entero para repetir un bloque expansivo.

Los datos afines de un bloque son D=3^s, N=2^d, E y C=D-N>0.
Las ecuaciones de cada bloque se declaran como hipótesis; su lectura como
palabra de paridades usa la biyección ya documentada en Semilla.
-/

namespace PerdicesRepeticiones

open Ocelotas CasaPlano PerdicesCola PerdicesTamano PerdicesAporte

theorem potencial_paso {N D C E x y : ℕ}
    (hD : D = N + C) (h : N * y = D * x + E) :
    N * (C * y + E) = D * (C * x + E) := by
  nlinarith [congrArg (C * ·) h]

theorem potencial_repetido {N D C E : ℕ} (hD : D = N + C)
    (x : ℕ → ℕ) (r : ℕ)
    (h : ∀ j, j < r → N * x (j + 1) = D * x j + E) :
    N ^ r * (C * x r + E) = D ^ r * (C * x 0 + E) := by
  induction r with
  | zero => simp
  | succ r ih =>
    have hp := potencial_paso hD (h r (by omega))
    have ha := ih (fun j hj => h j (by omega))
    calc
      _ = N ^ r * (N * (C * x (r + 1) + E)) := by ring
      _ = N ^ r * (D * (C * x r + E)) := by rw [hp]
      _ = D * (N ^ r * (C * x r + E)) := by ring
      _ = D * (D ^ r * (C * x 0 + E)) := by rw [ha]
      _ = _ := by ring

theorem divisibilidad_repeticion {d s C E : ℕ}
    (hD : 3 ^ s = 2 ^ d + C) (x : ℕ → ℕ) (r : ℕ)
    (h : ∀ j, j < r → 2 ^ d * x (j + 1) = 3 ^ s * x j + E) :
    2 ^ (d * r) ∣ C * x 0 + E := by
  have he := potencial_repetido hD x r h
  have hd : (2 ^ d) ^ r ∣ (3 ^ s) ^ r * (C * x 0 + E) :=
    ⟨C * x r + E, he.symm⟩
  have hc : Nat.Coprime ((2 ^ d) ^ r) ((3 ^ s) ^ r) :=
    (Nat.Coprime.pow d s (by decide : Nat.Coprime 2 3)).pow r r
  simpa only [← pow_mul] using hc.dvd_of_dvd_mul_left hd

theorem presupuesto_repeticion {d s C E : ℕ}
    (hD : 3 ^ s = 2 ^ d + C) (x : ℕ → ℕ) (r : ℕ)
    (hp : 0 < C * x 0 + E)
    (h : ∀ j, j < r → 2 ^ d * x (j + 1) = 3 ^ s * x j + E) :
    2 ^ (d * r) ≤ C * x 0 + E :=
  Nat.le_of_dvd hp (divisibilidad_repeticion hD x r h)

theorem presupuesto_orbital {n u d s C E r : ℕ}
    (hD : 3 ^ s = 2 ^ d + C) (hp : 0 < C * T^[u] n + E)
    (h : ∀ j, j < r →
      2 ^ d * T^[u + d * (j + 1)] n = 3 ^ s * T^[u + d * j] n + E) :
    2 ^ (d * r) ≤ C * T^[u] n + E := by
  simpa using presupuesto_repeticion hD (fun j => T^[u + d * j] n) r
    (by simpa using hp) h

theorem cota_reloj (n u : ℕ) :
    2 ^ u * (T^[u] n + 1) ≤ 3 ^ u * (n + 1) := by
  have h := PerdicesColisiones.cota_afin n u
  have hs := Nat.pow_le_pow_right (by decide : 1 ≤ 3) (PerdicesEstela.S_le_pasos u n)
  nlinarith [Nat.mul_le_mul_right n hs]

theorem presupuesto_reloj {n u d s C E r : ℕ}
    (hD : 3 ^ s = 2 ^ d + C) (hp : 0 < C * T^[u] n + E)
    (h : ∀ j, j < r →
      2 ^ d * T^[u + d * (j + 1)] n = 3 ^ s * T^[u + d * j] n + E) :
    2 ^ (u + d * r) ≤ max C E * 3 ^ u * (n + 1) := by
  have hb := presupuesto_orbital hD hp h
  have hm : C * T^[u] n + E ≤ max C E * (T^[u] n + 1) := by
    nlinarith [Nat.mul_le_mul_right (T^[u] n) (le_max_left C E), le_max_right C E]
  calc
    _ = 2 ^ u * 2 ^ (d * r) := pow_add _ _ _
    _ ≤ 2 ^ u * (max C E * (T^[u] n + 1)) := Nat.mul_le_mul_left _ (hb.trans hm)
    _ = max C E * (2 ^ u * (T^[u] n + 1)) := by ring
    _ ≤ max C E * (3 ^ u * (n + 1)) := Nat.mul_le_mul_left _ (cota_reloj n u)
    _ = _ := by ring

theorem presupuesto_largo {n u d s C E r : ℕ}
    (hD : 3 ^ s = 2 ^ d + C) (hp : 0 < C * T^[u] n + E)
    (h : ∀ j, j < r →
      2 ^ d * T^[u + d * (j + 1)] n = 3 ^ s * T^[u + d * j] n + E)
    (hl : u ≤ d * r) :
    4 ^ u ≤ max C E * 3 ^ u * (n + 1) := by
  calc
    _ = 2 ^ (u + u) := by rw [show u + u = 2 * u by omega, pow_mul]; norm_num
    _ ≤ 2 ^ (u + d * r) := Nat.pow_le_pow_right (by decide) (by omega)
    _ ≤ _ := presupuesto_reloj hD hp h

theorem presupuesto_cohete {n u d s C E r : ℕ}
    (hn : 0 < n) (hi : Function.Injective (fun j => T^[j] n))
    (hD : 3 ^ s = 2 ^ d + C) (hp : 0 < C * T^[u] n + E)
    (h : ∀ j, j < r →
      2 ^ d * T^[u + d * (j + 1)] n = 3 ^ s * T^[u + d * j] n + E) :
    (2 : ℝ) ^ (d * r) * inverso n u ≤ max C E * estatura n := by
  have hb : (2 : ℝ) ^ (d * r) ≤ C * (T^[u] n : ℝ) + E := by
    exact_mod_cast presupuesto_orbital hD hp h
  have hm : (C : ℝ) * T^[u] n + E ≤ (max C E : ℕ) * ((T^[u] n : ℝ) + 1) := by
    have hC : (C : ℝ) ≤ (max C E : ℕ) := by exact_mod_cast le_max_left C E
    have hE : (E : ℝ) ≤ (max C E : ℕ) := by exact_mod_cast le_max_right C E
    nlinarith [mul_le_mul_of_nonneg_right hC (Nat.cast_nonneg (T^[u] n))]
  have ha := aumentado_acota hn hi u
  have he : aumentado n u = ((T^[u] n : ℝ) + 1) * inverso n u := by
    unfold aumentado normalizado
    ring
  rw [he] at ha
  calc
    _ ≤ ((max C E : ℕ) : ℝ) * (((T^[u] n : ℝ) + 1) * inverso n u) := by
      nlinarith [mul_le_mul_of_nonneg_right (hb.trans hm) (inverso_pos n u).le]
    _ ≤ _ := mul_le_mul_of_nonneg_left ha (Nat.cast_nonneg _)

theorem defecto_variable {N D C E F x y : ℤ}
    (h : N * y = D * x + F) :
    N * (C * y + E) = D * (C * x + E) + (C * F - E * (D - N)) := by
  linear_combination C * h

theorem salto_cientodiez {x y z : ℕ} (hz : x + 1 = 4 * z)
    (h : 8 * y = 9 * x + 5) : 2 * (y + 1) = 9 * z + 1 := by
  omega

theorem entre_cientodiez {a z z' h : ℕ}
    (hb : 2 * h = 9 * z + 1)
    (ha : 2 ^ a * (4 * z') = 3 ^ a * h) :
    2 ^ (a + 3) * z' = 3 ^ a * (9 * z + 1) := by
  rw [pow_add]
  norm_num
  nlinarith [congrArg (3 ^ a * ·) hb]

theorem intervalo_uno {t : ℝ} (h1 : 1 ≤ t) (h5 : t ≤ 5) :
    1 ≤ (1 + 2 * t) / 3 ∧ (1 + 2 * t) / 3 ≤ 5 := by
  constructor <;> linarith

theorem intervalo_cientodiez {t : ℝ} (h1 : 1 ≤ t) (h5 : t ≤ 5) :
    1 ≤ (5 + 8 * t) / 9 ∧ (5 + 8 * t) / 9 ≤ 5 := by
  constructor <;> linarith

#print axioms PerdicesRepeticiones.potencial_paso
#print axioms PerdicesRepeticiones.potencial_repetido
#print axioms PerdicesRepeticiones.divisibilidad_repeticion
#print axioms PerdicesRepeticiones.presupuesto_repeticion
#print axioms PerdicesRepeticiones.presupuesto_orbital
#print axioms PerdicesRepeticiones.cota_reloj
#print axioms PerdicesRepeticiones.presupuesto_reloj
#print axioms PerdicesRepeticiones.presupuesto_largo
#print axioms PerdicesRepeticiones.presupuesto_cohete
#print axioms PerdicesRepeticiones.defecto_variable
#print axioms PerdicesRepeticiones.salto_cientodiez
#print axioms PerdicesRepeticiones.entre_cientodiez
#print axioms PerdicesRepeticiones.intervalo_uno
#print axioms PerdicesRepeticiones.intervalo_cientodiez

end PerdicesRepeticiones
