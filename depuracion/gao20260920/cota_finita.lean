/- Certificados universales de aritmética del reloj finito CF.
   No afirma la desigualdad probabilística CF ni la conjetura de Gao. -/
namespace CotaFinitaGao

theorem presupuesto_frontera (m : Nat) :
    (24*m+5)*(48*m+7) <= 2048*(m+1)^2 := by grind

theorem presupuesto_interior (m : Nat) : 10*m+3 <= 16*(m+1) := by omega

theorem crecimiento_exponencial : ∀ j : Nat,
    64*((j+10)+1) <= 2^(j+10) := by
  intro j
  induction j with
  | zero => decide
  | succ j ih =>
    have e : j+1+10 = (j+10)+1 := by omega
    rw [e, Nat.pow_succ]
    omega

theorem presupuesto_reloj (m n : Nat)
    (hn : 64*(m+1) <= n) (hn2 : 2 <= n) :
    2*n*(n^4*(10*m+3)+(24*m+5)*(48*m+7)) <= n^6 := by
  have hb := presupuesto_frontera m
  have hi := presupuesto_interior m
  have hs : (64*(m+1))^2 <= n^2 := Nat.pow_le_pow_left hn 2
  have hb2 : 2*((24*m+5)*(48*m+7)) <= n^2 := by grind
  have hi4 : 4*(10*m+3) <= n := by omega
  have hd : 4*(n^4*(10*m+3)) <= n^5 := by
    have hh := Nat.mul_le_mul_left (n^4) hi4
    grind
  have hn3 : 2 <= n^3 := by
    have hh := Nat.pow_le_pow_left hn2 3
    omega
  have hsmall : 2*n^2 <= n^5 := by
    have hh := Nat.mul_le_mul_left (n^2) hn3
    grind
  have hsum : 2*(n^4*(10*m+3)+(24*m+5)*(48*m+7)) <= n^5 := by omega
  have hh := Nat.mul_le_mul_left n hsum
  grind

-- La guardia debe dar hpaso bajo la ley original, no bajo un futuro condicionado.
-- Aquí se certifica la inducción aritmética de C7, dadas esas desigualdades.
theorem riesgos_finitos (w : Nat → Rat) (p : Rat) (hp : p <= 1)
    (hinicio : w 0 <= 1)
    (hpaso : ∀ j, w (j+1) <= (1-p)*w j) :
    ∀ j, w j <= (1-p)^j := by
  intro j
  induction j with
  | zero => simpa using hinicio
  | succ j ih =>
    have hfactor : 0 <= 1-p := by grind
    have hmul := Rat.mul_le_mul_of_nonneg_left ih hfactor
    calc
      w (j+1) <= (1-p)*w j := hpaso j
      _ <= (1-p)*(1-p)^j := hmul
      _ = (1-p)^(j+1) := by rw [Rat.pow_succ, Rat.mul_comm]

#print axioms presupuesto_frontera
#print axioms presupuesto_interior
#print axioms crecimiento_exponencial
#print axioms presupuesto_reloj
#print axioms riesgos_finitos
end CotaFinitaGao
