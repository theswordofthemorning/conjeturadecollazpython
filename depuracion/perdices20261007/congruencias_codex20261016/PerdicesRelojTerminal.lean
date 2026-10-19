import PerdicesTransporteImpar
import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Log

/-! La carga terminal puede convertirse en pasos reales desde la misma semilla.
No se supone una cota del reloj para construir la continuación. La equivalencia
final es entre dos enunciados universales; ninguno se afirma verdadero. -/

namespace PerdicesRelojTerminal

open PerdicesTransporteImpar

def constante : Bloque → ℕ | .a => 1 | .b => 5
def duracion : Bloque → ℕ | .a => 1 | .b => 3

theorem concatenar {us vs : List Bloque} {n x y : ℕ}
    (hu : Camino us n x) (hv : Camino vs x y) : Camino (us ++ vs) n y := by
  induction hu with
  | nil => exact hv
  | cons hp _ ih => exact Camino.cons hp (ih hv)

theorem largo_concatenar (us vs : List Bloque) :
    largo (us ++ vs) = largo us + largo vs := by
  induction us with
  | nil => simp [largo]
  | cons p us ih => cases p <;> simp [largo, ih, Nat.add_assoc]

theorem paso_divisible (p : Bloque) (x : ℕ)
    (h : 2 ^ duracion p ∣ x + constante p) :
    ∃ y, Paso p x y ∧
      2 ^ duracion p * (y + constante p) = D p * (x + constante p) := by
  cases p <;> simp only [duracion, constante] at *
  · obtain ⟨k, hk⟩ := h
    refine ⟨3 * k - 1, ?_, ?_⟩ <;> simp only [Paso, N, D, E] <;> omega
  · obtain ⟨k, hk⟩ := h
    refine ⟨9 * k - 5, ?_, ?_⟩ <;> simp only [Paso, N, D, E] <;> omega

theorem continuar_racha (p : Bloque) (k x : ℕ)
    (h : 2 ^ (duracion p * k) ∣ x + constante p) :
    ∃ y, Camino (List.replicate k p) x y ∧
      2 ^ (duracion p * k) * (y + constante p) = D p ^ k * (x + constante p) := by
  induction k generalizing x with
  | zero => exact ⟨x, Camino.nil x, by simp⟩
  | succ k ih =>
    have hpaso : 2 ^ duracion p ∣ x + constante p :=
      (pow_dvd_pow 2 (by omega : duracion p ≤ duracion p * k + duracion p)).trans
        (by simpa [Nat.mul_succ] using h)
    obtain ⟨z, hp, hz⟩ := paso_divisible p x hpaso
    have hr : 2 ^ (duracion p * k) ∣ z + constante p := by
      apply Nat.dvd_of_mul_dvd_mul_left (pow_pos (by omega : 0 < 2) (duracion p))
      rw [hz, ← pow_add, Nat.add_comm, ← Nat.mul_succ]
      exact dvd_mul_of_dvd_right h _
    obtain ⟨y, hy, he⟩ := ih z hr
    refine ⟨y, Camino.cons hp hy, ?_⟩
    rw [Nat.mul_succ, pow_add, pow_succ]
    nlinarith [congrArg (fun t => 2 ^ duracion p * t) he,
      congrArg (fun t => D p ^ k * t) hz]

theorem largo_racha (p : Bloque) (k : ℕ) :
    largo (List.replicate k p) = duracion p * k := by
  induction k with
  | zero => simp [largo]
  | succ k ih => cases p <;> simp [List.replicate_succ, largo, duracion] at * <;> omega

theorem continuar_carga (x c v : ℕ) (hc : c = 1 ∨ c = 5)
    (hv : 2 ^ v ∣ x + c) :
    ∃ ps y, Camino ps x y ∧ largo ps = v := by
  rcases hc with rfl | rfl
  · obtain ⟨y, hy, _⟩ := continuar_racha .a v x (by simpa [duracion, constante] using hv)
    exact ⟨List.replicate v .a, y, hy, by simp [largo_racha, duracion]⟩
  · have hq : 2 ^ (3 * (v / 3)) ∣ x + 5 :=
      (pow_dvd_pow 2 (by omega : 3 * (v / 3) ≤ v)).trans hv
    obtain ⟨z, hz, he⟩ := continuar_racha .b (v / 3) x hq
    simp only [duracion, constante, D] at he
    have hr : 2 ^ (v % 3) ∣ z + 5 := by
      apply Nat.dvd_of_mul_dvd_mul_left (pow_pos (by omega : 0 < 2) (3 * (v / 3)))
      rw [he, ← pow_add, show 3 * (v / 3) + v % 3 = v by omega]
      exact dvd_mul_of_dvd_right hv _
    have hcuatro : 2 ^ (v % 3) ∣ 4 := by
      have : v % 3 ≤ 2 := by omega
      exact pow_dvd_pow 2 this
    have ha : 2 ^ (v % 3) ∣ z + 1 := by
      have hd := Nat.dvd_sub hr hcuatro
      simpa using hd
    obtain ⟨y, hy, _⟩ := continuar_racha .a (v % 3) z
      (by simpa [duracion, constante] using ha)
    refine ⟨List.replicate (v / 3) .b ++ List.replicate (v % 3) .a,
      y, concatenar hz hy, ?_⟩
    simp only [largo_concatenar, largo_racha, duracion, one_mul]
    omega

theorem prolongar_terminal {ps : List Bloque} {n x : ℕ}
    (h : Camino ps n x) (c : ℕ) (hc : c = 1 ∨ c = 5) :
    ∃ qs y, Camino (ps ++ qs) n y ∧
      largo (ps ++ qs) = largo ps + orden (x + c) := by
  obtain ⟨qs, y, hq, hl⟩ := continuar_carga x c (orden (x + c)) hc pow_padicValNat_dvd
  exact ⟨qs, y, concatenar h hq, by rw [largo_concatenar, hl]⟩

def Reloj (n : ℕ) (H : ℝ) : Prop :=
  ∀ ps y, Camino ps n y → (largo ps : ℝ) ≤ H

theorem reloj_controla_carga {n : ℕ} {H : ℝ} (hH : Reloj n H)
    {ps : List Bloque} {y c : ℕ} (h : Camino ps n y) (hc : c = 1 ∨ c = 5) :
    (largo ps : ℝ) + orden (y + c) ≤ H := by
  obtain ⟨qs, z, hz, hl⟩ := prolongar_terminal h c hc
  have ht := hH (ps ++ qs) z hz
  rw [hl, Nat.cast_add] at ht
  exact ht

theorem reloj_iff_carga (n : ℕ) (H : ℝ) :
    Reloj n H ↔ ∀ ps y c, Camino ps n y → (c = 1 ∨ c = 5) →
      (largo ps : ℝ) + orden (y + c) ≤ H := by
  constructor
  · intro h ps y c hp hc; exact reloj_controla_carga h hp hc
  · intro h ps y hp
    have ht := h ps y 1 hp (Or.inl rfl)
    have hv : (0 : ℝ) ≤ orden (y + 1) := Nat.cast_nonneg _
    linarith

def ell (n : ℕ) : ℕ := Nat.clog 2 (n + 5)

theorem carga_inicial_acotada (n : ℕ) (p : Bloque) :
    orden (n + constante p) ≤ ell n := by
  have hp : n + constante p ≤ n + 5 := by cases p <;> simp [constante]
  exact (padicValNat_le_nat_log _).trans
    ((Nat.log_le_clog _ _).trans (Nat.clog_mono_right 2 hp))

def Presupuesto (e a b : ℝ) : Prop :=
  ∀ n ps y, 0 < n → ps ≠ [] → Camino ps n y →
    e * (largo ps : ℝ) + orden (y + constante (ps.getLastD .a)) ≤
      orden (n + constante (ps.headD .a)) + a * ell n + b

theorem presupuesto_da_reloj {e a b : ℝ} (he : 0 < e) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h : Presupuesto e a b) {n : ℕ} (hn : 0 < n) :
    Reloj n (((1 + a) / e) * ell n + b / e) := by
  intro ps y hp
  have hell : (0 : ℝ) ≤ ell n := Nat.cast_nonneg _
  by_cases hv : ps = []
  · subst ps
    simp only [largo, Nat.cast_zero]
    positivity
  · have ht := h n ps y hn hv hp
    have hi : (orden (n + constante (ps.headD .a)) : ℝ) ≤ ell n := by
      exact_mod_cast carga_inicial_acotada n (ps.headD .a)
    have hf : (0 : ℝ) ≤ orden (y + constante (ps.getLastD .a)) := Nat.cast_nonneg _
    have hx : e * (largo ps : ℝ) ≤ (1 + a) * ell n + b := by nlinarith
    have hd : (largo ps : ℝ) ≤ ((1 + a) * ell n + b) / e :=
      (le_div_iff₀ he).mpr (by nlinarith [hx])
    convert hd using 1; ring

theorem reloj_da_presupuesto {a b : ℝ}
    (h : ∀ n, 0 < n → Reloj n (a * ell n + b)) : Presupuesto 1 a b := by
  intro n ps y hn _ hp
  have hc : constante (ps.getLastD .a) = 1 ∨ constante (ps.getLastD .a) = 5 := by
    cases ps.getLastD .a <;> simp [constante]
  have ht := reloj_controla_carga (h n hn) hp hc
  have hi : (0 : ℝ) ≤ orden (n + constante (ps.headD .a)) := Nat.cast_nonneg _
  nlinarith

theorem presupuesto_normalizado {e a b : ℝ} (he : 0 < e) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h : Presupuesto e a b) : Presupuesto 1 ((1 + a) / e) (b / e) :=
  reloj_da_presupuesto (fun _ hn => presupuesto_da_reloj he ha hb h hn)

theorem presupuesto_iff_reloj :
    (∃ e a b : ℝ, 0 < e ∧ 0 ≤ a ∧ 0 ≤ b ∧ Presupuesto e a b) ↔
      ∃ C D : ℝ, 0 ≤ C ∧ 0 ≤ D ∧ ∀ n, 0 < n → Reloj n (C * ell n + D) := by
  constructor
  · rintro ⟨e, a, b, he, ha, hb, hp⟩
    exact ⟨(1 + a) / e, b / e, by positivity, by positivity,
      fun _ hn => presupuesto_da_reloj he ha hb hp hn⟩
  · rintro ⟨C, D, hC, hD, hr⟩
    exact ⟨1, C, D, by norm_num, hC, hD, reloj_da_presupuesto hr⟩

end PerdicesRelojTerminal

#print axioms PerdicesRelojTerminal.concatenar
#print axioms PerdicesRelojTerminal.largo_concatenar
#print axioms PerdicesRelojTerminal.paso_divisible
#print axioms PerdicesRelojTerminal.continuar_racha
#print axioms PerdicesRelojTerminal.largo_racha
#print axioms PerdicesRelojTerminal.continuar_carga
#print axioms PerdicesRelojTerminal.prolongar_terminal
#print axioms PerdicesRelojTerminal.reloj_controla_carga
#print axioms PerdicesRelojTerminal.reloj_iff_carga
#print axioms PerdicesRelojTerminal.carga_inicial_acotada
#print axioms PerdicesRelojTerminal.presupuesto_da_reloj
#print axioms PerdicesRelojTerminal.reloj_da_presupuesto
#print axioms PerdicesRelojTerminal.presupuesto_normalizado
#print axioms PerdicesRelojTerminal.presupuesto_iff_reloj
