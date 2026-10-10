import Mathlib.Data.Int.DivMod
import Mathlib.Data.Nat.Find
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic.Linarith

/-! # Jinetas: restricciones de todos los prefijos

La identidad orbital y la clase de paridades se explican en PREFIJOS.md.
Aquí se certifican sus consecuencias algebraicas, la redundancia anterior
al primer cruce y un ciclo de control en el mapa vecino 5n+1.
-/

namespace JinetasPrefijos

def sobrevive (D B : ℕ → ℤ) (L : ℕ) (n : ℤ) : Prop :=
  ∀ j, 1 ≤ j → j ≤ L → D j * n ≤ B j

theorem identidad_margen {M A B n x : ℤ} (hM : 0 < M)
    (h : M * x = A * n + B) : n ≤ x ↔ (M - A) * n ≤ B := by
  constructor <;> intro hn <;> nlinarith

theorem cota_entera {D B n : ℤ} (hD : 0 < D) :
    D * n ≤ B ↔ n ≤ B / D := by
  rw [Int.le_ediv_iff_mul_le hD, mul_comm]

theorem sin_cruce {D B n : ℤ} (hD : D ≤ 0) (hB : 0 ≤ B) (hn : 0 ≤ n) :
    D * n ≤ B := by
  nlinarith

theorem herencia {D B : ℕ → ℤ} {K L : ℕ} {n : ℤ}
    (hKL : K ≤ L) (h : sobrevive D B L n) : sobrevive D B K n := by
  intro j hj hjK
  exact h j hj (le_trans hjK hKL)

/-- En el primer cruce, todos los límites anteriores son automáticos. -/
theorem primer_cruce {D B : ℕ → ℤ} {L : ℕ} {n : ℤ}
    (hL : 1 ≤ L) (hn : 0 ≤ n)
    (hD : ∀ j, 1 ≤ j → j < L → D j ≤ 0)
    (hB : ∀ j, 1 ≤ j → j < L → 0 ≤ B j) :
    sobrevive D B L n ↔ D L * n ≤ B L := by
  constructor
  · intro h
    exact h L hL (le_refl L)
  · intro h j hj hjL
    by_cases heq : j = L
    · simpa [heq] using h
    · have hlt : j < L := by omega
      exact sin_cruce (hD j hj hlt) (hB j hj hlt) hn

theorem interseccion_cotas (n H C : ℤ) :
    (n ≤ H ∧ n ≤ C) ↔ n ≤ min H C := by
  exact le_min_iff.symm

/-- Una subclase no puede tener un mínimo menor que el de su clase madre. -/
theorem minimo_anidado {S R : ℤ → Prop} {m m' : ℤ}
    (hsub : ∀ n, S n → R n) (hm : ∀ n, R n → m ≤ n) (hm' : S m') :
    m ≤ m' := hm m' (hsub m' hm')

theorem holgura_no_crece {H H' m m' : ℤ} (hH : H' ≤ H) (hm : m ≤ m') :
    H' - m' ≤ H - m := by omega

theorem poda_persistente {H H' m m' : ℤ} (hH : H' ≤ H) (hm : m ≤ m')
    (hvacio : H < m) : H' < m' := by omega

/-- Basta probar el menor representante de una clase en un límite positivo. -/
theorem minimo_decide {S : ℤ → Prop} {m D B : ℤ}
    (hm : S m) (hmin : ∀ n, S n → m ≤ n) (hD : 0 < D) :
    (∃ n, S n ∧ D * n ≤ B) ↔ D * m ≤ B := by
  constructor
  · rintro ⟨n, hn, h⟩
    have := hmin n hn
    nlinarith
  · intro h
    exact ⟨m, hm, h⟩

/-- Una rama anidada con mínimos acotados tiene una semilla común a todos
    los niveles. La unicidad por módulos crecientes se justifica en la nota. -/
theorem rama_acotada_iff_semilla_fija (C : ℕ → ℕ → Prop) (m : ℕ → ℕ)
    (hmem : ∀ L, C L (m L)) (hmin : ∀ L n, C L n → m L ≤ n)
    (hsub : ∀ K L, K ≤ L → ∀ n, C L n → C K n) :
    (∃ H, ∀ L, m L ≤ H) ↔ ∃ n, ∀ L, C L n := by
  classical
  constructor
  · rintro ⟨H, hb⟩
    let G := Nat.findGreatest (fun v => ∃ L, m L = v) H
    have hG : ∃ K, m K = G :=
      Nat.findGreatest_spec (P := fun v => ∃ L, m L = v) (hb 0) ⟨0, rfl⟩
    obtain ⟨K, hK⟩ := hG
    have hu (L : ℕ) : m L ≤ G :=
      Nat.le_findGreatest (P := fun v => ∃ K, m K = v) (hb L) ⟨L, rfl⟩
    refine ⟨G, ?_⟩
    intro L
    have hge := hmin K (m (max K L))
      (hsub K (max K L) (le_max_left K L) _ (hmem (max K L)))
    have hle := hu (max K L)
    have heq : m (max K L) = G := by omega
    exact hsub L (max K L) (le_max_right K L) G (heq ▸ hmem (max K L))
  · rintro ⟨n, hn⟩
    exact ⟨n, fun L => hmin L n (hn L)⟩

def paso (a n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (a * n + 1) / 2

theorem siete_paradojico_pero_descendio :
    (paso 3)^[7] 7 = 5 ∧ (paso 3)^[8] 7 = 8 ∧
    3 ^ 5 < (2 : ℕ) ^ 8 ∧ (347 : ℤ) / 13 = 26 ∧ (73 : ℤ) / 47 = 1 := by
  decide

theorem vecino_tabla :
    (paso 5)^[7] 13 = 13 ∧ ∀ r : Fin 7, 13 ≤ (paso 5)^[r.val] 13 := by
  decide

theorem vecino_vueltas (q : ℕ) : (paso 5)^[7 * q] 13 = 13 := by
  induction q with
  | zero => rfl
  | succ q ih =>
    rw [Nat.mul_succ, Function.iterate_add_apply, vecino_tabla.1, ih]

theorem vecino_no_baja (k : ℕ) : 13 ≤ (paso 5)^[k] 13 := by
  conv_rhs => rw [← Nat.mod_add_div k 7]
  rw [Function.iterate_add_apply, vecino_vueltas]
  exact vecino_tabla.2 ⟨k % 7, Nat.mod_lt k (by decide)⟩

end JinetasPrefijos

#print axioms JinetasPrefijos.identidad_margen
#print axioms JinetasPrefijos.cota_entera
#print axioms JinetasPrefijos.sin_cruce
#print axioms JinetasPrefijos.herencia
#print axioms JinetasPrefijos.primer_cruce
#print axioms JinetasPrefijos.interseccion_cotas
#print axioms JinetasPrefijos.minimo_anidado
#print axioms JinetasPrefijos.holgura_no_crece
#print axioms JinetasPrefijos.poda_persistente
#print axioms JinetasPrefijos.minimo_decide
#print axioms JinetasPrefijos.rama_acotada_iff_semilla_fija
#print axioms JinetasPrefijos.siete_paradojico_pero_descendio
#print axioms JinetasPrefijos.vecino_tabla
#print axioms JinetasPrefijos.vecino_vueltas
#print axioms JinetasPrefijos.vecino_no_baja
