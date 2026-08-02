-- A16: el espejo base 2 de UN paso del mapa CLASICO de Collatz.
-- Enunciado de la ficha: T(2^k - n) = 3*2^k + 2 - T(n), "en los impares
-- casi conmuta, pero sobra un +2". Cuantificador declarado: todo_n.
--
-- MAPA: el CLASICO (n par -> n/2, n impar -> 3n+1). Lo defino yo mismo abajo
-- y lo compruebo contra una trayectoria conocida antes de usarlo.

set_option maxRecDepth 40000

-- El mapa clasico, escrito desde cero.
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

-- LA TRAMPA DE LEAN: comprobar que T es Collatz de verdad, con casos
-- conocidos, como TEOREMA por decide (no #eval).
-- Trayectoria del 6: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1,
-- mas el arranque del 27: 27 -> 82 -> 41.
theorem T_es_collatz :
    T 6 = 3 ∧ T 3 = 10 ∧ T 10 = 5 ∧ T 5 = 16 ∧ T 16 = 8 ∧
    T 8 = 4 ∧ T 4 = 2 ∧ T 2 = 1 ∧ T 1 = 4 ∧
    T 27 = 82 ∧ T 82 = 41 := by decide

-- EL TEOREMA, con las hipotesis que el enunciado necesita y no escribia
-- todas: n IMPAR (la ficha lo dice en prosa), k >= 1 (NO lo dice, y k = 0
-- falla, ver contraejemplo abajo) y n < 2^k para que la resta de Nat no
-- trunque (sobre Z no haria falta; ver nota al final).
theorem espejo_un_paso (k n : Nat) (hk : 1 ≤ k) (himpar : n % 2 = 1)
    (hlt : n < 2 ^ k) : T (2 ^ k - n) = 3 * 2 ^ k + 2 - T n := by
  cases k with
  | zero => omega
  | succ m =>
    have hp : 2 ^ (m + 1) = 2 * 2 ^ m := by
      rw [Nat.pow_succ, Nat.mul_comm]
    rw [hp] at hlt ⊢
    unfold T
    have hmod : (2 * 2 ^ m - n) % 2 = 1 := by omega
    rw [hmod, himpar]
    simp
    omega

#print axioms espejo_un_paso

-- Un caso concreto del teorema, cerrado por el nucleo:
-- k = 5, n = 13:  T(32-13) = T(19) = 58  y  3*32 + 2 - T(13) = 98 - 40 = 58.
theorem caso_k5_n13 : T (2 ^ 5 - 13) = 3 * 2 ^ 5 + 2 - T 13 := by decide

-- Y el caso del repo, con numeros mas grandes: k = 8, n = 221 (impar, < 256):
-- T(256-221) = T(35) = 106  y  3*256 + 2 - T(221) = 770 - 664 = 106.
theorem caso_k8_n221 : T (2 ^ 8 - 221) = 3 * 2 ^ 8 + 2 - T 221 := by decide

-- CONTRAEJEMPLO 1: k = 0 rompe el enunciado (n = 1, impar).
-- T(1-1) = T(0) = 0  pero  3*1 + 2 - T(1) = 5 - 4 = 1.
theorem contraejemplo_k0 : T (2 ^ 0 - 1) ≠ 3 * 2 ^ 0 + 2 - T 1 := by decide

-- CONTRAEJEMPLO 2: n PAR rompe el enunciado (el "todo_n" de la base es
-- falso al pie de la letra). n = 2, k = 2:
-- T(4-2) = T(2) = 1  pero  3*4 + 2 - T(2) = 14 - 1 = 13.
theorem contraejemplo_n_par : T (2 ^ 2 - 2) ≠ 3 * 2 ^ 2 + 2 - T 2 := by decide

-- CONTRAEJEMPLO 3: al SEGUNDO paso la identidad ya no itera, como dice la
-- nota de la ficha. n = 13, k = 5:
-- T(T(32-13)) = T(58) = 29  pero  3*32 + 2 - T(T(13)) = 98 - 20 = 78.
theorem no_itera : T (T (2 ^ 5 - 13)) ≠ 3 * 2 ^ 5 + 2 - T (T 13) := by decide

#print axioms T_es_collatz
#print axioms caso_k5_n13
#print axioms caso_k8_n221
#print axioms contraejemplo_k0
#print axioms contraejemplo_n_par
#print axioms no_itera

-- NOTA sobre n > 2^k: en Nat las dos restas truncan a 0 y la igualdad "se
-- cumple" vacuamente (0 = 0); sobre Z la identidad vale de verdad para TODO
-- n impar (tambien negativo) con k >= 1, porque 2^k - n sigue siendo impar y
-- el algebra es la misma. La hipotesis n < 2^k es del tipo Nat, no del
-- fenomeno.
