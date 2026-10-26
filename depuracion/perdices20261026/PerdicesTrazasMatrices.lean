import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Rigidez de las seis reglas de intercambio en dimension dos.
Se trata de matrices de coeficientes; no de un certificado de terminacion. -/

namespace PerdicesTrazasMatrices

structure Matriz where
  m00 : ℝ
  m01 : ℝ
  m10 : ℝ
  m11 : ℝ

def sumar (u v : Matriz) : Matriz :=
  ⟨u.m00 + v.m00, u.m01 + v.m01, u.m10 + v.m10, u.m11 + v.m11⟩

noncomputable def producto (u v : Matriz) : Matriz :=
  ⟨u.m00 * v.m00 + u.m01 * v.m10, u.m00 * v.m01 + u.m01 * v.m11,
   u.m10 * v.m00 + u.m11 * v.m10, u.m10 * v.m01 + u.m11 * v.m11⟩

def debil (u v : Matriz) : Prop :=
  v.m00 ≤ u.m00 ∧ v.m01 ≤ u.m01 ∧ v.m10 ≤ u.m10 ∧ v.m11 ≤ u.m11

theorem igualdad_matriz (u v : Matriz)
    (h00 : u.m00 = v.m00) (h01 : u.m01 = v.m01)
    (h10 : u.m10 = v.m10) (h11 : u.m11 = v.m11) : u = v := by
  cases u
  cases v
  simp_all

theorem diagonales_iguales (u v : Matriz) (h : debil (producto v u) (producto u v)) :
    (producto v u).m00 = (producto u v).m00 ∧
    (producto v u).m11 = (producto u v).m11 := by
  rcases h with ⟨h00, _, _, h11⟩
  dsimp [producto] at *
  constructor <;> nlinarith

theorem traza_ponderada (u v : Matriz) :
    ((producto v u).m00 - (producto u v).m00) * (u.m00 + v.m00) +
    ((producto v u).m01 - (producto u v).m01) * (u.m10 + v.m10) +
    ((producto v u).m10 - (producto u v).m10) * (u.m01 + v.m01) +
    ((producto v u).m11 - (producto u v).m11) * (u.m11 + v.m11) = 0 := by
  dsimp [producto]
  ring

theorem holgura_cruzada (u v : Matriz) (h : debil (producto v u) (producto u v)) :
    ((producto v u).m01 - (producto u v).m01) * (u.m10 + v.m10) +
    ((producto v u).m10 - (producto u v).m10) * (u.m01 + v.m01) = 0 := by
  have hd := diagonales_iguales u v h
  have ht := traza_ponderada u v
  rw [hd.1, hd.2] at ht
  simpa using ht

theorem conmutan_si_conectadas (u v : Matriz)
    (h : debil (producto v u) (producto u v))
    (h01 : 0 < u.m01 + v.m01) (h10 : 0 < u.m10 + v.m10) :
    producto v u = producto u v := by
  have hd := diagonales_iguales u v h
  have ht := holgura_cruzada u v h
  have hp : 0 ≤ (producto v u).m01 - (producto u v).m01 := sub_nonneg.mpr h.2.1
  have hq : 0 ≤ (producto v u).m10 - (producto u v).m10 := sub_nonneg.mpr h.2.2.1
  have ep : (producto v u).m01 = (producto u v).m01 := by
    nlinarith [mul_nonneg hp (le_of_lt h10), mul_nonneg hq (le_of_lt h01)]
  have eq : (producto v u).m10 = (producto u v).m10 := by
    nlinarith [mul_nonneg hp (le_of_lt h10), mul_nonneg hq (le_of_lt h01)]
  exact igualdad_matriz _ _ hd.1 ep eq hd.2

structure Intercambios (a b e f g : Matriz) : Prop where
  ea : debil (producto e a) (producto a e)
  fa : debil (producto f a) (producto b e)
  ga : debil (producto g a) (producto a f)
  eb : debil (producto e b) (producto b f)
  fb : debil (producto f b) (producto a g)
  gb : debil (producto g b) (producto b g)

theorem conmutador_no_negativo (a b e f g : Matriz) (h : Intercambios a b e f g) :
    debil (producto (sumar (sumar e f) g) (sumar a b))
      (producto (sumar a b) (sumar (sumar e f) g)) := by
  rcases h with ⟨hea, hfa, hga, heb, hfb, hgb⟩
  rcases hea with ⟨a0, a1, a2, a3⟩
  rcases hfa with ⟨b0, b1, b2, b3⟩
  rcases hga with ⟨c0, c1, c2, c3⟩
  rcases heb with ⟨d0, d1, d2, d3⟩
  rcases hfb with ⟨e0, e1, e2, e3⟩
  rcases hgb with ⟨f0, f1, f2, f3⟩
  dsimp [debil, producto, sumar] at *
  refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith

theorem componente_sin_holgura (l1 l2 l3 l4 l5 l6 r1 r2 r3 r4 r5 r6 : ℝ)
    (h1 : r1 ≤ l1) (h2 : r2 ≤ l2) (h3 : r3 ≤ l3)
    (h4 : r4 ≤ l4) (h5 : r5 ≤ l5) (h6 : r6 ≤ l6)
    (hs : l1 + l2 + l3 + l4 + l5 + l6 = r1 + r2 + r3 + r4 + r5 + r6) :
    l1 = r1 ∧ l2 = r2 ∧ l3 = r3 ∧ l4 = r4 ∧ l5 = r5 ∧ l6 = r6 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> linarith

theorem intercambios_iguales_si_conectadas (a b e f g : Matriz)
    (h : Intercambios a b e f g)
    (h01 : 0 < a.m01 + b.m01 + e.m01 + f.m01 + g.m01)
    (h10 : 0 < a.m10 + b.m10 + e.m10 + f.m10 + g.m10) :
    producto e a = producto a e ∧
    producto f a = producto b e ∧
    producto g a = producto a f ∧
    producto e b = producto b f ∧
    producto f b = producto a g ∧
    producto g b = producto b g := by
  have hc := conmutan_si_conectadas (sumar a b) (sumar (sumar e f) g)
    (conmutador_no_negativo a b e f g h)
    (by simpa [sumar, add_assoc] using h01)
    (by simpa [sumar, add_assoc] using h10)
  have hs0 : (producto e a).m00 + (producto f a).m00 + (producto g a).m00 + (producto e b).m00 + (producto f b).m00 + (producto g b).m00 =
      (producto a e).m00 + (producto b e).m00 + (producto a f).m00 + (producto b f).m00 + (producto a g).m00 + (producto b g).m00 := by
    have he := congrArg Matriz.m00 hc
    dsimp [producto, sumar] at he
    dsimp [producto]
    nlinarith only [he]
  have h0 := componente_sin_holgura (producto e a).m00 (producto f a).m00 (producto g a).m00 (producto e b).m00 (producto f b).m00 (producto g b).m00
    (producto a e).m00 (producto b e).m00 (producto a f).m00 (producto b f).m00 (producto a g).m00 (producto b g).m00
    h.ea.1 h.fa.1 h.ga.1 h.eb.1 h.fb.1 h.gb.1 hs0
  have hs1 : (producto e a).m01 + (producto f a).m01 + (producto g a).m01 + (producto e b).m01 + (producto f b).m01 + (producto g b).m01 =
      (producto a e).m01 + (producto b e).m01 + (producto a f).m01 + (producto b f).m01 + (producto a g).m01 + (producto b g).m01 := by
    have he := congrArg Matriz.m01 hc
    dsimp [producto, sumar] at he
    dsimp [producto]
    nlinarith only [he]
  have h1 := componente_sin_holgura (producto e a).m01 (producto f a).m01 (producto g a).m01 (producto e b).m01 (producto f b).m01 (producto g b).m01
    (producto a e).m01 (producto b e).m01 (producto a f).m01 (producto b f).m01 (producto a g).m01 (producto b g).m01
    h.ea.2.1 h.fa.2.1 h.ga.2.1 h.eb.2.1 h.fb.2.1 h.gb.2.1 hs1
  have hs2 : (producto e a).m10 + (producto f a).m10 + (producto g a).m10 + (producto e b).m10 + (producto f b).m10 + (producto g b).m10 =
      (producto a e).m10 + (producto b e).m10 + (producto a f).m10 + (producto b f).m10 + (producto a g).m10 + (producto b g).m10 := by
    have he := congrArg Matriz.m10 hc
    dsimp [producto, sumar] at he
    dsimp [producto]
    nlinarith only [he]
  have h2 := componente_sin_holgura (producto e a).m10 (producto f a).m10 (producto g a).m10 (producto e b).m10 (producto f b).m10 (producto g b).m10
    (producto a e).m10 (producto b e).m10 (producto a f).m10 (producto b f).m10 (producto a g).m10 (producto b g).m10
    h.ea.2.2.1 h.fa.2.2.1 h.ga.2.2.1 h.eb.2.2.1 h.fb.2.2.1 h.gb.2.2.1 hs2
  have hs3 : (producto e a).m11 + (producto f a).m11 + (producto g a).m11 + (producto e b).m11 + (producto f b).m11 + (producto g b).m11 =
      (producto a e).m11 + (producto b e).m11 + (producto a f).m11 + (producto b f).m11 + (producto a g).m11 + (producto b g).m11 := by
    have he := congrArg Matriz.m11 hc
    dsimp [producto, sumar] at he
    dsimp [producto]
    nlinarith only [he]
  have h3 := componente_sin_holgura (producto e a).m11 (producto f a).m11 (producto g a).m11 (producto e b).m11 (producto f b).m11 (producto g b).m11
    (producto a e).m11 (producto b e).m11 (producto a f).m11 (producto b f).m11 (producto a g).m11 (producto b g).m11
    h.ea.2.2.2 h.fa.2.2.2 h.ga.2.2.2 h.eb.2.2.2 h.fb.2.2.2 h.gb.2.2.2 hs3
  exact ⟨igualdad_matriz _ _ h0.1 h1.1 h2.1 h3.1,
    igualdad_matriz _ _ h0.2.1 h1.2.1 h2.2.1 h3.2.1,
    igualdad_matriz _ _ h0.2.2.1 h1.2.2.1 h2.2.2.1 h3.2.2.1,
    igualdad_matriz _ _ h0.2.2.2.1 h1.2.2.2.1 h2.2.2.2.1 h3.2.2.2.1,
    igualdad_matriz _ _ h0.2.2.2.2.1 h1.2.2.2.2.1 h2.2.2.2.2.1 h3.2.2.2.2.1,
    igualdad_matriz _ _ h0.2.2.2.2.2 h1.2.2.2.2.2 h2.2.2.2.2.2 h3.2.2.2.2.2⟩

/- Núcleo escalar ponderado para M_a=M_b=t I. No presupone que los
vectores de las letras conserven una recta afín. -/
theorem constantes_binarias_escalares
    (t x y z w c p : ℝ) (ht : 1 ≤ t) (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hz : 0 ≤ z) (hw : 0 ≤ w) (hc : 0 ≤ c)
    (hp : p ≤ t * c) (he : t * c + y ≤ p + z)
    (hf : t * t * c + (t + 1) * x ≤ p + w)
    (h2 : t * t * z + t * y + x ≤ t * t * x + t * x + y)
    (h3 : x + t * w ≤ t * x + y) :
    x = 0 ∧ y = 0 ∧
    t * t * x + t * x + y - (t * t * z + t * y + x) = 0 ∧
    t * (t * x + y - (x + t * w)) = 0 := by
  have ht0 : 0 < t := by linarith
  have ht2 : 0 < t * t + t - 1 := by nlinarith [sq_nonneg t]
  have hey : y ≤ z := by linarith
  have htc : t * c ≤ t * t * c := by
    nlinarith [mul_nonneg (sub_nonneg.mpr ht) (mul_nonneg (le_of_lt ht0) hc)]
  have hfw : (t + 1) * x ≤ w := by linarith
  have hfx : 2 * x ≤ w := by nlinarith [mul_nonneg (sub_nonneg.mpr ht) hx]
  have hyx : y ≤ x := by
    by_contra h
    have hxy : 0 < y - x := by linarith
    have hpz : 0 ≤ t * t * (z - y) :=
      mul_nonneg (mul_nonneg (le_of_lt ht0) (le_of_lt ht0)) (sub_nonneg.mpr hey)
    nlinarith [mul_pos ht2 hxy]
  have hxx : 2 * x ≤ y := by
    nlinarith [mul_nonneg (le_of_lt ht0) (sub_nonneg.mpr hfx),
      mul_nonneg (sub_nonneg.mpr ht) hx]
  have ex : x = 0 := by linarith
  have ey : y = 0 := by linarith
  have ez : z = 0 := by
    rw [ex, ey] at h2
    nlinarith [mul_pos ht0 ht0]
  have ew : w = 0 := by
    rw [ex, ey] at h3
    nlinarith
  simp [ex, ey, ez, ew]

end PerdicesTrazasMatrices

#print axioms PerdicesTrazasMatrices.igualdad_matriz
#print axioms PerdicesTrazasMatrices.diagonales_iguales
#print axioms PerdicesTrazasMatrices.traza_ponderada
#print axioms PerdicesTrazasMatrices.holgura_cruzada
#print axioms PerdicesTrazasMatrices.conmutan_si_conectadas
#print axioms PerdicesTrazasMatrices.conmutador_no_negativo
#print axioms PerdicesTrazasMatrices.componente_sin_holgura
#print axioms PerdicesTrazasMatrices.intercambios_iguales_si_conectadas
#print axioms PerdicesTrazasMatrices.constantes_binarias_escalares
