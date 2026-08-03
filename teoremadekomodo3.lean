/- teoremadekomodo3.lean
   EL TEOREMA DE KOMODO 3 (el teorema mod 3 del programa de fusion),
   demostrado en Lean 4.
   (04-08-2026; el sexto .lean del repo. Nucleo puro, sin Mathlib.)

   ENUNCIADO (la version de auditoria_rigor.py R34): tras el paso 0 de
   cualquier par consecutivo (r, r+1) bajo el mapa del atajo
   T(n) = n/2 (par) / (3n+1)/2 (impar), el lado MAYOR del par es
   siempre = 2 (mod 3); y la propiedad "el mayor no es multiplo de 3"
   es INVARIANTE bajo la dinamica compartida.

   COROLARIO (en el .py): D = gap - 2*menor - 1 nunca es = 2 (mod 3)
   en ningun estado posterior al paso 0 - los aterrizajes -4, +8, -16
   y los tramos D = 5, 11, 17 son imposibles para siempre.

   Cuatro piezas, cada una de una linea matematica. -/

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- ── BASE, r PAR: (2s, 2s+1) pasa a (s, 3s+2); el mayor es 3s+2 = 2 (mod 3)
theorem base_par (s : Nat) : (3 * s + 2) % 3 = 2 := by omega

theorem base_par_T (s : Nat) (h : 1 ≤ s) :
    T (2 * s) = s ∧ T (2 * s + 1) = 3 * s + 2 ∧ s < 3 * s + 2 := by
  unfold T
  constructor
  · simp [Nat.mul_mod_right]
  constructor
  · have h2 : (2 * s + 1) % 2 = 1 := by omega
    simp [h2]
    omega
  · omega

-- ── BASE, r IMPAR: (2k+1, 2k+2) pasa a (3k+2, k+1); el mayor es 3k+2
theorem base_impar_T (k : Nat) :
    T (2 * k + 1) = 3 * k + 2 ∧ T (2 * k + 2) = k + 1 ∧ k + 1 ≤ 3 * k + 2 := by
  unfold T
  constructor
  · have h2 : (2 * k + 1) % 2 = 1 := by omega
    simp [h2]
    omega
  constructor
  · have h2 : (2 * k + 2) % 2 = 0 := by omega
    simp [h2]
  · omega

theorem base_impar (k : Nat) : (3 * k + 2) % 3 = 2 := by omega

-- ── INVARIANCIA, paso compartido-par: si l no es multiplo de 3,
--    l/2 tampoco (2*(l/2) = l fuerza el contrarreciproco)
theorem inv_par (l : Nat) (hpar : l % 2 = 0) (h3 : l % 3 ≠ 0) :
    (l / 2) % 3 ≠ 0 := by omega

-- ── INVARIANCIA, paso compartido-impar: (3l+1)/2 = 2 (mod 3), SIEMPRE
--    (l impar: l = 2k+1, (3(2k+1)+1)/2 = 3k+2)
theorem inv_impar (k : Nat) : ((3 * (2 * k + 1) + 1) / 2) % 3 = 2 := by
  have h : (3 * (2 * k + 1) + 1) / 2 = 3 * k + 2 := by omega
  rw [h]
  omega

-- ── Y el empaquetado: el sucesor de un mayor l (no multiplo de 3) bajo
--    cualquiera de las dos ramas de T sigue sin ser multiplo de 3
theorem invariancia (l : Nat) (h3 : l % 3 ≠ 0) : T l % 3 ≠ 0 := by
  unfold T
  by_cases hp : l % 2 = 0
  · simp [hp]
    omega
  · simp [hp]
    omega

-- ── Casos concretos por el nucleo (decide, no #eval): los mayores del
--    programa - 9w+2 y 9w-1 con w=5, y el mayor tras el paso 0 del par
--    (6,7) - son todos = 2 (mod 3), y el 11 = 2 (mod 3) queda prohibido
theorem caso_9w2 : (9 * 5 + 2) % 3 = 2 := by decide
theorem caso_9w1 : (9 * 5 - 1) % 3 = 2 := by decide
theorem caso_par67 : T 7 % 3 = 2 := by decide
theorem caso_D11 : (11 : Nat) % 3 = 2 := by decide

#print axioms base_par_T
#print axioms base_impar_T
#print axioms inv_par
#print axioms inv_impar
#print axioms invariancia
