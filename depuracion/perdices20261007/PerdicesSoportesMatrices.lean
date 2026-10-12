import PerdicesProyeccionesMatrices
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Tauto

/-! Soportes que alimentan las constantes dinámicas y rectas invariantes.
No afirma la existencia de una interpretación estricta ni la terminación de H.
-/

namespace PerdicesSoportesMatrices

open PerdicesProyeccionesMatrices

-- El rayo discreto es {(x, k*x+t) : x : ℕ}.
def conservaRecta (k t : ℕ) (a : AfinDos) : Prop :=
  a.m10 + a.m11 * k = k * (a.m00 + a.m01 * k) ∧
  a.m11 * t + a.v1 = k * (a.m01 * t + a.v0) + t

def proyectar (k t : ℕ) (a : AfinDos) : Afin :=
  ⟨a.m00 + a.m01 * k, a.m01 * t + a.v0⟩

theorem producto_proyectado (k t : ℕ) (a b : AfinDos)
    (hb : conservaRecta k t b) :
    proyectar k t (compDos a b) = comp (proyectar k t a) (proyectar k t b) := by
  rcases hb with ⟨hm, hv⟩
  unfold proyectar comp
  congr 1
  · dsimp [proyectar, compDos, comp]
    calc
      _ = a.m00 * (b.m00 + b.m01 * k) + a.m01 * (b.m10 + b.m11 * k) := by ring
      _ = _ := by rw [hm]; ring
  · dsimp [proyectar, compDos, comp]
    calc
      _ = a.m00 * (b.m01 * t + b.v0) + a.m01 * (b.m11 * t + b.v1) + a.v0 := by ring
      _ = _ := by rw [hv]; ring

theorem conserva_producto (k t : ℕ) (a b : AfinDos)
    (ha : conservaRecta k t a) (hb : conservaRecta k t b) :
    conservaRecta k t (compDos a b) := by
  rcases ha with ⟨ham, hav⟩
  rcases hb with ⟨hbm, hbv⟩
  constructor
  · dsimp [compDos]
    calc
      _ = a.m10 * (b.m00 + b.m01 * k) + a.m11 * (b.m10 + b.m11 * k) := by ring
      _ = (a.m10 + a.m11 * k) * (b.m00 + b.m01 * k) := by rw [hbm]; ring
      _ = k * ((a.m00 + a.m01 * k) * (b.m00 + b.m01 * k)) := by rw [ham]; ring
      _ = k * (a.m00 * (b.m00 + b.m01 * k) + a.m01 * (k * (b.m00 + b.m01 * k))) := by ring
      _ = _ := by rw [← hbm]; ring
  · dsimp [compDos]
    calc
      _ = a.m10 * (b.m01 * t + b.v0) + a.m11 * (b.m11 * t + b.v1) + a.v1 := by ring
      _ = (a.m10 + a.m11 * k) * (b.m01 * t + b.v0) + (a.m11 * t + a.v1) := by rw [hbv]; ring
      _ = k * ((a.m00 + a.m01 * k) * (b.m01 * t + b.v0) + (a.m01 * t + a.v0)) + t := by
        rw [ham, hav]; ring
      _ = k * (a.m00 * (b.m01 * t + b.v0) + a.m01 * (k * (b.m01 * t + b.v0) + t) + a.v0) + t := by ring
      _ = _ := by rw [← hbv]; ring

theorem orden_proyectado (k t : ℕ) (a b : AfinDos) (h : debilDos a b) :
    debil (proyectar k t a) (proyectar k t b) := by
  exact ⟨Nat.add_le_add h.1 (Nat.mul_le_mul_right k h.2.1),
    Nat.add_le_add (Nat.mul_le_mul_right t h.2.1) h.2.2.2.2.1⟩

theorem reglas_en_recta (k t : ℕ) (a b c d e f g : AfinDos)
    (ha : conservaRecta k t a) (hb : conservaRecta k t b)
    (hc : conservaRecta k t c) (he : conservaRecta k t e)
    (hf : conservaRecta k t f) (hg : conservaRecta k t g)
    (h : ReglasDos a b c d e f g) :
    Reglas (proyectar k t a) (proyectar k t b) (proyectar k t c)
      (proyectar k t d) (proyectar k t e) (proyectar k t f) (proyectar k t g) := by
  have haa := conserva_producto k t a a ha ha
  have hba := conserva_producto k t b a hb ha
  have hbe := conserva_producto k t b e hb he
  have haf := conserva_producto k t a f ha hf
  have hbaa := conserva_producto k t b (compDos a a) hb haa
  have habe := conserva_producto k t a (compDos b e) ha hbe
  have hbba := conserva_producto k t b (compDos b a) hb hba
  have hbaf := conserva_producto k t b (compDos a f) hb haf
  have hac := conserva_producto k t a c ha hc
  constructor
  all_goals first
    | simpa only [producto_proyectado _ _ _ _ ha] using orden_proyectado k t _ _ h.da
    | simpa only [producto_proyectado _ _ _ _ hbaa, producto_proyectado _ _ _ _ habe,
        producto_proyectado _ _ _ _ haa, producto_proyectado _ _ _ _ hbe,
        producto_proyectado _ _ _ _ ha, producto_proyectado _ _ _ _ he] using
          orden_proyectado k t _ _ h.dbaa
    | simpa only [producto_proyectado _ _ _ _ hbba, producto_proyectado _ _ _ _ hbaf,
        producto_proyectado _ _ _ _ hba, producto_proyectado _ _ _ _ haf,
        producto_proyectado _ _ _ _ ha, producto_proyectado _ _ _ _ hf] using
          orden_proyectado k t _ _ h.dbba
    | simpa only [producto_proyectado _ _ _ _ ha, producto_proyectado _ _ _ _ he] using
          orden_proyectado k t _ _ h.fa
    | simpa only [producto_proyectado _ _ _ _ ha, producto_proyectado _ _ _ _ hf] using
          orden_proyectado k t _ _ h.ga
    | simpa only [producto_proyectado _ _ _ _ hb, producto_proyectado _ _ _ _ hf] using
          orden_proyectado k t _ _ h.eb
    | simpa only [producto_proyectado _ _ _ _ hb, producto_proyectado _ _ _ _ hg] using
          orden_proyectado k t _ _ h.fb
    | simpa only [producto_proyectado _ _ _ _ hc] using orden_proyectado k t _ _ h.ec
    | simpa only [producto_proyectado _ _ _ _ hc, producto_proyectado _ _ _ _ hac] using
          orden_proyectado k t _ _ h.fc

theorem igualdad_constante_original (k t : ℕ) (a b : AfinDos)
    (h : debilDos a b) (heq : (proyectar k t a).v = (proyectar k t b).v) :
    a.v0 = b.v0 := by
  have hm := Nat.mul_le_mul_right t h.2.1
  have hv := h.2.2.2.2.1
  dsimp [proyectar] at heq
  omega

def igualesDinamicas (a b d e f : AfinDos) : Prop :=
  (compDos d a).v0 = d.v0 ∧
  (compDos d (compDos b (compDos a a))).v0 =
    (compDos d (compDos a (compDos b e))).v0 ∧
  (compDos d (compDos b (compDos b a))).v0 =
    (compDos d (compDos b (compDos a f))).v0

theorem sin_descenso_recta (k t : ℕ) (a b c d e f g : AfinDos)
    (ha : conservaRecta k t a) (hb : conservaRecta k t b)
    (hc : conservaRecta k t c) (he : conservaRecta k t e)
    (hf : conservaRecta k t f) (hg : conservaRecta k t g)
    (h : ReglasDos a b c d e f g) : igualesDinamicas a b d e f := by
  have hp := sin_descenso_escalar _ _ _ _ _ _ _
    (reglas_en_recta k t a b c d e f g ha hb hc he hf hg h)
  have haa := conserva_producto k t a a ha ha
  have hba := conserva_producto k t b a hb ha
  have hbe := conserva_producto k t b e hb he
  have haf := conserva_producto k t a f ha hf
  have hbaa := conserva_producto k t b (compDos a a) hb haa
  have habe := conserva_producto k t a (compDos b e) ha hbe
  have hbba := conserva_producto k t b (compDos b a) hb hba
  have hbaf := conserva_producto k t b (compDos a f) hb haf
  refine ⟨igualdad_constante_original k t _ _ h.da ?_,
    igualdad_constante_original k t _ _ h.dbaa ?_,
    igualdad_constante_original k t _ _ h.dbba ?_⟩
  · simpa only [producto_proyectado _ _ _ _ ha] using hp.1
  · simpa only [producto_proyectado _ _ _ _ hbaa, producto_proyectado _ _ _ _ habe,
        producto_proyectado _ _ _ _ haa, producto_proyectado _ _ _ _ hbe,
        producto_proyectado _ _ _ _ ha, producto_proyectado _ _ _ _ he] using hp.2.1
  · simpa only [producto_proyectado _ _ _ _ hbba, producto_proyectado _ _ _ _ hbaf,
        producto_proyectado _ _ _ _ hba, producto_proyectado _ _ _ _ haf,
        producto_proyectado _ _ _ _ ha, producto_proyectado _ _ _ _ hf] using hp.2.2

theorem recta_cero (a : AfinDos) (hm : a.m10 = 0) (hv : a.v1 = 0) :
    conservaRecta 0 0 a := by simp [conservaRecta, hm, hv]

theorem recta_diagonal (a : AfinDos)
    (hm : a.m10 + a.m11 = a.m00 + a.m01) (hv : a.v1 = a.v0) :
    conservaRecta 1 0 a := by simpa [conservaRecta] using And.intro hm hv

theorem sin_descenso_segunda_inactiva (a b c d e f g : AfinDos)
    (hz : a.m10 + b.m10 + c.m10 + e.m10 + f.m10 + g.m10 +
      a.v1 + b.v1 + c.v1 + e.v1 + f.v1 + g.v1 = 0)
    (h : ReglasDos a b c d e f g) : igualesDinamicas a b d e f := by
  apply sin_descenso_recta 0 0 a b c d e f g ?_ ?_ ?_ ?_ ?_ ?_ h
  all_goals apply recta_cero <;> omega

theorem sin_descenso_diagonal (a b c d e f g : AfinDos)
    (ha : a.m10 + a.m11 = a.m00 + a.m01 ∧ a.v1 = a.v0)
    (hb : b.m10 + b.m11 = b.m00 + b.m01 ∧ b.v1 = b.v0)
    (hc : c.m10 + c.m11 = c.m00 + c.m01 ∧ c.v1 = c.v0)
    (he : e.m10 + e.m11 = e.m00 + e.m01 ∧ e.v1 = e.v0)
    (hf : f.m10 + f.m11 = f.m00 + f.m01 ∧ f.v1 = f.v0)
    (hg : g.m10 + g.m11 = g.m00 + g.m01 ∧ g.v1 = g.v0)
    (h : ReglasDos a b c d e f g) : igualesDinamicas a b d e f :=
  sin_descenso_recta 1 0 a b c d e f g
    (recta_diagonal a ha.1 ha.2) (recta_diagonal b hb.1 hb.2)
    (recta_diagonal c hc.1 hc.2) (recta_diagonal e he.1 he.2)
    (recta_diagonal f hf.1 hf.2) (recta_diagonal g hg.1 hg.2) h

-- Aportes positivos de los lados izquierdos, sin la constante exterior de d.
def aporteTotal (a b d : AfinDos) : ℕ :=
  d.m00 * a.v0 + d.m01 * a.v1 +
  d.m00 * (compDos b (compDos a a)).v0 + d.m01 * (compDos b (compDos a a)).v1 +
  d.m00 * (compDos b (compDos b a)).v0 + d.m01 * (compDos b (compDos b a)).v1

def rutasMinimas (a b d : AfinDos) : Prop :=
  0 < d.m00 * a.v0 ∨ 0 < d.m01 * a.v1 ∨
  0 < d.m00 * b.v0 ∨ 0 < d.m01 * b.v1 ∨
  0 < d.m00 * b.m01 * a.v1 ∨ 0 < d.m01 * b.m10 * a.v0 ∨
  0 < d.m00 * b.m01 * b.v1 ∨ 0 < d.m01 * b.m10 * b.v0 ∨
  0 < d.m00 * b.m00 * a.m01 * a.v1 ∨
  0 < d.m01 * b.m11 * a.m10 * a.v0

theorem producto_positivo (x y : ℕ) : 0 < x * y ↔ 0 < x ∧ 0 < y := by
  simp only [Nat.pos_iff_ne_zero, ne_eq, Nat.mul_eq_zero, not_or]

set_option maxHeartbeats 2000000 in
theorem soporte_aporte_exacto (a b d : AfinDos) :
    0 < aporteTotal a b d ↔ rutasMinimas a b d := by
  simp only [aporteTotal, rutasMinimas, compDos, Nat.add_pos_iff_pos_or_pos, producto_positivo]
  simp only [and_or_left]
  aesop

theorem descenso_exige_aporte (a b d e f : AfinDos)
    (h : d.v0 < (compDos d a).v0 ∨
      (compDos d (compDos a (compDos b e))).v0 <
        (compDos d (compDos b (compDos a a))).v0 ∨
      (compDos d (compDos b (compDos a f))).v0 <
        (compDos d (compDos b (compDos b a))).v0) :
    0 < aporteTotal a b d := by
  dsimp [aporteTotal]
  rcases h with h | h | h <;> simp only [compDos] at h ⊢ <;> omega

theorem descenso_exige_ruta (a b d e f : AfinDos)
    (h : d.v0 < (compDos d a).v0 ∨
      (compDos d (compDos a (compDos b e))).v0 <
        (compDos d (compDos b (compDos a a))).v0 ∨
      (compDos d (compDos b (compDos a f))).v0 <
        (compDos d (compDos b (compDos b a))).v0) : rutasMinimas a b d :=
  (soporte_aporte_exacto a b d).mp (descenso_exige_aporte a b d e f h)

#print axioms producto_proyectado
#print axioms conserva_producto
#print axioms orden_proyectado
#print axioms reglas_en_recta
#print axioms igualdad_constante_original
#print axioms sin_descenso_recta
#print axioms recta_cero
#print axioms recta_diagonal
#print axioms sin_descenso_segunda_inactiva
#print axioms sin_descenso_diagonal
#print axioms producto_positivo
#print axioms soporte_aporte_exacto
#print axioms descenso_exige_aporte
#print axioms descenso_exige_ruta

end PerdicesSoportesMatrices
