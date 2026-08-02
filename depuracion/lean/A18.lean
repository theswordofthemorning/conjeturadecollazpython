/-
  A18.lean  —  AGENTE 1 (LEAN) del trio de verificacion

  ENUNCIADO LITERAL (afirmaciones.db, item A18):
    "los primeros k pasos de cualquier numero los decide n mod 2^k"

  INTERPRETACION FORMALIZADA (mapa y cuantificador explicitos):
    Para TODO k >= 0 y todos n, m naturales:
      n % 2^k = m % 2^k  ->  el vector de paridad de los primeros k pasos
      (es decir, QUE regla se aplica en cada uno de los k primeros pasos)
      es identico para n y para m.
    "Paso" = una aplicacion del mapa. "Decidir el paso" = decidir la paridad
    del numero en ese instante, que es lo que elige la rama.

  SE DEMUESTRA PARA LOS DOS MAPAS, escritos aqui desde cero:
      clasico:  n/2 si par,  3n+1 si impar
      atajo:    n/2 si par,  (3n+1)/2 si impar
  (el mapa 3n-1 no es objeto del enunciado; el enunciado de la base cita
   Terras 1976 / Everett 1977, que son sobre 3n+1)

  Nucleo de Lean 4 solamente, sin Mathlib, sin sorry.
-/

set_option maxRecDepth 40000

-- ==================== los mapas, definidos aqui mismo ====================

def pasoC (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1
def pasoA (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- vector de paridad de los primeros k pasos (la sucesion de ramas tomadas)
def vecC : Nat → Nat → List Nat
  | 0, _ => []
  | k+1, n => n % 2 :: vecC k (pasoC n)

def vecA : Nat → Nat → List Nat
  | 0, _ => []
  | k+1, n => n % 2 :: vecA k (pasoA n)

def iterC : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => iterC k (pasoC n)

def iterA : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => iterA k (pasoA n)

-- ========== LA TRAMPA DE LEAN: comprobar que el objeto es Collatz ==========
-- casos conocidos, por el NUCLEO (decide), no por #eval

-- clasico, 27: 27 -> 82 -> 41 -> 124 -> 62 -> 31 -> 94
theorem control_iter_clasico : iterC 6 27 = 94 := by decide
-- clasico, 6: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2  (paridades 0,1,0,1,0,0,0,0)
theorem control_vec_clasico : vecC 8 6 = [0,1,0,1,0,0,0,0] := by decide
-- atajo, 27: 27 -> 41 -> 62 -> 31 -> 47 -> 71 -> 107
theorem control_iter_atajo : iterA 6 27 = 107 := by decide
theorem control_vec_atajo : vecA 6 27 = [1,1,0,1,1,1] := by decide

-- ==================== lemas de UN paso ====================
-- sumar 2*M no cambia la paridad
theorem paridad_estable (n M : Nat) : (n + 2 * M) % 2 = n % 2 := by omega

-- atajo, rama par: el desplazamiento 2M se convierte en M
theorem pasoA_par (n M : Nat) (h : n % 2 = 0) :
    pasoA (n + 2 * M) = pasoA n + M := by
  unfold pasoA
  rw [if_pos (show (n + 2 * M) % 2 = 0 by omega), if_pos h]
  omega

-- atajo, rama impar: el desplazamiento 2M se convierte en 3M
theorem pasoA_impar (n M : Nat) (h : n % 2 = 1) :
    pasoA (n + 2 * M) = pasoA n + 3 * M := by
  unfold pasoA
  rw [if_neg (show ¬(n + 2 * M) % 2 = 0 by omega),
      if_neg (show ¬n % 2 = 0 by omega)]
  omega

-- clasico, rama par: 2M -> M
theorem pasoC_par (n M : Nat) (h : n % 2 = 0) :
    pasoC (n + 2 * M) = pasoC n + M := by
  unfold pasoC
  rw [if_pos (show (n + 2 * M) % 2 = 0 by omega), if_pos h]
  omega

-- clasico, rama impar: 2M -> 6M (no divide, y multiplica por 3)
theorem pasoC_impar (n M : Nat) (h : n % 2 = 1) :
    pasoC (n + 2 * M) = pasoC n + 6 * M := by
  unfold pasoC
  rw [if_neg (show ¬(n + 2 * M) % 2 = 0 by omega),
      if_neg (show ¬n % 2 = 0 by omega)]
  omega

-- ============ reordenaciones (sin Mathlib no hay ring) ============
theorem pow_succ_dos (k t : Nat) : 2^(k+1) * t = 2 * (2^k * t) := by
  have e : (2:Nat)^(k+1) = 2^k * 2 := rfl
  rw [e, Nat.mul_comm (2^k) 2, Nat.mul_assoc]

theorem saca_tres (k t : Nat) : 3 * (2^k * t) = 2^k * (3 * t) := by
  rw [← Nat.mul_assoc, Nat.mul_comm 3 (2^k), Nat.mul_assoc]

theorem saca_seis (k t : Nat) : 6 * (2^k * t) = 2^k * (6 * t) := by
  rw [← Nat.mul_assoc, Nat.mul_comm 6 (2^k), Nat.mul_assoc]

theorem vecA_succ (k n : Nat) : vecA (k+1) n = n % 2 :: vecA k (pasoA n) := rfl
theorem vecC_succ (k n : Nat) : vecC (k+1) n = n % 2 :: vecC k (pasoC n) := rfl

-- ==================== EL TEOREMA, forma aditiva ====================
-- sumar cualquier multiplo de 2^k no cambia los primeros k pasos

theorem atajo_suma (k : Nat) : ∀ n t, vecA k (n + 2^k * t) = vecA k n := by
  induction k with
  | zero => intro n t; rfl
  | succ k ih =>
    intro n t
    show vecA (k+1) (n + 2^(k+1) * t) = vecA (k+1) n
    rw [vecA_succ, vecA_succ, pow_succ_dos, paridad_estable]
    by_cases hn : n % 2 = 0
    · rw [pasoA_par n (2^k * t) hn, ih]
    · rw [pasoA_impar n (2^k * t) (by omega), saca_tres, ih]

theorem clasico_suma (k : Nat) : ∀ n t, vecC k (n + 2^k * t) = vecC k n := by
  induction k with
  | zero => intro n t; rfl
  | succ k ih =>
    intro n t
    show vecC (k+1) (n + 2^(k+1) * t) = vecC (k+1) n
    rw [vecC_succ, vecC_succ, pow_succ_dos, paridad_estable]
    by_cases hn : n % 2 = 0
    · rw [pasoC_par n (2^k * t) hn, ih]
    · rw [pasoC_impar n (2^k * t) (by omega), saca_seis, ih]

-- ==================== EL TEOREMA, forma de congruencia ====================
-- (el enunciado literal: "los decide n mod 2^k")

theorem vecA_mod (k n : Nat) : vecA k n = vecA k (n % 2^k) := by
  have h : n % 2^k + 2^k * (n / 2^k) = n := Nat.mod_add_div n (2^k)
  have e := atajo_suma k (n % 2^k) (n / 2^k)
  rw [h] at e
  exact e

theorem vecC_mod (k n : Nat) : vecC k n = vecC k (n % 2^k) := by
  have h : n % 2^k + 2^k * (n / 2^k) = n := Nat.mod_add_div n (2^k)
  have e := clasico_suma k (n % 2^k) (n / 2^k)
  rw [h] at e
  exact e

/-- A18, mapa del ATAJO: n ≡ m (mod 2^k) obliga a los mismos k primeros pasos -/
theorem A18_atajo (k n m : Nat) (h : n % 2^k = m % 2^k) :
    vecA k n = vecA k m := by
  rw [vecA_mod k n, vecA_mod k m, h]

/-- A18, mapa CLASICO: n ≡ m (mod 2^k) obliga a los mismos k primeros pasos -/
theorem A18_clasico (k n m : Nat) (h : n % 2^k = m % 2^k) :
    vecC k n = vecC k m := by
  rw [vecC_mod k n, vecC_mod k m, h]

-- ==================== instancias concretas, por el nucleo ====================
-- 251 = 27 + 2^5 * 7 : mismos 5 primeros pasos del atajo
theorem instancia_atajo : vecA 5 27 = vecA 5 251 := by decide
-- 411 = 27 + 2^7 * 3 : mismos 7 primeros pasos del clasico
theorem instancia_clasico : vecC 7 27 = vecC 7 411 := by decide

-- ==================== controles de ajuste (que 2^k no sobra) ====================
-- 1 ≡ 3 (mod 2), pero ya el SEGUNDO paso del atajo difiere:
-- o sea, n mod 2^1 NO decide 2 pasos — el modulo tiene que crecer con k
theorem ajuste_atajo : vecA 2 1 ≠ vecA 2 3 := by decide
-- 1 ≡ 3 (mod 2): en el clasico difieren al tercer paso
theorem ajuste_clasico : vecC 3 1 ≠ vecC 3 3 := by decide

-- ==================== bordes ====================
-- k = 0: el enunciado es trivialmente cierto (vector vacio); compila arriba
--        porque A18_* no exige k >= 1.
theorem borde_k0 : vecA 0 5 = vecA 0 999 := by decide
-- n = 0 y n = 2^k - 1 (los dos extremos del bloque de restos):
theorem borde_cero : vecA 4 0 = vecA 4 16 := by decide
theorem borde_tope : vecA 4 15 = vecA 4 31 := by decide

#print axioms A18_atajo
#print axioms A18_clasico
#print axioms atajo_suma
#print axioms clasico_suma
#print axioms instancia_atajo
#print axioms instancia_clasico
#print axioms control_iter_clasico
#print axioms control_vec_clasico
#print axioms control_iter_atajo
#print axioms ajuste_atajo
#print axioms borde_tope
