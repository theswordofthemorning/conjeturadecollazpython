# Perdices: repeticiones, representantes y complejidad de la palabra

11-10-2026. Continúa [Cancelaciones](CANCELACIONES.md), cuya tarea pendiente
era acotar el crecimiento de los representantes en historias no periódicas
de una misma semilla. Resultado: una ley exacta y elemental que acota **toda**
repetición temprana y excluye las palabras de complejidad baja, sturmianas
incluidas. En Lean queda el enunciado completo para racionales: ningún p/q con
q impar tiene palabra de paridades sturmiana (§4). También se identifica con
precisión la frontera: la ley no alcanza a las historias genéricas, y los
peores casos medidos son genéricos.
**MuroB y Collatz siguen abiertos.** No se reclama prioridad (§6).

## 1. Mapa, índices y cuantificadores

Atajo T sobre naturales: n/2 si n es par y (3n+1)/2 si es impar.
`x_t=T^t(n)`; `S_t` cuenta los impares entre `x_0,...,x_(t-1)`. El factor de
largo m en el instante t son las paridades de `x_t,...,x_(t+m-1)`. Hay una
**repetición** (i, j, m) si los factores de largo m en i<j coinciden;
`d=j-i` y `s=S_j-S_i`. La complejidad `p(m)` es el número de factores
distintos de largo m. No hay ley aleatoria ni condicionamiento.

## 2. La ley de repetición

Tres piezas, las tres en Lean:

1. Mismas m paridades desde dos números equivalen a congruencia módulo `2^m`
   (`CasaRetrato.misma_paridad_congruentes`; el recíproco es
   `CasaTerras.congruentes_mismo_baile`).
2. `x+1` se multiplica exactamente por 3/2 en cada paso impar y no crece en
   cada paso par: `2^(S_t)(x_t+1) <= 3^(S_t)(n+1)` (`cota_impares`).
3. Dos naturales distintos y congruentes módulo `2^m` distan al menos `2^m`.

Juntas dan, si `x_i ≠ x_j`:

```text
local:   2^(m+s)   < 3^s   (x_i+1)                       (1)
global:  2^(m+S_j) < 3^S_j (n+1)                          (2)
```

Es decir, `m < log2(3/2)·S_j + log2(n+1)`: una repetición no puede durar
más que el tamaño acumulado. La hipótesis es necesaria: en el circuito
1→2→1 hay repeticiones de cualquier largo con valores iguales.

**Sin inyectividad.** Si el tramo entre las dos apariciones es expansivo,
`2^d <= 3^s`, y `x_i>=1`, entonces `x_i ≠ x_j`: un circuito natural tiene
pronóstico de vuelta menor que 1 (`CasaRetrato.ciclo_cruza`). Así (1)–(2)
valen para toda semilla `n>=1` (`ley_expansiva`, `representante_crece`).

(1) generaliza el presupuesto de [Repeticiones](REPETICIONES.md), (1): permite
copias parciales, bloques variables y una constante explícita. Allí `H=max(C,E)`
dependía del bloque; aquí sólo cuentan s, S_j y la semilla.

## 3. Representantes de historias no periódicas

Sea W una palabra finita y `r(W)` el menor natural que la realiza. Para
cada repetición (i, j, m) dentro de W con tramo expansivo,

```text
r(W)+1 > 2^m (2/3)^(S_j).                                 (3)
```

En la clase `1`/`110` y en sus historias F, (3) vale para **toda** repetición,
aunque el tramo corto entre ambas apariciones no sea expansivo (por ejemplo
`0110`). Con m<=1 es trivial, porque `S_j>=1` y `r(W)>=1`. Con m>=2, si fuera
`x_i=x_j` la cola sería `V^ω`, con `V=W[i,j)`; sus factores de largo 3 ya están
en W, así que evita 00 y 010. Entonces V tiene al menos 2/3 de unos, luego
`3^s>=3^(2d/3)>2^d`, y `ciclo_cruza` lo prohíbe. Esta reducción es escrita sobre
los lemas Lean.

Los representantes crecen exponencialmente a lo largo de cualquier historia con
repeticiones tempranas largas. Por eso ninguna órbita inyectiva tiene palabra
de exponente diofántico mayor que `1+log2(3/2)·ρ̄`, con ρ̄ la densidad
superior de unos: a lo sumo `log2 3≈1,585`. Esta traducción asintótica es
escrita; Lean certifica las desigualdades enteras.

**Un ejemplo que no es de complejidad mínima.** Sea la palabra de Thue–Morse
sobre A=`1` y B=`110`. Empieza por la codificación de `μ^k(011)=UVV`, con
`|U|=|V|=2^(k+1)` paridades y `S_j=3·2^k` impares en UV. (2) exigiría
`2^(k+1)<0,585·3·2^k+log2(n+1)`, imposible para k grande, y el tramo V es
expansivo (3/4 de unos). Ningún natural la sigue. La cota crece como
`0,245·2^k` bits: 63 bits en k=8, prefijo de 1536 pasos (cotejo).

## 4. Complejidad

**Identidad exacta.** Por las dos direcciones de §2.1, dos instantes tienen el
mismo factor de largo m si y sólo si sus valores son congruentes módulo `2^m`.
Por tanto `p(m)` es exactamente el número de clases módulo `2^m` que visita la
órbita. En `3x+q`, la equivalencia está en Lean (`factor_iff`, con
`congruentes` y `mismas_paridades`); cotejo de 317 952 pares.

**Cota formal.** En una órbita inyectiva, los instantes con valor menor que
`2^m` tienen factores distintos (`factores_distintos`, `complejidad_cota`). Si
`3^K(n+1) <= 2^(m+K)`, los valores `x_0,...,x_K` quedan bajo `2^m`
(`bajo_umbral`) y sus K+1 factores son distintos (`factores_iniciales`):

```text
p(m) >= floor((m - log2(n+1)) / log2(3/2)) + 1  ≈ 1,71·m.  (4)
```

Con `m>=5(n+1)` basta `K=m+1` (`umbral_explicito`, por Bernoulli entero
`3^m(3+m) <= 3·4^m`): los m+2 primeros factores son distintos
(`mas_que_sturmiana`). Una palabra sturmiana tiene exactamente m+1 factores
de cada largo. Luego **ningún natural tiene palabra de paridades sturmiana**:
si su órbita es inyectiva lo impide (4); si no, la palabra es eventualmente
periódica (en Lean, `natural_sin_palabra_sturmiana`, abajo). Más en general, toda órbita inyectiva cumple
`liminf p(m)/m >= 1/log2(3/2)≈1,71` (`no_inyectiva_si_pocos_factores`
certifica la forma finita).

**Racionales, en Lean.** Con `x=p/q` y q impar positivo, la órbita del atajo
es `p_t/q`, con `p_(t+1)=Tq(p_t)` para el mapa `3x+q` sobre enteros (la
correspondencia usual para órbitas racionales). En
[PerdicesRacional.lean](PerdicesRacional.lean) el argumento usa `|x|+q` en lugar de `x+1`
y cierra también el caso no inyectivo:

- `congruentes` y `mismas_paridades`: mismas k paridades bajo `3x+q` equivalen
  a congruencia módulo `2^k` (`factor_iff`);
- `cota`: `2^(S_t)(|x_t|+q) <= 3^(S_t)(|p|+q)`;
- `inyectiva_no_sturmiana`: con `m=9(|p|+q)`, los m+3 primeros factores de largo
  m+1 son distintos;
- `repetida_no_sturmiana`: si la órbita repite un valor en i y en i+d, la
  palabra tiene a lo sumo i+d factores de largo i+d;
- **`sin_palabra_sturmiana`**: para todo q impar positivo y todo entero p, la
  palabra de paridades de p bajo `3x+q` no tiene exactamente m+1 factores de
  cada largo m. `natural_sin_palabra_sturmiana` lo enlaza con el `T` natural;
- **`racional_sin_palabra_sturmiana`**: lo mismo para todo racional x de
  denominador impar bajo el atajo sobre `ℚ`, cuya paridad es la del numerador.
  `num_div_impar`, `TQ_div` e `iter_TQ` prueban `TQ^t(a/q)=(Tq^t a)/q`.

Es, en forma contrapuesta, el enunciado del preprint de De Jesus (§6): Φ lleva
toda palabra sturmiana a un 2-ádico irracional. La prueba aquí es otra y más
corta, y la formalización es una verificación independiente. Lean certifica el
enunciado tal como queda definido: palabra sturmiana = exactamente m+1 factores
de cada largo; la identificación con la conjugación Φ es la usual (§6).

## 5. La frontera

La ley sólo usa el tamaño de los valores. No toca las palabras con
`p(m) >= 1,71·m`: todas las genéricas, y en particular casi todas las de
`{1,110}^ω`, cuyo lenguaje crece como `1,4656^m` (raíz de `x^3=x^2+1`).
Un argumento por congruencias de una sola repetición tampoco puede dar más:
para un objetivo racional, la cota de Liouville 2-ádica es óptima.

**Medición inicial en la clase `1`/`110`.** `λ(n)` es el mayor largo L tal que
las L primeras paridades de n forman un prefijo de `{1,110}^ω` (empiezan por
11 y evitan 00 y 010). Una búsqueda por niveles con representantes menores que
`2^36` da el menor natural con `λ>=L`:

| L | 6–10 | 11–13 | 21–35 | 36 | 46–53 | 59–65 | 66–71 | 72–81 | 82 |
|---|---|---|---|---|---|---|---|---|---|
| mínimo | 27 | 91 | 4591 | 159487 | 6416623 | 120080895 | 3156298491 | 4081276143 | `>=2^36` |

Ningún `n<2^36` sigue la clase 82 pasos. Como cada mínimo cumple
`mínimo^3 >= 2^(L-1)` (comprobación entera), todo `n<2^36` cumple
`λ(n) <= 3 log2(n) + 1`. Hay igualdad en n=1; fuera de ese caso, el más
ajustado es 4591, con 35 pasos y cociente `(L-1)/log2 n≈2,79`.
**Ampliación auditada:** [Salidas](SALIDAS.md) conserva el censo por profundidad
hasta `2^50`: máximo λ=112, alcanzado primero en 338203040342655, y la misma
desigualdad en todo el dominio. El solapamiento con la tabla anterior coincide;
la auditoría independiente completa llega a 16 bits, sin repetir el censo grande.

**Conjetura:** esa desigualdad vale para todo n>=1. Implicaría MuroB en esta
clase. En lenguaje de Syracuse, `x -> (3x+1)/2^v` con `v=v2(3x+1)`: A=`1`
aporta el exponente 1 y B=`110` los exponentes 1 y 2. La clase es, pues, la de
los impares cuyos exponentes son siempre 1 o 2, empiezan por 1 y nunca tienen
dos 2 seguidos. La conjetura dice que ninguna órbita mantiene esa regla más de
unos `3 log2 n` pasos del atajo. Sin la regla «nunca dos 2», el circuito del 1
(exponente 2 para siempre) la cumpliría. La heurística aleatoria da `2^(0,4485 L)`, compatible con la tabla.
Los récords **no son repetitivos**: en los 24 mínimos de la tabla, (3) acota a
lo sumo 12 bits (3156298491, de 32); para 4081276143 da 5 de 32. Los peores
casos son genéricos, y la ley no los alcanza.

Conclusión para la ruta: controlar los representantes de todas las historias
no periódicas equivale a MuroB en la clase. Las repeticiones ya están agotadas
como herramienta: ninguna cota que dependa sólo de ellas pasa de (4).

## 6. Prioridad y fuentes

El paso «mismas paridades ⇒ congruencia» es la biyección clásica (Terras 1976;
Lagarias 1985; Bernstein–Lagarias 1996, isometría 2-ádica). López–Stoll,
*The 3x+1 conjugacy map over a Sturmian word*, Integers 9 (2009) A13, calculan
Φ en palabras mecánicas de intercepto cero y dicen que se desconoce si alguna
palabra aperiódica tiene imagen periódica. En septiembre y octubre de 2026
aparecieron, sin arbitraje y **sin leer aquí sus textos completos**:

- E. De Jesus, *The 3x+1 Conjugacy Map Sends Every Sturmian Word to an
  Irrational 2-adic Integer*, Zenodo, 10.5281/zenodo.23108370, v5 del
  02-10-2026. La ficha del registro confirma el título, el autor, la fecha y
  el enunciado: toda pendiente, intercepto y palabra inferior o superior. El
  método citado son aproximantes de fracción continua y cotas efectivas de
  altura. Del mismo autor se indexa una cota de complejidad «drift-sensitive».
- Un PR público, innerlightr-wq/eoc-divergence #5, del 23-09-2026, con un paso
  de Liouville para la palabra sturmiana de pendiente crítica `log_3 2`.

El corolario sturmiano **no es nuestro**. Aquí se usa otra vía, el conteo de
residuos de §4. Lo propio es la forma entera de (1)–(4), su formalización, la
medición de §5 y el uso de todo ello para delimitar esta ruta.

**Antecedente anterior, agregado el 16-10-2026** ([Judas J2 §5](../judas20261016/J2_MECANISMOS.md#5-prioridad-la-cota-de-complejidad-ya-estaba-en-2009)).
A. Dubickas, «On integer sequences generated by linear maps», Glasgow Math.
J. 51 (2009) 243–252, Teorema 5, leído completo: toda órbita divergente del
atajo tiene `P(X,n)>1,70951129·n` para n grande. La constante es
`log 2/log(3/2)` y la prueba es la de §4: mismo factor implica congruencia
módulo `2^m`, y el crecimiento es a lo sumo `(3/2)^n`. En naturales, una órbita
inyectiva tiende a infinito, así que la cota (4) y el corolario sturmiano para
naturales ya están ahí. Las filas del registro que citan sólo a De Jesus deben
citar también este trabajo.

## 7. Evidencia

[PerdicesComplejidad.lean](PerdicesComplejidad.lean): 17 teoremas.
[comprobar_complejidad.py](comprobar_complejidad.py) audita 27 módulos previos
y compila sólo el nuevo: 28 módulos, 346 consultas, Lean 4.32.2, sólo
`propext`, `Classical.choice` y `Quot.sound`, sin avisos ni `sorry`.
[Evidencia](evidencia_complejidad.json) y [salida](evidencia_complejidad.txt).
[PerdicesRacional.lean](PerdicesRacional.lean): 22 teoremas;
[comprobar_racional.py](comprobar_racional.py) audita los 28 anteriores: 29
módulos, 368 consultas, mismos axiomas. [Evidencia](evidencia_racional.json) y
[salida](evidencia_racional.txt). Revisión humana pendiente.

[cotejar_complejidad.py](cotejar_complejidad.py), enteros y Fraction, con
implementaciones independientes de las del módulo:

- n=0..255, 48 pasos: 239 372 repeticiones con valores distintos cumplen (1)
  y (2); peor cociente 64/123. Las 49 396 cíclicas quedan fuera; 36 006 violan
  la cota, y todas las de valor positivo tienen tramo contractivo.
- 317 952 pares: factor igual si y sólo si residuo igual.
- 549 pares (n, m) con `x_0..x_K` distintos: factores distintos; Bernoulli
  hasta m=400 y el umbral `m>=5(n+1)` en 64 valores por semilla.
- Diez palabras sturmianas, cinco pendientes cuadráticas y dos interceptos,
  400 pasos: complejidad m+1 hasta m=12; representantes mínimos exactos y (3)
  en todos los cortes. Incluye la pendiente contractiva `(√5-1)/2`.
- `3x+q`, q impar hasta 9, numeradores −64..64: 119 564 repeticiones.
- Familia `2^L-1`: cociente local exacto 1/3, L=2..64.
- Thue–Morse sobre A/B, k=1..8: la ley en `μ^k(011)` y representantes exactos.
- Clase `1`/`110`: tabla de §5, hasta 578 949 clases por nivel; L<=30
  repetido por fuerza bruta independiente; desigualdad `mínimo^3>=2^(L-1)`
  y bits acotados por (3) en los 24 récords. **Es medición, no prueba.**

[Resultado](cotejo_complejidad.json). [cotejar_racional.py](cotejar_racional.py),
con q impar hasta 15 y p entre −64 y 64, coteja las dos ramas de
`sin_palabra_sturmiana`: 6695 casos de la rama inyectiva en forma finita, 1032
órbitas periódicas con a lo sumo i+d factores (se alcanza en p/q=1/7) y el
umbral `m=9(|p|+q)`; con `Fraction` reducida repite 66 048 pasos del puente
sobre ℚ. Los representantes racionales de 50 prefijos sturmianos
tienen casi tantos bits como el prefijo: no se estabilizan
([resultado](cotejo_racional.json)). No se relanzan censos anteriores.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_complejidad.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_complejidad.json
python -B -X utf8 depuracion/perdices20261007/cotejar_complejidad.py --nmax 255 --pasos 48 --mmax 8 --kmax 24 --largo-sturm 400 --lmax-ab 90 --cota-bits-ab 36 --lmax-bruto 30 --pmax 64 --qmax 9 --salida depuracion/perdices20261007/cotejo_complejidad.json
python -B -X utf8 depuracion/perdices20261007/comprobar_racional.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_racional.json
python -B -X utf8 depuracion/perdices20261007/cotejar_racional.py --qmax 15 --pmax 64 --mmax 24 --largo 400 --salida depuracion/perdices20261007/cotejo_racional.json
```

Si faltan objetos previos, reproducir primero [Cancelaciones](CANCELACIONES.md).
