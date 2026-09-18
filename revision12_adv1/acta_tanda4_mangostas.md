# 12a REVISION ADVERSARIAL -- TANDA 4: RELOJ DE LAS MANGOSTAS

Revisor: Claude (Opus 5), 12-09-2026. Cuarta tanda, de a una, sin
agentes. Nada del laboratorio modificado.

**Objeto:** `depuracion/frente20260910/Mangostas.md`, `rachas.lean`,
`rachas_salida.txt`, `rachas_ampliada.txt`.

**Encargo atendido:** el que la nota deja escrito -- "Revisar el enlace
entre el automata y la cadena original, el desfase entre L>=j y V(n), y
la medida de entrada de (M4). Atacar el paso de (M2) a (M6) en tiempos
de parada."

## Veredicto adelantado

**Todo lo que la nota afirma es correcto.** Verifique el mecanismo, la
ley (M1), la cota (M2), el conteo (M3), el desfase, la reduccion (M4),
la constante (M5), la identidad de `A`, el control (M6) y la correccion
del ejemplo de racha forzada. Cero discrepancias.

La unica mordida es que **(M6) es mas floja de lo necesario**, por un
factor logaritmico que su propia estructura regala.

## 1. El mecanismo, comprobado exhaustivamente

Los dos pasos compartidos son `c/2` y `(3c-D)/2` con `D = 3^k-1`, que
son exactamente las corrientes N0 y N1 de `paso` (ya verificado contra
pares enteros reales en la tanda 2).

La prueba descansa en dos hechos aritmeticos. Los comprobe por
enumeracion directa, `k = 2..14`, `c = -3000..3000` (`rep_mangostas2.py`):

| afirmacion | casos | fallos |
|---|---|---|
| si `0<r<A`: **los dos** hijos tienen `v2` exactamente `r-1` | 17.066 | **0** |
| si `2^A \| c`: **exactamente uno** sigue divisible por `2^A`, el otro cae a `v2 = A-1` | 21.934 | **0** |

El nucleo del paso 2 es que `u` y `3u-d` tienen paridades opuestas
cuando `d` es impar -- correcto, y `d` es impar precisamente porque
`A = v2(D)`. De ahi que cada bit fresco valga 1/2 para permanecer
arriba, y `L = G + A`. La cuenta `G+1` pasos hasta caer mas `A-1`
deterministas da `G+A`. **Correcto**, incluido el borde `A=1`.

Punto fino bien resuelto por la nota: la ley de `L` depende solo de
`r = min(v2(c), A)`, luego de `c` modulo `2^A`, **aunque** cual de las
dos ramas permanece dependa de `c` modulo `2^(A+1)`. Esa distincion es
justo la que hace que "NO depende de las valuaciones superiores de
entrada o de las recargas individuales" sea cierto. Es sutil y esta
bien.

## 2. (M2), (M3) y el desfase

- **(M2)** con colas exactas: **0 violaciones** de `P(L>=A+s) <= 2^-s`,
  y **125 igualdades exactas** confirmadas en la rama `r=A`, como la
  nota afirma. `E[L|k,c] <= A+1` con igualdad en esa rama.
- **(M3)** `V(A,r,n)`: reproduje la formula por conteo directo,
  **0 discrepancias**. Verifique tambien a mano por que
  `V = 2^(A-1)` es constante en `n >= A`: sumando `2^(j-1)` para
  `j=1..A-1` mas la palabra que nunca baja da `2^(A-1)-1+1`.
- **El desfase.** `P(L>=j) = V(A,r,j-1)/2^(j-1)` es correcto, y el
  aviso "no confundir `L>=n` con seguir par tras `n` pasos, que es
  `L>n`" es exacto. **Es la clase de error de indice que suele colarse
  y aqui esta cazado de antemano.** Comprobe la consistencia entre
  (M1) y (M3): ambas dan `P(L>=j) = 2^(A-j)` para `j > A`.

## 3. La identidad de A y la correccion del ejemplo

`A = 1` si `k` impar, `A = 2+v2(k)` si `k` par, y `2^A <= 4k`:
**verificado para `k = 1..2999`, 0 discrepancias.** La derivacion por
LTE (`v2(3^k-1) = v2(2)+v2(4)+v2(k)-1 = 2+v2(k)` para `k` par) es
correcta.

La correccion del ejemplo de racha forzada, punto por punto:

| afirmacion de la nota | comprobado |
|---|---|
| `(2,1398101)` --mixto bit 0--> `(3, 2^21)` | si, `2097152` |
| en `k=3`, `A = v2(26) = 1` | si |
| `P(L>=21) = 2^-20`, no 1 | si (cola geometrica exacta verificada `j=2..16`, y el mecanismo la extiende) |
| bit compartido 1 inmediato da `c=3145715`, impar, `L=1` | si |
| la palabra de ceros si realiza 21 pasos | si |

Esta es una **autocorreccion real**: el laboratorio retira su propia
lectura de "racha forzada de 21 pasos" y la sustituye por la ley
correcta. `rachas.lean` incluso certifica el conteo del caso
(`adversarial_cuenta : vivos 1 1 20 = 1`), que es exactamente el
`2^-20`. Bien hecho y bien archivado.

## 4. (M4) y (M5)

Derive (M4) por mi cuenta separando `A>=j` (donde `L>=j` equivale a
`2^j | c`) de `A<j` (donde solo contribuyen las entradas altas, con
peso exacto `2^(A-j)`), y comprobe la identidad sobre una mezcla
sintetica de 40 entradas: **0 discrepancias en `j=1..14`**. La
constante `C_cola` de (M5) resulta en efecto constante para todo
`j > Amax` y coincide con `E[2^A 1_{2^A|c}]`.

La reserva de la nota tambien es correcta y necesaria: **no** hay
constante uniforme sobre todas las mezclas, porque una entrada con
`2^A|c` y `A` grande exige `C >= 2^A`. La nota lo dice.

## 5. El paso de (M2) a (M6), que la nota pedia atacar

Lo ataque y **aguanta**. La union sobre las `n` rachas no necesita
independencia: (M2) es condicional al estado de entrada completo, los
bits futuros son frescos, y la torre de esperanzas da
`P(existe i: L_i >= a_n+s) <= n 2^-s` sin mas. Las rachas inexistentes
tras salir aportan cero, asi que `n` es cota del numero de sumandos.
Y `a_n >= A_i` esta garantizado porque `A_i <= 2+v2(k_i) <= 2+log2(k_i)`
y `k_i <= k0+n`. El bloque racha+mixto cabe en `a_n+s+1` con holgura.
Correcto.

## Mordida

### M6. El control (M6) pierde un factor logaritmico que no hace falta perder

(M6) acota `T_n` por `n * (a_n+s+1)`: es decir, acota la **suma** de las
rachas por `n` veces el **maximo**. Eso cuesta un `log n` por dos vias a
la vez: usa el peor `a_n` para todas las rachas, y usa
`s = techo(3 log2(n+1))` para que la union aguante.

Pero la media ya da `O(n)` sin ninguna union. Medi la ley de alturas de
la cadena real en `t=24` (`rep_mangostas_holgura.txt`):

    E[A] sobre las alturas visitadas = 397430/169127 = 2.3499
    max A = 6      a_n que (M6) aplica a TODAS las rachas = 6

O sea: (M6) le cobra 6 (mas `s`) a cada racha cuando el promedio real
es 2,35. Con `E[L|entrada] <= A+1` y linealidad,
`E[T_n] <= n(E[A]+2) = O(n)`.

Y la concentracion tambien esta al alcance sin el logaritmo: por (M1)
la racha es `A_i + G_i` con `G_i` condicionalmente `Geom(1/2)`, y una
suma de geometricas condicionales concentra en `O(n)` con colas
exponenciales por un argumento de supermartingala sobre la funcion
generatriz -- que **no** necesita independencia, exactamente igual que
la union que la nota ya usa. El unico termino que puede traer un
logaritmo es `sum_i v2(k_i)`, y solo si las alturas se concentran en
potencias altas de 2, cosa que los datos del propio laboratorio
desmienten.

Consecuencia: **el reloj es `O(n)`, no `O(n log n)`**, y la nota se
esta cobrando menos de lo que su propia (M1) le da. Igual que en
Erizas con el exponente 3/4, la casa infra-declara. Aqui importa mas
que alli, porque LEEME anuncia "un control `O(n log n)` del reloj" como
el resultado de la tanda, y el resultado disponible es mejor.

Etiqueta: `E[A]=2.3499` es **medicion** sobre la cadena real en `t=24`;
`E[T_n] = O(n)` es consecuencia de (M1) mas esa medicion, no un teorema
todavia.

## 6. El Lean

`lean depuracion/frente20260910/rachas.lean`: exit 0, **11 resultados**,
salida identica a `rachas_lean.txt`, **sin `sorryAx`**.

Y no afirma de mas: son los seis lemas aritmeticos del mecanismo
(`hijos_altos`, `paridades_altas`, `factor_par/impar`, `hijos_bajos`,
`paridades_bajas`), la funcion `vivos` con `conteo_bajo` y
`conteo_alto` --que es (M3) por induccion para TODOS los parametros--
y tres comprobaciones del ejemplo adversarial. La ley probabilistica
(M1) **no** esta en Lean, y la nota lo declara ("Tampoco se formaliza
una biblioteca de probabilidad"). Declaracion exacta.

## 7. Dos errores mios, anotados

Mi primera version del script daba 130 violaciones de (M2) y 19 fallos
de (M4), y `P(L>=21) = 2^-20 - 2^-39` en vez de `2^-20`. Los tres eran
**mios**: truncaba la enumeracion a profundidad finita y perdia la cola.
Con colas exactas (`P(L>=j)` = masa que sigue par tras `j-1` pasos)
desaparecen los tres. Lo dejo escrito porque el sintoma --una cola
corta por un epsilon del tamano de la truncatura-- es facil de
confundir con un error de la nota, y no lo era.

## Veredicto de la tanda 4

- **La ley (M1) es correcta y su mecanismo esta verificado
  exhaustivamente.** Es, matematicamente, el resultado mas limpio y
  cerrado del frente: una ley exacta, no una cota.
- (M2) a (M5) correctas, con las igualdades donde la nota dice que hay
  igualdad.
- El paso a tiempos de parada, que la nota pedia atacar, **aguanta**.
- La autocorreccion del ejemplo de racha forzada es real y esta bien
  documentada.
- **Una mordida (M6):** el reloj declarado `O(n log n)` es en realidad
  `O(n)`; la nota se cobra de menos.

Y sigue en pie lo que la propia nota advierte, que es el cuello del
frente entero: "Condicionar a sobrevivir un horizonte FUTURO puede
sesgar los bits y requiere otro argumento; no esta incluido." Eso es
la tanda 5.

## Reproduccion

    lean depuracion/frente20260910/rachas.lean
    python revision12_adv1/rep_mangostas2.py
