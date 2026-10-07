import CasaPlano

/-! # El retrato del fugitivo

Ruta B, paso 2 (06-10-2026). Inventario y ruta en `LEEME.md` de esta carpeta.

Una **fuga pura** (`FugaPura n`) es un número cuyo pronóstico `3^S k n / 2^k` nunca baja
de 1: su primer cruce τ(n) no existe. El muro B dice exactamente que no hay ninguna con
`n ≥ 2` (`CasaPlano.muroB_iff`). La reducción al absurdo supone una y anota lo que tendría
que cumplir. Este archivo demuestra sus rasgos, sin hipótesis externas:

* `rasgo_sube`: en todo momento lleva al menos 63 subidas de cada 100 pasos;
* `rasgo_sin_repetir` y `rasgo_infinito`: su órbita nunca repite un valor y crece hacia el
  infinito; en particular es una fuga (`rasgo_fuga`);
* `rasgo_no_periodico`: su patrón de subidas y bajadas nunca se vuelve periódico;
* `rasgo_raro_cuenta` y `rasgo_raro`: casi ningún número puede ser así (densidad cero,
  Terras 1976); entre 0 y N−1 hay a lo sumo `N / 16^m + 2^(96m)`, para cada `m`.

`retrato` reúne los rasgos de un mismo número. Ninguno contradice a otro: el choque, si
existe, está por encontrar (paso 3 de la ruta).

Herramientas: `misma_paridad_congruentes` (dos números con las mismas `k` primeras
paridades coinciden módulo `2^k`), `ciclo_cruza` (en un ciclo, el pronóstico de un periodo
baja de 1) y `cuenta_sin_cruce` (cuenta exacta por bloques de `2^(100m)`).

Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaRetrato

open Ocelotas OcelotasContador CasaPlano

/-! ## Sube mucho -/

/-- Una fuga pura es al menos 2: el 0 y el 1 cruzan. -/
theorem fuga_pura_dos {n : ℕ} (h : FugaPura n) : 2 ≤ n := by
  by_contra hn
  apply h
  rcases (by omega : n = 0 ∨ n = 1) with rfl | rfl
  · exact ⟨1, by decide⟩
  · exact ⟨2, by decide⟩

/-- La fuga pura, paso a paso: el pronóstico nunca baja de 1. -/
theorem nunca_cruza {n : ℕ} (h : FugaPura n) (k : ℕ) : 2 ^ k ≤ 3 ^ S k n :=
  not_lt.mp fun hk => h ⟨k, hk⟩

/-- Si `2^j ≤ 3^s`, entonces `63 j ≤ 100 s`, porque `3^63 < 2^100`. -/
theorem sesenta_y_tres {j s : ℕ} (h : 2 ^ j ≤ 3 ^ s) : 63 * j ≤ 100 * s := by
  by_contra hc
  have h1 : 2 ^ (j * 100) ≤ 3 ^ (s * 100) := by
    rw [pow_mul, pow_mul]
    exact Nat.pow_le_pow_left h 100
  have h2 : 3 ^ (s * 100) < 3 ^ (63 * j) := Nat.pow_lt_pow_right (by norm_num) (by omega)
  have h3 : 3 ^ (63 * j) ≤ 2 ^ (j * 100) := by
    rw [pow_mul, mul_comm j 100, pow_mul]
    exact Nat.pow_le_pow_left (by norm_num) j
  exact lt_irrefl _ (lt_of_le_of_lt h1 (lt_of_lt_of_le h2 h3))

/-- **Rasgo: sube mucho.** En todo momento, una fuga pura lleva al menos 63 subidas de
    cada 100 pasos. -/
theorem rasgo_sube {n : ℕ} (h : FugaPura n) (k : ℕ) : 63 * k ≤ 100 * S k n :=
  sesenta_y_tres (nunca_cruza h k)

/-! ## Se escapa -/

/-- En un ciclo, el pronóstico de un periodo baja de 1: si `m ≥ 1` vuelve a sí mismo en
    `p ≥ 1` pasos, entonces `3^S p m < 2^p`. -/
theorem ciclo_cruza {m p : ℕ} (hm : 1 ≤ m) (hp : 1 ≤ p) (hmp : T^[p] m = m) :
    3 ^ S p m < 2 ^ p := by
  have h := cota_inferior m p
  rw [hmp] at h
  exact lt_of_le_of_ne (Nat.le_of_mul_le_mul_right h (by omega)) (tres_ne_dos hp)

/-- Dar `t` vueltas a un ciclo de `p` pasos que empieza en el paso `i`. -/
theorem vueltas {n m i p : ℕ} (him : T^[i] n = m) (hmp : T^[p] m = m) (t : ℕ) :
    T^[i + p * t] n = m ∧ S (i + p * t) n = S i n + S p m * t := by
  induction t with
  | zero => simp [him]
  | succ t ih =>
    have e : i + p * (t + 1) = (i + p * t) + p := by ring
    rw [e, iter_add, ih.1, hmp, S_add, ih.2, ih.1]
    exact ⟨rfl, by ring⟩

/-- Bernoulli entero: `v^t (v + t) ≤ v (v + 1)^t`. -/
theorem bernoulli (v : ℕ) : ∀ t, v ^ t * (v + t) ≤ v * (v + 1) ^ t := by
  intro t
  induction t with
  | zero => simp
  | succ t ih =>
    calc v ^ (t + 1) * (v + (t + 1)) ≤ v ^ t * (v + t) * (v + 1) :=
          Nat.le.intro (show v ^ (t + 1) * (v + (t + 1)) + v ^ t * t =
            v ^ t * (v + t) * (v + 1) by ring)
      _ ≤ v * (v + 1) ^ t * (v + 1) := Nat.mul_le_mul_right _ ih
      _ = v * (v + 1) ^ (t + 1) := by ring

/-- Si `v < u`, la desigualdad `d·u^t ≤ c·v^t` con `d ≥ 1` falla al dar `t = c·v` vueltas. -/
theorem crece_mas {u v c d : ℕ} (hvu : v < u) (hv : 1 ≤ v) (hd : 1 ≤ d) :
    c * v ^ (c * v) < d * u ^ (c * v) := by
  by_contra hcon
  have hcon' : d * u ^ (c * v) ≤ c * v ^ (c * v) := not_lt.mp hcon
  have h4 : v ^ (c * v) * (v + c * v) ≤ v ^ (c * v) * (v * c) :=
    calc v ^ (c * v) * (v + c * v) ≤ v * (v + 1) ^ (c * v) := bernoulli v (c * v)
      _ ≤ v * u ^ (c * v) := Nat.mul_le_mul_left v (Nat.pow_le_pow_left (by omega) _)
      _ ≤ v * (d * u ^ (c * v)) := Nat.mul_le_mul_left v (Nat.le_mul_of_pos_left _ hd)
      _ ≤ v * (c * v ^ (c * v)) := Nat.mul_le_mul_left v hcon'
      _ = v ^ (c * v) * (v * c) := by ring
  have h5 := Nat.le_of_mul_le_mul_left h4 (pow_pos hv _)
  have h6 : v + c * v ≤ c * v := by rwa [mul_comm v c] at h5
  omega

/-- **Rasgo: nunca repite.** La órbita de una fuga pura nunca vuelve a un valor ya
    visitado: si volviera, daría vueltas a un ciclo y el pronóstico terminaría bajando
    de 1. -/
theorem rasgo_sin_repetir {n : ℕ} (h : FugaPura n) {i j : ℕ} (hij : i < j) :
    T^[i] n ≠ T^[j] n := by
  intro heq
  have hm : 1 ≤ T^[i] n := iter_pos (by have := fuga_pura_dos h; omega) i
  have hmp : T^[j - i] (T^[i] n) = T^[i] n := by
    rw [← Function.iterate_add_apply, Nat.sub_add_cancel hij.le, heq]
  have hc := ciclo_cruza hm (by omega) hmp
  have hv : 1 ≤ 3 ^ S (j - i) (T^[i] n) := Nat.one_le_pow _ _ (by norm_num)
  obtain ⟨-, hS⟩ := vueltas (n := n) (i := i) rfl hmp (3 ^ S i n * 3 ^ S (j - i) (T^[i] n))
  have h1 := nunca_cruza h (i + (j - i) * (3 ^ S i n * 3 ^ S (j - i) (T^[i] n)))
  rw [hS, pow_add, pow_add, pow_mul (2 : ℕ) (j - i), pow_mul (3 : ℕ) (S (j - i) (T^[i] n))]
    at h1
  have h2 := crece_mas (c := 3 ^ S i n) (d := 2 ^ i) hc hv Nat.one_le_two_pow
  exact absurd h1 (not_le.mpr h2)

/-- La órbita de una fuga pura nunca repite valores. -/
theorem rasgo_inyectiva {n : ℕ} (h : FugaPura n) :
    Function.Injective (fun k => T^[k] n) := by
  intro i j heq
  by_contra hij
  rcases lt_or_gt_of_ne hij with hlt | hlt
  · exact rasgo_sin_repetir h hlt heq
  · exact rasgo_sin_repetir h hlt heq.symm

/-- **Rasgo: se escapa.** La órbita de una fuga pura crece hacia el infinito: pasado cierto
    paso, nunca vuelve a quedar por debajo de una cota dada. -/
theorem rasgo_infinito {n : ℕ} (h : FugaPura n) (M : ℕ) :
    ∃ K, ∀ k, K ≤ k → M < T^[k] n := by
  have hfin : ((fun k => T^[k] n) ⁻¹' Set.Iic M).Finite :=
    (Set.finite_Iic M).preimage (rasgo_inyectiva h).injOn
  obtain ⟨K, hK⟩ := hfin.bddAbove
  refine ⟨K + 1, fun k hk => ?_⟩
  by_contra hc
  have hmem : k ∈ (fun k => T^[k] n) ⁻¹' Set.Iic M := by
    simp only [Set.mem_preimage, Set.mem_Iic]
    omega
  have := hK hmem
  omega

/-- En particular, una fuga pura es una fuga: su órbita supera cualquier cota. -/
theorem rasgo_fuga {n : ℕ} (h : FugaPura n) : Fuga n := fun M =>
  let ⟨K, hK⟩ := rasgo_infinito h M
  ⟨K, hK K le_rfl⟩

/-! ## Su patrón nunca se vuelve periódico -/

/-- Dos números con las mismas `k` primeras paridades coinciden módulo `2^k`. -/
theorem misma_paridad_congruentes : ∀ k n n' : ℕ,
    (∀ i, i < k → T^[i] n % 2 = T^[i] n' % 2) → n % 2 ^ k = n' % 2 ^ k := by
  intro k
  induction k with
  | zero => intro n n' _; simp [Nat.mod_one]
  | succ k ih =>
    intro n n' h
    have h0 : n % 2 = n' % 2 := h 0 (by omega)
    have hT : T n % 2 ^ k = T n' % 2 ^ k := ih (T n) (T n') fun i hi => by
      have := h (i + 1) (by omega)
      rwa [iterT_succ, iterT_succ] at this
    rcases Nat.mod_two_eq_zero_or_one n with hp | hp
    · -- pares: `n = 2a` y `T n = a`
      obtain ⟨a, rfl⟩ : ∃ a, n = 2 * a := ⟨n / 2, by omega⟩
      obtain ⟨a', rfl⟩ : ∃ a', n' = 2 * a' := ⟨n' / 2, by omega⟩
      have e : ∀ x, T (2 * x) = x := fun x => by
        unfold T
        rw [if_pos (by omega)]
        omega
      rw [e, e] at hT
      have h2 : 2 * a ≡ 2 * a' [MOD 2 * 2 ^ k] := Nat.ModEq.mul_left' 2 hT
      rw [← pow_succ'] at h2
      exact h2
    · -- impares: `n = 2a + 1` y `T n = 3a + 2`
      obtain ⟨a, rfl⟩ : ∃ a, n = 2 * a + 1 := ⟨n / 2, by omega⟩
      obtain ⟨a', rfl⟩ : ∃ a', n' = 2 * a' + 1 := ⟨n' / 2, by omega⟩
      have e : ∀ x, T (2 * x + 1) = 3 * x + 2 := fun x => by
        unfold T
        rw [if_neg (by omega)]
        omega
      rw [e, e] at hT
      have h3 : 3 * a ≡ 3 * a' [MOD 2 ^ k] := Nat.ModEq.add_right_cancel' 2 hT
      have ha : a ≡ a' [MOD 2 ^ k] :=
        Nat.ModEq.cancel_left_of_coprime (Nat.Coprime.pow_left k (by decide : Nat.gcd 2 3 = 1)) h3
      have h2 : 2 * a ≡ 2 * a' [MOD 2 * 2 ^ k] := Nat.ModEq.mul_left' 2 ha
      rw [← pow_succ'] at h2
      exact Nat.ModEq.add_right 1 h2

/-- Dos números con el mismo patrón completo de subidas y bajadas son el mismo número. -/
theorem mismo_patron_iguales {x y : ℕ} (h : ∀ i, T^[i] x % 2 = T^[i] y % 2) : x = y := by
  have hk := misma_paridad_congruentes (x + y + 1) x y fun i _ => h i
  have hx : x < 2 ^ (x + y + 1) := lt_of_lt_of_le (by omega) Nat.lt_two_pow_self.le
  have hy : y < 2 ^ (x + y + 1) := lt_of_lt_of_le (by omega) Nat.lt_two_pow_self.le
  rwa [Nat.mod_eq_of_lt hx, Nat.mod_eq_of_lt hy] at hk

/-- Si el patrón de `n` se vuelve periódico desde el paso `a`, con periodo `p`, la órbita
    vuelve en el paso `a + p` al valor del paso `a`. -/
theorem patron_periodico_repite {n a p : ℕ}
    (h : ∀ i, a ≤ i → T^[i + p] n % 2 = T^[i] n % 2) : T^[a + p] n = T^[a] n := by
  apply mismo_patron_iguales
  intro i
  rw [← Function.iterate_add_apply, ← Function.iterate_add_apply,
    show i + (a + p) = (a + i) + p by ring, show i + a = a + i by ring]
  exact h (a + i) (by omega)

/-- **Rasgo: patrón nunca periódico.** El patrón de subidas y bajadas de una fuga pura
    nunca se vuelve periódico, desde ningún paso y con ningún periodo. -/
theorem rasgo_no_periodico {n : ℕ} (hF : FugaPura n) (a p : ℕ) (hp : 1 ≤ p) :
    ¬ ∀ i, a ≤ i → T^[i + p] n % 2 = T^[i] n % 2 := fun h =>
  rasgo_sin_repetir hF (by omega : a < a + p) (patron_periodico_repite h).symm

/-! ## Casi ningún número es así (Terras, 1976) -/

/-- Las posiciones de las subidas entre los `k` primeros pasos de `n`. -/
def subidas (k n : ℕ) : Finset ℕ := (Finset.range k).filter fun i => T^[i] n % 2 = 1

theorem card_subidas (k n : ℕ) : (subidas k n).card = S k n := by
  induction k with
  | zero => simp [subidas, S]
  | succ k ih =>
    have hS : S (k + 1) n = S k n + T^[k] n % 2 := by
      rw [S_add]
      simp [S]
    rw [hS, ← ih]
    unfold subidas
    rw [Finset.range_add_one, Finset.filter_insert]
    split_ifs with hk
    · rw [Finset.card_insert_of_notMem (by simp), hk]
    · have h0 : T^[k] n % 2 = 0 := by omega
      rw [h0, Nat.add_zero]

theorem subidas_sub (k n : ℕ) : subidas k n ⊆ Finset.range k := Finset.filter_subset _ _

/-- Las subidas de los `k` primeros pasos determinan `n` módulo `2^k`. -/
theorem congruentes_de_subidas {k n n' : ℕ} (h : subidas k n = subidas k n') :
    n % 2 ^ k = n' % 2 ^ k := by
  apply misma_paridad_congruentes
  intro i hi
  have hiff : i ∈ subidas k n ↔ i ∈ subidas k n' := by rw [h]
  simp only [subidas, Finset.mem_filter, Finset.mem_range] at hiff
  rcases Nat.mod_two_eq_zero_or_one (T^[i] n) with ha | ha <;>
    rcases Nat.mod_two_eq_zero_or_one (T^[i] n') with hb | hb
  · rw [ha, hb]
  · exact absurd (hiff.2 ⟨hi, hb⟩).2 (by omega)
  · exact absurd (hiff.1 ⟨hi, ha⟩).2 (by omega)
  · rw [ha, hb]

/-- Cuenta por bloques de `2^k`: entre 0 y N−1, los números cuya cantidad de subidas en
    `k` pasos cumple `Q` son a lo sumo `N / 2^k + 1` veces los patrones de longitud `k`
    que cumplen `Q`. -/
theorem cuenta_por_bloques (N k : ℕ) (Q : ℕ → Prop) [DecidablePred Q] :
    ((Finset.range N).filter fun n => Q (S k n)).card ≤
      (N / 2 ^ k + 1) * ((Finset.range k).powerset.filter fun A => Q A.card).card := by
  rw [← Finset.card_range (N / 2 ^ k + 1), ← Finset.card_product]
  refine Finset.card_le_card_of_injOn (fun n => (n / 2 ^ k, subidas k n)) ?_ ?_
  · intro n hn
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hn
    simp only [Finset.mem_coe, Finset.mem_product, Finset.mem_range, Finset.mem_filter,
      Finset.mem_powerset, card_subidas]
    exact ⟨Nat.lt_succ_of_le (Nat.div_le_div_right hn.1.le), subidas_sub k n, hn.2⟩
  · intro n _ n' _ heq
    simp only [Prod.mk.injEq] at heq
    rw [← Nat.div_add_mod n (2 ^ k), ← Nat.div_add_mod n' (2 ^ k), heq.1,
      congruentes_de_subidas heq.2]

/-- Entre los subconjuntos de `{0, …, 100m − 1}`, los que cumplen `2^(100m) ≤ 3^|A|` son a
    lo sumo `2^(96m)`: cada uno pesa al menos `2^(63m)` y el peso total es `3^(100m)`. -/
theorem pocos_patrones (m : ℕ) :
    ((Finset.range (100 * m)).powerset.filter fun A => 2 ^ (100 * m) ≤ 3 ^ A.card).card
      ≤ 2 ^ (96 * m) := by
  set B := (Finset.range (100 * m)).powerset.filter fun A => 2 ^ (100 * m) ≤ 3 ^ A.card
  have hgrande : ∀ A ∈ B, 63 * m ≤ A.card := by
    intro A hA
    have := sesenta_y_tres (Finset.mem_filter.1 hA).2
    omega
  have hsuma : ∑ A ∈ (Finset.range (100 * m)).powerset, 2 ^ A.card = 3 ^ (100 * m) := by
    have := Finset.sum_pow_mul_eq_add_pow (2 : ℕ) 1 (Finset.range (100 * m))
    simpa using this
  have h1 : B.card * 2 ^ (63 * m) ≤ 3 ^ (100 * m) := by
    calc B.card * 2 ^ (63 * m) = ∑ A ∈ B, 2 ^ (63 * m) := by rw [Finset.sum_const, smul_eq_mul]
      _ ≤ ∑ A ∈ B, 2 ^ A.card :=
          Finset.sum_le_sum fun A hA => Nat.pow_le_pow_right (by norm_num) (hgrande A hA)
      _ ≤ ∑ A ∈ (Finset.range (100 * m)).powerset, 2 ^ A.card :=
          Finset.sum_le_sum_of_subset (Finset.filter_subset _ _)
      _ = 3 ^ (100 * m) := hsuma
  have h2 : 3 ^ (100 * m) ≤ 2 ^ (96 * m) * 2 ^ (63 * m) := by
    rw [← pow_add, show 96 * m + 63 * m = 159 * m by ring, pow_mul, pow_mul]
    exact Nat.pow_le_pow_left (by norm_num) m
  exact Nat.le_of_mul_le_mul_right (h1.trans h2) (by positivity)

/-- **Cuenta de Terras.** Entre 0 y N−1, a lo sumo `(N / 2^(100m) + 1) · 2^(96m)` números
    aguantan `100m` pasos sin que el pronóstico baje de 1. -/
theorem cuenta_sin_cruce (N m : ℕ) :
    ((Finset.range N).filter fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n).card ≤
      (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) :=
  (cuenta_por_bloques N (100 * m) (fun s => 2 ^ (100 * m) ≤ 3 ^ s)).trans
    (Nat.mul_le_mul_left _ (pocos_patrones m))

open Classical in
/-- **Rasgo: rareza, en cifras.** Para cada `m`, entre 0 y N−1 hay a lo sumo
    `N / 16^m + 2^(96m)` fugas puras. -/
theorem rasgo_raro_cuenta (N m : ℕ) :
    ((Finset.range N).filter FugaPura).card ≤ N / 16 ^ m + 2 ^ (96 * m) := by
  have hsub : (Finset.range N).filter FugaPura ⊆
      (Finset.range N).filter fun n => 2 ^ (100 * m) ≤ 3 ^ S (100 * m) n := by
    intro n hn
    rw [Finset.mem_filter] at hn ⊢
    exact ⟨hn.1, nunca_cruza hn.2 _⟩
  have h1 := (Finset.card_le_card hsub).trans (cuenta_sin_cruce N m)
  have e : 2 ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h2 : N / 2 ^ (100 * m) * 2 ^ (96 * m) ≤ N / 16 ^ m := by
    rw [e, ← Nat.div_div_eq_div_mul]
    exact Nat.div_mul_le_self _ _
  calc ((Finset.range N).filter FugaPura).card ≤ (N / 2 ^ (100 * m) + 1) * 2 ^ (96 * m) := h1
    _ = N / 2 ^ (100 * m) * 2 ^ (96 * m) + 2 ^ (96 * m) := by ring
    _ ≤ N / 16 ^ m + 2 ^ (96 * m) := Nat.add_le_add_right h2 _

open Classical in
/-- **Rasgo: rareza (Terras, 1976).** Las fugas puras tienen densidad cero: para todo
    `ε > 0`, desde cierto `N₀` hay a lo sumo `ε·N` fugas puras entre 0 y N−1. -/
theorem rasgo_raro {ε : ℝ} (hε : 0 < ε) :
    ∃ N₀ : ℕ, ∀ N, N₀ ≤ N → (((Finset.range N).filter FugaPura).card : ℝ) ≤ ε * N := by
  obtain ⟨m, hm⟩ := pow_unbounded_of_one_lt (2 / ε) (by norm_num : (1 : ℝ) < 16)
  refine ⟨⌈2 * 2 ^ (96 * m) / ε⌉₊, fun N hN => ?_⟩
  have h1 : (((Finset.range N).filter FugaPura).card : ℝ) ≤
      ((N / 16 ^ m : ℕ) : ℝ) + 2 ^ (96 * m) := by
    exact_mod_cast rasgo_raro_cuenta N m
  have h16 : (0 : ℝ) < 16 ^ m := by positivity
  have h2 : ((N / 16 ^ m : ℕ) : ℝ) ≤ (N : ℝ) / 16 ^ m := by
    rw [le_div_iff₀ h16]
    exact_mod_cast Nat.div_mul_le_self N (16 ^ m)
  have h3 : (N : ℝ) / 16 ^ m ≤ ε * N / 2 := by
    rw [div_le_iff₀ h16]
    have h4 : 2 < 16 ^ m * ε := (div_lt_iff₀ hε).1 hm
    nlinarith [Nat.cast_nonneg (α := ℝ) N]
  have h5 : (2 : ℝ) ^ (96 * m) ≤ ε * N / 2 := by
    have h6 : 2 * 2 ^ (96 * m) / ε ≤ (N : ℝ) := (Nat.le_ceil _).trans (by exact_mod_cast hN)
    rw [div_le_iff₀ hε] at h6
    linarith
  linarith

/-! ## El retrato completo -/

/-- **El retrato del fugitivo.** Una fuga pura `n` cumple a la vez: es al menos 2; nunca
    baja de sí misma; lleva en todo momento al menos 63 subidas de cada 100 pasos; su
    órbita crece hacia el infinito; y su patrón de subidas y bajadas nunca se vuelve
    periódico. Además, casi ningún número es así (`rasgo_raro`). -/
theorem retrato {n : ℕ} (h : FugaPura n) :
    2 ≤ n ∧ (∀ k, n ≤ T^[k] n) ∧ (∀ k, 63 * k ≤ 100 * S k n) ∧
      (∀ M, ∃ K, ∀ k, K ≤ k → M < T^[k] n) ∧
      (∀ a p, 1 ≤ p → ¬ ∀ i, a ≤ i → T^[i + p] n % 2 = T^[i] n % 2) :=
  ⟨fuga_pura_dos h, fuga_pura_no_baja h, rasgo_sube h, rasgo_infinito h,
    rasgo_no_periodico h⟩

end CasaRetrato

#print axioms CasaRetrato.fuga_pura_dos
#print axioms CasaRetrato.sesenta_y_tres
#print axioms CasaRetrato.rasgo_sube
#print axioms CasaRetrato.ciclo_cruza
#print axioms CasaRetrato.rasgo_sin_repetir
#print axioms CasaRetrato.rasgo_infinito
#print axioms CasaRetrato.rasgo_fuga
#print axioms CasaRetrato.misma_paridad_congruentes
#print axioms CasaRetrato.mismo_patron_iguales
#print axioms CasaRetrato.rasgo_no_periodico
#print axioms CasaRetrato.card_subidas
#print axioms CasaRetrato.cuenta_por_bloques
#print axioms CasaRetrato.pocos_patrones
#print axioms CasaRetrato.cuenta_sin_cruce
#print axioms CasaRetrato.rasgo_raro_cuenta
#print axioms CasaRetrato.rasgo_raro
#print axioms CasaRetrato.retrato
