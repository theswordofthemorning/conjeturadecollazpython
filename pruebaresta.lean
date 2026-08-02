/-
  pruebaresta.lean

  LA COMPILACION QUE DECIDIO UNA DISPUTA. No demuestra nada sobre Collatz:
  demuestra algo sobre COMO SE ESCRIBE una demostracion, y por eso existe.

  ---------------------------------------------------------------------------
  DE QUE VA
  ---------------------------------------------------------------------------

  El 01-08-2026 el CLAUDE.md afirmo, sobre el mapa 3n-1:

      "la C es negativa y el tipo Nat ya no sirve"

  y colgo de ahi un corolario mas fuerte: que la discriminacion del control A/B
  entre 3n+1 y 3n-1 aparece en Lean "como un cambio de tipo forzoso".

  El trio de LA REGLA DE LOS TRES devolvio dos respuestas que PARECIAN
  contradecirse. El agente 1 (cotatramos3n1.lean) dijo que no hizo falta salir
  de Nat, y que el truco es poner la C en el lado del n_k:

      2^B*n_k + C = 3^A*n0        (sin ninguna resta)

  y que con la forma restada -- 2^B*n_k = 3^A*n0 - C -- "la induccion NO SE
  SOSTIENE SOLA en Nat", porque habria que arrastrar C <= 3^A*n0 como segunda
  mitad del invariante. El agente 2 (cotatramos3n1.py) dijo que lo que cambia
  es el SIGNO de la C.

  ---------------------------------------------------------------------------
  QUE HACE ESTE FICHERO
  ---------------------------------------------------------------------------

  Intenta lo que el agente 1 declaro imposible: conservar la forma CON RESTA
  TRUNCADA, sobre un estado ARBITRARIO (no solo alcanzable), SIN ninguna
  hipotesis extra y SIN reforzar el invariante.

  COMPILA. Y con eso quedan decididas tres cosas a la vez:

    1. "el tipo Nat ya no sirve" es FALSO. Las dos formas viven en Nat.
    2. La explicacion del agente 1 tambien era falsa, aunque su conclusion
       fuera correcta: poner la C al otro lado es MAS COMODO, no NECESARIO.
       Cuesta cuatro lineas mas, no un invariante reforzado.
    3. Los dos agentes no se contradecian. Sus dos C son OPUESTAS
       (C_lean = -C_python), o sea el mismo objeto con el signo cambiado. El
       error del CLAUDE.md no era ninguna de las dos mitades: era el "luego"
       que las unia. Un no sequitur, no un desacuerdo empirico.

  POR QUE CIERRA SOLA, en una linea: en la rama impar el propio invariante ya
  fuerza 2^B*n_k >= 1, y de ahi sale que la resta no trunca. Es el MISMO hecho
  que `impar_no_trunca` de cotatramos3n1.lean necesitaba de todas formas.

  ---------------------------------------------------------------------------
  LO QUE ESTE FICHERO NO ES
  ---------------------------------------------------------------------------

  No aporta ninguna matematica nueva sobre 3n-1 ni sobre Collatz: la identidad,
  la cota y el corolario estan en cotatramos3n1.lean y ahi es donde valen. Esto
  es el registro de que una frase publicada se refuto COMPILANDO en vez de
  opinando, que es la unica ventaja que Lean tiene sobre un agente adversarial.

  Se comprueba con:   lean pruebaresta.lean
  Si no imprime ningun "error:", la disputa esta cerrada.
-/

set_option maxRecDepth 40000

structure Tramo where
  n : Nat
  A : Nat
  B : Nat
  C : Nat

def paso (s : Tramo) : Tramo :=
  if s.n % 2 = 0 then
    { n := s.n / 2,     A := s.A,     B := s.B + 1, C := s.C }
  else
    { n := 3 * s.n - 1, A := s.A + 1, B := s.B,     C := 3 * s.C + 2 ^ s.B }

def inicio (n0 : Nat) : Tramo := { n := n0, A := 0, B := 0, C := 0 }

def tramo (n0 : Nat) : Nat → Tramo
  | 0     => inicio n0
  | k + 1 => paso (tramo n0 k)

/-- LA FORMA CON RESTA TRUNCADA, como invariante de un estado cualquiera. -/
def invR (n0 : Nat) (s : Tramo) : Prop :=
  2 ^ s.B * s.n = 3 ^ s.A * n0 - s.C

/-- ¿Se conserva SOLA, sin arrastrar `C <= 3^A*n0`? -/
theorem pasoR (n0 : Nat) (s : Tramo) (h : invR n0 s) : invR n0 (paso s) := by
  unfold invR at h
  unfold invR paso
  by_cases hp : s.n % 2 = 0
  · rw [if_pos hp]
    show 2 ^ (s.B + 1) * (s.n / 2) = 3 ^ s.A * n0 - s.C
    have hn : s.n / 2 * 2 = s.n := Nat.div_mul_cancel (Nat.dvd_of_mod_eq_zero hp)
    have : 2 ^ (s.B + 1) * (s.n / 2) = 2 ^ s.B * s.n := by
      rw [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm 2 (s.n / 2), hn]
    rw [this]; exact h
  · rw [if_neg hp]
    show 2 ^ s.B * (3 * s.n - 1) = 3 ^ (s.A + 1) * n0 - (3 * s.C + 2 ^ s.B)
    -- s.n impar => s.n >= 1 => 2^B * s.n >= 2^B >= 1 => la resta de h NO trunca
    have hn1 : 1 ≤ s.n := by omega
    have hp2 : 1 ≤ 2 ^ s.B := Nat.one_le_two_pow
    have hge : 2 ^ s.B ≤ 2 ^ s.B * s.n := Nat.le_mul_of_pos_right _ (by omega)
    -- de h y de que el lado izquierdo es positivo sale C < 3^A*n0
    have hlt : s.C + 2 ^ s.B * s.n = 3 ^ s.A * n0 := by omega
    -- ahora todo es algebra sin truncamiento
    have e1 : 2 ^ s.B * (3 * s.n - 1) + 2 ^ s.B = 2 ^ s.B * (3 * s.n) := by
      have : 3 * s.n - 1 + 1 = 3 * s.n := by omega
      calc 2 ^ s.B * (3 * s.n - 1) + 2 ^ s.B
          = 2 ^ s.B * (3 * s.n - 1 + 1) := by rw [Nat.mul_add, Nat.mul_one]
        _ = 2 ^ s.B * (3 * s.n)         := by rw [this]
    have e2 : 2 ^ s.B * (3 * s.n) = 3 * (2 ^ s.B * s.n) := by
      rw [Nat.mul_left_comm]
    have e3 : 3 ^ (s.A + 1) * n0 = 3 * (3 ^ s.A * n0) := by
      rw [Nat.pow_succ, Nat.mul_comm (3 ^ s.A) 3, Nat.mul_assoc]
    omega

/-- Y por tanto la identidad restada, por induccion directa. -/
theorem identidadR (n0 k : Nat) : invR n0 (tramo n0 k) := by
  induction k with
  | zero      => show 2 ^ 0 * n0 = 3 ^ 0 * n0 - 0; simp
  | succ k ih => exact pasoR n0 (tramo n0 k) ih

#print axioms pasoR
#print axioms identidadR
