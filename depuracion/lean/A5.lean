/-
  ITEM A5 - "eps > 0 siempre, y vale 0 exactamente en las potencias de 2"

  MAPA: CLASICO (par -> n/2, impar -> 3n+1), definido aqui mismo.
  En forma entera, sin logaritmos:  eps = ln(2^B / (3^A n))  sobre la
  trayectoria completa de n hasta el PRIMER 1, o sea

     eps >= 0   <=>   3^A * n <= 2^B      (Res(n) >= 1)
     eps  = 0   <=>   3^A * n  = 2^B      <=>   A = 0   <=>   n = 2^m

  Lo que se demuestra abajo, todo condicionado a "iter k n = 1" (la
  trayectoria LLEGA al 1, que es lo que 'trayectoria completa' presupone):

   1. cota                : 3^A n <= 2^B * iter k n   (para todo n>=1, todo k)
   2. res_ge_uno          : si iter k n = 1, entonces 3^A n <= 2^B   (eps >= 0)
   3. eps_estrictamente_pos: si ademas A >= 1, entonces 3^A n < 2^B  (eps > 0)
   4. igualdad_solo_potencias: si 3^A n = 2^B entonces n = 2^B (potencia de 2)
   5. potencias_dan_igualdad : para n = 2^m, en su primera llegada (k = m),
                               A = 0, B = m y la igualdad es exacta (eps = 0)
   6. contraejemplo_literal  : n = 4 refuta el literal "eps > 0 SIEMPRE"
-/
set_option maxRecDepth 40000

-- EL MAPA CLASICO, escrito aqui, sin mirar ningun fichero del repo
def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

def iter : Nat → Nat → Nat
  | 0,     n => n
  | k + 1, n => iter k (paso n)

-- A = pasos impares (3n+1), B = pasos pares (n/2), en k pasos desde n
def cA : Nat → Nat → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 0 else 1) + cA k (paso n)

def cB : Nat → Nat → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 1 else 0) + cB k (paso n)

-- LA TRAMPA: comprobar que el mapa es el clasico de verdad (nucleo, no #eval)
theorem mapa_es_clasico : paso 6 = 3 ∧ paso 3 = 10 ∧ paso 10 = 5 ∧ paso 1 = 4 := by
  decide

theorem paso_pos {n : Nat} (h : 1 ≤ n) : 1 ≤ paso n := by
  unfold paso; split <;> omega

-- ayudantes de monotonia (solo nucleo)
theorem ayuda_par {x y z m : Nat} (h : x * m ≤ y * z) :
    x * (2 * m) ≤ y * 2 * z := by
  have h1 : 2 * (x * m) ≤ 2 * (y * z) := Nat.mul_le_mul_left 2 h
  calc x * (2 * m) = 2 * (x * m) := Nat.mul_left_comm x 2 m
    _ ≤ 2 * (y * z) := h1
    _ = y * 2 * z := by rw [← Nat.mul_assoc, Nat.mul_comm 2 y]

theorem ayuda_par_lt {x y z m : Nat} (h : x * m < y * z) :
    x * (2 * m) < y * 2 * z := by
  have h1 : 2 * (x * m) < 2 * (y * z) := (Nat.mul_lt_mul_left (by omega)).mpr h
  calc x * (2 * m) = 2 * (x * m) := Nat.mul_left_comm x 2 m
    _ < 2 * (y * z) := h1
    _ = y * 2 * z := by rw [← Nat.mul_assoc, Nat.mul_comm 2 y]

-- el paso impar es ESTRICTO: ahi nace el eps > 0 (el +1 de 3n+1)
theorem ayuda_impar {x y z n : Nat} (hx : 0 < x) (h : x * (3 * n + 1) ≤ y * z) :
    x * 3 * n < y * z := by
  have h1 : x * (3 * n) < x * (3 * n + 1) :=
    (Nat.mul_lt_mul_left hx).mpr (by omega)
  rw [Nat.mul_assoc]
  exact Nat.lt_of_lt_of_le h1 h

-- 1. LA COTA: 3^A * n <= 2^B * (valor alcanzado), para TODO n >= 1 y TODO k
theorem cota : ∀ (k n : Nat), 1 ≤ n → 3 ^ cA k n * n ≤ 2 ^ cB k n * iter k n := by
  intro k
  induction k with
  | zero => intro n _; simp [cA, cB, iter]
  | succ k ih =>
    intro n h
    by_cases hp : n % 2 = 0
    · have hex : ∃ m, n = 2 * m := ⟨n / 2, by omega⟩
      cases hex with
      | intro m hm =>
        subst hm
        have h2 : (2 * m) % 2 = 0 := by omega
        have h3 : (2 * m) / 2 = m := by omega
        have hpaso : paso (2 * m) = m := by unfold paso; rw [if_pos h2]; exact h3
        have ih' := ih m (by omega)
        simp [cA, cB, iter, h2, hpaso]
        rw [Nat.add_comm 1 (cB k m), Nat.pow_succ]
        exact ayuda_par ih'
    · have hpaso : paso n = 3 * n + 1 := by unfold paso; rw [if_neg hp]
      have ih' := ih (3 * n + 1) (by omega)
      simp [cA, cB, iter, hp, hpaso]
      rw [Nat.add_comm 1 (cA k (3 * n + 1)), Nat.pow_succ]
      exact Nat.le_of_lt (ayuda_impar (Nat.pow_pos (by omega)) ih')

-- version ESTRICTA: con al menos un paso impar, la desigualdad es estricta
theorem cota_lt : ∀ (k n : Nat), 1 ≤ n → 1 ≤ cA k n →
    3 ^ cA k n * n < 2 ^ cB k n * iter k n := by
  intro k
  induction k with
  | zero => intro n _ hA; simp [cA] at hA
  | succ k ih =>
    intro n h hA
    by_cases hp : n % 2 = 0
    · have hex : ∃ m, n = 2 * m := ⟨n / 2, by omega⟩
      cases hex with
      | intro m hm =>
        subst hm
        have h2 : (2 * m) % 2 = 0 := by omega
        have h3 : (2 * m) / 2 = m := by omega
        have hpaso : paso (2 * m) = m := by unfold paso; rw [if_pos h2]; exact h3
        have hA' : 1 ≤ cA k m := by simp [cA, h2, hpaso] at hA; exact hA
        have ih' := ih m (by omega) hA'
        simp [cA, cB, iter, h2, hpaso]
        rw [Nat.add_comm 1 (cB k m), Nat.pow_succ]
        exact ayuda_par_lt ih'
    · have hpaso : paso n = 3 * n + 1 := by unfold paso; rw [if_neg hp]
      have hc := cota k (3 * n + 1) (by omega)
      simp [cA, cB, iter, hp, hpaso]
      rw [Nat.add_comm 1 (cA k (3 * n + 1)), Nat.pow_succ]
      exact ayuda_impar (Nat.pow_pos (by omega)) hc

-- 2. eps >= 0 sobre la trayectoria completa (llega al 1)
theorem res_ge_uno (n k : Nat) (h : 1 ≤ n) (hfin : iter k n = 1) :
    3 ^ cA k n * n ≤ 2 ^ cB k n := by
  have hc := cota k n h
  rw [hfin, Nat.mul_one] at hc
  exact hc

-- 3. eps > 0 en cuanto hay UN paso impar
theorem eps_estrictamente_pos (n k : Nat) (h : 1 ≤ n) (hfin : iter k n = 1)
    (hA : 1 ≤ cA k n) : 3 ^ cA k n * n < 2 ^ cB k n := by
  have hc := cota_lt k n h hA
  rw [hfin, Nat.mul_one] at hc
  exact hc

-- 4. si eps = 0 entonces A = 0 y n ES una potencia de 2 (n = 2^B)
theorem igualdad_solo_potencias (n k : Nat) (h : 1 ≤ n) (hfin : iter k n = 1)
    (heq : 3 ^ cA k n * n = 2 ^ cB k n) : n = 2 ^ cB k n := by
  by_cases hA : 1 ≤ cA k n
  · exact absurd heq (Nat.ne_of_lt (eps_estrictamente_pos n k h hfin hA))
  · have h0 : cA k n = 0 := by omega
    rw [h0, Nat.pow_zero, Nat.one_mul] at heq
    exact heq

-- 5. toda potencia de 2 llega al 1 en m pasos, con A = 0, B = m
theorem potencias_dan_igualdad : ∀ m : Nat,
    iter m (2 ^ m) = 1 ∧ cA m (2 ^ m) = 0 ∧ cB m (2 ^ m) = m := by
  intro m
  induction m with
  | zero => decide
  | succ m ih =>
    have h2 : 2 ^ (m + 1) % 2 = 0 := by rw [Nat.pow_succ]; omega
    have h3 : paso (2 ^ (m + 1)) = 2 ^ m := by
      unfold paso; rw [if_pos h2, Nat.pow_succ]; omega
    refine ⟨?_, ?_, ?_⟩
    · simp [iter, h3]; exact ih.1
    · simp [cA, h2, h3]; exact ih.2.1
    · have hb : cB (m + 1) (2 ^ (m + 1)) = 1 + cB m (2 ^ m) := by
        simp [cB, h2, h3]
      rw [hb, ih.2.2]; omega

-- ... y en esa primera llegada la igualdad es EXACTA: eps = 0
theorem potencia_eps_cero (m : Nat) :
    3 ^ cA m (2 ^ m) * 2 ^ m = 2 ^ cB m (2 ^ m) := by
  have h := potencias_dan_igualdad m
  rw [h.2.1, h.2.2, Nat.pow_zero, Nat.one_mul]

-- 6. EL LITERAL "eps > 0 siempre" ES FALSO: n = 4 da eps = 0 exacto
theorem contraejemplo_literal :
    iter 2 4 = 1 ∧ cA 2 4 = 0 ∧ cB 2 4 = 2 ∧ 3 ^ cA 2 4 * 4 = 2 ^ cB 2 4 := by
  decide

-- casos conocidos, comprobados por el NUCLEO (by decide, no #eval)
-- 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 : 7 pasos, A=2, B=5, 27 < 32
theorem caso_3 : iter 7 3 = 1 ∧ cA 7 3 = 2 ∧ cB 7 3 = 5 ∧ 3 ^ 2 * 3 < 2 ^ 5 := by
  decide
-- 7: 16 pasos, A=5, B=11, 3^5*7 = 1701 < 2048 = 2^11
theorem caso_7 : iter 16 7 = 1 ∧ cA 16 7 = 5 ∧ cB 16 7 = 11 ∧ 3 ^ 5 * 7 < 2 ^ 11 := by
  decide
-- 16 = 2^4: A=0, B=4, igualdad exacta
theorem caso_16 : iter 4 16 = 1 ∧ cA 4 16 = 0 ∧ cB 4 16 = 4 ∧ 3 ^ 0 * 16 = 2 ^ 4 := by
  decide
-- el 27, 111 pasos clasicos: eps > 0 comprobado por el nucleo
theorem caso_27 : iter 111 27 = 1 ∧ 3 ^ cA 111 27 * 27 < 2 ^ cB 111 27 := by
  decide
-- AVISO de enunciado fino: si se sigue MAS ALLA del primer 1 (aqui n=4 con
-- k=5, dando la vuelta al ciclo 4-2-1), eps deja de ser 0 incluso en una
-- potencia de 2. "eps = 0 en potencias de 2" es sobre la PRIMERA llegada.
theorem aviso_primera_llegada :
    iter 5 4 = 1 ∧ cA 5 4 = 1 ∧ cB 5 4 = 4 ∧ 3 ^ 1 * 4 < 2 ^ 4 := by
  decide

#print axioms cota
#print axioms cota_lt
#print axioms res_ge_uno
#print axioms eps_estrictamente_pos
#print axioms igualdad_solo_potencias
#print axioms potencias_dan_igualdad
#print axioms potencia_eps_cero
#print axioms contraejemplo_literal
#print axioms caso_27
#print axioms aviso_primera_llegada
