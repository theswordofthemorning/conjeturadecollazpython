# Perdices: tamaño de la población protegida y límite del certificado

25-10-2026. Continuación de [Umbral](../perdices20261007/UMBRAL.md),
especialmente su segunda tarea probabilística. Se conserva Perdices;
no se reclama prioridad para los argumentos elementales de rotación,
conteo binomial o inclinación de pesos.

**Resultado escrito:** para todo horizonte K>=1 y bloque terminal
1<=L<=K, la fracción protegida de aquella nota satisface

```text
G(K,L) <= min(1, K(K+1)(3/4)^L).                         (1)
```

Además, el certificado `F=1-G(1-q)` tiene un piso de 1/31 en una
proporción positiva de horizontes, cualquiera que sea la longitud
elegida en cada uno. Este piso pertenece a **la cota superior F**, no
a la distancia de variación total real. No prueba que falle la mezcla,
no controla una órbita excepcional individual y no demuestra Collatz
ni el reloj A/B. La prueba combinatoria completa es escrita; el alcance
de Lean y de los contrastes se declara al final.

## 1. Mapa, ley y cuentas

T actúa en los enteros no negativos: n/2 si n es par y (3n+1)/2 si
es impar. Una palabra tiene K bits, S_j unos en sus primeros j bits
y producto `P_j=3^S_j/2^j`. Sobrevive si P_j>=1 para todo j<=K.
N_K cuenta esas palabras, N_0=1. La ley es uniforme entre ellas;
por la biyección de paridades, corresponde a semillas uniformes en
`[0,2^K)` condicionadas a supervivencia. No es una ley temporal de
una semilla fija. El cero no sobrevive para K>=1.

Escribir `s=s_K=min{j:3^j>=2^K}` y `rho=log(2)/log(3)`, de modo
que s=ceil(rho K). Los tiempos se miden en pasos T.
A(K,L) cuenta los prefijos supervivientes de largo K-L con al menos
s unos. Cada uno admite las 2^L continuaciones. Por tanto

```text
G(K,L)=2^L A(K,L)/N_K.
q(L,m)=2^(-L) sum_(0<=j<m,j<=L) binom(L,j),  m>=1.
F(K,L,m)=1-G(K,L)(1-q(L,m)).
```

La cota anterior era `TV<=F`. Aquí se estima G, sin cambiar su ley.

## 2. Rotaciones: una cota inferior de N_K

Toda palabra con s unos y producto final >=1 tiene una rotación que
sobrevive. Para verlo, tomar sus sumas parciales
`h_j=S_j log(3)-j log(2)` y elegir un mínimo entre j=0,...,K-1.
Rotar después de ese índice. Antes de envolver, cada nueva suma es
`h_j-h_min>=0`; después de envolver es
`h_K-h_min+h_j>=0`. Se usa h_K>=0 y h_j>=h_min.

Cada clase de rotaciones contiene a lo sumo K palabras, incluso si
la palabra es periódica. Entre las binom(K,s) palabras con exactamente
s unos hay, pues, al menos binom(K,s)/K supervivientes. En particular,

```text
N_K >= binom(K,s)/K.                                    (2)
```

No se presume independencia después de condicionar ni se reemplaza
una trayectoria dada por una de sus rotaciones. Es una cuenta de la
población finita.

## 3. Prueba uniforme de (1)

Para K=1,2 se tiene s=K y A(K,L)=0 cuando L>=1. Lo mismo ocurre
para cualquier K si s>K-L. En los otros casos poner b=K-s>0.
Como rho>1/2, s>b. El peso de una palabra de largo K-L con j unos es
`s^j b^(K-L-j)`. Para j>=s, ese peso es al menos
`s^s b^(K-L-s)`. La suma de pesos de todas las palabras es K^(K-L),
por el binomio. De aquí

```text
A(K,L) s^s b^(K-s) <= K^(K-L) b^L.                      (3)
```

El mayor término de `sum_j binom(K,j)s^j b^(K-j)=K^K` está en j=s.
Se puede comprobar sin aproximaciones: el cociente entre los términos
j+1 y j es `(K-j)s/((j+1)b)`; es >=1 para j<s y <=1 para j>=s.
Por consiguiente,

```text
K^K <= (K+1) binom(K,s) s^s b^b.                        (4)
```

Multiplicar (3) por K^L, aplicar (4) y (2), y cancelar el peso
positivo s^s b^b. Se obtiene la cota más precisa, enteramente racional,

```text
G(K,L) <= K(K+1) [2(K-s_K)/K]^L.                         (5)
```

Como 3^5<2^8, rho>5/8, luego `2(K-s_K)/K<3/4` para K>=1.
Esto prueba (1). No se deduce (1) de los datos medidos.

Una consecuencia explícita: sea h=ceil(log2(K+1)). Si 8h<=L<=K,
entonces `(3/4)^8<1/8` y `2^h>=K+1` implican

```text
G(K,L) <= 1/(K+1),       F(K,L,m) >= 1-1/(K+1).          (6)
```

Por tanto, para esas ventanas crecientes, el certificado anterior
tiende a la cota trivial 1, cualquiera que sea m>=1. (6) no afirma
que la distancia real tienda a 1. Puede ser mucho menor que F.

## 4. Ni siquiera elegir L adaptativamente elimina el piso

Sea B_(K-1) el número de padres supervivientes cuyo hijo par muere.
El hijo impar siempre sobrevive, por lo que

```text
N_K=2N_(K-1)-B_(K-1),   1<=N_K/N_(K-1)<=2,
1-G(K,1)=B_(K-1)/N_K=2N_(K-1)/N_K-1.                   (7)
```

Los conjuntos protegidos están anidados al aumentar L. Si un prefijo
tenía reserva para L pasos, incluso después de L-1 bajadas tiene
reserva para el último. Así G(K,L)<=G(K,1). Como q>=0,

```text
F(K,L,m) >= 1-G(K,1)       para todos L,m>=1.             (8)
```

Hace falta demostrar que (7) no se aproxima a cero en todos los
horizontes. Para ello basta una cuenta exponencial. De 3^17<2^27
y 3^s>=2^K se deduce s>=17K/27. Pesar cada palabra con
`5^s 3^(K-s)`. La suma de todos los pesos es 8^K y cada superviviente
tiene peso al menos `(5^17 3^10)^(K/27)`. Luego

```text
N_K^27 <= c^K,    c=8^27/(5^17 3^10).                    (9)
```

La comprobación entera `8^27 16^27 < 31^27 5^17 3^10` da
`c^(1/27)<r=31/16<2`. Contar entre los horizontes 1,...,H aquellos
con `N_K/N_(K-1)<=r`, y llamar J_H a su cantidad. El producto de los
cocientes es N_H; cada cociente es >=1 y los restantes son >r.
Por (9),

```text
J_H >= delta H,
delta = 1-log(c)/(27 log(31/16)) > 0.                   (10)
```

Numéricamente delta es aproximadamente 0,0033265; el signo positivo
procede de la desigualdad entera, no del redondeo. En cada horizonte
contado, (7)-(8) dan

```text
F(K,L,m) >= 1/31       simultáneamente para todo 1<=L<=K, m>=1. (11)
```

Así, ninguna elección L=L(K), ni siquiera dependiente del horizonte,
hace que **este certificado** tienda a cero a lo largo de todos los K.
Se puede tomar m variable. No se excluye una subsucesión especial, un
acoplamiento distinto o una estimación de TV más fina que esta partición.

## 5. Implicación para la ruta

La tarea de Umbral «buscar una estimación demostrada de G» recibe una
respuesta: hay una cota superior universal y un obstáculo cuantificado
para convertir `TV<=Gq+(1-G)` en una prueba de mezcla asintótica.
No basta mejorar q o escoger bloques más largos dentro de este argumento.

La población condicionada a sobrevivir hasta K y una órbita fugitiva
fija son objetos diferentes. Umbral ya probaba que un fugitivo tendría
reserva para todo L fijo en densidad temporal 1. Eso no contradice
(7)-(11), que muestrean representantes distintos en cada horizonte.
Esta diferencia precisa una obligación de transferencia; no la cumple.

La continuación [Sesgo de frontera](SESGO_FRONTERA.md) resuelve después
la cuestión de la TV real mediante una inyección adicional: la ley bajo
H_K no converge a ninguna ley fija, ya módulo 3. Ese resultado no se
deduce del piso de F. Siguen abiertos la transferencia a órbitas
excepcionales, el reloj uniforme A/B, MuroB y la ausencia general
de circuitos. La tentativa determinista de esta sesión no produjo una
restricción aritmética nueva: separar fronteras por contextos coincidentes
recupera la ley de repetición y el cilindro que ya estaban documentados.

## 6. Comprobación y formalización

[Cotejo exacto](cotejar_protegidos.py), [resultado](cotejo_protegidos.json):
12 880 cotas G con K<=160; 4095 palabras y 4095 semillas enumeradas
independientemente hasta K=11; 973 rotaciones con producto final >=1;
78 cuentas de reservas directas; siete coincidencias con la evidencia
previa, sin ejecutar su programa. Se conserva el control condicionado
de tres pasos: semillas 3 y 7, TV=1/6>1/8. No se amplía el censo A/B.

```powershell
python -B -X utf8 depuracion/perdices20261025/cotejar_protegidos.py --horizonte 160 --directo 11 --salida depuracion/perdices20261025/cotejo_protegidos.json
```

[Lean](PerdicesProtegidos.lean), [evidencia](evidencia_lean.json) y
[salida](evidencia_lean.txt): Lean 4.32.2 certifica 17 lemas, incluidos
el máximo binomial ponderado para todo K,s,j, su suma, la transferencia
algebraica de las cuentas, la identidad de frontera, los pisos del
certificado y las constantes exactas. Sólo axiomas estándar, sin sorryAx.
Se cotejan los imports directos y sus objetos con Mathlib fijado;
no se audita toda la cadena transitiva ni se recompila el laboratorio.

**Tramo formal pendiente:** la rotación y el conteo (2), la extracción
de A,N desde palabras/órbitas, el ensamblaje completo de (1), y el paso
del producto de cocientes a la densidad (10). Conservan la prueba
escrita anterior; no se atribuyen a Lean. La revisión humana sigue pendiente.

```powershell
python -B -X utf8 depuracion/perdices20261025/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --salida depuracion/perdices20261025/evidencia_lean.json
```

Las [cinco altas versionadas](alta_registro.json), incluidas las continuaciones,
integran los resultados mediante el generador del laboratorio.
La [conservación](evidencia_registro.json) coteja las 360 afirmaciones
anteriores a esta sesión sin cambios y respuestas.db intacta;
el catálogo pasa a 365. Se reutiliza el verificador de integración
anterior, sin presentarlo como una auditoría independiente.
