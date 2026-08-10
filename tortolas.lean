-- tortolas.lean
--
-- EL LEMA DEL ACOPLAMIENTO DE LA MONEDA (TORTOLAS, propuesto;
-- 10-08-2026). El nucleo aritmetico del lema de firmaacoplamiento.py:
-- los dos hijos de una moneda en (k, c par) de la cadena de Leonas
-- difieren en Delta = c + (1-3^k)/2, y bajo la MISMA palabra, mientras
-- las dos copias compartan paridad y ley (sin vortice asimetrico y sin
-- el signo mixto del unico abs), la diferencia evoluciona EXACTO por
-- +-1/2 o +-3/2: v2 baja 1 por paso y las paridades divergen JUSTO en
-- j* = v2(Delta).
--
-- LA FORMA (testigos sin division, estilo aterrizajen2.lean):
--   c par     = 2a            3^k = 2m+1 (m testigo)
--   c impar   = 2a+1          3^(k-1) = 2m'+1
--   las leyes:  N1: 2a -> a          N2: 2a -> 3a - m
--               N3: 2a+1 -> 3a+2     N4: 2a+1 -> a - m'
--               F1: 2a -> a          F2: 2a -> 3a
--               F3: 2a+1 -> 3a+2     F4: 2a+1 -> -(3a+1)
--               salida k=1: 2a+1 -> |a|  (el unico abs: la excepcion E2)
-- Cada teorema toma la MITAD D de la diferencia de preimagenes como
-- testigo (h : pre' - pre = 2*D) y entrega la diferencia de imagenes
-- como +-D o +-3*D: la "parte lineal" del lema, ley por ley, sin
-- dividir jamas.
--
-- EL CIERRE DEL DESCENSO: pot2_mitad (2^(j+1)*d = 2*(2^j*d)) engancha
-- el testigo D = 2^j*d de cada paso con el del siguiente;
-- impar_por_tres e impar_menos conservan la imparidad del corazon d;
-- y par_par_impar / impar_impar_impar dicen que una diferencia IMPAR
-- es incompatible con paridades iguales: en j* = v2(Delta), cuando el
-- testigo queda impar, las paridades divergen. La instancia del repo
-- (k=2, c=8: Delta=4, j*=2) esta cotejada con decide sobre las 4
-- palabras: paridades iguales en los pasos 0 y 1, divergencia en el
-- paso 2 exacto, con la transicion REAL de la cadena (funcion aparte,
-- solo para las instancias).
--
-- Verificacion cruzada sin codigo comun: firmaacoplamiento.py C0
-- (48.015 pruebas contra la cadena real, 0 fallos, excepciones E1/E2
-- una vez cada una). Nucleo puro, sin Mathlib. Control final:
-- #print axioms sin sorryAx.

def pot2 : Nat → Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

def pot3 : Nat → Int
  | 0 => 1
  | n + 1 => 3 * pot3 n

-- ---------------------------------------------------------------------
-- LA DIFERENCIA DE LOS HIJOS: con c = 2a y 3^k = 2m+1, los hijos de la
-- moneda son a (bit 0) y 3a - m (bit 1), y su diferencia es EXACTAMENTE
-- Delta = c + (1-3^k)/2 = 2a - m.
-- ---------------------------------------------------------------------

theorem delta_hijos (a m : Int) : (3 * a - m) - a = 2 * a - m := by omega

-- Delta = 0: la moneda sin efecto (los dos hijos son EL MISMO estado)
theorem moneda_sin_efecto (a m : Int) (h : 2 * a - m = 0) :
    3 * a - m = a := by omega

-- ---------------------------------------------------------------------
-- LAS LEYES, PAR A PAR (mismo bit, misma ley, testigo D = mitad de la
-- diferencia de preimagenes). Las /2: la diferencia de imagenes es D
-- (o -D en la salida negativa); las x3/2: es 3D (o -3D en F4).
-- ---------------------------------------------------------------------

-- N1 y F1 (c par, bit 0: 2a -> a)
theorem acopla_N1 (a b D : Int) (h : 2 * b - 2 * a = 2 * D) :
    b - a = D := by omega

-- N2 (c par, bit 1: 2a -> 3a - m, con 3^k = 2m+1 comun a las dos copias)
theorem acopla_N2 (a b m D : Int) (h : 2 * b - 2 * a = 2 * D) :
    (3 * b - m) - (3 * a - m) = 3 * D := by omega

-- N3 y F3 (c impar, bit 0: 2a+1 -> 3a+2)
theorem acopla_N3 (a b D : Int) (h : (2 * b + 1) - (2 * a + 1) = 2 * D) :
    (3 * b + 2) - (3 * a + 2) = 3 * D := by omega

-- N4 (k >= 2, c impar, bit 1: 2a+1 -> a - m', con 3^(k-1) = 2m'+1 comun)
theorem acopla_N4 (a b m D : Int) (h : (2 * b + 1) - (2 * a + 1) = 2 * D) :
    (b - m) - (a - m) = D := by omega

-- F2 (frontera, g par, bit 1: 2a -> 3a)
theorem acopla_F2 (a b D : Int) (h : 2 * b - 2 * a = 2 * D) :
    3 * b - 3 * a = 3 * D := by omega

-- F4 (frontera, g impar, bit 1: 2a+1 -> -(3a+1); el signo no toca v2)
theorem acopla_F4 (a b D : Int) (h : (2 * b + 1) - (2 * a + 1) = 2 * D) :
    (-(3 * b + 1)) - (-(3 * a + 1)) = -(3 * D) := by omega

-- la salida k=1 (c impar, bit 1: 2a+1 -> |a|), en sus dos casos de
-- MISMO signo: la diferencia de los valores absolutos es +-D
theorem acopla_salida_nonneg (a b D : Int) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h : (2 * b + 1) - (2 * a + 1) = 2 * D) :
    (b.natAbs : Int) - (a.natAbs : Int) = D := by omega

theorem acopla_salida_nonpos (a b D : Int) (ha : a ≤ 0) (hb : b ≤ 0)
    (h : (2 * b + 1) - (2 * a + 1) = 2 * D) :
    (b.natAbs : Int) - (a.natAbs : Int) = -D := by omega

-- y LA EXCEPCION E2, con su porque exacto: si los signos son OPUESTOS,
-- la diferencia de los abs no es la diferencia sino la SUMA -- el
-- salto de v2 que el lema exceptua (y que puede coalescer: b = -a)
theorem salida_signo_mixto (a b : Int) (ha : a ≤ 0) (hb : 0 ≤ b) :
    (b.natAbs : Int) - (a.natAbs : Int) = b + a := by omega

-- ---------------------------------------------------------------------
-- LA CONTABILIDAD DE v2: el testigo 2^(j+1)*d de un paso es 2 veces el
-- testigo 2^j*d del siguiente (el enganche del descenso), y ni el x3
-- ni el signo tocan la imparidad del corazon d.
-- ---------------------------------------------------------------------

theorem pot2_mitad (j : Nat) (d : Int) :
    pot2 (j + 1) * d = 2 * (pot2 j * d) := by
  show 2 * pot2 j * d = 2 * (pot2 j * d)
  rw [Int.mul_assoc]

theorem impar_por_tres (e : Int) : 3 * (2 * e + 1) = 2 * (3 * e + 1) + 1 := by
  omega

theorem impar_menos (e : Int) : -(2 * e + 1) = 2 * (-e - 1) + 1 := by
  omega

-- ---------------------------------------------------------------------
-- LA DIVERGENCIA: una diferencia IMPAR es incompatible con paridades
-- iguales -- en el paso j* el testigo queda impar y las copias se
-- separan. (Las dos formas: par-par e impar-impar.)
-- ---------------------------------------------------------------------

theorem par_par_impar (u v e : Int) (h : 2 * v - 2 * u = 2 * e + 1) :
    False := by omega

theorem impar_impar_impar (u v e : Int)
    (h : (2 * v + 1) - (2 * u + 1) = 2 * e + 1) : False := by omega

-- ---------------------------------------------------------------------
-- LA LEY DE LA MUERTE DE LA RACHA (10-08-2026, el sub-lema mod 4 del
-- lema local): los dos hijos de la moneda en (k, c par) son AMBOS
-- pares -- la racha compartida sigue segura -- exactamente cuando
-- a = c/2 es par Y m = (3^k - 1)/2 es par; y m es par si y solo si k
-- es par (3^k mod 4 alterna 3, 1, 3, 1...). En cualquier otro caso al
-- menos un bit mata la racha: la cola del reloj de los mixtos es
-- geometrica de tasa >= 1/2 (medido: P(racha >= j) * 2^j -> 0,9265).
-- Testigos: c = 2a, 3^k = 2m+1; hijos a y 3a - m.
-- ---------------------------------------------------------------------

-- si a y m son pares, ambos hijos son pares (la racha sigue)
theorem racha_sigue (u v : Int) : ∃ w, (3 * (2 * u) - 2 * v) = 2 * w := by
  exact ⟨3 * u - v, by omega⟩

-- si a es impar, el hijo 0 (= a) es impar: la racha muere con bit 0
theorem racha_muere_a_impar (u : Int) : 2 * u + 1 ≠ 2 * ((2 * u + 1) / 2) := by
  omega

-- si a es par y m es impar, el hijo 1 = 3a - m es impar: muere con bit 1
theorem racha_muere_m_impar (u v : Int) :
    3 * (2 * u) - (2 * v + 1) = 2 * (3 * u - v - 1) + 1 := by omega

-- y la alternancia de 3^k mod 4 que decide la paridad de m:
-- pot3 par = 4q + 1 (m par), pot3 impar = 4q + 3 (m impar)
theorem pot3_mod4 : ∀ n : Nat,
    (∃ q : Int, pot3 (2 * n) = 4 * q + 1) ∧
    (∃ q : Int, pot3 (2 * n + 1) = 4 * q + 3) := by
  intro n
  induction n with
  | zero => exact ⟨⟨0, rfl⟩, ⟨0, rfl⟩⟩
  | succ p ih =>
      cases ih with
      | intro hpar himp =>
        cases hpar with
        | intro q hq =>
          constructor
          · show ∃ r, pot3 (2 * p + 1 + 1) = 4 * r + 1
            cases himp with
            | intro s hs =>
              exact ⟨3 * s + 2, by show 3 * pot3 (2 * p + 1) = _; omega⟩
          · show ∃ r, pot3 (2 * p + 1 + 1 + 1) = 4 * r + 3
            cases himp with
            | intro s hs =>
              have h2 : pot3 (2 * p + 1 + 1) = 3 * pot3 (2 * p + 1) := rfl
              exact ⟨9 * s + 6, by
                show 3 * pot3 (2 * p + 1 + 1) = _
                rw [h2]; omega⟩

-- ---------------------------------------------------------------------
-- LA INSTANCIA DEL REPO, con la transicion REAL de la cadena
-- modificada (definida aqui solo para las instancias; los teoremas de
-- arriba no dividen). La moneda (k=2, c=8): hijos (2,4) y (2,8),
-- Delta = 4, j* = v2(4) = 2. Sobre LAS CUATRO palabras de largo 2:
-- paridades iguales en los pasos 0 y 1, divergencia EXACTA en el 2.
-- ---------------------------------------------------------------------

def paso : Nat × Int → Bool → Nat × Int
  | (0, c), false => if c % 2 = 0 then (0, c / 2) else (1, (3 * c + 1) / 2)
  | (0, c), true  => if c % 2 = 0 then (0, 3 * c / 2) else (1, (1 - 3 * c) / 2)
  | (k + 1, c), false =>
      if c % 2 = 0 then (k + 1, c / 2)
      else if k + 1 = 1 ∧ c = 1 then (2, 2)
      else (k + 2, (3 * c + 1) / 2)
  | (k + 1, c), true  =>
      if c % 2 = 0 then (k + 1, (3 * c + 1 - 3 ^ (k + 1)) / 2)
      else if k + 1 = 1 ∧ c = 1 then (2, 2)
      else if k + 1 = 1 then (0, ((c - 1) / 2).natAbs)
      else (k, (c - 3 ^ k) / 2)

def anda : Nat × Int → List Bool → Nat × Int
  | e, [] => e
  | e, b :: r => anda (paso e b) r

def paridad (e : Nat × Int) : Bool := e.2 % 2 = 0

-- los hijos de la moneda (2, 8) son (2, 4) y (2, 8)
theorem hijos_2_8 : paso (2, 8) false = (2, 4) ∧ paso (2, 8) true = (2, 8) := by
  decide

-- paridades iguales en los pasos 0 y 1, para las cuatro palabras
theorem acuerdo_antes :
    ([false, true].all fun b1 =>
      paridad (2, 4) = paridad (2, 8) ∧
      paridad (anda (2, 4) [b1]) = paridad (anda (2, 8) [b1])) = true := by
  decide

-- divergencia EXACTA en el paso 2 = v2(Delta) = v2(4), para las cuatro
theorem divergencia_en_2 :
    ([[false, false], [false, true], [true, false], [true, true]].all
      fun w => paridad (anda (2, 4) w) != paridad (anda (2, 8) w)) = true := by
  decide

-- y el testigo del descenso en esta instancia: Delta = 4 = pot2 2 * 1,
-- con el corazon d = 1 impar
theorem testigo_2_8 : (8 : Int) - 4 = pot2 2 * 1 ∧ pot2 2 * (1 : Int) = 4 := by
  decide

#print axioms delta_hijos
#print axioms moneda_sin_efecto
#print axioms acopla_N1
#print axioms acopla_N2
#print axioms acopla_N3
#print axioms acopla_N4
#print axioms acopla_F2
#print axioms acopla_F4
#print axioms acopla_salida_nonneg
#print axioms acopla_salida_nonpos
#print axioms salida_signo_mixto
#print axioms pot2_mitad
#print axioms impar_por_tres
#print axioms impar_menos
#print axioms par_par_impar
#print axioms impar_impar_impar
#print axioms racha_sigue
#print axioms racha_muere_a_impar
#print axioms racha_muere_m_impar
#print axioms pot3_mod4
#print axioms hijos_2_8
#print axioms acuerdo_antes
#print axioms divergencia_en_2
#print axioms testigo_2_8
