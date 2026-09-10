/-
  LEMA DE LAS SURICATAS: rigidez de los invariantes comunes de alturas 2 y 3.
  Dos operadores DISTINTOS: tau_2(x)=3x-4 y tau_3(x)=3x-13.
  Una funcion periodica modulo 2^m invariante bajo ambos es constante.
  Esto no prueba un gap uniforme ni la contraccion de la excursion.
  Nucleo Lean, sin Mathlib. Sin dependencia de los scripts Python.
-/

namespace Frente20260910

def pot2 : Nat -> Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

def Periodica {A : Type} (f : Int -> A) (p : Int) : Prop :=
  forall x, f (x + p) = f x

theorem periodo_multiplo {A : Type} (f : Int -> A) (p : Int)
    (hp : Periodica f p) (n : Nat) :
    forall x, f (x + (n : Int) * p) = f x := by
  induction n with
  | zero => intro x; simp
  | succ n ih =>
    intro x
    have eqn : x + ((n + 1 : Nat) : Int) * p =
        (x + (n : Int) * p) + p := by
      simp [Int.add_mul, Int.add_assoc]
    rw [eqn, hp, ih]

theorem pot2_pos (m : Nat) : 0 < pot2 m := by
  induction m with
  | zero => decide
  | succ m ih => simp only [pot2]; omega

theorem pot2_no_tres (m : Nat) : Not (pot2 m % 3 = 0) := by
  induction m with
  | zero => decide
  | succ m ih => simp only [pot2]; omega

theorem periodo_nueve {A : Type} (f : Int -> A) (n : Int)
    (hn : Not (n % 3 = 0)) (hp : Periodica f n)
    (h2 : forall x, f (3*x - 4) = f x)
    (h3 : forall x, f (3*x - 13) = f x) : Periodica f 9 := by
  have linea (y : Int) (hy : (y + 13) % 3 = 0) : f (y + 9) = f y := by
    have a := h2 ((y + 13) / 3)
    have b := h3 ((y + 13) / 3)
    have e1 : 3 * ((y + 13) / 3) - 4 = y + 9 := by omega
    have e2 : 3 * ((y + 13) / 3) - 13 = y := by omega
    rw [e1] at a
    rw [e2] at b
    exact a.trans b.symm
  intro x
  by_cases h0 : (x + 13) % 3 = 0
  · exact linea x h0
  · by_cases h1 : (x + n + 13) % 3 = 0
    · have h := linea (x + n) h1
      have e : x + n + 9 = (x + 9) + n := by omega
      rw [e, hp, hp] at h
      exact h
    · have h2mod : (x + 2*n + 13) % 3 = 0 := by
        have hn_cases : Or (n % 3 = 1) (n % 3 = 2) := by omega
        have hx_cases : Or ((x + 13) % 3 = 1) ((x + 13) % 3 = 2) := by omega
        cases hn_cases with
        | inl hn1 => cases hx_cases with
          | inl hx1 => omega
          | inr hx2 => omega
        | inr hn2 => cases hx_cases with
          | inl hx1 => omega
          | inr hx2 => omega
      have h := linea (x + 2*n) h2mod
      have e : x + 2*n + 9 = (x + 9) + (2 : Int)*n := by omega
      rw [e] at h
      have pa := periodo_multiplo f n hp 2 (x + 9)
      have pb := periodo_multiplo f n hp 2 x
      exact pa.symm.trans (h.trans pb)

theorem periodo_uno {A : Type} (f : Int -> A) (m : Nat)
    (h9 : Periodica f 9) (hp : Periodica f (pot2 m)) :
    Periodica f 1 := by
  induction m with
  | zero => exact hp
  | succ m ih =>
    apply ih
    intro x
    have hr := pot2_pos m
    have ha := periodo_multiplo f 9 h9 (pot2 m).toNat x
    have hb := periodo_multiplo f (pot2 (m + 1)) hp 4 (x + pot2 m)
    change f (x + pot2 m + (4 : Int) * pot2 (m + 1)) = f (x + pot2 m) at hb
    have cast : ((pot2 m).toNat : Int) = pot2 m := by omega
    rw [cast] at ha
    have eqn : x + pot2 m + (4 : Int)*pot2 (m + 1) =
        x + pot2 m * 9 := by simp only [pot2]; omega
    rw [eqn] at hb
    exact hb.symm.trans ha

theorem invariantes_comunes_constantes {A : Type} (f : Int -> A) (m : Nat)
    (hp : Periodica f (pot2 m))
    (h2 : forall x, f (3*x - 4) = f x)
    (h3 : forall x, f (3*x - 13) = f x) :
    forall x, f x = f 0 := by
  have h9 := periodo_nueve f (pot2 m) (pot2_no_tres m) hp h2 h3
  have h1 := periodo_uno f m h9 hp
  intro x
  by_cases hx : 0 <= x
  · have h := periodo_multiplo f 1 h1 x.toNat 0
    have cast : (x.toNat : Int) = x := by omega
    simpa [cast] using h
  · have h := periodo_multiplo f 1 h1 (-x).toNat x
    have cast : ((-x).toNat : Int) = -x := by omega
    have eqn : x + ((-x).toNat : Int) * 1 = 0 := by omega
    rw [eqn] at h
    exact h.symm

def chi (x : Int) : Int := if x % 4 = 0 || x % 4 = 3 then 1 else -1

theorem chi_periodica : Periodica chi 4 := by
  intro x
  unfold chi
  have e : (x + 4) % 4 = x % 4 := by omega
  rw [e]

theorem chi_invariante_tres : forall x, chi (3*x - 13) = chi x := by
  intro x
  unfold chi
  split <;> split <;> simp_all <;> omega

theorem chi_invariante_cinco : forall x, chi (3*x - 121) = chi x := by
  intro x
  have e : (3*x - 121) % 4 = (3*x - 13) % 4 := by omega
  unfold chi
  rw [e]
  exact chi_invariante_tres x

theorem chi_no_invariante_dos : Not (chi (3*1 - 4) = chi 1) := by decide
theorem chi_media_cero : chi 0 + chi 1 + chi 2 + chi 3 = 0 := by decide

#print axioms invariantes_comunes_constantes
#print axioms chi_invariante_tres
#print axioms chi_invariante_cinco
#print axioms chi_no_invariante_dos
#print axioms chi_media_cero

end Frente20260910
