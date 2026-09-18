# 12a REVISION ADVERSARIAL -- TANDA 3: OBSTRUCCION DE LAS ERIZAS

Revisor: Claude (Opus 5), 12-09-2026. Tercera tanda, de a una, sin
agentes. Nada del laboratorio modificado.

**Objeto:** `depuracion/frente20260910/Erizas.md`, `obstruccion.lean`,
`obstruccion_salida.txt`, `obstruccion_ampliada.txt`.

Esta es la tanda mas consecuente del frente, porque es la unica que
**mata** una ruta. Si Erizas estuviera mal, el laboratorio habria
retirado un objetivo vivo por nada. Por eso la revise entera y con
DP propio.

## Veredicto adelantado

**La demostracion es correcta.** Revise (E1) a (E8) y la seccion 5 paso
por paso, rehice cada desigualdad, y reproduje sus numeros con un DP
independiente. No encontre ningun error. Es, ademas, la pieza mas
limpia del frente: elemental, autocontenida y sin apoyarse en ningun
teorema previo del laboratorio, tal como declara.

La unica mordida es de **alcance declarado**, no de matematica.

## 1. La prueba, verificada linea por linea

**(E1) los momentos.** `X_t = k_t - 1`, cero tras salir.

- `E X_t = 1`: `X` es martingala. Con `c` par las dos ramas conservan
  `k`; con `c` impar van a `k+1` y `k-1` con peso 1/2; en `k=2` la
  segunda sale y vale 0, y `(1-1) = 0` es justo lo que la martingala
  pide. **No hace falta independencia entre la paridad de `c` y la
  altura**, como la nota subraya: es un enunciado por trayectoria.
- `E X_t^2 <= t+1`: el incremento de `X^2` es 1 solo en los pasos con
  `c` impar, 0 en los demas.
- `E X_t^4`: `[(x+1)^4+(x-1)^4]/2 = x^4+6x^2+1` (correcto al
  desarrollar), luego `E X_{t+1}^4 <= E X_t^4 + 6(t+1) + 1`, y sumando
  `j=0..t-1` desde `X_0^4=1` sale `1 + 3t(t+1) + t = 3t^2+4t+1`, que en
  efecto es `(t+1)(3t+1)`. **Correcto.**

**(E2)** `1 = E X_t = E[X_t 1_vivo] <= (t+1) S_t` porque `X_t <= t+1`
sobre las palabras vivas. Elemental y correcto.

**(E3) las cuatro ramas normalizadas.** Las derive yo desde `paso` con
`u = c/3^k`:

| rama | nuevo `u` | Erizas |
|---|---|---|
| N0 (`c` par) | `u/2` | `u/2` |
| N1 (`c` par) | `(3u - 1 + 3^(-k))/2` | idem |
| A (`c` impar) | `u/2 + 1/(2*3^(k+1))` | idem |
| D (`c` impar) | `(3u - 1)/2` | idem |

Las cuatro coinciden. Y las dos constantes aditivas que la nota
declara tambien: en la fila par el termino es `(1 - 3^(-k))/4 < 1/4`
(la nota dice "basta incluso 1/4" -- correcto, y noto que el signo
importa: es `1 - 3^(-k)`, no `1 + 3^(-k)`), y en la impar
`(1 + 3^(-k-1))/4 <= 1/2`. De ahi `E U_t <= |c0|/9 + t/2`, con la
convencion no condicionada bien mantenida. **Correcto.**

**(E4) la caja.** Con `h_t = techo([4(t+1)^2(3t+1)]^(1/4))`:
Markov de orden 4 mas (E2) da `P(X_t>h_t | vivo) <= (t+1)^2(3t+1)/h_t^4
<= 1/4` por definicion de `h_t`. Markov de orden 1 mas (E3) da
`P(U_t>J_t | vivo) <= (|c0|/9 + t/2)/(4(|c0|+t+1)) <= 1/4`. Union
(sin independencia) deja media masa en la caja. La caja tiene
`k` en `2..h_t+1`, o sea `h_t` alturas, y `2L_t+1` valores de `c`:
`D_t = h_t(2L_t+1)`. `log D_t = O(t^(3/4)) + O(log t) = o(t)`.
**Todo correcto**, incluidos los conteos de la caja.

**(E5)-(E6).** Cauchy sobre la media masa da `A_t >= 1/(4 D_t)`; la cota
superior `A_t <= 1` sale de `A_t = sum_k P_t(k) C_k` con `C_k <= 1`.
Con `log D_t = o(t)`, `A_t^(1/t) -> 1`. **Correcto**, y la nota es
cuidadosa al decir que esto NO da limite positivo ni limite del
cociente.

**(E7)-(E8).** Reducir modulo `2^m` solo agrupa, luego aumenta la suma
de cuadrados; de ahi `e_t(m)+1 >= 2^m A_t`. La version marginal es el
mismo Cauchy sobre `2L_t+1` enteros. **Correcto.**

**Seccion 5.** Sobre la escala inyectiva, `e_t(m) = 2^m A_t - 1`
exactamente. Suponiendo (E0), fijando `t` y haciendo `m -> infinito`:
`A_{t+1} <= 2 rho A_t`, e iterando `A_{T+n} <= (2rho)^n A_T`, cuyo
`^(1/t)` tiende a `2rho < 1` y contradice (E6). La version por bloques
es el mismo argumento sobre la subsucesion `T+nL`. **Correcto.**

Y el parrafo final de cuantificadores es exacto y es el punto delicado
bien resuelto: la refutacion produce un `m` **finito** que viola (E0),
aunque el argumento pase por un limite; y "no se afirma que el cociente
cruce 1/2: puede quedar debajo y perder todo margen uniforme".

## 2. Reproduccion independiente (DP propio, sin leer obstruccion.py)

`rep_erizas.py` construye el DP desde `paso` con conteos enteros y
palabras de bits justas, y comprueba en `Fraction` exacta:

| control | t=0..28, c0=1 |
|---|---|
| `E X_t = 1` | **exacto en los 29 tiempos** |
| `E X_t^2 <= t+1` | se cumple |
| `E X_t^4 <= (t+1)(3t+1)` | se cumple |
| `S_t >= 1/(t+1)` | se cumple |
| `E U_t <= \|c0\|/9 + t/2` | se cumple |
| `1 >= A_t >= 1/(4 D_t)` | se cumple |
| estados en t=28 | **590.042** (Erizas dice 590.042) |
| estados en t=16 | **3.154** (contraccion_salida.txt dice 3154) |

Y los dos decimales publicados, reproducidos al ultimo digito:

    19 -> 20 : 0.450422    Erizas dice 0,450422
    27 -> 28 : 0.469286    Erizas dice 0,469286

La serie entera sube monotona: 0.4413, 0.4460, 0.4504, 0.4533, 0.4563,
0.4590, 0.4620, 0.4641, 0.4660, 0.4677, 0.4693. Es exactamente el
comportamiento que (E6) obliga.

`rep_erizas_escala.py` verifica ademas la identidad de la seccion 5:
`e_t(m) = 2^m A_t - 1` para `m` sobre la escala inyectiva, comprobado
en `t = 12, 16, 20` y en tres escalas cada uno. **Cierra exacta.**

**Discrepancia resuelta (no es defecto).** `contraccion_salida.txt`
informa `escala_inyectiva=19` en `t=16`, y yo calculo que la escala
minima que separa los `c` de cada fibra es **14**. La diferencia es de
definicion: el diametro del soporte de `c` en `t=16` es 275.564, y
`techo(log2(275565)) = 19`. Usan la cota **suficiente** por diametro,
no la minima. Es la eleccion conservadora, que es la correcta aqui.

## 2-bis. El Lean, recompilado y leido

`lean depuracion/frente20260910/obstruccion.lean`: exit 0, nueve
resultados, **sin `sorryAx`**, y la salida es identica a
`obstruccion_lean.txt` (solo diferian los fines de linea).

Mas importante que recompilarlo es comprobar que no afirma de mas. El
teorema de nombre mas fuerte es

    obstruccion_finita (a b rho z : Rat)
      (h : 1-rho < z*(b-2*rho*a)) : rho*(2*z*a-1) < z*b-1

que con `z = 2^m`, `a = A_t`, `b = A_{t+1}` dice exactamente:
si `A_{t+1} > 2 rho A_t` con holgura suficiente a esa escala, entonces
`rho * e_t(m+1) < e_{t+1}(m)`, o sea **el testigo de violacion a escala
FINITA**. Es el nucleo escalar del ultimo parrafo de la seccion 5,
formalizado como condicional. No pretende ser la obstruccion: la
declaracion de la nota ("Lean toma las recurrencias de momentos como
hipotesis") es exacta.

## 3. Una correccion a mis propias actas anteriores

En las tandas 1 y 2 anote como mordida que el frente publica "cero
cruces de 1/2" y el rango de `H/E` sin reportar que la tendencia va en
contra. **Erizas si la reporta**: da 0,450422 y 0,469286 precisamente
para mostrar la subida, y aclara que no es prueba de convergencia.

Luego el frente **no** es ciego a esa senal. Las mordidas M1 y M4 se
mantienen, pero rebajadas: el defecto esta en que `LEEME.md` seccion 4
y `Castoras.md` resumen sus barridos sin ese dato, no en que el
laboratorio lo ignore. Lo corrijo aqui en vez de dejarlo torcido.

## Mordida

### M5. La retirada anunciada en LEEME es mas ancha que lo que Erizas demuestra

Erizas refuta (E0) **con `m` no acotada**: la seccion 5 fija `t` y hace
crecer `m` sin cota. Medi si esa hipotesis es necesaria o decorativa.
`rep_erizas_escala.py`, cociente `rho(t,m) = e_{t+1}(m)/e_t(m+1)`:

| t | m=6 | m=12 | m=18 | limite de escala |
|---|---|---|---|---|
| 12 | 0.3147 | 0.3964 | 0.3996 | 0.399665 |
| 16 | 0.3138 | 0.4313 | 0.4370 | 0.437395 |
| 19 | 0.3118 | 0.4422 | 0.4498 | 0.450422 |

En **todo** `m` finito el cociente esta estrictamente por debajo del
limite, al que se acerca por abajo (no es monotono: hay hundimientos en
`m` pequena, pero el supremo es el limite). Es decir: el supremo sobre
`1 <= m <= M(t)` con `M(t)` finita es estrictamente menor que el numero
que la seccion 5 usa para llegar al absurdo. **La refutacion necesita
`m` ilimitada a `t` fijo; no es un tecnicismo del argumento, es su
motor.**

Y (E8) refuta la cota uniforme de `C2` solo cuando `2^m` supera el
tamano de la caja, o sea `m` del orden de `t^(3/4)` hacia arriba.

La propia Erizas lo dice bien: "Esto NO impide equidistribucion a una
escala `m` FIJA al crecer `t`". Pero `LEEME.md` seccion 5 lo traduce a
un mandato sin condiciones: **"No continuar intentando demostrar el
margen uniforme global siguiente"**, sin decir que las versiones a
escala acotada quedan intactas.

Calibro la mordida con honestidad, porque tiene un contrapeso: el
telescopio de LEEME seccion 1 recorre la **diagonal** `m -> m+n`, asi
que ESE argumento necesita `m` ilimitada de todos modos y para el la
ruta si esta muerta. La mordida no es que la ruta siga viva; es que el
indice convierte "esta ruta concreta esta muerta" en "no continuar", y
borra la frontera que la propia Erizas habia dibujado. Con M3 de la
tanda 2, `LEEME.md` seccion 5 queda **equivocada en las dos
direcciones a la vez**: prohibe lo que sigue abierto y propone lo que
ya esta cerrado.

## 4. Una mejora concreta que esta a mano

Erizas declara sus cotas "deliberadamente holgadas" y que el exponente
3/4 "no se afirma que sea la escala verdadera". Su propio DP dice cual
es. Midiendo `S_t` (`rep_supervivencia.txt`):

    t     4      8     12     16     20     24
    S_t*sqrt(t+1)  1.118  1.125  1.124  1.110  1.108  1.109

`S_t` es `~ 1.11/sqrt(t+1)`, no `1/(t+1)`: la tasa clasica de un paseo
critico. `E[X_t | vivo]` sale `~ 0.9 sqrt(t+1)`, tambien la clasica.

Sustituir (E2) por `S_t >= c/sqrt(t)` bajaria `h_t` de `O(t^(3/4))` a
`O(t^(5/8))`, y con ello el umbral de escala de (E8). No cambia (E6) ni
la seccion 5 --que solo necesitan `o(t)`-- pero **ensancha el rango de
`m` excluido**, que es justo la frontera que M5 senala como no dibujada.
Es una mejora barata y su evidencia ya esta en el repositorio.

## Veredicto de la tanda 3

- **La obstruccion es real y la demostracion es correcta.** No
  encontre ni un paso que ceda. La retirada del margen uniforme esta
  justificada.
- **Los numeros son reproducibles al digito** con un DP escrito desde
  cero, incluidos los conteos de estados.
- La nota es la mas honesta del frente en sus propias limitaciones
  (declara que Lean no formaliza el enlace, que las cotas son holgadas,
  que el Python no es revision ciega, y que no cierra P2 ni Collatz).
- **Una mordida (M5)**, de alcance declarado y localizada en `LEEME.md`,
  no en `Erizas.md`.

## Reproduccion

    python revision12_adv1/rep_erizas.py 28
    python revision12_adv1/rep_erizas_escala.py
