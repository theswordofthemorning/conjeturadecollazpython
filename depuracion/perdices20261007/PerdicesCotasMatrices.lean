import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset

/-! # Cotas de productos de matrices naturales.

Una palabra es una lista de matrices cuadradas de dimensión m; cada entrada
es natural. Si cada coeficiente de símbolo es <=C y m*C>=1, toda entrada
de una palabra de largo <=L es <=(m*C)^L. Para el buscador natural m=d+1,
incluyendo la fila aumentada afín (0,...,0,1), y C>=1.

No se formaliza la traducción Python/BitVec ni la interpretación ártica.
-/

namespace PerdicesCotasMatrices

open scoped BigOperators

def Matriz (m : ℕ) := Fin m → Fin m → ℕ

def producto {m : ℕ} (a b : Matriz m) : Matriz m :=
  fun i j => ∑ k, a i k * b k j

def fila {m : ℕ} (a : Matriz m) (i : Fin m) : ℕ := ∑ j, a i j

def identidad {m : ℕ} : Matriz m := fun i j => if j = i then 1 else 0

def palabra {m : ℕ} : List (Matriz m) → Matriz m
  | [] => identidad
  | a :: resto => producto a (palabra resto)

theorem entrada_le_fila {m : ℕ} (a : Matriz m) (i j : Fin m) : a i j ≤ fila a i := by
  exact Finset.single_le_sum (fun k _ => Nat.zero_le (a i k)) (Finset.mem_univ j)

theorem fila_producto {m u v : ℕ} (a b : Matriz m) (i : Fin m)
    (ha : fila a i ≤ u) (hb : ∀ j, fila b j ≤ v) : fila (producto a b) i ≤ u * v := by
  calc
    fila (producto a b) i = ∑ k, a i k * fila b k := by
      simp only [fila, producto]
      rw [Finset.sum_comm]
      simp only [Finset.mul_sum]
    _ ≤ ∑ k, a i k * v := Finset.sum_le_sum (fun k _ => Nat.mul_le_mul_left _ (hb k))
    _ = fila a i * v := by simp [fila, Finset.sum_mul]
    _ ≤ u * v := Nat.mul_le_mul_right v ha

theorem fila_identidad {m : ℕ} (i : Fin m) : fila identidad i = 1 := by
  simp [fila, identidad]

theorem fila_palabra {m k : ℕ} (letras : List (Matriz m))
    (h : ∀ a ∈ letras, ∀ i, fila a i ≤ k) (i : Fin m) :
    fila (palabra letras) i ≤ k ^ letras.length := by
  induction letras generalizing i with
  | nil => simp [palabra, fila_identidad]
  | cons a resto ih =>
    have ha : fila a i ≤ k := h a (by simp) i
    have hr : ∀ b ∈ resto, ∀ j, fila b j ≤ k := fun b hb => h b (by simp [hb])
    have hprod := fila_producto a (palabra resto) i ha (fun j => ih hr j)
    simpa [palabra, pow_succ, Nat.mul_comm] using hprod

theorem fila_por_coeficientes {m c : ℕ} (a : Matriz m)
    (h : ∀ i j, a i j ≤ c) (i : Fin m) : fila a i ≤ m * c := by
  calc
    fila a i ≤ ∑ _j : Fin m, c := Finset.sum_le_sum (fun j _ => h i j)
    _ = m * c := by simp

theorem entrada_palabra {m c : ℕ} (letras : List (Matriz m))
    (h : ∀ a ∈ letras, ∀ i j, a i j ≤ c) (i j : Fin m) :
    palabra letras i j ≤ (m * c) ^ letras.length := by
  exact (entrada_le_fila _ i j).trans
    (fila_palabra letras (fun a ha r => fila_por_coeficientes a (h a ha) r) i)

theorem entrada_largo_acotado {m c l : ℕ} (letras : List (Matriz m))
    (h : ∀ a ∈ letras, ∀ i j, a i j ≤ c) (hk : 1 ≤ m * c)
    (hl : letras.length ≤ l) (i j : Fin m) : palabra letras i j ≤ (m * c) ^ l := by
  exact (entrada_palabra letras h i j).trans (Nat.pow_le_pow_right hk hl)

theorem entrada_cabe_en_bits {m c l w : ℕ} (letras : List (Matriz m))
    (h : ∀ a ∈ letras, ∀ i j, a i j ≤ c) (hk : 1 ≤ m * c)
    (hl : letras.length ≤ l) (hw : (m * c) ^ l < 2 ^ w) (i j : Fin m) :
    palabra letras i j < 2 ^ w :=
  (entrada_largo_acotado letras h hk hl i j).trans_lt hw

#print axioms entrada_le_fila
#print axioms fila_producto
#print axioms fila_identidad
#print axioms fila_palabra
#print axioms fila_por_coeficientes
#print axioms entrada_palabra
#print axioms entrada_largo_acotado
#print axioms entrada_cabe_en_bits

end PerdicesCotasMatrices
