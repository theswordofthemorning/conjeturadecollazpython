import Mathlib.Data.List.Basic
import Mathlib.Data.Fintype.Vector
import Mathlib.Data.Rat.Lemmas
import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-! Intercambio de la última subida y un cero terminal.
El producto es multiplicativo de paridades, no el valor de la órbita. -/

namespace PerdicesIntercambio

def factor (b : Bool) : ℚ := if b then 3 / 2 else 1 / 2

def producto : List Bool → ℚ
  | [] => 1
  | b :: w => factor b * producto w

def Viva (p : ℚ) : List Bool → Prop
  | [] => 1 ≤ p
  | b :: w => 1 ≤ p ∧ Viva (p * factor b) w

theorem viva_inicio {p : ℚ} {w : List Bool} (h : Viva p w) : 1 ≤ p := by
  cases w with
  | nil => exact h
  | cons b w => exact h.1

theorem producto_append (u v : List Bool) :
    producto (u ++ v) = producto u * producto v := by
  induction u with
  | nil => simp [producto]
  | cons b u ih => simp [producto, ih, mul_assoc]

theorem producto_formula (w : List Bool) :
    producto w = (3 : ℚ) ^ w.count true / 2 ^ w.length := by
  induction w with
  | nil => simp [producto]
  | cons b w ih =>
    cases b <;> simp [producto, factor, ih, pow_succ] <;> ring

theorem viva_append (p : ℚ) (u v : List Bool) :
    Viva p (u ++ v) ↔ Viva p u ∧ Viva (p * producto u) v := by
  induction u generalizing p with
  | nil =>
    simp only [List.nil_append, Viva, producto, mul_one]
    exact ⟨fun h => ⟨viva_inicio h, h⟩, fun h => h.2⟩
  | cons b u ih =>
    simp only [List.cons_append, Viva, producto, ih, mul_assoc]
    tauto

theorem viva_iff_prefijos (p : ℚ) (w : List Bool) :
    Viva p w ↔ ∀ u v, w = u ++ v → 1 ≤ p * producto u := by
  constructor
  · intro h u v he
    subst w
    have ht := ((viva_append p u v).mp h).2
    exact viva_inicio ht
  · intro h
    induction w generalizing p with
    | nil => simpa [Viva, producto] using h [] [] rfl
    | cons b w ih =>
      constructor
      · simpa [producto] using h [] (b :: w) rfl
      · apply ih
        intro u v he
        have hh := h (b :: u) v (by simp [he])
        simpa [producto, mul_assoc] using hh

theorem producto_ceros (j : ℕ) :
    producto (List.replicate j false) = 1 / (2 : ℚ) ^ j := by
  induction j with
  | zero => simp [producto]
  | succ j ih =>
    simp only [List.replicate_succ, producto, factor, Bool.false_eq_true, ite_false, ih, pow_succ]
    ring

theorem viva_ceros (p : ℚ) (j : ℕ) :
    Viva p (List.replicate j false) ↔ (2 : ℚ) ^ j ≤ p := by
  induction j generalizing p with
  | zero => simp [Viva]
  | succ j ih =>
    simp only [List.replicate_succ, Viva, factor, Bool.false_eq_true, ite_false, ih, pow_succ]
    have hpot : (1 : ℚ) ≤ 2 ^ j := one_le_pow₀ (by norm_num)
    constructor
    · rintro ⟨h1, h2⟩
      linarith
    · intro h
      constructor <;> linarith

def original (v : List Bool) (j : ℕ) : List Bool :=
  v ++ true :: List.replicate j false

def imagen (v : List Bool) (j : ℕ) : List Bool :=
  v ++ false :: true :: List.replicate (j - 1) false

theorem producto_original (v : List Bool) (j : ℕ) :
    producto (original v j) = producto v * (3 / 2) / 2 ^ j := by
  simp [original, producto_append, producto, factor, producto_ceros]
  ring

theorem cola_intercambiada_viva {p : ℚ} {j : ℕ}
    (hj : 1 ≤ j) (hp : 3 / 2 ≤ p * (3 / 2) / 2 ^ j) :
    Viva p (false :: true :: List.replicate (j - 1) false) := by
  have hpos : (0 : ℚ) < 2 ^ j := by positivity
  have hmul := (le_div_iff₀ hpos).mp hp
  have hpres : (2 : ℚ) ^ j ≤ p := by linarith
  cases j with
  | zero => omega
  | succ j =>
    simp only [Nat.add_sub_cancel, Viva, factor, Bool.false_eq_true, ite_false, ite_true, viva_ceros]
    have hpot : (1 : ℚ) ≤ 2 ^ j := one_le_pow₀ (by norm_num)
    rw [pow_succ] at hpres
    constructor
    · linarith
    · constructor <;> linarith

theorem intercambio_conserva_supervivencia {v : List Bool} {j : ℕ}
    (hj : 1 ≤ j) (hv : Viva 1 (original v j))
    (hfinal : 3 / 2 ≤ producto (original v j)) :
    Viva 1 (imagen v j) := by
  have hprefix := ((viva_append 1 v (true :: List.replicate j false)).mp hv).1
  apply (viva_append 1 v (false :: true :: List.replicate (j - 1) false)).mpr
  refine ⟨hprefix, ?_⟩
  simp only [one_mul]
  apply cola_intercambiada_viva hj
  simpa [producto_original] using hfinal

theorem intercambio_conserva_producto (v : List Bool) {j : ℕ} (hj : 1 ≤ j) :
    producto (imagen v j) = producto (original v j) := by
  cases j with
  | zero => omega
  | succ j =>
    simp only [imagen, original, producto_append, producto, factor, Bool.false_eq_true,
      ite_false, ite_true, Nat.add_sub_cancel, producto_ceros, pow_succ]
    ring

theorem intercambio_conserva_longitud (v : List Bool) {j : ℕ} (hj : 1 ≤ j) :
    (imagen v j).length = (original v j).length := by
  simp only [imagen, original, List.length_append, List.length_cons, List.length_replicate]
  omega

theorem intercambio_conserva_subidas (v : List Bool) (j : ℕ) :
    (imagen v j).count true = (original v j).count true := by
  simp [imagen, original, List.count_append, List.count_replicate]

def codigo (v : List Bool) (j : ℕ) : List Bool :=
  List.replicate j false ++ true :: v

theorem codigo_inyectivo {v w : List Bool} {j k : ℕ}
    (h : codigo v j = codigo w k) : v = w ∧ j = k := by
  induction j generalizing k with
  | zero =>
    cases k with
    | zero => simpa [codigo] using h
    | succ k => simp [codigo, List.replicate_succ] at h
  | succ j ih =>
    cases k with
    | zero => simp [codigo, List.replicate_succ] at h
    | succ k =>
      have hrest : codigo v j = codigo w k := by
        simpa [codigo, List.replicate_succ] using h
      rcases ih hrest with ⟨hv, hj⟩
      exact ⟨hv, by omega⟩

theorem imagen_inyectiva {v w : List Bool} {j k : ℕ}
    (hj : 1 ≤ j) (hk : 1 ≤ k) (h : imagen v j = imagen w k) :
    v = w ∧ j = k := by
  have hr := congrArg List.reverse h
  have hc : codigo (false :: v.reverse) (j - 1) = codigo (false :: w.reverse) (k - 1) := by
    simpa [imagen, codigo, List.reverse_append, List.reverse_cons,
      List.reverse_replicate, List.append_assoc] using hr
  rcases codigo_inyectivo hc with ⟨hv, he⟩
  have hrev : v.reverse = w.reverse := List.cons.inj hv |>.2
  exact ⟨List.reverse_injective hrev, by omega⟩

theorem ceros_cambian_paridad {j : ℕ} (hj : j % 2 = 1) :
    1 ≤ j ∧ (j - 1) % 2 = 0 := by omega

def recorrido (r : ℕ) : List Bool → ℕ
  | [] => r
  | b :: w => recorrido (if b then 2 else 2 * r % 3) w

theorem recorrido_append (r : ℕ) (u v : List Bool) :
    recorrido r (u ++ v) = recorrido (recorrido r u) v := by
  induction u generalizing r with
  | nil => rfl
  | cons b u ih => simp [recorrido, ih]

theorem recorrido_ceros (r j : ℕ) (hr : r < 3) :
    recorrido r (List.replicate j false) = if j % 2 = 0 then r else 2 * r % 3 := by
  induction j generalizing r with
  | zero => simp [recorrido]
  | succ j ih =>
    simp only [List.replicate_succ, recorrido, Bool.false_eq_true, ite_false]
    rw [ih _ (Nat.mod_lt _ (by decide))]
    split_ifs <;> omega

theorem residuo_original (r : ℕ) (v : List Bool) (j : ℕ) :
    recorrido r (original v j) = if j % 2 = 0 then 2 else 1 := by
  simp [original, recorrido_append, recorrido, recorrido_ceros 2 j (by decide)]

theorem residuo_imagen (r : ℕ) (v : List Bool) {j : ℕ} (hj : j % 2 = 1) :
    recorrido r (imagen v j) = 2 := by
  have he := (ceros_cambian_paridad hj).2
  simp [imagen, recorrido_append, recorrido, recorrido_ceros 2 (j - 1) (by decide), he]

theorem sin_subidas {w : List Bool} (h : true ∉ w) :
    w = List.replicate w.length false := by
  induction w with
  | nil => rfl
  | cons b w ih =>
    have ht : true ∉ w := fun hw => h (List.mem_cons_of_mem b hw)
    cases b with
    | false =>
      simp only [List.length_cons, List.replicate_succ]
      exact congrArg (List.cons false) (ih ht)
    | true => exact False.elim (h (by simp))

theorem descomposicion_ultima_subida {w : List Bool} (h : true ∈ w) :
    ∃ v j, w = original v j := by
  induction w with
  | nil => simp at h
  | cons b w ih =>
    by_cases ht : true ∈ w
    · obtain ⟨v, j, he⟩ := ih ht
      exact ⟨b :: v, j, by simpa [original] using congrArg (List.cons b) he⟩
    · have hb : b = true := by simpa [ht, eq_comm] using h
      subst b
      exact ⟨[], w.length, by simpa [original] using congrArg (List.cons true) (sin_subidas ht)⟩

theorem descomposicion_residuo_uno {w : List Bool} (h : recorrido 0 w = 1) :
    ∃ v j, w = original v j ∧ j % 2 = 1 := by
  have ht : true ∈ w := by
    by_contra hn
    have he := sin_subidas hn
    rw [he, recorrido_ceros 0 _ (by decide)] at h
    simp at h
  obtain ⟨v, j, he⟩ := descomposicion_ultima_subida ht
  refine ⟨v, j, he, ?_⟩
  rw [he, residuo_original] at h
  split_ifs at h <;> omega

/-- Frontera alta a longitud y numero de subidas fijos. -/
def Alta (K s : ℕ) (w : List Bool) : Prop :=
  w.length = K ∧ w.count true = s ∧ Viva 1 w ∧ 3 / 2 ≤ producto w ∧ producto w < 2

def Estado (K s : ℕ) := {w : List Bool // Alta K s w}

def Clase (K s r : ℕ) := {w : Estado K s // recorrido 0 w.val = r}

instance (K s : ℕ) : Finite (Estado K s) := by
  let f : Estado K s → List.Vector Bool K := fun w => ⟨w.val, w.property.1⟩
  apply Finite.of_injective f
  intro a b h
  exact Subtype.ext (congrArg (fun z : List.Vector Bool K => z.val) h)

instance (K s r : ℕ) : Finite (Clase K s r) :=
  inferInstanceAs (Finite {w : Estado K s // recorrido 0 w.val = r})

noncomputable def descomponer {K s : ℕ} (w : Clase K s 1) :
    {d : List Bool × ℕ // w.val.val = original d.1 d.2 ∧ d.2 % 2 = 1} :=
  Classical.choice (by
    obtain ⟨v, j, he, hj⟩ := descomposicion_residuo_uno w.property
    exact ⟨⟨(v, j), he, hj⟩⟩)

noncomputable def intercambiar {K s : ℕ} (w : Clase K s 1) : Clase K s 2 := by
  let v := (descomponer w).val.1
  let j := (descomponer w).val.2
  have he : w.val.val = original v j := (descomponer w).property.1
  have hj : j % 2 = 1 := (descomponer w).property.2
  have hpos : 1 ≤ j := (ceros_cambian_paridad hj).1
  refine ⟨⟨imagen v j, ?_⟩, residuo_imagen 0 v hj⟩
  have hw := w.val.property
  rw [he] at hw
  exact ⟨(intercambio_conserva_longitud v hpos).trans hw.1,
    (intercambio_conserva_subidas v j).trans hw.2.1,
    intercambio_conserva_supervivencia hpos hw.2.2.1 hw.2.2.2.1,
    by simpa [intercambio_conserva_producto v hpos] using hw.2.2.2.1,
    by simpa [intercambio_conserva_producto v hpos] using hw.2.2.2.2⟩

theorem intercambiar_forma {K s : ℕ} (w : Clase K s 1) :
    ∃ v j, w.val.val = original v j ∧ j % 2 = 1 ∧
      (intercambiar w).val.val = imagen v j := by
  exact ⟨(descomponer w).val.1, (descomponer w).val.2,
    (descomponer w).property.1, (descomponer w).property.2, rfl⟩

theorem intercambiar_inyectivo (K s : ℕ) :
    Function.Injective (@intercambiar K s) := by
  intro a b h
  obtain ⟨v, j, ha, hj, hi⟩ := intercambiar_forma a
  obtain ⟨u, k, hb, hk, hu⟩ := intercambiar_forma b
  have he : imagen v j = imagen u k := by
    rw [← hi, ← hu, h]
  obtain ⟨hvu, hjk⟩ := imagen_inyectiva (ceros_cambian_paridad hj).1
    (ceros_cambian_paridad hk).1 he
  apply Subtype.ext
  apply Subtype.ext
  simp [ha, hb, hvu, hjk]

theorem frontera_residuo_uno_a_lo_mas_mitad (K s : ℕ) :
    2 * Nat.card (Clase K s 1) ≤ Nat.card (Estado K s) := by
  let f : Clase K s 1 ⊕ Clase K s 1 → Estado K s :=
    Sum.elim (fun w => w.val) (fun w => (intercambiar w).val)
  have hinj : Function.Injective f := by
    intro a b h
    cases a with
    | inl a =>
      cases b with
      | inl b => exact congrArg Sum.inl (Subtype.ext h)
      | inr b =>
        have hc := congrArg (fun w : Estado K s => recorrido 0 w.val) h
        change recorrido 0 a.val.val = recorrido 0 (intercambiar b).val.val at hc
        rw [a.property, (intercambiar b).property] at hc
        omega
    | inr a =>
      cases b with
      | inl b =>
        have hc := congrArg (fun w : Estado K s => recorrido 0 w.val) h
        change recorrido 0 (intercambiar a).val.val = recorrido 0 b.val.val at hc
        rw [(intercambiar a).property, b.property] at hc
        omega
      | inr b =>
        apply congrArg Sum.inr
        exact intercambiar_inyectivo K s (Subtype.ext h)
  have hc := Nat.card_le_card_of_injective f hinj
  simpa [Nat.card_sum, two_mul] using hc

end PerdicesIntercambio

#print axioms PerdicesIntercambio.viva_inicio
#print axioms PerdicesIntercambio.producto_append
#print axioms PerdicesIntercambio.producto_formula
#print axioms PerdicesIntercambio.viva_append
#print axioms PerdicesIntercambio.viva_iff_prefijos
#print axioms PerdicesIntercambio.producto_ceros
#print axioms PerdicesIntercambio.viva_ceros
#print axioms PerdicesIntercambio.producto_original
#print axioms PerdicesIntercambio.cola_intercambiada_viva
#print axioms PerdicesIntercambio.intercambio_conserva_supervivencia
#print axioms PerdicesIntercambio.intercambio_conserva_producto
#print axioms PerdicesIntercambio.intercambio_conserva_longitud
#print axioms PerdicesIntercambio.intercambio_conserva_subidas
#print axioms PerdicesIntercambio.codigo_inyectivo
#print axioms PerdicesIntercambio.imagen_inyectiva
#print axioms PerdicesIntercambio.ceros_cambian_paridad
#print axioms PerdicesIntercambio.recorrido_append
#print axioms PerdicesIntercambio.recorrido_ceros
#print axioms PerdicesIntercambio.residuo_original
#print axioms PerdicesIntercambio.residuo_imagen
#print axioms PerdicesIntercambio.sin_subidas
#print axioms PerdicesIntercambio.descomposicion_ultima_subida
#print axioms PerdicesIntercambio.descomposicion_residuo_uno
#print axioms PerdicesIntercambio.intercambiar_forma
#print axioms PerdicesIntercambio.intercambiar_inyectivo
#print axioms PerdicesIntercambio.frontera_residuo_uno_a_lo_mas_mitad
