/-
  ERIZAS: ingredientes algebraicos del argumento de momentos.
  Las recurrencias son HIPOTESIS aqui. El enlace con la cadena, Cauchy,
  las colas y el argumento asintotico estan escritos en Erizas.md.
  No es una formalizacion integral del teorema de obstruccion.
-/

namespace Erizas

theorem paso_primero (x : Rat) : ((x+1)+(x-1))/2 = x := by grind

theorem paso_segundo (x : Rat) :
    ((x+1)*(x+1)+(x-1)*(x-1))/2 = x*x+1 := by grind

theorem paso_cuarto (x : Rat) :
    ((x+1)^4+(x-1)^4)/2 = x^4+6*x*x+1 := by grind

theorem segundo_acumulado (b : Nat -> Rat) (hb : b 0 = 1)
    (hpaso : forall n, b (n+1) <= b n+1) :
    forall n, b n <= (n : Rat)+1 := by
  intro n
  induction n with
  | zero => simp [hb]; grind
  | succ n ih =>
    have hp := hpaso n
    grind

theorem cuarto_acumulado (b d : Nat -> Rat) (hb : b 0 = 1) (hd : d 0 = 1)
    (hsegundo : forall n, b (n+1) <= b n+1)
    (hcuarto : forall n, d (n+1) <= d n+6*b n+1) :
    forall n, d n <= 3*(n : Rat)^2+4*(n : Rat)+1 := by
  intro n
  induction n with
  | zero => simp [hd]; grind
  | succ n ih =>
    have hp := hcuarto n
    have hbnd := segundo_acumulado b hb hsegundo n
    grind

theorem u_acumulado (u : Nat -> Rat) (a : Rat) (hu : u 0 <= a)
    (hpaso : forall n, u (n+1) <= u n+1/2) :
    forall n, u n <= a+(n : Rat)/2 := by
  intro n
  induction n with
  | zero => simp; grind
  | succ n ih =>
    have hp := hpaso n
    grind

theorem presupuesto_colas (s mala_altura mala_u : Rat)
    (ha : 4*mala_altura <= s) (hu : 4*mala_u <= s) :
    s/2 <= s-mala_altura-mala_u := by grind

theorem identidad_escala (a b rho z : Rat) :
    (z*b-1)-rho*(2*z*a-1) = z*(b-2*rho*a)+(rho-1) := by grind

theorem obstruccion_finita (a b rho z : Rat)
    (h : 1-rho < z*(b-2*rho*a)) :
    rho*(2*z*a-1) < z*b-1 := by grind

#print axioms paso_primero
#print axioms paso_segundo
#print axioms paso_cuarto
#print axioms segundo_acumulado
#print axioms cuarto_acumulado
#print axioms u_acumulado
#print axioms presupuesto_colas
#print axioms identidad_escala
#print axioms obstruccion_finita

end Erizas
