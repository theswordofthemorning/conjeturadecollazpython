# Perdices: dos congruencias compartidas y una banda excluida

16-10-2026. Ruta de Codex, separada del trabajo simultáneo de Claude Code.
Continúa [Tres cambios, §6–7](../TRES_CAMBIOS.md#6-una-congruencia-impide-realizar-ese-testigo).
Se conserva el nombre Perdices, sin reivindicar prioridad bibliográfica.

**Resultado:** para toda palabra real `B A^b B^c A^d B^e`, con
`b,c,d,e>=1`, se prueba la cota óptima

```text
b + delta(b mod 6) <= ell(n),
delta = (8,6,8,8,7,8),       ell(n)=ceil(log2(n+5)).       (1)
```

Excluye una familia completa de rachas demasiado largas para la semilla,
no sólo el modelo anterior. Cada uno de los seis bordes se alcanza en
infinitas semillas construidas. Es una restricción necesaria en cuatro
cambios; **no prueba (P) para cuatro cambios ni para cambios arbitrarios**.
El presupuesto global, la salida del piloto y el descenso siguen abiertos.

**Continuación:** [Órbitas y ventanas](ORBITAS.md) formaliza el enlace
desde caminos reales hasta (1), admite b,d=0 y transporta la restricción
a ventanas interiores conservando la semilla original.

## 1. Mapa, dominio y partes compartidas

`T(x)=x/2` para x par y `(3x+1)/2` para x impar, sobre enteros positivos.
`A=1`, `B=110` son paridades reales; las letras cuentan bloques, mientras
sus longitudes en pasos de T son 1 y 3. No se asigna ley aleatoria ni se
condiciona probabilísticamente. La semilla inicial n se conserva.

Considerar primero `B^a A^b B^c A^d B^e`, con los cinco exponentes >=1.
Sean y,z,t las fronteras después de las tres primeras rachas. Que A^b
termine en B obliga a `v2(y+1)=b+2`, pues una entrada B es `3 mod 8`.
Análogamente `v2(t+1)=d+2`. Como b,d>=1, sumar 4 a esos potenciales
da `v2(y+5)=v2(t+5)=2`. El consumo exacto de cada racha produce

```text
n+5 = 2^(3a+2) q,       y+1 = 2^(b+2) r,
z+5 = 2^(3c+2) s,       t+1 = 2^(d+2) v,
9^a q = 2^b r+1,
8^c s = 3^b r+1,
9^c s = 2^d v+1,         q,r,s,v positivos impares.       (2)
```

Las dos primeras ecuaciones enlazan el mismo r. Reducirlas módulo 9 y
módulo 8, respectivamente, es legítimo porque a,c>=1. La tercera muestra
cómo seguir acumulando condiciones; s no es una parte impar independiente.

## 2. La tabla compartida y su prueba

De (2) se deduce simultáneamente

```text
2^b r = -1 mod 9,          3^b r = -1 mod 8.              (3)
```

`2^6=1 mod 9` y `3^6=1 mod 8`. Para cada j=b mod 6, (3) fija r módulo
9 y módulo 8. Como ambos módulos son coprimos, hay exactamente una clase:

| j | r mod 9 | r mod 8 | rho_j = r mod 72 | delta_j |
|---:|---:|---:|---:|---:|
| 0 | 8 | 7 | 71 | 8 |
| 1 | 4 | 5 | 13 | 6 |
| 2 | 2 | 7 | 47 | 8 |
| 3 | 1 | 5 | 37 | 8 |
| 4 | 5 | 7 | 23 | 7 |
| 5 | 7 | 5 | 61 | 8 |

Por tanto `r>=rho_j>=13`. Vale para todos a,c>=1, sin acotar los bits
ni enumerar semillas. En particular r=1 no puede realizar estas dos
recargas enlazadas, aunque la primera congruencia aislada lo permita.
Conservar a general da la cota entera

```text
9^a (n+5) >= 2^(3a+2) (2^b rho_j+1).                    (4)
```

Para a=1, `9(n+5)=32(2^b r+1)`. La tabla satisface
`32 rho_j > 9*2^(delta_j-1)`, luego `n+5>2^(b+delta_j-1)`.
Por la definición entera de ell se obtiene (1).

En particular ell>=b+6: se excluye toda la banda `b>=ell-5`, sean cuales
sean c,d,e>=1. Los residuos 0,2,3,5 excluyen además `b>=ell-7`; el
residuo 4 excluye `b>=ell-6`. Se usa siempre ell(n), no la altura de y,z,t.

## 3. Optimalidad mediante familias orbitales

Fijar j en 0..5 y cualquier b>=1 con `b=j mod 12`. Poner

```text
r=rho_j,    q=(2^b r+1)/9,    s=(3^b r+1)/8,
d=v2(9s-1),                 n=32q-5.                    (5)
```

La tabla da q entero positivo impar. Además `3^b rho_j+1=8 mod 16`,
comprobable en los seis residuos j porque `3^12=1 mod 16`. Así s es
entero positivo impar y d>=1.

Desde n, B termina en `y=36q-5`, con `y+1=2^(b+2)r`. Por consumo,
A^b realiza sus paridades y acaba en z con `z+5=32s`. Un B lleva
a `t=36s-5`, donde `t+1=4(9s-1)` tiene valuación d+2. Por tanto
A^d acaba en otra entrada B, que admite un B final. Se ha construido
la palabra real `B A^b B A^d B` desde esa misma n; todas sus fronteras
son positivas. No se supone previamente que la órbita salga.

Ya se tiene `n+5>2^(b+delta_j-1)`. Como b>=1 y la tabla satisface
`32(rho_j+1/2)<=9*2^delta_j`, también

```text
n+5 = (32/9)(rho_j*2^b+1) <= 2^(b+delta_j).
```

Así `ell(n)=b+delta_j`. Aumentar b en múltiplos de 12 da seis familias
infinitas de semillas distintas. Ejemplo de j=1: b=1, n=91, d=2,
palabra `B A B A^2 B`.

## 4. Control acumulado exacto con carga terminal

Para distinguir la tabla parcial de todas las congruencias, se implementa
un control de la historia completa. No es un teorema nuevo de crecimiento:
desarrolla la codificación de [Cancelaciones, §5](../CANCELACIONES.md#5-toda-historia-finita-de-cambios-tiene-un-cilindro-modular)
y permite exigir además una valuación terminal exacta.

Para una palabra finita W de A/B, sean L sus pasos, S sus unos,
`D=2^L`, `C=3^S` y E el aporte afín: `D*x_final=C*n+E`.
Sea c=1 o 5 según la última letra. Para V>=0 entero, exigir
`v2(x_final+c)=V` equivale a

```text
C*n = D*(2^V-c)-E mod 2^(L+V+1).                       (6)
```

C es impar, luego (6) determina una clase. Su menor representante positivo
n0 realiza W y la carga V; todas las soluciones positivas son
`n0+t*2^(L+V+1)`, t>=0. Para la suficiencia orbital, reducir (6)
módulo 2^L recupera el cilindro de paridades de W. La equivalencia de
ese cilindro con las paridades se obtiene por inducción: un bit de n
elige la paridad siguiente, pues el coeficiente de la frontera es impar.
La ecuación restante fija exactamente la valuación, no sólo una cota.

El programa conserva dos construcciones independientes: composición afín
y levantamiento de bits de n mediante pasos literales de T. Además recorre
la órbita del representante calculado y comprueba su valuación. No enumera
semillas menores ni supone un censo.

Para la palabra anterior `B A^998 B^527 A^1670 B`, L=4255:

| Condición exigida | ell del menor n positivo |
|---|---:|
| Sólo las paridades de la palabra | 4255 |
| Las mismas paridades y V=2600 | 6855 |

Los representantes exactos se conservan en hexadecimal en
[cotejo.json](cotejo.json). Es un cálculo exacto de dos cilindros,
**no una afirmación universal sobre el tamaño de todos los cilindros**.
La tabla de §2 ya obliga a ell>=1006 para b=998; la historia completa
exige mucho más y refuerza su incompatibilidad con ell=1000.

## 5. Evidencia, alcance formal y siguiente obligación

[PerdicesCongruencias.lean](PerdicesCongruencias.lean) certifica la
periodicidad modular, la tabla simultánea, r>=13, la exclusión de r=1,
las cotas enteras inferior y superior y las congruencias de las seis
familias. [Evidencia Lean](evidencia_lean.json), con ocho consultas de
axiomas. La [continuación orbital](ORBITAS.md) añade trece resultados
desde caminos reales hasta la cota con ell y ventanas interiores. La
realización completa de las familias (5) y el cilindro (6) conservan prueba
escrita; no se declara formalización completa de estos dos resultados.

El [cotejo independiente](cotejo.json) cubre 2430 casos orbitales
con rachas 1..3, dos representantes por cilindro y cargas finales
0,1,2,5 o sin fijar; 66 bordes de otras palabras, incluida la vacía;
48 miembros de las familias óptimas; y los dos cilindros grandes.
Estos conteos contrastan las fórmulas, no sustituyen sus pruebas.

La tabla tampoco permite sumar seis bits por cambio: las partes impares
de fronteras sucesivas se relacionan por transporte, y sus cotas mínimas
no constituyen un coste aditivo desde n. Las familias de §3 impiden
mejorar (1) con una constante mayor para el mismo residuo sin más datos.

**Siguiente obligación:** obtener una cota inferior de los representantes
de (6) uniforme en el número de cambios y suficiente para (P), o una
desigualdad acumulativa más débil que aún excluya persistencia desde n.
Reescribir (6) o descartar más palabras aisladas no cierra esa obligación.

La [alta separada](alta_registro.json) queda preparada para integración;
su [verificación](evidencia_registro.json) usa el generador existente
sobre una copia temporal y coteja todas las filas anteriores. No se
modifican el registro central, las bases ni los mapas mientras la otra
ruta trabaja. Revisión humana pendiente. Sin commit ni push en esta tanda.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_congruencias.py --racha-max 3 --periodos-optimos 8 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_lean.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_lean.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/verificar_alta.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_registro.json
```
