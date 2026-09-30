import GarnerEnunciado
import GaoLiteral

/-! # Pandas y Marmotas: residuos y la pregunta de Gao (1993, pág. 266)

Mapa clásico `C` de `GarnerEnunciado`. Si `altura n h`, en h pasos n llega a 1 por primera
vez; `mitades n h` es el tiempo total de parada σ∞(n) de Gao y `triples n h` el número S(n)
de pasos `3n+1`, con `mitades n h + triples n h = h`. El residuo de Roosendaal cumple
`2^σ∞(n) = 3^S(n) · n · Res(n)`.

* `residuo_ge_uno`: `Res(n) ≥ 1` siempre; en enteros, `3^S · n ≤ 2^σ∞`.
* `seis`: núcleo aritmético de Pandas en un encuentro `C^j(n) = C^j(n+1) = Y`.
* `pandas`: igual altura, `Res(n) ≤ 6` y `Res(n+1) < 6n/(n+1)` dan igual σ∞ e igual S.
  `pandas_escrito` es la forma de `lemadepandas.txt`, con `Res < 3` en los dos.
* `gao_de_residuo`: si todo residuo es menor que 4, la pregunta de Gao
  (¿igual altura implica igual σ∞?) tiene respuesta afirmativa.
* `gao_casi_siempre`: sin hipótesis, los contraejemplos tienen densidad natural cero.
  Sale de `GaoLiteral` (Hienas): coalescencia de Gao e igual altura dan igual σ∞.
* `equilibrio_quince`: un encuentro en el paso j con `2^j + 3 < 15n` es equilibrado.
  `Hienas.equilibrio` pedía `2^j ≤ n`.
* Marmotas (`transporte`, `residuo_por_escalas`, `gao_por_escalas`): combinar escalas.
  Una cota del residuo en [1, B) se transporta a todo n cuya órbita entra en [1, B)
  tras a lo sumo 2B pasos `3n+1` hechos en valores ≥ B; el factor no pasa de 3.

Las hipótesis de terminación y de residuo quedan explícitas en cada enunciado.
Compilación, desde `depuracion/gao20260920/formal`:
`lake env lean ../../pandas20260930/Pandas.lean` -/

open Filter Topology

namespace PandasGao

open GarnerEnunciado

/-- Pasos `3n+1` entre los h primeros pasos desde n: S(n) si `h = height(n)`. -/
def triples (n h : ℕ) : ℕ := ((Finset.range h).filter (fun k => C^[k] n % 2 = 1)).card

/-- Residuo de Roosendaal: `2^σ∞(n) = 3^S(n) · n · Res(n)`. -/
def residuo (n h : ℕ) : ℚ := 2 ^ mitades n h / (3 ^ triples n h * n)

/-- La pregunta de Gao (1993, pág. 266): ¿`height(n) = height(n+1)` implica
    `σ∞(n) = σ∞(n+1)`? -/
def PreguntaGao : Prop :=
  ∀ n h, altura n h → altura (n + 1) h → mitades n h = mitades (n + 1) h

/-! ## Puente con las cuentas recursivas de Hienas -/

theorem C_hienas : Hienas.C = C := rfl

theorem mitades_add : ∀ j k n,
    Hienas.mitades (j + k) n = Hienas.mitades j n + Hienas.mitades k (C^[j] n) := by
  intro j
  induction j with
  | zero => intro k n; simp [Hienas.mitades]
  | succ j ih =>
    intro k n
    rw [show j + 1 + k = (j + k) + 1 by omega]
    show (if n % 2 = 0 then 1 else 0) + Hienas.mitades (j + k) (Hienas.C n) =
      ((if n % 2 = 0 then 1 else 0) + Hienas.mitades j (Hienas.C n)) +
        Hienas.mitades k (C^[j + 1] n)
    rw [ih k (Hienas.C n), Function.iterate_succ_apply, C_hienas]
    ring

theorem triples_add : ∀ j k n,
    Hienas.triples (j + k) n = Hienas.triples j n + Hienas.triples k (C^[j] n) := by
  intro j
  induction j with
  | zero => intro k n; simp [Hienas.triples]
  | succ j ih =>
    intro k n
    rw [show j + 1 + k = (j + k) + 1 by omega]
    show (if n % 2 = 0 then 0 else 1) + Hienas.triples (j + k) (Hienas.C n) =
      ((if n % 2 = 0 then 0 else 1) + Hienas.triples j (Hienas.C n)) +
        Hienas.triples k (C^[j + 1] n)
    rw [ih k (Hienas.C n), Function.iterate_succ_apply, C_hienas]
    ring

theorem mitades_succ (n k : ℕ) :
    mitades n (k + 1) = mitades n k + (if C^[k] n % 2 = 0 then 1 else 0) := by
  unfold mitades
  rw [Finset.card_filter, Finset.card_filter, Finset.sum_range_succ]

theorem triples_succ (n k : ℕ) :
    triples n (k + 1) = triples n k + (if C^[k] n % 2 = 1 then 1 else 0) := by
  unfold triples
  rw [Finset.card_filter, Finset.card_filter, Finset.sum_range_succ]

theorem mitades_hienas : ∀ k n, mitades n k = Hienas.mitades k n := by
  intro k
  induction k with
  | zero => intro n; simp [mitades, Hienas.mitades]
  | succ k ih =>
    intro n
    rw [mitades_succ, ih n, mitades_add k 1 n]
    rfl

theorem triples_hienas : ∀ k n, triples n k = Hienas.triples k n := by
  intro k
  induction k with
  | zero => intro n; simp [triples, Hienas.triples]
  | succ k ih =>
    intro n
    rw [triples_succ, ih n, triples_add k 1 n]
    congr 1
    show (if C^[k] n % 2 = 1 then 1 else 0) = (if C^[k] n % 2 = 0 then 0 else 1) + 0
    rcases Nat.mod_two_eq_zero_or_one (C^[k] n) with h | h <;> simp [h]

theorem suma (n h : ℕ) : mitades n h + triples n h = h := by
  rw [mitades_hienas, triples_hienas]; exact Hienas.suma_cuentas h n

/-- Las dos cotas de Hienas con las cuentas de `GarnerEnunciado`. -/
theorem cotas (i x : ℕ) :
    3 ^ triples x i * x ≤ 2 ^ mitades x i * C^[i] x ∧
    3 * (2 ^ mitades x i * C^[i] x) ≤ 3 ^ triples x i * (3 * x + 2 ^ i) := by
  rw [mitades_hienas, triples_hienas]; exact Hienas.invariante i x

/-! ## Altura -/

/-- Tener altura obliga a `n ≥ 1`: la órbita de 0 es constante. -/
theorem pos_de_altura {n h : ℕ} (ha : altura n h) : 1 ≤ n := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · have h0 : ∀ k, C^[k] 0 = 0 := by
      intro k
      induction k with
      | zero => rfl
      | succ k ih => rw [Function.iterate_succ_apply', ih]; simp [C]
    have := ha.1
    rw [h0] at this
    exact absurd this (by decide)
  · exact hn

theorem altura_unica {n h h' : ℕ} (a : altura n h) (b : altura n h') : h = h' := by
  by_contra hne
  rcases Nat.lt_or_gt_of_ne hne with hlt | hlt
  · exact b.2 h hlt a.1
  · exact a.2 h' hlt b.1

/-- Dos consecutivos con la misma altura empiezan en n ≥ 2. -/
theorem dos_de_par {n h : ℕ} (a : altura n h) (b : altura (n + 1) h) : 2 ≤ n := by
  have h1 := pos_de_altura a
  by_contra hlt
  obtain rfl : n = 1 := by omega
  have h0 : h = 0 := altura_unica a ⟨rfl, fun k hk => absurd hk (Nat.not_lt_zero k)⟩
  subst h0
  exact absurd b.1 (by decide)

/-- La cola: `C^k(x)` tiene altura `h − k`. -/
theorem altura_cola {x h k : ℕ} (a : altura x h) (hk : k ≤ h) : altura (C^[k] x) (h - k) := by
  constructor
  · rw [← Function.iterate_add_apply, Nat.sub_add_cancel hk, a.1]
  · intro i hi
    rw [← Function.iterate_add_apply]
    exact a.2 (i + k) (by omega)

/-! ## Pandas -/

/-- `Res(n) ≥ 1`: en enteros, `3^S · n ≤ 2^σ∞`. -/
theorem residuo_ge_uno {n h : ℕ} (ha : altura n h) : 3 ^ triples n h * n ≤ 2 ^ mitades n h := by
  have := (cotas h n).1
  rwa [ha.1, mul_one] at this

/-- Núcleo aritmético de Pandas en un encuentro Y. Con `t1 + s1 = t2 + s2`, las cotas
    inferiores `3^s1·n ≤ 2^t1·Y`, `3^s2·(n+1) ≤ 2^t2·Y` y las superiores
    `2^t1·Y ≤ 6·3^s1·n`, `2^t2·Y < 6·3^s2·n` obligan a `t1 = t2`. -/
theorem seis {n Y t1 s1 t2 s2 : ℕ} (hh : t1 + s1 = t2 + s2)
    (L1 : 3 ^ s1 * n ≤ 2 ^ t1 * Y) (L2 : 3 ^ s2 * (n + 1) ≤ 2 ^ t2 * Y)
    (U1 : 2 ^ t1 * Y ≤ 6 * (3 ^ s1 * n)) (U2 : 2 ^ t2 * Y < 6 * (3 ^ s2 * n)) :
    t1 = t2 := by
  have seisP : ∀ e : ℕ, (6:ℕ) ^ (e + 1) = 2 ^ (e + 1) * 3 ^ (e + 1) := fun e => by
    rw [← mul_pow]; norm_num
  have h6 : ∀ e : ℕ, 6 ≤ 6 ^ (e + 1) := fun e => by
    calc 6 = 6 ^ 1 := by norm_num
      _ ≤ 6 ^ (e + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
  by_contra hne
  rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
  · -- t1 < t2: la órbita de n+1 dividió más veces; la de n triplicó más
    obtain ⟨e, rfl⟩ := Nat.exists_eq_add_of_lt hlt
    obtain rfl : s1 = s2 + (e + 1) := by omega
    have key : 6 ^ (e + 1) * (3 ^ s2 * n) ≤ 2 ^ (t1 + e + 1) * Y := by
      calc 6 ^ (e + 1) * (3 ^ s2 * n) = 2 ^ (e + 1) * (3 ^ (s2 + (e + 1)) * n) := by
            rw [seisP]; ring
        _ ≤ 2 ^ (e + 1) * (2 ^ t1 * Y) := Nat.mul_le_mul_left _ L1
        _ = 2 ^ (t1 + e + 1) * Y := by ring
    have h7 : 6 * (3 ^ s2 * n) ≤ 6 ^ (e + 1) * (3 ^ s2 * n) := Nat.mul_le_mul_right _ (h6 e)
    omega
  · -- t2 < t1
    obtain ⟨e, rfl⟩ := Nat.exists_eq_add_of_lt hgt
    obtain rfl : s2 = s1 + (e + 1) := by omega
    have key : 6 ^ (e + 1) * (3 ^ s1 * (n + 1)) ≤ 2 ^ (t2 + e + 1) * Y := by
      calc 6 ^ (e + 1) * (3 ^ s1 * (n + 1)) = 2 ^ (e + 1) * (3 ^ (s1 + (e + 1)) * (n + 1)) := by
            rw [seisP]; ring
        _ ≤ 2 ^ (e + 1) * (2 ^ t2 * Y) := Nat.mul_le_mul_left _ L2
        _ = 2 ^ (t2 + e + 1) * Y := by ring
    have h7 : 6 * (3 ^ s1 * (n + 1)) ≤ 6 ^ (e + 1) * (3 ^ s1 * (n + 1)) :=
      Nat.mul_le_mul_right _ (h6 e)
    have h8 : 3 ^ s1 * n < 3 ^ s1 * (n + 1) :=
      Nat.mul_lt_mul_of_pos_left (by omega) (by positivity)
    omega

/-- Pandas en un encuentro: si `C^j(n) = C^j(n+1)` con residuos parciales `R_j(n) ≤ 6` y
    `R_j(n+1) < 6n/(n+1)`, el encuentro es equilibrado. -/
theorem pandas_encuentro {n j : ℕ} (he : C^[j] n = C^[j] (n + 1))
    (U1 : 2 ^ mitades n j * C^[j] n ≤ 6 * (3 ^ triples n j * n))
    (U2 : 2 ^ mitades (n + 1) j * C^[j] n < 6 * (3 ^ triples (n + 1) j * n)) :
    mitades n j = mitades (n + 1) j := by
  have L1 := (cotas j n).1
  have L2 := (cotas j (n + 1)).1
  rw [← he] at L2
  exact seis (by rw [suma, suma]) L1 L2 U1 U2

/-- Pandas, forma afilada: igual altura, `Res(n) ≤ 6` y `Res(n+1) < 6n/(n+1)`. -/
theorem pandas {n h : ℕ} (a : altura n h) (b : altura (n + 1) h)
    (U1 : 2 ^ mitades n h ≤ 6 * (3 ^ triples n h * n))
    (U2 : 2 ^ mitades (n + 1) h < 6 * (3 ^ triples (n + 1) h * n)) :
    mitades n h = mitades (n + 1) h ∧ triples n h = triples (n + 1) h := by
  have he : C^[h] n = C^[h] (n + 1) := by rw [a.1, b.1]
  have e := pandas_encuentro he (by rw [a.1, mul_one]; exact U1)
    (by rw [a.1, mul_one]; exact U2)
  refine ⟨e, ?_⟩
  have s1 := suma n h
  have s2 := suma (n + 1) h
  omega

theorem cota_de_residuo {n h : ℕ} {q : ℚ} (hn : 1 ≤ n) (r : residuo n h < q) :
    (2 : ℚ) ^ mitades n h < q * (3 ^ triples n h * n) := by
  have hn' : (0 : ℚ) < n := by exact_mod_cast hn
  have hpos : (0 : ℚ) < 3 ^ triples n h * n := mul_pos (by positivity) hn'
  unfold residuo at r
  rwa [div_lt_iff₀ hpos] at r

/-- El lema de Pandas tal como está escrito en `lemadepandas.txt`: `Res < 3` en los dos. -/
theorem pandas_escrito {n h : ℕ} (a : altura n h) (b : altura (n + 1) h)
    (r1 : residuo n h < 3) (r2 : residuo (n + 1) h < 3) :
    mitades n h = mitades (n + 1) h ∧ triples n h = triples (n + 1) h := by
  have hn := pos_de_altura a
  have c1 := cota_de_residuo hn r1
  have c2 := cota_de_residuo (by omega) r2
  have hn1 : (1 : ℚ) ≤ n := by exact_mod_cast hn
  apply pandas a b
  · have hX : (0 : ℚ) ≤ 3 ^ triples n h * n := by positivity
    have : (2 : ℚ) ^ mitades n h ≤ 6 * (3 ^ triples n h * n) := by linarith
    exact_mod_cast this
  · push_cast at c2
    have hZ : (0 : ℚ) ≤ 3 ^ triples (n + 1) h := by positivity
    have : (2 : ℚ) ^ mitades (n + 1) h < 6 * (3 ^ triples (n + 1) h * n) := by
      nlinarith [mul_nonneg hZ (sub_nonneg.2 hn1)]
    exact_mod_cast this

/-- Si todo residuo es menor que 4, la pregunta de Gao tiene respuesta afirmativa. -/
theorem gao_de_residuo (hR : ∀ m h, altura m h → residuo m h < 4) : PreguntaGao := by
  intro n h a b
  have hn := dos_de_par a b
  have c1 := cota_de_residuo (by omega) (hR n h a)
  have c2 := cota_de_residuo (by omega) (hR (n + 1) h b)
  have hn2 : (2 : ℚ) ≤ n := by exact_mod_cast hn
  refine (pandas a b ?_ ?_).1
  · have hX : (0 : ℚ) ≤ 3 ^ triples n h * n := by positivity
    have : (2 : ℚ) ^ mitades n h ≤ 6 * (3 ^ triples n h * n) := by linarith
    exact_mod_cast this
  · push_cast at c2
    have hZ : (0 : ℚ) ≤ 3 ^ triples (n + 1) h := by positivity
    have : (2 : ℚ) ^ mitades (n + 1) h < 6 * (3 ^ triples (n + 1) h * n) := by
      nlinarith [mul_nonneg hZ (sub_nonneg.2 hn2)]
    exact_mod_cast this

/-! ## La pregunta de Gao casi siempre, sin hipótesis -/

/-- Coalescencia de Gao e igual altura dan igual σ∞. -/
theorem mitades_de_coalescencia {n j h : ℕ} (hc : Hienas.coalescen n j)
    (a : altura n h) (b : altura (n + 1) h) : mitades n h = mitades (n + 1) h := by
  obtain ⟨he, hm, hs⟩ := hc
  have he' : C^[j] n = C^[j] (n + 1) := he
  have hjh : j < h := by
    by_contra hcon
    exact (hs h (by omega)).1 a.1
  obtain ⟨k, rfl⟩ : ∃ k, h = j + k := ⟨h - j, by omega⟩
  rw [mitades_hienas, mitades_hienas, mitades_add, mitades_add, hm, he']

open Classical in
/-- Pregunta de Gao en densidad: los n con `height(n) = height(n+1)` y
    `σ∞(n) ≠ σ∞(n+1)` tienen densidad natural cero. -/
theorem gao_casi_siempre :
    Tendsto (fun N : ℕ => (((Finset.range N).filter (fun n =>
      ∃ h, altura n h ∧ altura (n + 1) h ∧ mitades n h ≠ mitades (n + 1) h)).card : ℝ) / N)
      atTop (𝓝 0) := by
  have hD : Tendsto Hienas.d atTop (𝓝 1) := GaoLiteral.conjetura_gao_literal.2
  have hup : ∀ N : ℕ, (((Finset.range N).filter (fun n =>
      ∃ h, altura n h ∧ altura (n + 1) h ∧ mitades n h ≠ mitades (n + 1) h)).card : ℝ) / N ≤
      1 - Hienas.d N := by
    intro N
    rcases Nat.eq_zero_or_pos N with rfl | hN
    · simp [Hienas.d]
    have hd : Hienas.d N =
        (((Finset.range N).filter (fun n => ∃ j, Hienas.coalescen n j)).card : ℝ) / N := rfl
    rw [hd]
    have hsub : (Finset.range N).filter (fun n =>
        ∃ h, altura n h ∧ altura (n + 1) h ∧ mitades n h ≠ mitades (n + 1) h) ⊆
        Finset.range N \ (Finset.range N).filter (fun n => ∃ j, Hienas.coalescen n j) := by
      intro n hn
      rw [Finset.mem_filter] at hn
      rw [Finset.mem_sdiff, Finset.mem_filter]
      refine ⟨hn.1, fun ⟨_, j, hj⟩ => ?_⟩
      obtain ⟨h, a, b, hne⟩ := hn.2
      exact hne (mitades_de_coalescencia hj a b)
    have hGsub : (Finset.range N).filter (fun n => ∃ j, Hienas.coalescen n j) ⊆
        Finset.range N := Finset.filter_subset _ _
    have h1 := Finset.card_le_card hsub
    rw [Finset.card_sdiff_of_subset hGsub, Finset.card_range] at h1
    have h2 : ((Finset.range N).filter (fun n => ∃ j, Hienas.coalescen n j)).card ≤ N := by
      simpa using Finset.card_le_card hGsub
    have hc : ((Finset.range N).filter (fun n =>
        ∃ h, altura n h ∧ altura (n + 1) h ∧ mitades n h ≠ mitades (n + 1) h)).card +
        ((Finset.range N).filter (fun n => ∃ j, Hienas.coalescen n j)).card ≤ N := by omega
    have hNr : (0 : ℝ) < N := by exact_mod_cast hN
    have hcr : (((Finset.range N).filter (fun n =>
        ∃ h, altura n h ∧ altura (n + 1) h ∧ mitades n h ≠ mitades (n + 1) h)).card : ℝ) +
        ((Finset.range N).filter (fun n => ∃ j, Hienas.coalescen n j)).card ≤ N := by
      exact_mod_cast hc
    rw [div_le_iff₀ hNr, sub_mul, div_mul_cancel₀ _ hNr.ne', one_mul]
    linarith
  have hlow : ∀ N : ℕ, (0 : ℝ) ≤ (((Finset.range N).filter (fun n =>
      ∃ h, altura n h ∧ altura (n + 1) h ∧ mitades n h ≠ mitades (n + 1) h)).card : ℝ) / N :=
    fun N => div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)
  have hlim : Tendsto (fun N : ℕ => 1 - Hienas.d N) atTop (𝓝 0) := by
    have := (tendsto_const_nhds : Tendsto (fun _ : ℕ => (1 : ℝ)) atTop (𝓝 1)).sub hD
    simpa using this
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hlim hlow hup

/-- Un encuentro en el paso j con `2^j + 3 < 15n` es equilibrado. `Hienas.equilibrio`
    pedía `2^j ≤ n`; aquí basta la cota `Res_j ≤ 1 + 2^j/(3x)` de `cotas`. -/
theorem equilibrio_quince {n j : ℕ} (hj : 2 ^ j + 3 < 15 * n)
    (he : C^[j] n = C^[j] (n + 1)) : mitades n j = mitades (n + 1) j := by
  have V1 := (cotas j n).2
  have V2 := (cotas j (n + 1)).2
  rw [← he] at V2
  apply pandas_encuentro he
  · have : 3 ^ triples n j * (3 * n + 2 ^ j) ≤ 3 ^ triples n j * (18 * n) :=
      Nat.mul_le_mul_left _ (by omega)
    nlinarith
  · have : 3 ^ triples (n + 1) j * (3 * (n + 1) + 2 ^ j) < 3 ^ triples (n + 1) j * (18 * n) :=
      Nat.mul_lt_mul_of_pos_left (by omega) (by positivity)
    nlinarith

/-! ## Marmotas: combinar escalas para el residuo -/

/-- Transporte: si las k primeras iteradas de x no bajan de B, el residuo parcial es a lo
    sumo `(1 + 1/(3B))^S`, con S los pasos `3n+1`. En enteros:
    `2^m · C^k(x) · (3B)^S ≤ 3^S · x · (3B+1)^S`. -/
theorem transporte (B : ℕ) : ∀ k x, (∀ i, i < k → B ≤ C^[i] x) →
    2 ^ Hienas.mitades k x * C^[k] x * (3 * B) ^ Hienas.triples k x ≤
      3 ^ Hienas.triples k x * x * (3 * B + 1) ^ Hienas.triples k x := by
  intro k
  induction k with
  | zero => intro x _; simp [Hienas.mitades, Hienas.triples]
  | succ k ih =>
    intro x hx
    have hBx : B ≤ x := hx 0 (by omega)
    have IH := ih (C x) (fun i hi => by
      have := hx (i + 1) (by omega)
      rwa [Function.iterate_succ_apply] at this)
    rw [Function.iterate_succ_apply]
    have hm : Hienas.mitades (k + 1) x =
        (if x % 2 = 0 then 1 else 0) + Hienas.mitades k (C x) := rfl
    have ht : Hienas.triples (k + 1) x =
        (if x % 2 = 0 then 0 else 1) + Hienas.triples k (C x) := rfl
    rw [hm, ht]
    rcases Nat.mod_two_eq_zero_or_one x with h | h
    · rw [if_pos h, if_pos h]
      have hC : C x = x / 2 := by simp [C, h]
      rw [hC] at IH ⊢
      generalize Hienas.mitades k (x / 2) = m at IH ⊢
      generalize Hienas.triples k (x / 2) = t at IH ⊢
      generalize C^[k] (x / 2) = Z at IH ⊢
      obtain ⟨y, rfl⟩ : ∃ y, x = 2 * y := ⟨x / 2, by omega⟩
      rw [show 2 * y / 2 = y by omega] at IH
      calc 2 ^ (1 + m) * Z * (3 * B) ^ (0 + t) = 2 * (2 ^ m * Z * (3 * B) ^ t) := by ring
        _ ≤ 2 * (3 ^ t * y * (3 * B + 1) ^ t) := Nat.mul_le_mul_left _ IH
        _ = 3 ^ (0 + t) * (2 * y) * (3 * B + 1) ^ (0 + t) := by ring
    · rw [if_neg (by omega), if_neg (by omega)]
      have hC : C x = 3 * x + 1 := by simp [C, show x % 2 ≠ 0 by omega]
      rw [hC] at IH ⊢
      generalize Hienas.mitades k (3 * x + 1) = m at IH ⊢
      generalize Hienas.triples k (3 * x + 1) = t at IH ⊢
      generalize C^[k] (3 * x + 1) = Z at IH ⊢
      have key : 3 * B * (3 * x + 1) ≤ 3 * x * (3 * B + 1) := by nlinarith
      calc 2 ^ (0 + m) * Z * (3 * B) ^ (1 + t) = 3 * B * (2 ^ m * Z * (3 * B) ^ t) := by ring
        _ ≤ 3 * B * (3 ^ t * (3 * x + 1) * (3 * B + 1) ^ t) := Nat.mul_le_mul_left _ IH
        _ = 3 ^ t * (3 * B + 1) ^ t * (3 * B * (3 * x + 1)) := by ring
        _ ≤ 3 ^ t * (3 * B + 1) ^ t * (3 * x * (3 * B + 1)) := Nat.mul_le_mul_left _ key
        _ = 3 ^ (1 + t) * x * (3 * B + 1) ^ (1 + t) := by ring

/-- Marmotas. Si todo m < B con altura cumple `b · 2^σ∞(m) ≤ a · 3^S(m) · m`, es decir,
    `Res(m) ≤ a/b`, y la órbita de x entra en [1, B) en el paso k tras S' pasos `3n+1`
    hechos en valores ≥ B, entonces `Res(x) ≤ (a/b) · (1 + 1/(3B))^S'`. -/
theorem residuo_por_escalas {B a b x h k : ℕ}
    (hbase : ∀ m h', m < B → altura m h' → b * 2 ^ mitades m h' ≤ a * (3 ^ triples m h' * m))
    (ha : altura x h) (hk : k ≤ h) (hsobre : ∀ i, i < k → B ≤ C^[i] x)
    (hbajo : C^[k] x < B) :
    b * 2 ^ mitades x h * (3 * B) ^ triples x k ≤
      a * (3 ^ triples x h * x) * (3 * B + 1) ^ triples x k := by
  have hy := altura_cola ha hk
  have hy1 := pos_de_altura hy
  have base := hbase _ _ hbajo hy
  have tr := transporte B k x hsobre
  rw [← mitades_hienas, ← triples_hienas] at tr
  obtain ⟨r, rfl⟩ : ∃ r, h = k + r := ⟨h - k, by omega⟩
  rw [show k + r - k = r by omega] at base
  have em : mitades x (k + r) = mitades x k + mitades (C^[k] x) r := by
    rw [mitades_hienas, mitades_hienas, mitades_hienas, mitades_add]
  have et : triples x (k + r) = triples x k + triples (C^[k] x) r := by
    rw [triples_hienas, triples_hienas, triples_hienas, triples_add]
  rw [em, et]
  clear em et hy
  generalize C^[k] x = y at hy1 base tr ⊢
  generalize mitades x k = m1 at tr ⊢
  generalize triples x k = s1 at tr ⊢
  generalize mitades y r = m2 at base ⊢
  generalize triples y r = s2 at base ⊢
  have hprod := Nat.mul_le_mul base tr
  have e1 : b * 2 ^ m2 * (2 ^ m1 * y * (3 * B) ^ s1) =
      (b * 2 ^ (m1 + m2) * (3 * B) ^ s1) * y := by ring
  have e2 : a * (3 ^ s2 * y) * (3 ^ s1 * x * (3 * B + 1) ^ s1) =
      (a * (3 ^ (s1 + s2) * x) * (3 * B + 1) ^ s1) * y := by ring
  rw [e1, e2] at hprod
  exact Nat.le_of_mul_le_mul_right hprod hy1

/-- `(N+1)^S ≤ 3 · N^S` si `3S ≤ 2N`. Con `x = 1/N`, Bernoulli da
    `(1+x)^S · (1 − Sx) ≤ (1+x)^S · (1−x)^S = (1 − x²)^S ≤ 1`, y `1 − Sx ≥ 1/3`. -/
theorem potencia_tres {N S : ℕ} (hN : 1 ≤ N) (hS : 3 * S ≤ 2 * N) :
    ((N : ℚ) + 1) ^ S ≤ 3 * (N : ℚ) ^ S := by
  have hNpos : (0 : ℚ) < N := by exact_mod_cast hN
  have hx0 : (0 : ℚ) ≤ 1 / N := by positivity
  have hx1 : (1 : ℚ) / N ≤ 1 := by
    rw [div_le_one hNpos]; exact_mod_cast hN
  have hb : 1 + (S : ℚ) * (-(1 / N)) ≤ (1 + -(1 / N)) ^ S :=
    one_add_mul_le_pow (by linarith) S
  have hsq : (1 + 1 / (N : ℚ)) ^ S * (1 + -(1 / N)) ^ S ≤ 1 := by
    rw [← mul_pow]
    apply pow_le_one₀ <;> nlinarith
  have hSx : (S : ℚ) * (1 / N) ≤ 2 / 3 := by
    rw [mul_one_div, div_le_div_iff₀ hNpos (by norm_num)]
    have : (3 * S : ℚ) ≤ 2 * N := by exact_mod_cast hS
    linarith
  have hpos : (0 : ℚ) ≤ (1 + 1 / (N : ℚ)) ^ S := by positivity
  have h1 : (1 + 1 / (N : ℚ)) ^ S * (1 / 3) ≤ 1 := by
    calc (1 + 1 / (N : ℚ)) ^ S * (1 / 3)
        ≤ (1 + 1 / (N : ℚ)) ^ S * (1 + (S : ℚ) * (-(1 / N))) := by
          apply mul_le_mul_of_nonneg_left _ hpos
          linarith
      _ ≤ (1 + 1 / (N : ℚ)) ^ S * (1 + -(1 / N)) ^ S := mul_le_mul_of_nonneg_left hb hpos
      _ ≤ 1 := hsq
  have h3 : ((N : ℚ) + 1) ^ S = (N : ℚ) ^ S * (1 + 1 / N) ^ S := by
    rw [← mul_pow, mul_add, mul_one, mul_one_div_cancel hNpos.ne']
  rw [h3]
  have : (0 : ℚ) ≤ (N : ℚ) ^ S := by positivity
  nlinarith

/-- La órbita de x entra en [1, B) en el paso k ≤ h tras a lo sumo 2B pasos `3n+1`, todos
    ellos en valores ≥ B. -/
def EntraPronto (B x h : ℕ) : Prop :=
  ∃ k, k ≤ h ∧ (∀ i, i < k → B ≤ C^[i] x) ∧ C^[k] x < B ∧ triples x k ≤ 2 * B

/-- Con una base `Res ≤ a/b < 4/3` en [1, B), el transporte deja `Res(x) < 4`. -/
theorem residuo_menor_cuatro {B a b x h : ℕ} (hB : 1 ≤ B) (hab : 3 * a < 4 * b)
    (hbase : ∀ m h', m < B → altura m h' → b * 2 ^ mitades m h' ≤ a * (3 ^ triples m h' * m))
    (ha : altura x h) (hx : EntraPronto B x h) :
    2 ^ mitades x h < 4 * (3 ^ triples x h * x) := by
  obtain ⟨k, hk, hs, hbj, hS⟩ := hx
  have R := residuo_por_escalas hbase ha hk hs hbj
  have hx1 := pos_de_altura ha
  by_contra hcon
  rw [not_lt] at hcon
  generalize mitades x h = M at R hcon
  generalize triples x h = T at R hcon
  generalize triples x k = S at R hS
  have hQ : (3 * B + 1) ^ S ≤ 3 * (3 * B) ^ S := by
    have := potencia_tres (N := 3 * B) (S := S) (by omega) (by omega)
    exact_mod_cast this
  have hX : 0 < 3 ^ T * x := Nat.mul_pos (by positivity) hx1
  have hP : 0 < (3 * B) ^ S := pow_pos (by omega) S
  have s1 : 4 * b * (3 ^ T * x * (3 * B) ^ S) ≤ 3 * a * (3 ^ T * x * (3 * B) ^ S) := by
    calc 4 * b * (3 ^ T * x * (3 * B) ^ S) = b * (4 * (3 ^ T * x)) * (3 * B) ^ S := by ring
      _ ≤ b * 2 ^ M * (3 * B) ^ S := by gcongr
      _ ≤ a * (3 ^ T * x) * (3 * B + 1) ^ S := R
      _ ≤ a * (3 ^ T * x) * (3 * (3 * B) ^ S) := by gcongr
      _ = 3 * a * (3 ^ T * x * (3 * B) ^ S) := by ring
  have s2 := Nat.le_of_mul_le_mul_right s1 (Nat.mul_pos hX hP)
  omega

/-- Marmotas y la pregunta de Gao: con una base `Res ≤ a/b < 4/3` en [1, B), igual altura
    implica igual σ∞ para todo par n, n+1 cuyas órbitas entren pronto en [1, B). -/
theorem gao_por_escalas {B a b n h : ℕ} (hB : 1 ≤ B) (hab : 3 * a < 4 * b)
    (hbase : ∀ m h', m < B → altura m h' → b * 2 ^ mitades m h' ≤ a * (3 ^ triples m h' * m))
    (a1 : altura n h) (a2 : altura (n + 1) h)
    (e1 : EntraPronto B n h) (e2 : EntraPronto B (n + 1) h) :
    mitades n h = mitades (n + 1) h := by
  have hn := dos_de_par a1 a2
  have c1 := residuo_menor_cuatro hB hab hbase a1 e1
  have c2 := residuo_menor_cuatro hB hab hbase a2 e2
  refine (pandas a1 a2 ?_ ?_).1
  · omega
  · have hZ := Nat.mul_le_mul_left (3 ^ triples (n + 1) h) hn
    have : 4 * (3 ^ triples (n + 1) h * (n + 1)) ≤ 6 * (3 ^ triples (n + 1) h * n) := by
      nlinarith
    omega

end PandasGao

#print axioms PandasGao.pandas
#print axioms PandasGao.pandas_escrito
#print axioms PandasGao.gao_de_residuo
#print axioms PandasGao.gao_casi_siempre
#print axioms PandasGao.equilibrio_quince
#print axioms PandasGao.residuo_por_escalas
#print axioms PandasGao.gao_por_escalas

/- Cotejo con los cálculos: 993 alcanza el residuo máximo de [1, 2^20), según
   `verificar_pandas.py` y `pandas_gao.py`; la racha 943..949 de Gao cumple las hipótesis
   de `pandas` con holgura. Si una cuenta no coincide, el archivo no compila. -/
#guard decide (GarnerEnunciado.altura 993 93) &&
  PandasGao.residuo 993 93 == (2305843009213693952 : ℚ) / 1840049047529878113
#guard (List.range 6).all (fun i =>
  decide (GarnerEnunciado.altura (943 + i) 36) && decide (GarnerEnunciado.altura (944 + i) 36) &&
  decide (2 ^ GarnerEnunciado.mitades (943 + i) 36 ≤
    6 * (3 ^ PandasGao.triples (943 + i) 36 * (943 + i))) &&
  decide (2 ^ GarnerEnunciado.mitades (944 + i) 36 <
    6 * (3 ^ PandasGao.triples (944 + i) 36 * (943 + i))))
