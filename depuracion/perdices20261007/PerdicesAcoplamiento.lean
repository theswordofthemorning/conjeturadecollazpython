import CasaCadena
import Mathlib.Data.ZMod.Basic

/-! # Perdices: olvido del arranque para una palabra común

La cadena es exactamente la de CasaCadena, recuperada del 05-10.
Los bits aquí se fijan de antemano: no se afirma que dos enteros de
Collatz produzcan espontáneamente la misma palabra.
-/

namespace PerdicesAcoplamiento

open CasaCadena

def recorrido (m : ℕ) : List Bool → ZMod (3 ^ m) → ZMod (3 ^ m)
  | [], x => x
  | b :: w, x => recorrido m w ((if b then 3 * x + 1 else x) * medio m)

theorem recorrido_diferencia (m : ℕ) (w : List Bool) (x y : ZMod (3 ^ m)) :
    recorrido m w x - recorrido m w y =
      3 ^ w.count true * (medio m : ZMod (3 ^ m)) ^ w.length * (x - y) := by
  induction w generalizing x y with
  | nil => simp [recorrido]
  | cons b w ih =>
    simp only [recorrido]
    rw [ih]
    cases b <;> simp [pow_succ] <;> ring

theorem recorrido_nat (m : ℕ) (w : List Bool) (x : ℕ) :
    (cadena m w x : ZMod (3 ^ m)) = recorrido m w x := by
  induction w generalizing x with
  | nil => simp [cadena, recorrido]
  | cons b w ih =>
    simp only [cadena, recorrido]
    rw [ih]
    congr 1
    cases b <;> simp [paso]

/-- Con al menos m bits impares, la palabra borra todo el arranque módulo 3^m. -/
theorem olvido (m : ℕ) (w : List Bool) (h : m ≤ w.count true)
    (x y : ZMod (3 ^ m)) : recorrido m w x = recorrido m w y := by
  apply sub_eq_zero.mp
  rw [recorrido_diferencia]
  obtain ⟨d, hd⟩ := Nat.exists_eq_add_of_le h
  rw [hd, pow_add]
  have hz : (3 : ZMod (3 ^ m)) ^ m = 0 := by
    simpa only [Nat.cast_pow, Nat.cast_ofNat] using ZMod.natCast_self (3 ^ m)
  rw [hz]
  simp

theorem cadena_menor (m : ℕ) (w : List Bool) (x : ℕ) : cadena m w x < 3 ^ m := by
  induction w generalizing x with
  | nil => exact Nat.mod_lt _ (by positivity)
  | cons b w ih => exact ih (paso m b x)

/-- La igualdad también vale con los representantes naturales de CasaCadena. -/
theorem cadena_olvida (m : ℕ) (w : List Bool) (h : m ≤ w.count true) (x y : ℕ) :
    cadena m w x = cadena m w y := by
  have he : (cadena m w x : ZMod (3 ^ m)) = (cadena m w y : ZMod (3 ^ m)) := by
    rw [recorrido_nat, recorrido_nat]
    exact olvido m w h _ _
  have hc := (ZMod.natCast_eq_natCast_iff' _ _ _).mp he
  simpa only [Nat.mod_eq_of_lt (cadena_menor m w x),
    Nat.mod_eq_of_lt (cadena_menor m w y)] using hc

theorem cuenta_palabra (k n : ℕ) : (palabra k n).count true = Ocelotas.S k n := by
  induction k generalizing n with
  | zero => rfl
  | succ k ih =>
    rcases Nat.mod_two_eq_zero_or_one n with h | h <;>
      simp [palabra, Ocelotas.S, h, ih, Nat.add_comm]

/-- El propio n puede reemplazarse por cualquier arranque artificial una vez S_k >= m. -/
theorem orbita_olvida (m k n x : ℕ) (h : m ≤ Ocelotas.S k n) :
    Ocelotas.T^[k] n % 3 ^ m = cadena m (palabra k n) x := by
  rw [cadena_correcta]
  exact cadena_olvida m _ (by rwa [cuenta_palabra]) n x

/-- Cota de acoplamiento para cualquier evento y colección finita de palabras.
    Se permite que los arranques dependan de la palabra. -/
theorem cota_evento (m : ℕ) (W : Finset (List Bool)) (x y : List Bool → ℕ)
    (E : Finset ℕ) :
    (W.filter fun w => cadena m w (x w) ∈ E).card ≤
      (W.filter fun w => cadena m w (y w) ∈ E).card +
      (W.filter fun w => w.count true < m).card := by
  calc
    _ ≤ ((W.filter fun w => cadena m w (y w) ∈ E) ∪
        (W.filter fun w => w.count true < m)).card := by
      apply Finset.card_le_card
      intro w hw
      obtain ⟨hW, hE⟩ := Finset.mem_filter.mp hw
      by_cases h : w.count true < m
      · exact Finset.mem_union_right _ (Finset.mem_filter.mpr ⟨hW, h⟩)
      · apply Finset.mem_union_left
        apply Finset.mem_filter.mpr
        refine ⟨hW, ?_⟩
        rwa [← cadena_olvida m w (by omega) (x w) (y w)]
    _ ≤ _ := Finset.card_union_le _ _

theorem medio_inverso (m : ℕ) : (2 : ZMod (3 ^ m)) * medio m = 1 := by
  have h := congrArg (fun a : ℕ => (a : ZMod (3 ^ m))) (dos_medio m)
  simpa using h

theorem unos_fijan_menos_uno (m k : ℕ) :
    recorrido m (List.replicate k true) (-1) = -1 := by
  have hf : (3 * (-1 : ZMod (3 ^ m)) + 1) * medio m = -1 := by
    calc
      _ = -((2 : ZMod (3 ^ m)) * medio m) := by ring
      _ = -1 := by rw [medio_inverso]
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [List.replicate_succ]
    change recorrido m (List.replicate k true)
      ((3 * (-1 : ZMod (3 ^ m)) + 1) * medio m) = -1
    rw [hf]
    exact ih

/-- Olvidar x no hace uniforme la salida si la palabra está sesgada. -/
theorem olvido_sin_uniformidad (m k : ℕ) (h : m ≤ k) (x : ZMod (3 ^ m)) :
    recorrido m (List.replicate k true) x = -1 := by
  rw [olvido m _ (by simpa using h) x (-1)]
  exact unos_fijan_menos_uno m k

/-- Cada horizonte sesgado finito es realizable por un entero; el entero puede variar con k. -/
theorem prefijo_sesgado_realizable (m k : ℕ) (h : m ≤ k) :
    ∃ n, n < 2 ^ k ∧ palabra k n = List.replicate k true ∧
      (Ocelotas.T^[k] n : ZMod (3 ^ m)) = -1 := by
  obtain ⟨n, hn, hp⟩ := palabra_sobre k (List.replicate k true) (by simp)
  refine ⟨n, hn, hp, ?_⟩
  have hc := congrArg (fun a : ℕ => (a : ZMod (3 ^ m))) (cadena_correcta m k n)
  rw [recorrido_nat, hp, olvido_sin_uniformidad m k h] at hc
  simpa using hc

/-- Representantes cuyo pronóstico no cruza en ninguno de los primeros k pasos. -/
def supervivientes (k : ℕ) : Finset ℕ :=
  (Finset.range (2 ^ k)).filter fun n =>
    ∀ j ∈ Finset.range (k + 1), 2 ^ j ≤ 3 ^ Ocelotas.S j n

theorem supervivientes_tres : supervivientes 3 = {3, 7} := by decide +kernel

theorem salidas_supervivientes_tres :
    Ocelotas.T^[3] 3 % 3 = 1 ∧ Ocelotas.T^[3] 7 % 3 = 2 := by decide +kernel

/-- La ecuación estacionaria módulo 3 da masas (0,1/3,2/3). -/
theorem estacionaria_mod_tres :
    ((2 / 3 : ℚ) / 2 = 1 / 3) ∧ ((1 / 3 : ℚ) / 2 + 1 / 2 = 2 / 3) := by
  norm_num

/-- Incluso para el evento {1}, el error condicionado supera q(3,1)=1/8. -/
theorem condicionar_no_cruce_rompe_cota :
    (1 / 8 : ℚ) <
      |(((supervivientes 3).filter fun n => Ocelotas.T^[3] n % 3 = 1).card : ℚ) /
        (supervivientes 3).card - 1 / 3| := by decide +kernel

/-- Supervivencia de una continuación desde el tiempo k y con s subidas previas.
    Incluye el punto inicial y todos los prefijos de w. -/
def Admisible : ℕ → ℕ → List Bool → Prop
  | k, s, [] => 2 ^ k ≤ 3 ^ s
  | k, s, b :: w => 2 ^ k ≤ 3 ^ s ∧
      Admisible (k + 1) (s + if b then 1 else 0) w

theorem admisible_inicio (k s : ℕ) (w : List Bool) (h : Admisible k s w) :
    2 ^ k ≤ 3 ^ s := by
  cases w with
  | nil => exact h
  | cons b w => exact h.1

theorem admisible_fin (k s : ℕ) (w : List Bool) (h : Admisible k s w) :
    2 ^ (k + w.length) ≤ 3 ^ (s + w.count true) := by
  induction w generalizing k s with
  | nil => simpa [Admisible] using h
  | cons b w ih =>
    have hf := ih (k + 1) (s + if b then 1 else 0) h.2
    cases b <;> simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hf

/-- La frontera sólo depende del tiempo y del número acumulado de subidas. -/
theorem admisible_append (k s : ℕ) (u v : List Bool) :
    Admisible k s (u ++ v) ↔ Admisible k s u ∧
      Admisible (k + u.length) (s + u.count true) v := by
  induction u generalizing k s with
  | nil =>
    simp only [List.nil_append, Admisible, List.length_nil, List.count_nil, Nat.add_zero]
    exact ⟨fun h => ⟨admisible_inicio k s v h, h⟩, fun h => h.2⟩
  | cons b u ih =>
    cases b <;>
      simp [Admisible, ih, and_assoc, Nat.add_comm, Nat.add_left_comm]

/-- Un margen de L bajadas permite TODA continuación de L pasos. -/
theorem reserva_suficiente (k s : ℕ) (w : List Bool)
    (h : 2 ^ (k + w.length) ≤ 3 ^ s) : Admisible k s w := by
  induction w generalizing k s with
  | nil => simpa [Admisible] using h
  | cons b w ih =>
    refine ⟨le_trans (Nat.pow_le_pow_right (by decide) (Nat.le_add_right k _)) h, ?_⟩
    apply ih
    have hs : 3 ^ s ≤ 3 ^ (s + if b then 1 else 0) :=
      Nat.pow_le_pow_right (by decide) (Nat.le_add_right s _)
    exact le_trans (by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using h) hs

/-- Criterio necesario y suficiente: la peor continuación es la de puras bajadas. -/
theorem todas_continuaciones_iff (k s L : ℕ) :
    (∀ w : List Bool, w.length = L → Admisible k s w) ↔ 2 ^ (k + L) ≤ 3 ^ s := by
  constructor
  · intro h
    have hf := admisible_fin k s (List.replicate L false) (h _ (by simp))
    simpa [List.count_replicate] using hf
  · intro h w hw
    apply reserva_suficiente
    simpa [hw] using h

/-- Puente con las órbitas reales; no se presupone independencia de sus bits. -/
theorem admisible_palabra (a s k n : ℕ) :
    Admisible a s (palabra k n) ↔
      ∀ j ≤ k, 2 ^ (a + j) ≤ 3 ^ (s + Ocelotas.S j n) := by
  induction k generalizing a s n with
  | zero => simp [palabra, Admisible, Ocelotas.S]
  | succ k ih =>
    have hb : (if decide (n % 2 = 1) then 1 else 0) = n % 2 := by
      rcases Nat.mod_two_eq_zero_or_one n with h | h <;> simp [h]
    simp only [palabra, Admisible, hb, ih]
    constructor
    · rintro ⟨h0, h⟩ j hj
      cases j with
      | zero => simpa [Ocelotas.S] using h0
      | succ j =>
        simpa [Ocelotas.S, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
          h j (by omega)
    · intro h
      refine ⟨by simpa [Ocelotas.S] using h 0 (by omega), ?_⟩
      intro j hj
      simpa [Ocelotas.S, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
        h (j + 1) (by omega)

theorem superviviente_iff_admisible (k n : ℕ) :
    n ∈ supervivientes k ↔ n < 2 ^ k ∧ Admisible 0 0 (palabra k n) := by
  simp [supervivientes, admisible_palabra]

/-- Cada continuación protegida se realiza por un representante entero superviviente.
    El representante puede cambiar con w y con el horizonte. -/
theorem bloque_libre_realizable (u w : List Bool) (hu : Admisible 0 0 u)
    (hr : 2 ^ (u.length + w.length) ≤ 3 ^ u.count true) :
    ∃ n, n < 2 ^ (u.length + w.length) ∧
      palabra (u.length + w.length) n = u ++ w ∧
      n ∈ supervivientes (u.length + w.length) := by
  obtain ⟨n, hn, hw⟩ := palabra_sobre (u.length + w.length) (u ++ w) (by simp)
  refine ⟨n, hn, hw, ?_⟩
  rw [superviviente_iff_admisible, hw]
  refine ⟨hn, (admisible_append 0 0 u w).mpr ⟨hu, ?_⟩⟩
  simpa using reserva_suficiente u.length (u.count true) w hr

/-- Desde un prefijo vivo, la rama impar siempre sigue viva. -/
theorem subida_permitida (k s : ℕ) (h : 2 ^ k ≤ 3 ^ s) :
    2 ^ (k + 1) ≤ 3 ^ (s + 1) := by
  rw [pow_succ, pow_succ]
  omega

/-- Restricción individual: con pronóstico menor que 2, el fugitivo debe dar un paso impar. -/
theorem fugitivo_frontera_impar (n k : ℕ)
    (hf : ∀ j, 2 ^ j ≤ 3 ^ Ocelotas.S j n)
    (hb : 3 ^ Ocelotas.S k n < 2 ^ (k + 1)) : Ocelotas.T^[k] n % 2 = 1 := by
  rcases Nat.mod_two_eq_zero_or_one (Ocelotas.T^[k] n) with h | h
  · have hn := hf (k + 1)
    rw [Ocelotas.S_add] at hn
    simp only [Ocelotas.S, h, Nat.add_zero, zero_add] at hn
    omega
  · exact h

/-- Las ventanas sin reserva están contenidas en los tiempos bajos ya estudiados
    en CasaPlaneador. El umbral 3^L es una mayoración, no una igualdad. -/
theorem cuenta_sin_reserva (n L K : ℕ) :
    ((Finset.range K).filter fun j => 3 ^ Ocelotas.S j n < 2 ^ (j + L)).card ≤
      ((Finset.range K).filter fun j => 3 ^ Ocelotas.S j n ≤ 3 ^ L * 2 ^ j).card := by
  apply Finset.card_le_card
  intro j hj
  obtain ⟨hj, h⟩ := Finset.mem_filter.mp hj
  refine Finset.mem_filter.mpr ⟨hj, le_trans h.le ?_⟩
  rw [pow_add, Nat.mul_comm (3 ^ L)]
  exact Nat.mul_le_mul_left _ (Nat.pow_le_pow_left (by decide) L)

end PerdicesAcoplamiento

#print axioms PerdicesAcoplamiento.recorrido_diferencia
#print axioms PerdicesAcoplamiento.recorrido_nat
#print axioms PerdicesAcoplamiento.olvido
#print axioms PerdicesAcoplamiento.cadena_menor
#print axioms PerdicesAcoplamiento.cadena_olvida
#print axioms PerdicesAcoplamiento.cuenta_palabra
#print axioms PerdicesAcoplamiento.orbita_olvida
#print axioms PerdicesAcoplamiento.cota_evento
#print axioms PerdicesAcoplamiento.medio_inverso
#print axioms PerdicesAcoplamiento.unos_fijan_menos_uno
#print axioms PerdicesAcoplamiento.olvido_sin_uniformidad
#print axioms PerdicesAcoplamiento.prefijo_sesgado_realizable
#print axioms PerdicesAcoplamiento.supervivientes_tres
#print axioms PerdicesAcoplamiento.salidas_supervivientes_tres
#print axioms PerdicesAcoplamiento.estacionaria_mod_tres
#print axioms PerdicesAcoplamiento.condicionar_no_cruce_rompe_cota
#print axioms PerdicesAcoplamiento.admisible_inicio
#print axioms PerdicesAcoplamiento.admisible_fin
#print axioms PerdicesAcoplamiento.admisible_append
#print axioms PerdicesAcoplamiento.reserva_suficiente
#print axioms PerdicesAcoplamiento.todas_continuaciones_iff
#print axioms PerdicesAcoplamiento.admisible_palabra
#print axioms PerdicesAcoplamiento.superviviente_iff_admisible
#print axioms PerdicesAcoplamiento.bloque_libre_realizable
#print axioms PerdicesAcoplamiento.subida_permitida
#print axioms PerdicesAcoplamiento.fugitivo_frontera_impar
#print axioms PerdicesAcoplamiento.cuenta_sin_reserva
