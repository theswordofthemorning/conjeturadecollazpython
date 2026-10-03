# Estado para continuar — 02-10-2026

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal; de ella la de Garner (1985) sobre rachas y la conjetura 2 de Wu
(1992). CST: Ocelotas hasta diez rachas contadas directamente,
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
- **Ocelotas.** [CST](depuracion/cst20260930/LEEME.md): `cst_lmn` prueba
  primer descenso = primer cruce hasta diez rachas impares, sin Rhin. La
  única hipótesis externa es la cota publicada de Laurent–Mignotte–
  Nesterenko (1995), en forma debilitada
  ([OcelotasLMN](depuracion/cst20260930/LMN_LEAN.md), 02-10). Caso par
  incluido. Con cálculo exacto por convergentes, sin Lean y sin Rhin (basta
  Laurent–Mignotte–Nesterenko), un fallo necesita al menos 18 rachas, o 74
  con Rozier–Terracol
  ([séptima tanda](depuracion/cst20260930/RACHAS_CONVERGENTES.md)).

Axiomas estándar en todo. **Pendiente de revisión humana.** Salvo en las
rachas construidas, nada de esto afirma la llegada a 1.

Cadena de Gao (en `depuracion/gao20260920/formal`): ensayos guardados →
[Lagartijas](depuracion/gao20260920/Lagartijas.md) →
[Martas](depuracion/gao20260920/Martas.md) (ritmo pésimo:
[Cigarras](depuracion/gao20260924/Cigarras.md)) → Tejonas (clases módulo
`2^t` y densidad) → Hienas → Alpacas → Condoras. El artículo I la expone
entera.

## Revisión y publicación

Criterios y lista: [gaopendientes.md](gaopendientes.md). Prioridad: revisión
humana de los enunciados de Gao, Hienas, Garner y Wu. Lean certifica el
enunciado, no su interpretación. La [revisión del 27-09](papers/revision20260927/REVISION.md#4-novedad)
no halló pruebas publicadas; faltan MathSciNet, Scholar y el original de
Garner.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos.** Tres `.tex` ([papers](papers/README.md)) y artefacto en
  Zenodo ([DOI](papers/zenodo/LEEME.md)). AFM rechazó el I; II y III siguen
  allí. **01-10: el I, adaptado, se envió al *Journal of Automated
  Reasoning*** (SNAPP `6ea1db0a…`, en revisión técnica;
  [JAR](papers/jar/LEEME.md)). [Qeios](papers/qeios/LEEME.md) descartado:
  retiro del 5962 pedido el 01-10. Palomar, 29-09: Gao en Lean
  v4.35.0-rc2 en `theswordofthemorning/gao-palomar`, CI en verde, en
  verificación ([Palomar](papers/palomar/LEEME.md)). Zulip: publicado el 29-09
  ([registro](papers/qeios/ZULIP_borrador.md)); responder sólo con autorización.
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

CST: [certificado exacto](depuracion/cst20260930/REVISION_RACHAS.md) y
criba Lean para `1<=q<=82696`; diez módulos sin `sorryAx`. El tramo
`82696 < q < 53715833` lo cubren los convergentes 11 a 16 de `log2 3` y un
lema de Lagrange; el resto, LMN.
[Auditoría de Rhin](depuracion/cst20260930/RHIN_LEAN.md), 02-10: la
proposición de la p. 160 no se leyó y Rhin–Toffin (1986) no alcanza
`log 2, log 3`; con los convergentes y LMN, Rhin ya no hace falta.
Siguiente: revisión humana de `LMNDebil`; decidir si se formaliza la
séptima tanda. No ampliar censos.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; recompilación limpia del 26-09 y `leanchecker`
de 28 módulos, código 0
([compilación, hashes y axiomas](depuracion/gao20260920/evidencia_gao_lean.json);
[reconstrucción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos se compilan con `lake env lean` y dejan su `lean_local.txt`.

Contrastes finitos independientes: [cadena](depuracion/gao20260920/verificar_lagartijas.py),
[pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py),
[Hienas](depuracion/gao20260920/verificar_hienas.py),
[Alpacas](depuracion/garner20260926/verificar_alpacas.py) y los scripts de
cada ficha nueva. No sustituyen los certificados universales.

Registro: 251 afirmaciones
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar
históricos. zootheorem permanece intacto.
