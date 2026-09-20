/- Refinamiento afín y paridad del ancla. No formaliza la medida producto.
   Independiente del código Python y sin importar archivos del laboratorio. -/
namespace CilindrosGao

def T (x : Int) : Int := if x % 2 = 0 then x/2 else (3*x+1)/2

theorem paso_par (x : Int) : T (2*x) = x := by
  unfold T
  have h : (2*x)%2=0 := by omega
  simp [h]

theorem paso_impar (x : Int) : T (2*x+1) = 3*x+2 := by
  unfold T
  have h : (2*x+1)%2=1 := by omega
  simp [h]
  omega

theorem paridad_pendiente_impar (q m b : Int) :
    ((2*q+1)*m+b)%2 = (m+b)%2 := by
  have h : (2*q+1)*m+b = 2*(q*m)+m+b := by grind
  rw [h]
  omega

theorem paridades_opuestas (b : Int) :
    (b%2=0) ↔ ¬ ((1+b)%2=0) := by omega

theorem refinar_par (a m d b h : Int) (hc : a*d+b=2*h) :
    T (a*(2*m+d)+b) = a*m+h := by
  have he : a*(2*m+d)+b = 2*(a*m+h) := by grind
  rw [he, paso_par]

theorem refinar_impar (a m d b h : Int) (hc : a*d+b=2*h+1) :
    T (a*(2*m+d)+b) = (3*a)*m+(3*h+2) := by
  have he : a*(2*m+d)+b = 2*(a*m+h)+1 := by grind
  rw [he, paso_impar]
  grind

theorem pendiente_sigue_impar (a : Int) (h : a%2=1) :
    (3*a)%2=1 := by omega

theorem orden_frontera_independiente (a b s m : Int) :
    s*m+a <= s*m+b ↔ a<=b := by omega

#print axioms paso_par
#print axioms paso_impar
#print axioms paridad_pendiente_impar
#print axioms paridades_opuestas
#print axioms refinar_par
#print axioms refinar_impar
#print axioms pendiente_sigue_impar
#print axioms orden_frontera_independiente
end CilindrosGao
