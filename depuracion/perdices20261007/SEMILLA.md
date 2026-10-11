# Perdices: la misma semilla y excursiones que superan su quinta potencia

10-10-2026. Continuación de [Aporte](APORTE.md) y enlace con los
[prefijos de Jinetas](../jinetas20261010/PREFIJOS.md). Son consecuencias
de las identidades y cotas del laboratorio; no se reclama prioridad.

**Resultado:** el aporte local no decide si se prolonga el representante
mínimo de una palabra. La congruencia completa sí lo decide, pero su
estabilización reformula la existencia de una semilla fija. Una
consecuencia cuantitativa del tiempo de los regresos permite precisar
el objetivo: bajo fuga pura e infinitos regresos a un techo fijo,

```text
para todo H,U naturales existen regresos consecutivos u<v, u>U,
              v-u > H (T^u(n)+1)^5.                         (1)
```

Una cota superior opuesta, uniforme en los regresos de esa semilla
después de algún instante, excluiría al planeador intermitente. Esa
cota **no está probada**. El cohete y la grieta siguen abiertos.

## 1. Convenciones y el levantamiento exacto

Mapa atajo `T(n)=n/2` para par y `(3n+1)/2` para impar. Las órbitas
objetivo tienen n entero positivo; para los residuos se permite n=0.
`x_j=T^j(n)`, `S_j` cuenta entradas impares antes de j,
`P_j=3^S_j/2^j`, `R_j=x_j/P_j` y `J_l(j)=(x_j+l)/P_j`.
El tiempo se mide en pasos del atajo. Todo es determinista, sin ley
aleatoria ni condicionamiento probabilístico.

Una palabra prefijo de longitud u tiene datos enteros `(A,B,M)`:

```text
M=2^u, A=3^S_u, M x_u=A n+B,
r=-B A^(-1) mod M, 0<=r<M, q=(A r+B)/M.
```

El sufijo de longitud d tiene `(D,E,N)`, con `N=2^d` y D una potencia
de 3; su identidad es `N y=D x+E`. Aquí **D no es el margen M-A**
empleado en Jinetas. La composición da

```text
(A',B',M')=(D A, D B+M E, M N).
```

El nuevo residuo mínimo es `r'=r+M t`, donde

```text
t=-(D q+E)(D A)^(-1) mod N,       0<=t<N.                 (2)
```

Prueba: cualquier prolongación debe pertenecer a la clase del prefijo.
Para n=r+Mt su entrada al sufijo es q+At. La identidad

```text
D A(r+Mt)+(D B+M E)=M[D(q+At)+E]
```

reduce la divisibilidad por MN a la divisibilidad del corchete por N.
DA es impar, luego tiene inversa módulo N. El rango de t hace
`0<=r'<MN` y da el único representante. N=1 (sufijo vacío) da t=0.
La equivalencia entre congruencia y palabra de paridades es la de
[Jinetas](../jinetas20261010/LEEME.md); no se añade como un nuevo supuesto
sobre las órbitas.

El aporte y la carga desplazada satisfacen, en cambio,

```text
Delta R   = M E/(A D),
Delta J_l = M[E+l(N-D)]/(A D).                            (3)
```

Se obtienen restando `B/A` de `B'/A'` y usando `1/P_u=M/A`.
No dependen de r o q. Se conservan al cambiar la semilla por otro
representante de la misma palabra completa.

## 2. El mismo aporte puede admitir o exigir cambiar el mínimo

Cada fila compara dos prefijos del mismo largo y con el mismo número
de impares, seguidos por el mismo sufijo. El techo es C=3^c.
Se muestran el mínimo r del prefijo y el levantamiento t de (2).

| c | Prefijo con t=0 | r | Otro prefijo | r | t | Sufijo | Delta J_5 común |
|---:|---|---:|---|---:|---:|---|---:|
| 1 | 11011101 | 91 | 11011011 | 251 | 120 | 1110100 | 78848/59049 |
| 1 | 1101110110 | 603 | 1101110101 | 859 | 7 | 110 | 0 |
| 2 | 1111011011 | 111 | 1111010111 | 559 | 41 | 111100 | -20480/531441 |

Los aportes Delta R comunes son, respectivamente, `18688/59049`,
`5120/19683` y `66560/531441`. Los mínimos de las palabras completas
de la segunda columna comparada son 30971, 8027 y 42543; los de la
primera permanecen en 91, 603 y 111.

Todas las palabras completas son prefijos reales con P>=1 y sus
extremos u,u+d son regresos consecutivos al techo indicado. Así, ni
el signo ni el valor exacto del aporte local decide t=0, aun fijando
P_u, el techo y todo el sufijo. Los q difieren; (2) no los omite.
Son seis ejemplos finitos, comprobados directamente con racionales,
**no ejemplos de fuga pura infinita ni teoremas orbitales nuevos en Lean**.

La distinción importa: la suma de aportes de **todo el prefijo** sí
determina B/A y, conocidos A y M, determina r. No hay dos fuentes
independientes de información que puedan contradecirse por sumar (2)
y (3); son dos lecturas de la misma identidad afín.

## 3. Estabilizar el residuo conserva la semilla, pero no prueba su desaparición

Para una rama infinita de palabras compatibles, los r_L son enteros
no decrecientes. Si están acotados, se estabilizan en un n. La
compatibilidad de los prefijos implica que n realiza cada palabra.
Recíprocamente, si una semilla n realiza la rama, `r_L=n mod 2^L`;
por tanto `r_L=n` en cuanto `2^L>n`. A partir de ahí cada levantamiento
debe ser cero. Un t positivo daría `r'>=2^L>n` y descartaría esa semilla.

Es la especialización del criterio ya escrito en
[PREFIJOS.md](../jinetas20261010/PREFIJOS.md), cuyo teorema Lean trata
conjuntos anidados y mínimos. No demuestra que aparezca un t positivo
en toda rama sin cruce. Exigirlo sin una desigualdad adicional sería
volver a formular la dificultad, no resolverla.

## 4. Una restricción efectiva sobre la semilla local

Fijar **el mismo** n y C=3^c. Suponer `FugaPura n`, es decir,
P_j>=1 para todo j, e infinitos regresos P_j<=C. Enumerarlos desde
un instante arbitrario como t_i. Escribir `x_i=T^(t_i)(n)` y
`d_i=t_(i+1)-t_i`.

Las cotas ya formalizadas dan

```text
(x_i+1)^6 <= K(t_i+1),      K=64 C^6 n^6,                 (4)
(i+1)^150 <= A(t_i+1)^24,   A constante para n,C.         (5)
```

(4) es [entrada_sexta](PerdicesRitmo.lean); (5),
[tiempo_por_indice](PerdicesSeparacion.lean). En particular, (5)
prohíbe `t_i+1<=B(i+1)^6` para todos los i y B fijo.

Supongamos que todos los saltos de una cola cumplieran
`d_i<=H(x_i+1)^5`. Entonces, con D=H^6 K^5,

```text
d_i^6 <= H^6 (x_i+1)^30 <= D(t_i+1)^5.
```

Esto fuerza un tiempo de regresos de grado seis. Una comprobación
independiente del paso inductivo: si `t_i+1<=B(i+1)^6`, con
`B=D+t_0+1`, entonces `d_i<=B(i+1)^5`; y
`(i+1)^6+(i+1)^5<=(i+2)^6`. Así se obtiene la cota prohibida.
Como la enumeración puede empezar después de cualquier U, queda (1).
El H puede depender de n y C, pero **no del regreso i**.

Pidiendo H+1 en (1), la entrada x=T^u(n) satisface

```text
d > (H+1)(x+1)^5,       x < d < 2^d.
```

La semilla x es entonces exactamente el representante mínimo de la
palabra **local** módulo 2^d. La biyección de paridades identifica
ese representante con x, no con una semilla elegida de nuevo. Además,
para `rho=C/P_u` se tiene `1<=rho<=C`, el factor multiplicativo local
supera rho en todos los tiempos interiores y vuelve a <=rho al final.
Por tanto una cota de duración para estas palabras de semilla pequeña
sí se aplicaría al frente pendiente. No basta una cota para palabras
con otras semillas o con otros tiempos de regreso.

### Por qué no lo contradice la familia de Aporte

En la familia `(1110)^k 0^b` de [Aporte, §4](APORTE.md#4-muchas-excepciones-aporte-total-acotado),
k>=3 y el último regreso inicial es u=8. Allí

```text
d=4k+b-8,       11x+19=729*16^(k-2)*m,       m>=1.
```

La minimalidad de b y `27^k<32^k` dan b<=k. Como
`16^(k-2)>=k-1`, se deduce `d<=5k-8<x`. Esta familia tiene muchas
excepciones y poco aporte, pero **no** satisface la exigencia de (1)
con H>=1. Lean certifica esta última desigualdad a partir de las
identidades mostradas; la construcción orbital general de la familia
sigue siendo la prueba escrita de Aporte.

## 5. Alcance formal, cotejo y siguiente trabajo

[PerdicesSemilla.lean](PerdicesSemilla.lean) contiene catorce lemas:
composición, aportes, criterio de divisibilidad, intervalo del
levantamiento, casos cero y positivo, deducción orbital de (1),
criterio suficiente contrario, módulo local y cota de la familia.
La deducción (1) y su contraposición son orbitales completas bajo las
hipótesis indicadas. Las fórmulas con inversa modular y la equivalencia
infinita de la sección 3 tienen prueba escrita; el módulo formaliza
el criterio de divisibilidad, no una nueva biyección completa de paridades.

[comprobar_semilla.py](comprobar_semilla.py) compila sólo este módulo
y audita veinte previos: 21 módulos, 206 consultas acumuladas.
Lean 4.32.2, axiomas estándar, sin pruebas incompletas; ninguna hipótesis
externa en los nuevos resultados. [Evidencia](evidencia_semilla.json),
[salida](evidencia_semilla.txt). Revisión humana pendiente.

[cotejar_semilla.py](cotejar_semilla.py) contrasta composición e inversa
modular con órbitas directas y `Fraction`: 2047 palabras de longitudes
0..10, 20481 cortes y dos representantes de cada palabra en cada corte.
Incluye prefijo/sufijo vacío, residuo cero y los tres pares de signos.
[Salida](cotejo_semilla.json): 4083 levantamientos nulos y 16398 positivos.

En semillas 2..512, hasta 256 pasos y c=0..4, sólo antes del primer
cruce, se examinaron 223 excursiones no unitarias (más 4514 unitarias):
33 tienen x<2^d; ninguna tiene d>(x+1)^5. El máximo de d/(x+1)^5
fue `1/944784`, para n=7,c=1,u=2,v=4,x=17. Esto mide esa ventana;
no confirma una cota universal ni verifica FugaPura. También pasó
el borde `--largo-max 0 --n-max 2 --pasos 1 --nivel-max 0`.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_semilla.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_semilla.json
python -B -X utf8 depuracion/perdices20261007/cotejar_semilla.py --largo-max 10 --n-max 512 --pasos 256 --nivel-max 4 --salida depuracion/perdices20261007/cotejo_semilla.json
```

**Siguiente:** buscar una cota de duración que utilice el valor de
entrada y su congruencia, comenzando por las palabras de retorno
descritas en §4. El objetivo suficiente es d<=H(x+1)^5 en una cola
de cada órbita considerada. Hay que obtenerla de la dinámica; (2)
por sí sola no la proporciona.
No se ha probado esa cota ni excluido al planeador, al cohete o a la grieta.
