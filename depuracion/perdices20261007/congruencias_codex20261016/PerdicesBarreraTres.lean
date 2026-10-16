import PerdicesBarreraTablas
import PerdicesVentanasConjuntas

/-! Tres partes consecutivas no pueden tener todos sus excesos menores que 17. -/
set_option maxRecDepth 1000000
set_option maxHeartbeats 3200000
set_option Elab.async false

namespace PerdicesBarreraTres

open PerdicesCongruencias PerdicesCongruenciasOrbitales PerdicesTransporteImpar
open PerdicesBarreraTablas

theorem inicial_cubre {p m limite b c d k j : ℕ}
    (hb : b < p) (hc : c < p) (hd : d < p) (hk : k < limite) (hj : j < limite)
    (he : compatible m b c d k j) : (b, c, d, k, j) ∈ inicial p m limite := by
  unfold inicial
  refine List.mem_flatMap.mpr ⟨k, List.mem_range.mpr hk, ?_⟩
  unfold inicialCarga
  refine List.mem_flatMap.mpr ⟨b, List.mem_range.mpr hb, ?_⟩
  refine List.mem_flatMap.mpr ⟨c, List.mem_range.mpr hc, ?_⟩
  refine List.mem_flatMap.mpr ⟨d, List.mem_range.mpr hd, ?_⟩
  exact List.mem_map.mpr ⟨j, List.mem_filter.mpr ⟨List.mem_range.mpr hj, by simpa using he⟩, rfl⟩

theorem levantar_cubre {p factor m b c d k j : ℕ} {antes : List Arista}
    (hp : 0 < p) (hb : b < factor * p) (hc : c < factor * p) (hd : d < factor * p)
    (ht : (b % p, c % p, d % p, k, j) ∈ antes) (he : compatible m b c d k j) :
    (b, c, d, k, j) ∈ levantarTabla p factor m antes := by
  have hb' : b / p < factor := (Nat.div_lt_iff_lt_mul hp).mpr (by omega)
  have hc' : c / p < factor := (Nat.div_lt_iff_lt_mul hp).mpr (by omega)
  have hd' : d / p < factor := (Nat.div_lt_iff_lt_mul hp).mpr (by omega)
  apply List.mem_filter.mpr
  refine ⟨?_, by simpa using he⟩
  refine List.mem_flatMap.mpr ⟨(b % p, c % p, d % p, k, j), ht, ?_⟩
  refine List.mem_flatMap.mpr ⟨b / p, List.mem_range.mpr hb', ?_⟩
  refine List.mem_flatMap.mpr ⟨c / p, List.mem_range.mpr hc', ?_⟩
  refine List.mem_map.mpr ⟨d / p, List.mem_range.mpr hd', ?_⟩
  simp only [Nat.mod_add_div]

theorem levantar_append (p factor m : ℕ) (xs ys : List Arista) :
    levantarTabla p factor m (xs ++ ys) =
      levantarTabla p factor m xs ++ levantarTabla p factor m ys := by
  simp only [levantarTabla, List.flatMap_append, List.filter_append]

theorem levantar_flatMap (p factor m : ℕ) (xs : List ℕ) (f : ℕ → List Arista) :
    levantarTabla p factor m (xs.flatMap f) =
      xs.flatMap (fun k => levantarTabla p factor m (f k)) := by
  induction xs with
  | nil => simp [levantarTabla]
  | cons a xs ih => simp only [List.flatMap_cons, levantar_append, ih]

theorem tabla_doce : levantarTabla 6 2 455 tabla6 = tabla12 := by
  unfold tabla6 tabla12
  rw [levantar_flatMap]
  apply List.flatMap_congr_left
  intro k hk
  exact paso12 k (List.mem_range.mp hk)
theorem tabla_treinta_seis : levantarTabla 12 3 23350145 tabla12 = tabla36 := by
  unfold tabla12 tabla36
  rw [levantar_flatMap]
  apply List.flatMap_congr_left
  intro k hk
  exact paso36 k (List.mem_range.mp hk)
theorem tabla_ciento_ocho : levantarTabla 36 3 2545165805 tabla36 = tabla108 := by
  unfold tabla36 tabla108
  rw [levantar_flatMap]
  apply List.flatMap_congr_left
  intro k hk
  exact paso108 k (List.mem_range.mp hk)
theorem tabla_trescientos : levantarTabla 108 3 414862026215 tabla108 = tabla324 := by
  unfold tabla108 tabla324
  rw [levantar_flatMap]
  apply List.flatMap_congr_left
  intro k hk
  exact paso324 k (List.mem_range.mp hk)

theorem reducir {m p b c d k j : ℕ} (hp : 6 ∣ p)
    (h2 : 2 ^ p % m = 1) (h3 : 3 ^ p % m = 1)
    (h8 : 8 ^ p % m = 1) (h9 : 9 ^ p % m = 1)
    (he : 9 ^ c * (3 ^ b * parte b k + 1) = 8 ^ c * (2 ^ d * parte d j + 1)) :
    compatible m (b % p) (c % p) (d % p) k j := by
  have hb : parte (b % p) k = parte b k := by
    simp only [parte, Nat.mod_mod_of_dvd b hp]
  have hd : parte (d % p) j = parte d j := by
    simp only [parte, Nat.mod_mod_of_dvd d hp]
  have hl : Nat.ModEq m (9 ^ c * (3 ^ b * parte b k + 1))
      (9 ^ (c % p) * (3 ^ (b % p) * parte b k + 1)) :=
    Nat.ModEq.mul (potencia_periodica h9 c)
      (Nat.ModEq.add (Nat.ModEq.mul (potencia_periodica h3 b) (Nat.ModEq.refl _)) (Nat.ModEq.refl _))
  have hr : Nat.ModEq m (8 ^ c * (2 ^ d * parte d j + 1))
      (8 ^ (c % p) * (2 ^ (d % p) * parte d j + 1)) :=
    Nat.ModEq.mul (potencia_periodica h8 c)
      (Nat.ModEq.add (Nat.ModEq.mul (potencia_periodica h2 d) (Nat.ModEq.refl _)) (Nat.ModEq.refl _))
  rw [he] at hl
  unfold compatible
  rw [hb, hd]
  exact hl.symm.trans hr

theorem candidatos {b c d k j : ℕ} (hk : k < 17) (hj : j < 17)
    (he : 9 ^ c * (3 ^ b * parte b k + 1) = 8 ^ c * (2 ^ d * parte d j + 1)) :
    (b % 324, c % 324, d % 324, k, j) ∈ tabla324 := by
  have h6 := reducir (m := 7) (p := 6) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t6 : (b % 6, c % 6, d % 6, k, j) ∈ tabla6 :=
    inicial_cubre (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega))
      (Nat.mod_lt _ (by omega)) hk hj h6
  have h12 := reducir (m := 455) (p := 12) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t12 : (b % 12, c % 12, d % 12, k, j) ∈ tabla12 := by
    rw [← tabla_doce]
    apply levantar_cubre (p := 6) (by omega) (Nat.mod_lt _ (by omega))
      (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h12
    simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 6 ∣ 12)] using t6
  have h36 := reducir (m := 23350145) (p := 36) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t36 : (b % 36, c % 36, d % 36, k, j) ∈ tabla36 := by
    rw [← tabla_treinta_seis]
    apply levantar_cubre (p := 12) (by omega) (Nat.mod_lt _ (by omega))
      (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h36
    simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 12 ∣ 36)] using t12
  have h108 := reducir (m := 2545165805) (p := 108) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  have t108 : (b % 108, c % 108, d % 108, k, j) ∈ tabla108 := by
    rw [← tabla_ciento_ocho]
    apply levantar_cubre (p := 36) (by omega) (Nat.mod_lt _ (by omega))
      (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h108
    simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 36 ∣ 108)] using t36
  have h324 := reducir (m := 414862026215) (p := 324) (by decide +kernel)
    (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) he
  rw [← tabla_trescientos]
  apply levantar_cubre (p := 108) (by omega) (Nat.mod_lt _ (by omega))
    (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) _ h324
  simpa only [Nat.mod_mod_of_dvd _ (by decide +kernel : 108 ∣ 324)] using t108

def filtro (b c d k j : ℕ) : Prop :=
  c = 1 ∨ ((3 ^ b * parte b k + 1) % 16 = 0 ∧ (2 ^ d * parte d j + 1) % 81 = 0)

theorem pasa_filtro {b c d k j : ℕ} (hc : 1 ≤ c)
    (he : 9 ^ c * (3 ^ b * parte b k + 1) = 8 ^ c * (2 ^ d * parte d j + 1)) :
    filtro (b % 324) (c % 324) (d % 324) k j := by
  by_cases h : c % 324 = 1
  · exact Or.inl h
  have hc2 : 2 ≤ c := by omega
  have h8 : 8 ^ c ∣ 3 ^ b * parte b k + 1 := by
    apply (((by decide +kernel : Nat.Coprime 8 9).pow c c)).dvd_of_dvd_mul_left
    rw [he]
    exact dvd_mul_right _ _
  have h9 : 9 ^ c ∣ 2 ^ d * parte d j + 1 := by
    apply (((by decide +kernel : Nat.Coprime 9 8).pow c c)).dvd_of_dvd_mul_left
    rw [← he]
    exact dvd_mul_right _ _
  have hz16 := Nat.mod_eq_zero_of_dvd
    (((by decide +kernel : 16 ∣ 8 ^ 2).trans (pow_dvd_pow 8 hc2)).trans h8)
  have hz81 := Nat.mod_eq_zero_of_dvd
    (((by decide +kernel : 81 ∣ 9 ^ 2).trans (pow_dvd_pow 9 hc2)).trans h9)
  have hb : parte (b % 324) k = parte b k := by
    simp only [parte, Nat.mod_mod_of_dvd _ (by decide +kernel : 6 ∣ 324)]
  have hd : parte (d % 324) j = parte d j := by
    simp only [parte, Nat.mod_mod_of_dvd _ (by decide +kernel : 6 ∣ 324)]
  have h3 := potencia_periodica (a := 3) (m := 16) (k := 324) (by decide +kernel) b
  have h2 := potencia_periodica (a := 2) (m := 81) (k := 324) (by decide +kernel) d
  apply Or.inr
  constructor
  · rw [hb, Nat.add_mod, Nat.mul_mod, ← h3, ← Nat.mul_mod, ← Nat.add_mod]
    exact hz16
  · rw [hd, Nat.add_mod, Nat.mul_mod, ← h2, ← Nat.mul_mod, ← Nat.add_mod]
    exact hz81

theorem filtrar_tabla : ∀ t ∈ tabla324,
    filtro t.1 t.2.1 t.2.2.1 t.2.2.2.1 t.2.2.2.2 → t ∈ aristas := by
  unfold filtro parte
  decide +kernel

theorem sin_empalmes : ∀ t ∈ aristas, ∀ u ∈ aristas,
    t.2.2.1 = u.1 → t.2.2.2.2 = u.2.2.2.1 → False := by
  unfold aristas
  decide +kernel

theorem barrera_tres {b c d e f k j l : ℕ} (hc : 1 ≤ c) (he : 1 ≤ e)
    (h₁ : 9 ^ c * (3 ^ b * parte b k + 1) = 8 ^ c * (2 ^ d * parte d j + 1))
    (h₂ : 9 ^ e * (3 ^ d * parte d j + 1) = 8 ^ e * (2 ^ f * parte f l + 1)) :
    17 ≤ k ∨ 17 ≤ j ∨ 17 ≤ l := by
  by_contra h
  have hk : k < 17 := by omega
  have hj : j < 17 := by omega
  have hl : l < 17 := by omega
  have ht := filtrar_tabla _ (candidatos hk hj h₁) (pasa_filtro hc h₁)
  have hu := filtrar_tabla _ (candidatos hj hl h₂) (pasa_filtro he h₂)
  exact sin_empalmes _ ht _ hu rfl rfl

theorem barrera_orbital {b c d e f x y z t u k j l : ℕ}
    (hc : 1 ≤ c) (he : 1 ≤ e)
    (h₁ : Camino (List.replicate b .a) x y)
    (h₂ : Camino (List.replicate c .b) y z)
    (h₃ : Camino (List.replicate d .a) z t)
    (h₄ : Camino (List.replicate e .b) t u)
    (hx : x + 1 = 2 ^ (b + 2) * parte b k)
    (hz : z + 1 = 2 ^ (d + 2) * parte d j)
    (hu : u + 1 = 2 ^ (f + 2) * parte f l) :
    17 ≤ k ∨ 17 ≤ j ∨ 17 ≤ l :=
  barrera_tres hc he
    (PerdicesVentanasConjuntas.enlace_compartido h₁ h₂ hx hz)
    (PerdicesVentanasConjuntas.enlace_compartido h₃ h₄ hz hu)

theorem parte_alta {b k : ℕ} (hk : 17 ≤ k) : 1237 ≤ parte b k := by
  have hb : b % 6 < 6 := Nat.mod_lt _ (by omega)
  unfold parte
  interval_cases j : b % 6 <;> norm_num [j, minimoResiduo] <;> omega

theorem banda_alta {n b k : ℕ} (hk : 17 ≤ k)
    (he : 9 * (n + 5) = 32 * (2 ^ b * parte b k + 1)) :
    2 ^ (b + 12) < n + 5 ∧ b + 13 ≤ Nat.clog 2 (n + 5) := by
  have hr := parte_alta (b := b) hk
  have hp : 0 < (2 : ℕ) ^ b := pow_pos (by omega) _
  have hg : 2 ^ (b + 12) < n + 5 := by
    rw [pow_add]
    norm_num
    nlinarith [Nat.mul_le_mul_left (2 ^ b) hr]
  exact ⟨hg, by have := (Nat.lt_clog_iff_pow_lt (by omega : 1 < 2)).mpr hg; omega⟩

theorem transporte_alto {n x b k : ℕ} {prefijo : List Bloque}
    (h : Camino prefijo n x) (hk : 17 ≤ k)
    (he : 9 * (x + 5) = 32 * (2 ^ b * parte b k + 1)) :
    2 ^ (largo prefijo + b + 12) < 3 ^ impares prefijo * (n + 5) := by
  have hg := (banda_alta hk he).1
  have ht := (encaje h).2
  have hp : 0 < (2 : ℕ) ^ largo prefijo := pow_pos (by omega) _
  have hm := Nat.mul_lt_mul_of_pos_left hg hp
  rw [pow_add, pow_add] at hm ⊢
  nlinarith

def SinTresBajas : List ℕ → Prop
  | a :: b :: c :: resto => (17 ≤ a ∨ 17 ≤ b ∨ 17 ≤ c) ∧ SinTresBajas (b :: c :: resto)
  | _ => True

theorem exceso_cadena (cargas : List ℕ) (h : SinTresBajas cargas) :
    17 * (cargas.length / 3) ≤ cargas.sum := by
  match cargas with
  | [] => simp
  | [a] => simp
  | [a, b] => simp
  | a :: b :: c :: resto =>
    have hr : SinTresBajas resto := by
      cases resto with
      | nil => trivial
      | cons x xs =>
        cases xs with
        | nil => trivial
        | cons y ys => exact h.2.2.2
    have hi := exceso_cadena resto hr
    have habc := h.1
    simp only [List.length_cons, List.sum_cons]
    omega
termination_by cargas.length

end PerdicesBarreraTres

#print axioms PerdicesBarreraTres.inicial_cubre
#print axioms PerdicesBarreraTres.levantar_cubre
#print axioms PerdicesBarreraTres.levantar_append
#print axioms PerdicesBarreraTres.levantar_flatMap
#print axioms PerdicesBarreraTres.tabla_doce
#print axioms PerdicesBarreraTres.tabla_treinta_seis
#print axioms PerdicesBarreraTres.tabla_ciento_ocho
#print axioms PerdicesBarreraTres.tabla_trescientos
#print axioms PerdicesBarreraTres.reducir
#print axioms PerdicesBarreraTres.candidatos
#print axioms PerdicesBarreraTres.pasa_filtro
#print axioms PerdicesBarreraTres.filtrar_tabla
#print axioms PerdicesBarreraTres.sin_empalmes
#print axioms PerdicesBarreraTres.barrera_tres
#print axioms PerdicesBarreraTres.barrera_orbital
#print axioms PerdicesBarreraTres.parte_alta
#print axioms PerdicesBarreraTres.banda_alta
#print axioms PerdicesBarreraTres.transporte_alto
#print axioms PerdicesBarreraTres.exceso_cadena
