# Clases residuales y bits del ancla

20-09-2026. Desarrollo escrito universal del transporte de medida usado
en el candidato. Los certificados `cilindros.lean` cubren el refinamiento
afín y la paridad; no contienen toda la inducción de estados y medidas.

## Invariante inductivo

Para cada palabra viva w de longitud t hay exactamente una clase
`n=r_w+2^t*m`, `0<=r_w<2^t`, sobre la cual las dos trayectorias tienen
en tiempo t las expresiones, con orientación que depende sólo de w,

    ancla = 3^p*m+a,     otro = 3^q*m+b,      p<=q,

donde a,b son enteros y p,q son los conteos de entradas impares de
las dos trayectorias orientadas. No se ordenan por valor si p<q.
Si p=q y a!=b, orientar de modo que b>a. El estado es

    k=q-p,   c=b-3^k*a.

Para k=0 se tiene c=b-a>0. La pareja representada es
`{v,3^k*v+c}` para todos los m de la clase, no sólo para un representante.
En el caso p=q y a=b se declara absorción y se deja de normalizar.

En t=0 hay una sola clase: r=0, ancla=m, otro=m+1, estado `(0,1)`.
Se pueden considerar todos los m enteros en las identidades algebraicas;
las densidades posteriores usan sólo n positivos suficientemente grandes.

## Un bit determina exactamente un refinamiento

La paridad del ancla es `m+a mod 2`, pues `3^p` es impar. Para cada
bit e existe un único d en {0,1} con `d+a=e mod 2`. Escribir

    m=2*l+d,      r_(we)=r_w+2^t*d.

Así el nuevo residuo está en `[0,2^(t+1))`. Las dos elecciones e
dan exactamente las dos clases hijas, en orden posiblemente invertido.
No hay descarte, ponderación adicional ni hipótesis de distribución
de c. Cada extensión tiene peso 1/2 bajo la medida uniforme residual.

Una expresión `3^p*m+a` se vuelve `2*3^p*l+(3^p*d+a)`.
Si el último paréntesis es 2h, aplicar T da `3^p*l+h`.
Si es 2h+1, aplicar T da `3^(p+1)*l+3h+2`.
En particular, la pendiente vuelve a ser una potencia de 3 impar,
y su exponente registra exactamente el nuevo conteo impar.
Lo mismo ocurre en la otra trayectoria.

## Normalización después del paso

Si k>=1, la paridad del otro miembro es la del ancla más c, módulo 2.
Para c par, ambos exponentes cambian igual. Para c impar, bit 0
incrementa sólo el exponente del otro: k sube. Bit 1 incrementa sólo
el del ancla: k baja. Las identidades de `cadenakc.lean` dan los offsets.

Si k=1, c impar y bit 1, los exponentes resultantes son iguales y
el offset es `(c-1)/2`. Si es cero, las dos expresiones son idénticas:
absorción. Si es positivo se conserva el ancla; si es negativo se
intercambian los miembros. La orientación depende del signo de ese
entero conocido, **no** de l. El nuevo gap es `abs((c-1)/2)`.

Si k=0 y c par, los exponentes vuelven a coincidir y el gap sigue
positivo. Si c es impar y bit 0, el exponente del otro aumenta y se
conserva el ancla. Si el bit es 1, aumenta el del ancla anterior y
se intercambian los miembros: las nuevas coordenadas son
`k=1, c=(1-3g)/2`, sin tomar su valor absoluto. También este intercambio
está determinado por la palabra, y la nueva pendiente del ancla es impar.

Se preserva por inducción el invariante y la biyección entre palabras
vivas y clases vivas. Después de absorber, si se desea completar el
árbol, se siguen refinando las dos trayectorias iguales por su paridad
común: cada clase absorbida tiene dos hijos absorbidos.

## Absorción y medida

Una fusión balanceada en una clase tiene igualdad de los dos valores
y de sus conteos impares, por lo que p=q y a=b. Recíprocamente esa
igualdad de expresiones es una fusión balanceada de toda la clase.
Una coincidencia accidental con p!=q para algún m aislado no cuenta
como fusión balanceada y no es absorción de este árbol.

La medida de absorción hasta t es exactamente `a(t)/2^t`. En el espacio
de bits producto, la absorción eventual es la unión creciente de esos
eventos; la continuidad de la medida da

    P(absorción eventual)=lim_t a(t)/2^t=phi.

La continuidad se usa para **probabilidad en un espacio fijo**. No se
intercambian aquí límites de densidades naturales. El paso a densidad
uno se hace por inclusión: si phi=1, para cualquier epsilon>0 se fija
t con `a(t)/2^t>1-epsilon`; la unión periódica de esas clases ya da esa
cota inferior de densidad para todas las fusiones posteriores.

## Fusión clásica dentro del horizonte de Gao

Para una clase absorbida antes de t, extender la igualdad hasta t.
Sean s<=t las entradas impares comunes. Sustituir cada paso impar de
T por los dos pasos correspondientes de C implica
`C^(t+s)(n)=C^(t+s)(n+1)`. Para `n>=2^(2t)` se cumple
`t+s<=2t<=log2(n)`. Sólo se eliminan finitos elementos de la unión
periódica fija. Por tanto la densidad inferior del conjunto de fusión
clásica dentro de log2(n) es al menos `a(t)/2^t` para cada t.
Si phi=1, ese conjunto tiene densidad natural uno.

No se usa terminación en 1. Esta distinción permite estudiar la
formulación de fusión atribuida a Gao sin afirmar que Collatz esté resuelta.
