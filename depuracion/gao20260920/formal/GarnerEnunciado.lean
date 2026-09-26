import Alpacas

/- Enunciado para revisión humana: la conjetura de Garner (1985) sobre rachas de
   consecutivos con la misma altura, en la forma en que la recoge Gao (1993, pág. 262):
   «It has been conjectured that there exist arbitrarily long sets of consecutive numbers
   of the same height and the same σ∞(n) [1, 5]», con [1] = Garner y [5] = Penning.
   La prueba está en Alpacas.lean y sus dependencias. -/

namespace GarnerEnunciado

/-- Mapa clásico de Collatz (Gao, pág. 261): 3n+1 si n es impar, n/2 si es par. -/
def C (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- `height(n) = h` (Gao, pág. 262): h es el mínimo k con `C^(k)(n) = 1`. -/
def altura (n h : ℕ) : Prop := C^[h] n = 1 ∧ ∀ k, k < h → C^[k] n ≠ 1

instance (n h : ℕ) : Decidable (altura n h) := by unfold altura; infer_instance

/-- Divisiones por 2 entre los h primeros pasos desde n. Con `h = height(n)` es el
    tiempo total de parada `σ∞(n)` de Gao (pág. 262): «the number of divisions by 2
    taken in reaching 1». -/
def mitades (n h : ℕ) : ℕ := ((Finset.range h).filter (fun k => C^[k] n % 2 = 0)).card

/-- La conjetura: para cada L hay L+1 consecutivos n, …, n+L, con n tan grande como se
    quiera, que tienen todos la misma altura h y el mismo tiempo total de parada s. -/
def FormaGarner : Prop :=
  ∀ L N : ℕ, ∃ n h s : ℕ, N ≤ n ∧ ∀ i, i ≤ L → altura (n + i) h ∧ mitades (n + i) h = s

theorem conjetura_garner : FormaGarner := by
  intro L N
  have hC : C = TejonasGao.collatz := rfl
  obtain ⟨n, h, d, hN, hi⟩ := AlpacasGarner.alpacas L N
  refine ⟨n, h, d, hN, fun i hiL => ?_⟩
  obtain ⟨h1, h2, h3⟩ := hi i hiL
  refine ⟨⟨by rw [hC]; exact h1, by rw [hC]; exact h2⟩, ?_⟩
  rw [← h3]
  unfold mitades AlpacasGarner.pares
  rw [hC]

end GarnerEnunciado

#print axioms GarnerEnunciado.conjetura_garner

/- Cotejo con Gao (1993). Pág. 262: 943 a 949 tienen altura 36 y σ∞ = 26; la 17-upla de
   Penning, 7083 a 7099, altura 57 y σ∞ = 40. Tabla 1 (pág. 263): la 25-upla desde 57346
   tiene altura 78 y σ∞ = 54. Si alguna cuenta no coincide, el archivo no compila. -/
#guard (List.range 7).all (fun i =>
  decide (GarnerEnunciado.altura (943 + i) 36) && GarnerEnunciado.mitades (943 + i) 36 == 26)
#guard (List.range 17).all (fun i =>
  decide (GarnerEnunciado.altura (7083 + i) 57) && GarnerEnunciado.mitades (7083 + i) 57 == 40)
#guard (List.range 25).all (fun i =>
  decide (GarnerEnunciado.altura (57346 + i) 78) && GarnerEnunciado.mitades (57346 + i) 78 == 54)
