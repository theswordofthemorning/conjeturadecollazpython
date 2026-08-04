/- zoologico.lean
   LOS NUCLEOS DE LOS TEOREMAS QUE VIVIAN SOLO EN .TXT, portados a Lean.
   (04-08-2026; el 13o .lean del repo. Nucleo puro, sin Mathlib.
   Orden del usuario: "pasar los teoremas y lemas que estan solo en .txt
   a Lean, sin borrar los .txt". Los .txt siguen siendo los documentos;
   esto es su esqueleto verificado por maquina.)

   1. JIRAFAS (teoremadejirafas.txt): el argumento entero del teorema --
      igualar dos formas afines en dos puntos fuerza los coeficientes
      (jirafas_coeficientes), y 3^Sx = 3^Sy fuerza Sx = Sy
      (pow3_inyectiva). Compuestos: jirafas_nucleo.
   2. PANDAS (lemadepandas.txt): la discretitud de las potencias de 6 --
      6^d = 1 o 6^d >= 6, y 6^d >= 36 para d >= 2. Es el paso "la unica
      potencia entera de 6 en el intervalo es 6^0" del argumento 6^d.
   3. LOS 3 CHANCHITOS (teoremadelos3chanchitos.txt): D1 = -3 del piso h,
      el grafo {-3, -5} completo con sus dos aterrizajes {-2, -8}, y la
      puerta P3. (Con la cadena (k,c) de cadenakc.lean estos son
      coeficientes concretos: cada transicion es una linea de omega.)
   4. GATAS, rama h (teoremadegatas.txt R5): (4t+3, 4t+4) baja en dos
      pasos a {t+1, 9(t+1) - 1} -- la reduccion que faltaba en Lean.

   Todo con el mapa del atajo sobre Z (division exacta en ambas ramas). -/

def T (n : Int) : Int := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

-- ══ 1. JIRAFAS ══

-- igualar dos formas afines en DOS puntos distintos fuerza pendiente y
-- ordenada (el "igualdad para infinitos r obliga a igualar coeficientes")
theorem jirafas_coeficientes (A B C D r1 r2 : Int)
    (h1 : A * r1 + B = C * r1 + D) (h2 : A * r2 + B = C * r2 + D)
    (hne : r1 ≠ r2) : A = C ∧ B = D := by
  have hAC : A = C := by
    have e : (A - C) * (r1 - r2) = 0 := by
      have e1 : A * r1 - C * r1 = D - B := by omega
      have e2 : A * r2 - C * r2 = D - B := by omega
      have d1 : (A - C) * r1 = A * r1 - C * r1 := by
        rw [Int.sub_mul]
      have d2 : (A - C) * r2 = A * r2 - C * r2 := by
        rw [Int.sub_mul]
      have d3 : (A - C) * (r1 - r2) = (A - C) * r1 - (A - C) * r2 := by
        rw [Int.mul_sub]
      omega
    rcases Int.mul_eq_zero.mp e with h | h
    · omega
    · exact absurd (by omega : r1 = r2) hne
  exact ⟨hAC, by rw [hAC] at h1; omega⟩

-- 3^a es estrictamente creciente, luego inyectiva: Sx = Sy
theorem pow3_pos (a : Nat) : 1 ≤ 3 ^ a := Nat.one_le_pow a 3 (by decide)

theorem pow3_lt (a d : Nat) : 3 ^ a < 3 ^ (a + (d + 1)) := by
  induction d with
  | zero =>
      show 3 ^ a < 3 ^ (a + 1)
      rw [Nat.pow_succ]
      have hp := pow3_pos a
      omega
  | succ n ih =>
      show 3 ^ a < 3 ^ (a + (n + 1) + 1)
      rw [Nat.pow_succ]
      have hp := pow3_pos (a + (n + 1))
      omega

theorem pow3_inyectiva (a b : Nat) (h : 3 ^ a = 3 ^ b) : a = b := by
  cases Nat.lt_trichotomy a b with
  | inl hlt =>
      have ⟨d, hd⟩ : ∃ d, b = a + (d + 1) := ⟨b - a - 1, by omega⟩
      rw [hd] at h
      have := pow3_lt a d
      omega
  | inr hr =>
      cases hr with
      | inl he => exact he
      | inr hlt =>
          have ⟨d, hd⟩ : ∃ d, a = b + (d + 1) := ⟨a - b - 1, by omega⟩
          rw [hd] at h
          have := pow3_lt b d
          omega

-- el nucleo del teorema, compuesto: si las dos trayectorias son afines
-- sobre la clase (Terras 1.2, caja) y coinciden en dos representantes,
-- las pendientes 3^Sx y 3^Sy son iguales, luego Sx = Sy
theorem jirafas_nucleo (Sx Sy : Nat) (Cx Cy r1 r2 : Int)
    (h1 : (3 : Int) ^ Sx * r1 + Cx = (3 : Int) ^ Sy * r1 + Cy)
    (h2 : (3 : Int) ^ Sx * r2 + Cx = (3 : Int) ^ Sy * r2 + Cy)
    (hne : r1 ≠ r2) : Sx = Sy := by
  have ⟨hp, _⟩ := jirafas_coeficientes _ _ _ _ _ _ h1 h2 hne
  have hnat : (3 : Nat) ^ Sx = 3 ^ Sy := by
    have e1 : ((3 ^ Sx : Nat) : Int) = (3 : Int) ^ Sx := Int.natCast_pow 3 Sx
    have e2 : ((3 ^ Sy : Nat) : Int) = (3 : Int) ^ Sy := Int.natCast_pow 3 Sy
    omega
  exact pow3_inyectiva _ _ hnat

-- ══ 2. PANDAS ══

theorem pandas_seis (d : Nat) : 6 ^ d = 1 ∨ 6 ≤ 6 ^ d := by
  cases d with
  | zero => exact Or.inl rfl
  | succ n =>
      right
      have h : 6 ^ (n + 1) = 6 ^ n * 6 := Nat.pow_succ 6 n
      have hp : 1 ≤ 6 ^ n := Nat.one_le_pow n 6 (by decide)
      omega

theorem pandas_seis2 (d : Nat) (hd : 2 ≤ d) : 36 ≤ 6 ^ d := by
  have ⟨e, he⟩ : ∃ e, d = e + 2 := ⟨d - 2, by omega⟩
  have h1 : 6 ^ (e + 2) = 6 ^ (e + 1) * 6 := Nat.pow_succ 6 (e + 1)
  have h2 : 6 ^ (e + 1) = 6 ^ e * 6 := Nat.pow_succ 6 e
  have hp : 1 ≤ 6 ^ e := Nat.one_le_pow e 6 (by decide)
  subst he
  omega

-- ══ 3. LOS 3 CHANCHITOS: el grafo {-3, -5} entero, parametrico ══
-- (formas (1, c): {v, 3v + c}, D = c - 1; el grafo es c en {-2, -4})

-- D1 = -3: el primer paso de {w, 9w - 1} con w = 2u+1 impar cae en la
-- forma (1, -2), o sea D = -3  [el corazon del piso h]
theorem chanchitos_D1 (u : Int) :
    T (2 * u + 1) = 3 * u + 2 ∧
    T (9 * (2 * u + 1) - 1) = 3 * (3 * u + 2) - 2 := by
  constructor
  · unfold T
    have h : (2 * u + 1) % 2 = 1 := by omega
    simp [h]
    omega
  · unfold T
    have h : (9 * (2 * u + 1) - 1) % 2 = 0 := by omega
    simp [h]
    omega

-- el grafo: (1,-2) -0-> (1,-1) [aterriza D=-2]  y  (1,-2) -1-> (1,-4)
theorem chanchitos_c2_b0 (u : Int) :
    T (3 * (2 * u) - 2) = 3 * u - 1 := by
  unfold T
  have h : (3 * (2 * u) - 2) % 2 = 0 := by omega
  simp [h]
  omega

theorem chanchitos_c2_b1 (u : Int) :
    T (3 * (2 * u + 1) - 2) = 3 * (3 * u + 2) - 4 := by
  unfold T
  have h : (3 * (2 * u + 1) - 2) % 2 = 1 := by omega
  simp [h]
  omega

-- (1,-4) -0-> (1,-2)  y  (1,-4) -1-> (1,-7) [aterriza D=-8]
theorem chanchitos_c4_b0 (u : Int) :
    T (3 * (2 * u) - 4) = 3 * u - 2 := by
  unfold T
  have h : (3 * (2 * u) - 4) % 2 = 0 := by omega
  simp [h]
  omega

theorem chanchitos_c4_b1 (u : Int) :
    T (3 * (2 * u + 1) - 4) = 3 * (3 * u + 2) - 7 := by
  unfold T
  have h : (3 * (2 * u + 1) - 4) % 2 = 1 := by omega
  simp [h]
  omega

-- la puerta P3: {v, 9v + 1} con v = 2u+1 impar aterriza DIRECTO en la
-- forma (1, -2), o sea D = -2... no: gap 3v, D = -2 en el estado k=0.
-- La identidad exacta (P3 del .txt): el paso da {3u+2, 9u+5} =
-- {s, 3s - 1}: la forma (1, -1), D = -2.
theorem chanchitos_P3 (u : Int) :
    T (2 * u + 1) = 3 * u + 2 ∧
    T (9 * (2 * u + 1) + 1) = 3 * (3 * u + 2) - 1 := by
  constructor
  · unfold T
    have h : (2 * u + 1) % 2 = 1 := by omega
    simp [h]
    omega
  · unfold T
    have h : (9 * (2 * u + 1) + 1) % 2 = 0 := by omega
    simp [h]
    omega

-- ══ 4. GATAS, LA RAMA h: (4t+3, 4t+4) -> dos pasos -> {t+1, 9(t+1)-1} ══

theorem gatas_rama_h (t : Int) :
    T (T (4 * t + 3)) = 9 * (t + 1) - 1 ∧ T (T (4 * t + 4)) = t + 1 := by
  have p1 : T (4 * t + 3) = 6 * t + 5 := by
    unfold T
    have h : (4 * t + 3) % 2 = 1 := by omega
    simp [h]
    omega
  have p2 : T (4 * t + 4) = 2 * t + 2 := by
    unfold T
    have h : (4 * t + 4) % 2 = 0 := by omega
    simp [h]
    omega
  rw [p1, p2]
  constructor
  · unfold T
    have h : (6 * t + 5) % 2 = 1 := by omega
    simp [h]
    omega
  · unfold T
    have h : (2 * t + 2) % 2 = 0 := by omega
    simp [h]
    omega

-- ── casos por el nucleo (decide) ──
-- Jirafas con numeros: la clase r = 4 mod 8 (Garner) tiene Sx = Sy = 1
theorem caso_jirafas : T (T (T 4)) = T (T (T 5)) ∧ T (T (T 12)) = T (T (T 13)) := by
  decide
-- el germen del piso h (w = 25): (25, 224) con vortice (22, 7)
theorem caso_germen_h : T 25 = 38 ∧ T (9 * 25 - 1) = 112 := by decide
-- la rama h de Gatas con t = 5: (23, 24) -> {6, 53} = {6, 9*6 - 1}
theorem caso_rama_h : T (T 23) = 53 ∧ T (T 24) = 6 := by decide

#print axioms jirafas_coeficientes
#print axioms pow3_inyectiva
#print axioms jirafas_nucleo
#print axioms pandas_seis
#print axioms pandas_seis2
#print axioms chanchitos_D1
#print axioms chanchitos_c2_b1
#print axioms chanchitos_c4_b1
#print axioms chanchitos_P3
#print axioms gatas_rama_h
