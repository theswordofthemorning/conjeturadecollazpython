import CasaTablero

/-! # El planeador: paso 3 de la ruta B, segunda ronda

07-10-2026. Explicación en `LEEME.md` de esta carpeta, sección «Paso 3, segunda ronda: el
planeador».

El tablero (`CasaTablero`) separó dos especies de fugitivo: el **cohete**, cuyo pronóstico
crece sin límite, y el **planeador**, cuyo pronóstico vuelve una y otra vez por debajo de un
mismo nivel. Este archivo estudia al planeador y encuentra el primer choque del tablero,
para una subespecie:

* `casi_fuga_de_bajo`: en un momento en que el pronóstico del fugitivo es a lo sumo `3^c`,
  el número al que llegó es **casi fugitivo** de nivel `3^c`: su propio pronóstico nunca
  baja de `1/3^c`;
* `cuenta_casi_fugas`: los casi fugitivos son raros, como los fugitivos (Terras), con un
  factor `2^c` más;
* `chico_si_bajo`: en un momento bajo, el fugitivo es chico: `T^j(n) ≤ 3^c·(n + j)`;
* `tiempos_bajos`: **rasgo 8**: entre los primeros `k` pasos hay pocos momentos bajos,
  porque cada uno deja un casi fugitivo chico y la órbita nunca repite un valor;
* `sin_planeador_fuerte`: **el primer choque**: el pronóstico de un fugitivo no puede quedar
  acotado para siempre; `pronostico_sin_techo`: pasa cualquier nivel, tan tarde como se
  quiera;
* `tiempos_bajos_potencia`: en cifras: en los primeros `2^(100m)` pasos, el pronóstico pasa
  de `3^m` salvo en una fracción `3·(3/8)^m` de los momentos; `techo_crece`: desde `m = 2`,
  en esos pasos el pronóstico pasa de `3^m`, una potencia del tiempo;
* `tiempos_bajos_raros`: para cada nivel, los momentos bajos tienen densidad cero;
* `cohete_o_planeador_intermitente`: las dos especies que quedan;
* `fuga_inyectiva`, `tamano_en_franja` y `estela`: la estela no necesita un fugitivo puro,
  basta una órbita que crezca sin límite;
* `ninguna_orbita_en_franja`: para todo número y todo nivel `3^c`, el pronóstico sale alguna
  vez de la franja entre `1/3^c` y `3^c`: por abajo si la órbita cae en un circuito
  (`acotada_baja`), y por arriba o por abajo si crece sin límite (`fuga_sale_de_franja`);
* `atras_acotado`: hacia atrás, un número que llega a `v` sin que su pronóstico baje de
  `1/3^c` es a lo sumo `3^c·v`; el árbol de un fugitivo aporta pocos casi fugitivos de cada
  nivel;
* `fantasma_planeador`: la prueba de fuego del fantasma, en Lean: para cada `L` hay un número
  menor que `2^L` cuyos primeros `L` pasos son los de un planeador fuerte (pronóstico siempre
  entre 1 y 3), así que el choque necesita todos los pasos y el tamaño del número.

El choque usa a la vez que el fugitivo es un número común (su órbita no repite valores y su
tamaño va pegado al pronóstico) y algo propio del 3 (la cuenta de patrones, con
`3^63 < 2^100` y `3^100 ≤ 2^159`, que en la casa de 5n+1 no tiene equivalente). El planeador
que sobrevive es **intermitente**: vuelve por debajo de un nivel una y otra vez, pero cada vez
más de tarde en tarde, y entre medio su pronóstico pasa cualquier techo.

Sin hipótesis externas. Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaPlaneador

open Ocelotas OcelotasContador CasaPlano CasaRetrato CasaTablero

/-! ## Casi fugitivos -/

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
  have ht := (rasgo_tamano h j).2
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

/-! ## El primer choque -/

/-- **El primer choque: no hay planeador fuerte.** El pronóstico de un fugitivo no puede
    quedar acotado para siempre: para cada nivel `3^c` hay un paso en que lo pasa. Si no lo
    pasara nunca, los `k` primeros valores de su órbita serían `k` casi fugitivos distintos
    menores que `3^c·(n+k)`, y para `k` grande no hay tantos. -/
theorem sin_planeador_fuerte {n : ℕ} (h : FugaPura n) (c : ℕ) :
    ∃ j, 3 ^ c * 2 ^ j < 3 ^ S j n := by
  by_contra hc
  push Not at hc
  have h1 := tiempos_bajos_mul h c (n + 2 ^ c * 2 ^ (100 * (c + 1)) + 1) (c + 1)
  rw [Finset.filter_true_of_mem fun j _ => hc j, Finset.card_range] at h1
  generalize 2 ^ c * 2 ^ (100 * (c + 1)) = b at h1
  have h6 : 16 * 6 ^ c ≤ 16 ^ (c + 1) := by
    rw [pow_succ]
    have : 6 ^ c ≤ 16 ^ c := Nat.pow_le_pow_left (by norm_num) c
    omega
  have hpos : 1 ≤ 6 ^ c := Nat.one_le_pow _ _ (by norm_num)
  generalize 6 ^ c = a at h1 h6 hpos
  generalize 16 ^ (c + 1) = s at h1 h6
  have h7 := Nat.mul_le_mul_left (n + b + 1) h6
  nlinarith

/-- **El pronóstico del fugitivo no tiene techo**: pasa cualquier nivel `3^c`, tan tarde como
    se quiera. -/
theorem pronostico_sin_techo {n : ℕ} (h : FugaPura n) (c K : ℕ) :
    ∃ j, K ≤ j ∧ 3 ^ c * 2 ^ j < 3 ^ S j n := by
  by_contra hc
  push Not at hc
  obtain ⟨j, hj⟩ := sin_planeador_fuerte h (c + K)
  rcases le_or_gt K j with hKj | hjK
  · have h1 := hc j hKj
    have h2 : 3 ^ c * 2 ^ j ≤ 3 ^ (c + K) * 2 ^ j :=
      Nat.mul_le_mul_right _ (Nat.pow_le_pow_right (by norm_num) (by omega))
    omega
  · have h1 : 3 ^ S j n ≤ 3 ^ (c + K) * 2 ^ j :=
      calc 3 ^ S j n ≤ 3 ^ (c + K) :=
            Nat.pow_le_pow_right (by norm_num) (by have := S_le_pasos j n; omega)
        _ ≤ 3 ^ (c + K) * 2 ^ j := Nat.le_mul_of_pos_right _ (by positivity)
    omega

/-- **Rasgo 8, en cifras.** Si `n ≤ 2^(100m)`, en los primeros `2^(100m)` pasos el
    pronóstico del fugitivo pasa de `3^m` salvo en a lo sumo `3·6^m·2^(96m)` momentos: una
    fracción `3·(3/8)^m` de ellos. -/
theorem tiempos_bajos_potencia {n : ℕ} (h : FugaPura n) (m : ℕ) (hn : n ≤ 2 ^ (100 * m)) :
    ((Finset.range (2 ^ (100 * m))).filter fun j => 3 ^ S j n ≤ 3 ^ m * 2 ^ j).card ≤
      3 * 6 ^ m * 2 ^ (96 * m) := by
  have h1 := tiempos_bajos_mul h m (2 ^ (100 * m)) m
  generalize ((Finset.range (2 ^ (100 * m))).filter fun j => 3 ^ S j n ≤ 3 ^ m * 2 ^ j).card = q
    at h1 ⊢
  have hL : (2 : ℕ) ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h2 : 2 ^ m ≤ 6 ^ m := Nat.pow_le_pow_left (by norm_num) m
  have h3 : q * 16 ^ m ≤ 3 * 6 ^ m * 2 ^ (96 * m) * 16 ^ m :=
    calc q * 16 ^ m ≤ 6 ^ m * (n + 2 ^ (100 * m)) + 2 ^ m * 2 ^ (100 * m) := h1
      _ ≤ 6 ^ m * (2 ^ (100 * m) + 2 ^ (100 * m)) + 6 ^ m * 2 ^ (100 * m) :=
          Nat.add_le_add (Nat.mul_le_mul_left _ (by omega)) (Nat.mul_le_mul_right _ h2)
      _ = 3 * 6 ^ m * 2 ^ (100 * m) := by ring
      _ = 3 * 6 ^ m * 2 ^ (96 * m) * 16 ^ m := by rw [hL]; ring
  exact Nat.le_of_mul_le_mul_right h3 (by positivity)

/-- **El techo crece como una potencia del tiempo.** Si el fugitivo es menor que `2^(100m)`,
    con `m ≥ 2`, en sus primeros `2^(100m)` pasos el pronóstico pasa de `3^m`: con
    `k = 2^(100m)`, pasa de `k^0,0158`. -/
theorem techo_crece {n m : ℕ} (h : FugaPura n) (hm : 2 ≤ m) (hn : n ≤ 2 ^ (100 * m)) :
    ∃ j, j < 2 ^ (100 * m) ∧ 3 ^ m * 2 ^ j < 3 ^ S j n := by
  by_contra hc
  push Not at hc
  have h1 := tiempos_bajos_potencia h m hn
  rw [Finset.filter_true_of_mem fun j hj => hc j (Finset.mem_range.1 hj), Finset.card_range] at h1
  have hL : (2 : ℕ) ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  rw [hL] at h1
  have h2 := Nat.le_of_mul_le_mul_right h1 (by positivity)
  obtain ⟨t, rfl⟩ : ∃ t, m = t + 2 := ⟨m - 2, by omega⟩
  have h6 : 6 ^ t ≤ 16 ^ t := Nat.pow_le_pow_left (by norm_num) t
  have h16 : 1 ≤ 16 ^ t := Nat.one_le_pow _ _ (by norm_num)
  rw [pow_add, pow_add] at h2
  norm_num at h2
  omega

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

/-- **Las dos especies que quedan.** Todo fugitivo es un cohete (su pronóstico termina
    pasando cualquier nivel y ya no vuelve a bajar de él) o un planeador intermitente (vuelve
    una y otra vez por debajo de un mismo nivel, pero esas vueltas tienen densidad cero y
    entre medio su pronóstico pasa cualquier techo). El planeador fuerte, siempre bajo, no
    existe (`sin_planeador_fuerte`). -/
theorem cohete_o_planeador_intermitente {n : ℕ} (h : FugaPura n) :
    (∀ c, ∃ K, ∀ k, K ≤ k → 3 ^ c * 2 ^ k < 3 ^ S k n) ∨
      ∃ c, (∀ K, ∃ k, K ≤ k ∧ 3 ^ S k n ≤ 3 ^ c * 2 ^ k) ∧
        (∀ d K, ∃ k, K ≤ k ∧ 3 ^ d * 2 ^ k < 3 ^ S k n) ∧
        ∀ ε : ℝ, 0 < ε → ∃ K : ℕ, ∀ k, K ≤ k →
          (((Finset.range k).filter fun j => 3 ^ S j n ≤ 3 ^ c * 2 ^ j).card : ℝ) ≤ ε * k := by
  by_cases hp : ∃ c, ∀ K, ∃ k, K ≤ k ∧ 3 ^ S k n ≤ 3 ^ c * 2 ^ k
  · right
    obtain ⟨c, hc⟩ := hp
    exact ⟨c, hc, pronostico_sin_techo h, fun ε hε => tiempos_bajos_raros h c hε⟩
  · left
    push Not at hp
    exact hp

/-! ## Ninguna órbita vuela en franja -/

/-- La órbita de una fuga nunca repite un valor: si lo repitiera, daría vueltas para siempre
    entre sus primeros valores y quedaría acotada. -/
theorem fuga_no_repite {n i j : ℕ} (hf : Fuga n) (hij : i < j) : T^[i] n ≠ T^[j] n := by
  intro heq
  have hacot : ∀ k, T^[k] n ≤ ∑ t ∈ Finset.range j, T^[t] n := by
    intro k
    induction k using Nat.strong_induction_on with
    | _ k ih =>
      rcases lt_or_ge k j with hk | hk
      · exact Finset.single_le_sum (f := fun t => T^[t] n) (fun t _ => Nat.zero_le _)
          (Finset.mem_range.2 hk)
      · obtain ⟨d, rfl⟩ : ∃ d, k = d + j := ⟨k - j, by omega⟩
        have e : T^[d + j] n = T^[d + i] n := by
          rw [Function.iterate_add_apply, Function.iterate_add_apply, heq]
        rw [e]
        exact ih (d + i) (by omega)
  obtain ⟨k, hk⟩ := hf (∑ t ∈ Finset.range j, T^[t] n)
  exact absurd (hacot k) (not_le.mpr hk)

theorem fuga_inyectiva {n : ℕ} (hf : Fuga n) : Function.Injective (fun k => T^[k] n) := by
  intro i j heq
  by_contra hij
  rcases lt_or_gt_of_ne hij with hlt | hlt
  · exact fuga_no_repite hf hlt heq
  · exact fuga_no_repite hf hlt heq.symm

/-- **El tamaño en una franja.** Si antes de cada paso el pronóstico es al menos `1/3^c`,
    entonces `3·2^k·T^k(n) ≤ 3^S·(3n + 3^c·S)`. Con `c = 0` es `tamano_antes_del_cruce`. -/
theorem tamano_en_franja {n c : ℕ} :
    ∀ k, (∀ i, i < k → 2 ^ i ≤ 3 ^ c * 3 ^ S i n) →
      3 * (2 ^ k * T^[k] n) ≤ 3 ^ S k n * (3 * n + 3 ^ c * S k n) := by
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
        _ ≤ 3 * (3 ^ S k n * (3 * n + 3 ^ c * S k n)) + 3 * (3 ^ c * 3 ^ S k n) :=
            Nat.add_le_add (Nat.mul_le_mul_left 3 ih') (Nat.mul_le_mul_left 3 hk)
        _ = 3 ^ (S k n + 1) * (3 * n + 3 ^ c * (S k n + 1)) := by ring

open Classical in
/-- **La estela.** Si los `k` primeros valores de una órbita son distintos, menores que `X`
    y casi fugitivos de nivel `3^d`, entonces `k·16^m ≤ (X + 2^(100m))·2^d`, para cada `m`. -/
theorem estela {n k d X m : ℕ} (hiny : Set.InjOn (fun j => T^[j] n) (Finset.range k : Set ℕ))
    (hX : ∀ j, j < k → T^[j] n < X) (hcasi : ∀ j, j < k → CasiFuga d (T^[j] n)) :
    k * 16 ^ m ≤ (X + 2 ^ (100 * m)) * 2 ^ d := by
  have h1 : k ≤ (X / 2 ^ (100 * m) + 1) * (2 ^ d * 2 ^ (96 * m)) := by
    rw [← Finset.card_range k]
    refine le_trans (Finset.card_le_card_of_injOn (fun j => T^[j] n) ?_ hiny)
      (cuenta_casi_fugas X m d)
    intro j hj
    simp only [Finset.mem_coe, Finset.mem_range, Finset.mem_filter] at hj ⊢
    exact ⟨hX j hj, hcasi j hj⟩
  have hL : (2 : ℕ) ^ (100 * m) = 16 ^ m * 2 ^ (96 * m) := by
    rw [show 100 * m = 4 * m + 96 * m by ring, pow_add, pow_mul]
    norm_num
  have h2 : (X / 2 ^ (100 * m) + 1) * 2 ^ (100 * m) ≤ X + 2 ^ (100 * m) := by
    rw [Nat.add_mul, one_mul]
    exact Nat.add_le_add_right (Nat.div_mul_le_self _ _) _
  have h3 : k * 16 ^ m * 2 ^ (96 * m) ≤ (X + 2 ^ (100 * m)) * 2 ^ d * 2 ^ (96 * m) :=
    calc k * 16 ^ m * 2 ^ (96 * m) = k * 2 ^ (100 * m) := by rw [hL]; ring
      _ ≤ (X / 2 ^ (100 * m) + 1) * (2 ^ d * 2 ^ (96 * m)) * 2 ^ (100 * m) :=
          Nat.mul_le_mul_right _ h1
      _ = (X / 2 ^ (100 * m) + 1) * 2 ^ (100 * m) * (2 ^ d * 2 ^ (96 * m)) := by ring
      _ ≤ (X + 2 ^ (100 * m)) * (2 ^ d * 2 ^ (96 * m)) := Nat.mul_le_mul_right _ h2
      _ = (X + 2 ^ (100 * m)) * 2 ^ d * 2 ^ (96 * m) := by ring
  exact Nat.le_of_mul_le_mul_right h3 (by positivity)

/-- **Una fuga no vuela en franja.** Si la órbita de `n` crece sin límite, su pronóstico sale
    de cualquier franja `[1/3^c, 3^c]`: o la pasa por arriba o por abajo. Si quedara siempre
    dentro, los `k` primeros valores serían `k` casi fugitivos distintos de nivel `3^(2c)`,
    menores que `9^c·(n + k)`, y para `k` grande no hay tantos. -/
theorem fuga_sale_de_franja {n : ℕ} (hf : Fuga n) (c : ℕ) :
    ∃ k, 3 ^ c * 2 ^ k < 3 ^ S k n ∨ 3 ^ c * 3 ^ S k n < 2 ^ k := by
  by_contra hc
  push Not at hc
  have hchico : ∀ k, T^[k] n ≤ 9 ^ c * (n + k) := by
    intro k
    have ht := tamano_en_franja k fun i _ => (hc i).2
    have hS := S_le_pasos k n
    have h9 : (9 : ℕ) ^ c = 3 ^ c * 3 ^ c := by rw [← mul_pow]; norm_num
    have h1 : 1 ≤ 3 ^ c := Nat.one_le_pow _ _ (by norm_num)
    have h2 : 2 ^ k * (3 * T^[k] n) ≤ 2 ^ k * (3 * (9 ^ c * (n + k))) :=
      calc 2 ^ k * (3 * T^[k] n) = 3 * (2 ^ k * T^[k] n) := by ring
        _ ≤ 3 ^ S k n * (3 * n + 3 ^ c * S k n) := ht
        _ ≤ 3 ^ c * 2 ^ k * (3 * n * 3 ^ c + 3 ^ c * k) :=
            Nat.mul_le_mul (hc k).1 (Nat.add_le_add (Nat.le_mul_of_pos_right _ (by positivity))
              (Nat.mul_le_mul_left _ hS))
        _ ≤ 2 ^ k * (3 * (9 ^ c * (n + k))) := by
            rw [h9]
            have : 3 ^ c * k ≤ 3 * (3 ^ c * k) := by omega
            nlinarith [Nat.zero_le (3 ^ c * 2 ^ k)]
    exact Nat.le_of_mul_le_mul_left (Nat.le_of_mul_le_mul_left h2 (by positivity)) (by norm_num)
  have hcasi : ∀ j, CasiFuga (2 * c) (T^[j] n) := by
    intro j i
    have h1 := (hc (j + i)).2
    rw [S_add, pow_add, pow_add] at h1
    have h2 : 2 ^ j * 2 ^ i ≤ 2 ^ j * (3 ^ (2 * c) * 3 ^ S i (T^[j] n)) :=
      calc 2 ^ j * 2 ^ i ≤ 3 ^ c * (3 ^ S j n * 3 ^ S i (T^[j] n)) := h1
        _ ≤ 3 ^ c * (3 ^ c * 2 ^ j * 3 ^ S i (T^[j] n)) :=
            Nat.mul_le_mul_left _ (Nat.mul_le_mul_right _ (hc j).1)
        _ = 2 ^ j * (3 ^ (2 * c) * 3 ^ S i (T^[j] n)) := by ring
    exact Nat.le_of_mul_le_mul_left h2 (by positivity)
  set B := 4 ^ c * 2 ^ (100 * (2 * c + 2)) with hB
  have h1 := estela (n := n) (k := n + B + 1) (d := 2 * c) (X := 9 ^ c * (n + (n + B + 1)))
    (m := 2 * c + 2) (fuga_inyectiva hf).injOn
    (fun j hj => lt_of_le_of_lt (hchico j) (Nat.mul_lt_mul_of_pos_left (by omega) (by positivity)))
    (fun j _ => hcasi j)
  have h36 : (9 : ℕ) ^ c * 2 ^ (2 * c) = 36 ^ c := by
    rw [pow_mul, show (2 : ℕ) ^ 2 = 4 by norm_num, ← mul_pow]
    norm_num
  have h4 : (2 : ℕ) ^ (2 * c) = 4 ^ c := by
    rw [pow_mul]
    norm_num
  have h16 : 16 * 36 ^ c ≤ 16 ^ (2 * c + 2) := by
    have e : (16 : ℕ) ^ (2 * c + 2) = 256 ^ c * 256 := by
      rw [pow_add, pow_mul]
      norm_num
    have : 36 ^ c ≤ 256 ^ c := Nat.pow_le_pow_left (by norm_num) c
    rw [e]
    omega
  -- h1 : k·16^m ≤ (9^c (n + k) + 2^(100m))·2^(2c)
  have h5 : (n + B + 1) * 16 ^ (2 * c + 2) ≤ 36 ^ c * (n + (n + B + 1)) + B := by
    calc (n + B + 1) * 16 ^ (2 * c + 2) ≤ (9 ^ c * (n + (n + B + 1)) + 2 ^ (100 * (2 * c + 2))) *
          2 ^ (2 * c) := h1
      _ = 9 ^ c * 2 ^ (2 * c) * (n + (n + B + 1)) + 2 ^ (2 * c) * 2 ^ (100 * (2 * c + 2)) := by
          ring
      _ = 36 ^ c * (n + (n + B + 1)) + B := by rw [h36, h4, hB]
  have hpos : 1 ≤ 36 ^ c := Nat.one_le_pow _ _ (by norm_num)
  generalize 36 ^ c = a at h5 h16 hpos
  generalize 16 ^ (2 * c + 2) = s at h5 h16
  have h7 := Nat.mul_le_mul_left (n + B + 1) h16
  nlinarith

/-- Una órbita acotada cae en un circuito, y allí el pronóstico tiende a cero: termina por
    debajo de `1/3^c`, para cada `c`. -/
theorem acotada_baja {n : ℕ} (hf : ¬ Fuga n) (c : ℕ) : ∃ k, 3 ^ c * 3 ^ S k n < 2 ^ k := by
  classical
  simp only [Fuga, not_forall, not_exists, not_lt] at hf
  obtain ⟨M, hM⟩ := hf
  have hmaps : Set.MapsTo (fun k => T^[k] n) (↑(Finset.range (M + 2)) : Set ℕ)
      (↑(Finset.range (M + 1)) : Set ℕ) := by
    intro k _
    simp only [Finset.mem_coe, Finset.mem_range]
    exact Nat.lt_succ_of_le (hM k)
  obtain ⟨i, -, j, -, hij, heq⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to (by simp) hmaps
  -- un circuito: T^[p] m = m con p ≥ 1
  have hciclo : ∃ i p, 1 ≤ p ∧ T^[p] (T^[i] n) = T^[i] n := by
    rcases lt_or_gt_of_ne hij with hlt | hlt
    · refine ⟨i, j - i, by omega, ?_⟩
      rw [← Function.iterate_add_apply, Nat.sub_add_cancel hlt.le]
      exact heq.symm
    · refine ⟨j, i - j, by omega, ?_⟩
      rw [← Function.iterate_add_apply, Nat.sub_add_cancel hlt.le]
      exact heq
  obtain ⟨i, p, hp, hmp⟩ := hciclo
  have hbaja : 3 ^ S p (T^[i] n) < 2 ^ p := by
    rcases Nat.eq_zero_or_pos (T^[i] n) with h0 | h0
    · have hS0 : ∀ q, S q 0 = 0 := by
        intro q
        induction q with
        | zero => rfl
        | succ q ih =>
          simp only [S]
          have : T 0 = 0 := by decide
          rw [this, ih]
      rw [h0, hS0]
      exact Nat.one_lt_two_pow (by omega)
    · exact ciclo_cruza h0 hp hmp
  have hv : 1 ≤ 3 ^ S p (T^[i] n) := Nat.one_le_pow _ _ (by norm_num)
  obtain ⟨-, hS⟩ := vueltas (n := n) (i := i) rfl hmp
    (3 ^ c * 3 ^ S i n * 3 ^ S p (T^[i] n))
  refine ⟨i + p * (3 ^ c * 3 ^ S i n * 3 ^ S p (T^[i] n)), ?_⟩
  have h2 := crece_mas (c := 3 ^ c * 3 ^ S i n) (d := 2 ^ i) hbaja hv Nat.one_le_two_pow
  rw [hS, pow_add, pow_add, pow_mul (2 : ℕ) p, pow_mul (3 : ℕ) (S p (T^[i] n))]
  calc 3 ^ c * (3 ^ S i n * (3 ^ S p (T^[i] n)) ^ (3 ^ c * 3 ^ S i n * 3 ^ S p (T^[i] n)))
      = 3 ^ c * 3 ^ S i n * (3 ^ S p (T^[i] n)) ^ (3 ^ c * 3 ^ S i n * 3 ^ S p (T^[i] n)) := by
        ring
    _ < 2 ^ i * (2 ^ p) ^ (3 ^ c * 3 ^ S i n * 3 ^ S p (T^[i] n)) := h2

/-- **Ninguna órbita vuela en franja.** Para todo número y todo nivel `3^c`, el pronóstico
    sale alguna vez de la franja `[1/3^c, 3^c]`: si la órbita está acotada cae en un circuito
    y el pronóstico baja hacia cero (`acotada_baja`); si crece sin límite, la estela lo saca
    (`fuga_sale_de_franja`). -/
theorem ninguna_orbita_en_franja (n c : ℕ) :
    ∃ k, 3 ^ c * 2 ^ k < 3 ^ S k n ∨ 3 ^ c * 3 ^ S k n < 2 ^ k := by
  by_cases hf : Fuga n
  · exact fuga_sale_de_franja hf c
  · obtain ⟨k, hk⟩ := acotada_baja hf c
    exact ⟨k, Or.inr hk⟩

/-! ## Hacia atrás -/

/-- **Hacia atrás, a nivel fijo, el árbol es chico.** Si `u` llega a `v` en `r` pasos sin que
    su pronóstico de esos `r` pasos baje de `1/3^c`, entonces `u ≤ 3^c·v`. Por eso el árbol
    de un fugitivo aporta pocos casi fugitivos de cada nivel, y la pinza no cierra por ahí. -/
theorem atras_acotado {u v r c : ℕ} (hr : T^[r] u = v) (hc : 2 ^ r ≤ 3 ^ c * 3 ^ S r u) :
    u ≤ 3 ^ c * v := by
  have h1 := cota_inferior u r
  rw [hr] at h1
  have h2 : 3 ^ S r u * u ≤ 3 ^ S r u * (3 ^ c * v) :=
    calc 3 ^ S r u * u ≤ 2 ^ r * v := h1
      _ ≤ 3 ^ c * 3 ^ S r u * v := Nat.mul_le_mul_right _ hc
      _ = 3 ^ S r u * (3 ^ c * v) := by ring
  exact Nat.le_of_mul_le_mul_left h2 (by positivity)

/-! ## El fantasma que vuela bajo, en cada tramo finito -/

theorem existe_nivel (j : ℕ) : ∃ s, 2 ^ j ≤ 3 ^ s :=
  ⟨j, Nat.pow_le_pow_left (by norm_num) j⟩

open Classical in
/-- Subidas del fantasma que vuela bajo en sus primeros `j` pasos: el menor `s` con
    `2^j ≤ 3^s`. -/
noncomputable def subidasFantasma (j : ℕ) : ℕ := Nat.find (existe_nivel j)

theorem fantasma_arriba (j : ℕ) : 2 ^ j ≤ 3 ^ subidasFantasma j := by
  classical
  exact Nat.find_spec (existe_nivel j)

theorem fantasma_abajo (j : ℕ) : 3 ^ subidasFantasma j < 3 * 2 ^ j := by
  classical
  rcases Nat.eq_zero_or_pos (subidasFantasma j) with h0 | hpos
  · rw [h0]
    have : 1 ≤ 2 ^ j := Nat.one_le_two_pow
    simp only [pow_zero]
    omega
  · obtain ⟨s, hs⟩ : ∃ s, subidasFantasma j = s + 1 := ⟨subidasFantasma j - 1, by omega⟩
    have hmin : ¬ 2 ^ j ≤ 3 ^ s := Nat.find_min (existe_nivel j) (by
      unfold subidasFantasma at hs
      omega)
    rw [hs, pow_succ]
    omega

theorem fantasma_paso (j : ℕ) :
    subidasFantasma (j + 1) = subidasFantasma j ∨
      subidasFantasma (j + 1) = subidasFantasma j + 1 := by
  classical
  have h1 : subidasFantasma j ≤ subidasFantasma (j + 1) := by
    apply Nat.find_min'
    exact (Nat.pow_le_pow_right (by norm_num) (by omega)).trans (fantasma_arriba (j + 1))
  have h2 : subidasFantasma (j + 1) ≤ subidasFantasma j + 1 := by
    apply Nat.find_min'
    rw [pow_succ, pow_succ]
    have := fantasma_arriba j
    omega
  omega

theorem fantasma_cero : subidasFantasma 0 = 0 := by
  classical
  have h : subidasFantasma 0 ≤ 0 := Nat.find_min' (existe_nivel 0) (by norm_num)
  omega

/-- Cada patrón de largo `L` es el de un número menor que `2^L`. -/
theorem patron_realizable (L : ℕ) (A : Finset ℕ) (hA : A ⊆ Finset.range L) :
    ∃ x, x < 2 ^ L ∧ subidas L x = A := by
  have hsurj := Finset.surj_on_of_inj_on_of_card_le (s := Finset.range (2 ^ L))
    (t := (Finset.range L).powerset) (fun x _ => subidas L x)
    (fun x _ => Finset.mem_powerset.2 (subidas_sub L x))
    (fun x y hx hy hxy => by
      have h := congruentes_de_subidas hxy
      rw [Finset.mem_range] at hx hy
      rwa [Nat.mod_eq_of_lt hx, Nat.mod_eq_of_lt hy] at h)
    (by simp)
  obtain ⟨x, hx, hxA⟩ := hsurj A (Finset.mem_powerset.2 hA)
  exact ⟨x, Finset.mem_range.1 hx, hxA.symm⟩

theorem subidas_prefijo {j L : ℕ} (hjL : j ≤ L) (x : ℕ) :
    subidas j x = (subidas L x).filter (· < j) := by
  ext i
  simp only [subidas, Finset.mem_filter, Finset.mem_range]
  constructor
  · rintro ⟨hi, hp⟩
    exact ⟨⟨by omega, hp⟩, hi⟩
  · rintro ⟨⟨_, hp⟩, hi⟩
    exact ⟨hi, hp⟩

/-- El patrón del fantasma en sus primeros `L` pasos. -/
noncomputable def patronFantasma (L : ℕ) : Finset ℕ :=
  (Finset.range L).filter fun j => subidasFantasma (j + 1) = subidasFantasma j + 1

theorem cuenta_patron_fantasma {j L : ℕ} (hjL : j ≤ L) :
    ((patronFantasma L).filter (· < j)).card = subidasFantasma j := by
  induction j with
  | zero =>
    rw [fantasma_cero]
    simp
  | succ j ih =>
    have ih' := ih (by omega)
    have e : (patronFantasma L).filter (· < j + 1) =
        if j ∈ patronFantasma L then insert j ((patronFantasma L).filter (· < j))
        else (patronFantasma L).filter (· < j) := by
      ext i
      split_ifs with hj
      · simp only [Finset.mem_filter, Finset.mem_insert]
        constructor
        · rintro ⟨hi, hlt⟩
          rcases Nat.lt_succ_iff_lt_or_eq.1 hlt with h | h
          · exact Or.inr ⟨hi, h⟩
          · exact Or.inl h
        · rintro (h | ⟨hi, hlt⟩)
          · subst h
            exact ⟨hj, by omega⟩
          · exact ⟨hi, by omega⟩
      · simp only [Finset.mem_filter]
        constructor
        · rintro ⟨hi, hlt⟩
          refine ⟨hi, ?_⟩
          rcases Nat.lt_succ_iff_lt_or_eq.1 hlt with h | h
          · exact h
          · subst h
            exact absurd hi hj
        · rintro ⟨hi, hlt⟩
          exact ⟨hi, by omega⟩
    rw [e]
    have hmem : j ∈ patronFantasma L ↔ subidasFantasma (j + 1) = subidasFantasma j + 1 := by
      simp only [patronFantasma, Finset.mem_filter, Finset.mem_range]
      constructor
      · exact fun h => h.2
      · exact fun h => ⟨by omega, h⟩
    split_ifs with hj
    · rw [Finset.card_insert_of_notMem (by simp), ih', hmem.1 hj]
    · rw [ih']
      rcases fantasma_paso j with h | h
      · exact h.symm
      · exact absurd (hmem.2 h) hj

/-- **El fantasma que vuela bajo, en cada tramo finito.** Para cada `L` hay un número menor
    que `2^L` cuyos primeros `L` pasos son los de un planeador fuerte: su pronóstico queda
    siempre entre 1 y 3. Ningún argumento que mire sólo una cantidad fija de pasos puede
    descartar al planeador fuerte; la estela (`sin_planeador_fuerte`) usa todos los pasos y
    el tamaño del número. -/
theorem fantasma_planeador (L : ℕ) :
    ∃ x, x < 2 ^ L ∧ ∀ j, j ≤ L → 2 ^ j ≤ 3 ^ S j x ∧ 3 ^ S j x < 3 * 2 ^ j := by
  have hsub : patronFantasma L ⊆ Finset.range L := Finset.filter_subset _ _
  obtain ⟨x, hx, hpat⟩ := patron_realizable L (patronFantasma L) hsub
  refine ⟨x, hx, fun j hj => ?_⟩
  have hS : S j x = subidasFantasma j := by
    rw [← card_subidas, subidas_prefijo hj, hpat, cuenta_patron_fantasma hj]
  rw [hS]
  exact ⟨fantasma_arriba j, fantasma_abajo j⟩

end CasaPlaneador

#print axioms CasaPlaneador.casiFuga_cero
#print axioms CasaPlaneador.casi_fuga_de_bajo
#print axioms CasaPlaneador.pocos_patrones_nivel
#print axioms CasaPlaneador.cuenta_casi_fugas
#print axioms CasaPlaneador.chico_si_bajo
#print axioms CasaPlaneador.tiempos_bajos
#print axioms CasaPlaneador.tiempos_bajos_mul
#print axioms CasaPlaneador.sin_planeador_fuerte
#print axioms CasaPlaneador.pronostico_sin_techo
#print axioms CasaPlaneador.tiempos_bajos_potencia
#print axioms CasaPlaneador.techo_crece
#print axioms CasaPlaneador.tiempos_bajos_raros
#print axioms CasaPlaneador.cohete_o_planeador_intermitente
#print axioms CasaPlaneador.fuga_no_repite
#print axioms CasaPlaneador.fuga_inyectiva
#print axioms CasaPlaneador.tamano_en_franja
#print axioms CasaPlaneador.estela
#print axioms CasaPlaneador.fuga_sale_de_franja
#print axioms CasaPlaneador.acotada_baja
#print axioms CasaPlaneador.ninguna_orbita_en_franja
#print axioms CasaPlaneador.atras_acotado
#print axioms CasaPlaneador.fantasma_arriba
#print axioms CasaPlaneador.fantasma_abajo
#print axioms CasaPlaneador.fantasma_paso
#print axioms CasaPlaneador.patron_realizable
#print axioms CasaPlaneador.cuenta_patron_fantasma
#print axioms CasaPlaneador.fantasma_planeador
