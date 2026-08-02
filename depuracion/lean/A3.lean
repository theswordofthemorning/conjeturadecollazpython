/-
  ITEM A3 — el piso de la altitud, version SIN el +1 y SIN hipotesis de paridad.

  ENUNCIADO LITERAL:  log2( altitud_atajo(n)/n ) >= racha(n) * log2(3/2)
  Forma entera equivalente (la que se formaliza, porque log2 real no vive en el
  nucleo de Lean):   alt * 2^r >= n * 3^r,   con r = racha(n).

  MAPA: el del ATAJO — par -> n/2, impar -> (3n+1)/2. Lo defino yo mismo abajo
  y lo compruebo contra una trayectoria conocida (27 -> 41 -> 62 -> 31) para no
  demostrar un teorema impecable sobre otro objeto.

  QUE ES racha(n): el numero de pasos IMPARES consecutivos al arranque de la
  trayectoria. Para no tener que demostrar que es finita (lo es, pero no hace
  falta), el teorema se enuncia para TODO r tal que los primeros r pasos son
  impares — en particular vale para r = racha(n), sea cual sea.

  CADENA COMPLETA:
    (1) cota:      si los primeros r pasos son impares, 3^r * n <= 2^r * iter r n
    (2) no_baja:   durante la racha la trayectoria nunca baja de n; luego si
                   n >= 2 nunca toca el 1, y por tanto CUALQUIER definicion
                   razonable de altitud (maximo hasta llegar al 1, o maximo de
                   la orbita) cubre el punto iter r n
    (3) corolario: para cualquier alt >= iter r n,  3^r * n <= 2^r * alt
  Es exactamente el enunciado en enteros: alt * 2^r >= n * 3^r.

  BORDES (abajo, todos por decide, no por #eval):
    n par (racha 0): trivial, 1*n <= 1*alt.
    n = 2, potencias de 2: caso r = 0 del corolario.
    n = 1: racha(1) = 1 y T(1) = 2. Si la altitud incluye ese paso, se cumple
           (4 >= 3). Si la trayectoria de 1 se define como parada en el 1
           (alt = 1), FALLA: 3 <= 2 es falso. Por eso el ambito n >= 2 de la
           base no es decorativo.
-/

set_option maxRecDepth 40000

-- El mapa del ATAJO
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- iter r n = T^r(n)
def iter : Nat → Nat → Nat
  | 0,     n => n
  | k + 1, n => T (iter k n)

-- ============================================================
-- LA TRAMPA: comprobar que T es el objeto correcto.
-- Atajo del 27: 27 -> 41 -> 62 -> 31 (el clasico daria 27 -> 82).
-- Y un paso par: T 6 = 3.
-- ============================================================
theorem objeto_correcto :
    iter 1 27 = 41 ∧ iter 2 27 = 62 ∧ iter 3 27 = 31 ∧ T 6 = 3 ∧ T 1 = 2 := by
  decide

-- En un paso impar el atajo cumple 2 * T x = 3x + 1 (exacto, sin truncar,
-- porque 3x+1 es par cuando x es impar).
theorem paso_impar (x : Nat) (h : x % 2 = 1) : 2 * T x = 3 * x + 1 := by
  unfold T
  split
  · omega
  · omega

-- Un paso impar SUBE estrictamente (por eso la racha no puede tocar el 1).
theorem paso_impar_sube (x : Nat) (h : x % 2 = 1) : x < T x := by
  have := paso_impar x h
  omega

-- ============================================================
-- (1) LA COTA: si los primeros r pasos son impares,
--     3^r * n <= 2^r * iter r n.
-- ============================================================
theorem cota (n : Nat) :
    ∀ r : Nat, (∀ j, j < r → iter j n % 2 = 1) →
      3 ^ r * n ≤ 2 ^ r * iter r n := by
  intro r
  induction r with
  | zero =>
      intro _
      show 3 ^ 0 * n ≤ 2 ^ 0 * n
      omega
  | succ k ih =>
      intro h
      have hk : ∀ j, j < k → iter j n % 2 = 1 :=
        fun j hj => h j (Nat.lt_succ_of_lt hj)
      have hodd : iter k n % 2 = 1 := h k (Nat.lt_succ_self k)
      have hstep : 2 * T (iter k n) = 3 * iter k n + 1 := paso_impar _ hodd
      have ihk : 3 ^ k * n ≤ 2 ^ k * iter k n := ih hk
      calc 3 ^ (k + 1) * n
          = 3 ^ k * 3 * n := by rw [Nat.pow_succ]
        _ = 3 * (3 ^ k * n) := by
              rw [Nat.mul_comm (3 ^ k) 3, Nat.mul_assoc]
        _ ≤ 3 * (2 ^ k * iter k n) := Nat.mul_le_mul_left 3 ihk
        _ = 2 ^ k * (3 * iter k n) := Nat.mul_left_comm 3 (2 ^ k) (iter k n)
        _ ≤ 2 ^ k * (3 * iter k n + 1) :=
              Nat.mul_le_mul_left (2 ^ k) (Nat.le_succ _)
        _ = 2 ^ k * (2 * T (iter k n)) := by rw [hstep]
        _ = 2 ^ k * 2 * T (iter k n) := by rw [Nat.mul_assoc]
        _ = 2 ^ (k + 1) * T (iter k n) := by rw [Nat.pow_succ]
        _ = 2 ^ (k + 1) * iter (k + 1) n := rfl

-- ============================================================
-- (2) Durante la racha la trayectoria NUNCA baja de n.
--     Consecuencia: si n >= 2, nunca toca el 1 antes del paso r,
--     asi que la altitud (se trunque donde se trunque) cubre iter r n.
-- ============================================================
theorem no_baja (n r : Nat) (h : ∀ j, j < r → iter j n % 2 = 1) :
    ∀ j, j ≤ r → n ≤ iter j n := by
  intro j
  induction j with
  | zero =>
      intro _
      exact Nat.le_refl n
  | succ i ih =>
      intro hle
      have hi : i < r := Nat.lt_of_lt_of_le (Nat.lt_succ_self i) hle
      have hodd : iter i n % 2 = 1 := h i hi
      have hsube : iter i n < T (iter i n) := paso_impar_sube _ hodd
      have hin : n ≤ iter i n := ih (Nat.le_of_lt hi)
      show n ≤ T (iter i n)
      omega

-- Y explicitamente: con n >= 2, ningun punto de la racha es 1.
theorem no_toca_uno (n r : Nat) (hn : 2 ≤ n)
    (h : ∀ j, j < r → iter j n % 2 = 1) :
    ∀ j, j ≤ r → 1 < iter j n := by
  intro j hj
  have := no_baja n r h j hj
  omega

-- ============================================================
-- (3) EL COROLARIO = EL ENUNCIADO EN ENTEROS:
--     para cualquier alt que cubra el punto iter r n (y la altitud del
--     repo lo cubre, por no_toca_uno, siempre que n >= 2):
--     alt * 2^r >= n * 3^r.
-- ============================================================
theorem piso_altitud (n r alt : Nat)
    (h : ∀ j, j < r → iter j n % 2 = 1)
    (halt : iter r n ≤ alt) :
    3 ^ r * n ≤ 2 ^ r * alt :=
  Nat.le_trans (cota n r h) (Nat.mul_le_mul_left (2 ^ r) halt)

-- ============================================================
-- BORDES Y CASOS CONOCIDOS, todos como teoremas por decide.
-- ============================================================

-- Caso conocido 1: n = 27, racha = 2 (27 y 41 impares, 62 par).
-- 3^2 * 27 = 243 <= 2^2 * 62 = 248. Ajustado: margen 5.
theorem caso_27 :
    (∀ j, j < 2 → iter j 27 % 2 = 1) ∧ iter 2 27 % 2 = 0 ∧
    3 ^ 2 * 27 ≤ 2 ^ 2 * iter 2 27 := by decide

-- Caso conocido 2: n = 31 = 2^5 - 1, racha = 5, iter 5 31 = 242.
-- 3^5 * 31 = 7533 <= 2^5 * 242 = 7744.
theorem caso_31 :
    (∀ j, j < 5 → iter j 31 % 2 = 1) ∧ iter 5 31 = 242 ∧ iter 5 31 % 2 = 0 ∧
    3 ^ 5 * 31 ≤ 2 ^ 5 * iter 5 31 := by decide

-- Borde n par (racha 0): el piso solo pide alt >= n. Trivial y cierto.
theorem borde_par (n : Nat) : 3 ^ 0 * n ≤ 2 ^ 0 * n := by omega

-- Borde n = 2 y potencia de 2 (n = 16): racha 0, instancias del anterior.
theorem borde_2 : 3 ^ 0 * 2 ≤ 2 ^ 0 * 2 ∧ 3 ^ 0 * 16 ≤ 2 ^ 0 * 16 := by decide

-- Borde n = 1, mitad buena: racha(1) = 1 (1 impar, T 1 = 2 par).
-- Si la altitud incluye el paso a 2: 3^1 * 1 = 3 <= 2^1 * 2 = 4. Se cumple.
theorem borde_uno_con_orbita :
    (1 % 2 = 1) ∧ iter 1 1 = 2 ∧ 3 ^ 1 * 1 ≤ 2 ^ 1 * iter 1 1 := by decide

-- Borde n = 1, mitad mala: si alt(1) = 1 (trayectoria parada en el 1),
-- el piso pide 3 <= 2 y es FALSO. El ambito n >= 2 de la base es necesario
-- bajo ese convenio de altitud.
theorem borde_uno_sin_orbita : ¬ (3 ^ 1 * 1 ≤ 2 ^ 1 * 1) := by decide

-- Control de que la hipotesis de racha no es vacua en el caso general:
-- un n donde el primer paso NO es impar (n = 4) solo admite r = 0.
theorem racha_de_par_es_cero : iter 0 4 % 2 = 0 := by decide

#print axioms cota
#print axioms no_baja
#print axioms no_toca_uno
#print axioms piso_altitud
#print axioms caso_27
#print axioms caso_31
#print axioms borde_uno_con_orbita
#print axioms borde_uno_sin_orbita
#print axioms objeto_correcto
