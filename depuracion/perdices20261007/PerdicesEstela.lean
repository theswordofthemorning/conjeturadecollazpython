import CasaRetrato

/-! # Perdices: tramo ligero de la estela vigente

Reproduce las pruebas necesarias de CasaTablero y CasaPlaneador, con
nombres bajo PerdicesEstela. Sólo se sustituye el acceso a rasgo_tamano
por su prueba tamano_antes_del_cruce. Así no se importa CasaOcelotas ni
sus certificados de 24 rachas, ajenos a estos resultados. Véase TAMANO.md.
-/

namespace PerdicesEstela

open Ocelotas OcelotasContador CasaPlano CasaRetrato

/-- Las subidas nunca superan a los pasos. -/
theorem S_le_pasos : ∀ k n, S k n ≤ k := by
  intro k
  induction k with
  | zero => intro n; simp [S]
  | succ k ih =>
    intro n
    have h1 := ih (T n)
    simp only [S]
    omega

/-- **El tamaño va pegado al pronóstico** mientras el pronóstico no haya bajado de 1:
    `n · 3^S/2^k ≤ T^k(n) ≤ (n + S/3) · 3^S/2^k`. La cota de abajo vale siempre
    (`cota_inferior`); la de arriba usa que antes de cada subida el pronóstico era al
    menos 1. -/
theorem tamano_antes_del_cruce {n : ℕ} :
    ∀ k, (∀ i, i < k → 2 ^ i ≤ 3 ^ S i n) →
      3 * (2 ^ k * T^[k] n) ≤ 3 ^ S k n * (3 * n + S k n) := by
  intro k
  induction k with
  | zero => intro _; simp [S]
  | succ k ih =>
    intro hpre
    have hk := hpre k (by omega)
    have ih' := ih fun i hi => hpre i (by omega)
    have hS : S (k + 1) n = S k n + T^[k] n % 2 := by
      rw [S_add]
      simp [S]
    rw [Function.iterate_succ_apply', hS]
    rcases Nat.mod_two_eq_zero_or_one (T^[k] n) with hp | hp
    · rw [hp, Nat.add_zero]
      have he := T_par hp
      calc 3 * (2 ^ (k + 1) * T (T^[k] n)) = 3 * (2 ^ k * (2 * T (T^[k] n))) := by ring
        _ = 3 * (2 ^ k * T^[k] n) := by rw [he]
        _ ≤ _ := ih'
    · rw [hp]
      have he := T_impar hp
      calc 3 * (2 ^ (k + 1) * T (T^[k] n)) = 3 * (2 ^ k * (2 * T (T^[k] n))) := by ring
        _ = 3 * (3 * (2 ^ k * T^[k] n)) + 3 * 2 ^ k := by rw [he]; ring
        _ ≤ 3 * (3 ^ S k n * (3 * n + S k n)) + 3 * 3 ^ S k n :=
            Nat.add_le_add (Nat.mul_le_mul_left 3 ih') (Nat.mul_le_mul_left 3 hk)
        _ = 3 ^ (S k n + 1) * (3 * n + (S k n + 1)) := by ring


/-- `v` es **casi fugitivo** de nivel `3^c`: su pronóstico nunca baja de `1/3^c`. Los de
    nivel 1 son las fugas puras (`casiFuga_cero`). -/
def CasiFuga (c v : ℕ) : Prop := ∀ i, 2 ^ i ≤ 3 ^ c * 3 ^ S i v

theorem casiFuga_cero (v : ℕ) : CasiFuga 0 v ↔ FugaPura v := by
  unfold CasiFuga
  simp only [pow_zero, one_mul]
  constructor
  · rintro h ⟨k, hk⟩
    exact absurd (h k) (not_le.mpr hk)
  · exact fun h i => nunca_cruza h i

/-- **Lo que deja un momento bajo.** Si en el paso `j` el pronóstico del fugitivo es a lo
    sumo `3^c`, el número al que llegó es casi fugitivo de nivel `3^c`: desde allí el
    pronóstico puede bajar, pero nunca más que el factor `3^c`. -/
theorem casi_fuga_de_bajo {n j c : ℕ} (h : FugaPura n) (hj : 3 ^ S j n ≤ 3 ^ c * 2 ^ j) :
    CasiFuga c (T^[j] n) := by
  intro i
  have h1 := nunca_cruza h (j + i)
  rw [S_add, pow_add, pow_add] at h1
  have h2 : 2 ^ j * 2 ^ i ≤ 2 ^ j * (3 ^ c * 3 ^ S i (T^[j] n)) :=
    calc 2 ^ j * 2 ^ i ≤ 3 ^ S j n * 3 ^ S i (T^[j] n) := h1
      _ ≤ 3 ^ c * 2 ^ j * 3 ^ S i (T^[j] n) := Nat.mul_le_mul_right _ hj
      _ = 2 ^ j * (3 ^ c * 3 ^ S i (T^[j] n)) := by ring
  exact Nat.le_of_mul_le_mul_left h2 (by positivity)

/-- Entre los subconjuntos de `{0, …, 100m − 1}`, los que cumplen `2^(100m) ≤ 3^c·3^|A|` son
    a lo sumo `2^c·2^(96m)`: cada uno tiene al menos `63m − c` elementos, pesa al menos
    `2^(63m)/2^c`, y el peso total es `3^(100m)`. Con `c = 0` es `pocos_patrones`. -/
theorem pocos_patrones_nivel (m c : ℕ) :
    ((Finset.range (100 * m)).powerset.filter fun A => 2 ^ (100 * m) ≤ 3 ^ c * 3 ^ A.card).card
      ≤ 2 ^ c * 2 ^ (96 * m) := by
  set B := (Finset.range (100 * m)).powerset.filter fun A => 2 ^ (100 * m) ≤ 3 ^ c * 3 ^ A.card
  have hgrande : ∀ A ∈ B, 63 * m ≤ c + A.card := by
    intro A hA
    have h := (Finset.mem_filter.1 hA).2
    rw [← pow_add] at h
    have := sesenta_y_tres h
    omega
  have hsuma : ∑ A ∈ (Finset.range (100 * m)).powerset, 2 ^ A.card = 3 ^ (100 * m) := by
    have := Finset.sum_pow_mul_eq_add_pow (2 : ℕ) 1 (Finset.range (100 * m))
    simpa using this
  have h1 : B.card * 2 ^ (63 * m) ≤ 2 ^ c * 3 ^ (100 * m) := by
    calc B.card * 2 ^ (63 * m) = ∑ A ∈ B, 2 ^ (63 * m) := by rw [Finset.sum_const, smul_eq_mul]
      _ ≤ ∑ A ∈ B, 2 ^ c * 2 ^ A.card :=
          Finset.sum_le_sum fun A hA => by
            rw [← pow_add]
            exact Nat.pow_le_pow_right (by norm_num) (hgrande A hA)
      _ = 2 ^ c * ∑ A ∈ B, 2 ^ A.card := by rw [Finset.mul_sum]
      _ ≤ 2 ^ c * ∑ A ∈ (Finset.range (100 * m)).powerset, 2 ^ A.card :=
          Nat.mul_le_mul_left _ (Finset.sum_le_sum_of_subset (Finset.filter_subset _ _))
      _ = 2 ^ c * 3 ^ (100 * m) := by rw [hsuma]
  have h2 : 3 ^ (100 * m) ≤ 2 ^ (96 * m) * 2 ^ (63 * m) := by
    rw [← pow_add, show 96 * m + 63 * m = 159 * m by ring, pow_mul, pow_mul]
    exact Nat.pow_le_pow_left (by norm_num) m
  have h3 : B.card * 2 ^ (63 * m) ≤ 2 ^ c * 2 ^ (96 * m) * 2 ^ (63 * m) :=
    calc B.card * 2 ^ (63 * m) ≤ 2 ^ c * 3 ^ (100 * m) := h1
      _ ≤ 2 ^ c * (2 ^ (96 * m) * 2 ^ (63 * m)) := Nat.mul_le_mul_left _ h2
      _ = 2 ^ c * 2 ^ (96 * m) * 2 ^ (63 * m) := by ring
  exact Nat.le_of_mul_le_mul_right h3 (by positivity)

open Classical in
/-- **Los casi fugitivos son raros.** Entre 0 y N−1 hay a lo sumo
    `(N / 2^(100m) + 1)·2^c·2^(96m)` casi fugitivos de nivel `3^c`, para cada `m`. -/
theorem cuenta_casi_fugas (N m c : ℕ) :
    ((Finset.range N).filter (CasiFuga c)).card ≤
      (N / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m)) := by
  have hsub : (Finset.range N).filter (CasiFuga c) ⊆
      (Finset.range N).filter fun v => 2 ^ (100 * m) ≤ 3 ^ c * 3 ^ S (100 * m) v := by
    intro v hv
    rw [Finset.mem_filter] at hv ⊢
    exact ⟨hv.1, hv.2 _⟩
  exact (Finset.card_le_card hsub).trans
    ((cuenta_por_bloques N (100 * m) fun s => 2 ^ (100 * m) ≤ 3 ^ c * 3 ^ s).trans
      (Nat.mul_le_mul_left _ (pocos_patrones_nivel m c)))

/-! ## Los momentos bajos del fugitivo -/

/-- **En un momento bajo, el fugitivo es chico**: si en el paso `j` su pronóstico es a lo
    sumo `3^c`, entonces `T^j(n) ≤ 3^c·(n + j)`. -/
theorem chico_si_bajo {n j c : ℕ} (h : FugaPura n) (hj : 3 ^ S j n ≤ 3 ^ c * 2 ^ j) :
    T^[j] n ≤ 3 ^ c * (n + j) := by
  have ht := tamano_antes_del_cruce j (fun i _ => nunca_cruza h i)
  have hS := S_le_pasos j n
  have h2 : 2 ^ j * (3 * T^[j] n) ≤ 2 ^ j * (3 * (3 ^ c * (n + j))) :=
    calc 2 ^ j * (3 * T^[j] n) = 3 * (2 ^ j * T^[j] n) := by ring
      _ ≤ 3 ^ S j n * (3 * n + S j n) := ht
      _ ≤ 3 ^ c * 2 ^ j * (3 * n + 3 * j) := Nat.mul_le_mul hj (by omega)
      _ = 2 ^ j * (3 * (3 ^ c * (n + j))) := by ring
  exact Nat.le_of_mul_le_mul_left (Nat.le_of_mul_le_mul_left h2 (by positivity)) (by norm_num)

open Classical in
/-- **Rasgo 8: el fugitivo casi nunca está bajo.** Entre los primeros `k` pasos, los momentos
    en que su pronóstico es a lo sumo `3^c` son a lo sumo
    `(3^c·(n+k) / 2^(100m) + 1)·2^c·2^(96m)`, para cada `m`: cada momento bajo deja un casi
    fugitivo menor que `3^c·(n+k)`, y son todos distintos porque la órbita nunca repite un
    valor. -/
theorem tiempos_bajos {n : ℕ} (h : FugaPura n) (c k m : ℕ) :
    ((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card ≤
      (3 ^ c * (n + k) / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m)) := by
  refine le_trans ?_ (cuenta_casi_fugas (3 ^ c * (n + k)) m c)
  refine Finset.card_le_card_of_injOn (fun j => T^[j] n) ?_ ?_
  · intro j hj
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hj ⊢
    refine ⟨lt_of_le_of_lt (chico_si_bajo h hj.2) ?_, casi_fuga_de_bajo h hj.2⟩
    exact Nat.mul_lt_mul_of_pos_left (by omega) (by positivity)
  · intro i _ j _ hij
    exact rasgo_inyectiva h hij

/-- La cuenta de `tiempos_bajos`, sin divisiones. -/
theorem tiempos_bajos_mul {n : ℕ} (h : FugaPura n) (c k m : ℕ) :
    ((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card * 16 ^ m ≤
      6 ^ c * (n + k) + 2 ^ c * 2 ^ (100 * m) := by
  have h1 := tiempos_bajos h c k m
  generalize ((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card = q at h1 ⊢
  have hL : (2 : ℕ) ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h2 : (3 ^ c * (n + k) / 2 ^ (100 * m) + 1) * 2 ^ (100 * m) ≤
      3 ^ c * (n + k) + 2 ^ (100 * m) := by
    rw [Nat.add_mul, one_mul]
    exact Nat.add_le_add_right (Nat.div_mul_le_self _ _) _
  have h3 : q * 16 ^ m * 2 ^ (96 * m) ≤ (3 ^ c * (n + k) + 2 ^ (100 * m)) * 2 ^ c * 2 ^ (96 * m) :=
    calc q * 16 ^ m * 2 ^ (96 * m) = q * 2 ^ (100 * m) := by rw [hL]; ring
      _ ≤ (3 ^ c * (n + k) / 2 ^ (100 * m) + 1) * (2 ^ c * 2 ^ (96 * m)) * 2 ^ (100 * m) :=
          Nat.mul_le_mul_right _ h1
      _ = (3 ^ c * (n + k) / 2 ^ (100 * m) + 1) * 2 ^ (100 * m) * (2 ^ c * 2 ^ (96 * m)) := by
          ring
      _ ≤ (3 ^ c * (n + k) + 2 ^ (100 * m)) * (2 ^ c * 2 ^ (96 * m)) := Nat.mul_le_mul_right _ h2
      _ = (3 ^ c * (n + k) + 2 ^ (100 * m)) * 2 ^ c * 2 ^ (96 * m) := by ring
  calc q * 16 ^ m ≤ (3 ^ c * (n + k) + 2 ^ (100 * m)) * 2 ^ c :=
        Nat.le_of_mul_le_mul_right h3 (by positivity)
    _ = 6 ^ c * (n + k) + 2 ^ c * 2 ^ (100 * m) := by
        rw [show (6 : ℕ) = 3 * 2 by norm_num, mul_pow]
        ring


/-- **Rasgo 8, densidad cero.** Para cada nivel `3^c`, los momentos en que el pronóstico del
    fugitivo es a lo sumo `3^c` tienen densidad cero: desde cierto `K`, entre los primeros `k`
    pasos hay a lo sumo `ε·k`. -/
theorem tiempos_bajos_raros {n : ℕ} (h : FugaPura n) (c : ℕ) {ε : ℝ} (hε : 0 < ε) :
    ∃ K : ℕ, ∀ k, K ≤ k →
      (((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) ≤ ε * k := by
  obtain ⟨m, hm⟩ := pow_unbounded_of_one_lt (2 * 6 ^ c / ε) (by norm_num : (1 : ℝ) < 16)
  have h16 : (0 : ℝ) < 16 ^ m := by positivity
  have hm' : 2 * 6 ^ c ≤ 16 ^ m * ε := ((div_lt_iff₀ hε).1 hm).le
  refine ⟨⌈2 * (6 ^ c * n + 2 ^ c * 2 ^ (100 * m)) / (ε * 16 ^ m)⌉₊, fun k hk => ?_⟩
  have h1 : (((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) * 16 ^ m ≤
      6 ^ c * (n + k) + 2 ^ c * 2 ^ (100 * m) := by
    exact_mod_cast tiempos_bajos_mul h c k m
  generalize (((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) = q at h1 ⊢
  have h2 : (2 * 6 ^ c : ℝ) * k ≤ 16 ^ m * ε * k :=
    mul_le_mul_of_nonneg_right hm' (Nat.cast_nonneg k)
  have h3 : 2 * (6 ^ c * n + 2 ^ c * 2 ^ (100 * m)) ≤ (k : ℝ) * (ε * 16 ^ m) := by
    have h4 : 2 * (6 ^ c * n + 2 ^ c * 2 ^ (100 * m)) / (ε * 16 ^ m) ≤ (k : ℝ) :=
      (Nat.le_ceil _).trans (by exact_mod_cast hk)
    rwa [div_le_iff₀ (by positivity)] at h4
  refine le_of_mul_le_mul_right ?_ h16
  nlinarith


end PerdicesEstela

#print axioms PerdicesEstela.S_le_pasos
#print axioms PerdicesEstela.tamano_antes_del_cruce
#print axioms PerdicesEstela.casiFuga_cero
#print axioms PerdicesEstela.casi_fuga_de_bajo
#print axioms PerdicesEstela.pocos_patrones_nivel
#print axioms PerdicesEstela.cuenta_casi_fugas
#print axioms PerdicesEstela.chico_si_bajo
#print axioms PerdicesEstela.tiempos_bajos
#print axioms PerdicesEstela.tiempos_bajos_mul
#print axioms PerdicesEstela.tiempos_bajos_raros
