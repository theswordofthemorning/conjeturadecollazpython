import PerdicesBalance

/-! # Perdices: las excepciones al bloque 110 tampoco pueden estar acotadas.

Se cuenta como excepción cada bloque impar/par (a,b) distinto de (2,1),
incluido el último bloque, cuya racha par puede terminar en el regreso.
La longitud de las cadenas intermedias 110 permanece libre.
-/

namespace PerdicesExcepciones

open Ocelotas CasaPlano CasaRetrato OcelotasTrayectorias OcelotasContador
open PerdicesSeparacion PerdicesExcursiones PerdicesRitmo PerdicesBalance

theorem crecimiento_paso (x : ℕ) : T x + 5 ≤ 2 * (x + 5) := by
  rcases Nat.mod_two_eq_zero_or_one x with hp | hp
  · have hh := T_par hp; omega
  · have hh := T_impar hp; omega

theorem crecimiento_prefijo (x t : ℕ) : T^[t] x + 5 ≤ 2 ^ t * (x + 5) := by
  induction t with
  | zero => simp
  | succ t ih =>
    rw [Function.iterate_succ_apply']
    calc
      _ ≤ 2 * (T^[t] x + 5) := crecimiento_paso _
      _ ≤ 2 * (2 ^ t * (x + 5)) := Nat.mul_le_mul_left _ ih
      _ = _ := by rw [pow_succ]; ring

theorem techo_prefijo {x L : ℕ} (hx : x + 5 ≤ 2 ^ L) (t : ℕ) :
    T^[t] x + 5 ≤ 2 ^ (L + t) := by
  calc
    _ ≤ 2 ^ t * (x + 5) := crecimiento_prefijo x t
    _ ≤ 2 ^ t * 2 ^ L := Nat.mul_le_mul_left _ hx
    _ = _ := by rw [← pow_add, Nat.add_comm]

theorem tiempo_110 {a b : ℕ → ℕ} {j k : ℕ}
    (hg : ∀ i < k, a (j + i) = 2 ∧ b (j + i) = 1) :
    tiempo a b (j + k) = tiempo a b j + 3 * k := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hprev := ih (fun i hi => hg i (by omega))
    have hh := hg k (by omega)
    rw [Nat.add_succ, tiempo, hh.1, hh.2, hprev]
    omega

theorem divisibilidad_cadena {x r j k : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hk : j + k ≤ r)
    (hg : ∀ i < k, a (j + i) = 2 ∧ b (j + i) = 1) :
    8 ^ k ∣ T^[tiempo a b j] x + 5 := by
  have hh := divisibilidad_trasladada (z := fun i => T^[tiempo a b (j + i)] x + 5)
    (by decide : Nat.Coprime 8 9) (r := k)
    (fun i hi => by
      simpa only [Nat.add_assoc] using
        bloque_110 hw (by omega : j + i < r) (hg i hi).1 (hg i hi).2)
  simpa only [Nat.add_zero] using hh

theorem comprimir_cadena {x r j k L : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra x a b r) (hx : x + 5 ≤ 2 ^ L) (hjk : j ≤ k) (hkr : k ≤ r)
    (hg : ∀ i, j ≤ i → i < k → a i = 2 ∧ b i = 1) :
    tiempo a b k + L ≤ 2 * (tiempo a b j + L) := by
  have hg' : ∀ i < k - j, a (j + i) = 2 ∧ b (j + i) = 1 :=
    fun i hi => hg (j + i) (by omega) (by omega)
  have hd := divisibilidad_cadena hw (by omega : j + (k - j) ≤ r) hg'
  have hp := Nat.le_of_dvd (by omega : 0 < T^[tiempo a b j] x + 5) hd
  have hpow : 2 ^ (3 * (k - j)) ≤ 2 ^ (L + tiempo a b j) := by
    simpa only [pow_mul, show (2 : ℕ) ^ 3 = 8 by decide] using
      hp.trans (techo_prefijo hx (tiempo a b j))
  have hlen := (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 hpow
  have ht := tiempo_110 hg'
  rw [show j + (k - j) = k by omega] at ht
  omega

theorem cota_bloque {x r i L : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < x) (hw : Palabra x a b r) (hx : x + 5 ≤ 2 ^ L) (hi : i < r) :
    tiempo a b (i + 1) + L ≤ 4 * (tiempo a b i + L) := by
  have hdiv := Nat.le_of_dvd (by omega : 0 < T^[tiempo a b i] x + 1)
    (congruencia_racha hw hi)
  have ha : a i ≤ L + tiempo a b i := by
    apply (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1
    exact hdiv.trans ((by omega : T^[tiempo a b i] x + 1 ≤ T^[tiempo a b i] x + 5).trans
      (techo_prefijo hx _))
  have he := identidad_par hw hi
  have hy := iter_pos hn (tiempo a b (i + 1))
  have hpar : 2 ^ b i ≤ T^[tiempo a b i + a i] x := by
    rw [← he]
    exact Nat.le_mul_of_pos_right _ hy
  have hb : b i ≤ L + (tiempo a b i + a i) := by
    apply (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1
    exact hpar.trans ((Nat.le_add_right _ 5).trans (techo_prefijo hx _))
  simp only [tiempo]
  omega

def excepciones (a b : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | i + 1 => excepciones a b i + if a i = 2 ∧ b i = 1 then 0 else 1

/-- El testigo j es el extremo posterior a la última excepción ya leída. -/
theorem ultima_excepcion {x r L : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < x) (hw : Palabra x a b r) (hx : x + 5 ≤ 2 ^ L) :
    ∀ k ≤ r, ∃ j ≤ k,
      tiempo a b j + L ≤ 8 ^ excepciones a b k * L ∧
      ∀ i, j ≤ i → i < k → a i = 2 ∧ b i = 1 := by
  intro k
  induction k with
  | zero => intro _; exact ⟨0, le_rfl, by simp [tiempo, excepciones], by omega⟩
  | succ k ih =>
    intro hk
    obtain ⟨j, hj, hpres, hcola⟩ := ih (by omega)
    by_cases hg : a k = 2 ∧ b k = 1
    · refine ⟨j, by omega, ?_, ?_⟩
      · simpa only [excepciones, if_pos hg, Nat.add_zero] using hpres
      · intro i hji hik
        by_cases hik' : i < k
        · exact hcola i hji hik'
        · have hie : i = k := by omega
          simpa only [hie] using hg
    · refine ⟨k + 1, le_rfl, ?_, by omega⟩
      have hcadena := comprimir_cadena hw hx hj (by omega) hcola
      calc
        _ ≤ 4 * (tiempo a b k + L) := cota_bloque hn hw hx (by omega)
        _ ≤ 8 * (tiempo a b j + L) := by omega
        _ ≤ 8 * (8 ^ excepciones a b k * L) := Nat.mul_le_mul_left _ hpres
        _ = _ := by simp only [excepciones, hg, ↓reduceIte, pow_succ]; ring

theorem duracion_excepciones {x r L : ℕ} {a b : ℕ → ℕ}
    (hn : 0 < x) (hw : Palabra x a b r) (hx : x + 5 ≤ 2 ^ L) :
    tiempo a b r + L ≤ 2 * 8 ^ excepciones a b r * L := by
  obtain ⟨j, hj, hpres, hcola⟩ := ultima_excepcion hn hw hx r le_rfl
  have hh := comprimir_cadena hw hx hj le_rfl hcola
  have hm := Nat.mul_le_mul_left 2 hpres
  simpa only [Nat.mul_assoc] using hh.trans hm

def PocasExcepciones (x d H : ℕ) : Prop :=
  d = 1 ∨ ∃ r a b, Palabra x a b r ∧ tiempo a b r = d ∧ excepciones a b r ≤ H

theorem excepciones_cuadrado {n c u v H : ℕ} (h : FugaPura n)
    (he : Consecutivos n c u v) (hp : PocasExcepciones (T^[u] n) (v - u) H) :
    (v - u) ^ 2 ≤
      ((12 * 8 ^ H) ^ 2 * ((3 ^ c) ^ 6 * n ^ 6) + 1) * (u + 1) := by
  rcases hp with hd | ⟨r, a, b, hw, ht, hH⟩
  · rw [hd]; simp only [one_pow]
    exact Nat.one_le_iff_ne_zero.mpr (by positivity)
  · have hx : 1 ≤ T^[u] n := iter_pos (by have := fuga_pura_dos h; omega) u
    have hh := duracion_excepciones hx hw (Nat.le_of_lt Nat.lt_two_pow_self)
    rw [ht] at hh
    have hpow := Nat.pow_le_pow_right (by decide : 1 ≤ 8) hH
    have hm := Nat.mul_le_mul_right (T^[u] n + 5) (Nat.mul_le_mul_left 2 hpow)
    have hd : v - u ≤ (12 * 8 ^ H) * T^[u] n := by
      have hentry : T^[u] n + 5 ≤ 6 * T^[u] n := by omega
      have hmul := Nat.mul_le_mul_left (2 * 8 ^ H) hentry
      nlinarith only [hh, hm, hmul, Nat.zero_le (T^[u] n + 5)]
    have h6 := PerdicesSexta.regreso_sexta h he.2.1
    have hs := PerdicesEstela.S_le_pasos u n
    have h2 : (T^[u] n) ^ 2 ≤ (3 ^ c) ^ 6 * n ^ 6 * (u + 1) :=
      (Nat.pow_le_pow_right hx (by decide : 2 ≤ 6)).trans
        (h6.trans (Nat.mul_le_mul_left _ (by omega)))
    have hd2 := Nat.pow_le_pow_left hd 2
    rw [mul_pow] at hd2
    have hmul := Nat.mul_le_mul_left ((12 * 8 ^ H) ^ 2) h2
    nlinarith only [hd2, hmul, Nat.zero_le (u + 1)]

theorem infinitos_sin_cota {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (H U : ℕ) :
    ∃ u v, U < u ∧ Consecutivos n c u v ∧ ¬ PocasExcepciones (T^[u] n) (v - u) H := by
  obtain ⟨t, hU, he⟩ := enumerar_regresos hi U
  have ht : StrictMono t := strictMono_nat_of_lt_succ (fun i => (he i).1)
  have hx : ∃ i, ¬ PocasExcepciones (T^[t i] n) (t (i + 1) - t i) H := by
    by_contra hh
    have hr : ∀ i, PocasExcepciones (T^[t i] n) (t (i + 1) - t i) H := by simpa using hh
    have hclock := reloj_cuadratico ht.monotone (fun i => excepciones_cuadrado h (he i) (hr i))
    apply reloj_sextico_imposible h ht (fun i => (he i).2.1)
      ((12 * 8 ^ H) ^ 2 * ((3 ^ c) ^ 6 * n ^ 6) + 1 + t 0 + 1)
    intro i
    exact (hclock i).trans (Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by omega) (by decide)))
  obtain ⟨i, hir⟩ := hx
  have h0 := ht.monotone (Nat.zero_le i)
  exact ⟨t i, t (i + 1), by omega, he i, hir⟩

theorem infinitos_exigen_excepciones {n c : ℕ} (h : FugaPura n)
    (hi : InfinitosRegresos n c) (H U : ℕ) :
    ∃ u v r a b, U < u ∧ Consecutivos n c u v ∧
      Palabra (T^[u] n) a b r ∧ tiempo a b r = v - u ∧
      r = rachas (T^[u] n) (v - u) ∧ H < excepciones a b r := by
  obtain ⟨u, v, hU, he, hp⟩ := infinitos_sin_cota h hi H U
  have hd : u + 1 < v := by
    by_contra hh
    have hlen : v - u = 1 := by have := he.1; omega
    exact hp (Or.inl hlen)
  obtain ⟨_, a, b, hw, ht⟩ := palabra_excursion he hd
  refine ⟨u, v, _, a, b, hU, he, hw, ht, rfl, ?_⟩
  by_contra hh
  exact hp (Or.inr ⟨_, a, b, hw, ht, by omega⟩)

end PerdicesExcepciones

#print axioms PerdicesExcepciones.crecimiento_paso
#print axioms PerdicesExcepciones.crecimiento_prefijo
#print axioms PerdicesExcepciones.techo_prefijo
#print axioms PerdicesExcepciones.tiempo_110
#print axioms PerdicesExcepciones.divisibilidad_cadena
#print axioms PerdicesExcepciones.comprimir_cadena
#print axioms PerdicesExcepciones.cota_bloque
#print axioms PerdicesExcepciones.ultima_excepcion
#print axioms PerdicesExcepciones.duracion_excepciones
#print axioms PerdicesExcepciones.excepciones_cuadrado
#print axioms PerdicesExcepciones.infinitos_sin_cota
#print axioms PerdicesExcepciones.infinitos_exigen_excepciones
