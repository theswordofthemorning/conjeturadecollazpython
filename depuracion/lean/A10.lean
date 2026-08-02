/-
  ITEM A10 — "Collatz sobre los enteros negativos es exactamente el mapa 3m-1
  sobre los positivos".

  MAPA USADO: el CLASICO (n par -> n/2, n impar -> 3n+1), extendido a todo Z.
  El mapa espejo es el 3m-1 CLASICO (m par -> m/2, m impar -> 3m-1).

  Formalizacion: si n = -m, entonces  C(-m) = -(M(m))  para TODO m en Z,
  y por induccion  C^k(-m) = -(M^k(m))  para todo k. Eso es exactamente
  "Collatz sobre los negativos ES el mapa 3m-1 sobre los positivos", con
  el signo como diccionario.

  Nota de division: en Lean 4 el `/` de Int es ediv, pero aqui SOLO se divide
  cuando el numero es par, asi que la division es exacta y no depende del
  convenio (ediv = tdiv = fdiv sobre pares). El `%` de Int es emod (siempre
  no negativo), asi que la paridad de -m coincide con la de m.
-/

set_option maxRecDepth 40000

-- El mapa de Collatz CLASICO sobre Z
def colZ (n : Int) : Int := if n % 2 = 0 then n / 2 else 3 * n + 1

-- El mapa 3m-1 CLASICO sobre Z
def tmuZ (m : Int) : Int := if m % 2 = 0 then m / 2 else 3 * m - 1

-- iteradores
def colIter : Nat → Int → Int
  | 0,     n => n
  | k + 1, n => colIter k (colZ n)

def tmuIter : Nat → Int → Int
  | 0,     m => m
  | k + 1, m => tmuIter k (tmuZ m)

-- ============================================================
-- LA TRAMPA: comprobar que colZ es Collatz de verdad, contra
-- casos conocidos, POR EL NUCLEO (by decide, no #eval).
-- ============================================================

-- 7 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 (mapa clasico)
theorem colZ_es_collatz :
    colZ 7 = 22 ∧ colZ 22 = 11 ∧ colZ 11 = 34 ∧ colZ 34 = 17 ∧
    colZ 17 = 52 ∧ colZ 52 = 26 ∧ colZ 26 = 13 := by decide

-- 27 tarda 111 pasos clasicos en llegar a 1 (record conocido chico):
-- comprobamos el prefijo 27 -> 82 -> 41 -> 124 -> 62 -> 31 -> 94 -> 47
theorem colZ_27 : colIter 7 27 = 47 := by decide

-- el mapa 3m-1 contra su definicion: 5 -> 14 -> 7 -> 20 -> 10 -> 5 (ciclo de largo 5)
theorem tmuZ_es_3m1 :
    tmuZ 5 = 14 ∧ tmuZ 14 = 7 ∧ tmuZ 7 = 20 ∧ tmuZ 20 = 10 ∧ tmuZ 10 = 5 := by decide

-- ============================================================
-- EL TEOREMA DEL PASO:  C(-m) = -(M(m))  para TODO m en Z
-- (mas fuerte que el enunciado, que pide m >= 1)
-- ============================================================

theorem paso (m : Int) : colZ (-m) = -(tmuZ m) := by
  unfold colZ tmuZ
  by_cases h : m % 2 = 0
  · have h' : (-m) % 2 = 0 := by omega
    rw [if_pos h, if_pos h']
    omega
  · have h' : ¬((-m) % 2 = 0) := by omega
    rw [if_neg h, if_neg h']
    omega

-- ============================================================
-- LA TRAYECTORIA ENTERA:  C^k(-m) = -(M^k(m))  para todo k y todo m
-- ============================================================

theorem trayectoria (k : Nat) : ∀ m : Int, colIter k (-m) = -(tmuIter k m) := by
  induction k with
  | zero => intro m; rfl
  | succ k ih =>
      intro m
      show colIter k (colZ (-m)) = -(tmuIter k (tmuZ m))
      rw [paso]
      exact ih (tmuZ m)

-- ============================================================
-- BORDES, comprobados por el nucleo
-- ============================================================

-- m = 0 (fuera del ambito declarado, pero el teorema tambien lo cubre)
theorem borde_m0 : colZ (-0) = -(tmuZ 0) := by decide

-- m = 1: el ciclo [-1, -2] de Collatz negativo = ciclo [1, 2] de 3m-1
theorem ciclo_menos1 : colIter 2 (-1) = -1 := by decide
theorem ciclo_1 : tmuIter 2 1 = 1 := by decide

-- m = 2 (par chico)
theorem borde_m2 : colZ (-2) = -(tmuZ 2) := by decide

-- el ciclo de largo 5:  [-5,-14,-7,-20,-10] contra [5,14,7,20,10]
theorem ciclo_menos5 : colIter 5 (-5) = -5 := by decide
theorem ciclo_5 : tmuIter 5 5 = 5 := by decide

-- el ciclo de largo 18: [-17, -50, -25, ..., -34] contra el de 3m-1
theorem ciclo_menos17 : colIter 18 (-17) = -17 := by decide
theorem ciclo_17 : tmuIter 18 17 = 17 := by decide

-- un caso "corriente" largo, espejo paso a paso comprobado por decide
-- (instancia concreta del teorema, para atrapar un enunciado mal escrito)
theorem espejo_100 : colIter 25 (-100) = -(tmuIter 25 100) := by decide
theorem espejo_101 : colIter 25 (-101) = -(tmuIter 25 101) := by decide

-- ============================================================
-- CONTROL DE AXIOMAS
-- ============================================================
#print axioms paso
#print axioms trayectoria
#print axioms colZ_es_collatz
#print axioms colZ_27
#print axioms tmuZ_es_3m1
#print axioms ciclo_menos5
#print axioms ciclo_menos17
#print axioms espejo_100
