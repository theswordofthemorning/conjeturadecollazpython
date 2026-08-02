/-
A63 — "el unico ciclo positivo, escrito con la identidad del repo, es 2^2 = 3^1 + 1"

MAPA: CLASICO (n/2 si par, 3n+1 si impar). El enunciado cuenta A=1 aplicaciones
de 3n+1 y B=2 divisiones en el ciclo 1 -> 4 -> 2 -> 1, que es el conteo del mapa
clasico.

QUE SE DEMUESTRA AQUI (todo por el nucleo, sin Mathlib):
  1. El ciclo trivial existe: 1 -> 4 -> 2 -> 1, y sus tres miembros vuelven a si
     mismos en 3 pasos.
  2. La identidad del repo (2^B * v_k = 3^A * v_0 + C, con C -> 3C + 2^B en los
     pasos impares) se demuestra COMO INVARIANTE GENERAL, por induccion, para
     todo n0 y todo k.
  3. Evaluada en el ciclo: (A,B,C) = (1,2,1), o sea 2^2 = 3^1 + 1: 4 = 3 + 1.
     Y en 2 y 3 vueltas: 2^4 = 3^2 + 7 y 2^6 = 3^3 + 37 (los "95 candidatos"
     de la ficha son estas orbitas).
  4. UNICIDAD ACOTADA (lo unico demostrable de "el unico"): ningun n con
     1 <= n <= 200 que vuelva a si mismo en <= 150 pasos esta fuera de {1,2,4}.
     Y ademas todo 1 <= n <= 200 alcanza el 1 en <= 250 pasos.

QUE NO SE PUEDE DEMOSTRAR: la unicidad GLOBAL ("el unico ciclo positivo") es
la mitad de ciclos de la conjetura de Collatz, abierta. El estado "demostrado"
de la base solo puede referirse a la identidad del ciclo y a los 95 candidatos
finitos, no al cuantificador universal.

Nota de borde: en Nat, paso 0 = 0 es un punto fijo (un "ciclo" de largo 1),
por eso todos los teoremas de unicidad exigen 1 <= n. "Positivo" lo excluye.
-/

set_option maxRecDepth 40000

-- ===== el objeto: el mapa clasico, escrito aqui mismo =====

def paso (n : Nat) : Nat := if n % 2 == 0 then n / 2 else 3 * n + 1

def itera : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => itera k (paso n)

-- guardia contra la trampa del objeto: casos concretos del mapa
theorem mapa_es_collatz :
    paso 6 = 3 ∧ paso 3 = 10 ∧ paso 10 = 5 ∧ paso 5 = 16 ∧
    paso 16 = 8 ∧ paso 7 = 22 ∧ paso 1 = 4 := by decide

-- ===== (1) el ciclo trivial =====

theorem ciclo_trivial : paso 1 = 4 ∧ paso 4 = 2 ∧ paso 2 = 1 := by decide

theorem miembros_ciclan : itera 3 1 = 1 ∧ itera 3 2 = 2 ∧ itera 3 4 = 4 := by
  decide

-- ===== (2) la identidad del repo, como invariante demostrado =====

structure Est where
  v : Nat  -- valor actual
  a : Nat  -- cuantas veces se aplico 3n+1
  b : Nat  -- cuantas divisiones
  c : Nat  -- la C de la identidad
  deriving DecidableEq

def pasoE (s : Est) : Est :=
  if s.v % 2 == 0 then ⟨s.v / 2, s.a, s.b + 1, s.c⟩
  else ⟨3 * s.v + 1, s.a + 1, s.b, 3 * s.c + 2 ^ s.b⟩

def trayE : Nat → Nat → Est
  | 0, n0 => ⟨n0, 0, 0, 0⟩
  | k + 1, n0 => pasoE (trayE k n0)

-- coherencia entre las dos definiciones: el valor de trayE es itera
theorem trayE_coincide_itera :
    (trayE 7 27).v = itera 7 27 ∧ (trayE 5 6).v = itera 5 6 := by decide

-- un paso conserva la identidad
theorem paso_conserva (n0 : Nat) (s : Est)
    (h : 2 ^ s.b * s.v = 3 ^ s.a * n0 + s.c) :
    2 ^ (pasoE s).b * (pasoE s).v = 3 ^ (pasoE s).a * n0 + (pasoE s).c := by
  cases s with
  | mk v a b c =>
    unfold pasoE
    split
    · -- rama par: v/2, B+1, C igual
      rename_i hcond
      simp at hcond h ⊢
      have h2 : 2 * (v / 2) = v := by omega
      calc 2 ^ (b + 1) * (v / 2)
          = 2 ^ b * (2 * (v / 2)) := by rw [Nat.pow_succ, Nat.mul_assoc]
        _ = 2 ^ b * v := by rw [h2]
        _ = 3 ^ a * n0 + c := h
    · -- rama impar: 3v+1, A+1, C -> 3C + 2^B
      simp at h ⊢
      calc 2 ^ b * (3 * v + 1)
          = 2 ^ b * (3 * v) + 2 ^ b := by rw [Nat.mul_add, Nat.mul_one]
        _ = 3 * (2 ^ b * v) + 2 ^ b := by rw [Nat.mul_left_comm]
        _ = 3 * (3 ^ a * n0 + c) + 2 ^ b := by rw [h]
        _ = 3 ^ (a + 1) * n0 + (3 * c + 2 ^ b) := by
            rw [Nat.pow_succ, Nat.mul_comm (3 ^ a) 3, Nat.mul_assoc]
            omega

-- LA IDENTIDAD, para todo n0 y todo k: 2^B * v_k = 3^A * n0 + C
theorem identidad_general (n0 : Nat) : ∀ k,
    2 ^ (trayE k n0).b * (trayE k n0).v
      = 3 ^ (trayE k n0).a * n0 + (trayE k n0).c := by
  intro k
  induction k with
  | zero => simp [trayE]
  | succ k ih =>
    show 2 ^ (pasoE (trayE k n0)).b * (pasoE (trayE k n0)).v
        = 3 ^ (pasoE (trayE k n0)).a * n0 + (pasoE (trayE k n0)).c
    exact paso_conserva n0 (trayE k n0) ih

-- ===== (3) el ciclo escrito con la identidad: A=1, B=2, C=1 =====

theorem ciclo_con_identidad : trayE 3 1 = ⟨1, 1, 2, 1⟩ := by decide

theorem cuatro_es_tres_mas_uno : 2 ^ 2 = 3 ^ 1 + 1 := by decide

-- dos y tres vueltas (las orbitas de los "95 candidatos" de la ficha)
theorem dos_vueltas : trayE 6 1 = ⟨1, 2, 4, 7⟩ ∧ 2 ^ 4 = 3 ^ 2 + 7 := by decide
theorem tres_vueltas : trayE 9 1 = ⟨1, 3, 6, 37⟩ ∧ 2 ^ 6 = 3 ^ 3 + 37 := by
  decide

-- ===== (4) unicidad ACOTADA, que es lo unico demostrable de "el unico" =====

-- ¿vuelve m a chocar con n en <= fuel pasos? (arrancando un paso por delante)
def vuelveAux : Nat → Nat → Nat → Bool
  | 0, _, _ => false
  | fuel + 1, m, n => paso m == n || vuelveAux fuel (paso m) n

-- todo n en 1..200 que vuelve a si mismo en <= 150 pasos es 1, 2 o 4
theorem unico_ciclo_hasta_200 :
    ∀ n, n < 201 → 1 ≤ n → vuelveAux 150 n n = true →
      n = 1 ∨ n = 2 ∨ n = 4 := by decide

-- ¿llega n al 1 en <= fuel pasos?
def llega1 : Nat → Nat → Bool
  | 0, n => n == 1
  | fuel + 1, n => n == 1 || llega1 fuel (paso n)

-- y ademas todo n en 1..200 baja al 1 (luego ningun ciclo nuevo pasa por ahi)
theorem todos_bajan_hasta_200 :
    ∀ n, n < 201 → 1 ≤ n → llega1 250 n = true := by decide

-- el borde: 0 es punto fijo del mapa en Nat, y por eso se exige 1 <= n
theorem cero_es_punto_fijo : paso 0 = 0 := by decide

-- ===== controles finales =====

#print axioms mapa_es_collatz
#print axioms ciclo_trivial
#print axioms miembros_ciclan
#print axioms paso_conserva
#print axioms identidad_general
#print axioms ciclo_con_identidad
#print axioms cuatro_es_tres_mas_uno
#print axioms dos_vueltas
#print axioms tres_vueltas
#print axioms unico_ciclo_hasta_200
#print axioms todos_bajan_hasta_200
#print axioms cero_es_punto_fijo
