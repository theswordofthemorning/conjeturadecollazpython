import OcelotasDescuentoRachas
import OcelotasPrefijosAfinados
import OcelotasTreceBase

/-! # Ocelotas: pesos por racha

Un fallo de CST obliga a muchas rachas que empiezan en valores pequeños
("pesadas"), y cada una reinicia el crecimiento permitido por las
congruencias. Mapa e índices de `Ocelotas.T`, `S`, `PrimerCruce` y
`OcelotasTrayectorias.Palabra`. Sin ley probabilística ni censo externo.
-/

namespace OcelotasPesos

open Real Ocelotas OcelotasTrayectorias

/-! ## Palabras desplazadas -/

def desp (a : ℕ → ℕ) (j : ℕ) : ℕ → ℕ := fun i => a (j + i)

theorem tiempo_desp (a b : ℕ → ℕ) (j : ℕ) : ∀ i,
    tiempo a b (j + i) = tiempo a b j + tiempo (desp a j) (desp b j) i := by
  intro i
  induction i with
  | zero => simp [tiempo]
  | succ i ih =>
    rw [← Nat.add_assoc, tiempo, ih, tiempo]
    simp only [desp]
    omega

theorem iter_desp (a b : ℕ → ℕ) (j i n : ℕ) :
    T^[tiempo (desp a j) (desp b j) i] (T^[tiempo a b j] n) =
      T^[tiempo a b (j + i)] n := by
  rw [← iter_add, tiempo_desp]

theorem palabra_desp {n r j : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r) (hj : j ≤ r) :
    Palabra (T^[tiempo a b j] n) (desp a j) (desp b j) (r - j) := by
  intro i hi
  obtain ⟨ha, hb, ho, he⟩ := hw (j + i) (by omega)
  refine ⟨ha, hb, ?_, ?_⟩
  · intro t ht
    rw [← iter_add]
    have h := ho t ht
    rw [tiempo_desp a b j i, Nat.add_assoc] at h
    exact h
  · intro t ht
    rw [← iter_add]
    have h := he t ht
    have e : tiempo a b j + (tiempo (desp a j) (desp b j) i + desp a j i + t) =
        tiempo a b (j + i) + a (j + i) + t := by
      rw [tiempo_desp a b j i]
      simp only [desp]
      omega
    rw [e]
    exact h

theorem palabra_prefijo {n r j : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r) (hj : j ≤ r) :
    Palabra n a b j := fun i hi => hw i (by omega)

theorem S_desp (a b : ℕ → ℕ) (j i n : ℕ) :
    S (tiempo a b (j + i)) n =
      S (tiempo a b j) n + S (tiempo (desp a j) (desp b j) i) (T^[tiempo a b j] n) := by
  rw [tiempo_desp, S_add]

/-! ## Un segmento: la criba de descuento desde su comienzo -/

/-- Cota de un segmento de j rachas que empieza en x con x+1 <= 2^m. -/
def g (m j : ℕ) : ℕ := j + OcelotasPrefijosAfinados.cota (256 * m - 256) j

theorem segmento {x j m : ℕ} {a b : ℕ → ℕ} (hx : 0 < x) (hw : Palabra x a b j)
    (hm : x + 1 ≤ 2 ^ m) (hm1 : 1 ≤ m) : S (tiempo a b j) x ≤ g m j := by
  have hbeta : log ((2 ^ m : ℕ) : ℝ) ≤ (m : ℝ) * log 2 := by
    rw [Nat.cast_pow, Real.log_pow]
    norm_num
  have hc := OcelotasDescuentoRachas.criba_palabra hx hw (by positivity : 0 < 2 ^ m) hm
    (le_refl j) (by norm_num : (1 : ℝ) ≤ 1585 / 1000)
    (by exact_mod_cast hm1 : (1 : ℝ) ≤ m) OcelotasTreceBase.alfa_valida hbeta
  have he : ((256 * m - 256 : ℕ) : ℝ) / 256 = (m : ℝ) - 1 := by
    rw [Nat.cast_sub (by omega : 256 ≤ 256 * m)]
    push_cast
    ring
  unfold g
  rw [OcelotasPrefijosAfinados.cota_real, he]
  exact hc

/-! ## Convexidad de la cota de segmento -/

theorem cota_mono (B : ℕ) : ∀ j, OcelotasPrefijosAfinados.cota B j ≤
    OcelotasPrefijosAfinados.cota B (j + 1) := by
  intro j
  induction j with
  | zero => simp [OcelotasPrefijosAfinados.cota]
  | succ j ih =>
    show OcelotasPrefijosAfinados.cota B (j + 1) ≤
      (25 * B + 10144 * OcelotasPrefijosAfinados.cota B (j + 1)) / 6400
    have e : OcelotasPrefijosAfinados.cota B (j + 1) =
        (25 * B + 10144 * OcelotasPrefijosAfinados.cota B j) / 6400 := rfl
    omega

theorem cota_convexa (B : ℕ) (j : ℕ) :
    OcelotasPrefijosAfinados.cota B (j + 1) + OcelotasPrefijosAfinados.cota B (j + 1) ≤
      OcelotasPrefijosAfinados.cota B (j + 1 + 1) + OcelotasPrefijosAfinados.cota B j := by
  have h := cota_mono B j
  have e1 : OcelotasPrefijosAfinados.cota B (j + 1) =
      (25 * B + 10144 * OcelotasPrefijosAfinados.cota B j) / 6400 := rfl
  have e2 : OcelotasPrefijosAfinados.cota B (j + 1 + 1) =
      (25 * B + 10144 * OcelotasPrefijosAfinados.cota B (j + 1)) / 6400 := rfl
  omega

/-- Los incrementos de la cota crecen: c(i+1)+c(j) <= c(j+1)+c(i) si i<=j. -/
theorem incrementos (B i : ℕ) : ∀ j, i ≤ j →
    OcelotasPrefijosAfinados.cota B (i + 1) + OcelotasPrefijosAfinados.cota B j ≤
      OcelotasPrefijosAfinados.cota B (j + 1) + OcelotasPrefijosAfinados.cota B i := by
  intro j hij
  induction j, hij using Nat.le_induction with
  | base => omega
  | succ j _ ih =>
    have h := cota_convexa B j
    omega

theorem g_uno {m : ℕ} (hm : 1 ≤ m) : g m 1 = m := by
  simp only [g, OcelotasPrefijosAfinados.cota]
  omega

theorem g_mono (m : ℕ) {i j : ℕ} (hij : i ≤ j) : g m i ≤ g m j := by
  induction j, hij using Nat.le_induction with
  | base => exact le_refl _
  | succ j _ ih =>
    have h := cota_mono (256 * m - 256) j
    unfold g at *
    omega

/-- Convexidad: dos segmentos de p y q rachas no superan uno de p+q-1 y otro de 1. -/
theorem g_convexa (m p : ℕ) (hp : 1 ≤ p) : ∀ q, 1 ≤ q →
    g m p + g m q ≤ g m (p + q - 1) + g m 1 := by
  intro q hq
  induction q, hq using Nat.le_induction with
  | base =>
    rw [show p + 1 - 1 = p by omega]
  | succ q hq ih =>
    have hi := incrementos (256 * m - 256) q (p + q - 1) (by omega)
    rw [show p + (q + 1) - 1 = (p + q - 1) + 1 by omega]
    unfold g at *
    omega

/-- Más rachas pesadas nunca aumentan la cota: g(N+1) >= g(N)+m. -/
theorem g_paso {m : ℕ} (hm : 1 ≤ m) (N : ℕ) : g m N + m ≤ g m (N + 1) := by
  have hi := incrementos (256 * m - 256) 0 N (Nat.zero_le N)
  have h1 := g_uno hm
  unfold g at *
  simp only [OcelotasPrefijosAfinados.cota] at hi h1 ⊢
  omega

/-! ## Rachas pesadas -/

/-- Racha i pesada: su comienzo x_i cumple x_i+1 <= M. -/
def pesada (n M : ℕ) (a b : ℕ → ℕ) (i : ℕ) : Prop := T^[tiempo a b i] n + 1 ≤ M

instance (n M : ℕ) (a b : ℕ → ℕ) : DecidablePred (pesada n M a b) := by
  intro i
  unfold pesada
  infer_instance

theorem cuenta_hasta_uno {p : ℕ → Prop} [DecidablePred p] :
    ∀ r, (∀ i, 1 ≤ i → i < r → ¬ p i) → Nat.count p r ≤ 1 := by
  intro r
  induction r with
  | zero => intro _; simp
  | succ r ih =>
    intro h
    rw [Nat.count_succ]
    by_cases hr : r = 0
    · subst hr
      simp only [Nat.count_zero]
      split_ifs <;> omega
    · have hn : ¬ p r := h r (by omega) (by omega)
      have := ih (fun i hi1 hi2 => h i hi1 (by omega))
      simp [hn]
      omega

theorem cuenta_desp (n M : ℕ) (a b : ℕ → ℕ) (j : ℕ) : ∀ l,
    Nat.count (pesada (T^[tiempo a b j] n) M (desp a j) (desp b j)) l =
      Nat.count (fun k => pesada n M a b (j + k)) l := by
  intro l
  induction l with
  | zero => simp
  | succ l ih =>
    rw [Nat.count_succ, Nat.count_succ, ih]
    congr 1
    simp only [pesada, iter_desp]
    congr

/-- Composición: con al menos h rachas pesadas (la primera lo es), la suma de
longitudes impares no supera g(r-h+1)+(h-1)m. -/
theorem suma_por_segmentos {m : ℕ} (hm : 1 ≤ m) : ∀ r, ∀ (n h : ℕ) (a b : ℕ → ℕ),
    0 < n → Palabra n a b r → n + 1 ≤ 2 ^ m → 1 ≤ h →
    h ≤ Nat.count (pesada n (2 ^ m) a b) r →
    S (tiempo a b r) n ≤ g m (r - h + 1) + (h - 1) * m := by
  intro r
  induction r using Nat.strong_induction_on with
  | _ r ih =>
  intro n h a b hn hw hm0 hh hcount
  have hcr : Nat.count (pesada n (2 ^ m) a b) r ≤ r := Nat.count_le _
  by_cases h1 : h = 1
  · subst h1
    have hs := segmento hn hw hm0 hm
    rw [show r - 1 + 1 = r by omega]
    simpa using hs
  · have hex : ∃ j, 1 ≤ j ∧ j < r ∧ pesada n (2 ^ m) a b j := by
      by_contra hno
      push Not at hno
      have := cuenta_hasta_uno r (fun i hi1 hi2 hp => absurd hp (by
        have := hno i hi1 hi2; exact this))
      omega
    classical
    let j := Nat.find hex
    have hjspec : 1 ≤ j ∧ j < r ∧ pesada n (2 ^ m) a b j := Nat.find_spec hex
    have hjmin : ∀ i, 1 ≤ i → i < j → ¬ pesada n (2 ^ m) a b i := by
      intro i hi1 hi2 hp
      exact Nat.find_min hex hi2 ⟨hi1, by omega, hp⟩
    obtain ⟨hj1, hjr, hjp⟩ := hjspec
    -- conteo: la primera parte tiene a lo sumo una pesada
    have hc1 : Nat.count (pesada n (2 ^ m) a b) j ≤ 1 := cuenta_hasta_uno j hjmin
    have hsplit := Nat.count_add (pesada n (2 ^ m) a b) j (r - j)
    rw [show j + (r - j) = r by omega] at hsplit
    have hcount' : h - 1 ≤ Nat.count (pesada (T^[tiempo a b j] n) (2 ^ m)
        (desp a j) (desp b j)) (r - j) := by
      rw [cuenta_desp]
      omega
    -- primer segmento
    have hS1 := segmento hn (palabra_prefijo hw hjr.le) hm0 hm
    -- resto
    have hxpos : 0 < T^[tiempo a b j] n := OcelotasDescuentoRachas.iterado_positivo hn _
    have hS2 := ih (r - j) (by omega) (T^[tiempo a b j] n) (h - 1) (desp a j) (desp b j)
      hxpos (palabra_desp hw hjr.le) hjp (by omega) hcount'
    have hcr2 : Nat.count (pesada (T^[tiempo a b j] n) (2 ^ m) (desp a j) (desp b j))
        (r - j) ≤ r - j := Nat.count_le _
    have hsum := S_desp a b j (r - j) n
    rw [show j + (r - j) = r by omega] at hsum
    have hconv := g_convexa m j hj1 (r - j - (h - 1) + 1) (by omega)
    have hg1 := g_uno hm
    rw [show j + (r - j - (h - 1) + 1) - 1 = r - h + 1 by omega] at hconv
    have hh2 : (h - 1) * m = (h - 1 - 1) * m + m := by
      rw [show h - 1 = (h - 1 - 1) + 1 by omega, Nat.add_mul, one_mul]
      simp
    omega

/-! ## Cadena de pesos -/

/-- Peso de la racha i: M si es pesada, n+R si es ligera. -/
def peso (n M R : ℕ) (a b : ℕ → ℕ) (i : ℕ) : ℕ :=
  if pesada n M a b i then M else n + R

def pesos (n M R : ℕ) (a b : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => pesos n M R a b i + peso n M R a b i

theorem peso_acota {n r R M i : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r)
    (hk : PrimerCruce n (tiempo a b r)) (hi : i < r) (hR : r ≤ R) :
    2 ^ tiempo a b i * M ≤ 3 ^ acumulados a i * peso n M R a b i := by
  unfold peso
  split_ifs with hp
  · have h := pre_cruce hk (tiempo_lt hw hi)
    rw [cuenta_impares hw i (by omega)] at h
    exact Nat.mul_le_mul_right _ h
  · unfold pesada at hp
    have h := cota_afin hw hk i (by omega)
    have hM : M ≤ T^[tiempo a b i] n := by omega
    have h1 := Nat.mul_le_mul_left (2 ^ tiempo a b i) hM
    have h2 := Nat.mul_le_mul_left (3 ^ acumulados a i) (show n + i ≤ n + R by omega)
    exact le_trans h1 (le_trans h h2)

theorem paso_pesos {n r R M i : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r)
    (hk : PrimerCruce n (tiempo a b r)) (hi : i < r) (hR : r ≤ R) (hM : 0 < M)
    (hprev : 2 ^ tiempo a b i * T^[tiempo a b i] n * M ≤
      3 ^ acumulados a i * (n * M + pesos n M R a b i)) :
    2 ^ tiempo a b (i + 1) * T^[tiempo a b (i + 1)] n * M <
      3 ^ acumulados a (i + 1) * (n * M + pesos n M R a b (i + 1)) := by
  have he := identidad_bloque hw hi
  have hw' := peso_acota (M := M) hw hk hi hR
  set E := 2 ^ tiempo a b i
  set X := T^[tiempo a b i] n
  set F := 2 ^ tiempo a b (i + 1)
  set Y := T^[tiempo a b (i + 1)] n
  set P := 3 ^ acumulados a i
  set Q := 3 ^ a i
  set W := pesos n M R a b i
  set w := peso n M R a b i
  have hpos : 0 < 2 ^ (tiempo a b i + a i) * M := by positivity
  have hA : 3 ^ acumulados a (i + 1) = P * Q := by
    rw [show acumulados a (i + 1) = acumulados a i + a i from rfl, pow_add]
  have hW : pesos n M R a b (i + 1) = W + w := rfl
  rw [hA, hW]
  have h1 : F * Y * M + 2 ^ (tiempo a b i + a i) * M = Q * (E * X * M) + Q * (E * M) := by
    rw [show Q * (E * X * M) + Q * (E * M) = (Q * E * (X + 1)) * M by ring, ← he]
    ring
  have h2 := Nat.mul_le_mul_left Q hprev
  have h3 := Nat.mul_le_mul_left Q hw'
  calc F * Y * M < F * Y * M + 2 ^ (tiempo a b i + a i) * M := by omega
    _ = Q * (E * X * M) + Q * (E * M) := h1
    _ ≤ Q * (P * (n * M + W)) + Q * (P * w) := Nat.add_le_add h2 h3
    _ = P * Q * (n * M + (W + w)) := by ring

theorem cadena_pesos {n r R M : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r)
    (hk : PrimerCruce n (tiempo a b r)) (hR : r ≤ R) (hM : 0 < M) :
    ∀ i, i ≤ r → 2 ^ tiempo a b i * T^[tiempo a b i] n * M ≤
      3 ^ acumulados a i * (n * M + pesos n M R a b i) := by
  intro i
  induction i with
  | zero => intro _; simp [tiempo, acumulados, pesos]
  | succ i ih =>
    intro hi
    exact (paso_pesos hw hk (by omega) hR hM (ih (by omega))).le

theorem pesos_cuenta (n M R : ℕ) (a b : ℕ → ℕ) : ∀ i,
    pesos n M R a b i = Nat.count (pesada n M a b) i * M +
      (i - Nat.count (pesada n M a b) i) * (n + R) := by
  intro i
  induction i with
  | zero => simp [pesos]
  | succ i ih =>
    have hle : Nat.count (pesada n M a b) i ≤ i := Nat.count_le _
    rw [pesos, ih, Nat.count_succ]
    unfold peso
    split_ifs with hp
    · rw [show i + 1 - (Nat.count (pesada n M a b) i + 1) =
        i - Nat.count (pesada n M a b) i by omega]
      ring
    · rw [show i + 1 - (Nat.count (pesada n M a b) i + 0) =
        (i - Nat.count (pesada n M a b) i) + 1 by omega]
      ring

/-- Un fallo real: (2^k-3^q) n M < 3^q (H M + (r-H)(n+R)). -/
theorem fallo_pesos {n r R M : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r) (hr : 0 < r)
    (hR : r ≤ R) (hM : 0 < M) (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n) :
    (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n * M <
      3 ^ S (tiempo a b r) n * (Nat.count (pesada n M a b) r * M +
        (r - Nat.count (pesada n M a b) r) * (n + R)) := by
  obtain ⟨i, rfl⟩ : ∃ i, r = i + 1 := ⟨r - 1, by omega⟩
  have hprev := cadena_pesos hw hk hR hM i (by omega)
  have hlast := paso_pesos hw hk (by omega) hR hM hprev
  rw [← pesos_cuenta, cuenta_impares hw (i + 1) le_rfl]
  have hp := hk.2
  rw [cuenta_impares hw (i + 1) le_rfl] at hp
  have hm1 := Nat.mul_le_mul_left (2 ^ tiempo a b (i + 1)) hf
  have hm2 := Nat.mul_le_mul_right M hm1
  rw [Nat.sub_mul, Nat.sub_mul]
  have hle : 3 ^ acumulados a (i + 1) * n * M ≤ 2 ^ tiempo a b (i + 1) * n * M :=
    Nat.mul_le_mul_right M (Nat.mul_le_mul_right n hp.le)
  have hexp : 3 ^ acumulados a (i + 1) * (n * M + pesos n M R a b (i + 1)) =
      3 ^ acumulados a (i + 1) * n * M +
        3 ^ acumulados a (i + 1) * pesos n M R a b (i + 1) := by ring
  rw [hexp] at hlast
  have hm3 : 2 ^ tiempo a b (i + 1) * n * M ≤
      2 ^ tiempo a b (i + 1) * T^[tiempo a b (i + 1)] n * M := hm2
  omega

/-! ## Paso real y exclusión de una pieza -/

theorem pesadas_de_fallo {n r R M : ℕ} {a b : ℕ → ℕ} {c : ℝ} (hw : Palabra n a b r)
    (hr : 0 < r) (hR : r ≤ R) (hM : 0 < M) (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n)
    (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 - S (tiempo a b r) n * log 3) :
    c * n * M < (Nat.count (pesada n M a b) r * M +
      (r - Nat.count (pesada n M a b) r) * (n + R) : ℕ) := by
  set k := tiempo a b r
  set q := S k n
  set W := (Nat.count (pesada n M a b) r * M + (r - Nat.count (pesada n M a b) r) * (n + R))
  set lam : ℝ := (k : ℝ) * log 2 - q * log 3
  have hpos3 : (0 : ℝ) < (3 : ℝ) ^ q := by positivity
  have hpos2 : (0 : ℝ) < (2 : ℝ) ^ k := by positivity
  have hexp : Real.exp lam = (2 : ℝ) ^ k / (3 : ℝ) ^ q := by
    have hl : lam = log ((2 : ℝ) ^ k) - log ((3 : ℝ) ^ q) := by
      rw [Real.log_pow, Real.log_pow]
    rw [hl, Real.exp_sub, Real.exp_log hpos2, Real.exp_log hpos3]
  have he := Real.add_one_le_exp lam
  rw [hexp, le_div_iff₀ hpos3] at he
  have hlt : 3 ^ q < 2 ^ k := hk.2
  have hfp := fallo_pesos hw hr hR hM hk hf
  have hreal : (((2 ^ k - 3 ^ q) * n * M : ℕ) : ℝ) < ((3 ^ q * W : ℕ) : ℝ) := by
    exact_mod_cast hfp
  have hcast : (((2 ^ k - 3 ^ q) * n * M : ℕ) : ℝ) =
      ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * n * M := by
    rw [Nat.cast_mul, Nat.cast_mul, Nat.cast_sub hlt.le]
    push_cast
    ring
  rw [hcast] at hreal
  push_cast at hreal
  have hnM : (0 : ℝ) ≤ (n : ℝ) * M := by positivity
  have h1 : c * (3 : ℝ) ^ q ≤ (2 : ℝ) ^ k - (3 : ℝ) ^ q := by nlinarith
  have h2 : c * (3 : ℝ) ^ q * ((n : ℝ) * M) ≤ ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * ((n : ℝ) * M) :=
    mul_le_mul_of_nonneg_right h1 hnM
  have h3 : (3 : ℝ) ^ q * (c * n * M) < (3 : ℝ) ^ q * (W : ℝ) := by
    have : ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * ((n : ℝ) * M) =
        ((2 : ℝ) ^ k - (3 : ℝ) ^ q) * n * M := by ring
    nlinarith
  exact lt_of_mul_lt_mul_left h3 hpos3.le

/-- Exclusión de una pieza [ninf, nsup] de semillas con q >= qmin. -/
theorem pieza_imposible {n r R m h0 ninf nsup qmin : ℕ} {a b : ℕ → ℕ} {c : ℝ}
    (hn : 0 < n) (hw : Palabra n a b r) (hr : 0 < r) (hR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hc : 0 ≤ c)
    (hLambda : c ≤ (tiempo a b r : ℝ) * log 2 - S (tiempo a b r) n * log 3)
    (hlo : ninf ≤ n) (hhi : n ≤ nsup) (hM : nsup + R ≤ 2 ^ m) (hm : 1 ≤ m)
    (hh0 : h0 ≤ R)
    (hcert : ((h0 * 2 ^ m + (R - h0) * (nsup + R) : ℕ) : ℝ) ≤ c * ninf * 2 ^ m)
    (hcriba : h0 < R → g m (R - h0) + h0 * m < qmin)
    (hq : qmin ≤ S (tiempo a b r) n) : False := by
  set H := Nat.count (pesada n (2 ^ m) a b) r
  have hHr : H ≤ r := Nat.count_le _
  have hW := pesadas_de_fallo (M := 2 ^ m) hw hr hR (by positivity) hk hf hLambda
  -- H > h0
  have hH : h0 + 1 ≤ H := by
    by_contra hlt
    have hHh : H ≤ h0 := by omega
    have hmono : H * 2 ^ m + (r - H) * (n + R) ≤ h0 * 2 ^ m + (R - h0) * (nsup + R) := by
      have e1 : (r - H) * (n + R) ≤ (R - H) * (nsup + R) :=
        Nat.mul_le_mul (by omega) (by omega)
      have e2 : H * 2 ^ m + (R - H) * (nsup + R) ≤ h0 * 2 ^ m + (R - h0) * (nsup + R) := by
        obtain ⟨D, hD⟩ : ∃ D, h0 = H + D := ⟨h0 - H, by omega⟩
        rw [hD, show R - H = (R - (H + D)) + D by omega]
        have : D * (nsup + R) ≤ D * 2 ^ m := Nat.mul_le_mul_left _ hM
        nlinarith
      omega
    have hmonoR : ((H * 2 ^ m + (r - H) * (n + R) : ℕ) : ℝ) ≤
        ((h0 * 2 ^ m + (R - h0) * (nsup + R) : ℕ) : ℝ) := by exact_mod_cast hmono
    have hlo' : c * (ninf : ℝ) * 2 ^ m ≤ c * n * 2 ^ m := by
      have h1 : (ninf : ℝ) ≤ n := by exact_mod_cast hlo
      have h2m : (0 : ℝ) ≤ 2 ^ m := by positivity
      exact mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left h1 hc) h2m
    have hW' : c * (n : ℝ) * ((2 ^ m : ℕ) : ℝ) <
        ((H * 2 ^ m + (r - H) * (n + R) : ℕ) : ℝ) := hW
    push_cast at hW' hcert hmonoR
    linarith
  have hh0R : h0 < R := by omega
  have hn1 : n + 1 ≤ 2 ^ m := by omega
  have hS := suma_por_segmentos hm r n (h0 + 1) a b hn hw hn1 (by omega) hH
  have hg := g_mono m (show r - (h0 + 1) + 1 ≤ R - h0 by omega)
  have hcr := hcriba hh0R
  simp only [Nat.add_sub_cancel] at hS
  omega

/-- Sin rachas pesadas adicionales: basta un solo segmento desde n. -/
theorem pieza_cadena {n r R m nsup qmin : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < n) (hw : Palabra n a b r) (hr : 0 < r) (hR : r ≤ R)
    (hhi : n ≤ nsup) (hM : nsup + R ≤ 2 ^ m) (hm : 1 ≤ m)
    (hcriba : g m R < qmin) (hq : qmin ≤ S (tiempo a b r) n) : False := by
  have hS := segmento hn hw (by omega : n + 1 ≤ 2 ^ m) hm
  have hg := g_mono m hR
  omega

end OcelotasPesos

#print axioms OcelotasPesos.palabra_desp
#print axioms OcelotasPesos.segmento
#print axioms OcelotasPesos.g_convexa
#print axioms OcelotasPesos.suma_por_segmentos
#print axioms OcelotasPesos.fallo_pesos
#print axioms OcelotasPesos.pesadas_de_fallo
#print axioms OcelotasPesos.pieza_imposible
#print axioms OcelotasPesos.pieza_cadena
