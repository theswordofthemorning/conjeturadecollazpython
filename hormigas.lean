/-
  EL ESQUELETO ARITMETICO DE HORMIGAS (accesibilidad) Y DEL DESCENSO
  DE FRONTERA DE GOLONDRINAS -- el 14o .lean del repo (09-08-2026).

  Nucleo puro, sin Mathlib. Estilo de la casa (cadenakc/zoologico):
  las leyes se enuncian como IDENTIDADES CON TESTIGOS -- sin division
  dentro de Lean: quien llama entrega los enteros exactos y las
  hipotesis de divisibilidad como ecuaciones, y el teorema da la
  desigualdad o la identidad. Los testigos los produce el .py.

  LO QUE SE DEMUESTRA AQUI:

  1. hormigas_viaje_j0: el viaje de fase 3 del constructor con j = 0
     (c del vuelco ya impar): si 4*g' = 3*g + 1 y g > 1, entonces
     g' < g. [El descenso estricto del gap, caso corto.]
  2. hormigas_viaje_j_ge1: con j >= 1 halvings intermedios: si
     2^(1+j) * d = 3*g - 1 con 2*g' = d + 1 y g >= 1, entonces
     g' < g. [El descenso estricto, caso largo: la cota (3g+3)/8.]
  3. frontera_desciende_F1 / _F2: en la frontera con g = 2^(j+1) * d,
     los dos bits dejan el gap con un factor 2 menos: F1 da 2^j * d y
     F2 da 2^j * (3*d) -- las identidades exactas que hacen al
     descenso de v2(g) DETERMINISTA (la pieza de frontera de L2).
  4. impar_por_tres: d impar => 3*d impar (el factor de F2 conserva
     la paridad: el testigo de que v2 baja EXACTAMENTE 1).

  LO QUE NO ESTA AQUI (pendiente, con su porque): el aterrizaje
  exacto de N2 en v2 = A - 1 exige aritmetica 2-adica con SIGNO
  (c en Z con el vuelco); es el candidato al 15o .lean. Y la
  terminacion COMPLETA del constructor es la composicion de 1-4 con
  la fase de torre: el argumento esta en accesibilidad.py; aqui
  quedan sus piezas aritmeticas selladas por el nucleo.

  CASO CONOCIDO COMPROBADO CONTRA EL REPO (la regla de los .lean):
  g = 5 (impar, > 1): el vuelco da c = (1-15)/2 = -7 impar (j = 0),
  el gap nuevo cumple 4*g' = 3*5 + 1 = 16, g' = 4 < 5. Y g = 3:
  4*g' = 10 no es entero con j = 0 -- en efecto c = -4 es par, j = 2:
  2^3 * 1 = 8 = 3*3 - 1, d = 1, 2*g' = 2, g' = 1 < 3. Los dos
  cerrados abajo con decide/omega sobre los numeros concretos.
-/

-- 4 <= 2^(2+j), por induccion (la base la decide el nucleo)
theorem cuatro_le_pow (j : Nat) : 4 <= 2 ^ (2 + j) := by
  induction j with
  | zero => decide
  | succ n ih =>
    have h : 2 + (n + 1) = (2 + n) + 1 := rfl
    rw [h, Nat.pow_succ]
    omega

-- 1. EL VIAJE CORTO DE HORMIGAS (j = 0): 4*g' = 3*g + 1, g > 1 => g' < g
theorem hormigas_viaje_j0 (g g' : Nat) (h : 4 * g' = 3 * g + 1)
    (hg : 1 < g) : g' < g := by omega

-- 2. EL VIAJE LARGO (j >= 1): 2^(1+j)*d = 3*g - 1, 2*g' = d + 1,
--    g >= 1 => g' < g. (De 2^(1+j) >= 4 sale 4*d <= 3*g - 1, o sea
--    8*g' = 4*d + 4 <= 3*g + 3 < 8*g.)
theorem hormigas_viaje_j_ge1 (g d g' j : Nat) (hj : 1 <= j)
    (hd : 2 ^ (1 + j) * d = 3 * g - 1) (hg' : 2 * g' = d + 1)
    (hg : 1 <= g) : g' < g := by
  cases j with
  | zero => omega
  | succ n =>
    have hpow : 4 <= 2 ^ (1 + (n + 1)) := by
      have h : 1 + (n + 1) = 2 + n := by omega
      rw [h]; exact cuatro_le_pow n
    have hd4 : 4 * d <= 3 * g - 1 := by
      calc 4 * d <= 2 ^ (1 + (n + 1)) * d := Nat.mul_le_mul_right d hpow
        _ = 3 * g - 1 := hd
    omega

-- 3. EL DESCENSO DE FRONTERA, EXACTO: con g = 2^(j+1) * d,
--    F1 (bit 0) deja 2^j * d y F2 (bit 1) deja 2^j * (3*d):
--    las dos identidades que el barrido usa como "ambos bits restan
--    1 a v2(g)".
theorem frontera_desciende_F1 (g d j : Nat) (h : g = 2 ^ (j + 1) * d) :
    2 * (2 ^ j * d) = g := by
  rw [h, Nat.pow_succ]
  calc 2 * (2 ^ j * d) = (2 ^ j * d) * 2 := Nat.mul_comm 2 (2 ^ j * d)
    _ = 2 ^ j * (d * 2) := Nat.mul_assoc (2 ^ j) d 2
    _ = 2 ^ j * (2 * d) := by rw [Nat.mul_comm d 2]
    _ = (2 ^ j * 2) * d := (Nat.mul_assoc (2 ^ j) 2 d).symm

theorem frontera_desciende_F2 (g d j : Nat) (h : g = 2 ^ (j + 1) * d) :
    2 * (2 ^ j * (3 * d)) = 3 * g := by
  rw [h, Nat.pow_succ]
  calc 2 * (2 ^ j * (3 * d)) = (2 * 2 ^ j) * (3 * d) :=
        (Nat.mul_assoc 2 (2 ^ j) (3 * d)).symm
    _ = (2 ^ j * 2) * (3 * d) := by rw [Nat.mul_comm 2 (2 ^ j)]
    _ = 2 ^ j * (2 * (3 * d)) := Nat.mul_assoc (2 ^ j) 2 (3 * d)
    _ = 2 ^ j * (3 * (2 * d)) := by rw [show 2 * (3 * d) = 3 * (2 * d) by omega]
    _ = (2 ^ j * 3) * (2 * d) := (Nat.mul_assoc (2 ^ j) 3 (2 * d)).symm
    _ = (3 * 2 ^ j) * (2 * d) := by rw [Nat.mul_comm (2 ^ j) 3]
    _ = 3 * (2 ^ j * (2 * d)) := Nat.mul_assoc 3 (2 ^ j) (2 * d)
    _ = 3 * ((2 ^ j * 2) * d) := by rw [Nat.mul_assoc (2 ^ j) 2 d]

-- 4. EL FACTOR DE F2 CONSERVA LA PARIDAD: d impar => 3*d impar
--    (por eso v2 baja EXACTAMENTE 1 y no mas).
theorem impar_por_tres (d q : Nat) (h : d = 2 * q + 1) :
    3 * d = 2 * (3 * q + 1) + 1 := by omega

-- LOS DOS CASOS CONOCIDOS, cerrados por el nucleo:
-- g = 5, j = 0: 4*4 = 3*5 + 1 y 4 < 5
theorem caso_g5 : (4 * 4 = 3 * 5 + 1) /\ (4 < 5) := by decide
-- g = 3, j = 2: 2^3 * 1 = 3*3 - 1, 2*1 = 1 + 1, 1 < 3
theorem caso_g3 : (2 ^ (1 + 2) * 1 = 3 * 3 - 1) /\ (2 * 1 = 1 + 1) /\ (1 < 3) := by decide

-- el control final de la casa
#print axioms hormigas_viaje_j0
#print axioms hormigas_viaje_j_ge1
#print axioms frontera_desciende_F1
#print axioms frontera_desciende_F2
#print axioms impar_por_tres
