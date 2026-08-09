-- urracas.lean
--
-- LA CONTABILIDAD DEL SESGO, demostrada en el nucleo (09-08-2026).
-- El teorema de URRACAS: en la cadena modificada (liebres.py), a lo
-- largo de TODA palabra vale la igualdad de enteros
--
--     exp - contr  =  2·V + (Ee - E0) + k0 - k_t
--
-- donde exp/contr son los pasos expansivos/contractivos (la
-- clasificacion de CEBRAS), V las visitas al vortice con bit 1 y
-- Ee - E0 el desbalance de bits en los pasos con c par.
--
-- La forma: un paso de la cadena es una relacion `Paso` con NUEVE
-- constructores (testigos sin division, estilo hormigas.lean); el
-- `libro` es la cantidad  exp - contr - 2·V - (Ee-E0) + k;  se
-- demuestra que CADA paso conserva el libro, que todo `Camino`
-- (palabra) lo conserva por induccion, y el teorema sale evaluando el
-- libro en el arranque (contadores a cero: libro = k0).
--
-- La exhaustividad de los nueve constructores contra la cadena real
-- la verifica la COMPROBACION 0 de urracas.py sobre la rejilla
-- k <= 9, |c| <= 2000: las formulas de aqui son EXACTAMENTE las de
-- tipo_de_paso() alli. Lean garantiza demostracion <-> enunciado; el
-- enunciado <-> objeto lo cierra ese barrido.
--
-- Nucleo puro, sin Mathlib. Control final: #print axioms sin sorryAx.

-- 3^k con definicion propia (para no depender de lemas de pow)
def pot3 : Nat → Int
  | 0 => 1
  | n + 1 => 3 * pot3 n

-- los testigos de imparidad de 3^k existen siempre
theorem pot3_impar : (n : Nat) → ∃ m : Int, pot3 n = 2 * m + 1
  | 0 => ⟨0, rfl⟩
  | n + 1 =>
    match pot3_impar n with
    | ⟨m, h⟩ => ⟨3 * m + 1, by unfold pot3; rw [h]; omega⟩

-- cruce con valores conocidos (por decide, no por #eval)
theorem pot3_valores :
    pot3 0 = 1 ∧ pot3 1 = 3 ∧ pot3 2 = 9 ∧ pot3 3 = 27 ∧
    pot3 4 = 81 ∧ pot3 5 = 243 ∧ pot3 6 = 729 := by decide

-- el estado con su libro: (k, c) y los cuatro contadores
structure Estado where
  k : Nat        -- la altura de la torre
  c : Int        -- la deuda
  exp : Int      -- pasos expansivos (CEBRAS)
  contr : Int    -- pasos contractivos
  vor : Int      -- visitas al vortice con bit 1 (rebotes)
  dif : Int      -- Ee - E0: desbalance de bits en pasos con c par

def libro : Estado → Int
  | ⟨k, _, e, x, v, f⟩ => e - x - 2 * v - f + (k : Int)

-- LOS NUEVE TIPOS DE PASO (el espejo exacto de tipo_de_paso() en
-- urracas.py; d, m son testigos: c par = 2d, c impar = 2d+1,
-- pot3 k = 2m+1). Nombres: f_ = frontera (k = 0), n_ = nucleo.
inductive Paso : Estado → Estado → Prop where
  | f_par0 (d e x v f : Int) (hd : 1 ≤ d) :
      Paso ⟨0, 2 * d, e, x, v, f⟩ ⟨0, d, e, x + 1, v, f - 1⟩
  | f_par1 (d e x v f : Int) (hd : 1 ≤ d) :
      Paso ⟨0, 2 * d, e, x, v, f⟩ ⟨0, 3 * d, e + 1, x, v, f + 1⟩
  | f_impar0 (d e x v f : Int) (hd : 0 ≤ d) :
      Paso ⟨0, 2 * d + 1, e, x, v, f⟩ ⟨1, 3 * d + 2, e, x + 1, v, f⟩
  | f_impar1 (d e x v f : Int) (hd : 0 ≤ d) :
      Paso ⟨0, 2 * d + 1, e, x, v, f⟩ ⟨1, -(3 * d + 1), e, x + 1, v, f⟩
  | n_par0 (k : Nat) (d e x v f : Int) :
      Paso ⟨k + 1, 2 * d, e, x, v, f⟩ ⟨k + 1, d, e, x + 1, v, f - 1⟩
  | n_par1 (k : Nat) (d m e x v f : Int) (hm : pot3 (k + 1) = 2 * m + 1) :
      Paso ⟨k + 1, 2 * d, e, x, v, f⟩ ⟨k + 1, 3 * d - m, e + 1, x, v, f + 1⟩
  | n_impar0 (k : Nat) (d e x v f : Int) :
      Paso ⟨k + 1, 2 * d + 1, e, x, v, f⟩ ⟨k + 2, 3 * d + 2, e, x + 1, v, f⟩
  | n_impar1 (k : Nat) (d m e x v f : Int) (hm : pot3 (k + 1) = 2 * m + 1) :
      Paso ⟨k + 2, 2 * d + 1, e, x, v, f⟩ ⟨k + 1, d - m, e + 1, x, v, f⟩
  | salida_pos (d e x v f : Int) (hd : 1 ≤ d) :
      Paso ⟨1, 2 * d + 1, e, x, v, f⟩ ⟨0, d, e + 1, x, v, f⟩
  | salida_neg (d e x v f : Int) (hd : d ≤ -1) :
      Paso ⟨1, 2 * d + 1, e, x, v, f⟩ ⟨0, -d, e + 1, x, v, f⟩
  | rebote (e x v f : Int) :
      Paso ⟨1, 1, e, x, v, f⟩ ⟨2, 2, e + 1, x, v + 1, f⟩

-- EL LEMA DEL LIBRO: cada uno de los once constructores (nueve tipos;
-- el 3 y el 8 tienen dos ramas) conserva el libro
theorem paso_libro {a b : Estado} (h : Paso a b) : libro b = libro a := by
  cases h <;> (simp only [libro]; omega)

-- una palabra es una cadena de pasos
inductive Camino : Estado → Estado → Prop where
  | quieta (s : Estado) : Camino s s
  | anda {a b c : Estado} (cab : Camino a b) (pbc : Paso b c) : Camino a c

theorem camino_libro {a b : Estado} (h : Camino a b) : libro b = libro a := by
  induction h with
  | quieta => rfl
  | anda cab pbc ih => rw [paso_libro pbc, ih]

-- EL TEOREMA DE URRACAS: desde contadores a cero, al final de toda
-- palabra vale  exp - contr = 2·V + (Ee - E0) + k0 - k_t
theorem urracas (k0 : Nat) (c0 : Int) {s : Estado}
    (h : Camino ⟨k0, c0, 0, 0, 0, 0⟩ s) :
    s.exp - s.contr = 2 * s.vor + s.dif + (k0 : Int) - (s.k : Int) := by
  have hb := camino_libro h
  cases s with
  | mk k c e x v f =>
    simp only [libro] at hb
    show e - x = 2 * v + f + (k0 : Int) - (k : Int)
    omega

-- EL CASO CONOCIDO DEL REPO: el camino de ida de la COMPROBACION 1 de
-- liebres.py, (0,1) -bit0-> (1,2) -bit0-> (1,1), con su contabilidad
theorem caso_ida :
    Camino ⟨0, 1, 0, 0, 0, 0⟩ ⟨1, 1, 0, 2, 0, -1⟩ := by
  apply Camino.anda (c := ⟨1, 1, 0, 2, 0, -1⟩)
    (b := ⟨1, 2, 0, 1, 0, 0⟩)
  · apply Camino.anda (Camino.quieta _)
    show Paso ⟨0, 2 * 0 + 1, 0, 0, 0, 0⟩ ⟨1, 3 * 0 + 2, 0, 0 + 1, 0, 0⟩
    exact Paso.f_impar0 0 0 0 0 0 (by omega)
  · show Paso ⟨0 + 1, 2 * 1, 0, 1, 0, 0⟩ ⟨0 + 1, 1, 0, 1 + 1, 0, 0 - 1⟩
    exact Paso.n_par0 0 1 0 1 0 0

-- y la identidad del caso, cerrada por el teorema y por decide:
-- exp - contr = -2  y  2·V + dif + k0 - k = 0 + (-1) + 0 - 1 = -2
theorem caso_ida_identidad :
    (0 : Int) - 2 = 2 * 0 + (-1) + ((0 : Nat) : Int) - ((1 : Nat) : Int) := by
  decide

-- EL REGALO DEL VORTICE: los dos bits del vortice aterrizan en (2,2) --
-- el bit 1 por el rebote (tipo 9, unico que mueve V) y el bit 0 por el
-- tipo 6 con d = 0. Lean lo ve sin calculadora:
theorem vortice_bit1 (e x v f : Int) :
    Paso ⟨1, 1, e, x, v, f⟩ ⟨2, 2, e + 1, x, v + 1, f⟩ :=
  Paso.rebote e x v f

theorem vortice_bit0 (e x v f : Int) :
    Paso ⟨1, 1, e, x, v, f⟩ ⟨2, 2, e, x + 1, v, f⟩ := by
  show Paso ⟨0 + 1, 2 * 0 + 1, e, x, v, f⟩ ⟨0 + 2, 3 * 0 + 2, e, x + 1, v, f⟩
  exact Paso.n_impar0 0 0 e x v f

#print axioms paso_libro
#print axioms camino_libro
#print axioms urracas
#print axioms caso_ida
#print axioms vortice_bit0
