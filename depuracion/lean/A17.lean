/-
  A17: sigma_clasico(n) = sigma_atajo(n) + (pasos impares dentro de ellos), exacto.

  MAPAS (escritos aqui mismo, sin leer nada del repo):
    C = mapa CLASICO : n/2 si par, 3n+1 si impar
    T = mapa ATAJO   : n/2 si par, (3n+1)/2 si impar

  sigma = tiempo de parada (glide): primer indice cuyo valor cae por debajo de n.
  Como sigma solo esta definido cuando la trayectoria baja (afirmarlo para todo n
  seria la conjetura), el teorema se enuncia CONDICIONAL:

    si el atajo no baja de n en los pasos 0..s-1 y baja en el paso s
    (o sea sigma_atajo(n) = s), y A = pasos impares entre esos s,
    entonces el clasico no baja en los pasos 0..s+A-1 y baja en el paso s+A
    (o sea sigma_clasico(n) = s + A).

  Eso es exactamente el enunciado A17 para cualquier n cuyo sigma exista,
  que es el unico caso en que el enunciado tiene sentido.
-/

set_option maxRecDepth 40000

namespace A17

/-- mapa CLASICO -/
def C (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- mapa del ATAJO -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- k iteraciones del clasico -/
def iterC (n : Nat) : Nat → Nat
  | 0 => n
  | k+1 => C (iterC n k)

/-- k iteraciones del atajo -/
def iterT (n : Nat) : Nat → Nat
  | 0 => n
  | k+1 => T (iterT n k)

/-- pasos impares entre los primeros k pasos del atajo -/
def A (n : Nat) : Nat → Nat
  | 0 => 0
  | k+1 => A n k + (if (iterT n k) % 2 = 0 then 0 else 1)

/-- indice clasico que corresponde al indice k del atajo -/
def idx (n k : Nat) : Nat := k + A n k

theorem iterC_succ (n k : Nat) : iterC n (k+1) = C (iterC n k) := rfl

theorem A_succ (n k : Nat) :
    A n (k+1) = A n k + (if (iterT n k) % 2 = 0 then 0 else 1) := rfl

/-- LA CORRESPONDENCIA: el valor del atajo en el paso k es el valor del
    clasico en el paso k + A(k). Vale para TODO n y TODO k, sin hipotesis. -/
theorem interleave (n : Nat) : ∀ k, iterC n (idx n k) = iterT n k := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    by_cases h : (iterT n k) % 2 = 0
    · -- paso PAR: un solo paso clasico
      have hidx : idx n (k+1) = idx n k + 1 := by
        unfold idx; rw [A_succ, if_pos h]; omega
      rw [hidx, iterC_succ, ih]
      show C (iterT n k) = T (iterT n k)
      unfold C T; rw [if_pos h, if_pos h]
    · -- paso IMPAR: dos pasos clasicos, con 3m+1 en medio
      have h1 : (iterT n k) % 2 = 1 := by omega
      have hidx : idx n (k+1) = idx n k + 2 := by
        unfold idx; rw [A_succ, if_neg h]; omega
      have hC1 : C (iterT n k) = 3 * (iterT n k) + 1 := by
        unfold C; rw [if_neg h]
      have heven : (3 * (iterT n k) + 1) % 2 = 0 := by omega
      have hC2 : C (3 * (iterT n k) + 1) = (3 * (iterT n k) + 1) / 2 := by
        unfold C; rw [if_pos heven]
      have hT : T (iterT n k) = (3 * (iterT n k) + 1) / 2 := by
        unfold T; rw [if_neg h]
      rw [hidx]
      show C (C (iterC n (idx n k))) = iterT n (k+1)
      rw [ih, hC1, hC2]
      show (3 * (iterT n k) + 1) / 2 = T (iterT n k)
      rw [hT]

/-- Si el atajo no ha bajado de n antes del paso s, el clasico no baja de n
    antes del paso idx(s) = s + A(s): los valores compartidos son los mismos
    y los intermedios 3m+1 de los pasos impares son SIEMPRE > m >= n. -/
theorem clasico_no_baja_antes (n s : Nat)
    (H : ∀ j, j < s → n ≤ iterT n j) :
    ∀ i, i < idx n s → n ≤ iterC n i := by
  induction s with
  | zero =>
    intro i hi
    unfold idx A at hi
    omega
  | succ s ih =>
    intro i hi
    have Hs : ∀ j, j < s → n ≤ iterT n j := fun j hj => H j (Nat.lt_succ_of_lt hj)
    have hTs : n ≤ iterT n s := H s (Nat.lt_succ_self s)
    by_cases h : (iterT n s) % 2 = 0
    · have hidx : idx n (s+1) = idx n s + 1 := by
        unfold idx; rw [A_succ, if_pos h]; omega
      rw [hidx] at hi
      by_cases hlt : i < idx n s
      · exact ih Hs i hlt
      · have hieq : i = idx n s := by omega
        rw [hieq, interleave]
        exact hTs
    · have h1 : (iterT n s) % 2 = 1 := by omega
      have hidx : idx n (s+1) = idx n s + 2 := by
        unfold idx; rw [A_succ, if_neg h]; omega
      rw [hidx] at hi
      by_cases hlt : i < idx n s
      · exact ih Hs i hlt
      · by_cases heq : i = idx n s
        · rw [heq, interleave]; exact hTs
        · have hieq : i = idx n s + 1 := by omega
          rw [hieq, iterC_succ, interleave]
          have hC1 : C (iterT n s) = 3 * (iterT n s) + 1 := by
            unfold C; rw [if_neg h]
          rw [hC1]
          omega

/-- EL ENUNCIADO A17, en forma de teorema exacto:
    sigma_atajo(n) = s con A(s) pasos impares  ==>  sigma_clasico(n) = s + A(s).
    Las dos conjunciones de la conclusion son exactamente "el clasico baja por
    primera vez en el paso s + A(s)". -/
theorem sigma_clasico_eq_sigma_atajo_mas_impares (n s : Nat)
    (H : ∀ j, j < s → n ≤ iterT n j)   -- el atajo no baja antes de s
    (Hs : iterT n s < n) :             -- y baja en s: sigma_atajo = s
    (∀ i, i < s + A n s → n ≤ iterC n i) ∧ iterC n (s + A n s) < n := by
  constructor
  · exact clasico_no_baja_antes n s H
  · have hi : iterC n (idx n s) = iterT n s := interleave n s
    unfold idx at hi
    rw [hi]
    exact Hs

/- ===== CASOS CONOCIDOS, COMPROBADOS POR EL NUCLEO (by decide, no #eval) ===== -/

/-- BORDE n = 2: sigma_atajo = 1, 0 impares, sigma_clasico = 1. -/
theorem caso_2 :
    (∀ j, j < 1 → 2 ≤ iterT 2 j) ∧ iterT 2 1 < 2 ∧ A 2 1 = 0 ∧
    (∀ i, i < 1 → 2 ≤ iterC 2 i) ∧ iterC 2 1 < 2 := by decide

/-- n = 3: sigma_atajo = 4, 2 impares, sigma_clasico = 6. -/
theorem caso_3 :
    (∀ j, j < 4 → 3 ≤ iterT 3 j) ∧ iterT 3 4 < 3 ∧ A 3 4 = 2 ∧
    (∀ i, i < 6 → 3 ≤ iterC 3 i) ∧ iterC 3 6 < 3 := by decide

/-- n = 7: sigma_atajo = 7, 4 impares, sigma_clasico = 11, y los dos
    terminan en el MISMO valor, 5. -/
theorem caso_7 :
    (∀ j, j < 7 → 7 ≤ iterT 7 j) ∧ iterT 7 7 = 5 ∧ A 7 7 = 4 ∧
    (∀ i, i < 11 → 7 ≤ iterC 7 i) ∧ iterC 7 11 = 5 := by decide

/-- EL CASO GRANDE, n = 27: sigma_atajo = 59, 37 impares,
    sigma_clasico = 59 + 37 = 96 (el glide publicado del 27),
    y los dos mapas aterrizan en 23. -/
theorem caso_27 :
    (∀ j, j < 59 → 27 ≤ iterT 27 j) ∧ iterT 27 59 = 23 ∧ A 27 59 = 37 ∧
    (∀ i, i < 96 → 27 ≤ iterC 27 i) ∧ iterC 27 96 = 23 := by decide

/-- BORDE n = 1: el atajo NUNCA baja de 1 (cicla 1 -> 2 -> 1), asi que la
    hipotesis del teorema es incumplible en los primeros pasos: sigma no existe
    y el enunciado es vacuo ahi. Comprobado el ciclo por el nucleo. -/
theorem caso_1_no_baja : iterT 1 2 = 1 ∧ (∀ j, j < 20 → 1 ≤ iterT 1 j) := by decide

#print axioms interleave
#print axioms clasico_no_baja_antes
#print axioms sigma_clasico_eq_sigma_atajo_mas_impares
#print axioms caso_2
#print axioms caso_3
#print axioms caso_7
#print axioms caso_27

end A17
