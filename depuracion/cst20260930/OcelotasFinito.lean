import OcelotasTrayectorias

/-! # Ocelotas: descenso finito certificado en el núcleo

El verificador transporta el valor de la órbita y las potencias del coeficiente.
Agotar el combustible es un rechazo, nunca una certificación. Su corrección
produce un primer cruce real y descenso, sin hipótesis de Rhin ni de rachas.
-/

namespace OcelotasFinito

open Ocelotas OcelotasTrayectorias OcelotasRachas

/-- Un estado por índice: valor x, numerador p y denominador d del coeficiente. -/
def comprobar (n : ℕ) : ℕ → ℕ → ℕ → ℕ → Bool
  | _, _, _, 0 => false
  | x, p, d, combustible + 1 =>
    if p < d then decide (x < n)
    else comprobar n (T x) (if x % 2 = 0 then p else 3 * p) (2 * d) combustible

theorem numerador_siguiente (n i : ℕ) :
    3 ^ S (i + 1) n =
      if T^[i] n % 2 = 0 then 3 ^ S i n else 3 * 3 ^ S i n := by
  rw [S_add]
  simp only [S, Nat.add_zero]
  by_cases h : T^[i] n % 2 = 0
  · simp [h]
  · have h1 : T^[i] n % 2 = 1 := by omega
    simp [h1, pow_succ, Nat.mul_comm]

/-- La aceptación da un testigo acotado y comprueba también todos sus prefijos. -/
theorem comprobar_correcto (n combustible : ℕ) : ∀ i,
    (∀ j, j < i → 1 ≤ j → 2 ^ j ≤ 3 ^ S j n) →
    comprobar n (T^[i] n) (3 ^ S i n) (2 ^ i) combustible = true →
    ∃ k, i ≤ k ∧ k < i + combustible ∧ PrimerCruce n k ∧ T^[k] n < n := by
  induction combustible with
  | zero => simp [comprobar]
  | succ combustible ih =>
    intro i hpref hc
    simp only [comprobar] at hc
    split at hc
    next hcruce =>
      exact ⟨i, le_rfl, by omega, ⟨hpref, hcruce⟩, of_decide_eq_true hc⟩
    next hantes =>
      have hpref' : ∀ j, j < i + 1 → 1 ≤ j → 2 ^ j ≤ 3 ^ S j n := by
        intro j hj hj1
        by_cases hji : j < i
        · exact hpref j hji hj1
        · have he : j = i := by omega
          subst j
          omega
      have hc' : comprobar n (T^[i + 1] n) (3 ^ S (i + 1) n)
          (2 ^ (i + 1)) combustible = true := by
        simpa only [Function.iterate_succ_apply', numerador_siguiente,
          pow_succ, Nat.mul_comm] using hc
      obtain ⟨k, hik, hkc, hk, hn⟩ := ih (i + 1) hpref' hc'
      exact ⟨k, by omega, by omega, hk, hn⟩

def semilla (n : ℕ) : Bool := comprobar n n 1 1 106

theorem semilla_correcta {n : ℕ} (h : semilla n = true) :
    ∃ k, k ≤ 105 ∧ PrimerCruce n k ∧ T^[k] n < n := by
  have hc : comprobar n (T^[0] n) (3 ^ S 0 n) (2 ^ 0) 106 = true := by
    simpa only [semilla, S, pow_zero, Function.iterate_zero, id_eq] using h
  obtain ⟨k, _, hkc, hk, hn⟩ := comprobar_correcto n 106 0 (by omega) hc
  exact ⟨k, by omega, hk, hn⟩

theorem primer_cruce_unico {n i j : ℕ}
    (hi : PrimerCruce n i) (hj : PrimerCruce n j) : i = j := by
  have hi0 : 0 < i := (ventana_cruce hi).1
  have hj0 : 0 < j := (ventana_cruce hj).1
  rcases lt_trichotomy i j with h | h | h
  · have := hj.1 i h hi0
    have := hi.2
    omega
  · exact h
  · have := hi.1 j h hj0
    have := hj.2
    omega

/-- División equilibrada del intervalo, evitando una cadena lineal de pruebas. -/
def intervalo (inicio cantidad : ℕ) : Bool :=
  if cantidad = 0 then true
  else if cantidad = 1 then semilla inicio
  else
    intervalo inicio (cantidad / 2) &&
      intervalo (inicio + cantidad / 2) (cantidad - cantidad / 2)
termination_by cantidad
decreasing_by all_goals omega

theorem intervalo_correcto (cantidad : ℕ) : ∀ inicio,
    intervalo inicio cantidad = true →
    ∀ n, inicio ≤ n → n < inicio + cantidad → semilla n = true := by
  induction cantidad using Nat.strong_induction_on with
  | h cantidad ih =>
    intro inicio hc n hn hnfin
    rw [intervalo] at hc
    split at hc
    next hz => omega
    next hz =>
      split at hc
      next h1 =>
        have he : n = inicio := by omega
        simpa only [he] using hc
      next h1 =>
        simp only [Bool.and_eq_true] at hc
        obtain ⟨hizq, hder⟩ := hc
        by_cases hmitad : n < inicio + cantidad / 2
        · exact ih (cantidad / 2) (by omega) inicio hizq n hn hmitad
        · exact ih (cantidad - cantidad / 2) (by omega)
            (inicio + cantidad / 2) hder n (by omega) (by omega)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem intervalo_comprobado : intervalo 2 11213 = true := by
  decide +kernel

theorem semillas_comprobadas : ∀ n, n ≤ 11214 → 2 ≤ n → semilla n = true := by
  intro n hmax hmin
  exact intervalo_correcto 11213 2 intervalo_comprobado n hmin (by omega)

/-- CST en el intervalo cerrado, con existencia del cruce y sin Rhin. -/
theorem existe_descenso_finito {n : ℕ} (hn : 2 ≤ n) (hnmax : n ≤ 11214) :
    ∃ k, k ≤ 105 ∧ PrimerCruce n k ∧ T^[k] n < n :=
  semilla_correcta (semillas_comprobadas n hnmax hn)

/-- Para cualquier índice que sea el primer cruce, sin imponerle un tope. -/
theorem descenso_finito {n k : ℕ} (hn : 2 ≤ n) (hnmax : n ≤ 11214)
    (hk : PrimerCruce n k) : T^[k] n < n := by
  obtain ⟨j, _, hj, hd⟩ := existe_descenso_finito hn hnmax
  simpa only [primer_cruce_unico hj hk] using hd

set_option exponentiation.threshold 131072 in
/-- El corte de tiempo de la reducción universal implica este corte de exponentes. -/
theorem exponente_acotado {k q : ℕ} (hk : k < 131072) (hP : 3 ^ q < 2 ^ k) :
    q ≤ 82696 := by
  by_contra hq
  have h3 : 3 ^ 82697 ≤ 3 ^ q := Nat.pow_le_pow_right (by decide) (by omega)
  have h2 : 2 ^ k ≤ 2 ^ 131071 := Nat.pow_le_pow_right (by decide) (by omega)
  have hbase : (2 : ℕ) ^ 131071 ≤ 3 ^ 82697 := by decide +kernel
  omega

/-- Obligación aritmética restante: cota de semilla o exclusión por la criba lineal.
No se presupone ni se declara probada su validez para todos los exponentes. -/
def CertificadoAritmetico (q : ℕ) : Prop :=
  let P := 3 ^ q
  let D := 2 ^ (Nat.log2 P + 1) - P
  10 * P ≤ 11215 * D ∨ 11 * P ≤ 2 ^ ((q - 1) / 182) * D

instance (q : ℕ) : Decidable (CertificadoAritmetico q) := by
  unfold CertificadoAritmetico
  infer_instance

/-- Ensamblaje explícito: la única pieza finita que falta es hcriba.
Rhin continúa siendo una hipótesis externa distinta de esa pieza. -/
theorem diez_de_certificado (hR : RhinEntera)
    (hcriba : ∀ q, 1 ≤ q → q ≤ 82696 → CertificadoAritmetico q)
    {n r : ℕ} {a b : ℕ → ℕ} (hn : 2 ≤ n)
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n := by
  by_contra hdesc
  have hf : n ≤ T^[tiempo a b r] n := by omega
  let k := tiempo a b r
  let q := S k n
  have hkt : k < 131072 := tiempo_diez hR hw hr hr10 hk hf
  have hk2 : 2 ≤ k := by
    have ha := (hw 0 hr).1
    have hb := (hw 0 hr).2.1
    have ht := tiempo_mono a b (show 1 ≤ r by omega)
    simp only [tiempo] at ht
    dsimp [k]
    omega
  have hkd : k = Nat.log2 (3 ^ q) + 1 := k_de_q (ventana_estricta hk hk2) hk.2
  have hq1 : 1 ≤ q := by
    by_contra h
    have hq0 : q = 0 := by omega
    simp only [hq0, pow_zero, show Nat.log2 1 = 0 from rfl] at hkd
    omega
  have hqmax : q ≤ 82696 := exponente_acotado hkt hk.2
  have hc := hcriba q hq1 hqmax
  simp only [CertificadoAritmetico] at hc
  rw [← hkd] at hc
  rcases hc with hsemilla | hfuera
  · have hp := fallo_producto hw hr hk hf
    have hrP := Nat.mul_le_mul_right (3 ^ q) hr10
    change (2 ^ k - 3 ^ q) * n < r * 3 ^ q at hp
    have hnsmall : n < 11215 := Nat.lt_of_mul_lt_mul_left
      (show (2 ^ k - 3 ^ q) * n < (2 ^ k - 3 ^ q) * 11215 by nlinarith)
    exact hdesc (descenso_finito hn (by omega) hk)
  · have hcribado : q ≤ cota 10 ((q - 1) / 182) :=
      criba_fallo hw hr hr10 hk hf hfuera
    have hlineal := cota_diez_lineal ((q - 1) / 182)
    omega

-- Los bordes 0 y 1 no se aceptan; el combustible insuficiente tampoco.
example : semilla 0 = false := by decide +kernel
example : semilla 1 = false := by decide +kernel
example : comprobar 3 3 1 1 4 = false := by decide +kernel
example : comprobar 3 3 1 1 5 = true := by decide +kernel
example : semilla 11214 = true := by decide +kernel

end OcelotasFinito

#print axioms OcelotasFinito.comprobar_correcto
#print axioms OcelotasFinito.intervalo_comprobado
#print axioms OcelotasFinito.semillas_comprobadas
#print axioms OcelotasFinito.existe_descenso_finito
#print axioms OcelotasFinito.descenso_finito
#print axioms OcelotasFinito.exponente_acotado
#print axioms OcelotasFinito.diez_de_certificado
