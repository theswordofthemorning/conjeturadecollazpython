/-
  A31 — "los evitados de la malla 2n mod 27 son exactamente los multiplos de 3,
         y predicen que rayos del arbol son mudos"

  MAPA: el arbol inverso es el del mapa CLASICO (n/2 si par, 3n+1 si impar).
  Un "rayo" es la orbita de duplicacion {2^k * v : k}. Un rayo "brota" en k
  cuando el valor 2^k*v tiene segundo padre impar, es decir 2^k*v = 4 (mod 6).
  Un rayo es MUDO cuando no brota nunca.
  La "malla 2n mod 27" es el aro de duplicacion mod 27 arrancando en 1:
  los residuos visitados son {2^i mod 27 : i < 18} (orden de 2 mod 27 = 18);
  los EVITADOS son los que no se visitan nunca.

  Se demuestra:
   (1) evitado(r)  <->  3 | r          (los 27 residuos, por el nucleo, decide)
   (2) rayo v mudo <->  3 | v          (para TODO v, sin cota)
   (3) el puente:  rayo v mudo <-> v mod 27 es un residuo evitado de la malla
   (4) que "brotar" es de verdad tener padre impar en el mapa clasico,
       escrito contra una definicion propia de `paso`, con caso concreto.
-/
set_option maxRecDepth 40000

-- El mapa CLASICO de Collatz, escrito aqui mismo (no importado de nada).
def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

-- Caso conocido del mapa, comprobado por el NUCLEO (no #eval):
-- 5 -> 16 -> 8 -> 4 -> 2 -> 1
theorem caso_trayectoria_5 :
    paso 5 = 16 ∧ paso 16 = 8 ∧ paso 8 = 4 ∧ paso 4 = 2 ∧ paso 2 = 1 := by
  decide

-- "Brotar" es aritmetica real del arbol: si w = 4 (mod 6), entonces
-- (w-1)/3 es impar y paso((w-1)/3) = w  (el segundo padre existe).
theorem brote_da_padre_impar (w : Nat) (h : w % 6 = 4) :
    ((w - 1) / 3) % 2 = 1 ∧ paso ((w - 1) / 3) = w := by
  constructor
  · omega
  · unfold paso
    split
    · omega
    · omega

-- Y un multiplo de 3 no tiene NINGUN padre impar bajo el mapa clasico.
theorem multiplo3_sin_padre_impar (w n : Nat) (h3 : w % 3 = 0) (hn : n % 2 = 1) :
    paso n ≠ w := by
  unfold paso
  split
  · omega
  · omega

-- (2) EL TEOREMA DEL RAYO, para todo v (incluye v = 0 y v par):
--     el rayo {2^k v} es mudo  <->  3 divide a v.
theorem rayo_mudo_iff_multiplo3 (v : Nat) :
    (∀ k, (2 ^ k * v) % 6 ≠ 4) ↔ v % 3 = 0 := by
  constructor
  · -- si nunca brota, en particular no brota en k = 1 ni en k = 2,
    -- y eso ya obliga a 3 | v
    intro h
    have h1 := h 1
    have h2 := h 2
    rw [show (2:Nat)^1 = 2 from rfl] at h1
    rw [show (2:Nat)^2 = 4 from rfl] at h2
    by_cases hc : v % 3 = 0
    · exact hc
    · exfalso
      by_cases hc1 : v % 3 = 1
      · exact h2 (by omega)
      · exact h1 (by omega)
  · -- si 3 | v, todo 2^k v es multiplo de 3, y 4 no lo es mod 6
    intro hv k hc
    have h3 : (2 ^ k * v) % 3 = 0 := by
      rw [Nat.mul_mod, hv]
      simp
    omega

-- (1) LA MALLA: residuos visitados por el aro de 2 mod 27 (18 potencias);
--     los evitados son EXACTAMENTE los multiplos de 3. Los 27 casos, decide.
theorem malla_evitados :
    ∀ r, r < 27 → ((∃ i, i < 18 ∧ 2 ^ i % 27 = r) ↔ ¬ (r % 3 = 0)) := by
  decide

-- El aro cierra: 2^18 = 1 (mod 27), o sea que i < 18 recorre el aro entero.
theorem aro_cierra : 2 ^ 18 % 27 = 1 := by decide

-- (3) EL PUENTE (la "prediccion"): un rayo es mudo exactamente cuando su
--     semilla cae, mod 27, en un residuo EVITADO por la malla.
theorem malla_predice_mudos (v : Nat) :
    (∀ k, (2 ^ k * v) % 6 ≠ 4) ↔ ¬ (∃ i, i < 18 ∧ 2 ^ i % 27 = v % 27) := by
  have hb := malla_evitados (v % 27) (by omega)
  rw [rayo_mudo_iff_multiplo3]
  constructor
  · intro h hex
    have hno := hb.mp hex
    omega
  · intro h
    cases Nat.decEq (v % 3) 0 with
    | isTrue ht => exact ht
    | isFalse hf => exact absurd (hb.mpr (by omega)) h

-- Casos concretos por el nucleo:
-- el rayo del 3 no brota en ningun k < 20 (y por el teorema, en ninguno)
theorem caso_rayo_3_mudo : ∀ k, k < 20 → (2 ^ k * 3) % 6 ≠ 4 := by decide
-- el rayo del 5 brota ya en k = 1 (2*5 = 10 = 4 mod 6; padre impar 3)
theorem caso_rayo_5_brota : (2 ^ 1 * 5) % 6 = 4 ∧ paso 3 = 10 := by decide
-- y el conteo de la nota de la base: de los 200 primeros rayos impares
-- (v = 1, 3, ..., 399), los mudos predichos son exactamente 67
theorem caso_conteo_67 :
    (((List.range 200).map (fun j => 2 * j + 1)).filter
      (fun v => v % 3 == 0)).length = 67 := by decide

#print axioms caso_trayectoria_5
#print axioms brote_da_padre_impar
#print axioms multiplo3_sin_padre_impar
#print axioms rayo_mudo_iff_multiplo3
#print axioms malla_evitados
#print axioms aro_cierra
#print axioms malla_predice_mudos
#print axioms caso_rayo_3_mudo
#print axioms caso_rayo_5_brota
#print axioms caso_conteo_67
