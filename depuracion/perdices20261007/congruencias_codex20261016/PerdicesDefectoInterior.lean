import PerdicesRelojTerminal

/-! Nucleo orbital y aritmetico de la familia con defecto interior fijo.
La existencia del prefijo mediante levantamiento modulo 3^S se prueba
por escrito; no es una conclusion de los lemas condicionales de este modulo. -/

namespace PerdicesDefectoInterior

open PerdicesTransporteImpar PerdicesRelojTerminal

theorem cola_real {x k : ℕ} (hx : x + 1 = 2 ^ (k + 2)) :
    ∃ y, Camino (List.replicate k .a ++ [.b]) x y := by
  have hd : 2 ^ (duracion .a * k) ∣ x + constante .a := by
    simp only [duracion, constante, one_mul, hx, pow_add]
    exact dvd_mul_right _ _
  obtain ⟨z, hz, he⟩ := continuar_racha .a k x hd
  simp only [duracion, constante, D, one_mul] at he
  have hz1 : z + 1 = 4 * 3 ^ k := by
    apply Nat.eq_of_mul_eq_mul_left (pow_pos (by omega : 0 < 2) k)
    rw [he, hx, pow_add]
    ring
  have hodd : 3 ^ k % 2 = 1 := by simp [Nat.pow_mod]
  have hb : 2 ^ duracion .b ∣ z + constante .b := by
    simp only [duracion, constante]
    norm_num
    omega
  obtain ⟨y, hy, _⟩ := paso_divisible .b z hb
  exact ⟨y, concatenar hz (Camino.cons hy (Camino.nil y))⟩

theorem prolongacion_real {ps : List Bloque} {n x k : ℕ}
    (hp : Camino ps n x) (hx : x + 1 = 2 ^ (k + 2)) :
    ∃ y, Camino (ps ++ List.replicate k .a ++ [.b]) n y := by
  obtain ⟨y, hy⟩ := cola_real hx
  exact ⟨y, by simpa [List.append_assoc] using concatenar hp hy⟩

theorem largo_prolongacion (ps : List Bloque) (k : ℕ) :
    largo (ps ++ List.replicate k .a ++ [.b]) = largo ps + k + 3 := by
  simp [largo_concatenar, largo_racha, duracion, largo, Nat.add_assoc]

theorem altura_exacta {n d h factor residuo : ℕ}
    (hh : 0 < h) (hd : factor < 2 ^ (d + 1))
    (hr : 0 < residuo)
    (he : factor * (n + 5) = 2 ^ (h + d) + residuo)
    (hc : residuo ≤ 2 ^ h * (factor - 2 ^ d)) :
    ell n = h := by
  have hp : 0 < 2 ^ d := by positivity
  have hfd : 2 ^ d ≤ factor := by
    by_contra hn
    have : factor - 2 ^ d = 0 := by omega
    rw [this] at hc
    omega
  have hsup : n + 5 ≤ 2 ^ h := by
    have he' : factor * (n + 5) = 2 ^ h * 2 ^ d + residuo := by
      simpa [pow_add] using he
    have hsub : factor - 2 ^ d + 2 ^ d = factor := Nat.sub_add_cancel hfd
    nlinarith
  have hinf : 2 ^ (h - 1) < n + 5 := by
    have hpow : 2 ^ h = 2 ^ (h - 1) * 2 := by
      rw [← pow_succ]; congr 1; omega
    have he' : factor * (n + 5) = 2 ^ (h - 1) * (2 * 2 ^ d) + residuo := by
      simpa [pow_add, hpow, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using he
    have hd' : factor < 2 * 2 ^ d := by simpa [pow_succ, Nat.mul_comm] using hd
    by_contra hn
    have hn' : n + 5 ≤ 2 ^ (h - 1) := by omega
    nlinarith [Nat.mul_le_mul_left factor hn']
  have hlo : h - 1 < Nat.clog 2 (n + 5) :=
    (Nat.lt_clog_iff_pow_lt (by omega)).2 hinf
  have hup := Nat.clog_le_of_le_pow hsup
  simp only [ell]
  omega

theorem defecto_fijo {altura prefijo k d s : ℕ}
    (he : altura + d = prefijo + k + 2) :
    (altura : ℚ) + (27 / 17 : ℚ) * s - prefijo - k =
      2 + (27 / 17 : ℚ) * s - d := by
  have he' : (altura : ℚ) + d = prefijo + k + 2 := by exact_mod_cast he
  linarith

theorem exceso_fijo {altura prefijo k d : ℕ}
    (he : altura + d = prefijo + k + 2) :
    (prefijo + k + 3 : ℤ) - altura = d + 1 := by
  omega

end PerdicesDefectoInterior

#print axioms PerdicesDefectoInterior.cola_real
#print axioms PerdicesDefectoInterior.prolongacion_real
#print axioms PerdicesDefectoInterior.largo_prolongacion
#print axioms PerdicesDefectoInterior.altura_exacta
#print axioms PerdicesDefectoInterior.defecto_fijo
#print axioms PerdicesDefectoInterior.exceso_fijo
