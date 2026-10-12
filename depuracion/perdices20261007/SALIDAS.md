# Perdices: salidas finitas y el retorno que evita 5 y 7

11-10-2026. Continúa [Complejidad](COMPLEJIDAD.md). Se conservan los tres
censos locales y sus fuentes exactas; se corrigen los informes cuando el
horizonte trunca una búsqueda. La ruta nueva usa el mapa parcial H publicado
por Yolcu–Aaronson–Heule. **No se demuestra su terminación universal ni Collatz.**

**Continuación:** [Rachas H](RACHAS_H.md) comprime las rachas completas,
recupera sus etiquetas desde la salida y prueba la compatibilidad de todo
pasado y futuro finitos. Añade ocho teoremas Lean; densidades y empalmes
conservan prueba escrita.

## 1. Convenciones y resultados finitos

Atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar, sobre naturales.
Un prefijo de largo L contiene las paridades de `n,T(n),...,T^(L-1)(n)`.
`λ(n)` es el mayor largo admitido por el lenguaje indicado, o infinito si
no se sale. Los cortes B y L son parámetros: semillas `n<2^B` y a lo sumo
L paridades. No se supone aleatoriedad ni independencia.

| Lenguaje | Dominio del censo | Máximo λ | Menor semilla que lo alcanza |
|---|---|---:|---:|
| Prefijos de `{1,110}^ω` | `1<=n<2^50` | 112 | 338203040342655 |
| Evitar `00` | `3<=n<2^36` | 111 | 32679321654 |
| Evitar `00` y `111` | `3<=n<2^52` | 89 | 3696298745089794 |

Evidencias conservadas: [AB](medicion_salida_ab.json),
[sin 00](medicion_salida_sin00.json) y [sin 00 ni 111](medicion_yah_5_7.json).
Sus censos visitaron 719397383, 267833764 y 22736417 nodos, respectivamente.
Los máximos están por debajo de los horizontes 200, 400 y 400: estas tres
ejecuciones agotaron las ramas del dominio antes del corte.

Para AB, cada mínimo r de largo L satisface `r^3>=2^(L-1)`, luego
`λ(n)<=3 log2(n)+1` en todo el dominio censado. Se amplía la medición anterior
de 36 bits, cuya evidencia por niveles permanece intacta. Los nuevos récords
finales son 163439703581415 para L=102–106, 197943312098751 para L=107–109 y
338203040342655 para L=110–112. La desigualdad universal sigue conjeturada.

Para los otros dos lenguajes, se excluyen 1 y 2 porque su palabra alternante
continúa indefinidamente. Esto **no permite** ignorar sus clases residuales:
la clase de 1 módulo 2 también contiene 3. El primer mínimo en ambos casos
es 3 para L=1; los JSON históricos empezaban en L=2. Esa omisión no cambia
los máximos de la tabla.

## 2. Auditoría y correcciones de los medidores

[auditar_salidas.py](auditar_salidas.py) compara con órbitas directas,
independientes del levantamiento de residuos. Con 16 bits y corte 160:

- 420 combinaciones de lenguaje, dominio y horizonte, incluidos el dominio
  vacío, cortes 0 y 1, prohibir ambos bits y un lenguaje con supervivencia infinita;
- 25 ejecuciones de las CLI, cotejando truncamiento y el primer nivel vacío;
- contraste directo de todas las semillas del dominio menor que 65536;
- huellas de los tres generadores originales, todos sus 310 testigos y las
  82 filas del solapamiento entre la búsqueda AB por niveles y por profundidad.

[Resultado](auditoria_salidas.json). No se han repetido los censos grandes:
la comprobación independiente de exhaustividad llega a 16 bits. Para los
censos mayores se conserva la evidencia de las ejecuciones originales y se
verifican sus fuentes, los testigos y el margen hasta el horizonte.

Los originales están en [fuentes_salidas_20261011](fuentes_salidas_20261011/medir_salida_ab.py),
con las mismas huellas que los JSON. Las versiones vigentes mantienen sus
implementaciones independientes y corrigen tres puntos:

1. Un superviviente en el horizonte produce `truncado=true` y máximo global
   `null`. El informe anterior podía afirmar una salida aún no observada.
2. Para `n>=3`, cada cilindro `r mod 2^L` usa su menor miembro >=3, aunque
   r sea 0, 1 o 2. Se admite y se informa el dominio vacío.
3. La cota AB se contrasta y se informa; si aparece un contraejemplo, se
   conserva en el JSON. Una aserción de esa conjetura no debe borrar el hallazgo.

## 3. Enlace con el problema publicado

Para una semilla impar, evitar `00` equivale a no visitar un impar `5 mod 8`:
ése es exactamente el caso `v2(3n+1)>=3`. Evitar `111` equivale a no visitar
`7 mod 8`, pues las tres paridades iniciales determinan el residuo módulo 8.
Para semillas pares, la equivalencia con evitar `00` requiere tratar el
tramo inicial: por ejemplo, 4 empieza por `00` y converge sin visitar 5.

Yolcu–Aaronson–Heule, [arXiv:2105.14697v3, §4.5](https://arxiv.org/html/2105.14697v3#S4.SS5),
formulan en la conjetura 4.14 que toda órbita no convergente visita 5 o 7
módulo 8. Su proposición 4.15 la reduce a la terminación del mapa parcial
siguiente sobre enteros positivos:

```text
H(x) = 3x/4        si x = 0 mod 4       (rama D),
       (9x+1)/8    si x = 7 mod 8       (rama E),
       indefinido en otro caso.
```

La coordenada de retorno es `n=8x+1`, con x>=1. D corresponde a las paridades
`10` y E a `101`, hasta volver a `1 mod 8`. Por tanto una etapa H dura **dos
o tres pasos T**. El artículo es la fuente de esta reducción; no se reclama
como resultado nuevo ni se infiere una solución por el censo.

## 4. Inversa e historias: qué se puede probar

La rama D tiene imagen `0 mod 3`; la E tiene imagen `8 mod 9`. Son disjuntas,
y ambas son inyectivas. Así H tiene la inversa parcial

```text
H^(-1)(y) = 4y/3        si y = 0 mod 3,
           (8y-1)/9    si y = 8 mod 9,
           indefinida en otro caso.
```

Las clases `1,2,4,5,7 mod 9` no tienen predecesor. Tener fuentes y una inversa
única no impide una cadena infinita hacia delante.

**Prueba escrita de la cuenta exacta.** Una historia de k ramas, con a letras
D y b letras E, admite exactamente una clase `r mod M`, con
`M=4^a 8^b`, y satisface `M H^k(x)=A x+B`, con `A=3^a 9^b` impar.
Para extenderla por una rama de divisor d, pendiente c, término e y residuo
de entrada s, escribir `x=r+Mt`, `y=(Ar+B)/M`. La nueva condición es
`y+A t=s mod d`; como A es impar, hay exactamente un t módulo d.
Los nuevos datos son

```text
r' = r+M*((s-y)*A^(-1) mod d),
M' = M*d,     A' = c*A,     B' = c*B+e*M.
```

Las historias son disjuntas porque H es determinista. Cada clase contiene
positivos arbitrariamente grandes, incluso cuando r=0. La densidad natural
del conjunto que admite k pasos H es exactamente

```text
sum_{historias de k ramas} 1/(4^a 8^b) = (1/4+1/8)^k = (3/8)^k.
```

La intersección infinita tiene densidad cero, pues está contenida en cada
uno de esos conjuntos. **No se sigue que esté vacía.** El argumento permite
todas las historias finitas y no mantiene una semilla positiva al variar k.

Las rachas homogéneas son explícitas:

```text
D^a(x) = 3^a*x/4^a;         máximo a = floor(v2(x)/2),
E^b(x) = 9^b*(x+1)/8^b-1;   máximo b = floor(v2(x+1)/3).
```

Ambos máximos son finitos para x>=1. Una trayectoria infinita tendría,
por tanto, infinitas rachas de ambos tipos. Las fórmulas y la cuenta de
historias tienen derivación escrita y cotejo independiente; no están en Lean.

## 5. Una obstrucción a los rangos polinómicos por residuos

Para cualquier módulo fijo M>=1 y t>=1,

```text
x=8*M*t-1,   H(x)=9*M*t-1>x,   x=H(x)=-1 mod M.
```

Así no puede certificar cada paso de H un rango escalar R con valores
naturales que, en cada clase módulo M, coincida eventualmente con un
polinomio racional y deba disminuir estrictamente. En la clase `-1 mod M`,
ese polinomio es constante o tiene coeficiente principal positivo, porque
toma valores no negativos en una sucesión no acotada. En el primer caso
no disminuye; en el segundo es estrictamente creciente para x grande y
aumenta sobre la familia anterior. Contradicción en ambos casos.

La obstrucción vale también para cualquier número fijo k>=1 de pasos:
`x=8^k*M*t-1` admite k ramas E y termina en `9^k*M*t-1`, en la misma clase
y por encima de x. **Las semillas dependen de k y t**; no es una órbita
expansiva infinita. No excluye rangos definidos sobre dígitos completos,
órdenes más generales, descenso sólo en algunas ramas o horizontes variables.
Es una deducción elemental sobre H, sin pretensión de prioridad.

## 6. Formalización, cotejo y siguiente acción

[PerdicesRetornoH.lean](PerdicesRetornoH.lean) certifica diez teoremas: las
ecuaciones de ambas ramas, positividad, imagen, inyectividad, las dos inversas,
los dos retornos T, ausencia de predecesor en las clases indicadas y la arista
expansiva `8u-1 -> 9u-1`. Define T de forma independiente por la misma fórmula
del atajo. Lean 4.32.2; sólo `propext`, `Classical.choice`, `Quot.sound`.
[Evidencia](evidencia_retorno_h.json), [salida](evidencia_retorno_h.txt) y
[reproductor](comprobar_retorno_h.py). No formaliza la equivalencia global
de terminación del artículo, la densidad ni el corolario sobre polinomios.

[cotejar_retorno_h.py](cotejar_retorno_h.py) comprueba 6144 puentes T/H,
13425 identidades de la inversa y 16382 representantes positivos de todas
las historias de hasta doce ramas, además de rachas homogéneas, 1536 testigos
de §5 y densidades con `Fraction`. Las semillas H entre 1 y 16384 salen antes de 128 pasos;
el récord observado es 11 pasos desde 11504. [Resultado](cotejo_retorno_h.json).
Revisión humana pendiente.

**Siguiente, actualizado:** [Rachas H](RACHAS_H.md) completa el análisis de
E seguida de D: el tamaño del empalme transporta exactamente el mínimo de
la historia concatenada. [Matrices H](MATRICES_H.md) ensaya órdenes sobre
dígitos. La obstrucción de §5 y el límite de las densidades de §4 permanecen.

```powershell
python -B -X utf8 depuracion/perdices20261007/auditar_salidas.py --bits 16 --corte 160 --salida depuracion/perdices20261007/auditoria_salidas.json
python -B -X utf8 depuracion/perdices20261007/cotejar_retorno_h.py --nmax 16384 --profundidad 12 --corte 128 --salida depuracion/perdices20261007/cotejo_retorno_h.json
python -B -X utf8 depuracion/perdices20261007/comprobar_retorno_h.py --compilados "$env:TEMP/perdices_retorno_h_20261011" --salida depuracion/perdices20261007/evidencia_retorno_h.json
```
