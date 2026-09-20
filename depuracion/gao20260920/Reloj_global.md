# Moscas, Mangostas y Gacelas: reloj global

20-09-2026. Deducción escrita nueva, sobre la cadena absorbente original.
No se sustituye por la cadena rebotada ni se condiciona a supervivencia.
Las estimaciones casi seguras se restringen al evento de no absorción
**después** de demostrarlas bajo la ley original. Sin revisión externa.

## 1. Ley, coordenada y tiempos

Bits iid justos, filtración de los bits leídos, transiciones de
[`estratoscadena.py`](../../estratoscadena.py). Estados vivos: `(0,g)`,
`g` entero positivo, y `(k,c)`, `k>=1`, `c` entero firmado. Cementerio
absorbente después de la fusión. Se prolongan los bits independientemente.
Poner `u=c/3^k` en estados vivos y `u=0` en el cementerio.

Arranque fijo en la frontera `k=0,1` (en particular `(0,1)`), o en
`(2,c0)`. `S_i` es la i-ésima entrada en k=2 desde k=1; si se empieza
en k=2, `S_1=0`. `R_i` es la primera llegada a k=1 después de `S_i`.
`D_i=R_i-S_i` es la excursión interior. `B_i=S_(i+1)-R_i` es el
tramo de frontera, terminado antes si hay fusión. Los tiempos de
entrada inexistentes se dejan en infinito; las duraciones inexistentes
se ponen a cero al aplicar estimaciones incondicionales.

**Conclusión escrita:** en el evento de no absorción, todas las entradas
existen y, casi seguramente, para constantes finitas aleatorias que
dependen del arranque,

    S_i = O(i^4),     |c_(S_i)| = O(i^16).                 (RG)

Los exponentes son holgados. No se afirma una constante determinista
uniforme en todos los arranques, ni una esperanza finita de las excursiones.

## 2. Envolvente válida en todos los tiempos

Por las seis leyes y las dos puertas de frontera, en cada rama viva,

    |u_(t+1)| <= A_(t+1)|u_t| + 1/2,
    A=1/2 para bit 0, A=3/2 para bit 1.                   (E1)

En k=0 impar, la puerta con bit 1 tiene realmente pendiente `-1/2`;
su valor absoluto queda dominado por `3/2`. Al bajar de k=1 se toma
el valor absoluto del gap. Ambas operaciones respetan E1. En el
cementerio la desigualdad también vale.

Segunda auditoría: `cadena_completa.lean` define toda la transición
absorbente y demuestra `dominacion_cadena` para cada estado y bit,
incluyendo las divisiones enteras. Usa la forma sin denominadores
`2|c'|p <= (1+2b)|c|p'+p*p'`, con `p=3^k`, `p'=3^k'` positivos.
Dividir por `2pp'` da E1. [Momentos.lean](formal/Momentos.lean) certifica
ahora esa división sobre reales y el promedio sobre todas las palabras
equiprobables: `E sqrt(|u_t|)<=rho^t sqrt(|u_0|)+32(1-rho^t)`,
`rho=31/32`. Desde `(0,1)` certifica incluso la cota 32.
La identificación del promedio con la suma de las `2^t` hojas también
está formalizada. El paso posterior a Borel–Cantelli sigue escrito.

Moscas, subaditividad e independencia del siguiente bit dan

    E sqrt(|u_t|) <= sqrt(|u_0|)+32 = K0, para todo t.    (E2)

En efecto `lambda=(1+sqrt(3))/(2sqrt(2))<31/32`:
`lambda^2=(2+sqrt(3))/4<15/16<961/1024`. El término aditivo es
`1/sqrt(2)<=1`, por lo que la suma geométrica está acotada por 32.
Markov y la primera Borel–Cantelli, pues `sum (t+1)^(-2)<infinito`,
implican una variable `K<infinito` casi seguramente tal que

    |u_t| <= K(t+1)^4 para TODOS los t>=0.                (E3)

Se absorben las finitas excepciones en K. E3 es una envolvente de la
trayectoria completa: evaluarla en un tiempo aleatorio no traslada
incorrectamente un momento a un tiempo de parada.

## 3. Frontera: duración y posibilidad de salir

En k=0, `g=2^r*d`, d impar positivo. Cada paso compartido divide por
2 y multiplica opcionalmente por 3; por tanto hacen falta exactamente
r pasos para obtener un gap impar. El siguiente paso entra en k=1.
En particular el tramo compartido dura `v2(g)<=log2(g)`.

En k=1 los compartidos son `c/2` y `(3c-2)/2`. Si c es par, exactamente
una de estas dos ramas vuelve a ser par. Así el número L de compartidos
hasta c impar tiene `P(L>=l | estado)<=2^{-(l-1)}` para `l>=1`.
Si c es impar, L=0. Esto incluye c=0 y ambos signos.

Al siguiente mixto de k=1, el bit 0 entra en k=2; el bit 1 baja a
k=0 o fusiona. Cada mixto se decide con un bit fresco. Si J es el
número de estos mixtos hasta entrar en k=2 o fusionar,

    P(J>=j | pasado al empezar la frontera) <= 2^{-(j-1)}.

Las rachas de k=1 son finitas casi seguramente; las de k=0 son finitas
determinísticamente. Por ello cada tramo de frontera termina casi
seguramente, incluso antes de usar cualquier cota de magnitud.

Aplicar las dos colas geométricas en cada tiempo entero t donde pueda
empezar una racha de k=1 o un tramo de frontera. Con umbral
`ceil(4 log2(t+2))+2`, las probabilidades son sumables en t. Borel–Cantelli
da una constante aleatoria común que acota L y J por `C log(t+2)`
en todos esos inicios, absorbiendo las finitas excepciones.

Para un tramo de frontera con inicio a y final b finitos, todos sus
subtramos empiezan antes de b. E3 da en k=0
`log2(g)<=log2(K)+4log2(b+1)`. Hay a lo sumo J+1 rachas de k=0,
J rachas de k=1 y 2J+1 pasos de cambio de piso. En consecuencia,

    b-a <= C_omega [log(b+2)]^2.                         (E4)

No se ha supuesto independencia entre esas duraciones.

## 4. Excursiones y ensamblaje del reloj

Por [R2](../coherencia20260913/Matematica.md#3-corolario-del-reloj-de-mangostas-y-gacelas)
y Markov fuerte en `S_i`,

    P(D_i>i^3, S_i<infinito) <= C sqrt(log(i+2))/i^(3/2).

La suma converge. Por Borel–Cantelli `D_i<=i^3` salvo finitos i;
la suma de las primeras n duraciones interiores es `O_omega(n^4)`.
Cada excursión retorna casi seguramente por Gacelas. Junto con el
apartado 3, esto prueba que, sobre la no absorción, hay infinitas
entradas y todos los `S_i,R_i` son finitos.

Sumar E4 hasta `S_n` entrega

    S_n <= C_omega [1+n^4+n log(S_n+2)^2].                (E5)

Esta desigualdad implica `S_n=O_omega(n^4)`. Para verlo sin presuponer
un soporte temporal, fijar la constante de una trayectoria. Si
`S_n>2C(1+n^4)`, E5 obliga `S_n/log(S_n+2)^2<=2Cn`.
La función `x/log(x+2)^2` es creciente para x suficientemente grande;
en `x=2C(1+n^4)` su orden es `n^4/log(n)^2`, mayor que `2Cn`.
Contradicción para n grande. Finalmente E3 en `S_i`, con k=2,
da `|c_(S_i)|=9|u_(S_i)|=O_omega(i^16)`.

## 5. Alcance

Se obtiene un reloj polinómico y arranques polinómicos casi seguros
en el evento de no absorción, sin afirmar que dicho evento tenga
probabilidad positiva. No es todavía una prueba de absorción: falta
un piso suficiente de éxito y ensayos que no se solapen.

La siguiente pieza es [Salida_ampliada.md](Salida_ampliada.md).
La probabilidad, Borel–Cantelli y el ensamblaje RG son prueba escrita;
no están formalizados integralmente en Lean. Los certificados y cruces
de esta tanda se especifican en [REVISION.md](REVISION.md).
