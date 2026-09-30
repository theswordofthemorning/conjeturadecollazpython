import OcelotasCierre

/-! # Ocelotas: contador de rachas y extracción de la palabra real

`rachas n k` cuenta los inicios de rachas impares en los índices `0 ≤ j < k`.
El índice cero inicia una racha si es impar; los demás necesitan un predecesor par.
Se usa el atajo `Ocelotas.T`, sin hipótesis de existencia del primer cruce.
-/

namespace OcelotasContador

open Ocelotas OcelotasTrayectorias OcelotasCertificado OcelotasCierre

/-- Número canónico de rachas impares en los primeros k pasos del atajo. -/
def rachas (n : ℕ) : ℕ → ℕ
  | 0 => 0
  | k + 1 => rachas n k +
      if T^[k] n % 2 = 1 ∧ (k = 0 ∨ T^[k - 1] n % 2 = 0) then 1 else 0

theorem rachas_eq_card (n k : ℕ) :
    rachas n k = ((Finset.range k).filter fun j =>
      T^[j] n % 2 = 1 ∧ (j = 0 ∨ T^[j - 1] n % 2 = 0)).card := by
  induction k with
  | zero => simp [rachas]
  | succ k ih =>
    rw [rachas, Finset.range_add_one, Finset.filter_insert]
    by_cases h : T^[k] n % 2 = 1 ∧ (k = 0 ∨ T^[k - 1] n % 2 = 0)
    · simp [h, ih]
    · simp [h, ih]

theorem tiempo_actualizar (a b : ℕ → ℕ) (r u v i : ℕ) (hi : i ≤ r) :
    tiempo (Function.update a r u) (Function.update b r v) i = tiempo a b i := by
  induction i with
  | zero => rfl
  | succ i ih =>
    simp only [tiempo, ih (by omega), Function.update_of_ne (show i ≠ r by omega)]

theorem anexar {n r u v : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hu : 0 < u) (hv : 0 < v)
    (ho : ∀ t, t < u → T^[tiempo a b r + t] n % 2 = 1)
    (he : ∀ t, t < v → T^[tiempo a b r + u + t] n % 2 = 0) :
    Palabra n (Function.update a r u) (Function.update b r v) (r + 1) ∧
    tiempo (Function.update a r u) (Function.update b r v) (r + 1) =
      tiempo a b r + u + v := by
  constructor
  · intro i hi
    rw [tiempo_actualizar a b r u v i (by omega)]
    by_cases hir : i = r
    · subst i
      simp only [Function.update_self]
      exact ⟨by omega, by omega, ho, he⟩
    · simp only [Function.update_of_ne hir]
      exact hw i (by omega)
  · simp only [tiempo, tiempo_actualizar a b r u v r le_rfl, Function.update_self]

/-- Bloques completos seguidos de una racha impar y de un tramo par quizá vacío. -/
def Pendiente (n : ℕ) (a b : ℕ → ℕ) (r u v : ℕ) : Prop :=
  Palabra n a b r ∧ 0 < u ∧
    (∀ t, t < u → T^[tiempo a b r + t] n % 2 = 1) ∧
    (∀ t, t < v → T^[tiempo a b r + u + t] n % 2 = 0)

theorem ultimo_impar {n r u k : ℕ} {a b : ℕ → ℕ}
    (hp : Pendiente n a b r u 0) (hk : tiempo a b r + u = k) :
    T^[k - 1] n % 2 = 1 := by
  have hu := hp.2.1
  have h := hp.2.2.1 (u - 1) (by omega)
  rwa [show tiempo a b r + (u - 1) = k - 1 by omega] at h

theorem ultimo_par {n r u v k : ℕ} {a b : ℕ → ℕ}
    (hp : Pendiente n a b r u v) (hv : 0 < v)
    (hk : tiempo a b r + u + v = k) : T^[k - 1] n % 2 = 0 := by
  have h := hp.2.2.2 (v - 1) (by omega)
  rwa [show tiempo a b r + u + (v - 1) = k - 1 by omega] at h

/-- Invariante de lectura: el contador coincide con los bloques, incluido el abierto. -/
theorem leer_prefijo {n : ℕ} (hn : n % 2 = 1) (k : ℕ) :
    ∃ a b r u v, Pendiente n a b r u v ∧
      tiempo a b r + u + v = k + 1 ∧ rachas n (k + 1) = r + 1 := by
  induction k with
  | zero =>
    refine ⟨fun _ => 0, fun _ => 0, 0, 1, 0, ?_, rfl, ?_⟩
    · refine ⟨?_, by omega, ?_, ?_⟩
      · intro i hi; omega
      · intro t ht
        have : t = 0 := by omega
        simpa [this, tiempo] using hn
      · intro t ht; omega
    · simp [rachas, hn]
  | succ k ih =>
    obtain ⟨a, b, r, u, v, hp, hlen, hcount⟩ := ih
    by_cases hpar : T^[k + 1] n % 2 = 0
    · refine ⟨a, b, r, u, v + 1, ?_, by omega, ?_⟩
      · refine ⟨hp.1, hp.2.1, hp.2.2.1, ?_⟩
        intro t ht
        by_cases htv : t < v
        · exact hp.2.2.2 t htv
        · have : t = v := by omega
          simpa only [this, hlen] using hpar
      · simp only [rachas, hpar, Nat.zero_ne_one, false_and, ↓reduceIte, Nat.add_zero]
        exact hcount
    · have himpar : T^[k + 1] n % 2 = 1 := by omega
      by_cases hv : v = 0
      · subst v
        have hprev : T^[k] n % 2 = 1 := by
          simpa using ultimo_impar hp (by omega : tiempo a b r + u = k + 1)
        refine ⟨a, b, r, u + 1, 0, ?_, by omega, ?_⟩
        · refine ⟨hp.1, by omega, ?_, ?_⟩
          · intro t ht
            by_cases htu : t < u
            · exact hp.2.2.1 t htu
            · have : tiempo a b r + t = k + 1 := by omega
              simpa only [this] using himpar
          · intro t ht; omega
        · rw [rachas, hcount]
          simp only [Nat.add_sub_cancel, hprev, Nat.add_eq_zero_iff, Nat.one_ne_zero,
            and_false, Nat.one_ne_zero, or_self, and_false, ↓reduceIte, Nat.add_zero]
      · obtain ⟨hw, htime⟩ := anexar hp.1 hp.2.1 (by omega : 0 < v)
          hp.2.2.1 hp.2.2.2
        have hprev : T^[k] n % 2 = 0 := by
          simpa using ultimo_par hp (by omega : 0 < v) hlen
        refine ⟨Function.update a r u, Function.update b r v, r + 1, 1, 0,
          ?_, by omega, ?_⟩
        · refine ⟨hw, by omega, ?_, ?_⟩
          · intro t ht
            have : t = 0 := by omega
            simpa only [this, Nat.add_zero, htime, hlen] using himpar
          · intro t ht; omega
        · rw [rachas, hcount]
          simp only [Nat.add_sub_cancel, hprev, himpar, or_true, and_self, ↓reduceIte]

theorem extraer_palabra {n k : ℕ} (hn : n % 2 = 1) (hk : 0 < k)
    (hfin : T^[k - 1] n % 2 = 0) :
    0 < rachas n k ∧ ∃ a b, Palabra n a b (rachas n k) ∧
      tiempo a b (rachas n k) = k := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : k ≠ 0)
  obtain ⟨a, b, r, u, v, hp, hlen, hcount⟩ := leer_prefijo hn j
  have hv : 0 < v := by
    by_contra h
    have hv0 : v = 0 := by omega
    subst v
    have hh := ultimo_impar hp (by omega : tiempo a b r + u = j + 1)
    rw [hh] at hfin
    omega
  obtain ⟨hw, he⟩ := anexar hp.1 hp.2.1 hv hp.2.2.1 hp.2.2.2
  rw [hcount]
  exact ⟨by omega, Function.update a r u, Function.update b r v, hw, he.trans hlen⟩

/-- El paso que cruza por primera vez el coeficiente tiene entrada par. -/
theorem cruce_termina_par {n k : ℕ} (hk : PrimerCruce n k) :
    T^[k - 1] n % 2 = 0 := by
  have hk0 := (ventana_cruce hk).1
  have hp := pre_cruce hk (show k - 1 < k by omega)
  by_contra h
  have ho : T^[k - 1] n % 2 = 1 := by omega
  have hs := S_add (k - 1) 1 n
  rw [show k - 1 + 1 = k by omega] at hs
  simp only [S, ho, Nat.add_zero] at hs
  have hpow : 2 ^ k = 2 ^ (k - 1) * 2 := by
    rw [← pow_succ]
    congr 1
    omega
  have hc := hk.2
  rw [hs, pow_succ, hpow] at hc
  have hpos : 0 < 3 ^ S (k - 1) n := by positivity
  omega

theorem palabra_del_cruce {n k : ℕ} (hn : n % 2 = 1) (hk : PrimerCruce n k) :
    0 < rachas n k ∧ ∃ a b, Palabra n a b (rachas n k) ∧
      tiempo a b (rachas n k) = k :=
  extraer_palabra hn (ventana_cruce hk).1 (cruce_termina_par hk)

/-- CST hasta diez rachas contadas directamente, bajo la hipótesis externa de Rhin. -/
theorem descenso_contador (hR : RhinEntera) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) : T^[k] n < n := by
  by_cases hpar : n % 2 = 0
  · exact descenso_par hn hpar hk
  · obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hh := ocelotas_diez hR hn hw hpos hr
    rw [he] at hh
    exact hh hk

theorem fallo_contador_exige_once (hR : RhinEntera) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hf : n ≤ T^[k] n) : 11 ≤ rachas n k := by
  by_contra h
  have := descenso_contador hR hn hk (by omega : rachas n k ≤ 10)
  omega

/-- El término aditivo del atajo nunca es negativo. -/
theorem cota_inferior (n k : ℕ) : 3 ^ S k n * n ≤ 2 ^ k * T^[k] n := by
  induction k with
  | zero => simp [S]
  | succ k ih =>
    rw [OcelotasFinito.numerador_siguiente, pow_succ, Function.iterate_succ_apply']
    by_cases h : T^[k] n % 2 = 0
    · rw [if_pos h]
      have he := congrArg (fun x => 2 ^ k * x) (T_par h)
      nlinarith
    · rw [if_neg h]
      have he := congrArg (fun x => 2 ^ k * x) (T_impar (by omega : T^[k] n % 2 = 1))
      calc
        _ ≤ 3 * (2 ^ k * T^[k] n) := by
          simpa only [Nat.mul_assoc] using Nat.mul_le_mul_left 3 ih
        _ ≤ _ := by nlinarith only [he, Nat.zero_le (2 ^ k)]

theorem no_desciende_antes {n k j : ℕ} (hk : PrimerCruce n k) (hj : j < k) :
    n ≤ T^[j] n := by
  have hp := Nat.mul_le_mul_right n (pre_cruce hk hj)
  have hc := cota_inferior n j
  have hpos : 0 < 2 ^ j := by positivity
  nlinarith

/-- Coinciden el primer descenso real y el primer cruce del coeficiente. -/
theorem cst_contador (hR : RhinEntera) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  ⟨fun _ hj => no_desciende_antes hk hj, descenso_contador hR hn hk hr⟩

-- Bordes: prefijo vacío, racha abierta, caso par y dos rachas completas.
example : rachas 3 0 = 0 := by decide +kernel
example : rachas 3 1 = 1 := by decide +kernel
example : rachas 3 2 = 1 := by decide +kernel
example : rachas 2 1 = 0 := by decide +kernel
example : rachas 3 4 = 1 ∧ PrimerCruce 3 4 := by decide +kernel
example : rachas 7 7 = 2 ∧ PrimerCruce 7 7 := by decide +kernel
example : rachas 27 59 = 15 ∧ PrimerCruce 27 59 := by decide +kernel
-- n=1 está fuera del dominio del descenso estricto.
example : rachas 1 2 = 1 ∧ PrimerCruce 1 2 ∧ T^[2] 1 = 1 := by decide +kernel

end OcelotasContador

#print axioms OcelotasContador.rachas_eq_card
#print axioms OcelotasContador.leer_prefijo
#print axioms OcelotasContador.extraer_palabra
#print axioms OcelotasContador.cruce_termina_par
#print axioms OcelotasContador.palabra_del_cruce
#print axioms OcelotasContador.descenso_contador
#print axioms OcelotasContador.fallo_contador_exige_once
#print axioms OcelotasContador.no_desciende_antes
#print axioms OcelotasContador.cst_contador
