-- revision10_adv1/test_negativos.lean
--
-- TAREA b1 DE LA 10a REVISION (adversario 1): tres_inyectivo de
-- lecturaracha.lean usa z % 2 = 0 y z / 2 sobre Int -- verificar que
-- la convencion de division del nucleo (emod/ediv) no esconde un
-- caso con negativos. Se copian VERBATIM pot2, pot2_mitad y
-- tres_inyectivo de lecturaracha.lean (el copiado es deliberado:
-- este fichero debe compilar SOLO) y se anaden:
--   (1) sondas de la convencion / y % del nucleo sobre negativos;
--   (2) instancias NEGATIVAS de tres_inyectivo y una_clase_bit0
--       certificadas por decide (no #eval);
--   (3) el chequeo de que emod de un par negativo es 0 y ediv es
--       exacto (el unico punto donde la induccion podria cojear).

def pot2 : Nat → Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

theorem pot2_mitad (j : Nat) (d : Int) :
    pot2 (j + 1) * d = 2 * (pot2 j * d) := by
  show 2 * pot2 j * d = 2 * (pot2 j * d)
  rw [Int.mul_assoc]

theorem tres_inyectivo (n : Nat) (z w : Int)
    (h : 3 * z = pot2 n * w) : ∃ u, z = pot2 n * u := by
  induction n generalizing z w with
  | zero =>
      exact ⟨z, by
        show z = pot2 0 * z
        have h0 : pot2 0 = 1 := rfl
        rw [h0]
        omega⟩
  | succ m ih =>
      have he := pot2_mitad m w
      have hz : z % 2 = 0 := by omega
      have hz2 : 3 * (z / 2) = pot2 m * w := by omega
      cases ih (z / 2) w hz2 with
      | intro u hu =>
          have he2 := pot2_mitad m u
          exact ⟨u, by omega⟩

-- ---------------------------------------------------------------
-- (1) LA CONVENCION DEL NUCLEO: / y % sobre Int son ediv/emod
--     (resto siempre en [0, |b|)). Si alguna de estas fallara al
--     compilar, la convencion seria otra y habria que re-auditar.
-- ---------------------------------------------------------------
example : (-7 : Int) / 2 = -4 := by decide     -- ediv, NO truncada (-3)
example : (-7 : Int) % 2 = 1 := by decide      -- emod, NO truncado (-1)
example : (-6 : Int) / 2 = -3 := by decide     -- par negativo: exacto
example : (-6 : Int) % 2 = 0 := by decide      -- par negativo: resto 0
example : (-1 : Int) % 2 = 1 := by decide
example : (2 : Int) * ((-6 : Int) / 2) = -6 := by decide  -- exactitud

-- el punto fino de la induccion: para z PAR (lo unico que el paso
-- usa), ediv y la division exacta coinciden con cualquier signo
example : 2 * ((-10 : Int) / 2) = -10 := by decide
example : 2 * ((-4 : Int) / 2) = -4 := by decide
example : 2 * ((0 : Int) / 2) = 0 := by decide
example : 2 * ((4 : Int) / 2) = 4 := by decide
example : 2 * ((10 : Int) / 2) = 10 := by decide

-- ---------------------------------------------------------------
-- (2) INSTANCIAS NEGATIVAS de tres_inyectivo (premisas por decide;
--     la conclusion la construye el teorema, no un calculo)
-- ---------------------------------------------------------------
-- 3*(-8) = -24 = 2^3 * (-3)  ==>  2^3 | -8
example : ∃ u, (-8 : Int) = pot2 3 * u :=
  tres_inyectivo 3 (-8) (-3) (by decide)

-- 3*(-1398101-1)... el adversarial con signo: 3*(-2796202) = 2^22*(-2)+...
-- mejor uno limpio grande: 3*(-4194304) = 2^22 * (-3)
example : ∃ u, (-4194304 : Int) = pot2 22 * u :=
  tres_inyectivo 22 (-4194304) (-3) (by decide)

-- z negativo IMPAR con w par (el caso que baja por la mitad del w
-- no existe: aqui z debe ser multiplo, la premisa lo fuerza):
-- 3*(-32) = -96 = 2^5 * (-3)
example : ∃ u, (-32 : Int) = pot2 5 * u :=
  tres_inyectivo 5 (-32) (-3) (by decide)

-- ---------------------------------------------------------------
-- (3) una_clase_bit0 con c NEGATIVO (copiada verbatim + instancia):
--     c = -11 y c' = 21 comparten racha >= 4 tras bit 0
--     (3(-11)+1 = -32 = 2^5*(-1); 3*21+1 = 64 = 2^5*2) y el teorema
--     los pone en LA MISMA clase mod 2^5: -11 - 21 = -32 = 2^5*(-1).
-- ---------------------------------------------------------------
theorem una_clase_bit0 (c c' d d' : Int) (n : Nat)
    (h1 : 3 * c + 1 = pot2 n * d) (h2 : 3 * c' + 1 = pot2 n * d') :
    ∃ u, c - c' = pot2 n * u := by
  have h3 : 3 * (c - c') = pot2 n * (d - d') := by
    have hm : pot2 n * (d - d') = pot2 n * d - pot2 n * d' :=
      Int.mul_sub (pot2 n) d d'
    omega
  exact tres_inyectivo n (c - c') (d - d') h3

example : ∃ u, (-11 : Int) - 21 = pot2 5 * u :=
  una_clase_bit0 (-11) 21 (-1) 2 5 (by decide) (by decide)

#print axioms tres_inyectivo
#print axioms una_clase_bit0
