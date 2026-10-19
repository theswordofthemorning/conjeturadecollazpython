import PerdicesBarreraTres
import Mathlib.Tactic.FieldSimp

/-! Suma ponderada desde una misma semilla. No acota el reloj ni la salida.
Las ventanas llevan caminos desde n; los enlaces son las identidades exactas
entre partes vecinas. La extracción de estos datos de una palabra arbitraria
se conserva como el enlace escrito de BARRERA.md. -/

namespace PerdicesBarreraPonderada

open PerdicesTransporteImpar PerdicesCongruencias PerdicesBarreraTablas
open PerdicesBarreraTres

structure Ventana where
  b : ℕ
  k : ℕ
  entrada : ℕ
  prefijo : List Bloque

def Realizada (n : ℕ) (v : Ventana) : Prop :=
  Camino v.prefijo n v.entrada ∧
    9 * (v.entrada + 5) = 32 * (2 ^ v.b * parte v.b v.k + 1)

def Enlazadas : List Ventana → Prop
  | v :: w :: resto =>
      (∃ c : ℕ, 1 ≤ c ∧
        9 ^ c * (3 ^ v.b * parte v.b v.k + 1) =
          8 ^ c * (2 ^ w.b * parte w.b w.k + 1)) ∧ Enlazadas (w :: resto)
  | _ => True

def peso (v : Ventana) : ℚ :=
  3 ^ impares v.prefijo / 2 ^ (largo v.prefijo + v.b)

def correccion (v : Ventana) : ℚ := 1 / 2 ^ v.b

theorem enlaces_barrera (vs : List Ventana) (h : Enlazadas vs) :
    SinTresBajas (vs.map Ventana.k) := by
  match vs with
  | [] => trivial
  | [v] => trivial
  | [v, w] => trivial
  | v :: w :: u :: resto =>
    obtain ⟨c, hc, h₁⟩ := h.1
    obtain ⟨d, hd, h₂⟩ := h.2.1
    exact ⟨barrera_tres hc hd h₁ h₂, enlaces_barrera (w :: u :: resto) h.2⟩
termination_by vs.length

theorem suma_partes (vs : List Ventana) :
    (vs.map (fun v => parte v.b v.k)).sum =
      (vs.map (fun v => minimoResiduo (v.b % 6))).sum +
        72 * (vs.map Ventana.k).sum := by
  induction vs with
  | nil => simp
  | cons v vs ih => simp only [List.map_cons, List.sum_cons, parte] at *; omega

theorem exceso_partes (vs : List Ventana) (h : Enlazadas vs) :
    (vs.map (fun v => minimoResiduo (v.b % 6))).sum + 1224 * (vs.length / 3) ≤
      (vs.map (fun v => parte v.b v.k)).sum := by
  have hc := exceso_cadena (vs.map Ventana.k) (enlaces_barrera vs h)
  simp only [List.length_map] at hc
  rw [suma_partes]
  omega

theorem ventana_ponderada {n : ℕ} {v : Ventana} (h : Realizada n v) :
    (parte v.b v.k : ℚ) + correccion v ≤ (9 / 32 : ℚ) * (n + 5) * peso v := by
  have ht : (2 : ℚ) ^ largo v.prefijo * (v.entrada + 5) ≤
      3 ^ impares v.prefijo * (n + 5) := by exact_mod_cast (encaje h.1).2
  have he : (9 : ℚ) * (v.entrada + 5) =
      32 * (2 ^ v.b * (parte v.b v.k : ℚ) + 1) := by exact_mod_cast h.2
  have hp : (0 : ℚ) < 2 ^ largo v.prefijo := pow_pos (by norm_num) _
  have hb : (0 : ℚ) < 2 ^ v.b := pow_pos (by norm_num) _
  unfold correccion peso
  rw [pow_add]
  apply (mul_le_mul_iff_left₀ (mul_pos hp hb)).mp
  field_simp
  nlinarith [congrArg (fun x : ℚ => 2 ^ largo v.prefijo * x) he]

theorem suma_ventanas {n : ℕ} (vs : List Ventana)
    (h : ∀ v ∈ vs, Realizada n v) :
    (vs.map (fun v => (parte v.b v.k : ℚ) + correccion v)).sum ≤
      (9 / 32 : ℚ) * (n + 5) * (vs.map peso).sum := by
  induction vs with
  | nil => simp
  | cons v vs ih =>
    have hv := ventana_ponderada (h v (by simp))
    have hr := ih (fun w hw => h w (by simp [hw]))
    simp only [List.map_cons, List.sum_cons]
    nlinarith

theorem separar_suma (vs : List Ventana) :
    (vs.map (fun v => (parte v.b v.k : ℚ) + correccion v)).sum =
      ((vs.map (fun v => parte v.b v.k)).sum : ℚ) + (vs.map correccion).sum := by
  induction vs with
  | nil => simp
  | cons v vs ih => simp only [List.map_cons, List.sum_cons, Nat.cast_add, ih]; ring

theorem barrera_ponderada {n : ℕ} (vs : List Ventana)
    (hr : ∀ v ∈ vs, Realizada n v) (he : Enlazadas vs) :
    ((vs.map (fun v => minimoResiduo (v.b % 6))).sum : ℚ) +
      1224 * (vs.length / 3 : ℕ) + (vs.map correccion).sum ≤
        (9 / 32 : ℚ) * (n + 5) * (vs.map peso).sum := by
  have hp : ((vs.map (fun v => minimoResiduo (v.b % 6))).sum : ℚ) +
      1224 * (vs.length / 3 : ℕ) ≤ (vs.map (fun v => parte v.b v.k)).sum := by
    exact_mod_cast exceso_partes vs he
  have hs := suma_ventanas vs hr
  rw [separar_suma] at hs
  linarith

end PerdicesBarreraPonderada

#print axioms PerdicesBarreraPonderada.enlaces_barrera
#print axioms PerdicesBarreraPonderada.suma_partes
#print axioms PerdicesBarreraPonderada.exceso_partes
#print axioms PerdicesBarreraPonderada.ventana_ponderada
#print axioms PerdicesBarreraPonderada.suma_ventanas
#print axioms PerdicesBarreraPonderada.separar_suma
#print axioms PerdicesBarreraPonderada.barrera_ponderada
