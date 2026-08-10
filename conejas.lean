-- conejas.lean
--
-- LAS NUEVAS NUNCA SE ACABAN, demostrado en el nucleo (09-08-2026,
-- noche). El TEOREMA DE CONEJAS (nuevasfusion.py C5): para todo j PAR
-- (j = 2m+2), el par consecutivo (2^j - 2, 2^j - 1) se funde bajo el
-- mapa del atajo A MAS TARDAR en el paso j+2: los dos miembros llegan
-- al MISMO valor x = 3t+2, donde 3^(j-1) = 4t+3 (el testigo de que
-- 3^(j-1) es 3 mod 4 -- por eso j debe ser par) y w = 2t+1 es el
-- REPUNIT TERNARIO (3^(j-1)-1)/2 del vortice. Corolario del repo:
-- b(j+2) >= 1 para todo j par -- la fuente de clases nuevas no se
-- seca jamas (la "primera vez" exacta la da el barrido de
-- nuevasfusion.py C5; aqui va la mitad formalizable: la fusion en
-- j+2 y que justo antes siguen separados).
--
-- LA FORMA. El atajo como relacion con testigos sin division:
--     PasoT (2u) u          (paso par)
--     PasoT (2u+1) (3u+2)   (paso impar: (3(2u+1)+1)/2 = 3u+2)
-- y CaminoN n a b = "de a se llega a b en EXACTAMENTE n pasos".
--
-- LAS DOS TRAYECTORIAS (j = 2m+2):
--   a: 2^j-2 -par-> 2^(j-1)-1 -[escalera, j-1 impares]-> 3^(j-1)-1
--      -par-> w = 2t+1 -impar-> 3t+2
--   b: 2^j-1 -impar-> 3*2^(j-1)-1 -[escalera, j-1 impares]-> 3^j-1
--      -par-> 6t+4 -par-> 3t+2
-- EL PELDANO de la escalera es el lema de identidad del repo
-- (T(c*2^q - 1) = 3c*2^(q-1) - 1, aqui con c = 3^p), y la escalera
-- sale por induccion. Los largos: 1 + (j-1) + 1 + 1 = j+2 ambos.
--
-- REVISION ADVERSARIAL PROPIA (10-08-2026 madrugada, antes de entrar
-- al repo -- regla del ritmo): (A1) los constructores de PasoT SON el
-- atajo; (A2) para j = 2..20 par las DOS trayectorias reales
-- coinciden PASO A PASO con las formulas de este fichero (arranque,
-- escalera de j-1 peldanos, remates) y llegan al mismo x = 3t+2 en
-- exactamente j+2 pasos; (A3) en el paso j+1 son (w, 3w+1), distintos;
-- (A4) w es el repunit ternario impar; (A5) ninguna fusion real antes
-- de j+2 (esto ultimo lo afirma nuevasfusion C5, no este fichero --
-- comprobado igual). Cero fallos en los cinco.
--
-- Nucleo puro, sin Mathlib. Control final: #print axioms sin sorryAx.

def pot2 : Nat → Int
  | 0 => 1
  | n + 1 => 2 * pot2 n

def pot3 : Nat → Int
  | 0 => 1
  | n + 1 => 3 * pot3 n

inductive PasoT : Int → Int → Prop where
  | par (u : Int) : PasoT (2 * u) u
  | impar (u : Int) : PasoT (2 * u + 1) (3 * u + 2)

inductive CaminoN : Nat → Int → Int → Prop where
  | quieta (a : Int) : CaminoN 0 a a
  | anda {n : Nat} {a b c : Int} (cab : CaminoN n a b) (pbc : PasoT b c) :
      CaminoN (n + 1) a c

-- prepender un paso por la izquierda
theorem anda_izq {n : Nat} {a b c : Int} (pab : PasoT a b)
    (cbc : CaminoN n b c) : CaminoN (n + 1) a c := by
  induction cbc with
  | quieta d => exact CaminoN.anda (CaminoN.quieta a) pab
  | anda cab pbc ih => exact CaminoN.anda (ih pab) pbc

-- EL PELDANO: 3^p * 2^(q+1) - 1  --paso impar-->  3^(p+1) * 2^q - 1
theorem peldano (p q : Nat) :
    PasoT (pot3 p * pot2 (q + 1) - 1) (pot3 (p + 1) * pot2 q - 1) := by
  have h1 : pot3 p * pot2 (q + 1) - 1 = 2 * (pot3 p * pot2 q - 1) + 1 := by
    show pot3 p * (2 * pot2 q) - 1 = 2 * (pot3 p * pot2 q - 1) + 1
    rw [Int.mul_left_comm]
    omega
  have h2 : pot3 (p + 1) * pot2 q - 1 = 3 * (pot3 p * pot2 q - 1) + 2 := by
    show 3 * pot3 p * pot2 q - 1 = 3 * (pot3 p * pot2 q - 1) + 2
    rw [Int.mul_assoc]
    omega
  rw [h1, h2]
  exact PasoT.impar _

-- LA ESCALERA: i peldanos impares seguidos
theorem escalera (i : Nat) : ∀ (p q : Nat),
    CaminoN i (pot3 p * pot2 (q + i) - 1) (pot3 (p + i) * pot2 q - 1) := by
  induction i with
  | zero => intro p q; exact CaminoN.quieta _
  | succ n ih =>
      intro p q
      have paso := peldano (p + n) q
      have cuerpo := ih p (q + 1)
      have e1 : q + 1 + n = q + (n + 1) := by omega
      rw [e1] at cuerpo
      exact CaminoN.anda cuerpo paso

-- 3^(2m+1) es 3 mod 4: el testigo t (la razon por la que j es PAR)
theorem tres_mod4 : (m : Nat) → ∃ t : Int, pot3 (2 * m + 1) = 4 * t + 3
  | 0 => ⟨0, rfl⟩
  | m + 1 =>
    match tres_mod4 m with
    | ⟨t, h⟩ => ⟨9 * t + 6, by
        have e : 2 * (m + 1) + 1 = (2 * m + 1) + 1 + 1 := by omega
        rw [e]
        show 3 * (3 * pot3 (2 * m + 1)) = 4 * (9 * t + 6) + 3
        rw [h]; omega⟩

theorem pot3_pos : (n : Nat) → 1 ≤ pot3 n
  | 0 => by decide
  | n + 1 => by
      have h := pot3_pos n
      show 1 ≤ 3 * pot3 n
      omega

-- EL TEOREMA DE CONEJAS
theorem conejas (m : Nat) :
    ∃ t : Int, pot3 (2 * m + 1) = 4 * t + 3 ∧
      CaminoN (2 * m + 4) (pot2 (2 * m + 2) - 2) (3 * t + 2) ∧
      CaminoN (2 * m + 4) (pot2 (2 * m + 2) - 1) (3 * t + 2) := by
  match tres_mod4 m with
  | ⟨t, h4⟩ =>
    refine ⟨t, h4, ?_, ?_⟩
    -- ---------- CAMINO a ----------
    · have p1 : PasoT (pot2 (2 * m + 2) - 2) (pot2 (2 * m + 1) - 1) := by
        have e : pot2 (2 * m + 2) - 2 = 2 * (pot2 (2 * m + 1) - 1) := by
          show 2 * pot2 (2 * m + 1) - 2 = 2 * (pot2 (2 * m + 1) - 1)
          omega
        rw [e]
        exact PasoT.par _
      have esc := escalera (2 * m + 1) 0 0
      have e1 : (0 : Nat) + (2 * m + 1) = 2 * m + 1 := by omega
      rw [e1] at esc
      have e2 : pot3 0 * pot2 (2 * m + 1) - 1 = pot2 (2 * m + 1) - 1 := by
        show (1 : Int) * pot2 (2 * m + 1) - 1 = pot2 (2 * m + 1) - 1
        rw [Int.one_mul]
      rw [e2] at esc
      have e3 : pot3 (2 * m + 1) * pot2 0 - 1 = pot3 (2 * m + 1) - 1 := by
        show pot3 (2 * m + 1) * 1 - 1 = pot3 (2 * m + 1) - 1
        rw [Int.mul_one]
      rw [e3] at esc
      have p3 : PasoT (pot3 (2 * m + 1) - 1) (2 * t + 1) := by
        have e : pot3 (2 * m + 1) - 1 = 2 * (2 * t + 1) := by omega
        rw [e]
        exact PasoT.par _
      have p4 : PasoT (2 * t + 1) (3 * t + 2) := PasoT.impar t
      exact CaminoN.anda (CaminoN.anda (anda_izq p1 esc) p3) p4
    -- ---------- CAMINO b ----------
    · have p1 : PasoT (pot2 (2 * m + 2) - 1) (pot3 1 * pot2 (2 * m + 1) - 1) := by
        have ea : pot2 (2 * m + 2) - 1 = 2 * (pot2 (2 * m + 1) - 1) + 1 := by
          show 2 * pot2 (2 * m + 1) - 1 = 2 * (pot2 (2 * m + 1) - 1) + 1
          omega
        have eb : pot3 1 * pot2 (2 * m + 1) - 1
            = 3 * (pot2 (2 * m + 1) - 1) + 2 := by
          show 3 * pot3 0 * pot2 (2 * m + 1) - 1
              = 3 * (pot2 (2 * m + 1) - 1) + 2
          show 3 * 1 * pot2 (2 * m + 1) - 1
              = 3 * (pot2 (2 * m + 1) - 1) + 2
          rw [Int.mul_one, Int.mul_sub]
          omega
        rw [ea, eb]
        exact PasoT.impar _
      have esc := escalera (2 * m + 1) 1 0
      have e1 : (0 : Nat) + (2 * m + 1) = 2 * m + 1 := by omega
      rw [e1] at esc
      have e3 : pot3 (1 + (2 * m + 1)) * pot2 0 - 1 = pot3 (2 * m + 2) - 1 := by
        have en : (1 : Nat) + (2 * m + 1) = 2 * m + 2 := by omega
        rw [en]
        show pot3 (2 * m + 2) * 1 - 1 = pot3 (2 * m + 2) - 1
        rw [Int.mul_one]
      rw [e3] at esc
      have p3 : PasoT (pot3 (2 * m + 2) - 1) (2 * (3 * t + 2)) := by
        have e : pot3 (2 * m + 2) - 1 = 2 * (2 * (3 * t + 2)) := by
          show 3 * pot3 (2 * m + 1) - 1 = 2 * (2 * (3 * t + 2))
          rw [h4]; omega
        rw [e]
        exact PasoT.par _
      have p4 : PasoT (2 * (3 * t + 2)) (3 * t + 2) := PasoT.par _
      exact CaminoN.anda (CaminoN.anda (anda_izq p1 esc) p3) p4

-- Y JUSTO ANTES DE FUNDIR SIGUEN SEPARADOS: en el paso j+1 los dos
-- valores son w = 2t+1 (impar) y 3w+1 = 6t+4 (par) -- distintos para
-- TODO t: la fusion del paso j+2 es un encuentro de verdad.
theorem separados_antes (t : Int) : 2 * t + 1 ≠ 2 * (3 * t + 2) := by
  omega

-- EL CASO CONOCIDO DEL REPO (j = 2, el par (2,3)): las trayectorias
-- reales son 2,1,2,1,2 y 3,5,8,4,2 -- se encuentran en x = 2 en el
-- paso 4 = j+2, con t = 0 (3^1 = 4*0+3). Cerrado instanciando el
-- teorema y por decide en los valores.
example :
    CaminoN 4 (pot2 2 - 2) 2 ∧ CaminoN 4 (pot2 2 - 1) 2 := by
  match conejas 0 with
  | ⟨t, h4, ca, cb⟩ =>
    have h4' : pot3 1 = 4 * t + 3 := h4
    have hv : pot3 1 = 3 := by decide
    have ht : t = 0 := by omega
    rw [ht] at ca cb
    exact ⟨ca, cb⟩

theorem caso_valores : pot2 2 - 2 = 2 ∧ pot2 2 - 1 = 3 ∧ pot3 1 = 3 := by
  decide

#print axioms peldano
#print axioms escalera
#print axioms tres_mod4
#print axioms conejas
#print axioms separados_antes
#print axioms caso_valores
