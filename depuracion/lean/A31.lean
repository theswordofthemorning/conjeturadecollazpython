/-
  A31 - AGENTE 1 (LEAN) del trio de verificacion.

  ENUNCIADO LITERAL: "los evitados de la malla 2n mod 27 son exactamente los
  multiplos de 3, y predicen que rayos del arbol son mudos"

  FORMALIZACION (mapa CLASICO: n/2 en pares, 3n+1 en impares; el arbol
  inverso se construye doblando y la rama impar invierte u -> 3u+1):

    * la malla: iterar n -> (2n) % 27 desde la semilla 1; itera k = 2^k mod 27.
      "Evitado" = residuo r < 27 que la orbita NO pisa para NINGUN k.
    * el rayo de v son los numeros 2^k * v. "Brota" en el nivel k si existe
      un padre impar u con 3u+1 = 2^k * v. "Mudo" = no brota en ningun nivel.
    * la prediccion: v % 27 es evitado por la malla  <->  el rayo de v es mudo.

  Sin Mathlib: nucleo solo.
-/

set_option maxRecDepth 40000

/-- un paso de la malla: doblar modulo 27 -/
def pasoMalla (n : Nat) : Nat := (2 * n) % 27

/-- la orbita de la malla desde 1: itera k = 2^k mod 27 -/
def itera : Nat → Nat
  | 0 => 1
  | k + 1 => pasoMalla (itera k)

theorem itera_succ (k : Nat) : itera (k + 1) = pasoMalla (itera k) := rfl

/-- los 18 valores de la orbita -/
def orbita : List Nat := (List.range 18).map itera

/-- CASO CONOCIDO (decide, lo revisa el nucleo): la orbita explicita -/
theorem orbita_explicita :
    orbita = [1, 2, 4, 8, 16, 5, 10, 20, 13, 26, 25, 23, 19, 11, 22, 17, 7, 14] := by
  decide

/-- CASO CONOCIDO (decide): los evitados de 0..26 son exactamente los 9
    multiplos de 3 -/
theorem evitados_lista :
    (List.range 27).filter (fun r => !(orbita.contains r)) =
      [0, 3, 6, 9, 12, 15, 18, 21, 24] := by
  decide

/-- la orbita es periodica de periodo 18 (el orden de 2 modulo 27) -/
theorem periodo : ∀ k, itera (k + 18) = itera k := by
  intro k
  induction k with
  | zero => decide
  | succ n ih =>
    have h : n + 1 + 18 = (n + 18) + 1 := by omega
    rw [h, itera_succ, itera_succ, ih]

/-- un paso de la malla conserva "no multiplo de 3" -/
theorem paso_mod3 (x : Nat) (hx : x % 3 ≠ 0) : (pasoMalla x) % 3 ≠ 0 := by
  unfold pasoMalla
  omega

/-- la orbita nunca pisa un multiplo de 3 -/
theorem itera_mod3 : ∀ k, (itera k) % 3 ≠ 0 := by
  intro k
  induction k with
  | zero => decide
  | succ n ih =>
    rw [itera_succ]
    exact paso_mod3 _ ih

/-- si r < 27 no es multiplo de 3, la orbita lo pisa antes del paso 18
    (comprobacion finita: 27 x 18 casos, revisados por el nucleo) -/
theorem existencia_acotada :
    ∀ r, r < 27 → r % 3 ≠ 0 → ¬(∀ k, k < 18 → itera k ≠ r) := by
  decide

/-- TEOREMA 1: los evitados de la malla son EXACTAMENTE los multiplos de 3.
    (cuantificador sobre TODO k, no solo k < 18) -/
theorem malla_evita_exactamente_multiplos_de_3 :
    ∀ r, r < 27 → ((∀ k, itera k ≠ r) ↔ r % 3 = 0) := by
  intro r hr
  constructor
  · intro h
    by_cases h3 : r % 3 = 0
    · exact h3
    · exact absurd (fun k _ => h k) (existencia_acotada r hr h3)
  · intro h3 k hk
    exact itera_mod3 k (by rw [hk]; exact h3)

/-- brote del rayo de v en el nivel k: un padre IMPAR u con 3u+1 = 2^k * v -/
def Brota (v k : Nat) : Prop := ∃ u, u % 2 = 1 ∧ 3 * u + 1 = 2 ^ k * v

/-- forma cerrada del brote: 2^k * v = 4 (mod 6) -/
theorem brota_syss (v k : Nat) : Brota v k ↔ (2 ^ k * v) % 6 = 4 := by
  unfold Brota
  constructor
  · intro h
    cases h with
    | intro u hu => omega
  · intro h
    exact ⟨(2 ^ k * v - 1) / 3, by omega, by omega⟩

/-- TEOREMA 2: el rayo de v es mudo si y solo si v es multiplo de 3 -/
theorem rayo_mudo_syss_multiplo_de_3 (v : Nat) :
    (∀ k, ¬ Brota v k) ↔ v % 3 = 0 := by
  constructor
  · intro h
    by_cases h3 : v % 3 = 0
    · exact h3
    · exfalso
      by_cases h1 : v % 3 = 1
      · -- v = 1 mod 3: brota en k = 2 con u = (4v-1)/3
        apply h 2
        unfold Brota
        have h4 : (2 : Nat) ^ 2 = 4 := by decide
        rw [h4]
        exact ⟨(4 * v - 1) / 3, by omega, by omega⟩
      · -- v = 2 mod 3: brota en k = 1 con u = (2v-1)/3
        have h2 : v % 3 = 2 := by omega
        apply h 1
        unfold Brota
        have h5 : (2 : Nat) ^ 1 = 2 := by decide
        rw [h5]
        exact ⟨(2 * v - 1) / 3, by omega, by omega⟩
  · -- 3 | v: 2^k * v = 0 (mod 3), y 3u+1 = 1 (mod 3). Nunca brota.
    intro h3 k hb
    cases hb with
    | intro u hu =>
      have hmod : (2 ^ k * v) % 3 = 0 := by
        rw [Nat.mul_mod, h3, Nat.mul_zero]
      omega

/-- TEOREMA 3 (la prediccion): v % 27 es evitado por la malla
    si y solo si el rayo de v es mudo -/
theorem malla_predice_rayos_mudos (v : Nat) :
    (∀ k, itera k ≠ v % 27) ↔ (∀ k, ¬ Brota v k) := by
  have h1 : (∀ k, itera k ≠ v % 27) ↔ (v % 27) % 3 = 0 :=
    malla_evita_exactamente_multiplos_de_3 (v % 27) (Nat.mod_lt v (by decide))
  have h2 : (v % 27) % 3 = v % 3 := by omega
  have h3 : (∀ k, ¬ Brota v k) ↔ v % 3 = 0 := rayo_mudo_syss_multiplo_de_3 v
  rw [h1, h2, h3]

/- ------------ casos concretos y bordes, revisados por el nucleo ------------ -/

/-- el rayo de 3 (multiplo de 3) no brota en sus 12 primeros niveles (decide) -/
theorem rayo_3_mudo_12 : ∀ k, k < 12 → (2 ^ k * 3) % 6 ≠ 4 := by decide

/-- y por el TEOREMA 2, mudo en TODOS los niveles -/
theorem rayo_3_mudo_siempre : ∀ k, ¬ Brota 3 k :=
  (rayo_mudo_syss_multiplo_de_3 3).mpr (by decide)

/-- el rayo de 5 brota en el nivel 1: testigo u = 3 (3*3+1 = 10 = 2*5) -/
theorem rayo_5_brota : Brota 5 1 := ⟨3, by decide, by decide⟩

/-- y 5 esta EN la orbita de la malla (paso 5), como exige la prediccion -/
theorem cinco_en_orbita : itera 5 = 5 := by decide

/-- borde v = 0: mudo, y 0 es multiplo de 3 -- coherente, sin excepcion -/
theorem borde_cero : ∀ k, ¬ Brota 0 k :=
  (rayo_mudo_syss_multiplo_de_3 0).mpr (by decide)

/-- borde v = 1: brota en k = 2 con u = 1 (3*1+1 = 4 = 2^2). El tronco. -/
theorem borde_uno : Brota 1 2 := ⟨1, by decide, by decide⟩

/-- borde r = 0: evitado (es multiplo de 3) -/
theorem borde_r0 : ∀ k, itera k ≠ 0 :=
  (malla_evita_exactamente_multiplos_de_3 0 (by decide)).mpr (by decide)

#print axioms malla_evita_exactamente_multiplos_de_3
#print axioms rayo_mudo_syss_multiplo_de_3
#print axioms malla_predice_rayos_mudos
#print axioms brota_syss
#print axioms periodo
#print axioms evitados_lista
#print axioms orbita_explicita
#print axioms rayo_3_mudo_siempre
#print axioms rayo_5_brota
#print axioms borde_cero
#print axioms borde_uno
#print axioms borde_r0
