/-
  A23 — N(k+1) >= 2*N(k) siempre, luego la fraccion f(k) = N(k)/2^k es monotona.

  MAPA: el ATAJO.  T(n) = n/2 si n par, (3n+1)/2 si n impar.
  N(k) = numero de restos r en [0, 2^k) con  Sk k r = Sk k (r+1)  y  Tk k r = Tk k (r+1),
  donde r+1 se toma como ENTERO (en el borde r = 2^k - 1 el companero es 2^k).

  Sin Mathlib. Todo por el nucleo.
-/

set_option maxRecDepth 40000

/-- El mapa del ATAJO. -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- k iteraciones de T. -/
def Tk : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => Tk k (T n)

/-- Pasos impares en las primeras k iteraciones. -/
def Sk : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, n => n % 2 + Sk k (T n)

/-- Comprobacion de que T es el ATAJO y no otro mapa:
    3 -> 5 (el clasico daria 10, el 3n-1 daria 4), 6 -> 3, 5 -> 8, 1 -> 2. -/
theorem mapa_es_atajo : T 3 = 5 ∧ T 6 = 3 ∧ T 5 = 8 ∧ T 1 = 2 := by decide

/-- Caso conocido del repo: r=5, k=5 da T^5(5)=2, S=2 y T^5(6)=2, S=2. -/
theorem caso_conocido_5_6 : Tk 5 5 = 2 ∧ Sk 5 5 = 2 ∧ Tk 5 6 = 2 ∧ Sk 5 6 = 2 := by decide

-- ── Aritmetica de un paso ──────────────────────────────────────────────

theorem T_par (q r : Nat) (h : r % 2 = 0) : T (2 * q + r) = q + r / 2 := by
  unfold T
  split
  · omega
  · omega

theorem T_impar (q r : Nat) (h : r % 2 = 1) : T (2 * q + r) = 3 * q + T r := by
  unfold T
  split <;> split <;> omega

-- ── El lema de Terras (forma afin), para TODO m y TODO r ───────────────

theorem terras : ∀ (k m r : Nat),
    Sk k (2^k * m + r) = Sk k r ∧
    Tk k (2^k * m + r) = 3^(Sk k r) * m + Tk k r := by
  intro k
  induction k with
  | zero =>
    intro m r
    constructor
    · rfl
    · simp [Sk, Tk, Nat.pow_zero]
  | succ k ih =>
    intro m r
    have h2 : 2^(k+1) * m + r = 2 * (2^k * m) + r := by
      have hp : 2^(k+1) = 2^k * 2 := Nat.pow_succ 2 k
      rw [hp, Nat.mul_comm (2^k) 2, Nat.mul_assoc]
    by_cases hpar : r % 2 = 0
    case pos =>
      have hTr : T r = r / 2 := by unfold T; rw [if_pos hpar]
      have hT : T (2^(k+1) * m + r) = 2^k * m + T r := by
        rw [h2, T_par _ _ hpar, hTr]
      have hmod : (2^(k+1) * m + r) % 2 = r % 2 := by rw [h2]; omega
      constructor
      · show (2^(k+1) * m + r) % 2 + Sk k (T (2^(k+1) * m + r)) = r % 2 + Sk k (T r)
        rw [hT, (ih m (T r)).1, hmod]
      · show Tk k (T (2^(k+1) * m + r)) = 3^(r % 2 + Sk k (T r)) * m + Tk k (T r)
        rw [hT, (ih m (T r)).2, hpar]
        rw [Nat.zero_add]
    case neg =>
      have hpar1 : r % 2 = 1 := by omega
      have hT : T (2^(k+1) * m + r) = 2^k * (3 * m) + T r := by
        rw [h2, T_impar _ _ hpar1, ← Nat.mul_assoc, Nat.mul_comm 3 (2^k), Nat.mul_assoc]
      have hmod : (2^(k+1) * m + r) % 2 = r % 2 := by rw [h2]; omega
      constructor
      · show (2^(k+1) * m + r) % 2 + Sk k (T (2^(k+1) * m + r)) = r % 2 + Sk k (T r)
        rw [hT, (ih (3*m) (T r)).1, hmod]
      · show Tk k (T (2^(k+1) * m + r)) = 3^(r % 2 + Sk k (T r)) * m + Tk k (T r)
        rw [hT, (ih (3*m) (T r)).2, hpar1]
        have hp : (3:Nat)^(1 + Sk k (T r)) = 3^(Sk k (T r)) * 3 := by
          rw [Nat.add_comm]
          exact Nat.pow_succ 3 (Sk k (T r))
        rw [hp, Nat.mul_assoc]

-- ── Recursion por detras: la iteracion k+1 es T despues de las k primeras ──

theorem Tk_atras : ∀ (k n : Nat), Tk (k+1) n = T (Tk k n) := by
  intro k
  induction k with
  | zero => intro n; rfl
  | succ k ih =>
    intro n
    show Tk (k+1) (T n) = T (Tk (k+1) n)
    rw [ih (T n)]
    rfl

theorem Sk_atras : ∀ (k n : Nat), Sk (k+1) n = Sk k n + (Tk k n) % 2 := by
  intro k
  induction k with
  | zero => intro n; simp [Sk, Tk]
  | succ k ih =>
    intro n
    show n % 2 + Sk (k+1) (T n) = (n % 2 + Sk k (T n)) + (Tk k (T n)) % 2
    rw [ih (T n)]
    omega

-- ── El criterio de fusion (bueno = misma S y misma T^k que el vecino r+1) ──

def buena (k r : Nat) : Bool := (Sk k r == Sk k (r+1)) && (Tk k r == Tk k (r+1))

theorem buena_iff (k r : Nat) :
    buena k r = true ↔ Sk k r = Sk k (r+1) ∧ Tk k r = Tk k (r+1) := by
  simp [buena]

-- ── LOS DOS LEMAS DE SUBIDA: si r es buena a nivel k,
--    r y 2^k + r son buenas a nivel k+1 ──────────────────────────────────

theorem sube (k r : Nat) (h : buena k r = true) : buena (k+1) r = true := by
  rw [buena_iff] at h
  rw [buena_iff]
  constructor
  · rw [Sk_atras, Sk_atras, h.1, h.2]
  · rw [Tk_atras, Tk_atras, h.2]

theorem sube_espejo (k r : Nat) (h : buena k r = true) :
    buena (k+1) (2^k + r) = true := by
  rw [buena_iff] at h
  have hr1 : 2^k + r + 1 = 2^k + (r+1) := by omega
  have eT1 : Tk k (2^k + r) = 3^(Sk k r) + Tk k r := by
    have e := (terras k 1 r).2
    rw [Nat.mul_one, Nat.mul_one] at e
    exact e
  have eT2 : Tk k (2^k + (r+1)) = 3^(Sk k (r+1)) + Tk k (r+1) := by
    have e := (terras k 1 (r+1)).2
    rw [Nat.mul_one, Nat.mul_one] at e
    exact e
  have eS1 : Sk k (2^k + r) = Sk k r := by
    have e := (terras k 1 r).1
    rw [Nat.mul_one] at e
    exact e
  have eS2 : Sk k (2^k + (r+1)) = Sk k (r+1) := by
    have e := (terras k 1 (r+1)).1
    rw [Nat.mul_one] at e
    exact e
  have hTeq : Tk k (2^k + r) = Tk k (2^k + (r+1)) := by
    rw [eT1, eT2, h.1, h.2]
  rw [buena_iff]
  constructor
  · rw [hr1, Sk_atras, Sk_atras, eS1, eS2, h.1, hTeq]
  · rw [hr1, Tk_atras, Tk_atras, hTeq]

-- ── El conteo, y el teorema A23 ────────────────────────────────────────

/-- N(k) = cuantos restos de [0, 2^k) son buenos. -/
def N (k : Nat) : Nat := (List.range (2^k)).countP (fun r => buena k r)

/-- EL ENUNCIADO A23, primera mitad: N(k+1) >= 2*N(k), para TODO k. -/
theorem duplica (k : Nat) : 2 * N k ≤ N (k+1) := by
  unfold N
  have h2 : 2^(k+1) = 2^k * 2 := Nat.pow_succ 2 k
  have hsplit : 2^(k+1) = 2^k + 2^k := by omega
  rw [hsplit, List.range_add, List.countP_append, List.countP_map]
  have hA : (List.range (2^k)).countP (fun r => buena k r)
      ≤ (List.range (2^k)).countP (fun r => buena (k+1) r) :=
    List.countP_mono_left (fun r _ h => sube k r h)
  have hB : (List.range (2^k)).countP (fun r => buena k r)
      ≤ (List.range (2^k)).countP ((fun r => buena (k+1) r) ∘ (fun x => 2^k + x)) :=
    List.countP_mono_left (fun r _ h => sube_espejo k r h)
  omega

/-- EL ENUNCIADO A23, segunda mitad: la fraccion f(k) = N(k)/2^k es monotona,
    escrita en enteros: N(k) * 2^(k+1) <= N(k+1) * 2^k. -/
theorem fraccion_monotona (k : Nat) : N k * 2^(k+1) ≤ N (k+1) * 2^k := by
  have h := duplica k
  have h2 : 2^(k+1) = 2^k * 2 := Nat.pow_succ 2 k
  calc N k * 2^(k+1) = N k * (2^k * 2) := by rw [h2]
    _ = N k * 2^k * 2 := by rw [← Nat.mul_assoc]
    _ = 2 * (N k * 2^k) := Nat.mul_comm _ _
    _ = 2 * N k * 2^k := (Nat.mul_assoc 2 (N k) (2^k)).symm
    _ ≤ N (k+1) * 2^k := Nat.mul_le_mul h (Nat.le_refl _)

-- ── El borde r = 2^k - 1, demostrado y no supuesto ─────────────────────

theorem cero_fijo : ∀ (k : Nat), Sk k 0 = 0 ∧ Tk k 0 = 0 := by
  intro k
  induction k with
  | zero => exact ⟨rfl, rfl⟩
  | succ k ih =>
    have hT0 : T 0 = 0 := rfl
    constructor
    · show 0 % 2 + Sk k (T 0) = 0
      rw [hT0, ih.1]
    · show Tk k (T 0) = 0
      rw [hT0, ih.2]

theorem Sk_borde (k : Nat) : Sk k (2^k - 1) = k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have hpos := Nat.two_pow_pos k
    have h2 : 2^(k+1) = 2^k * 2 := Nat.pow_succ 2 k
    have hodd : (2^(k+1) - 1) % 2 = 1 := by omega
    have hT : T (2^(k+1) - 1) = 2^k * 2 + (2^k - 1) := by
      unfold T
      split
      · omega
      · omega
    show (2^(k+1) - 1) % 2 + Sk k (T (2^(k+1) - 1)) = k + 1
    rw [hT, (terras k 2 (2^k - 1)).1, ih]
    omega

theorem Sk_potencia (k : Nat) : Sk k (2^k) = 0 := by
  have e := (terras k 1 0).1
  rw [Nat.mul_one, Nat.add_zero] at e
  rw [e]
  exact (cero_fijo k).1

/-- El borde NUNCA es bueno (k >= 1): S del borde es k y S de su vecino 2^k es 0.
    Luego la subida jamas tiene que preocuparse del caso en que r buena sea el borde. -/
theorem borde_nunca_buena (k : Nat) (hk : 1 ≤ k) : buena k (2^k - 1) = false := by
  cases hb : buena k (2^k - 1) with
  | false => rfl
  | true =>
    exfalso
    have h := (buena_iff k (2^k - 1)).mp hb
    have hpos := Nat.two_pow_pos k
    have h1 : 2^k - 1 + 1 = 2^k := by omega
    have hS := h.1
    rw [h1, Sk_borde, Sk_potencia] at hS
    omega

-- ── Casos conocidos, por el NUCLEO (decide), no por #eval ──────────────

/-- Los conteos chicos del repo: a(3)=1, a(4)=3, a(5)=8, a(6)=18, a(7)=39, a(8)=82.
    Y los bordes k=0,1,2 dan 0 (el enunciado vale tambien ahi, trivialmente). -/
theorem casos_N :
    N 0 = 0 ∧ N 1 = 0 ∧ N 2 = 0 ∧ N 3 = 1 ∧ N 4 = 3 ∧ N 5 = 8 ∧
    N 6 = 18 ∧ N 7 = 39 ∧ N 8 = 82 := by decide

/-- Las ocho clases buenas mod 32, exactas. -/
theorem buenas_mod32 :
    (List.range 32).filter (fun r => buena 5 r) = [2, 4, 5, 12, 18, 20, 22, 28] := by decide

-- ── Control de axiomas ─────────────────────────────────────────────────

#print axioms terras
#print axioms sube
#print axioms sube_espejo
#print axioms duplica
#print axioms fraccion_monotona
#print axioms borde_nunca_buena
#print axioms casos_N
#print axioms buenas_mod32
#print axioms caso_conocido_5_6
#print axioms mapa_es_atajo
