/-
  LA COTA POR TRAMO, DEMOSTRADA EN LEAN 4.

  `cotatramos.py` COMPRUEBA esto sobre 329.400 pares y saca 0 fallos.
  Aqui se DEMUESTRA: vale para todo n0 y todo numero de pasos, no para una
  muestra. Ese es el salto de categoria, y es el unico motivo de este fichero.

  EL MAPA ES EL CLASICO:   n par -> n/2 ,  n impar -> 3n+1.
  NO es el atajo. En el atajo cada paso impar tambien divide entre dos, asi que
  el B saldria distinto. Confundirlos ya costo caro en este repo.

      A = cuantas veces se aplico 3n+1
      B = cuantas veces se aplico n/2
      C = la constante de la identidad de Terras (Teorema 1.1)

  LA IDENTIDAD    2^B * n_k  =  3^A * n_0 + C
  LA COTA         2^B * n_k >=  3^A * n_0

  La cota sale de la identidad sin trabajo: aqui C es un natural, luego C >= 0
  por construccion. Ese "C >= 0" es exactamente el +1 del 3n+1.

  No usa Mathlib: solo el nucleo de Lean 4. Se comprueba con
      lean cotatramos.lean
  y si no imprime nada, esta demostrado.
-/

/-- El estado de un tramo: donde estamos y la cuenta de A, B y C. -/
structure Tramo where
  n : Nat
  A : Nat
  B : Nat
  C : Nat

/-- Un paso del mapa clasico, arrastrando las tres cuentas. -/
def paso (s : Tramo) : Tramo :=
  if s.n % 2 = 0 then
    { n := s.n / 2,     A := s.A,     B := s.B + 1, C := s.C }
  else
    { n := 3 * s.n + 1, A := s.A + 1, B := s.B,     C := 3 * s.C + 2 ^ s.B }

/-- El arranque: cero pasos dados, C = 0. -/
def inicio (n0 : Nat) : Tramo := { n := n0, A := 0, B := 0, C := 0 }

/-- El estado despues de k pasos saliendo de n0. -/
def tramo (n0 : Nat) : Nat → Tramo
  | 0     => inicio n0
  | k + 1 => paso (tramo n0 k)

/-- La identidad de Terras escrita como invariante del estado. -/
def inv (n0 : Nat) (s : Tramo) : Prop :=
  2 ^ s.B * s.n = 3 ^ s.A * n0 + s.C

/-- UN PASO CONSERVA LA IDENTIDAD. Aqui esta toda la aritmetica. -/
theorem paso_conserva (n0 : Nat) (s : Tramo) (h : inv n0 s) : inv n0 (paso s) := by
  unfold inv paso
  by_cases hp : s.n % 2 = 0
  · -- PASO PAR: n -> n/2, B sube uno, C no se mueve.
    rw [if_pos hp]
    show 2 ^ (s.B + 1) * (s.n / 2) = 3 ^ s.A * n0 + s.C
    have hn : s.n / 2 * 2 = s.n := Nat.div_mul_cancel (Nat.dvd_of_mod_eq_zero hp)
    calc 2 ^ (s.B + 1) * (s.n / 2)
        = 2 ^ s.B * (s.n / 2 * 2) := by
            rw [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm 2 (s.n / 2)]
      _ = 2 ^ s.B * s.n           := by rw [hn]
      _ = 3 ^ s.A * n0 + s.C      := h
  · -- PASO IMPAR: n -> 3n+1, A sube uno, C -> 3C + 2^B.
    rw [if_neg hp]
    show 2 ^ s.B * (3 * s.n + 1) = 3 ^ (s.A + 1) * n0 + (3 * s.C + 2 ^ s.B)
    calc 2 ^ s.B * (3 * s.n + 1)
        = 3 * (2 ^ s.B * s.n) + 2 ^ s.B := by
            rw [Nat.mul_add, Nat.mul_one, Nat.mul_left_comm]
      _ = 3 * (3 ^ s.A * n0 + s.C) + 2 ^ s.B := by rw [h]
      _ = 3 ^ (s.A + 1) * n0 + (3 * s.C + 2 ^ s.B) := by
            rw [Nat.pow_succ, Nat.mul_add, Nat.mul_comm (3 ^ s.A) 3,
                Nat.mul_assoc, Nat.add_assoc]

/-- LA IDENTIDAD, para todo n0 y todo k. -/
theorem identidad (n0 k : Nat) : inv n0 (tramo n0 k) := by
  induction k with
  | zero      => show 2 ^ 0 * n0 = 3 ^ 0 * n0 + 0; simp
  | succ k ih => exact paso_conserva n0 (tramo n0 k) ih

/-- LA COTA. Es lo que `cotatramos.py` mide, aqui para todos los casos. -/
theorem cota (n0 k : Nat) :
    3 ^ (tramo n0 k).A * n0 ≤ 2 ^ (tramo n0 k).B * (tramo n0 k).n := by
  rw [identidad n0 k]
  exact Nat.le_add_right _ _

/-- EL COROLARIO: si un tramo BAJA, entonces 2^B > 3^A.

    Ojo con la hipotesis: NO hace falta pedir 0 < n0. Sobre los naturales,
    "el tramo baja" (n_k < n0) ya obliga a que n0 sea positivo. Lo comprobo
    Lean: la demostracion cierra sin usarla. -/
theorem corolario (n0 k : Nat) (hbaja : (tramo n0 k).n < n0) :
    3 ^ (tramo n0 k).A < 2 ^ (tramo n0 k).B := by
  have hc := cota n0 k
  cases Nat.lt_or_ge (3 ^ (tramo n0 k).A) (2 ^ (tramo n0 k).B) with
  | inl h => exact h
  | inr h =>
      -- Suponer 2^B <= 3^A lleva a 3^A * n0 < 3^A * n0, que es absurdo.
      exfalso
      have hpos : 0 < 3 ^ (tramo n0 k).A := Nat.pow_pos (by decide)
      have h1 : 2 ^ (tramo n0 k).B * (tramo n0 k).n
              ≤ 3 ^ (tramo n0 k).A * (tramo n0 k).n :=
        Nat.mul_le_mul h (Nat.le_refl _)
      have h2 : 3 ^ (tramo n0 k).A * (tramo n0 k).n
              < 3 ^ (tramo n0 k).A * n0 :=
        (Nat.mul_lt_mul_left hpos).mpr hbaja
      exact Nat.lt_irrefl _ (Nat.lt_of_le_of_lt (Nat.le_trans hc h1) h2)

/-
  EL CONTROL FINAL, y es el que importa: `#print axioms` lista de que depende
  cada teorema. Si apareciera `sorryAx`, habria un agujero tapado. Tienen que
  salir SOLO los tres axiomas estandar de Lean (propext, Classical.choice,
  Quot.sound) -- o menos.
-/
#print axioms identidad
#print axioms cota
#print axioms corolario

/-
  Y LA OTRA COMPROBACION, que es la que Lean NO puede hacer por si sola.

  Lean garantiza que la demostracion corresponde al enunciado. No garantiza que
  el enunciado hable del objeto que uno cree. Si `paso` no fuera Collatz de
  verdad, esto seria un teorema impecable sobre otra cosa.

  El repo tiene medido que el 221 llega al 1 en 114 pasos, con A = 41 y B = 73
  (de ahi el 73/41 = 1,78 que aparece en el CLAUDE.md). Si estos evals no dan
  eso, la formalizacion esta describiendo otra dinamica.
-/
#eval (tramo 221 114).n                                   -- 1
#eval (tramo 221 114).A                                   -- 41
#eval (tramo 221 114).B                                   -- 73

/-
  Y LO MISMO OTRA VEZ, pero como TEOREMA en vez de como `#eval`.

  No es redundante y la diferencia importa: `#eval` lo calcula el COMPILADOR,
  y su resultado no lo revisa nadie. Un `by decide` lo revisa el NUCLEO de
  Lean, que es lo unico en lo que se apoya la confianza de todo lo de arriba.
  Si estas tres lineas compilan, el 221 esta comprobado de verdad.
-/
-- Los 114 pasos se desenrollan anidados y pasan del limite por defecto (512).
set_option maxRecDepth 20000

theorem el_221_llega_al_uno : (tramo 221 114).n = 1 := by decide
theorem el_221_tiene_A_41   : (tramo 221 114).A = 41 := by decide
theorem el_221_tiene_B_73   : (tramo 221 114).B = 73 := by decide

#print axioms el_221_tiene_B_73
