# Perdices: añadir el peso binario no repara los rangos monótonos

26-10-2026. Completa el [borrador digital del 25-10](../perdices20261025/borradores/LEEME.md)
y extiende [Retornos aritméticos](../perdices20261025/RETORNOS_ARITMETICOS.md).
Se conserva Perdices, sin reivindicación de prioridad.

**Resultado escrito:** los retornos de observaciones fijas admiten, dentro
de la misma clase aritmética y con la misma palabra, diferencias de peso
binario arbitrariamente positivas y arbitrariamente negativas. Por tanto
no funciona un rango eventualmente no decreciente en tamaño y monótono
en el peso binario, en cualquiera de los dos sentidos elegido por
observación. Esto cierra una plantilla pendiente; no prueba terminación.

## 1. Dominio y enunciado

T(n)=n/2 para n par y (3n+1)/2 para n impar, n>=1. A=1 y B=110 son
bloques de paridades **realizadas**, con fronteras impares. L cuenta pasos
T, S impares y s_2(n) los unos de la escritura binaria finita de n.
No hay ley aleatoria ni condicionamiento.

Fijar un módulo M_0>=1, un lote h>=1 y una lista finita de pares
(p_i,P_i), con p_i primo y P_i polinomio entero no nulo. Sea

```text
O(n)=(n mod M_0, v_(p_i)(P_i(n)))_i.
```

La valoración se toma del valor absoluto; las semillas elegidas evitan
todos los ceros. Existe una palabra V no vacía de A/B, con cantidad de
bloques múltiplo de h, y una clase aritmética n=n_0+Mt, t>=0, tal que
todos sus miembros realizan V, sus salidas y superan n y O(n)=O(y)=o
es constante. Además, **para todos los enteros R,X>=0** existen en esa
misma clase semillas n_+,n_->X con sus salidas correspondientes y_+,y_-
que satisfacen

```text
s_2(y_+)-s_2(n_+) > R,
s_2(y_-)-s_2(n_-) < -R.                              (1)
```

No hay una órbita infinita común a las distintas semillas. Cada retorno
es un tramo entero real desde su propio arranque fijo.

## 2. Reducción a una progresión afín

La construcción CRT de Retornos aritméticos proporciona V y la clase
anterior, con

```text
N=2^L, D=3^S>1, N*y=D*n+E,
M=N*H, y=y_0+D*H*t, y_0=(D*n_0+E)/N.
```

En aquella construcción M contiene 2^(L+k_2), de modo que N divide M.
Conserva las observaciones en toda la progresión, no sólo en t=0.
Basta probar (1) para cualquier progresión de esta forma. Las dos
construcciones siguientes conservan exactamente n=n_0 mod M; no
suponen independencia de las valoraciones ni cambian V.

## 3. Familia con aumento ilimitado del peso

Escribir M=2^a b, b impar. Elegir g>=1 con 2^g=1 mod b y 2^g>D;
para b=1 no hay restricción de orden. Elegir

```text
K>=a, 2^K>n_0, 2^(K-L)>y_0.
```

Para cada múltiplo positivo m de b poner

```text
U_m=sum_(j=0)^(m-1) 2^(gj),
n_m=n_0+2^K U_m,
y_m=y_0+D*2^(K-L) U_m.                              (2)
```

Como U_m=m=0 mod b, M divide 2^K U_m. Los trozos binarios de (2)
no se solapan: K separa la parte baja y g separa las copias de D.
Por ello, exactamente,

```text
s_2(n_m)=s_2(n_0)+m,
s_2(y_m)=s_2(y_0)+m*s_2(D).
```

D es impar y mayor que 1, luego s_2(D)>=2. La diferencia crece sin
límite, al igual que n_m. Esto prueba el primer lado de (1).

## 4. Familia con disminución ilimitada del peso

Escribir D*H=2^a d, d impar. Como D=3^S, D divide d. Elegir v>=0
de modo que

```text
v=y_0 mod 2^a,     N*v-E != 0 mod 3.
```

Se consigue empezando con el residuo de y_0 módulo 2^a y, si hace
falta, sumando 2^a una vez: N*2^a no es divisible por 3.
Elegir u en {1,...,d-1} congruente con y_0-v módulo d. Este residuo
no es divisible por 3, porque N*y_0-E=D*n_0=0 mod 3. En particular
u existe, es positivo y coprimo con D.

Tomar g con 2^g=1 mod d, poner R_0=2^g, y elegir un múltiplo K_0
de g suficientemente grande, con K_0>=a y 2^K_0>v. Definir

```text
y_j=u*2^K_0*R_0^j+v,
n_j=(N*y_j-E)/D.                                    (3)
```

CRT da y_j=y_0 mod D*H, así que n_j=n_0 mod M. Para j grande
n_j>=n_0; ambas semillas crecen sin límite. Los pesos de y_j son
constantes: s_2(y_j)=s_2(u)+s_2(v).

Para contar exactamente los de n_j, dividir

```text
N*u*2^K_0 = D*Q+r,       0<r<D,
B=N*v-E,  C=(r+B)/D,
c=r*(R_0-1)/D,          1<=c<=R_0-2.
```

C y c son enteros por las congruencias. Se obtiene

```text
n_j=Q*R_0^j+c*(1+R_0+...+R_0^(j-1))+C.              (4)
```

El término fijo C puede generar acarreos en la parte baja. No se
ignoran: elegir J tal que

```text
U_J=c*(R_0^J-1)/(R_0-1)+C,       0<=U_J<R_0^J.
```

Existe porque 0<c/(R_0-1)<1. Para j>=J, (4) tiene parte baja U_J,
j-J copias de c en base R_0 y parte alta Q. Como R_0 es potencia de 2,
las escrituras binarias no se solapan y

```text
s_2(n_j)=s_2(Q)+(j-J)*s_2(c)+s_2(U_J) -> infinito.
```

Así s_2(y_j)-s_2(n_j) tiende a menos infinito. Esto prueba el segundo
lado de (1), incluyendo los posibles acarreos y ambos umbrales R,X.

## 5. Consecuencia para los rangos

Supongamos que, para cada observación o, existe un umbral X_o y se
escoge uno de estos órdenes para el rango R(n), con valores en un
preorden:

- n<=y y s_2(n)<=s_2(y) implican R(n)<=R(y);
- n<=y y s_2(y)<=s_2(n) implican R(n)<=R(y).

Se exige sólo dentro de O(n)=O(y)=o, para n,y>X_o. La elección del
sentido puede depender de o. Elegir la familia correspondiente de (1)
superando X_o da R(n)<=R(y). Si R descendiera estrictamente cada h
bloques reales, V podría partirse en esos lotes y daría R(y)<R(n).
Contradicción.

Se descartan, por ejemplo, perfiles a_o*log(n)+b_o*s_2(n)+c_o con
a_o>=0, cualquiera que sea el signo de b_o, usados como descensos en
lotes fijos. También perfiles no lineales con esa monotonía conjunta.
Quedan fuera los perfiles que oscilan, los que observan la colocación
completa de los bits, y los presupuestos amortizados sin descenso en
cada lote fijo. No se supone que esas otras opciones funcionen.

## 6. Evidencia y formalización

El caso de O(n)=(v_2(n+1),v_2(n+5)) ya tiene dos retornos AB:

| n -> y | Firma común | s_2(n) -> s_2(y) |
| --- | --- | --- |
| 231 -> 391 | (3,2) | 6 -> 5 |
| 8423 -> 14215 | (3,2) | 7 -> 9 |

[Lean](PerdicesRetornoFirmaDigital.lean) integra el borrador y certifica
ambos recorridos literales, firmas, pesos y la imposibilidad completa
de un perfil con cualquiera de las dos monotonías por firma que
descienda en cada A/B. **La construcción general, diferencias
ilimitadas, umbrales eventuales y lotes arbitrarios conservan la prueba
escrita anterior.** No se atribuyen a Lean.
[Compilación](evidencia_lean_digital.json): ocho consultas con Lean 4.32.2,
axiomas estándar y sin sorryAx; [salida](evidencia_lean_digital.txt).
Imports directos cotejados con Mathlib fijado; sin auditoría transitiva
completa. Revisión humana pendiente.

[Cotejo](cotejar_pesos.py) y [resultado](cotejo_pesos.json): 40 retornos,
248 pasos T literales; cinco clases y cuatro miembros de cada familia.
Incluye observaciones binarias, módulo 3, primo 5, polinomio cuadrático,
11n+19 que obliga a cambiar de palabra, y lotes de tres bloques.
No se importan experimentos previos ni se repite el censo A/B.

Las diferencias medidas en la clase 231 mod 256 son 2,5,8,11 para
la familia (2), y -24,-33,-42,-51 para (3). La prueba de ilimitación
es (2)–(4), no estos cuatro valores. Las fórmulas y las semillas
pequeñas se guardan; para las grandes se conservan parámetros, tamaño,
peso y huella exacta, sin llenar el informe con miles de dígitos.

```powershell
python -B -X utf8 depuracion/perdices20261026/cotejar_pesos.py --repeticiones 4 --salida depuracion/perdices20261026/cotejo_pesos.json
python -B -X utf8 depuracion/perdices20261026/comprobar_lean.py --modulo PerdicesRetornoFirmaDigital --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --salida depuracion/perdices20261026/evidencia_lean_digital.json
```

Esto resuelve el pendiente de la ampliación digital. **No se satisface
la primera condición primordial**: se descarta una propuesta de control,
sin obtener un control individual que imponga el reloj uniforme.

Segunda [alta versionada](alta_registro.json), integrada mediante el
generador con [conservación de las 365 afirmaciones previas](evidencia_registro.json).
