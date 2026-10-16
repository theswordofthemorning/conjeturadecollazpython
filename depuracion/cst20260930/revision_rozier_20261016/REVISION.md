# Comprobación previa a la respuesta a Olivier Rozier — 16-10-2026

Encargo: comprobar los cuatro puntos antes de responder, preparar un borrador
y **no enviarlo**. La ruta de Perdices permanece detenida. Esta revisión trabaja
con Ocelotas y no supone que Rozier haya revisado o avalado nuestras pruebas.

**Decisión de cierre:** el [Plan B](PLAN_RESPUESTA.md) aplaza la respuesta
hasta disponer de un avance considerable y un nuevo paper. Se responderán
entonces todas sus preguntas, brevemente, junto con la presentación del trabajo.

## Resultado y dependencias

**83 rachas comprobadas en Lean**, con dos entradas alternativas:

```text
LMN23 + RecordRoosendaal -> CST para todo primer cruce finito con r<=83
RhinHomogenea 2 + RecordRoosendaal -> la misma conclusión
```

Mapa `T(n)=n/2` para n par y `(3n+1)/2` para n impar; dominio `n>=2`;
`k` es el primer índice finito con `3^S(k,n)<2^k`; `S` cuenta pasos
impares entre los índices 0 y k-1; r cuenta inicios de rachas impares.
Conclusión: no hay descenso antes de k y `T^k(n)<n`. **La existencia
universal de k, Collatz y CST sin límite de rachas no se demuestran.**

`RecordRoosendaal` significa que cada entero entre 2 y
`N=46645791847966786687`, inclusive, llega a 1 en como mucho 2480 pasos
del mapa **clásico** `Col(n)=3n+1` para n impar, `n/2` para n par.
Es una hipótesis de cobertura externa; no se deduce de comprobar una semilla.
El teorema trascendente escogido también sigue como hipótesis explícita.

Código final: [OcelotasRozier.lean](../OcelotasRozier.lean).
Auditoría: [evidencia_rozier.json](../evidencia_rozier.json) y
[salida con los tipos completos](../evidencia_rozier.txt).
La cadena registra **146 consultas de axiomas**, todas estándar:
`propext`, `Classical.choice`, `Quot.sound`; ninguna `sorryAx`.
Se reutiliza la base auditada por SHA256 y se compilan las extensiones.
No es una reconstrucción limpia de Mathlib ni una revisión humana.

## 1. Antecedentes y Simons

El correo original contiene tanto una valoración favorable sobre el tratamiento
general como la advertencia de que John Simons investigó la cuestión. No permite
certificar prioridad. La búsqueda dirigida localizó el artículo de Simons,
[*Het 3x+1-probleem, recente ontwikkelingen en oplossingsrichtingen*](https://www.nieuwarchief.nl/serie5/pdf/naw5-2022-23-3-147.pdf),
NAW 5/23(3), 147–152 (2022). Sus pp. 150 y 152 estudian **m-nykels**:
segmentos entre mínimos, con incremento final positivo, y restricciones sobre
su concatenación y sobre órbitas divergentes. Es un antecedente real y cercano;
no se debe presentar nuestra adaptación como nacida sin antecedentes.

En las secciones consultadas no aparece el cierre general de CST por número
de rachas que usamos. Esto **no demuestra ausencia de trabajos publicados o
inéditos**. La prioridad queda pendiente; una búsqueda web no la certifica.
La búsqueda de enviados a `j.l.simons@rug.nl` o destinatarios `simons` no devolvió
mensajes. No se contactó a Simons ni se envió nada a Rozier.
Por petición del usuario, el borrador solicita a Rozier el contacto actual de
Simons. Se distingue la dirección publicada años atrás de una dirección vigente
confirmada; no se afirma que no exista ninguna dirección pública.

## 2. Qué comprueba Lean y qué queda fuera

En la versión de 81, `LMN23` y `RozierTerracol54` eran argumentos del
teorema. Que `#print axioms` sólo enumere axiomas estándar no demuestra esas
premisas. La respuesta correcta describe **las premisas y la conclusión**.

La revisión añade [OcelotasRoosendaal.lean](../OcelotasRoosendaal.lean),
que descarga la premisa CST a partir del registro de tiempos. No copia el
corolario externo como si hubiese quedado demostrado por cambiar una constante:

1. La pareja de fracciones `3647/2301` y `1054/665` tiene determinante 1.
   La primera está por encima de `log(3)/log(2)` y la segunda por debajo.
   Los encierros racionales de log 2 y log 3 certificados dan
   `3647 log 2 - 2301 log 3 > 1/1200`.
2. El lema unilateral existente transporta esa cota a toda forma positiva
   `k log 2-q log 3` con `0<q<2966`. No se enumeran sólo convergentes sin
   justificar el paso a los demás enteros.
3. Si k<=2480 y falla CST, r<=k y el lema de semillas dan
   `n < 2480*1200 = 2976000`. El certificado previo en el núcleo cubre
   todas las semillas hasta **4912740**. Contradicción. Así se prueba
   CST para todo primer cruce con k<=2480, sin hipótesis externas.
4. Una inducción formal relaciona los mapas: llegar a 1 en d pasos clásicos
   implica llegar en t<=d pasos de T. Si k es el primer cruce, k<=t:
   de lo contrario, el lema de no descenso anterior impediría alcanzar 1.
5. Por tanto, la cobertura clásica hasta N con d<=2480 implica CST hasta N.
   Este puente se ensambla con la tabla de 83 y con cada una de las dos colas.

No se reivindica como nuevo el enunciado de CST para tiempos cortos.
El original de Terras (1976), p. 252, ya da un alcance mayor, hasta 2592
en su notación. Se leyó la página escaneada del
[archivo de Acta Arithmetica](https://matwbn.icm.edu.pl/ksiazki/aa/aa30/aa3034.pdf).
La contribución aquí es la comprobación formal concreta y su enlace con los
datos externos, suficiente para esta revisión.

## 3. Rhin frente a LMN: comprobación y corrección de la explicación

**LMN original vuelto a leer:** *Formes linéaires en deux logarithmes et
déterminants d'interpolation*, JNT 55 (1995), 285–321,
[DOI](https://doi.org/10.1006/jnth.1995.1141), corolario 2, p. 288.
El PDF conservado está ahora en `Collatz Investigacion/` dentro del repositorio;
su SHA256 coincide con el registrado el 03-10. Se toman alpha1=3, alpha2=2,
b1=q, b2=k, D=1, log A1=log 3, log A2=1. Se satisfacen las condiciones de
altura y positividad; 2 y 3 son multiplicativamente independientes. Se
conservan el máximo, 24.34 y 0.14 del original. El paso a la cota debilitada
ya está en `OcelotasLMNFuente.lean`.

**Original de Rhin obtenido y cotejado:** DOI
[10.1007/978-1-4757-4267-1_11](https://doi.org/10.1007/978-1-4757-4267-1_11),
*Approximants de Padé et mesures effectives d'irrationalité*, pp. 155–164.
La búsqueda inicial en Springer, ResearchGate, Academia, OpenAlex y HAL no
permitió obtener el texto completo; las primeras copias sólo tenían pp. 155–156.
El usuario aportó después `28Rhin_Sm_Paris_1987.pdf`, localizado en Descargas:
**10 páginas, 490221 bytes**, copia de trabajo en
`Collatz Investigacion/28Rhin_Sm_Paris_1987.pdf`.
SHA256: `1ada4c7f51933af33feb14757e4fcd46c19f33748da93d950b8e6a9b647cfd1e`.
No se ha establecido la URL de descarga de esta copia; el DOI identifica
el artículo. El PDF local permanece fuera del control de versiones.

Se leyó visualmente la proposición de la **p. 160, ecuación (7)**. Para
`u0,u1,u2` enteros y `H=max(|u1|,|u2|)>=2`, afirma

```text
|u0 + u1 log 2 + u2 log 3| >= H^(-13,3).
```

El signo es **>=**, tanto en el umbral como en la conclusión; el OCR omite
algunas barras. No hay factor multiplicativo adicional ni restricción sobre
u0. Esto coincide con `OcelotasRhin.RhinProposicion 2`. Poniendo u0=0 se
obtiene `RhinHomogenea 2`, la premisa del cierre de 83 ya compilado.
En nuestra aplicación u1=k, u2=-q y 3^q<2^k implica q<k; por ello H=k.
El paso a `RhinDesde 2`, incluida la relajación de 13,3 a 14, ya está
formalizado en `desde_homogenea`. No hace falta cambiar el código Lean.

La ecuación (8) da el exponente **7,616 sólo para H>=H0**, con H0
efectivamente calculable pero sin valor numérico en el capítulo. No se usa
esa cota asintótica en nuestro cierre.

**Alcance de la lectura:** se cotejaron también el método de pp. 158–160 y
el apéndice de p. 162. El texto indica que (7) usa mejores aproximaciones
simultáneas `q log 2-p1`, `q log 3-p2` para `q<=7,32*10^12`, calculadas
por E. Dubois y P. Toffin con Macsyma. No incluye la salida completa de
esos cálculos; el apéndice proporciona polinomios para (8). No hemos
reconstruido esos cálculos ni formalizado la prueba de Rhin. Queda cerrado
el cotejo del **enunciado original y su aplicación**, conservando Rhin
como teorema externo explícito. El comentario inicial de `OcelotasRhin.lean`
describe la situación anterior a obtener este PDF.

Sí se obtuvieron y leyeron dos fuentes académicas explícitas sobre el rango:

- Waldschmidt, [*Linear independence of logarithms of algebraic numbers*](https://webusers.imj-prg.fr/~michel.waldschmidt/articles/pdf/LIL.pdf),
  sección 12, p. 12-4 (página PDF 106): `H=max(|b1|,|b2|)>=2` y
  `|b0+b1 log 2+b2 log 3|>=H^(-13.3)`.
- Siefken, [*A Minimal Subsystem of the Kari–Culik Tilings*](https://www.math.toronto.edu/siefkenj/homepage/papers/kc-minimality.pdf),
  proposición 31: mismo umbral y exponente; distingue el 7.616 asintótico.

Estas dos referencias coinciden con el original ahora leído. La nueva
versión Lean asume literalmente el caso homogéneo para H>=2; comprobar
la fuente no convierte ese supuesto en una prueba formal de Rhin.

[OcelotasColaRhin.lean](../OcelotasColaRhin.lean) prueba la cola con el
puente real-entero de Rhin ya existente. Si `n<r*k^14`, `R<=2^c` y
`5*8^R <= (3*A+5)*5^R`, basta

```text
8*A*(14*(H+1)+c+1)+5 < 5*2^H
```

para excluir todos los k>=2^H. La propagación a exponentes mayores se
demuestra por inducción. Con los mismos A y c=7:

| Rachas | H con LMN | H con Rhin |
|---|---:|---:|
| 81 | 75 | 67 |
| 82 | 75 | 67 |
| 83 | 76 | 68 |
| 84 | 77 | 69 |

Son los primeros H que satisfacen **estos criterios suficientes**, no cotas
óptimas de los teoremas trascendentes. Para 83, la mejora por un factor 256
del corte se certificó en Lean y se ensambló con la misma tabla finita.

**Tramo que no mejora con esa sustitución:** el generador de pesos vuelve
a fallar para 84 en `4640282259296926456<=q<27444133206411171953`.
La primera pieza fallida empieza en N+1. En ese intervalo la cota unilateral
c ya satisface exactamente `c*q_inicio^13>1`. Como k>q, resulta
`k^(-13.3)<=q_inicio^(-13)<c`: la cota general de Rhin es más débil allí que
la información finita utilizada. Y el primer cruce cumple
`5*k<=8*q+5`, por lo que esta ventana queda por debajo del corte Rhin.
Esto explica por qué **la sustitución en la criba actual** no cierra 84.
No descarta otras aplicaciones de Rhin, nuevas cribas ni la verdad de 84.

## 4. Récord, 2510 y certificado de 83

Se conservaron URL, fecha de consulta, cabeceras pertinentes y SHA256 en
[fuentes.json](fuentes.json). La [página de Roosendaal](http://www.ericr.nl/wondrous/delrecs.html)
define la tabla como récords confirmados: todos los enteros anteriores fueron
comprobados y tienen menor tiempo. Su [archivo de datos](http://www.ericr.nl/wondrous/delays.txt)
termina en N; `Last-Modified: Mon, 28 Sep 2026 18:14:54 GMT`.

[comprobar_numeros.py](comprobar_numeros.py), independiente del generador de
pesos, verifica los 149 números publicados con dos implementaciones de mapa:
para N obtiene **2480 pasos clásicos = 1546 pasos T + 934 pasos impares T**.
Esto verifica las trayectorias y unidades, **no la cobertura intermedia**.

También se reconstruyeron con enteros las constantes de
[Rozier–Terracol v5](https://arxiv.org/pdf/2502.00948v5), prueba del teorema
5.3: todos los m<113383 tienen máximo T<=785412368<10^9;
113383 alcanza 1241055674. La primera j>1 con H(j)>=113383 es j=1539;
la cota correspondiente de impares es q>=971. Así, 1539+971=2510>2480.
Se hicieron las comparaciones de potencias exactas, sin usar un logaritmo
de coma flotante para decidir los bordes. El censo de secuencias paradójicas
hasta 10^9 del artículo no se repitió. El puente de la sección 2 permite
prescindir de él para **esta consecuencia CST**.

La tabla de 83 se regeneró desde cero: 101 intervalos, 92 remisiones al
intervalo externo, nueve filas por pesos, **115 piezas** y cola LMN H=76.
[cotejo_pesos_83.json](../cotejo_pesos_83.json) confirma logaritmos mediante
series racionales independientes, determinantes, signos, contigüidad,
cobertura y cotas. Los ocho módulos de tabla y el cierre pasaron Lean.
La trayectoria individual del récord tiene además su
[módulo separado](../OcelotasRecordRoosendaal.lean), deliberadamente distinto
de la hipótesis universal `RecordRoosendaal`. Su comprobación de 2480 pasos
fue aceptada por el núcleo **sin depender de ningún axioma**:
[evidencia](../evidencia_record_roosendaal.json).

## Reproducir y responder

Los números independientes están en [cotejo_numeros.json](cotejo_numeros.json).
Las fuentes descargadas quedan en `%TEMP%/rozier_fuentes_20261016`;
los originales locales y sus huellas se conservan. No se redistribuyen aquí
los artículos completos. Los comandos de auditoría constan en cada JSON;
Lean 4.32.2 y Mathlib están fijados por el proyecto.

Para repetir el cotejo numérico en esta máquina:

```powershell
python -B -X utf8 depuracion/cst20260930/revision_rozier_20261016/comprobar_numeros.py --fuentes "$env:TEMP/rozier_fuentes_20261016" --carpeta depuracion/cst20260930/revision_rozier_20261016 --salida depuracion/cst20260930/revision_rozier_20261016/cotejo_numeros.json
```

La auditoría final reutilizable se ejecutó con:

```powershell
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasRozier --compilados-base "$env:TEMP/ocelotas_auditado_20261003" --compilados-extension "$env:TEMP/ocelotas_rozier_auditado_20261016" --salida depuracion/cst20260930/evidencia_rozier.json
```

Esos comandos requieren las fuentes descargadas y la base auditada locales.
La reconstrucción de la base se describe en [77 rachas](../SETENTA_Y_SIETE_LEAN.md);
no se presenta esta invocación como una instalación independiente desde cero.

El [borrador](BORRADOR_RESPUESTA.md) responde sobre Simons, Rhin y las
premisas, agradece la mejora concreta y separa la revisión matemática de un
aval humano. El correo está **sin enviar** y se conserva para el Plan B.
El usuario autorizó el commit y push de esta revisión al cerrar la sesión
del 16-10; esa publicación del código no activa el envío del correo.
