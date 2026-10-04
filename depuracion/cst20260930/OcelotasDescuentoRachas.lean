import OcelotasAfinada
import OcelotasTrayectorias

/-! # Descuento de un paso impar por cada racha

Para palabras reales con entradas positivas, cada bloque impar seguido
de al menos un paso par permite encadenar exponentes a_i - 1.
No se usa LMN ni se supone un primer cruce. Este módulo mejora una cota
auxiliar; por sí solo no demuestra un nuevo cierre de CST.
-/

namespace OcelotasDescuentoRachas

open Real Ocelotas OcelotasTrayectorias

def descontados (a : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => descontados a i + (a i - 1)

theorem paso_positivo {n : ℕ} (hn : 0 < n) : 0 < T n := by
  unfold T
  split <;> omega

theorem iterado_positivo {n : ℕ} (hn : 0 < n) (k : ℕ) : 0 < T^[k] n := by
  induction k with
  | zero => exact hn
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    exact paso_positivo ih

theorem cuenta_descontada {n r : ℕ} {a b : ℕ → ℕ} (hw : Palabra n a b r) :
    ∀ i, i ≤ r → acumulados a i = descontados a i + i := by
  intro i
  induction i with
  | zero => intros; rfl
  | succ i ih =>
    intro hi
    have ha := (hw i (by omega)).1
    have hp := ih (by omega)
    simp only [acumulados, descontados]
    omega

theorem paso_descontado {n r i : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < n) (hw : Palabra n a b r) (hi : i < r) :
    2 ^ (a i - 1) * (T^[tiempo a b (i + 1)] n + 1) ≤
      3 ^ (a i - 1) * (T^[tiempo a b i] n + 1) := by
  have ha := (hw i hi).1
  have hb := (hw i hi).2.1
  have h2 : 2 ^ a i = 2 * 2 ^ (a i - 1) := by
    conv_lhs => rw [← Nat.sub_add_cancel ha]
    rw [pow_succ]
    omega
  have h3 : 3 ^ a i = 3 * 3 ^ (a i - 1) := by
    conv_lhs => rw [← Nat.sub_add_cancel ha]
    rw [pow_succ]
    omega
  have hpot : 2 ≤ 2 ^ b i := by
    simpa using (Nat.pow_le_pow_right (by decide : 1 ≤ 2) hb)
  have he := identidad_par hw hi
  have ho := identidad_impar hw hi
  rw [h2, h3] at ho
  have hy := iterado_positivo hn (tiempo a b (i + 1))
  have hle : 2 * T^[tiempo a b (i + 1)] n ≤ T^[tiempo a b i + a i] n := by
    nlinarith
  have hm := Nat.mul_le_mul_left (2 * 2 ^ (a i - 1)) hle
  have hym := Nat.mul_le_mul_left (2 ^ (a i - 1)) (Nat.succ_le_of_lt hy)
  nlinarith

theorem cadena_descontada {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < n) (hw : Palabra n a b r) :
    ∀ i, i ≤ r → 2 ^ descontados a i * (T^[tiempo a b i] n + 1) ≤
      3 ^ descontados a i * (n + 1) := by
  intro i
  induction i with
  | zero => intros; simp [descontados, tiempo]
  | succ i ih =>
    intro hi
    have h1 := Nat.mul_le_mul_left (2 ^ descontados a i)
      (paso_descontado hn hw (show i < r by omega))
    have h2 := Nat.mul_le_mul_left (3 ^ (a i - 1)) (ih (by omega))
    simp only [descontados, pow_add]
    nlinarith

theorem congruencias_descontadas {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < n) (hw : Palabra n a b r) :
    ∀ i, i < r → 2 ^ (descontados a (i + 1) + 1) ≤
      (n + 1) * 3 ^ descontados a i := by
  intro i hi
  have ha := (hw i hi).1
  have hd := Nat.le_of_dvd (by omega : 0 < T^[tiempo a b i] n + 1)
    (congruencia_racha hw hi)
  have hm := Nat.mul_le_mul_left (2 ^ descontados a i) hd
  have hc := cadena_descontada hn hw i (by omega)
  have he : descontados a (i + 1) + 1 = descontados a i + a i := by
    simp only [descontados]
    omega
  rw [he, pow_add]
  simpa [Nat.mul_comm] using le_trans hm hc

theorem criba_congruencias (D : ℕ → ℕ) {n s r : ℕ} {alfa beta : ℝ}
    (hs : 0 < s) (hn : n + 1 ≤ s) (h0 : D 0 = 0) (ha : 0 ≤ alfa)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2)
    (hc : ∀ i, i < r → 2 ^ (D (i + 1) + 1) ≤ (n + 1) * 3 ^ D i) :
    D r ≤ OcelotasAfinada.cota alfa (beta - 1) r := by
  induction r with
  | zero => simp [OcelotasAfinada.cota, h0]
  | succ r ih =>
    have hprev := ih (fun i hi => hc i (by omega))
    have hp := OcelotasAfinada.paso_real hs hn (hc r (by omega)) halfa hbeta
    have hprevR : (D r : ℝ) ≤ OcelotasAfinada.cota alfa (beta - 1) r := by
      exact_mod_cast hprev
    have hmul := mul_le_mul_of_nonneg_left hprevR ha
    simp only [OcelotasAfinada.cota]
    apply Nat.le_floor
    push_cast at hp
    linarith

theorem criba_palabra {n s r R : ℕ} {a b : ℕ → ℕ} {alfa beta : ℝ}
    (hn : 0 < n) (hw : Palabra n a b r) (hs : 0 < s) (hns : n + 1 ≤ s)
    (hr : r ≤ R) (ha : 1 ≤ alfa) (hb : 1 ≤ beta)
    (halfa : log 3 ≤ alfa * log 2) (hbeta : log s ≤ beta * log 2) :
    S (tiempo a b r) n ≤ R + OcelotasAfinada.cota alfa (beta - 1) R := by
  have hcriba := criba_congruencias (descontados a) hs hns rfl
    (by linarith : 0 ≤ alfa) halfa hbeta (congruencias_descontadas hn hw)
  have hmono := OcelotasAfinada.cota_monotona ha (by linarith : 0 ≤ beta - 1) hr
  rw [cuenta_impares hw r le_rfl, cuenta_descontada hw r le_rfl]
  omega

end OcelotasDescuentoRachas

#print axioms OcelotasDescuentoRachas.paso_descontado
#print axioms OcelotasDescuentoRachas.cadena_descontada
#print axioms OcelotasDescuentoRachas.congruencias_descontadas
#print axioms OcelotasDescuentoRachas.criba_congruencias
#print axioms OcelotasDescuentoRachas.criba_palabra
