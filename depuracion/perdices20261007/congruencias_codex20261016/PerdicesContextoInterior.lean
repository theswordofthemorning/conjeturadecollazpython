import PerdicesRelojTerminal

/-! Nucleo condicional de la construccion con parte impar 13.
Los dos levantamientos, CRT y la existencia de contextos arbitrarios
mantienen prueba escrita. No se formaliza aqui esa existencia universal. -/

namespace PerdicesContextoInterior

open PerdicesTransporteImpar PerdicesRelojTerminal

theorem racha_trece {x a : ℕ} (hx : x + 1 = 13 * 2 ^ (a + 2)) :
    ∃ z, Camino (List.replicate a .a) x z ∧ z + 1 = 52 * 3 ^ a := by
  have hd : 2 ^ (duracion .a * a) ∣ x + constante .a := by
    simp only [duracion, constante, one_mul, hx, pow_add]
    exact ⟨13 * 2 ^ 2, by ring⟩
  obtain ⟨z, hz, he⟩ := continuar_racha .a a x hd
  refine ⟨z, hz, ?_⟩
  apply Nat.eq_of_mul_eq_mul_left (pow_pos (by omega : 0 < 2) a)
  simp only [duracion, constante, D, one_mul] at he
  rw [he, hx, pow_add]
  ring

theorem residuo_frontera {z a : ℕ} (hz : z + 1 = 52 * 3 ^ a)
    (ha : 3 ^ a % 8 = 3) : z % 32 = 27 := by omega

theorem empalme_contexto {us vs : List Bloque} {n x z y a : ℕ}
    (hu : Camino us n x) (hx : x + 1 = 13 * 2 ^ (a + 2))
    (hz : z + 1 = 52 * 3 ^ a) (hv : Camino ([.b, .a, .a] ++ vs) z y) :
    Camino (us ++ List.replicate a .a ++ [.b, .a, .a] ++ vs) n y := by
  obtain ⟨w, hw, he⟩ := racha_trece hx
  have : w = z := by omega
  subst w
  simpa [List.append_assoc] using concatenar (concatenar hu hw) hv

theorem largo_contexto (us vs : List Bloque) (a : ℕ) :
    largo (us ++ List.replicate a .a ++ [.b, .a, .a] ++ vs) =
      largo us + a + 5 + largo vs := by
  simp [largo_concatenar, largo_racha, duracion, largo, Nat.add_assoc]
  omega

theorem altura_trece {n d h factor residuo : ℕ}
    (hh : 0 < h) (hd : factor < 13 * 2 ^ (d + 1))
    (hr : 0 < residuo)
    (he : factor * (n + 5) = 13 * 2 ^ (h + d) + residuo)
    (hc : residuo ≤ 2 ^ h * (factor - 13 * 2 ^ d)) : ell n = h := by
  have hp : 0 < 2 ^ d := by positivity
  have hfd : 13 * 2 ^ d ≤ factor := by
    by_contra hn
    have : factor - 13 * 2 ^ d = 0 := by omega
    rw [this] at hc
    omega
  have hsup : n + 5 ≤ 2 ^ h := by
    have he' : factor * (n + 5) = 2 ^ h * (13 * 2 ^ d) + residuo := by
      simpa [pow_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using he
    have hsub := Nat.sub_add_cancel hfd
    nlinarith
  have hinf : 2 ^ (h - 1) < n + 5 := by
    have hpow : 2 ^ h = 2 ^ (h - 1) * 2 := by
      rw [← pow_succ]; congr 1; omega
    have he' : factor * (n + 5) = 2 ^ (h - 1) * (26 * 2 ^ d) + residuo := by
      rw [he, pow_add, hpow]
      ring
    have hd' : factor < 26 * 2 ^ d := by
      rw [pow_succ] at hd
      nlinarith
    by_contra hn
    have hn' : n + 5 ≤ 2 ^ (h - 1) := by omega
    nlinarith [Nat.mul_le_mul_left factor hn']
  have hlo : h - 1 < Nat.clog 2 (n + 5) :=
    (Nat.lt_clog_iff_pow_lt (by omega)).2 hinf
  have hup := Nat.clog_le_of_le_pow hsup
  simp only [ell]
  omega

theorem defecto_fijo {altura prefijo a d s : ℕ}
    (he : altura + d = prefijo + a + 6) :
    (altura : ℚ) + (27 / 17 : ℚ) * s - prefijo - a =
      6 + (27 / 17 : ℚ) * s - d := by
  have he' : (altura : ℚ) + d = prefijo + a + 6 := by exact_mod_cast he
  linarith

theorem exceso_fijo {altura prefijo sufijo a d : ℕ}
    (he : altura + d = prefijo + a + 6) :
    (prefijo + a + 5 + sufijo : ℤ) - altura = sufijo + d - 1 := by omega

end PerdicesContextoInterior

#print axioms PerdicesContextoInterior.racha_trece
#print axioms PerdicesContextoInterior.residuo_frontera
#print axioms PerdicesContextoInterior.empalme_contexto
#print axioms PerdicesContextoInterior.largo_contexto
#print axioms PerdicesContextoInterior.altura_trece
#print axioms PerdicesContextoInterior.defecto_fijo
#print axioms PerdicesContextoInterior.exceso_fijo
