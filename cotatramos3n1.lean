/-
  LA COTA POR TRAMO DEL MAPA 3n-1, DEMOSTRADA EN LEAN 4.

  ================== QUE MAPA ES ESTE. LEER ANTES DE NADA ==================

  EL MAPA ES  3n-1,  Y NO ES COLLATZ:

      n par    ->  n / 2
      n impar  ->  3n - 1

  NO es el mapa clasico de Collatz (3n+1), que es el de `cotatramos.lean`.
  NO es el mapa del atajo ((3n+1)/2), donde el paso impar tambien divide y
  por tanto el B sale distinto. Este repo ya confundio esos tres mapas tres
  veces, asi que se escribe aqui arriba y en cada teorema.

  Sobre los naturales, 3n-1 es la imagen espejo de Collatz sobre los enteros
  negativos: si n = -m, un paso de Collatz sobre n es un paso de 3m-1 sobre m.
  Por eso este mapa tiene TRES ciclos (1, el de largo 5 y el de largo 18) y
  no uno solo, y por eso sirve como control A/B: una cantidad que no separe
  3n+1 de 3n-1 no puede decir nada sobre la convergencia de Collatz.

  Sobre un tramo que arranca en n0 y da k pasos:

      A = cuantas veces se aplico  3n-1   (los pasos impares)
      B = cuantas veces se aplico  n/2    (los pasos pares)
      C = la constante acumulada de la identidad (ver abajo)

  ======================= LA IDENTIDAD, Y COMO SALE =======================

  Se deriva imponiendo que sea invariante, sin copiarla de ningun sitio.
  Se busca un invariante de la forma  2^B * n  ~  3^A * n0  y se mira que le
  hace cada uno de los dos pasos:

    PASO PAR   n -> n/2, B -> B+1.  Entonces  2^(B+1) * (n/2) = 2^B * n.
               El miembro izquierdo NO SE MUEVE. Luego C tampoco se mueve.

    PASO IMPAR n -> 3n-1, A -> A+1.  Entonces
               2^B * (3n-1) = 3 * (2^B * n) - 2^B.
               El miembro derecho se multiplica por 3 (porque 3^(A+1) = 3*3^A),
               asi que sobra un DEFECTO de 2^B respecto de lo que deberia.
               Si antes el defecto era C, ahora es  3*C + 2^B.

  De ahi, con C arrancando en 0:

      REGLA DE C:   paso par   ->  C  se queda igual
                    paso impar ->  C  pasa a  3*C + 2^B     (B = el B de ANTES)

      IDENTIDAD:    2^B * n_k  +  C  =  3^A * n_0

  El SIGNO es la unica diferencia con Collatz, y lo es todo: en 3n+1 la
  constante SE SUMA al lado del n_k (2^B*n_k = 3^A*n0 + C) y en 3n-1 se resta,
  o lo que es lo mismo, se suma al OTRO lado. Ese cambio de lado es el que da
  la vuelta a la cota.

  ============================= LA COTA ==============================

      2^B * n_k  <=  3^A * n_0            (para todo n0 y todo k)

  Va AL REVES que en Collatz, donde vale  3^A*n0 <= 2^B*n_k.
  Y sale igual de gratis: C es un natural, luego C >= 0 por construccion.
  Ese "C >= 0" es exactamente el -1 del 3n-1, contado con el signo cambiado.

  ====================== LA PREGUNTA DE TIPO: Nat o Int ======================

  NO HIZO FALTA IRSE A `Int`. Todo el fichero vive en `Nat`.
  Se pone la C en el lado del n_k en vez de restarla, y asi no hay ninguna
  resta de naturales (que es truncada) en el invariante.

  PERO OJO, Y ES UNA CORRECCION AL PROPIO FICHERO (comparador, 01-08-2026): eso
  es una COMODIDAD, no una NECESIDAD. La forma restada "2^B*n_k = 3^A*n0 - C"
  TAMBIEN compila en `Nat` y su induccion cierra sola, sin invariante reforzado.
  Este fichero afirmaba lo contrario en el docstring de `C_no_se_pasa` y era
  falso. Lo que sigue siendo cierto es que la forma sin resta es mas limpia.

  Y LA CONSECUENCIA QUE IMPORTA, porque el CLAUDE.md llego a escribir lo
  contrario: la discriminacion del control A/B entre 3n+1 y 3n-1 NO aparece
  como un cambio de tipo forzoso. Aparece como el SIGNO de la C, la desigualdad
  invertida y el corolario que cambia de sentido -- las tres cosas cerradas con
  `decide` en la PARTE 2 de este fichero.

  Queda un segundo sitio donde `Nat` podria colarse: la propia definicion del
  paso impar escribe `3 * n - 1`, y en `Nat` eso es resta truncada (con n = 0
  daria 0 en vez de -1). NO es un problema, y no se deja como impresion: el
  teorema `impar_no_trunca` demuestra que la rama impar solo se dispara con
  n impar, luego n >= 1, luego 3n >= 3 y la resta nunca trunca.

  No usa Mathlib: solo el nucleo de Lean 4. Se comprueba con
      lean cotatramos3n1.lean
  y si no imprime ningun `error:`, esta demostrado.
-/

-- El desenrollado del ciclo de 18 pasos pasa del limite por defecto (512).
set_option maxRecDepth 40000

/-! ## PARTE 1 — el mapa 3n-1 y su identidad -/

/-- El estado de un tramo: donde estamos y la cuenta de A, B y C. -/
structure Tramo where
  n : Nat
  A : Nat
  B : Nat
  C : Nat

/-- Un paso del mapa **3n-1**, arrastrando las tres cuentas.
    Ojo: `3 * s.n - 1` es resta de `Nat`. Ver `impar_no_trunca`. -/
def paso (s : Tramo) : Tramo :=
  if s.n % 2 = 0 then
    { n := s.n / 2,     A := s.A,     B := s.B + 1, C := s.C }
  else
    { n := 3 * s.n - 1, A := s.A + 1, B := s.B,     C := 3 * s.C + 2 ^ s.B }

/-- El arranque: cero pasos dados, C = 0. -/
def inicio (n0 : Nat) : Tramo := { n := n0, A := 0, B := 0, C := 0 }

/-- El estado despues de k pasos saliendo de n0. -/
def tramo (n0 : Nat) : Nat → Tramo
  | 0     => inicio n0
  | k + 1 => paso (tramo n0 k)

/-- LA RESTA DE `Nat` NO TRUNCA NUNCA AQUI.

    La rama impar solo se ejecuta con `n` impar, y entonces `n >= 1`, luego
    `3n >= 3` y `3n - 1` es la resta de verdad. Esto es lo que impide que el
    fichero entero sea un teorema que se cumple por accidente de truncamiento. -/
theorem impar_no_trunca (s : Tramo) (hp : ¬ (s.n % 2 = 0)) :
    (paso s).n + 1 = 3 * s.n := by
  unfold paso
  rw [if_neg hp]
  show 3 * s.n - 1 + 1 = 3 * s.n
  omega

/-- La identidad escrita como invariante del estado, SIN NINGUNA RESTA. -/
def inv (n0 : Nat) (s : Tramo) : Prop :=
  2 ^ s.B * s.n + s.C = 3 ^ s.A * n0

/-- UN PASO CONSERVA LA IDENTIDAD. Aqui esta toda la aritmetica. -/
theorem paso_conserva (n0 : Nat) (s : Tramo) (h : inv n0 s) : inv n0 (paso s) := by
  unfold inv paso
  by_cases hp : s.n % 2 = 0
  · -- PASO PAR: n -> n/2, B sube uno, C no se mueve.
    rw [if_pos hp]
    show 2 ^ (s.B + 1) * (s.n / 2) + s.C = 3 ^ s.A * n0
    have hn : s.n / 2 * 2 = s.n := Nat.div_mul_cancel (Nat.dvd_of_mod_eq_zero hp)
    calc 2 ^ (s.B + 1) * (s.n / 2) + s.C
        = 2 ^ s.B * (s.n / 2 * 2) + s.C := by
            rw [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm 2 (s.n / 2)]
      _ = 2 ^ s.B * s.n + s.C           := by rw [hn]
      _ = 3 ^ s.A * n0                  := h
  · -- PASO IMPAR: n -> 3n-1, A sube uno, C -> 3C + 2^B.
    rw [if_neg hp]
    show 2 ^ s.B * (3 * s.n - 1) + (3 * s.C + 2 ^ s.B) = 3 ^ (s.A + 1) * n0
    -- La unica vez que se toca la resta: se cancela contra el 2^B que sobra.
    have h1 : 1 ≤ 3 * s.n := by omega
    have hsub : 3 * s.n - 1 + 1 = 3 * s.n := Nat.sub_add_cancel h1
    calc 2 ^ s.B * (3 * s.n - 1) + (3 * s.C + 2 ^ s.B)
        = 2 ^ s.B * (3 * s.n - 1) + 2 ^ s.B + 3 * s.C := by omega
      _ = 2 ^ s.B * (3 * s.n - 1 + 1) + 3 * s.C       := by
            rw [Nat.mul_add, Nat.mul_one]
      _ = 2 ^ s.B * (3 * s.n) + 3 * s.C               := by rw [hsub]
      _ = 3 * (2 ^ s.B * s.n) + 3 * s.C               := by rw [Nat.mul_left_comm]
      _ = 3 * (2 ^ s.B * s.n + s.C)                   := by rw [Nat.mul_add]
      _ = 3 * (3 ^ s.A * n0)                          := by rw [h]
      _ = 3 ^ (s.A + 1) * n0                          := by
            rw [Nat.pow_succ, Nat.mul_comm (3 ^ s.A) 3, Nat.mul_assoc]

/-- **(I) LA IDENTIDAD**, para todo n0 y todo k, sobre el mapa 3n-1:
        2^B * n_k + C = 3^A * n_0 -/
theorem identidad (n0 k : Nat) :
    2 ^ (tramo n0 k).B * (tramo n0 k).n + (tramo n0 k).C
      = 3 ^ (tramo n0 k).A * n0 := by
  induction k with
  | zero      => show 2 ^ 0 * n0 + 0 = 3 ^ 0 * n0; simp
  | succ k ih => exact paso_conserva n0 (tramo n0 k) ih

/-- La misma identidad escrita CON la resta truncada de `Nat`, para dejar
    constancia de que la version restada tambien es cierta —y de que es un
    corolario de la de arriba, no al reves. La forma sin resta es la que
    sostiene todo; esta es solo la traduccion. -/
theorem identidad_con_resta (n0 k : Nat) :
    3 ^ (tramo n0 k).A * n0 - (tramo n0 k).C
      = 2 ^ (tramo n0 k).B * (tramo n0 k).n := by
  have h := identidad n0 k
  omega

/-- LA C NUNCA SE PASA:  C <= 3^A * n_0.

    Poniendo la C en el lado del n_k, este hecho sale GRATIS como corolario de
    la identidad, en una linea, en vez de haber que cargarlo.

    CORRECCION DEL COMPARADOR (01-08-2026). Este docstring decia que con la
    forma restada —"2^B*n_k = 3^A*n0 - C"— la induccion NO SE SOSTIENE SOLA en
    `Nat`, y que habria que arrastrar este `C <= 3^A*n0` como segunda mitad del
    invariante. ESO ES FALSO, y no se discutio: el comparador escribio el
    `paso_conserva` de la forma restada sobre estado arbitrario, SIN invariante
    reforzado, y COMPILA (`#print axioms` limpio). En la rama impar el propio
    invariante ya fuerza `2^B*n_k >= 1`, y de ahi sale la no-truncacion — que es
    el mismo hecho que `impar_no_trunca` necesitaba de todas formas. Cuesta
    cuatro lineas mas.

    O sea: poner la C al otro lado es MAS COMODO, no NECESARIO. La conclusion
    de este fichero -que no hace falta `Int`- queda reforzada; lo que estaba mal
    era la razon que se daba. Ver `prueba_resta.lean`, que es la compilacion que
    lo decide. -/
theorem C_no_se_pasa (n0 k : Nat) :
    (tramo n0 k).C ≤ 3 ^ (tramo n0 k).A * n0 := by
  have h := identidad n0 k
  omega

/-- **(II) LA COTA**, y va al reves que en Collatz:
        2^B * n_k  <=  3^A * n_0
    Sale de la identidad sin trabajo: C es un `Nat`, luego C >= 0. -/
theorem cota (n0 k : Nat) :
    2 ^ (tramo n0 k).B * (tramo n0 k).n ≤ 3 ^ (tramo n0 k).A * n0 := by
  have h := identidad n0 k
  omega

/-- **(III) EL COROLARIO ESPEJO**: si el tramo SUBE (n_k > n0), entonces
        2^B < 3^A.

    SIN HIPOTESIS EXTRA. No hace falta pedir `0 < n0` ni `n0` impar: sobre los
    naturales, "el tramo sube" ya obliga a que n_k sea positivo, y el argumento
    solo necesita `2^B > 0`, que es cierto siempre. Lo comprueba Lean: la
    demostracion cierra sin ninguna hipotesis mas. -/
theorem corolario (n0 k : Nat) (hsube : n0 < (tramo n0 k).n) :
    2 ^ (tramo n0 k).B < 3 ^ (tramo n0 k).A := by
  have hc := cota n0 k
  cases Nat.lt_or_ge (2 ^ (tramo n0 k).B) (3 ^ (tramo n0 k).A) with
  | inl h => exact h
  | inr h =>
      -- Suponer 3^A <= 2^B lleva a 3^A * n0 < 3^A * n0, que es absurdo.
      exfalso
      have hpos : 0 < 2 ^ (tramo n0 k).B := Nat.two_pow_pos _
      have h1 : 3 ^ (tramo n0 k).A * n0 ≤ 2 ^ (tramo n0 k).B * n0 :=
        Nat.mul_le_mul h (Nat.le_refl _)
      have h2 : 2 ^ (tramo n0 k).B * n0
              < 2 ^ (tramo n0 k).B * (tramo n0 k).n :=
        (Nat.mul_lt_mul_left hpos).mpr hsube
      have h3 : 3 ^ (tramo n0 k).A * n0
              < 2 ^ (tramo n0 k).B * (tramo n0 k).n :=
        Nat.lt_of_le_of_lt h1 h2
      exact Nat.lt_irrefl _ (Nat.lt_of_le_of_lt hc h3)

/-- EL COROLARIO NO ES VACUO, y conviene demostrarlo: un teorema con una
    hipotesis que nunca se cumple es cierto y no dice nada. Hay tramos que
    suben (el 1 sube a 2 en un paso), y ahi el corolario se instancia. -/
theorem corolario_no_es_vacuo :
    2 ^ (tramo 1 1).B < 3 ^ (tramo 1 1).A :=
  corolario 1 1 (by decide)

/-! ## PARTE 2 — (IV) LA DISCRIMINACION: el control A/B del repo

  Una cota que valiera para los dos mapas no mediria nada. Aqui se define
  ADEMAS el mapa clasico 3n+1, con las mismas cuentas, y se demuestra que
  cada cota es FALSA sobre el otro mapa. Las dos falsedades se cierran con
  `decide`, o sea que las comprueba el nucleo sobre un caso concreto.
-/

/-- Un paso del mapa **clasico 3n+1** (el de `cotatramos.lean`), para poder
    contrastar. Aqui no hay ninguna resta. -/
def pasoMas (s : Tramo) : Tramo :=
  if s.n % 2 = 0 then
    { n := s.n / 2,     A := s.A,     B := s.B + 1, C := s.C }
  else
    { n := 3 * s.n + 1, A := s.A + 1, B := s.B,     C := 3 * s.C + 2 ^ s.B }

/-- k pasos del mapa clasico 3n+1 saliendo de n0. -/
def tramoMas (n0 : Nat) : Nat → Tramo
  | 0     => inicio n0
  | k + 1 => pasoMas (tramoMas n0 k)

/-- **(IV.a) LA COTA DE 3n-1 ES FALSA PARA 3n+1.**

    Contraejemplo: n0 = 1, un solo paso. El 1 es impar, luego 1 -> 4, con
    A = 1 y B = 0. La cota pediria  2^0 * 4 <= 3^1 * 1,  o sea  4 <= 3. -/
theorem cota_3n1_falla_en_el_mapa_clasico :
    ¬ (∀ n0 k : Nat,
        2 ^ (tramoMas n0 k).B * (tramoMas n0 k).n ≤ 3 ^ (tramoMas n0 k).A * n0) := by
  intro h
  exact absurd (h 1 1) (by decide)

/-- **(IV.b) LA COTA DE `cotatramos.lean` (3n+1) ES FALSA PARA 3n-1.**

    Contraejemplo: n0 = 1, un solo paso. El 1 es impar, luego 1 -> 2, con
    A = 1 y B = 0. Esa cota pediria  3^1 * 1 <= 2^0 * 2,  o sea  3 <= 2. -/
theorem cota_clasica_falla_en_el_mapa_3n1 :
    ¬ (∀ n0 k : Nat,
        3 ^ (tramo n0 k).A * n0 ≤ 2 ^ (tramo n0 k).B * (tramo n0 k).n) := by
  intro h
  exact absurd (h 1 1) (by decide)

/-- Y la identidad tambien discrimina, no solo la cota: sobre 3n+1 la C
    acumulada de este fichero NO cierra la identidad del mapa 3n-1.
    Con n0 = 1 y un paso: 2^0*4 + 1 = 5, y 3^1*1 = 3. -/
theorem identidad_3n1_falla_en_el_mapa_clasico :
    ¬ (∀ n0 k : Nat,
        2 ^ (tramoMas n0 k).B * (tramoMas n0 k).n + (tramoMas n0 k).C
          = 3 ^ (tramoMas n0 k).A * n0) := by
  intro h
  exact absurd (h 1 1) (by decide)

/-- Y LOS DOS CONTRAEJEMPLOS NO SON UN ARTEFACTO DE NUMEROS CHICOS.
    El mismo choque con n0 = 27, que es el numero grande de referencia del repo:
      3n+1:  27 -> 82,  y  2^0*82 <= 3^1*27  pediria  82 <= 81.
      3n-1:  27 -> 80,  y  3^1*27 <= 2^0*80  pediria  81 <= 80.
    Las dos desigualdades fallan por UNO, que es exactamente el +1 y el -1. -/
theorem contraejemplo_27_clasico :
    ¬ (2 ^ (tramoMas 27 1).B * (tramoMas 27 1).n ≤ 3 ^ (tramoMas 27 1).A * 27) := by
  decide

theorem contraejemplo_27_menos :
    ¬ (3 ^ (tramo 27 1).A * 27 ≤ 2 ^ (tramo 27 1).B * (tramo 27 1).n) := by
  decide

/-! ## PARTE 3 — los axiomas de los que depende cada teorema

  Si en alguna linea apareciera `sorryAx`, habria un agujero tapado y el
  fichero entero no valdria. Tienen que salir SOLO los tres axiomas estandar
  de Lean (propext, Classical.choice, Quot.sound) -- o menos.
-/
#print axioms impar_no_trunca
#print axioms paso_conserva
#print axioms identidad
#print axioms identidad_con_resta
#print axioms C_no_se_pasa
#print axioms cota
#print axioms corolario
#print axioms corolario_no_es_vacuo
#print axioms contraejemplo_27_clasico
#print axioms contraejemplo_27_menos
#print axioms cota_3n1_falla_en_el_mapa_clasico
#print axioms cota_clasica_falla_en_el_mapa_3n1
#print axioms identidad_3n1_falla_en_el_mapa_clasico

/-! ## PARTE 4 — LOS CASOS CONOCIDOS, COMPROBADOS POR EL NUCLEO

  Lean garantiza que la demostracion corresponde al enunciado. NO garantiza
  que el enunciado hable del objeto que uno cree. Si `paso` no fuera 3n-1 de
  verdad, todo lo de arriba seria un teorema impecable sobre otra cosa.

  El repo tiene medido que 3n-1 sobre los positivos tiene TRES ciclos, que son
  el espejo de los tres ciclos de Collatz sobre los negativos:

      [-1, -2]                  ->  1 -> 2 -> 1        (largo 2,  A=1, B=1)
      [-5,-14,-7,-20,-10]       ->  5 -> ... -> 5      (largo 5,  A=2, B=3)
      [-17, ... , -34]          ->  17 -> ... -> 17    (largo 18, A=7, B=11)

  Y los tres B/A -- 1/1, 3/2, 11/7 -- son los tres convergentes de la fraccion
  continua de log2(3) por DEBAJO, que es justo el lado que el barrido (A,B) de
  Collatz descarta. Eso es lo que aqui se comprueba.

  Va con `decide` y NO con `#eval`: `#eval` lo calcula el compilador y su
  resultado no lo revisa nadie; un `decide` lo revisa el nucleo, que es lo
  unico en lo que se apoya la confianza de todo lo de arriba.
-/

-- El ciclo trivial: 1 -> 2 -> 1.
theorem ciclo1_vuelve      : (tramo 1 2).n = 1 := by decide
theorem ciclo1_tiene_A_1   : (tramo 1 2).A = 1 := by decide
theorem ciclo1_tiene_B_1   : (tramo 1 2).B = 1 := by decide

-- El ciclo de largo 5: 5 -> 14 -> 7 -> 20 -> 10 -> 5.
theorem ciclo5_vuelve      : (tramo 5 5).n = 5 := by decide
theorem ciclo5_tiene_A_2   : (tramo 5 5).A = 2 := by decide
theorem ciclo5_tiene_B_3   : (tramo 5 5).B = 3 := by decide

-- El ciclo de largo 18: 17 -> 50 -> 25 -> ... -> 34 -> 17.
theorem ciclo18_vuelve     : (tramo 17 18).n = 17 := by decide
theorem ciclo18_tiene_A_7  : (tramo 17 18).A = 7  := by decide
theorem ciclo18_tiene_B_11 : (tramo 17 18).B = 11 := by decide

/-- Y LA IDENTIDAD CRUZADA A MANO SOBRE EL CICLO DE 18, comprobada por el
    nucleo: 2^11 * 17 + C = 3^7 * 17, o sea 34816 + 2363 = 37179. -/
theorem ciclo18_tiene_C_2363 : (tramo 17 18).C = 2363 := by decide

theorem ciclo18_cuadra_la_identidad :
    2 ^ (tramo 17 18).B * (tramo 17 18).n + (tramo 17 18).C
      = 3 ^ (tramo 17 18).A * 17 := by decide

/-- Y la cota, en ese mismo ciclo, es ESTRICTA: 34816 < 37179.
    En un ciclo del mapa 3n-1 se tiene 2^B < 3^A, que es el corolario de
    arriba aplicado al caso de igualdad n_k = n0 -- y por eso los tres B/A
    caen por DEBAJO de log2(3). -/
theorem ciclo18_cota_estricta :
    2 ^ (tramo 17 18).B * (tramo 17 18).n < 3 ^ (tramo 17 18).A * 17 := by decide

#print axioms ciclo18_cuadra_la_identidad
#print axioms ciclo18_cota_estricta
