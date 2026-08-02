/-
A30.lean -- Agente 1 (LEAN) del trio de verificacion. Sin Mathlib, solo nucleo.

ENUNCIADO (ficha A30): el ritmo de brotes del arbol inverso es periodico de
periodo 2 segun v mod 3; los hijos ciclan con periodo 3 mod 9; y el patron
completo se repite cada 18 duplicaciones (18 = orden de 2 mod 27).

MAPA: arbol inverso del mapa CLASICO (n par -> n/2, n impar -> 3n+1).
Un rayo es v, 2v, 4v, 8v, ... con v IMPAR (todo arranque de rayo es impar).
El nodo m = 2^k * v "brota" en la duplicacion k si ademas del padre por
duplicacion tiene un padre IMPAR c por 3n+1, o sea 3c+1 = m con c impar.
Eso equivale a m % 6 = 4 (brota_correcto / brota_completo, abajo).
El hijo (ese padre impar) es c = (m-1)/3.
-/
set_option maxRecDepth 40000

def brota (v k : Nat) : Prop := (2 ^ k * v) % 6 = 4

instance (v k : Nat) : Decidable (brota v k) :=
  inferInstanceAs (Decidable ((2 ^ k * v) % 6 = 4))

def hijo (m : Nat) : Nat := (m - 1) / 3

/- ─── 0. LA TRAMPA: la definicion habla del objeto correcto ───────────────
   brota v k  <->  el nodo 2^k*v tiene un padre impar por 3n+1 (mapa clasico),
   y ese padre es exactamente hijo (2^k*v) = (m-1)/3. -/

theorem brota_correcto (v k : Nat) (hb : brota v k) :
    3 * hijo (2 ^ k * v) + 1 = 2 ^ k * v ∧ hijo (2 ^ k * v) % 2 = 1 := by
  unfold brota at hb
  unfold hijo
  omega

theorem brota_completo (v k c : Nat) (hc : c % 2 = 1) (h : 3 * c + 1 = 2 ^ k * v) :
    brota v k := by
  unfold brota
  omega

/- ─── 1. EL RITMO DE PERIODO 2, segun v mod 3 ──────────────────────────── -/

-- 2^(k+1) mod 6 alterna 2, 4, 2, 4, ... con periodo 2
theorem pow2_mod6 (k : Nat) : 2 ^ (k + 1) % 6 = if k % 2 = 0 then 2 else 4 := by
  induction k with
  | zero => decide
  | succ n ih =>
    rw [Nat.pow_succ, Nat.mul_mod, ih]
    split <;> split <;> omega

-- v = 0 (mod 3): el rayo NUNCA brota (rayo mudo), para todo k
theorem rayo_mudo (v : Nat) (h3 : v % 3 = 0) (k : Nat) : ¬ brota v k := by
  intro hb
  unfold brota at hb
  have hm : (2 ^ k * v) % 3 = 0 := by
    rw [Nat.mul_mod, h3]
    simp
  omega

-- v = 1 (mod 6): brota exactamente en k par con k >= 1 (en k = 0 la semilla es impar)
theorem brota_r1 (v : Nat) (h6 : v % 6 = 1) (k : Nat) :
    brota v k ↔ (k % 2 = 0 ∧ k ≠ 0) := by
  unfold brota
  cases k with
  | zero =>
    rw [Nat.pow_zero, Nat.one_mul]
    omega
  | succ n =>
    rw [Nat.mul_mod, pow2_mod6, h6]
    split <;> omega

-- v = 5 (mod 6): brota exactamente en k impar
theorem brota_r5 (v : Nat) (h6 : v % 6 = 5) (k : Nat) :
    brota v k ↔ k % 2 = 1 := by
  unfold brota
  cases k with
  | zero =>
    rw [Nat.pow_zero, Nat.one_mul]
    omega
  | succ n =>
    rw [Nat.mul_mod, pow2_mod6, h6]
    split <;> omega

-- El enunciado «segun v mod 3», para v impar (todo arranque de rayo es impar):
theorem ritmo_por_mod3 (v : Nat) (hv : v % 2 = 1) (k : Nat) :
    (v % 3 = 0 → ¬ brota v k) ∧
    (v % 3 = 1 → (brota v k ↔ (k % 2 = 0 ∧ k ≠ 0))) ∧
    (v % 3 = 2 → (brota v k ↔ k % 2 = 1)) := by
  refine ⟨fun h3 => rayo_mudo v h3 k, fun h3 => ?_, fun h3 => ?_⟩
  · have h6 : v % 6 = 1 := by omega
    exact brota_r1 v h6 k
  · have h6 : v % 6 = 5 := by omega
    exact brota_r5 v h6 k

-- LA PERIODICIDAD LITERAL de periodo 2, valida desde la primera duplicacion
theorem periodo_2 (v k : Nat) (hv : v % 2 = 1) (hk : k ≠ 0) :
    brota v (k + 2) ↔ brota v k := by
  have h : v % 6 = 1 ∨ v % 6 = 3 ∨ v % 6 = 5 := by omega
  cases h with
  | inl h1 =>
    rw [brota_r1 v h1 (k + 2), brota_r1 v h1 k]
    omega
  | inr h' =>
    cases h' with
    | inl h3 =>
      have hm : v % 3 = 0 := by omega
      exact iff_of_false (rayo_mudo v hm (k + 2)) (rayo_mudo v hm k)
    | inr h5 =>
      rw [brota_r5 v h5 (k + 2), brota_r5 v h5 k]
      omega

-- BORDE k = 0: la periodicidad NO se extiende a la semilla (impar, no brota)
theorem borde_k0 : ¬ brota 1 0 ∧ brota 1 2 := by decide

/- ─── 2. LOS HIJOS CICLAN CON PERIODO 3, mod 9 ─────────────────────────── -/

-- Todo brote cae en m = 1 (mod 3), o sea m % 9 ∈ {1, 4, 7}
theorem brote_mod9 (v k : Nat) (hb : brota v k) :
    (2 ^ k * v) % 9 = 1 ∨ (2 ^ k * v) % 9 = 4 ∨ (2 ^ k * v) % 9 = 7 := by
  unfold brota at hb
  omega

-- La tabla {1:0, 4:1, 7:2}: la clase mod 3 del hijo la fija m mod 9
theorem tabla_hijo (m : Nat) :
    (m % 9 = 1 → hijo m % 3 = 0) ∧
    (m % 9 = 4 → hijo m % 3 = 1) ∧
    (m % 9 = 7 → hijo m % 3 = 2) := by
  unfold hijo
  omega

-- Entre brote y brote hay 2 duplicaciones: el siguiente nodo que brota es 4*m
theorem siguiente_brote (v k : Nat) : 2 ^ (k + 2) * v = 4 * (2 ^ k * v) := by
  have h2 : (2 : Nat) ^ 2 = 4 := by decide
  rw [Nat.pow_add, h2, Nat.mul_comm (2 ^ k) 4, Nat.mul_assoc]

-- El aro de 4 mod 9: 1 -> 4 -> 7 -> 1, y con la tabla, hijos 0 -> 1 -> 2 -> 0
theorem aro_4_mod9 (m : Nat) :
    (m % 9 = 1 → (4 * m) % 9 = 4) ∧
    (m % 9 = 4 → (4 * m) % 9 = 7) ∧
    (m % 9 = 7 → (4 * m) % 9 = 1) := by
  omega

-- El ciclo completo de hijos con periodo 3, en un solo teorema
theorem ciclo_hijos (m : Nat) (h : m % 9 = 1) :
    hijo m % 3 = 0 ∧ hijo (4 * m) % 3 = 1 ∧ hijo (4 * (4 * m)) % 3 = 2 ∧
    (4 * (4 * (4 * m))) % 9 = m % 9 := by
  unfold hijo
  omega

-- Y el periodo es EXACTAMENTE 3: 4^1 y 4^2 no vuelven, 4^3 si (orden de 4 mod 9)
theorem aro_4_minimal : 4 % 9 ≠ 1 ∧ (4 * 4) % 9 ≠ 1 ∧ (4 * (4 * 4)) % 9 = 1 := by decide

/- ─── 3. LA RUEDA MAESTRA: periodo 18 = orden de 2 mod 27 ──────────────── -/

theorem orden_2_mod27 : 2 ^ 18 % 27 = 1 := by decide

theorem orden_2_mod27_minimal : ∀ j, j < 18 → j ≠ 0 → 2 ^ j % 27 ≠ 1 := by decide

-- El estado mod 27 del rayo se repite cada 18 duplicaciones, para TODO k y TODO v
theorem rueda_27 (v k : Nat) : 2 ^ (k + 18) * v % 27 = 2 ^ k * v % 27 := by
  have h : 2 ^ (k + 18) * v = 2 ^ k * v * 2 ^ 18 := by
    rw [Nat.pow_add, Nat.mul_assoc, Nat.mul_comm ((2 : Nat) ^ 18) v, ← Nat.mul_assoc]
  rw [h, Nat.mul_mod, orden_2_mod27]
  omega

-- Para k >= 1 el nodo duplicado es par
theorem nodo_par (v k : Nat) (hk : k ≠ 0) : 2 ^ k * v % 2 = 0 := by
  cases k with
  | zero => exact absurd rfl hk
  | succ n =>
    have h : 2 ^ (n + 1) * v = 2 * (2 ^ n * v) := by
      rw [Nat.pow_succ, Nat.mul_comm (2 ^ n) 2, Nat.mul_assoc]
    rw [h]
    omega

-- El patron de brotes se repite cada 18 duplicaciones (desde k >= 1)
theorem rueda_brote (v k : Nat) (hk : k ≠ 0) : brota v (k + 18) ↔ brota v k := by
  have h27 := rueda_27 v k
  have e1 : 2 ^ k * v % 2 = 0 := nodo_par v k hk
  have e2 : 2 ^ (k + 18) * v % 2 = 0 := nodo_par v (k + 18) (by omega)
  unfold brota
  omega

-- La clase mod 3 del hijo se repite cada 18 duplicaciones
theorem rueda_hijo (v k : Nat) (hb : brota v k) :
    hijo (2 ^ (k + 18) * v) % 3 = hijo (2 ^ k * v) % 3 := by
  have h27 := rueda_27 v k
  unfold brota at hb
  unfold hijo
  omega

-- Y POR QUE 27 y no 9: el hijo conserva incluso su clase mod 9 (que es la que
-- gobierna la tabla de los NIETOS) -- eso exige el nodo mod 27, no mod 9
theorem rueda_hijo_mod9 (v k : Nat) (hb : brota v k) :
    hijo (2 ^ (k + 18) * v) % 9 = hijo (2 ^ k * v) % 9 := by
  have h27 := rueda_27 v k
  unfold brota at hb
  unfold hijo
  omega

-- NOTA DE MINIMALIDAD: lo observable mod 9 (brote + clase mod 3 del hijo) ya
-- se repite cada 6 duplicaciones (2^6 = 1 mod 9); el 18 es el periodo del
-- estado mod 27, no el periodo minimo de aquella parte del patron
theorem nota_repite_6 (v k : Nat) : 2 ^ (k + 6) * v % 9 = 2 ^ k * v % 9 := by
  have h6 : (2 : Nat) ^ 6 % 9 = 1 := by decide
  have h : 2 ^ (k + 6) * v = 2 ^ k * v * 2 ^ 6 := by
    rw [Nat.pow_add, Nat.mul_assoc, Nat.mul_comm ((2 : Nat) ^ 6) v, ← Nat.mul_assoc]
  rw [h, Nat.mul_mod, h6]
  omega

-- BORDE k = 0 de la rueda: el estado mod 27 SI se repite desde k = 0
-- (rueda_27 no pide nada), pero el brote no: la semilla impar no brota
theorem borde_rueda : ¬ brota 1 0 ∧ brota 1 18 := by decide

/- ─── 4. CASOS CONCRETOS COMPROBADOS POR EL NUCLEO (by decide) ─────────── -/

-- El rayo v = 5 (v = 2 mod 3): brota exactamente en k impar; hijos 3, 13, 53
-- con clases 0, 1, 2; y cada hijo es padre impar DE VERDAD: 3c+1 = nodo
theorem caso_rayo_5 :
    ¬ brota 5 0 ∧ brota 5 1 ∧ ¬ brota 5 2 ∧ brota 5 3 ∧ ¬ brota 5 4 ∧ brota 5 5 ∧
    hijo (2 ^ 1 * 5) = 3 ∧ 3 * 3 + 1 = 2 ^ 1 * 5 ∧ 3 % 2 = 1 ∧
    hijo (2 ^ 3 * 5) = 13 ∧ 3 * 13 + 1 = 2 ^ 3 * 5 ∧ 13 % 2 = 1 ∧
    hijo (2 ^ 5 * 5) = 53 ∧ 3 * 53 + 1 = 2 ^ 5 * 5 ∧ 53 % 2 = 1 ∧
    hijo (2 ^ 1 * 5) % 3 = 0 ∧ hijo (2 ^ 3 * 5) % 3 = 1 ∧ hijo (2 ^ 5 * 5) % 3 = 2 ∧
    (2 ^ 1 * 5) % 9 = 1 ∧ (2 ^ 3 * 5) % 9 = 4 ∧ (2 ^ 5 * 5) % 9 = 7 := by decide

-- El rayo v = 1 (v = 1 mod 3): brota en k par >= 2; el 16 brota al 5
-- (16 % 9 = 7 y 5 % 3 = 2, la fila {7:2} de la tabla)
theorem caso_rayo_1 :
    ¬ brota 1 0 ∧ ¬ brota 1 1 ∧ brota 1 2 ∧ ¬ brota 1 3 ∧ brota 1 4 ∧
    hijo (2 ^ 4 * 1) = 5 ∧ 3 * 5 + 1 = 2 ^ 4 * 1 ∧
    (2 ^ 4 * 1) % 9 = 7 ∧ 5 % 3 = 2 := by decide

-- El rayo v = 3 (v = 0 mod 3): mudo (comprobado 0..5; el teorema general
-- rayo_mudo lo da para todo k)
theorem caso_rayo_3 :
    ¬ brota 3 0 ∧ ¬ brota 3 1 ∧ ¬ brota 3 2 ∧ ¬ brota 3 3 ∧ ¬ brota 3 4 ∧
    ¬ brota 3 5 := by decide

-- La rueda 18 en concreto: el estado mod 27 del rayo 5 a las 18 duplicaciones
theorem caso_rueda :
    (2 ^ 19 * 5) % 27 = (2 ^ 1 * 5) % 27 ∧ (2 ^ 18 * 1) % 27 = 1 % 27 := by decide

/- ─── 5. CONTROL DE AXIOMAS ────────────────────────────────────────────── -/

#print axioms brota_correcto
#print axioms brota_completo
#print axioms pow2_mod6
#print axioms rayo_mudo
#print axioms brota_r1
#print axioms brota_r5
#print axioms ritmo_por_mod3
#print axioms periodo_2
#print axioms borde_k0
#print axioms brote_mod9
#print axioms tabla_hijo
#print axioms siguiente_brote
#print axioms aro_4_mod9
#print axioms ciclo_hijos
#print axioms aro_4_minimal
#print axioms orden_2_mod27
#print axioms orden_2_mod27_minimal
#print axioms rueda_27
#print axioms nodo_par
#print axioms rueda_brote
#print axioms rueda_hijo
#print axioms rueda_hijo_mod9
#print axioms nota_repite_6
#print axioms borde_rueda
#print axioms caso_rayo_5
#print axioms caso_rayo_1
#print axioms caso_rayo_3
#print axioms caso_rueda
