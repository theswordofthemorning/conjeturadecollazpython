import PerdicesSeparacion
import OcelotasContador

/-! # Perdices: rachas no acotadas entre regresos consecutivos.

Mapa atajo, semilla n y techo 3^c fijos. Todas las cotas orbitales
reciben FugaPura n. El contador canónico se aplica a las entradas
de los pasos del intervalo [u,v), incluida su última racha par truncada.
-/

namespace PerdicesExcursiones

open Ocelotas CasaPlano CasaRetrato PerdicesSeparacion OcelotasTrayectorias
open OcelotasContador

def Bajo (n c j : ℕ) : Prop := 3 ^ S j n ≤ 3 ^ c * 2 ^ j

def Consecutivos (n c u v : ℕ) : Prop :=
  u < v ∧ Bajo n c u ∧ Bajo n c v ∧ ∀ j, u < j → j < v → ¬ Bajo n c j

theorem salida_impar {n c u v : ℕ} (he : Consecutivos n c u v)
    (hd : u + 1 < v) : T^[u] n % 2 = 1 := by
  by_contra hh
  have hp : T^[u] n % 2 = 0 := by omega
  have hs : S (u + 1) n = S u n := by rw [S_add]; simp [S, hp]
  have hu := he.2.1
  have hn := he.2.2.2 (u + 1) (by omega) hd
  apply hn
  unfold Bajo at hu ⊢
  rw [hs, pow_succ]
  exact hu.trans (Nat.mul_le_mul_left _ (by omega : 2 ^ u ≤ 2 ^ u * 2))

theorem llegada_par {n c u v : ℕ} (he : Consecutivos n c u v)
    (hd : u + 1 < v) : T^[v - 1] n % 2 = 0 := by
  by_contra hh
  have hp : T^[v - 1] n % 2 = 1 := by omega
  have hs := S_add (v - 1) 1 n
  rw [show v - 1 + 1 = v by omega] at hs
  simp only [S, hp, Nat.add_zero] at hs
  have hv := he.2.2.1
  have hn := he.2.2.2 (v - 1) (by omega) (by omega)
  unfold Bajo at hv hn
  have hpow : 2 ^ v = 2 ^ (v - 1) * 2 := by
    rw [← pow_succ]; congr 1; omega
  rw [hs, pow_succ, hpow] at hv
  have hpos : 0 < 3 ^ S (v - 1) n := by positivity
  nlinarith

theorem palabra_excursion {n c u v : ℕ} (he : Consecutivos n c u v)
    (hd : u + 1 < v) :
    0 < rachas (T^[u] n) (v - u) ∧ ∃ a b,
      Palabra (T^[u] n) a b (rachas (T^[u] n) (v - u)) ∧
      tiempo a b (rachas (T^[u] n) (v - u)) = v - u := by
  apply extraer_palabra (salida_impar he hd) (by omega)
  rw [← iter_add, show u + (v - u - 1) = v - 1 by have := he.1; omega]
  exact llegada_par he hd

theorem entrada_cuadrado {n c u : ℕ} (h : FugaPura n) (hu : Bajo n c u) :
    (T^[u] n + 1) ^ 2 ≤ 4 * ((3 ^ c) ^ 6 * n ^ 6) * (u + 1) := by
  have hp : 1 ≤ T^[u] n := iter_pos (by have := fuga_pura_dos h; omega) u
  have hs := PerdicesSexta.regreso_sexta h hu
  have ht := PerdicesEstela.S_le_pasos u n
  have h6 : (T^[u] n) ^ 6 ≤ (3 ^ c) ^ 6 * n ^ 6 * (u + 1) :=
    hs.trans (Nat.mul_le_mul_left _ (by omega))
  have h2 : (T^[u] n) ^ 2 ≤ (T^[u] n) ^ 6 :=
    Nat.pow_le_pow_right hp (by decide)
  have hx : T^[u] n ≤ (T^[u] n) ^ 2 := le_self_pow₀ hp (by decide)
  nlinarith

theorem duracion_cuadrado {n c u v H : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v) (hr : rachas (T^[u] n) (v - u) ≤ H) :
    (v - u) ^ 2 ≤
      (4 * (2 * (2 ^ H + c) + 1) ^ 2 * ((3 ^ c) ^ 6 * n ^ 6) + 1) * (u + 1) := by
  by_cases hd : u + 1 < v
  · obtain ⟨_, a, b, hw, hwtime⟩ := palabra_excursion he hd
    have hx : T^[u] n + 1 ≤ 2 ^ (T^[u] n + 1) := Nat.le_of_lt (Nat.lt_two_pow_self)
    have hl := tramo_desde_regreso h he.2.1 hw hx
    rw [hwtime] at hl
    have hh : 2 ^ rachas (T^[u] n) (v - u) - 1 ≤ 2 ^ H :=
      (Nat.sub_le _ _).trans (Nat.pow_le_pow_right (by decide) hr)
    have hm := Nat.mul_le_mul_right (T^[u] n + 1) hh
    have hlen : v - u ≤ (2 * (2 ^ H + c) + 1) * (T^[u] n + 1) := by
      nlinarith
    have hs := Nat.pow_le_pow_left hlen 2
    rw [mul_pow] at hs
    have hb := Nat.mul_le_mul_left ((2 * (2 ^ H + c) + 1) ^ 2) (entrada_cuadrado h he.2.1)
    nlinarith
  · have hv : v - u = 1 := by have := he.1; omega
    rw [hv]
    simp only [one_pow]
    exact Nat.one_le_iff_ne_zero.mpr (by positivity)

/-- Una recurrencia de saltos con cuadrado acotado tiene reloj cuadrático. -/
theorem reloj_cuadratico {t : ℕ → ℕ} (ht : Monotone t) {D : ℕ}
    (hs : ∀ i, (t (i + 1) - t i) ^ 2 ≤ D * (t i + 1)) :
    ∀ i, t i + 1 ≤ (D + t 0 + 1) * (i + 1) ^ 2 := by
  let B := D + t 0 + 1
  have hDB : D ≤ B := by dsimp [B]; omega
  have hB : 0 < B := by dsimp [B]; omega
  intro i
  induction i with
  | zero => simp
  | succ i ih =>
    change t (i + 1) + 1 ≤ B * (i + 1 + 1) ^ 2
    change t i + 1 ≤ B * (i + 1) ^ 2 at ih
    have hmul := Nat.mul_le_mul hDB ih
    have hg : (t (i + 1) - t i) ^ 2 ≤ (B * (i + 1)) ^ 2 := by
      have hh := hs i
      nlinarith
    have hd : t (i + 1) - t i ≤ B * (i + 1) :=
      (Nat.pow_le_pow_iff_left (by decide : 2 ≠ 0)).1 hg
    have hm := ht (show i ≤ i + 1 by omega)
    have he : t (i + 1) = t i + (t (i + 1) - t i) := by omega
    nlinarith

theorem rachas_no_acotadas {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (he : ∀ i, Consecutivos n c (t i) (t (i + 1))) (H : ℕ) :
    ∃ i, H < rachas (T^[t i] n) (t (i + 1) - t i) := by
  by_contra hh
  have hr : ∀ i, rachas (T^[t i] n) (t (i + 1) - t i) ≤ H := by simpa using hh
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have hs := reloj_cuadratico ht.monotone (fun i => duracion_cuadrado h (he i) (hr i))
  apply reloj_sextico_imposible h ht (fun i => (he i).2.1)
    (4 * (2 * (2 ^ H + c) + 1) ^ 2 * ((3 ^ c) ^ 6 * n ^ 6) + 1 + t 0 + 1)
  intro i
  exact (hs i).trans (Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by omega) (by decide)))

theorem rachas_grandes_tarde {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (he : ∀ i, Consecutivos n c (t i) (t (i + 1))) (H a : ℕ) :
    ∃ i, a ≤ i ∧ H < rachas (T^[t i] n) (t (i + 1) - t i) := by
  obtain ⟨i, hi⟩ := rachas_no_acotadas h (t := fun i => t (a + i))
    (fun i => by simpa [Nat.add_assoc] using he (a + i)) H
  exact ⟨a + i, by omega, by simpa [Nat.add_assoc] using hi⟩

def InfinitosRegresos (n c : ℕ) : Prop := ∀ U, ∃ j, U < j ∧ Bajo n c j

theorem siguiente_regreso {n c u : ℕ} (hi : InfinitosRegresos n c)
    (hu : Bajo n c u) : ∃ v, Consecutivos n c u v := by
  classical
  let v := Nat.find (hi u)
  have hv := Nat.find_spec (hi u)
  refine ⟨v, hv.1, hu, hv.2, ?_⟩
  intro j huj hjv hj
  exact Nat.find_min (hi u) hjv ⟨huj, hj⟩

/-- Enunciado orbital sin una enumeración de regresos como hipótesis. -/
theorem infinitos_exigen_rachas {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (H U : ℕ) :
    ∃ u v, U < u ∧ Consecutivos n c u v ∧ H < rachas (T^[u] n) (v - u) := by
  classical
  have hs : ∀ u, ∃ v, u < v ∧ Bajo n c v ∧
      ∀ j, u < j → j < v → ¬ Bajo n c j := by
    intro u
    refine ⟨Nat.find (hi u), (Nat.find_spec (hi u)).1, (Nat.find_spec (hi u)).2, ?_⟩
    intro j huj hjv hj
    exact Nat.find_min (hi u) hjv ⟨huj, hj⟩
  choose siguiente hsig using hs
  obtain ⟨u0, hU, hu0⟩ := hi U
  let t : ℕ → ℕ := fun i => siguiente^[i] u0
  have hrec (i : ℕ) : t (i + 1) = siguiente (t i) := Function.iterate_succ_apply' _ _ _
  have hb : ∀ i, Bajo n c (t i) := by
    intro i
    cases i with
    | zero => exact hu0
    | succ i => rw [hrec]; exact (hsig (t i)).2.1
  have he : ∀ i, Consecutivos n c (t i) (t (i + 1)) := by
    intro i
    rw [hrec]
    exact ⟨(hsig (t i)).1, hb i, (hsig (t i)).2⟩
  obtain ⟨i, hr⟩ := rachas_no_acotadas h he H
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have h0 : u0 ≤ t i := ht.monotone (Nat.zero_le i)
  exact ⟨t i, t (i + 1), by omega, he i, hr⟩

end PerdicesExcursiones

#print axioms PerdicesExcursiones.salida_impar
#print axioms PerdicesExcursiones.llegada_par
#print axioms PerdicesExcursiones.palabra_excursion
#print axioms PerdicesExcursiones.entrada_cuadrado
#print axioms PerdicesExcursiones.duracion_cuadrado
#print axioms PerdicesExcursiones.reloj_cuadratico
#print axioms PerdicesExcursiones.rachas_no_acotadas
#print axioms PerdicesExcursiones.rachas_grandes_tarde
#print axioms PerdicesExcursiones.siguiente_regreso
#print axioms PerdicesExcursiones.infinitos_exigen_rachas
