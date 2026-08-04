/- perrasconteo.lean
   EL ESQUELETO ARITMETICO DEL CONTEO DE PERRAS, demostrado en Lean 4.
   (04-08-2026; el 12o .lean del repo. Nucleo puro, sin Mathlib.)

   El teorema de Perras cuenta 2^(m-1) clases fusionadas en el estrato 2:
   2^(m-1) - 1 por la suma de ventanas (los patrones 1^j 0 1) mas
   EXACTAMENTE UNO de los dos residuos frontera. Aqui se demuestran las
   tres piezas aritmeticas de ese conteo (la biyeccion residuo-vector es
   Terras, caja demostrada, como en todos los documentos del programa):

   1. LA SUMA DE VENTANAS: suma_{i<m} 2^i = 2^m - 1 (la proposicion del
      punto 10 de teoremadeperras.txt: suma_{j=0}^{k-1} 2^(k-1-j) es la
      misma suma reindexada).
   2. EL BORDE ALTERNANTE: 3^m mod 4 alterna 1, 3, 1, 3, ... -- la
      identidad que decide cual de los dos residuos frontera funde.
   3. EXACTAMENTE UNO: para todo m >= 1, los dos residuos frontera
      (vectores 1^(m-1) 0 y 1^m) deciden en sentidos OPUESTOS: la
      paridad de (3^(m-1) - 1)/2 y la de (3^m - 1)/2 difieren siempre.
      Total: (2^(m-1) - 1) + 1 = 2^(m-1), sin casos. -/

-- ── 0. potencias positivas (para que las restas de Nat no trunquen) ──
theorem pow_pos (b m : Nat) (h : 1 ≤ b) : 1 ≤ b ^ m := by
  induction m with
  | zero => simp
  | succ n ih => rw [Nat.pow_succ]; exact Nat.le_trans ih (Nat.le_mul_of_pos_right _ h)

-- ── 1. LA SUMA DE VENTANAS ──
def sumaVentanas : Nat → Nat
  | 0 => 0
  | m + 1 => 2 ^ m + sumaVentanas m

theorem ventanas (m : Nat) : sumaVentanas m = 2 ^ m - 1 := by
  induction m with
  | zero => rfl
  | succ n ih =>
      have h1 : 1 ≤ 2 ^ n := pow_pos 2 n (by decide)
      have h2 : 2 ^ (n + 1) = 2 ^ n * 2 := Nat.pow_succ 2 n
      unfold sumaVentanas
      omega

-- ── 2. EL BORDE ALTERNANTE: 3^m mod 4 = 1 si m par, 3 si m impar ──
theorem borde_alterna (m : Nat) :
    3 ^ m % 4 = (if m % 2 = 0 then 1 else 3) := by
  induction m with
  | zero => rfl
  | succ n ih =>
      have h2 : 3 ^ (n + 1) = 3 ^ n * 3 := Nat.pow_succ 3 n
      by_cases h : n % 2 = 0
      · simp [h] at ih
        have : (n + 1) % 2 = 1 := by omega
        simp [this, h2]
        omega
      · simp [h] at ih
        have : (n + 1) % 2 = 0 := by omega
        simp [this, h2]
        omega

-- ── 3. EXACTAMENTE UNO: las paridades de (3^(m-1)-1)/2 y (3^m-1)/2
--      difieren para todo m >= 1 -- cada nivel funde UN solo borde ──
theorem exactamente_uno (m : Nat) (h : 1 ≤ m) :
    (3 ^ (m - 1) - 1) / 2 % 2 ≠ (3 ^ m - 1) / 2 % 2 := by
  have e : m = (m - 1) + 1 := by omega
  have hb1 := borde_alterna (m - 1)
  have hb2 := borde_alterna m
  have hp1 : 1 ≤ 3 ^ (m - 1) := pow_pos 3 (m - 1) (by decide)
  have hp2 : 1 ≤ 3 ^ m := pow_pos 3 m (by decide)
  by_cases hpar : (m - 1) % 2 = 0
  · have hm : m % 2 = 1 := by omega
    simp [hpar] at hb1
    simp [hm] at hb2
    omega
  · have hm : m % 2 = 0 := by omega
    simp [hpar] at hb1
    simp [hm] at hb2
    omega

-- ── el conteo, cerrado: (2^(m-1) - 1) + 1 = 2^(m-1) ──
theorem conteo_perras (m : Nat) (_h : 1 ≤ m) :
    sumaVentanas (m - 1) + 1 = 2 ^ (m - 1) := by
  have h1 : 1 ≤ 2 ^ (m - 1) := pow_pos 2 (m - 1) (by decide)
  rw [ventanas]
  omega

-- ── casos por el nucleo (decide): m = 2 (dos clases: s1 = 1, 2) y los
--    bordes concretos del documento: (3^1-1)/2 = 1 impar (m = 2 funde
--    2^(m-1)-1... el borde 1^(m-1) 0), (3^2-1)/2 = 4 par ──
theorem caso_m2 : sumaVentanas 1 + 1 = 2 := by decide
theorem caso_bordes : (3 ^ 1 - 1) / 2 % 2 = 1 ∧ (3 ^ 2 - 1) / 2 % 2 = 0 := by
  decide

#print axioms ventanas
#print axioms borde_alterna
#print axioms exactamente_uno
#print axioms conteo_perras
