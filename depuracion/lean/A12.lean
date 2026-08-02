/-
  ITEM A12: "n + espejo(n) = 10^k, exacto y siempre" (todo n >= 1, base 10)

  INTERPRETACION FORMALIZADA:
    espejo(n) = el complemento a 10 de n, construido DIGITO A DIGITO
    (los ceros finales quedan cero, el primer digito no nulo por la derecha
     pasa a 10-d, y los restantes a 9-d), y k = numero de cifras de n.

  PUNTO CRITICO ANTI-CIRCULARIDAD: si espejo se definiera como 10^k - n,
  el enunciado seria una tautologia. Aqui espejo se define por construccion
  digital independiente, y "n + espejo(n) = 10^(cifras n)" se DEMUESTRA.

  Todas las definiciones van por recursion estructural sobre un combustible
  (fuel = n basta, porque n/10 < n cuando n >= 10), para que el nucleo
  pueda evaluarlas con `decide`.

  No hay mapa de Collatz aqui: el enunciado es aritmetica decimal pura.
-/

set_option maxRecDepth 40000

-- numero de cifras decimales (convenio: numDigits 0 = 1)
def numDigitsAux : Nat → Nat → Nat
  | 0, _ => 1
  | fuel+1, n => if n < 10 then 1 else numDigitsAux fuel (n / 10) + 1

def numDigits (n : Nat) : Nat := numDigitsAux n n

-- complemento a 9, digito a digito: cada digito d pasa a 9 - d
def comp9Aux : Nat → Nat → Nat
  | 0, n => 9 - n
  | fuel+1, n => if n < 10 then 9 - n else 10 * comp9Aux fuel (n / 10) + (9 - n % 10)

def comp9 (n : Nat) : Nat := comp9Aux n n

-- EL ESPEJO: complemento a 10, digito a digito.
--   n < 10          ->  10 - n
--   ultimo digito 0 ->  se conserva el 0 y se refleja el resto
--   ultimo digito d ->  10 - d, y los digitos restantes a 9 - (digito)
def espejoAux : Nat → Nat → Nat
  | 0, n => 10 - n
  | fuel+1, n =>
    if n < 10 then 10 - n
    else if n % 10 = 0 then 10 * espejoAux fuel (n / 10)
    else 10 * comp9Aux fuel (n / 10) + (10 - n % 10)

def espejo (n : Nat) : Nat := espejoAux n n

-- ============================================================
-- LEMA: el complemento a 9 digital cumple  comp9(n) + n + 1 = 10^cifras(n)
-- ============================================================
theorem comp9Aux_correct : ∀ (fuel n : Nat), n ≤ fuel →
    comp9Aux fuel n + n + 1 = 10 ^ numDigitsAux fuel n := by
  intro fuel
  induction fuel with
  | zero =>
    intro n h
    have hn : n = 0 := by omega
    subst hn
    decide
  | succ f ih =>
    intro n h
    by_cases h10 : n < 10
    · simp only [comp9Aux, numDigitsAux]
      rw [if_pos h10, if_pos h10]
      have hp : (10:Nat) ^ 1 = 10 := by decide
      rw [hp]
      omega
    · simp only [comp9Aux, numDigitsAux]
      rw [if_neg h10, if_neg h10, Nat.pow_succ]
      have ihd := ih (n / 10) (by omega)
      omega

-- ============================================================
-- TEOREMA CENTRAL:  n + espejo(n) = 10^cifras(n)   (para TODO n, incluso 0)
-- ============================================================
theorem espejoAux_correct : ∀ (fuel n : Nat), n ≤ fuel →
    n + espejoAux fuel n = 10 ^ numDigitsAux fuel n := by
  intro fuel
  induction fuel with
  | zero =>
    intro n h
    have hn : n = 0 := by omega
    subst hn
    decide
  | succ f ih =>
    intro n h
    by_cases h10 : n < 10
    · simp only [espejoAux, numDigitsAux]
      rw [if_pos h10, if_pos h10]
      have hp : (10:Nat) ^ 1 = 10 := by decide
      rw [hp]
      omega
    · simp only [espejoAux, numDigitsAux]
      rw [if_neg h10, if_neg h10]
      by_cases hm0 : n % 10 = 0
      · rw [if_pos hm0, Nat.pow_succ]
        have ihd := ih (n / 10) (by omega)
        omega
      · rw [if_neg hm0, Nat.pow_succ]
        have hc := comp9Aux_correct f (n / 10) (by omega)
        omega

-- El enunciado A12 tal cual: para todo n >= 1, n + espejo(n) = 10^k
-- con k = numero de cifras de n.
theorem enunciado_A12 (n : Nat) (_h : 1 ≤ n) :
    n + espejo n = 10 ^ numDigits n :=
  espejoAux_correct n n (Nat.le_refl n)

-- La forma existencial ("cae exacto sobre ALGUNA recta x + y = 10^k")
theorem enunciado_A12_existe (n : Nat) (_h : 1 ≤ n) :
    ∃ k : Nat, n + espejo n = 10 ^ k :=
  ⟨numDigits n, espejoAux_correct n n (Nat.le_refl n)⟩

-- ============================================================
-- CASOS CONOCIDOS, comprobados por el NUCLEO con `decide` (no #eval):
-- las parejas espejo del repo (2-8, 20-80, 47-53, 332-668, 350-650)
-- y el punto fijo 5. Esto ancla que `espejo` es EL objeto del repo.
-- ============================================================
theorem caso_punto_fijo_5 : espejo 5 = 5 ∧ 5 + espejo 5 = 10 ^ 1 := by decide
theorem caso_2_8   : espejo 2 = 8 ∧ espejo 8 = 2 := by decide
theorem caso_20_80 : espejo 20 = 80 ∧ espejo 80 = 20 := by decide
theorem caso_47_53 : espejo 47 = 53 ∧ espejo 53 = 47 ∧ 47 + 53 = 10 ^ 2 := by decide
theorem caso_332_668 : espejo 332 = 668 ∧ espejo 668 = 332 := by decide
theorem caso_350_650 : espejo 350 = 650 ∧ espejo 650 = 350 := by decide

-- BORDES: n = 1, n = 9, la frontera de decada n = 10 y n = 100,
-- y el tope de 3 cifras n = 999. El convenio en la frontera: espejo(10)=90
-- y la suma cae en 10^2 (la decada de "2 cifras"), no en 10^1.
theorem borde_1    : espejo 1 = 9 ∧ 1 + espejo 1 = 10 ^ 1 := by decide
theorem borde_9    : espejo 9 = 1 := by decide
theorem borde_10   : espejo 10 = 90 ∧ 10 + espejo 10 = 10 ^ 2 := by decide
theorem borde_100  : espejo 100 = 900 ∧ 100 + espejo 100 = 10 ^ 3 := by decide
theorem borde_999  : espejo 999 = 1 ∧ 999 + espejo 999 = 10 ^ 3 := by decide
theorem borde_1000 : espejo 1000 = 9000 := by decide

-- El 0, EXCLUIDO por el enunciado (n >= 1): con esta definicion espejo(0)=10
-- y la identidad tambien se cumple (0 + 10 = 10^1), pero es convenio.
theorem borde_0 : espejo 0 = 10 ∧ 0 + espejo 0 = 10 ^ 1 := by decide

-- BARRIDO exhaustivo verificado por el nucleo: todo n de 1 a 999.
theorem barrido_hasta_1000 :
    ∀ n : Nat, n < 1000 → 1 ≤ n → n + espejo n = 10 ^ numDigits n := by decide

-- HALLAZGO DE BORDE (no toca el enunciado A12, pero queda registrado):
-- el espejo NO es una involucion. Cuando el complemento pierde cifras
-- (n en la parte alta de la decada), espejo(espejo n) cae en otra decada:
--   espejo(95) = 5   (95 + 5 = 100, correcto para el enunciado)
--   espejo(5)  = 5   (5 esta en la decada de 1 cifra)  ->  5 ≠ 95.
-- El enunciado de la suma se cumple SIEMPRE; la simetria del dibujo
-- (cada punto tiene su reflejo en la MISMA recta) no — ese seria otro
-- enunciado, y es falso tal cual.
theorem no_involucion_95 : espejo 95 = 5 ∧ espejo (espejo 95) = 5 := by decide
theorem no_involucion_999 : espejo 999 = 1 ∧ espejo (espejo 999) = 9 := by decide

-- ============================================================
-- CONTROL DE AXIOMAS
-- ============================================================
#print axioms comp9Aux_correct
#print axioms espejoAux_correct
#print axioms enunciado_A12
#print axioms enunciado_A12_existe
#print axioms caso_47_53
#print axioms barrido_hasta_1000
#print axioms no_involucion_95
#print axioms no_involucion_999
