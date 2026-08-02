/-
  a(k) NO DISTINGUE 3n+1 DE 3n-1, Y ES UN TEOREMA. DEMOSTRADO EN LEAN 4.

  EL ENUNCIADO. Con el mapa del ATAJO:

      Tmas   n  =  n/2  si n par ,  (3n+1)/2  si n impar
      Tmenos n  =  n/2  si n par ,  (3n-1)/2  si n impar

  Para un k y un resto r en {0, ..., 2^k - 1}, con S_k(r) = cuantos de los k
  primeros pasos son impares, se dice que r ES BUENO si

      S_k(r) = S_k(r+1)      y      T^k(r) = T^k(r+1)

  y a(k) = cuantos restos son buenos. La afirmacion a decidir era

      amas(k) = amenos(k)   para todo k >= 1

  y la pregunta que de verdad importaba: TEOREMA o COINCIDENCIA NUMERICA.

  VEREDICTO: TEOREMA. Y la razon es de una linea:

      EL MAPA DE 3n-1 ES EL DE 3n+1 VISTO EN EL ESPEJO DEL CERO.

      Tmenos(-n) = -(Tmas n)      para todo entero n

  (n par: -n/2 = -(n/2). n impar: (3(-n)-1)/2 = -(3n+1)/2.)

  De ahi sale todo. El espejo manda el par (r, r+1) al par (-(r+1), -r), o sea
  que le da la vuelta al orden; y como la propiedad de ser bueno es periodica de
  periodo 2^k (identidad de Terras), ese par vuelve a caer dentro del bloque
  {0, ..., 2^k - 1} en la posicion 2^k - 1 - r. La biyeccion es LA REFLEXION:

      r es bueno para Tmas   <=>   2^k - 1 - r es bueno para Tmenos

  Contar los buenos de un lado es contar los del otro al reves. Por eso las dos
  sucesiones coinciden termino a termino, y por eso NO se pueden romper en
  ningun k grande: no hay nada que medir, hay una simetria.

  LO QUE ESTO DECIDE, Y CIERRA UN PENDIENTE. No hace falta gastar CPU llegando a
  k >= 20 para ver si la igualdad aguanta. Aguanta para todo k.

  Y CONFIRMA LA RETIRADA DEL BORRADOR A OEIS, con un argumento mas fuerte que el
  que se tenia. No es que a(k) "resulte no distinguir" los dos mapas: es que a(k)
  es un invariante de la conjugacion n -> -n, y los ciclos NO lo son (3n+1 tiene
  uno sobre los positivos, 3n-1 tiene tres). Una cantidad invariante bajo una
  simetria no puede ser evidencia sobre algo que la simetria no respeta.

  No usa Mathlib: solo el nucleo de Lean 4. Se comprueba con
      lean espejoak.lean
  y si no imprime ningun "error:", esta demostrado.
-/

/- ------------------------------------------------------------------------ -/
/- LOS DOS MAPAS, sobre los enteros. Sobre Z y no sobre N a proposito: el
   espejo del cero es lo que hace toda la demostracion, y necesita negativos. -/

/-- El atajo de 3n+1. -/
def Tmas (n : Int) : Int := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- El atajo de 3n-1. -/
def Tmenos (n : Int) : Int := if n % 2 = 0 then n / 2 else (3 * n - 1) / 2

/-- Donde esta n despues de k pasos de Tmas. -/
def itM : Nat → Int → Int
  | 0,     n => n
  | k + 1, n => itM k (Tmas n)

/-- Donde esta n despues de k pasos de Tmenos. -/
def itN : Nat → Int → Int
  | 0,     n => n
  | k + 1, n => itN k (Tmenos n)

/-- S_k(n) para Tmas: cuantos de los k primeros pasos salen de un impar. -/
def sM : Nat → Int → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 0 else 1) + sM k (Tmas n)

/-- S_k(n) para Tmenos. -/
def sN : Nat → Int → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 0 else 1) + sN k (Tmenos n)

/- ------------------------------------------------------------------------ -/
/- PARTE 1 -- EL ESPEJO DEL CERO. Aqui esta toda la idea; el resto es arrastre. -/

/-- UN PASO: dar un paso de 3n-1 sobre -n es dar un paso de 3n+1 sobre n y
    cambiar el signo. Los dos casos salen de la aritmetica entera exacta, y
    ninguna de las dos divisiones redondea: si n es par, 2 divide a n; si n es
    impar, 3n+1 es par y 3(-n)-1 = -(3n+1) tambien. -/
theorem paso_conj (n : Int) : Tmenos (-n) = -(Tmas n) := by
  unfold Tmenos Tmas
  by_cases h : n % 2 = 0
  · rw [if_pos h, if_pos (show (-n) % 2 = 0 by omega)]
    omega
  · rw [if_neg h, if_neg (show ¬ ((-n) % 2 = 0) by omega)]
    omega

/-- k PASOS: el espejo sobrevive a la iteracion. -/
theorem conj_it (k : Nat) : ∀ n : Int, itN k (-n) = -(itM k n) := by
  induction k with
  | zero => intro n; rfl
  | succ k ih =>
      intro n
      show itN k (Tmenos (-n)) = -(itM k (Tmas n))
      rw [paso_conj n, ih (Tmas n)]

/-- Y la cuenta de pasos impares no la toca: -n es impar exactamente cuando lo
    es n, asi que los dos mapas gastan el mismo S_k. -/
theorem conj_s (k : Nat) : ∀ n : Int, sN k (-n) = sM k n := by
  induction k with
  | zero => intro n; rfl
  | succ k ih =>
      intro n
      show (if (-n) % 2 = 0 then 0 else 1) + sN k (Tmenos (-n))
         = (if n % 2 = 0 then 0 else 1) + sM k (Tmas n)
      rw [paso_conj n, ih (Tmas n)]
      by_cases h : n % 2 = 0
      · rw [if_pos h, if_pos (show (-n) % 2 = 0 by omega)]
      · rw [if_neg h, if_neg (show ¬ ((-n) % 2 = 0) by omega)]

/- ------------------------------------------------------------------------ -/
/- PARTE 2 -- LA IDENTIDAD DE TERRAS (1976, Teoremas 1.1 y 1.2), demostrada.

   T^k(n + 2^k * m) = 3^{S_k(n)} * m + T^k(n)   y   S_k(n + 2^k * m) = S_k(n)

   Es la recta en m que el repo ya tenia escrita en `sucesiones.txt` y medida en
   `clasesfusion.py`. Aqui vale para TODO k, TODO n y TODO m, incluidos los
   negativos -- que es justo lo que hace falta para traer el par reflejado de
   vuelta dentro del bloque. -/

/-- Un paso par absorbe un desplazamiento de 2X como un desplazamiento de X. -/
theorem paso_par (n X : Int) (h : n % 2 = 0) : Tmas (n + 2 * X) = Tmas n + X := by
  unfold Tmas
  rw [if_pos h, if_pos (show (n + 2 * X) % 2 = 0 by omega)]
  omega

/-- Un paso impar lo absorbe como 3X. Ese 3 es el que se acumula en 3^{S_k}. -/
theorem paso_imp (n X : Int) (h : ¬ (n % 2 = 0)) :
    Tmas (n + 2 * X) = Tmas n + 3 * X := by
  unfold Tmas
  rw [if_neg h, if_neg (show ¬ ((n + 2 * X) % 2 = 0) by omega)]
  omega

/- Tres reescrituras de puro algebra. Sin Mathlib no hay `ring`, asi que van a
   mano con conmutar y asociar. -/
theorem desdoble (k : Nat) (m : Int) : (2:Int)^(k+1) * m = 2 * ((2:Int)^k * m) := by
  rw [Int.pow_succ, Int.mul_comm ((2:Int)^k) 2, Int.mul_assoc]

theorem tresmueve (k : Nat) (m : Int) : (3:Int) * ((2:Int)^k * m) = (2:Int)^k * (3*m) := by
  rw [← Int.mul_assoc, Int.mul_comm 3 ((2:Int)^k), Int.mul_assoc]

theorem potuno (s : Nat) (m : Int) : (3:Int)^(1+s) * m = (3:Int)^s * (3*m) := by
  rw [Nat.add_comm, Int.pow_succ, Int.mul_assoc]

/-- LA IDENTIDAD DE TERRAS. Las dos mitades a la vez, porque la induccion las
    necesita juntas: el exponente de la segunda es la primera. -/
theorem terras (k : Nat) : ∀ n m : Int,
    sM k (n + 2^k * m) = sM k n ∧
    itM k (n + 2^k * m) = 3^(sM k n) * m + itM k n := by
  induction k with
  | zero =>
      intro n m
      refine ⟨rfl, ?_⟩
      show n + 2^0 * m = 3^0 * m + n
      omega
  | succ k ih =>
      intro n m
      have hp : (2:Int)^(k+1) * m = 2 * ((2:Int)^k * m) := desdoble k m
      by_cases h : n % 2 = 0
      · -- PASO PAR: el desplazamiento se parte por la mitad y m no cambia.
        have hq : (n + (2:Int)^(k+1) * m) % 2 = 0 := by rw [hp]; omega
        have hs : Tmas (n + (2:Int)^(k+1) * m) = Tmas n + 2^k * m := by
          rw [hp]; exact paso_par n _ h
        have i1 := (ih (Tmas n) m).1
        have i2 := (ih (Tmas n) m).2
        constructor
        · show (if (n + (2:Int)^(k+1)*m) % 2 = 0 then 0 else 1)
                 + sM k (Tmas (n + 2^(k+1)*m))
             = (if n % 2 = 0 then 0 else 1) + sM k (Tmas n)
          rw [if_pos hq, if_pos h, hs, i1]
        · show itM k (Tmas (n + (2:Int)^(k+1)*m))
             = 3 ^ ((if n % 2 = 0 then 0 else 1) + sM k (Tmas n)) * m + itM k (Tmas n)
          rw [if_pos h, hs, i2, Nat.zero_add]
      · -- PASO IMPAR: el desplazamiento se parte por la mitad y m se triplica.
        have hq : ¬ ((n + (2:Int)^(k+1) * m) % 2 = 0) := by rw [hp]; omega
        have hs : Tmas (n + (2:Int)^(k+1) * m) = Tmas n + 2^k * (3*m) := by
          rw [hp, paso_imp n _ h, tresmueve k m]
        have i1 := (ih (Tmas n) (3*m)).1
        have i2 := (ih (Tmas n) (3*m)).2
        constructor
        · show (if (n + (2:Int)^(k+1)*m) % 2 = 0 then 0 else 1)
                 + sM k (Tmas (n + 2^(k+1)*m))
             = (if n % 2 = 0 then 0 else 1) + sM k (Tmas n)
          rw [if_neg hq, if_neg h, hs, i1]
        · show itM k (Tmas (n + (2:Int)^(k+1)*m))
             = 3 ^ ((if n % 2 = 0 then 0 else 1) + sM k (Tmas n)) * m + itM k (Tmas n)
          rw [if_neg h, hs, i2, potuno]

/- ------------------------------------------------------------------------ -/
/- PARTE 3 -- SER BUENO, Y QUE EL CASO DE BORDE NO ES UN CASO APARTE. -/

/-- r es bueno si el, y el entero de al lado, gastan el mismo numero de pasos
    impares y aterrizan en el mismo sitio. OJO: el vecino es el ENTERO r+1, sin
    reducir modulo nada. Para r = 2^k - 1 eso da el entero 2^k, y el teorema
    `borde` de aqui abajo demuestra que eso es exactamente la condicion de borde
    del enunciado. -/
def buenoM (k : Nat) (r : Int) : Bool :=
  decide (sM k r = sM k (r+1) ∧ itM k r = itM k (r+1))

def buenoN (k : Nat) (r : Int) : Bool :=
  decide (sN k r = sN k (r+1) ∧ itN k r = itN k (r+1))

/-- EL CASO DE BORDE, DEMOSTRADO. El enunciado pedia aparte, para r = 2^k - 1,
        S_k(2^k - 1) = S_k(0)   y   T^k(2^k - 1) = 3^{S_k(0)} + T^k(0).
    Aqui se ve que no hay que pedirlo: usar el entero 2^k como vecino ya lo da,
    porque T^k(2^k) = 3^{S_k(0)} + T^k(0) por Terras con n = 0 y m = 1. Sin este
    teorema la formalizacion estaria hablando de otro objeto. -/
theorem borde (k : Nat) :
    sM k ((2:Int)^k) = sM k 0 ∧ itM k ((2:Int)^k) = 3^(sM k 0) + itM k 0 := by
  have h := terras k 0 1
  have e : (0:Int) + 2^k * 1 = 2^k := by omega
  rw [e] at h
  refine ⟨h.1, ?_⟩
  have h2 := h.2
  rw [Int.mul_one] at h2
  exact h2

/-- SER BUENO ES PERIODICO DE PERIODO 2^k. Es lo que permite devolver el par
    reflejado, que cae en los negativos, al bloque {0, ..., 2^k - 1}. -/
theorem periodico (k : Nat) (n : Int) : buenoM k (n + 2^k) = buenoM k n := by
  unfold buenoM
  apply decide_eq_decide.mpr
  have e : n + (2:Int)^k + 1 = (n+1) + 2^k := by omega
  have hA := terras k n 1
  have hB := terras k (n+1) 1
  have z1 : n + (2:Int)^k * 1 = n + 2^k := by omega
  have z2 : (n+1) + (2:Int)^k * 1 = (n+1) + 2^k := by omega
  rw [z1] at hA
  rw [z2] at hB
  have hA1 := hA.1
  have hA2 := hA.2
  have hB1 := hB.1
  have hB2 := hB.2
  rw [Int.mul_one] at hA2 hB2
  rw [e, hA1, hB1, hA2, hB2]
  refine ⟨fun h => ?_, fun h => ?_⟩
  · have h1 := h.1
    have h2 := h.2
    rw [h1] at h2
    exact ⟨h1, by omega⟩
  · exact ⟨h.1, by rw [h.1, h.2]⟩

/-- LA CONJUGACION AL NIVEL DEL PREDICADO: ser bueno para 3n-1 en s es ser bueno
    para 3n+1 en -(s+1). El espejo del cero le da la vuelta al par: manda
    (s, s+1) a (-(s+1), -s), que es el par que arranca en -(s+1). -/
theorem conj_bueno (k : Nat) (s : Int) : buenoN k s = buenoM k (-(s+1)) := by
  unfold buenoN buenoM
  apply decide_eq_decide.mpr
  have e1 : sN k s = sM k (-s) := by
    have h := conj_s k (-s); rw [Int.neg_neg] at h; exact h
  have e2 : sN k (s+1) = sM k (-(s+1)) := by
    have h := conj_s k (-(s+1)); rw [Int.neg_neg] at h; exact h
  have e3 : itN k s = -(itM k (-s)) := by
    have h := conj_it k (-s); rw [Int.neg_neg] at h; exact h
  have e4 : itN k (s+1) = -(itM k (-(s+1))) := by
    have h := conj_it k (-(s+1)); rw [Int.neg_neg] at h; exact h
  have e5 : -(s+1) + 1 = -s := by omega
  rw [e1, e2, e3, e4, e5]
  refine ⟨fun h => ⟨h.1.symm, ?_⟩, fun h => ⟨h.1.symm, ?_⟩⟩
  · have := h.2; omega
  · have := h.2; omega

/-- LA BIYECCION, que es el corazon de todo:
        r es bueno para 3n-1   <=>   2^k - 1 - r es bueno para 3n+1.
    Sale de juntar el espejo (par reflejado, en los negativos) con la
    periodicidad (traerlo de vuelta al bloque sumando 2^k). -/
theorem reflexion (k : Nat) (s : Int) : buenoN k s = buenoM k ((2:Int)^k - 1 - s) := by
  rw [conj_bueno k s]
  have e : (2:Int)^k - 1 - s = -(s+1) + 2^k := by omega
  rw [e, periodico k (-(s+1))]

/- ------------------------------------------------------------------------ -/
/- PARTE 4 -- CONTAR. Contar los buenos de un bloque al derecho es contarlos al
   reves, y eso es un hecho de listas que no sabe nada de Collatz. -/

/-- Cuantos de los j enteros b, b+1, ..., b+j-1 cumplen p. -/
def cuenta (p : Int → Bool) : Nat → Int → Nat
  | 0,     _ => 0
  | j + 1, b => (if p b then 1 else 0) + cuenta p j (b + 1)

/-- Pelar por el final en vez de por el principio. -/
theorem cuenta_fin (p : Int → Bool) (j : Nat) : ∀ b : Int,
    cuenta p (j+1) b = cuenta p j b + (if p (b + (j:Int)) then 1 else 0) := by
  induction j with
  | zero =>
      intro b
      have hb : b + ((0:Nat):Int) = b := by omega
      show (if p b then 1 else 0) + cuenta p 0 (b+1)
         = cuenta p 0 b + (if p (b + ((0:Nat):Int)) then 1 else 0)
      rw [hb]
      show (if p b then 1 else 0) + 0 = 0 + (if p b then 1 else 0)
      rw [Nat.add_zero, Nat.zero_add]
  | succ j ih =>
      intro b
      have hb : b + 1 + (j:Int) = b + ((j+1 : Nat) : Int) := by omega
      show (if p b then 1 else 0) + cuenta p (j+1) (b+1)
         = ((if p b then 1 else 0) + cuenta p j (b+1))
           + (if p (b + ((j+1:Nat):Int)) then 1 else 0)
      rw [ih (b+1), ← Nat.add_assoc, hb]

/-- CONTAR AL REVES DA LO MISMO. Contar los x del tramo que cumplen p(c - x) es
    contar los del tramo reflejado que cumplen p. Puro conteo, cero Collatz. -/
theorem cuenta_refl (p : Int → Bool) (c : Int) (j : Nat) : ∀ b : Int,
    cuenta (fun x => p (c - x)) j b = cuenta p j (c - b - (j:Int) + 1) := by
  induction j with
  | zero => intro b; rfl
  | succ j ih =>
      intro b
      have e1 : c - (b+1) - (j:Int) + 1 = c - b - (j:Int) := by omega
      have e2 : c - b - ((j+1:Nat):Int) + 1 = c - b - (j:Int) := by omega
      have e3 : (c - b - (j:Int)) + (j:Int) = c - b := by omega
      show (if p (c - b) then 1 else 0) + cuenta (fun x => p (c - x)) j (b+1)
         = cuenta p (j+1) (c - b - ((j+1:Nat):Int) + 1)
      rw [ih (b+1), e1, e2, cuenta_fin p j (c - b - (j:Int)), e3]
      exact Nat.add_comm _ _

/- ------------------------------------------------------------------------ -/
/- PARTE 5 -- LAS DOS SUCESIONES, Y EL TEOREMA. -/

/-- a(k) del repo: cuantos restos de {0, ..., 2^k - 1} se funden con 3n+1. -/
def amas (k : Nat) : Nat := cuenta (buenoM k) (2^k) 0

/-- Lo mismo con 3n-1. -/
def amenos (k : Nat) : Nat := cuenta (buenoN k) (2^k) 0

/-- EL TEOREMA. Para TODO k, no para los k que se hayan medido.
    No es una coincidencia numerica: es la reflexion r -> 2^k - 1 - r. -/
theorem espejo (k : Nat) : amenos k = amas k := by
  unfold amenos amas
  have hf : buenoN k = fun x => buenoM k ((2:Int)^k - 1 - x) := by
    funext s; exact reflexion k s
  rw [hf, cuenta_refl (buenoM k) ((2:Int)^k - 1) (2^k) 0]
  have hdos : ((2:Nat) : Int) = 2 := rfl
  have hc : ((2:Int)^k - 1) - 0 - ((2^k : Nat) : Int) + 1 = 0 := by
    rw [Int.natCast_pow, hdos]; omega
  rw [hc]

/- ------------------------------------------------------------------------ -/
/- PARTE 6 -- LOS DOS CONTROLES QUE LEAN NO PUEDE HACER SOLO.

   Lean garantiza que la demostracion corresponde al ENUNCIADO, no que el
   enunciado hable del objeto que uno cree. Si `Tmas` no fuera el atajo de
   Collatz, todo lo de arriba seria un teorema impecable sobre otra cosa. Por eso
   van (a) el cruce contra los numeros que el repo ya tiene medidos y (b) una
   segunda implementacion que no comparte ni una linea con la de arriba. -/

/- (b) LA SEGUNDA IMPLEMENTACION. Todo distinto a proposito: va sobre Nat en vez
   de sobre Int, cuenta con List.range/filter/length en vez de con `cuenta`, y
   escribe el CASO DE BORDE LITERAL del enunciado en vez de usar el entero 2^k.
   Si las dos dan lo mismo, el borde esta bien tratado y la traduccion tambien. -/

def pasoNat (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
def pasoNatM (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n - 1) / 2

def iterNat : Nat → Nat → Nat
  | 0,     n => n
  | k + 1, n => iterNat k (pasoNat n)
def iterNatM : Nat → Nat → Nat
  | 0,     n => n
  | k + 1, n => iterNatM k (pasoNatM n)

def sNat : Nat → Nat → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 0 else 1) + sNat k (pasoNat n)
def sNatM : Nat → Nat → Nat
  | 0,     _ => 0
  | k + 1, n => (if n % 2 = 0 then 0 else 1) + sNatM k (pasoNatM n)

/-- El criterio con el borde ESCRITO COMO EN EL ENUNCIADO. -/
def buenoLitMas (k r : Nat) : Bool :=
  if r + 1 = 2^k then
    (sNat k r == sNat k 0) && (iterNat k r == 3^(sNat k 0) + iterNat k 0)
  else
    (sNat k r == sNat k (r+1)) && (iterNat k r == iterNat k (r+1))

def buenoLitMenos (k r : Nat) : Bool :=
  if r + 1 = 2^k then
    (sNatM k r == sNatM k 0) && (iterNatM k r == 3^(sNatM k 0) + iterNatM k 0)
  else
    (sNatM k r == sNatM k (r+1)) && (iterNatM k r == iterNatM k (r+1))

def amasLit   (k : Nat) : Nat := ((List.range (2^k)).filter (buenoLitMas   k)).length
def amenosLit (k : Nat) : Nat := ((List.range (2^k)).filter (buenoLitMenos k)).length

-- Desenrollar 128 restos anidados pasa del limite por defecto (512).
set_option maxRecDepth 40000

/- (a) EL CRUCE CONTRA EL REPO. Estos cinco numeros estan en `sucesiones.txt`:
       a(3)=1, a(4)=3, a(5)=8, a(6)=18, a(7)=39.
   Van como `by decide` y NO como `#eval` a proposito: el `#eval` lo calcula el
   compilador y su resultado no lo revisa nadie; el `by decide` lo revisa el
   NUCLEO, que es lo unico en lo que se apoya todo lo de arriba. -/
theorem repo_a3 : amas 3 = 1  := by decide
theorem repo_a4 : amas 4 = 3  := by decide
theorem repo_a5 : amas 5 = 8  := by decide
theorem repo_a6 : amas 6 = 18 := by decide
theorem repo_a7 : amas 7 = 39 := by decide

/- Las ocho clases modulo 32 que `sucesiones.txt` lista una por una:
   2, 4, 5, 12, 18, 20, 22, 28. Aqui se comprueban de dos en dos: las ocho
   buenas y una muestra de las malas. La 4 es Garner 1985 y la 5 es Wu-Huang
   2001, o sea que los dos anclajes publicados quedan comprobados por el nucleo. -/
theorem clases32_buenas :
    buenoM 5 2 = true ∧ buenoM 5 4 = true ∧ buenoM 5 5 = true ∧ buenoM 5 12 = true ∧
    buenoM 5 18 = true ∧ buenoM 5 20 = true ∧ buenoM 5 22 = true ∧ buenoM 5 28 = true := by
  decide

theorem clases32_malas :
    buenoM 5 0 = false ∧ buenoM 5 1 = false ∧ buenoM 5 3 = false ∧
    buenoM 5 31 = false := by
  decide

/- Y el cruce contra la implementacion independiente, en los dos mapas. -/
theorem cruce_mas :
    amasLit 1 = amas 1 ∧ amasLit 2 = amas 2 ∧ amasLit 3 = amas 3 ∧
    amasLit 4 = amas 4 ∧ amasLit 5 = amas 5 ∧ amasLit 6 = amas 6 ∧
    amasLit 7 = amas 7 := by decide

theorem cruce_menos :
    amenosLit 1 = amenos 1 ∧ amenosLit 2 = amenos 2 ∧ amenosLit 3 = amenos 3 ∧
    amenosLit 4 = amenos 4 ∧ amenosLit 5 = amenos 5 ∧ amenosLit 6 = amenos 6 ∧
    amenosLit 7 = amenos 7 := by decide

/- Y la igualdad, en la version literal e independiente, medida en vez de
   demostrada. Es la comprobacion que el pendiente de la bitacora pedia hacer a
   base de CPU; el teorema `espejo` la da para todo k, pero esto verifica que el
   teorema habla del mismo objeto que se midio. -/
theorem igualdad_literal :
    amasLit 1 = amenosLit 1 ∧ amasLit 2 = amenosLit 2 ∧ amasLit 3 = amenosLit 3 ∧
    amasLit 4 = amenosLit 4 ∧ amasLit 5 = amenosLit 5 ∧ amasLit 6 = amenosLit 6 ∧
    amasLit 7 = amenosLit 7 := by decide

/- Y la biyeccion en concreto, para verla con los dedos: en k = 5 los ocho
   buenos de 3n-1 son los reflejos 31 - r de los ocho buenos de 3n+1.
   {2,4,5,12,18,20,22,28} reflejado es {29,27,26,19,13,11,9,3}. -/
theorem reflexion_k5 :
    buenoN 5 29 = true ∧ buenoN 5 27 = true ∧ buenoN 5 26 = true ∧
    buenoN 5 19 = true ∧ buenoN 5 13 = true ∧ buenoN 5 11 = true ∧
    buenoN 5 9  = true ∧ buenoN 5 3  = true := by decide

/- ------------------------------------------------------------------------ -/
/- EL CONTROL FINAL. `#print axioms` lista de que depende cada teorema. Si
   apareciera `sorryAx` habria un agujero tapado y el fichero entero no valdria.
   Tienen que salir solo los axiomas estandar de Lean (propext, Quot.sound,
   Classical.choice) -- o ninguno. -/
#print axioms paso_conj
#print axioms conj_it
#print axioms conj_s
#print axioms terras
#print axioms borde
#print axioms periodico
#print axioms conj_bueno
#print axioms reflexion
#print axioms cuenta_fin
#print axioms cuenta_refl
#print axioms espejo
#print axioms repo_a7
#print axioms clases32_buenas
#print axioms cruce_mas
#print axioms cruce_menos
#print axioms igualdad_literal
#print axioms reflexion_k5
