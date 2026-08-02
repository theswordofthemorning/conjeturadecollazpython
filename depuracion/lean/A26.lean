/-
  A26 — G2 de Garner CON sus dos hipotesis, en el MAPA CLASICO
  (n par -> n/2 ; n impar -> 3n+1).

  ENUNCIADO: si las trayectorias de n1 y n2 se funden en el mismo indice t
  gastando los MISMOS pasos pares y los MISMOS impares, entonces
  2^r*k + n1 y 2^r*k + n2 se funden (en el mismo indice t) para todo k,
  siempre que r sea ESTRICTAMENTE MAYOR que el numero de pasos pares del tramo.

  Nucleo de Lean 4, sin Mathlib.
-/

set_option maxRecDepth 40000

/-- El mapa CLASICO de Collatz, escrito aqui mismo (no importado de nada). -/
def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- t pasos del mapa clasico. -/
def itera : Nat → Nat → Nat
  | 0,     n => n
  | t + 1, n => itera t (paso n)

/-- Cuantos pasos PARES (divisiones) gasta el tramo de t pasos que arranca en n. -/
def pares : Nat → Nat → Nat
  | 0,     _ => 0
  | t + 1, n => (if n % 2 = 0 then 1 else 0) + pares t (paso n)

/-- Cuantos pasos IMPARES (3n+1) gasta el tramo de t pasos que arranca en n. -/
def impares : Nat → Nat → Nat
  | 0,     _ => 0
  | t + 1, n => (if n % 2 = 0 then 0 else 1) + impares t (paso n)

/- ── LA TRAMPA: comprobar que `paso`/`itera` son Collatz de verdad,
     con casos concretos decididos por el NUCLEO (by decide, no #eval). ── -/

theorem control_mapa :
    paso 6 = 3 ∧ paso 3 = 10 ∧ paso 10 = 5 ∧ paso 16 = 8 ∧ paso 1 = 4 ∧
    itera 8 6 = 1 ∧ itera 3 4 = 4 ∧ itera 1 2 = 1 := by decide

/-- Auxiliar AC: a*(b*c) = b*(a*c). -/
theorem mul_lc (a b c : Nat) : a * (b * c) = b * (a * c) := by
  rw [← Nat.mul_assoc, Nat.mul_comm a b, Nat.mul_assoc]

/-- Auxiliar: para r >= 1, 2^(r-1) * 2 = 2^r. -/
theorem pow_pred {r : Nat} (h : 1 ≤ r) : (2:Nat) ^ (r - 1) * 2 = 2 ^ r := by
  cases r with
  | zero => exact absurd h (by decide)
  | succ m =>
      rw [Nat.succ_sub_one]
      exact (Nat.pow_succ 2 m).symm

/-- EL LEMA DEL DESPLAZAMIENTO: si r es MAYOR que los pares gastados en t pasos,
    entonces sumar 2^r*k desplaza la trayectoria entera de forma afin:
      itera t (2^r*k + n) = 2^(r - pares) * 3^(impares) * k + itera t n.
    La hipotesis `pares t n < r` es exactamente el "r mayor que los pares"
    del enunciado: garantiza que el termino 2^(r - e_j)*3^(a_j)*k sigue siendo
    PAR en cada paso intermedio, y por eso la paridad de la trayectoria
    desplazada copia la de la original. -/
theorem desplaza (t : Nat) : ∀ (n r k : Nat), pares t n < r →
    itera t (2 ^ r * k + n)
      = 2 ^ (r - pares t n) * 3 ^ (impares t n) * k + itera t n := by
  induction t with
  | zero =>
      intro n r k _
      simp [itera, pares, impares]
  | succ t ih =>
      intro n r k h
      by_cases hp : n % 2 = 0
      · -- paso PAR: n -> n/2
        have hpaso : paso n = n / 2 := by
          unfold paso; rw [if_pos hp]
        have hparEq : pares (t + 1) n = 1 + pares t (n / 2) := by
          show (if n % 2 = 0 then 1 else 0) + pares t (paso n) = 1 + pares t (n / 2)
          rw [if_pos hp, hpaso]
        have himpEq : impares (t + 1) n = impares t (n / 2) := by
          show (if n % 2 = 0 then 0 else 1) + impares t (paso n) = impares t (n / 2)
          rw [if_pos hp, hpaso, Nat.zero_add]
        rw [hparEq] at h
        have hr1 : 1 ≤ r := by omega
        have hpow : 2 ^ (r - 1) * 2 = (2:Nat) ^ r := pow_pred hr1
        have hmul : (2:Nat) ^ r * k = 2 * (2 ^ (r - 1) * k) := by
          rw [← hpow, Nat.mul_comm (2 ^ (r - 1)) 2, Nat.mul_assoc]
        have hstep : paso (2 ^ r * k + n) = 2 ^ (r - 1) * k + n / 2 := by
          unfold paso
          have hmod : (2 ^ r * k + n) % 2 = 0 := by omega
          rw [if_pos hmod]
          omega
        have h2 : pares t (n / 2) < r - 1 := by omega
        have hIH := ih (n / 2) (r - 1) k h2
        calc itera (t + 1) (2 ^ r * k + n)
            = itera t (paso (2 ^ r * k + n)) := rfl
          _ = itera t (2 ^ (r - 1) * k + n / 2) := by rw [hstep]
          _ = 2 ^ (r - 1 - pares t (n / 2)) * 3 ^ (impares t (n / 2)) * k
                + itera t (n / 2) := hIH
          _ = 2 ^ (r - pares (t + 1) n) * 3 ^ (impares (t + 1) n) * k
                + itera (t + 1) n := by
              rw [hparEq, himpEq]
              have e1 : r - 1 - pares t (n / 2) = r - (1 + pares t (n / 2)) := by
                omega
              have e3 : itera (t + 1) n = itera t (n / 2) := by
                show itera t (paso n) = itera t (n / 2)
                rw [hpaso]
              rw [e1, e3]
      · -- paso IMPAR: n -> 3n+1
        have hpaso : paso n = 3 * n + 1 := by
          unfold paso; rw [if_neg hp]
        have hparEq : pares (t + 1) n = pares t (3 * n + 1) := by
          show (if n % 2 = 0 then 1 else 0) + pares t (paso n) = pares t (3 * n + 1)
          rw [if_neg hp, hpaso, Nat.zero_add]
        have himpEq : impares (t + 1) n = 1 + impares t (3 * n + 1) := by
          show (if n % 2 = 0 then 0 else 1) + impares t (paso n) = 1 + impares t (3 * n + 1)
          rw [if_neg hp, hpaso]
        rw [hparEq] at h
        have hr1 : 1 ≤ r := by omega
        have hpow : 2 ^ (r - 1) * 2 = (2:Nat) ^ r := pow_pred hr1
        have hmul : (2:Nat) ^ r * k = 2 * (2 ^ (r - 1) * k) := by
          rw [← hpow, Nat.mul_comm (2 ^ (r - 1)) 2, Nat.mul_assoc]
        have hmul3 : (2:Nat) ^ r * (3 * k) = 3 * (2 ^ r * k) := mul_lc _ _ _
        have hstep : paso (2 ^ r * k + n) = 2 ^ r * (3 * k) + (3 * n + 1) := by
          unfold paso
          have hmod : ¬ ((2 ^ r * k + n) % 2 = 0) := by omega
          rw [if_neg hmod, hmul3]
          omega
        have hIH := ih (3 * n + 1) r (3 * k) h
        calc itera (t + 1) (2 ^ r * k + n)
            = itera t (paso (2 ^ r * k + n)) := rfl
          _ = itera t (2 ^ r * (3 * k) + (3 * n + 1)) := by rw [hstep]
          _ = 2 ^ (r - pares t (3 * n + 1)) * 3 ^ (impares t (3 * n + 1)) * (3 * k)
                + itera t (3 * n + 1) := hIH
          _ = 2 ^ (r - pares (t + 1) n) * 3 ^ (impares (t + 1) n) * k
                + itera (t + 1) n := by
              rw [hparEq, himpEq]
              have e3 : itera (t + 1) n = itera t (3 * n + 1) := by
                show itera t (paso n) = itera t (3 * n + 1)
                rw [hpaso]
              have epow : (3:Nat) ^ (1 + impares t (3 * n + 1))
                  = 3 ^ (impares t (3 * n + 1)) * 3 := by
                rw [Nat.add_comm 1 (impares t (3 * n + 1)), Nat.pow_succ]
              have eac : 2 ^ (r - pares t (3 * n + 1)) * 3 ^ (impares t (3 * n + 1)) * (3 * k)
                  = 2 ^ (r - pares t (3 * n + 1)) * (3 ^ (impares t (3 * n + 1)) * 3) * k := by
                rw [← Nat.mul_assoc _ 3 k, Nat.mul_assoc _ _ 3]
              rw [e3, epow, eac]

/-- EL TEOREMA A26 (G2 con sus dos hipotesis): si n1 y n2 se funden en el
    indice t gastando los MISMOS pares y los MISMOS impares, y r es MAYOR
    que esos pares, entonces 2^r*k + n1 y 2^r*k + n2 se funden en el mismo
    indice t, PARA TODO k (incluido k = 0). -/
theorem garner_G2 (t n1 n2 r k : Nat)
    (hfus : itera t n1 = itera t n2)
    (hpar : pares t n1 = pares t n2)
    (himp : impares t n1 = impares t n2)
    (hr : pares t n1 < r) :
    itera t (2 ^ r * k + n1) = itera t (2 ^ r * k + n2) := by
  rw [desplaza t n1 r k hr]
  rw [desplaza t n2 r k (by rw [← hpar]; exact hr)]
  rw [hfus, hpar, himp]

/- ── CASO CONOCIDO, decidido por el nucleo: el par (4,5) se funde en el
     indice 3 (los dos llegan a 4) gastando 2 pares y 1 impar cada uno. ── -/
theorem base_4_5 :
    itera 3 4 = 4 ∧ itera 3 5 = 4 ∧
    pares 3 4 = 2 ∧ pares 3 5 = 2 ∧
    impares 3 4 = 1 ∧ impares 3 5 = 1 := by decide

/-- Del teorema sale la familia de Garner 1985 entera: e = 2, luego r = 3
    (el minimo permitido), y 8k+4 / 8k+5 se funden PARA TODO k >= 0. -/
theorem familia_garner (k : Nat) : itera 3 (8 * k + 4) = itera 3 (8 * k + 5) := by
  have h := garner_G2 3 4 5 3 k (by decide) (by decide) (by decide) (by decide)
  have e : (2:Nat) ^ 3 = 8 := by decide
  rw [e] at h
  exact h

/-- Un caso concreto de la familia comprobado ademas por el nucleo. -/
theorem familia_caso_k7 : itera 3 (8 * 7 + 4) = itera 3 (8 * 7 + 5) := by decide

/- ── BORDE 1: el "MAYOR que" es necesario. Con r = e (aqui e = 2, r = 2,
     k = 1) la propagacion FALLA: 8 -> 1 pero 9 -> 7 en 3 pasos. ── -/
theorem borde_r_igual_e :
    pares 3 4 = 2 ∧ pares 3 5 = 2 ∧
    itera 3 (2 ^ 2 * 1 + 4) ≠ itera 3 (2 ^ 2 * 1 + 5) := by decide

/- ── BORDE 2: "fundirse" a secas NO basta. El par (3, 20) de la ficha:
     los dos pasan por el 10 en el indice 1, pero 3 gasta 0 pares y 1 impar
     y 20 gasta 1 par y 0 impares. Con r = 2 > pares de los dos tramos y
     k = 1 la propagacion FALLA (7 -> 22, 24 -> 12). Sin la hipotesis de
     las mismas cuentas el enunciado seria falso. ── -/
theorem borde_cuentas_distintas :
    itera 1 3 = itera 1 20 ∧
    pares 1 3 = 0 ∧ pares 1 20 = 1 ∧
    impares 1 3 = 1 ∧ impares 1 20 = 0 ∧
    itera 1 (2 ^ 2 * 1 + 3) ≠ itera 1 (2 ^ 2 * 1 + 20) := by decide

#print axioms desplaza
#print axioms garner_G2
#print axioms familia_garner
#print axioms control_mapa
#print axioms base_4_5
#print axioms borde_r_igual_e
#print axioms borde_cuentas_distintas
