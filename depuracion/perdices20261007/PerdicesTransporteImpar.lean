import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! Transporte universal entre fronteras reales A/B.
Las cotas son universales; no se supone ni se demuestra una cota de salida.
La identidad multiplicativa de las recargas firmadas se deriva por escrito
en TRANSPORTE_IMPAR.md. Aquí se certifica el encaje orbital y su cota global.
-/

namespace PerdicesTransporteImpar

def T (x : ℕ) : ℕ := if x % 2 = 0 then x / 2 else (3*x+1)/2

inductive Bloque where
  | a | b

def N : Bloque → ℕ | .a => 2 | .b => 8
def D : Bloque → ℕ | .a => 3 | .b => 9
def E : Bloque → ℕ | .a => 1 | .b => 5
def largo : List Bloque → ℕ | [] => 0 | .a::ps => 1 + largo ps | .b::ps => 3 + largo ps
def impares : List Bloque → ℕ | [] => 0 | .a::ps => 1 + impares ps | .b::ps => 2 + impares ps

def Paso (p : Bloque) (x y : ℕ) : Prop := N p * y = D p * x + E p

inductive Camino : List Bloque → ℕ → ℕ → Prop where
  | nil (n) : Camino [] n n
  | cons {p ps x z y} : Paso p x z → Camino ps z y → Camino (p::ps) x y

theorem paso_a_real (x y : ℕ) :
    Paso .a x y ↔ x % 2 = 1 ∧ T x = y := by
  simp only [Paso, N, D, E, T]
  split_ifs <;> omega

theorem paso_b_real (x y : ℕ) :
    Paso .b x y ↔ x % 2 = 1 ∧ T x % 2 = 1 ∧
      T (T x) % 2 = 0 ∧ T (T (T x)) = y := by
  simp only [Paso, N, D, E, T]
  split_ifs <;> omega

theorem paso_encaje {p x y} (h : Paso p x y) :
    D p * (x+1) ≤ N p * (y+1) ∧
    N p * (y+5) ≤ D p * (x+5) := by
  cases p <;> simp_all only [Paso, N, D, E] <;> omega

theorem encaje {ps n y} (h : Camino ps n y) :
    3 ^ impares ps * (n+1) ≤ 2 ^ largo ps * (y+1) ∧
    2 ^ largo ps * (y+5) ≤ 3 ^ impares ps * (n+5) := by
  induction h with
  | nil n => simp [impares, largo]
  | @cons p ps x z y hp _ ih =>
    obtain ⟨h₁, h₂⟩ := paso_encaje hp
    obtain ⟨i₁, i₂⟩ := ih
    have j₁ := Nat.mul_le_mul_left (3 ^ impares ps) h₁
    have j₂ := Nat.mul_le_mul_left (3 ^ impares ps) h₂
    have k₁ := Nat.mul_le_mul_left (N p) i₁
    have k₂ := Nat.mul_le_mul_left (N p) i₂
    cases p <;> simp only [impares, largo, N, D, pow_add] at * <;>
      norm_num only <;> constructor <;> nlinarith only [j₁, j₂, k₁, k₂]

theorem encaje_potencial {ps n y c} (h : Camino ps n y) (hc : 1 ≤ c ∧ c ≤ 5) :
    3 ^ impares ps * (n+1) ≤ 2 ^ largo ps * (y+c) ∧
    2 ^ largo ps * (y+c) ≤ 3 ^ impares ps * (n+5) := by
  obtain ⟨hi, hs⟩ := encaje h
  constructor
  · exact hi.trans (Nat.mul_le_mul_left _ (by omega))
  · exact (Nat.mul_le_mul_left _ (by omega : y+c ≤ y+5)).trans hs

def orden (x : ℕ) : ℕ := padicValNat 2 x
def impar (x : ℕ) : ℕ := x / 2 ^ orden x

theorem descomposicion (x : ℕ) : 2 ^ orden x * impar x = x :=
  Nat.mul_div_cancel' pow_padicValNat_dvd

theorem transporte_impar {ps n y c} (h : Camino ps n y) (hc : 1 ≤ c ∧ c ≤ 5) :
    3 ^ impares ps * (n+1) ≤ 2 ^ (largo ps + orden (y+c)) * impar (y+c) ∧
    2 ^ (largo ps + orden (y+c)) * impar (y+c) ≤ 3 ^ impares ps * (n+5) := by
  simpa only [pow_add, mul_assoc, descomposicion] using encaje_potencial h hc

theorem condicion_suficiente {ps : List Bloque} {n y c t : ℕ}
    (h : Camino ps n y) (hc : 1 ≤ c ∧ c ≤ 5)
    (hq : 3 ^ impares ps * (n+5) ≤ t * impar (y+c)) :
    2 ^ (largo ps + orden (y+c)) ≤ t := by
  have hpos : 0 < impar (y+c) := by
    have hd := descomposicion (y+c)
    by_contra he
    have hz : impar (y+c) = 0 := by omega
    rw [hz, mul_zero] at hd
    omega
  exact (Nat.mul_le_mul_right_iff hpos).mp ((transporte_impar h hc).2.trans hq)

end PerdicesTransporteImpar

#print axioms PerdicesTransporteImpar.paso_a_real
#print axioms PerdicesTransporteImpar.paso_b_real
#print axioms PerdicesTransporteImpar.paso_encaje
#print axioms PerdicesTransporteImpar.encaje
#print axioms PerdicesTransporteImpar.encaje_potencial
#print axioms PerdicesTransporteImpar.descomposicion
#print axioms PerdicesTransporteImpar.transporte_impar
#print axioms PerdicesTransporteImpar.condicion_suficiente
