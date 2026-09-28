# Análisis de zootheorem — 20-09-2026

`zootheorem` es la capa de publicación del laboratorio: tres papers, siete
b-files, cuatro verificadores Python independientes del motor experimental y un
certificado Lean. Los controles ejecutados pasan. La ruta de investigación
coincide con el laboratorio: P1, P2 y P3 siguen abiertos.

Esta revisión no modifica programas, papers, datos ni drafts de `zootheorem`.
El informe y su evidencia se conservan aquí, junto al análisis del laboratorio.

## Relación entre los repositorios y alcance

Se revisó `zootheorem` en el commit `5e03432`, rama `main`, sin cambios locales;
tras `git fetch origin` seguía coincidiendo con `origin/main`. Tiene su propio
directorio `.git` y no hay commits compartidos entre las referencias locales de
ambos repositorios. Es un derivado del trabajo del laboratorio con historia Git
propia, no un worktree de la misma rama.

El inventario completo tiene **40 archivos**: 14 Markdown, 18 TXT, cuatro Python,
dos JSON, un TSV y un Lean. Se leyeron los tres papers, los cuatro verificadores,
las definiciones y resultados del certificado, el plan y los drafts vigentes
necesarios para comprobar las sucesiones. Los archivos históricos se inventariaron
sin precargar todas las versiones de planes y entregas.

Los verificadores Python sólo dependen de la biblioteca estándar, usan enteros
para contar y no importan módulos del laboratorio. El archivo
`lean/mirror_theorem.lean` es idéntico byte a byte a `espejoak.lean` del laboratorio:
son dos copias del mismo certificado, no dos formalizaciones independientes.

## Qué afirma y qué acredita cada pieza

| Pieza | Resultado y límites |
|---|---|
| [Paper 01](../../../zootheorem/papers/01-merging-classes.md) | Define a(n), prueba la duplicación y la cota de densidad inferior, y presenta el espejo. La igualdad de alturas finitas requiere convergencia y controlar primeras llegadas. |
| [Paper 02](../../../zootheorem/papers/02-generalized-maps.md) | Extiende los conteos a q=5,7, prueba la obstrucción modular y calcula el multiplicador medio en pasos compartidos bajo una ley explícita. No deduce densidades asintóticas de esa media. |
| [Paper 03](../../../zootheorem/papers/03-uniform-fractional-moment-bound.md) | Prueba escrita del control de momentos fraccionarios a tiempos deterministas, bajo dominación e independencia del multiplicador respecto de u_t. No demuestra el control condicionado en la salida. |
| [Espejo Lean](../../../zootheorem/lean/mirror_theorem.lean) | Conjugación sobre enteros, periodicidad, reflexión y equivalencia de conteos para todos los niveles. No demuestra convergencia ni clasificación exhaustiva de ciclos. |
| `seqs/` y `drafts/` | Almacenan datos, definiciones y preparación editorial. Las validaciones distinguen recálculo directo de coherencia entre copias. |

La lógica de las pruebas escritas revisadas es consistente con sus hipótesis:
la duplicación eleva una clase a dos; la inclusión de cada conjunto periódico
da una cota para la densidad inferior de la unión; la obstrucción modular usa un
factor invertible común cuando coinciden tiempo y conteo impar. El paper 03
itera una desigualdad de momentos obtenida por subaditividad y Jensen estricto.
Ninguno de esos argumentos permite sustituir automáticamente tiempo fijo por
tiempo de salida condicionado.

## Hallazgos y pendientes de mantenimiento

### 1. Comentario del certificado con alcance excesivo

Las líneas 44–45 de `lean/mirror_theorem.lean` dicen que 3n+1 «tiene uno» y
3n−1 «tiene tres» ciclos positivos. Esa redacción presenta una clasificación
exhaustiva que los teoremas del archivo no prueban. Debe distinguir los ciclos
conocidos de la exclusión de otros ciclos. El comentario no interviene en la
prueba formal del espejo, que compila y conserva su alcance.

Como el archivo coincide con el del laboratorio, una futura corrección editorial
debe conservar la coherencia de ambas copias. La línea 49 también conserva el
comando del laboratorio `lean espejoak.lean`; aquí el comando ejecutable es
`lean lean/mirror_theorem.lean`, ya indicado correctamente en el README.

### 2. Dos verificadores ejecutan el recálculo al importarse

`verify_merging_classes.py:69` y `verify_q_family.py:49` tienen los barridos
en el nivel superior, sin guardia `__main__`. Una importación para reutilizar
las funciones de conteo lanza los controles completos. Sus límites actuales
son acotados y pasaron; no es corrupción de datos, pero dificulta reutilizarlos.

`verify_consistency.py` evita ese efecto leyendo las listas mediante AST;
`verify_strata.py` sí protege su entrada. Sería conveniente encapsular los otros
dos sin unificar sus algoritmos con el laboratorio, para conservar el contraste
independiente. Esta revisión no realiza esa modificación.

### 3. La reproducción de términos altos depende de evidencia del laboratorio

| Sucesión | Datos locales | Recálculo directo ejecutado |
|---|---|---|
| a(n), q=3 | n=1..36 | n=1..20 |
| b(n), q=3 | n=1..35 | Diferencias de a(n); ambos operandos recalculados para n=1..19 |
| a(n), q=5 y q=7 | n=1..22 | n=1..18 |
| e8, e10, e12 | Desde 9, 11 y 13, respectivamente, hasta 29 | Los tres conteos para n=1..20, incluidos ceros iniciales |

Los textos declaran correctamente esos límites. Las listas más largas son
coherentes entre scripts, papers y b-files, pero esta sesión no reconstruye sus
últimos términos. Las extensiones de q=5,7 hasta 29 figuran en la documentación
editorial como aportaciones de Irvine; los b-files locales llegan a 22.
Para una entrega autosuficiente futura convendría enlazar el generador y el
commit de procedencia de cada rango alto. No hace falta repetir esos censos para
empezar P1.

### 4. Detalles menores de reproducción y presentación

No hay versión de Lean fijada mediante `lean-toolchain`; aquí se verificó con
**Lean 4.32.2**. Los programas no necesitan NumPy, por lo que el desbordamiento
detectado en el contador paralelo del laboratorio no se traslada a estos cuatro
verificadores.

El paper 03 aproxima la constante para theta=0.9 como `45.192`; el evaluador
Decimal a 60 dígitos obtiene `45.191013417939...`, que redondea a `45.191`.
Es una errata menor: la cota publicada `46.2` continúa siendo superior.
La evaluación Decimal es un control numérico, no un certificado de intervalos
ni una formalización de las potencias reales.

## Bordes y programas incluidos en los drafts

Los tres programas OEIS recorren `range(2**n-1)`, aunque la definición incluye
también r=2**n−1. Esa omisión no cambia el conteo: para n>=1, la trayectoria
de 2**n−1 tiene n entradas impares y termina en 3**n−1; la de 2**n tiene n
entradas pares y termina en 1. El último residuo nunca es balanceado.
Es el borde ya tratado por el certificado del espejo, no un resultado nuevo.

Se extrajeron sólo las funciones de esos programas y se contrastaron **39
conteos**, tres estratos en n=1..13, con el verificador independiente. También
se comprobó el borde para n=1..100 como contraste finito de la identidad, y el
ejemplo (3067,3068): primer encuentro en 692 tras 18 iteraciones, diez entradas
impares por trayectoria y ocho pasos mixtos. No apareció una discrepancia.

## Validación y situación editorial

- Los cuatro Python y los dos JSON pasan análisis sintáctico.
- Pasan los cuatro verificadores públicos con sus límites predeterminados.
- `mirror_theorem.lean` compila con Lean 4.32.2; sus 17 consultas de axiomas
  muestran sólo `propext`, `Quot.sound` o ausencia de axiomas, sin `sorryAx`.
- Existen los destinos de los 27 enlaces locales encontrados en los Markdown
  fuera del archivo histórico; no se validaron las anclas internas.
- Los siete b-files y los offsets de los tres estratos concuerdan con sus
  verificadores. Los programas de los drafts también pasaron el contraste adicional.

Los resultados capturados están en [evidencia_zootheorem.json](evidencia_zootheorem.json).
No se consultó OEIS en vivo: «publicado» y «proposed» describen el último estado
registrado, el 17-09. Las cuatro correcciones preparadas siguen pendientes según
esa documentación. No se enviaron mensajes, editaron fichas ni hicieron commits
o push durante este análisis.

La ruta conjunta para después de compactar está en
[CONTINUIDAD.md](CONTINUIDAD.md). El próximo trabajo matemático continúa siendo
P1; este análisis no declara resuelto ninguno de P1–P3.
