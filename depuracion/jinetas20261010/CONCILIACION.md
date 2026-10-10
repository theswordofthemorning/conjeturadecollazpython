# Conciliación de la base utilizada el 10-10-2026

Bloque 0 de la [ruta](../casa20261004/RUTA_20261010.md). Comparación de
claves, enunciados y huellas; no es recompilación de las fuentes históricas.
Las altas nuevas de Jinetas se registran aparte de esta conciliación.

## Registros anteriores

Se comparó el [registro recuperado](../casa20261005_recuperada/sesion_original/depuracion/coherencia20260913/registro.json)
con el [registro activo](../coherencia20260913/registro.json) **antes**
de añadir Jinetas: base común de 208 filas; 72 altas recuperadas y 75
locales actuales, es decir 280 y 283 afirmaciones. De las 63 claves
compartidas, 62 coinciden literalmente en todos sus campos. En
`casa_plano_collatz_dos_muros_lean` sólo cambian las notas: la versión
activa incorpora las certificaciones posteriores. Se conserva ésta.

Las nueve claves exclusivas recuperadas se compararon por enunciado:

| Clave recuperada | Relación con el catálogo activo y decisión |
|---|---|
| `corzas_retrato_fugitivo_lean` | Solapa con `casa_retrato_fugitivo_lean`; las cotas y cláusulas no son idénticas. Mantener la implementación recuperada como testigo independiente. |
| `corzas_choques_periodicidad_lean` | Solapa con el tablero y el retrato; el alcance de periodicidad no se identifica automáticamente. |
| `corzas_grieta_domino_lean` | Solapa con `casa_grieta_retrato_lean` y el tablero; conserva otra cota y presentación del dominó. |
| `corzas_terras_densidad_lean` | Solapa con Terras y Korec vigentes; error cuantitativo y constante de Chernoff distintos. |
| `chinchillas_korec_lean` | El Korec vigente contiene también la formulación real; mantener separados los objetos de ambas implementaciones. |
| `chinchillas_potencia_lean` | Comparte el exponente 0,95 del fugitivo con Korec vigente; las cotas 31/32 para otros conjuntos requieren una ficha separada si se integran. |
| `chinchillas_lmn_potencia_lean` | Hipótesis `LMNEntera`, umbral `2^125000` y conteos propios; no sustituir por la grieta bajo `LMN23`. |
| `perdices_tres_adico_lean` | Identidad afín y fibras recuperadas; el acoplamiento vigente tiene otro enunciado y usa el puente de CasaCadena. |
| `perdices_mezcla_medida` | Medición en flotantes hasta m=14; no convertir en teorema ni confundir con la refutación posterior de una cota condicionada. |

Ninguna de estas nueve claves se necesita para el ensayo de Jinetas.
La conciliación identifica solapamientos y diferencias; **no crea nueve
altas por simple suma**. Queda pendiente decidir e integrar las fichas
que merezcan entrada independiente, sin cambiar los IDs históricos.
Los archivos de la sesión recuperada permanecen intactos.

Las doce claves exclusivas activas corresponden a las siete de la casa
vigente (retrato, tablero, planeador, grieta, ventana, Korec y Terras),
las cuatro extensiones de Perdices (acoplamiento, umbral, tamaño y sexta)
y Mahler. Sexta y Mahler ya estaban sin commit; esta sesión no publica
esas dos altas ni sus cambios anteriores de fichas.

## Procedencia de las huellas de Perdices

Frente a las fuentes de trabajo, el manifiesto versionado
[evidencia_tamano.json](../perdices20261007/evidencia_tamano.json) tiene
una coincidencia binaria y once discrepancias. Su clasificación exacta:

- Siete fuentes coinciden al normalizar CRLF a LF: Ocelotas,
  OcelotasRachas, OcelotasTrayectorias, OcelotasFinito, OcelotasCriba,
  OcelotasCierre y OcelotasContador.
- CasaPlano y CasaRetrato coinciden al usar CRLF.
- OcelotasCertificado ya coincide byte por byte.
- PerdicesEstela y PerdicesTamano no coinciden con ninguna de esas
  conversiones; no atribuir sus diferencias sólo a finales de línea.

El manifiesto local `depuracion/perdices20261007/evidencia_sexta.json`
coincide byte por byte con las 13 fuentes que enumera. Registra para
los doce módulos comunes los mismos hashes de objeto que el manifiesto
anterior. Ésta es una comparación entre registros: no se han regenerado
ni comprobado esos objetos en esta sesión. No se reutiliza ninguna de
esas cachés para certificar Jinetas, que importa sólo Mathlib.

La formalización local de sexta raíz sigue separada de lo versionado.
Su integración requiere revisar la diferencia restante de las dos
fuentes y la evidencia de construcción; el nuevo ensayo no depende de
ella y no la declara recertificada.

## Conservación y reproducción de las altas nuevas

Se respaldaron los 18 archivos locales previos antes de editar. Los
cambios nuevos se separan al preparar el commit, incluso en estado,
registro y SQLite. El generador acepta ahora `--registro` y `--salida`
para contrastar una instantánea sin reemplazar la base de trabajo.

La nueva fuente versionada añade `jinetas_algebra_intercambio` y
`jinetas_monotonia_refutada`. Las altas antiguas mantienen su orden:
Jinetas ocupa 282–283 en la instantánea publicada y 284–285 en el
registro local que ya contiene sexta y Mahler. Las claves son la
identidad estable; esos números no se usan para enlazar fichas.

Validación de persistencia: reconstrucción desde el registro, comparación
literal de filas y claves, integridad SQLite y controles acotados de
`verificar_registro.py`. No se ejecuta el conjunto general de experimentos.
