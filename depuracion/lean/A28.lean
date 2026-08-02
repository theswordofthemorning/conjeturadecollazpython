/-
A28 -- AGENTE 1 (LEAN) del trio de verificacion.

ENUNCIADO: "el mapa RESTO -> VECTOR DE PARIDAD es una biyeccion
Z/2^k -> {0,1}^k, luego no hay descarte EN BLOQUE de clases para buscar ciclos"

MAPA USADO: el ATAJO de Terras 1976:  T(n) = n/2 si n par,  (3n+1)/2 si n impar.
(La fuente declarada es Terras 1976, cuyo vector de paridad es sobre T.
 Con el mapa CLASICO el enunciado es FALSO: contraejemplo por decide abajo.)

Lo demostrado, para TODO k:
  (1) pv_eq_of_mod_eq : el vector de paridad depende solo de n mod 2^k
      (el mapa Z/2^k -> {0,1}^k esta BIEN DEFINIDO)
  (2) mod_eq_of_pv_eq : el vector de paridad DETERMINA n mod 2^k
      (INYECTIVO; ademas es el "no comparten destino" del enunciado)
  (3) pv_surj         : todo vector de longitud k tiene preimagen r < 2^k
      (SURYECTIVO, con testigo construido con el inverso de 3 mod 2^(k+1))

Sin Mathlib: solo nucleo. Sin sorry.
-/
set_option maxRecDepth 40000

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3*n+1)/2

def pv : Nat → Nat → List Bool
  | 0, _ => []
  | k+1, n => (n % 2 == 1) :: pv k (T n)

-- mapa CLASICO, solo para el control A/B del final
def Tc (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3*n+1

def pvc : Nat → Nat → List Bool
  | 0, _ => []
  | k+1, n => (n % 2 == 1) :: pvc k (Tc n)

-- == utilidades elementales ==================================================

theorem T_even {n : Nat} (h : n % 2 = 0) : T n = n / 2 := by
  unfold T; rw [if_pos h]

theorem T_odd {n : Nat} (h : n % 2 = 1) : T n = (3*n+1)/2 := by
  unfold T; rw [if_neg (by omega : ¬ n % 2 = 0)]

theorem pow_succ_eq (k : Nat) : 2^(k+1) = 2 * 2^k := by
  rw [Nat.pow_succ, Nat.mul_comm]

theorem two_pow_pos (k : Nat) : 0 < 2^k := by
  induction k with
  | zero => decide
  | succ k ih => rw [pow_succ_eq]; omega

theorem mul_mod_arg (a b n : Nat) : (a * (b % n)) % n = (a * b) % n := by
  rw [Nat.mul_mod, Nat.mod_mod_of_dvd b (Nat.dvd_refl n), ← Nat.mul_mod]

-- == (1) BIEN DEFINIDO: pv k solo mira n mod 2^k =============================

theorem pv_shift (k : Nat) : ∀ n a, pv k (n + 2^k * a) = pv k n := by
  induction k with
  | zero => intro n a; rfl
  | succ k ih =>
    intro n a
    have hsh : 2^(k+1) * a = 2 * (2^k * a) := by
      calc 2^(k+1) * a = 2^k * 2 * a := by rw [Nat.pow_succ]
        _ = 2^k * (2 * a) := Nat.mul_assoc _ _ _
        _ = 2 * (2^k * a) := Nat.mul_left_comm _ _ _
    have hpar : (n + 2^(k+1) * a) % 2 = n % 2 := by rw [hsh]; omega
    simp only [pv]
    rw [hpar]
    by_cases hp : n % 2 = 0
    · have h1 : (n + 2^(k+1)*a) % 2 = 0 := by rw [hpar]; exact hp
      have hTn : T (n + 2^(k+1)*a) = T n + 2^k * a := by
        rw [T_even h1, T_even hp, hsh]; omega
      rw [hTn, ih (T n) a]
    · have hp1 : n % 2 = 1 := by omega
      have h1 : (n + 2^(k+1)*a) % 2 = 1 := by rw [hpar]; exact hp1
      have h3 : 2^k * (3*a) = 3 * (2^k * a) := Nat.mul_left_comm _ _ _
      have hTn : T (n + 2^(k+1)*a) = T n + 2^k * (3*a) := by
        rw [T_odd h1, T_odd hp1, hsh, h3]; omega
      rw [hTn, ih (T n) (3*a)]

theorem pv_mod (k n : Nat) : pv k (n % 2^k) = pv k n := by
  have h := Nat.div_add_mod n (2^k)
  calc pv k (n % 2^k)
      = pv k (n % 2^k + 2^k * (n / 2^k)) := (pv_shift k (n % 2^k) (n / 2^k)).symm
    _ = pv k (2^k * (n / 2^k) + n % 2^k) := by rw [Nat.add_comm]
    _ = pv k n := by rw [h]

theorem pv_eq_of_mod_eq {k n m : Nat} (h : n % 2^k = m % 2^k) :
    pv k n = pv k m := by
  rw [← pv_mod k n, ← pv_mod k m, h]

-- == el inverso de 3 modulo 2^j, construido =================================

theorem uc_spec : ∀ j : Nat, ∃ u c : Nat, 3 * u = 2^j * c + 1 := by
  intro j
  induction j with
  | zero => exact ⟨1, 2, rfl⟩
  | succ j ih =>
    cases ih with
    | intro u hu =>
      cases hu with
      | intro c hc =>
        by_cases hpar : c % 2 = 0
        · refine ⟨u, c/2, ?_⟩
          rw [Nat.pow_succ, Nat.mul_assoc]
          have h2 : 2 * (c/2) = c := by omega
          rw [h2]; exact hc
        · refine ⟨u + 2^j, (c+3)/2, ?_⟩
          rw [Nat.pow_succ, Nat.mul_assoc]
          have h2 : 2 * ((c+3)/2) = c + 3 := by omega
          rw [h2]
          have h3 : 2^j * (c+3) = 2^j * c + 2^j * 3 := Nat.mul_add _ _ _
          have h4 : 3 * (u + 2^j) = 3*u + 3*2^j := Nat.mul_add _ _ _
          omega

theorem cancel3 {j a b : Nat} (h : (3*a) % 2^j = (3*b) % 2^j) :
    a % 2^j = b % 2^j := by
  cases uc_spec j with
  | intro u hu =>
    cases hu with
    | intro c h3u =>
      have expand : ∀ x : Nat, (u * (3*x)) % 2^j = x % 2^j := by
        intro x
        have e1 : u * (3*x) = x + 2^j * (c*x) := by
          calc u * (3*x) = u * 3 * x := (Nat.mul_assoc u 3 x).symm
            _ = 3 * u * x := by rw [Nat.mul_comm u 3]
            _ = (2^j * c + 1) * x := by rw [h3u]
            _ = 2^j * c * x + 1 * x := Nat.add_mul _ _ _
            _ = x + 2^j * (c*x) := by rw [Nat.one_mul, Nat.mul_assoc, Nat.add_comm]
        rw [e1, Nat.add_mul_mod_self_left]
      have hc2 : (u * (3*a)) % 2^j = (u * (3*b)) % 2^j := by
        rw [Nat.mul_mod u (3*a), Nat.mul_mod u (3*b), h]
      rw [← expand a, ← expand b]
      exact hc2

-- == subir una congruencia un nivel =========================================

-- si a y b son pares y a/2 = b/2 (mod 2^k), entonces a = b (mod 2^(k+1))
theorem double_mod {k a b : Nat} (ha : a % 2 = 0) (hb : b % 2 = 0)
    (h : (a/2) % 2^k = (b/2) % 2^k) : a % 2^(k+1) = b % 2^(k+1) := by
  have hPQ : 2^(k+1) = 2*2^k := pow_succ_eq k
  have hQ : 0 < 2^k := two_pow_pos k
  have hd1 := Nat.div_add_mod (a/2) (2^k)
  have hd2 := Nat.div_add_mod (b/2) (2^k)
  have hq1 : 2^(k+1) * (a/2 / 2^k) = 2*(2^k*(a/2 / 2^k)) := by
    rw [hPQ, Nat.mul_assoc]
  have hq2 : 2^(k+1) * (b/2 / 2^k) = 2*(2^k*(b/2 / 2^k)) := by
    rw [hPQ, Nat.mul_assoc]
  have ea : a = 2^(k+1) * (a/2 / 2^k) + 2*((a/2) % 2^k) := by omega
  have eb : b = 2^(k+1) * (b/2 / 2^k) + 2*((b/2) % 2^k) := by omega
  rw [ea, eb, h, Nat.mul_add_mod, Nat.mul_add_mod]

theorem succ_mod_cancel {P a b : Nat} (h : (a+1) % P = (b+1) % P) :
    a % P = b % P := by
  by_cases hP : P = 0
  · subst hP
    rw [Nat.mod_zero, Nat.mod_zero] at h
    rw [Nat.mod_zero, Nat.mod_zero]
    omega
  · have hP0 : 0 < P := by omega
    have hxa : a % P < P := Nat.mod_lt _ hP0
    have hxb : b % P < P := Nat.mod_lt _ hP0
    have h1 : (a % P + 1) % P = (b % P + 1) % P := by
      rw [Nat.mod_add_mod, Nat.mod_add_mod]; exact h
    by_cases ha1 : a % P + 1 < P
    · by_cases hb1 : b % P + 1 < P
      · rw [Nat.mod_eq_of_lt ha1, Nat.mod_eq_of_lt hb1] at h1; omega
      · have hb2 : b % P + 1 = P := by omega
        rw [Nat.mod_eq_of_lt ha1, hb2, Nat.mod_self] at h1; omega
    · have ha2 : a % P + 1 = P := by omega
      by_cases hb1 : b % P + 1 < P
      · rw [ha2, Nat.mod_self, Nat.mod_eq_of_lt hb1] at h1; omega
      · have hb2 : b % P + 1 = P := by omega
        omega

theorem odd_lift {k a b : Nat} (ha : a % 2 = 1) (hb : b % 2 = 1)
    (h : ((3*a+1)/2) % 2^k = ((3*b+1)/2) % 2^k) :
    a % 2^(k+1) = b % 2^(k+1) := by
  have h1 : (3*a+1) % 2 = 0 := by omega
  have h2 : (3*b+1) % 2 = 0 := by omega
  have hd : (3*a+1) % 2^(k+1) = (3*b+1) % 2^(k+1) := double_mod h1 h2 h
  have h3 : (3*a) % 2^(k+1) = (3*b) % 2^(k+1) := succ_mod_cancel hd
  exact cancel3 h3

theorem head_parity {n m : Nat}
    (h : ((n % 2 == 1) : Bool) = (m % 2 == 1)) : n % 2 = m % 2 := by
  by_cases hn : n % 2 = 0
  · by_cases hm : m % 2 = 0
    · rw [hn, hm]
    · have hm1 : m % 2 = 1 := by omega
      rw [hn, hm1] at h
      exact absurd h (by decide)
  · have hn1 : n % 2 = 1 := by omega
    by_cases hm : m % 2 = 0
    · rw [hn1, hm] at h
      exact absurd h (by decide)
    · have hm1 : m % 2 = 1 := by omega
      rw [hn1, hm1]

-- == (2) INYECTIVO: el vector de paridad determina n mod 2^k ================

theorem mod_eq_of_pv_eq : ∀ k n m, pv k n = pv k m → n % 2^k = m % 2^k := by
  intro k
  induction k with
  | zero =>
    intro n m _
    rw [Nat.pow_zero]
    omega
  | succ k ih =>
    intro n m h
    simp only [pv] at h
    injection h with h1 h2
    have hpar : n % 2 = m % 2 := head_parity h1
    have ht := ih (T n) (T m) h2
    by_cases hp : n % 2 = 0
    · have hmp : m % 2 = 0 := by omega
      rw [T_even hp, T_even hmp] at ht
      exact double_mod hp hmp ht
    · have hp1 : n % 2 = 1 := by omega
      have hmp : m % 2 = 1 := by omega
      rw [T_odd hp1, T_odd hmp] at ht
      exact odd_lift hp1 hmp ht

-- == (3) SURYECTIVO: preimagen explicita ====================================

-- para el bit 1: existe un r impar < 2^(k+1) con T r = s (mod 2^k)
theorem odd_preimage {k s : Nat} (hs : s < 2^k) :
    ∃ r, r < 2^(k+1) ∧ r % 2 = 1 ∧ T r % 2^k = s := by
  cases uc_spec (k+1) with
  | intro u hu =>
    cases hu with
    | intro c h3u =>
      have hPQ : 2^(k+1) = 2*2^k := pow_succ_eq k
      have hQ : 0 < 2^k := two_pow_pos k
      have hP : 0 < 2^(k+1) := by omega
      have hdvd : (2:Nat) ∣ 2^(k+1) := ⟨2^k, hPQ⟩
      have hA : (3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1))) % 2^(k+1)
              = (2*s + 2^(k+1) - 1) % 2^(k+1) := by
        rw [mul_mod_arg]
        have e : 3 * (u * (2*s + 2^(k+1) - 1))
               = (2*s + 2^(k+1) - 1) + 2^(k+1) * (c * (2*s + 2^(k+1) - 1)) := by
          calc 3 * (u * (2*s + 2^(k+1) - 1))
              = 3 * u * (2*s + 2^(k+1) - 1) := (Nat.mul_assoc 3 u _).symm
            _ = (2^(k+1) * c + 1) * (2*s + 2^(k+1) - 1) := by rw [h3u]
            _ = 2^(k+1) * c * (2*s + 2^(k+1) - 1) + 1 * (2*s + 2^(k+1) - 1) :=
                Nat.add_mul _ _ _
            _ = (2*s + 2^(k+1) - 1) + 2^(k+1) * (c * (2*s + 2^(k+1) - 1)) := by
                rw [Nat.one_mul, Nat.mul_assoc, Nat.add_comm]
        rw [e, Nat.add_mul_mod_self_left]
      have hparity : ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) % 2 = 1 := by
        have t1 : (3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1))) % 2
                = (3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1))) % 2^(k+1) % 2 :=
          (Nat.mod_mod_of_dvd _ hdvd).symm
        rw [hA, Nat.mod_mod_of_dvd _ hdvd] at t1
        omega
      have hodd2 : (3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) + 1) % 2^(k+1)
                 = 2*s := by
        rw [← Nat.mod_add_mod, hA, Nat.mod_add_mod]
        have e2 : 2*s + 2^(k+1) - 1 + 1 = 2*s + 2^(k+1) := by omega
        rw [e2, Nat.add_mod_right]
        exact Nat.mod_eq_of_lt (by omega)
      refine ⟨(u * (2*s + 2^(k+1) - 1)) % 2^(k+1), Nat.mod_lt _ hP, hparity, ?_⟩
      rw [T_odd hparity]
      have hd := Nat.div_add_mod
        (3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) + 1) (2^(k+1))
      rw [hodd2] at hd
      have hq2 : 2^(k+1) * ((3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) + 1) / 2^(k+1))
               = 2 * (2^k * ((3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) + 1) / 2^(k+1))) := by
        rw [hPQ, Nat.mul_assoc]
      have h5 : (3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) + 1) / 2
               = 2^k * ((3 * ((u * (2*s + 2^(k+1) - 1)) % 2^(k+1)) + 1) / 2^(k+1)) + s := by
        omega
      rw [h5, Nat.mul_add_mod]
      exact Nat.mod_eq_of_lt hs

theorem pv_surj : ∀ v : List Bool, ∃ r, r < 2^(v.length) ∧ pv (v.length) r = v := by
  intro v
  induction v with
  | nil => exact ⟨0, by decide, rfl⟩
  | cons b v ih =>
    cases ih with
    | intro s hs =>
      cases hs with
      | intro hslt hspv =>
        cases b with
        | false =>
          refine ⟨2*s, ?_, ?_⟩
          · simp only [List.length_cons]
            have := pow_succ_eq (v.length)
            omega
          · simp only [List.length_cons, pv]
            have hp : (2*s) % 2 = 0 := by omega
            have hT : T (2*s) = s := by rw [T_even hp]; omega
            rw [hp, hT, hspv]
            rfl
        | true =>
          simp only [List.length_cons]
          cases odd_preimage hslt with
          | intro r hr =>
            cases hr with
            | intro hrlt hr2 =>
              cases hr2 with
              | intro hrodd hrT =>
                refine ⟨r, hrlt, ?_⟩
                simp only [pv]
                rw [hrodd, ← pv_mod (v.length) (T r), hrT, hspv]
                rfl

-- == EL TEOREMA A28: biyeccion Z/2^k <-> {0,1}^k, para todo k ===============

theorem A28_biyeccion (k : Nat) :
    (∀ n m : Nat, n % 2^k = m % 2^k → pv k n = pv k m) ∧
    (∀ r₁ r₂ : Nat, r₁ < 2^k → r₂ < 2^k → pv k r₁ = pv k r₂ → r₁ = r₂) ∧
    (∀ v : List Bool, v.length = k → ∃ r, r < 2^k ∧ pv k r = v) := by
  refine ⟨fun n m h => pv_eq_of_mod_eq h, fun r₁ r₂ h1 h2 h => ?_, fun v hv => ?_⟩
  · have hm := mod_eq_of_pv_eq k r₁ r₂ h
    rw [Nat.mod_eq_of_lt h1, Nat.mod_eq_of_lt h2] at hm
    exact hm
  · cases pv_surj v with
    | intro r hr =>
      rw [hv] at hr
      exact ⟨r, hr⟩

-- el "no hay descarte en bloque", en su unica parte matematica:
-- dos clases distintas mod 2^k NUNCA comparten vector de paridad
theorem clases_no_comparten (k r₁ r₂ : Nat) (h1 : r₁ < 2^k) (h2 : r₂ < 2^k)
    (hne : r₁ ≠ r₂) : pv k r₁ ≠ pv k r₂ := by
  intro h
  apply hne
  have hm := mod_eq_of_pv_eq k r₁ r₂ h
  rw [Nat.mod_eq_of_lt h1, Nat.mod_eq_of_lt h2] at hm
  exact hm

-- == CASOS CONOCIDOS, comprobados por el NUCLEO con decide ==================

-- la trayectoria del 27 con el atajo: 27,41,62,31,47,71,107,161 -> paridades
theorem caso_27 : pv 8 27 = [true, true, false, true, true, true, true, true] := by
  decide

-- los dos extremos del eje: resto 0 = PPPPPP, resto 2^k-1 = IIIIII
theorem caso_extremos :
    pv 6 0 = [false, false, false, false, false, false] ∧
    pv 6 63 = [true, true, true, true, true, true] := by
  decide

-- biyeccion exhaustiva a k = 6: los 64 restos dan 64 vectores distintos
theorem inyectividad_k6_decide :
    ∀ r₁, r₁ < 64 → ∀ r₂, r₂ < 64 → pv 6 r₁ = pv 6 r₂ → r₁ = r₂ := by
  decide

-- == CONTROL A/B: con el mapa CLASICO el enunciado es FALSO =================

-- 1 y 3 son restos distintos mod 4 con el MISMO vector clasico [1,0]
theorem clasico_no_inyectivo :
    pvc 2 1 = pvc 2 3 ∧ (1 : Nat) % 2^2 ≠ (3 : Nat) % 2^2 := by
  decide

-- == control final ==========================================================

#print axioms pv_eq_of_mod_eq
#print axioms mod_eq_of_pv_eq
#print axioms pv_surj
#print axioms A28_biyeccion
#print axioms clases_no_comparten
#print axioms caso_27
#print axioms caso_extremos
#print axioms inyectividad_k6_decide
#print axioms clasico_no_inyectivo
