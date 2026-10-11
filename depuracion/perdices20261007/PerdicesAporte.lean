import PerdicesExcepciones

/-! # Perdices: aporte normalizado y balance firmado de las excepciones.

La carga con desplazamiento cinco neutraliza exactamente el bloque 110.
Las identidades son orbitales, sin hipótesis probabilísticas ni FugaPura.
Los ejemplos finales certifican sólo condiciones finitas de excursión.
-/

namespace PerdicesAporte

open Ocelotas OcelotasTrayectorias PerdicesTamano PerdicesExcursiones
open PerdicesBalance
open scoped BigOperators

noncomputable def carga (l : ℝ) (n k : ℕ) : ℝ :=
  inverso n k * ((T^[k] n : ℝ) + l)

noncomputable def correccion (l : ℝ) (a b : ℕ) : ℝ :=
  (3 ^ a - 2 ^ a + l * (2 ^ (a + b) - 3 ^ a)) / 3 ^ a

theorem inverso_traslado (n u t : ℕ) :
    inverso n (u + t) = inverso n u * inverso (T^[u] n) t := by
  unfold inverso
  rw [S_add, pow_add, pow_add]
  ring

theorem carga_traslado (l : ℝ) (n u t : ℕ) :
    carga l n (u + t) = inverso n u * carga l (T^[u] n) t := by
  unfold carga
  rw [inverso_traslado, iter_add]
  ring

theorem inverso_bloque {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) :
    inverso n (tiempo a b (i + 1)) = inverso n (tiempo a b i) *
      (2 ^ (a i + b i) / 3 ^ a i) := by
  unfold inverso
  rw [cuenta_impares hw (i + 1) (by omega), cuenta_impares hw i (by omega), acumulados]
  simp only [tiempo, pow_add]
  ring

theorem algebra_carga {x y I l A M Q : ℝ} (hA : A ≠ 0)
    (ha : M * y + Q = A * (x + 1)) :
    I * (M / A) * (y + l) - I * (x + l) =
      I * ((A - Q + l * (M - A)) / A) := by
  field_simp
  have hh := congrArg (fun z : ℝ => I * z) ha
  nlinarith only [hh]

theorem carga_bloque_local {n r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hi : i < r) (l : ℝ) :
    carga l n (tiempo a b (i + 1)) - carga l n (tiempo a b i) =
      inverso n (tiempo a b i) * correccion l (a i) (b i) := by
  have hb := balance_bloque hw hi
  have hn : 2 ^ (a i + b i) * T^[tiempo a b (i + 1)] n + 2 ^ a i =
      3 ^ a i * (T^[tiempo a b i] n + 1) := by nlinarith only [hb]
  have hr : (2 : ℝ) ^ (a i + b i) * (T^[tiempo a b (i + 1)] n : ℝ) + 2 ^ a i =
      3 ^ a i * ((T^[tiempo a b i] n : ℝ) + 1) := by exact_mod_cast hn
  unfold carga correccion
  rw [inverso_bloque hw hi]
  exact algebra_carga (by positivity) hr

theorem carga_bloque {n u r i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra (T^[u] n) a b r) (hi : i < r) (l : ℝ) :
    carga l n (u + tiempo a b (i + 1)) - carga l n (u + tiempo a b i) =
      inverso n (u + tiempo a b i) * correccion l (a i) (b i) := by
  rw [carga_traslado, carga_traslado, ← mul_sub, carga_bloque_local hw hi,
    inverso_traslado]
  ring

theorem correccion_110 (l : ℝ) : correccion l 2 1 = (5 - l) / 9 := by
  unfold correccion
  norm_num
  ring

theorem desplazamiento_unico (l : ℝ) : correccion l 2 1 = 0 ↔ l = 5 := by
  rw [correccion_110]
  constructor <;> intro h <;> linarith

theorem correccion_cinco (a b : ℕ) :
    correccion 5 a b = (2 ^ a * (5 * 2 ^ b - 1) - 4 * 3 ^ a) / 3 ^ a := by
  unfold correccion
  rw [pow_add]
  ring

theorem carga_suma {n u r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra (T^[u] n) a b r) (l : ℝ) :
    carga l n (u + tiempo a b r) - carga l n u =
      ∑ i ∈ Finset.range r, inverso n (u + tiempo a b i) * correccion l (a i) (b i) := by
  have hg : ∀ k ≤ r, carga l n (u + tiempo a b k) - carga l n u =
      ∑ i ∈ Finset.range k, inverso n (u + tiempo a b i) * correccion l (a i) (b i) := by
    intro k
    induction k with
    | zero => intro _; simp [tiempo]
    | succ k ih =>
      intro hk
      rw [Finset.sum_range_succ]
      have hh := carga_bloque hw (by omega : k < r) l
      have hprev := ih (by omega)
      linarith
  exact hg r le_rfl

theorem suma_excepciones {n u r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra (T^[u] n) a b r) :
    carga 5 n (u + tiempo a b r) - carga 5 n u =
      ∑ i ∈ Finset.range r, if a i = 2 ∧ b i = 1 then 0 else
        inverso n (u + tiempo a b i) * correccion 5 (a i) (b i) := by
  rw [carga_suma hw]
  apply Finset.sum_congr rfl
  intro i _
  split_ifs with hg
  · rw [hg.1, hg.2, correccion_110]; norm_num
  · rfl

theorem carga_cadena {n u r j k : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra (T^[u] n) a b r) (hk : j + k ≤ r)
    (hg : ∀ i < k, a (j + i) = 2 ∧ b (j + i) = 1) :
    carga 5 n (u + tiempo a b (j + k)) = carga 5 n (u + tiempo a b j) := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hprev := ih (by omega) (fun i hi => hg i (by omega))
    have hh := carga_bloque hw (by omega : j + k < r) (5 : ℝ)
    rw [(hg k (by omega)).1, (hg k (by omega)).2, correccion_110] at hh
    norm_num at hh
    rw [Nat.add_succ]
    linarith

theorem aporte_cadena {n u r j k : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra (T^[u] n) a b r) (hk : j + k ≤ r)
    (hg : ∀ i < k, a (j + i) = 2 ∧ b (j + i) = 1) :
    normalizado n (u + tiempo a b (j + k)) - normalizado n (u + tiempo a b j) =
      5 * (inverso n (u + tiempo a b j) - inverso n (u + tiempo a b (j + k))) ∧
    normalizado n (u + tiempo a b (j + k)) - normalizado n (u + tiempo a b j) <
      5 * inverso n (u + tiempo a b j) := by
  have hh := carga_cadena hw hk hg
  have hp := inverso_pos n (u + tiempo a b (j + k))
  unfold carga at hh
  unfold normalizado
  constructor <;> nlinarith only [hh, hp]

theorem ejemplos_consecutivos :
    Consecutivos 7 1 2 4 ∧ Consecutivos 15 1 2 5 ∧ Consecutivos 63 1 2 8 := by
  have probar : ∀ n v, (n = 7 ∧ v = 4) ∨ (n = 15 ∧ v = 5) ∨ (n = 63 ∧ v = 8) →
      Consecutivos n 1 2 v := by
    intro n v h
    rcases h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    all_goals
      refine ⟨by decide, ?_, ?_, ?_⟩
      · norm_num [Bajo, S, T, Function.iterate_succ_apply']
      · norm_num [Bajo, S, T, Function.iterate_succ_apply']
      · intro j hj hv
        have hcasos : j = 3 ∨ j = 4 ∨ j = 5 ∨ j = 6 ∨ j = 7 := by omega
        rcases hcasos with rfl | rfl | rfl | rfl | rfl
        all_goals norm_num [Bajo, S, T, Function.iterate_succ_apply'] at *
  exact ⟨probar 7 4 (Or.inl ⟨rfl, rfl⟩), probar 15 5 (Or.inr (Or.inl ⟨rfl, rfl⟩)),
    probar 63 8 (Or.inr (Or.inr ⟨rfl, rfl⟩))⟩

theorem ejemplos_signos :
    carga 5 7 4 - carga 5 7 2 = 8 / 9 ∧
    carga 5 15 5 - carga 5 15 2 = 0 ∧
    carga 5 63 8 - carga 5 63 2 = -80 / 729 := by
  norm_num [carga, inverso, S, T, Function.iterate_succ_apply']

end PerdicesAporte

#print axioms PerdicesAporte.inverso_traslado
#print axioms PerdicesAporte.carga_traslado
#print axioms PerdicesAporte.inverso_bloque
#print axioms PerdicesAporte.algebra_carga
#print axioms PerdicesAporte.carga_bloque_local
#print axioms PerdicesAporte.carga_bloque
#print axioms PerdicesAporte.correccion_110
#print axioms PerdicesAporte.desplazamiento_unico
#print axioms PerdicesAporte.correccion_cinco
#print axioms PerdicesAporte.carga_suma
#print axioms PerdicesAporte.suma_excepciones
#print axioms PerdicesAporte.carga_cadena
#print axioms PerdicesAporte.aporte_cadena
#print axioms PerdicesAporte.ejemplos_consecutivos
#print axioms PerdicesAporte.ejemplos_signos
