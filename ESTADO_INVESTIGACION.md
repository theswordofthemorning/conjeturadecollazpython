# Estado para continuar — 03-10-2026

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal; de ella la de Garner (1985) sobre rachas y la conjetura 2 de Wu
(1992). CST: Ocelotas hasta veintiuna rachas contadas directamente,
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
- **Ocelotas.** [Veintiuna rachas en Lean](depuracion/cst20260930/VEINTIUNA_LEAN.md):
  `cst_veintiuna_corolario` prueba primer descenso = primer cruce, supuesto
  existente y finito, bajo el
  corolario especializado de Laurent–Mignotte–Nesterenko (1995), con caso
  par incluido. Tabla de 42 intervalos, semillas hasta 4912740, criba
  por prefijos y cola infinita certificadas. Original cotejado y traducción
  `LMN23 -> LMNDebil` en Lean
  ([lecturas](depuracion/cst20260930/LECTURAS_20261003.md)). La
  criba por prefijos exige **al menos 22 rachas** para un fallo, en Lean.
  La [criba unilateral](depuracion/cst20260930/RACHAS_UNILATERALES.md) exige
  **76 con Rozier–Terracol**, con prueba escrita y cálculo exacto; este último
  cierre sigue pendiente en Lean. No amplía el censo.

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

- **Artículos.** [Tres `.tex`](papers/README.md) y
  [Zenodo](papers/zenodo/LEEME.md). AFM rechazó el I; II y III siguen allí.
  I enviado a [JAR](papers/jar/LEEME.md) el 01-10, revisión técnica
  (SNAPP `6ea1db0a…`). [Qeios](papers/qeios/LEEME.md): retiro del 5962
  pedido el 01-10. [Palomar](papers/palomar/LEEME.md), 29-09: Gao en
  Lean v4.35.0-rc2, CI verde, en verificación.
  [Zulip](papers/qeios/ZULIP_borrador.md): publicado el 29-09;
  responder sólo con autorización.
- **OEIS, 30-09.** A078441 aprobada (#40)
  ([ficha](depuracion/oeis20260917/A078441_20260930_aprobada.txt)); valida
  citas y datos, no argumentos propios. A400486 y A400487 sin aprobar
  ([captura](depuracion/oeis20260917/A400486_A400487_20260930_publico.txt));
  si A400487 no se aprobara, retirar su referencia en A078441
  ([respuesta del 28-09](papers/oeis/RESPUESTA_20260928.md)). 02-10: Jason
  Yuen añadió `more` a A400487, sin preguntas; sigue *proposed*.

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

CST: [auditoría completa de 21](depuracion/cst20260930/evidencia_veintiuna_lean.json),
76 módulos y 943 consultas sin `sorryAx`; reanudación con 31 compilados y
45 reutilizados por huellas. Tabla de 42 filas y 202801 clases cotejadas
independientemente; cola reforzada por `5k<=8q+5`. **Sesión cerrada por
petición del usuario.** Al retomar: 22 tiene tabla, prefijos cotejados y
cola auxiliar Lean; faltan evaluación de prefijos y ensamblaje. El cierre
Lean de 75 continúa pendiente. No se amplía el censo hasta `2^23`.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; reconstrucción limpia del 26-09 y
`leanchecker` de 28 módulos, código 0
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Contrastes finitos independientes: [cadena](depuracion/gao20260920/verificar_lagartijas.py),
[pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py),
[Hienas](depuracion/gao20260920/verificar_hienas.py),
[Alpacas](depuracion/garner20260926/verificar_alpacas.py) y los scripts de
cada ficha nueva. No sustituyen los certificados universales.

Registro: 260 afirmaciones
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar
históricos. zootheorem permanece intacto.
