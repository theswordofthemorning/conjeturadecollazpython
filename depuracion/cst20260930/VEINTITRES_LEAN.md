# Ocelotas: 23 rachas aceptadas en Lean bajo LMN

Comprobación terminada el **03-10-2026 a las 23:59:59**, hora local.
Fuentes, objetos y consultas finales cotejados el 04-10-2026.
La sesión 27647 terminó con código 0; ya no está en ejecución.

## Resultado y alcance

Mapa atajo: `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, `n>=2`.
`S_j(n)` cuenta las entradas impares entre los primeros j pasos.
El primer cruce finito k cumple `3^S_j>=2^j` para `1<=j<k` y
`3^S_k<2^k`. Las rachas son los bloques maximales de entradas impares.

Bajo `LMN23`, el corolario de Laurent–Mignotte–Nesterenko especializado
en 2 y 3, si hay **como máximo 23 rachas hasta k**, entonces

```text
n <= T^j(n) para todo j<k,
T^k(n) < n.
```

[OcelotasVeintitres.lean](OcelotasVeintitres.lean) contiene
`cst_veintitres_corolario`, su versión desde `LMNDebil` y
`fallo_exige_veinticuatro`: bajo LMN, un fallo en un primer cruce
finito necesita **al menos 24 rachas**.

Esta vía no usa Rozier–Terracol. Se mantiene el certificado interno
para `n<=4912740`. LMN es una hipótesis matemática externa explícita;
su traducción a la forma débil ya está formalizada. No se demuestra
existencia universal del primer cruce ni llegada universal a 1.
Revisión humana y prioridad histórica pendientes.

## Ensamblaje aceptado

La [preparación y sus cotejos](VEINTITRES_PROPUESTA.md) conservan el
desarrollo previo y los intentos finitos. La tabla tiene 43 intervalos
para `q<19362882631`: 35 remiten al certificado interno, seis se
descartan por criba y dos por ventanas de prefijos. Cola paramétrica:
`R=23`, `A=82528`, `c=5`, `H=34`.

| Ventana inclusiva | q mínimo | Nodos | Hojas no vacías | Partes Lean |
|---|---:|---:|---:|---:|
| 4912741..6276058 | 79335 | 528949 | 39815 | 28 |
| 4912741..356547672 | 190537 | 12368501 | 2189377 | 62 |

Las ventanas se solapan y usan combustible 128. La baja cubre
1363318 semillas; la alta, 351634932, con profundidad máxima 60.
Los subárboles y sus uniones se verifican con el núcleo de Lean;
el agotamiento de combustible rechaza.

Contrastes independientes conservados:

- [Tabla y cola](cotejo_veintitres_lean.json), mediante series racionales
  de atanh, potencias enteras y `Fraction`.
- [Ventana baja](cotejo_prefijos_23_bajo.json) y
  [ventana alta](cotejo_prefijos_23_alto.json), por órbitas directas,
  cotas y cobertura disjunta.

Las salidas de preparación pueden decir que Lean estaba pendiente:
registran el momento anterior al cierre y se conservan literalmente.

## Auditoría final

[Evidencia JSON](evidencia_veintitres_lean.json) y
[registro de ejecución](evidencia_veintitres_lean.txt):

- Lean 4.32.2, commit `f3b06c705e6c85f5314019d5d3baab0fec5b580c`.
- **105 módulos de extensión: 69 compilados y 36 reutilizados.**
- **11806 consultas:** 11797 listas con `propext`, `Classical.choice`
  y `Quot.sound`; cinco con `propext` y `Quot.sound`; cuatro con `propext`.
  Ninguna usa `sorryAx`.
- 38 módulos de base reutilizados por huellas, con 156 consultas
  cotejadas además de las anteriores.
- Duración de esta ejecución persistente: **11834,236 segundos**, unas
  3 h 17 min. Incluye reutilización de avances anteriores; no es una
  reconstrucción desde cero ni un indicador comparable de rendimiento.

El 04-10 se cotejaron las huellas actuales de todas las fuentes y objetos
de ambos grupos, las de los dos auditores, el número de consultas por
fuente y los axiomas de cada respuesta. El JSON final tiene SHA-256
`ece5b16a27b4edd95e1171908bb3e55d38499ed4c0f5643c1e947aabd26b62c9`.
Las consultas incluyen muchas piezas de certificados; no equivalen a
11806 afirmaciones científicas independientes.

## Continuación

Quedan 23 rachas certificadas bajo LMN y
[77 bajo LMN y Rozier–Terracol](SETENTA_Y_SIETE_LEAN.md).
No se inicia automáticamente una extensión a 24. La siguiente dirección
acordada es estudiar argumentos generales y las restricciones que tendría
una trayectoria que evitase el primer cruce indefinidamente.

Reproducción de la auditoría, con las cachés verificadas existentes:

```powershell
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasVeintitres --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_veintitres_20261003 --salida depuracion/cst20260930/evidencia_veintitres_lean.json
```
