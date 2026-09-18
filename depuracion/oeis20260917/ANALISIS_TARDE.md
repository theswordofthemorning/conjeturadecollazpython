# Revisión de las siete fichas y respuestas de la tarde — 17-09-2026

## Diagnóstico

Hay problemas de presentación propios y una desincronización entre nuestras
correcciones locales y algunas afirmaciones publicadas. Las intervenciones
de los editores no sustentan la lectura de una refutación de los conteos,
ni permiten concluir que no entienden la matemática. Tampoco hay fundamento
para presentar el intercambio como una competición que estemos ganando.

Irvine pide inteligibilidad y una contribución reconocible; Howroyd señala
terminología local presentada como si el lector ya la conociera; Marcus
pide acceso a la bibliografía. Son tres peticiones diferentes. La tercera
vía del diagnóstico es que un conteo correcto puede estar insuficientemente
presentado y su interés editorial seguir sujeto a juicio. Corregir datos o
demostrar que existen familias no obliga a OEIS a aceptar cada refinamiento.

La respuesta de las 16:35 sí daba la regla de conteo y una motivación
matemática válida, pero seguía siendo larga, empezaba desde nuestro programa
de investigación y dejaba títulos con dos expresiones que el lector debía
descifrar. El comentario ya explicaba operativamente el paso de paridades
opuestas: sería injusto afirmar que no había ninguna definición. La mejora
necesaria era hacerla explícita como convención local, definir también la
clase y poner el conteo directamente en el título. Las búsquedas sin
resultados citadas por Howroyd, por sí solas, no prueban novedad terminológica
ni inexistencia matemática; su observación editorial sigue siendo útil.

## Estado inicial de repositorios y OEIS

Se ejecutó `git fetch origin` y se cotejó `git status -sb` en ambos repositorios.
Ambos estaban en `main`, sincronizados con `origin/main`: laboratorio
`5a0fa32`, zootheorem `152a3ab`. El laboratorio tenía únicamente
`revision12_adv1/` sin seguimiento, conservada íntegramente.
Las notas previas que decían «sin commit/push» describían aquella sesión;
al inicio de esta revisión esos trabajos ya estaban en ambos remotos.

Se leyeron estado, plan, checklist, papers 01–02 y las verificaciones
necesarias. P1–P3 siguen abiertos; la aprobación editorial no certifica
el objetivo phi=1. No se recorrió todo SQLite ni se usaron subagentes.

La búsqueda por autor devuelve cuatro fichas publicadas. El panel del
usuario muestra tres solicitudes adicionales; los dos borradores de reserva
G,H del repositorio no son fichas OEIS enviadas.

| Ficha | Objeto | Datos públicos | Estado al cerrar |
|---|---|---|---|
| A398792 | Encuentros balanceados hasta n, q=3 | n=1..36 | Publicada; aclaraciones preparadas |
| A398793 | Nuevas clases en n+1, q=3 | n=1..35 | Publicada; correcciones preparadas |
| A398794 | Encuentros balanceados hasta n, q=5 | n=1..29 | Publicada; aclaración de ley preparada |
| A398795 | Encuentros balanceados hasta n, q=7 | n=1..29 | Publicada; aclaración de ley preparada |
| A399819 | Primer encuentro en n, ocho desacuerdos | n=9..29, offset 9,2 | proposed, revisión #12 |
| A399820 | Primer encuentro en n, diez desacuerdos | n=11..29, offset 11,2 | proposed, revisión #13 |
| A399821 | Primer encuentro en n, doce desacuerdos | n=13..29, offset 13,2 | proposed, revisión #11 |

Los términos públicos coinciden con todos los términos locales disponibles.
En los mapas q=5,7 el repositorio conserva n<=22; las extensiones públicas
hasta 29 corresponden a Irvine, según los historiales. No se atribuye esa
extensión a nuestro control directo.

## Cronología comprobada

Todas las horas siguientes son **EDT**, como las presenta OEIS.

| Hora del 17-09 | Intervención |
|---|---|
| 00:13–00:14 | Irvine, A399819: dificultad de comprensión y pregunta por la utilidad para Collatz |
| 16:35 | Nuestra respuesta anterior y aclaración de las tres fichas |
| 17:30–17:32 | Marcus, A399820: faltan enlaces; añade Gao; precisa que lo copió de A277109 y extiende la petición a A398792 |
| 18:47–18:49 | Howroyd, A399819: identificar y definir las expresiones locales |
| 20:08 | Nueva nota en A399821 y reenvío |
| 20:10 | Respuesta a Howroyd en A399819 y reenvío |
| 20:11 | Respuesta a Marcus en A399820 y reenvío |

No se observó otra intervención nueva de Irvine después de nuestra
respuesta de las 16:35, ni una objeción nueva en A399821. A399820 había
vuelto a `editing` por la edición de Marcus; no era un rechazo.
Los historiales de agosto muestran que Irvine ya había pedido nombres
autocontenidos y había sustituido lenguaje de clases por conteos directos.
Volver a títulos dependientes de jerga en septiembre repitió ese problema.

## Hallazgos matemáticos y bibliográficos propios

Estos hallazgos resultan de esta revisión; no se atribuyen a las nuevas
observaciones de los editores.

1. **A398792:** algunos comentarios todavía presentan una cota de densidad
   para tiempos finitos iguales sin conservar explícitamente la hipótesis
   de convergencia. Lo incondicional es la cota para la unión de clases de
   encuentros balanceados. Monotonía sólo da `densidad inferior(F)>=phi`.
   El paper ya recogía esta distinción desde el 13-09.
2. **A398793:** la supuesta equivalencia entre razón límite 2 y densidad
   total no está justificada; crecimiento relativo no fija la suma ponderada.
   Además, el cociente final disponible es `a(35)/a(34)`, aproximadamente
   1.9468608. La afirmación de monotonía de todos los cocientes tampoco
   describe los primeros términos.
3. **A398793:** confunde el repunit previo de Conejas con el encuentro.
   El encuentro es `(3^j-1)/4`, no `(3^(j-1)-1)/2`. El caso j=2 da 2 y 1,
   respectivamente. Es una errata concreta en un comentario, no en DATA.
4. **A398794–A398795:** `(1+q)/4` requiere la ley uniforme de clases y un
   próximo paso de igual paridad, condicionado a historia finita. No es
   el promedio de la evolución completa de un par consecutivo, ni una
   afirmación bajo condicionamiento a supervivencia futura.
5. La referencia Barina 2025 combina año/volumen con el título de su
   artículo anterior. El título correcto está en la propuesta enlazada.
   El paper local también tenía una inicial errónea de Amanda Tucker;
   se corrigió. Los metadatos se contrastaron con las fuentes editoriales
   y arXiv. Para Wu–Huang sólo se localizó la referencia comentada por
   Lagarias, entrada 125, y se identifica así.

Los cambios exactos, con enlaces y sustituciones completas, están en
[la propuesta para las cuatro publicadas](../../../zootheorem/drafts/CORRECCIONES_PUBLICADAS_20260917.md).

### Derivación de la errata de Conejas

Se usa `T(x)=x/2` para x par y `(3x+1)/2` para x impar, sobre enteros
no negativos, con j par >=2. Tras j pasos, las dos escaleras dan
`3^(j-1)-1` y `3^j-1`. Tras j+1 pasos dan
`w=(3^(j-1)-1)/2` y `3w+1=(3^j-1)/2`. El primero es impar y el segundo
par. Un paso más lleva ambos a `(3w+1)/2=(3^j-1)/4`.
Las cuentas de entradas impares son j en ambos lados. Como los valores
en j+1 son distintos, determinismo excluye cualquier encuentro anterior.
Para `b(n)=A398792(n+1)-2*A398792(n)`, la consecuencia es `b(j+1)>=1`.

La derivación del primer encuentro es escrita. Lean construye los caminos
y el valor terminal `3t+2`, donde `3^(j-1)=4t+3`; el paso de determinismo
al primer encuentro y el conteo no están ensamblados en ese teorema.

## Respuestas y ediciones efectivamente realizadas

En las tres solicitudes se cambió NAME, COMMENTS y LINKS. Se conservaron
literalmente datos, offset, ejemplos, programas, autor y referencias.
Los títulos cuentan enteros en `0<=r<2^n`, especifican primer encuentro,
igual número de entradas impares y 8/10/12 posiciones de paridad opuesta.
Los comentarios definen las dos expresiones locales y distinguen los
índices de entrada 0..n-1 de los pasos 1..n usados en ejemplos.
Se preservó el enlace de Gao añadido por Marcus; las tres enlazan Gao
y Terras, y A399819 enlaza además Garner y Elia–Tucker.

Respuestas publicadas y comprobadas en las capturas finales:

- [Howroyd](respuesta_howroyd_tarde.txt), [discusión A399819](https://oeis.org/draft/A399819).
- [Marcus](respuesta_marcus_tarde.txt), [discusión A399820](https://oeis.org/draft/A399820).
- [Nota compañera](respuesta_companera_tarde.txt), [discusión A399821](https://oeis.org/draft/A399821).

**Límite externo real:** al abrir la edición de A398792, OEIS impidió
continuar por exceso de ediciones pendientes. La [captura](limite_ediciones_tarde.txt)
conserva el mensaje. No es una negativa de aprobación automática de las
herramientas ni una falta de autorización del usuario. No se retiraron
solicitudes ni se modificaron cuentas para sortearlo. Marcus fue informado.
Las cuatro correcciones públicas siguen pendientes de un cupo; las tres
solicitudes existentes sí quedaron reenviadas y comprobadas como proposed.

## Verificación y mantenimiento

- Directo y simbólico: se ejecutó `verificar_respuesta.py`, n=1..13,
  identidad exacta y telescopado con `Fraction`, testigos y levantamientos.
  Se conserva la procedencia histórica n<=20 y simbólica posterior.
- [Verificación de esta entrega](verificacion_tarde.txt): propuesta frente
  al texto realmente guardado, todos los campos conservados, las tres
  respuestas presentes, estado del panel y datos de las siete fichas.
  El script [verificar_tarde.py](verificar_tarde.py) sincroniza los tres
  drafts locales sólo con `--sincronizar` explícito.
- `lean +leanprover/lean4:v4.32.2 --version`: Lean 4.32.2, commit f3b06c7.
  Se ejecutó `conejas.lean`: `peldano`, `escalera`, `tres_mod4`, `conejas`
  y `separados_antes` usan `propext` y `Quot.sound`; `caso_valores` no usa
  axiomas. Sin `sorryAx`. Cálculo independiente j=2..20 pares.
- Registro versionado a 2026-09-17: filas 36 y 176 precisan el valor previo
  y el terminal; una corrección se añade al final sin desplazar las anteriores.
  `guardarafirmaciones.py` regeneró la base atómicamente. El verificador de
  persistencia pasó: 216 afirmaciones, 52 nodos, 84 dependencias.
- El lector web no pudo abrir las fichas; se usó Chrome autenticado y
  accesibilidad UIA. Las capturas de diffs incluyen texto borrado y añadido:
  para leer el contenido actual usar `A*_vigente_tarde.txt`. UIA devolvió
  algunos valores obsoletos antes de enfocar el campo; el cotejo decisivo
  se hizo con los textos del servidor tras guardar. No interpretar los
  archivos intermedios llamados `formulario_verificado` como un resultado
  exitoso cuando conservan una lectura anterior.

Cambios de esta sesión locales, sin commit ni push a GitHub. No se modificó
`respuestas.db`, ni se reconstruyeron conversaciones. Siguiente acción
editorial: atender la próxima observación y enviar las cuatro correcciones
cuando OEIS permita otra edición. Siguiente acción matemática: P1.

Después de esta entrega, el usuario solicitó commit y push de ambos
repositorios y documentar el reenvío. Se añadió el
[procedimiento operativo](../../../zootheorem/drafts/PROCEDIMIENTO_OEIS.md)
para el cierre; la declaración anterior de cambios locales describe el
momento de entrega del análisis.
