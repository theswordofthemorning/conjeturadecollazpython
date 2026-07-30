# Bitácora

Resumen corto por sesión. Lo detallado va en `CLAUDE.md`; esto es para saber en
diez líneas qué pasó y por dónde se iba. La entrada más reciente arriba.

---

## 2026-07-30 — el día de las correcciones

Sesión larga. **El saldo real no son los hallazgos: son las siete correcciones a
cosas que el repo daba por buenas.** Ninguna la encontró nadie de fuera.

### Lo que se midió nuevo

| | |
|---|---|
| **El umbral de los 45 rumbos** | El coral de Harriss **sí** se vuelve a juntar. Primer choque exacto en profundidad **31**; a la 59 es el 1–1,5% de los nodos. Verificado con resto cero módulo `Φ₄₅` en aritmética entera. La causa es `45 = 3²·5`, o sea el ángulo, no Collatz |
| **Los negativos son `3n−1`** | Identidad exacta, 8.095.665 pasos, 0 fallos. Tres ciclos, ningún cuarto hasta 10⁶. Y las dos reglas ciclan en **lados opuestos de `log₂3`**, forzosamente |
| **Las constantes** | Wagon `9,4779555…` (con entrada en OEIS) medida a 0,064%. La escalera `1:2:3` de las constantes de parada |
| **El ajuste fino** | `q = 3` es el único impar que converge. Pero el umbral `4` resultó ser `f = 1/2` reescrito, o sea Terras otra vez |
| **Collatz contra la moneda** | Entropía de exactamente `k` bits hasta `k=12` y a profundidad 128; pero `P(impar\|impar) = 0` exacto y el patrón **se puede encargar** (`2^4000−1` da 3.999 impares seguidos) |
| **El piso de la altitud** | Una **cota**, no una tendencia. Lo único de la sesión con forma de teorema |
| **La pinza de ciclos** | Barrido de 2.147 millones de restos. Recuperó **los cuatro ciclos de Collatz sobre `Z`** sin que se le hablara de negativos |
| **`k = 32`** | La cota inferior demostrada sube a **43,5658%**. `a(32) = 1.871.137.623` |
| **Los récords publicados** | 243 récords de Roosendaal y Barina traídos y cruzados contra el repo. Nada se rompe |

### Las siete correcciones

1. El `0%` de encimadas del coral **era falso** — sólo valía hasta 3.000 semillas.
2. El `1,7345` del coral **no es una constante**, es el valor de una muestra (se asienta en `1,7320`).
3. La fila "se escapan del rango" del A/B **no discrimina**: mide el rango, no la regla.
4. `2/ln(4/3)` es la constante del **atajo**, no del mapa clásico.
5. El par `(8k+4, 8k+5)` es de **Garner**, no de Lagarias.
6. `Wu–Huang 2001` **no se pudo verificar**: sin DOI, no está en Crossref, y Elia–Tucker no la citan.
7. **Al piso de la altitud le faltaba la hipótesis `n impar`** — sin ella es falso en 28.325 de 50.000 pares.

**La séptima es la que más enseña.** El piso se probó contra los **243 récords
publicados** —los números que más suben y más tardan de todo lo conocido— y
**pasaron los 243**. Lo cazó el barrido de control sobre números corrientes.
*Los extremos confirman; los controles refutan.*

### Dos negativos nuevos

- **Ninguna constante de Collatz coincide con ninguna constante fundamental.**
  Test con modelo nulo: `p = 0,317`, y **sube a 0,45** al corregir el nulo.
- **La racha inicial no predice la altitud** (correlación 0,59). Lo que hace es
  ponerle un piso exacto — cota sí, tendencia no.

### Vías que quedaron cerradas, con su razón

- **El barrido de restos está muerto.** Terras excluyó en 1976 todos los bucles
  de periodo ≤ 2.592, y nuestro `k` *es* ese periodo. Todo su rango alcanzable ya
  es teorema. Para territorio virgen harían falta `2^2592` restos: 781 cifras.
- **Las cribas no sirven para ciclos, y es estructural.** `T^k` es una biyección
  sobre `Z/2^k`: cada vector de paridad es una clase única. No hay nada que
  descartar. Una criba necesita que muchas clases compartan destino.
- **Los promedios no pueden demostrar nada** sobre un caso individual. La
  pregunta que queda como filtro permanente: **¿esto es un promedio o es una cota?**

---

## Lo que queda pendiente

### 1. El plan de la pinza, en tres fases

Lo que lo hace viable: **Hercher no usa el teorema de Baker en ninguna parte** —
toda la maquinaria diofántica entra como un número importado. Y la métrica del
esfuerzo, medida: **60 líneas de stdlib excluyen `m ≤ 82`**; todo el aparato del
paper (dos programas en C++, cinco semanas de cómputo) compra el tramo 82 → 91.

- **Fase 1** — traer `reimpl.py` al repo. 130 líneas, reproduce el Teorema 23
  dígito a dígito en 5,5 s. Sería el primer programa del laboratorio que
  reproduce matemática arbitrada.
- **Fase 2** — la escalera afín de Wang: un intervalo intersecado con una clase
  residual. *Eso es la pinza.* Media está construida en `clasesfusion.py`.
- **Fase 3** — **verificar a Wang**, no superarlo. Su preprint (`m ≤ 95`) tiene
  dos días, no está arbitrado y nadie lo ha comprobado. Si aguanta, se dice; si
  se cae, eso sí es un hallazgo.

### 2. El resto de la cola

- **El número primo de rumbos.** Predicción escrita y sin medir: con un número
  primo de rumbos el umbral de profundidad del coral debería dispararse. Barato.
- **Colorear el árbol de `collazarbol.py` con la rueda** mod 3.
- **El `+1` aparece ya tres veces** (grosor 0,2286 de la lámina, el `+2` del
  espejo base 2, la desviación −0,0035 de la fracción impar). ¿Son la misma
  cantidad? Sería lo único que **unifica** piezas en vez de acumularlas.
- **`clasesfusion.py` a `k = 34`.** Con `clasesparalelo.py` cuesta ~4× lo de
  `k=32`. No va a decidir la conjetura de Wu — los incrementos de la razón
  (`0,0050 → 0,0039 → 0,0037 → 0,0031 → 0,0027 → 0,0026`) encogen demasiado
  despacio para distinguir "geométrico" de "1/k" — pero alarga la única serie
  que puede.
- **OEIS.** `oeis_borrador.txt` está redactado y listo. **No se ha enviado**, y
  requiere una cuenta y una firma que son de una persona.

### 3. La deuda de método

**La sesión del 30-07-2026 casi no dejó código.** Casi todo se midió en scripts
sueltos fuera del repo y sólo quedó escrito en el `CLAUDE.md`. Sobrevivieron
`pinzaciclos.py`, `cruzarecords.py`, `records.json` y `clasesparalelo.py`; el
resto de las mediciones **no se pueden reproducir**. Es la deuda más concreta
que tiene el laboratorio.

---

## El objetivo, reformulado

> **No vamos a encontrar un número que haga bucle. Ni a demostrar que todos bajan
> a 1. Ni que exista uno que suba para siempre.**
>
> **Lo que sí se puede buscar es el cuarto camino: las reglas que generan todos
> los números de la secuencia de Collatz, sin generar la secuencia.**

Es alcanzable, se puede contradecir, y el repo ya tiene cuatro piezas antes de
que tuviera nombre: `mallaresiduos.py`, `clasesfusion.py`, `mallascerradas.py`, y
el Lema 8 de Hercher, que resultó ser el mismo objeto. Para calibrar: el
resultado más fuerte que existe sobre Collatz, **Tao 2019**, es de este tipo.
