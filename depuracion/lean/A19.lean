/-
  A19 — "biyeccion perfecta entre los 2^k restos y los 2^k patrones de paridad posibles"

  MAPA DEL ENUNCIADO: el ATAJO,  T(n) = n/2 si n par, (3n+1)/2 si n impar.
  (La nota de la base añade la otra mitad: con el mapa CLASICO C(n) = n/2 / 3n+1
   NO hay biyeccion y los patrones alcanzables son F(k+2), Fibonacci.)

  Codificacion: pat k n es el Nat < 2^k cuyo bit i es la paridad del i-esimo
  iterado de n bajo T (bit 0 = paridad de n).  "Patron de paridad de longitud k"
  = un numero p con 0 <= p < 2^k.  Asi "los 2^k restos" son [0, 2^k) y
  "los 2^k patrones" son [0, 2^k), y la biyeccion es r |-> pat k r.

  LO DEMOSTRADO AQUI, PARA TODO k (sin Mathlib, solo nucleo):
    clase_residual : pat k n = pat k (n % 2^k)      (el patron depende solo del resto)
    pat_lt         : pat k n < 2^k                  (el patron cae en [0,2^k))
    pat_inj        : inyectiva sobre [0,2^k)
    pat_surj       : sobreyectiva sobre [0,2^k)
    biyeccion_unica: para cada patron p < 2^k existe UN UNICO resto r < 2^k
  Y PARA EL CLASICO:
    patC_clase_residual (todo k), sin_dos_impares (todo n),
    clasico_no_inyectivo (contraejemplo concreto por decide),
    fibonacci_clasico: patrones alcanzables = F(k+2) para k = 1..7 (nucleo, decide)
-/
set_option maxRecDepth 40000

namespace A19

/-- Mapa del ATAJO (el del enunciado). -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- Mapa CLASICO (el de la nota: Fibonacci). -/
def C (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- Patron de paridad de los primeros k pasos del atajo, codificado como Nat. -/
def pat : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, n => n % 2 + 2 * pat k (T n)

/-- Lo mismo para el mapa clasico. -/
def patC : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, n => n % 2 + 2 * patC k (C n)

def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n+2 => fib n + fib (n+1)

/- ---------- ayudantes ---------- -/

theorem pow2_pos : ∀ k : Nat, 0 < 2^k := by
  intro k
  induction k with
  | zero => decide
  | succ k ih => rw [Nat.pow_succ]; omega

theorem two_pow_succ (k : Nat) : 2^(k+1) = 2 * 2^k := by
  rw [Nat.pow_succ, Nat.mul_comm]

theorem pow_succ_shift (k x : Nat) : 2^(k+1) * x = 2 * (2^k * x) := by
  rw [Nat.pow_succ, Nat.mul_comm (2^k) 2, Nat.mul_assoc]

/- ---------- ANCLAS contra el objeto real (LA TRAMPA) ----------
   Comprobadas por el NUCLEO con decide, no con #eval.
   La trayectoria del 27 en el atajo empieza 27,41,62,31,... y su patron
   de 6 pasos es 1,1,0,1,1,1 = 59. Cotejado contra un calculo Python
   independiente antes de escribir esto. -/

theorem ancla_T : T 27 = 41 ∧ T 41 = 62 ∧ T 62 = 31 ∧ T 2 = 1 ∧ T 1 = 2 := by decide
theorem ancla_C : C 27 = 82 ∧ C 82 = 41 ∧ C 1 = 4 ∧ C 2 = 1 := by decide
theorem ancla_pat : pat 6 0 = 0 ∧ pat 6 63 = 63 ∧ pat 6 27 = 59 := by decide

/- ---------- el patron cae en [0, 2^k) ---------- -/

theorem pat_lt : ∀ k n, pat k n < 2^k := by
  intro k
  induction k with
  | zero => intro n; simp only [pat]; decide
  | succ k ih =>
    intro n
    simp only [pat]
    have h1 := ih (T n)
    have h2 := two_pow_succ k
    omega

theorem patC_lt : ∀ k n, patC k n < 2^k := by
  intro k
  induction k with
  | zero => intro n; simp only [patC]; decide
  | succ k ih =>
    intro n
    simp only [patC]
    have h1 := ih (C n)
    have h2 := two_pow_succ k
    omega

/- ---------- Terras 1.2: el patron depende solo del resto mod 2^k ---------- -/

theorem pat_period : ∀ k m n, pat k (n + 2^k * m) = pat k n := by
  intro k
  induction k with
  | zero => intro m n; rfl
  | succ k ih =>
    intro m n
    have hx : 2^(k+1) * m = 2 * (2^k * m) := pow_succ_shift k m
    rw [hx]
    simp only [pat]
    have hpar : (n + 2*(2^k*m)) % 2 = n % 2 := by omega
    by_cases h : n % 2 = 0
    · have hT : T (n + 2*(2^k*m)) = T n + 2^k * m := by
        unfold T
        rw [if_pos (show (n + 2*(2^k*m)) % 2 = 0 by omega), if_pos h]
        omega
      rw [hpar, hT, ih m (T n)]
    · have hT : T (n + 2*(2^k*m)) = T n + 2^k * (3*m) := by
        unfold T
        rw [if_neg (show ¬(n + 2*(2^k*m)) % 2 = 0 by omega), if_neg h]
        have h3 : 2^k * (3*m) = 3 * (2^k*m) := Nat.mul_left_comm _ _ _
        rw [h3]
        omega
      rw [hpar, hT, ih (3*m) (T n)]

theorem patC_period : ∀ k m n, patC k (n + 2^k * m) = patC k n := by
  intro k
  induction k with
  | zero => intro m n; rfl
  | succ k ih =>
    intro m n
    have hx : 2^(k+1) * m = 2 * (2^k * m) := pow_succ_shift k m
    rw [hx]
    simp only [patC]
    have hpar : (n + 2*(2^k*m)) % 2 = n % 2 := by omega
    by_cases h : n % 2 = 0
    · have hC : C (n + 2*(2^k*m)) = C n + 2^k * m := by
        unfold C
        rw [if_pos (show (n + 2*(2^k*m)) % 2 = 0 by omega), if_pos h]
        omega
      rw [hpar, hC, ih m (C n)]
    · have hC : C (n + 2*(2^k*m)) = C n + 2^k * (6*m) := by
        unfold C
        rw [if_neg (show ¬(n + 2*(2^k*m)) % 2 = 0 by omega), if_neg h]
        have h3 : 2^k * (6*m) = 6 * (2^k*m) := Nat.mul_left_comm _ _ _
        rw [h3]
        omega
      rw [hpar, hC, ih (6*m) (C n)]

/-- El cuantificador del enunciado ("clase_residual"): el patron de CUALQUIER n
    es el de su resto mod 2^k. -/
theorem clase_residual : ∀ k n, pat k n = pat k (n % 2^k) := by
  intro k n
  have h := pat_period k (n / 2^k) (n % 2^k)
  rw [Nat.mod_add_div] at h
  exact h

theorem patC_clase_residual : ∀ k n, patC k n = patC k (n % 2^k) := by
  intro k n
  have h := patC_period k (n / 2^k) (n % 2^k)
  rw [Nat.mod_add_div] at h
  exact h

/- ---------- 2^j se cancela contra el 3 (coprimalidad, explicita) ---------- -/

theorem cancel_pow2 : ∀ j a c, 3*a = 2^j * c → ∃ d, a = 2^j * d := by
  intro j
  induction j with
  | zero => intro a c _; exact ⟨a, by rw [Nat.pow_zero, Nat.one_mul]⟩
  | succ j ih =>
    intro a c h
    have h2 : 2^(j+1)*c = 2*(2^j*c) := pow_succ_shift j c
    have h3 : 3*(a/2) = 2^j * c := by omega
    cases ih (a/2) c h3 with
    | intro d hd =>
      refine ⟨d, ?_⟩
      have h4 : 2^(j+1)*d = 2*(2^j*d) := pow_succ_shift j d
      omega

/- ---------- inyectividad de t |-> (3t+2) mod 2^k ---------- -/

theorem cancel3_aux (k a b : Nat) (hba : b ≤ a) (ha : a < 2^k)
    (hm : (3*a+2) % 2^k = (3*b+2) % 2^k) : a = b := by
  have hE : 0 < 2^k := pow2_pos k
  have d1 := Nat.div_add_mod (3*a+2) (2^k)
  have d2 := Nat.div_add_mod (3*b+2) (2^k)
  rw [hm] at d1
  have hx12 : 2^k * ((3*b+2)/2^k) ≤ 2^k * ((3*a+2)/2^k) := by omega
  have hq : (3*b+2)/2^k ≤ (3*a+2)/2^k := Nat.le_of_mul_le_mul_left hx12 hE
  have hd : (3*a+2)/2^k = (3*b+2)/2^k + ((3*a+2)/2^k - (3*b+2)/2^k) := by omega
  rw [hd, Nat.mul_add] at d1
  have hW : 3*(a-b) = 2^k * ((3*a+2)/2^k - (3*b+2)/2^k) := by omega
  cases cancel_pow2 k (a-b) _ hW with
  | intro e he =>
    cases e with
    | zero => rw [Nat.mul_zero] at he; omega
    | succ e' => rw [Nat.mul_succ] at he; omega

theorem cancel3 (k a b : Nat) (ha : a < 2^k) (hb : b < 2^k)
    (hm : (3*a+2) % 2^k = (3*b+2) % 2^k) : a = b := by
  cases Nat.le_total b a with
  | inl h => exact cancel3_aux k a b h ha hm
  | inr h => exact (cancel3_aux k b a h hb hm.symm).symm

/- ---------- INYECTIVIDAD ---------- -/

theorem pat_inj : ∀ k r s, r < 2^k → s < 2^k → pat k r = pat k s → r = s := by
  intro k
  induction k with
  | zero =>
    intro r s hr hs _
    have h1 : (2:Nat)^0 = 1 := rfl
    omega
  | succ k ih =>
    intro r s hr hs h
    have hEr := two_pow_succ k
    have hE : 0 < 2^k := pow2_pos k
    simp only [pat] at h
    have hpar : r % 2 = s % 2 := by omega
    have htails : pat k (T r) = pat k (T s) := by omega
    have hred : pat k (T r % 2^k) = pat k (T s % 2^k) := by
      rw [← clase_residual, ← clase_residual]; exact htails
    have h1 : T r % 2^k = T s % 2^k :=
      ih _ _ (Nat.mod_lt _ hE) (Nat.mod_lt _ hE) hred
    by_cases hp : r % 2 = 0
    · have hsp : s % 2 = 0 := by omega
      have hTr : T r = r / 2 := by unfold T; rw [if_pos hp]
      have hTs : T s = s / 2 := by unfold T; rw [if_pos hsp]
      have hr2 : r / 2 < 2^k := by omega
      have hs2 : s / 2 < 2^k := by omega
      rw [hTr, hTs, Nat.mod_eq_of_lt hr2, Nat.mod_eq_of_lt hs2] at h1
      omega
    · have hp1 : r % 2 = 1 := by omega
      have hsp : s % 2 = 1 := by omega
      have hTr : T r = 3*(r/2) + 2 := by
        unfold T; rw [if_neg (by omega)]; omega
      have hTs : T s = 3*(s/2) + 2 := by
        unfold T; rw [if_neg (by omega)]; omega
      rw [hTr, hTs] at h1
      have ha : r/2 < 2^k := by omega
      have hb : s/2 < 2^k := by omega
      have := cancel3 k (r/2) (s/2) ha hb h1
      omega

/- ---------- inverso explicito de 3 mod 2^k (sin Baker, sin nada) ---------- -/

theorem ex3inv : ∀ k, ∃ x q, 3 * x = 2^k * q + 1 := by
  intro k
  induction k with
  | zero => exact ⟨1, 2, by decide⟩
  | succ k ih =>
    cases ih with
    | intro x hx =>
      cases hx with
      | intro q hq =>
        by_cases hqp : q % 2 = 0
        · refine ⟨x, q/2, ?_⟩
          have hu : q = 2*(q/2) := by omega
          have h3 : 2^k*q = 2*(2^k*(q/2)) := by
            calc 2^k*q = 2^k*(2*(q/2)) := by rw [← hu]
              _ = 2*(2^k*(q/2)) := Nat.mul_left_comm _ _ _
          have h2 : 2^(k+1)*(q/2) = 2*(2^k*(q/2)) := pow_succ_shift k (q/2)
          omega
        · refine ⟨x + 2^k, (q+3)/2, ?_⟩
          have hu : q + 3 = 2*((q+3)/2) := by omega
          have h3 : 2^k*(q+3) = 2*(2^k*((q+3)/2)) := by
            calc 2^k*(q+3) = 2^k*(2*((q+3)/2)) := by rw [← hu]
              _ = 2*(2^k*((q+3)/2)) := Nat.mul_left_comm _ _ _
          have h4 : 2^k*(q+3) = 2^k*q + 2^k*3 := Nat.mul_add _ _ _
          have h2 : 2^(k+1)*((q+3)/2) = 2*(2^k*((q+3)/2)) := pow_succ_shift k ((q+3)/2)
          omega

theorem mod_eq_helper (E a s c d : Nat) (hs : s < E) (h : a + E*c = s + E*d) :
    a % E = s := by
  have h1 : (a + E*c) % E = (s + E*d) % E := by rw [h]
  rw [Nat.add_mul_mod_self_left, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hs] at h1
  exact h1

/-- Para cada resto objetivo s hay t < 2^k con 3t+2 = s (mod 2^k). -/
theorem solve3 (k s : Nat) (hs : s < 2^k) : ∃ t, t < 2^k ∧ (3*t + 2) % 2^k = s := by
  cases ex3inv k with
  | intro x hx =>
    cases hx with
    | intro q hq =>
      have hE : 0 < 2^k := pow2_pos k
      refine ⟨(x*(s + 2*2^k - 2)) % 2^k, Nat.mod_lt _ hE, ?_⟩
      have hd := Nat.div_add_mod (x*(s + 2*2^k - 2)) (2^k)
      have hkey : 3*(x*(s + 2*2^k - 2))
          = 2^k*(q*(s + 2*2^k - 2)) + (s + 2*2^k - 2) := by
        calc 3*(x*(s + 2*2^k - 2))
            = (3*x)*(s + 2*2^k - 2) := by rw [← Nat.mul_assoc]
          _ = (2^k*q + 1)*(s + 2*2^k - 2) := by rw [hq]
          _ = 2^k*q*(s + 2*2^k - 2) + 1*(s + 2*2^k - 2) := Nat.add_mul _ _ _
          _ = 2^k*(q*(s + 2*2^k - 2)) + (s + 2*2^k - 2) := by
              rw [Nat.mul_assoc, Nat.one_mul]
      apply mod_eq_helper (2^k) _ s (3*((x*(s + 2*2^k - 2))/2^k))
          (2 + q*(s + 2*2^k - 2)) hs
      have e1 : 2^k*(3*((x*(s + 2*2^k - 2))/2^k))
          = 3*(2^k*((x*(s + 2*2^k - 2))/2^k)) := Nat.mul_left_comm _ _ _
      have e2 : 2^k*(2 + q*(s + 2*2^k - 2))
          = 2^k*2 + 2^k*(q*(s + 2*2^k - 2)) := Nat.mul_add _ _ _
      omega

/- ---------- SOBREYECTIVIDAD ---------- -/

theorem pat_surj : ∀ k p, p < 2^k → ∃ r, r < 2^k ∧ pat k r = p := by
  intro k
  induction k with
  | zero =>
    intro p hp
    have h1 : (2:Nat)^0 = 1 := rfl
    have hp0 : p = 0 := by omega
    exact ⟨0, by omega, by simp only [pat, hp0]⟩
  | succ k ih =>
    intro p hp
    have hEr := two_pow_succ k
    have hp2 : p / 2 < 2^k := by omega
    cases ih (p/2) hp2 with
    | intro s hsp =>
      cases hsp with
      | intro hs1 hs2 =>
        by_cases hb : p % 2 = 0
        · refine ⟨2*s, by omega, ?_⟩
          simp only [pat]
          have hT : T (2*s) = s := by
            unfold T; rw [if_pos (by omega)]; omega
          rw [hT, hs2]
          omega
        · cases solve3 k s hs1 with
          | intro t htp =>
            cases htp with
            | intro ht1 ht2 =>
              refine ⟨2*t+1, by omega, ?_⟩
              simp only [pat]
              have hT : T (2*t+1) = 3*t+2 := by
                unfold T; rw [if_neg (by omega)]; omega
              rw [hT, clase_residual k (3*t+2), ht2, hs2]
              omega

/- ---------- LA BIYECCION, enunciada entera ---------- -/

/-- A19, mapa del atajo, PARA TODO k: r ↦ pat k r manda [0,2^k) DENTRO de
    [0,2^k), es inyectiva y es sobreyectiva — biyeccion perfecta entre los
    2^k restos y los 2^k patrones de paridad. -/
theorem biyeccion (k : Nat) :
    (∀ r, r < 2^k → pat k r < 2^k) ∧
    (∀ r s, r < 2^k → s < 2^k → pat k r = pat k s → r = s) ∧
    (∀ p, p < 2^k → ∃ r, r < 2^k ∧ pat k r = p) :=
  ⟨fun r _ => pat_lt k r, pat_inj k, pat_surj k⟩

/-- Version con unicidad explicita: cada patron tiene EXACTAMENTE un resto. -/
theorem biyeccion_unica (k p : Nat) (hp : p < 2^k) :
    ∃ r, (r < 2^k ∧ pat k r = p) ∧ ∀ r', r' < 2^k → pat k r' = p → r' = r := by
  cases pat_surj k p hp with
  | intro r hr =>
    cases hr with
    | intro h1 h2 =>
      exact ⟨r, ⟨h1, h2⟩, fun r' hr' hp' => pat_inj k r' r hr' h1 (by rw [hp', h2])⟩

/-- Ancla de la biyeccion a escala concreta (k=6), decidida por el NUCLEO:
    los 64 patrones son alcanzados por los 64 restos. -/
theorem ancla_biyeccion_k6 :
    ((List.range 64).all (fun p => (List.range 64).any (fun r => pat 6 r == p))) = true := by
  decide

/- ---------- LA OTRA MITAD: el mapa CLASICO ---------- -/

/-- La razon estructural de Fibonacci: tras un impar viene un par (3n+1 es par).
    Dos impares seguidos son imposibles con el mapa clasico. -/
theorem sin_dos_impares (n : Nat) (h : n % 2 = 1) : C n % 2 = 0 := by
  unfold C
  rw [if_neg (by omega)]
  omega

/-- Con el clasico NO hay biyeccion: contraejemplo concreto, restos 1 y 3
    mod 4 comparten el patron (impar, par). Decidido por el nucleo. -/
theorem clasico_no_inyectivo : patC 2 1 = patC 2 3 ∧ (1:Nat) ≠ 3 := by decide

/-- Cuantos patrones p < 2^k alcanza el clasico (los restos bastan, por
    patC_clase_residual; y patC_lt garantiza que todos caen en [0,2^k)). -/
def patC_alcanzables (k : Nat) : Nat :=
  ((List.range (2^k)).filter
    (fun p => (List.range (2^k)).any (fun r => patC k r == p))).length

set_option maxHeartbeats 2000000 in
/-- Los patrones alcanzables del clasico son F(k+2): 2,3,5,8,13,21,34 para
    k = 1..7.  Decidido por el NUCLEO (no #eval). Junto con patC_clase_residual
    (todo n se reduce a su resto) esto cuenta TODOS los patrones alcanzables. -/
theorem fibonacci_clasico :
    patC_alcanzables 1 = fib 3 ∧ patC_alcanzables 2 = fib 4 ∧
    patC_alcanzables 3 = fib 5 ∧ patC_alcanzables 4 = fib 6 ∧
    patC_alcanzables 5 = fib 7 ∧ patC_alcanzables 6 = fib 8 ∧
    patC_alcanzables 7 = fib 9 := by decide

/- ---------- control final ---------- -/

#print axioms biyeccion
#print axioms biyeccion_unica
#print axioms clase_residual
#print axioms pat_period
#print axioms pat_inj
#print axioms pat_surj
#print axioms sin_dos_impares
#print axioms clasico_no_inyectivo
#print axioms fibonacci_clasico
#print axioms ancla_pat
#print axioms ancla_biyeccion_k6
#print axioms patC_clase_residual

end A19
