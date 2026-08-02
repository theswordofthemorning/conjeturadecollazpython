/-
  ITEM A61 -- verificacion en Lean 4 (nucleo, sin Mathlib).

  ENUNCIADO: en un ciclo de 3n+1 la C de la identidad es POSITIVA,
  luego B/A > log2(3); en uno de 3n-1 es negativa y B/A < log2(3).

  MAPA: el CLASICO en las dos variantes -- par: n/2; impar: 3n+1 (resp. 3n-1).
  A = numero de pasos impares, B = numero de divisiones.
  (Los conteos A,B son los mismos con el atajo, pero aqui se itera el clasico.)

  IDENTIDAD (convenio del enunciado): tras k pasos desde n0,
      3n+1:  2^B * n_k = 3^A * n0 + C,   C >= 0  (aqui C : Nat)
      3n-1:  2^B * n_k = 3^A * n0 - D,   D >= 0  (aqui se arrastra D = -C : Nat,
             y la identidad se escribe SIN resta: 2^B * n_k + D = 3^A * n0)

  FORMALIZACION DE  B/A > log2(3):  como  2^B > 3^A  (equivalente exacto:
  B*ln2 > A*ln3 sii 2^B > 3^A, con A >= 1 que aqui se DEMUESTRA, no se supone).
  Igual  B/A < log2(3)  sii  2^B < 3^A.  Asi no hacen falta reales.

  HIPOTESIS EXPLICITAS (el enunciado las deja implicitas): n0 >= 1 y k >= 1.
  Con n0 = 0 el "ciclo" 0 -> 0 tiene A = 0, C = 0 y la mitad 3n-1 seria falsa.
-/

set_option maxRecDepth 40000

structure Est where
  n : Nat
  a : Nat
  b : Nat
  c : Nat
deriving DecidableEq, Repr

/-- Un paso del mapa CLASICO 3n+1, arrastrando (A, B, C). -/
def pasoP (s : Est) : Est :=
  if s.n % 2 = 0 then
    { s with n := s.n / 2, b := s.b + 1 }
  else
    { n := 3 * s.n + 1, a := s.a + 1, b := s.b, c := 3 * s.c + 2 ^ s.b }

def runP (n0 : Nat) : Nat → Est
  | 0 => ⟨n0, 0, 0, 0⟩
  | k + 1 => pasoP (runP n0 k)

/-- Un paso del mapa CLASICO 3n-1, arrastrando (A, B, D) con D = -C >= 0.
    La resta 3*n - 1 solo se ejecuta con n impar (n >= 1), asi que no trunca. -/
def pasoM (s : Est) : Est :=
  if s.n % 2 = 0 then
    { s with n := s.n / 2, b := s.b + 1 }
  else
    { n := 3 * s.n - 1, a := s.a + 1, b := s.b, c := 3 * s.c + 2 ^ s.b }

def runM (n0 : Nat) : Nat → Est
  | 0 => ⟨n0, 0, 0, 0⟩
  | k + 1 => pasoM (runM n0 k)

/- ============ INVARIANTES (identidad de Terras, las dos firmas) ============ -/

theorem paso_conservaP (s : Est) (n0 : Nat)
    (h : 2 ^ s.b * s.n = 3 ^ s.a * n0 + s.c) :
    2 ^ (pasoP s).b * (pasoP s).n = 3 ^ (pasoP s).a * n0 + (pasoP s).c := by
  unfold pasoP
  by_cases hp : s.n % 2 = 0
  · rw [if_pos hp]
    show 2 ^ (s.b + 1) * (s.n / 2) = 3 ^ s.a * n0 + s.c
    have h2 : 2 * (s.n / 2) = s.n := by omega
    calc 2 ^ (s.b + 1) * (s.n / 2)
        = 2 ^ s.b * (2 * (s.n / 2)) := by rw [Nat.pow_succ, Nat.mul_assoc]
      _ = 2 ^ s.b * s.n := by rw [h2]
      _ = 3 ^ s.a * n0 + s.c := h
  · rw [if_neg hp]
    show 2 ^ s.b * (3 * s.n + 1) = 3 ^ (s.a + 1) * n0 + (3 * s.c + 2 ^ s.b)
    have e1 : 2 ^ s.b * (3 * s.n + 1) = 3 * (2 ^ s.b * s.n) + 2 ^ s.b := by
      rw [Nat.mul_add, Nat.mul_one, Nat.mul_left_comm]
    have e3 : 3 ^ (s.a + 1) * n0 = 3 * (3 ^ s.a * n0) := by
      rw [Nat.pow_succ, Nat.mul_comm (3 ^ s.a) 3, Nat.mul_assoc]
    omega

theorem invP (n0 : Nat) :
    ∀ k, 2 ^ (runP n0 k).b * (runP n0 k).n = 3 ^ (runP n0 k).a * n0 + (runP n0 k).c := by
  intro k
  induction k with
  | zero => show 2 ^ 0 * n0 = 3 ^ 0 * n0 + 0; simp
  | succ k ih => exact paso_conservaP (runP n0 k) n0 ih

theorem paso_conservaM (s : Est) (n0 : Nat)
    (h : 2 ^ s.b * s.n + s.c = 3 ^ s.a * n0) :
    2 ^ (pasoM s).b * (pasoM s).n + (pasoM s).c = 3 ^ (pasoM s).a * n0 := by
  unfold pasoM
  by_cases hp : s.n % 2 = 0
  · rw [if_pos hp]
    show 2 ^ (s.b + 1) * (s.n / 2) + s.c = 3 ^ s.a * n0
    have h2 : 2 * (s.n / 2) = s.n := by omega
    calc 2 ^ (s.b + 1) * (s.n / 2) + s.c
        = 2 ^ s.b * (2 * (s.n / 2)) + s.c := by rw [Nat.pow_succ, Nat.mul_assoc]
      _ = 2 ^ s.b * s.n + s.c := by rw [h2]
      _ = 3 ^ s.a * n0 := h
  · rw [if_neg hp]
    show 2 ^ s.b * (3 * s.n - 1) + (3 * s.c + 2 ^ s.b) = 3 ^ (s.a + 1) * n0
    -- n impar: la PARIDAD da n >= 1, y la resta 3n - 1 no trunca
    have hodd : s.n % 2 = 1 := by omega
    have hsub : (3 * s.n - 1) + 1 = 3 * s.n := by omega
    have e1 : 2 ^ s.b * (3 * s.n - 1) + 2 ^ s.b = 2 ^ s.b * (3 * s.n) := by
      calc 2 ^ s.b * (3 * s.n - 1) + 2 ^ s.b
          = 2 ^ s.b * ((3 * s.n - 1) + 1) := by rw [Nat.mul_add, Nat.mul_one]
        _ = 2 ^ s.b * (3 * s.n) := by rw [hsub]
    have e2 : 2 ^ s.b * (3 * s.n) = 3 * (2 ^ s.b * s.n) := by
      rw [Nat.mul_left_comm]
    have e3 : 3 ^ (s.a + 1) * n0 = 3 * (3 ^ s.a * n0) := by
      rw [Nat.pow_succ, Nat.mul_comm (3 ^ s.a) 3, Nat.mul_assoc]
    omega

theorem invM (n0 : Nat) :
    ∀ k, 2 ^ (runM n0 k).b * (runM n0 k).n + (runM n0 k).c = 3 ^ (runM n0 k).a * n0 := by
  intro k
  induction k with
  | zero => show 2 ^ 0 * n0 + 0 = 3 ^ 0 * n0; simp
  | succ k ih => exact paso_conservaM (runM n0 k) n0 ih

/- ============ CONTABILIDAD: a + b = k, y el signo de C ============ -/

theorem abP (n0 : Nat) : ∀ k, (runP n0 k).a + (runP n0 k).b = k := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    show (pasoP (runP n0 k)).a + (pasoP (runP n0 k)).b = k + 1
    unfold pasoP
    by_cases hp : (runP n0 k).n % 2 = 0
    · rw [if_pos hp]
      show (runP n0 k).a + ((runP n0 k).b + 1) = k + 1
      omega
    · rw [if_neg hp]
      show ((runP n0 k).a + 1) + (runP n0 k).b = k + 1
      omega

theorem abM (n0 : Nat) : ∀ k, (runM n0 k).a + (runM n0 k).b = k := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    show (pasoM (runM n0 k)).a + (pasoM (runM n0 k)).b = k + 1
    unfold pasoM
    by_cases hp : (runM n0 k).n % 2 = 0
    · rw [if_pos hp]
      show (runM n0 k).a + ((runM n0 k).b + 1) = k + 1
      omega
    · rw [if_neg hp]
      show ((runM n0 k).a + 1) + (runM n0 k).b = k + 1
      omega

/-- Sin pasos impares no hay mas-uno que sumar: A = 0 implica C = 0 (3n+1). -/
theorem c0P (n0 : Nat) : ∀ k, (runP n0 k).a = 0 → (runP n0 k).c = 0 := by
  intro k
  induction k with
  | zero => intro _; rfl
  | succ k ih =>
    show (pasoP (runP n0 k)).a = 0 → (pasoP (runP n0 k)).c = 0
    unfold pasoP
    by_cases hp : (runP n0 k).n % 2 = 0
    · rw [if_pos hp]; intro h; exact ih h
    · rw [if_neg hp]
      intro h
      have h2 : (runP n0 k).a + 1 = 0 := h
      exact absurd h2 (by omega)

theorem c0M (n0 : Nat) : ∀ k, (runM n0 k).a = 0 → (runM n0 k).c = 0 := by
  intro k
  induction k with
  | zero => intro _; rfl
  | succ k ih =>
    show (pasoM (runM n0 k)).a = 0 → (pasoM (runM n0 k)).c = 0
    unfold pasoM
    by_cases hp : (runM n0 k).n % 2 = 0
    · rw [if_pos hp]; intro h; exact ih h
    · rw [if_neg hp]
      intro h
      have h2 : (runM n0 k).a + 1 = 0 := h
      exact absurd h2 (by omega)

/-- LA MITAD "C POSITIVA": con al menos un paso impar, C >= 1 (mapa 3n+1). -/
theorem cposP (n0 : Nat) : ∀ k, 1 ≤ (runP n0 k).a → 1 ≤ (runP n0 k).c := by
  intro k
  induction k with
  | zero =>
    intro h
    have h2 : (1 : Nat) ≤ 0 := h
    omega
  | succ k ih =>
    show 1 ≤ (pasoP (runP n0 k)).a → 1 ≤ (pasoP (runP n0 k)).c
    unfold pasoP
    by_cases hp : (runP n0 k).n % 2 = 0
    · rw [if_pos hp]; intro h; exact ih h
    · rw [if_neg hp]
      intro _
      show 1 ≤ 3 * (runP n0 k).c + 2 ^ (runP n0 k).b
      have h2 : 1 ≤ 2 ^ (runP n0 k).b := Nat.one_le_two_pow
      omega

/-- LA MITAD "C NEGATIVA": con al menos un paso impar, D = -C >= 1 (3n-1). -/
theorem cposM (n0 : Nat) : ∀ k, 1 ≤ (runM n0 k).a → 1 ≤ (runM n0 k).c := by
  intro k
  induction k with
  | zero =>
    intro h
    have h2 : (1 : Nat) ≤ 0 := h
    omega
  | succ k ih =>
    show 1 ≤ (pasoM (runM n0 k)).a → 1 ≤ (pasoM (runM n0 k)).c
    unfold pasoM
    by_cases hp : (runM n0 k).n % 2 = 0
    · rw [if_pos hp]; intro h; exact ih h
    · rw [if_neg hp]
      intro _
      show 1 ≤ 3 * (runM n0 k).c + 2 ^ (runM n0 k).b
      have h2 : 1 ≤ 2 ^ (runM n0 k).b := Nat.one_le_two_pow
      omega

/- ============ EN UN CICLO HAY ALGUN PASO IMPAR (A >= 1) ============ -/

theorem aposP (n0 k : Nat) (hn : 1 ≤ n0) (hk : 1 ≤ k)
    (hc : (runP n0 k).n = n0) : 1 ≤ (runP n0 k).a := by
  by_cases ha : (runP n0 k).a = 0
  · exfalso
    have hc0 := c0P n0 k ha
    have hid := invP n0 k
    rw [hc, ha, hc0] at hid
    simp at hid
    have hab := abP n0 k
    have hb : 1 ≤ (runP n0 k).b := by omega
    have h2 : 2 ≤ 2 ^ (runP n0 k).b := by
      calc (2 : Nat) = 2 ^ 1 := rfl
        _ ≤ 2 ^ (runP n0 k).b := Nat.pow_le_pow_right (by omega) hb
    have h3 : 2 * n0 ≤ 2 ^ (runP n0 k).b * n0 := Nat.mul_le_mul_right n0 h2
    omega
  · omega

theorem aposM (n0 k : Nat) (hn : 1 ≤ n0) (hk : 1 ≤ k)
    (hc : (runM n0 k).n = n0) : 1 ≤ (runM n0 k).a := by
  by_cases ha : (runM n0 k).a = 0
  · exfalso
    have hc0 := c0M n0 k ha
    have hid := invM n0 k
    rw [hc, ha, hc0] at hid
    simp at hid
    have hab := abM n0 k
    have hb : 1 ≤ (runM n0 k).b := by omega
    have h2 : 2 ≤ 2 ^ (runM n0 k).b := by
      calc (2 : Nat) = 2 ^ 1 := rfl
        _ ≤ 2 ^ (runM n0 k).b := Nat.pow_le_pow_right (by omega) hb
    have h3 : 2 * n0 ≤ 2 ^ (runM n0 k).b * n0 := Nat.mul_le_mul_right n0 h2
    omega
  · omega

/- ============ LOS DOS TEOREMAS DEL ENUNCIADO ============ -/

/-- CICLO DE 3n+1: C es positiva (C >= 1). -/
theorem C_positiva_en_ciclo_3n1 (n0 k : Nat) (hn : 1 ≤ n0) (hk : 1 ≤ k)
    (hc : (runP n0 k).n = n0) : 1 ≤ (runP n0 k).c :=
  cposP n0 k (aposP n0 k hn hk hc)

/-- CICLO DE 3n+1: 2^B > 3^A, o sea B/A > log2(3). -/
theorem ciclo_3n1_encima (n0 k : Nat) (hn : 1 ≤ n0) (hk : 1 ≤ k)
    (hc : (runP n0 k).n = n0) :
    3 ^ (runP n0 k).a < 2 ^ (runP n0 k).b := by
  have ha := aposP n0 k hn hk hc
  have hcp := cposP n0 k ha
  have hid := invP n0 k
  rw [hc] at hid
  by_cases hle : 2 ^ (runP n0 k).b ≤ 3 ^ (runP n0 k).a
  · exfalso
    have h3 : 2 ^ (runP n0 k).b * n0 ≤ 3 ^ (runP n0 k).a * n0 :=
      Nat.mul_le_mul_right n0 hle
    omega
  · omega

/-- CICLO DE 3n-1: C es negativa (D = -C >= 1). -/
theorem C_negativa_en_ciclo_3nm1 (n0 k : Nat) (hn : 1 ≤ n0) (hk : 1 ≤ k)
    (hc : (runM n0 k).n = n0) : 1 ≤ (runM n0 k).c :=
  cposM n0 k (aposM n0 k hn hk hc)

/-- CICLO DE 3n-1: 2^B < 3^A, o sea B/A < log2(3). -/
theorem ciclo_3nm1_debajo (n0 k : Nat) (hn : 1 ≤ n0) (hk : 1 ≤ k)
    (hc : (runM n0 k).n = n0) :
    2 ^ (runM n0 k).b < 3 ^ (runM n0 k).a := by
  have ha := aposM n0 k hn hk hc
  have hcp := cposM n0 k ha
  have hid := invM n0 k
  rw [hc] at hid
  by_cases hle : 3 ^ (runM n0 k).a ≤ 2 ^ (runM n0 k).b
  · exfalso
    have h3 : 3 ^ (runM n0 k).a * n0 ≤ 2 ^ (runM n0 k).b * n0 :=
      Nat.mul_le_mul_right n0 hle
    omega
  · omega

/- ======== CASOS CONOCIDOS, COMPROBADOS POR EL NUCLEO (decide) ======== -/

-- El mapa es Collatz de verdad: 7 pasos del 27 dan 47 con A=3, B=4, C=23
-- (27 -> 82 -> 41 -> 124 -> 62 -> 31 -> 94 -> 47; 2^4*47 = 3^3*27 + 23).
theorem caso_27 : runP 27 7 = ⟨47, 3, 4, 23⟩ := by decide

-- El ciclo trivial de 3n+1: 1 -> 4 -> 2 -> 1, A=1, B=2, C=1, o sea 4 = 3 + 1.
theorem caso_ciclo_421 : runP 1 3 = ⟨1, 1, 2, 1⟩ := by decide
theorem caso_421_identidad : 2 ^ 2 * 1 = 3 ^ 1 * 1 + 1 := by decide
theorem caso_421_encima : 3 ^ (runP 1 3).a < 2 ^ (runP 1 3).b :=
  ciclo_3n1_encima 1 3 (by decide) (by decide) (by decide)

-- El ciclo [1,2] de 3n-1: 1 -> 2 -> 1, A=1, B=1, D=1, o sea 2 = 3 - 1.
theorem caso_ciclo_12 : runM 1 2 = ⟨1, 1, 1, 1⟩ := by decide
theorem caso_12_identidad : 2 ^ 1 * 1 + 1 = 3 ^ 1 * 1 := by decide
theorem caso_12_debajo : 2 ^ (runM 1 2).b < 3 ^ (runM 1 2).a :=
  ciclo_3nm1_debajo 1 2 (by decide) (by decide) (by decide)

-- El ciclo [5,14,7,20,10] de 3n-1: k=5, A=2, B=3, D=5; 8*5 + 5 = 9*5.
theorem caso_ciclo_5 : runM 5 5 = ⟨5, 2, 3, 5⟩ := by decide
theorem caso_5_debajo : 2 ^ (runM 5 5).b < 3 ^ (runM 5 5).a :=
  ciclo_3nm1_debajo 5 5 (by decide) (by decide) (by decide)

-- El ciclo de 18 pasos del 17 en 3n-1: k=18, A=7, B=11, D=(3^7-2^11)*17=2363.
theorem caso_ciclo_17 : runM 17 18 = ⟨17, 7, 11, 2363⟩ := by decide
theorem caso_17_debajo : 2 ^ (runM 17 18).b < 3 ^ (runM 17 18).a :=
  ciclo_3nm1_debajo 17 18 (by decide) (by decide) (by decide)

-- Contraste de mapas: la desigualdad de cada mitad es FALSA en el otro mapa.
-- (el ciclo trivial de 3n+1 NO cumple 2^B < 3^A: 4 < 3 es falso;
--  el ciclo [1,2] de 3n-1 NO cumple 3^A < 2^B: 3 < 2 es falso)
theorem contraste_P : ¬ (2 ^ (runP 1 3).b < 3 ^ (runP 1 3).a) := by decide
theorem contraste_M : ¬ (3 ^ (runM 1 2).a < 2 ^ (runM 1 2).b) := by decide

/- ============ CONTROL DE AXIOMAS ============ -/
#print axioms invP
#print axioms invM
#print axioms C_positiva_en_ciclo_3n1
#print axioms ciclo_3n1_encima
#print axioms C_negativa_en_ciclo_3nm1
#print axioms ciclo_3nm1_debajo
#print axioms caso_27
#print axioms caso_ciclo_421
#print axioms caso_ciclo_17
#print axioms contraste_P
