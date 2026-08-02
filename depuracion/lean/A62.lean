/-
A62.lean -- Agente 1 (LEAN) del trio de verificacion.

ENUNCIADO (ficha A62): "las casillas (A,B) que sobreviven al barrido son
(semi)convergentes de log2(3), pero solo LAS QUE LO APROXIMAN POR ENCIMA."
Cuantificador: ciclos.

MAPA: el enunciado es del mapa CLASICO (n par -> n/2, n impar -> 3n+1).
Aqui se usa ese mapa, con el mapa 3n-1 como control A/B.

Lo que se demuestra en este fichero:

1. `por_encima`: para TODO n >= 1 y TODO k >= 1, si la trayectoria del mapa
   clasico vuelve a n en k pasos (un ciclo), entonces 3^A < 2^B, donde A es el
   numero de pasos impares y B el de pares del ciclo. Es decir: la casilla
   (A,B) de cualquier ciclo aproxima log2(3) POR ENCIMA (B/A > log2 3).
   General, sin `decide`, via la identidad 2^B*m = 3^A*n + C con C en Nat.

2. `tablaC` / `tablaC_A`: los records de aproximacion por encima
   (los B donde 3^bestA(B)/2^B bate record acercandose a 1 por debajo)
   hasta B = 65 son EXACTAMENTE B = 1,2,5,8,27,46,65 con
   A = 0,1,3,5,17,29,41 -- la lista de semiconvergentes POR ENCIMA de log2(3)
   (Tabla C de Terras). Decidido por el nucleo, no por #eval.

3. `abajo_excluido`: los cuatro convergentes POR DEBAJO senalados en la
   correccion de la ficha -- 3/2, 19/12, 84/53, 1054/665 -- cumplen
   2^B < 3^A, luego el teorema 1 los EXCLUYE como casillas de ciclo del
   mapa clasico. (Con (A,B) = (2,3), (12,19), (53,84), (665,1054).)

4. `ciclo_trivial_estado`: caso conocido contra el repo: el ciclo 1->4->2->1
   da A=1, B=2, C=1, o sea 2^2 = 3^1 + 1 (el "4 = 3 + 1"). Por `decide`.

5. Control 3n-1: el ciclo {5,14,7,20,10} del mapa 3n-1 tiene (A,B) = (2,3)
   con 2^3 < 3^2: aproxima POR DEBAJO. El "por encima" discrimina el mapa.
-/

set_option maxRecDepth 40000

namespace A62

/-- Estado de la trayectoria: valor actual m, A = pasos impares (3n+1),
    B = pasos pares (n/2), C = el resto acumulado de la identidad de Terras. -/
structure Estado where
  m : Nat
  A : Nat
  B : Nat
  C : Nat
deriving Repr, DecidableEq

/-- Un paso del mapa CLASICO, arrastrando contadores y C.
    Par:   m -> m/2,    B+1, C queda.
    Impar: m -> 3m+1,   A+1, C -> 3C + 2^B. -/
def pasoE (e : Estado) : Estado :=
  if e.m % 2 = 0 then
    { m := e.m / 2, A := e.A, B := e.B + 1, C := e.C }
  else
    { m := 3 * e.m + 1, A := e.A + 1, B := e.B, C := 3 * e.C + 2 ^ e.B }

def iterE : Nat -> Nat -> Estado
  | 0, n => { m := n, A := 0, B := 0, C := 0 }
  | k + 1, n => pasoE (iterE k n)

/-- La identidad de Terras se conserva en cada paso. -/
theorem paso_inv (n : Nat) (e : Estado)
    (h : 2 ^ e.B * e.m = 3 ^ e.A * n + e.C) :
    2 ^ (pasoE e).B * (pasoE e).m = 3 ^ (pasoE e).A * n + (pasoE e).C := by
  unfold pasoE
  by_cases hp : e.m % 2 = 0
  · rw [if_pos hp]
    show 2 ^ (e.B + 1) * (e.m / 2) = 3 ^ e.A * n + e.C
    have h2 : 2 * (e.m / 2) = e.m := by omega
    calc 2 ^ (e.B + 1) * (e.m / 2) = 2 ^ e.B * (2 * (e.m / 2)) := by
          rw [Nat.pow_succ, Nat.mul_assoc]
      _ = 2 ^ e.B * e.m := by rw [h2]
      _ = 3 ^ e.A * n + e.C := h
  · rw [if_neg hp]
    show 2 ^ e.B * (3 * e.m + 1) = 3 ^ (e.A + 1) * n + (3 * e.C + 2 ^ e.B)
    have h1 : 2 ^ e.B * (3 * e.m + 1) = 3 * (2 ^ e.B * e.m) + 2 ^ e.B := by
      rw [Nat.mul_add, Nat.mul_one, Nat.mul_left_comm]
    rw [h1, h, Nat.pow_succ, Nat.mul_comm (3 ^ e.A) 3, Nat.mul_assoc]
    omega

/-- Identidad de Terras iterada: 2^B * m_k = 3^A * n + C, en Nat. -/
theorem invariante (n : Nat) : forall k,
    2 ^ (iterE k n).B * (iterE k n).m = 3 ^ (iterE k n).A * n + (iterE k n).C
  | 0 => by simp [iterE]
  | k + 1 => paso_inv n (iterE k n) (invariante n k)

/-- Si no hubo ningun paso impar, C = 0. -/
theorem paso_A0 (e : Estado) (h : e.A = 0 -> e.C = 0) :
    (pasoE e).A = 0 -> (pasoE e).C = 0 := by
  unfold pasoE
  by_cases hp : e.m % 2 = 0
  · rw [if_pos hp]; exact h
  · rw [if_neg hp]
    intro hA
    exact absurd hA (Nat.succ_ne_zero e.A)

theorem iter_A0 (n : Nat) : forall k, (iterE k n).A = 0 -> (iterE k n).C = 0
  | 0 => fun _ => rfl
  | k + 1 => paso_A0 (iterE k n) (iter_A0 n k)

/-- Si hubo al menos un paso impar, C >= 1 (el +1 del 3n+1). -/
theorem paso_Apos (e : Estado) (h : 1 <= e.A -> 1 <= e.C) :
    1 <= (pasoE e).A -> 1 <= (pasoE e).C := by
  unfold pasoE
  by_cases hp : e.m % 2 = 0
  · rw [if_pos hp]; exact h
  · rw [if_neg hp]
    intro _
    show 1 <= 3 * e.C + 2 ^ e.B
    have h2 : 0 < 2 ^ e.B := Nat.two_pow_pos e.B
    omega

theorem iter_Apos (n : Nat) : forall k, 1 <= (iterE k n).A -> 1 <= (iterE k n).C
  | 0 => by intro h; simp [iterE] at h
  | k + 1 => paso_Apos (iterE k n) (iter_Apos n k)

/-- Cada paso es par o impar: A + B = k. -/
theorem paso_AB (k : Nat) (e : Estado) (h : e.A + e.B = k) :
    (pasoE e).A + (pasoE e).B = k + 1 := by
  unfold pasoE
  by_cases hp : e.m % 2 = 0
  · rw [if_pos hp]; show e.A + (e.B + 1) = k + 1; omega
  · rw [if_neg hp]; show (e.A + 1) + e.B = k + 1; omega

theorem iter_AB (n : Nat) : forall k, (iterE k n).A + (iterE k n).B = k
  | 0 => rfl
  | k + 1 => paso_AB k (iterE k n) (iter_AB n k)

/-- EL TEOREMA: todo ciclo del mapa clasico (n >= 1, k >= 1 pasos,
    vuelve a n) tiene 3^A < 2^B -- su casilla (A,B) aproxima log2(3)
    POR ENCIMA. Vale para TODO n y TODO k, sin excepciones. -/
theorem por_encima (n k : Nat) (hn : 1 <= n) (hk : 1 <= k)
    (hcic : (iterE k n).m = n) :
    3 ^ (iterE k n).A < 2 ^ (iterE k n).B := by
  have hinv := invariante n k
  rw [hcic] at hinv
  by_cases hA : (iterE k n).A = 0
  · -- solo divisiones: imposible volver a n >= 1 con k >= 1 pasos
    exfalso
    have hC := iter_A0 n k hA
    have hAB := iter_AB n k
    rw [hA, hC] at hinv
    rw [Nat.pow_zero, Nat.one_mul, Nat.add_zero] at hinv
    -- hinv : 2 ^ B * n = n
    rw [hA] at hAB
    have hB : 1 <= (iterE k n).B := by omega
    have h2 : 2 <= 2 ^ (iterE k n).B := by
      calc 2 = 2 ^ 1 := rfl
        _ <= 2 ^ (iterE k n).B := Nat.pow_le_pow_right (by omega) hB
    have hge : 2 * n <= 2 ^ (iterE k n).B * n := Nat.mul_le_mul_right n h2
    omega
  · -- hubo al menos un 3n+1: C >= 1 fuerza la desigualdad estricta
    have hApos : 1 <= (iterE k n).A := by omega
    have hC := iter_Apos n k hApos
    have hlt : 3 ^ (iterE k n).A * n < 2 ^ (iterE k n).B * n := by omega
    exact Nat.lt_of_mul_lt_mul_right hlt

/-- CASO CONOCIDO contra el repo (por el nucleo, no #eval):
    el ciclo trivial 1 -> 4 -> 2 -> 1 da A=1, B=2, C=1:
    la ecuacion 2^2 = 3^1 + 1, el "4 = 3 + 1" del documento. -/
theorem ciclo_trivial_estado : iterE 3 1 = { m := 1, A := 1, B := 2, C := 1 } := by
  decide

/-- Y su casilla (1,2) esta por encima: 3^1 < 2^2. -/
theorem ciclo_trivial_por_encima : 3 ^ 1 < 2 ^ 2 := by decide

/- ------------------------------------------------------------------
   PARTE 2: la lista de casillas supervivientes = Tabla C de Terras
   = semiconvergentes de log2(3) POR ENCIMA, hasta B = 65.
   ------------------------------------------------------------------ -/

/-- El mayor A con 3^A < 2^B (la casilla por-encima mas apretada para B). -/
def bestA (b : Nat) : Nat :=
  (List.range (b + 1)).foldl (fun acc a => if 3 ^ a < 2 ^ b then a else acc) 0

/-- B es record si su cociente 3^bestA(B)/2^B se acerca a 1 (por debajo)
    mas que el de todo B' < B. Comparado en enteros, sin un solo real:
    3^A'/2^B' < 3^A/2^B  <=>  3^A' * 2^B < 3^A * 2^B'. -/
def esRecord (b : Nat) : Bool :=
  b != 0 && (List.range b).all fun b' =>
    b' == 0 || decide (3 ^ (bestA b') * 2 ^ b < 3 ^ (bestA b) * 2 ^ b')

/-- Los records hasta B = 65 son exactamente los de la Tabla C. -/
theorem tablaC : (List.range 66).filter esRecord = [1, 2, 5, 8, 27, 46, 65] := by
  decide

/-- Y sus A: (0,1), (1,2), (3,5), (5,8), (17,27), (29,46), (41,65) --
    los semiconvergentes de log2(3) por encima: 1/0, 2/1, 5/3, 8/5,
    27/17, 46/29, 65/41. -/
theorem tablaC_A : [1, 2, 5, 8, 27, 46, 65].map bestA = [0, 1, 3, 5, 17, 29, 41] := by
  decide

/- Los cuatro convergentes POR DEBAJO de la correccion de la ficha
   (3/2, 19/12, 84/53, 1054/665, como B/A) cumplen 2^B < 3^A:
   `por_encima` los excluye como casillas de ciclo del mapa clasico. -/
set_option exponentiation.threshold 1100 in
theorem abajo_excluido :
    2 ^ 3 < 3 ^ 2 ∧ 2 ^ 19 < 3 ^ 12 ∧ 2 ^ 84 < 3 ^ 53 ∧ 2 ^ 1054 < 3 ^ 665 := by
  decide

/- ------------------------------------------------------------------
   PARTE 3: control A/B con el mapa 3n-1. Su ciclo {5,14,7,20,10}
   cae POR DEBAJO: el enunciado discrimina el mapa.
   ------------------------------------------------------------------ -/

def pasoM (e : Nat × Nat × Nat) : Nat × Nat × Nat :=
  match e with
  | (m, a, b) => if m % 2 = 0 then (m / 2, a, b + 1) else (3 * m - 1, a + 1, b)

def iterM : Nat -> Nat -> Nat × Nat × Nat
  | 0, n => (n, 0, 0)
  | k + 1, n => pasoM (iterM k n)

/-- El ciclo de periodo 5 del mapa 3n-1: 5 -> 14 -> 7 -> 20 -> 10 -> 5,
    con A = 2 impares y B = 3 pares. -/
theorem control_3n1_ciclo : iterM 5 5 = (5, 2, 3) := by decide

/-- Y su casilla (2,3) esta POR DEBAJO: 2^3 < 3^2 (8 < 9). -/
theorem control_3n1_por_debajo : 2 ^ 3 < 3 ^ 2 := by decide

/- Controles finales -/
#print axioms por_encima
#print axioms invariante
#print axioms ciclo_trivial_estado
#print axioms tablaC
#print axioms tablaC_A
#print axioms abajo_excluido
#print axioms control_3n1_ciclo

end A62
