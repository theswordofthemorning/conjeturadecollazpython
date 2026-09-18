# 12a REVISION ADVERSARIAL -- TANDA 2: BALANCE DE LAS CASTORAS

Revisor: Claude (Opus 5), 12-09-2026. Segunda tanda, de a una, sin
agentes. Nada del laboratorio ha sido modificado.

**Objeto:** `depuracion/frente20260910/Castoras.md`, `balance.lean`,
`balance_celdas.json`, `balance_salida.txt`,
`balance_reproduccion.txt`.

**Encargo atendido:** el que la propia nota deja escrito al final --
"atacar la normalizacion N frente a 2N, la omision de grupos vacios, el
factor 2V en Delta y s, el alcance de la formalizacion general, y la
distincion entre una ley arbitraria y una ley alcanzable".

## 0. El cimiento, verificado antes que nada

Las cuatro tandas del frente descansan en una sola ley de paso, la que
`balance.lean` escribe como `paso`. Antes de revisar el balance
comprobe que esa ley **es la cadena (k,c) real**, no una idealizacion.

La derive a mano desde el mapa `T(x)=x/2` si par, `(3x+1)/2` si impar,
sobre un estado `{v, w}` con `w = 3^k v + c` y ancla `v`:

| ancla | c | `T` sobre los dos da | ley |
|---|---|---|---|
| par | par | `w' = 3^k (v/2) + c/2` | `(k, c/2)` |
| par | impar | `w' = 3^(k+1)(v/2) + (3c+1)/2` | `(k+1, (3c+1)/2)` |
| impar | par | `w' = 3^k v' + (3c+1-3^k)/2` | `(k, (3c+1-3^k)/2)` |
| impar | impar | `w' = 3^(k-1) v' + (c-3^(k-1))/2` | `(k-1, (c-3^(k-1))/2)` |

que son **exactamente** las cuatro ramas de `paso`, con `bit` = paridad
del **ancla** (la moneda de Terras de LEONAS), no la de `c`.

Comprobacion numerica en `rep_cadena_real.py`: `k=2..8`, `c=-400..400`,
`v=1..259`, **1.439.748 casos, 0 fallos**. Como control de que la prueba
tiene filo, la repeti usando la paridad de `c` en vez de la del ancla:
**53.559 fallos de 118.917**. La comprobacion no es vacua.

Ademas: ninguna rama con `k>=3` produce `k'<2` (0 casos). Luego la unica
salida de la excursion es `k=2`, `c` impar, ancla impar -- **una sola de
las dos ramas de ese grupo**. Esto es justo lo que el paso 2 de la
demostracion necesita, y se confirma abajo.

## 1. La identidad (C): la derive entera por mi cuenta y es correcta

Rehice los tres pasos sin mirar `balance.py`.

**Paso 1.** Partiendo residuos pares e impares en la escala padre `2N`:
`2N sum_r p(r|k)^2 = 2a^2(1+E_{k,0}) + 2b^2(1+E_{k,1})`. Con `a+b=1`,
`2a^2+2b^2-1 = (a-b)^2`, y la cuenta

    a E0 + b E1 + (a-b)(a E0 - b E1) = 2a^2 E0 + 2b^2 E1

(usando `1+a-b = 2a` y `1-a+b = 2b`) da `E = G + Q + R`. **Correcto.**
Es exactamente `separar_paridad` de Lean.

**Paso 2.** Escribiendo `c=2u` o `c=2u+1`, las cuatro corrientes son

    N0: u -> u                        (alpha=1)
    N1: u -> 3u + (1-3^k)/2           (alpha=3)
    A:  u -> 3u + 2                   (alpha=3)
    D:  u -> u + (1-3^(k-1))/2        (alpha=1)

Todas afines con `alpha` en `{1,3}`, unidades modulo `2^m`, luego
biyecciones de `Z/N`, luego conservan `sum_r p(r)^2`. **Verificado por
enumeracion** en `rep_testigos.py` para `m=2..10`, `k=2..8`, todo `u`:
sin excepciones. Tambien comprobe que cada formula esta bien definida
modulo `N` a partir de `c` modulo `2N` (los sobrantes son `3N` o `N`,
ambos `= 0` mod `N`). La afirmacion del paso 2 es exacta.

**Paso 3.** La identidad de varianza ponderada

    S_j F(p_j) = sum_i M_i F_i - (1/S_j) sum_{i<l} M_i M_l D_{i,l}

sale de multiplicar `varianza_cuatro` por `N/S_j` y sumar en `r`; el
termino cruzado se reordena con `sum_i M_i F_i (M_i + sum_{l!=i} M_l)
= S_j sum_i M_i F_i`. Al pasar de `F` a `E` los `-1` se cancelan
exactamente. **Correcto.**

Y el cierre: `V' e' = 2VG - OU - 2V Delta`, con `V'/(2V) = 1-s`, da

    (1-s) e' = E - Q - R - sU - Delta.

**Punto fino que si aguanta:** `varianza_cuatro` tiene exactamente
cuatro sumandos. Comprobe que eso no es una aproximacion: leyendo
`paso`, a una altura hija `j` solo pueden llegar padres de altura `j`
(pares, dos corrientes), `j-1` (impares, rama A) y `j+1` (impares, rama
D). **Son cuatro exactas, nunca cinco.** El lema escalar cubre el caso
general, no un caso tipico.

## 2. Los cuatro ataques del encargo

**a) La normalizacion `N` frente a `2N`.** Correcta. `E_{k,b}` se
normaliza con `N` porque, tras partir por paridad, cada mitad esta
indexada por `u` modulo `N`, no modulo `2N`. Si se usara `2N` el paso 1
no cerraria; con `N` cierra exacto, y lo comprobe en los dos testigos.

**b) La omision de grupos vacios.** Inocua, y por dos motivos distintos
que conviene no confundir. En el texto, un grupo vacio entra con
`a_k = 0`, y todos los terminos donde aparece `E_{k,0}` llevan factor
`a_k` o `a_k^2`, asi que el valor indefinido nunca se usa. En Lean, la
funcion `exceso` divide por `suma f`, y para una fibra vacia eso es
`0/0`; **el resultado correcto sale porque `Rat` define `x/0 = 0`.**
Funciona, pero descansa en un valor basura del nucleo, no en el
argumento. Los testigos no tienen fibras vacias, asi que hoy no muerde;
merece un comentario en el fichero para que nadie lo herede sin saberlo.

**c) El factor `2V` en `Delta` y `s`.** Correcto y consistente: cada
padre emite **dos** ramas, luego el denominador natural es `2V`, y
`s = O/(2V)` es la fraccion de RAMAS que sale, no de padres. De ahi
`0 <= s <= 1/2` (porque `O <= V`), comprobado en las 234 celdas.
`V' = 2V - O` cuadra con la masa hija en los dos testigos.

**d) Ley arbitraria frente a ley alcanzable.** La nota lo dice ella
misma y con todas las letras: "NO se ha demostrado que estas leyes sean
alcanzables desde un arranque puntual de la excursion. Refutan la
extension a distribuciones arbitrarias, no el candidato sobre la
orbita." Es la lectura correcta y es la restrictiva. Sin objecion.

**e) Alcance de la formalizacion.** La nota declara que Lean formaliza
las identidades escalares, la equivalencia del umbral y los dos
testigos, y que el enlace general con las sumatorias de la cadena NO
esta formalizado. Lei `balance.lean` entero y la declaracion es exacta:
`balance_global` es el esqueleto escalar (con `masa=V`, `energia=VG`,
`paridad=VQ`, `sesgo=VR`, `salida=O`, `mezcla=2V*Delta`), no la cadena.
Ni sobra ni falta nada en esa declaracion.

**Lo recompile yo:** `lean depuracion/frente20260910/balance.lean`,
exit 0, los 19 `#print axioms` identicos a `balance_lean.txt`, **sin
`sorryAx` ni `native_decide`**. Salida en `relean_balance.txt`.

## 3. Los dos testigos: reproducidos desde cero, y son genuinos

El ataque obvio era que `llegada` estuviera escrita a mano. **No lo
esta:** se calcula con `entrada.flatMap` aplicando `paso` a los dos
bits y dejando caer el `none`. Son pasos reales de la ley, no un
conjunto hija fabricado.

Los rehice enteros con mis propias definiciones (`rep_testigos.py`):

| | Castoras.md | mi reproduccion |
|---|---|---|
| testigo 1: V, E, Q, R, s, U | 16, 5/8, 1/4, -3/8, 3/8, 0 | idem |
| testigo 1: V', e', e'/E, Delta | 20, 6/5, 48/25, 0 | idem |
| testigo 2: E, e', Q, R, s, U, Delta | 3, 3, 0, 0, 1/4, 3, 0 | idem |
| ramas muertas = O | 12 y 1 | 12 y 1 |
| identidad (C) | -- | **cierra exacta en los dos** |

Nota de honestidad sobre mi propio trabajo: mi primera version del
script daba `G=12`, `R=9/4`, `U=11` en el testigo 1 y la identidad
fallaba. El error era **mio** -- normalice el exceso interno dividiendo
por la masa en vez de por su cuadrado. Lo dejo escrito porque explica
por que el testigo 2 pasaba igual con el bug (sus grupos tienen un solo
elemento, y ahi `m` y `m^2` coinciden): una reproduccion que solo
mirara el testigo 2 no habria detectado nada.

## 4. Las 234 celdas: la identidad cierra, y los rangos coinciden al digito

`rep_castoras.py` lee `balance_celdas.json` y comprueba en `Fraction`,
celda por celda, la identidad y las dos formas del margen.

| control | resultado |
|---|---|
| fallos de `(1-s)e' = E-Q-R-sU-Delta` en 234 celdas | **0** |
| fallos de `H = B-(1+s)E/2 = (1-s)(E/2-e')` | **0** |
| rango de `H/E` [la nota dice 0,038917 a 0,266228] | **0.038917 a 0.266228** |
| N0-N1 dentro de Delta a `m=8`, 39 celdas [dice 17,7%-25,6%] | **17.7200% a 25.6189%** |
| `Q, sU, Delta >= 0` | 0 celdas negativas |
| `R < 0` | **38 celdas de 234** |
| `s <= 1/2` | en todas |

Los tres numeros publicados son exactos, no redondeos amables. Y `R`
negativa no es una posibilidad teorica: ocurre en el **16%** de las
celdas medidas, lo que respalda que la nota insista en que "el simple
equilibrio par/impar no basta".

## Mordidas

### M3 (la seria). LEEME.md sigue proponiendo, como objetivo vigente, lo que Erizas demostro imposible

Castoras.md **si** retiro el objetivo: su cabecera dice "Erizas excluye
el margen uniforme ... se retira ese objetivo global del apartado
'Proximo ataque'", y en efecto su "Proximo ataque" pide controlar `H`
desde abajo **sin** la palabra "uniforme".

Pero `LEEME.md`, que es la puerta de entrada del frente, no recibio esa
correccion. En su seccion 5, dos parrafos seguidos dicen lo contrario:

> "No continuar intentando demostrar el margen uniforme global
> siguiente."
>
> "Ahora se busca una propiedad propagable de las leyes alcanzables que
> acote su margen H desde abajo, **con constante uniforme**."

Y no es una ambiguedad de vocabulario: la propia Castoras define
"margen uniforme" como `H >= epsilon(1-s)E` con `epsilon>0` fijo, y
demuestra que eso entrega `e' <= (1/2-epsilon)E` -- que es literalmente
`(E0)`, el enunciado que Erizas refuta para cada semilla fija.

Consecuencia practica: quien abra el frente por `LEEME.md` (que es lo
que la propia nota manda hacer) se lleva como tarea siguiente la unica
tarea que el frente ya sabe imposible. La retirada se aplico a la nota
y no se propago al indice.

### M4 (de reporte, la misma familia que M1 de la tanda 1). Se publica el rango de H/E y no su tendencia

La nota informa que `H/E` esta entre 0,038917 y 0,266228 en las 234
celdas. Cierto. Lo que no informa es que **cae con el tiempo**. Peor
`H/E` por arranque:

| arranque | t=12 | t=18 | t=24 | cociente 24/12 |
|---|---|---|---|---|
| 999983 | 0.172723 | 0.112392 | 0.069509 | **0.40** |
| 999999937 | 0.150660 | 0.088155 | 0.042741 | **0.28** |
| 1398101 | 0.116086 | 0.063039 | 0.081484 | 0.70 |

Como `H/E = (1-s)(1/2 - e'/E)`, esto es la misma senal que encontre en
la tanda 1 (`rho` subiendo hacia 1/2), vista desde el otro lado. Las 234
celdas no son apoyo neutro del objetivo "acotar H desde abajo": son su
**sombra numerica en contra**, y coinciden con lo que Erizas demuestra.

La nota deberia decirlo, sobre todo porque es el dato que justifica M3.

## Veredicto de la tanda 2

- **La identidad (C) es correcta.** La derive independientemente en sus
  tres pasos, cierra exacta en los dos testigos y en las 234 celdas
  registradas, y sus constantes (`N` frente a `2N`, el `2V`, el `O`) son
  todas las correctas. No encontre ningun error algebraico.
- **El cimiento es solido:** `paso` es la cadena real, verificado contra
  1,44 millones de pares enteros.
- **Los testigos son genuinos** (calculados por la ley, no escritos a
  mano) y refutan lo que dicen refutar, con el alcance correctamente
  limitado a leyes arbitrarias.
- **El Lean recompila sin `sorryAx`** y su alcance esta declarado con
  precision; la unica arista es el `0/0 = 0` de `Rat` en `exceso`, que
  hoy no muerde.
- **Dos mordidas:** una de documentacion con consecuencia real (M3, el
  indice propone un objetivo ya demostrado imposible) y una de reporte
  (M4, se publica el rango y no la tendencia adversa).

Esta tanda es, de las revisadas hasta ahora, la mas solida en su
matematica. Su problema no esta en lo que demuestra sino en lo que su
indice dice que hay que hacer despues.

## Reproduccion

    lean depuracion/frente20260910/balance.lean
    python revision12_adv1/rep_cadena_real.py
    python revision12_adv1/rep_testigos.py
    python revision12_adv1/rep_castoras.py
