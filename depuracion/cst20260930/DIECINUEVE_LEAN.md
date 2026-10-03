# Ocelotas: diecinueve rachas mediante criba por prefijos — 03-10-2026

**Cierre verificado:** reconstrucción limpia de 32 módulos, código 0.
Las 139 consultas contienen 133 listas de axiomas estándar y seis
declaraciones libres de axiomas, sin `sorryAx`. Se cotejaron las huellas
de fuentes y comprobador ([registro completo](lean_diecinueve.txt)).
Extiende el [cierre de dieciocho rachas](DIECIOCHO_LEAN.md).

## Enunciado y límite

Se usa el atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar,
para enteros n>=2. `S_j(n)` cuenta entradas impares entre los primeros
j pasos. El primer cruce k exige `3^S_j(n)>=2^j` para `1<=j<k` y
`3^S_k(n)<2^k`. `rachas n k` cuenta los bloques maximales de unos
de la palabra de paridad. No hay ley probabilística.

[OcelotasDiecinueve.lean](OcelotasDiecinueve.lean) prueba:

```lean
theorem cst_diecinueve_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 19) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

Un fallo necesita **al menos veinte rachas** (`fallo_exige_veinte`).
Se incluye el caso par. La existencia del primer cruce es una hipótesis;
no se afirma que todo n lo tenga ni que llegue a 1.

`LMN23` es la especialización en 2 y 3 del corolario 2 de
Laurent–Mignotte–Nesterenko, conservado como hipótesis externa explícita.
Su paso a `LMNDebil` está formalizado; la fórmula publicada está
[cotejada con el original](LECTURAS_20261003.md). Sólo la cola usa LMN.

## La dificultad que quedaba

La criba unilateral de la tanda anterior cerraba 18 rachas. Para 19,
la tabla reduce un supuesto fallo a n<294539510, mucho más allá del
certificado finito conservado. Dos intervalos impiden usarlo directamente:

| q=S_k(n) | Cota exclusiva de n |
|---|---:|
| 79335<=q<190537 | 5184570 |
| 190537<=q<10781274 | 294539510 |

Los otros 35 intervalos supervivientes dan n<4912741, ya certificado.
Cinco intervalos más se excluyen directamente por la criba afinada.
Los 42 intervalos cubren `1<=q<2213511501`.

## Reiniciar la criba con un prefijo real

Sea i<k un corte vacío o posterior a una entrada par. Escribimos
`x=T^i(n)`, `q_i=S_i(n)` y `s=rachas n i`. Entonces

`rachas n k = s + rachas x (k-i)`.

No se fusiona una racha a través del corte. Si `rachas n k<=R` y
`x+1<2^M`, la criba entera anterior se aplica a las rachas restantes:

`S_k(n) <= q_i + cota(R-s,M)`,

con `cota(0,M)=0`,
`cota(j+1,M)=floor((5*M+8*cota(j,M)-1)/5)`.

[OcelotasPrefijos.lean](OcelotasPrefijos.lean) demuestra:

- monotonía del contador;
- `rachas_add_corte`, la suma exacta en el corte;
- `criba_contador`, que admite ceros iniciales y palabra vacía, para
  palabras que terminan en entrada par;
- `criba_despues_corte`, usando que el primer cruce termina en entrada par.

La prueba de `criba_contador` quita las entradas pares iniciales por
inducción sobre la longitud, y luego extrae la palabra de rachas ya
formalizada. No presupone una distribución de paridades.

## Certificado por clases

[OcelotasCribaPrefijos.lean](OcelotasCribaPrefijos.lean) conserva el estado

`n=r+m*u`, `T^i(n)=a*u+c`, `m=2^i`, `a=3^S_i(n)`,

junto con q_i, s y la paridad anterior. Para `n<=L` se tiene

`u<=floor((L-r)/m)`, `x<=X=a*floor((L-r)/m)+c`.

Se toma `M=floor(log2(X+1))+1`, por lo que `x+1<2^M`, incluso cuando
X+1 es una potencia de dos. El verificador acepta una clase si:

1. está vacía dentro del intervalo;
2. el coeficiente ya cruzó y `c<r`, lo que prueba descenso para toda
   la clase;
3. el prefijo ya supera R rachas; o
4. el corte está permitido y `q_i+cota(R-s,M)<q_min`.

En los demás casos separa u par e impar y continúa. Agotar el combustible
rechaza. `comprobar_correcto` prueba que la aceptación contradice un fallo
real con n en el intervalo, `S_k(n)>=q_min` y `rachas n k<=R`.
`certificado_descenso` expresa esa consecuencia sin presuponer una cota de k.

[OcelotasDiecinuevePrefijos.lean](OcelotasDiecinuevePrefijos.lean) evalúa
dos certificados en el núcleo con `decide +kernel` y combustible 64:

| Intervalo de n, inclusivo | q mínimo | Nodos | Profundidad máxima |
|---|---:|---:|---:|
| 4912741..5184569 | 79335 | 12201 | 36 |
| 4912741..294539509 | 190537 | 4047 | 38 |

Las dos declaraciones booleanas no dependen de ningún axioma.
La corrección universal sólo usa los axiomas estándar de Lean.
Las cantidades de semillas son 271829 y 289626769, respectivamente;
los dominios se solapan y esas cantidades **no se suman**.
No se censan individualmente cientos de millones de órbitas.

## Tabla, cola y ensamblaje

[OcelotasDiecinueveTabla.lean](OcelotasDiecinueveTabla.lean) conserva las
42 parejas unilaterales, los signos de logaritmos certificados y las cotas
de semilla. En las dos filas señaladas aplica los certificados nuevos;
todo supuesto fallo restante tiene n<4912741. El generador y su JSON sólo
proponen constantes: Lean comprueba todos los productos, pisos y potencias.

Se reutiliza sin ampliar el certificado
[OcelotasResiduosFinito.lean](OcelotasResiduosFinito.lean), válido hasta
4912740 para cualquier cantidad de rachas y sin LMN.

La [cola de 19](OcelotasDiecinueveCola.lean) usa el lema geométrico
genérico para probar `cota(19,M)<=12592*M`. Para t>=31,

`25184*(19*(t+33)^2+6)<2^t`.

LMN y el supuesto fallo dan `k<=25184*(19*(t+33)^2+6)`, mientras
`2^t<=k`. Como `q>=2213511501>2^31` implica k>q, cubre la cola completa.
El ensamblaje extrae las rachas del contador real y conserva explícita esa
relación al aplicar los certificados de prefijos.

## Contraste independiente

[cotejar_diecinueve_lean.py](cotejar_diecinueve_lean.py) verifica las 42
filas con series racionales de `atanh`, comparaciones enteras y una
recurrencia distinta para los pisos. Confirma que sólo las filas 35 y 36
necesitan los certificados nuevos ([salida](cotejo_diecinueve_lean.json)).

[cotejar_prefijos.py](cotejar_prefijos.py) no importa el explorador ni sus
transiciones afines: reconstruye cada prefijo por iteración directa desde
su menor representante. En cada hoja prueba otro representante, incluido
el máximo dentro del intervalo cuando hay varios. Comprueba las potencias,
el contador, la paridad anterior, la cota por racionales exactos y la
disjunción de las clases mediante intervalos diádicos de bits invertidos.
Las cantidades coinciden con ambos intervalos inclusivos y las huellas
de todas las hojas coinciden ([salida](cotejo_prefijos_19.json)).
Es un contraste finito de la interpretación; la prueba universal es la
de corrección del verificador y su evaluación en Lean.

El [registro versionado](../coherencia20260913/registro.json) incorpora
`ocelotas_cst_diecinueve_rachas_prefijos_lean`. La base se regeneró con
258 afirmaciones y las comprobaciones de vocabulario, referencias e
integridad pasaron sin fallos ([salida](registro_diecinueve.txt)).

El ensayo inicial con criba afinada, desde n=2, necesitó 2715 nodos
([salida conservada](exploracion_prefijos_19.json)). Para la prueba se
eligió la criba entera ya certificada, que también cierra y simplifica
la interfaz formal. Los dos certificados finales conservan sus
[parámetros bajos](prefijos_19_bajo.json) y [altos](prefijos_19_alto.json).

## Preparación de veinte rachas

La [tabla propuesta de R=20](preparacion_veinte_lean.json) vuelve a dejar
dos intervalos por encima del certificado finito. La exploración entera,
con combustible 96 y presupuesto de **un millón de nodos por caso**, da:

| Intervalo de n, inclusivo | q mínimo | Nodos | Profundidad máxima |
|---|---:|---:|---:|
| 4912741..5457441 | 79335 | 55811 | 43 |
| 4912741..310041588 | 190537 | 67649 | 46 |

Ambos terminaron sin obligaciones pendientes. El cotejo independiente de
prefijos, cotas y cobertura coincidió en las 30348 hojas no vacías
([salida](cotejo_prefijos_20.json), [caso bajo](prefijos_20_bajo.json),
[caso alto](prefijos_20_alto.json)). En la tanda siguiente se evaluaron
en Lean mediante bloques y se ensambló el cierre de veinte rachas:
[prueba y evidencia posterior](VEINTE_LEAN.md). Esta ficha conserva
el cierre y el registro originales de diecinueve.

## Reproducir

Desde la raíz, con Lean 4.32.2 y el Mathlib fijado:

```text
python -B -X utf8 depuracion/cst20260930/preparar_cierre_lean.py --rachas 19 --bits-cola 31 --salida depuracion/cst20260930/preparacion_diecinueve_lean.json
python -B -X utf8 depuracion/cst20260930/generar_diecinueve_lean.py --certificado depuracion/cst20260930/preparacion_diecinueve_lean.json --salida depuracion/cst20260930/OcelotasDiecinueveTabla.lean
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_diecinueve.txt
python -B -X utf8 depuracion/cst20260930/explorar_criba_prefijos.py --inicio 4912741 --limite 5184569 --q-min 79335 --rachas 19 --combustible 64 --criba entera --salida depuracion/cst20260930/prefijos_19_bajo.json
python -B -X utf8 depuracion/cst20260930/explorar_criba_prefijos.py --inicio 4912741 --limite 294539509 --q-min 190537 --rachas 19 --combustible 64 --criba entera --salida depuracion/cst20260930/prefijos_19_alto.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos.py --certificados depuracion/cst20260930/prefijos_19_bajo.json depuracion/cst20260930/prefijos_19_alto.json --salida depuracion/cst20260930/cotejo_prefijos_19.json
python -B -X utf8 depuracion/cst20260930/cotejar_diecinueve_lean.py --certificado depuracion/cst20260930/preparacion_diecinueve_lean.json --salida depuracion/cst20260930/cotejo_diecinueve_lean.json
```

No se amplía el censo consecutivo anterior hasta `2^23`. La prueba
trascendente de LMN, la revisión humana y la novedad siguen pendientes.
El cierre exacto de 75 rachas bajo Rozier–Terracol conserva su alcance;
no se presenta como un cierre Lean completo.
