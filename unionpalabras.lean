-- unionpalabras.lean
--
-- LA UNION POR PALABRAS -- TEOREMA DE LORAS (leen la palabra
-- entera; bautizado el 12-08-2026 por delegacion del usuario) --
-- el sub-lema (a) del teorema de conteo, nacido de la 10a revision
-- adversarial (acta actarevision1208.txt, M1): el compuesto de
-- recargas via E[2^salto] estaba roto desde siempre, y este lema
-- lo reemplaza. El 21o .lean del repo; nucleo puro, sin Mathlib,
-- 0 sorryAx.
--
-- QUE DICE. Tras un mixto, la racha de pasos compartidos avanza con
-- SOLO DOS leyes (la cadena (k, c) con c par en todo el tramo):
--
--   division (bit 0 compartido):  2 h' = h            (c -> c/2)
--   recarga  (bit 1 compartido):  2 h' = 3 h + 1 - q  (q = 3^k)
--
-- y durante la racha k NO cambia (los dos miembros del par
-- multiplican por 3 a la vez: la razon 3^k se conserva), asi que q
-- es constante en la corrida real. AQUI q es un PARAMETRO LIBRE por
-- paso: el lema demostrado es MAS FUERTE que lo que la cadena
-- necesita (vale para cualquier sucesion de q, en particular la
-- real, que ademas queda fijada por la palabra y la altura de
-- entrada -- las dos trayectorias comparadas llevan LA MISMA).
--
-- EL TEOREMA: si dos arranques c y c' del mixto (bit 0 o bit 1)
-- sobreviven la MISMA palabra de j leyes (cada paso exige que el
-- doble del siguiente sea el valor afin: la integralidad ES la
-- supervivencia), entonces c = c' mod 2^(j+1): "racha >= j con
-- palabra u" es A LO SUMO UNA clase mod 2^(j+1). Esa unicidad es
-- exactamente lo que la union sobre palabras necesita:
--   P(racha_total >= j | mixto) <= max_clase <= sqrt(C2) 2^-(j+1)/2
-- (notaequidistribucion.txt 3.iv, la via que reemplaza al
-- compuesto). El ingrediente no lineal es el mismo de siempre:
-- tres_inyectivo (x3 inyectivo mod 2^n), aqui re-demostrado para
-- que el fichero compile solo (mismo enunciado que
-- lecturaracha.lean).
--
-- Verificacion cruzada sin codigo comun: el barrido exhaustivo del
-- adversario 1 de la 10a (revision10_adv1/compuesto_l2.py: 1.016
-- combinaciones, k = 3..6, ambos bits, j = 1..7, todas las
-- palabras) y el cruce fresco de esta sesion (union_cruce.py).
-- Control final: #print axioms sin sorryAx.

def pot2 : Nat → Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

-- el enganche de la mitad (identico a lecturaracha.lean)
theorem pot2_mitad (j : Nat) (d : Int) :
    pot2 (j + 1) * d = 2 * (pot2 j * d) := by
  show 2 * pot2 j * d = 2 * (pot2 j * d)
  rw [Int.mul_assoc]

-- x3 inyectivo mod 2^n (mismo enunciado y prueba que lecturaracha)
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

-- ---------------------------------------------------------------------
-- LA PALABRA: una lista de leyes. La corrida "corre h L g" dice que
-- desde h, aplicando las leyes de L en orden, se llega a g con TODOS
-- los pasos enteros (el ∃ h1 con 2*h1 = ... fuerza la paridad del
-- valor corriente en cada paso: sobrevivir la palabra ES la racha).
-- ---------------------------------------------------------------------

inductive Ley where
  | division : Ley
  | recarga : Int → Ley

def paso : Int → Ley → Int → Prop
  | h, Ley.division, h' => 2 * h' = h
  | h, Ley.recarga q, h' => 2 * h' = 3 * h + 1 - q

def corre : Int → List Ley → Int → Prop
  | h, [], g => g = h
  | h, ley :: resto, g => ∃ h1, paso h ley h1 ∧ corre h1 resto g

-- ---------------------------------------------------------------------
-- EL CORAZON: dos corridas de la MISMA palabra comparten clase --
-- cada paso dobla el modulo (division es lineal directa; recarga
-- pasa por tres_inyectivo). Induccion sobre la palabra.
-- ---------------------------------------------------------------------

theorem corre_comparte : ∀ (L : List Ley) (h h' g g' : Int),
    corre h L g → corre h' L g' →
    ∃ v, h - h' = pot2 (List.length L) * v := by
  intro L
  induction L with
  | nil =>
      intro h h' g g' r1 r2
      have e1 : g = h := r1
      have e2 : g' = h' := r2
      exact ⟨h - h', by
        show h - h' = pot2 0 * (h - h')
        have h0 : pot2 0 = 1 := rfl
        rw [h0]
        omega⟩
  | cons ley resto ih =>
      intro h h' g g' r1 r2
      cases r1 with
      | intro h1 hp1 =>
          cases r2 with
          | intro h1' hp1' =>
              cases ih h1 h1' g g' hp1.2 hp1'.2 with
              | intro v hv =>
                  cases ley with
                  | division =>
                      have e1 : 2 * h1 = h := hp1.1
                      have e2 : 2 * h1' = h' := hp1'.1
                      show ∃ u, h - h' = pot2 (List.length resto + 1) * u
                      exact ⟨v, by
                        have he := pot2_mitad (List.length resto) v
                        omega⟩
                  | recarga q =>
                      have e1 : 2 * h1 = 3 * h + 1 - q := hp1.1
                      have e2 : 2 * h1' = 3 * h' + 1 - q := hp1'.1
                      show ∃ u, h - h' = pot2 (List.length resto + 1) * u
                      have h3 : 3 * (h - h') =
                          pot2 (List.length resto + 1) * v := by
                        have he := pot2_mitad (List.length resto) v
                        omega
                      exact tres_inyectivo (List.length resto + 1)
                        (h - h') v h3

-- ---------------------------------------------------------------------
-- LAS DOS PUERTAS DEL MIXTO: el paso de entrada aporta el bit que
-- falta -- "racha >= j con palabra u" es A LO SUMO UNA clase de c
-- mod 2^(j+1), para CUALQUIER palabra u de largo j.
-- ---------------------------------------------------------------------

-- mixto bit 0: 2h = 3c + 1 (la entrada multiplica por 3: el bit
-- extra tambien pasa por tres_inyectivo)
theorem una_clase_palabra_bit0 (c c' h h' g g' : Int) (L : List Ley)
    (m1 : 2 * h = 3 * c + 1) (m2 : 2 * h' = 3 * c' + 1)
    (r1 : corre h L g) (r2 : corre h' L g') :
    ∃ u, c - c' = pot2 (List.length L + 1) * u := by
  cases corre_comparte L h h' g g' r1 r2 with
  | intro v hv =>
      have h3 : 3 * (c - c') = pot2 (List.length L + 1) * v := by
        have he := pot2_mitad (List.length L) v
        omega
      exact tres_inyectivo (List.length L + 1) (c - c') v h3

-- mixto bit 1: 2h = c - p (p = 3^(k-1); la entrada es lineal y la
-- misma p cancela en la resta)
theorem una_clase_palabra_bit1 (c c' p h h' g g' : Int) (L : List Ley)
    (m1 : 2 * h = c - p) (m2 : 2 * h' = c' - p)
    (r1 : corre h L g) (r2 : corre h' L g') :
    ∃ u, c - c' = pot2 (List.length L + 1) * u := by
  cases corre_comparte L h h' g g' r1 r2 with
  | intro v hv =>
      exact ⟨v, by
        have he := pot2_mitad (List.length L) v
        omega⟩

-- ---------------------------------------------------------------------
-- INSTANCIAS POR EL NUCLEO. Las corridas llevan testigos explicitos
-- (corre es un ∃: no es decidable -- los testigos son los valores
-- reales de la cadena); las igualdades aritmeticas van por decide.
-- ---------------------------------------------------------------------

-- c = 5, mixto bit 0: hijo 8, palabra [div, div, div]: 8 -> 4 -> 2
-- -> 1 (la racha del caso chico de lecturaracha.lean)
theorem corrida_c5 :
    corre 8 [Ley.division, Ley.division, Ley.division] 1 :=
  ⟨4, by show (2 : Int) * 4 = 8; decide,
   ⟨2, by show (2 : Int) * 2 = 4; decide,
    ⟨1, by show (2 : Int) * 1 = 2; decide,
     by show (1 : Int) = 1; decide⟩⟩⟩

-- c' = 21, mismo mixto y MISMA palabra: hijo 32, 32 -> 16 -> 8 -> 4
theorem corrida_c21 :
    corre 32 [Ley.division, Ley.division, Ley.division] 4 :=
  ⟨16, by show (2 : Int) * 16 = 32; decide,
   ⟨8, by show (2 : Int) * 8 = 16; decide,
    ⟨4, by show (2 : Int) * 4 = 8; decide,
     by show (4 : Int) = 4; decide⟩⟩⟩

-- y la clase compartida que el teorema predice: c - c' = 5 - 21 =
-- -16 = 2^4 * (-1) -- mod 2^(3+1), como debe ser
theorem clase_c5_c21 : (5 : Int) - 21 = pot2 4 * (-1) := by decide

-- una corrida CON recarga (k = 2, q = 3^2 = 9): 8 -> (3*8+1-9)/2 =
-- 8 -> 4 -- la recarga del caso de lecturaracha.lean, seguida de
-- una division
theorem corrida_recarga :
    corre 8 [Ley.recarga 9, Ley.division] 4 :=
  ⟨8, by show (2 : Int) * 8 = 3 * 8 + 1 - 9; decide,
   ⟨4, by show (2 : Int) * 4 = 8; decide,
    by show (4 : Int) = 4; decide⟩⟩

-- y su companera por la misma palabra: 16 -> (3*16+1-9)/2 = 20 ->
-- 10; los arranques 8 y 16 difieren en 8 = 2^3 * 1 (mod 2^(2+1)
-- comparten clase: el corre_comparte con L de largo 2 pide 2^2 | 8)
theorem corrida_recarga_b :
    corre 16 [Ley.recarga 9, Ley.division] 10 :=
  ⟨20, by show (2 : Int) * 20 = 3 * 16 + 1 - 9; decide,
   ⟨10, by show (2 : Int) * 10 = 20; decide,
    by show (10 : Int) = 10; decide⟩⟩

theorem clase_recargas : (8 : Int) - 16 = pot2 3 * (-1) := by decide

#print axioms tres_inyectivo
#print axioms corre_comparte
#print axioms una_clase_palabra_bit0
#print axioms una_clase_palabra_bit1
#print axioms corrida_c5
#print axioms corrida_recarga
#print axioms clase_c5_c21
