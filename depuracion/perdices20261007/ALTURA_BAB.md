# Perdices: obstrucción de altura para el presupuesto BAB

16-10-2026. Continúa [Dos cambios, §§4–6](DOS_CAMBIOS.md#4-parametrización-exacta-de-ba-ab-bc).
Se conserva el nombre Perdices y no se reclama prioridad bibliográfica.

**Resultado de presupuesto:** todo prefijo real con hasta dos cambios de
tipo satisface (P) con **epsilon=7/17 y K(n)=2*ell(n)**, por tamaño y
consumo (§6). Es uniforme en todas las semillas y longitudes de esa clase.
No cierra las alternancias arbitrarias.

**Filtro para el candidato más fuerte:** si falla P2 en un prefijo real
`B^a A^b B^c`, entonces,
con los parámetros impares r,s definidos abajo,

```text
1024*8^b*(r*s)^2 < 9^b,
(6*r*s)^18 < 3^b,
rad((3^b*r)*(3^b*r+1))^18 < 3^b*r+1.                (H)
```

En particular, `3^b <= (6*r*s)^18` es un criterio suficiente nuevo para
P2, también fuera de la región de tamaño de Dos cambios. No se demuestra
ese criterio para todos los parámetros. (H) conecta una eventual
refutación del presupuesto con una terna abc de calidad mayor que 18;
**no prueba abc, no supone abc y no cierra P2 en todo BAB ni Collatz**.

## 1. Dominio y parametrización conservada

Se usa el atajo T sobre naturales positivos, A=1 y B=110 con sus paridades
reales. a,b,c>=1 cuentan bloques; L=3a+b+3c cuenta pasos de T. No hay ley
aleatoria ni condicionamiento probabilístico. Se conserva la semilla

```text
q=(2^b*r+1)/9^a,       n=2^(3a+2)*q-5,
9^a | 2^b*r+1,        r>0 impar,
3^b*r+1=2^k*s,        s>0 impar, k=v2(3^b*r+1),
1 <= 3c <= k+2,       ell=ceil(log2(n+5)).            (1)
```

La equivalencia orbital y suficiencia de estos parámetros están probadas
en [Dos cambios](DOS_CAMBIOS.md#4-parametrización-exacta-de-ba-ab-bc).
P2 equivale a `b+2k<=3a+3c+4ell`. Como c=1 es admisible y es el caso más
exigente, cualquier fallo para algún c implica

```text
3a+3+4ell < b+2k.                                   (2)
```

El radical `rad(m)` es el producto de los primos distintos que dividen al
entero positivo m; rad(1)=1. La terna de esta nota es
`(1, 3^b*r, 3^b*r+1)`, cuyos términos son coprimos por ser consecutivos.
Se distingue la terna abc de las longitudes a,b,c de las rachas.

## 2. Del fallo al producto de partes impares

Para evitar logaritmos y redondeos, poner

```text
U=2^b, V=3^b, D=9^a, A0=2^(3a+2), H0=2^ell, K0=2^k.
```

De (1), la definición de ell y (2) se obtiene

```text
A0*(U*r+1) <= D*H0,
K0*s = V*r+1,
2*A0*H0^4 < U*K0^2.                                (3)
```

Elevar a la cuarta la primera desigualdad, usando `A0*U*r<=D*H0`,
y combinar con la tercera produce

```text
2*A0^5*U^4*r^4 < D^4*U*K0^2.
```

Multiplicar por s^2 y sustituir K0*s. Como `V*r>=3`,
`(V*r+1)^2<=2*V^2*r^2`. Cancelando los factores positivos 2, U y r^2:

```text
A0^5*U^3*(r*s)^2 < D^4*V^2.                         (4)
```

Finalmente, `3^8<=2^15` implica
`1024*D^4=2^10*3^(8a)<=2^(15a+10)=A0^5`. Sustituir en (4) y cancelar
D^4 demuestra la primera desigualdad de (H). Todas las cancelaciones
son entre enteros positivos; se mantienen los sumandos +1 al pasar a (3).

**Contraste algebraico independiente.** En logaritmos exactos de base 2,
escribir `lambda=log2(3)`, u=log2(r), v=log2(s). De (1):

```text
ell >= (3-2lambda)*a+2+b+u,
k <= lambda*b+u-v+log2(4/3).
```

Por tanto el exceso de (2) es a lo sumo
`(2lambda-3)b-2(u+v)+(8lambda-15)a-11+2log2(4/3)`.
Como `3^8<2^15` y `(4/3)^2<2`, un exceso positivo obliga a
`2log2(rs)<b*log2(9/8)-10`, la misma primera desigualdad de (H).
Las comparaciones usadas son enteras, no aproximaciones decimales.

## 3. Por qué aparece exactamente el exponente 18

Como 36<1024, la primera desigualdad de (H) implica

```text
(6*r*s)^2 * 2^(3b) < 3^(2b).
```

Elevar a la novena da
`(6rs)^18 * 2^(27b) < 3^(18b)`. La comparación ya usada para ABA,
`3^17<2^27`, permite sustituir el factor 2^(27b) por 3^(17b) y
cancelar. Resulta `(6rs)^18<3^b`.

Todos los divisores primos de `(3^b*r)*(3^b*r+1)` dividen 6rs, porque
`3^b*r+1=2^k*s`. Así,

```text
rad((3^b*r)*(3^b*r+1)) <= 6*r*s.
```

Elevar a 18 y usar `3^b<3^b*r+1` prueba la última parte de (H).
La palabra «calidad» significa aquí el cociente
`log(3^b*r+1)/log(rad((3^b*r)*(3^b*r+1)))`, que sería mayor que 18.
No se optimiza ese exponente.

Por contraposición, la condición computable

```text
3^b <= (6*r*s)^18                                   (C18)
```

garantiza P2 desde la misma semilla para todas las terceras rachas
admisibles c. También lo garantiza la condición más fuerte
`3^b*r+1 <= rad((3^b*r)*(3^b*r+1))^18`. Estas condiciones son suficientes,
no equivalencias con P2.

## 4. Qué permite y qué no permite importar de abc

La formulación usual de abc permite una constante dependiente del
exponente, o equivalentemente un conjunto finito de excepciones por
exponente. No afirma que `C<=rad(ABC)^18` sin excepciones. Esa distinción
está explícita en la introducción de [Curtis Bright, *A new lower bound
in the abc conjecture* (2023/2024)](https://doi.org/10.4153/S0008439523000784).
La misma fuente presenta la cota exponencial de Stewart–Yu; no se
incorpora como si fuese una cota por una potencia fija del radical.

Si se **supusiera** abc, quedarían a lo sumo finitas ternas de (H),
pero aún habría que excluirlas. Más explícitamente, una cota
`C<=M*rad(ABC)^2` junto con (H) implica `rad(ABC)^16<M`, y después
acota C. Sin una M efectiva y una comprobación de las excepciones no
hay cierre del presupuesto. Este comentario es condicional y no una
hipótesis añadida a los resultados del laboratorio.

Se revisó además [Hector Pasten, *Shimura curves and the abc conjecture*,
versión del 05-07-2018](https://lemkeoliver.github.io/papers/20-TwistedZeros.pdf),
teorema 1.10: controla un producto de valuaciones por una potencia del
radical. Para nuestra terna, los exponentes en 3 y 2 son b y k, de modo
que da un control del tipo `b*k < M*(6rs)^(8/3+epsilon)`.
Ese control no fuerza el crecimiento exponencial en b requerido por
(C18). Es una comparación de la fuerza de los enunciados, no una
refutación del método modular de ese trabajo.

## 5. Comprobación dirigida en el repositorio math

Se mantuvo la revisión local
`1581d4cbdd69a0faf34b2089614fe2a814316a6a`, sin modificarla.
Una búsqueda de `abc.conjecture`, `Szpiro` y referencias Stewart–Yu/Tijdeman
en los .tex, .bib y .md de preprints no encontró una cota abc utilizable.
Los aciertos por Szpiro fueron referencias a Peskine–Szpiro en módulos
Cohen–Macaulay y a Szpiro–Ullmo–Zhang en la familia 016, Zilber–Pink.
Se leyeron las hipótesis y las primeras 200 líneas de la sección aritmética
de esta última: su positividad requiere
variedades abelianas y familias con grados acotados, condiciones que no
hemos construido para estos enteros.

Esto no excluye conexiones indirectas ni certifica todo el corpus. Sí
descarta importar esos aciertos textuales como un teorema de altura para
BAB. La pista útil sigue siendo el control conjunto de dos cancelaciones;
ahora tiene la obligación explícita (C18) y el caso excepcional (H).

## 6. Todo el dominio de dos cambios con epsilon=7/17

La ruta original exige epsilon>0 uniforme, no necesariamente epsilon=1/2.
Esto permite resolver toda la clase de dos cambios sin suponer (C18).
Para BAB, la primera racha satisface
`2^(3a)(y+5)=3^(2a)(n+5)`, y `2^(b+2)<=y+1<=y+5`.
Aplicar la cota `17(d+v)<=27S+17ell` de Dos cambios da

```text
17b+34 <= 17ell+3a.                                 (5)
```

Para las primeras dos rachas ya teníamos
`17(3c+v_fin)<=17ell+3a+10b`. Por tanto

```text
7L+17v_fin <= 24a+17b+17ell-30c
            <= 27a+34ell-34-30c
            <= 17*(3a+2)+34ell
             = 17v_in+34ell.                        (6)
```

La primera línea usa L=3a+b+3c. Dividir por 17 demuestra
`(7/17)L+v_fin<=v_in+2ell`, exactamente (P) por la identidad firmada
de las recargas. Para ABA, el resultado previo con epsilon=1/2 implica
el de epsilon=7/17, puesto que L>=0. Para cero o un cambio ya se tenía
epsilon=1 con el mismo K. Así quedan cubiertas **todas** las palabras
reales de A/B con hasta dos cambios.

No se ha ajustado epsilon a datos: 7/17=2-27/17 procede de la cota
entera `3^17<2^27`, fijada en la prueba. K depende sólo de la semilla
original y no cambia entre rachas. El resultado no permite reiniciar
ese K en cada grupo de tres rachas para concluir el presupuesto global.

## 7. Formalización y siguiente acción

[PerdicesAlturaBAB.lean](PerdicesAlturaBAB.lean) certifica el producto de
(H) desde (3), la especialización a potencias, el exponente 18 y el
criterio (C18) y el cierre lineal (6). El lema del radical recibe
como hipótesis `rad<=6rs`; no
define ni calcula el radical. La prueba de esa hipótesis y el enlace
con las órbitas conservan prueba escrita arriba y en Dos cambios.
Para epsilon=7/17, las cotas orbitales que entran en el cierre lineal
tienen prueba escrita; no se declara una formalización orbital completa.
No hay una prueba Lean de abc ni un supuesto externo de ese tipo.

[Evidencia Lean](evidencia_altura_bab.json) y
[salida](evidencia_altura_bab.txt): ocho consultas en Lean 4.32.2,
con sólo propext, Classical.choice y Quot.sound. Imports directos
cotejados; sin auditoría transitiva completa de Mathlib.

[Cotejo entero](cotejo_altura_bab.json): 1004 casos BAB construidos con
a<=4, b<=256 y r impar<=63, todos con T literal. Los criterios de producto
y C18 cubren los 1004; 481 quedan fuera de la región anterior de tamaño.
Se verifican también las desigualdades del presupuesto epsilon=7/17.
En 46 casos con b<=12 se calcula el radical por factorización independiente.
Es evidencia finita, no la demostración universal de C18.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_altura_bab.py --a-max 4 --b-max 256 --r-max 63 --factorizar-hasta-b 12 --salida depuracion/perdices20261007/cotejo_altura_bab.json
python -B -X utf8 depuracion/perdices20261007/comprobar_altura_bab.py --salida depuracion/perdices20261007/evidencia_altura_bab.json
```

Continuación: [Tres cambios](TRES_CAMBIOS.md) obtiene epsilon=1/13 y
documenta una obstrucción de las cotas para 7/17, sin refutar el presupuesto
orbital. (C18) queda como vía secundaria para el candidato P2 más fuerte;
no sustituir el objetivo por abc general.
Hay que distinguir si una herramienta elimina todas las excepciones o
sólo acota su cantidad. Revisión humana pendiente.
