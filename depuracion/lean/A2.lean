/-
  ITEM A2 — el piso de la altitud, formalizado en Lean 4 (solo nucleo, sin Mathlib).

  ENUNCIADO (de afirmaciones.db, con el ambito de las notas):
    para todo n IMPAR:  log2( altitud(n)/n ) >= racha(n) * log2(3/2) + 1
  forma entera equivalente (la que se decide):
    altitud(n) * 2^racha(n) >= 2 * n * 3^racha(n)

  MAPAS (los dos aparecen en el enunciado, y NO se mezclan):
    - racha(n)   se define sobre el mapa del ATAJO:   x -> (3x+1)/2 en los impares.
      racha = numero de pasos impares seguidos al arranque.
    - altitud(n) se define sobre el mapa CLASICO:     x -> 3x+1 impar, x -> x/2 par.
      altitud = valor mas alto de la trayectoria clasica, incluyendo n.

  FORMALIZACION:
    - `atajo`, `atajoIter`      : el atajo y sus iterados.
    - `clasico`, `clasicoIter`  : el clasico y sus iterados.
    - `maxTray F n`             : maximo de {clasicoIter j n : j <= F}  (altitud con
                                  presupuesto F de pasos; cualquier altitud real que
                                  incluya al menos 2*racha-1 pasos la mayora).
    - la hipotesis "racha(n) >= r" se escribe literal:
         forall i < r, (atajoIter i n) % 2 = 1
      que es la DEFINICION de racha: con r = racha(n) se cumple por construccion,
      y para n impar racha(n) >= 1 (el propio n es impar).

  ESQUELETO DE LA DEMOSTRACION:
    (1) paso impar del atajo:      x impar  =>  2 * atajo x = 3x+1        [dos_atajo]
    (2) crecimiento:   r pasos impares  =>  2^r * atajoIter r n >= 3^r * n [crecimiento]
    (3) el pico: la trayectoria CLASICA pasa por 3x+1 antes de dividir, o sea
        clasicoIter (2r-1) n = 2 * atajoIter r n                           [pico]
        (cada paso impar del atajo son DOS pasos clasicos; el pico es el paso
         impar de indice 2r-1, ese factor 2 es el "+1" del enunciado en log2)
    (4) juntando:  2 * 3^r * n <= 2^r * clasicoIter (2r-1) n <= 2^r * altitud(n).
-/

set_option maxRecDepth 40000

-- ===================== definiciones (escritas aqui, sin mirar el repo) ==========

def atajo (x : Nat) : Nat := (3*x+1)/2

def atajoIter : Nat → Nat → Nat
  | 0,   n => n
  | k+1, n => atajoIter k (atajo n)

def clasico (x : Nat) : Nat := if x % 2 = 1 then 3*x+1 else x/2

def clasicoIter : Nat → Nat → Nat
  | 0,   n => n
  | k+1, n => clasicoIter k (clasico n)

/-- altitud con presupuesto: maximo de la trayectoria clasica en los pasos 0..F -/
def maxTray : Nat → Nat → Nat
  | 0,   n => n
  | f+1, n => Nat.max n (maxTray f (clasico n))

/-- racha con combustible: pasos impares seguidos al arranque, bajo el ATAJO.
    (solo para los casos concretos por `decide`; los teoremas usan la hipotesis literal) -/
def rachaFuel : Nat → Nat → Nat
  | 0,   _ => 0
  | f+1, n => if n % 2 = 1 then 1 + rachaFuel f (atajo n) else 0

-- ===================== control del objeto (LA TRAMPA): casos contra el mapa =====

-- la trayectoria clasica del 7:  7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1
theorem control_clasico_7 : clasicoIter 1 7 = 22 ∧ clasicoIter 2 7 = 11 ∧
    clasicoIter 5 7 = 52 ∧ clasicoIter 16 7 = 1 ∧ maxTray 16 7 = 52 := by decide

-- el atajo del 7:  7 -> 11 -> 17 -> 26 (tres impares seguidos, racha 3)
theorem control_atajo_7 : atajoIter 1 7 = 11 ∧ atajoIter 2 7 = 17 ∧
    atajoIter 3 7 = 26 ∧ rachaFuel 7 7 = 3 ∧ atajoIter 3 7 % 2 = 0 := by decide

-- el caso conocido del repo: altitud(27) = 9232, racha(27) = 2, y llega al 1 en 111 pasos
theorem control_27 : rachaFuel 27 27 = 2 ∧ clasicoIter 111 27 = 1 ∧
    maxTray 111 27 = 9232 := by decide

-- ===================== lema (1): el paso impar del atajo ========================

theorem dos_atajo (x : Nat) (h : x % 2 = 1) : 2 * atajo x = 3*x+1 := by
  unfold atajo; omega

/-- monotonia del producto por la izquierda, con el nombre corto que usa el resto -/
theorem mulmono (a b c : Nat) (h : b ≤ c) : a * b ≤ a * c :=
  Nat.mul_le_mul_left a h

-- ===================== lema (2): r pasos impares crecen como (3/2)^r ============

theorem crecimiento : ∀ (r n : Nat), (∀ i, i < r → atajoIter i n % 2 = 1) →
    3^r * n ≤ 2^r * atajoIter r n := by
  intro r
  induction r with
  | zero =>
    intro n _
    show 3^0 * n ≤ 2^0 * atajoIter 0 n
    simp [atajoIter]
  | succ k ih =>
    intro n h
    have hn : n % 2 = 1 := h 0 (Nat.zero_lt_succ k)
    have hshift : ∀ i, i < k → atajoIter i (atajo n) % 2 = 1 := by
      intro i hi
      exact h (i+1) (Nat.succ_lt_succ hi)
    have ihn := ih (atajo n) hshift
    have h2 : 2 * atajo n = 3*n+1 := dos_atajo n hn
    show 3^(k+1) * n ≤ 2^(k+1) * atajoIter (k+1) n
    calc 3^(k+1) * n
        = 3^k * (3*n) := by rw [Nat.pow_succ, Nat.mul_assoc]
      _ ≤ 3^k * (3*n+1) := mulmono _ _ _ (Nat.le_succ _)
      _ = 3^k * (2 * atajo n) := by rw [h2]
      _ = 2 * (3^k * atajo n) := by
          rw [← Nat.mul_assoc, Nat.mul_comm (3^k) 2, Nat.mul_assoc]
      _ ≤ 2 * (2^k * atajoIter k (atajo n)) := mulmono _ _ _ ihn
      _ = 2^(k+1) * atajoIter (k+1) n := by
          rw [← Nat.mul_assoc, Nat.mul_comm 2 (2^k), Nat.pow_succ]
          rfl

-- ===================== lema (3): el pico de la trayectoria CLASICA ==============

/-- n impar: el clasico da 3n+1, y el clasico de 3n+1 (par) es el atajo de n -/
theorem paso_doble (n : Nat) (hn : n % 2 = 1) :
    clasico n = 3*n+1 ∧ clasico (3*n+1) = atajo n := by
  constructor
  · simp [clasico, hn]
  · have h2 : ¬ ((3*n+1) % 2 = 1) := by omega
    simp [clasico, atajo, h2]

/-- con m+1 pasos impares al arranque, el paso clasico 2m+1 es EXACTAMENTE
    el doble del iterado m+1 del atajo: ahi vive el factor 2 del enunciado -/
theorem pico : ∀ (m n : Nat), (∀ i, i < m+1 → atajoIter i n % 2 = 1) →
    clasicoIter (2*m+1) n = 2 * atajoIter (m+1) n := by
  intro m
  induction m with
  | zero =>
    intro n h
    have hn : n % 2 = 1 := h 0 (Nat.zero_lt_succ 0)
    show clasicoIter 1 n = 2 * atajoIter 1 n
    show clasico n = 2 * atajo n
    rw [(paso_doble n hn).1, dos_atajo n hn]
  | succ m ih =>
    intro n h
    have hn : n % 2 = 1 := h 0 (Nat.zero_lt_succ (m+1))
    have hshift : ∀ i, i < m+1 → atajoIter i (atajo n) % 2 = 1 := by
      intro i hi
      exact h (i+1) (Nat.succ_lt_succ hi)
    have e1 : clasico (clasico n) = atajo n := by
      rw [(paso_doble n hn).1]
      exact (paso_doble n hn).2
    show clasicoIter (2*m+1) (clasico (clasico n)) = 2 * atajoIter (m+1) (atajo n)
    rw [e1]
    exact ih (atajo n) hshift

-- ===================== el teorema: el piso, sobre el paso pico ==================

/-- EL PISO (forma nuclear): si n arranca con r >= 1 pasos impares del atajo,
    el paso clasico 2r-1 ya cumple  2 * 3^r * n <= 2^r * (ese valor).
    La hipotesis `hodd` ES la definicion de racha(n) >= r; con r = racha(n)
    se cumple por construccion, y n impar da racha >= 1. -/
theorem piso (n r : Nat) (hr : 1 ≤ r)
    (hodd : ∀ i, i < r → atajoIter i n % 2 = 1) :
    2 * (3^r * n) ≤ 2^r * clasicoIter (2*r - 1) n := by
  cases r with
  | zero => omega
  | succ m =>
    have hidx : 2*(m+1) - 1 = 2*m+1 := by omega
    rw [hidx, pico m n hodd]
    have hg := crecimiento (m+1) n hodd
    calc 2 * (3^(m+1) * n)
        ≤ 2 * (2^(m+1) * atajoIter (m+1) n) := mulmono _ _ _ hg
      _ = 2^(m+1) * (2 * atajoIter (m+1) n) := by
          rw [← Nat.mul_assoc, Nat.mul_comm 2 (2^(m+1)), Nat.mul_assoc]

-- ===================== la altitud mayora cualquier paso =========================

theorem tray_le_max : ∀ (F j n : Nat), j ≤ F → clasicoIter j n ≤ maxTray F n := by
  intro F
  induction F with
  | zero =>
    intro j n hj
    have hj0 : j = 0 := Nat.le_zero.mp hj
    subst hj0
    exact Nat.le_refl n
  | succ F ih =>
    intro j n hj
    cases j with
    | zero =>
      exact Nat.le_max_left n (maxTray F (clasico n))
    | succ j =>
      have hj' : j ≤ F := Nat.le_of_succ_le_succ hj
      exact Nat.le_trans (ih j (clasico n) hj')
        (Nat.le_max_right n (maxTray F (clasico n)))

-- ===================== EL ENUNCIADO A2, en forma entera =========================

/-- EL PISO DE LA ALTITUD: para n con r >= 1 pasos impares del atajo al arranque
    (o sea: n IMPAR y r = racha(n)), y cualquier presupuesto F que alcance el
    paso pico 2r-1, la altitud cumple

        altitud(n) * 2^r  >=  2 * n * 3^r

    que es  log2(altitud/n) >= r*log2(3/2) + 1  decidido en enteros. -/
theorem piso_altitud (n r F : Nat) (hr : 1 ≤ r) (hF : 2*r - 1 ≤ F)
    (hodd : ∀ i, i < r → atajoIter i n % 2 = 1) :
    2 * (3^r * n) ≤ 2^r * maxTray F n :=
  Nat.le_trans (piso n r hr hodd)
    (mulmono _ _ _ (tray_le_max F (2*r-1) n hF))

-- ===================== casos concretos del teorema, por decide ==================

-- n = 7, racha 3, altitud 52:   52 * 8 = 416 >= 2*7*27 = 378
theorem caso_7 : 2 * (3^3 * 7) ≤ 2^3 * maxTray 16 7 := by decide

-- n = 27, racha 2, altitud 9232:   9232 * 4 >= 2*27*9 = 486
theorem caso_27 : 2 * (3^2 * 27) ≤ 2^2 * maxTray 111 27 := by decide

-- BORDE n = 1: racha(1) = 1, y la trayectoria 1 -> 4 -> 2 -> 1 da altitud 4:
--   4 * 2 = 8 >= 2*1*3 = 6.  PERO exige que la altitud incluya el paso al 4:
--   con una "trayectoria" que se pare en el 1 sin dar el paso, seria 2 >= 6, FALSO.
theorem caso_1 : rachaFuel 1 1 = 1 ∧ (2 * (3^1 * 1) ≤ 2^1 * maxTray 1 1) := by decide
theorem borde_1_sin_paso : ¬ (2 * (3^1 * 1) ≤ 2^1 * maxTray 0 1) := by decide

-- n = 3, racha 2, altitud 16:   16*4 = 64 >= 2*3*9 = 54  (apretado)
theorem caso_3 : rachaFuel 3 3 = 2 ∧ (2 * (3^2 * 3) ≤ 2^2 * maxTray 7 3) := by decide

-- BORDE n PAR: la hipotesis de imparidad es NECESARIA. n = 10 tiene racha 0 y
-- el piso con r = 0 pediria altitud >= 2n = 20, pero altitud(10) = 16.
theorem borde_par_10 : rachaFuel 10 10 = 0 ∧
    ¬ (2 * (3^0 * 10) ≤ 2^0 * maxTray 6 10) := by decide

-- racha alta: n = 2^6 - 1 = 63 arranca con 6 impares seguidos (racha real = 6)
theorem caso_63 : rachaFuel 63 63 = 6 ∧ atajoIter 6 63 % 2 = 0 ∧
    (2 * (3^6 * 63) ≤ 2^6 * maxTray 107 63) := by decide

-- para n impar la racha es >= 1 (el propio n es impar): el enunciado nunca
-- se evalua con r = 0 en su ambito
theorem racha_impar_pos (n f : Nat) (hn : n % 2 = 1) : 1 ≤ rachaFuel (f+1) n := by
  unfold rachaFuel
  simp [hn]

-- ===================== control final ============================================

#print axioms piso
#print axioms piso_altitud
#print axioms crecimiento
#print axioms pico
#print axioms caso_27
#print axioms borde_par_10
