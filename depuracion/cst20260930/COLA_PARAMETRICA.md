# Ocelotas: exclusión uniforme de la cola mediante tres desigualdades

03-10-2026. **Formalizado bajo LMN**, con primer cruce finito.
Afina la [cota general](COTA_GENERAL.md) usando la suma geométrica que
ya estaba demostrada en [OcelotasGeometrica.lean](OcelotasGeometrica.lean).
No establece prioridad histórica; revisión humana pendiente.

## Criterio

Mapa atajo T, n>=2, k primer cruce del coeficiente, q=S_k(n) entradas
impares y r=rachas(n,k) bloques maximales de entradas impares. No hay
ley probabilística. Sean R,A,c,H naturales que satisfacen:

```text
R <= 2^c,
5*8^R <= (3A+5)*5^R,
8A*(19(H+33)^2+c+1)+5 < 5*2^H.
```

Si r<=R y falla el descenso en k, entonces:

```text
k < 2^H,
n < 2^(19(H+32)^2+c).
```

[OcelotasColaParametrica.lean](OcelotasColaParametrica.lean) prueba
`region_del_fallo`, su versión desde `LMN23`, y `cst_en_cola`: un primer
cruce con r<=R y k>=2^H coincide con el primer descenso.
Las tres desigualdades son condiciones de un certificado numérico;
la conclusión excluye una región infinita de tiempos, por inducción.

Esto conserva los casos de k pequeño como trabajo pendiente. No prueba
CST completo para cualquiera de los valores grandes de R que aparecen
en los ejemplos, ni existencia universal del primer cruce, ni Collatz.

## Por qué funciona

Pongamos t=floor(log2 k), E=19(t+33)^2 y D=2^k-3^q>0.
LMN y la identidad afín del fallo dan
`Dn<r*3^q<=r*D*2^E`. Por tanto
`n<r*2^E<=2^(E+c)` y `n+1<2^(E+c+1)`.

Las congruencias de las rachas implican
`q<=cota(r,E+c+1)<=cota(R,E+c+1)<=A*(E+c+1)`.
La última desigualdad proviene de la segunda condición del certificado
y de la cota geométrica universal; no expande una cantidad fija de pisos.

Como `5k<=8q+5`, un fallo obliga a

```text
5*2^t <= 5k <= 8A*(19(t+33)^2+c+1)+5.
```

La tercera condición contradice esto para t=H. Persiste para todo t>=H:
la derecha exponencial se duplica, mientras

```text
2*(19(t+33)^2+c+1) - (19(t+34)^2+c+1)
= 19t^2+1216t+19419+c >= 0.
```

Así, t<H. De k<2^(t+1) y t+33<=H+32 salen las dos cotas.
La prueba trata los pares por descenso inmediato y extrae la palabra
de rachas para los impares; no supone una representación ajena a la órbita.

## Ejemplos certificados

Se toma `A=ceil(5(8^R-5^R)/(3*5^R))`, el menor c con R<=2^c y se busca
el primer H que satisface la tercera desigualdad.

| R | H con la fórmula anterior `2R+32` | H con el criterio geométrico |
|---:|---:|---:|
| 21 | 74 | 32 |
| 22 | 76 | 33 |
| 23 | 78 | 34 |
| 50 | 132 | 53 |
| 75 | 182 | 70 |
| 100 | 232 | 88 |
| 1000 | 2032 | 703 |

H es un **exponente**: el límite del tiempo es 2^H pasos del atajo.
Los ejemplos grandes sólo certifican la región posible de fallos;
no significan CST hasta 1000 rachas. Los cierres de pocas rachas ya
usaban colas ajustadas. La aportación aquí es la interfaz uniforme y
su aplicación sin escribir una prueba de cola distinta para cada R.

## Verificación

[OcelotasColasCertificadas.lean](OcelotasColasCertificadas.lean) comprueba
las constantes con `decide +kernel`. [Auditoría completa](evidencia_colas_certificadas.json)
y [salida](evidencia_colas_certificadas.txt): dos módulos compilados,
13 consultas, axiomas estándar, sin `sorryAx`; prefijo de 38 módulos
reutilizado por fuentes, objetos y entorno verificados.

El [cotejo independiente](cotejo_colas_parametricas.json) reconstruye A
con una suma racional iterada, verifica c y la minimalidad de H para
estas constantes. No importa el generador. Las cotas numéricas y sus
huellas están en [colas_parametricas.json](colas_parametricas.json).

```text
python -B -X utf8 depuracion/cst20260930/preparar_colas_parametricas.py --rachas 21 22 23 50 75 100 1000 --salida depuracion/cst20260930/colas_parametricas.json --lean depuracion/cst20260930/OcelotasColasCertificadas.lean
python -B -X utf8 depuracion/cst20260930/cotejar_colas_parametricas.py --certificado depuracion/cst20260930/colas_parametricas.json --salida depuracion/cst20260930/cotejo_colas_parametricas.json
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasColasCertificadas --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_colas_certificadas.json
```

El comprobador compila las dependencias locales nuevas en orden,
reutiliza el prefijo comprobado y conserva todas las consultas y huellas.
No modifica el manifiesto usado por la ejecución de 22 rachas.
