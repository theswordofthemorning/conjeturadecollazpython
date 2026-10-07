# Estado para continuar — 07-10-2026

[Premisa del usuario](PREMISA_DE_INVESTIGACION.md): interpreta los resultados
acumulados como evidencia de que Collatz es verdadero y busca cerrar la
prueba universal. Esta conclusión de trabajo orienta la búsqueda, sin
servir como hipótesis de prueba.

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal; de ella la de Garner (1985) sobre rachas y la conjetura 2 de Wu
(1992). CST: Ocelotas hasta veinticuatro rachas contadas directamente,
en Lean sin Rhin, bajo Laurent–Mignotte–Nesterenko.**

- **Gao, forma de Lagarias.** `GaoEnunciado.conjetura_gao`
  ([Tejonas](depuracion/gao20260920/Tejonas.md)): con el mapa clásico, los n
  con `f^k(n)=f^k(n+1)` para algún `k<=log2 n` tienen densidad natural 1.
- **Gao (1993).** `GaoLiteral.conjetura_gao_literal`
  ([Hienas](depuracion/gao20260920/Hienas.md)): `d̄_k -> 1` con su coalescencia
  exigente, y además `d(x) -> 1`.
- **Garner (1985).** `GarnerEnunciado.conjetura_garner`
  ([Alpacas](depuracion/garner20260926/Alpacas.md)): L+1 consecutivos, tan
  grandes como se quiera, con igual altura e igual tiempo total de parada.
- **Wu (1992).** `WuEnunciado` ([Condoras](depuracion/gao20260920/formal/Condoras.lean)):
  `lim L=∞`. La conjetura 1 equivale, dado Gao, a que casi todo n llegue a 1:
  sigue abierta. Citas leídas con la IA de CNKI; falta cotejar el original.
- **Ocelotas.** [Veinticuatro rachas en Lean](depuracion/cst20260930/VEINTICUATRO_LEAN.md):
  `cst_veinticuatro_corolario` prueba primer descenso = primer cruce, supuesto
  existente y finito, bajo el
  corolario especializado de Laurent–Mignotte–Nesterenko (1995), con caso
  par incluido. Tabla, semillas pequeñas, prefijos y cola certificadas.
  Original cotejado y `LMN23 -> LMNDebil` en Lean
  ([lecturas](depuracion/cst20260930/LECTURAS_20261003.md)). La
  criba por prefijos exige **al menos 25 rachas** para un fallo, en Lean.
  El [cierre de 77](depuracion/cst20260930/SETENTA_Y_SIETE_LEAN.md) también está
  formalizado: exige **78 con LMN y Rozier–Terracol** como hipótesis externas.

Sólo axiomas estándar en los módulos Lean. **Revisión humana pendiente.**
Salvo en las rachas construidas, nada afirma la llegada a 1.

Cadena y alcance de Gao: [Tejonas](depuracion/gao20260920/Tejonas.md).
Ritmo muy lento: [Cigarras](depuracion/gao20260924/Cigarras.md).

## Revisión y publicación

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y
Wu. Lean certifica el enunciado, no su interpretación. La
[revisión del 27-09](papers/revision20260927/REVISION.md#4-novedad) no halló
pruebas publicadas; faltan MathSciNet, Scholar y el original de Garner.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos.** [Tres `.tex`](papers/README.md), [Zenodo](papers/zenodo/LEEME.md).
  AFM rechazó los tres el 28-09 ([correos](papers/CORREOS_20261004.md)):
  II y III quedan libres. I en revisión técnica de
  [JAR](papers/jar/LEEME.md), sin noticias al 04-10. Borrador del
  [IV, Ocelotas](papers/articulo_IV_ocelotas.tex), sin enviar.
  [Qeios](papers/qeios/LEEME.md): retiro confirmado.
  [Palomar](papers/palomar/LEEME.md): Gao en verificación, Lean
  v4.35.0-rc2 y CI verde. [Zulip](papers/qeios/ZULIP_borrador.md): la
  moderación borró el anuncio por estar escrito con IA.
- **OEIS.** Aprobadas [A078441](depuracion/oeis20260917/A078441_20260930_aprobada.txt)
  (30-09) y [A400486](depuracion/oeis20260917/A400486_20261004_aprobada.txt)
  (04-10; Irvine añadió a(29)–a(30)); no validan pruebas. A400487 sigue
  pendiente, con `more`. Si se rechaza, retirar su referencia en A078441:
  [seguimiento](papers/oeis/RESPUESTA_20260928.md).

## Ruta vigente y próximo bloque

[Plan por sesiones](depuracion/transversal20260927/PLAN_SESIONES_20260928.md):
presupuestos de exploración, no plazos.

- [Nashida](depuracion/nashida20260928/LEEME.md): puente condicional de
  barrera para Wu 1.
- [Pandas](depuracion/pandas20260930/LEEME.md), en Lean: sí a la pregunta
  de Gao con `Res < 4` y para casi todo n. Marmotas: un contraejemplo
  necesita más de `2^21` pasos `3n+1` sobre `2^20`.
- [Wirsching](depuracion/wirsching20260930/LEEME.md), cerrado: la versión
  útil de la condición por residuos equivale a un teorema local límite.
- [CST](depuracion/cst20260930/LEEME.md): Ocelotas, arriba.

Ruta B, elegida por el usuario el 04-10
([plano de la casa](depuracion/casa20261004/LEEME.md)), sin fuerza
bruta: no se amplía a 25 rachas. En Lean, sin hipótesis externas:
Collatz equivale a los dos muros, y el retrato del fugitivo tiene ocho
rasgos. La
[segunda ronda de choques](depuracion/casa20261004/LEEME.md#paso-3-segunda-ronda-el-planeador)
(07-10) halló el primer choque, sólo contra una subespecie: ningún
fugitivo tiene el pronóstico acotado; además, ninguna órbita vuela en
franja. Quedan el cohete y el planeador intermitente, fuera del alcance
de todo conteo. El
[retrato de la grieta](depuracion/casa20261004/LEEME.md#el-retrato-de-la-grieta)
(07-10), el intruso del muro A, le dio a ese muro su tramo de «casi todo
número» (Terras, Everett) y el teorema E de Lagarias con constante
escrita bajo LMN, sin choque. Ventanas, también en Lean: el teorema de
Korec completo (casi toda órbita baja por debajo de `n^θ`, para todo
`θ > log 3/log 4`), CST para casi todo número, la rareza `x^0,95` de
Lagarias y los teoremas A, B y C de Terras. El censo hasta `2^23` se
conserva.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; reconstrucción del 26-09 y
`leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Cada ficha enlaza sus contrastes independientes y certificados;
los cálculos finitos no sustituyen las pruebas universales.

Registro: 278 afirmaciones: 173 demostradas, 86 medidas, 12 conjeturadas
y siete refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar
históricos. zootheorem permanece intacto.

Sesión local del 05-10 [recuperada el 07-10](depuracion/casa20261005_recuperada/RECUPERACION.md):
Corzas, Chinchillas y Perdices, incluida la cadena módulo `3^m`, se conservan
como implementación independiente. GitHub mantiene prioridad; catálogo
activo sin cambios. Huellas históricas verificadas y contraste de la cadena
repetido; falta conciliar las altas locales con el catálogo vigente.
