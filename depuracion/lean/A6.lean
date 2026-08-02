/-
  A6 — LA REGLA DE LOS DOS PADRES, DEMOSTRADA.

  Enunciado (ficha A6): "un numero tiene dos padres en el arbol si y solo si
  deja resto 4 al dividirlo entre 6; el segundo padre es (v-1)/3".

  MAPA: el CLASICO (n/2 si par, 3n+1 si impar). El arbol inverso del que habla
  la regla estandar de la literatura es el de este mapa. La definicion T de
  abajo la escribo yo mismo y la compruebo contra una trayectoria conocida
  (6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1) con `decide`, por el nucleo.

  "padre de v" = un n >= 1 con T n = v.
  "dos padres" = existen dos padres DISTINTOS; y ademas se demuestra que no
  puede haber un tercero (padres_clasificados: todo padre es 2v o (v-1)/3).

  Sin Mathlib. Solo nucleo.
-/

set_option maxRecDepth 40000

-- El mapa clasico de Collatz, escrito aqui mismo.
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

-- n es padre de v en el arbol inverso (ambito v >= 1, padres n >= 1).
def esPadre (n v : Nat) : Prop := 1 ≤ n ∧ T n = v

-- ============================================================
-- COMPROBACION DEL OBJETO: la definicion T es Collatz de verdad.
-- Trayectoria conocida del 6, ambas paridades ejercitadas, por el nucleo.
-- ============================================================
theorem mapa_es_collatz :
    T 6 = 3 ∧ T 3 = 10 ∧ T 10 = 5 ∧ T 5 = 16 ∧ T 16 = 8 ∧
    T 8 = 4 ∧ T 4 = 2 ∧ T 2 = 1 := by decide

-- Caso conocido de la propia ficha: el 4 tiene dos padres, 8 y 1
-- (el 1 es (4-1)/3; en el dibujo borrado se excluia a mano, aritmeticamente cuenta).
theorem caso_4 : T 8 = 4 ∧ T 1 = 4 ∧ 4 % 6 = 4 ∧ (4 - 1) / 3 = 1 := by decide

-- Otro caso concreto: 16 = 6*2+4 tiene padres 32 y 5.
theorem caso_16 : T 32 = 16 ∧ T 5 = 16 ∧ 16 % 6 = 4 ∧ (16 - 1) / 3 = 5 := by decide

-- Caso negativo concreto: 8 % 6 = 2, y su unico padre por debajo de 1000 es 16.
theorem caso_8_un_solo_padre :
    (∀ n, n < 1000 → T n = 8 → n = 16) ∧ 8 % 6 = 2 := by decide

-- ============================================================
-- LA CLASIFICACION: todo padre es 2v o el impar (v-1)/3.
-- (Esto es lo que impide que haya un TERCER padre.)
-- ============================================================
theorem padres_clasificados (n v : Nat) (h : esPadre n v) :
    n = 2 * v ∨ (n % 2 = 1 ∧ 3 * n + 1 = v) := by
  cases h with
  | intro h1 h2 =>
    unfold T at h2
    by_cases hp : n % 2 = 0
    · rw [if_pos hp] at h2
      left
      omega
    · rw [if_neg hp] at h2
      right
      omega

-- El primer padre existe siempre (v >= 1): es 2v.
theorem padre_par (v : Nat) (hv : 1 ≤ v) : esPadre (2 * v) v := by
  unfold esPadre T
  have h2 : (2 * v) % 2 = 0 := by omega
  rw [if_pos h2]
  exact ⟨by omega, by omega⟩

-- EL SEGUNDO PADRE: si v % 6 = 4, entonces (v-1)/3 es padre de v.
theorem segundo_padre (v : Nat) (h : v % 6 = 4) : esPadre ((v - 1) / 3) v := by
  unfold esPadre T
  have h1 : (v - 1) / 3 % 2 = 1 := by omega
  rw [if_neg (by omega : ¬ (v - 1) / 3 % 2 = 0)]
  exact ⟨by omega, by omega⟩

-- ============================================================
-- EL TEOREMA: dos padres distintos  <->  v % 6 = 4.
-- Vale para todo v : Nat (incluido v = 0, donde ambos lados son falsos);
-- el ambito declarado de la ficha, v >= 1, queda cubierto de sobra.
-- ============================================================
theorem dos_padres_iff (v : Nat) :
    (∃ a b, esPadre a v ∧ esPadre b v ∧ a ≠ b) ↔ v % 6 = 4 := by
  constructor
  · intro h
    match h with
    | ⟨a, b, ha, hb, hab⟩ =>
      have ca := padres_clasificados a v ha
      have cb := padres_clasificados b v hb
      cases ca with
      | inl h1 =>
        cases cb with
        | inl h2 => omega     -- a = 2v = b contradice a ≠ b
        | inr h2 => omega     -- b impar con 3b+1 = v fuerza v % 6 = 4
      | inr h1 =>
        cases cb with
        | inl h2 => omega     -- simetrico
        | inr h2 => omega     -- 3a+1 = v = 3b+1 fuerza a = b, contradiccion
  · intro h
    exact ⟨2 * v, (v - 1) / 3, padre_par v (by omega), segundo_padre v h,
           by omega⟩          -- 2v ≠ (v-1)/3 porque (v-1)/3 < v ≤ 2v

-- Y NO HAY TERCER PADRE: si v % 6 = 4, todo padre es exactamente 2v o (v-1)/3.
theorem solo_esos_dos (n v : Nat) (h : v % 6 = 4) (hp : esPadre n v) :
    n = 2 * v ∨ n = (v - 1) / 3 := by
  cases padres_clasificados n v hp with
  | inl h1 => exact Or.inl h1
  | inr h1 =>
    right
    omega

-- ============================================================
-- BARRIDO EXHAUSTIVO POR EL NUCLEO (no #eval): el iff, comprobado
-- para todo v < 30 con padres acotados por 70 (los padres de v < 30
-- son 2v <= 58 y (v-1)/3 < 30, ambos < 70).
-- ============================================================
theorem barrido_chico :
    ∀ v, v < 30 →
      ((∃ a, a < 70 ∧ 1 ≤ a ∧ T a = v ∧
        ∃ b, b < 70 ∧ 1 ≤ b ∧ T b = v ∧ a ≠ b) ↔ v % 6 = 4) := by decide

-- ============================================================
-- CONTROL FINAL
-- ============================================================
#print axioms mapa_es_collatz
#print axioms caso_4
#print axioms caso_16
#print axioms caso_8_un_solo_padre
#print axioms padres_clasificados
#print axioms padre_par
#print axioms segundo_padre
#print axioms dos_padres_iff
#print axioms solo_esos_dos
#print axioms barrido_chico
