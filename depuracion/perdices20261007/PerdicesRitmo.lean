import PerdicesExcursiones

/-! # Perdices: una tasa necesaria para las rachas entre regresos.

El factor 8/5 sustituye a 2 usando 3^5 ≤ 2^8. Las desigualdades
se escriben con naturales, sin redondeos ni logaritmos formales.
-/

namespace PerdicesRitmo

open Ocelotas CasaPlano CasaRetrato OcelotasTrayectorias OcelotasContador
open PerdicesSeparacion PerdicesExcursiones

theorem paso_ocho_quintos {x r L i : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hx : x + 1 ≤ 2 ^ L) (hi : i < r) :
    5 * acumulados a (i + 1) ≤ 5 * L + 8 * acumulados a i := by
  have hc := Nat.pow_le_pow_left (congruencias_acumuladas hw i hi) 5
  have htres : (3 ^ acumulados a i) ^ 5 ≤ 2 ^ (8 * acumulados a i) := by
    rw [← pow_mul, Nat.mul_comm (acumulados a i) 5, pow_mul]
    simpa only [← pow_mul] using
      Nat.pow_le_pow_left (by decide : 3 ^ 5 ≤ 2 ^ 8) (acumulados a i)
  have hh : 2 ^ (5 * acumulados a (i + 1)) ≤
      2 ^ (5 * L + 8 * acumulados a i) := by
    calc
      _ = (2 ^ acumulados a (i + 1)) ^ 5 := by rw [← pow_mul]; congr 1; omega
      _ ≤ ((x + 1) * 3 ^ acumulados a i) ^ 5 := hc
      _ ≤ (2 ^ L) ^ 5 * 2 ^ (8 * acumulados a i) := by
        rw [mul_pow]
        exact Nat.mul_le_mul (Nat.pow_le_pow_left hx 5) htres
      _ = _ := by rw [← pow_mul, ← pow_add]; congr 1; omega
  exact (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 hh

theorem impares_ocho_quintos {x r L : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hx : x + 1 ≤ 2 ^ L) :
    3 * 5 ^ r * acumulados a r + 5 * 5 ^ r * L ≤ 5 * 8 ^ r * L := by
  have hg : ∀ i ≤ r,
      3 * 5 ^ i * acumulados a i + 5 * 5 ^ i * L ≤ 5 * 8 ^ i * L := by
    intro i
    induction i with
    | zero => intro _; simp [acumulados]
    | succ i ih =>
      intro hi
      have h1 := Nat.mul_le_mul_left 8 (ih (by omega))
      have h2 := Nat.mul_le_mul_left (3 * 5 ^ i) (paso_ocho_quintos hw hx (by omega : i < r))
      simp only [pow_succ]
      nlinarith
  exact hg r le_rfl

theorem duracion_ocho_quintos {x r L c : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hx : x + 1 ≤ 2 ^ L)
    (hp : 2 ^ tiempo a b r ≤ 3 ^ c * 3 ^ S (tiempo a b r) x) :
    5 ^ r * tiempo a b r ≤ (3 * L + 2 * c) * 8 ^ r := by
  have hi := cuenta_impares hw r le_rfl
  have hpow : 2 ^ (5 * tiempo a b r) ≤ 2 ^ (8 * (c + acumulados a r)) := by
    calc
      _ = (2 ^ tiempo a b r) ^ 5 := by rw [← pow_mul]; congr 1; omega
      _ ≤ (3 ^ c * 3 ^ S (tiempo a b r) x) ^ 5 := Nat.pow_le_pow_left hp 5
      _ = (3 ^ 5) ^ (c + acumulados a r) := by rw [hi, ← pow_add, ← pow_mul, ← pow_mul]; congr 1; omega
      _ ≤ (2 ^ 8) ^ (c + acumulados a r) := Nat.pow_le_pow_left (by decide) _
      _ = _ := (pow_mul _ _ _).symm
  have hd := (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 hpow
  have hh := impares_ocho_quintos hw hx
  have h5 : 5 ^ r ≤ 8 ^ r := Nat.pow_le_pow_left (by decide) r
  have h1 := Nat.mul_le_mul_left (3 * 5 ^ r) hd
  have h2 := Nat.mul_le_mul_left 8 hh
  have h3 := Nat.mul_le_mul_left (24 * c) h5
  have h4 := Nat.zero_le ((5 * L + 6 * c) * 8 ^ r + 40 * 5 ^ r * L)
  nlinarith only [h1, h2, h3, h4]

theorem duracion_orbital {n c u v : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v) :
    5 ^ rachas (T^[u] n) (v - u) * (v - u) ≤
      (3 + 2 * c) * 8 ^ rachas (T^[u] n) (v - u) * (T^[u] n + 1) := by
  by_cases hd : u + 1 < v
  · obtain ⟨_, a, b, hw, htime⟩ := palabra_excursion he hd
    have hh := duracion_ocho_quintos hw (Nat.le_of_lt (Nat.lt_two_pow_self))
      (PerdicesEstela.casi_fuga_de_bajo h he.2.1 _)
    rw [htime] at hh
    calc
      _ ≤ (3 * (T^[u] n + 1) + 2 * c) * 8 ^ rachas (T^[u] n) (v - u) := hh
      _ ≤ ((3 + 2 * c) * (T^[u] n + 1)) * 8 ^ rachas (T^[u] n) (v - u) :=
        Nat.mul_le_mul_right _ (by nlinarith)
      _ = _ := by ring
  · have hv : v - u = 1 := by have := he.1; omega
    rw [hv]
    have hh := Nat.pow_le_pow_left (by decide : 5 ≤ 8) (rachas (T^[u] n) 1)
    simpa only [Nat.mul_one] using hh.trans
      (show 8 ^ rachas (T^[u] n) 1 ≤
        (3 + 2 * c) * 8 ^ rachas (T^[u] n) 1 * (T^[u] n + 1) from by
          calc
            _ ≤ (3 + 2 * c) * 8 ^ rachas (T^[u] n) 1 := Nat.le_mul_of_pos_left _ (by omega)
            _ ≤ _ := Nat.le_mul_of_pos_right _ (by omega))

theorem entrada_sexta {n c u : ℕ} (h : FugaPura n) (hu : Bajo n c u) :
    (T^[u] n + 1) ^ 6 ≤ 64 * ((3 ^ c) ^ 6 * n ^ 6) * (u + 1) := by
  have hp : 1 ≤ T^[u] n := iter_pos (by have := fuga_pura_dos h; omega) u
  have hs := PerdicesSexta.regreso_sexta h hu
  have ht := PerdicesEstela.S_le_pasos u n
  have h6 : (T^[u] n) ^ 6 ≤ (3 ^ c) ^ 6 * n ^ 6 * (u + 1) :=
    hs.trans (Nat.mul_le_mul_left _ (by omega))
  have hx : T^[u] n + 1 ≤ 2 * T^[u] n := by omega
  have hh := Nat.pow_le_pow_left hx 6
  rw [mul_pow] at hh
  norm_num at hh
  nlinarith

theorem reloj_sextico {t : ℕ → ℕ} (ht : Monotone t) {D : ℕ}
    (hs : ∀ i, (t (i + 1) - t i) ^ 6 ≤ D * (t i + 1) ^ 5) :
    ∀ i, t i + 1 ≤ (D + t 0 + 1) * (i + 1) ^ 6 := by
  generalize hB : D + t 0 + 1 = B
  have hDB : D ≤ B := by omega
  have h0 : t 0 + 1 ≤ B := by omega
  intro i
  induction i with
  | zero => simpa using h0
  | succ i ih =>
    have hg : (t (i + 1) - t i) ^ 6 ≤ (B * (i + 1) ^ 5) ^ 6 := by
      calc
        _ ≤ D * (t i + 1) ^ 5 := hs i
        _ ≤ B * (B * (i + 1) ^ 6) ^ 5 := Nat.mul_le_mul hDB (Nat.pow_le_pow_left ih 5)
        _ = _ := by ring
    have hd := (Nat.pow_le_pow_iff_left (by decide : 6 ≠ 0)).1 hg
    have hm := ht (Nat.le_succ i)
    have hstep : (i + 1) ^ 6 + (i + 1) ^ 5 ≤ (i + 1 + 1) ^ 6 := by
      calc
        _ = (i + 1) ^ 5 * (i + 1 + 1) := by ring
        _ ≤ (i + 1 + 1) ^ 5 * (i + 1 + 1) :=
          Nat.mul_le_mul_right _ (Nat.pow_le_pow_left (Nat.le_succ (i + 1)) 5)
        _ = _ := (pow_succ _ 5).symm
    calc
      _ = (t i + 1) + (t (i + 1) - t i) := by
        rw [Nat.add_right_comm, Nat.add_sub_of_le hm]
      _ ≤ B * (i + 1) ^ 6 + B * (i + 1) ^ 5 := Nat.add_le_add ih hd
      _ = B * ((i + 1) ^ 6 + (i + 1) ^ 5) := by ring
      _ ≤ _ := Nat.mul_le_mul_left _ hstep

@[irreducible] def constante_ritmo (n c : ℕ) : ℕ :=
  64 * (3 + 2 * c) ^ 6 * ((3 ^ c) ^ 6 * n ^ 6)

theorem salto_de_factor {n c u v B : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v)
    (hf : 8 ^ (6 * rachas (T^[u] n) (v - u)) ≤
      B * 5 ^ (6 * rachas (T^[u] n) (v - u)) * (u + 1) ^ 4) :
    (v - u) ^ 6 ≤ constante_ritmo n c * B * (u + 1) ^ 5 := by
  let q := rachas (T^[u] n) (v - u)
  have hd := Nat.pow_le_pow_left (duracion_orbital h he) 6
  have hx := entrada_sexta h he.2.1
  have h5 : (5 ^ q) ^ 6 = 5 ^ (6 * q) := by rw [← pow_mul]; congr 1; omega
  have h8 : (8 ^ q) ^ 6 = 8 ^ (6 * q) := by rw [← pow_mul]; congr 1; omega
  change (5 ^ q * (v - u)) ^ 6 ≤ ((3 + 2 * c) * 8 ^ q * (T^[u] n + 1)) ^ 6 at hd
  simp only [mul_pow, h5, h8] at hd
  have hh : 5 ^ (6 * q) * (v - u) ^ 6 ≤
      5 ^ (6 * q) * (constante_ritmo n c * B * (u + 1) ^ 5) := by
    calc
      _ ≤ (3 + 2 * c) ^ 6 * 8 ^ (6 * q) * (T^[u] n + 1) ^ 6 := hd
      _ ≤ (3 + 2 * c) ^ 6 * (B * 5 ^ (6 * q) * (u + 1) ^ 4) *
          (64 * ((3 ^ c) ^ 6 * n ^ 6) * (u + 1)) :=
        Nat.mul_le_mul (Nat.mul_le_mul_left _ hf) hx
      _ = _ := by unfold constante_ritmo; ring
  exact Nat.le_of_mul_le_mul_left hh (by positivity)

theorem factor_no_acotado {n c : ℕ} {t : ℕ → ℕ} (h : FugaPura n)
    (he : ∀ i, Consecutivos n c (t i) (t (i + 1))) (B : ℕ) :
    ∃ i, B * 5 ^ (6 * rachas (T^[t i] n) (t (i + 1) - t i)) * (t i + 1) ^ 4 <
      8 ^ (6 * rachas (T^[t i] n) (t (i + 1) - t i)) := by
  by_contra hh
  have hf : ∀ i, 8 ^ (6 * rachas (T^[t i] n) (t (i + 1) - t i)) ≤
      B * 5 ^ (6 * rachas (T^[t i] n) (t (i + 1) - t i)) * (t i + 1) ^ 4 := by
    simpa using hh
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have hs := reloj_sextico ht.monotone (fun i => salto_de_factor h (he i) (hf i))
  exact reloj_sextico_imposible h ht (fun i => (he i).2.1)
    (constante_ritmo n c * B + t 0 + 1) hs

theorem enumerar_regresos {n c : ℕ} (hi : InfinitosRegresos n c) (U : ℕ) :
    ∃ t : ℕ → ℕ, U < t 0 ∧ ∀ i, Consecutivos n c (t i) (t (i + 1)) := by
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
  refine ⟨t, hU, ?_⟩
  intro i
  rw [hrec]
  exact ⟨(hsig (t i)).1, hb i, (hsig (t i)).2⟩

theorem infinitos_exigen_ritmo {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (B U : ℕ) :
    ∃ u v, U < u ∧ Consecutivos n c u v ∧
      B * 5 ^ (6 * rachas (T^[u] n) (v - u)) * (u + 1) ^ 4 <
        8 ^ (6 * rachas (T^[u] n) (v - u)) := by
  obtain ⟨t, hU, he⟩ := enumerar_regresos hi U
  obtain ⟨i, hf⟩ := factor_no_acotado h he B
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have h0 := ht.monotone (Nat.zero_le i)
  exact ⟨t i, t (i + 1), by omega, he i, hf⟩

end PerdicesRitmo

#print axioms PerdicesRitmo.paso_ocho_quintos
#print axioms PerdicesRitmo.impares_ocho_quintos
#print axioms PerdicesRitmo.duracion_ocho_quintos
#print axioms PerdicesRitmo.duracion_orbital
#print axioms PerdicesRitmo.entrada_sexta
#print axioms PerdicesRitmo.reloj_sextico
#print axioms PerdicesRitmo.salto_de_factor
#print axioms PerdicesRitmo.factor_no_acotado
#print axioms PerdicesRitmo.enumerar_regresos
#print axioms PerdicesRitmo.infinitos_exigen_ritmo
