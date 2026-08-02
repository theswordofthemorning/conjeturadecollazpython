/-
  A15: T(2^k - n) = 2^(k-1) - T(n) para n PAR ("el espejo base 2 conmuta
  con Collatz en los pasos pares").

  Mapa usado: el CLASICO  T(n) = n/2 si n par, 3n+1 si n impar.
  Nota: el enunciado solo toca la rama PAR, que es identica en el mapa
  clasico y en el del atajo ((3n+1)/2), asi que la identidad es la misma
  para los dos mapas.

  Se demuestra sobre Nat (resta truncada) para todo n par y todo k >= 1,
  SIN hipotesis n <= 2^k: con resta truncada la identidad vale igual
  cuando n > 2^k (los dos lados truncan a 0 a la vez, porque
  n >= 2^k  <->  n/2 >= 2^(k-1) para n par).

  Bordes comprobados como contraejemplos con decide:
    - k = 0  rompe la identidad (T(1-n) no es un paso par).
    - n impar rompe la identidad (la rama impar no conmuta con el espejo).
-/

-- el mapa clasico, escrito aqui mismo (no importado de ningun sitio)
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

-- version con el exponente en forma j+1 (o sea k >= 1 estructural)
theorem espejo_par_succ (j n : Nat) (hn : n % 2 = 0) :
    T (2 ^ (j + 1) - n) = 2 ^ j - T n := by
  have hp : 2 ^ (j + 1) = 2 * 2 ^ j := by
    rw [Nat.pow_succ, Nat.mul_comm]
  rw [hp]
  generalize 2 ^ j = p
  have h1 : (2 * p - n) % 2 = 0 := by omega
  unfold T
  rw [if_pos h1, if_pos hn]
  omega

-- el enunciado tal como esta en la base: k >= 1, n par, todo n
theorem espejoA15 (k n : Nat) (hk : 1 ≤ k) (hn : n % 2 = 0) :
    T (2 ^ k - n) = 2 ^ (k - 1) - T n := by
  cases k with
  | zero => exact absurd hk (by decide)
  | succ j =>
      show T (2 ^ (j + 1) - n) = 2 ^ (j + 1 - 1) - T n
      rw [Nat.add_sub_cancel]
      exact espejo_par_succ j n hn

-- == casos conocidos, comprobados por el NUCLEO con decide (no #eval) ==

-- caso concreto: k = 6, n = 40:  T(64-40) = T(24) = 12  y  32 - T(40) = 32 - 20 = 12
theorem caso_64_40 : T (2 ^ 6 - 40) = 2 ^ 5 - T 40 := by decide

-- barrido exhaustivo chico: k = 7, todos los n pares < 128
theorem barrido_k7 : ∀ n : Nat, n < 128 → n % 2 = 0 → T (2 ^ 7 - n) = 2 ^ 6 - T n := by
  decide

-- y fuera de rango (n > 2^k) tambien vale, por la resta truncada:
theorem fuera_de_rango : T (2 ^ 4 - 100) = 2 ^ 3 - T 100 := by decide

-- == los dos bordes que ROMPEN el enunciado si se quitan hipotesis ==

-- k = 0 NO vale:  T(2^0 - 0) = T(1) = 4,  pero 2^(0-1) - T(0) = 1 - 0 = 1
theorem borde_k0_falla : ¬ (T (2 ^ 0 - 0) = 2 ^ (0 - 1) - T 0) := by decide

-- n IMPAR no vale:  k = 3, n = 1:  T(7) = 22,  pero 4 - T(1) = 4 - 4 = 0
theorem borde_impar_falla : ¬ (T (2 ^ 3 - 1) = 2 ^ 2 - T 1) := by decide

-- control de que T es Collatz de verdad: la trayectoria del 6
-- 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
theorem control_trayectoria_6 :
    T 6 = 3 ∧ T 3 = 10 ∧ T 10 = 5 ∧ T 5 = 16 ∧ T 16 = 8 ∧
    T 8 = 4 ∧ T 4 = 2 ∧ T 2 = 1 := by decide

#print axioms espejo_par_succ
#print axioms espejoA15
#print axioms caso_64_40
#print axioms barrido_k7
#print axioms fuera_de_rango
#print axioms borde_k0_falla
#print axioms borde_impar_falla
#print axioms control_trayectoria_6
