# Perdices: una familia que obliga a superar la pendiente uno

18-10-2026. Continúa [Reloj terminal](RELOJ_TERMINAL.md), con el objetivo
de obtener un reloj uniforme. Se conserva Perdices, sin atribuir prioridad.

**Resultado:** para cualquier constante real D hay una semilla positiva y
una palabra real con L>ell(n)+D, incluso con sólo dos cambios de bloque.
Por tanto cualquier reloj universal L<=C*ell(n)+D necesita **C>1**.
La misma familia refuta una desigualdad multiplicativa entre los mínimos
de palabras concatenadas. **No demuestra ni refuta el reloj con C>1**;
en particular no contradice la candidata de pendiente 3 de Salidas.

**Continuación:** [Reloj por rachas](RELOJ_RACHAS.md) conserva el crecimiento
del prefijo y obtiene L+v_fin<7*ell con hasta cuatro rachas. El coeficiente
general crece; una reserva aditiva fija por racha no cierra su relajación.

## 1. Familia, dominio y realización

T es el atajo sobre enteros positivos: x/2 si x es par y (3x+1)/2 si es
impar. A=1 y B=110 son paridades reales. L cuenta pasos T, a y b cuentan
bloques; ell(n)=ceil(log2(n+5)). No hay ley aleatoria ni condicionamiento.

Para todo entero a>=2, poner

```text
b = 2*3^(a-2),       q = (2^(3b)-1)/3^a,
n = 2^(a+2)*q-1,     W = A^a B^b A^2,
L = a+3b+2.                                                   (1)
```

q es un entero positivo. En efecto 2^(3b)=4^(3^(a-1)) y
3^a divide 4^(3^(a-1))-1. Una prueba por inducción comienza en
4^3=1+9*7; al elevar 1+3^a*q al cubo, la diferencia con 1 es
divisible por 3^(a+1). No se exige que la valuación sea exactamente a.

Las fronteras de W son explícitas:

```text
n+1 = 2^(a+2)*q,
tras A^a:  x+1 = 4*3^a*q,    x+5 = 4*8^b,
tras B^b:  y+5 = 4*9^b,      y+1 = 4*(9^b-1),
tras A^2:  z = 9^(b+1)-10.                                  (2)
```

Las divisibilidades por 2^a, 8^b y 4 justifican las paridades, mediante
las fórmulas orbitales del reloj terminal. Todos los valores son positivos.
No se eligen semillas diferentes en cada frontera, ni se supone que W
sea maximal. La construcción general (2) vale para a>=0,b>=1 siempre
que 3^a*q+1=2^(3b), con q entero positivo.

## 2. Exceso sin cota aditiva

Como 2^a<=3^a, la misma semilla satisface

```text
n+5 = 4*2^a*q+4 <= 4*3^a*q+4 = 2^(3b+2),
ell(n) <= 3b+2,
L-ell(n) >= a.                                               (3)
```

Dado D real, elegir un entero a>=2 con a>D. Entonces (3) da
L>ell(n)+D. Si C<=1, también C*ell(n)+D<=ell(n)+D, así que esa pendiente
queda excluida. **No se obtiene C>=1+delta para ningún delta fijo positivo.**

Algunos miembros, contrastados con T literal:

| a | b | n | L | ell(n) | L-ell(n) |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 111 | 10 | 7 | 3 |
| 3 | 6 | 310687 | 23 | 19 | 4 |
| 4 | 18 | 14233598822306751 | 60 | 54 | 6 |
| 9 | 4374 | semilla de 13119 bits | 13133 | 13119 | 14 |

La familia tiene b exponencial en a, mientras el exceso es de orden a.
De (1), log2(n+5)=3b+2-a*log2(3/2)+o(1); por tanto L/ell(n) tiende a 1.
Es compatible con cualquier pendiente fija C>1 después de un número
finito de miembros. No proporciona una familia de contraejemplos al objetivo.

## 3. El mínimo del sufijo no se paga de nuevo

Sea r(V) la menor semilla positiva que realiza una palabra completa V.
Cada palabra de L paridades tiene una única clase de semillas módulo 2^L;
es la biyección orbital usada en los verificadores anteriores.
Tomar U=A^a y V=B^b A^2, con los parámetros de (1). Entonces

```text
r(U)=2^a-1,        r(V)=2^(3b+2)-5,        r(UV)=n.            (4)
```

Para V, la ecuación B^b es 8^b(y+5)=9^b(x+5). Exigir después A^2
equivale a 4|y+1, o 4|y+5. Puesto que 9^b es impar, resulta
2^(3b+2)|x+5, y la condición es también suficiente. Su menor positivo
es el de (4). Para UV, n realiza la palabra y 0<n<2^L por (1), así que
es su menor representante positivo. U se trata con 2^a|x+1.

Escribiendo h=(2/3)^a, se obtiene la identidad racional exacta

```text
(r(UV)+5)/(r(V)+5) = h + (1-h)/8^b <= 2*h -> 0.             (5)
```

Para la desigualdad basta b>=a: ocurre en a=2 y se conserva al triplicar b
e incrementar a. Así 8^b>=3^a y 1/8^b<=h.
En consecuencia **no existe una constante kappa>0** tal que, para todas
las palabras U,V,

```text
r(UV)+5 >= kappa*(r(V)+5),
```

ni la condición más fuerte

```text
r(UV)+5 >= kappa*(r(U)+5)*(r(V)+5).                          (6)
```

Esto refuta una vía concreta de inducción por concatenación: la parte
inicial expande la órbita antes de entrar al sufijo. No refuta una posible
desigualdad distinta para el mínimo global entre todas las palabras de
una longitud dada. La biyección y la identificación de los mínimos de (4),
así como (5)-(6), conservan prueba escrita; no se presentan como Lean.

## 4. Verificación y siguiente obligación

[PerdicesPendienteUno.lean](PerdicesPendienteUno.lean) formaliza la
divisibilidad, la realización de la familia, la longitud, la cota de altura,
el exceso arbitrario y la necesidad C>1, con D real arbitrario.
La [compilación](evidencia_pendiente.json) y su [salida](evidencia_pendiente.txt)
recompilan también transporte y reloj terminal: siete consultas nuevas,
29 con dependencias, Lean 4.32.2 y Mathlib fijado; sólo axiomas estándar.
Se comprueban imports directos, no toda la cadena transitiva de Mathlib.

[cotejar_pendiente.py](cotejar_pendiente.py) y su
[evidencia](cotejo_pendiente.json) contrastan 61 casos y 122 recorridos
completos. Incluyen a=2..9 de (1), los bordes a=0 y a=1 de la fórmula
general y dos representantes por cilindro. Dos algoritmos independientes
de cilindros, T literal y composición racional comprueban las fronteras,
los mínimos y (3)-(5). Son controles finitos, no la prueba universal.
No se repite el censo de Salidas.

**Siguiente:** buscar una cota exponencial para el mínimo global de
longitud L, conservando el transporte afín del prefijo en cualquier
descomposición. El intento de sumar costes de mínimos independientes
queda descartado por (5). Falta una estimación conjunta que controle la
semilla original sin perder el factor de expansión. El reloj uniforme
con C>1, P, MuroB y Collatz permanecen abiertos.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_pendiente.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_pendiente.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_pendiente.py --a-max 9 --b-borde-max 24 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_pendiente.json
```
