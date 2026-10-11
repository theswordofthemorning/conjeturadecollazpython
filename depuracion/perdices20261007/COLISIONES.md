# Perdices: colisiones, sumabilidad y exclusión del planeador

**Continuación del mismo día:** [Cola](COLA.md) formaliza el piso,
la dinámica y el límite relativo de la cola real. La exclusión de
esta nota permanece vigente; cohete y grieta siguen abiertos.

10-10-2026. Continúa [Novena](NOVENA.md) y sustituye su siguiente paso.
Se conserva el nombre Perdices. **Resultado:** toda órbita positiva
inyectiva tiene suma de recíprocos finita, tamaño normalizado acotado
y `P_k -> infinito`. En particular, una fuga pura no puede ser un
planeador intermitente. Quedan abiertos el cohete y la grieta; Collatz
no está demostrado. Revisión humana pendiente.

El principio de colisiones tiene un antecedente directo en Garcia–Tal
(1999). Se desarrolla y formaliza aquí una prueba con constantes
explícitas para intervalos que empiezan en cero. **No se reclama
prioridad matemática.**

## 1. Mapa, índices e hipótesis

Atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar, sobre naturales.
Para una semilla fija n, `x_j=T^j(n)`, `S_k=#{j<k:x_j impar}`,
`P_k=3^S_k/2^k` y `R_k=x_k/P_k`. Un paso es una aplicación de T.
No hay ley aleatoria ni condicionamiento probabilístico.

La cuenta de imágenes incluye n=0 y vale sin hipótesis orbitales.
La suma temporal y el producto requieren n>0 e inyectividad de
`j -> x_j` en **todos** los índices naturales. `FugaPura n` aporta
esas condiciones mediante los lemas existentes de CasaRetrato.
No se afirma que exista una fuga pura ni que un prefijo finito
certifique la inyectividad infinita.

## 2. Por qué contar imágenes restringe una órbita

Si `T^k(x_i)=T^k(x_j)`, entonces `x_(i+k)=x_(j+k)`.
La inyectividad orbital implica i=j y x_i=x_j. Así, cada iterado
`T^k` es inyectivo en el conjunto de valores de esa órbita.

Por tanto, para cualquier conjunto finito A de valores orbitales
menores que N,

```text
|A| = |T^k(A)| <= |T^k({0,...,N-1})|.                    (1)
```

Aquí se usa más que la ausencia de repeticiones en A: se usa que
sus valores tampoco pueden coalescer en el futuro. Por ejemplo,
el prefijo `4,2,1` no repite valores, pero sus imágenes por T²
son `1,2,1`. Aplicarle (1) como igualdad sería incorrecto.

## 3. Una cota explícita para la imagen

Fijar m>=0, k=100m y N=2^k. Separar las entradas n<N según
`S_k(n)>=60m` (muchas subidas) o `S_k(n)<60m`.

**Muchas subidas.** La correspondencia de paridades inyecta las
entradas n<N en los subconjuntos de `{0,...,k-1}`. Cada patrón
con s subidas recibe peso 2^s y el peso total es `(1+2)^k=3^k`.
Luego su número B cumple

```text
B*2^(60m) <= 3^(100m) <= 2^(159m),
B <= 2^(99m),                                           (2)
```

pues `3^100<2^159`. Son pesos de un conteo exacto; no se atribuye
una distribución de paridades a una semilla fija.

**Pocas subidas.** Para todo n,k naturales,

```text
2^k (T^k(n)+1) <= 3^S_k(n) n + 3^k.                     (3)
```

Lean prueba (3) directamente por inducción sobre los pasos. Como
derivación independiente, escribir `2^k T^k(n)=3^S_k n+B_k`.
La composición afín da B_0=0; en un paso par B no cambia y en
uno impar `B_(k+1)=3B_k+2^k`. Inducción da
`0<=B_k<=3^k-2^k`, de donde (3). No hace falta un primer cruce.

Si S_k<60m, entonces `3^S_k<=3^(60m)<=2^(96m)` por `3^5<2^8`.
Usando n<2^(100m) en (3),

```text
T^(100m)(n)+1 <= 2^(96m)+2^(59m) <= 2*2^(96m).
```

Estas salidas caben en un intervalo de `2*2^(96m)` naturales.
Las demás aportan a lo sumo B salidas, aunque haya colisiones.
Por (2),

```text
|T^(100m)({0,...,2^(100m)-1})| <= 3*2^(99m).              (4)
```

El caso m=0 también está incluido. Combinando (1) y (4), cualquier
conjunto finito A de valores de una órbita inyectiva satisface

```text
#{a en A: a<2^(100m)} <= 3*2^(99m).                      (5)
```

La constante no depende de la semilla ni de la longitud del prefijo.
No es una estimación en promedio ni exige enumerar 2^100 entradas.

## 4. Recíprocos y producto corrector

En el anillo `2^(100m)<=a<2^(100(m+1))`, (5) implica

```text
sum 1/a <= 3*2^(99(m+1))/2^(100m) = (3*2^99)*2^(-m).
```

Sumando geométricamente todos los anillos,

```text
sum_{j<k} 1/x_j <= 3*2^100, para todo k;
sum_{j>=0} 1/x_j < infinito.                             (6)
```

Lean empieza con conjuntos finitos positivos: la suma hasta el
anillo M, más la cola geométrica `2*(3*2^99)/2^M`, no supera
`2*(3*2^99)`. Todo conjunto finito cabe en algún corte. Sólo después
se pasa a índices orbitales, usando su inyectividad, y se aplica
el criterio de sumas parciales no negativas acotadas.

La identidad ya formalizada en PerdicesTamano es

```text
R_k = n producto_{j<k, x_j impar} (1+1/(3x_j)).
```

Por `1+t<=exp(t)` y (6),

```text
n <= R_k <= n exp(2^100),
R_k -> ξ, con n<=ξ<=n exp(2^100)<infinito.                (7)
```

El límite existe porque R_k es monótono. Todo este paso, incluido
el límite real, está formalizado. La constante es deliberadamente
muy grande: sólo se necesita finitud.

Una órbita inyectiva de naturales termina fuera de cualquier
conjunto finito, luego x_k->infinito. Como `x_k=P_k R_k` y (7)
da una cota superior fija para R_k,

```text
P_k -> infinito.                                        (8)
```

En forma explícita: para cada C>0 existe K tal que k>=K implica
P_k>C. Para FugaPura, Lean da en naturales
`forall c, exists K, forall k>=K, 3^c*2^k<3^S_k(n)`.
Esto niega exactamente la alternativa de regresos infinitos que
define al planeador intermitente en CasaPlaneador.

## 5. Qué cambia en la investigación

La exclusión no necesita la cota superior de duración buscada en
[Novena](NOVENA.md). Sus cotas finitas siguen siendo válidas;
las condiciones sobre infinitos regresos tienen ahora una premisa
imposible bajo FugaPura. Se conserva su evidencia histórica.

La revisión de [Mahler](../mahler20261007/LEEME.md) se precisa:
un cohete positivo inyectivo **siempre** tiene ξ finito. La posibilidad
antes contemplada de un cohete lento con ξ=infinito queda excluida
para estas órbitas. Por la identidad afín, también converge la suma
de 1/P_j sobre los índices impares; esta última formulación se deduce
aquí por escrito, sin un nuevo lema Lean específico.

Eso no excluye los cohetes ni fija una tasa puntual de crecimiento
de P_k. Tampoco transforma un cruce previo en descenso: las grietas
siguen abiertas. El método de ventanas de Mahler no adquiere por
ello una ventana aplicable a Collatz.

**Siguiente trabajo:** estudiar para un hipotético cohete la cola
`t_k=ξ P_k-x_k=(1/3) sum_{j>=k, impar} P_k/P_j`, ahora válida para
toda fuga pura. Buscar una restricción aritmética de esa cola y
del entero fijo n; separar lo que realmente añade de la identidad
afín y la congruencia ya conocidas. No asumir una tasa uniforme
ni convertir el tamaño de ξ en contradicción.

## 6. Antecedente bibliográfico y límite de la atribución

Garcia, M. V. P. y Tal, F. A., *A note on the generalized 3n+1 problem*,
Acta Arithmetica 90.3 (1999), 245–250,
[DOI 10.4064/aa-90-3-245-250](https://doi.org/10.4064/aa-90-3-245-250),
[original](https://matwbn.icm.edu.pl/ksiazki/aa/aa90/aa9033.pdf).
Se leyeron las seis páginas. La ecuación (6), p. 249, obtiene una
cota de potencia con factor logarítmico en intervalos trasladados;
el corolario 1 usa que una órbita infinita carece de colisiones entre
valores distintos. Esa cota cuantitativa permite deducir la sumabilidad.
El corolario enunciado en el artículo es la densidad de Banach cero,
que **por sí sola** no basta para deducir (6) de esta nota.

La presente prueba usa intervalos desde cero, peso 2^s y constantes
explícitas; no importa el resultado de Heppner ni Garcia–Tal como
hipótesis externa. El [índice del editor](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/90/3)
confirma la publicación. PDF cotejado: 211308 bytes,
SHA256 `dc2ab0a006bdc25430cd14f578439937b37eda3cda0701688be12e49d5c51dd8`.

La [pregunta de MathOverflow sobre recíprocos](https://mathoverflow.net/questions/513539/is-it-known-that-a-divergent-collatz-trajectory-must-have-summable-reciprocals)
sirvió de pista bibliográfica y ya describe esta consecuencia; no
se utiliza como autoridad de prueba ni se reclama haberla descubierto.

Control conceptual: incluso **densidad de Banach cero** no implica
sumabilidad. Reunir las progresiones `2^r+j*r`, con r>=2 y
`0<=j<floor(2^r/r)`. Dentro de cada bloque y hasta el inicio del
siguiente, la separación es al menos r. Para cada H, una cola
tiene separaciones >=H: cualquier intervalo de longitud L contiene
a lo sumo L/H+1 elementos de la cola, más un prefijo finito fijo.
Su densidad superior de Banach es <=1/H para todo H, luego cero.
Pero cada bloque aporta al menos 1/(4r) a la suma de recíprocos,
que diverge. Es un contraejemplo escrito, independiente de Collatz.
La prueba positiva depende de la potencia estrictamente menor que uno
en (5), no sólo de una afirmación cualitativa de rareza.

## 7. Formalización y cotejo

[PerdicesColisiones.lean](PerdicesColisiones.lean): 20 lemas nuevos.

| Tramo | Certificados principales |
|---|---|
| Imagen finita | `cota_afin`, `patrones_sesenta`, `entradas_sesenta`, `cuenta_imagen` |
| Órbita y recíprocos | `inyectiva_en_orbita`, `cuenta_orbita`, `suma_orbital`, `reciprocos_sumables` |
| Producto y límite | `normalizado_acotado`, `normalizado_monotono`, `normalizado_limite` |
| Exclusión | `pronostico_supera`, `fuga_supera`, `sin_regresos_infinitos`, `sin_planeador_intermitente` |

[comprobar_colisiones.py](comprobar_colisiones.py) compila sólo el
nuevo módulo y audita 22 previos: 23 módulos, 252 consultas de axiomas.
Lean 4.32.2 y Mathlib fijado; sólo `propext`, `Classical.choice` y
`Quot.sound`, sin avisos ni pruebas incompletas. Los resultados nuevos
no tienen LMN ni otra hipótesis bibliográfica. [Evidencia](evidencia_colisiones.json),
[salida](evidencia_colisiones.txt). Lean certifica los enunciados;
la interpretación y la revisión humana siguen pendientes.

[cotejar_colisiones.py](cotejar_colisiones.py), con enteros y Fraction:

- Todos los residuos de longitudes 0..14: 425986 prefijos cotejados
  mediante iteración y composición afín independientes; biyección de
  patrones, cuentas binomiales, pesos e imágenes.
- Diecisiete cuentas binomiales exactas, m=0..16, sin enumerar sus
  residuos; desigualdades 60/96/99/100/159 y telescopio geométrico.
- Semillas 1..256, hasta 128 pasos, deteniendo al repetir: 7989
  identidades de producto, aditivo y suma sobre valores distintos.
- Controles del prefijo 4,2,1, multiplicidad temporal en el ciclo 1,2,
  m=0 y progresiones de densidad de Banach cero. No certifican fugas infinitas.

[Resultado](cotejo_colisiones.json). Los cálculos son controles finitos;
la universalidad proviene de la prueba escrita y de Lean.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_colisiones.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_colisiones.json
python -B -X utf8 depuracion/perdices20261007/cotejar_colisiones.py --largo 14 --bloques 16 --nmax 256 --pasos 128 --salida depuracion/perdices20261007/cotejo_colisiones.json
```

Si faltan objetos previos, reproducir primero [Novena](NOVENA.md).
