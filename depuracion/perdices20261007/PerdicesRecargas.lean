import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Data.Nat.Log
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! # Perdices: certificado orbital de una plantilla de presupuesto falsa.

Mapa atajo sobre naturales. Las recargas son enteras, con signo.
El certificado finito se enlaza a las valuaciones reales; no usa native_decide.
La familia infinita de la nota RECARGAS.md conserva prueba escrita aparte.
-/

namespace PerdicesRecargas

inductive Bloque where
  | A | B
  deriving DecidableEq

open Bloque

def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
def largoBloque : Bloque → ℕ | A => 1 | B => 3
def constante : Bloque → ℕ | A => 1 | B => 5
def salto (n : ℕ) : Bloque → ℕ | A => T n | B => T (T (T n))
def admite (n : ℕ) : Bloque → Prop
  | A => n % 2 = 1
  | B => n % 2 = 1 ∧ T n % 2 = 1 ∧ T (T n) % 2 = 0

instance (n : ℕ) (p : Bloque) : Decidable (admite n p) := by
  cases p <;> unfold admite <;> infer_instance

def admisible (n : ℕ) : List Bloque → Prop
  | [] => True
  | p :: ps => admite n p ∧ admisible (salto n p) ps

def largo : List Bloque → ℕ
  | [] => 0
  | p :: ps => largoBloque p + largo ps

def recargas (n : ℕ) : List Bloque → ℤ
  | [] => 0
  | [_] => 0
  | p :: q :: ps =>
      (padicValNat 2 (salto n p + constante q) : ℤ) -
      (padicValNat 2 (salto n p + constante p) : ℤ) +
      recargas (salto n p) (q :: ps)

def exacta (z a : ℕ) : Prop := z % 2 ^ a = 0 ∧ z % 2 ^ (a + 1) ≠ 0
instance (z a : ℕ) : Decidable (exacta z a) := inferInstanceAs (Decidable (_ ∧ _))

theorem orden_certificado {z a : ℕ} (h : exacta z a) : padicValNat 2 z = a := by
  have hz : z ≠ 0 := by intro he; simp [exacta, he] at h
  have hle : a ≤ padicValNat 2 z :=
    (padicValNat_dvd_iff_le hz).mp (Nat.dvd_of_mod_eq_zero h.1)
  have hlt : ¬ a + 1 ≤ padicValNat 2 z := by
    intro he
    exact h.2 (Nat.mod_eq_zero_of_dvd ((padicValNat_dvd_iff_le hz).mpr he))
  omega

-- Cada fila contiene bloque, valuación de entrada y valuación de salida.
abbrev Fila := Bloque × ℕ × ℕ

def certifica (n : ℕ) : List Fila → Prop
  | [] => True
  | (p, a, b) :: ps => admite n p ∧ exacta (n + constante p) a ∧
      exacta (salto n p + constante p) b ∧ certifica (salto n p) ps

instance (n : ℕ) (ds : List Fila) : Decidable (certifica n ds) := by
  induction ds generalizing n with
  | nil => exact isTrue trivial
  | cons d ds ih =>
      rcases d with ⟨p, a, b⟩
      unfold certifica
      have := ih (salto n p)
      infer_instance

def recargasDatos : List Fila → ℤ
  | [] => 0
  | [_] => 0
  | (_, _, b) :: (q, c, d) :: ps => (c : ℤ) - (b : ℤ) +
      recargasDatos ((q, c, d) :: ps)

theorem certificado_admisible (ds : List Fila) (n : ℕ) (h : certifica n ds) :
    admisible n (ds.map Prod.fst) := by
  induction ds generalizing n with
  | nil => trivial
  | cons d ds ih =>
      rcases d with ⟨p, a, b⟩
      exact ⟨h.1, ih _ h.2.2.2⟩

theorem recargas_certificadas (ds : List Fila) (n : ℕ) (h : certifica n ds) :
    recargas n (ds.map Prod.fst) = recargasDatos ds := by
  induction ds generalizing n with
  | nil => rfl
  | cons d ds ih =>
      rcases d with ⟨p, a, b⟩
      cases ds with
      | nil => rfl
      | cons e es =>
          rcases e with ⟨q, c, d⟩
          have hb := orden_certificado h.2.2.1
          have hc := orden_certificado h.2.2.2.2.1
          have hi := ih (salto n p) h.2.2.2
          simpa only [List.map_cons, recargas, recargasDatos, hb, hc] using
            congrArg (fun z : ℤ => (c : ℤ) - (b : ℤ) + z) hi

def datos : List Fila :=
  [(A,4,3), (A,3,2), (B,5,2), (A,3,2), (B,5,2),
   (A,5,4), (A,4,3), (A,3,2), (B,5,2), (A,4,3),
   (A,3,2), (B,5,2), (A,4,3), (A,3,2), (B,8,5)]

def testigo : List Bloque := datos.map Prod.fst

theorem testigo_certificado : certifica 4591 datos := by decide

theorem testigo_admisible : admisible 4591 testigo :=
  certificado_admisible datos 4591 testigo_certificado

theorem testigo_recarga : recargas 4591 testigo = 26 := by
  rw [testigo, recargas_certificadas datos 4591 testigo_certificado]
  decide

theorem testigo_largo : largo testigo = 25 := by decide

theorem testigo_presupuesto : Nat.clog 2 (4591 + 5) = 13 := by decide

-- Forma entera exacta de P para epsilon=1/2, K(n)=ceil(log2(n+5)).
theorem plantilla_refutada : ¬ (∀ n ps, 0 < n → admisible n ps →
    2 * recargas n ps ≤ (largo ps : ℤ) + 2 * (Nat.clog 2 (n + 5) : ℤ)) := by
  intro h
  have he := h 4591 testigo (by decide) testigo_admisible
  rw [testigo_recarga, testigo_largo, testigo_presupuesto] at he
  norm_num at he

-- Balance algebraico separado: con los consumos exactos, R implica esta forma de P.
theorem presupuesto_equivalente (L v₀ v₁ eta K e : ℚ)
    (h : L = v₀ + eta - v₁) :
    eta ≤ (1-e)*L + K ↔ e*L + v₁ ≤ v₀ + K := by
  constructor <;> intro he <;> nlinarith

end PerdicesRecargas

#print axioms PerdicesRecargas.orden_certificado
#print axioms PerdicesRecargas.certificado_admisible
#print axioms PerdicesRecargas.recargas_certificadas
#print axioms PerdicesRecargas.testigo_certificado
#print axioms PerdicesRecargas.testigo_admisible
#print axioms PerdicesRecargas.testigo_recarga
#print axioms PerdicesRecargas.testigo_largo
#print axioms PerdicesRecargas.testigo_presupuesto
#print axioms PerdicesRecargas.plantilla_refutada
#print axioms PerdicesRecargas.presupuesto_equivalente
