# Cierre de tanda de Ocelotas — 03-10-2026

## Resultados aceptados

Desde el commit `98a322b` se incorporaron ocho afirmaciones al registro:
región finita para cualquier límite fijo de rachas, cola paramétrica,
criba afinada tras un corte, cierres de 76 y 22, descuento por racha,
criba con suelo y cierre de 77. Las hipótesis se conservan en cada ficha.

- [22 rachas](VEINTIDOS_LEAN.md): cierre Lean bajo LMN, con el
  certificado interno de semillas pequeñas; no usa Rozier–Terracol.
- [77 rachas](SETENTA_Y_SIETE_LEAN.md): cierre Lean bajo LMN y el
  resultado finito externo de Rozier–Terracol. Un fallo, supuesto
  un primer cruce finito, exige al menos 78 rachas. La sesión 64800
  terminó con código 0: 91 módulos de extensión y 5030 consultas
  estándar, sin `sorryAx`; fuentes y objetos cotejados después.
- [Descuento por racha](DESCUENTO_RACHAS_LEAN.md): mejora universal de
  la cota auxiliar, verificador formal y piloto de 76 aceptados.
- [Cota con suelo](SUELO_RACHAS_LEAN.md): conserva información sobre
  los valores intermedios. Prueba universal y especialización entera
  aceptadas; faltan el puente tras cortes y su verificador de árboles.

En palabras sencillas, se estrechó el conjunto de recorridos que
podrían fallar en CST. No se demuestra que todos los números lleguen
a 1 ni que todos tengan primer cruce finito. Tampoco se establece una
mejora del teorema de Tao. Revisión humana y prioridad histórica pendientes.

## Registro y controles

268 afirmaciones: **163 demostradas**, **86 medidas**, **12 conjeturadas**
y **7 refutadas**. Las demostradas incluyen resultados condicionales;
el total no cuenta sólo teoremas nuevos independientes.

Se actualizó la fuente versionada, se regeneró `afirmaciones.db` y
pasaron los controles de catálogo, integridad, atomicidad y captura
literal. Los cotejos matemáticos independientes están enlazados en
cada ficha. Se preservan intentos fallidos y evidencia histórica.

## Estado de la comprobación al cerrar esa tanda

[23 sin Rozier–Terracol](VEINTITRES_PROPUESTA.md) quedó pendiente de
la cadena Lean completa. La ventana baja y el cotejo independiente
de ambas ventanas estaban completos. La
[foto del avance al cierre](avance_veintitres_cierre_20261003.json)
registra las partes altas aceptadas; no acredita el resultado final.

La sesión 27647 se dejó activa. Su salida `.txt`, todavía cambiante,
quedó fuera de aquel commit. Se acordó recoger la terminación y verificar
huellas y axiomas antes de registrar el resultado.

## Actualización del 04-10-2026

La cadena terminó el 03-10 a las **23:59:59**, con código 0:
[23 rachas aceptadas bajo LMN](VEINTITRES_LEAN.md), 105 módulos de
extensión y 11806 consultas sin `sorryAx`. Fuentes, objetos y auditores
cotejados después. Registro actual: **269 afirmaciones, 164 demostradas**.
También quedó aceptada la [conexión del suelo tras cortes](SUELO_CORTES_LEAN.md),
con verificador y piloto. Las cifras anteriores conservan el estado
del primer cierre; no se inicia una extensión automática a 24.
