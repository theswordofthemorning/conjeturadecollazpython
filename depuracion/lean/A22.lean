/-
  A22 — AGENTE 1 (LEAN), a ciegas.

  ENUNCIADO: a(32) = 1.871.137.623 clases mod 2^32 se funden: cota inferior
  demostrada del 43,5658% de los pares consecutivos (con la misma altura).

  MAPA: el criterio de fusion vive en el mapa del ATAJO
      T(n) = n/2 si n par,  (3n+1)/2 si n impar
  y "altura" es la del mapa CLASICO, que se recupera como
      altura_clasica = j + S_j(n)
  donde j = primer indice con T^j(n) = 1 y S_j = pasos impares del atajo
  (cada paso impar del atajo cuesta 2 pasos clasicos). Aqui todo se define
  sobre T (atajo) y la altura clasica se expresa como j + S_j.

  LO QUE ESTE FICHERO DEMUESTRA (nucleo de Lean 4, sin Mathlib):
    1. terras     : T^k(2^k*m + r) = 3^(S_k(r))*m + T^k(r)   para TODO k, m, r
    2. terras_S   : S_k(2^k*m + r) = S_k(r)                  para TODO k, m, r
    3. fusion_en_k: criterio (S_k(r)=S_k(r+1) y T^k(r)=T^k(r+1))
                    ==> T^k(2^k*m+r) = T^k(2^k*m+(r+1))      para TODO m (incluso m=0)
    4. clase_buena_fusiona: con m >= 1, colas identicas para todo j >= k,
                    S_j identicas para todo j >= k, y ambos iterados >= 2
                    para todo j < k (la hipotesis que en m = 0 se rompe)
    5. misma_altura_clasica: con m >= 1, el primer j con T^j = 1 es el MISMO
                    para los dos, y j + S_j (la altura clasica) coincide.
    6. cuenta k = a(k) para k = 0 y 3..10, por el NUCLEO (decide), contra la
                    sucesion dada en el encargo: 1,3,8,18,39,82,170,351
    7. la aritmetica del porcentaje: 0,435658 <= 1871137623/2^32 < 0,435659
    8. casos concretos por decide: (5,6) con k=5; (101,102) = m=3 de la clase
       r=5 mod 32; el contraejemplo m=0 (alturas 5 y 8); trayectoria del 7.

  LO QUE NO PUEDE DEMOSTRAR: el valor a(32) en si (2^32 clases; prohibido y
  no decidible en tiempo razonable por el nucleo). Se acepta como medicion.
-/

set_option maxRecDepth 40000

/-- El mapa del ATAJO. -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- k iteraciones del atajo. -/
def Tk : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => Tk k (T n)

/-- S_k(n): pasos impares entre los primeros k pasos del atajo. -/
def Sk : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, n => n % 2 + Sk k (T n)

theorem Tk_zero (n : Nat) : Tk 0 n = n := rfl
theorem Tk_succ (k n : Nat) : Tk (k+1) n = Tk k (T n) := rfl
theorem Sk_zero (n : Nat) : Sk 0 n = 0 := rfl
theorem Sk_succ (k n : Nat) : Sk (k+1) n = n % 2 + Sk k (T n) := rfl

/-- Paso par: T(2q + r) = q + T r si r es par. -/
theorem T_even (q r : Nat) (hr : r % 2 = 0) : T (2*q + r) = q + T r := by
  unfold T
  rw [if_pos (show (2*q + r) % 2 = 0 by omega), if_pos hr]
  omega

/-- Paso impar: T(2q + r) = 3q + T r si r es impar. -/
theorem T_odd (q r : Nat) (hr : r % 2 = 1) : T (2*q + r) = 3*q + T r := by
  unfold T
  rw [if_neg (show ¬((2*q + r) % 2 = 0) by omega), if_neg (show ¬(r % 2 = 0) by omega)]
  omega

/-- TERRAS (linealidad): T^k(2^k*m + r) = 3^(S_k(r))*m + T^k(r), sin restriccion
    alguna sobre m ni r. Es el Teorema 1.2 escrito sobre el atajo. -/
theorem terras : ∀ (k m r : Nat), Tk k (2^k * m + r) = 3 ^ (Sk k r) * m + Tk k r := by
  intro k
  induction k with
  | zero =>
    intro m r
    rw [Tk_zero, Tk_zero, Sk_zero]
  | succ k ih =>
    intro m r
    have hsplit : (2:Nat)^(k+1) * m = 2 * (2^k * m) := by
      rw [Nat.pow_succ, Nat.mul_comm ((2:Nat)^k) 2, Nat.mul_assoc]
    rw [Tk_succ, Tk_succ, Sk_succ, hsplit]
    by_cases hr : r % 2 = 0
    · rw [T_even (2^k * m) r hr, ih m (T r), hr, Nat.zero_add]
    · have hr1 : r % 2 = 1 := by omega
      rw [T_odd (2^k * m) r hr1]
      have h3 : 3 * (2^k * m) = 2^k * (3 * m) := by
        rw [← Nat.mul_assoc, Nat.mul_comm 3 ((2:Nat)^k), Nat.mul_assoc]
      rw [h3, ih (3*m) (T r), hr1]
      have h4 : (3:Nat)^(1 + Sk k (T r)) * m = 3^(Sk k (T r)) * (3 * m) := by
        rw [Nat.add_comm 1 (Sk k (T r)), Nat.pow_succ, Nat.mul_assoc]
      rw [h4]

/-- El vector de paridad (y con el S_k) depende solo del resto mod 2^k. -/
theorem terras_S : ∀ (k m r : Nat), Sk k (2^k * m + r) = Sk k r := by
  intro k
  induction k with
  | zero => intro m r; rw [Sk_zero, Sk_zero]
  | succ k ih =>
    intro m r
    have hsplit : (2:Nat)^(k+1) * m = 2 * (2^k * m) := by
      rw [Nat.pow_succ, Nat.mul_comm ((2:Nat)^k) 2, Nat.mul_assoc]
    rw [Sk_succ, Sk_succ, hsplit]
    have hpar : (2 * (2^k * m) + r) % 2 = r % 2 := by omega
    rw [hpar]
    by_cases hr : r % 2 = 0
    · rw [T_even (2^k * m) r hr, ih m (T r)]
    · have hr1 : r % 2 = 1 := by omega
      rw [T_odd (2^k * m) r hr1]
      have h3 : 3 * (2^k * m) = 2^k * (3 * m) := by
        rw [← Nat.mul_assoc, Nat.mul_comm 3 ((2:Nat)^k), Nat.mul_assoc]
      rw [h3, ih (3*m) (T r)]

/-- Componer iteraciones. -/
theorem Tk_add : ∀ (a b n : Nat), Tk (a + b) n = Tk b (Tk a n) := by
  intro a
  induction a with
  | zero => intro b n; rw [Nat.zero_add, Tk_zero]
  | succ a ih =>
    intro b n
    have h : a + 1 + b = (a + b) + 1 := by omega
    rw [h, Tk_succ, Tk_succ, ih b (T n)]

/-- Componer conteos de impares. -/
theorem Sk_add : ∀ (a b n : Nat), Sk (a + b) n = Sk a n + Sk b (Tk a n) := by
  intro a
  induction a with
  | zero => intro b n; rw [Nat.zero_add, Sk_zero, Tk_zero, Nat.zero_add]
  | succ a ih =>
    intro b n
    have h : a + 1 + b = (a + b) + 1 := by omega
    rw [h, Sk_succ, Sk_succ, Tk_succ, ih b (T n)]
    omega

/-- CRITERIO ==> FUSION en el paso k, para TODO m (m = 0 incluido: la fusion
    no es lo que falla en m = 0; lo que falla es la ALTURA). -/
theorem fusion_en_k (k m r : Nat)
    (h1 : Sk k r = Sk k (r+1)) (h2 : Tk k r = Tk k (r+1)) :
    Tk k (2^k * m + r) = Tk k (2^k * m + (r+1)) := by
  rw [terras k m r, terras k m (r+1), h1, h2]

/-- Un paso del atajo divide como mucho entre 2. -/
theorem T_doble (x : Nat) : x ≤ T x * 2 := by
  unfold T
  by_cases h : x % 2 = 0
  · rw [if_pos h]; omega
  · rw [if_neg h]; omega

/-- j pasos dividen como mucho entre 2^j. -/
theorem Tk_doble : ∀ (j x : Nat), x ≤ Tk j x * 2^j := by
  intro j
  induction j with
  | zero => intro x; rw [Tk_zero, Nat.pow_zero, Nat.mul_one]; exact Nat.le_refl x
  | succ j ih =>
    intro x
    rw [Tk_succ, Nat.pow_succ]
    calc x ≤ T x * 2 := T_doble x
      _ ≤ Tk j (T x) * 2^j * 2 := Nat.mul_le_mul (ih (T x)) (Nat.le_refl 2)
      _ = Tk j (T x) * (2^j * 2) := Nat.mul_assoc _ _ _

/-- Con m >= 1, la trayectoria no puede tocar el 1 antes del paso k.
    Esta es la hipotesis que con m = 0 se rompe (y por eso el criterio pide m >= 1). -/
theorem dos_le_Tk (k m r j : Nat) (hm : 1 ≤ m) (hj : j < k) :
    2 ≤ Tk j (2^k * m + r) := by
  have ha : (2:Nat)^k * 1 ≤ 2^k * m := Nat.mul_le_mul_left _ hm
  have hb : (2:Nat)^k ≤ 2^k * m + r := by
    rw [Nat.mul_one] at ha
    omega
  have hk : j + (k - j) = k := by omega
  have hsp : (2:Nat)^(j + (k - j)) = 2^j * 2^(k - j) := Nat.pow_add 2 j (k - j)
  rw [hk] at hsp
  have h2j : (2:Nat) ≤ 2^(k - j) := by
    calc (2:Nat) = 2^1 := (Nat.pow_one 2).symm
      _ ≤ 2^(k - j) := Nat.pow_le_pow_right (by omega) (by omega)
  have hy : (2:Nat)^j * 2 ≤ 2^j * 2^(k - j) := Nat.mul_le_mul_left _ h2j
  have hx := Tk_doble j (2^k * m + r)
  have hchain : 2 * 2^j ≤ Tk j (2^k * m + r) * 2^j := by omega
  exact Nat.le_of_mul_le_mul_right hchain (Nat.pow_pos (by omega))

/-- EL TEOREMA CENTRAL: si la clase r mod 2^k es buena (criterio finito) y
    m >= 1, entonces (a) para todo j >= k las dos trayectorias son IDENTICAS
    en valor y en conteo de impares, y (b) para todo j < k ninguna de las dos
    ha tocado el 1. -/
theorem clase_buena_fusiona (k m r : Nat) (hm : 1 ≤ m)
    (h1 : Sk k r = Sk k (r+1)) (h2 : Tk k r = Tk k (r+1)) :
    (∀ j, k ≤ j →
       Tk j (2^k * m + r) = Tk j (2^k * m + (r+1)) ∧
       Sk j (2^k * m + r) = Sk j (2^k * m + (r+1))) ∧
    (∀ j, j < k → 2 ≤ Tk j (2^k * m + r) ∧ 2 ≤ Tk j (2^k * m + (r+1))) := by
  constructor
  · intro j hj
    have hd : j = k + (j - k) := by omega
    rw [hd, Tk_add, Tk_add, Sk_add, Sk_add, fusion_en_k k m r h1 h2,
        terras_S k m r, terras_S k m (r+1), h1]
    exact ⟨rfl, rfl⟩
  · intro j hj
    exact ⟨dos_le_Tk k m r j hm hj, dos_le_Tk k m (r+1) j hm hj⟩

/-- LA ALTURA CLASICA COINCIDE: si j es el PRIMER indice con T^j = 1 para
    2^k*m + r (con m >= 1 y clase buena), entonces j es tambien el primer
    indice para 2^k*m + (r+1), y las alturas clasicas j + S_j son iguales. -/
theorem misma_altura_clasica (k m r j : Nat) (hm : 1 ≤ m)
    (h1 : Sk k r = Sk k (r+1)) (h2 : Tk k r = Tk k (r+1))
    (hhit : Tk j (2^k * m + r) = 1)
    (hmin : ∀ i, i < j → Tk i (2^k * m + r) ≠ 1) :
    Tk j (2^k * m + (r+1)) = 1 ∧
    (∀ i, i < j → Tk i (2^k * m + (r+1)) ≠ 1) ∧
    j + Sk j (2^k * m + r) = j + Sk j (2^k * m + (r+1)) := by
  have hk : k ≤ j := by
    by_cases h : k ≤ j
    · exact h
    · exfalso
      have hlt : j < k := by omega
      have hge := (clase_buena_fusiona k m r hm h1 h2).2 j hlt
      omega
  have hmain := (clase_buena_fusiona k m r hm h1 h2).1 j hk
  refine ⟨?_, ?_, ?_⟩
  · rw [← hmain.1]; exact hhit
  · intro i hi
    by_cases hik : k ≤ i
    · have hi2 := (clase_buena_fusiona k m r hm h1 h2).1 i hik
      rw [← hi2.1]
      exact hmin i hi
    · have hlow := (clase_buena_fusiona k m r hm h1 h2).2 i (by omega)
      omega
  · rw [hmain.2]

/- ================= LA PARTE COMPUTABLE, CERRADA POR EL NUCLEO ============= -/

/-- El criterio, como Bool decidible. -/
def buenaB (k r : Nat) : Bool := (Sk k r == Sk k (r+1)) && (Tk k r == Tk k (r+1))

theorem buenaB_iff (k r : Nat) :
    buenaB k r = true ↔ (Sk k r = Sk k (r+1) ∧ Tk k r = Tk k (r+1)) := by
  simp [buenaB]

/-- a(k): cuantas clases r de 0..2^k-1 pasan el criterio. -/
def cuenta (k : Nat) : Nat := ((List.range (2^k)).filter (buenaB k)).length

-- Borde k = 0: ninguna clase es buena (T^0(r) = r ≠ r+1).
theorem cuenta_0 : cuenta 0 = 0 := by decide

-- La sucesion dada en el encargo: a(3..10) = 1, 3, 8, 18, 39, 82, 170, 351.
theorem cuenta_3 : cuenta 3 = 1 := by decide
theorem cuenta_4 : cuenta 4 = 3 := by decide
theorem cuenta_5 : cuenta 5 = 8 := by decide
theorem cuenta_6 : cuenta 6 = 18 := by decide
theorem cuenta_7 : cuenta 7 = 39 := by decide
theorem cuenta_8 : cuenta 8 = 82 := by decide
theorem cuenta_9 : cuenta 9 = 170 := by decide
theorem cuenta_10 : cuenta 10 = 351 := by decide
theorem cuenta_11 : cuenta 11 = 721 := by decide

-- La aritmetica del porcentaje: 0,435658 <= 1871137623 / 2^32 < 0,435659.
theorem porcentaje :
    435658 * 2^32 ≤ 1871137623 * 10^6 ∧ 1871137623 * 10^6 < 435659 * 2^32 := by
  decide

-- Caso conocido (5,6) con k = 5: S_5(5) = S_5(6) = 2 y T^5(5) = T^5(6) = 2.
theorem caso_r5_k5 : Sk 5 5 = 2 ∧ Sk 5 6 = 2 ∧ Tk 5 5 = 2 ∧ Tk 5 6 = 2 := by decide

-- Y su instancia m = 3 de la clase (32m+5, 32m+6): el par (101, 102).
theorem caso_101_102 : Tk 5 101 = Tk 5 102 ∧ Sk 5 101 = Sk 5 102 := by decide

-- EL BORDE m = 0, comprobado por el nucleo: el par (5,6) SIN el m >= 1.
-- 5 llega al 1 en 4 pasos del atajo con 1 impar  -> altura clasica 4+1 = 5.
-- 6 llega al 1 en 6 pasos del atajo con 2 impares -> altura clasica 6+2 = 8.
-- Alturas DISTINTAS: por eso el enunciado necesita m >= 1.
theorem contraejemplo_m0 :
    Tk 4 5 = 1 ∧ Sk 4 5 = 1 ∧ Tk 6 6 = 1 ∧ Sk 6 6 = 2 := by decide

-- Trayectoria de control: el 7 tarda 11 pasos del atajo con 5 impares
-- (altura clasica 11 + 5 = 16, el valor conocido).
theorem trayectoria_7 : Tk 11 7 = 1 ∧ Sk 11 7 = 5 := by decide

-- El mapa es el que digo que es: primeros pasos del 7 comprobados a mano.
theorem mapa_correcto : T 7 = 11 ∧ T 11 = 17 ∧ T 17 = 26 ∧ T 26 = 13 ∧ T 6 = 3 := by
  decide

/- ================= CONTROL DE AXIOMAS ============= -/
#print axioms terras
#print axioms terras_S
#print axioms fusion_en_k
#print axioms clase_buena_fusiona
#print axioms misma_altura_clasica
#print axioms cuenta_8
#print axioms porcentaje
#print axioms contraejemplo_m0
