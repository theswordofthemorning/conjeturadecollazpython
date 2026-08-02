/-
  ITEM A14 (agente 1, LEAN) — "el espejo en base b tiene puntos fijos exactamente
  (b/2)*b^m si b es par, y NI UNO si b es impar".

  El espejo en base b es el complemento: espejo_b(n) = b^(cifras de n en base b) - n.
  (Es el unico mapa compatible con la nota de la ficha "el enunciado sale de
  n = b^k/2" y con los puntos fijos conocidos 5, 50, 500 en base 10:
  10^1-5=5, 10^2-50=50, 10^3-500=500.)

  Aqui se define el mapa desde cero (sin mirar ningun fichero del repo), se
  demuestra el enunciado para todo b y todo n >= 1, y se comprueban casos
  concretos con `decide` (revisados por el nucleo, no por #eval).

  NO interviene ningun mapa de Collatz (ni clasico, ni atajo, ni 3n-1).
-/

set_option maxRecDepth 40000

/-- Numero de cifras de `n` en base `b`, con combustible estructural para que
    el nucleo pueda evaluarlo con `decide`. Con combustible suficiente
    (fuel >= n basta) devuelve el numero de cifras de verdad. -/
def numDigitsAux (b : Nat) : Nat → Nat → Nat
  | _, 0 => 1
  | n, fuel + 1 => if b ≤ 1 ∨ n < b then 1 else 1 + numDigitsAux b (n / b) fuel

/-- Numero de cifras de `n` en base `b` (fuel = n es siempre suficiente). -/
def numDigits (b n : Nat) : Nat := numDigitsAux b n n

/-- EL MAPA: el espejo (complemento) en base b. -/
def espejo (b n : Nat) : Nat := b ^ numDigits b n - n

-- ---------------------------------------------------------------------------
-- Propiedades de numDigits
-- ---------------------------------------------------------------------------

theorem numDigitsAux_pos (b n fuel : Nat) : 1 ≤ numDigitsAux b n fuel := by
  cases fuel with
  | zero =>
    simp only [numDigitsAux]
    omega
  | succ f =>
    simp only [numDigitsAux]
    split
    · omega
    · omega

theorem numDigits_pos (b n : Nat) : 1 ≤ numDigits b n := numDigitsAux_pos b n n

/-- Con combustible suficiente, numDigitsAux devuelve el numero de cifras:
    si b^m <= n < b^(m+1) entonces la respuesta es m+1. -/
theorem numDigitsAux_eq (b : Nat) (hb : 2 ≤ b) :
    ∀ fuel n m, n ≤ fuel → b ^ m ≤ n → n < b ^ (m + 1) →
      numDigitsAux b n fuel = m + 1 := by
  intro fuel
  induction fuel with
  | zero =>
    intro n m hn hl _
    have hp : 0 < b ^ m := Nat.pow_pos (by omega)
    omega
  | succ f ih =>
    intro n m hn hl hu
    cases m with
    | zero =>
      have hub : n < b := by
        have h1 : b ^ (0 + 1) = b := by
          have := Nat.pow_one b
          omega
        omega
      simp only [numDigitsAux]
      rw [if_pos (Or.inr hub)]
    | succ m' =>
      have hbp : 0 < b ^ m' := Nat.pow_pos (by omega)
      have h1 : b ≤ b ^ (m' + 1) := Nat.le_self_pow (by omega) b
      have hbn : b ≤ n := by omega
      have hcond : ¬(b ≤ 1 ∨ n < b) := by omega
      simp only [numDigitsAux]
      rw [if_neg hcond]
      have hdiv1 : b ^ m' ≤ n / b := by
        rw [Nat.le_div_iff_mul_le (by omega : 0 < b)]
        rw [← Nat.pow_succ]
        exact hl
      have hdiv2 : n / b < b ^ (m' + 1) := by
        rw [Nat.div_lt_iff_lt_mul (by omega : 0 < b)]
        rw [← Nat.pow_succ]
        exact hu
      have hfuel : n / b ≤ f := by
        have hlt : n / b < n := Nat.div_lt_self (by omega) (by omega)
        omega
      rw [ih (n / b) m' hfuel hdiv1 hdiv2]
      omega

/-- El numero de cifras caracterizado por el sandwich b^m <= n < b^(m+1). -/
theorem numDigits_eq (b n m : Nat) (hb : 2 ≤ b)
    (hl : b ^ m ≤ n) (hu : n < b ^ (m + 1)) : numDigits b n = m + 1 :=
  numDigitsAux_eq b hb n n m (Nat.le_refl n) hl hu

-- ---------------------------------------------------------------------------
-- Caso b IMPAR: ni un punto fijo
-- ---------------------------------------------------------------------------

theorem odd_pow (b k : Nat) (h : b % 2 = 1) : b ^ k % 2 = 1 := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Nat.pow_succ, Nat.mul_mod, ih, h]

/-- TEOREMA (mitad impar del enunciado): si b es impar, el espejo en base b
    no tiene NINGUN punto fijo n >= 1. Vale para todo b impar (1, 3, 5, ...)
    y no necesita siquiera acotar el numero de cifras. -/
theorem espejo_fix_odd (b n : Nat) (hodd : b % 2 = 1) (hn : 1 ≤ n) :
    espejo b n ≠ n := by
  intro hfix
  unfold espejo at hfix
  have h := odd_pow b (numDigits b n) hodd
  -- si b^L >= n, el punto fijo exige b^L = 2n (par) contra b^L impar;
  -- si b^L < n, la resta truncada da 0 = n contra n >= 1. omega cierra ambos.
  omega

-- ---------------------------------------------------------------------------
-- Caso b PAR: los puntos fijos son exactamente (b/2) * b^m
-- ---------------------------------------------------------------------------

theorem cancel_half (c P : Nat) : 2 * c * P - c * P = c * P := by
  have h : 2 * c * P = 2 * (c * P) := Nat.mul_assoc 2 c P
  omega

/-- TEOREMA (mitad par del enunciado): si b es par (b >= 2), los puntos fijos
    del espejo en base b con n >= 1 son EXACTAMENTE los n = (b/2) * b^m. -/
theorem espejo_fix_even (b n : Nat) (hb : 2 ≤ b) (hev : b % 2 = 0) (hn : 1 ≤ n) :
    espejo b n = n ↔ ∃ m, n = b / 2 * b ^ m := by
  constructor
  · -- punto fijo -> tiene la forma (b/2)*b^m con m = L-1
    intro hfix
    unfold espejo at hfix
    have hL : 1 ≤ numDigits b n := numDigits_pos b n
    have h2 : b ^ numDigits b n = 2 * n := by omega
    refine ⟨numDigits b n - 1, ?_⟩
    have hLs : numDigits b n = numDigits b n - 1 + 1 := by omega
    have hps : b ^ (numDigits b n - 1 + 1) = b ^ (numDigits b n - 1) * b :=
      Nat.pow_succ b (numDigits b n - 1)
    have h2' : b ^ (numDigits b n - 1) * b = 2 * n := by
      rw [← hps, ← hLs]; exact h2
    have hb2 : b = 2 * (b / 2) := by omega
    have hbb : b ^ (numDigits b n - 1) * b = b ^ (numDigits b n - 1) * (2 * (b / 2)) :=
      congrArg (fun x => b ^ (numDigits b n - 1) * x) hb2
    have hcomm : b ^ (numDigits b n - 1) * (2 * (b / 2))
        = 2 * (b / 2) * b ^ (numDigits b n - 1) := Nat.mul_comm _ _
    have hassoc : 2 * (b / 2) * b ^ (numDigits b n - 1)
        = 2 * (b / 2 * b ^ (numDigits b n - 1)) :=
      Nat.mul_assoc 2 (b / 2) (b ^ (numDigits b n - 1))
    have h2'' : 2 * (b / 2 * b ^ (numDigits b n - 1)) = 2 * n := by
      rw [← hassoc, ← hcomm, ← hbb]; exact h2'
    have hcancel := Nat.eq_of_mul_eq_mul_left (by omega : 0 < 2) h2''
    omega
  · -- (b/2)*b^m es punto fijo: tiene m+1 cifras y b^(m+1) - el = el
    intro hex
    cases hex with
    | intro m hm =>
      have hc : 1 ≤ b / 2 := by omega
      have hpm : 0 < b ^ m := Nat.pow_pos (by omega)
      have hl : b ^ m ≤ b / 2 * b ^ m := by
        have h1 : 1 * b ^ m ≤ b / 2 * b ^ m := Nat.mul_le_mul_right (b ^ m) hc
        omega
      have hu : b / 2 * b ^ m < b ^ (m + 1) := by
        have hps : b ^ (m + 1) = b ^ m * b := Nat.pow_succ b m
        have hlt : b ^ m * (b / 2) < b ^ m * b :=
          (Nat.mul_lt_mul_left hpm).mpr (by omega : b / 2 < b)
        have hcomm : b / 2 * b ^ m = b ^ m * (b / 2) := Nat.mul_comm _ _
        omega
      have hL : numDigits b (b / 2 * b ^ m) = m + 1 := numDigits_eq b _ m hb hl hu
      rw [hm]
      unfold espejo
      rw [hL]
      have hps : b ^ (m + 1) = b ^ m * b := Nat.pow_succ b m
      have hb2 : b = 2 * (b / 2) := by omega
      have hbb : b ^ m * b = b ^ m * (2 * (b / 2)) :=
        congrArg (fun x => b ^ m * x) hb2
      have hkey : b ^ m * (2 * (b / 2)) = 2 * (b / 2) * b ^ m := Nat.mul_comm _ _
      have hch := cancel_half (b / 2) (b ^ m)
      omega

-- ---------------------------------------------------------------------------
-- Casos conocidos comprobados por el NUCLEO (by decide, no #eval)
-- ---------------------------------------------------------------------------

-- los tres puntos fijos conocidos de base 10 (los "5, 50, 500" del repo)
theorem caso_base10_5 : espejo 10 5 = 5 := by decide
theorem caso_base10_50 : espejo 10 50 = 50 := by decide
theorem caso_base10_500 : espejo 10 500 = 500 := by decide

-- un no-fijo de control en base 10
theorem caso_base10_7 : espejo 10 7 = 3 := by decide

-- base 2: los fijos son (2/2)*2^m = las potencias de 2
theorem caso_base2_64 : espejo 2 64 = 64 := by decide

-- base 16: los fijos son 8*16^m
theorem caso_base16_8 : espejo 16 8 = 8 := by decide
theorem caso_base16_128 : espejo 16 128 = 128 := by decide

-- barrido exhaustivo n = 1..999 en base 10: los fijos son EXACTAMENTE 5, 50, 500
theorem barrido_base10 :
    ∀ n, n < 1000 → 1 ≤ n → (espejo 10 n = n ↔ (n = 5 ∨ n = 50 ∨ n = 500)) := by
  decide

-- barridos exhaustivos en bases impares: ni un punto fijo
theorem barrido_base3 : ∀ n, n < 1000 → 1 ≤ n → espejo 3 n ≠ n := by decide
theorem barrido_base7 : ∀ n, n < 500 → 1 ≤ n → espejo 7 n ≠ n := by decide

-- barrido exhaustivo en base 2: los fijos son exactamente las potencias de 2
theorem barrido_base2 :
    ∀ n, n < 300 → 1 ≤ n →
      (espejo 2 n = n ↔
        (n = 1 ∨ n = 2 ∨ n = 4 ∨ n = 8 ∨ n = 16 ∨ n = 32 ∨ n = 64 ∨ n = 128 ∨ n = 256)) := by
  decide

-- barrido en base 6 (par no potencia de 2): fijos exactamente 3*6^m
theorem barrido_base6 :
    ∀ n, n < 700 → 1 ≤ n → (espejo 6 n = n ↔ (n = 3 ∨ n = 18 ∨ n = 108 ∨ n = 648)) := by
  decide

-- ---------------------------------------------------------------------------
-- Control de axiomas
-- ---------------------------------------------------------------------------

#print axioms espejo_fix_even
#print axioms espejo_fix_odd
#print axioms numDigits_eq
#print axioms caso_base10_5
#print axioms barrido_base10
#print axioms barrido_base3
#print axioms barrido_base2
#print axioms barrido_base6
