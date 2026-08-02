/-
  A34 — "los supervivientes de la criba tienen densidad -> 0 pero cardinal -> infinito,
         del orden de 2^(0,95k). La criba compra densidad, no compra cobertura"

  MAPA USADO: el ATAJO de Terras  T(n) = n/2 si n par, (3n+1)/2 si n impar.
  (La criba de descenso / A076227 se define sobre este mapa.)

  La criba: la clase r mod 2^k queda DESCARTADA si en algun j <= k el coeficiente
  3^{s_j} < 2^j (descenso garantizado). SOBREVIVE si 3^{s_j} >= 2^j para todo j <= k.

  Se demuestra (nucleo, sin Mathlib, sin sorry):
   1. cerrada / nunca_baja : trayectoria de 2^k - 1 en forma cerrada; no baja en k pasos
      (para TODO k, por induccion).
   2. criba_impares / criba_nunca_vacia : para TODO k el resto 2^k - 1 sobrevive
      => los supervivientes NUNCA se vacian.
   3. cuenta_pos : para TODO k, cuenta k >= 1  (cardinal por nivel >= 1).
   4. por `decide` (kernel, no #eval): trayectoria del 7; a(1)..a(13); densidad no
      creciente y cardinal no decreciente en 1..13; y a(12)*9 <= 2^11, o sea a(12)
      esta mas de un orden por debajo de 2^(0.95*12).
-/
set_option maxRecDepth 40000

/-- El mapa del ATAJO. -/
def T (n : Nat) : Nat := if n % 2 = 1 then (3*n+1)/2 else n/2

/-- j iteraciones de T. -/
def iterT : Nat → Nat → Nat
  | 0, n => n
  | j+1, n => T (iterT j n)

/-- La criba de descenso: pasos restantes, valor actual (solo se usa su paridad),
    c3 = 3^{impares vistos}, c2 = 2^{pasos dados}. Descarta si c3 < c2 en algun paso. -/
def criba : Nat → Nat → Nat → Nat → Bool
  | 0, _, _, _ => true
  | j+1, x, c3, c2 =>
    if x % 2 = 1 then
      if 3*c3 < 2*c2 then false else criba j (T x) (3*c3) (2*c2)
    else
      if c3 < 2*c2 then false else criba j (T x) c3 (2*c2)

/-- Sobrevive la clase r mod 2^k a la criba de k pasos? -/
def sobrevive (k r : Nat) : Bool := criba k r 1 1

/-- Cuantos restos < n sobreviven a la criba de k pasos. -/
def cuentaAux (k : Nat) : Nat → Nat
  | 0 => 0
  | r+1 => (if sobrevive k r = true then 1 else 0) + cuentaAux k r

/-- a(k): supervivientes mod 2^k. -/
def cuenta (k : Nat) : Nat := cuentaAux k (2^k)

/- ------------------------------------------------------------------ -/
/- 0. El mapa es el que se cree: caso conocido, comprobado por el KERNEL.
   Trayectoria del 7 con el atajo: 7,11,17,26,13,20,10,5,8,4,2,1
   (tiempo de parada 7: el primer valor < 7 es el 5, en el paso 7).    -/

theorem caso_7 :
    iterT 1 7 = 11 ∧ iterT 4 7 = 13 ∧ iterT 7 7 = 5 ∧ iterT 11 7 = 1 ∧
    T 7 = 11 ∧ T 8 = 4 := by decide

/- ------------------------------------------------------------------ -/
/- 1. Un paso impar, en general -/

theorem T_impar (t : Nat) (ht : 1 ≤ t) : T (2*t - 1) = 3*t - 1 := by
  have h1 : (2*t - 1) % 2 = 1 := by omega
  unfold T
  rw [if_pos h1]
  omega

/- 2. Forma cerrada: T^j(2^k - 1) = 3^j * 2^(k-j) - 1  para j <= k -/

theorem cerrada (k : Nat) : ∀ j, j ≤ k → iterT j (2^k - 1) = 3^j * 2^(k-j) - 1 := by
  intro j
  induction j with
  | zero =>
    intro _
    simp [iterT]
  | succ j ih =>
    intro hjk
    have hj : j ≤ k := Nat.le_of_succ_le hjk
    have hkj : k - j = (k - (j+1)) + 1 := by omega
    have ht : 1 ≤ 3^j * 2^(k-(j+1)) :=
      Nat.mul_pos (Nat.pow_pos (by omega)) (Nat.pow_pos (by omega))
    have hx : iterT j (2^k - 1) = 2 * (3^j * 2^(k-(j+1))) - 1 := by
      rw [ih hj, hkj, Nat.pow_succ]
      have hac : 3^j * (2^(k-(j+1)) * 2) = 2 * (3^j * 2^(k-(j+1))) := by
        simp [Nat.mul_comm, Nat.mul_assoc]
      rw [hac]
    have hT : T (2 * (3^j * 2^(k-(j+1))) - 1) = 3 * (3^j * 2^(k-(j+1))) - 1 :=
      T_impar _ ht
    have hA : 3 * (3^j * 2^(k-(j+1))) = 3^(j+1) * 2^(k-(j+1)) := by
      rw [Nat.pow_succ]
      simp [Nat.mul_comm, Nat.mul_left_comm]
    simp only [iterT]
    rw [hx, hT, hA]

/- 3. COTA, para TODO k: la trayectoria de 2^k - 1 nunca baja de su inicio
      durante los primeros k pasos. -/

theorem nunca_baja (k : Nat) : ∀ j, j ≤ k → 2^k - 1 ≤ iterT j (2^k - 1) := by
  intro j hj
  rw [cerrada k j hj]
  have h1 : 2^k ≤ 3^j * 2^(k-j) := by
    have e : (2:Nat)^k = 2^j * 2^(k-j) := by
      rw [← Nat.pow_add]
      congr 1
      omega
    rw [e]
    exact Nat.mul_le_mul_right _ (Nat.pow_le_pow_left (by omega) j)
  omega

/- 4. LA CRIBA NUNCA SE VACIA, para TODO k:
      un numero de la forma 2^j * t - 1 (t >= 1) da j pasos impares seguidos,
      y en cada uno el coeficiente 3^s / 2^j no baja de 1. -/

theorem criba_impares : ∀ (j t c3 c2 : Nat), 1 ≤ t → c2 ≤ c3 →
    criba j (2^j * t - 1) c3 c2 = true := by
  intro j
  induction j with
  | zero => intro t c3 c2 _ _; rfl
  | succ j ih =>
    intro t c3 c2 ht hc
    have ht2 : 1 ≤ 2^j * t := Nat.mul_pos (Nat.pow_pos (by omega)) ht
    have hx : 2^(j+1) * t - 1 = 2 * (2^j * t) - 1 := by
      rw [Nat.pow_succ]
      have hac : 2^j * 2 * t = 2 * (2^j * t) := by
        simp [Nat.mul_comm, Nat.mul_left_comm]
      rw [hac]
    have hodd : (2 * (2^j * t) - 1) % 2 = 1 := by omega
    have hT : T (2 * (2^j * t) - 1) = 3 * (2^j * t) - 1 := T_impar _ ht2
    have hng : ¬ (3*c3 < 2*c2) := by omega
    have hAC : 3 * (2^j * t) = 2^j * (3*t) := by
      simp [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    rw [hx]
    simp only [criba]
    rw [if_pos hodd, if_neg hng, hT, hAC]
    exact ih (3*t) (3*c3) (2*c2) (by omega) (by omega)

/-- Para TODO k, el resto 2^k - 1 sobrevive a la criba: nunca queda vacia. -/
theorem criba_nunca_vacia (k : Nat) : sobrevive k (2^k - 1) = true := by
  unfold sobrevive
  have h := criba_impares k 1 1 1 (Nat.le_refl 1) (Nat.le_refl 1)
  rw [Nat.mul_one] at h
  exact h

/- 5. Y por tanto el CARDINAL por nivel es >= 1 para TODO k. -/

theorem cuentaAux_pos (k : Nat) : ∀ n r, r < n → sobrevive k r = true →
    1 ≤ cuentaAux k n := by
  intro n
  induction n with
  | zero => intro r h _; omega
  | succ m ih =>
    intro r h hs
    simp only [cuentaAux]
    by_cases hr : r = m
    · rw [hr] at hs
      rw [if_pos hs]
      omega
    · have hlt : r < m := by omega
      have h1 := ih r hlt hs
      by_cases hm : sobrevive k m = true
      · rw [if_pos hm]; omega
      · rw [if_neg hm]; omega

theorem cuenta_pos (k : Nat) : 1 ≤ cuenta k := by
  unfold cuenta
  have hlt : 2^k - 1 < 2^k := by
    have := @Nat.one_le_two_pow k
    omega
  exact cuentaAux_pos k (2^k) (2^k - 1) hlt (criba_nunca_vacia k)

/- ------------------------------------------------------------------ -/
/- 6. Los conteos concretos, por el KERNEL (decide, no #eval):
      a(k) para k = 1..13. Coinciden con el prefijo de A076227. -/

theorem cuentas_1_a_13 :
    cuenta 1 = 1 ∧ cuenta 2 = 1 ∧ cuenta 3 = 2 ∧ cuenta 4 = 3 ∧
    cuenta 5 = 4 ∧ cuenta 6 = 8 ∧ cuenta 7 = 13 ∧ cuenta 8 = 19 ∧
    cuenta 9 = 38 ∧ cuenta 10 = 64 ∧ cuenta 11 = 128 ∧ cuenta 12 = 226 ∧
    cuenta 13 = 367 := by decide

/- 7. Densidad NO CRECIENTE y cardinal NO DECRECIENTE en el rango kernel:
      a(k+1) <= 2*a(k)  (densidad)   y   a(k) <= a(k+1)  (cardinal). -/

theorem densidad_no_crece_1_a_13 :
    cuenta 2 ≤ 2 * cuenta 1 ∧ cuenta 3 ≤ 2 * cuenta 2 ∧
    cuenta 4 ≤ 2 * cuenta 3 ∧ cuenta 5 ≤ 2 * cuenta 4 ∧
    cuenta 6 ≤ 2 * cuenta 5 ∧ cuenta 7 ≤ 2 * cuenta 6 ∧
    cuenta 8 ≤ 2 * cuenta 7 ∧ cuenta 9 ≤ 2 * cuenta 8 ∧
    cuenta 10 ≤ 2 * cuenta 9 ∧ cuenta 11 ≤ 2 * cuenta 10 ∧
    cuenta 12 ≤ 2 * cuenta 11 ∧ cuenta 13 ≤ 2 * cuenta 12 := by decide

theorem cardinal_no_decrece_1_a_13 :
    cuenta 1 ≤ cuenta 2 ∧ cuenta 2 ≤ cuenta 3 ∧ cuenta 3 ≤ cuenta 4 ∧
    cuenta 4 ≤ cuenta 5 ∧ cuenta 5 ≤ cuenta 6 ∧ cuenta 6 ≤ cuenta 7 ∧
    cuenta 7 ≤ cuenta 8 ∧ cuenta 8 ≤ cuenta 9 ∧ cuenta 9 ≤ cuenta 10 ∧
    cuenta 10 ≤ cuenta 11 ∧ cuenta 11 ≤ cuenta 12 ∧ cuenta 12 ≤ cuenta 13 := by decide

/- 8. El "orden 2^(0,95k)" NO se cumple en rango alcanzable:
      2^(0.95*12) = 2^11.4 > 2^11, y  a(12)*9 = 2034 <= 2048 = 2^11.
      O sea a(12) esta a mas de un factor 9 (de hecho ~12) por debajo. -/

theorem orden_095_lejos_en_k12 : cuenta 12 * 9 ≤ 2^11 := by decide

/- ------------------------------------------------------------------ -/
#print axioms caso_7
#print axioms T_impar
#print axioms cerrada
#print axioms nunca_baja
#print axioms criba_impares
#print axioms criba_nunca_vacia
#print axioms cuenta_pos
#print axioms cuentas_1_a_13
#print axioms densidad_no_crece_1_a_13
#print axioms cardinal_no_decrece_1_a_13
#print axioms orden_095_lejos_en_k12
