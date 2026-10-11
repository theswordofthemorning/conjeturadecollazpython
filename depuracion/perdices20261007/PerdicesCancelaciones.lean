import PerdicesRepeticiones
import Mathlib.NumberTheory.Padics.PadicVal.Basic

/-! # Perdices: cancelaciones y resonancia en la mezcla 1 / 110.

La transición es total como función natural; su dominio orbital se declara
por z % 8 = 7. Persistir no se deduce de ninguna comprobación finita.
-/

namespace PerdicesCancelaciones

def orden2 (n : ℕ) : ℕ := padicValNat 2 n
def orden3 (n : ℕ) : ℕ := padicValNat 3 n

def transicion (z : ℕ) : ℕ :=
  3 ^ (orden2 (9 * z + 1) - 3) * ((9 * z + 1) / 2 ^ orden2 (9 * z + 1))

def Persiste (z : ℕ) : Prop := ∀ j, transicion^[j] z % 8 = 7

theorem orden_potencia {q : ℕ} (hq : 0 < q) (a : ℕ) :
    orden2 (2 ^ a * q) = a + orden2 q := by
  unfold orden2
  rw [padicValNat.mul (by positivity) (by omega), padicValNat.prime_pow]

theorem transicion_identidad (z : ℕ) :
    2 ^ orden2 (9 * z + 1) * transicion z =
      3 ^ (orden2 (9 * z + 1) - 3) * (9 * z + 1) := by
  have hd : 2 ^ orden2 (9 * z + 1) ∣ 9 * z + 1 := pow_padicValNat_dvd
  unfold transicion
  rw [mul_left_comm, Nat.mul_div_cancel' hd]

theorem dominio_orden (z : ℕ) : z % 8 = 7 ↔ 3 ≤ orden2 (z + 1) := by
  unfold orden2
  rw [← padicValNat_dvd_iff_le (by omega : z + 1 ≠ 0)]
  norm_num
  rw [Nat.dvd_iff_mod_eq_zero]
  omega

theorem transicion_cero {z : ℕ} (hz : 16 ∣ z + 1) :
    orden2 (9 * z + 1) = 3 ∧ 8 * (transicion z + 1) = 9 * (z + 1) := by
  obtain ⟨q, hq⟩ := hz
  have h8 : 2 ^ 3 ∣ 9 * z + 1 := ⟨18 * q - 1, by norm_num; omega⟩
  have h16 : ¬ 2 ^ 4 ∣ 9 * z + 1 := by
    rintro ⟨b, hb⟩
    norm_num at hb
    omega
  have hlo := (padicValNat_dvd_iff_le (by omega : 9 * z + 1 ≠ 0)).mp h8
  have hhi := mt (padicValNat_dvd_iff_le (by omega : 9 * z + 1 ≠ 0)).mpr h16
  have hv : orden2 (9 * z + 1) = 3 := by unfold orden2; omega
  have he := transicion_identidad z
  rw [hv] at he
  norm_num at he
  exact ⟨hv, by omega⟩

theorem orden_baja {z : ℕ} (hz : 3 < orden2 (z + 1)) :
    orden2 (transicion z + 1) + 3 = orden2 (z + 1) := by
  have h16 : 16 ∣ z + 1 := by
    have h := (padicValNat_dvd_iff_le (p := 2) (by omega : z + 1 ≠ 0)).mpr
      (show 4 ≤ orden2 (z + 1) by omega)
    simpa using h
  have he := congrArg (padicValNat 2) (transicion_cero h16).2
  rw [padicValNat.mul (by decide) (by omega),
    padicValNat.mul (by decide) (by omega)] at he
  have h8 : padicValNat 2 8 = 3 := by simpa using padicValNat.prime_pow (p := 2) 3
  have h9 : padicValNat 2 9 = 0 := padicValNat.eq_zero_of_not_dvd (by decide)
  unfold orden2
  omega

theorem persiste_paso {z : ℕ} (h : Persiste z) : Persiste (transicion z) := by
  intro j
  simpa only [Function.iterate_succ_apply] using h (j + 1)

theorem persistencia_resonante {z : ℕ} (h : Persiste z) : 3 ∣ orden2 (z + 1) := by
  suffices ∀ v z, orden2 (z + 1) = v → Persiste z → 3 ∣ v from
    this _ z rfl h
  intro v
  induction v using Nat.strong_induction_on with
  | h v ih =>
    intro z hv hz
    have h0 : z % 8 = 7 := by simpa using hz 0
    have hlo := (dominio_orden z).mp h0
    by_cases hc : v ≤ 3
    · have he : v = 3 := by omega
      simp [he]
    · have hb := orden_baja (z := z) (by omega)
      have hi := ih (orden2 (transicion z + 1)) (by omega)
        (transicion z) rfl (persiste_paso hz)
      have hd : 3 ∣ orden2 (transicion z + 1) + 3 := dvd_add hi (by decide)
      simpa only [hb, hv] using hd

theorem salida_acotada {z : ℕ} (h : orden2 (z + 1) % 3 ≠ 0) :
    ∃ j, j ≤ orden2 (z + 1) / 3 ∧ transicion^[j] z % 8 ≠ 7 := by
  suffices ∀ v z, orden2 (z + 1) = v → v % 3 ≠ 0 →
      ∃ j, j ≤ v / 3 ∧ transicion^[j] z % 8 ≠ 7 from this _ z rfl h
  intro v
  induction v using Nat.strong_induction_on with
  | h v ih =>
    intro z hv hr
    by_cases h0 : z % 8 = 7
    · have hlo := (dominio_orden z).mp h0
      have hb := orden_baja (z := z) (by omega)
      obtain ⟨j, hj, he⟩ := ih (orden2 (transicion z + 1)) (by omega)
        (transicion z) rfl (by omega)
      refine ⟨j + 1, by omega, ?_⟩
      simpa only [Function.iterate_succ_apply] using he
    · exact ⟨0, Nat.zero_le _, by simpa using h0⟩

theorem iteracion_ceros (b q z : ℕ) (hz : z + 1 = 8 ^ (b + 1) * q) :
    transicion^[b] z + 1 = 8 * 9 ^ b * q := by
  induction b generalizing q z with
  | zero => simpa using hz
  | succ b ih =>
    have h16 : 16 ∣ z + 1 := by
      refine ⟨4 * 8 ^ b * q, ?_⟩
      rw [hz, pow_succ, pow_succ]
      ring
    have hG := (transicion_cero h16).2
    have hg : transicion z + 1 = 8 ^ (b + 1) * (9 * q) := by
      rw [hz, pow_succ] at hG
      nlinarith only [hG]
    have hh := ih (9 * q) (transicion z) hg
    rw [Function.iterate_succ_apply]
    rw [hh, pow_succ]
    ring

def impar2 (x : ℕ) : ℕ := x / 2 ^ orden2 x
def exponente (h : ℕ) : ℕ := orden2 (9 * h - 1)
def carga (h : ℕ) : ℕ := 3 ^ exponente h * impar2 (9 * h - 1) + 1
def reinicio (h : ℕ) : ℕ := 9 ^ (orden2 (carga h) / 3 - 1) * impar2 (carga h)

theorem descomposicion (x : ℕ) : 2 ^ orden2 x * impar2 x = x :=
  Nat.mul_div_cancel' pow_padicValNat_dvd

theorem impar2_pos {x : ℕ} (hx : 0 < x) : 0 < impar2 x := by
  have he := descomposicion x
  by_contra hh
  have hz : impar2 x = 0 := by omega
  rw [hz, mul_zero] at he
  omega

theorem impar2_impar {x : ℕ} (hx : 0 < x) : impar2 x % 2 = 1 := by
  have hd : ¬ 2 ∣ impar2 x := by
    rintro ⟨r, hr⟩
    apply pow_succ_padicValNat_not_dvd (p := 2) (by omega : x ≠ 0)
    refine ⟨r, ?_⟩
    change x = 2 ^ (orden2 x + 1) * r
    calc
      x = 2 ^ orden2 x * impar2 x := (descomposicion x).symm
      _ = _ := by rw [hr]; ring
  rw [Nat.dvd_iff_mod_eq_zero] at hd
  omega

theorem exponente_pos {h : ℕ} (hp : 0 < h) (hi : h % 2 = 1) :
    1 ≤ exponente h := by
  apply one_le_padicValNat_of_dvd (by omega : 9 * h - 1 ≠ 0)
  exact Nat.dvd_of_mod_eq_zero (by omega)

theorem carga_identidad (h : ℕ) :
    2 ^ exponente h * carga h = 3 ^ exponente h * (9 * h - 1) + 2 ^ exponente h := by
  have he := descomposicion (9 * h - 1)
  change 2 ^ exponente h * impar2 (9 * h - 1) = 9 * h - 1 at he
  unfold carga
  nlinarith only [congrArg (3 ^ exponente h * ·) he]

theorem carga_transicion {h z : ℕ} (hz : z + 1 = 8 * h) :
    transicion z + 1 = carga h := by
  have hp : 0 < 9 * h - 1 := by omega
  have he : 9 * z + 1 = 2 ^ 3 * (9 * h - 1) := by norm_num; omega
  have hv : orden2 (9 * z + 1) = 3 + exponente h := by
    rw [he, orden_potencia hp]
    rfl
  have hd : (9 * z + 1) / 2 ^ (3 + exponente h) = impar2 (9 * h - 1) := by
    rw [he, pow_add, Nat.mul_div_mul_left _ _ (by norm_num : 0 < (2 : ℕ) ^ 3)]
    rfl
  unfold transicion carga
  rw [hv, hd]
  rw [show 3 + exponente h - 3 = exponente h by omega]

theorem reinicio_correspondencia {h z b : ℕ}
    (hz : z + 1 = 8 * h) (hk : orden2 (carga h) = 3 * (b + 1)) :
    transicion^[b + 1] z + 1 = 8 * reinicio h := by
  have hg := carga_transicion hz
  have hd := descomposicion (carga h)
  rw [hk, pow_mul] at hd
  norm_num at hd
  have hh := iteracion_ceros b (impar2 (carga h)) (transicion z) (by omega)
  rw [Function.iterate_succ_apply, hh]
  unfold reinicio
  rw [hk]
  have hb : 3 * (b + 1) / 3 - 1 = b := by omega
  rw [hb]
  ring

theorem carga_crece {h : ℕ} (hp : 0 < h) (hi : h % 2 = 1) :
    13 * h ≤ carga h := by
  have ha := exponente_pos hp hi
  obtain ⟨a, he⟩ : ∃ a, exponente h = a + 1 := ⟨exponente h - 1, by omega⟩
  have hpot := Nat.pow_le_pow_left (by decide : 2 ≤ 3) a
  have hc := carga_identidad h
  rw [he, pow_succ, pow_succ] at hc
  have hsub : 9 * h - 1 + 1 = 9 * h := by omega
  have hmul := Nat.mul_le_mul_right (9 * h - 1) hpot
  have hp2 : 0 < (2 : ℕ) ^ a := by positivity
  nlinarith [Nat.mul_le_mul_left (2 ^ a) (show 1 ≤ h by omega)]

theorem reinicio_crece {h b : ℕ} (hp : 0 < h) (hi : h % 2 = 1)
    (hk : orden2 (carga h) = 3 * (b + 1)) : 13 * h ≤ 8 * reinicio h := by
  have hc := carga_crece hp hi
  have hd := descomposicion (carga h)
  rw [hk, pow_mul] at hd
  norm_num at hd
  have hpot := Nat.pow_le_pow_left (by decide : 8 ≤ 9) b
  unfold reinicio
  rw [hk, show 3 * (b + 1) / 3 - 1 = b by omega]
  rw [pow_succ] at hd
  nlinarith [Nat.mul_le_mul_right (impar2 (carga h)) hpot]

theorem orden3_carga {h : ℕ} (hp : 0 < h) (hi : h % 2 = 1) :
    orden3 (carga h) = 0 := by
  have ha := exponente_pos hp hi
  have hd : 3 ∣ 3 ^ exponente h := dvd_pow_self _ (by omega : exponente h ≠ 0)
  have hm : 3 ∣ 3 ^ exponente h * impar2 (9 * h - 1) := dvd_mul_of_dvd_left hd _
  unfold orden3
  apply padicValNat.eq_zero_of_not_dvd
  intro hh
  unfold carga at hh
  obtain ⟨q, hq⟩ := hm
  obtain ⟨r, hr⟩ := hh
  omega

theorem perfil_ternario {h b : ℕ} (hp : 0 < h) (hi : h % 2 = 1)
    (hk : orden2 (carga h) = 3 * (b + 1)) : orden3 (reinicio h) = 2 * b := by
  have hc : 0 < carga h := by unfold carga; omega
  have hq := impar2_pos hc
  have hd : 2 ^ orden2 (carga h) ∣ carga h := pow_padicValNat_dvd
  have hco : Nat.Coprime 3 (2 ^ orden2 (carga h)) :=
    (show Nat.Coprime 3 2 by decide).pow_right _
  have hv : padicValNat 3 (impar2 (carga h)) = 0 := by
    rw [impar2, padicValNat.div' hco hd]
    exact orden3_carga hp hi
  unfold orden3 reinicio
  rw [hk, show 3 * (b + 1) / 3 - 1 = b by omega]
  rw [padicValNat.mul (by positivity) (by omega), hv, add_zero, padicValNat.pow]
  have h9 : padicValNat 3 9 = 2 := by simpa using padicValNat.prime_pow (p := 3) 2
  rw [h9]
  omega

end PerdicesCancelaciones

#print axioms PerdicesCancelaciones.orden_potencia
#print axioms PerdicesCancelaciones.transicion_identidad
#print axioms PerdicesCancelaciones.dominio_orden
#print axioms PerdicesCancelaciones.transicion_cero
#print axioms PerdicesCancelaciones.orden_baja
#print axioms PerdicesCancelaciones.persiste_paso
#print axioms PerdicesCancelaciones.persistencia_resonante
#print axioms PerdicesCancelaciones.salida_acotada
#print axioms PerdicesCancelaciones.iteracion_ceros
#print axioms PerdicesCancelaciones.descomposicion
#print axioms PerdicesCancelaciones.impar2_pos
#print axioms PerdicesCancelaciones.impar2_impar
#print axioms PerdicesCancelaciones.exponente_pos
#print axioms PerdicesCancelaciones.carga_identidad
#print axioms PerdicesCancelaciones.carga_transicion
#print axioms PerdicesCancelaciones.reinicio_correspondencia
#print axioms PerdicesCancelaciones.carga_crece
#print axioms PerdicesCancelaciones.reinicio_crece
#print axioms PerdicesCancelaciones.orden3_carga
#print axioms PerdicesCancelaciones.perfil_ternario
