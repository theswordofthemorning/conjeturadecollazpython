/- Ingredientes de los corolarios de Moscas/Gacelas/Hormigas, 20-09-2026.
   No formaliza probabilidades, paradas, Borel-Cantelli ni densidad.
   Las variables racionales describen coordenadas normalizadas;
   el enlace completo con la cadena entera se prueba por escrito.
-/
namespace Gao20260920

set_option maxRecDepth 20000
set_option exponentiation.threshold 4096

def absoluto (x : Rat) : Rat := if x < 0 then -x else x

theorem dominacion_afin (u a d : Rat) (ha : a = 1/2 ∨ a = 3/2)
    (hd0 : -(1/2 : Rat) <= d) (hd1 : d <= (1/2 : Rat)) :
    absoluto (a*u+d) <= a*absoluto u + 1/2 := by
  rcases ha with rfl | rfl <;>
    unfold absoluto <;> split <;> split <;> grind

theorem puerta_vuelco (g : Rat) (hg : 0 <= g) :
    absoluto ((1/3-g)/2) <= (3/2)*g+1/2 := by
  unfold absoluto
  split <;> grind

theorem k1_rama_par_unica (j : Int) :
    (j % 2 = 0) ↔ ¬ ((3*j-1) % 2 = 0) := by omega

theorem viaje_gap (g d nuevo : Nat) (hg : 3 <= g)
    (hd : 2*d <= 3*g-1) (hn : 2*nuevo = d+1) :
    6*nuevo <= 5*g := by omega

theorem cuatro_viajes : 2*5^4 < 6^4 := by decide

theorem cota_longitud (m : Nat) :
    m+2+4*m*(m+2)+(4*m+1)*m+3 <= 16*(m+1)^2 := by
  grind

theorem parametros_salida (t : Nat) (ht : 1 <= t) :
    256*(t+1)^2+1 >= 128*(2*t+3) := by
  grind

theorem binomial_paso (m : Nat) :
    (2*m+1)^2*(m+2) <= 4*(m+1)^3 := by
  grind

theorem lambda_certificado : (15 : Rat)/16 < (31/32)^2 := by grind

theorem producto_bloque : 2*31^32 < 32^32 := by decide

theorem producto_cuarto :
    16*62^2*61^2048*2051 <= 62^2048 := by decide

theorem producto_monotono (t : Nat) (ht : 29 <= t) :
    61^2*(2*t+5) <= 62^2*(2*t+3) := by omega

#print axioms dominacion_afin
#print axioms puerta_vuelco
#print axioms k1_rama_par_unica
#print axioms viaje_gap
#print axioms cuatro_viajes
#print axioms cota_longitud
#print axioms parametros_salida
#print axioms binomial_paso
#print axioms lambda_certificado
#print axioms producto_bloque
#print axioms producto_cuarto
#print axioms producto_monotono
end Gao20260920
