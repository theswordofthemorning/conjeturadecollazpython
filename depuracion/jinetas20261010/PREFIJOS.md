# Jinetas: conservar una semilla no da todavía una reducción

**Continuación ejecutada el 10-10:** la [revisión de rachas](RACHAS.md)
precisa el coste de reiniciar y documenta la decisión siguiente. El
apartado final conserva la propuesta que dio origen a esa revisión.

10-10-2026. Segundo ensayo de la [ruta](../casa20261004/RUTA_20261010.md),
continuación del [intercambio](LEEME.md). Se mantiene el nombre Jinetas;
son consecuencias elementales de las herramientas existentes, sin
atribución de novedad matemática.

**Resultado:** hay un intervalo exacto y monótono de semillas compatibles
con todos los prefijos. Sirve para podar una rama cuando queda vacío.
Pero en el primer cruce se reduce al criterio CST ya estudiado por
Ocelotas. En una rama infinita, impedir que su semilla mínima quede
acotada equivale a impedir una semilla fija que nunca desciende. Ninguna
de esas reformulaciones aporta la desigualdad adicional pedida por la
ruta. Se cierra este segundo mecanismo como argumento suficiente por sí
solo y se vuelve al balance. **No se demuestra CST ni Collatz.**

## Convenciones y conjunto que se conserva

Atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar, sobre enteros
positivos. Las semillas candidatas son `n≥3`; 1 y 2 se tratan aparte.
Una palabra temporal w tiene L bits, con `w_j` la paridad de `T^j(n)`.
Para su prefijo de longitud j, incluido j=0, definir

```text
M_j = 2^j,       A_j = 3^S_j,       D_j = M_j-A_j,
M_j T^j(n) = A_j n+B_j,             B_j ≥ 0,
r_j = -B_j A_j^(-1) mod M_j,        0 ≤ r_j < M_j.
```

`S_j` cuenta entradas impares antes de j. L y j cuentan pasos del atajo;
B es el numerador entero del término aditivo. No hay ley aleatoria ni
condicionamiento probabilístico. La hipótesis determinista exigida es
`T^j(n)≥n` en **todos** los prefijos hasta L.

Sea `m_L` el menor entero ≥3 congruente con `r_L` módulo `M_L`:

```text
m_L = r_L + M_L max(0, ceil((3-r_L)/M_L)).
H_L = min { floor(B_j/D_j) : 1≤j≤L, D_j>0 },
```

con `H_L=∞` si no hay cruce. En j=0: `m_0=3`, `H_0=∞`.
El conjunto exacto de semillas de la palabra que nunca bajan en ese
horizonte es

```text
C_L(w) = { m_L + t M_L : t entero ≥0, m_L+t M_L ≤ H_L }.       (1)
```

**Prueba.** La congruencia final caracteriza la palabra y sus prefijos
(biyección de paridades, justificada en [Jinetas](LEEME.md)). La identidad
afín da `T^j(n)≥n ↔ D_j n≤B_j`. Si `D_j≤0`, esto es automático porque
`n>0` y `B_j≥0`. Si `D_j>0`, equivale a `n≤floor(B_j/D_j)`. Intersectar
estas condiciones da (1). No se sustituye una semilla por otra al aplicar
el criterio: para estudiar n se sigue exclusivamente su palabra `w_L(n)`.

Cuando H es finito, el número de candidatos es exactamente

```text
N_L = max(0, 1+floor((H_L-m_L)/M_L)).                         (2)
```

La condición terminal es `m_L>H_L`. Incluye correctamente los residuos
0, 1 y 2 y la igualdad `m_L=H_L`, que deja un candidato, no cero.

## Monotonía válida, sin garantía de terminación

Al extender w por un bit, la nueva clase residual está contenida en la
anterior. Por tanto `m_(L+1)≥m_L`. Si aparece una cota nueva, H se
actualiza por un mínimo, luego `H_(L+1)≤H_L`.
Además `C_(L+1)⊆C_L`. Una rama vacía no revive, y tanto N como la holgura
entera `H-m` son no crecientes después del primer cruce.

Esto repara el fallo del intercambio `01/10`: la extensión conserva
los prefijos y las semillas que todavía sobreviven. Sin embargo,
**no se ha demostrado un descenso estricto de ninguna de esas cantidades**.
Si H es finito y `2^L>H`, una rama viva contiene exactamente una semilla.
Decidir que ese último candidato también desaparece es el problema
orbital pendiente. Contar candidatos ya no lo resuelve.

Usar el mínimo racional antes de redondear tampoco crea un orden bien
fundado: una sucesión como `13+1/k` puede disminuir siempre sin pasar de
13. Es un ejemplo lógico sobre cotas, no una órbita atribuida a Collatz.

### Testigo de lo que sí elimina: n=7

La órbita `7,11,17,26,13,20,10,5,8` tiene palabra `11101001`.
El ejemplo ya aparece en Rozier–Terracol,
[v5, §1](https://arxiv.org/html/2502.00948v5#S1).

| Horizonte | Final | A | B | D | Cota del último paso | H de todos los prefijos |
|---|---:|---:|---:|---:|---:|---:|
| 7 | 5 | 81 | 73 | 47 | 1 | 1 |
| 8 | 8 | 243 | 347 | 13 | 26 | 1 |

En ambos casos `m=7`. El segmento de ocho pasos es paradójico, pero
su rama ya quedó vacía en el séptimo. Exigir sólo la cota final perdería
esa información. La poda no prueba que todos los segmentos paradójicos
tengan esa forma.

### Control de terminación: el ciclo vecino

En el mapa auxiliar `T_5(n)=n/2` si es par y `(5n+1)/2` si es impar,
el ciclo es `13,33,83,208,104,52,26,13`. No se cambia el problema objetivo:
este control comprueba qué se puede deducir de las propiedades compartidas
por ambas álgebras.

Su primer cruce es j=7, con `A=125`, `M=128`, `B=39`, `D=3`.
Desde entonces `m_L=H_L=13` y `N_L=1` para todo L≥7: el mínimo de la
órbita sigue siendo 13, y la primera cota ya vale 13. En q vueltas,

```text
A_(7q)=125^q, M_(7q)=128^q,
B_(7q)=13(128^q-125^q),       B_(7q)/D_(7q)=13,   q≥1.
```

Así, anidamiento, positividad, divisibilidad y monotonía de las cotas
admiten una rama viva eterna. Esto **no refuta una reducción especial
para el factor 3**: demuestra que le hace falta una propiedad adicional.
El ciclo vecino ya estaba en [CasaGrieta](../casa20261004/CasaGrieta.lean);
aquí se usa para auditar el nuevo candidato a medida de progreso.

## Primer cruce: vuelve exactamente CST

Si w termina en su primer cruce, `D_j≤0` para j<L y `D_L>0`.
Entonces no hay ninguna cota anterior que aprovechar:

```text
H_L = floor(B_L/D_L),
C_L(w) vacío  ↔  D_L m_L > B_L.                            (3)
```

Exigir (3) para **toda** palabra de primer cruce equivale a que cada
entero ≥3 que cruza descienda en ese mismo instante. La prueba en ambas
direcciones es directa: todo entero realiza una de esas palabras y,
si (3) falla, su mínimo m realiza la palabra, no desciende antes (no hay
cruce) y tampoco desciende al cruzar. Si no hay cruce, no puede haber
descenso. Añadiendo el caso n=2, esto es CST, con ambos tiempos infinitos
permitidos; **no demuestra que el cruce exista**.

Se cotejó esta identificación con las formulaciones C1–C3 de
[Rozier–Terracol, §1](https://arxiv.org/html/2502.00948v5#S1) y con el
[teorema E y la grieta](../casa20261004/CasaGrieta.lean).
Los tramos certificados de [Ocelotas](../cst20260930/VEINTICUATRO_LEAN.md)
ya trabajan sobre este obstáculo. El intervalo de prefijos no extiende
su número de rachas ni elimina sus hipótesis externas.

### El relleno no evita esta dificultad

No se puede aplicar «nunca baja de su inicio» a la palabra trasladada
`0^k w` desde `2^k n`, con k>0. Su primer cero tiene D=1, B=0: H pasa
a cero y su C queda vacío inmediatamente. Esto sólo registra el descenso
inicial conocido. **No contradice que después haya una paradoja**, ni que
la cola desde n nunca baje de n. Si se exige el no-descenso únicamente
respecto de n en esa cola, se recupera exactamente (1) para w. El
[traslado](TRASLADO.md) no aporta aquí otra restricción.

## Una rama infinita no es todavía una semilla entera fija

Para cada L≥2, `n_L=2^L-1` realiza L unos seguidos. En sus prefijos,

```text
T^j(n_L)=3^j 2^(L-j)-1 ≥ n_L,       0≤j≤L.
```

Para j<L el valor es impar, lo que prueba inductivamente la fórmula.
Aquí `H_L=∞`, `m_L=2^L-1`: hay una rama infinita de palabras vivas,
pero ningún entero positivo realiza todos sus niveles. Sus residuos
crecen sin cota. Confundir `para cada L existe n_L` con `existe n para
todo L` reintroduciría el error que debía evitar este ensayo.

Para una rama infinita w con `C_L(w)` no vacío en cada nivel, vale:

```text
los mínimos m_L están acotados
    ↔ existe un mismo n≥3 en todos los C_L(w).                (4)
```

**Prueba.** Si tal n existe, `m_L≤n`. En sentido contrario, m es una
sucesión entera no decreciente y acotada: alcanza un máximo n y queda
constante. En cada nivel posterior, n pertenece a C por (1); en todos
los anteriores, por anidamiento. La congruencia en todos los módulos
`2^L` hace única a esa semilla común. Es su misma órbita la que nunca
desciende. Para una semilla fija n, además `m_L=n` en cuanto `2^L>n`.

Por ello pedir que los mínimos de **todas** las ramas vivas infinitas
tiendan a infinito equivale al descenso eventual de cada n≥3, y por
inducción fuerte, a Collatz. No es una hipótesis más débil ya disponible.
En ramas sin cruce H permanece infinito: el techo de (1) no toca al
cohete ni al planeador intermitente.

## Evidencia y alcance formal

[JinetasPrefijos.lean](JinetasPrefijos.lean) comprueba 15 enunciados:
identidad del margen, redondeo entero, restricciones automáticas sin
cruce, herencia, redundancia en el primer cruce, intersección de cotas,
mínimos anidados, holgura, poda persistente, criterio por el mínimo,
equivalencia abstracta (4), el testigo 7 y el ciclo vecino para todo tiempo.
Sólo axiomas estándar; sin avisos ni `sorryAx`.

La formalización de (4) es para conjuntos anidados con mínimos elegidos;
su aplicación a las palabras y la unicidad por módulos crecientes se
prueban por escrito arriba. Este módulo **no formaliza la biyección general
de paridades, el conjunto (1) desde T, ni la equivalencia completa con
CST o Collatz**. No contiene un teorema de exclusión universal.

[verificar_prefijos.py](verificar_prefijos.py) contrasta la recurrencia
afín y el intervalo con órbitas calculadas por separado: 1022 palabras,
L=0…8 y factores 3 y 5; 1426 semillas, 822 intervalos finitos y 7172
controles de transición. Las 822 comprobaciones de primer cruce cuentan
su aparición en cada palabra, con repeticiones entre palabras.
Comprueba además cuatro vueltas del vecino, seis horizontes de unos
hasta L=64, el cero, 1, 2, residuos pequeños, techo infinito y margen
nulo. Son controles finitos; las afirmaciones universales descansan
en las pruebas, no en extrapolar esas cifras.

```text
python -B -X utf8 depuracion/jinetas20261010/verificar_prefijos.py --longitud-maxima 8 --vueltas-vecino 4 --salida depuracion/jinetas20261010/cotejo_prefijos.json
python -B -X utf8 depuracion/jinetas20261010/comprobar_prefijos.py --salida depuracion/jinetas20261010/evidencia_prefijos.json
```

[Cotejo exacto](cotejo_prefijos.json) y [evidencia Lean](evidencia_prefijos.json):
Lean 4.32.2, Mathlib fijado, huellas de fuentes y comprobadores y salida
de `#print axioms`. No se reutilizan cachés locales de Casa, no se
recalculan censos históricos y no se integran los avances locales previos.
Revisión humana pendiente.

## Decisión y siguiente acción

La extensión por prefijos conserva la semilla y corrige el problema del
intercambio, pero su candidato a invariante es la intersección del criterio
afín existente. No se encontró una ley adicional que fuerce la condición
terminal. Se cumple la cláusula de parada de la ruta: **volver al balance,
sin ampliar tablas ni anunciar una reducción nueva**.

La próxima revisión matemática debe volver a la criba por prefijos de
Ocelotas y localizar qué desigualdad dependiente del factor 3 podría
permitir reducir el número de rachas sin una cota fija. Antes de ejecutar
otro censo, debe escribir la regla, sus hipótesis, la cantidad entera que
disminuye estrictamente y el caso terminal. Es una búsqueda pendiente,
no una inducción ya construida. Aun un cierre completo de CST dejaría
pendiente el muro B, la existencia universal del cruce.
