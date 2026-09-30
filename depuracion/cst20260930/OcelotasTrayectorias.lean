import Ocelotas
import OcelotasRachas

/-! # Ocelotas: de las rachas de la órbita a las cotas enteras

Mapa e índices exactamente los de `Ocelotas.T`, `S` y `PrimerCruce`.
Las longitudes `a i`, `b i` describen bloques impares y pares consecutivos.
No se postulan congruencias: se deducen de las paridades de la órbita.
-/

namespace OcelotasTrayectorias

open Ocelotas OcelotasRachas

def tiempo (a b : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => tiempo a b i + a i + b i

def acumulados (a : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => acumulados a i + a i

/-- Palabra real `1^(a 0) 0^(b 0) ...`, con longitudes positivas. -/
def Palabra (n : ℕ) (a b : ℕ → ℕ) (r : ℕ) : Prop :=
  ∀ i, i < r → 1 ≤ a i ∧ 1 ≤ b i ∧
    (∀ t, t < a i → T^[tiempo a b i + t] n % 2 = 1) ∧
    (∀ t, t < b i → T^[tiempo a b i + a i + t] n % 2 = 0)

instance (n r : ℕ) (a b : ℕ → ℕ) : Decidable (Palabra n a b r) := by
  unfold Palabra
  infer_instance

theorem tiempo_mono (a b : ℕ → ℕ) : Monotone (tiempo a b) := by
  apply monotone_nat_of_le_succ
  intro i
  simp only [tiempo]
  omega

theorem tiempo_lt {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) : tiempo a b i < tiempo a b r := by
  have ha := (hw i hi).1
  have hm := tiempo_mono a b (show i + 1 ≤ r by omega)
  simp only [tiempo] at hm
  omega

theorem tramos {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    (∀ t, t < a i → T^[t] (T^[tiempo a b i] n) % 2 = 1) ∧
    (∀ t, t < b i → T^[t] (T^[tiempo a b i + a i] n) % 2 = 0) := by
  obtain ⟨_, _, ho, he⟩ := hw i hi
  constructor
  · intro t ht
    rw [← iter_add]
    exact ho t ht
  · intro t ht
    rw [← iter_add]
    exact he t ht

theorem cuenta_impares {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) : ∀ i, i ≤ r → S (tiempo a b i) n = acumulados a i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    obtain ⟨ho, he⟩ := tramos hw (show i < r by omega)
    rw [tiempo, S_add, S_add, S_impar (a i) _ ho, S_par (b i) _ he,
      ih (by omega), acumulados]
    omega

theorem identidad_impar {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    2 ^ a i * (T^[tiempo a b i + a i] n + 1) =
      3 ^ a i * (T^[tiempo a b i] n + 1) := by
  have h := tramo_impar (a i) _ (tramos hw hi).1
  rwa [← iter_add] at h

theorem identidad_par {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    2 ^ b i * T^[tiempo a b (i + 1)] n = T^[tiempo a b i + a i] n := by
  have h := tramo_par (b i) _ (tramos hw hi).2
  rwa [← iter_add] at h

theorem congruencia_racha {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    2 ^ a i ∣ T^[tiempo a b i] n + 1 := by
  have hc : Nat.Coprime (2 ^ a i) (3 ^ a i) := Nat.Coprime.pow _ _ (by decide)
  apply hc.dvd_of_dvd_mul_left
  exact ⟨_, (identidad_impar hw hi).symm⟩

theorem paso_encadenado {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    2 ^ a i * (T^[tiempo a b (i + 1)] n + 1) ≤
      3 ^ a i * (T^[tiempo a b i] n + 1) := by
  have he := identidad_par hw hi
  have hp := Nat.one_le_two_pow (n := b i)
  have hle : T^[tiempo a b (i + 1)] n ≤ T^[tiempo a b i + a i] n := by
    nlinarith
  rw [← identidad_impar hw hi]
  exact Nat.mul_le_mul_left _ (by omega)

theorem cadena {n r : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r) :
    ∀ i, i ≤ r → 2 ^ acumulados a i * (T^[tiempo a b i] n + 1) ≤
      3 ^ acumulados a i * (n + 1) := by
  intro i
  induction i with
  | zero => intro _; simp [acumulados, tiempo]
  | succ i ih =>
    intro hi
    have h1 := Nat.mul_le_mul_left (2 ^ acumulados a i)
      (paso_encadenado hw (show i < r by omega))
    have h2 := Nat.mul_le_mul_left (3 ^ a i) (ih (by omega))
    simp only [acumulados, pow_add]
    nlinarith

/-- La hipótesis aritmética de la criba se obtiene de la palabra real. -/
theorem congruencias_acumuladas {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) :
    ∀ i, i < r → 2 ^ acumulados a (i + 1) ≤ (n + 1) * 3 ^ acumulados a i := by
  intro i hi
  have hd := Nat.le_of_dvd (by omega : 0 < T^[tiempo a b i] n + 1)
    (congruencia_racha hw hi)
  have hm := Nat.mul_le_mul_left (2 ^ acumulados a i) hd
  have hc := cadena hw i (by omega)
  simpa [acumulados, pow_add, Nat.mul_comm] using le_trans hm hc

theorem criba_desde_trayectoria {n r m : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hn : n + 1 < 2 ^ m) :
    S (tiempo a b r) n ≤ cota r m := by
  rw [cuenta_impares hw r le_rfl]
  exact criba_desde_congruencias (acumulados a) n m r rfl hn
    (congruencias_acumuladas hw)

theorem pre_cruce {n k j : ℕ} (hk : PrimerCruce n k) (hj : j < k) :
    2 ^ j ≤ 3 ^ S j n := by
  by_cases h0 : j = 0
  · simp [h0, S]
  · exact hk.1 j hj (by omega)

/-- Ventana necesaria para aplicar Rhin, incluso cuando k=1. -/
theorem ventana_cruce {n k : ℕ} (hk : PrimerCruce n k) :
    0 < k ∧ 2 ^ k ≤ 2 * 3 ^ S k n := by
  have hk0 : 0 < k := by
    by_contra h
    have he : k = 0 := by omega
    have := hk.2
    simp [he, S] at this
  have hp := pre_cruce hk (show k - 1 < k by omega)
  have hs : S (k - 1) n ≤ S k n := by
    have he := S_add (k - 1) 1 n
    rw [show k - 1 + 1 = k by omega] at he
    omega
  have hm := Nat.pow_le_pow_right (by decide : 1 ≤ 3) hs
  have he : 2 ^ k = 2 * 2 ^ (k - 1) := by
    rw [← pow_succ']
    congr 1
    omega
  constructor
  · exact hk0
  · rw [he]
    omega

theorem identidad_bloque {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    2 ^ tiempo a b (i + 1) * T^[tiempo a b (i + 1)] n +
      2 ^ (tiempo a b i + a i) =
      3 ^ a i * 2 ^ tiempo a b i * (T^[tiempo a b i] n + 1) := by
  calc
    _ = 2 ^ tiempo a b i * (2 ^ a i *
        (2 ^ b i * T^[tiempo a b (i + 1)] n + 1)) := by
      simp only [tiempo, pow_add]
      ring
    _ = 2 ^ tiempo a b i * (2 ^ a i * (T^[tiempo a b i + a i] n + 1)) := by
      rw [identidad_par hw hi]
    _ = _ := by rw [identidad_impar hw hi]; ring

/-- Control del término aditivo, sin introducir restas ni sumas racionales. -/
theorem cota_afin {n r : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r)
    (hk : PrimerCruce n (tiempo a b r)) :
    ∀ i, i ≤ r → 2 ^ tiempo a b i * T^[tiempo a b i] n ≤
      3 ^ acumulados a i * (n + i) := by
  intro i
  induction i with
  | zero => intro _; simp [tiempo, acumulados]
  | succ i ih =>
    intro hi
    have hp := pre_cruce hk (tiempo_lt hw (show i < r by omega))
    rw [cuenta_impares hw i (by omega)] at hp
    have he := identidad_bloque hw (show i < r by omega)
    have h1 := ih (by omega)
    have h2 := Nat.mul_le_mul_left (3 ^ a i) h1
    have h3 := Nat.mul_le_mul_left (3 ^ a i) hp
    have hpos : 0 < 2 ^ (tiempo a b i + a i) := by positivity
    simp only [acumulados, pow_add]
    nlinarith

theorem cota_afin_estricta {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hk : PrimerCruce n (tiempo a b r)) :
    2 ^ tiempo a b r * T^[tiempo a b r] n < 3 ^ acumulados a r * (n + r) := by
  obtain ⟨i, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : r ≠ 0)
  have hp := pre_cruce hk (tiempo_lt hw (show i < i + 1 by omega))
  rw [cuenta_impares hw i (by omega)] at hp
  have he := identidad_bloque hw (show i < i + 1 by omega)
  have h1 := cota_afin hw hk i (by omega)
  have h2 := Nat.mul_le_mul_left (3 ^ a i) h1
  have h3 := Nat.mul_le_mul_left (3 ^ a i) hp
  have hpos : 0 < 2 ^ (tiempo a b i + a i) := by positivity
  simp only [acumulados, pow_add]
  nlinarith

/-- Un fallo real fuerza la misma desigualdad Delta*n < r*P de la prueba escrita. -/
theorem fallo_producto {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n) :
    (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
      r * 3 ^ S (tiempo a b r) n := by
  have hc := cota_afin_estricta hw hr hk
  rw [← cuenta_impares hw r le_rfl] at hc
  have hm := Nat.mul_le_mul_left (2 ^ tiempo a b r) hf
  rw [Nat.sub_mul]
  have hp := hk.2
  have he := Nat.mul_le_mul_right n (le_of_lt hp)
  have hs := Nat.sub_add_cancel he
  nlinarith

/-- Rhin permanece como argumento explícito del teorema. -/
theorem fallo_rhin (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n) : n < r * tiempo a b r ^ 14 := by
  have hp := fallo_producto hw hr hk hf
  have he := hR _ _ (ventana_cruce hk).2 hk.2
  have hm := Nat.mul_le_mul_left r he
  have hc : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * n <
      (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * (r * tiempo a b r ^ 14) := by
    nlinarith
  exact Nat.lt_of_mul_lt_mul_left hc

theorem cota_diez_lineal (m : ℕ) : cota 10 m ≤ 182 * m := by
  simp only [cota]
  omega

theorem cota_monotona {r R m : ℕ} (hm : 1 ≤ m) (hr : r ≤ R) :
    cota r m ≤ cota R m := by
  induction R, hr using Nat.le_induction with
  | base => rfl
  | succ R hR ih => exact le_trans ih (cota_paso_monotono R m hm)

theorem tiempo_por_impares {k q : ℕ} (hq : 0 < q) (hvent : 2 ^ k ≤ 2 * 3 ^ q) :
    k ≤ 2 * q := by
  have hp : 3 ^ q < 4 ^ q := Nat.pow_lt_pow_left (by decide) (by omega)
  have he : 2 * 4 ^ q = 2 ^ (2 * q + 1) := by
    rw [pow_succ', pow_mul]
    norm_num
  have hm : 2 ^ k < 2 ^ (2 * q + 1) := by omega
  have := (Nat.pow_lt_pow_iff_right (by decide)).1 hm
  omega

theorem ventana_estricta {n k : ℕ} (hk : PrimerCruce n k) (hk2 : 2 ≤ k) :
    2 ^ k < 2 * 3 ^ S k n := by
  have hp := pre_cruce hk (show k - 1 < k by omega)
  have hne := par_ne_impar (pot2_par (show 1 ≤ k - 1 by omega)) (pot3_impar (S (k - 1) n))
  have hlt := lt_of_le_of_ne hp hne
  have hs : S (k - 1) n ≤ S k n := by
    have he := S_add (k - 1) 1 n
    rw [show k - 1 + 1 = k by omega] at he
    omega
  have hm := Nat.pow_le_pow_right (by decide : 1 ≤ 3) hs
  have he : 2 ^ k = 2 * 2 ^ (k - 1) := by
    rw [← pow_succ']
    congr 1
    omega
  rw [he]
  omega

/-- Interfaz exacta con la criba del certificado: no se aproxima el techo binario. -/
theorem criba_fallo {n r R m : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hm : (R + 1) * 3 ^ S (tiempo a b r) n ≤
      2 ^ m * (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n)) :
    S (tiempo a b r) n ≤ cota R m := by
  have hk2 : 2 ≤ tiempo a b r := by
    have ha := (hw 0 hr).1
    have hb := (hw 0 hr).2.1
    have ht := tiempo_mono a b (show 1 ≤ r by omega)
    simp only [tiempo] at ht
    omega
  have hwnd := ventana_estricta hk hk2
  have hP := hk.2
  have hD : 2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n < 3 ^ S (tiempo a b r) n := by
    omega
  have hp := fallo_producto hw hr hk hf
  have hmul := Nat.mul_le_mul_right (3 ^ S (tiempo a b r) n) hrR
  have hn : n + 1 < 2 ^ m := by
    have hprod : (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * (n + 1) <
        (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) * 2 ^ m := by
      nlinarith
    exact Nat.lt_of_mul_lt_mul_left hprod
  have hm1 : 1 ≤ m := by
    by_contra h
    have he : m = 0 := by omega
    simp [he] at hn
  exact le_trans (criba_desde_trayectoria hw hn) (cota_monotona hm1 hrR)

theorem cota_semilla {n r R : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ R)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n) :
    n ≤ (R * 3 ^ S (tiempo a b r) n - 1) /
      (2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n) := by
  have hp := fallo_producto hw hr hk hf
  have hmul := Nat.mul_le_mul_right (3 ^ S (tiempo a b r) n) hrR
  have hD : 0 < 2 ^ tiempo a b r - 3 ^ S (tiempo a b r) n := Nat.sub_pos_of_lt hk.2
  apply (Nat.le_div_iff_mul_le hD).2
  rw [Nat.mul_comm]
  omega

/-- Reducción universal del tiempo, bajo Rhin, desde una palabra real de hasta diez rachas. -/
theorem tiempo_diez (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n) :
    tiempo a b r < 131072 := by
  let k := tiempo a b r
  let t := Nat.log 2 k
  let m := 4 + 14 * (t + 1)
  have hk0 : 0 < k := (ventana_cruce hk).1
  have hlo : 2 ^ t ≤ k := Nat.pow_log_le_self 2 (by omega)
  have hhi : k < 2 ^ (t + 1) := Nat.lt_pow_succ_log_self (by decide) k
  have hn : n + 1 < 2 ^ m := by
    have hfR := fallo_rhin hR hw hr hk hf
    have hrk := Nat.mul_le_mul_right (k ^ 14) hr10
    have hp := Nat.pow_lt_pow_left hhi (by decide : 14 ≠ 0)
    have he : 16 * (2 ^ (t + 1)) ^ 14 = 2 ^ m := by
      dsimp [m]
      rw [pow_add 2 4, show 14 * (t + 1) = (t + 1) * 14 by omega, pow_mul]
      norm_num
    have hpos : 0 < k ^ 14 := by positivity
    change n < r * k ^ 14 at hfR
    nlinarith
  have hc := criba_desde_trayectoria hw hn
  have hcm := cota_monotona (by dsimp [m]; omega : 1 ≤ m) hr10
  have hd := cota_diez_lineal m
  have hq : 0 < S k n := by
    rw [show k = tiempo a b r from rfl, cuenta_impares hw r le_rfl]
    have ha := (hw 0 hr).1
    have hs := cuenta_impares hw 1 (by omega)
    have ht := tiempo_mono a b (show 1 ≤ r by omega)
    have hsum := S_add (tiempo a b 1) (tiempo a b r - tiempo a b 1) n
    rw [Nat.add_sub_of_le ht] at hsum
    rw [cuenta_impares hw r le_rfl, hs] at hsum
    simp only [acumulados] at hsum
    omega
  have hki := tiempo_por_impares hq (ventana_cruce hk).2
  have hlin : k ≤ 364 * (4 + 14 * (t + 1)) := by
    change S k n ≤ cota r m at hc
    dsimp [m] at hc hcm hd
    omega
  by_contra hlarge
  have ht : 17 ≤ t := Nat.le_log_of_pow_le (by decide) (by norm_num; omega)
  have hcola := cola_diez t ht
  omega

/-! Bordes de la interpretación: una racha, dos rachas y exclusión del inicio par. -/

example : Palabra 3 (fun _ => 2) (fun _ => 2) 1 := by decide
example : tiempo (fun _ => 2) (fun _ => 2) 1 = 4 := by decide
example : PrimerCruce 3 4 := by decide
example : ¬ Palabra 2 (fun _ => 1) (fun _ => 1) 1 := by decide
example : Palabra 39 (fun i => if i = 0 then 3 else 2)
    (fun i => if i = 0 then 1 else 2) 2 := by decide
example : PrimerCruce 39 8 := by decide

end OcelotasTrayectorias

#print axioms OcelotasTrayectorias.cuenta_impares
#print axioms OcelotasTrayectorias.congruencia_racha
#print axioms OcelotasTrayectorias.congruencias_acumuladas
#print axioms OcelotasTrayectorias.criba_desde_trayectoria
#print axioms OcelotasTrayectorias.fallo_producto
#print axioms OcelotasTrayectorias.fallo_rhin
#print axioms OcelotasTrayectorias.criba_fallo
#print axioms OcelotasTrayectorias.cota_semilla
#print axioms OcelotasTrayectorias.tiempo_diez
