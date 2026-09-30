import OcelotasFinito

/-! # Ocelotas: verificador por intervalos enteros para la criba

Los extremos encierran escala * 3^q / 2^k. Cada redondeo es hacia fuera.
La aceptación comprueba la ventana estricta y una de las dos desigualdades
del CertificadoAritmetico. No se usan aproximaciones de logaritmos.
-/

namespace OcelotasCriba

open Ocelotas OcelotasFinito

def escala : ℕ := 281474976710656

structure Marco where
  inferior : ℕ
  superior : ℕ
  exponente : ℕ

def Encierra (q : ℕ) (s : Marco) : Prop :=
  s.inferior * 2 ^ s.exponente ≤ escala * 3 ^ q ∧
    escala * 3 ^ q ≤ s.superior * 2 ^ s.exponente

instance (q : ℕ) (s : Marco) : Decidable (Encierra q s) := by
  unfold Encierra
  infer_instance

def paso (s : Marco) : Marco :=
  if 3 * s.superior < 2 * escala then
    ⟨3 * s.inferior / 2, (3 * s.superior + 1) / 2, s.exponente + 1⟩
  else
    ⟨3 * s.inferior / 4, (3 * s.superior + 3) / 4, s.exponente + 2⟩

theorem paso_encierra {q : ℕ} {s : Marco} (h : Encierra q s) :
    Encierra (q + 1) (paso s) := by
  obtain ⟨hl, hu⟩ := h
  unfold paso
  split
  · change (3 * s.inferior / 2) * 2 ^ (s.exponente + 1) ≤ escala * 3 ^ (q + 1) ∧
      escala * 3 ^ (q + 1) ≤ ((3 * s.superior + 1) / 2) * 2 ^ (s.exponente + 1)
    have hl' : (3 * s.inferior / 2) * 2 ≤ 3 * s.inferior := by omega
    have hu' : 3 * s.superior ≤ ((3 * s.superior + 1) / 2) * 2 := by omega
    have hml := Nat.mul_le_mul_right (2 ^ s.exponente) hl'
    have hmu := Nat.mul_le_mul_right (2 ^ s.exponente) hu'
    simp only [pow_succ]
    constructor <;> nlinarith
  · change (3 * s.inferior / 4) * 2 ^ (s.exponente + 2) ≤ escala * 3 ^ (q + 1) ∧
      escala * 3 ^ (q + 1) ≤ ((3 * s.superior + 3) / 4) * 2 ^ (s.exponente + 2)
    have hl' : (3 * s.inferior / 4) * 4 ≤ 3 * s.inferior := by omega
    have hu' : 3 * s.superior ≤ ((3 * s.superior + 3) / 4) * 4 := by omega
    have hml := Nat.mul_le_mul_right (2 ^ s.exponente) hl'
    have hmu := Nat.mul_le_mul_right (2 ^ s.exponente) hu'
    simp only [pow_succ]
    constructor <;> nlinarith

def acepta (q : ℕ) (s : Marco) : Bool :=
  decide (escala < 2 * s.inferior ∧ s.superior < escala ∧
    (11225 * s.superior ≤ 11215 * escala ∨
      (2 ^ ((q - 1) / 182) + 11) * s.superior ≤ 2 ^ ((q - 1) / 182) * escala))

theorem acepta_correcto {q : ℕ} {s : Marco} (he : Encierra q s)
    (ha : acepta q s = true) : CertificadoAritmetico q := by
  have hdatos := of_decide_eq_true ha
  change escala < 2 * s.inferior ∧ s.superior < escala ∧
    (11225 * s.superior ≤ 11215 * escala ∨
      (2 ^ ((q - 1) / 182) + 11) * s.superior ≤ 2 ^ ((q - 1) / 182) * escala) at hdatos
  obtain ⟨hlo, hup, hcasos⟩ := hdatos
  obtain ⟨hl, hu⟩ := he
  have hesc : 0 < escala := by decide
  have hpot : 0 < (2 : ℕ) ^ s.exponente := by positivity
  have hP : 3 ^ q < 2 ^ s.exponente := by
    have hm := Nat.mul_lt_mul_of_pos_right hup hpot
    exact Nat.lt_of_mul_lt_mul_left (lt_of_le_of_lt hu hm)
  have hvent : 2 ^ s.exponente < 2 * 3 ^ q := by
    have hm := Nat.mul_lt_mul_of_pos_right hlo hpot
    apply Nat.lt_of_mul_lt_mul_left (a := escala)
    nlinarith
  have hk := k_de_q hvent hP
  dsimp only [CertificadoAritmetico]
  rw [← hk]
  have hD : 2 ^ s.exponente - 3 ^ q + 3 ^ q = 2 ^ s.exponente :=
    Nat.sub_add_cancel (Nat.le_of_lt hP)
  rcases hcasos with hc | hc
  · left
    have hm := Nat.mul_le_mul_right (2 ^ s.exponente) hc
    have hmul : escala * (11225 * 3 ^ q) ≤ escala * (11215 * 2 ^ s.exponente) := by
      nlinarith
    have hcancel := Nat.le_of_mul_le_mul_left hmul hesc
    omega
  · right
    let M := 2 ^ ((q - 1) / 182)
    change (M + 11) * s.superior ≤ M * escala at hc
    have hm := Nat.mul_le_mul_right (2 ^ s.exponente) hc
    have hprod := Nat.mul_le_mul_left (M + 11) hu
    have hmul : escala * ((M + 11) * 3 ^ q) ≤ escala * (M * 2 ^ s.exponente) := by
      nlinarith
    have hcancel := Nat.le_of_mul_le_mul_left hmul hesc
    change 11 * 3 ^ q ≤ M * (2 ^ s.exponente - 3 ^ q)
    nlinarith

def recorrer (q : ℕ) (s : Marco) : ℕ → Bool
  | 0 => true
  | cantidad + 1 => acepta (q + 1) (paso s) && recorrer (q + 1) (paso s) cantidad

theorem recorrer_correcto (cantidad : ℕ) : ∀ q s,
    Encierra q s → recorrer q s cantidad = true →
    ∀ t, q < t → t ≤ q + cantidad → CertificadoAritmetico t := by
  induction cantidad with
  | zero => intro q s he hc t ht hfin; omega
  | succ cantidad ih =>
    intro q s he hc t ht hfin
    simp only [recorrer, Bool.and_eq_true] at hc
    have he' := paso_encierra he
    by_cases hprimero : t = q + 1
    · subst t
      exact acepta_correcto he' hc.1
    · exact ih (q + 1) (paso s) he' hc.2 t (by omega) (by omega)

-- Ventana estricta, rechazo de una cota falsa y aceptación del primer exponente.
example : acepta 0 ⟨140737488355328, 140737488355328, 1⟩ = false := by decide +kernel
example : ¬ Encierra 1 ⟨281474976710655, 281474976710655, 2⟩ := by decide +kernel
example : acepta 1 ⟨281474976710655, 281474976710655, 2⟩ = false := by decide +kernel
example : Encierra 1 ⟨211106232532992, 211106232532992, 2⟩ := by decide +kernel
example : acepta 1 ⟨211106232532992, 211106232532992, 2⟩ = true := by decide +kernel

end OcelotasCriba

#print axioms OcelotasCriba.paso_encierra
#print axioms OcelotasCriba.acepta_correcto
#print axioms OcelotasCriba.recorrer_correcto
