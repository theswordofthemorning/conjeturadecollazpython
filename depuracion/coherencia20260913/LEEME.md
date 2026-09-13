# Auditoría de coherencia de ambos repositorios — 13-09-2026

El estado utilizable y el siguiente trabajo están en
[ESTADO_INVESTIGACION.md](../../ESTADO_INVESTIGACION.md) y en
[el plan de zootheorem](../../../zootheorem/PLAN_INVESTIGACION.md).
Esta tanda corrige código, registros y alcance matemático. No declara
resuelta la densidad ni recertifica todos los experimentos históricos.

## Alcance de la revisión

Se cotejaron las instrucciones, RutaTeoremas, los resúmenes del programa,
las cinco tandas del frente del 10-09, la revisión local 12, los generadores
SQLite y sus bases, los tres papers públicos, los datos y los drafts OEIS.
El inventario inicial del laboratorio contenía 200 archivos Python y 78
archivos Lean, incluidos experimentos y sondas históricas. El análisis de
sintaxis cubre todos los Python inventariados; la ejecución se concentra
en el motor, persistencia, frente actual y verificadores públicos.

Se recompilaron nueve archivos Lean: los cinco del frente, cadenakc,
cabras, conejas y el espejo publicado. Que compilen acredita sus
enunciados formales, no cualquier interpretación de sus títulos ni el
ensamblaje probabilístico escrito alrededor. No se ejecutaron todas las
sondas históricas ni los censos grandes de n=29..36.

Al cierre se analizaron sintácticamente los **205 Python del laboratorio
y los 4 de zootheorem**, y se comprobaron 24 enlaces locales de los
documentos actuales. El detalle está en `estatica.json`. Los dos
`git diff --check` terminaron sin errores de espacios.

`revision12_adv1/` ya existía sin seguimiento en Git al comenzar esta
tanda. Se leyó y se preservó sin modificar. Las actas y transcripciones
anteriores se conservan; Pandas tiene una copia literal con aviso en
[historico/lemadepandas_20260803.txt](historico/lemadepandas_20260803.txt).

## Hallazgos y reparaciones

| Hallazgo | Reparación y límite |
|---|---|
| El CLI llamaba «contraejemplo» a superar un tope de pasos | Ahora informa «inconcluso», semilla pendiente y prefijo verificado; permite una llegada exactamente en el tope y valida el dominio |
| Pandas/Jirafas intercambiaban densidad y unión creciente | Se retira esa prueba; queda densidad inferior(F)>=phi. El contraejemplo periódico y el lema condicional correcto están escritos |
| Fusión se confundía con igualdad de alturas finitas | Se explicitan convergencia y primeras llegadas; la fusión levantada vale incluso para m=0 |
| Se infería phi<1 de un riesgo que tiende a cero | Se retira la inferencia y se da el contraejemplo p_i=1/(i+1) |
| La razón de términos se trataba como equivalente a phi=1 | Se distingue tasa exponencial de suma ponderada; la equivalencia queda retirada |
| Cabras mezclaba c firmado con su valor absoluto | Ambas puertas entran en 2 mod 3; se corrigen comentario Lean, cálculo Python, catálogo y registro. La puerta directa también puede fundir |
| E[m]=1 se confundía con E[log m]=0 y una perpetuidad iid | Se precisan la ley y el alcance; el paper 03 usa Jensen estricto y exige 0<=s<=1/2 |
| Se excluían cuasipolinomios a partir de una búsqueda restringida | El script declara P(n)+C(n mod p), distingue insuficiencia de datos y ajuste fallido, y no deduce una ley asintótica |
| Los drafts locales y las notas de envío estaban atrasados | Se copian los textos ya enviados el 13-09, se añaden b-files y verificador; los envíos antiguos quedan marcados como históricos |
| Las conclusiones actuales faltaban en SQLite | Registro versionado: 31 correcciones y 8 altas; se actualizan nodos y dependencias, sin desplazar los 208 IDs históricos |
| Regenerar SQLite borraba primero la base anterior | Se construye un temporal, se valida todo y sólo entonces se reemplaza; fallo de validación o reemplazo conserva el archivo previo |
| La captura ignoraba conflictos literales y confirmaba antes de validar | Rechaza conflictos y revierte el lote; funciona desde otro directorio usando la ubicación del script |

Las demostraciones, hipótesis y contraejemplos están en
[Matematica.md](Matematica.md). Las correcciones precisas de cada fila,
incluidos los textos anteriores, están en [registro.json](registro.json).
No se atribuye novedad bibliográfica a los argumentos elementales añadidos.

## Resultado de los estratos

e8(9)=1; los tres estratos son cero en n=1..8. Los 33 términos
originalmente mostrados en n=10..20 coinciden con el cálculo directo.
Los offsets completos actuales son 9,2; 11,2; 13,2. El verificador
público enumera las tres sucesiones en n=1..20: **60 conteos**.

Testigos: e8(9), r=65; e8(10), r=131,193,473; e10(11), r=769;
e12(13), r=1025, en sus módulos respectivos. Las trazas y pasos mixtos
quedan en [zoo_strata_salida.txt](zoo_strata_salida.txt).

Durante la implementación del control de testigos se corrigió una
suposición demasiado fuerte del propio verificador: k pasos mixtos
no obligan a que cada trayectoria tenga exactamente k/2 impares, pues
puede haber pasos compartidos impares. El criterio correcto exige
igualdad de los dos conteos. No apareció una discrepancia de DATA.

## SQLite y continuidad del registro

La fuente histórica literal de `guardarafirmaciones.py` coincidía con
sus 208 filas, 78 correcciones, 45 nodos y 74 dependencias antes de la
actualización. El registro vigente conserva esas filas como base y
aplica cambios verificados por identidad literal y huella SHA-256.
Ahora hay **216 afirmaciones, 84 correcciones, 52 nodos, 84 dependencias**
y claves estables para las ocho altas. Las 20 constantes se conservan.

`depuracion/veredictos.jsonl` se interpreta contra los enunciados de sus
fichas históricas. Sus A-números internos no son una clave foránea segura
hacia la tabla actual: por ejemplo, la ficha A50 y la fila 50 actual
describen objetos diferentes. No se trasladaron veredictos por número.

`respuestas.db` pasó de 1.826 a 1.957 mensajes, incorporando 131 mensajes
literales de dos archivos disponibles. La fecha máxima pasó de
2026-08-12 a **2026-08-24**. No se encontraron transcripciones de
septiembre en esas fuentes. Las 1.826 filas previas se compararon
íntegramente con la copia de seguridad: ninguna cambió. `hilos.db`
almacena trayectorias, no este catálogo; no se regeneró.

La captura repetida añadió cero filas. La segunda regeneración del
catálogo fue idéntica byte a byte. Véanse [captura.json](captura.json) y
[persistencia.json](persistencia.json). Las copias SQLite previas se
hicieron mediante la API de backup en
`%TEMP%/coherencia20260913_backup/`; son respaldo local, no una dependencia
necesaria para reproducir los controles.

## Reproducción y resultados

Desde la raíz del laboratorio:

```powershell
python -B -X utf8 guardarafirmaciones.py
python -B -X utf8 depuracion/coherencia20260913/ejecutar_controles.py
```

La primera orden regenera el catálogo. La segunda ejecuta **24 controles
acotados**, guarda cada salida y crea [controles.json](controles.json).
Todos pasaron en esta tanda, con Lean 4.32.2; las salidas revisadas no
contienen `sorryAx`. La prueba de persistencia incluye fallos simulados
de escritura y confirma que no destruyen el original.

Además de los controles del frente:

- Motor: topes, prefijo, CLI y comparación de 1.001 trayectorias clásicas.
- Aritmética: Garner y puertas con signo, cotas de balota hasta 1.000,
  inversión entera del reloj hasta 10.000, ajuste restringido y cruce
  simbólico/directo de estratos hasta 13.
- zootheorem: a(n) directo hasta 20, q=5,7 hasta 18, obstrucción hasta
  14, estratos hasta 20; listas almacenadas y b-files completos concordantes.
- Documentos: cuatro listas largas y las constantes explícitas del
  paper 03. Más allá de los rangos directos sólo se comprueba coherencia
  de copias, no una nueva enumeración.

Los barridos `estratoscadena.py` y `subrenovacionc.py` se importan sin
ejecutar experimentos; por defecto llegan a 20. Un límite de estados
produce un error explícito de cálculo incompleto. Los scripts antiguos
no cubiertos aquí deben seguir revisándose antes de lanzar barridos.

## Qué deja abierto esta depuración

Se obtiene una deducción escrita útil al combinar Mangostas y Gacelas:
la cola uniforme de una excursión es O(sqrt(log(t)/t)). No cierra el
reloj global, porque faltan tramos de frontera. Tampoco se adopta el
O(n) propuesto en la revisión 12 a partir de una media medida.

El próximo trabajo es P1 y P2 del plan: reloj global y ventana de W en
la salida bajo la ley real. Faltan después los arranques y la suma de
riesgos condicionales. No hay fundamento para asignar un porcentaje
fiable de éxito al cierre de la conjetura.

Los cambios de esta auditoría son locales: no se hizo commit, push ni
una nueva edición en OEIS. La aclaración adicional de A398792 quedó
preparada en la revisión de zootheorem. La aprobación de los tres
drafts sigue pendiente de los editores en el último estado registrado.
