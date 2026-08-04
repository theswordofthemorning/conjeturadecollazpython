/- cadenakc.lean
   LAS SEIS LEYES DE LA CADENA (k, c), demostradas en Lean 4 con k GENERAL.
   (04-08-2026; el 11o .lean del repo. Nucleo puro, sin Mathlib.)

   paseodeladeuda.py establecio que todo estado de par vivo es una forma
   {v, p*v + c} con p = 3^k (k >= 1, el nivel de torre) o p = 1 (la
   frontera k = 0), y que la dinamica entera del par la deciden SEIS
   leyes, una por paridad de v y de c. Aqui se demuestran para
   COEFICIENTE IMPAR ARBITRARIO p (que es mas general que 3^k y cierra
   el pendiente "k general del Lean de torre" en su forma fuerte):
   la escalera de la torre solo necesita que p sea impar y que
   ascender multiplique p por 3 -- las dos cosas estan demostradas.

   Convenciones sin division en los enunciados: v = 2u o 2u+1,
   c = 2j o 2j+1, y p impar se escribe con su testigo q (p = 2q+1).
   Todo sobre Z: c puede ser negativo (torre negativa) y las
   identidades valen para todo entero. -/

def T (n : Int) : Int := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- ── los dos pasos basicos ──
theorem T_par (x : Int) : T (2 * x) = x := by
  unfold T
  have h : (2 * x) % 2 = 0 := by omega
  simp [h]

theorem T_impar (x : Int) : T (2 * x + 1) = 3 * x + 2 := by
  unfold T
  have h : (2 * x + 1) % 2 = 1 := by omega
  simp [h]
  omega

-- ── ayudantes de reescritura (el unico algebra no lineal que hace falta) ──
theorem dos_fuera (p x : Int) : p * (2 * x) = 2 * (p * x) := by
  rw [Int.mul_left_comm]

theorem prod_impar (q u : Int) :
    (2 * q + 1) * (2 * u + 1) = 2 * ((2 * q + 1) * u) + (2 * q + 1) := by
  rw [Int.mul_add, dos_fuera, Int.mul_one]

theorem prod_3u2 (q u : Int) :
    (2 * q + 1) * (3 * u + 2) = 3 * ((2 * q + 1) * u) + 2 * (2 * q + 1) := by
  rw [Int.mul_add, Int.mul_left_comm, Int.mul_comm (2 * q + 1) 2]

-- ══ LAS SEIS LEYES ══

-- N1 (compartido-par): {v, pv + c}, v = 2u, c = 2j  ->  (p, c/2).
--    Vale para TODO p (la paridad de p no hace falta).
theorem ley_N1 (p u j : Int) : T (p * (2 * u) + 2 * j) = p * u + j := by
  rw [dos_fuera]
  unfold T
  have h : (2 * (p * u) + 2 * j) % 2 = 0 := by omega
  simp [h]
  omega

-- N2 (compartido-impar): {v, pv + c}, v = 2u+1, c = 2j, p = 2q+1
--    ->  (p, (3c + 1 - p)/2), o sea el desplazamiento 3j - q.
theorem ley_N2 (q u j : Int) :
    T ((2 * q + 1) * (2 * u + 1) + 2 * j)
      = (2 * q + 1) * (3 * u + 2) + 3 * j - q := by
  rw [prod_impar, prod_3u2]
  unfold T
  have h : (2 * ((2 * q + 1) * u) + (2 * q + 1) + 2 * j) % 2 = 1 := by omega
  simp [h]
  omega

-- N3 (mixto-ASCIENDE, deuda +1): {v, pv + c}, v = 2u, c = 2j+1
--    ->  coeficiente 3p, offset (3c+1)/2 = 3j+2. El mayor gana el impar.
--    Vale para TODO p: la torre sube p -> 3p.
theorem ley_N3 (p u j : Int) :
    T (p * (2 * u) + (2 * j + 1)) = 3 * (p * u) + (3 * j + 2) := by
  rw [dos_fuera]
  unfold T
  have h : (2 * (p * u) + (2 * j + 1)) % 2 = 1 := by omega
  simp [h]
  omega

-- N4 (mixto-COMPENSA, deuda -1): {v, (3p')v + c}, v = 2u+1, c = 2j+1,
--    p' = 2q+1  ->  coeficiente p', offset (c - p')/2 = j - q.
--    El menor gana el impar y la torre BAJA 3p' -> p'.
theorem ley_N4 (q u j : Int) :
    T (3 * ((2 * q + 1) * (2 * u + 1)) + (2 * j + 1))
      = (2 * q + 1) * (3 * u + 2) + (j - q) := by
  rw [prod_impar, prod_3u2]
  unfold T
  have h : (3 * (2 * ((2 * q + 1) * u) + (2 * q + 1)) + (2 * j + 1)) % 2 = 0 := by
    omega
  simp [h]
  omega

-- Los pasos del MENOR en los mixtos (la contabilidad de la deuda):
-- en N3 el menor 2u es par (T = u: no gana impar); en N4 el menor 2u+1
-- es impar (T = 3u+2: gana el impar). Con T_par y T_impar ya estan.
-- La ley de la moneda: el gap (p-1)v + c tiene la paridad de c
-- (p impar => p-1 par), o sea mixto <=> c impar:
theorem ley_moneda (q v c : Int) :
    ((2 * q + 1) * v + c - v) % 2 = c % 2 := by
  have h : (2 * q + 1) * v = 2 * (q * v) + v := by
    rw [Int.add_mul, Int.mul_assoc, Int.one_mul]
  omega

-- ══ LA FUSION Y EL VUELCO (la frontera k = 0..1) ══

-- EL VORTICE: en (1, 1) con v impar los dos lados caen al MISMO valor.
-- Es N4 con q = 0, j = 0: la unica absorcion de la cadena.
theorem vortice_fusion (u : Int) : T (3 * (2 * u + 1) + 1) = T (2 * u + 1) := by
  have h4 := ley_N4 0 u 0
  simp at h4
  rw [T_impar]
  have e : 3 * (2 * u + 1) + 1 = 2 * (3 * u + 2) := by omega
  rw [e, T_par]

-- EL VUELCO (F4): frontera {v, v + g}, v = 2u+1, g = 2j+1: el par
-- aterriza en {u + j + 1, 3u + 2}, que es la forma (1, -(3j+1)):
-- reentra al nucleo con c' = (1 - 3g)/2. Las dos identidades:
theorem ley_F4 (u j : Int) :
    T ((2 * u + 1) + (2 * j + 1)) = u + j + 1 ∧
    T (2 * u + 1) = 3 * (u + j + 1) + (-(3 * j + 1)) := by
  constructor
  · have e : (2 * u + 1) + (2 * j + 1) = 2 * (u + j + 1) := by omega
    rw [e, T_par]
  · rw [T_impar]
    omega

-- ══ LA ESCALERA DE LA TORRE, con p general ══

-- ascender conserva la imparidad del coeficiente (p -> 3p), asi que
-- las seis leyes se aplican en TODOS los pisos: el k general.
theorem escalera_impar (p : Int) (h : p % 2 = 1) : (3 * p) % 2 = 1 := by
  omega

-- y el coeficiente 3^k es impar para todo k, por induccion (la version
-- entera del pow3_impar de torredeladeuda.lean), escrito con la
-- escalera: el piso 0 es p = 1 y cada piso multiplica por 3.
def piso : Nat → Int
  | 0 => 1
  | k + 1 => 3 * piso k

theorem piso_impar : ∀ k, piso k % 2 = 1 := by
  intro k
  induction k with
  | zero => rfl
  | succ n ih => exact escalera_impar (piso n) ih

-- ── casos concretos por el nucleo (decide, no #eval) ──
-- Gatas: (0,1) -1-> (1,-1) -1-> (0,1) es el par (5,6) -> (8,3) -> (4,5)
theorem caso_gatas : T 5 = 8 ∧ T 6 = 3 ∧ T 8 = 4 ∧ T 3 = 5 := by decide
-- Garner: la palabra 0,0,1 desde (0,1): el par (4,5) funde en 3 pasos
theorem caso_garner : T (T (T 4)) = T (T (T 5)) := by decide
-- la puerta P1: (2,2) -1-> (2,-1): el par (5, 47) -> (8, 71) = {8, 9*8-1}
theorem caso_P1 : T 5 = 8 ∧ T 47 = 71 := by decide

#print axioms ley_N1
#print axioms ley_N2
#print axioms ley_N3
#print axioms ley_N4
#print axioms ley_moneda
#print axioms vortice_fusion
#print axioms ley_F4
#print axioms piso_impar
