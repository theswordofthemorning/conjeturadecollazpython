import PerdicesAporte

/-! # Perdices: aporte, levantamiento de residuos y tamaño de la semilla local.

La parte algebraica declara sus identidades afines como hipótesis. La parte
orbital deduce de FugaPura e infinitos regresos excursiones de duración
mayor que cualquier múltiplo fijo de la quinta potencia de la entrada.
-/

namespace PerdicesSemilla

open Ocelotas CasaPlano CasaRetrato OcelotasTrayectorias PerdicesTamano PerdicesExcursiones
open PerdicesRitmo PerdicesSeparacion

theorem composicion_entera {M A B r q : ℤ} (h : M * q = A * r + B)
    (D E t : ℤ) :
    D * A * (r + M * t) + (D * B + M * E) =
      M * (D * (q + A * t) + E) := by
  linear_combination -D * h

theorem aporte_composicion {A D : ℚ} (hA : A ≠ 0) (hD : D ≠ 0)
    (M B E : ℚ) :
    (D * B + M * E) / (D * A) - B / A = M * E / (A * D) := by
  field_simp
  ring

theorem carga_composicion {A D : ℚ} (hA : A ≠ 0) (hD : D ≠ 0)
    (M B E N l : ℚ) :
    (D * B + M * E + l * M * N) / (D * A) - (B + l * M) / A =
      M * (E + l * (N - D)) / (A * D) := by
  field_simp
  ring

theorem criterio_levantamiento {M A B r q : ℤ} (hM : M ≠ 0)
    (h : M * q = A * r + B) (N D E t : ℤ) :
    M * N ∣ D * A * (r + M * t) + (D * B + M * E) ↔
      N ∣ D * (q + A * t) + E := by
  rw [composicion_entera h]
  exact mul_dvd_mul_iff_left hM

theorem intervalo_levantamiento {M N r t : ℕ}
    (hr : r < M) (ht : t < N) : r + M * t < M * N := by
  have hm := Nat.mul_le_mul_left M (show t + 1 ≤ N by omega)
  nlinarith only [hr, hm]

theorem levantamiento_cero {M r t : ℕ} (hM : 0 < M) :
    r + M * t = r ↔ t = 0 := by
  constructor
  · intro h
    have hz : M * t = 0 := by omega
    exact (Nat.mul_eq_zero.mp hz).resolve_left (by omega)
  · intro h; simp [h]

theorem levantamiento_supera_semilla {M r t n : ℕ} (hn : n < M)
    (ht : 0 < t) : n < r + M * t := by
  have hm := Nat.le_mul_of_pos_right M ht
  omega

theorem cota_quinta_sexta {n c u v H : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v)
    (hd : v - u ≤ H * (T^[u] n + 1) ^ 5) :
    (v - u) ^ 6 ≤
      (H ^ 6 * (64 * ((3 ^ c) ^ 6 * n ^ 6)) ^ 5) * (u + 1) ^ 5 := by
  have hx := entrada_sexta h he.2.1
  calc
    _ ≤ (H * (T^[u] n + 1) ^ 5) ^ 6 := Nat.pow_le_pow_left hd 6
    _ = H ^ 6 * ((T^[u] n + 1) ^ 6) ^ 5 := by ring
    _ ≤ H ^ 6 * (64 * ((3 ^ c) ^ 6 * n ^ 6) * (u + 1)) ^ 5 :=
      Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hx 5)
    _ = _ := by ring

theorem infinitos_exigen_quinta {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (H U : ℕ) :
    ∃ u v, U < u ∧ Consecutivos n c u v ∧
      H * (T^[u] n + 1) ^ 5 < v - u := by
  obtain ⟨t, hU, he⟩ := enumerar_regresos hi U
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have hx : ∃ i, H * (T^[t i] n + 1) ^ 5 < t (i + 1) - t i := by
    by_contra hh
    have hd : ∀ i, t (i + 1) - t i ≤ H * (T^[t i] n + 1) ^ 5 := by
      simpa using hh
    have hclock := reloj_sextico ht.monotone (fun i => cota_quinta_sexta h (he i) (hd i))
    exact reloj_sextico_imposible h ht (fun i => (he i).2.1)
      (H ^ 6 * (64 * ((3 ^ c) ^ 6 * n ^ 6)) ^ 5 + t 0 + 1) hclock
  obtain ⟨i, hir⟩ := hx
  have h0 := ht.monotone (Nat.zero_le i)
  exact ⟨t i, t (i + 1), by omega, he i, hir⟩

theorem cota_quinta_excluye_regresos {n c H U : ℕ} (h : FugaPura n)
    (hc : ∀ u v, U < u → Consecutivos n c u v →
      v - u ≤ H * (T^[u] n + 1) ^ 5) : ¬ InfinitosRegresos n c := by
  intro hi
  obtain ⟨u, v, hu, he, hd⟩ := infinitos_exigen_quinta h hi H U
  exact (not_lt_of_ge (hc u v hu he)) hd

theorem entrada_menor_modulo {x d H : ℕ}
    (hd : (H + 1) * (x + 1) ^ 5 < d) : x < 2 ^ d := by
  have hx : x + 1 ≤ (x + 1) ^ 5 := by
    simpa using Nat.pow_le_pow_right (by omega : 1 ≤ x + 1) (by decide : 1 ≤ 5)
  have hm := Nat.le_mul_of_pos_left ((x + 1) ^ 5) (by omega : 0 < H + 1)
  have hd2 : d < 2 ^ d := Nat.lt_two_pow_self
  omega

theorem infinitos_semilla_corta {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (H U : ℕ) :
    ∃ u v, U < u ∧ Consecutivos n c u v ∧
      (H + 1) * (T^[u] n + 1) ^ 5 < v - u ∧
      T^[u] n < 2 ^ (v - u) ∧ T^[u] n % 2 ^ (v - u) = T^[u] n := by
  obtain ⟨u, v, hu, he, hd⟩ := infinitos_exigen_quinta h hi (H + 1) U
  have hm := entrada_menor_modulo hd
  exact ⟨u, v, hu, he, hd, hm, Nat.mod_eq_of_lt hm⟩

theorem residuo_unico {M x r : ℕ} (hx : x < M) (hr : r < M)
    (he : x % M = r % M) : x = r := by
  simpa [Nat.mod_eq_of_lt hx, Nat.mod_eq_of_lt hr] using he

theorem familia_aporte_entrada_grande {k b m x : ℕ} (hk : 3 ≤ k)
    (hm : 1 ≤ m) (hb : b ≤ k)
    (hx : 11 * x + 19 = 729 * 16 ^ (k - 2) * m) :
    4 * k + b - 8 < x := by
  have hp : k - 1 ≤ 16 ^ (k - 2) := by
    have hh : k - 2 < 2 ^ (k - 2) := Nat.lt_two_pow_self
    have hg := Nat.pow_le_pow_left (by decide : 2 ≤ 16) (k - 2)
    omega
  have hm' := Nat.le_mul_of_pos_right (16 ^ (k - 2)) (by omega : 0 < m)
  have hl : 729 * (k - 1) ≤ 11 * x + 19 := by
    calc
      _ ≤ 729 * (16 ^ (k - 2) * m) := Nat.mul_le_mul_left _ (hp.trans hm')
      _ = _ := by rw [← mul_assoc, ← hx]
  omega

end PerdicesSemilla

#print axioms PerdicesSemilla.composicion_entera
#print axioms PerdicesSemilla.aporte_composicion
#print axioms PerdicesSemilla.carga_composicion
#print axioms PerdicesSemilla.criterio_levantamiento
#print axioms PerdicesSemilla.intervalo_levantamiento
#print axioms PerdicesSemilla.levantamiento_cero
#print axioms PerdicesSemilla.levantamiento_supera_semilla
#print axioms PerdicesSemilla.cota_quinta_sexta
#print axioms PerdicesSemilla.infinitos_exigen_quinta
#print axioms PerdicesSemilla.cota_quinta_excluye_regresos
#print axioms PerdicesSemilla.entrada_menor_modulo
#print axioms PerdicesSemilla.infinitos_semilla_corta
#print axioms PerdicesSemilla.residuo_unico
#print axioms PerdicesSemilla.familia_aporte_entrada_grande
