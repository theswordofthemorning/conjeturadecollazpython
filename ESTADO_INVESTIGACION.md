# Estado para continuar — 27-09-2026

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

## Primera obligación al retomar

Lista completa y criterios de cierre: [gaopendientes.md](gaopendientes.md).

1. **Revisión humana de los enunciados.** Leer
   [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean),
   líneas 11–20; [Hienas.lean](depuracion/gao20260920/formal/Hienas.lean),
   líneas 34–76, y [GarnerEnunciado.lean](depuracion/gao20260920/formal/GarnerEnunciado.lean),
   líneas 11–27, y [WuEnunciado.lean](depuracion/gao20260920/formal/WuEnunciado.lean),
   líneas 12–58. Lean certifica el enunciado, no su lectura. Hay tres apoyos:
   - las definiciones reproducen la tabla 3 de Gao;
   - Hienas escribe de nuevo la forma de Lagarias sin importar nada del
     proyecto;
   - los `#guard` de Garner reproducen las rachas 943–949, 7083–7099 y
     57346–57370 de Gao.
2. **Bibliografía a fondo.** No se halló prueba publicada de ninguna de las
   tres ([ficha](depuracion/gao20260920/ficha_gao_lagarias.md),
   [revisión del 27-09](papers/revision20260927/REVISION.md#4-novedad)).
   El 27-09 se consultaron zbMATH (API), arXiv y la web. Faltan
   MathSciNet, Scholar y el texto de Garner (1985).
3. **Destino.** Los datos del autor, la declaración de IA y el cotejo de
   Wu con la IA de CNKI ya están en los artículos (27-09). Destino elegido
   el 27-09: Zenodo + *Annals of Formalized Mathematics*. Todo está
   publicado en Zenodo y los tres artículos se enviaron a AFM (#19502–#19504)
   ([papers/zenodo/](papers/zenodo/LEEME.md)).

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos: escritos, compilados y revisados el 27-09.** Son tres `.tex`
  en inglés (Gao, Garner y Wu), con la revisión adversarial y lo que falta
  en [papers/README.md](papers/README.md).
  - El 27-09 por la noche se publicaron en Zenodo el artefacto Lean
    (10.5281/zenodo.23003500) y los tres artículos (23003524, 23003526 y
    23003528).
  - Los artículos se enviaron a *Annals of Formalized Mathematics*: #19502,
    #19503 y #19504, en *Submitted* ([papers/zenodo/](papers/zenodo/LEEME.md)).
  - Contestar a los editores requiere autorización.
- **OEIS: enviadas el 27-09 con autorización del usuario; las tres en
  *proposed*** ([papers/oeis/LEEME.md](papers/oeis/LEEME.md)). Son A400486
  (la tabla 3 de Gao), A400487 (la cuenta de Wu) y la revisión #31 de
  A078441 (Garner). Cupos: 3 de 3. La propuesta del encuentro del 24-09
  nunca se envió. Contestar a los editores requiere autorización.
- **Siguiente ruta:** la elige el usuario. Candidatas en
  [gaopendientes.md](gaopendientes.md), punto 6: el corolario
  `A398792(t)/2^t -> 1`, un ritmo útil, y Garner (1) con alturas en `ℕ∪{∞}`.
  Garner (1) con alturas finitas sigue abierta.

## Evidencia y conservación

Lean 4.32.2 y Mathlib fijado. El 26-09 se recompiló todo desde cero (1610
tareas, 175 consultas de axiomas estándar). Tras Alpacas, `leanchecker` da
código 0 en los 28 módulos propios, y `leanchecker --fresh GarnerEnunciado`,
que repasa además Mathlib, sale con código 0.
[Compilación, hashes y axiomas](depuracion/gao20260920/evidencia_gao_lean.json),
con hashes en LF. `formal/.lake/build_respaldo_20260920`, fuera de Git, se
puede borrar. `.lake/` se reconstruye con `lake exe cache get` ([README](depuracion/gao20260920/formal/README.md)).

Contrastes independientes, finitos: [cadena](depuracion/gao20260920/verificar_lagartijas.py),
[262.144 pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py),
[Hienas](depuracion/gao20260920/verificar_hienas.py),
[Alpacas](depuracion/garner20260926/verificar_alpacas.py) y la
[revisión del 27-09](papers/revision20260927/REVISION.md). Esta última usa
código nuevo y reproduce enteras las tablas 2 y 3 de Gao; hasta entonces la
2 no se había cotejado. Cubre también Garner por otra ruta y Wu hasta
`N=26`, y comprueba que los hashes de Lean son los de la evidencia. El
certificado universal es Lean.

Registro 2026-09-26: 235 afirmaciones; Lagartijas, CF_F, Martas, Tejonas,
`gao_densidad`, `hienas`, `alpacas_garner` y `condoras_wu` demostradas. Fuente versionada `depuracion/coherencia20260913/registro.json`
y generador `guardarafirmaciones.py`. No reconstruir conversaciones ni
alterar históricos. zootheorem permanece intacto.
