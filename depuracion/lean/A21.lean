/-
A21 — Verificacion en Lean 4 (nucleo, SIN Mathlib) del criterio de fusion de clases.

ENUNCIADO LITERAL (afirmaciones.db, A21):
  "dos consecutivos se funden para todos los infinitos m >= 1 de la clase
   exactamente cuando S_k(r) == S_k(r+1) y T^k(r) == T^k(r+1)"

MAPA: T = ATAJO  (n par -> n/2 ; n impar -> (3n+1)/2).  Lo defino yo mismo abajo
y lo compruebo contra una trayectoria calculada a mano (n = 7), como teorema
`by decide`, no con #eval.
Las alturas del contraejemplo m = 0 se miden con el mapa CLASICO C
(n par -> n/2 ; n impar -> 3n+1), que es donde la base da "alturas 5 y 8".

FORMALIZACION DE "SE FUNDEN": las dos trayectorias coinciden en el paso k del
atajo. Ademas se demuestra (fusion_desfase_cero) que coinciden en el MISMO
indice del mapa clasico, k + S_k, o sea con desfase 0.

RESULTADOS:
  terras            : T^k(2^k*m + s) = 3^(S_k(s))*m + T^k(s)   (todo k, m, s)
  suficiencia       : criterio => coinciden en el paso k PARA TODO m (incluido m=0)
  necesidad         : coinciden para todo m>=1 => criterio  (bastan m=1 y m=2)
  criterio          : el "exactamente cuando" como iff, con m >= 1
  fusion_desfase_cero: criterio => mismo valor en el MISMO indice clasico k+S_k
  no_toca_uno       : m >= 1 => la trayectoria no toca el 1 antes del paso k
                      (esta es la funcion exacta de la hipotesis m >= 1)
  contraejemplos m=0: (5,6) alturas clasicas 5 y 8; (4,5) alturas 2 y 5 (decide)
  excepciones       : en k=5,6,7 las clases buenas con alturas distintas en m=0
                      son EXACTAMENTE r = 2, 4, 5 (decide)
-/

set_option maxRecDepth 40000

-- ============================ definiciones ============================

/-- El mapa del ATAJO: par -> n/2, impar -> (3n+1)/2. -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- k iteraciones del atajo. -/
def Titer : Nat → Nat → Nat
  | 0,     n => n
  | k + 1, n => Titer k (T n)

/-- S_k(n): cuantos de los primeros k pasos del atajo caen en impar. -/
def S : Nat → Nat → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 0 else 1) + S k (T n)

/-- El mapa CLASICO: par -> n/2, impar -> 3n+1. Solo para medir alturas. -/
def C (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- j iteraciones del clasico. -/
def Citer : Nat → Nat → Nat
  | 0,     n => n
  | j + 1, n => Citer j (C n)

/-- Altura clasica con combustible: pasos del clasico hasta tocar 1 por
    primera vez. Con combustible suficiente (certificado abajo) es LA altura. -/
def alturaC : Nat → Nat → Nat
  | 0,     _ => 0
  | f + 1, n => if n = 1 then 0 else 1 + alturaC f (C n)

-- ecuaciones de desplegado
theorem Titer_zero (n : Nat) : Titer 0 n = n := rfl
theorem Titer_succ (k n : Nat) : Titer (k + 1) n = Titer k (T n) := rfl
theorem S_zero (n : Nat) : S 0 n = 0 := rfl
theorem S_succ (k n : Nat) :
    S (k + 1) n = (if n % 2 = 0 then 0 else 1) + S k (T n) := rfl
theorem Citer_succ (j n : Nat) : Citer (j + 1) n = Citer j (C n) := rfl

-- ==================== el paso, separado por paridad ====================

theorem T_par {x s : Nat} (h : s % 2 = 0) : T (2 * x + s) = x + T s := by
  unfold T
  rw [if_pos (show (2 * x + s) % 2 = 0 by omega), if_pos h]
  omega

theorem T_impar {x s : Nat} (h : s % 2 = 1) : T (2 * x + s) = 3 * x + T s := by
  unfold T
  rw [if_neg (show ¬(2 * x + s) % 2 = 0 by omega),
      if_neg (show ¬s % 2 = 0 by omega)]
  omega

-- ===================== Terras 1.2: la recta en m =====================

/-- T^k(2^k*m + s) = 3^(S_k(s))*m + T^k(s), para TODO k, m, s.
    La pendiente y la ordenada dependen solo de s. -/
theorem terras (k : Nat) :
    ∀ m s : Nat, Titer k (2 ^ k * m + s) = 3 ^ S k s * m + Titer k s := by
  induction k with
  | zero =>
    intro m s
    rw [Titer_zero, Titer_zero, S_zero, Nat.pow_zero]
  | succ k ih =>
    intro m s
    have hsplit : 2 ^ (k + 1) * m + s = 2 * (2 ^ k * m) + s := by
      rw [Nat.pow_succ, Nat.mul_comm (2 ^ k) 2, Nat.mul_assoc]
    rw [Titer_succ, Titer_succ, S_succ, hsplit]
    by_cases h : s % 2 = 0
    · rw [T_par h, ih m (T s), if_pos h, Nat.zero_add]
    · have h1 : s % 2 = 1 := by omega
      rw [T_impar h1]
      have h2 : 3 * (2 ^ k * m) = 2 ^ k * (3 * m) := by
        rw [Nat.mul_comm 3 (2 ^ k * m), Nat.mul_assoc, Nat.mul_comm m 3]
      rw [h2, ih (3 * m) (T s), if_neg h]
      have h3 : 3 ^ (1 + S k (T s)) = 3 ^ S k (T s) * 3 := by
        rw [Nat.add_comm 1 (S k (T s)), Nat.pow_succ]
      rw [h3, Nat.mul_assoc]

/-- El vector de paridad (su cuenta S_k) depende solo del resto: invariante. -/
theorem S_inv (k : Nat) : ∀ m s : Nat, S k (2 ^ k * m + s) = S k s := by
  induction k with
  | zero => intro m s; rfl
  | succ k ih =>
    intro m s
    have hsplit : 2 ^ (k + 1) * m + s = 2 * (2 ^ k * m) + s := by
      rw [Nat.pow_succ, Nat.mul_comm (2 ^ k) 2, Nat.mul_assoc]
    rw [S_succ, S_succ, hsplit]
    by_cases h : s % 2 = 0
    · rw [if_pos h, if_pos (show (2 * (2 ^ k * m) + s) % 2 = 0 by omega),
          T_par h, ih m (T s)]
    · have h1 : s % 2 = 1 := by omega
      rw [if_neg h, if_neg (show ¬(2 * (2 ^ k * m) + s) % 2 = 0 by omega),
          T_impar h1]
      have h2 : 3 * (2 ^ k * m) = 2 ^ k * (3 * m) := by
        rw [Nat.mul_comm 3 (2 ^ k * m), Nat.mul_assoc, Nat.mul_comm m 3]
      rw [h2, ih (3 * m) (T s)]

-- ================== el criterio: las dos direcciones ==================

/-- SUFICIENCIA, y vale para TODO m, incluido m = 0: si S y T^k coinciden en
    (r, r+1), las trayectorias coinciden en el paso k para todo m. -/
theorem suficiencia (k r : Nat)
    (h1 : S k r = S k (r + 1)) (h2 : Titer k r = Titer k (r + 1)) :
    ∀ m : Nat, Titer k (2 ^ k * m + r) = Titer k (2 ^ k * m + (r + 1)) := by
  intro m
  rw [terras k m r, terras k m (r + 1), h1, h2]

theorem pow3_pos (a : Nat) : 0 < 3 ^ a := by
  induction a with
  | zero => decide
  | succ a ih => rw [Nat.pow_succ]; omega

theorem pow3_inj {a b : Nat} (h : 3 ^ a = 3 ^ b) : a = b := by
  induction a generalizing b with
  | zero =>
    cases b with
    | zero => rfl
    | succ b =>
      exfalso
      rw [Nat.pow_zero, Nat.pow_succ] at h
      have := pow3_pos b
      omega
  | succ a ih =>
    cases b with
    | zero =>
      exfalso
      rw [Nat.pow_zero, Nat.pow_succ] at h
      have := pow3_pos a
      omega
    | succ b =>
      rw [Nat.pow_succ, Nat.pow_succ] at h
      have h2 : 3 ^ a = 3 ^ b := by omega
      rw [ih h2]

/-- NECESIDAD: si coinciden en el paso k para todo m >= 1, el criterio se
    cumple. Bastan dos valores (m = 1 y m = 2): dos rectas que coinciden en
    dos puntos tienen la misma pendiente y la misma ordenada. -/
theorem necesidad (k r : Nat)
    (h : ∀ m, 1 ≤ m → Titer k (2 ^ k * m + r) = Titer k (2 ^ k * m + (r + 1))) :
    S k r = S k (r + 1) ∧ Titer k r = Titer k (r + 1) := by
  have e1 := h 1 (by omega)
  have e2 := h 2 (by omega)
  rw [terras k 1 r, terras k 1 (r + 1)] at e1
  rw [terras k 2 r, terras k 2 (r + 1)] at e2
  have hpow : 3 ^ S k r = 3 ^ S k (r + 1) := by omega
  exact ⟨pow3_inj hpow, by omega⟩

/-- EL ENUNCIADO A21, como iff, con el cuantificador m >= 1 literal. -/
theorem criterio (k r : Nat) :
    (∀ m, 1 ≤ m → Titer k (2 ^ k * m + r) = Titer k (2 ^ k * m + (r + 1)))
      ↔ (S k r = S k (r + 1) ∧ Titer k r = Titer k (r + 1)) := by
  constructor
  · exact necesidad k r
  · intro hc m _
    exact suficiencia k r hc.1 hc.2 m

-- ========== puente atajo/clasico y fusion con desfase cero ==========

theorem C_par {n : Nat} (h : n % 2 = 0) : C n = T n := by
  unfold C T
  rw [if_pos h, if_pos h]

theorem C_impar1 {n : Nat} (h : n % 2 = 1) : C n = 3 * n + 1 := by
  unfold C
  rw [if_neg (show ¬n % 2 = 0 by omega)]

theorem C_impar2 {n : Nat} (h : n % 2 = 1) : C (3 * n + 1) = T n := by
  unfold C T
  rw [if_pos (show (3 * n + 1) % 2 = 0 by omega),
      if_neg (show ¬n % 2 = 0 by omega)]

/-- k pasos del atajo = k + S_k(n) pasos del clasico, aterrizando en el
    mismo valor. -/
theorem corresp (k : Nat) : ∀ n : Nat, Citer (k + S k n) n = Titer k n := by
  induction k with
  | zero => intro n; rfl
  | succ k ih =>
    intro n
    by_cases h : n % 2 = 0
    · have hS : S (k + 1) n = S k (T n) := by
        rw [S_succ, if_pos h, Nat.zero_add]
      have hidx : (k + 1) + S (k + 1) n = (k + S k (T n)) + 1 := by
        rw [hS]; omega
      rw [hidx, Citer_succ, C_par h, ih (T n), Titer_succ]
    · have h1 : n % 2 = 1 := by omega
      have hS : S (k + 1) n = S k (T n) + 1 := by
        rw [S_succ, if_neg h]; omega
      have hidx : (k + 1) + S (k + 1) n = ((k + S k (T n)) + 1) + 1 := by
        rw [hS]; omega
      rw [hidx, Citer_succ, Citer_succ, C_impar1 h1, C_impar2 h1,
          ih (T n), Titer_succ]

/-- LA FUSION DE VERDAD, en el mapa clasico y con DESFASE CERO: si el criterio
    se cumple, para TODO m los dos consecutivos gastan los mismos impares
    (misma S) y aterrizan en el MISMO valor en el MISMO indice clasico
    k + S_k. Esto formaliza "se funden paso j contra paso j". -/
theorem fusion_desfase_cero (k r m : Nat)
    (h1 : S k r = S k (r + 1)) (h2 : Titer k r = Titer k (r + 1)) :
    S k (2 ^ k * m + r) = S k (2 ^ k * m + (r + 1)) ∧
    Citer (k + S k (2 ^ k * m + r)) (2 ^ k * m + r)
      = Citer (k + S k (2 ^ k * m + (r + 1))) (2 ^ k * m + (r + 1)) := by
  constructor
  · rw [S_inv k m r, S_inv k m (r + 1), h1]
  · rw [corresp k, corresp k, terras k m r, terras k m (r + 1), h1, h2]

-- ============ la funcion de la hipotesis m >= 1, demostrada ============

theorem dos_mul_T (x : Nat) : x ≤ 2 * T x := by
  unfold T
  by_cases h : x % 2 = 0
  · rw [if_pos h]; omega
  · rw [if_neg h]; omega

theorem titer_cota (j : Nat) : ∀ n : Nat, n ≤ 2 ^ j * Titer j n := by
  induction j with
  | zero => intro n; rw [Titer_zero, Nat.pow_zero, Nat.one_mul]; omega
  | succ j ih =>
    intro n
    rw [Titer_succ]
    have h1 := dos_mul_T n
    have h2 := ih (T n)
    have h3 : 2 ^ (j + 1) * Titer j (T n) = 2 * (2 ^ j * Titer j (T n)) := by
      rw [Nat.pow_succ, Nat.mul_comm (2 ^ j) 2, Nat.mul_assoc]
    rw [h3]
    omega

theorem pow2_pos (a : Nat) : 0 < 2 ^ a := by
  induction a with
  | zero => decide
  | succ a ih => rw [Nat.pow_succ]; omega

/-- Con m >= 1 la trayectoria de 2^k*m + r NO toca el 1 antes del paso k.
    Esta es exactamente la hipotesis que la descomposicion de alturas
    necesita, y es la funcion del "m >= 1" del enunciado. -/
theorem no_toca_uno (k m r j : Nat) (hm : 1 ≤ m) (hj : j < k) :
    1 < Titer j (2 ^ k * m + r) := by
  have hn : 2 ^ k ≤ 2 ^ k * m + r := by
    have := Nat.mul_le_mul_left (2 ^ k) hm
    omega
  have h1 := titer_cota j (2 ^ k * m + r)
  have h2 : 2 ^ (j + 1) ≤ 2 ^ k := Nat.pow_le_pow_right (by omega) hj
  have h3 : (2 : Nat) ^ (j + 1) = 2 ^ j * 2 := Nat.pow_succ 2 j
  have h4 := pow2_pos j
  by_cases ht : 1 < Titer j (2 ^ k * m + r)
  · exact ht
  · exfalso
    have hcase : Titer j (2 ^ k * m + r) = 0 ∨ Titer j (2 ^ k * m + r) = 1 := by
      omega
    cases hcase with
    | inl h0 => rw [h0, Nat.mul_zero] at h1; omega
    | inr hu => rw [hu, Nat.mul_one] at h1; omega

-- ================= LA TRAMPA: el mapa contra la realidad =================

/-- Trayectoria del 7 calculada a mano, ambos mapas, como TEOREMA por decide:
    atajo:   7 -> 11 -> 17 -> 26 -> 13 -> 20 -> 10 -> 5 -> 8 -> 4 -> 2 -> 1
             (11 pasos, 5 de ellos impares)
    clasico: 7 -> 22 -> 11 -> ... -> 1 en 16 pasos. -/
theorem mapa_correcto :
    Titer 1 7 = 11 ∧ Titer 2 7 = 17 ∧ Titer 3 7 = 26 ∧ Titer 4 7 = 13 ∧
    Titer 11 7 = 1 ∧ S 11 7 = 5 ∧
    Citer 1 7 = 22 ∧ Citer 2 7 = 11 ∧ Citer 16 7 = 1 := by decide

/-- Instancia concreta de Terras: r = 5, k = 5, m = 1:
    T^5(37) = 3^2 * 1 + T^5(5) = 9 + 2 = 11, y T^5(38) = 11 tambien. -/
theorem terras_instancia :
    Titer 5 37 = 3 ^ 2 * 1 + 2 ∧ Titer 5 37 = 11 ∧ Titer 5 38 = 11 := by decide

/-- El caso Wu-Huang r = 5, k = 5 (la familia (32m+5, 32m+6)):
    S_5(5) = S_5(6) = 2 y T^5(5) = T^5(6) = 2. El criterio se cumple. -/
theorem caso_wu :
    S 5 5 = 2 ∧ S 5 6 = 2 ∧ Titer 5 5 = 2 ∧ Titer 5 6 = 2 := by decide

-- ==================== los contraejemplos de m = 0 ====================

/-- (5,6), el m = 0 de la familia r=5, k=5: las alturas CLASICAS son 5 y 8
    (exactas, con minimalidad comprobada). El criterio se cumple y sin
    embargo las alturas difieren: por eso el enunciado necesita m >= 1
    cuando "fundirse" se lee como "misma altura". Notese que la coincidencia
    en el paso k SI se da incluso en m = 0 (caso_wu: T^5(5) = T^5(6) = 2);
    lo que falla es la altura, porque el 5 toca el 1 en el paso 4 < 7 = k+S. -/
theorem contraejemplo_m0_56 :
    Citer 5 5 = 1 ∧ (∀ j, j < 5 → Citer j 5 ≠ 1) ∧
    Citer 8 6 = 1 ∧ (∀ j, j < 8 → Citer j 6 ≠ 1) := by decide

/-- (4,5), el m = 0 de r=4, k=3: alturas clasicas 2 y 5. -/
theorem contraejemplo_m0_45 :
    Citer 2 4 = 1 ∧ (∀ j, j < 2 → Citer j 4 ≠ 1) ∧
    Citer 5 5 = 1 ∧ (∀ j, j < 5 → Citer j 5 ≠ 1) ∧
    S 3 4 = S 3 5 ∧ Titer 3 4 = Titer 3 5 := by decide

/-- Y el punto fino: aun en m = 0, (5,6) se encuentran en el mismo indice
    clasico k + S = 7: Citer 7 5 = Citer 7 6 = 2. Se "funden" formalmente;
    lo que se rompe es la ALTURA, porque el 5 ya paso por el 1. -/
theorem m0_se_encuentran_igual :
    Citer 7 5 = 2 ∧ Citer 7 6 = 2 := by decide

-- ================== certificado del combustible ==================

/-- alturaC 250 es LA altura clasica exacta para todo 1 <= r <= 128:
    Citer (alturaC 250 r) r = 1 y ningun indice menor llega a 1. -/
theorem altura_certificada :
    ∀ r, r < 129 → 1 ≤ r →
      (Citer (alturaC 250 r) r = 1 ∧
       ∀ j, j < alturaC 250 r → Citer j r ≠ 1) := by decide

-- ============== las clases buenas y las 3 excepciones ==============

/-- Las clases buenas mod 32 (k = 5) son exactamente
    {2, 4, 5, 12, 18, 20, 22, 28}: 8 de 32. -/
theorem clases_buenas_k5 :
    ∀ r, r < 32 →
      ((S 5 r = S 5 (r + 1) ∧ Titer 5 r = Titer 5 (r + 1))
        ↔ (r = 2 ∨ r = 4 ∨ r = 5 ∨ r = 12 ∨ r = 18 ∨ r = 20 ∨ r = 22 ∨
           r = 28)) := by decide

/-- En k = 5, las clases buenas cuyo par m = 0 tiene alturas clasicas
    DISTINTAS son exactamente r = 2, 4, 5. -/
theorem excepciones_k5 :
    ∀ r, r < 32 →
      ((S 5 r = S 5 (r + 1) ∧ Titer 5 r = Titer 5 (r + 1) ∧
        alturaC 250 r ≠ alturaC 250 (r + 1))
        ↔ (r = 2 ∨ r = 4 ∨ r = 5)) := by decide

/-- Lo mismo en k = 6 (mod 64): siguen siendo exactamente r = 2, 4, 5. -/
theorem excepciones_k6 :
    ∀ r, r < 64 →
      ((S 6 r = S 6 (r + 1) ∧ Titer 6 r = Titer 6 (r + 1) ∧
        alturaC 250 r ≠ alturaC 250 (r + 1))
        ↔ (r = 2 ∨ r = 4 ∨ r = 5)) := by decide

/-- Lo mismo en k = 7 (mod 128): siguen siendo exactamente r = 2, 4, 5. -/
theorem excepciones_k7 :
    ∀ r, r < 128 →
      ((S 7 r = S 7 (r + 1) ∧ Titer 7 r = Titer 7 (r + 1) ∧
        alturaC 250 r ≠ alturaC 250 (r + 1))
        ↔ (r = 2 ∨ r = 4 ∨ r = 5)) := by decide

-- ==================== el borde k = 0, explicito ====================

/-- En k = 0 el criterio exige Titer 0 r = Titer 0 (r+1), o sea r = r+1:
    nunca se cumple, y la coincidencia tampoco. El iff vale vacuamente y
    el borde no esconde nada. -/
theorem borde_k0 (r : Nat) :
    ¬(S 0 r = S 0 (r + 1) ∧ Titer 0 r = Titer 0 (r + 1)) := by
  intro hc
  have := hc.2
  rw [Titer_zero, Titer_zero] at this
  omega

-- ======================= control de axiomas =======================

#print axioms terras
#print axioms suficiencia
#print axioms necesidad
#print axioms criterio
#print axioms fusion_desfase_cero
#print axioms no_toca_uno
#print axioms mapa_correcto
#print axioms terras_instancia
#print axioms caso_wu
#print axioms contraejemplo_m0_56
#print axioms contraejemplo_m0_45
#print axioms altura_certificada
#print axioms clases_buenas_k5
#print axioms excepciones_k5
#print axioms excepciones_k6
#print axioms excepciones_k7
#print axioms borde_k0
