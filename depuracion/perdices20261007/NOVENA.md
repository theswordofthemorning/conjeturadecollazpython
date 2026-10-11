# Perdices: la exclusión del tres mejora la sexta raíz a novena

10-10-2026. Continuación de [Semilla](SEMILLA.md), [Tamaño](TAMANO.md)
y [Cruce](CRUCE.md). Se conserva el nombre Perdices. La restricción
módulo 3 es elemental; se desarrolla aquí su efecto sobre estas cotas,
sin reclamar prioridad bibliográfica.

**Resultado:** bajo fuga pura, el tamaño normalizado satisface
`R_k^9<=3 n^9(2S_k+1)`. Combinado con la cuenta existente de casi
fugitivos, mejora los regresos a techo fijo de `O(K^(4/25))` a
`O(K^(8/75))`. Infinitos regresos exigirían excursiones
`d>H(x+1)^8` en toda cola, para cada H fijo. Por tanto bastaría
demostrar la cota superior opuesta, más permisiva que la quinta
potencia propuesta antes. **Esa cota superior sigue abierta.**

## 1. Dominio y restricción orbital

Atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, sobre
naturales. Las órbitas objetivo parten de n>0. `x_j=T^j(n)`,
`S_k=#{j<k:x_j impar}`, `P_k=3^S_k/2^k` y `R_k=x_k/P_k`.
k cuenta pasos del atajo. No hay ley aleatoria ni independencia.

`FugaPura n` significa P_j>=1 para todos los j. Implica n>=2,
ausencia de descenso e inyectividad orbital; se usa como hipótesis,
no se afirma su existencia. El lema del producto admite prefijos
finitos más generales, con impares distintos y al menos 3.

Si x es impar, `2T(x)=3x+1`, luego 3 no divide T(x). Si 3 no
divide x, tampoco divide T(x): para x par, `2T(x)=x`; para impar,
vale el argumento anterior. En consecuencia, después del primer
paso impar todos los valores evitan los múltiplos de 3. **Puede
haber como máximo una entrada impar divisible por 3**, incluso
cuando n tiene inicialmente factores de 2 y 3.

Esta restricción no requiere fuga pura. La inyectividad y el piso
3 de las entradas impares son condiciones adicionales del producto.

## 2. Producto finito y novena raíz

Sea A un conjunto de q impares distintos, >=3, ninguno divisible
por 3. En orden creciente sus elementos comienzan como
`5,7,11,13,17,19,...`; el i-ésimo, para i>=1, es >=3i+1.
Una prueba sin ordenar: `x -> floor((x-1)/3)` es inyectiva sobre
esos enteros, tiene valores positivos y envía los elementos <=a
al intervalo `1..floor((a-1)/3)`. Así, el máximo es >=3q+1.

El telescopio que se necesita es

```text
(2r+1)(9r+13)^9 <= (2r+3)(9r+12)^9,       r>=0.           (1)
```

Lean lo prueba expandiendo la diferencia como un polinomio de
coeficientes naturales positivos, de grado ocho. El cotejador
reconstruye esos coeficientes con el binomio de Newton.

Una derivación independiente de (1), con a=r+1, usa

```text
9 log(1+1/(9r+12)) <= 9/(9r+12) <= 1/(r+1)
                   <= log((r+3/2)/(r+1/2)).
```

La última desigualdad resulta de integrar
`1/t >= 2/a-t/a^2` entre a-1/2 y a+1/2; su diferencia es
`(t-a)^2/(a^2 t)>=0`. Esta derivación se escribe aquí;
la prueba Lean usa sólo la identidad polinómica exacta.

Quitando el mayor de A y aplicando (1), se obtiene por inducción

```text
[producto_{a en A}(1+1/(3a))]^9 <= 2q+1.                 (2)
```

Si hay una excepción b>=3 divisible por 3, se separa su factor:
`(1+1/(3b))^9 <= (10/9)^9 < 3`. La cota, incluyendo también el
caso sin excepción, queda

```text
[producto_{a en A}(1+1/(3a))]^9 <= 3(2q+1).             (3)
```

La [identidad multiplicativa](PerdicesTamano.lean) es
`R_k=n producto_{j<k,x_j impar}(1+1/(3x_j))`. Por tanto, para un
prefijo con entradas impares distintas y >=3,

```text
R_k^9 <= 3 n^9(2S_k+1).                                (4)
```

Los 3-divisibles son a lo sumo uno por §1. Una fuga pura cumple
las demás hipótesis para todo k, lo que da `R_k=O_n(k^(1/9))`.
Para P_k<=C, C natural, resulta

```text
x_k^9 <= 3 C^9 n^9(2S_k+1).                            (5)
```

La sexta raíz anterior sigue siendo válida y puede ser mejor en
horizontes pequeños. Para comparar las dos cotas de R/n basta
comparar `9(2S+1)^2` con `(S+1)^3`. La novena es menor para S>=34:
con S=34+t, la diferencia es `t^3+69t^2+1191t+26>0`.
No se descarta la cota anterior al elegir la mejor.

## 3. Regresos: de 4/25 a 8/75

Fijar n y c, C=3^c, y `F=#{j<K:P_j<=C}`. Para j<K,
`2S_j+1<=2K`, de modo que (5) encierra cada valor contado en
`1..X`, donde

```text
Q=6(Cn)^9 K,          X^9<=Q<(X+1)^9.                   (6)
```

Cada valor es distinto y es `CasiFuga c`, con el **mismo nivel**
c, exactamente como en [Cruce, §2](CRUCE.md#2-la-combinación-conserva-el-techo-y-la-semilla).
Así, para todo m natural,

```text
F <= (floor((X+1)/2^(100m))+1) 2^(c+96m),
F^25 <= 2^(25c+125)(X+1)^24.                            (7)
```

Para K>0, X>=1 y `(X+1)^9<=2^9 Q`. Elevando (7) a nueve y
sustituyendo (6), se obtiene la desigualdad entera formalizada

```text
F^225 <= 2^(225c+1341) 6^24 (Cn)^216 K^24.              (8)
```

K=0 se trata aparte y da F=0. El exponente es
`24/225=8/75≈0,10667`, frente a `4/25=0,16`. Las constantes
dependen de n y c; no es una cota uniforme sobre todas las semillas.

La mejora también compara las constantes. Sean L_6 y L_9 los lados
derechos de las cotas de potencias 150 y 225. Para K>0,
`L_9^2/L_6^3=(36/K)^24`: coinciden las potencias de 2 y de Cn.
Por tanto, para K>=36, (8) implica la cota anterior al elevar a 450
y tomar la raíz cúbica. Es una comparación escrita de las dos
desigualdades formalizadas, no sólo de sus exponentes asintóticos.

Comparación aritmética de radios para Cn=81; **no es una medición
de una órbita fugitiva**:

| K | Radio de sexta raíz | Radio de novena raíz |
|---:|---:|---:|
| 36 | 147 | 147 |
| 1000 | 256 | 212 |
| 10^12 | 8100 | 2129 |
| 10^24 | 810000 | 45878 |

Antes de redondear, los radios son `Cn K^(1/6)` y
`Cn (6K)^(1/9)`. El segundo es menor para K>36. Por tanto el
radio entero nuevo nunca es mayor para K>=36. La tabla sólo
evalúa esos límites condicionados, no sus hipótesis orbitales.

## 4. La reducción de duración se vuelve octava

Enumerar los regresos consecutivos como t_i y escribir
`x_i=T^(t_i)(n)`, `d_i=t_(i+1)-t_i`. De (8) se deduce

```text
(i+1)^225 <= A(t_i+1)^24,
A=2^(225c+1341) 6^24 (Cn)^216.                           (9)
```

En particular, ningún B fijo permite `t_i+1<=B(i+1)^9`
para todos los i. Al sustituir esa cota en (9) y cancelar
`(i+1)^216`, quedaría `(i+1)^9<=A B^24` para todos los i.

Como x_i>=1, (5) también da

```text
(x_i+1)^9 <= 3072(Cn)^9(t_i+1).                         (10)
```

Si `d_i<=H(x_i+1)^8` en toda una cola, entonces
`d_i^9<=D(t_i+1)^8`, con `D=H^9[3072(Cn)^9]^8` fijo.
La inducción de [Semilla](SEMILLA.md) se adapta a nueve:
para `B=D+t_0+1`, `t_i+1<=B(i+1)^9` implica
`d_i<=B(i+1)^8`; usar `(i+1)^9+(i+1)^8<=(i+2)^9` cierra
la inducción. Es la cota prohibida por (9). Como la lista puede
empezar después de cualquier U,

```text
FugaPura n e InfinitosRegresos n c implican:
para todo H,U hay u<v consecutivos, u>U,
                  v-u > H(T^u(n)+1)^8.                 (11)
```

La enumeración, el tiempo de grado nueve, la contradicción y la
contraposición orbital están formalizados. **No se ha obtenido
una cota superior de duración.** Para excluir este frente basta
ahora una cota de octava potencia; se permite más duración que
con la quinta, pero aún hay que demostrarla. Cohete y grieta
requieren argumentos adicionales.

## 5. Qué queda por aportar y evidencia

La inyectividad sola acota la duración mediante una **altura que
todavía hay que controlar**. Si una excursión comienza en x y
sus d entradas permanecen entre x y V, todas distintas, entonces
`d<=V-x+1` por conteo de enteros. Los valores interiores son >=x
porque el factor local supera el nivel de entrada. No tenemos
un techo V en función de x que produzca la cota de (11).
Reemplazar «duración» por «altura» no elimina esa deuda.

El siguiente trabajo debe probar una restricción de retorno que
controle duración o altura mediante la semilla local y su congruencia.
La exclusión de 3 ya está incorporada en (4); esa estimación del
producto no proporciona la cota superior que falta.

[PerdicesNovena.lean](PerdicesNovena.lean): 26 lemas nuevos,
incluido el enlace orbital completo de (4), (8) y (11).
[comprobar_novena.py](comprobar_novena.py) compila únicamente
este módulo y audita 21 previos: 22 módulos, 232 consultas.
Lean 4.32.2, sólo axiomas estándar, sin avisos ni pruebas incompletas.
Sin hipótesis externas en los nuevos enunciados.
[Evidencia](evidencia_novena.json), [salida](evidencia_novena.txt).
Revisión humana pendiente. Lean certifica los enunciados, no su interpretación.

[cotejar_novena.py](cotejar_novena.py), con enteros y `Fraction`:

- 4096 subconjuntos de doce impares admisibles; 8192 casos con
  excepción adicional 3 o 9; conjunto vacío incluido.
- Coeficientes del polinomio (1), obtenidos independientemente,
  y 2001 evaluaciones exactas r=0..2000.
- Semillas 1..512, hasta 256 pasos: 131072 controles de la
  restricción modular y 18555 prefijos que cumplen las hipótesis
  finitas del producto; 5730 incluyen la excepción. En 2596
  prefijos la cota de novena raíz es menor que la anterior.
- Controles que fallan al retirar hipótesis: n=1 en el primer
  paso; dieciséis copias del impar 5; los 48 impares 3..97 sin
  limitar sus múltiplos de 3. No son contraejemplos orbitales
  bajo fuga pura: identifican las condiciones necesarias del lema.
- Noventa evaluaciones de los radios, incluido K=0 y los bordes
  35,36,37. También pasó la configuración mínima del cotejador.

[Resultado](cotejo_novena.json). Estos prefijos no verifican
FugaPura ni infinitos regresos. No se usa un barrido finito para
concluir (4), (8) o (11).

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_novena.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_novena.json
python -B -X utf8 depuracion/perdices20261007/cotejar_novena.py --elementos 12 --factor-max 2000 --n-max 512 --pasos 256 --salida depuracion/perdices20261007/cotejo_novena.json
```

Si faltan objetos previos, reproducir primero [Semilla](SEMILLA.md#5-alcance-formal-cotejo-y-siguiente-trabajo).
Collatz, el planeador intermitente, el cohete y la grieta siguen abiertos.
