/-
ITEM A13 -- el espejo en base 2.

ENUNCIADO DE LA BASE: "el espejo en base 2 baja estrictamente, luego toda
orbita cae en una potencia de 2", ambito todo n >= 1.

EL MAPA (lo defino yo, sin mirar ningun fichero del repo): el espejo de n
dentro de su bloque binario. Si 2^j <= n < 2^(j+1) (o sea j = Nat.log2 n),
entonces  espejo(n) = 2^(j+1) - n.
  - las potencias de 2 son PUNTOS FIJOS:  espejo(2^j) = 2^j
  - fuera de las potencias (2^j < n < 2^(j+1)) el espejo BAJA ESTRICTO:
    espejo(n) < 2^j < n  -- que es la "linea de algebra" de la ficha.

NO es Collatz: aqui no hay 3n+1 ni division entre 2. El unico contacto con
los tres mapas del repo es que este enunciado no usa ninguno.

Lo que se demuestra:
  1. espejo_potencia : las potencias de 2 son puntos fijos (para todo j)
  2. espejo_baja     : n >= 1 y n no potencia de 2  ==>  espejo n < n
     (el "baja estrictamente" NECESITA esa hipotesis: en una potencia no baja)
  3. cae             : para TODO n >= 1 existe t y j con  itera t n = 2^j
     (la conclusion del enunciado, por buena fundacion de <)
  4. casos concretos cerrados por el NUCLEO con `decide`, no con #eval:
     la orbita del 221 (221 -> 35 -> 29 -> 3 -> 1 = 2^0) y los bordes
     n = 1, n = 2, n = 64.
-/

set_option maxRecDepth 40000

def espejo (n : Nat) : Nat := 2 ^ (Nat.log2 n + 1) - n

def itera : Nat → Nat → Nat
  | 0,     n => n
  | t + 1, n => itera t (espejo n)

-- ---------------------------------------------------------------------
-- 0. control del objeto: casos concretos, decididos por el nucleo
-- ---------------------------------------------------------------------

-- la orbita del 221:  221 -> 35 -> 29 -> 3 -> 1  y  1 = 2^0
theorem caso_espejo_221 : espejo 221 = 35 := by decide
theorem caso_orbita_221 : itera 4 221 = 2 ^ 0 := by decide

-- bordes: n = 1 y n = 2 son fijos ya; un fijo grande; y un impar tipico
theorem caso_fijo_1  : espejo 1 = 1 := by decide
theorem caso_fijo_2  : espejo 2 = 2 := by decide
theorem caso_fijo_64 : espejo 64 = 64 := by decide
theorem caso_7 : espejo 7 = 1 := by decide
theorem caso_orbita_100 : itera 3 100 = 2 ^ 2 := by decide

-- ---------------------------------------------------------------------
-- 1. log2 de una potencia, y las potencias son puntos fijos
-- ---------------------------------------------------------------------

theorem log2_pow (j : Nat) : Nat.log2 (2 ^ j) = j := by
  have hpos : 0 < 2 ^ j := Nat.two_pow_pos j
  have hne : 2 ^ j ≠ 0 := by omega
  -- cota superior: log2 (2^j) < j+1 porque 2^j < 2^(j+1)
  have harriba : Nat.log2 (2 ^ j) < j + 1 := by
    have h2 : 2 ^ j < 2 ^ (j + 1) := by
      rw [Nat.pow_succ]; omega
    exact (Nat.log2_lt hne).mpr h2
  -- cota inferior: no puede ser log2 (2^j) < j, daria 2^j < 2^j
  have habajo : ¬ Nat.log2 (2 ^ j) < j := by
    intro hc
    have : 2 ^ j < 2 ^ j := (Nat.log2_lt hne).mp hc
    omega
  omega

theorem espejo_potencia (j : Nat) : espejo (2 ^ j) = 2 ^ j := by
  unfold espejo
  rw [log2_pow, Nat.pow_succ]
  have hpos : 0 < 2 ^ j := Nat.two_pow_pos j
  omega

-- ---------------------------------------------------------------------
-- 2. el descenso estricto (fuera de las potencias de 2)
-- ---------------------------------------------------------------------

-- la "linea de algebra" de la ficha: si 2^j < n < 2^(j+1)
-- entonces 2^(j+1) - n < 2^j < n.
theorem espejo_baja (n : Nat) (h1 : 1 ≤ n) (hp : n ≠ 2 ^ Nat.log2 n) :
    espejo n < n := by
  have hne : n ≠ 0 := by omega
  have hlow : 2 ^ Nat.log2 n ≤ n := Nat.log2_self_le hne
  have hup : n < 2 ^ (Nat.log2 n + 1) :=
    (Nat.log2_lt hne).mp (Nat.lt_succ_self _)
  unfold espejo
  rw [Nat.pow_succ] at hup ⊢
  -- con a = 2^(log2 n):  a <= n, n ≠ a, n < a*2  ==>  a*2 - n < a < n
  omega

-- y el espejo nunca cae a 0 (necesario para iterar dentro del ambito n >= 1)
theorem espejo_pos (n : Nat) (h1 : 1 ≤ n) : 1 ≤ espejo n := by
  have hne : n ≠ 0 := by omega
  have hup : n < 2 ^ (Nat.log2 n + 1) :=
    (Nat.log2_lt hne).mp (Nat.lt_succ_self _)
  unfold espejo
  omega

-- ---------------------------------------------------------------------
-- 3. el teorema principal: toda orbita cae en una potencia de 2
-- ---------------------------------------------------------------------

theorem cae (n : Nat) (h : 1 ≤ n) : ∃ t j, itera t n = 2 ^ j := by
  by_cases hp : n = 2 ^ Nat.log2 n
  · -- n YA es una potencia de 2: t = 0
    exact ⟨0, Nat.log2 n, hp⟩
  · -- n no es potencia: el espejo baja estricto y se recurre
    have hb : espejo n < n := espejo_baja n h hp
    have h1 : 1 ≤ espejo n := espejo_pos n h
    have hrec := cae (espejo n) h1
    cases hrec with
    | intro t hj =>
      cases hj with
      | intro j ht => exact ⟨t + 1, j, ht⟩
termination_by n
decreasing_by exact hb

-- ---------------------------------------------------------------------
-- 4. los controles de axiomas
-- ---------------------------------------------------------------------

#print axioms caso_espejo_221
#print axioms caso_orbita_221
#print axioms caso_fijo_1
#print axioms caso_fijo_2
#print axioms caso_fijo_64
#print axioms log2_pow
#print axioms espejo_potencia
#print axioms espejo_baja
#print axioms espejo_pos
#print axioms cae
