-- aterrizajen2.lean
--
-- EL ATERRIZAJE DE N2, demostrado en el nucleo (09-08-2026, noche).
-- La pieza 2-adica CON SIGNO del lema del descenso de GOLONDRINAS
-- (oscilacion.py, PIEZA 1), declarada candidata al siguiente .lean en
-- la bitacora 09-08 (5). Con k >= 1 congelado y A = v2(3^k - 1), para
-- c PAR en el nucleo el paso bit 1 es c -> (3c + 1 - 3^k)/2, y:
--
--   (aterrizaje_N2)   si v2(c) > A, el resultado tiene v2 = A - 1
--                     EXACTO;
--   (aterrizaje_c0)   si c = 0, igual: v2 = A - 1 exacto;
--   (descenso_bajo_A) si v2(c) < A, el resultado tiene v2 = v2(c) - 1
--                     EXACTO (el descenso determinista de L2).
--
-- El mecanismo, en una linea: 3c + 1 - 3^k = 3c - (3^k - 1), y con
-- 3^k - 1 = 2^A*(impar): si v2(3c) > A el parentesis es 2^A*(par -
-- impar) = 2^A*impar; si v2(3c) = w < A es 2^w*(impar - par) =
-- 2^w*impar. Al dividir entre 2 queda A - 1 (o w - 1) exacto.
--
-- Estilo de la casa: TESTIGOS SIN DIVISION. La valuacion viaja en los
-- testigos (c = 2^w*u con u impar; el resultado se entrega como
-- 2 * (2^(A-1) * impar explicito), que es la forma "el paso divide
-- entre 2 y deja v2 = A-1"). A se escribe B+1 y w se parametriza para
-- esquivar la resta en Nat. La verificacion numerica masiva es la
-- COMPROBACION 1 de oscilacion.py (110.000 instancias exactas, k <=
-- 10, |c| <= 6000); aqui van ademas dos casos conocidos por decide.
--
-- Nucleo puro, sin Mathlib. Control final: #print axioms sin sorryAx.

def pot2 : Nat → Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

def pot3 : Nat → Int
  | 0 => 1
  | n + 1 => 3 * pot3 n

theorem pot2_add (a b : Nat) : pot2 (a + b) = pot2 a * pot2 b := by
  induction a with
  | zero =>
      rw [Nat.zero_add]
      show pot2 b = 1 * pot2 b
      rw [Int.one_mul]
  | succ n ih =>
      have h1 : n + 1 + b = (n + b) + 1 := by omega
      rw [h1]
      show 2 * pot2 (n + b) = pot2 (n + 1) * pot2 b
      rw [ih]
      show 2 * (pot2 n * pot2 b) = 2 * pot2 n * pot2 b
      rw [Int.mul_assoc]

-- EL ATERRIZAJE (v2(c) > A): con A = B+1, w = B+2+s (o sea w >= A+1),
--   c = 2^(B+2+s) * u   y   3^k - 1 = 2^(B+1) * (2b+1)
--   =>  3c + 1 - 3^k  =  2 * ( 2^B * (2*(3*2^s*u - b - 1) + 1) ).
-- El resultado del paso bit 1, (3c+1-3^k)/2, es 2^B por un IMPAR
-- explicito: v2 = B = A - 1, exacto. (u no necesita ser impar para
-- esta igualdad; la exactitud v2 = A-1 la da el impar de la derecha.)
theorem aterrizaje_N2 (k B s : Nat) (u b : Int)
    (h3 : pot3 k - 1 = pot2 (B + 1) * (2 * b + 1)) :
    3 * (pot2 (B + 2 + s) * u) + 1 - pot3 k
      = 2 * (pot2 B * (2 * (3 * pot2 s * u - b - 1) + 1)) := by
  have hk : pot3 k = pot2 (B + 1) * (2 * b + 1) + 1 := by omega
  have e1 : pot2 (B + 2 + s) = pot2 (B + 1) * pot2 (s + 1) := by
    have h : B + 2 + s = (B + 1) + (s + 1) := by omega
    rw [h, pot2_add]
  have e2 : pot2 (s + 1) = 2 * pot2 s := rfl
  have e3 : pot2 (B + 1) = 2 * pot2 B := rfl
  rw [hk, e1, e2, e3]
  simp only [Int.mul_add, Int.mul_sub,
             Int.mul_assoc, Int.mul_comm, Int.mul_left_comm,
             Int.mul_one, Int.one_mul]
  omega

-- EL CASO c = 0 (v2 infinita): mismo aterrizaje en v2 = A - 1
-- (el impar explicito es -(2b+1) = 2*(-b-1) + 1)
theorem aterrizaje_c0 (k B : Nat) (b : Int)
    (h3 : pot3 k - 1 = pot2 (B + 1) * (2 * b + 1)) :
    3 * 0 + 1 - pot3 k
      = 2 * (pot2 B * (-(2 * b + 1))) := by
  have hk : pot3 k = pot2 (B + 1) * (2 * b + 1) + 1 := by omega
  have e3 : pot2 (B + 1) = 2 * pot2 B := rfl
  rw [hk, e3]
  simp only [Int.mul_neg, Int.mul_add,
             Int.mul_comm, Int.mul_left_comm,
             Int.mul_one, Int.one_mul]
  omega

-- EL DESCENSO BAJO A (v2(c) = w < A): con w = W+1 y A = W+2+r,
--   c = 2^(W+1) * (2a+1)   y   3^k - 1 = 2^(W+2+r) * (2b+1)
--   =>  3c + 1 - 3^k  =  2 * ( 2^W * (2*(3*a + 1 - pot2 r*(2*b+1)) + 1) ).
-- Aqui el testigo impar de c SI hace falta (u = 2a+1): el impar 3u
-- gana al termino par 2^(A-w)*(2b+1) y v2 baja EXACTO en 1.
theorem descenso_bajo_A (k W r : Nat) (a b : Int)
    (h3 : pot3 k - 1 = pot2 (W + 2 + r) * (2 * b + 1)) :
    3 * (pot2 (W + 1) * (2 * a + 1)) + 1 - pot3 k
      = 2 * (pot2 W * (2 * (3 * a + 1 - pot2 r * (2 * b + 1)) + 1)) := by
  have hk : pot3 k = pot2 (W + 2 + r) * (2 * b + 1) + 1 := by omega
  have e1 : pot2 (W + 2 + r) = pot2 (W + 1) * pot2 (r + 1) := by
    have h : W + 2 + r = (W + 1) + (r + 1) := by omega
    rw [h, pot2_add]
  have e2 : pot2 (r + 1) = 2 * pot2 r := rfl
  have e3 : pot2 (W + 1) = 2 * pot2 W := rfl
  rw [hk, e1, e2, e3]
  simp only [Int.mul_add, Int.add_mul, Int.mul_sub,
             Int.mul_assoc, Int.mul_comm, Int.mul_left_comm,
             Int.mul_one, Int.one_mul]
  omega

-- LOS CASOS CONOCIDOS DEL REPO, cerrados por decide (no por #eval):
-- k = 2: 3^2 - 1 = 8 = 2^3*1 (A = 3, B = 2, b = 0).
--   c = 16 = 2^4 (w = 4 > A): (3*16+1-9)/2 = 20 = 2^2 * 5, v2 = 2 = A-1
theorem caso_conocido_aterrizaje :
    3 * 16 + 1 - 9 = 2 * ((4 : Int) * 5) ∧ (5 : Int) % 2 = 1 := by decide
--   c = 2 (w = 1 < A): (3*2+1-9)/2 = -1 = 2^0 * (-1), v2 = 0 = w-1
theorem caso_conocido_descenso :
    3 * 2 + 1 - 9 = 2 * ((1 : Int) * (-1)) ∧ (-1 : Int) % 2 = 1 := by decide

-- y el cruce de los enunciados generales con esos numeros: los mismos
-- valores salen INSTANCIANDO los teoremas (k=2, B=2, s=1/W=0, r=1)
example : 3 * (pot2 (2 + 2 + 0) * 1) + 1 - pot3 2
    = 2 * (pot2 2 * (2 * (3 * pot2 0 * 1 - 0 - 1) + 1)) :=
  aterrizaje_N2 2 2 0 1 0 (by decide)

example : 3 * (pot2 1 * (2 * 0 + 1)) + 1 - pot3 2
    = 2 * (pot2 0 * (2 * (3 * 0 + 1 - pot2 1 * (2 * 0 + 1)) + 1)) :=
  descenso_bajo_A 2 0 1 0 0 (by decide)

#print axioms pot2_add
#print axioms aterrizaje_N2
#print axioms aterrizaje_c0
#print axioms descenso_bajo_A
#print axioms caso_conocido_aterrizaje
