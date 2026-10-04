# Ocelotas: 24 rachas aceptadas en Lean bajo LMN

Comprobación terminada el **04-10-2026 a las 20:15:31**, hora local.
Huellas, consultas y axiomas cotejados por separado el mismo día. La pidió
el usuario: «puedes ejecutar la racha n24 en segundo plano sin agentes?».

## Resultado y alcance

Mapa atajo: `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, `n>=2`.
`S_j(n)` cuenta las entradas impares entre los primeros j pasos.
El primer cruce finito k cumple `3^S_j>=2^j` para `1<=j<k` y
`3^S_k<2^k`. Las rachas son los bloques maximales de entradas impares.

Bajo `LMN23`, el corolario de Laurent–Mignotte–Nesterenko especializado
en 2 y 3, si hay **como máximo 24 rachas hasta k**, entonces

```text
n <= T^j(n) para todo j<k,
T^k(n) < n.
```

[OcelotasVeinticuatro.lean](OcelotasVeinticuatro.lean) contiene
`cst_veinticuatro_corolario`, su versión desde `LMNDebil` y
`fallo_exige_veinticinco`: bajo LMN, un fallo en un primer cruce finito
necesita **al menos 25 rachas**. El módulo es el de 23 con los parámetros
nuevos: número de rachas, umbral de la tabla y cola.

Esta vía no usa Rozier–Terracol. Se mantiene el certificado interno
para `n<=4912740`. LMN es una hipótesis matemática externa explícita;
su traducción a la forma débil ya está formalizada. No se demuestra
existencia universal del primer cruce ni llegada universal a 1.
Revisión humana y prioridad histórica pendientes.

## Ensamblaje aceptado

La tabla tiene 43 intervalos para `q<39123338641`: 35 remiten al
certificado interno, seis se descartan por criba y dos por ventanas de
prefijos ([preparación](preparacion_veinticuatro_lean.json)). Cola
paramétrica: `R=24`, `A=132046`, `c=5`, `H=35`.

| Ventana inclusiva | q mínimo | Nodos | Hojas no vacías | Semillas | Profundidad | Partes Lean |
|---|---:|---:|---:|---:|---:|---:|
| 4912741..6548930 | 79335 | 756925 | 47048 | 1636190 | 62 | 39 |
| 4912741..372049745 | 190537 | 29403783 | 3939127 | 367137005 | 65 | 596 |

Las ventanas se solapan; usan combustible 128 y la criba afinada, sin
nodos pendientes ni ramas con exceso de rachas. Los certificados se
reparten en subárboles de hasta 2000 nodos: 664 en la baja y 25275 en la
alta, unidos por 663 y 25274 uniones en los módulos principales. Cada
parte reúne hasta 20000 nodos en la baja y 50000 en la alta. El núcleo de
Lean verifica subárboles y uniones; el agotamiento de combustible rechaza.

Contrastes independientes conservados, todos sin discrepancias:

- Tabla y cola: [sin ventanas](cotejo_tabla_veinticuatro_lean.json) y
  [con ellas](cotejo_veinticuatro_lean.json), mediante series racionales
  de atanh, potencias enteras y `Fraction`.
- [Ventana baja](cotejo_prefijos_24_bajo.json) y
  [ventana alta](cotejo_prefijos_24_alto.json), por órbitas directas,
  cotas y cobertura disjunta.
- Generación: [baja](generacion_OcelotasVeinticuatroPrefijosBajo.json) y
  [alta](generacion_OcelotasVeinticuatroPrefijosAlto.json) guardan la
  huella de cada parte, y las 635 coinciden con las fuentes compiladas.

## Cómo se ejecutó

- `preparar_`, `cotejar_` y `generar_veinticuatro_lean.py` se derivaron de
  los de 23 con sustituciones exactas, cada una con su número de
  apariciones comprobado. Las partes por prefijos salen del generador ya
  usado en 23, `generar_testigos_prefijos_lean.py`.
- [comprobar_extension_paralela.py](comprobar_extension_paralela.py) es
  una copia de `comprobar_extension_persistente.py` con las mismas
  comprobaciones. Sólo cambia el reparto: compila a la vez hasta
  `--trabajos` módulos con sus dependencias listas, con prioridad baja, y
  sólo el proceso principal escribe el manifiesto.
- Validación del reparto: sobre la ventana baja (46 módulos y 688
  consultas), la versión secuencial y la paralela dieron en cada módulo la
  misma fuente, el mismo objeto, las mismas dependencias y la misma
  auditoría literal. Antes, un piloto fuera del repositorio compiló la
  tabla y el ensamblaje contra ventanas sustitutas con `sorry`, sólo para
  detectar errores; no es evidencia.
- Partes altas de 50000 nodos: con 200000, cada pieza pedía unos 6 GB y
  sólo cabía una a la vez; con 50000, cada proceso de Lean usó unos 2,9 GB.
- Cronología del 04-10: generación y cotejos de 15:28 a 16:26; cadena
  lanzada a las 16:42 con cinco trabajos. A las 17:12 Claude Code la cortó
  al vigilar la memoria libre de sus tareas en segundo plano; Lean no
  había fallado. Quedaron guardados y auditados 177 módulos: 46 de la
  prueba de la ventana baja y 131 de ese intento (las partes altas 1–130
  y `OcelotasLogaritmosPrecisos`). El usuario la relanzó a las 18:02 en su
  propia ventana, con cuatro trabajos. Esa ejecución reutilizó los 177 por
  huellas y compiló los 473 restantes.

## Auditoría final

[Evidencia JSON](evidencia_veinticuatro_lean.json) y
[registro de ejecución](evidencia_veinticuatro_lean.txt). El comprobador
escribe el JSON sólo cuando pasan todas sus aserciones.

- Lean 4.32.2, commit `f3b06c705e6c85f5314019d5d3baab0fec5b580c`.
- **650 módulos de extensión: 473 compilados y 177 reutilizados.**
- **26022 consultas:** 26013 listas con `propext`, `Classical.choice`
  y `Quot.sound`; cinco con `propext` y `Quot.sound`; cuatro con `propext`.
  Ninguna usa `sorryAx`.
- 38 módulos de base comprobados por huellas, 20 de ellos dentro del
  cierre de importaciones, con 156 consultas cotejadas además de las
  anteriores.
- Última ejecución: **7992,84 segundos**, unas 2 h 13 min. Los tiempos de
  compilación de los 650 módulos suman 40766 segundos (11,3 h de proceso),
  con varias compilaciones simultáneas; no es una medida de rendimiento.
  Los objetos ocupan 11,1 GiB en la caché temporal.

[cotejar_evidencia_veinticuatro.py](cotejar_evidencia_veinticuatro.py)
no usa el código del comprobador
([salida](cotejo_evidencia_veinticuatro.txt)). Rehace las huellas de las
650 fuentes y objetos y de los 38 de base, más las de los dos
comprobadores. Cuenta el cierre de importaciones (670 módulos) y las
dependencias directas de cada módulo. En cada fuente cuenta las consultas,
comprueba los nombres consultados y los axiomas de cada respuesta, y busca
palabras prohibidas: sin fallos. El JSON final tiene SHA-256
`f349f71280aa6ab480347007d8245e0dd3da97a99401efb7b2c2e91f985a0839`.
Las huellas son de esta copia de trabajo de Windows: las partes generadas
y los JSON tienen fin de línea CRLF, y un clon con LF da otras huellas.
Las consultas incluyen muchas piezas de certificados; no equivalen a 26022
afirmaciones científicas independientes.

## Coste frente a las rachas anteriores

| Rachas | Nodos de la ventana alta | Factor | Profundidad |
|---:|---:|---:|---:|
| 19 | 4047 | | 38 |
| 20 | 67649 | ×16,7 | 46 |
| 21 | 670749 | ×9,9 | 51 |
| 22 | 3840535 | ×5,7 | 57 |
| 23 | 12368501 | ×3,2 | 60 |
| 24 | 29403783 | ×2,4 | 65 |

Las cifras de 19 a 22 son de la criba entera; las de 23 y 24, de la
afinada, algo más fuerte. Frente a 23 hubo 2,2 veces más consultas y 3,1
veces más tiempo de compilación (de 3,6 h a 11,3 h). Parte del aumento
viene de dividir en más piezas: cada módulo, por pequeño que sea, tarda
unos 17 segundos en cargar su entorno.

## Continuación

Quedan 24 rachas certificadas bajo LMN y
[77 bajo LMN y Rozier–Terracol](SETENTA_Y_SIETE_LEAN.md). No se inicia
automáticamente una extensión a 25. Extrapolando el factor, pediría unos
60–70 millones de nodos en la ventana alta y entre 20 y 26 h de proceso
de Lean; es una estimación, no una medida. La siguiente dirección acordada
sigue siendo estudiar argumentos generales y las restricciones que tendría
una trayectoria que evitase el primer cruce indefinidamente.

Reproducción, desde la raíz del repositorio:

```powershell
python -B -X utf8 depuracion/cst20260930/preparar_veinticuatro_lean.py --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/preparacion_veinticuatro_lean.json
python -B -X utf8 depuracion/cst20260930/cotejar_veinticuatro_lean.py --certificado depuracion/cst20260930/preparacion_veinticuatro_lean.json --salida depuracion/cst20260930/cotejo_tabla_veinticuatro_lean.json
python -B -X utf8 depuracion/cst20260930/explorar_prefijos_racionales.py --inicio 4912741 --limite 6548930 --q-min 79335 --rachas 24 --combustible 128 --criba afinada --max-nodos 16000000 --salida depuracion/cst20260930/prefijos_24_bajo_16m.json
python -B -X utf8 depuracion/cst20260930/explorar_prefijos_racionales.py --inicio 4912741 --limite 372049745 --q-min 190537 --rachas 24 --combustible 128 --criba afinada --max-nodos 256000000 --salida depuracion/cst20260930/prefijos_24_alto_256m.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos_afinados.py --certificados depuracion/cst20260930/prefijos_24_bajo_16m.json --salida depuracion/cst20260930/cotejo_prefijos_24_bajo.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos_afinados.py --certificados depuracion/cst20260930/prefijos_24_alto_256m.json --salida depuracion/cst20260930/cotejo_prefijos_24_alto.json
python -B -X utf8 depuracion/cst20260930/cotejar_veinticuatro_lean.py --certificado depuracion/cst20260930/preparacion_veinticuatro_lean.json --prefijos depuracion/cst20260930/prefijos_24_bajo_16m.json depuracion/cst20260930/prefijos_24_alto_256m.json --cotejos-prefijos depuracion/cst20260930/cotejo_prefijos_24_bajo.json depuracion/cst20260930/cotejo_prefijos_24_alto.json --salida depuracion/cst20260930/cotejo_veinticuatro_lean.json
python -B -X utf8 depuracion/cst20260930/generar_veinticuatro_lean.py --certificado depuracion/cst20260930/preparacion_veinticuatro_lean.json --salida depuracion/cst20260930/OcelotasVeinticuatroTabla.lean --filas-por-modulo 15
python -B -X utf8 depuracion/cst20260930/generar_testigos_prefijos_lean.py --certificado depuracion/cst20260930/prefijos_24_bajo_16m.json --cotejo depuracion/cst20260930/cotejo_prefijos_24_bajo.json --espacio OcelotasVeinticuatroPrefijosBajo --directorio depuracion/cst20260930 --nodos-subarbol 2000 --nodos-modulo 20000
python -B -X utf8 depuracion/cst20260930/generar_testigos_prefijos_lean.py --certificado depuracion/cst20260930/prefijos_24_alto_256m.json --cotejo depuracion/cst20260930/cotejo_prefijos_24_alto.json --espacio OcelotasVeinticuatroPrefijosAlto --directorio depuracion/cst20260930 --nodos-subarbol 2000 --nodos-modulo 50000
python -B -X utf8 depuracion/cst20260930/comprobar_extension_paralela.py --modulo OcelotasVeinticuatro --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_veinticuatro_paralelo_20261004 --trabajos 4 --salida depuracion/cst20260930/evidencia_veinticuatro_lean.json
python -B -X utf8 depuracion/cst20260930/cotejar_evidencia_veinticuatro.py --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_veinticuatro_paralelo_20261004 > depuracion/cst20260930/cotejo_evidencia_veinticuatro.txt
```

Con las cachés ya verificadas, el comprobador reutiliza todo lo guardado.
Desde cero, pide varias horas y unos 3 GB de memoria por trabajo.
