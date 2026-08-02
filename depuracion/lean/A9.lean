/-
  ITEM A9: "el rumbo de una rama del coral solo depende de (A,B):
            rumbo = A*giro_impar + B*giro_par"
  Cuantificador: todo_n.

  MAPA: el clasico (n/2 si par, 3n+1 si impar), definido aqui mismo.
  El lema central (rumbo_cuenta) es sobre la LISTA de paridades y no
  depende del mapa: vale igual para atajo y 3n-1, porque solo usa que
  la suma de angulos es conmutativa y asociativa.

  Angulos modelados en Int: el argumento solo usa (+, conmutativa,
  asociativa, distributiva sobre el multiplo entero), que es lo que
  tienen tambien los angulos reales modulo 2*pi.
-/

set_option maxRecDepth 40000

-- el mapa CLASICO, escrito aqui, no importado de ningun sitio
def paso (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

-- vector de paridad de k pasos desde n (true = el paso fue impar)
def paridades : Nat → Nat → List Bool
  | _, 0     => []
  | n, k + 1 => (n % 2 == 1) :: paridades (paso n) k

-- cuantos pasos impares (A) y pares (B) hay en una lista de paridades
def nImpares : List Bool → Int
  | []     => 0
  | b :: l => (if b then 1 else 0) + nImpares l

def nPares : List Bool → Int
  | []     => 0
  | b :: l => (if b then 0 else 1) + nPares l

-- el rumbo: se suma giro_impar en cada paso impar y giro_par en cada par,
-- EN EL ORDEN en que aparecen (es un fold sobre la rama)
def rumbo (gi gp : Int) : List Bool → Int
  | []     => 0
  | b :: l => (if b then gi else gp) + rumbo gi gp l

-- A y B de la trayectoria de Collatz (mapa clasico), y su rumbo
def A (n k : Nat) : Int := nImpares (paridades n k)
def B (n k : Nat) : Int := nPares  (paridades n k)
def rumboDesde (gi gp : Int) (n k : Nat) : Int := rumbo gi gp (paridades n k)

-- ============================================================
-- EL TEOREMA CENTRAL: el rumbo de CUALQUIER lista de paridades
-- es nImpares*gi + nPares*gp. El orden de los giros no importa.
-- ============================================================
theorem rumbo_cuenta (gi gp : Int) :
    ∀ l : List Bool, rumbo gi gp l = nImpares l * gi + nPares l * gp := by
  intro l
  induction l with
  | nil =>
    show (0 : Int) = 0 * gi + 0 * gp
    rw [Int.zero_mul, Int.zero_mul, Int.zero_add]
  | cons b l ih =>
    cases b with
    | true =>
      show gi + rumbo gi gp l
         = ((1 : Int) + nImpares l) * gi + ((0 : Int) + nPares l) * gp
      rw [ih, Int.zero_add, Int.add_mul, Int.one_mul, Int.add_assoc]
    | false =>
      show gp + rumbo gi gp l
         = ((0 : Int) + nImpares l) * gi + ((1 : Int) + nPares l) * gp
      rw [ih, Int.zero_add, Int.add_mul, Int.one_mul, Int.add_left_comm]

-- ============================================================
-- EL ENUNCIADO A9, sobre el mapa clasico: para TODO n, TODO k
-- y TODO par de giros:  rumbo = A*giro_impar + B*giro_par
-- ============================================================
theorem A9_rumbo_es_AB (gi gp : Int) (n k : Nat) :
    rumboDesde gi gp n k = A n k * gi + B n k * gp :=
  rumbo_cuenta gi gp (paridades n k)

-- COROLARIO ("solo depende de (A,B)"): dos ramas cualesquiera con el
-- mismo A y el mismo B tienen el mismo rumbo, aunque el orden de sus
-- pasos sea distinto.
theorem mismo_AB_mismo_rumbo (gi gp : Int) (n1 k1 n2 k2 : Nat)
    (hA : A n1 k1 = A n2 k2) (hB : B n1 k1 = B n2 k2) :
    rumboDesde gi gp n1 k1 = rumboDesde gi gp n2 k2 := by
  rw [A9_rumbo_es_AB, A9_rumbo_es_AB, hA, hB]

-- CONTROL DE COHERENCIA: A + B = k (cada paso es impar o par)
theorem cuenta_total : ∀ l : List Bool,
    nImpares l + nPares l = (l.length : Int) := by
  intro l
  induction l with
  | nil => rfl
  | cons b l ih =>
    cases b <;> simp [nImpares, nPares, List.length_cons] <;> omega

theorem longitud_paridades : ∀ k n, (paridades n k).length = k := by
  intro k
  induction k with
  | zero => intro n; rfl
  | succ k ih => intro n; show (paridades n (k+1)).length = k + 1
                 unfold paridades; rw [List.length_cons, ih]

theorem A_mas_B (n k : Nat) : A n k + B n k = (k : Int) := by
  have h := cuenta_total (paridades n k)
  rw [longitud_paridades k n] at h
  exact h

-- ============================================================
-- CASOS CONCRETOS COMPROBADOS POR EL NUCLEO (by decide, no #eval)
-- ============================================================

-- La trayectoria del 7 (mapa clasico, 16 pasos hasta el 1):
-- 7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2 -> 1.  A=5 impares, B=11 pares.
theorem caso_7 : A 7 16 = 5 ∧ B 7 16 = 11 := by decide

-- y su rumbo con giros concretos (3 y 7): 5*3 + 11*7 = 92
theorem caso_7_rumbo : rumboDesde 3 7 7 16 = 92 := by decide

-- BORDE k = 0: sin pasos, A = B = 0 y rumbo = 0
theorem caso_k0 : A 7 0 = 0 ∧ B 7 0 = 0 ∧ rumboDesde 3 7 7 0 = 0 := by decide

-- BORDE n = 1 (el ciclo 1,4,2): A = 1, B = 2, rumbo = 1*3 + 2*7 = 17
theorem caso_1 : A 1 3 = 1 ∧ B 1 3 = 2 ∧ rumboDesde 3 7 1 3 = 17 := by decide

-- BORDE n = 2 (par): 2 -> 1 -> 4 -> 2, A = 1, B = 2
theorem caso_2 : A 2 3 = 1 ∧ B 2 3 = 2 := by decide

-- LA PARTE CON CONTENIDO del "solo depende de (A,B)": dos ramas con
-- vectores de paridad DISTINTOS (orden distinto de giros) pero mismo
-- (A,B) tienen el mismo rumbo.
--   6 -> 3 -> 10 -> 5   da [par, impar, par, impar]
--   9 -> 28 -> 14 -> 7  da [impar, par, par, impar]
theorem caso_orden_distinto :
    paridades 6 4 ≠ paridades 9 4
    ∧ A 6 4 = A 9 4 ∧ B 6 4 = B 9 4
    ∧ rumboDesde 3 7 6 4 = rumboDesde 3 7 9 4 := by decide

-- el mismo par (A,B)=(2,2) con giros "genericos de sonda" (numeros
-- grandes y coprimos, para que ninguna coincidencia numerica lo salve)
theorem caso_orden_distinto_2 :
    rumboDesde 1000003 999983 6 4 = rumboDesde 1000003 999983 9 4 := by decide

-- ============================================================
#print axioms rumbo_cuenta
#print axioms A9_rumbo_es_AB
#print axioms mismo_AB_mismo_rumbo
#print axioms A_mas_B
#print axioms caso_7
#print axioms caso_7_rumbo
#print axioms caso_k0
#print axioms caso_1
#print axioms caso_2
#print axioms caso_orden_distinto
#print axioms caso_orden_distinto_2
