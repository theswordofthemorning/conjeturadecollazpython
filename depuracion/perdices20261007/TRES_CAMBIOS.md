# Perdices: tres cambios y límite de las cotas de tamaño

16-10-2026. Continúa [Altura BAB, §6](ALTURA_BAB.md#6-todo-el-dominio-de-dos-cambios-con-epsilon717).
Se conserva el nombre Perdices; no se reclama prioridad bibliográfica.

**Resultado positivo:** todo prefijo real de A/B con hasta tres cambios
satisface (P) con **epsilon=1/13 y K(n)=2*ell(n)**. El candidato
epsilon=7/17 con tres cambios sigue abierto: las cotas empleadas no
bastan para demostrarlo.

**Límite del mecanismo:** con cuatro cambios, las cotas de tamaño admiten
un testigo que viola incluso `v_fin<=v_in+2ell`, la condición epsilon=0.
Respeta también el balance firmado y los encajes superiores exactos.
**No es una órbita:** se demuestra que una congruencia módulo 9 impide
realizarlo. No refuta ningún presupuesto orbital, pero muestra que esos
controles de tamaño y balance, por sí solos, no bastan.

La prioridad después de esta nota es incorporar un control aritmético
acumulativo; no seguir reduciendo epsilon según el número de cambios.
Un epsilon que tendiese a cero con ese número no cumpliría (P) global.

## 1. Dominio y herramienta conservada

`T(x)=x/2` si x es par y `(3x+1)/2` si es impar, sobre naturales positivos.
A=1 y B=110 son bloques de paridades reales desde una misma semilla n.
Las cuatro rachas tienen multiplicidades a,b,c,d>=1; no son pasos de T.
L sí cuenta pasos de T. No se asigna distribución probabilística.

`ell=ceil(log2(n+5))`. Se toman v_in y v_fin con las constantes 1 para
A y 5 para B. La identidad firmada `L=v_in+Eeta-v_fin` hace equivalentes

```text
Eeta <= (12/13)*L+2ell,
L+13*v_fin <= 13*v_in+26ell.                         (P13)
```

Se usa el encaje universal y la cota entera de
[Dos cambios, §2](DOS_CAMBIOS.md#2-una-cota-de-tamaño-con-coeficientes-enteros):

```text
2^D*(x+c) <= 3^S*(n+5),  1<=c<=5,
2^v<=x+c  ==>  17*(D+v)<=27*S+17ell.                (1)
```

Aquí D,S son el tiempo y el conteo impar del prefijo hasta x. El factor
27/17 procede de `3^17<2^27`; todas las desigualdades de abajo son exactas.

## 2. A^a B^b A^c B^d

Las fronteras antes de cada cambio son y,z,t. La entrada y de B tiene
`v2(y+1)=2`, por lo que `v_in=a+2<=ell`. La racha A^c acaba en otra
entrada B, luego `v2(z+1)=c+2>=3`. Así `v2(z+5)=2` y la racha B^b
comienza con `v2(y+5)=3b+2`. El último B^d consume 3d unidades.

Aplicar (1) a las tres fronteras produce todas estas cotas:

```text
v_in=a+2,              a+2<=ell,
51b+34 <= 17ell+10a,
17c+34 <= 17ell+10a+3b,
17(3d+v_fin) <= 17ell+10a+3b+10c.                  (2)
L=a+3b+c+3d.
```

No se ha reemplazado n por una frontera intermedia. Las constantes 34
proceden de las dos unidades que permanecen al final de las rachas
interiores, y no deben omitirse al interpretar las valuaciones.

Para exhibir la prueba lineal sin depender de un verificador, definir
los cuatro residuos no negativos

```text
E=ell-a-2,
B0=17ell+10a-51b-34,
C0=17ell+10a+3b-17c-34,
V0=17ell+10a+3b+10c-51d-17v_fin.
```

Con `G=13v_in+26ell-L-13v_fin`, sustitución directa da

```text
4913G = 3757V0+2499C0+657B0+10174E
        +43ell+176868d+255390.                      (3)
```

Todos los sumandos son no negativos. Por tanto G>=0 y vale (P13).
Los residuos se interpretan como enteros con signo en (3); sus cotas
garantizan que aquí son no negativos.

## 3. B^a A^b B^c A^d

Como A^b termina en una entrada B, la frontera después de la primera B^a
tiene valuaciones b+2 para x+1 y 2 para x+5. Así `v_in=3a+2`.
La racha B^c consume 3c unidades, pero su salida no tiene por qué dejar
exactamente dos: el último bloque es A y ya no exige otro B posterior.
Por eso la segunda desigualdad de abajo no tiene el sumando 34.

```text
v_in=3a+2,
17b+34 <= 17ell+3a,
51c <= 17ell+3a+10b,
17(d+v_fin) <= 17ell+3a+10b+3c.                     (4)
L=3a+b+3c+d.
```

Estas cotas vuelven a ser aplicaciones de (1) y del consumo por racha,
incluidos los cambios de recarga negativa. Definir

```text
B0=17ell+3a-17b-34,
C0=17ell+3a+10b-51c,
V0=17ell+3a+10b+3c-17d-17v_fin.
```

Con el mismo significado de G:

```text
4913G = 3757V0+510C0+2799B0
        +155670a+7616ell+58956d+222904.              (5)
```

Se obtiene G>=0. Las palabras con hasta dos cambios ya satisfacen el
presupuesto con epsilon=7/17>1/13 y el mismo K, luego también (P13).
Así queda probado todo el dominio de hasta tres cambios.

## 4. Por qué no se afirma el candidato 7/17 con tres cambios

El testigo abstracto

```text
orientación ABAB, (a,b,c,d)=(997,527,1670,1),
ell=1000, v_in=999, v_fin=2600
```

satisface (2), pero no `7L+17v_fin<=17v_in+34ell`. Por tanto (2) no
implica ese presupuesto. Sí satisface (P13). No se atribuye una semilla
a este testigo ni se afirma que realice las paridades: es una refutación
de una implicación entre las cotas, no un contraejemplo orbital.

## 5. Barrera explícita con cuatro cambios

Para una palabra real `B^a A^b B^c A^d B^e`, los mismos argumentos dan

```text
v_in=3a+2<=ell,
17b+34 <= 17ell+3a,
51c+34 <= 17ell+3a+10b,
17d+34 <= 17ell+3a+10b+3c,
17(3e+v_fin) <= 17ell+3a+10b+3c+10d.                (6)
```

Ahora la segunda A también acaba en B, de modo que se restablece el
sumando 34 en la cota de la B interior. El siguiente testigo cumple (6):

```text
(a,b,c,d,e)=(1,998,527,1670,1),
ell=1000, v_in=5, v_fin=2600, L=4255.
```

También admite esta contabilidad por rachas:

| Racha | Valuación al entrar | Consumo | Valuación al salir |
|---|---:|---:|---:|
| B | 5 | 3 | 2 |
| A^998 | 1000 | 998 | 2 |
| B^527 | 1583 | 1581 | 2 |
| A^1670 | 1672 | 1670 | 2 |
| B | 2603 | 3 | 2600 |

Las recargas son 998,1581,1670,2601, suman 6850 y satisfacen
`4255+2600=5+6850`. Sin embargo `2600>5+2*1000`, con exceso 595.
Así falla incluso epsilon=0 para ese modelo de cotas.

No es sólo un efecto de redondear log2(3) por 27/17: también se verifican
las cuatro desigualdades superiores exactas

```text
2^(3+1000)    <= 3^2    *2^1000,
2^(1001+1583) <= 3^1000 *2^1000,
2^(2582+1672) <= 3^2054 *2^1000,
2^(4252+2603) <= 3^3724 *2^1000.                    (7)
```

Son encajes con `n+5<=2^ell`; no se afirma que exista un único n y
fronteras enteras que realicen simultáneamente las identidades afines.
No se han impuesto todas las condiciones orbitales del laboratorio,
ni se concluye que toda posible prueba basada en tamaño esté descartada.

## 6. Una congruencia impide realizar ese testigo

Si existiera tal semilla, `v_in=5` daría `n+5=32q`, con q positivo impar,
y ell=1000 exigiría `q<=2^995`. La primera B llevaría a
`y+1=4(9q-1)`. Como la A siguiente tiene longitud 998 y termina en B,
se exige `v2(y+1)=1000`, luego

```text
9q = 2^998*r+1,       r positivo impar.              (8)
```

Las cotas de q fuerzan r=1: si r>=2, el miembro derecho supera
`16*2^995`, mientras que `9q<=9*2^995`. Pero
`2^998=4 mod 9`, de modo que `2^998+1` no es divisible por 9.
Contradicción. Por tanto el modelo de §5 **no es realizable**.

Esto muestra el dato que perdía la relajación: no basta con asignar
valuaciones compatibles con el tamaño, hay que cumplir la congruencia
de la parte impar compartida. Eliminar este testigo no prueba la
inexistencia de otros ni el presupuesto global; es una separación
concreta entre la contabilidad relajada y la aritmética real.

## 7. Certificación y siguiente obligación

[PerdicesTresCambios.lean](PerdicesTresCambios.lean) certifica los cierres
lineales de (2),(4), el paso desde epsilon=7/17, ambos testigos abstractos,
el balance y (7). La incompatibilidad aritmética de §6 y la obtención
orbital de (2),(4),(6),(8) conservan la prueba escrita de esta nota.
No se declara una formalización orbital completa.

[cotejar_tres_cambios.py](cotejar_tres_cambios.py) verifica las dos
identidades lineales (3),(5) por sus coeficientes y contrasta las cotas
con iteración literal de T. El modelo sin semilla se guarda por separado
y no se cuenta como un caso orbital. No se amplía el censo de semillas.

[Evidencia Lean](evidencia_tres_cambios.json) y [salida](evidencia_tres_cambios.txt):
ocho consultas con Lean 4.32.2, sólo axiomas estándar y sin `sorryAx`.
El [cotejo](cotejo_tres_cambios.json) cubre 5196 casos construidos y 63
prefijos de las 34 semillas históricas: 5259 controles orbitales, sin
fallos observados de los dos presupuestos. No demuestra epsilon=7/17
con tres cambios; la prueba universal escrita y el cierre Lean son para 1/13.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_tres_cambios.py --racha-max 6 --traslados 2 --historicos depuracion/perdices20261007/medicion_salida_ab.json --salida depuracion/perdices20261007/cotejo_tres_cambios.json
python -B -X utf8 depuracion/perdices20261007/comprobar_tres_cambios.py --salida depuracion/perdices20261007/evidencia_tres_cambios.json
```

Siguiente obligación: controlar varias congruencias de partes impares
compartidas desde n, con un coste que se acumule sin reiniciar K.
La prueba debe excluir una familia completa de excesos, no sólo el
testigo de §5. El presupuesto universal, la salida del piloto y Collatz
siguen abiertos. Revisión humana pendiente.

Tanda cerrada por petición del usuario; investigación detenida a la espera
de la información que anuncia. El usuario autoriza después commit y push
de esta tanda, manteniendo la pausa.
