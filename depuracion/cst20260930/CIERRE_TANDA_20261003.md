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

## Comprobación que sigue en ejecución

[23 sin Rozier–Terracol](VEINTITRES_PROPUESTA.md) sigue pendiente de
la cadena Lean completa. La ventana baja y el cotejo independiente
de ambas ventanas están completos. La
[foto del avance al cierre](avance_veintitres_cierre_20261003.json)
registra las partes altas aceptadas; no acredita el resultado final.

La sesión 27647 continúa. Su salida `.txt`, todavía cambiante, queda
fuera del commit de cierre. No iniciar otra ejecución sobre su caché.
Siguiente acción: recoger la terminación, verificar huellas y axiomas,
y sólo entonces decidir si corresponde registrar el cierre de 23.
