import Condoras

/- Enunciado para revisión humana: las dos conjeturas de Wu Jiabang (邬家邦),
   《Collatz问题中同高连续数所占比例的变化趋势》, J. Huazhong Univ. Sci. Tech. 20 (1992),
   n.º 5, 171–174. Según su resumen, K es el número de enteros de [1, 2^N) que pertenecen a
   n-uplas (n ≥ 2) de consecutivos con la misma altura, y d = K/(2^N − 1). Las dos
   conjeturas, «笔者猜想: lim d(M)=1» y «笔者猜想: lim L=∞», con L la upla más larga, se
   leyeron el 26-09-2026 con la IA de CNKI, que tiene el texto completo. Falta cotejarlas
   con el original. La prueba está en Condoras.lean y sus dependencias. -/

open Filter Topology

namespace WuEnunciado

/-- Mapa clásico de Collatz: n/2 si n es par, 3n+1 si es impar. -/
def C (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- `altura n h`: h es el mínimo número de pasos con `C^(h)(n) = 1`. -/
def altura (n h : ℕ) : Prop := C^[h] n = 1 ∧ ∀ k, k < h → C^[k] n ≠ 1

instance (n h : ℕ) : Decidable (altura n h) := by unfold altura; infer_instance

/-- n está en una upla de Wu (dos o más consecutivos de igual altura): comparte altura
    con n − 1 o con n + 1. -/
def enUpla (n : ℕ) : Prop := ∃ h, altura n h ∧ (altura (n - 1) h ∨ altura (n + 1) h)

open Classical in
/-- `d(M) = K/(M − 1)`, con K los n de [1, M) que están en una upla. -/
noncomputable def d (M : ℕ) : ℝ :=
  (((Finset.Ico 1 M).filter enUpla).card : ℝ) / ((M : ℝ) - 1)

/-- Hay k consecutivos de igual altura dentro de [1, M). -/
def uplaEn (M k : ℕ) : Prop := ∃ n h, 1 ≤ n ∧ n + k ≤ M ∧ ∀ i, i < k → altura (n + i) h

/-- `L(M)`: la upla más larga dentro de [1, M). -/
noncomputable def L (M : ℕ) : ℕ := sSup {k | uplaEn M k}

/-- n llega a 1. -/
def llega (n : ℕ) : Prop := ∃ h, C^[h] n = 1

open Classical in
/-- Proporción de [1, M) que llega a 1, normalizada como d. -/
noncomputable def proporcionLlegan (M : ℕ) : ℝ :=
  (((Finset.Ico 1 M).filter llega).card : ℝ) / ((M : ℝ) - 1)

/-- Conjetura 2 de Wu: `lim L = ∞`. -/
theorem conjetura_wu_dos : Tendsto L atTop atTop := CondorasWu.wu_dos

/-- Conjetura 1 de Wu, reducida: `lim d(M) = 1` si y sólo si los enteros que llegan a 1
    tienen densidad natural 1. Esto último es un problema abierto. -/
theorem conjetura_wu_uno :
    Tendsto d atTop (𝓝 1) ↔ Tendsto proporcionLlegan atTop (𝓝 1) := CondorasWu.wu_uno

/-- Sólo para los `#guard`: altura por iteración directa, con tope de pasos. -/
def alturaRapida : ℕ → ℕ → ℕ → Option ℕ
  | 0, _, _ => none
  | f + 1, n, a => if n = 1 then some a else alturaRapida f (C n) (a + 1)

end WuEnunciado

#print axioms WuEnunciado.conjetura_wu_dos
#print axioms WuEnunciado.conjetura_wu_uno

/- Cotejo con Wu (1992). Su upla récord bajo 2^30: 176 consecutivos desde 722 067 240. Todos
   tienen altura 190, y 722 067 239 y 722 067 416 no. Si falla, el archivo no compila. -/
#guard (List.range 176).all (fun i => decide (WuEnunciado.altura (722067240 + i) 190)) &&
  !decide (WuEnunciado.altura 722067239 190) && !decide (WuEnunciado.altura 722067416 190)

/- d(2^10) = 620/1023 = 60,61 %, el valor de Wu. Primero se comprueba que `alturaRapida`
   da la altura de `altura` en todo [1, 1024]; luego se cuentan los n de [1, 1024) que
   comparten altura con un vecino. -/
#guard (List.range 1024).all (fun i => match WuEnunciado.alturaRapida 1000 (i + 1) 0 with
  | some h => decide (WuEnunciado.altura (i + 1) h)
  | none => false)
#guard ((List.range 1024).filter (fun n => 1 ≤ n &&
  match WuEnunciado.alturaRapida 1000 n 0 with
  | some h => WuEnunciado.alturaRapida 1000 (n - 1) 0 == some h ||
      WuEnunciado.alturaRapida 1000 (n + 1) 0 == some h
  | none => false)).length == 620
