/-
  A33 — "a(k) >= 1 para todo k: el resto 2^k - 1 sobrevive siempre a la
  criba de Brown/Terras, luego la criba NUNCA se vacia"

  MAPA USADO: el ATAJO  T(n) = n/2 si n par, (3n+1)/2 si n impar.
  (La criba de Brown/Terras se define sobre este mapa: un resto r mod 2^k
   queda ELIMINADO si existe j <= k con 3^(S_j(r)) < 2^j, donde S_j cuenta
   los pasos impares entre las iteradas 0..j-1. SOBREVIVE si para todo
   j <= k vale 2^j <= 3^(S_j(r)).)

  ESTRUCTURA:
    1. T, Titer, S definidos aqui mismo, desde cero.
    2. Casos conocidos comprobados por el nucleo con `decide`
       (trayectoria del 7 y del 31, y los conteos de A076227 a k = 1..6).
    3. Forma cerrada: Titer j (2^(j+d) - 1) = 3^j * 2^d - 1  (induccion).
    4. S_j(2^(j+d) - 1) = j  (todos los pasos son impares).
    5. TEOREMA: 2^k - 1 sobrevive a profundidad k, para TODO k.
    6. COROLARIO: el conjunto de supervivientes mod 2^k nunca es vacio.

  Sin Mathlib. Solo nucleo de Lean 4.
-/

set_option maxRecDepth 40000

namespace A33

/-- El mapa del ATAJO: n/2 si par, (3n+1)/2 si impar. -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- Iterada j-esima de T (Titer (j+1) n = T (Titer j n)). -/
def Titer : Nat → Nat → Nat
  | 0, n => n
  | j+1, n => T (Titer j n)

/-- S j n = cuantas de las iteradas 0 .. j-1 son impares. -/
def S : Nat → Nat → Nat
  | 0, _ => 0
  | j+1, n => S j n + (if Titer j n % 2 = 1 then 1 else 0)

-- ── 2. LA TRAMPA: comprobar que T es el objeto correcto, con casos conocidos ──

-- atajo: 7 -> 11 -> 17 -> 26 -> 13   (tres impares y un par en 4 pasos)
theorem caso_7_pasos : T 7 = 11 ∧ T 11 = 17 ∧ T 17 = 26 ∧ T 26 = 13 := by decide
theorem caso_7_iter  : Titer 4 7 = 13 ∧ S 4 7 = 3 := by decide

-- el testigo del enunciado con k = 5: 31 = 2^5 - 1 sube cinco veces seguidas
-- 31 -> 47 -> 71 -> 107 -> 161 -> 242 = 3^5 * 2^0 - 1
theorem caso_31 : Titer 5 31 = 242 ∧ S 5 31 = 5 := by decide
theorem caso_31_cota : 2 ^ 5 ≤ 3 ^ (S 5 31) := by decide

-- ── lemas de potencias, demostrados a mano (sin Mathlib) ──

theorem pow_ge_one (b j : Nat) (hb : 1 ≤ b) : 1 ≤ b ^ j := by
  induction j with
  | zero => simp
  | succ j ih =>
    rw [Nat.pow_succ]
    have h := Nat.mul_le_mul ih hb
    omega

theorem prod_pos (j d : Nat) : 1 ≤ 3 ^ j * 2 ^ d := by
  have h3 := pow_ge_one 3 j (by decide)
  have h2 := pow_ge_one 2 d (by decide)
  have h := Nat.mul_le_mul h3 h2
  omega

theorem dos_pow_le_tres_pow (j : Nat) : 2 ^ j ≤ 3 ^ j := by
  induction j with
  | zero => decide
  | succ j ih =>
    rw [Nat.pow_succ, Nat.pow_succ]
    exact Nat.mul_le_mul ih (by decide)

/-- Sobre un impar 2m-1 (m >= 1) el atajo da 3m-1. -/
theorem T_impar (m : Nat) (hm : 1 ≤ m) : T (2 * m - 1) = 3 * m - 1 := by
  unfold T
  split
  · omega
  · omega

theorem desdobla (j d : Nat) : 3 ^ j * 2 ^ (d + 1) = 2 * (3 ^ j * 2 ^ d) := by
  rw [Nat.pow_succ, ← Nat.mul_assoc, Nat.mul_comm (3 ^ j * 2 ^ d) 2]

-- ── 3. forma cerrada de la trayectoria de 2^k - 1 ──

/-- Titer j (2^(j+d) - 1) = 3^j * 2^d - 1: cada paso multiplica por 3/2. -/
theorem cerrada : ∀ j d : Nat, Titer j (2 ^ (j + d) - 1) = 3 ^ j * 2 ^ d - 1 := by
  intro j
  induction j with
  | zero =>
    intro d
    show 2 ^ (0 + d) - 1 = 3 ^ 0 * 2 ^ d - 1
    rw [Nat.zero_add, Nat.pow_zero, Nat.one_mul]
  | succ j ih =>
    intro d
    show T (Titer j (2 ^ (j + 1 + d) - 1)) = 3 ^ (j + 1) * 2 ^ d - 1
    have he : j + 1 + d = j + (d + 1) := by omega
    rw [he, ih (d + 1), desdobla j d, T_impar (3 ^ j * 2 ^ d) (prod_pos j d)]
    -- queda: 3 * (3^j * 2^d) - 1 = 3^(j+1) * 2^d - 1
    have h5 : 3 * (3 ^ j * 2 ^ d) = 3 ^ (j + 1) * 2 ^ d := by
      rw [Nat.pow_succ, Nat.mul_comm (3 ^ j) 3, Nat.mul_assoc]
    rw [h5]

-- ── 4. todos los pasos de 2^k - 1 son impares mientras j <= k ──

theorem S_todos_impares : ∀ j d : Nat, S j (2 ^ (j + d) - 1) = j := by
  intro j
  induction j with
  | zero => intro d; rfl
  | succ j ih =>
    intro d
    show S j (2 ^ (j + 1 + d) - 1)
         + (if Titer j (2 ^ (j + 1 + d) - 1) % 2 = 1 then 1 else 0) = j + 1
    have he : j + 1 + d = j + (d + 1) := by omega
    rw [he, ih (d + 1), cerrada j (d + 1)]
    have hodd : (3 ^ j * 2 ^ (d + 1) - 1) % 2 = 1 := by
      have h2 := desdobla j d
      have hm := prod_pos j d
      omega
    rw [hodd]
    simp

-- ── 5. la criba, y el teorema ──

/-- Un resto r sobrevive a la criba de Brown/Terras a profundidad k si en
    ningun j <= k el coeficiente 3^(S_j)/2^j cae por debajo de 1. -/
def sobrevive (k r : Nat) : Prop := ∀ j, j ≤ k → 2 ^ j ≤ 3 ^ (S j r)

/-- EL TEOREMA A33: el resto 2^k - 1 sobrevive a profundidad k, para TODO k. -/
theorem resto_sobrevive (k : Nat) : sobrevive k (2 ^ k - 1) := by
  intro j hj
  have hex : ∃ d, k = j + d := ⟨k - j, by omega⟩
  cases hex with
  | intro d hd =>
    rw [hd, S_todos_impares j d]
    exact dos_pow_le_tres_pow j

-- ── 6. corolario: la criba nunca se vacia (a(k) >= 1) ──

theorem criba_no_vacia (k : Nat) : ∃ r, r < 2 ^ k ∧ sobrevive k r := by
  refine ⟨2 ^ k - 1, ?_, resto_sobrevive k⟩
  have h := pow_ge_one 2 k (by decide)
  omega

-- ── cruce contra lo conocido: los conteos de A076227 a escala chica ──
-- (version booleana de la MISMA condicion, contada por el nucleo con decide)

def sobreviveB (k r : Nat) : Bool :=
  (List.range (k + 1)).all (fun j => decide (2 ^ j ≤ 3 ^ (S j r)))

-- el testigo del enunciado esta entre los supervivientes, comprobado directo:
theorem testigo_k3 : sobreviveB 3 7 = true := by decide
theorem testigo_k6 : sobreviveB 6 63 = true := by decide

-- conteos de supervivientes mod 2^k, k = 1..6: deben dar 1, 1, 2, 3, 4, 8
-- (los valores de A076227, que el repo tiene cruzados contra el b-file de OEIS)
theorem conteo_k1 : ((List.range 2).filter (fun r => sobreviveB 1 r)).length = 1 := by decide
theorem conteo_k2 : ((List.range 4).filter (fun r => sobreviveB 2 r)).length = 1 := by decide
theorem conteo_k3 : ((List.range 8).filter (fun r => sobreviveB 3 r)).length = 2 := by decide
theorem conteo_k4 : ((List.range 16).filter (fun r => sobreviveB 4 r)).length = 3 := by decide
theorem conteo_k5 : ((List.range 32).filter (fun r => sobreviveB 5 r)).length = 4 := by decide
theorem conteo_k6 : ((List.range 64).filter (fun r => sobreviveB 6 r)).length = 8 := by decide

-- ── bordes ──
-- k = 0: 2^0 - 1 = 0, sobrevive trivialmente (solo j = 0, 1 <= 1)
theorem borde_k0 : sobrevive 0 (2 ^ 0 - 1) := resto_sobrevive 0
-- k = 1: el resto 1 mod 2
theorem borde_k1 : sobrevive 1 (2 ^ 1 - 1) := resto_sobrevive 1
-- un resto PAR no sobrevive ya en j = 1 (S_1 = 0, y 2 > 1): la criba muerde
theorem par_no_sobrevive : ¬ sobrevive 1 4 := by
  intro h
  have h1 := h 1 (Nat.le_refl 1)
  revert h1
  decide

-- ── control de axiomas ──
#print axioms resto_sobrevive
#print axioms criba_no_vacia
#print axioms S_todos_impares
#print axioms cerrada
#print axioms caso_31
#print axioms conteo_k6
#print axioms par_no_sobrevive

end A33
