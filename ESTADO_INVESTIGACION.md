# Estado para continuar — 03-10-2026

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal; de ella la de Garner (1985) sobre rachas y la conjetura 2 de Wu
(1992). CST: Ocelotas hasta veintidós rachas contadas directamente,
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
- **Ocelotas.** [Veintidós rachas en Lean](depuracion/cst20260930/VEINTIDOS_LEAN.md):
  `cst_veintidos_corolario` prueba primer descenso = primer cruce, supuesto
  existente y finito, bajo el
  corolario especializado de Laurent–Mignotte–Nesterenko (1995), con caso
  par incluido. Tabla, semillas pequeñas, prefijos y cola certificadas.
  Original cotejado y `LMN23 -> LMNDebil` en Lean
  ([lecturas](depuracion/cst20260930/LECTURAS_20261003.md)). La
  criba por prefijos exige **al menos 23 rachas** para un fallo, en Lean.
  El [cierre de 77](depuracion/cst20260930/SETENTA_Y_SIETE_LEAN.md) también está
  formalizado: exige **78 con LMN y Rozier–Terracol** como hipótesis externas.

Sólo axiomas estándar en los módulos Lean. **Revisión humana pendiente.**
Salvo en las rachas construidas, nada afirma la llegada a 1.

Cadena de Gao, expuesta en el artículo I:
[Lagartijas](depuracion/gao20260920/Lagartijas.md) →
[Martas](depuracion/gao20260920/Martas.md) → Tejonas → Hienas → Alpacas →
Condoras. Ritmo pésimo: [Cigarras](depuracion/gao20260924/Cigarras.md).

## Revisión y publicación

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y
Wu. Lean certifica el enunciado, no su interpretación. La
[revisión del 27-09](papers/revision20260927/REVISION.md#4-novedad) no halló
pruebas publicadas; faltan MathSciNet, Scholar y el original de Garner.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos.** [Tres `.tex`](papers/README.md), [Zenodo](papers/zenodo/LEEME.md).
  AFM rechazó I; II/III siguen allí. I en revisión técnica de
  [JAR](papers/jar/LEEME.md). [Qeios](papers/qeios/LEEME.md): retiro
  solicitado. [Palomar](papers/palomar/LEEME.md): Gao en verificación,
  Lean v4.35.0-rc2 y CI verde. [Zulip](papers/qeios/ZULIP_borrador.md)
  publicado; responder sólo con autorización.
- **OEIS.** [A078441 aprobada](depuracion/oeis20260917/A078441_20260930_aprobada.txt);
  no valida pruebas. [A400486/A400487](depuracion/oeis20260917/A400486_A400487_20260930_publico.txt)
  siguen pendientes; `more` añadido a A400487. Si se rechaza, retirar
  su referencia en A078441: [seguimiento](papers/oeis/RESPUESTA_20260928.md).

## Ruta vigente y próximo bloque

[Plan por sesiones](depuracion/transversal20260927/PLAN_SESIONES_20260928.md):
presupuestos de exploración, no plazos.

- [Nashida](depuracion/nashida20260928/LEEME.md): puente condicional de
  barrera para Wu 1.
- [Pandas](depuracion/pandas20260930/LEEME.md), en Lean: sí a la pregunta
  de Gao con `Res < 4` y para casi todo n. Marmotas: un contraejemplo
  necesita más de `2^21` pasos `3n+1` sobre `2^20`.
- [Wirsching](depuracion/wirsching20260930/LEEME.md), cerrado: queda la
  condición por residuos, cuya versión útil equivale a un teorema local
  límite; (⋆1) literal falla en todo nivel `<=16`.
- [CST](depuracion/cst20260930/LEEME.md): Ocelotas, arriba.

CST: [22 auditado](depuracion/cst20260930/evidencia_veintidos_lean.json),
312 módulos, 3420 consultas sin `sorryAx`.
[Cota general](depuracion/cst20260930/COTA_GENERAL.md) y
[criterio geométrico](depuracion/cst20260930/COLA_PARAMETRICA.md) formalizados:
acotan una región posible de fallos para cualquier límite de rachas.
La [evaluación por bisección](depuracion/cst20260930/PREFIJOS_BINARIOS_LEAN.md)
conserva exactamente la criba afinada; igualdad y verificadores en Lean.
Permitió cerrar 76. [77 aceptado](depuracion/cst20260930/SETENTA_Y_SIETE_LEAN.md):
1420851 nodos y 97 filas cotejados; 91 módulos y 5030 consultas estándar.
[23 sin Rozier–Terracol](depuracion/cst20260930/VEINTITRES_PROPUESTA.md):
43 filas y dos ventanas cotejadas; baja y piloto alto aceptados, cadena en curso.
El [descuento por racha](depuracion/cst20260930/DESCUENTO_RACHAS_LEAN.md)
mejora universalmente la criba; verificador y piloto de 76 aceptados en Lean.
La [cota con suelo](depuracion/cst20260930/SUELO_RACHAS_LEAN.md) tiene prueba
universal y especialización entera aceptadas, sin LMN; faltan el puente
tras cortes y su verificador.
[Tanda cerrada](depuracion/cst20260930/CIERRE_TANDA_20261003.md) con 77;
23 queda en ejecución y pendiente. Siguiente:
recoger su resultado y auditarlo. El censo hasta `2^23` se conserva.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; reconstrucción del 26-09 y
`leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Cada ficha enlaza sus contrastes independientes y certificados;
los cálculos finitos no sustituyen las pruebas universales.

Registro: 268 afirmaciones: 163 demostradas, 86 medidas, 12 conjeturadas
y siete refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar
históricos. zootheorem permanece intacto.
