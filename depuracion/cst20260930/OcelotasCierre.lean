import OcelotasCertificado

/-! # Ocelotas: bordes y consecuencia para un posible fallo

El caso par no necesita Rhin. En el caso impar, las rachas se representan
mediante Palabra, como en ocelotas_diez. No se postula el certificado finito.
-/

namespace OcelotasCierre

open Ocelotas OcelotasFinito OcelotasTrayectorias OcelotasCertificado

theorem descenso_par {n k : ℕ} (hn : 2 ≤ n) (hpar : n % 2 = 0)
    (hk : PrimerCruce n k) : T^[k] n < n := by
  have h1 : PrimerCruce n 1 := by
    constructor
    · intro j hj hj1
      omega
    · simp [S, hpar]
  have he : k = 1 := primer_cruce_unico hk h1
  subst k
  simpa only [Function.iterate_one, T, if_pos hpar] using
    (Nat.div_lt_self (show 0 < n by omega) (by decide : 1 < 2))

/-- Un fallo representado por rachas reales requiere al menos once, bajo Rhin. -/
theorem fallo_exige_once (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n) :
    11 ≤ r := by
  by_contra h
  have hd := ocelotas_diez hR hn hw hr (by omega : r ≤ 10) hk
  omega

/-- Incluye las semillas pares y las palabras reales de una a diez rachas. -/
theorem descenso_hasta_diez (hR : RhinEntera) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k)
    (hforma : n % 2 = 0 ∨ ∃ r a b, 0 < r ∧ r ≤ 10 ∧
      Palabra n a b r ∧ tiempo a b r = k) : T^[k] n < n := by
  rcases hforma with hpar | ⟨r, a, b, hr, hr10, hw, he⟩
  · exact descenso_par hn hpar hk
  · subst k
    exact ocelotas_diez hR hn hw hr hr10 hk

end OcelotasCierre

#print axioms OcelotasCierre.descenso_par
#print axioms OcelotasCierre.fallo_exige_once
#print axioms OcelotasCierre.descenso_hasta_diez
