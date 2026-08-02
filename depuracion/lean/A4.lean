/-
A4 (Agente 1, LEAN) - trio de verificacion.

ENUNCIADO (literal de la base):
  eps = ln( 2^B / (3^A * n) ) es identicamente igual a la suma de
  ln(1 + 1/(3x)) sobre los valores impares x de la trayectoria completa
  de n hasta 1. Mapa CLASICO (par -> n/2, impar -> 3n+1); A = pasos
  impares, B = pasos pares; el 1 final no se cuenta.

MAPA USADO AQUI: el CLASICO, definido abajo en `paso`, y anclado con
`decide` (nucleo, no #eval) a la trayectoria conocida del 7 y a los
conteos conocidos del 27 (A = 41, B = 70, 111 pasos).

QUE SE FORMALIZA: `ln` no existe en el nucleo de Lean (no hay reales).
El contenido exacto del enunciado es su equivalente multiplicativo,
que la propia base declara: 2^B/(3^A*n) = prod(1 + 1/(3x)).
Cada factor es (3x+1)/(3x); el producto entero es
prod(3x+1) / (3^A * prod x). Con todo positivo, la identidad de
fracciones equivale a la identidad ENTERA

    2^B * (prod de los x impares) = n * (prod de los (3x+1))       (*)

(el 3^A aparece igual en los dos denominadores y se cancela; abajo se
demuestra tambien la version con el 3^A puesto, `identidad_con_3A`).

Se demuestra (*) para TODO n cuya trayectoria llega a 1, con cualquier
fuel. La identidad presupone trayectoria completa: A y B no existen sin
ella. El paso de (*) a la version con ln es dividir por 3^A * n * prod x
(positivos) y aplicar ln (inyectiva, producto -> suma); ese ultimo paso
es estandar y queda fuera del nucleo por no haber reales.
-/

set_option maxRecDepth 40000

-- el mapa clasico
def paso (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

def itera : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => itera k (paso n)

-- info fuel n = some (A, B, prod de impares x, prod de (3x+1)) si llega a 1
def info : Nat → Nat → Option (Nat × Nat × Nat × Nat)
  | 0, _ => none
  | fuel+1, n =>
    if n = 1 then some (0, 0, 1, 1)
    else if n % 2 = 0 then
      match info fuel (n / 2) with
      | none => none
      | some (a, b, p, q) => some (a, b + 1, p, q)
    else
      match info fuel (3 * n + 1) with
      | none => none
      | some (a, b, p, q) => some (a + 1, b, n * p, (3 * n + 1) * q)

-- EL TEOREMA: la identidad entera (*) para todo n que llega a 1
theorem identidad : ∀ (fuel n a b p q : Nat),
    info fuel n = some (a, b, p, q) → 2 ^ b * p = n * q := by
  intro fuel
  induction fuel with
  | zero =>
    intro n a b p q h
    simp [info] at h
  | succ f ih =>
    intro n a b p q h
    simp only [info] at h
    split at h
    · rename_i hn
      injection h with h1
      injection h1 with ha h2
      injection h2 with hb h3
      injection h3 with hp hq
      rw [← hb, ← hp, ← hq, hn]
    · rename_i hn
      split at h
      · -- caso par
        rename_i hpar
        split at h
        · simp at h
        · rename_i a' b' p' q' heq
          injection h with h1
          injection h1 with ha h2
          injection h2 with hb h3
          injection h3 with hp hq
          rw [← hb, ← hp, ← hq]
          have hrec := ih (n / 2) a' b' p' q' heq
          have h2 : 2 * (n / 2) = n := by omega
          calc 2 ^ (b' + 1) * p'
              = 2 ^ b' * 2 * p' := by rw [Nat.pow_succ]
            _ = 2 * (2 ^ b' * p') := by
                rw [Nat.mul_comm (2 ^ b') 2, Nat.mul_assoc]
            _ = 2 * (n / 2 * q') := by rw [hrec]
            _ = 2 * (n / 2) * q' := by rw [← Nat.mul_assoc]
            _ = n * q' := by rw [h2]
      · -- caso impar
        rename_i hpar
        split at h
        · simp at h
        · rename_i a' b' p' q' heq
          injection h with h1
          injection h1 with ha h2
          injection h2 with hb h3
          injection h3 with hp hq
          rw [← hb, ← hp, ← hq]
          have hrec := ih (3 * n + 1) a' b' p' q' heq
          calc 2 ^ b' * (n * p')
              = n * (2 ^ b' * p') := by
                rw [← Nat.mul_assoc, Nat.mul_comm (2 ^ b') n, Nat.mul_assoc]
            _ = n * ((3 * n + 1) * q') := by rw [hrec]

-- version con el 3^A puesto, para calcar el enunciado:
-- 2^B * (3^A * prod x) = 3^A * (n * prod(3x+1)),
-- o sea 2^B/(3^A*n) = prod(3x+1)/(3^A*prod x) cruz-multiplicado
theorem identidad_con_3A : ∀ (fuel n a b p q : Nat),
    info fuel n = some (a, b, p, q) →
    2 ^ b * (3 ^ a * p) = 3 ^ a * (n * q) := by
  intro fuel n a b p q h
  have hi := identidad fuel n a b p q h
  calc 2 ^ b * (3 ^ a * p)
      = 3 ^ a * (2 ^ b * p) := by
        rw [← Nat.mul_assoc, Nat.mul_comm (2 ^ b) (3 ^ a), Nat.mul_assoc]
    _ = 3 ^ a * (n * q) := by rw [hi]

-- ===================== ANCLAS CONTRA LA TRAMPA =====================
-- (Lean garantiza demostracion-enunciado; esto ancla enunciado-objeto)

-- la trayectoria conocida del 7, entera, por el nucleo
theorem tray7 : (List.range 17).map (fun k => itera k 7) =
    [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1] := by decide

-- el mapa NO es el atajo: al 5 le sigue 16, no 8
theorem no_es_atajo : paso 5 = 16 := by decide

-- bordes: n = 1 (cero pasos, productos vacios) y n = 2
theorem caso1 : info 1 1 = some (0, 0, 1, 1) := by decide
theorem caso2 : info 2 2 = some (0, 1, 1, 1) := by decide

-- caso con los productos calculados A MANO fuera de Lean:
-- impares del 7: 7*11*17*13*5 = 85085 ; (3x+1): 22*34*52*40*16 = 24893440
theorem caso7 : info 20 7 = some (5, 11, 85085, 24893440) := by decide
theorem caso7_identidad : 2 ^ 11 * 85085 = 7 * 24893440 := by decide

-- caso conocido de la literatura: el 27 tiene A = 41 impares y B = 70 pares
def conteo (fuel n : Nat) : Option (Nat × Nat) :=
  match info fuel n with
  | none => none
  | some (a, b, _, _) => some (a, b)

theorem caso27 : conteo 200 27 = some (41, 70) := by decide

-- la identidad comprobada por el nucleo en n = 1 .. 30
def comprueba (fuel n : Nat) : Bool :=
  match info fuel n with
  | none => false
  | some (_, b, p, q) => 2 ^ b * p == n * q

theorem casos_1_a_30 :
    ((List.range 30).all fun i => comprueba 300 (i + 1)) = true := by decide

-- la forma con fracciones del enunciado, en un caso concreto, en su
-- version cruz-multiplicada exacta (n = 3, impares 3 y 5, A = 2, B = 5):
--   2^5/(3^2*3) = (1+1/(3*3)) * (1+1/(3*5))  =  (10/9)*(16/15)
-- cruz-multiplicado con todo positivo:
--   (3*3+1)*(3*5+1) * (3^2*3)  =  (3*3)*(3*5) * 2^5     (4320 = 4320)
-- (la division exacta de Rat se atasca en el kernel por Nat.gcd;
--  la igualdad de fracciones positivas ES su cruz-multiplicacion)
theorem caso3_fracciones :
    (3*3+1) * (3*5+1) * (3^2*3) = (3*3) * (3*5) * 2^5 := by decide

#print axioms identidad
#print axioms identidad_con_3A
#print axioms tray7
#print axioms caso7
#print axioms caso27
#print axioms casos_1_a_30
#print axioms caso3_fracciones
