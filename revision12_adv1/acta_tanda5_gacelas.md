# 12a REVISION ADVERSARIAL -- TANDA 5: PUENTE DE LAS GACELAS

Revisor: Claude (Opus 5), 12-09-2026. Quinta y ultima tanda, de a una,
sin agentes. Nada del laboratorio modificado.

**Objeto:** `depuracion/frente20260910/Gacelas.md`,
`transferencia.lean`, `transferencia_*.txt`.

## Veredicto adelantado

**Correcta de principio a fin.** Verifique el h-transform, (G1), su
contraejemplo, (G2) con la identidad de balota, (G3), la identidad
afin, (G4), (G5) y los cuatro certificados enteros. Cero
discrepancias. Es la tanda con la matematica mas fina del frente.

Las dos mordidas son ambas de **cosecha no recogida**: la nota prueba
mas de lo que se cobra, y no conecta con Erizas un resultado que la
mejora directamente.

## 1. El h-transform y (G1)

`h(k,c) = k-1` es armonica (`Ph = h`), incluido `k=2` donde la rama que
sale vale cero: es la misma martingala que Erizas usa como `X_t`.
Las probabilidades de `Q` que la nota escribe son exactas:

    compartido 1/2, 1/2;  mixto  k/[2(k-1)] arriba,  (k-2)/[2(k-1)] abajo

Comprobado que suman 1 y son no negativas para `k=2..39`, y que desde
`k=2` la bajada tiene probabilidad exactamente cero.

**(G1)** la derive yo: para un prefijo vivo de largo `r`,
`P(prefijo | tau>H) = P(prefijo) S_(H-r)(z_r)/S_H(z0)` y
`Q(prefijo) = P(prefijo) h(z_r)/h(z0)`; el cociente es el de la nota.
Correcto.

**El contraejemplo, reproducido exacto.** Desde `(2,0)`, enumerando las
16 palabras de 4 bits: **12 supervivientes, 8 empiezan en bit 0 y 4 en
bit 1**, luego `P(bit 0 | tau>4) = 2/3` frente a `Q(bit 0) = 1/2`. Y
las dos primeras ramas son compartidas, o sea bits que ANTES de
condicionar eran libres. Coincide con la nota en los cuatro numeros.

Este contraejemplo es el aporte conceptual mas util de la tanda: dice
con un caso de cuatro bits por que **no** se puede identificar el
h-transform con el condicionamiento al futuro. Es exactamente la clase
de confusion que se lleva por delante un programa entero, y esta
cazada con un ejemplo de tamano 16.

## 2. (G2): la cota de supervivencia

`S_t(2,c0) >= q_t = 2^-t C(t, floor(t/2)) >= 1/sqrt(2t+3)`.

- El acoplamiento es correcto: en `t` pasos reales hay a lo sumo `t`
  mixtos, el bit del mixto es fresco (el instante es tiempo de parada
  de la filtracion de bits), y menos pasos del paseo solo pueden
  aumentar la supervivencia.
- La formula `q_t` la comprobe a mano en `t=1,2,3` (1/2, 1/2, 3/8) y
  numericamente contra la enumeracion: **6 semillas x t=1..16, 0
  fallos**, incluidos `c0 = 0`, negativos y grandes.
- La **identidad de balota** `(2m+1)^2(4m+5) - (2m+2)^2(4m+1) = 1`:
  la desarrolle a mano (`16m^3+36m^2+24m+5` menos `16m^3+36m^2+24m+4`)
  y la verifique para `m=0..4999`. **Es exactamente 1**, que es lo que
  hace funcionar la induccion `a_m >= 1/sqrt(4m+1)` sin holgura que
  perder. Verificada tambien la induccion (`m=0..2999`) y las dos
  identificaciones `q_(2m)=a_m`, `q_(2m+1)=a_(m+1)`.

Y es una cota **buena**, no de conveniencia: en la tanda 3 medi
`S_t ~ 1.11/sqrt(t+1)`, mientras (G2) da `0.707/sqrt(t+1.5)`. Esta a
un factor 1,57 de la verdad.

**(G3)** es (M6) dividida por `S_H` con la cota (G2): correcto, y el
"pago de horizonte" esta bien identificado.

## 3. La parte multiplicativa

La identidad afin `u_(t+1) = A u_t + delta` con `A = 1/2` (bit 0) y
`A = 3/2` (bit 1) la verifique en las cuatro corrientes por separado:

| corriente | `u'` | `A` | `delta` |
|---|---|---|---|
| N0 | `u/2` | 1/2 | 0 |
| N1 | `(3u-1+3^-k)/2` | 3/2 | `(3^-k - 1)/2` |
| A | `u/2 + 3^-(k+1)/2` | 1/2 | `3^-(k+1)/2` |
| D | `(3u-1)/2` | 3/2 | `-1/2` |

**15.516 transiciones comprobadas, 0 fallos**: `A` es siempre 1/2 o
3/2 y `delta` tiene exactamente la forma prevista. El truco de
prolongar los bits despues de la salida --para poder evaluar en `tau`
sin parada opcional-- es correcto y es elegante.

Los cuatro certificados de (G4)-(G5), en enteros exactos:

| certificado | comprobado |
|---|---|
| `lambda^2 = (2+sqrt3)/4 < 15/16` via `4 sqrt3 < 7` (o sea `48<49`) | si |
| `(15/16)/(31/32) = 30/31` | si |
| `30/31 < (61/62)^2`, con diferencia `1/3844` | si |
| `61^2(2T+5) <= 62^2(2T+3)` desde `T=29` | si, **el umbral es 29 exacto** |
| `f(1024) = 124(61/62)^1024 sqrt(2051) <= 1` | si, vale `3.3e-4` |

La cadena `lambda^t / (31/32)^(t/2) <= (61/62)^t` y la union
`sum_(t>=T) = 62(61/62)^T` son correctas.

**(G5)** la rehice: en el complemento del evento malo,
`Pi_tau <= (31/32)^tau <= (31/32)^T` para `tau > T`, y `(31/32)^T x <= 1`
por la eleccion de `T`. Luego `P >= S_T - P(malo)`. Correcto.

## 4. El Lean

`lean depuracion/frente20260910/transferencia.lean`: exit 0, **ocho
resultados**, salida identica a `transferencia_lean.txt`, **sin
`sorryAx`**. Los enunciados son `masa_armonica` (la armonicidad sobre
el arbol entero, todo `n, k>=1, c`), `pesos_mixtos`,
`certificado_balota`, `certificado_raiz`, `certificado_exponencial`,
`cola_monotona`, `cola_inicial` y `sesgo_compartido` (los conteos del
contraejemplo). Son los **ingredientes**, y la nota lo declara asi:
"(G1)-(G5) y las raices/limites estan demostrados POR ESCRITO, no
formalizados integralmente en Lean". Declaracion exacta.

## Mordidas

### M7 (la mas util de toda la revision). (G2) mejora a Erizas y nadie las conecto

Erizas usa `S_t >= 1/(t+1)` (su E2), que es lo que fija el tamano de
su caja y por tanto el exponente `t^(3/4)`. Gacelas, **el mismo dia y
en el mismo frente**, demuestra `S_t >= 1/sqrt(2t+3)`, que para `t>=2`
es estrictamente mejor. Es la misma cadena, el mismo `tau`, los mismos
bits, y la cota es uniforme en `c0`: **se puede sustituir directamente**.

Con (G2) en lugar de (E2), el Markov de orden 4 pide
`h_t^4 >= 4(t+1)(3t+1)sqrt(2t+3) = O(t^(5/2))`, luego
`h_t = O(t^(5/8))` en vez de `O(t^(3/4))`. Numeros
(`rep_puente_erizas_gacelas.txt`):

| t | `h_t` con (E2) | `h_t` con (G2) | `log2 L_t` (E2) | `log2 L_t` (G2) |
|---|---|---|---|---|
| 100 | 60 | 37 | 112.0 | 71.7 |
| 1000 | 332 | 153 | 549.7 | 260.5 |
| 5000 | 1107 | 417 | 1782.7 | 682.4 |

Exponentes ajustados en `t=5000`: 0,823 frente a 0,708, convergiendo a
los teoricos 0,75 y 0,625.

Que se gana. (E6) y la seccion 5 de Erizas no cambian --solo necesitan
`o(t)`-- pero **(E8) si**: el umbral de escala a partir del cual la
obstruccion muerde baja de `~t^(3/4)` a `~t^(5/8)`, o sea la
obstruccion excluye MAS. Y (E8) es justo el punto donde en la tanda 3
anote (M5) que la frontera no estaba dibujada. Dibujarla mejor esta a
mano y ya esta demostrado dentro de la casa.

Esto no es un error de Gacelas ni de Erizas: Erizas es la tanda 3 y
Gacelas la 5, asi que la realimentacion no era posible al escribirla.
Es cosecha sin recoger, y es lo mas rentable que sale de esta revision.

### M8. El "piso 1/sqrt(log x)" es la supervivencia, no el producto -- y la version condicionada no lleva logaritmo

(G5) da `P(tau>T y Pi_tau x <= 1) >= 1/sqrt(2T+3) - 62(61/62)^T`, y la
nota lo resume como "un piso `1/[2sqrt(2T+3)]`, del orden
`1/sqrt(log x)`". Cierto, pero mezcla dos cosas de tamanos
completamente distintos:

- `S_T`, que es del orden `1/sqrt(T)` --polinomico--;
- `P(malo)`, que es `62(61/62)^T` --exponencialmente pequeno--.

El primero es el precio de **sobrevivir**; el segundo, el de que el
producto sea pequeno. Dividiendo por `S_T` en vez de acotarlo por
abajo, el mismo argumento entrega

    P(Pi_tau * x <= 1 | tau > T) >= 1 - P(malo)/S_T
                                 >= 1 - 62(61/62)^T sqrt(2T+3)

y en `T = 1024` eso es `>= 1 - 1.65e-4`, es decir **0,99983, sin
ningun `1/sqrt(log x)`**.

O sea: condicionado a sobrevivir, la parte multiplicativa **ya no es un
problema en absoluto**; el `1/sqrt(log x)` del titular es enteramente
el coste de la supervivencia, que estaba ahi antes y no lo pone el
producto. Es una infra-declaracion, la tercera de este frente (con el
`3/4` de Erizas y el `O(n log n)` de Mangostas).

Y tiene consecuencia para el programa, no solo para la redaccion:
confirma desde el lado cuantitativo lo que la seccion 4 dice desde el
cualitativo. El cuello **no** es `Pi_tau`. Es `W_tau`, entero y solo.
Conviene que LEEME lo diga con ese enfasis, porque hoy su resumen
("un piso de orden 1/sqrt(log x) para excursiones largas cuya parte
multiplicativa es pequena") sugiere que el producto cuesta caro.

## 5. Lo que falta, y esta bien dicho

La seccion 4 es, de todo el frente, la formulacion mas precisa del
cuello: `u_tau = Pi_tau u0 + W_tau`, y aunque el primer sumando sea
pequeno el segundo puede no serlo; falta una constante `M`
independiente del arranque y **masa conjunta**. Y la frase "Una mediana
marginal o una medicion de desplazamiento del 5% no prueba esa
interseccion" es una autocritica dirigida contra mediciones previas del
propio laboratorio. Eso es lo que hay que hacer y casi nadie hace.

Tampoco cae en el atajo obvio: dice explicitamente que `Q` no resuelve
esto, porque (G1) trata prefijos y `W` depende de sufijos y de la
absorcion.

## Veredicto de la tanda 5

- **Correcta.** No encontre ni un paso que ceda, ni en el h-transform,
  ni en la balota, ni en los certificados, ni en (G5).
- El contraejemplo de `(2,0)` es pequeno, decisivo y esta bien usado.
- (G2) es una cota **buena**, a factor 1,57 de la verdad medida.
- El Lean recompila sin `sorryAx` y no afirma de mas.
- **Dos mordidas, ambas de cosecha no recogida** (M7, M8): la tanda
  prueba mas de lo que se cobra, y una de sus piezas mejora
  directamente a Erizas.

No prueba P2, y la nota es la primera en decirlo.

## Reproduccion

    lean depuracion/frente20260910/transferencia.lean
    python revision12_adv1/rep_gacelas.py
