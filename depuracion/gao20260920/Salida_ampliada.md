# Gacelas y Moscas: una ventana creciente para la salida

20-09-2026. Deducción escrita; no prueba el P2 original con M fijo.
La propuesta es pagar una ventana polilogarítmica en el arranque,
suficientemente pequeña para la accesibilidad de Hormigas.

## 1. Dominio y variables

Cadena interior desde `(2,c0)`, c0 entero de cualquier signo, bits iid
justos; tau es la primera llegada a k=1. `u=c/3^k` y, hasta la salida,

    u_t = Pi_t u_0 + W_t,   u_0=c0/9,
    W_(t+1)=A_(t+1)W_t+delta_(t+1), |delta|<=1/2.

Esta identidad incluye el paso de salida. Prolongar W después de tau
mediante `W_(t+1)=A_(t+1)W_t`, con los bits independientes prolongados.
**No congelar W después de salir**: congelarlo no conserva el argumento
de contracción del momento. Bajo esta extensión,

    E sqrt(|W_t|) <= 32, para cada t determinista.         (V1)

El término inicial es W_0=0. Por unión y Markov,

    P(existe t<=H: |W_t|>R) <= 32(H+1)/sqrt(R).            (V2)

No se ha condicionado ningún bit a la salida o a supervivencia futura.

V1 y V2 están ahora formalizadas sobre la transición completa en
[Resto.lean](formal/Resto.lean), incluida la identidad afín hasta el
paso de salida y la extensión multiplicativa posterior. También se
certifican el coste de la ventana y la conversión a offset de salida.
[Alcance y evidencia](Control_aditivo_producto.md). V3 completa sigue
pendiente de formalización de sus probabilidades conjuntas.

## 2. Parámetros explícitos, sin ajustar sobre una muestra

Definir, con logaritmos en base 2,

    m = ceil(log2(2+|c0|)),
    T = 32 max(32,m),
    n = 256(T+1)^2,
    a = 2+floor(log2(n+2)),
    s = ceil(3log2(n+1)),
    H = n(a+s+1),
    Q = ceil(sqrt(2T+3)),
    R = [128(H+1)Q]^2,
    G = 3(R+1).

En los scripts, s puede aumentarse a `3 ceil(log2(n+1))`, sin debilitar
ninguna cota. T>=1024 y `(31/32)^32<1/2` implican
`(31/32)^T max(1,|c0|/9)<=1`.

Para todo c0 se afirma la cota escrita

    P(T<tau<=H, |c_tau|<=G) >= 1/[4 sqrt(2T+3)].           (V3)

En particular `H=O(T^2 log(T+2))`, `G=O(T^5 log(T+2)^2)` y
`T=O(log(2+|c0|))`, con constantes absolutas y el umbral fijo declarado.

## 3. Prueba por tres sustracciones

Gacelas G2 da `P(tau>T)>=1/sqrt(2T+3)`. Restar tres eventos malos.

**Salida demasiado tardía.** R1 de Mangostas–Gacelas da
`P(tau>H)<=q_n+n*2^(-s)`. La inducción del binomial central proporciona
`q_n<=sqrt(2/(n+1))` (para n=2h, basta
`binom(2h,h)/4^h<=1/sqrt(h+1)`). Con los parámetros anteriores,

    q_n <= 1/[8 sqrt(2T+3)],
    n*2^(-s) <= 1/n^2 <= 1/[8 sqrt(2T+3)].

La primera desigualdad se verifica al cuadrado mediante
`n+1>=128(2T+3)`; la segunda mediante `n^4>=64(2T+3)`.
Así el coste es como máximo `1/[4 sqrt(2T+3)]`.

**Producto demasiado grande.** G4 entrega
`P(existe t>=T: Pi_t>(31/32)^t)<=62(61/62)^T`.
El certificado finito [Producto.lean](formal/Producto.lean) mejora el
factor 62 a 1 para cualquier horizonte T..T+H, mediante la raíz del
producto normalizado superarmónica. Es suficiente para V3; se mantiene
abajo la cota histórica más holgada para conservar sus parámetros.
Para T>=1024 esto es como máximo `1/[4sqrt(2T+3)]`.
El caso inicial al cuadrado es
`16*62^2*61^2048*2051<=62^2048`; se propaga porque
`61^2(2T+5)<=62^2(2T+3)` para T>=29.

**Resto aditivo demasiado grande.** V2 y la definición de R dan
`P(max_(t<=H)|W_t|>R)<=1/(4Q)<=1/[4sqrt(2T+3)]`.

En el evento restante, `T<tau<=H`, `|Pi_tau*u_0|<=1` y
`|W_tau|<=R`. Luego `|c_tau|=3|u_tau|<=3(R+1)=G`.
Al restar tres cuartas partes de la cota inicial se obtiene V3.

## 4. Una palabra corta desde k=1

La política de [Hormigas](../../accesibilidad.py) llega a la fusión.
Se necesita además una cota demostrada, no la constante histórica 2,5.
Si `l=ceil(log2(2+|c|))`, basta la cota holgada

    longitud desde (1,c) <= D(c)=16(l+1)^2.               (V4)

Primero dividir c no nulo y par con bits 0 hasta hacerlo impar, y
usar bit 1. Esto fusiona o llega a `(0,g)` con `g<=max(1,|c|)` en
a lo sumo l+2 pasos. Si c=0, usar primero bit 1, que produce c=-1.

En frontera, dividir gaps pares mediante bits 0. Para g impar>=3,
la política usa el vuelco, j divisiones del offset negativo, y la
bajada: `c=-(3g-1)/2`, `j=v2(c)` y

    g'=[(3g-1)/2^(1+j)+1]/2 <= (3g+1)/4 <= 5g/6.

El viaje consume j+2 pasos. Todos los gaps decrecen y son menores
que `2^l`; el offset intermedio tiene magnitud menor que `2^(l+1)`,
por lo que j<=l. Como `(5/6)^4<1/2`, hay a lo sumo 4l viajes
impares. Los a lo sumo 4l+1 grupos de divisiones de gap consumen
cada uno a lo sumo l pasos. Al llegar a g=1, la palabra 001 fusiona.
Sumando: `l+2 + 4l(l+2)+(4l+1)l+3=8l^2+10l+5<=16(l+1)^2`.

Por bits frescos, una palabra de longitud d tiene probabilidad 2^-d.
Para `|c_tau|<=G`, V4 da el piso de éxito en un ensayo

    p(c0) >= 2^(-16(ceil(log2(G+2))+1)^2)
                 /[4sqrt(2T+3)] =: f(c0).               (V5)

Por el crecimiento declarado de G y T, existen constantes absolutas
A,B tales que

    f(c) >= exp(-A[1+log log(e^e+|c|)]^2)
                  /[B sqrt(log(e^e+|c|))].              (V6)

Este piso es más débil que el propuesto con M fijo, pero decae más
lentamente que cualquier potencia de |c|. Sobre arranques polinómicos
en el índice del ensayo, su serie diverge. Falta comprobar que los
ensayos escogidos mantienen ese control: [Ensamblaje_candidato.md](Ensamblaje_candidato.md).

## 5. Alcance formal

V1–V6 son deducciones escritas bajo la ley original. Los controles
exactos verifican las transiciones, la extensión de W, constantes y
política en dominios finitos; no prueban por sí solos los cuantificadores
infinitos. Lean certifica ingredientes, no toda esta probabilidad.
