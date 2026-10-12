import PerdicesRetornoH
import Mathlib.Tactic.Ring

/-! # Perdices: rachas homogéneas y bloques E^b D^a del retorno H.

Un paso de `iterar` es un paso H. Las fórmulas incluyen cero para los bordes;
el retorno recurrente sobre positivos 15 mod 24 se describe en RACHAS_H.md.
La decodificación completa por valuaciones y las densidades conservan prueba
escrita; este módulo certifica las trayectorias y su balance algebraico.
-/

namespace PerdicesRachasH

open PerdicesRetornoH

def iterar : ℕ → ℕ → Option ℕ
  | 0, x => some x
  | k + 1, x => (H x).bind (iterar k)

theorem iterar_suma (a b x : ℕ) :
    iterar (a + b) x = (iterar a x).bind (iterar b) := by
  induction a generalizing x with
  | zero => simp [iterar]
  | succ a ih => simp [Nat.succ_add, iterar, ih, Option.bind_assoc]

theorem paso_D (u : ℕ) : H (4 * u) = some (3 * u) := by
  rw [caracterizacion]
  omega

theorem racha_D (a u : ℕ) : iterar a (4 ^ a * u) = some (3 ^ a * u) := by
  induction a generalizing u with
  | zero => simp [iterar]
  | succ a ih =>
    have he : 4 ^ (a + 1) * u = 4 * (4 ^ a * u) := by rw [pow_succ]; ring
    rw [he, iterar, paso_D]
    simp only [Option.bind_some]
    rw [show 3 * (4 ^ a * u) = 4 ^ a * (3 * u) by ring, ih]
    congr 1
    rw [pow_succ]
    ring

theorem racha_E (b u : ℕ) (hu : 1 ≤ u) :
    iterar b (8 ^ b * u - 1) = some (9 ^ b * u - 1) := by
  induction b generalizing u with
  | zero => simp [iterar]
  | succ b ih =>
    have hp : 1 ≤ 8 ^ b * u := by
      have hpow : 0 < 8 ^ b := Nat.pow_pos (by decide)
      exact Nat.mul_pos hpow hu
    have he : 8 ^ (b + 1) * u = 8 * (8 ^ b * u) := by rw [pow_succ]; ring
    rw [he, iterar, (expansion_residual hp).1]
    simp only [Option.bind_some]
    rw [show 9 * (8 ^ b * u) = 8 ^ b * (9 * u) by ring, ih (9 * u) (by omega)]
    congr 2
    rw [pow_succ]
    ring

/-- Si el extremo de E^b es 4^a*w, admite a pasos D; no se afirma maximalidad. -/
theorem bloque {a b u w : ℕ} (hu : 1 ≤ u) (h : 9 ^ b * u = 4 ^ a * w + 1) :
    iterar (b + a) (8 ^ b * u - 1) = some (3 ^ a * w) := by
  rw [iterar_suma, racha_E b u hu]
  simp only [Option.bind_some]
  rw [show 9 ^ b * u - 1 = 4 ^ a * w by omega]
  exact racha_D a w

/-- Identidad afín sin restas truncadas en el balance: M*y+3^a*8^b=A*(x+1). -/
theorem balance {a b u w : ℕ} (hu : 1 ≤ u) (h : 9 ^ b * u = 4 ^ a * w + 1) :
    (4 ^ a * 8 ^ b) * (3 ^ a * w) + 3 ^ a * 8 ^ b =
      3 ^ (a + 2 * b) * (8 ^ b * u - 1 + 1) := by
  have hp : 1 ≤ 8 ^ b * u := by
    have hpow : 0 < 8 ^ b := Nat.pow_pos (by decide)
    exact Nat.mul_pos hpow hu
  have hx : 8 ^ b * u - 1 + 1 = 8 ^ b * u := by omega
  have he : 3 ^ (a + 2 * b) = 3 ^ a * 9 ^ b := by
    rw [pow_add, pow_mul]
    norm_num
  calc
    (4 ^ a * 8 ^ b) * (3 ^ a * w) + 3 ^ a * 8 ^ b =
        3 ^ a * 8 ^ b * (4 ^ a * w + 1) := by ring
    _ = 3 ^ a * 8 ^ b * (9 ^ b * u) := by rw [h]
    _ = 3 ^ (a + 2 * b) * (8 ^ b * u - 1 + 1) := by rw [he, hx]; ring

/-- El factor w de la salida 3^a*w es una unidad módulo 3. -/
theorem salida_unidad {a b u w : ℕ} (hb : 1 ≤ b)
    (h : 9 ^ b * u = 4 ^ a * w + 1) : w % 3 ≠ 0 := by
  have hz : (9 ^ b * u) % 3 = 0 := by
    obtain ⟨c, hc⟩ : ∃ c, b = c + 1 := ⟨b - 1, by omega⟩
    rw [hc, pow_succ]
    simp [Nat.mul_mod]
  intro hw
  have hm := congrArg (fun z => z % 3) h
  rw [hz] at hm
  simp [Nat.add_mod, Nat.mul_mod, hw] at hm

/-- Si x es múltiplo de 3 y x+1=8^b*u, entonces u es una unidad módulo 3. -/
theorem entrada_unidad {x b u : ℕ} (hx : x % 3 = 0) (h : x + 1 = 8 ^ b * u) :
    u % 3 ≠ 0 := by
  intro hu
  have hm := congrArg (fun z => z % 3) h
  simp [Nat.add_mod, Nat.mul_mod, hx, hu] at hm

end PerdicesRachasH

#print axioms PerdicesRachasH.iterar_suma
#print axioms PerdicesRachasH.paso_D
#print axioms PerdicesRachasH.racha_D
#print axioms PerdicesRachasH.racha_E
#print axioms PerdicesRachasH.bloque
#print axioms PerdicesRachasH.balance
#print axioms PerdicesRachasH.salida_unidad
#print axioms PerdicesRachasH.entrada_unidad
