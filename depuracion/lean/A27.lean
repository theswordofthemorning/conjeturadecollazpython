/-
A27 (afirmaciones.db): "por cada resto mod 2^k hay COMO MUCHO UN candidato
de ciclo, y sale en cerrado: m = (r - T^k(r)) / (3^{S(r)} - 2^k)"

MAPA: el ATAJO.  T(n) = n/2 si n par, (3n+1)/2 si n impar.
"Ciclo de longitud k" significa T^k(n) = n con n = 2^k*m + r.

FORMALIZACION (sobre Nat, o sea candidatos m >= 0; el detalle de los m
negativos que recuperan 3n-1 queda declarado fuera del alcance):

  1. terras:           T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r)   para TODO m, r
  2. denominador:      3^s <> 2^k  para todo s, si k >= 1
  3. a_lo_sumo_un_candidato:  con k >= 1, si m1 y m2 dan ciclo sobre el mismo
                       resto r, entonces m1 = m2       <- "como mucho UN candidato"
  4. unico_por_clase:  version por clase residual: dos n k-periodicos con el
                       mismo n mod 2^k son EL MISMO n
  5. forma_cerrada_pos / forma_cerrada_neg:  el m del ciclo sale en cerrado;
                       la rama "neg" es la formula LITERAL del enunciado
  6. borde_k0:         con k = 0 el enunciado es FALSO (dos candidatos distintos),
                       o sea la hipotesis k >= 1 es necesaria y no decorativa
  7. casos concretos por `decide` (nucleo, no #eval): el ciclo {1,2}, el 7,
                       y el 221 con A = 41 impares en B = 73 pasos del atajo.
-/

set_option maxRecDepth 40000

namespace A27

/-- El mapa del ATAJO sobre Nat: n/2 si par, (3n+1)/2 si impar. -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- k iteraciones de T. -/
def Titer : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => Titer k (T n)

/-- S k n = cuantos de los primeros k pasos son impares. -/
def S : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, n => n % 2 + S k (T n)

theorem Titer_succ (k n : Nat) : Titer (k+1) n = Titer k (T n) := rfl

theorem S_succ (k n : Nat) : S (k+1) n = n % 2 + S k (T n) := rfl

/-- TEOREMA 1 (identidad de Terras, T1.2): la trayectoria de 2^k*m + r es
    una recta en m, con pendiente 3^{S_k(r)} y ordenada T^k(r), y las dos
    dependen SOLO de r.  Vale para TODO r (no hace falta r < 2^k). -/
theorem terras : ∀ (k m r : Nat),
    Titer k (2 ^ k * m + r) = 3 ^ (S k r) * m + Titer k r := by
  intro k
  induction k with
  | zero =>
    intro m r
    simp [Titer, S, Nat.pow_zero, Nat.one_mul]
  | succ k ih =>
    intro m r
    have hpow : (2:Nat) ^ (k+1) * m = 2 * (2 ^ k * m) := by
      rw [Nat.pow_succ, Nat.mul_comm ((2:Nat)^k) 2, Nat.mul_assoc]
    by_cases hr : r % 2 = 0
    · -- paso PAR
      have hTr : T r = r / 2 := by unfold T; rw [if_pos hr]
      have hcond : (2 * (2 ^ k * m) + r) % 2 = 0 := by omega
      have hTbig : T (2 ^ (k+1) * m + r) = 2 ^ k * m + T r := by
        rw [hpow, hTr]; unfold T; rw [if_pos hcond]; omega
      have hS : S (k+1) r = S k (T r) := by rw [S_succ]; omega
      calc Titer (k+1) (2 ^ (k+1) * m + r)
          = Titer k (T (2 ^ (k+1) * m + r)) := Titer_succ ..
        _ = Titer k (2 ^ k * m + T r) := by rw [hTbig]
        _ = 3 ^ (S k (T r)) * m + Titer k (T r) := ih m (T r)
        _ = 3 ^ (S (k+1) r) * m + Titer (k+1) r := by rw [hS, Titer_succ]
    · -- paso IMPAR
      have hr1 : r % 2 = 1 := by omega
      have hTr : T r = (3 * r + 1) / 2 := by unfold T; rw [if_neg hr]
      have hcond : ¬ ((2 * (2 ^ k * m) + r) % 2 = 0) := by omega
      have hmul : (2:Nat) ^ k * (3 * m) = 3 * (2 ^ k * m) := by
        rw [← Nat.mul_assoc, Nat.mul_comm ((2:Nat)^k) 3, Nat.mul_assoc]
      have hTbig : T (2 ^ (k+1) * m + r) = 2 ^ k * (3 * m) + T r := by
        rw [hpow, hTr, hmul]; unfold T; rw [if_neg hcond]; omega
      have hS : S (k+1) r = S k (T r) + 1 := by rw [S_succ]; omega
      calc Titer (k+1) (2 ^ (k+1) * m + r)
          = Titer k (T (2 ^ (k+1) * m + r)) := Titer_succ ..
        _ = Titer k (2 ^ k * (3 * m) + T r) := by rw [hTbig]
        _ = 3 ^ (S k (T r)) * (3 * m) + Titer k (T r) := ih (3 * m) (T r)
        _ = 3 ^ (S (k+1) r) * m + Titer (k+1) r := by
            rw [hS, Nat.pow_succ, ← Nat.mul_assoc, Titer_succ]

/-- 3^s es siempre impar. -/
theorem impar_pow3 : ∀ s : Nat, 3 ^ s % 2 = 1 := by
  intro s
  induction s with
  | zero => rfl
  | succ s ih => rw [Nat.pow_succ]; omega

/-- 2^k es par en cuanto k >= 1. -/
theorem par_pow2 (k : Nat) (hk : 1 ≤ k) : 2 ^ k % 2 = 0 := by
  cases k with
  | zero => omega
  | succ j => rw [Nat.pow_succ]; omega

/-- TEOREMA 2: el denominador 3^S - 2^k no se anula nunca con k >= 1
    (paridad: 3^S impar, 2^k par).  Es la nota de la base "3^S = 2^k solo
    con S = k = 0", demostrada. -/
theorem denominador_no_nulo (k s : Nat) (hk : 1 ≤ k) : 3 ^ s ≠ 2 ^ k := by
  have o := impar_pow3 s
  have e := par_pow2 k hk
  omega

/-- Cancelacion lineal en Nat, sin restas: si a*m + c = (a+d)*m + r para dos
    valores de m con d > 0, los dos m coinciden. -/
theorem cancel (a d c r m₁ m₂ : Nat) (hd : 0 < d)
    (h₁ : a * m₁ + c = (a + d) * m₁ + r)
    (h₂ : a * m₂ + c = (a + d) * m₂ + r) : m₁ = m₂ := by
  rw [Nat.add_mul, Nat.add_assoc] at h₁ h₂
  have e₁ : c = d * m₁ + r := Nat.add_left_cancel h₁
  have e₂ : c = d * m₂ + r := Nat.add_left_cancel h₂
  have e₃ : d * m₁ = d * m₂ := Nat.add_right_cancel (e₁.symm.trans e₂)
  exact Nat.eq_of_mul_eq_mul_left hd e₃

/-- TEOREMA 3 — EL ENUNCIADO A27: para k >= 1, por cada resto r hay COMO
    MUCHO UN candidato m de ciclo de longitud k.  (Sobre Nat: m >= 0.) -/
theorem a_lo_sumo_un_candidato (k : Nat) (hk : 1 ≤ k) (r m₁ m₂ : Nat)
    (h₁ : Titer k (2 ^ k * m₁ + r) = 2 ^ k * m₁ + r)
    (h₂ : Titer k (2 ^ k * m₂ + r) = 2 ^ k * m₂ + r) : m₁ = m₂ := by
  rw [terras k m₁ r] at h₁
  rw [terras k m₂ r] at h₂
  have hne : (3:Nat) ^ S k r ≠ 2 ^ k := denominador_no_nulo k (S k r) hk
  by_cases hlt : 3 ^ S k r < 2 ^ k
  · -- lado de los ciclos positivos: 2^k > 3^S
    have hd : (2:Nat) ^ k = 3 ^ S k r + (2 ^ k - 3 ^ S k r) := by omega
    rw [hd] at h₁ h₂
    exact cancel (3 ^ S k r) (2 ^ k - 3 ^ S k r) (Titer k r) r m₁ m₂
      (by omega) h₁ h₂
  · -- lado 3^S > 2^k
    have hgt : (2:Nat) ^ k < 3 ^ S k r := by omega
    have hd : (3:Nat) ^ S k r = 2 ^ k + (3 ^ S k r - 2 ^ k) := by omega
    rw [hd] at h₁ h₂
    exact cancel (2 ^ k) (3 ^ S k r - 2 ^ k) r (Titer k r) m₁ m₂
      (by omega) h₁.symm h₂.symm

/-- TEOREMA 4 — la version "por clase residual" literal: dos numeros
    k-periodicos con el mismo resto mod 2^k son el mismo numero. -/
theorem unico_por_clase (k : Nat) (hk : 1 ≤ k) (n₁ n₂ : Nat)
    (hmod : n₁ % 2 ^ k = n₂ % 2 ^ k)
    (hc₁ : Titer k n₁ = n₁) (hc₂ : Titer k n₂ = n₂) : n₁ = n₂ := by
  have e₁ : 2 ^ k * (n₁ / 2 ^ k) + n₁ % 2 ^ k = n₁ := Nat.div_add_mod n₁ (2 ^ k)
  have e₂ : 2 ^ k * (n₂ / 2 ^ k) + n₂ % 2 ^ k = n₂ := Nat.div_add_mod n₂ (2 ^ k)
  rw [← e₁] at hc₁
  rw [← e₂, ← hmod] at hc₂
  have hm := a_lo_sumo_un_candidato k hk (n₁ % 2 ^ k) (n₁ / 2 ^ k) (n₂ / 2 ^ k)
    hc₁ hc₂
  calc n₁ = 2 ^ k * (n₁ / 2 ^ k) + n₁ % 2 ^ k := e₁.symm
    _ = 2 ^ k * (n₂ / 2 ^ k) + n₂ % 2 ^ k := by rw [hm, hmod]
    _ = n₂ := e₂

/-- TEOREMA 5a — la forma cerrada, rama 2^k > 3^S (donde viven los ciclos
    positivos de 3n+1): m = (T^k(r) - r) / (2^k - 3^S). -/
theorem forma_cerrada_pos (k r m : Nat) (hlt : 3 ^ S k r < 2 ^ k)
    (h : Titer k (2 ^ k * m + r) = 2 ^ k * m + r) :
    m = (Titer k r - r) / (2 ^ k - 3 ^ S k r) := by
  rw [terras k m r] at h
  have key : (2 ^ k - 3 ^ S k r) * m = Titer k r - r := by
    rw [Nat.sub_mul]; omega
  have hD : 0 < 2 ^ k - 3 ^ S k r := by omega
  rw [← key]
  exact (Nat.mul_div_cancel_left m hD).symm

/-- TEOREMA 5b — la rama 3^S > 2^k, que es la formula LITERAL del enunciado:
    m = (r - T^k(r)) / (3^{S(r)} - 2^k).  (En Z las dos ramas son el mismo
    cociente, porque numerador y denominador cambian de signo juntos.) -/
theorem forma_cerrada_neg (k r m : Nat) (hgt : 2 ^ k < 3 ^ S k r)
    (h : Titer k (2 ^ k * m + r) = 2 ^ k * m + r) :
    m = (r - Titer k r) / (3 ^ S k r - 2 ^ k) := by
  rw [terras k m r] at h
  have key : (3 ^ S k r - 2 ^ k) * m = r - Titer k r := by
    rw [Nat.sub_mul]; omega
  have hD : 0 < 3 ^ S k r - 2 ^ k := by omega
  rw [← key]
  exact (Nat.mul_div_cancel_left m hD).symm

/-- BORDE k = 0: el enunciado es FALSO sin la hipotesis k >= 1.
    Con k = 0 todo n es "ciclo de longitud 0" (T^0 = id), asi que la clase
    unica mod 2^0 = 1 tiene infinitos candidatos; aqui dos concretos. -/
theorem borde_k0 :
    Titer 0 (2 ^ 0 * 3 + 0) = 2 ^ 0 * 3 + 0 ∧
    Titer 0 (2 ^ 0 * 7 + 0) = 2 ^ 0 * 7 + 0 ∧
    (3:Nat) ≠ 7 ∧ (3:Nat) ^ S 0 0 - 2 ^ 0 = 0 := by decide

/-- CASO CONOCIDO 1 (nucleo, no #eval): el ciclo trivial {1,2} del atajo.
    k = 2: 1 -> 2 -> 1 y 2 -> 1 -> 2, con S = 1 en los dos restos, y la
    formula cerrada da m = 0 en los dos. -/
theorem caso_ciclo_trivial :
    Titer 2 1 = 1 ∧ Titer 2 2 = 2 ∧
    S 2 1 = 1 ∧ S 2 2 = 1 ∧
    3 ^ S 2 1 < 2 ^ 2 ∧
    (Titer 2 1 - 1) / (2 ^ 2 - 3 ^ S 2 1) = 0 ∧
    (Titer 2 2 - 2) / (2 ^ 2 - 3 ^ S 2 2) = 0 := by decide

/-- CASO CONOCIDO 2: la trayectoria corta del 7 en el atajo:
    7 -> 11 -> 17 -> 26 -> 13 -> 20, con 4 impares en 5 pasos. -/
theorem caso_7 : Titer 5 7 = 20 ∧ S 5 7 = 4 := by decide

/-- CASO CONOCIDO 3: el 221 del repo: B = 73 pasos del atajo hasta el 1,
    con A = 41 de ellos impares. -/
theorem caso_221 : Titer 73 221 = 1 ∧ S 73 221 = 41 := by decide

/-- Y el unico n <= 100 con T^2(n) = n y n = 4m+1 es el 1 (m = 0): la
    unicidad, mirada en concreto sobre la clase r = 1 mod 4. -/
theorem unicidad_concreta_r1 :
    ∀ m ≤ 25, Titer 2 (4 * m + 1) = 4 * m + 1 → m = 0 := by decide

#print axioms terras
#print axioms denominador_no_nulo
#print axioms a_lo_sumo_un_candidato
#print axioms unico_por_clase
#print axioms forma_cerrada_pos
#print axioms forma_cerrada_neg
#print axioms borde_k0
#print axioms caso_ciclo_trivial
#print axioms caso_7
#print axioms caso_221
#print axioms unicidad_concreta_r1

end A27
