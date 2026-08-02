/-
A24 — Garner G1, mapa CLASICO (n par -> n/2, n impar -> 3n+1).

Enunciado: (8k+4, 8k+5) confluyen siempre en 3 pasos para todo k >= 0,
y tienen la MISMA ALTURA para todo k >= 1.

Formalizacion de "misma altura": la altura no es definible como funcion
total sin la conjetura entera, pero "misma altura" SI se formaliza exacto:
para todo n,  T^n(8k+4) = 1  <->  T^n(8k+5) = 1.
Los conjuntos de tiempos de llegada al 1 son identicos, luego sus minimos
(las alturas) coinciden si existen. Es mas fuerte que la igualdad de alturas.

Y el k >= 1 es NECESARIO: en k = 0, T^2(4) = 1 pero T^2(5) = 8 (decide).
-/

-- El mapa clasico, escrito aqui mismo (no importado de ningun sitio)
def T (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

def iterT : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => iterT k (T n)

-- La trampa del objeto: comprobar que T es Collatz de verdad, por el nucleo
theorem T_es_collatz : T 6 = 3 ∧ T 3 = 10 ∧ T 10 = 5 ∧ T 5 = 16 ∧ T 16 = 8 := by
  decide

theorem T_even (n : Nat) (h : n % 2 = 0) : T n = n / 2 := by
  unfold T; simp [h]

theorem T_odd (n : Nat) (h : n % 2 = 1) : T n = 3 * n + 1 := by
  unfold T; simp [h]

theorem iter1 (x : Nat) : iterT 1 x = T x := rfl
theorem iter2 (x : Nat) : iterT 2 x = T (T x) := rfl
theorem iter3 (x : Nat) : iterT 3 x = T (T (T x)) := rfl

-- ===== PARTE 1: CONFLUENCIA, para TODO k >= 0 =====
-- 8k+4 -> 4k+2 -> 2k+1 -> 6k+4   (2 pares, 1 impar)
theorem conf_a (k : Nat) : iterT 3 (8*k+4) = 6*k+4 := by
  rw [iter3, T_even (8*k+4) (by omega)]
  have h1 : (8*k+4)/2 = 4*k+2 := by omega
  rw [h1, T_even (4*k+2) (by omega)]
  have h2 : (4*k+2)/2 = 2*k+1 := by omega
  rw [h2, T_odd (2*k+1) (by omega)]
  omega

-- 8k+5 -> 24k+16 -> 12k+8 -> 6k+4   (1 impar, 2 pares)
theorem conf_b (k : Nat) : iterT 3 (8*k+5) = 6*k+4 := by
  rw [iter3, T_odd (8*k+5) (by omega)]
  have h1 : 3*(8*k+5)+1 = 24*k+16 := by omega
  rw [h1, T_even (24*k+16) (by omega)]
  have h2 : (24*k+16)/2 = 12*k+8 := by omega
  rw [h2, T_even (12*k+8) (by omega)]
  omega

theorem confluyen (k : Nat) : iterT 3 (8*k+4) = iterT 3 (8*k+5) := by
  rw [conf_a, conf_b]

-- ===== Los valores intermedios (para el argumento de altura) =====
theorem pref_a1 (k : Nat) : iterT 1 (8*k+4) = 4*k+2 := by
  rw [iter1, T_even (8*k+4) (by omega)]
  omega

theorem pref_a2 (k : Nat) : iterT 2 (8*k+4) = 2*k+1 := by
  rw [iter2, T_even (8*k+4) (by omega)]
  have h1 : (8*k+4)/2 = 4*k+2 := by omega
  rw [h1, T_even (4*k+2) (by omega)]
  omega

theorem pref_b1 (k : Nat) : iterT 1 (8*k+5) = 24*k+16 := by
  rw [iter1, T_odd (8*k+5) (by omega)]
  omega

theorem pref_b2 (k : Nat) : iterT 2 (8*k+5) = 12*k+8 := by
  rw [iter2, T_odd (8*k+5) (by omega)]
  have h1 : 3*(8*k+5)+1 = 24*k+16 := by omega
  rw [h1, T_even (24*k+16) (by omega)]
  omega

-- Composicion de iterados
theorem iter_add (a b n : Nat) : iterT (a + b) n = iterT b (iterT a n) := by
  induction a generalizing n with
  | zero =>
    have h : 0 + b = b := by omega
    rw [h]
    rfl
  | succ a ih =>
    have h : (a + 1) + b = (a + b) + 1 := by omega
    rw [h]
    show iterT (a + b) (T n) = iterT b (iterT (a+1) n)
    rw [ih (T n)]
    rfl

-- ===== PARTE 2: MISMA ALTURA, para todo k >= 1 =====
-- Formalizada como igualdad de los conjuntos de tiempos de llegada al 1.
theorem misma_altura (k : Nat) (hk : 1 ≤ k) (n : Nat) :
    iterT n (8*k+4) = 1 ↔ iterT n (8*k+5) = 1 := by
  by_cases h : n < 3
  · -- antes de la confluencia: ninguno de los dos toca el 1 (aqui entra k >= 1)
    have h3 : n = 0 ∨ n = 1 ∨ n = 2 := by omega
    cases h3 with
    | inl h0 =>
      rw [h0]
      show 8*k+4 = 1 ↔ 8*k+5 = 1
      omega
    | inr h12 =>
      cases h12 with
      | inl h1 =>
        rw [h1, pref_a1, pref_b1]
        omega
      | inr h2 =>
        -- el paso donde vive el contraejemplo de k = 0: 2k+1 = 1 sii k = 0
        rw [h2, pref_a2, pref_b2]
        omega
  · -- desde la confluencia las dos trayectorias son la misma
    have hn : n = 3 + (n - 3) := by omega
    rw [hn, iter_add, iter_add, conf_a, conf_b]

-- ===== EL BORDE k = 0: la altura FALLA, la confluencia NO =====
set_option maxRecDepth 4000

-- confluencia en k = 0 tambien vale (T^3(4) = T^3(5) = 4, pasando por el 1)
theorem k0_confluye : iterT 3 4 = 4 ∧ iterT 3 5 = 4 := by decide

-- pero altura(4) = 2 y altura(5) = 5: el 4 toca el 1 ANTES de la confluencia
theorem k0_altura_distinta :
    iterT 2 4 = 1 ∧ iterT 1 4 ≠ 1 ∧
    iterT 5 5 = 1 ∧ iterT 4 5 ≠ 1 ∧
    iterT 2 5 = 8 := by decide

-- ===== CASO CONOCIDO, comprobado por el nucleo (no #eval): k = 1 =====
-- el par (12, 13): confluyen en 10 al paso 3, y altura(12) = altura(13) = 9
theorem caso_12_13 :
    iterT 3 12 = 10 ∧ iterT 3 13 = 10 ∧
    iterT 9 12 = 1 ∧ iterT 9 13 = 1 ∧
    iterT 8 12 ≠ 1 ∧ iterT 8 13 ≠ 1 := by decide

-- y un k mas grande, k = 7: (60, 61) confluyen en 46
theorem caso_60_61 :
    iterT 3 60 = 46 ∧ iterT 3 61 = 46 ∧
    iterT 19 60 = 1 ∧ iterT 19 61 = 1 ∧
    iterT 18 60 ≠ 1 ∧ iterT 18 61 ≠ 1 := by decide

#print axioms confluyen
#print axioms conf_a
#print axioms conf_b
#print axioms misma_altura
#print axioms k0_confluye
#print axioms k0_altura_distinta
#print axioms caso_12_13
#print axioms caso_60_61
