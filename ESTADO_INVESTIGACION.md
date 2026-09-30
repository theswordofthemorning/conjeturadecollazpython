# Estado para continuar — 30-09-2026

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal; de ella la de Garner (1985) sobre rachas, y la conjetura 2 de
Wu (1992).**

- **Forma de Lagarias.** `GaoEnunciado.conjetura_gao`
  ([Tejonas](depuracion/gao20260920/Tejonas.md)): con f el mapa clásico
  (`n/2` o `3n+1`), el conjunto de n tales que `f^k(n)=f^k(n+1)` para algún
  `k<=log2 n` tiene densidad natural 1.
- **Forma de Gao (1993).** `GaoLiteral.conjetura_gao_literal`
  ([Hienas](depuracion/gao20260920/Hienas.md)): `d̄_k -> 1`, con su
  coalescencia exigente (mismas divisiones por 2, sin pasar por 1), y
  además `d(x) -> 1`.
- **Garner (1985).** `GarnerEnunciado.conjetura_garner`
  ([Alpacas](depuracion/garner20260926/Alpacas.md)): para cada L hay L+1
  consecutivos, tan grandes como se quiera, con la misma altura y el mismo
  tiempo total de parada.
- **Wu (1992).** `WuEnunciado` ([Condoras](depuracion/gao20260920/formal/Condoras.lean)):
  `lim L=∞` (conjetura 2). La conjetura 1, `lim d(M)=1`, equivale dado Gao a
  que casi todo n llegue a 1: sigue abierta. Citas leídas con la IA de CNKI;
  falta cotejar el original.

`#print axioms` sólo muestra `propext`, `Classical.choice` y `Quot.sound`.
**Pendiente de revisión humana.** Salvo en las rachas construidas, no
afirma nada sobre la llegada a 1.

## Objeto y ley

`T(x)=x/2` o `(3x+1)/2`. Cadena absorbente con bits iid justos (paridad
del ancla), estado `{v,3^k*v+c}`; sigma es la fusión. Tejonas demuestra que
la proporción `a(t)/2^t` de clases módulo `2^t` fusionadas hasta t es
`P(sigma<=t)`.

## Cadena demostrada (todo en `depuracion/gao20260920/formal`)

C1, H3, VH, Hormigas, EF y ensayos guardados (20-09) →
[Lagartijas](depuracion/gao20260920/Lagartijas.md) (CF_F) →
[Martas](depuracion/gao20260920/Martas.md) (`P(sigma>h)->0`; ritmo pésimo,
[Cigarras](depuracion/gao20260924/Cigarras.md)) →
[Tejonas](depuracion/gao20260920/Tejonas.md) (clases y densidad) →
[Hienas](depuracion/gao20260920/Hienas.md) (forma literal) →
[Alpacas](depuracion/garner20260926/Alpacas.md) (Garner) → Condoras (Wu).
El artículo I la expone entera, con cada nombre Lean.

## Revisión y publicación

Lista completa y criterios de cierre: [gaopendientes.md](gaopendientes.md).

Prioridad pendiente: revisión humana de
[GaoEnunciado](depuracion/gao20260920/formal/GaoEnunciado.lean),
[Hienas](depuracion/gao20260920/formal/Hienas.lean),
[GarnerEnunciado](depuracion/gao20260920/formal/GarnerEnunciado.lean) y
[WuEnunciado](depuracion/gao20260920/formal/WuEnunciado.lean).
Lean certifica el enunciado, no su interpretación. Las tablas, las rachas
de Gao y la formulación independiente de Hienas apoyan su lectura.

No se halló prueba publicada de las tres conjeturas en la
[revisión bibliográfica del 27-09](papers/revision20260927/REVISION.md#4-novedad).
Faltan MathSciNet, Scholar y el original de Garner; la novedad no está
certificada exhaustivamente.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos, 29-09.** Tres `.tex` en inglés ([papers](papers/README.md));
  artefacto y artículos en Zenodo ([DOI](papers/zenodo/LEEME.md)). AFM
  rechazó el I sin motivos; el usuario la descartó. **El I, versión 2, se
  envió a Qeios como preprint** (envío 5962; en línea en un día hábil), con
  reclutamiento gratuito de revisores y la sección de tres comprobaciones.
  No pasar a *Version of Record*; II y III esperan
  ([Qeios](papers/qeios/LEEME.md)). **Palomar, 29-09:** Gao portado a Lean
  v4.35.0-rc2 y al sistema de módulos en el repositorio público
  `theswordofthemorning/gao-palomar`; CI en verde, incluido `lake comparator`;
  enviado a las 21:38 UTC, en verificación ([Palomar](papers/palomar/LEEME.md)).
  Zulip: publicado el 29-09 en #Machine Learning for Theorem Proving
  ([registro](papers/qeios/ZULIP_borrador.md)); responder sólo con autorización.
- **OEIS, 30-09:** A078441 aprobada (#40) con el bloque firmado y los enlaces
  ([ficha](depuracion/oeis20260917/A078441_20260930_aprobada.txt)); valida
  citas y datos, no argumentos propios. A400486 y A400487 siguen sin aprobar
  ([captura](depuracion/oeis20260917/A400486_A400487_20260930_publico.txt));
  si A400487 no se aprobara, retirar su referencia en A078441. Antes:
  [respuesta del 28-09](papers/oeis/RESPUESTA_20260928.md).

## Ruta vigente y próximo bloque

[Plan por sesiones](depuracion/transversal20260927/PLAN_SESIONES_20260928.md):
Nashida, Pandas, Wirsching (4–6 sesiones), CST (6); presupuestos, no plazos.

- [Nashida](depuracion/nashida20260928/LEEME.md), 28-09: puente condicional
  de barrera, con la cota externa como hipótesis.
- [Pandas](depuracion/pandas20260930/LEEME.md), 30-09, en Lean: pregunta de
  Gao (¿igual altura, igual σ∞?) sí con `Res < 4` y para casi todo n; Marmotas
  exige a un contraejemplo más de `2^21` pasos `3n+1` sobre `2^20`.
- [Wirsching](depuracion/wirsching20260930/LEEME.md), sesión 1, 30-09: sólo
  queda la condición por residuos; (⋆1) literal falla en todo nivel `<=16`
  (el entero 34 no tiene caminos con `l` impares y `l` pares). Un 3-ádico malo
  en infinitos niveles refutaría la conjetura 2; hasta 16 no se agotan.

Siguiente: sesión 2 de Wirsching (W2: ventana desplazada y µ por entero,
medida; intento acotado de W1). Sin mecanismo, pasar a CST. Se conservan la
[evaluación CST](depuracion/transversal20260927/SEGUNDA_OPINION_20260928.md)
y el [plan anterior](depuracion/transversal20260927/LEEME.md).

## Evidencia y conservación

Evidencia previa: Lean 4.32.2, Mathlib fijado; recompilación limpia del
26-09, 1610 tareas y 175 consultas de axiomas estándar. `leanchecker`:
28 módulos propios y `--fresh GarnerEnunciado`, código 0.
[Compilación, hashes y axiomas](depuracion/gao20260920/evidencia_gao_lean.json);
[reconstrucción](depuracion/gao20260920/formal/README.md).

Contrastes independientes, finitos: [cadena](depuracion/gao20260920/verificar_lagartijas.py),
[pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py),
[Hienas](depuracion/gao20260920/verificar_hienas.py),
[Alpacas](depuracion/garner20260926/verificar_alpacas.py) y la
[revisión del 27-09](papers/revision20260927/REVISION.md): tablas 2 y 3 de
Gao, Garner por otra ruta, Wu hasta `N=26` y hashes. Estos controles
finitos no sustituyen el certificado universal de Lean.

Registro del 30-09: 243 afirmaciones, con Pandas, Marmotas y Wirsching;
[fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`. [Evidencia nueva](depuracion/nashida20260928/evidencia.json).
No reconstruir conversaciones ni alterar
históricos. zootheorem permanece intacto.
