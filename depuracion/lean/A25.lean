/-
  A25: (32m+5, 32m+6) se funden para todo m >= 1   [Wu-Huang 2001]

  MAPA: clasico (par -> n/2, impar -> 3n+1). Tambien se demuestra la
  version con el mapa del atajo (par -> n/2, impar -> (3n+1)/2).

  Resultado principal:
    * fusion_desfase_cero : itera 6 (32m+5) = itera 6 (32m+6)  (= 18m+4)
      -- vale para TODO m >= 0, no solo m >= 1: la fusion como identidad
      -- de iterados no necesita la hipotesis.
    * misma_altura : para m >= 1, itera k (32m+5) = 1 <-> itera k (32m+6) = 1
      -- la lectura fuerte ("misma altura"); AQUI si hace falta m >= 1,
      -- porque con m = 0 el 5 toca el 1 en el paso 5 (6m+1 = 1).
    * fusion_atajo : con el atajo se funden en el paso 5 (ambos = 9m+2).
  Bordes comprobados con decide: m = 1 (37, 38), m = 3125 (100005, 100006,
  el par del repo), y m = 0 (fusiona igual en el paso 6, pero alturas 5 y 8).
-/

set_option maxRecDepth 40000

-- ============ definiciones propias (la trampa: escribir el mapa uno mismo)

def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

def itera : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => itera k (paso n)

def pasoT (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

def iteraT : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => iteraT k (pasoT n)

-- caso concreto contra la definicion: trayectoria del 27 empieza
-- 27 -> 82 -> 41 -> 124 (mapa clasico), y del 6: 6 -> 3 -> 10 -> 5
theorem definicion_correcta :
    paso 27 = 82 ∧ paso 82 = 41 ∧ paso 41 = 124 ∧
    itera 3 6 = 5 ∧ pasoT 27 = 41 := by decide

-- ============ los seis pasos de 32m+5 (clasico)

theorem s5a (m : Nat) : paso (32*m+5) = 96*m+16 := by unfold paso; split <;> omega
theorem s5b (m : Nat) : paso (96*m+16) = 48*m+8 := by unfold paso; split <;> omega
theorem s5c (m : Nat) : paso (48*m+8) = 24*m+4 := by unfold paso; split <;> omega
theorem s5d (m : Nat) : paso (24*m+4) = 12*m+2 := by unfold paso; split <;> omega
theorem s5e (m : Nat) : paso (12*m+2) = 6*m+1 := by unfold paso; split <;> omega
theorem s5f (m : Nat) : paso (6*m+1) = 18*m+4 := by unfold paso; split <;> omega

-- ============ los seis pasos de 32m+6 (clasico)

theorem s6a (m : Nat) : paso (32*m+6) = 16*m+3 := by unfold paso; split <;> omega
theorem s6b (m : Nat) : paso (16*m+3) = 48*m+10 := by unfold paso; split <;> omega
theorem s6c (m : Nat) : paso (48*m+10) = 24*m+5 := by unfold paso; split <;> omega
theorem s6d (m : Nat) : paso (24*m+5) = 72*m+16 := by unfold paso; split <;> omega
theorem s6e (m : Nat) : paso (72*m+16) = 36*m+8 := by unfold paso; split <;> omega
theorem s6f (m : Nat) : paso (36*m+8) = 18*m+4 := by unfold paso; split <;> omega

-- ============ formas cerradas de los iterados (32m+5)

theorem it1_5 (m : Nat) : itera 1 (32*m+5) = 96*m+16 := by
  show paso (32*m+5) = 96*m+16
  rw [s5a]

theorem it2_5 (m : Nat) : itera 2 (32*m+5) = 48*m+8 := by
  show paso (paso (32*m+5)) = 48*m+8
  rw [s5a, s5b]

theorem it3_5 (m : Nat) : itera 3 (32*m+5) = 24*m+4 := by
  show paso (paso (paso (32*m+5))) = 24*m+4
  rw [s5a, s5b, s5c]

theorem it4_5 (m : Nat) : itera 4 (32*m+5) = 12*m+2 := by
  show paso (paso (paso (paso (32*m+5)))) = 12*m+2
  rw [s5a, s5b, s5c, s5d]

theorem it5_5 (m : Nat) : itera 5 (32*m+5) = 6*m+1 := by
  show paso (paso (paso (paso (paso (32*m+5))))) = 6*m+1
  rw [s5a, s5b, s5c, s5d, s5e]

theorem it6_5 (m : Nat) : itera 6 (32*m+5) = 18*m+4 := by
  show paso (paso (paso (paso (paso (paso (32*m+5)))))) = 18*m+4
  rw [s5a, s5b, s5c, s5d, s5e, s5f]

-- ============ formas cerradas de los iterados (32m+6)

theorem it1_6 (m : Nat) : itera 1 (32*m+6) = 16*m+3 := by
  show paso (32*m+6) = 16*m+3
  rw [s6a]

theorem it2_6 (m : Nat) : itera 2 (32*m+6) = 48*m+10 := by
  show paso (paso (32*m+6)) = 48*m+10
  rw [s6a, s6b]

theorem it3_6 (m : Nat) : itera 3 (32*m+6) = 24*m+5 := by
  show paso (paso (paso (32*m+6))) = 24*m+5
  rw [s6a, s6b, s6c]

theorem it4_6 (m : Nat) : itera 4 (32*m+6) = 72*m+16 := by
  show paso (paso (paso (paso (32*m+6)))) = 72*m+16
  rw [s6a, s6b, s6c, s6d]

theorem it5_6 (m : Nat) : itera 5 (32*m+6) = 36*m+8 := by
  show paso (paso (paso (paso (paso (32*m+6))))) = 36*m+8
  rw [s6a, s6b, s6c, s6d, s6e]

theorem it6_6 (m : Nat) : itera 6 (32*m+6) = 18*m+4 := by
  show paso (paso (paso (paso (paso (paso (32*m+6)))))) = 18*m+4
  rw [s6a, s6b, s6c, s6d, s6e, s6f]

-- ============ TEOREMA PRINCIPAL: la fusion, desfase 0, paso 6 contra paso 6
-- (vale para TODO m, incluido m = 0; el enunciado con m >= 1 es un caso)

theorem fusion_desfase_cero (m : Nat) :
    itera 6 (32*m+5) = itera 6 (32*m+6) := by
  rw [it6_5, it6_6]

-- ============ la lectura fuerte: misma altura, y aqui SI hace falta m >= 1

theorem itera_suma (j k : Nat) : ∀ n, itera (j + k) n = itera j (itera k n) := by
  induction k with
  | zero => intro n; rfl
  | succ k ih => intro n; exact ih (paso n)

-- para m >= 1 ninguno de los dos toca el 1 antes del paso 6
theorem antes_5 (m : Nat) (hm : 1 ≤ m) :
    ∀ k, k < 6 → itera k (32*m+5) ≠ 1 := by
  intro k
  cases k with
  | zero => intro _; show 32*m+5 ≠ 1; omega
  | succ a => cases a with
    | zero => intro _; show itera 1 (32*m+5) ≠ 1; rw [it1_5]; omega
    | succ b => cases b with
      | zero => intro _; show itera 2 (32*m+5) ≠ 1; rw [it2_5]; omega
      | succ c => cases c with
        | zero => intro _; show itera 3 (32*m+5) ≠ 1; rw [it3_5]; omega
        | succ d => cases d with
          | zero => intro _; show itera 4 (32*m+5) ≠ 1; rw [it4_5]; omega
          | succ e => cases e with
            | zero => intro _; show itera 5 (32*m+5) ≠ 1; rw [it5_5]; omega
            | succ f => intro h; exact absurd h (by omega)

-- para 32m+6 ni siquiera hace falta m >= 1 (sus seis primeros valores
-- nunca son 1, tampoco en m = 0: 6, 3, 10, 5, 16, 8)
theorem antes_6 (m : Nat) :
    ∀ k, k < 6 → itera k (32*m+6) ≠ 1 := by
  intro k
  cases k with
  | zero => intro _; show 32*m+6 ≠ 1; omega
  | succ a => cases a with
    | zero => intro _; show itera 1 (32*m+6) ≠ 1; rw [it1_6]; omega
    | succ b => cases b with
      | zero => intro _; show itera 2 (32*m+6) ≠ 1; rw [it2_6]; omega
      | succ c => cases c with
        | zero => intro _; show itera 3 (32*m+6) ≠ 1; rw [it3_6]; omega
        | succ d => cases d with
          | zero => intro _; show itera 4 (32*m+6) ≠ 1; rw [it4_6]; omega
          | succ e => cases e with
            | zero => intro _; show itera 5 (32*m+6) ≠ 1; rw [it5_6]; omega
            | succ f => intro h; exact absurd h (by omega)

-- la fusion + no tocar el 1 antes => llegan al 1 exactamente en los mismos
-- pasos: la "misma altura" sin necesitar definir altura (que exigiria
-- haber demostrado Collatz para ser total)
theorem misma_altura (m : Nat) (hm : 1 ≤ m) (k : Nat) :
    itera k (32*m+5) = 1 ↔ itera k (32*m+6) = 1 := by
  by_cases h : k < 6
  · constructor
    · intro h1; exact absurd h1 (antes_5 m hm k h)
    · intro h1; exact absurd h1 (antes_6 m k h)
  · have hk : k = (k - 6) + 6 := by omega
    rw [hk, itera_suma (k-6) 6 (32*m+5), itera_suma (k-6) 6 (32*m+6),
        fusion_desfase_cero m]

-- ============ version con el mapa del ATAJO: se funden en el paso 5

theorem t5a (m : Nat) : pasoT (32*m+5) = 48*m+8 := by unfold pasoT; split <;> omega
theorem t5b (m : Nat) : pasoT (48*m+8) = 24*m+4 := by unfold pasoT; split <;> omega
theorem t5c (m : Nat) : pasoT (24*m+4) = 12*m+2 := by unfold pasoT; split <;> omega
theorem t5d (m : Nat) : pasoT (12*m+2) = 6*m+1 := by unfold pasoT; split <;> omega
theorem t5e (m : Nat) : pasoT (6*m+1) = 9*m+2 := by unfold pasoT; split <;> omega

theorem t6a (m : Nat) : pasoT (32*m+6) = 16*m+3 := by unfold pasoT; split <;> omega
theorem t6b (m : Nat) : pasoT (16*m+3) = 24*m+5 := by unfold pasoT; split <;> omega
theorem t6c (m : Nat) : pasoT (24*m+5) = 36*m+8 := by unfold pasoT; split <;> omega
theorem t6d (m : Nat) : pasoT (36*m+8) = 18*m+4 := by unfold pasoT; split <;> omega
theorem t6e (m : Nat) : pasoT (18*m+4) = 9*m+2 := by unfold pasoT; split <;> omega

theorem itT5_5 (m : Nat) : iteraT 5 (32*m+5) = 9*m+2 := by
  show pasoT (pasoT (pasoT (pasoT (pasoT (32*m+5))))) = 9*m+2
  rw [t5a, t5b, t5c, t5d, t5e]

theorem itT5_6 (m : Nat) : iteraT 5 (32*m+6) = 9*m+2 := by
  show pasoT (pasoT (pasoT (pasoT (pasoT (32*m+6))))) = 9*m+2
  rw [t6a, t6b, t6c, t6d, t6e]

theorem fusion_atajo (m : Nat) :
    iteraT 5 (32*m+5) = iteraT 5 (32*m+6) := by
  rw [itT5_5, itT5_6]

-- ============ casos conocidos, por el NUCLEO (decide, no #eval)

-- m = 1: el par (37, 38); ambos llegan a 22 = 18*1+4 en el paso 6
theorem caso_m1 : itera 6 37 = 22 ∧ itera 6 38 = 22 := by decide

-- m = 3125: el par del repo (100005, 100006); ambos a 56254 = 18*3125+4
theorem caso_repo_m3125 :
    itera 6 100005 = 56254 ∧ itera 6 100006 = 56254 := by decide

-- BORDE m = 0: la fusion como iteracion TAMBIEN se cumple (ambos dan 4
-- en el paso 6)...
theorem borde_m0_fusiona : itera 6 5 = 4 ∧ itera 6 6 = 4 := by decide

-- ...pero las ALTURAS difieren: el 5 toca el 1 en el paso 5 (justo antes
-- de la fusion) y el 6 en el paso 8. Exactamente el "altura(5)=5,
-- altura(6)=8" de la ficha. Por eso el enunciado fuerte pide m >= 1.
theorem borde_m0_alturas :
    (itera 5 5 = 1 ∧ ∀ j, j < 5 → itera j 5 ≠ 1) ∧
    (itera 8 6 = 1 ∧ ∀ j, j < 8 → itera j 6 ≠ 1) := by decide

-- y el testigo de que misma_altura FALLA en m = 0, en el paso k = 5:
theorem borde_m0_contraejemplo : itera 5 5 = 1 ∧ itera 5 6 ≠ 1 := by decide

-- ============ control de axiomas

#print axioms fusion_desfase_cero
#print axioms misma_altura
#print axioms fusion_atajo
#print axioms caso_m1
#print axioms caso_repo_m3125
#print axioms borde_m0_alturas
#print axioms borde_m0_contraejemplo
