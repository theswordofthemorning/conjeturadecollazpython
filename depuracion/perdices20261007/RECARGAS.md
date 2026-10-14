# Perdices: presupuestos de recarga que no pueden funcionar

14-10-2026. Desarrollo del [piloto acordado](../coherencia20260913/RUTA_339_20261012.md#reanudar-la-próxima-sesión).
**Resultado:** la familia `K(n)=α ceil(log2(n+5))+β`, con `0<=α<=1` y
`β>=0` constantes, no satisface (P) para ningún epsilon positivo uniforme.
También falla cualquier presupuesto finito que sólo dependa de las dos
valuaciones iniciales `v2(n+1),v2(n+5)`. No se demuestra salida universal.

La refutación concreta de `epsilon=1/2, α=1, β=0` está formalizada en Lean.
Las dos barreras de familias tienen prueba escrita; su formalización completa
queda pendiente. Se conserva el nombre Perdices, sin asignar un animal nuevo
ni reclamar prioridad bibliográfica.

## 1. Dominio, índices y presupuesto elegido

Mapa atajo `T(x)=x/2` si x es par, `(3x+1)/2` si es impar, sobre enteros
positivos. `A=1`, `B=110`; longitudes `d_A=1`, `d_B=3`, constantes
`c_A=1`, `c_B=5`. Los pasos se cuentan en T, no en el mapa clásico.
Una palabra de bloques es admisible si realiza exactamente sus paridades
desde la misma semilla `n>=1`. No hay ley aleatoria ni condicionamiento
probabilístico; sí se exige admisibilidad orbital en cada afirmación.

Para `p_0,...,p_(s-1)`, `s>=1`, sean x_i sus fronteras, x_0=n, y

```text
L = suma d_(p_i),
eta_i = v2(x_(i+1)+c_(p_(i+1))) - v2(x_(i+1)+c_(p_i)),  0<=i<s-1,
Eeta = suma eta_i,
v_in = v2(n+c_(p_0)),   v_fin = v2(x_s+c_(p_(s-1))).
```

`v2(z)` sólo se aplica a z>0. Las diferencias y Eeta son **firmadas**.
Las ecuaciones `2(y+1)=3(x+1)` y `8(y+5)=9(x+5)` consumen respectivamente
una y tres unidades. Por telescopado:

```text
L = v_in + Eeta - v_fin.                               (R)
```

La familia fijada antes del contraste es

```text
ell(n) = ceil(log2(n+5)),
K_(alpha,beta)(n) = alpha*ell(n)+beta,   alpha,beta>=0.
```

Los parámetros son constantes independientes de n y de la palabra. La
plantilla pide que **existan** epsilon>0, alpha y beta tales que, para
**todo** n>=1 y **toda** concatenación real no vacía desde n,

```text
Eeta <= (1-epsilon)L + K_(alpha,beta)(n).                (P)
```

K se calcula exclusivamente desde n; no usa salida ni convergencia.
El primer candidato contrastado es `(epsilon,alpha,beta)=(1/2,1,0)`.
Por (R), (P) equivale a

```text
epsilon*L + v_fin <= v_in + K_(alpha,beta)(n).           (P')
```

Esta equivalencia expone el coste de la divisibilidad terminal todavía sin
consumir. No se puede descartarla para probar (P). Lean certifica el paso
algebraico sobre racionales, condicionado a (R); la derivación orbital
general de (R) permanece escrita.

## 2. Recargas de ambos cambios, incluidas las cancelaciones

Aquí x es la entrada del bloque anterior y y su salida.

**A a B.** Escribir `x+1=2^a q`, q impar. Como `y+1=3*2^(a-1)q`,
que y sea entrada de B equivale a a=3. Entonces

```text
y+1=12q,  y+5=4(3q+1),  eta_AB=v2(3q+1)>=1.            (1)
```

El sumando 1 puede producir una cancelación arbitrariamente larga.
No existe cota constante para esta recarga.

**B a A.** Escribir `x+5=2^b q`, q impar, b>=3. Entonces

```text
y+5=9*2^(b-3)q,  y+1=9*2^(b-3)q-4.
```

Para b=3, y es par y A no es admisible. En los demás casos:

| b | eta_BA | Causa |
|---|---:|---|
| 4 | 0 | Ambos potenciales tienen valuación 1. |
| 5 | `v2(9q-1)>=1` | Cancelación en `y+1=4(9q-1)`. |
| >5 | `5-b<0` | `v2(y+1)=2`, pero `v2(y+5)=b-3`. |

Repetir el mismo bloque da eta=0. Por tanto ni todos los cambios son
positivos ni se pueden omitir los negativos. Estas fórmulas se cotejan
directamente con T y con divisiones enteras independientes.

## 3. Un contraejemplo pequeño, ya entre los testigos conservados

Desde n=4591, la palabra de bloques

```text
A A B A B A A A B A A B A A B
```

tiene L=25 y las fronteras

```text
4591, 6887, 10331, 11623, 17435, 19615, 29423, 44135,
66203, 74479, 111719, 167579, 188527, 282791, 424187, 477211.
```

Las catorce recargas son

```text
0, 3, 1, 3, 3, 0, 0, 3, 2, 0, 3, 2, 0, 6;
Eeta=26, v_in=4, v_fin=5, 25=4+26-5.
```

Como `2^12 < 4591+5 <= 2^13`, ell(4591)=13. (P) exigiría
`26 <= 25/2+13 = 51/2`, falso. No es un nuevo récord ni el resultado
de ampliar el censo: 4591 ya figura en [la medición AB](medicion_salida_ab.json).

[PerdicesRecargas.lean](PerdicesRecargas.lean) comprueba las paridades de T,
las valuaciones mediante divisibilidad exacta y su enlace con `padicValNat`.
`plantilla_refutada` niega el cuantificador universal de esta plantilla.
No usa `native_decide`; sus certificados finitos pasan por el kernel.

## 4. No basta con las valuaciones iniciales

Para todo entero t>=1, tomar

```text
n_t=(2^(2t+3)-11)/3 > 0.
```

Es entero porque `2^(2t+3)=2 mod 3`. Se tiene

```text
v2(n_t+1)=3,   v2(n_t+5)=2,
A(n_t)=2^(2t+2)-5,
B(A(n_t))=9*2^(2t-1)-5.
```

AB es real, L=4, v_fin=2t-1 y Eeta=2t. Por tanto, para cualquier función
finita `F:N^2 -> R_>=0`, (P) con `K(n)=F(v2(n+1),v2(n+5))` exigiría

```text
2t <= 4(1-epsilon)+F(3,2)   para todo t>=1,
```

imposible. La semilla cambia con t; no se construye una órbita infinita.
El argumento también muestra por crecimiento que alpha<1 no puede bastar
en la familia logarítmica. El caso alpha=1 requiere otro argumento.

## 5. Ninguna constante repara K(n)=ell(n)

### Construcción con una semilla conservada durante todo el prefijo

Fijar r>=1 y la palabra `(AB)^r`, de longitud 4r. Como

```text
AB(x)=(27x+19)/16,
N=16^r, D=27^r, E=19(D-N)/11,
N*x_final=D*n+E,
```

E es entero. La misma fórmula se obtiene independientemente del potencial
`16(11*AB(x)+19)=27(11x+19)`.

Poner `M=3^(3r-2)=D/9` y `H=(E+5N)/9`. H es entero y `H=2 mod 3`:
`11(E+5N)=19D+36N` da la divisibilidad por 9; después
`11H=19M+4N=1 mod 3`.

El hecho elemental de que 2 genera las unidades módulo `3^k` permite
elegir exponentes m arbitrariamente grandes tales que

```text
2^(m+4r)=H mod M.                                      (2)
```

Este ingrediente ya está probado en
[`AlpacasGarner.dos_genera_grande`](../gao20260920/formal/Alpacas.lean).
También se obtiene por inducción: los tres levantamientos de un exponente
modulo `2*3^(k-1)` recorren las tres unidades que levantan el residuo
anterior, pues `v3(4^(3^(k-1))-1)=k`. No es una hipótesis nueva.

Definir, sin usar ningún tiempo de salida,

```text
n=(2^(m+4r)-H)/M.
```

(2) garantiza que n es entero. Para m suficientemente grande es positivo,
y la ecuación compuesta da `x_final=9*2^m-5`.
La divisibilidad `2^(4r) | 27^r*n+E` basta para que el prefijo sea real:
reduciendo módulo 2 se obtiene el primer bit, se realiza ese paso de T y
se repite con la palabra restante. Es la biyección entre residuos y
palabras de paridades, no una elección independiente de bloques entre saltos.

El primer AB impone `n=7 mod 16`, luego v_in=3; el potencial final
`x_final+5=9*2^m` tiene valuación m. Así, por (R),

```text
L=4r,  Eeta=4r+m-3,
n+5=9(16/27)^r * 2^m + (36/11)(1-(16/27)^r).          (3)
```

### Refutación uniforme con desigualdades exactas

Sea beta>=0 una constante real cualquiera. Elegir un entero b>=beta y
`r=2b+18`. Puesto que `(16/27)^2<1/2`,

```text
9(16/27)^r < 9/2^(b+9) < 1/2^(b+5).
```

Elegir en (2) un `m>=max(r+2,b+7)`. Esto garantiza n>0: en la fórmula
de n el término principal es mayor que `9*2^(m-r)>=36` y se resta
menos de 5. El término constante de (3) está entre 0 y 4; por tanto

```text
n+5 < 2^(m-b-5)+4 <= 2^(m-b-4),
ell(n)+beta <= ell(n)+b <= m-4.
```

Pero `Eeta-L=m-3`. Incluso para epsilon=0, (P) requeriría
`m-3 <= ell(n)+beta <= m-4`, una contradicción. Para epsilon>0 el
lado derecho de (P) sólo disminuye. Para `0<=alpha<=1`,
`K_(alpha,beta)(n)<=ell(n)+beta`, de modo que también falla.

**Cuantificadores:** para cada par de constantes alpha<=1 y beta>=0
hay una semilla positiva y un prefijo finito real que viola (P), a la
vez para todos los epsilon>=0. La semilla depende de los parámetros.
El prefijo repite un único bloque compuesto expansivo, que tiene por sí
mismo un presupuesto finito de repetición. Esta barrera no exhibe
persistencia ni contradice la conjetura de longitud de Salidas.

## 6. Evidencia y obligación pendiente

[Cotejo independiente](cotejo_recargas.json): 34 testigos históricos y
bordes, 40 semillas en total, 1847 prefijos hasta 116 pasos, sin barrido
de un intervalo nuevo. Incluye r=1, suma vacía, repetición sin recarga y
los tres signos de B a A. Hay 49 prefijos que refutan el candidato inicial;
no se afirma que 4591 sea la menor semilla entre todos los naturales.

También se comprueban 12 miembros de la familia de un cambio, tres
miembros completos de `(AB)^r` y nueve certificados simbólicos de (2)–(3)
para b=0,...,8. En estos últimos no se construye el entero `2^m`, que
puede ser enorme: se verifican las congruencias por exponenciación modular
y las cotas de los coeficientes con enteros y `Fraction`. Son controles
finitos de la derivación universal, no su sustituto.

[Evidencia Lean](evidencia_recargas.json) y [salida](evidencia_recargas.txt):
Lean 4.32.2, diez consultas de axiomas, sólo `propext`, `Classical.choice`
y `Quot.sound`; algunas no requieren axiomas. Se compila el módulo nuevo
desde fuente y se cotejan sus imports directos con Mathlib fijado. No se
reconstruye ni audita transitivamente toda Mathlib. La formalización
universal de las secciones 2, 4 y 5 sigue pendiente; revisión humana pendiente.

El registro se regenera con dos altas (340–341), conservando literalmente
las 339 filas anteriores. Su auditoría y la del mapa pasan: 341 afirmaciones,
123 piezas y 224 enlaces locales. Los HTML se regeneran; la comprobación
de navegador no se pudo ejecutar porque este Python no tiene Playwright.
Esto no afecta al certificado Lean ni al contraste aritmético.

Reproducción, desde la raíz:

```text
python -B -X utf8 depuracion/perdices20261007/cotejar_recargas.py --pasos 116 --familia-materializada 3 --beta-max 8 --salida depuracion/perdices20261007/cotejo_recargas.json
python -B -X utf8 depuracion/perdices20261007/comprobar_recargas.py --salida depuracion/perdices20261007/evidencia_recargas.json
```

El entregable acordado termina con una refutación, no con salida del piloto.
La familia alpha>1 no queda decidida por estas construcciones. Una siguiente
obligación concreta es estudiar `(epsilon,alpha,beta)=(1/2,2,0)`, es decir,

```text
L+2*v_fin <= 2*v_in+4*ell(n)
```

para todos los prefijos reales desde n. Es una plantilla abierta, no una
afirmación registrada como verdadera. Duplicar el coeficiente conserva el
mismo mecanismo; por sí solo no aporta una razón para que funcione. Hace
falta una nueva cota acumulada o un contraejemplo exacto, no más horizonte
de censo. La salida universal de A/B y la extensión a descenso eventual
para Collatz continúan abiertas.

Continuación del 14-10: [Perfiles](PERFILES.md) descarta una vía local de
prueba basada en tamaño creciente más un catálogo fijo de valuaciones.
No refuta (P) con alpha=2 ni cambia las barreras demostradas aquí.
