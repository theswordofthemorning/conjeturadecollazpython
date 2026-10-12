import Mathlib.Tactic.Linarith

/-! Obstrucción escalar natural del objetivo 57. No prueba terminación de H.
Las palabras ya están invertidas; la composición es de izquierda a derecha.
-/

namespace PerdicesProyeccionesMatrices

structure Afin where
  m : ℕ
  v : ℕ

def comp (a b : Afin) : Afin := ⟨a.m * b.m, a.m * b.v + a.v⟩

def debil (a b : Afin) : Prop := b.m ≤ a.m ∧ b.v ≤ a.v

structure Reglas (a b c d e f g : Afin) : Prop where
  da : debil (comp d a) d
  dbaa : debil (comp d (comp b (comp a a))) (comp d (comp a (comp b e)))
  dbba : debil (comp d (comp b (comp b a))) (comp d (comp b (comp a f)))
  fa : debil (comp f a) (comp b e)
  ga : debil (comp g a) (comp a f)
  eb : debil (comp e b) (comp b f)
  fb : debil (comp f b) (comp a g)
  ec : debil (comp e c) (comp b c)
  fc : debil (comp f c) (comp a (comp a c))

theorem pendientes {a b e f g : ℕ} (ha : 0 < a) (hb : 0 < b)
    (hfa : b * e ≤ f * a) (hga : a * f ≤ g * a)
    (heb : b * f ≤ e * b) (hfb : a * g ≤ f * b) :
    (f = 0 ∧ e = 0 ∧ g = 0) ∨ (a = b ∧ e = f ∧ g = f) := by
  have hfg : f ≤ g := (Nat.mul_le_mul_left_iff ha).mp (by simpa [Nat.mul_comm] using hga)
  have hfe : f ≤ e := (Nat.mul_le_mul_left_iff hb).mp (by simpa [Nat.mul_comm] using heb)
  by_cases hf : f = 0
  · left
    have he : b * e ≤ b * 0 := by simpa [hf] using hfa
    have hg : a * g ≤ a * 0 := by simpa [hf] using hfb
    exact ⟨hf, Nat.eq_zero_of_le_zero ((Nat.mul_le_mul_left_iff hb).mp he),
      Nat.eq_zero_of_le_zero ((Nat.mul_le_mul_left_iff ha).mp hg)⟩
  · have hfpos : 0 < f := Nat.pos_of_ne_zero hf
    have hba : b ≤ a := (Nat.mul_le_mul_left_iff hfpos).mp (by
      calc
        f * b = b * f := Nat.mul_comm _ _
        _ ≤ b * e := Nat.mul_le_mul_left _ hfe
        _ ≤ f * a := hfa)
    have hab : a ≤ b := (Nat.mul_le_mul_left_iff hfpos).mp (by
      calc
        f * a = a * f := Nat.mul_comm _ _
        _ ≤ a * g := Nat.mul_le_mul_left _ hfg
        _ ≤ f * b := hfb)
    have heq : a = b := Nat.le_antisymm hab hba
    subst b
    have hef : e ≤ f := (Nat.mul_le_mul_left_iff ha).mp (by simpa [Nat.mul_comm] using hfa)
    have hgf : g ≤ f := (Nat.mul_le_mul_left_iff ha).mp (by simpa [Nat.mul_comm] using hfb)
    exact Or.inr ⟨rfl, Nat.le_antisymm hef hfe, Nat.le_antisymm hgf hfg⟩

theorem constantes_pendiente_cero {p q a b e f g : ℕ} (hp : 1 ≤ p) (hq : 1 ≤ q)
    (hga : p * f + a ≤ g) (hfb : p * g + a ≤ f)
    (hfa : q * e + b ≤ f) (heb : q * f + b ≤ e) : a = 0 ∧ b = 0 := by
  have hpf : f ≤ p * f := by nlinarith
  have hpg : g ≤ p * g := by nlinarith
  have hqe : e ≤ q * e := by nlinarith
  have hqf : f ≤ q * f := by nlinarith
  omega

theorem cancelar_amplificacion {k a b : ℕ} (hk : 2 ≤ k)
    (h : k * b + a ≤ k * a + b) : b ≤ a := by
  by_contra hba
  have hab : a < b := by omega
  obtain ⟨r, hr⟩ := Nat.exists_eq_add_of_le (Nat.succ_le_of_lt hab)
  subst b
  nlinarith [Nat.mul_le_mul_right r hk]

theorem constantes_pendiente_comun {t s a b c e f : ℕ} (ht : 1 ≤ t) (hst : s ≤ t)
    (hec : t * c + b ≤ s * c + e)
    (hfc : t * (t * c + a) + a ≤ s * c + f)
    (h1 : t * (t * e + b) + a ≤ t * (t * a + a) + b)
    (h3 : t * (t * f + a) + b ≤ t * (t * a + b) + b) :
    a = 0 ∧ b = 0 := by
  have hsc : s * c ≤ t * c := Nat.mul_le_mul_right c hst
  have htt : t ≤ t * t := by nlinarith
  have hsc2 : s * c ≤ t * t * c := (Nat.mul_le_mul_right c hst).trans
    (Nat.mul_le_mul_right c htt)
  have heb : b ≤ e := by omega
  have hfa : 2 * a ≤ f := by nlinarith [Nat.mul_le_mul_right a ht]
  have hba : b ≤ a := cancelar_amplificacion (k := t * t + t) (by nlinarith)
    (by nlinarith [Nat.mul_le_mul_left (t * t) heb])
  have h3c : t * f + a ≤ t * a + b :=
    (Nat.mul_le_mul_left_iff (by omega : 0 < t)).mp (Nat.le_of_add_le_add_right h3)
  have hab : 2 * a ≤ b := by
    nlinarith [Nat.mul_le_mul_left t hfa, Nat.mul_le_mul_right a ht]
  omega

theorem sin_descenso_escalar (a b c d e f g : Afin) (h : Reglas a b c d e f g) :
    (comp d a).v = d.v ∧
    (comp d (comp b (comp a a))).v = (comp d (comp a (comp b e))).v ∧
    (comp d (comp b (comp b a))).v = (comp d (comp b (comp a f))).v := by
  by_cases hd : d.m = 0
  · simp [comp, hd]
  have hdpos : 0 < d.m := Nat.pos_of_ne_zero hd
  have ha : 1 ≤ a.m := (Nat.mul_le_mul_left_iff hdpos).mp (by
    simpa [debil, comp] using h.da.1)
  have h1 : a.m * (b.m * e.v + b.v) + a.v ≤ b.m * (a.m * a.v + a.v) + b.v :=
    (Nat.mul_le_mul_left_iff hdpos).mp (Nat.le_of_add_le_add_right h.dbaa.2)
  have h3 : b.m * (a.m * f.v + a.v) + b.v ≤ b.m * (b.m * a.v + b.v) + b.v :=
    (Nat.mul_le_mul_left_iff hdpos).mp (Nat.le_of_add_le_add_right h.dbba.2)
  by_cases hb : b.m = 0
  · simp only [hb, zero_mul, zero_add] at h1
    have hav : a.v = 0 := by nlinarith [Nat.mul_le_mul_right b.v ha]
    have hmul : a.m * b.v = b.v := by nlinarith [Nat.mul_le_mul_right b.v ha]
    simp [comp, hb, hav, hmul]
  have hab : a.v = 0 ∧ b.v = 0 := by
      have hbpos : 0 < b.m := Nat.pos_of_ne_zero hb
      rcases pendientes (by omega : 0 < a.m) hbpos h.fa.1 h.ga.1 h.eb.1 h.fb.1 with hz | heq
      · obtain ⟨hf, he, hg⟩ := hz
        apply constantes_pendiente_cero ha (by omega : 1 ≤ b.m)
        · simpa [debil, comp, hf, hg] using h.ga.2
        · simpa [debil, comp, hf, hg] using h.fb.2
        · simpa [debil, comp, hf, he] using h.fa.2
        · simpa [debil, comp, hf, he] using h.eb.2
      · obtain ⟨habm, hef, hgf⟩ := heq
        have hp : 0 < d.m * (a.m * b.m) := Nat.mul_pos hdpos (Nat.mul_pos (by omega) hbpos)
        have hema : e.m ≤ a.m := (Nat.mul_le_mul_left_iff hp).mp (by
          simpa [debil, comp, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using h.dbaa.1)
        apply constantes_pendiente_comun ha hema
        · simpa [comp, ← habm] using h.ec.2
        · simpa [comp, ← hef] using h.fc.2
        · simpa [← habm] using h1
        · simpa [← habm] using h3
  obtain ⟨hav, hbv⟩ := hab
  have he : a.m * (b.m * e.v) = 0 := by simpa [hav, hbv] using h1
  have hf : b.m * (a.m * f.v) = 0 := by simpa [hav, hbv] using h3
  simp [comp, hav, hbv, he, hf]

structure AfinDos where
  m00 : ℕ
  m01 : ℕ
  m10 : ℕ
  m11 : ℕ
  v0 : ℕ
  v1 : ℕ

def compDos (a b : AfinDos) : AfinDos :=
  ⟨a.m00 * b.m00 + a.m01 * b.m10, a.m00 * b.m01 + a.m01 * b.m11,
   a.m10 * b.m00 + a.m11 * b.m10, a.m10 * b.m01 + a.m11 * b.m11,
   a.m00 * b.v0 + a.m01 * b.v1 + a.v0, a.m10 * b.v0 + a.m11 * b.v1 + a.v1⟩

def primera (a : AfinDos) : Afin := ⟨a.m00, a.v0⟩

def debilDos (a b : AfinDos) : Prop :=
  b.m00 ≤ a.m00 ∧ b.m01 ≤ a.m01 ∧ b.m10 ≤ a.m10 ∧ b.m11 ≤ a.m11 ∧
  b.v0 ≤ a.v0 ∧ b.v1 ≤ a.v1

theorem proyeccion_producto (a b : AfinDos) (ha : a.m01 = 0) :
    primera (compDos a b) = comp (primera a) (primera b) := by
  simp [primera, compDos, comp, ha]

theorem proyeccion_debil (a b : AfinDos) (h : debilDos a b) :
    debil (primera a) (primera b) := ⟨h.1, h.2.2.2.2.1⟩

structure ReglasDos (a b c d e f g : AfinDos) : Prop where
  da : debilDos (compDos d a) d
  dbaa : debilDos (compDos d (compDos b (compDos a a)))
    (compDos d (compDos a (compDos b e)))
  dbba : debilDos (compDos d (compDos b (compDos b a)))
    (compDos d (compDos b (compDos a f)))
  fa : debilDos (compDos f a) (compDos b e)
  ga : debilDos (compDos g a) (compDos a f)
  eb : debilDos (compDos e b) (compDos b f)
  fb : debilDos (compDos f b) (compDos a g)
  ec : debilDos (compDos e c) (compDos b c)
  fc : debilDos (compDos f c) (compDos a (compDos a c))

theorem reglas_proyectadas (a b c d e f g : AfinDos)
    (ha : a.m01 = 0) (hb : b.m01 = 0) (hd : d.m01 = 0)
    (he : e.m01 = 0) (hf : f.m01 = 0) (hg : g.m01 = 0)
    (h : ReglasDos a b c d e f g) :
    Reglas (primera a) (primera b) (primera c) (primera d)
      (primera e) (primera f) (primera g) := by
  constructor
  all_goals first
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.da
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.dbaa
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.dbba
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.fa
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.ga
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.eb
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.fb
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.ec
    | simpa only [proyeccion_producto _ _ ha, proyeccion_producto _ _ hb,
        proyeccion_producto _ _ hd, proyeccion_producto _ _ he,
        proyeccion_producto _ _ hf, proyeccion_producto _ _ hg] using
          proyeccion_debil _ _ h.fc

theorem sin_descenso_primera_aislada (a b c d e f g : AfinDos)
    (ha : a.m01 = 0) (hb : b.m01 = 0) (hd : d.m01 = 0)
    (he : e.m01 = 0) (hf : f.m01 = 0) (hg : g.m01 = 0)
    (h : ReglasDos a b c d e f g) :
    (compDos d a).v0 = d.v0 ∧
    (compDos d (compDos b (compDos a a))).v0 =
      (compDos d (compDos a (compDos b e))).v0 ∧
    (compDos d (compDos b (compDos b a))).v0 =
      (compDos d (compDos b (compDos a f))).v0 := by
  have resultado := sin_descenso_escalar _ _ _ _ _ _ _
    (reglas_proyectadas a b c d e f g ha hb hd he hf hg h)
  simpa [comp, primera, compDos, ha, hb, hd] using resultado

theorem acoplamiento_necesario (a b c d e f g : AfinDos)
    (h : ReglasDos a b c d e f g)
    (hestricta : d.v0 < (compDos d a).v0 ∨
      (compDos d (compDos a (compDos b e))).v0 <
        (compDos d (compDos b (compDos a a))).v0 ∨
      (compDos d (compDos b (compDos a f))).v0 <
        (compDos d (compDos b (compDos b a))).v0) :
    0 < a.m01 + b.m01 + d.m01 + e.m01 + f.m01 + g.m01 := by
  by_contra hn
  have ha : a.m01 = 0 := by omega
  have hb : b.m01 = 0 := by omega
  have hd : d.m01 = 0 := by omega
  have he : e.m01 = 0 := by omega
  have hf : f.m01 = 0 := by omega
  have hg : g.m01 = 0 := by omega
  have resultado := sin_descenso_primera_aislada a b c d e f g ha hb hd he hf hg h
  rcases hestricta with h1 | h2 | h3 <;> omega

#print axioms pendientes
#print axioms constantes_pendiente_cero
#print axioms cancelar_amplificacion
#print axioms constantes_pendiente_comun
#print axioms sin_descenso_escalar
#print axioms proyeccion_producto
#print axioms proyeccion_debil
#print axioms reglas_proyectadas
#print axioms sin_descenso_primera_aislada
#print axioms acoplamiento_necesario

end PerdicesProyeccionesMatrices
