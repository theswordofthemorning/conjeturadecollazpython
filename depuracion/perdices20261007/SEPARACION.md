# Perdices: separación y rachas entre regresos

10-10-2026. Continuación de [Cruce](CRUCE.md). Se conserva el nombre
Perdices: consecuencias de las cotas ya disponibles, sin atribuir prioridad.

**Resultado:** si una misma fuga pura regresa infinitas veces bajo un
techo fijo, las excursiones entre regresos deben tener un número de
rachas impares **no acotado**, incluso después de cualquier tiempo.
Hay una prueba escrita del enlace completo. Lean certifica diez lemas,
incluidas la cota de duración por rachas y la incompatibilidad con un
reloj de regresos de grado seis. El enlace asintótico entre ambos y la
extracción de las excursiones consecutivas todavía no están formalizados.

Esto restringe al planeador intermitente; no lo excluye. Tampoco afirma
que el número de rachas tienda a infinito en todas las excursiones.

## 1. Regla, dominio e índices

Mapa atajo T(n)=n/2 para n par y (3n+1)/2 para n impar, n positivo.
`x_j=T^j(n)`, `S_j` cuenta las entradas impares anteriores a j,
`P_j=3^S_j/2^j`. El tiempo se mide en pasos de T.

La hipótesis global es **FugaPura n**, P_j≥1 para todo j. Se fijan
la misma semilla n y el mismo c natural, con techo C=3^c.
No hay ley probabilística ni independencia. Ninguna órbita finita
se declara una fuga pura. La infinitud de regresos es una hipótesis
adicional y excluye por definición el caso cohete para ese techo.

Si hay infinitos regresos, `t_0<t_1<…` enumera **todos** los tiempos
con P_t≤C; t_0=0. La excursión i es el segmento `[t_i,t_(i+1))`,
con duración d_i=t_(i+1)−t_i. Si d_i>1, sale mediante un paso impar,
permanece sobre C en sus tiempos interiores y termina con un paso par.
Su palabra es `1^a_0 0^b_0 … 1^a_(h−1) 0^b_(h−1)`, con a_i,b_i≥1.
La última racha par se corta en el regreso; no se exige maximalidad
después de ese instante. h cuenta las rachas impares de ese segmento.
Los intervalos de duración uno se tratan aparte.

Para dos regresos u<v, con d=v−u y s=S_v−S_u, siempre

```text
P_v/P_u = 3^s/2^d ∈ [1/C,C].                         (1)
R_v−R_u = (1/3) Σ_{u≤j<v, x_j impar} 1/P_j,
R_j=x_j/P_j.                                        (2)
```

(1) procede de la composición, y (2) de telescopar la identidad afín
de [Tamaño](TAMANO.md). Para una excursión de duración mayor que uno,
el último paso divide el coeficiente por dos: C/2<P_v≤C.
Estas identidades conservan el origen; reiniciar en x_u no lo
convierte en una fuga pura. Sí es una casi fuga del nivel C.

## 2. Lo que exige la cuenta anterior

Definir `A=2^(150c+894)(3^c n)^144`. Por [Cruce](CRUCE.md),
F(K)^150≤A K^24, donde F(K) cuenta los regresos j<K.
Hasta `t_r+1` hay exactamente r+1 regresos. Por tanto

```text
(r+1)^150 ≤ A(t_r+1)^24,
t_r+1 ≥ A^(−1/24)(r+1)^(25/4).                     (3)
```

La primera forma es entera y está formalizada. También vale para
cualquier lista estrictamente creciente de visitas, aun incompleta,
porque su cuenta es al menos r+1. Sólo la enumeración completa permite
llamar a los saltos huecos sin visitas interiores.

Si los primeros r saltos son ≤D, entonces `t_r≤t_0+Dr` y

```text
(r+1)^126 ≤ A(t_0+D+1)^24.                         (4)
```

Se obtiene sustituyendo `t_r+1≤(t_0+D+1)(r+1)` en (3) y cancelando
la potencia positiva (r+1)^24. En una lista infinita no puede existir
un D uniforme. Lo mismo vale para cualquier cola de esa lista.
Lean prueba ambas consecuencias sin suponer t_0=0.

Un criterio suficiente para contradicción sería `t_r=O(r^β)` con
β<25/4, manteniendo n,c fijos. Por ejemplo, una cota para todos los
saltos `d_r≤B(n,c)(r+1)^5` bastaría, por suma. No se ha obtenido.
`reloj_sextico_imposible` certifica el caso entero concreto:
ningún B natural puede satisfacer `t_r+1≤B(r+1)^6` para todos los r.

## 3. Pocas rachas sí limitan la duración

Sea x el valor al entrar en una palabra de h bloques impares/pares
y sea L natural con `x+1≤2^L`. Escribir s_i para el número de pasos
impares anteriores al bloque i, de modo que s_0=0.

La congruencia de una racha impar y el encadenamiento afín ya dan
en [OcelotasTrayectorias](../cst20260930/OcelotasTrayectorias.lean):

```text
2^(s_(i+1)) ≤ (x+1)3^s_i ≤ 2^(L+2s_i).
```

La primera desigualdad se obtiene de `2^a_i | x_i+1` y
`2^s_i(x_i+1)≤3^s_i(x+1)`. La segunda usa 3≤4. En consecuencia,
`s_(i+1)≤L+2s_i`; una inducción elemental entrega

```text
s_h+L ≤ 2^h L,       s_h ≤ (2^h−1)L.                (5)
```

Al partir de un regreso de la fuga pura, la casi fuga del mismo nivel
impone `2^d≤3^c3^s_h≤2^(2(c+s_h))`. Así,

```text
d ≤ 2((2^h−1)L+c).                                 (6)
```

**(6) está enlazada con la órbita en Lean**, usando `Palabra`,
`congruencias_acumuladas` y `casi_fuga_de_bajo`. No se postulan
congruencias nuevas ni se cambia de nivel. El lema incluso vale para
cualquier palabra completa de bloques desde un regreso, sin exigir
que su extremo sea el próximo regreso.

Se puede tomar `L=ceil(log2(x+1))`. Para h fijo, la duración crece a
lo sumo como log(x+1); la constante crece exponencialmente con h.
No se obtiene una cota uniforme si h también crece.

## 4. Enlace escrito: las excursiones necesitan rachas no acotadas

**Cierre posterior del 10-10:** [Excursiones](EXCURSIONES.md) formaliza
la conclusión completa, incluida la extracción orbital y enumeración.
Usa una derivación entera alternativa; se conserva aquí la prueba
logarítmica original.

Supongamos, por contradicción, que después de cierto regreso todas
las excursiones tienen h≤H, salvo los intervalos de duración uno.
Trabajamos con esa cola y su primer tiempo t_0, que puede ser positivo.

En un regreso, la sexta raíz da `x_t^6≤(Cn)^6(t+1)`; para esta
deducción basta la consecuencia más débil `x_t≤Cn(t+1)`.
Fijar m natural con Cn+1≤2^m y escribir q=ceil(log2(t+1)). Entonces
`x_t+1≤2^(m+q)`, de modo que en (6) sirve L=m+q.

La desigualdad elemental `q≤2√(t+1)` vale también en t=0. Para q≥1,
usar `2^(q−1)<t+1` y `q²≤4·2^(q−1)`; esta última se verifica en
q=1,2,3 y se induce usando `(q+1)²≤2q²` para q≥3.
Por tanto, con la constante fija

```text
B=2(2^H−1)(m+2)+2c+1,
d_i ≤ B√(t_i+1).                                   (7)
```

El +1 incorpora los intervalos de duración uno. Si y_i=√(t_i+1),
entonces `y_(i+1)²≤y_i²+B y_i≤(y_i+B/2)²`, de donde
`y_i≤y_0+Bi/2`. Así, `t_i+1=O(i²)`, en contradicción con (3),
que exige al menos orden i^(25/4). Más concretamente, un entero
M≥max(y_0,B/2) daría `t_i+1≤M²(i+1)²≤M²(i+1)^6`, lo que excluye
el lema formal `reloj_sextico_imposible`.

Conclusión escrita: para cada H y cada índice inicial hay una
excursión posterior con **más de H rachas impares**. Esto no significa
que todos los h_i crezcan ni prueba que tal planeador exista.
La sexta raíz anterior ya bastaba para esta contradicción, pues
exigiría orden i^6 frente a i². El exponente 4/25 afina (3), pero no
es indispensable para excluir un número uniformemente acotado de rachas.
Con c=0 sólo puede regresar j=0, por coprimalidad de 2 y 3; el caso
de infinitos regresos es entonces imposible desde el inicio.

## 5. Por qué el techo solo no basta: familia exacta

Para cada a≥3, elegir b mínimo con `3^a≤3·2^(a+b)`. Se tiene b≥1
y `3/2<3^a/2^(a+b)≤3`. Sea u el inverso de 3^a módulo 2^b,
tomado entre 1 y 2^b−1, y poner `n_a=2^a u−1`.

La órbita real de n_a empieza con `1^a0^b`, pues

```text
x_j=3^j2^(a−j)u−1                 (0≤j≤a),
x_(a+j)=(3^a u−1)/2^j             (0≤j≤b).
```

Los primeros a valores de entrada son impares; el numerador final
es divisible por 2^b. Todos los coeficientes del prefijo son ≥1.
Bajo el techo fijo **C=3**, los únicos regresos de ese prefijo son
`0,1,2,a+b`. El hueco `(a+b)−2` crece sin límite y el segmento entre
los dos últimos regresos tiene una sola racha impar. No contradice
(6): también crecen la semilla y el valor de entrada.

| a | b | n_a | Últimos regresos | Hueco |
|---:|---:|---:|---|---:|
| 3 | 1 | 7 | 2 y 4 | 2 |
| 5 | 2 | 95 | 2 y 7 | 5 |
| 128 | 74 | registrado en el cotejo | 2 y 202 | 200 |

Es una prueba escrita para todo a, con contraste independiente
finito. Refuta un tope de separación dependiente **sólo del techo**
para todos los prefijos sin cruce. No refuta un tope dependiente de n,
ni fabrica infinitos regresos de una misma semilla, ni constituye un
contraejemplo de Collatz. El inverso modular usa exactamente el factor 3.

## 6. Certificación y reproducción

[PerdicesSeparacion.lean](PerdicesSeparacion.lean) contiene diez lemas:
cuenta por índice, tiempo por índice, suma de saltos, presupuesto,
saltos grandes y arbitrariamente tardíos, imposibilidad del reloj
séxtico, impares por rachas, duración por rachas y enlace desde un regreso.
La cancelación de potencias positivas evita usar raíces aproximadas.

[comprobar_separacion.py](comprobar_separacion.py) compila ese módulo y
audita los 14 objetos previos mediante el auditor de Cruce: mismas
fuentes, entorno, dependencias y huellas. **No los recompila**.
[Evidencia JSON](evidencia_separacion.json) y [salida](evidencia_separacion.txt):
Lean 4.32.2, 132 consultas contando las 122 previas; sólo axiomas
estándar, sin pruebas incompletas ni avisos nuevos. Revisión humana pendiente.

El alcance de este módulo termina en los lemas indicados. El módulo
posterior [PerdicesExcursiones](EXCURSIONES.md) cierra la extracción,
la inducción cuadrática y la conclusión orbital de §4 sin logaritmos.
La derivación logarítmica específica y la familia modular general de
§5 conservan prueba escrita; no se presentan como resultados Lean.

[cotejar_separacion.py](cotejar_separacion.py) contrasta órbitas directas
con `Fraction`, composición afín e inverso modular independientes.
El [cotejo](cotejo_separacion.json) verifica 126 miembros de la familia,
1033 segmentos, 1541 controles de índices y otros tantos presupuestos,
y 215 controles de la cota de rachas, incluyendo potencias exactas.
Los controles de índices comprueban las expresiones sobre prefijos;
no sustituyen la hipótesis global del teorema ni dan evidencia de fugas.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_separacion.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_separacion.json
python -B -X utf8 depuracion/perdices20261007/cotejar_separacion.py --a-max 128 --n-max 128 --pasos 128 --nivel-max 3 --salida depuracion/perdices20261007/cotejo_separacion.json
```

Si faltan los objetos de Cruce, ejecutar primero su comprobador según
[la reproducción anterior](CRUCE.md#6-contraste-independiente-y-reproducción).
No se relanzan censos históricos ni se incorpora Mahler.

## 7. Decisión y siguiente paso

El estudio de separaciones produce una restricción estructural concreta:
un planeador necesitaría excursiones con rachas no acotadas. Para cada
H fijo las congruencias existentes ya controlan su duración; el obstáculo
se desplaza al crecimiento de h en una misma órbita.

El enlace de §4 ya está [cerrado en Lean](EXCURSIONES.md).
Siguiente bloque: examinar la pérdida `2^h` de (6). Hay que controlar
conjuntamente las rachas y el valor de
entrada conservando n, o encontrar una cantidad que disminuya al
encadenar excursiones. Mejorar una constante con H fijo no excluye
el caso h no acotado. El cohete y la grieta permanecen fuera de este
argumento; los dos muros de Collatz siguen abiertos.
