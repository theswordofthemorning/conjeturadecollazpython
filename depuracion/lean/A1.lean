/-
  ITEM A1 — agente 1 (LEAN) del trio.

  ENUNCIADO: 2^B * seq[j] = 3^A * seq[i] + C  para cualquier par i < j de una
  trayectoria del mapa CLASICO (n/2 si par, 3n+1 si impar), donde
    A = numero de pasos impares (3n+1) del tramo i..j
    B = numero de pasos pares  (n/2)  del tramo i..j
    C arranca en 0 en la posicion i, y se actualiza
        paso impar:  C -> 3C + 2^B   (B = pares acumulados hasta ese momento)
        paso par:    C no cambia.

  Formalizacion: seq[i] es un natural arbitrario n0 (cualquier posicion de
  cualquier trayectoria es a su vez el arranque de una trayectoria), y
  j = i + k con k arbitrario. Se demuestra para TODO n0 y TODO k.

  MAPA USADO: el CLASICO. `paso n = if n % 2 = 0 then n / 2 else 3*n+1`.
  Sin Mathlib: solo nucleo.
-/

set_option maxRecDepth 40000

/-- El mapa clasico de Collatz. -/
def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- k iteraciones del mapa clasico. -/
def iter : Nat → Nat → Nat
  | 0,     n => n
  | k + 1, n => iter k (paso n)

/-- Estado del tramo: valor actual n, contadores A (impares), B (pares), y C. -/
structure Estado where
  n : Nat
  a : Nat
  b : Nat
  c : Nat
deriving DecidableEq, Repr

/-- Un paso del tramo, actualizando los contadores EXACTAMENTE como dice el
    enunciado: par -> B+1 y C quieto; impar -> A+1 y C -> 3C + 2^B. -/
def pasoE (s : Estado) : Estado :=
  if s.n % 2 = 0 then ⟨s.n / 2, s.a, s.b + 1, s.c⟩
  else ⟨3 * s.n + 1, s.a + 1, s.b, 3 * s.c + 2 ^ s.b⟩

/-- k pasos del tramo. -/
def iterE : Nat → Estado → Estado
  | 0,     s => s
  | k + 1, s => iterE k (pasoE s)

/-- El estado inicial en la posicion i: contadores a cero, C = 0. -/
def estado0 (n0 : Nat) : Estado := ⟨n0, 0, 0, 0⟩

/-- LA TRAMPA, cerrada: la componente n del estado sigue el mapa clasico
    de verdad, paso a paso. -/
theorem pasoE_n (s : Estado) : (pasoE s).n = paso s.n := by
  unfold pasoE paso
  by_cases hp : s.n % 2 = 0
  · rw [if_pos hp, if_pos hp]
  · rw [if_neg hp, if_neg hp]

theorem iterE_n (k : Nat) : ∀ s : Estado, (iterE k s).n = iter k s.n := by
  induction k with
  | zero => intro s; rfl
  | succ k ih =>
      intro s
      show (iterE k (pasoE s)).n = iter k (paso s.n)
      rw [ih (pasoE s), pasoE_n]

/-- El invariante: la identidad del enunciado. -/
def inv (n0 : Nat) (s : Estado) : Prop :=
  2 ^ s.b * s.n = 3 ^ s.a * n0 + s.c

/-- EL PASO INDUCTIVO: un paso del mapa conserva la identidad. -/
theorem paso_conserva (n0 : Nat) (s : Estado) (h : inv n0 s) :
    inv n0 (pasoE s) := by
  unfold inv at h
  unfold inv pasoE
  by_cases hp : s.n % 2 = 0
  · rw [if_pos hp]
    show 2 ^ (s.b + 1) * (s.n / 2) = 3 ^ s.a * n0 + s.c
    have hn : 2 * (s.n / 2) = s.n := by omega
    calc 2 ^ (s.b + 1) * (s.n / 2)
        = 2 ^ s.b * 2 * (s.n / 2) := by rw [Nat.pow_succ]
      _ = 2 ^ s.b * (2 * (s.n / 2)) := by rw [Nat.mul_assoc]
      _ = 2 ^ s.b * s.n := by rw [hn]
      _ = 3 ^ s.a * n0 + s.c := h
  · rw [if_neg hp]
    show 2 ^ s.b * (3 * s.n + 1) = 3 ^ (s.a + 1) * n0 + (3 * s.c + 2 ^ s.b)
    calc 2 ^ s.b * (3 * s.n + 1)
        = 2 ^ s.b * (3 * s.n) + 2 ^ s.b := by rw [Nat.mul_add, Nat.mul_one]
      _ = 3 * (2 ^ s.b * s.n) + 2 ^ s.b := by rw [Nat.mul_left_comm]
      _ = 3 * (3 ^ s.a * n0 + s.c) + 2 ^ s.b := by rw [h]
      _ = 3 * (3 ^ s.a * n0) + 3 * s.c + 2 ^ s.b := by rw [Nat.mul_add]
      _ = 3 * (3 ^ s.a * n0) + (3 * s.c + 2 ^ s.b) := by rw [Nat.add_assoc]
      _ = 3 ^ (s.a + 1) * n0 + (3 * s.c + 2 ^ s.b) := by
            rw [Nat.pow_succ, Nat.mul_comm (3 ^ s.a) 3, Nat.mul_assoc]

/-- La identidad se conserva bajo k pasos, para todo k. -/
theorem invariante (n0 : Nat) (k : Nat) :
    ∀ s : Estado, inv n0 s → inv n0 (iterE k s) := by
  induction k with
  | zero => intro s h; exact h
  | succ k ih =>
      intro s h
      show inv n0 (iterE k (pasoE s))
      exact ih (pasoE s) (paso_conserva n0 s h)

/-- TEOREMA PRINCIPAL (el enunciado A1, cuantificador todo_n y todo k):
    para todo arranque n0 y todo numero de pasos k,
      2^B * seq[i+k] = 3^A * seq[i] + C
    con A, B, C llevados por la recurrencia literal del enunciado. -/
theorem identidad (n0 k : Nat) :
    2 ^ (iterE k (estado0 n0)).b * iter k n0
      = 3 ^ (iterE k (estado0 n0)).a * n0 + (iterE k (estado0 n0)).c := by
  have h0 : inv n0 (estado0 n0) := by
    unfold inv estado0
    show 2 ^ 0 * n0 = 3 ^ 0 * n0 + 0
    omega
  have h := invariante n0 k (estado0 n0) h0
  unfold inv at h
  rw [iterE_n k (estado0 n0)] at h
  exact h

/- ============ CASOS CONCRETOS, comprobados por el NUCLEO con decide ============ -/

/-- El caso conocido del repo: el 221 llega a 1 en 114 pasos clasicos,
    con A = 41 y B = 73. -/
theorem caso221 :
    (iterE 114 (estado0 221)).n = 1 ∧
    (iterE 114 (estado0 221)).a = 41 ∧
    (iterE 114 (estado0 221)).b = 73 := by decide

/-- Y la identidad instanciada en el 221 entero: 3^41 * 221 + C = 2^73. -/
theorem caso221_identidad :
    3 ^ 41 * 221 + (iterE 114 (estado0 221)).c = 2 ^ 73 := by decide

/-- Trayectoria corta completa, estado entero (incluida C):
    6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1, con A=2, B=6, C=10,
    y en efecto 2^6 * 1 = 64 = 3^2 * 6 + 10. -/
theorem caso6 : iterE 8 (estado0 6) = ⟨1, 2, 6, 10⟩ := by decide

/-- El ciclo trivial: 1 -> 4 -> 2 -> 1 da A=1, B=2, C=1, o sea 4 = 3 + 1. -/
theorem caso1 : iterE 3 (estado0 1) = ⟨1, 1, 2, 1⟩ := by decide

/- ============ BORDES ============ -/

/-- Borde k = 0 (el par i = j): identidad trivial, C = 0. -/
theorem borde_k0 : iterE 0 (estado0 7) = ⟨7, 0, 0, 0⟩ := by decide

/-- Borde n0 = 0: el 0 es par y se queda en 0; C nunca crece. -/
theorem borde_n0 : iterE 5 (estado0 0) = ⟨0, 0, 5, 0⟩ := by decide

/-- Borde n0 = 2 (par), un paso. -/
theorem borde_n2 : iterE 1 (estado0 2) = ⟨1, 0, 1, 0⟩ := by decide

/-- Arranque en mitad de otra trayectoria (10 = seq[1] del 3):
    10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1, A=1, B=5, C=2; 2^5 = 3*10 + 2. -/
theorem caso_medio : iterE 6 (estado0 10) = ⟨1, 1, 5, 2⟩ := by decide

/- ============ CONTROL DE AXIOMAS ============ -/

#print axioms identidad
#print axioms paso_conserva
#print axioms invariante
#print axioms iterE_n
#print axioms caso221
#print axioms caso221_identidad
#print axioms caso6
#print axioms caso1
#print axioms borde_k0
#print axioms borde_n0
#print axioms borde_n2
#print axioms caso_medio
