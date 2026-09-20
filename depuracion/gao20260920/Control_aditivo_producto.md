# Resto aditivo y producto: certificados finitos

20-09-2026. Corolarios de Moscas y Gacelas sobre la cadena original.
Formalización de V1, V2 y dos enlaces de la ventana creciente; no es
una formalización completa de V3, CF ni una resolución de Gao.

## Ley, índices y extensión

Arranque `(2,c0)`, c0 entero firmado; mapa atajo y bits de paridad del
ancla, independientes con probabilidades 1/2. El tiempo t cuenta
pasos físicos y empieza en cero. La salida tau es la primera llegada
a k=1. Poner `u=c/3^k`, `A(0)=1/2`, `A(1)=3/2`,
`Pi_0=1`, `Pi_t=producto_(j=1..t) A(bit_j)` y `W_0=0`.

[Resto.lean](formal/Resto.lean) importa la transición completa y prueba
para todo estado interior `(k,c)`, k>=2, ambos bits y el hijo real:

    delta = u_hijo-A(bit)*u,      |delta|<=1/2.

El argumento incluye divisiones enteras, ambos signos de c y el paso
de salida k=2→1. `hijo_interior_o_salida` certifica que salir del
interior en un paso significa llegar a k=1. `EstadoW` almacena la base, W, Pi y una marca de
salida. La base sigue siempre la cadena original. Antes de salir se
actualiza `W'=A W+delta`; tras salir se actualiza `W'=A W` y `Pi'=A Pi`.
La marca permanece activa aunque la base vuelva a entrar en k>=2.

`identidad_excursion` demuestra para toda palabra cuyos estados
anteriores a cada paso son interiores:

    u_final = Pi_final*(c0/9)+W_final.

La condición permite que el estado final sea k=1; por tanto incluye
la primera salida, sin requerir permanecer en el interior después.
`base_recorre` comprueba la proyección a la cadena original y
`resto_continuacion` prueba la extensión multiplicativa tras la marca.

## Momento, máximo y coste de W

De la dominación `|W'|<=A|W|+1/2`, el promedio de las ramas satisface
la deriva de Moscas con factor `31/32` y sumando 1. El certificado
deduce, desde cualquier c0 y para todo t determinista,

    E sqrt(|W_t|) <= 32.                                  (V1)

[Maximos.lean](formal/Maximos.lean) generaliza el máximo finito del
árbol de bits. Su función `cruce` es exactamente el número de hojas
marcadas dividido por `2^H`, conservando multiplicidades. Markov
puntual y unión sobre los instantes 0..H dan

    sqrt(R)*P(existe t<=H: |W_t|>R) <= 32(H+1).             (V2)

`coste_resto_ventana` demuestra, para todo H natural y Q real positivo,
que con `R=[128(H+1)Q]^2` ese coste es <=`1/(4Q)`.
No se han condicionado bits al evento de supervivencia futura.
Tampoco se ha reemplazado t por tau en una esperanza.

Si una palabra sale con `|Pi_tau*c0/9|<=1` y `|W_tau|<=R`,
`salida_controlada` prueba `|c_tau|<=3(R+1)` por la identidad anterior
y la desigualdad triangular. Este certificado conserva esas dos
hipótesis: la probabilidad conjunta se ensambla aparte.

## Producto: mejora de la cota máxima

En [Producto.lean](formal/Producto.lean), definir
`rho=31/32`, `r=61/62`, `Q_t=Pi_t/rho^t`. Aquí Q_t es un proceso;
no es el parámetro Q de la ventana anterior. Su transición multiplica
por `A/rho`. Los cuadrados racionales comprueban

    sqrt(16/31)<=23/32,    sqrt(48/31)<=319/256,
    ((23/32)+(319/256))/2 = 503/512 < 61/62.

Por ello `V(x)=sqrt(|x|)` es superarmónica y su promedio a tiempo t
es <=`r^t V(x_0)`. `cruce_dominado` demuestra por inducción finita
que la probabilidad de cruzar `|x|>1` antes de H es <=V(x_0):
en un nodo que ya cruza, 1<=V; en los demás, se promedian las dos
cotas de los hijos y se usa la superarmonicidad.

Promediar primero los T bits iniciales entrega el certificado

    P(existe t en [T,T+H]: Pi_t>rho^t) <= r^T.             (G4f)

Vale para todos T,H naturales. `producto_palabra` identifica el
producto normalizado con Pi para cada palabra. El paso H→infinito
por continuidad creciente de probabilidades queda como deducción
escrita, no como un teorema de medida en este archivo. CF sólo necesita
un horizonte finito. G4f mejora el coste previo `62*r^T`; se conservan
los parámetros anteriores, que siguen siendo suficientes.

## Evidencia y límite actual

`lake build GaoCore GaoFormal` pasó con Lean 4.32.2 y Mathlib fijada.
Los tres archivos nuevos imprimen 20 consultas de axiomas, sólo
`propext`, `Classical.choice` y `Quot.sound`; sin `sorryAx`.
[Compilación, versiones y hashes](evidencia_resto_producto.json).
Las desigualdades racionales del producto se contrastaron también
con `Fraction`, independientemente del comprobador Lean.

Quedan las leyes de rachas, la cota de duración de excursiones,
la probabilidad conjunta de V3 y los ensayos guardados de CF. El P2
original exige una ventana constante bajo condicionamiento; estas
cotas de ventana creciente no lo demuestran ni lo refutan.
