# Perdices: defecto fijo con contexto a ambos lados

18-10-2026. Continúa [Defecto interior](DEFECTO_INTERIOR.md) y
[Reloj por rachas](RELOJ_RACHAS.md). Se conserva Perdices, sin reivindicar
prioridad bibliográfica.

**Resultado:** sean U cualquier palabra terminada en B y V cualquier
palabra, incluso vacía. Hay infinitas semillas positivas que realizan
`U A^a B A^2 V`, con a arbitrariamente grande y **parte impar 13** en la
entrada de la racha A central. El defecto de esa racha es fijo: depende
de U, pero no de a ni de V. Su proporción respecto al presupuesto tiende
a cero. Por tanto, imponer cualquier cantidad prefijada de cambios
anteriores y posteriores tampoco da una pérdida proporcional por racha.
**La suma conjunta de defectos y el reloj uniforme siguen abiertos.**

## 1. Dominio y fórmulas

T es el atajo sobre enteros positivos: n/2 para n par y (3n+1)/2 para n
impar. A=1, B=110 son bloques de paridades reales. Todas las longitudes
cuentan pasos T. No hay ley aleatoria ni condicionamiento probabilístico.
U termina en B; P=|U|, S es su número de impares, y

```text
T^P(n)=(D*n+E)/N en el cilindro de U,
N=2^P, D=3^S, R=N+E, C=5D-R,
d=floor(log2(16D/13)).
```

Se tienen S>=2, `4N<=C<=4D` y 3 no divide R, por la prueba de
Defecto interior. Existen una clase a módulo un entero positivo y un
umbral, dependientes de U,V, tales que todos sus a superiores al umbral
son impares, positivos, y

```text
n_a=(13*2^(P+a+2)-R)/D
```

es el mínimo positivo del cilindro `U A^a B A^2 V`. En la racha central:

```text
x+1=13*2^(a+2),             z+1=52*3^a,
ell(n_a)=P+a+6-d,           L=P+a+5+|V|,
H_A=ell(n_a)+(27/17)*S-P,
delta_A=H_A-a=6+(27/17)*S-d,
L-ell(n_a)=|V|+d-1.                                      (1)
```

x,z son las fronteras anterior y posterior de A^a. Es una racha máxima
de la palabra: U termina en B y el sufijo comienza en B. La parte impar
de x+1 es exactamente 13. Las semillas cambian con a.

## 2. La condición del pasado

La congruencia necesaria para que n_a sea entero es

```text
2^(P+a+2) = R/13 mod 3^S.                                (2)
```

13 es invertible módulo 3^S. El levantamiento ternario ya probado en
Defecto interior da una clase `a=a_3 mod Q_3`, `Q_3=2*3^(S-1)`.
**a_3 es impar.** En efecto, al escribir U=U_0 B, tenemos
P=P_0+3 y R=13*2^P_0+9E_0, por lo que (2) módulo 3 exige
P+a+2=P_0 módulo 2, es decir a=1 módulo 2.

Si n_a es positivo, `D*n_a+E=N*(13*2^(a+2)-1)` identifica el cilindro
de U: D es impar y ese cilindro es la única solución de la congruencia
afín módulo N. U llega a x, A^a es real por divisibilidad, y llega a z.

## 3. La condición del futuro

Sea W=`B A^2 V`, l=|W|>=5, y r su menor representante positivo módulo
2^l. Sus cinco primeras paridades son 11011, por lo que `r=27 mod 32`.
Esto se comprueba también invirtiendo esos cinco pasos: su cilindro es
27 módulo 32. Por tanto t=(r+1)/4 es entero y t=7 módulo 8.

Poner m=l-2>=3. Para que z=52*3^a-1 pertenezca al cilindro de W basta
y es necesario que

```text
3^a = t/13 mod 2^m.                                     (3)
```

El lado derecho es 3 módulo 8, pues 13 inverso es 5 módulo 8.
Las potencias de 3 con exponente impar recorren precisamente todas las
unidades congruentes con 3 módulo 8, para cada módulo 2^m, m>=3.
Una prueba elemental, sin presuponer que (3) es soluble:

```text
3^(2^(j-2)) = 1+2^j*u_j,       u_j impar, j>=3.
```

El inicio es 9=1+8. Al cuadrar se obtiene
`u_(j+1)=u_j+2^(j-1)*u_j^2`, todavía impar. Si e resuelve (3) módulo
2^j, sus extensiones e y e+2^(j-2) difieren por 2^j veces una unidad
en sus potencias de 3, módulo 2^(j+1). Exactamente una es el objetivo.
Se empieza con e=1 módulo 2 cuando m=3. Esto da una clase
`a=a_2 mod Q_2`, `Q_2=2^(m-2)`, con a_2 impar, y 3^Q_2=1 módulo 2^m.

**Compatibilidad:** `gcd(Q_2,Q_3)=2` y a_2,a_3 son impares. Al dividir
por 2 la diferencia de las congruencias, sus módulos son coprimos; el
teorema chino del resto produce una clase módulo `lcm(Q_2,Q_3)` que
satisface ambas. Contiene a positivos arbitrariamente grandes.
Así quedan realizados el pasado y el futuro desde la **misma semilla**.

Además `0<n_a<2^(P+a+5+|V|)`, porque `13<8D*2^|V|` y R>0.
Como n_a realiza la palabra completa, es su mínimo positivo.

## 4. Altura y límite exactos

No hay igualdad entre 16D y 13 por una potencia de 2, puesto que D=3^S.
De la definición de d:

```text
13*2^d < 16D < 13*2^(d+1).
```

Sea h=P+a+6-d. Para a suficientemente grande, h>=1, n_a>0 y

```text
16D*(n_a+5)=13*2^(h+d)+16C,
16C <= 2^h*(16D-13*2^d).                                (4)
```

La segunda desigualdad vale, por ejemplo, si h>=bit_length(16C),
pues la diferencia entre paréntesis es un entero positivo. (4) y los
dos lados estrictos para d implican `2^(h-1)<n_a+5<=2^h`, de donde ell=h.
Esto prueba (1) por aritmética entera.

delta_A es positivo y fijo, y H_A=a+delta_A tiende a infinito. En
particular, para todo eta>0 y todos los contextos U,V elegidos, algún
miembro cumple `delta_A<eta*H_A`. Se pueden fijar U y V con tantos
cambios como se quiera **antes** de elegir a. La constante del defecto
no aumenta al alargar V: sólo cambia la progresión admisible de a.

Con el presupuesto exacto `H_A^*=log2(n_a+5)+S*log2(3)-P`:

```text
H_A^*-a = 2+log2(13)+log2(1+C/(13*2^(P+a+2)))
         -> 2+log2(13).                                 (5)
```

El fenómeno no procede del redondeo ni de sustituir log2(3) por 27/17.
Para cada U,V fijados, L/ell tiende a 1. No se construye una órbita
infinita desde una semilla fija ni se refuta ningún reloj de pendiente >1.

Ejemplo reproducible con futuro no vacío: U=B, V=BAB. Sirve
`a=481+768j`, j>=0, con `n_a=13*(2^(a+5)-1)/9`. La palabra es
`B A^a B A^2 B A B`, ell=a+6, L=a+15 y delta_A=105/17.
La racha central tiene cambios posteriores y, aun así, su defecto
relativo es `105/(17a+105)`, que tiende a cero.

## 5. Qué obliga a cambiar en la búsqueda

La familia anterior de parte impar 1 sí tiene poco futuro: después de
A^k llega a z=4*3^k-1 y B llega a y=(3^(k+2)-1)/2. Si k es par, y es
par; si k es impar, y=1 módulo 4 y un A adicional llega a un par.
No puede haber un segundo B después de ese B. Con prefijo terminado
en B, la construcción anterior fuerza k impar. Esta observación por sí
sola dejaba abierta una pérdida proporcional lejos del final.

La nueva familia de parte impar 13 descarta esa posibilidad en toda
racha individual, aun con contexto fijo arbitrariamente largo a ambos
lados. **No descarta una pérdida conjunta**: las demás rachas tienen
duraciones fijas cuando U,V están fijados, mientras sus presupuestos
crecen con a. Sus defectos pueden compensar el de la racha central.
Las barreras de parejas y triples se conservan; no se han hecho pequeños
los defectos de todas las rachas de una ventana.

Siguiente obligación: obtener una estimación para la suma ponderada de
varias pérdidas que permita redistribuirlas entre rachas, sin deducir
una pérdida proporcional positiva para cada una.

[Compensación relativa](COMPENSACION_RELATIVA.md) precisa que una fracción
fija del descuento máximo, incluso en todas las ventanas, tampoco basta
por sí sola en la relajación. Se distingue de la cota del residuo absoluto
necesaria para el reloj y de las restricciones de realización orbital.

## 6. Evidencia y frontera formal

[PerdicesContextoInterior.lean](PerdicesContextoInterior.lean) certifica
siete lemas: racha con parte impar 13, residuo de su frontera bajo la
congruencia indicada, empalme con caminos dados, largo, altura bajo (4),
defecto fijo y exceso fijo. **Los levantamientos, CRT, el cilindro general,
la existencia universal de los contextos y los límites sólo tienen prueba
escrita.** Lean no certifica esa existencia mediante el lema de empalme.

[Compilación](evidencia_contexto.json) y [salida](evidencia_contexto.txt):
tres módulos desde fuente, 29 consultas; Lean 4.32.2/Mathlib fijados,
axiomas estándar, sin sorryAx. Se auditan imports directos, no toda la
cadena transitiva de Mathlib.

[cotejar_contexto.py](cotejar_contexto.py) y [resultado](cotejo_contexto.json):
45 pares de contextos, 90 miembros y 21 bordes. Contrastan ambos
levantamientos con ciclos modulares completos, CRT,
inversa literal y T directo, dos constructores del cilindro, altura y
defecto con enteros/Fraction. Los casos y parámetros constan en el JSON;
se incluyen V vacío y 21 bordes de la familia anterior. El contraste
finito no sustituye la prueba universal.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_contexto.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_contexto.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_contexto.py --prefijos-max 2 --sufijos-max 3 --miembros 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_contexto.json
```
