/-
  A8 (agente 1, LEAN, del trio de verificacion).

  ENUNCIADO: los patrones de paridad alcanzables en k pasos del mapa
  CLASICO (n par -> n/2 ; n impar -> 3n+1) son F(k+2), los Fibonacci.
  Ambito declarado: k = 1..10.

  Formalizacion:
   - el patron de paridad de n en k pasos es la lista de k bits
       bit i = (T^i(n) es impar),  i = 0..k-1   (T = mapa clasico)
   - "alcanzable" = existe n >= 1 que lo produce.
   - Mitad estructural, demostrada PARA TODO n y TODO paso:
       tras un paso impar viene un paso par  =>  ningun patron
       alcanzable tiene dos true seguidos (patron_sin_dobles).
   - Mitad de completitud + conteo, decidida por el NUCLEO (decide)
     para k = 1..10: toda cadena sin dos true seguidos se alcanza con
     algun n en [1, 2^k], y el numero de esas cadenas es fib(k+2)
     con fib 0 = 0, fib 1 = 1 (la F de la ficha: F(6)=8, F(12)=144).

  Sin Mathlib. Solo nucleo.
-/
set_option maxRecDepth 40000

-- EL MAPA, escrito aqui mismo: es el CLASICO, no el atajo.
def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

def iter : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => paso (iter k n)

-- Casos conocidos comprobados por el nucleo (decide, no #eval):
-- 27 -> 82 -> 41 -> 124 -> 62 -> 31 -> 94 -> 47 -> 142 -> 71 -> 214
theorem caso_27 : iter 10 27 = 214 := by decide
-- 5 -> 16 -> 8 -> 4 -> 2 -> 1  (cinco pasos clasicos)
theorem caso_5 : iter 5 5 = 1 := by decide

-- el patron de paridad de los primeros k pasos
def patron : Nat → Nat → List Bool
  | 0, _ => []
  | k+1, n => (n % 2 == 1) :: patron k (paso n)

-- 3 -> 10 -> 5 -> 16 -> 8 : impar, par, impar, par, par
theorem caso_3 : patron 5 3 = [true, false, true, false, false] := by decide

-- cadenas sin dos true adyacentes
def sinDobles : List Bool → Bool
  | [] => true
  | [_] => true
  | a :: b :: t => !(a && b) && sinDobles (b :: t)

-- ============ MITAD ESTRUCTURAL: para TODO n, TODO k ============

theorem paso_de_impar_es_par (n : Nat) (h : n % 2 = 1) : paso n % 2 = 0 := by
  unfold paso
  rw [if_neg (show ¬ n % 2 = 0 by omega)]
  omega

-- dos pasos impares nunca van seguidos (para todo n, todo i)
theorem sin_dos_impares_seguidos (n i : Nat) (h : iter i n % 2 = 1) :
    iter (i + 1) n % 2 = 0 :=
  paso_de_impar_es_par (iter i n) h

-- luego NINGUN patron alcanzable tiene dos true seguidos:
theorem patron_sin_dobles : ∀ (k n : Nat), sinDobles (patron k n) = true := by
  intro k
  induction k with
  | zero => intro n; rfl
  | succ j ih =>
    cases j with
    | zero => intro n; rfl
    | succ i =>
      intro n
      have h2 := ih (paso n)
      simp only [patron, sinDobles] at h2 ⊢
      rw [h2, Bool.and_true]
      by_cases h : n % 2 = 1
      · rw [h, paso_de_impar_es_par n h]
        decide
      · have h0 : n % 2 = 0 := by omega
        rw [h0]
        rfl

-- ============ COMPLETITUD Y CONTEO, k = 1..10, por el nucleo ============

def cadenas : Nat → List (List Bool)
  | 0 => [[]]
  | k+1 => ((cadenas k).map (fun l => false :: l)) ++ ((cadenas k).map (fun l => true :: l))

def buenos (k : Nat) : List (List Bool) := (cadenas k).filter sinDobles

def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n+2 => fib n + fib (n+1)

-- los patrones alcanzados por n = 1 .. 2^k  (testigos con n >= 1)
def logrados (k : Nat) : List (List Bool) :=
  (List.range (2 ^ k)).map (fun i => patron k (i + 1))

-- el conteo de cadenas sin dobles es fib(k+2), k = 1..10
theorem conteo_1_a_10 :
    (((List.range 10).map (fun j => j + 1)).all
      (fun k => (buenos k).length == fib (k + 2))) = true := by decide

-- los cuatro valores que cita la ficha
theorem conteo_ficha :
    (buenos 4).length = 8 ∧ (buenos 6).length = 21 ∧
    (buenos 8).length = 55 ∧ (buenos 10).length = 144 := by decide

-- completitud: toda cadena sin dobles de longitud k la alcanza
-- algun n en [1, 2^k]   (k = 1..8 en bloque; 9 y 10 aparte)
theorem completitud_1_a_8 :
    (((List.range 8).map (fun j => j + 1)).all
      (fun k => (buenos k).all (fun l => (logrados k).contains l))) = true := by decide

theorem completitud_9 :
    ((buenos 9).all (fun l => (logrados 9).contains l)) = true := by decide

theorem completitud_10 :
    ((buenos 10).all (fun l => (logrados 10).contains l)) = true := by decide

-- bordes: k = 0 (patron vacio, 1 = fib 2) y k = 1 (2 patrones = fib 3)
theorem borde_k0 : (buenos 0).length = 1 ∧ fib 2 = 1 ∧ patron 0 1 = [] := by decide
theorem borde_k1 : (buenos 1).length = 2 ∧ fib 3 = 2 := by decide

#print axioms caso_27
#print axioms caso_3
#print axioms paso_de_impar_es_par
#print axioms sin_dos_impares_seguidos
#print axioms patron_sin_dobles
#print axioms conteo_1_a_10
#print axioms conteo_ficha
#print axioms completitud_1_a_8
#print axioms completitud_9
#print axioms completitud_10
#print axioms borde_k0
#print axioms borde_k1
