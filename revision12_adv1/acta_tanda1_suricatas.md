# 12a REVISION ADVERSARIAL -- TANDA 1: SURICATAS / INVARIANTES

Revisor: Claude (Opus 5), sesion del 12-09-2026. Revision de a una tanda,
sin agentes. No se ha modificado ningun archivo del laboratorio: todo lo
de esta revision vive en `revision12_adv1/`.

**Objeto:** `depuracion/frente20260910/LEEME.md` secciones 2, 3 y 4;
`invariantes.lean`; `invariantes.py`; `contraccion.py` y sus salidas.

**Encargo atendido:** el que el propio LEEME dejo escrito en
"Revision adversarial pendiente" (cinco puntos).

## Alcance honesto de esta revision

Lo que SI pude verificar de forma independiente:

- Recompile `invariantes.lean` con el Lean instalado (4.32.2, el mismo
  que declara el LEEME). Salida en `relean_invariantes.txt`: exit 0, los
  cinco `#print axioms` reproducen exactamente `[propext, Quot.sound]` o
  ninguno. **Sin `sorryAx`. Confirmado, no de palabra.**
- Lei la prueba Lean paso por paso y la rehice a mano.
- Reimplemente los conteos desde las definiciones del LEEME, sin abrir
  `invariantes.py` (`rep_invariantes.py`).

Lo que NO puedo verificar y no pretendo: nada aqui sustituye a un
revisor humano con el contexto completo del programa.

## Punto a) Los dos mapas de Lean, son los de las corrientes compartidas?

**SI. Verificado contra la fuente, no contra el resumen.**

`correlacionafin.py` linea 13 y bloque C0 (lineas 134-160) define las dos
corrientes de la fibra k sobre el mismo padre par `c = 2u`:

    N0: u -> u          N1: u -> 3u + s_k,  s_k = (1-3^k)/2

y C0 lo comprueba en enteros para m=3..11, k=0..7, todo u. Luego
`tau_k(u) = 3u + s_k`, y

    tau_2(x) = 3x - 4      tau_3(x) = 3x - 13      tau_5(x) = 3x - 121

que son **exactamente** los tres mapas que aparecen en `invariantes.lean`
(`h2`, `h3`, `chi_invariante_cinco`). El mapa auxiliar es el correcto.

## Punto b) La traduccion de periodicidad en Int a funciones sobre residuos

**Resiste el ataque, y ademas por el lado dificil.**

La objecion natural seria que el Lean prueba algo sobre `f : Int -> A`
que no equivale a lo de `Z/2^m`. No es asi, y en el sentido bueno:

- Una funcion sobre `Z/2^m` es exactamente una `f : Int -> A` con
  `Periodica f (2^m)`, y como `3x - (3^k-1)/2` esta dada por una formula
  entera, la reduccion conmuta. La correspondencia es fiel en ambos
  sentidos.
- El Lean es de hecho **mas fuerte** que la version modular:
  `periodo_nueve` solo pide un periodo `n` con `3` no divide a `n`, no
  `2^m` en particular.
- La unica grieta real del argumento escrito ("tau_2 compuesta con tau_3
  inversa es la traslacion por 9") es que sobre **Int** esa inversa no
  existe: `(y+13)/3` solo esta definida cuando `3 | y+13`. El Lean **no
  esconde esa grieta, la tapa**: el lema `linea` se prueba solo bajo
  `(y+13) % 3 = 0`, y luego se cubren los otros dos residuos empujando
  con el periodo `n` (casos `x+n` y `x+2n`), usando que `3` no divide a
  `n`. Ese es el punto donde una formalizacion floja habria hecho
  trampa. No la hace.

Rehice la aritmetica de `periodo_uno`, que es el otro punto fino:
`9*2^m = 2^m + 4*2^(m+1)`, luego periodo 9 y periodo `2^m` dan periodo
`2^m` a un nivel menos, y la induccion baja hasta `pot2 0 = 1`. Correcto.

No hay vacuidad: las hipotesis son satisfacibles (f constante), la
conclusion es la fuerte, y `A` es un tipo generico -- no se cuela por un
codominio degenerado.

## Punto c) El argumento de igualdad en la norma de M2 M3

**Correcto. Lo rehice entero.**

Con `M_k = (I+P_k)/2` y `P_k` permutacion (ortogonal):
`||M_k v|| <= (||v|| + ||P_k v||)/2 = ||v||`, con igualdad solo si
`P_k v = v` (estricta convexidad de la bola euclidea). Si
`||M2 M3 v|| = ||v||`, la cadena `||v|| <= ||M3 v|| <= ||v||` fuerza las
dos igualdades: `P_3 v = v`, luego `M3 v = v`, luego `P_2 v = v`. Un `v`
fijo por ambos es constante por el lema de las Suricatas, y en media cero
constante quiere decir cero. La esfera unidad del subespacio de media
cero es compacta y el subespacio es invariante (las permutaciones
conservan la suma), asi que el supremo se alcanza y es `< 1`.

La reserva del LEEME ("el archivo Lean formaliza el lema de invariantes,
no las normas") es exacta y esta bien puesta.

## Punto d) Alguna conclusion presume gap uniforme o sustituye la cadena real?

**No encontre ninguna.** Al contrario: la seccion 3 se adelanta a las dos
objeciones ("No implica un margen uniforme en m" y "Tampoco identifica
M2 M3 con la excursion real: ... corrientes de ascenso y descenso,
cambios de fibra, pesos y condicionamiento a sobrevivir"), y la
correccion esta ademas grabada **dentro de los ficheros originales**
(`correlacionafin.py` linea 1082, `gapmezcla.py` lineas 3 y 145) con
fecha, en vez de borrar la conclusion vieja. Eso es lo correcto.

Confirmado tambien el hecho que sostiene la correccion: `C6` usa
`k = 2..K_ZOCALO` con `K_ZOCALO = 5` (linea 67), mientras `G3/G5` usan
`k = 3,5`. Son operadores distintos. La inferencia "G5 no refuta C6" es
valida: un invariante comun de un SUBCONJUNTO de mapas no tiene por que
serlo del conjunto entero.

## Punto e) Reproduccion de los conteos, sin leer su Python

`rep_invariantes.py`, escrito solo desde las definiciones del LEEME.
Salida completa en `rep_invariantes_salida.txt`.

| afirmacion del LEEME | mi reproduccion | veredicto |
|---|---|---|
| componentes comunes (3,5)=2, (2,3)=1, m=2..12 | 2 y 1 en los once m | **coincide** |
| 8.188 identidades de traslacion exactas | 8.188 comprobadas, 0 fallos | **coincide** |
| chi invariante bajo tau_3 y tau_5, no bajo tau_2, media cero | asi es, m=2..12, en enteros | **coincide** |
| energia(M2 chi)/energia(chi) = 1/2 | 1/2 exacto en `Fraction`, m=2..8 | **coincide** |
| SVD 0.707107 ... 0.931140, m=2..8 | identico a 12 decimales | **coincide** |
| barrido por defecto = 672 celdas | 14 x 4 x 12 = 672 | **coincide** |
| reproduccion de la ventana = 234 celdas | 3 x 13 x 6 = 234 | **coincide** |

Ademas verifique a mano, sin ordenador, por que los numeros son esos:
`tau_5` compuesta con `tau_3^{-1}` es la traslacion por `-108`, y
`v2(108) = 2`, luego el grupo generado alcanza `4Z` y las componentes de
(3,5) son las clases mod 4 pegadas por `tau_3(x) = -x-1 (mod 4)`, o sea
`{0,3}` y `{1,2}`: **dos**, y son exactamente el `chi` del Lean. La
coincidencia numerica no es una casualidad de implementacion.

## Mordidas

### M1 (de reporte, real). La seccion 4 informa "cero cruces de 1/2" y calla que rho sube hacia 1/2

`contraccion_reproduccion.txt`, salida del propio laboratorio, para el
arranque `c0=999983`:

    t=16  rho_lim_m = 0.369418740
    t=20  rho_lim_m = 0.424752063
    t=24  rho_lim_m = 0.449308207
    t=25  rho_lim_m = 0.450638970

y lo mismo en los otros dos arranques largos (0.391 -> 0.452,
0.395 -> 0.453). El "peor" de la ventana sube de ~0.42 (t=12..15) a
~0.454-0.460 (t=12..24) para los mismos arranques.

Por que importa. La condicion suficiente de la seccion 1 no pide
`rho(t,m) < 1/2` punto por punto: pide **un rho fijo** `< 1/2` valido
para todo `t >= T`. La seccion 1 lo dice ella misma y hasta da el
contraejemplo abstracto `rho_t = (t+1)/(2(t+2))`, cuyo producto decae
solo polinomicamente. Pues bien: ajustando `1 - 2 rho_t ~ c/t` a los
cuatro puntos de arriba sale `c ~ 4.2, 3.0, 2.43, 2.47` -- es decir, los
datos del laboratorio tienen **la forma exacta de su propio
contraejemplo numero 1**, no la de un rho fijo.

Consecuencia: el barrido no es evidencia neutra ("finito, no prueba
universal"), es evidencia **levemente adversa**: extrapolado, dice que
`sup_t rho = 1/2` y que la condicion suficiente de la seccion 1 es
**falsa**, no meramente indemostrada. Es un segundo motivo, independiente
de Erizas, para haber retirado esa ruta -- y el LEEME deberia decirlo,
porque hoy el lector se lleva la impresion contraria del titular "cero
cruces de 1/2".

Etiqueta: **medicion y extrapolacion sobre cuatro puntos**, no teorema.
No contradice nada demostrado; contradice el tono del resumen.

### M2 (menor, de etiqueta). Una mejora cobrada y no anotada

`C6` media el invariante comun trivial por union-find en `m = 4, 6, 8`
-- tres escalas. El lema de las Suricatas lo **demuestra para todo m**
(con `k=2,3`, que ya bastan, porque anadir `k=4,5` solo puede pegar mas).
O sea que la tanda subio `C6` de *medido en tres escalas* a *teorema en
todas*, y ni el LEEME ni la etiqueta grabada en `correlacionafin.py`
(que sigue diciendo "C6 es un calculo de componentes de permutaciones")
registran ese ascenso de etiqueta. Es la casa infra-declarando, que es el
error bueno, pero es un error de contabilidad igual.

## Aporte propio: la pregunta del margen uniforme queda mejor planteada

La seccion 3 cierra con "Esa ventana no determina su limite" y se queda
en `m=8`. Dos cosas que puedo anadir:

**(i) La sucesion es monotona no decreciente. Esto es demostrable, no
medible.** Sea `iota` la inclusion de funciones mod `2^m` en funciones
mod `2^(m+1)`. Como `tau_k` viene de una formula entera, la reduccion
conmuta y `iota . M_k^(m) = M_k^(m+1) . iota`; ademas `iota` multiplica
la norma por `sqrt(2)` y conserva media cero. El cociente de Rayleigh se
conserva, luego

    ||M2 M3||_m  <=  ||M2 M3||_(m+1)   para todo m.

Por tanto el limite `L = sup_m ||M2 M3||_m` **existe**, y la pregunta
"hay margen uniforme?" es exactamente la pregunta "es `L < 1`?".

**(ii) La ventana ampliada si decide la tendencia.** Estime la norma por
iteracion de potencia aplicando los operadores como permutaciones en
`O(2^m)` -- sin construir matrices, que es lo que ataba el calculo a
`m=8` (`rep_norma_limite.py`). Reproduce sus siete valores a 12 decimales
y sigue hasta `m=20`:

    m=10  0.951529827812      m=16  0.979228803351
    m=12  0.964946962761      m=18  0.983353902813
    m=14  0.973162819492      m=20  0.986106848532

El hueco `1 - ||.||` cae 0.0689 -> 0.0139 y el cociente entre huecos
sucesivos **sube** hacia 1 (0.79, 0.86, 0.88, 0.91, 0.92): decaimiento
sub-geometrico, sin ningun indicio de suelo. Ademas la iteracion de
potencia, si no converge del todo, **subestima**, asi que el error va en
la direccion segura.

Lectura: `L >= 0.9861`, y nada en el rango accesible sugiere `L < 1`.
Esto es **medicion**, no prueba -- pero convierte "no determina su
limite" en "la ventana ampliada apunta inequivocamente a `L = 1`", que
es lo que Erizas demuestra por otra via. Dos caminos independientes al
mismo entierro.

## Veredicto de la tanda 1

- El lema de las Suricatas: **correcto, y correctamente formalizado.**
  Recompilado por mi, sin `sorryAx`. Es un lema pequeno (la prueba a mano
  cabe en cuatro lineas) pero el Lean tapa la unica grieta real, que es
  la no invertibilidad de 3 sobre Int.
- Los mapas son los correctos, la reproduccion coincide en todo, y la
  correccion de alcance de G5 esta bien hecha y bien archivada.
- Las reservas de la seccion 3 son exactas; no encontre ninguna
  conclusion que presuma gap uniforme ni que sustituya la cadena real.
- **Dos mordidas**, ambas de contabilidad, ninguna estructural: el
  resumen del barrido omite que sus propios numeros van en contra (M1),
  y no registra una mejora de etiqueta que la tanda si cobro (M2).

La tanda **se sostiene**. No demuestra el teorema de conteo, ni P2, ni
densidad uno, ni Collatz -- que es exactamente lo que ella misma dice.

## Reproduccion

    lean depuracion/frente20260910/invariantes.lean
    python revision12_adv1/rep_invariantes.py
    python revision12_adv1/rep_norma_limite.py
