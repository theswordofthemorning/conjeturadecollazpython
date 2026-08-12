-- lecturaracha.lean
--
-- LA LECTURA DE LA RACHA -- TEOREMA DE VIBORAS (la lectura: leen
-- con la lengua los bits bajos) + TEOREMA DE AVISPAS (el aguijon:
-- k impar inyecta el bit fresco). Bautizados por orden del usuario
-- el 12-08-2026; el 20o .lean del repo.
-- El nucleo aritmetico de la reduccion de equidistribucionmixto.py:
-- la racha de pasos compartidos que sigue a un mixto LEE los bits
-- bajos de c en el momento del mixto, y la condicion "racha >= j"
-- es pertenecer a UNA SOLA clase mod 2^(j+1):
--
--   mixto bit 0 (c impar):        2h = 3c + 1   (h el hijo)
--     racha >= j  <=>  2^(j+1) | 3c + 1   (una clase: 3c = -1)
--   mixto bit 1 (c impar, k >= 3): 2h = c - 3^(k-1)
--     racha >= j  <=>  2^(j+1) | c - 3^(k-1)  (una clase)
--
-- Las dos direcciones van con testigos sin division (estilo
-- tortolas.lean); la UNICIDAD de la clase del bit 0 necesita la
-- inyectividad de x3 mod 2^n, demostrada por induccion (el unico
-- ingrediente no lineal). "racha >= j" aqui es "2^j | h": el largo
-- de racha es v2 del hijo salvo los desvios de la Pieza A
-- (aterrizajen2.lean), que este fichero NO toca -- esto es solo la
-- lectura de los bits, la palanca de la reduccion.
--
-- Instancias por el nucleo (decide): el contraejemplo del adv 1 de
-- la 9a revision (c0 = 1398101 = -3^(-1) mod 2^21: 3c+1 = 2^22
-- exacto -- la racha forzada) y el caso chico c = 5.
-- Verificacion cruzada sin codigo comun: equidistribucionmixto.py
-- (DP exacto + enumeracion 2^14, E1). Nucleo puro, sin Mathlib.
-- Control final: #print axioms sin sorryAx.

def pot2 : Nat → Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

def pot3 : Nat → Int
  | 0 => 1
  | n + 1 => 3 * pot3 n

-- el enganche de la mitad (como pot2_mitad de tortolas.lean)
theorem pot2_mitad (j : Nat) (d : Int) :
    pot2 (j + 1) * d = 2 * (pot2 j * d) := by
  show 2 * pot2 j * d = 2 * (pot2 j * d)
  rw [Int.mul_assoc]

-- ---------------------------------------------------------------------
-- LA LECTURA GENERICA: si 2h = n, entonces 2^j | h <=> 2^(j+1) | n.
-- (n sera 3c+1 en el bit 0 y c - 3^(k-1) en el bit 1.)
-- ---------------------------------------------------------------------

theorem mitad_lee_ida (n h d : Int) (j : Nat)
    (hh : 2 * h = n) (hd : n = pot2 (j + 1) * d) :
    h = pot2 j * d := by
  have he := pot2_mitad j d
  omega

theorem mitad_lee_vuelta (n h d : Int) (j : Nat)
    (hh : 2 * h = n) (hd : h = pot2 j * d) :
    n = pot2 (j + 1) * d := by
  have he := pot2_mitad j d
  omega

-- ---------------------------------------------------------------------
-- LAS DOS LECTURAS, instanciadas: el hijo del mixto hereda EXACTO un
-- bit menos que la congruencia de c.
-- ---------------------------------------------------------------------

-- bit 0: c impar, hijo h con 2h = 3c+1; racha >= j <=> 3c+1 = 2^(j+1) d
theorem lectura_bit0_ida (c h d : Int) (j : Nat)
    (hh : 2 * h = 3 * c + 1) (hd : 3 * c + 1 = pot2 (j + 1) * d) :
    h = pot2 j * d :=
  mitad_lee_ida (3 * c + 1) h d j hh hd

theorem lectura_bit0_vuelta (c h d : Int) (j : Nat)
    (hh : 2 * h = 3 * c + 1) (hd : h = pot2 j * d) :
    3 * c + 1 = pot2 (j + 1) * d :=
  mitad_lee_vuelta (3 * c + 1) h d j hh hd

-- bit 1: c impar, k >= 3, hijo h con 2h = c - p donde p = 3^(k-1)
theorem lectura_bit1_ida (c h p d : Int) (j : Nat)
    (hh : 2 * h = c - p) (hd : c - p = pot2 (j + 1) * d) :
    h = pot2 j * d :=
  mitad_lee_ida (c - p) h d j hh hd

theorem lectura_bit1_vuelta (c h p d : Int) (j : Nat)
    (hh : 2 * h = c - p) (hd : h = pot2 j * d) :
    c - p = pot2 (j + 1) * d :=
  mitad_lee_vuelta (c - p) h d j hh hd

-- ---------------------------------------------------------------------
-- LA UNICIDAD DE LA CLASE: x3 es inyectivo mod 2^n (el unico paso no
-- lineal, por induccion: 3z par => z par, y el descenso).
-- ---------------------------------------------------------------------

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
      -- 3z = 2*(2^m w): z es par (3 impar)
      have hz : z % 2 = 0 := by omega
      have hz2 : 3 * (z / 2) = pot2 m * w := by omega
      cases ih (z / 2) w hz2 with
      | intro u hu =>
          have he2 := pot2_mitad m u
          exact ⟨u, by omega⟩

-- el corolario del bit 0: dos c con racha >= j caen en LA MISMA clase
-- mod 2^(j+1) -- "racha >= j" es UNA congruencia, no muchas
theorem una_clase_bit0 (c c' d d' : Int) (n : Nat)
    (h1 : 3 * c + 1 = pot2 n * d) (h2 : 3 * c' + 1 = pot2 n * d') :
    ∃ u, c - c' = pot2 n * u := by
  have h3 : 3 * (c - c') = pot2 n * (d - d') := by
    have hm : pot2 n * (d - d') = pot2 n * d - pot2 n * d' :=
      Int.mul_sub (pot2 n) d d'
    omega
  exact tres_inyectivo n (c - c') (d - d') h3

-- el del bit 1 es lineal puro: misma p, la resta cancela
theorem una_clase_bit1 (c c' p d d' : Int) (n : Nat)
    (h1 : c - p = pot2 n * d) (h2 : c' - p = pot2 n * d') :
    ∃ u, c - c' = pot2 n * u := by
  exact ⟨d - d', by
    have hm : pot2 n * (d - d') = pot2 n * d - pot2 n * d' :=
      Int.mul_sub (pot2 n) d d'
    omega⟩

-- ---------------------------------------------------------------------
-- LA RECARGA ES LA MISMA LECTURA (la segunda equidistribucion de la
-- nota de dominacion ES la primera): en el paso compartido bit 1
-- (c par) el hijo cumple 2h = 3c + 1 - 3^k, y "el salto de recarga
-- sube s" es v2(h) >= A + s, o sea 2^(A+s+1) | 3c + 1 - 3^k --
-- otra vez UNA clase de c, por el mismo tres_inyectivo. Las "DOS
-- equidistribuciones POR ESCRIBIR" de notadominacion.txt son UN
-- SOLO objeto: la equidistribucion de c mod 2^m.
-- ---------------------------------------------------------------------

-- q sera 3^k; la lectura es la generica con n = 3c + 1 - q
theorem lectura_recarga_ida (c h q d : Int) (j : Nat)
    (hh : 2 * h = 3 * c + 1 - q) (hd : 3 * c + 1 - q = pot2 (j + 1) * d) :
    h = pot2 j * d :=
  mitad_lee_ida (3 * c + 1 - q) h d j hh hd

theorem lectura_recarga_vuelta (c h q d : Int) (j : Nat)
    (hh : 2 * h = 3 * c + 1 - q) (hd : h = pot2 j * d) :
    3 * c + 1 - q = pot2 (j + 1) * d :=
  mitad_lee_vuelta (3 * c + 1 - q) h d j hh hd

-- y la unicidad: dos c con salto >= s comparten clase mod 2^n
theorem una_clase_recarga (c c' q d d' : Int) (n : Nat)
    (h1 : 3 * c + 1 - q = pot2 n * d) (h2 : 3 * c' + 1 - q = pot2 n * d') :
    ∃ u, c - c' = pot2 n * u := by
  have h3 : 3 * (c - c') = pot2 n * (d - d') := by
    have hm : pot2 n * (d - d') = pot2 n * d - pot2 n * d' :=
      Int.mul_sub (pot2 n) d d'
    omega
  exact tres_inyectivo n (c - c') (d - d') h3

-- ---------------------------------------------------------------------
-- INSTANCIAS POR EL NUCLEO (decide, no #eval):
--   el contraejemplo del adv 1: c = 1398101, 3c+1 = 4194304 = 2^22
--   (la racha forzada >= 21 tras bit 0: el hijo es 2^21);
--   y el caso chico c = 5: 3c+1 = 16 = 2^4, hijo 8 = 2^3.
-- ---------------------------------------------------------------------

theorem caso_adversarial : 3 * (1398101 : Int) + 1 = pot2 22 * 1 := by
  decide

theorem caso_adversarial_hijo : 2 * (2097152 : Int) = 3 * 1398101 + 1 := by
  decide

theorem caso_chico : 3 * (5 : Int) + 1 = pot2 4 * 1 ∧
    2 * (8 : Int) = 3 * 5 + 1 ∧ (8 : Int) = pot2 3 * 1 := by
  decide

-- el caso del bit 1 con el repo: c = 11, k = 3 (p = 9): c - p = 2,
-- el hijo es 1 = 2^0 * 1 y la racha para en j = 0... con d = 1:
theorem caso_bit1 : (11 : Int) - pot3 2 = pot2 1 * 1 ∧
    2 * (1 : Int) = 11 - pot3 2 := by
  decide

-- ---------------------------------------------------------------------
-- EL MECANISMO DE INYECCION DE BITS (la otra mitad del conteo, la
-- 3.i de notaequidistribucion.txt): en un paso compartido desde
-- (k, c par), los dos hijos son a y 3a - m con 3^k = 2m + 1
-- (tortolas.lean, delta_hijos). La paridad de m DECIDE:
--   k IMPAR:  m impar  ==> los hijos difieren mod 2 -- el bit de
--             la palabra aterriza como bit FRESCO en la posicion 0
--   k PAR:    m par    ==> los hijos comparten paridad: sin
--             inyeccion inmediata (v2(Delta) = 1 + v2(a - m/2))
-- La alternancia de la paridad de m es 3^k mod 4 = 1, 3, 1, 3, ...
-- (la misma identidad que borde_alterna de perrasconteo.lean, aqui
-- sobre Int y con el testigo explicito).
-- ---------------------------------------------------------------------

-- 3^k mod 4, con testigo: k par -> 4e+1, k impar -> 4e+3
theorem pot3_mod4 (k : Nat) :
    (k % 2 = 0 ∧ ∃ e, pot3 k = 4 * e + 1) ∨
    (k % 2 = 1 ∧ ∃ e, pot3 k = 4 * e + 3) := by
  induction k with
  | zero => exact Or.inl ⟨rfl, ⟨0, rfl⟩⟩
  | succ n ih =>
      cases ih with
      | inl h =>
          cases h.2 with
          | intro e he =>
              refine Or.inr ⟨by omega, ⟨3 * e, ?_⟩⟩
              show 3 * pot3 n = 4 * (3 * e) + 3
              omega
      | inr h =>
          cases h.2 with
          | intro e he =>
              refine Or.inl ⟨by omega, ⟨3 * e + 2, ?_⟩⟩
              show 3 * pot3 n = 4 * (3 * e + 2) + 1
              omega

-- k impar: la mitad m de 3^k = 2m+1 es IMPAR
theorem mitad_impar (k : Nat) (hk : k % 2 = 1) :
    ∃ m, pot3 k = 2 * m + 1 ∧ m % 2 = 1 := by
  cases pot3_mod4 k with
  | inl h => exfalso; omega
  | inr h =>
      cases h.2 with
      | intro e he => exact ⟨2 * e + 1, by omega, by omega⟩

-- k par: la mitad m es PAR
theorem mitad_par (k : Nat) (hk : k % 2 = 0) :
    ∃ m, pot3 k = 2 * m + 1 ∧ m % 2 = 0 := by
  cases pot3_mod4 k with
  | inl h =>
      cases h.2 with
      | intro e he => exact ⟨2 * e, by omega, by omega⟩
  | inr h => exfalso; omega

-- la inyeccion: m impar ==> los hijos a y 3a - m difieren mod 2
theorem inyeccion_bit (a m : Int) (hm : m % 2 = 1) :
    (3 * a - m) % 2 ≠ a % 2 := by omega

-- y su negacion: m par ==> misma paridad (sin bit fresco)
theorem sin_inyeccion (a m : Int) (hm : m % 2 = 0) :
    (3 * a - m) % 2 = a % 2 := by omega

-- instancias por el nucleo: k = 1 (m = 1, inyecta), k = 2 (m = 4,
-- no inyecta), k = 3 (m = 13, inyecta)
theorem casos_inyeccion : pot3 1 = 2 * 1 + 1 ∧ pot3 2 = 2 * 4 + 1 ∧
    pot3 3 = 2 * 13 + 1 := by decide

-- instancia de recarga con el repo (k = 2, A = v2(3^2-1) = 3):
-- c = 8: v2 = 3 = A, hijo h = (3*8 + 1 - 9)/2 = 8, v2(h) = 3 = A + 0
theorem caso_recarga : 2 * (8 : Int) = 3 * 8 + 1 - pot3 2 ∧
    (8 : Int) = pot2 3 * 1 := by decide

#print axioms mitad_lee_ida
#print axioms mitad_lee_vuelta
#print axioms tres_inyectivo
#print axioms una_clase_bit0
#print axioms una_clase_bit1
#print axioms lectura_recarga_ida
#print axioms una_clase_recarga
#print axioms pot3_mod4
#print axioms mitad_impar
#print axioms inyeccion_bit
#print axioms caso_adversarial
