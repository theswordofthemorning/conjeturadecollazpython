/-
ITEM A11 — "si n tarda S pasos, el numero de la posicion k tarda S-k;
             luego el de la posicion S/2 tarda S/2"
Agente 1 (LEAN) del trio. Sin Mathlib, solo nucleo.

FORMALIZACION:
  - "tardar exactamente S pasos" = itera S n = 1  Y  ningun j < S da 1
    (tiempo de PRIMERA llegada; "tarda S" presupone que llega, asi que el
    enunciado es condicional a la terminacion y eso queda como hipotesis).
  - El teorema es de CONTABILIDAD PURA: se demuestra para una f : Nat -> Nat
    ARBITRARIA (no usa nada de Collatz). Despues se instancia en el mapa
    clasico (n/2 si par, 3n+1 si impar) y se comprueba el caso conocido
    del 221 (114 pasos clasicos) con `decide` (nucleo, no #eval).
  - La mitad "S/2 tarda S/2" exige S PAR (si S es impar, la posicion S/2
    con division entera tarda S - S/2 = S/2 + 1, no S/2). La base ya
    declaraba ese ambito ("todo n con cantidad par de pasos").
-/

set_option maxRecDepth 40000

-- EL MAPA CLASICO, escrito aqui mismo (la trampa de Lean: definir uno el objeto)
def paso (n : Nat) : Nat := if n % 2 == 0 then n / 2 else 3 * n + 1

-- iteracion generica de cualquier funcion
def itera (f : Nat → Nat) : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => itera f k (f n)

-- "n tarda exactamente S pasos en llegar a 1 bajo f"
def tardaExacto (f : Nat → Nat) (S n : Nat) : Prop :=
  itera f S n = 1 ∧ ∀ j, j < S → itera f j n ≠ 1

instance (f : Nat → Nat) (S n : Nat) : Decidable (tardaExacto f S n) := by
  unfold tardaExacto
  exact inferInstance

-- lema de composicion: iterar a+b es iterar a y despues b
theorem itera_add (f : Nat → Nat) (a b n : Nat) :
    itera f (a + b) n = itera f b (itera f a n) := by
  induction a generalizing n with
  | zero =>
    rw [Nat.zero_add]
    rfl
  | succ a ih =>
    rw [Nat.succ_add]
    show itera f (a + b) (f n) = itera f b (itera f a (f n))
    exact ih (f n)

-- TEOREMA PRINCIPAL (la primera mitad del enunciado):
-- si n tarda exactamente S pasos y k <= S, el numero de la posicion k
-- tarda exactamente S - k pasos. Para f ARBITRARIA: es contabilidad.
theorem cola_tarda (f : Nat → Nat) (S k n : Nat)
    (hk : k ≤ S) (h : tardaExacto f S n) :
    tardaExacto f (S - k) (itera f k n) := by
  constructor
  · have hsum : k + (S - k) = S := by omega
    rw [← itera_add, hsum]
    exact h.1
  · intro j hj hcon
    rw [← itera_add] at hcon
    exact h.2 (k + j) (by omega) hcon

-- COROLARIO (la segunda mitad): con S PAR, el de la posicion S/2 tarda S/2
theorem mitad_tarda (f : Nat → Nat) (S n : Nat)
    (hpar : S % 2 = 0) (h : tardaExacto f S n) :
    tardaExacto f (S / 2) (itera f (S / 2) n) := by
  have h1 : S - S / 2 = S / 2 := by omega
  have h2 : S / 2 ≤ S := by omega
  have hc := cola_tarda f S (S / 2) n h2 h
  rw [h1] at hc
  exact hc

-- LA HIPOTESIS DE PARIDAD NO SOBRA: contraejemplo con S impar.
-- n = 5 tarda 5 pasos clasicos (5,16,8,4,2,1). S/2 = 2 (division entera):
-- la posicion 2 es el 8, que tarda 3 pasos, NO 2.
theorem contraejemplo_S_impar :
    tardaExacto paso 5 5 ∧ ¬ tardaExacto paso (5 / 2) (itera paso (5 / 2) 5) := by
  decide

-- ===== CASOS CONCRETOS COMPROBADOS POR EL NUCLEO (decide, no #eval) =====

-- caso chico: 6 tarda 8 pasos clasicos (6,3,10,5,16,8,4,2,1)
theorem caso_6 : tardaExacto paso 8 6 := by decide

-- ... y la posicion 4 (el 16) tarda 8 - 4 = 4
theorem caso_6_pos4 : tardaExacto paso 4 (itera paso 4 6) := by decide

-- EL CASO CONOCIDO DEL REPO: el 221 tarda 114 pasos CLASICOS (A=41, B=73).
-- Esto ancla mi `paso` al objeto correcto: si mi mapa fuera otro, no daria 114.
theorem caso_221 : tardaExacto paso 114 221 := by decide

-- ... y el enunciado en el: 114 es par, la posicion 57 tarda 57.
-- Comprobado DIRECTO por el nucleo (no solo via el teorema):
theorem caso_221_mitad : tardaExacto paso 57 (itera paso 57 221) := by decide

-- ... y tambien via el teorema general, para atar las dos cosas:
theorem caso_221_mitad_por_teorema :
    tardaExacto paso 57 (itera paso 57 221) := by
  have h : (114 : Nat) - 114 / 2 = 57 := by decide
  have hc := mitad_tarda paso 114 221 (by decide) caso_221
  exact hc

-- ===== BORDES =====

-- n = 1, S = 0: tarda 0 pasos; el enunciado con k = 0 devuelve lo mismo
theorem borde_n1 : tardaExacto paso 0 1 := by decide

-- k = S: el numero de la ultima posicion es 1 y tarda 0
theorem borde_k_igual_S : tardaExacto paso 0 (itera paso 114 221) := by
  have hc := cola_tarda paso 114 114 221 (Nat.le_refl 114) caso_221
  simpa using hc

-- k = 0: devuelve el enunciado original
theorem borde_k0 (f : Nat → Nat) (S n : Nat) (h : tardaExacto f S n) :
    tardaExacto f S (itera f 0 n) := by
  have hc := cola_tarda f S 0 n (Nat.zero_le S) h
  simpa using hc

-- n = 2 (par): tarda 1 paso
theorem borde_n2 : tardaExacto paso 1 2 := by decide

-- ===== CONTROL DE AXIOMAS =====
#print axioms cola_tarda
#print axioms mitad_tarda
#print axioms caso_221
#print axioms caso_221_mitad
#print axioms contraejemplo_S_impar
#print axioms borde_n1
#print axioms borde_k_igual_S
