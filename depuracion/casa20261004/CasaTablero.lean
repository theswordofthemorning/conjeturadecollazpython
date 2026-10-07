import CasaRetrato
import CasaOcelotas

/-! # El tablero del choque: paso 3 de la ruta B, primera ronda

06-10-2026. Explicación en `LEEME.md` de esta carpeta, sección «Paso 3: el tablero del
choque».

Un choque son dos rasgos del fugitivo (una fuga pura) que no pueden cumplirse a la vez.
Antes de buscarlo, cada rasgo pasa dos pruebas de fuego:

* la del **fantasma**: ¿lo cumple también un «número» con infinitas cifras binarias,
  como el −1 de los enteros con signo? Si lo cumple, ese rasgo solo no sirve para el
  choque, porque el fantasma existe (`fantasma_nunca_cruza`);
* la del **vecino**: ¿vale también en la casa de 5n+1? Allí el muro A se cae de verdad
  (`vecino_grieta`), así que un argumento que también valga allí está mal.

Este archivo trae:

* **rasgos nuevos del fugitivo**: `rasgo_minimos` (puntos sin retorno),
  `rasgo_tamano` (el tamaño va pegado al pronóstico), `rasgo_cohete_o_planeador`
  (o su pronóstico crece sin límite y su camino está lleno de fugitivos, o vuelve una
  y otra vez a tamaños que crecen apenas como el tiempo) y `rasgo_pocos` (a lo sumo
  2·2^(96m) fugitivos entre los primeros 2^(100m) números);
* **terminaciones de la casa**: `collatz_iff_sin_intrusos` (el plano clásico: Collatz
  equivale a que no haya circuitos ni fugas), `muroB_de_sin_fugas` (sin fugas, el
  muro B está en pie) y `tamano_antes_del_cruce`;
* **la retroalimentación**: `crias_con_muroA` (con el muro A, el fugitivo nunca anda
  solo) y `crias_con_ocelotas` (con el tramo de Ocelotas, bajo LMN, sus puntos sin
  retorno son fugitivos o necesitan al menos 25 picos para cruzar);
* **los testigos de la prueba de fuego**: `fantasma_nunca_cruza` y `vecino_grieta`.

No se encontró un choque. Ninguno de estos rasgos usa a la vez que el fugitivo es un
número común y la desigualdad propia del 3: ése es el puente que falta.

Sin hipótesis externas, salvo `LMN23` como argumento de `crias_con_ocelotas`.
Compilación: `comprobar_casa.py`, en esta carpeta. -/

namespace CasaTablero

open Ocelotas OcelotasContador OcelotasLMNFuente CasaPlano CasaRetrato CasaOcelotas

/-! ## Terminaciones de la casa -/

/-- **El plano clásico.** Collatz equivale a que no haya circuitos ni fugas. -/
theorem collatz_iff_sin_intrusos : Collatz ↔ (∀ x, ¬ Circuito x) ∧ ∀ n, ¬ Fuga n := by
  constructor
  · intro h
    obtain ⟨hA, hB⟩ := collatz_iff_muros.1 h
    exact casa_sin_fallas hA hB
  · rintro ⟨hc, hf⟩
    refine collatz_iff_atajo.2 fun n hn => ?_
    by_contra hl
    rcases dos_fallas hn hl with ⟨i, hi⟩ | hfuga
    · exact hc _ hi
    · exact hf n hfuga

/-- Si ninguna órbita crece sin límite, el muro B está en pie: una fuga pura sería una
    fuga (`rasgo_fuga`). Así se conectan los dos planos: el muro A excluye los circuitos
    (`muroA_sin_circuitos`) y la falta de fugas levanta el muro B. -/
theorem muroB_de_sin_fugas (h : ∀ n, ¬ Fuga n) : MuroB :=
  muroB_iff.2 fun n _ hf => h n (rasgo_fuga hf)

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

/-! ## Rasgos nuevos del fugitivo -/

/-- **Rasgo 5: puntos sin retorno.** En el camino de un fugitivo hay valores, tan lejos
    como se quiera, de los que nunca vuelve a bajar: después de ellos la órbita queda
    siempre más arriba. Usa que la órbita nunca repite un valor. -/
theorem rasgo_minimos {n : ℕ} (h : FugaPura n) (K : ℕ) :
    ∃ k, K ≤ k ∧ ∀ t, 1 ≤ t → T^[k] n < T^[t] (T^[k] n) := by
  classical
  have hex : ∃ v, ∃ j, K ≤ j ∧ T^[j] n = v := ⟨_, K, le_rfl, rfl⟩
  obtain ⟨k, hk, hkv⟩ := Nat.find_spec hex
  refine ⟨k, hk, fun t ht => ?_⟩
  have hmin : Nat.find hex ≤ T^[t + k] n := Nat.find_min' hex ⟨t + k, by omega, rfl⟩
  have hne : T^[k] n ≠ T^[t + k] n := rasgo_sin_repetir h (by omega)
  rw [← Function.iterate_add_apply]
  omega

/-- Un punto sin retorno es al menos 2 y nunca baja de sí mismo. -/
theorem rasgo_no_desciende {n : ℕ} (h : FugaPura n) (K : ℕ) :
    ∃ k, K ≤ k ∧ 2 ≤ T^[k] n ∧ ¬ Desciende (T^[k] n) := by
  obtain ⟨k, hk, hmin⟩ := rasgo_minimos h K
  refine ⟨k, hk, ?_, ?_⟩
  · have h1 := fuga_pura_no_baja h k
    have h2 := fuga_pura_dos h
    omega
  · rintro ⟨t, ht, hlt⟩
    have := hmin t ht
    omega

/-- **Rasgo 6: el tamaño del fugitivo va pegado a su pronóstico**, en todo momento:
    `n · 3^S/2^k ≤ T^k(n) ≤ (n + S/3) · 3^S/2^k`. -/
theorem rasgo_tamano {n : ℕ} (h : FugaPura n) (k : ℕ) :
    3 ^ S k n * n ≤ 2 ^ k * T^[k] n ∧
      3 * (2 ^ k * T^[k] n) ≤ 3 ^ S k n * (3 * n + S k n) :=
  ⟨cota_inferior n k, tamano_antes_del_cruce k fun i _ => nunca_cruza h i⟩

/-- El pronóstico de `n` a los `k` pasos, como fracción. -/
def pronostico (n k : ℕ) : ℚ := (3 : ℚ) ^ S k n / 2 ^ k

theorem pronostico_le_iff (n a b : ℕ) :
    pronostico n a ≤ pronostico n b ↔ 3 ^ S a n * 2 ^ b ≤ 3 ^ S b n * 2 ^ a := by
  unfold pronostico
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  norm_cast

/-- Si desde el paso `k` el pronóstico nunca baja de su valor en `k`, el número al que
    llega la órbita en el paso `k` es, a su vez, una fuga pura. -/
theorem fuga_de_minimo {n k : ℕ} (h : ∀ j, k ≤ j → pronostico n k ≤ pronostico n j) :
    FugaPura (T^[k] n) := by
  rintro ⟨i, hi⟩
  have h1 := (pronostico_le_iff n k (k + i)).1 (h (k + i) (by omega))
  rw [S_add, pow_add, pow_add] at h1
  have h2 : 3 ^ S k n * 2 ^ k * 2 ^ i ≤ 3 ^ S k n * 2 ^ k * 3 ^ S i (T^[k] n) := by
    linarith [h1]
  have h3 := Nat.le_of_mul_le_mul_left h2 (by positivity)
  omega

/-- **Rasgo 7: cohete o planeador.** O el pronóstico del fugitivo crece sin límite, y
    entonces su camino está lleno de fugas puras, sin ayuda del muro A; o vuelve una y
    otra vez por debajo de un mismo nivel C, y entonces el fugitivo regresa una y otra
    vez a tamaños que crecen apenas como el tiempo: `3 · T^k(n) ≤ C · (3n + k)`. -/
theorem rasgo_cohete_o_planeador {n : ℕ} (h : FugaPura n) :
    (∀ K, ∃ k, K ≤ k ∧ FugaPura (T^[k] n)) ∨
      ∃ C, ∀ K, ∃ k, K ≤ k ∧ 3 * T^[k] n ≤ C * (3 * n + k) := by
  by_cases hp : ∃ C, ∀ K, ∃ k, K ≤ k ∧ 3 ^ S k n ≤ C * 2 ^ k
  · right
    obtain ⟨C, hC⟩ := hp
    refine ⟨C, fun K => ?_⟩
    obtain ⟨k, hk, hkC⟩ := hC K
    refine ⟨k, hk, ?_⟩
    have ht := (rasgo_tamano h k).2
    have hS := S_le_pasos k n
    have h2 : 2 ^ k * (3 * T^[k] n) ≤ 2 ^ k * (C * (3 * n + k)) :=
      calc 2 ^ k * (3 * T^[k] n) = 3 * (2 ^ k * T^[k] n) := by ring
        _ ≤ 3 ^ S k n * (3 * n + S k n) := ht
        _ ≤ C * 2 ^ k * (3 * n + k) := Nat.mul_le_mul hkC (by omega)
        _ = 2 ^ k * (C * (3 * n + k)) := by ring
    exact Nat.le_of_mul_le_mul_left h2 (by positivity)
  · left
    push Not at hp
    intro K
    obtain ⟨K', hK'⟩ := hp (3 ^ S K n)
    have hKB : K ∈ Finset.Icc K (max K K') := Finset.mem_Icc.2 ⟨le_rfl, le_max_left _ _⟩
    obtain ⟨k, hkmem, hkmin⟩ := (Finset.Icc K (max K K')).exists_min_image (pronostico n) ⟨K, hKB⟩
    rw [Finset.mem_Icc] at hkmem
    refine ⟨k, hkmem.1, fuga_de_minimo fun j hj => ?_⟩
    by_cases hjB : j ≤ max K K'
    · exact hkmin j (Finset.mem_Icc.2 ⟨by omega, hjB⟩)
    · have hK'B := le_max_right K K'
      have h1 : 3 ^ S K n * 2 ^ j < 3 ^ S j n := hK' j (by omega)
      have h2 : pronostico n k ≤ pronostico n K := hkmin K hKB
      have h3 : pronostico n K ≤ (3 : ℚ) ^ S K n := by
        unfold pronostico
        exact div_le_self (by positivity) (one_le_pow₀ (by norm_num))
      have h4 : (3 : ℚ) ^ S K n < pronostico n j := by
        unfold pronostico
        rw [lt_div_iff₀ (by positivity)]
        exact_mod_cast h1
      linarith

open Classical in
/-- **Rasgo 4, afinado: son pocos de verdad.** Entre los primeros 2^(100m) números hay a
    lo sumo 2·2^(96m) fugas puras: por debajo de x, a lo sumo unas x^0,96. -/
theorem rasgo_pocos (m : ℕ) :
    ((Finset.range (2 ^ (100 * m))).filter FugaPura).card ≤ 2 * 2 ^ (96 * m) := by
  have h := rasgo_raro_cuenta (2 ^ (100 * m)) m
  have e : 2 ^ (100 * m) / 16 ^ m = 2 ^ (96 * m) := by
    rw [show (16 : ℕ) ^ m = 2 ^ (4 * m) by rw [pow_mul]; norm_num,
      Nat.pow_div (by omega) (by norm_num), show 100 * m - 4 * m = 96 * m by omega]
  rw [e] at h
  omega

/-- El retrato ampliado: los rasgos de un mismo fugitivo, juntos. La rareza
    (`rasgo_pocos`) es del conjunto de los fugitivos y va aparte. -/
theorem retrato_ampliado {n : ℕ} (h : FugaPura n) :
    2 ≤ n ∧ (∀ k, 63 * k ≤ 100 * S k n) ∧
      (∀ M, ∃ K, ∀ k, K ≤ k → M < T^[k] n) ∧
      (∀ a p, 1 ≤ p → ¬ ∀ i, a ≤ i → T^[i + p] n % 2 = T^[i] n % 2) ∧
      (∀ K, ∃ k, K ≤ k ∧ ∀ t, 1 ≤ t → T^[k] n < T^[t] (T^[k] n)) ∧
      (∀ k, 3 * (2 ^ k * T^[k] n) ≤ 3 ^ S k n * (3 * n + S k n)) ∧
      ((∀ K, ∃ k, K ≤ k ∧ FugaPura (T^[k] n)) ∨
        ∃ C, ∀ K, ∃ k, K ≤ k ∧ 3 * T^[k] n ≤ C * (3 * n + k)) :=
  ⟨fuga_pura_dos h, rasgo_sube h, rasgo_infinito h, rasgo_no_periodico h,
    rasgo_minimos h, fun k => (rasgo_tamano h k).2, rasgo_cohete_o_planeador h⟩

/-! ## La retroalimentación: piezas de la casa que dibujan al fugitivo -/

/-- **Con el muro A, el fugitivo nunca anda solo**: sus puntos sin retorno son, a su vez,
    fugas puras. -/
theorem crias_con_muroA (hA : MuroA) {n : ℕ} (h : FugaPura n) (K : ℕ) :
    ∃ k, K ≤ k ∧ FugaPura (T^[k] n) := by
  obtain ⟨k, hk, h2, hd⟩ := rasgo_no_desciende h K
  exact ⟨k, hk, fun hc => hd (hA _ h2 hc)⟩

/-- Con el muro A, si hay una fuga pura, las hay tan grandes como se quiera. -/
theorem fugas_sin_tope (hA : MuroA) {n : ℕ} (h : FugaPura n) (M : ℕ) :
    ∃ m, M < m ∧ FugaPura m := by
  obtain ⟨K, hK⟩ := rasgo_infinito h M
  obtain ⟨k, hk, hf⟩ := crias_con_muroA hA h K
  exact ⟨_, hK k hk, hf⟩

/-- **Con el tramo de Ocelotas** (bajo LMN): cada punto sin retorno del fugitivo es una
    fuga pura o necesita al menos 25 picos antes de su primer cruce. -/
theorem crias_con_ocelotas (hL : LMN23) {n : ℕ} (h : FugaPura n) (K : ℕ) :
    ∃ k, K ≤ k ∧ (FugaPura (T^[k] n) ∨
      ∃ j, PrimerCruce (T^[k] n) j ∧ 25 ≤ rachas (T^[k] n) j) := by
  obtain ⟨k, hk, h2, hd⟩ := rasgo_no_desciende h K
  refine ⟨k, hk, ?_⟩
  by_cases hc : Cruza (T^[k] n)
  · exact Or.inr (grieta_exige_25 hL h2 hc hd)
  · exact Or.inl hc

/-! ## Los testigos de la prueba de fuego -/

/-- El atajo, extendido a los enteros con signo. -/
def TZ (x : ℤ) : ℤ := if x % 2 = 0 then x / 2 else (3 * x + 1) / 2

/-- Subidas de `x` en los primeros `k` pasos, en los enteros con signo. -/
def SZ : ℕ → ℤ → ℕ
  | 0, _ => 0
  | k + 1, x => (if x % 2 = 0 then 0 else 1) + SZ k (TZ x)

/-- Es la misma regla: sobre los naturales, `TZ` coincide con el atajo `T`. -/
theorem TZ_natural (n : ℕ) : TZ n = (T n : ℤ) := by
  unfold TZ T
  split_ifs <;> omega

/-- El fantasma −1: con la misma regla, (3·(−1)+1)/2 = −1. -/
theorem fantasma_fijo : TZ (-1) = -1 := by decide

theorem fantasma_sube (k : ℕ) : SZ k (-1) = k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have hn : ¬ ((-1 : ℤ) % 2 = 0) := by decide
    rw [SZ, fantasma_fijo, ih, if_neg hn]
    omega

/-- **El fantasma nunca cruza**: sube en cada paso y su pronóstico, (3/2)^k, nunca baja
    de 1. Cumple «sube mucho» y «nunca cruza», pero da vueltas en su sitio: `ciclo_cruza`
    lo descarta sólo porque exige un número positivo. -/
theorem fantasma_nunca_cruza (k : ℕ) : 2 ^ k ≤ 3 ^ SZ k (-1) := by
  rw [fantasma_sube]
  exact Nat.pow_le_pow_left (by norm_num) k

/-- El atajo de la casa del vecino, con 5n+1. -/
def T5 (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (5 * n + 1) / 2

/-- Subidas en la casa del vecino. -/
def S5 : ℕ → ℕ → ℕ
  | 0, _ => 0
  | k + 1, n => n % 2 + S5 k (T5 n)

theorem vecino_vuelve : T5^[7] 13 = 13 := by decide

theorem vecino_no_baja (k : ℕ) : 13 ≤ T5^[k] 13 := by
  have h7 : ∀ r, r < 7 → 13 ≤ T5^[r] 13 := by decide
  have hq : T5^[7 * (k / 7)] 13 = 13 := by
    rw [Function.iterate_mul]
    exact Function.iterate_fixed vecino_vuelve _
  rw [← Nat.mod_add_div k 7, Function.iterate_add_apply, hq]
  exact h7 _ (Nat.mod_lt _ (by norm_num))

/-- **La grieta del vecino.** En la casa de 5n+1, el pronóstico del 13 baja de 1 a los 7
    pasos (5^3 = 125 < 128 = 2^7), pero el 13 nunca baja de sí mismo: da vueltas por
    13 → 33 → 83 → 208 → 104 → 52 → 26 → 13. Allí el muro A se cae de verdad, así que un
    argumento que levante nuestro muro A tiene que usar algo propio del 3. -/
theorem vecino_grieta : 5 ^ S5 7 13 < 2 ^ 7 ∧ ∀ k, 13 ≤ T5^[k] 13 :=
  ⟨by decide, vecino_no_baja⟩

end CasaTablero

#print axioms CasaTablero.collatz_iff_sin_intrusos
#print axioms CasaTablero.muroB_de_sin_fugas
#print axioms CasaTablero.S_le_pasos
#print axioms CasaTablero.tamano_antes_del_cruce
#print axioms CasaTablero.rasgo_minimos
#print axioms CasaTablero.rasgo_no_desciende
#print axioms CasaTablero.rasgo_tamano
#print axioms CasaTablero.pronostico_le_iff
#print axioms CasaTablero.fuga_de_minimo
#print axioms CasaTablero.rasgo_cohete_o_planeador
#print axioms CasaTablero.rasgo_pocos
#print axioms CasaTablero.retrato_ampliado
#print axioms CasaTablero.crias_con_muroA
#print axioms CasaTablero.fugas_sin_tope
#print axioms CasaTablero.crias_con_ocelotas
#print axioms CasaTablero.TZ_natural
#print axioms CasaTablero.fantasma_nunca_cruza
#print axioms CasaTablero.vecino_grieta
