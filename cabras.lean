-- cabras.lean
--
-- EL INVARIANTE MOD 3 DE LA TORRE, demostrado en el nucleo (09-08-2026,
-- noche). En la cadena modificada (liebres.py), desde CUALQUIER
-- arranque en la frontera (k = 0), todo estado alcanzado con k >= 1
-- cumple  c % 3 ≠ 0  (de hecho c % 3 ∈ {1, 2}): LA TORRE NUNCA FABRICA
-- MULTIPLOS DE 3. Corolarios: (k, 0) es inalcanzable para todo k >= 1,
-- el salto de c = 0 en las COMPROBACIONES 0 de liebres.py y urracas.py
-- es inocuo, y los estados con 3 | c del conjunto C de Doeblin son
-- fantasmas que solo abaratan eps.
--
-- Procedencia: regalo del informe 1 de la 5a revision externa
-- (actarevision0908b.txt, punto 4) -- que resulto ser LA PUERTA MOD 3
-- DE CABRAS (subrenovacionc.py: directa -> clase 2, vuelco -> clase 1,
-- nunca 0) viajando por la cadena entera. Lo nuevo aqui: la ENTRADA a
-- la torre siempre da c ≡ 2 (los cuatro caminos: f_impar0, f_impar1,
-- y dentro de la torre n_par1 y n_impar0 "resetean" a 2), los pasos
-- internos solo alternan {1, 2}, y el todo queda formalizado con la
-- inalcanzabilidad como teorema.
--
-- La mecanica: mismo esqueleto que urracas.lean (los once
-- constructores con testigos sin division, espejo de tipo_de_paso()
-- en urracas.py, alli verificado contra modificada() y contra pares
-- enteros reales por la 5a revision), SIN los contadores: aqui solo
-- viaja la clase mod 3. Verificacion externa de esta sesion: BFS
-- propio desde (0,1) -- 3.056.054 estados, profundidad 32, CERO
-- estados de torre con 3 | c, clases vistas en la torre = {1, 2}.
--
-- Nucleo puro, sin Mathlib. Control final: #print axioms sin sorryAx.

def pot3 : Nat → Int
  | 0 => 1
  | n + 1 => 3 * pot3 n

theorem pot3_impar : (n : Nat) → ∃ m : Int, pot3 n = 2 * m + 1
  | 0 => ⟨0, rfl⟩
  | n + 1 =>
    match pot3_impar n with
    | ⟨m, h⟩ => ⟨3 * m + 1, by unfold pot3; rw [h]; omega⟩

-- 3^(n+1) es multiplo de 3: la llave de los "reseteos" a clase 2
theorem pot3_mult3 (n : Nat) : pot3 (n + 1) % 3 = 0 := by
  unfold pot3; omega

structure Estado where
  k : Nat
  c : Int

-- los mismos once constructores de urracas.lean, sin contadores
inductive Paso : Estado → Estado → Prop where
  | f_par0 (d : Int) (hd : 1 ≤ d) :
      Paso ⟨0, 2 * d⟩ ⟨0, d⟩
  | f_par1 (d : Int) (hd : 1 ≤ d) :
      Paso ⟨0, 2 * d⟩ ⟨0, 3 * d⟩
  | f_impar0 (d : Int) (hd : 0 ≤ d) :
      Paso ⟨0, 2 * d + 1⟩ ⟨1, 3 * d + 2⟩
  | f_impar1 (d : Int) (hd : 0 ≤ d) :
      Paso ⟨0, 2 * d + 1⟩ ⟨1, -(3 * d + 1)⟩
  | n_par0 (k : Nat) (d : Int) :
      Paso ⟨k + 1, 2 * d⟩ ⟨k + 1, d⟩
  | n_par1 (k : Nat) (d m : Int) (hm : pot3 (k + 1) = 2 * m + 1) :
      Paso ⟨k + 1, 2 * d⟩ ⟨k + 1, 3 * d - m⟩
  | n_impar0 (k : Nat) (d : Int) :
      Paso ⟨k + 1, 2 * d + 1⟩ ⟨k + 2, 3 * d + 2⟩
  | n_impar1 (k : Nat) (d m : Int) (hm : pot3 (k + 1) = 2 * m + 1) :
      Paso ⟨k + 2, 2 * d + 1⟩ ⟨k + 1, d - m⟩
  | salida_pos (d : Int) (hd : 1 ≤ d) :
      Paso ⟨1, 2 * d + 1⟩ ⟨0, d⟩
  | salida_neg (d : Int) (hd : d ≤ -1) :
      Paso ⟨1, 2 * d + 1⟩ ⟨0, -d⟩
  | rebote :
      Paso ⟨1, 1⟩ ⟨2, 2⟩

-- el invariante: o estas en la frontera, o tu deuda no es multiplo de 3
def enClase (s : Estado) : Prop := s.k = 0 ∨ s.c % 3 ≠ 0

-- EL LEMA DE LA PUERTA: cada paso conserva el invariante. Los casos
-- con testigo m usan que 3^(k+1) = 2m+1 es multiplo de 3, o sea
-- m ≡ 1 (mod 3): la rama par-bit1 cae en 3d - m ≡ 2 (reseteo) y el
-- descenso impar manda {1, 2} en {2, 1} sin tocar el 0.
theorem paso_puerta {a b : Estado} (h : Paso a b) (ha : enClase a) :
    enClase b := by
  cases h with
  | f_par0 d hd => exact Or.inl rfl
  | f_par1 d hd => exact Or.inl rfl
  | f_impar0 d hd => exact Or.inr (show (3 * d + 2) % 3 ≠ 0 by omega)
  | f_impar1 d hd => exact Or.inr (show (-(3 * d + 1)) % 3 ≠ 0 by omega)
  | n_par0 k d =>
      cases ha with
      | inl h0 => exact absurd h0 (by simp)
      | inr h3 =>
          have h2 : (2 * d) % 3 ≠ 0 := h3
          exact Or.inr (show d % 3 ≠ 0 by omega)
  | n_par1 k d m hm =>
      have h3 := pot3_mult3 k
      rw [hm] at h3
      exact Or.inr (show (3 * d - m) % 3 ≠ 0 by omega)
  | n_impar0 k d => exact Or.inr (show (3 * d + 2) % 3 ≠ 0 by omega)
  | n_impar1 k d m hm =>
      have h3 := pot3_mult3 k
      rw [hm] at h3
      cases ha with
      | inl h0 => exact absurd h0 (by simp)
      | inr hc =>
          have h2 : (2 * d + 1) % 3 ≠ 0 := hc
          exact Or.inr (show (d - m) % 3 ≠ 0 by omega)
  | salida_pos d hd => exact Or.inl rfl
  | salida_neg d hd => exact Or.inl rfl
  | rebote => exact Or.inr (show (2 : Int) % 3 ≠ 0 by decide)

inductive Camino : Estado → Estado → Prop where
  | quieta (s : Estado) : Camino s s
  | anda {a b c : Estado} (cab : Camino a b) (pbc : Paso b c) : Camino a c

theorem camino_puerta {a b : Estado} (h : Camino a b) (ha : enClase a) :
    enClase b := by
  induction h with
  | quieta => exact ha
  | anda cab pbc ih => exact paso_puerta pbc ih

-- EL TEOREMA: desde la frontera, la torre nunca lleva multiplos de 3
theorem cabras (c0 : Int) {s : Estado} (h : Camino ⟨0, c0⟩ s)
    (hk : 1 ≤ s.k) : s.c % 3 ≠ 0 := by
  cases camino_puerta h (Or.inl rfl) with
  | inl h0 => omega
  | inr h3 => exact h3

-- COROLARIO: (k, 0) es inalcanzable desde la frontera, para todo k >= 1
theorem torre_sin_ceros (c0 : Int) {s : Estado} (h : Camino ⟨0, c0⟩ s)
    (hk : 1 ≤ s.k) : s.c ≠ 0 := by
  intro h0
  exact cabras c0 h hk (by rw [h0]; decide)

-- EL CASO CONOCIDO DEL REPO: el camino de ida de liebres.py C1,
-- (0,1) -bit0-> (1,2) -bit0-> (1,1); el teorema dispara y da 1 % 3 ≠ 0
theorem caso_ida : Camino ⟨0, 1⟩ ⟨1, 1⟩ := by
  apply Camino.anda (b := ⟨1, 2⟩)
  · apply Camino.anda (Camino.quieta _)
    show Paso ⟨0, 2 * 0 + 1⟩ ⟨1, 3 * 0 + 2⟩
    exact Paso.f_impar0 0 (by omega)
  · show Paso ⟨0 + 1, 2 * 1⟩ ⟨0 + 1, 1⟩
    exact Paso.n_par0 0 1

theorem caso_ida_clase : (1 : Int) % 3 ≠ 0 :=
  cabras 1 caso_ida (by decide)

-- y las dos clases de la puerta, cerradas por decide (no por #eval):
-- la entrada resetea a 2, y el doblado alterna 2 -> 1 -> 2
theorem puerta_valores :
    (2 : Int) % 3 = 2 ∧ (4 : Int) % 3 = 1 ∧ (8 : Int) % 3 = 2 ∧
    ((-1 : Int)) % 3 = 2 ∧ ((-4 : Int)) % 3 = 2 := by decide

#print axioms paso_puerta
#print axioms camino_puerta
#print axioms cabras
#print axioms torre_sin_ceros
#print axioms caso_ida_clase
