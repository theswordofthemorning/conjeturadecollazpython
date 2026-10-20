# Perdices: todas las ventanas desde una misma semilla

19-10-2026. Continúa [Denominador global](DENOMINADOR_GLOBAL.md).
Objetivo: el reloj uniforme `L<=C*ell(n)+D`, no una nueva ampliación del
censo. Se conserva Perdices, sin reivindicar prioridad.

**Balance:** se determina el óptimo exacto de una relajación que conserva
la misma semilla y todas las fronteras afines. Incluso imponer a la vez
todas las barreras de tamaño de las ventanas deja pasar falsos recorridos
racionales. El ejemplo de §3 persiste al añadir ventanas interiores en
pasos T. No se ha demostrado el reloj ni la imposibilidad de conseguirlo
con otras herramientas. El testigo finito tampoco excluye todo C,D en
esta relajación.

## 1. Dominio y una desigualdad exacta por ventana

T actúa sobre enteros positivos: n/2 si n es par y (3n+1)/2 si es impar.
A=1 y B=110 son bloques de paridades; L cuenta pasos T y
`ell(n)=ceil(log2(n+5))`. Índices i,j cuentan bloques, desde cero.
No hay ley aleatoria ni condicionamiento probabilístico.

Sea W una palabra y [i,j) una ventana no vacía. El prefijo U=W[0,i)
tiene datos `M=2^P, D=3^S, E`, con

```text
M*x_i = D*n+E.
```

Para V=W[i,j), escribir `N=2^l, d=3^s, e`, y
`g=gcd(d-N,e), q=(d-N)/g, r=e/g`. Todos los bloques expanden, luego
q>0. Realizar la ventana exige `N | q*x_i+r`; por positividad implica
`N<=q*x_i+r`. Usando el prefijo **con su término E exacto**:

```text
a_(i,j) = q*D > 0,
c_(i,j) = M*(N-r)-q*E,
N <= q*x_i+r  <->  a_(i,j)*n >= c_(i,j).             (1)
```

No se usa aquí el encaje superior `x_i+5<=(D/M)(n+5)`: se mantiene
la igualdad afín. Tampoco se elige una semilla independiente por ventana.

La misma fórmula vale para ventanas entre pasos T interiores siempre
que `d>N`. En ellas no se necesita afirmar `q<=r<=5q`.
Las ventanas contractivas no forman parte de esta ampliación.

## 2. Óptimo simultáneo: no falta sumar mejor estas cotas

Relajar únicamente la integridad/paridad de las fronteras y la
divisibilidad a su desigualdad de tamaño. Mantener la composición afín
racional de **todo** W y exigir (1) para todas las ventanas. Entonces

```text
H(W) = max(1, max_(i<j) c_(i,j)/a_(i,j)),
n_rel(W) = ceil(H(W)).                                (2)
```

Es el menor **entero positivo** admitido por esta relajación: cada
restricción es una semirrecta `n>=c/a`; su intersección es `n>=H`.
Todos sus puntos producen las mismas fronteras racionales prescritas.
La palabra vacía tiene H=1. Al añadir ventanas expansivas T interiores
sólo se amplía el conjunto sobre el que se toma el máximo.

Por tanto ninguna combinación lógica válida de **estas mismas**
desigualdades puede excluir n_rel: ya las satisface conjuntamente.
Esto no se extiende a nuevas desigualdades aritméticas ni a conservar
los residuos o la integridad. Es el óptimo del modelo, no del problema.

## 3. Testigo conservado: el obstáculo sobrevive a los solapamientos

La palabra histórica

```text
W = AABAAABBAAAAAABAAAAABABAAABAAABBB
```

tiene 33 bloques y L=53. Su menor semilla real es **6416623**,
con ell=23. Dos constructores de cilindros y T literal lo contrastan.

| Condiciones de tamaño | Cantidad | H exacto | Menor entero admitido |
| --- | ---: | ---: | ---: |
| Todas las ventanas de bloques | 561 | 4247/729 | 6 |
| Todas las ventanas T expansivas | 1391 | 3964757/177147 | 23 |

En el primer caso la ventana activa es [6,8), BB. También pasa n=7,
que realiza los dos primeros A: `7 -> 11 -> 17`. Pero el B prescrito
después daría `79/4`: `8` no divide `17+5=22`.

El segundo caso sigue admitiendo una semilla impar, n=23, con
`23 -> 35 -> 53`; el B siguiente daría `241/4`. Ahora todas las 1391
barreras pasan y `ell(23)=5`, pero `53>3*5`. No es una órbita de T
después de esos dos A, ni un contraejemplo al reloj.

Se trata de un certificado finito del límite de esta combinación.
**No** se deduce que permita L ilimitado con n fijo ni que descarte
cualesquiera constantes C,D. Su utilidad es mostrar que no basta
optimizar la suma o ponderación de las cotas ya presentes para obtener
`L<=3*ell`, sin término aditivo: faltan restricciones que excluyan este recorrido.

En los 34 testigos históricos, las ventanas de bloques certifican
`L<=3*ell(n_rel)` en ocho. No se presenta esa proporción como una ley
estadística ni como frecuencia entre todas las palabras.

## 4. Control positivo: el sufijo recupera A B^b

Para b>=1, tras el A inicial se tiene `2*x=3*n+1`. El sufijo B^b exige
`8^b | x+5`, luego

```text
2*8^b <= 3*n+11 < 3*(n+5),
L=3b+1 <= ell(n)+1.                                  (3)
```

La última implicación usa `n+5<=2^ell`: si L>=ell+2, el lado izquierdo
sería al menos `4*2^ell`, imposible. Incluye b=0 mediante A y ell>=1.
Es un corolario del mecanismo de repetición existente, no un reloj nuevo
para cambios arbitrarios.

Para las ventanas de bloques de esta familia, el óptimo (2) es exactamente
`H=(2*8^b-11)/3`. La desigualdad del sufijo da la cota inferior. Para ver
que se alcanza como semilla racional, tomar ese n: tras A resulta
`x=8^b-5`, que realiza realmente B^b. Las ventanas interiores al sufijo
cumplen sus barreras. Las que contienen A son A B^j y tienen g=1 por
[el ensayo anterior](DENOMINADOR_GLOBAL.md#2-una-sola-letra-destruye-esta-cancelación).
En ellas `q*n+r=N*(y-n)` y `y-n>=1`: ya el A incrementa n en
`(n+1)/2>=1`, y cada B lo incrementa. Todas las barreras pasan.

La congruencia exacta es `2*8^b | 3*n+11`. Sus mínimos positivos son

```text
n_min = (2*8^b-11)/3   si b>=2 es par,
n_min = (4*8^b-11)/3   si b>=1 es impar.
```

Se elige el menor múltiplo positivo que hace entero el cociente.
Para b par ell=3b y L=ell+1; para b impar ell=3b+1 y L=ell.
Así (3) es ajustada en infinitos miembros. Este control explica cómo
el sufijo ayuda donde el denominador de toda la palabra fallaba.

## 5. Lo que hay que conservar: frontera entera y CRT

Para un entero x, la frontera A es entera si y sólo si `2 | x+1`;
la frontera B lo es si y sólo si `8 | x+5`, o x=3 mod 8. Son precisamente
las condiciones orbitales de esos bloques. Con n positivo y todas las
fronteras enteras, la composición prescrita vuelve a ser un camino real.
Esta equivalencia general se obtiene por inducción en los bloques.

En un corte W=UV, los datos del prefijo son M,D,E y los del sufijo N,d,e.
Una frontera **entera** x compatible con pasado y futuro satisface

```text
x = E*M^(-1) mod D,      x = -e*d^(-1) mod N.          (4)
```

El primer módulo es una potencia de 3 y el segundo de 2, por lo que CRT
fija una clase x0 módulo D*N. Elegir su primer miembro con
`M*x>=E+D` y poner `n=(M*x-E)/D` recupera exactamente el menor n
positivo de W. Al incrementar x en D*N, n crece en M*N=2^L.
Los extremos U o V vacíos se interpretan módulo 1.

En el corte AA del testigo, el pasado exige `x=8 mod 9`; la clase del
futuro tiene menor representante 14437403 módulo 2^51. Compatibilizarlas
recupera n=6416623. Se contrasta (4) en **cada corte** de las palabras
del cotejo, contra los dos constructores globales independientes.

Esto explica dónde se pierde la información al pasar a (1). **CRT es
una reconstrucción exacta, no una nueva cota**: combinar más cortes
exactos no añade restricciones independientes al cilindro completo.
Para el objetivo inmediato falta una estimación uniforme de esos
representantes compatibles, sin enumerar las palabras y sin un factor
que dependa de sus cambios. No se ha encontrado aquí esa estimación.
Volver a optimizar sólo las barreras de tamaño no resolverá el testigo
anterior; el siguiente argumento debe usar la integridad de (4).

## 6. Evidencia y alcance formal

[Lean](PerdicesVentanasSimultaneas.lean) certifica ocho lemas: (1), su
conjunción para cualquier familia de ventanas, el máximo exacto,
las dos condiciones de integridad, el residuo B y las dos desigualdades
condicionales que dan (3). Lean 4.32.2, Mathlib fijado, sólo axiomas
estándar: [evidencia](evidencia_simultaneas.json) y [salida](evidencia_simultaneas.txt).
No formaliza aquí la extracción orbital general, el testigo de 53 pasos,
el óptimo de toda la familia ni la reconstrucción CRT: conservan la
prueba escrita y el contraste independiente. Revisión humana pendiente.

[Cotejo exacto](cotejar_simultaneas.py), [resultado](cotejo_simultaneas.json):
1023 palabras de hasta nueve bloques, incluida la vacía; 33 miembros
A B^b, b=0..32; los 34 testigos guardados. Se comprueban 70417 ventanas
de bloques, 10954 cortes CRT y 67224 ventanas T expansivas de los
testigos. Cada óptimo acepta su techo entero y rechaza el entero anterior
positivo. Se usan Fraction, dos composiciones afines, dos constructores
de cilindros y T literal. No se repite el censo grande.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_simultaneas.py --bloques-max 9 --familia-max 32 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_simultaneas.json
```

El [reproductor Lean](comprobar_denominador.py) recibe `--modulo
PerdicesVentanasSimultaneas`, `--lean` con el ejecutable 4.32.2 y
`--salida` con el JSON. Comprueba imports directos y axiomas; no audita
toda la cadena transitiva de Mathlib. El módulo anterior se recompila
también tras ampliar su reproductor, manteniendo su evidencia vigente.
