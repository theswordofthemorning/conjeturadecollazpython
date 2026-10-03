import OcelotasContador

/-! # Ocelotas: cortar las rachas después de una entrada par

La criba se puede reiniciar con el valor actual de la órbita. El contador
se suma sin fusionar rachas cuando el prefijo es vacío o termina en par.
-/

namespace OcelotasPrefijos

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasContador

theorem rachas_monotonas (n : ℕ) : Monotone (rachas n) := by
  apply monotone_nat_of_le_succ
  intro i
  simp only [rachas]
  omega

theorem rachas_add_corte {n i : ℕ}
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (j : ℕ) :
    rachas n (i + j) = rachas n i + rachas (T^[i] n) j := by
  induction j with
  | zero => simp [rachas]
  | succ j ih =>
    have hcond :
        (T^[i + j] n % 2 = 1 ∧ (i + j = 0 ∨ T^[i + j - 1] n % 2 = 0)) ↔
        (T^[j] (T^[i] n) % 2 = 1 ∧ (j = 0 ∨ T^[j - 1] (T^[i] n) % 2 = 0)) := by
      by_cases hj : j = 0
      · subst j
        simp only [Nat.add_zero, Function.iterate_zero, id_eq, true_or, and_true]
        simp [hcorte]
      · have hd : i + j - 1 = i + (j - 1) := by omega
        rw [iter_add, hd, iter_add]
        simp [hj]
    change rachas n ((i + j) + 1) = rachas n i + rachas (T^[i] n) (j + 1)
    rw [rachas, ih, rachas]
    simp only [hcond, Nat.add_assoc]

/-- La criba natural también admite ceros iniciales y una palabra vacía. -/
theorem criba_contador {k m : ℕ} : ∀ n,
    n + 1 < 2 ^ m → (k = 0 ∨ T^[k - 1] n % 2 = 0) →
    S k n ≤ cota (rachas n k) m := by
  induction k with
  | zero => intro n hn hf; simp [S, rachas, cota]
  | succ k ih =>
    intro n hn hf
    have hfin : T^[k] n % 2 = 0 := by simpa using hf
    by_cases hpar : n % 2 = 0
    · have hcut := rachas_add_corte (n := n) (i := 1) (Or.inr (by simpa using hpar)) k
      have hr : rachas n (k + 1) = rachas (T n) k := by
        simpa [Nat.add_comm, rachas, hpar] using hcut
      have hvalor : T n ≤ n := by
        simp only [T, hpar, if_pos]
        exact Nat.div_le_self _ _
      have hf' : k = 0 ∨ T^[k - 1] (T n) % 2 = 0 := by
        by_cases hk : k = 0
        · exact Or.inl hk
        · right
          have he : T^[k - 1] (T n) = T^[k] n := by
            have h := iter_add 1 (k - 1) n
            simpa [show 1 + (k - 1) = k by omega] using h.symm
          rw [he]
          exact hfin
      have h := ih (T n) (by omega) hf'
      simpa only [S, hpar, Nat.zero_add, hr] using h
    · obtain ⟨hpos, a, b, hw, he⟩ := extraer_palabra (by omega : n % 2 = 1)
        (by omega : 0 < k + 1) (by simpa using hfin)
      have h := criba_desde_trayectoria hw hn
      rwa [he] at h

theorem criba_despues_corte {n k i R m : ℕ}
    (hk : PrimerCruce n k) (hi : i < k)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0)
    (hr : rachas n k ≤ R) (hm : 1 ≤ m) (hvalor : T^[i] n + 1 < 2 ^ m) :
    S k n ≤ S i n + cota (R - rachas n i) m := by
  have ht : i + (k - i) = k := by omega
  have hs := S_add i (k - i) n
  rw [ht] at hs
  have hrpart := rachas_add_corte hcorte (k - i)
  rw [ht] at hrpart
  have hrest : rachas (T^[i] n) (k - i) ≤ R - rachas n i := by omega
  have hfin : T^[k - i - 1] (T^[i] n) % 2 = 0 := by
    rw [← iter_add, show i + (k - i - 1) = k - 1 by omega]
    exact cruce_termina_par hk
  have hc := criba_contador (T^[i] n) hvalor (Or.inr hfin)
  have hmono := cota_monotona hm hrest
  omega

end OcelotasPrefijos

#print axioms OcelotasPrefijos.rachas_monotonas
#print axioms OcelotasPrefijos.rachas_add_corte
#print axioms OcelotasPrefijos.criba_contador
#print axioms OcelotasPrefijos.criba_despues_corte
