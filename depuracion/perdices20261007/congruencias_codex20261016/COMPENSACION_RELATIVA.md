# Perdices: una compensación relativa no basta para el reloj

18-10-2026. Continúa [Reloj por rachas](RELOJ_RACHAS.md) y
[Contexto bilateral](CONTEXTO_INTERIOR.md). Se conserva Perdices, sin
reivindicar prioridad bibliográfica.

**Resultado sobre la relajación:** para cualquier fracción racional
`0<=eta<1` y constante racional `K>=0`, imponer incluso
`delta_i>=eta*H_i+K` en todas las rachas no implica un reloj uniforme.
Hay modelos con altura inicial fija, duraciones enteras 1 y 3 y coste
ilimitado. Satisfacen también una pérdida ponderada relativa de al menos
eta en **cada ventana contigua**, de cualquier longitud.
**No son contraejemplos orbitales.** La repetición real AB tiene una
barrera de divisibilidad que los excluye. El reloj general sigue abierto.

## 1. Dominio y construcción con altura fija

T es el atajo sobre enteros positivos; A=1 y B=110 son sus bloques de
paridades. Una duración A cuenta un paso T; una duración B, tres.
Aquí se estudia primero el modelo racional necesario de Reloj por rachas:

```text
H_(i+1)=H_i+gamma_(p_i)*d_i,  0<=d_i<=H_i,
gamma_A=10/17, gamma_B=1/17, delta_i=H_i-d_i.
```

No se supone que sus listas procedan de una órbita; tampoco se introduce
ley aleatoria ni condicionamiento probabilístico. H sustituye a ell en
la relajación, sin asignarle una semilla orbital.

Fijar eta,K y **una sola altura entera**
`H>=ceil((K+3)/(1-eta))`. Para todos m>=0 tomar m pares de rachas:

```text
(A,1),(B,3),...,(A,1),(B,3),
H_(2j+1)=H+13j/17,
H_(2j+2)=H+(13j+10)/17,          0<=j<m.
```

Cada duración es positiva, y las B son múltiplos de tres. Como todos
los presupuestos son >=H y d_i<=3,

```text
d_i+K <= 3+K <= (1-eta)*H_i,
delta_i >= eta*H_i+K,
L=4m.                                                    (1)
```

Para cualesquiera C*,D* reales, m suficientemente grande cumple
`4m>C*H+D*`, con el mismo H. Por tanto la reserva relativa más la
constante no implican ningún reloj uniforme en esta relajación.
Es más fuerte que la obstrucción anterior con reserva meramente constante.
El borde eta=1 es diferente: con K>=0 la condición prohíbe cualquier
duración positiva y sólo admite la lista vacía.

Este argumento utiliza únicamente que los gamma son no negativos.
También vale con `gamma_A=log2(3)-1` y
`gamma_B=(2/3)*log2(3)-1`, ambos positivos. No depende de redondear
log2(3) a 27/17. Esta extensión real se prueba aquí por escrito.

## 2. Pérdidas conjuntas: todas las ventanas y casi todo el máximo

Para cualquier lista de tipos usar el coeficiente ya definido
`C([])=0`, `C(p::s)=1+(1+gamma_p)*C(s)`. En una ventana con altura
inicial h, poner `w_i=1+gamma_(p_i)*C(cola_i)` y `Z=sum w_i*delta_i`.
La identidad previa es `coste+Z=C(ventana)*h`.

Una ventana contigua del modelo tiene r rachas, `coste<=3r`, h>=H y
`C(ventana)>=r`. Luego

```text
coste <= 3r <= (1-eta)*h*C(ventana),
Z >= eta*C(ventana)*h.                                   (2)
```

La ventana vacía tiene ambos lados cero. (2) vale para cualquier ventana,
no sólo para las de un ancho prefijado. Así, exigir una fracción fija
del descuento máximo, incluso conjuntamente, sigue siendo insuficiente
como única información adicional a la relajación. No se concluye que
cualquier otra condición conjunta sea insuficiente.

Para el modelo completo, con q=486/289>1,

```text
C_m=(44/17)*(q^m-1)/(q-1),
Z_m=C_m*H-4m,
R_m=1-Z_m/(C_m*H)=4m/(C_m*H),                 m>=1,
0<R_m<=(17/(11H))*m*q^(1-m) -> 0.                       (3)
```

El descuento recupera una fracción que tiende a uno, mientras L no está
acotado con H fijo. Ni siquiera decir que el residuo relativo decrece
exponencialmente basta: aquí su orden es `m*q^(-m)`. Un reloj uniforme
requeriría, para estas mismas listas y H fijo, un residuo de orden
`q^(-m)` con constante independiente de m.

Para cualquier lista, la condición exacta sigue siendo

```text
Z >= (C(lista)-C*)*H-D*.                                (4)
```

(4) es la reformulación anterior, ahora certificada también como
equivalencia algebraica. **No se ha demostrado (4) para las órbitas.**
El avance es distinguirla de (2) y de una mera convergencia relativa.

## 3. La aritmética que excluye estos modelos como órbitas

El control independiente no debe confundir la lista de presupuestos
con la realización de `(AB)^m`. Para una órbita real, un AB tiene
`16y=27x+19`, y por tanto `16(11y+19)=27(11x+19)`. Iterar da

```text
16^m*(11*x_m+19)=27^m*(11*n+19).
```

Como 16 y 27 son coprimos y `11n+19>0`,

```text
16^m divide 11n+19,   16^m<=11n+19<16(n+5),
L=4m <= ell(n)+3.                                       (5)
```

La última cota usa `n+5<=2^ell` y exponentes enteros. Es una aplicación
del mecanismo de [repetición](../COMPLEJIDAD.md), no una nueva solución
para historias no periódicas. Tampoco acota todos los sufijos desde n.

Ejemplo: eta=99/100, K=0 y H=300 admiten en el modelo 76 pares, con
L=304 y el 99% de pérdida en cada racha. Pero ninguna semilla con
ell=300 realiza esos 76 AB: (5) exige L<=303. El contraste finito
calcula además el cilindro y su altura mínima mediante dos algoritmos.

La obligación siguiente debe conservar una restricción aritmética de
realización capaz de controlar el **residuo absoluto** en (4) para
historias no periódicas. Un porcentaje fijo o la suma de reservas
constantes no aportan esa restricción.

## 4. Evidencia y frontera formal

[PerdicesCompensacionRelativa.lean](PerdicesCompensacionRelativa.lean):
once lemas sobre coste, longitud, reserva, admisibilidad, ausencia de
reloj con C*,D* reales en el modelo, identidad, criterio residual,
borde eta=1, balance orbital AB, divisibilidad y barrera entera.
Las ventanas generales de (2), la fórmula cerrada y el límite en (3),
la extensión a gamma reales y el corolario logarítmico de (5) conservan
prueba escrita. No se atribuye a Lean una cota orbital general.

[Compilación](evidencia_relativa.json) y [salida](evidencia_relativa.txt):
cinco módulos desde fuente, 57 consultas, Lean 4.32.2 y Mathlib fijados,
sólo axiomas estándar, sin sorryAx. Se auditan imports directos;
no toda la cadena transitiva de Mathlib.

[Cotejo](cotejar_relativa.py) y [resultado](cotejo_relativa.json):
1040 modelos con enteros/Fraction, 12048 ventanas, 50 órbitas periódicas
y el testigo de altura 300. Incluye eta=0, 1/2, 99/100, 999999/1000000;
K=0,1,17,1224; m=0 y ambos tipos al inicio de ventanas. Dos cálculos
independientes del coeficiente, dos constructores de cilindros y T
literal. Son contrastes finitos, no pruebas por barrido.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_relativa.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_relativa.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_relativa.py --pares-max 64 --ventana-max 6 --periodos-max 24 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_relativa.json
```
