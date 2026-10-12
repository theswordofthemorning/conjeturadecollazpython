# Estado para continuar — 12-10-2026

[Premisa](PREMISA_DE_INVESTIGACION.md): buscar la prueba universal de Collatz;
la convicción del usuario orienta la búsqueda, sin servir como hipótesis.

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
  existente, bajo Laurent–Mignotte–Nesterenko (1995), externo.
  Original cotejado; `LMN23 -> LMNDebil` en Lean
  ([lecturas](depuracion/cst20260930/LECTURAS_20261003.md)). La
  criba por prefijos exige **al menos 25 rachas** para un fallo, en Lean.
  El [cierre de 77](depuracion/cst20260930/SETENTA_Y_SIETE_LEAN.md) también está
  formalizado: exige **78 con LMN y Rozier–Terracol** como hipótesis externas.
  **12-10:** los [pesos por racha](depuracion/cst20260930/PESOS_RACHAS.md),
  la parte del teorema 21 de Hercher que pasa al primer cruce, cierran
  **81 rachas** en Lean con las mismas dos hipótesis y sin árbol de
  prefijos. Un fallo exige 82. La fusión del lema 9 no se transfiere.
  Sin Rozier–Terracol, LMN y un censo propio (cálculo en Python,
  hipótesis explícita, 0 fallos) dan en Lean **40 rachas** con censo hasta
  2^36, **41** con censo hasta 2·10^11 y **42** con censo hasta 3·10^11.

Sólo axiomas estándar en los módulos Lean. **Revisión humana pendiente.**
Salvo en las rachas construidas, nada afirma la llegada a 1.

Cadena y alcance de Gao: [Tejonas](depuracion/gao20260920/Tejonas.md).
Ritmo muy lento: [Cigarras](depuracion/gao20260924/Cigarras.md).

## Revisión y publicación

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y
Wu. Lean certifica el enunciado, no su interpretación. La
[revisión del 27-09](papers/revision20260927/REVISION.md#4-novedad) no halló
pruebas publicadas; zbMATH por citas (11-10) tampoco. Faltan MathSciNet,
Scholar y el original de Garner.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos.** [Índice](papers/README.md), [Zenodo](papers/zenodo/LEEME.md).
  [Rechazos AFM](papers/CORREOS_20261004.md): II y III libres;
  I en [JAR](papers/jar/LEEME.md), sin noticias al 04-10;
  [IV](papers/articulo_IV_ocelotas.tex), sin enviar.
  [Qeios](papers/qeios/LEEME.md): retirado.
  [Palomar](papers/palomar/LEEME.md): verificando Gao, CI verde.
  [Zulip](papers/qeios/ZULIP_borrador.md): anuncio borrado.
- **OEIS.** A078441, A400486 y [A400487](https://oeis.org/A400487)
  aprobadas; no validan pruebas. Tres cupos previstos para dos correcciones
  y una sucesión nueva, sin enviar y sujetos al panel de la cuenta:
  [pendiente de la próxima sesión](papers/oeis/PENDIENTE_20261010.md).

## Ruta vigente y próximo bloque

**Conservado:** [Colisiones](depuracion/perdices20261007/COLISIONES.md)
excluye al planeador: con n>0 e inyectividad orbital, `sum 1/T^j(n)<=3*2^100`,
`R_k->ξ` finito y `P_k->infinito` (antecedente Garcia–Tal 1999).
[Mínimos futuros](depuracion/perdices20261007/MINIMOS.md) da reinicios de fuga
pura sin MuroA y `Collatz <-> MuroB y ausencia de circuitos no triviales`.
**Ambas condiciones siguen abiertas.**

**Repeticiones:** [Complejidad](depuracion/perdices20261007/COMPLEJIDAD.md)
acota repeticiones y prueba `liminf p(m)/m>=1/log2(3/2)` en órbitas
inyectivas. Excluye paridades sturmianas para racionales de denominador
impar (antecedente De Jesus): 39 teoremas, 29 módulos, 368 consultas estándar.

**Frontera:** `λ(n)<=3log2(n)+1` para la clase `1`/`110` sigue conjeturado.
[Salidas](depuracion/perdices20261007/SALIDAS.md) conserva tres censos auditados;
el contraste independiente llega a 16 bits. Censo hasta `2^50`: máximo 112.

**H de Yolcu–Aaronson–Heule:** [Rachas](depuracion/perdices20261007/RACHAS_H.md),
18 lemas Lean. Pasados/futuros finitos compatibles en `x>0, x=15 mod 24`;
densidad relativa `21^(-k)*16^(-l)`, por escrito. El tamaño del empalme
transporta exactamente el mínimo original; no aporta una restricción nueva.

**Matrices naturales 2x2:** [Proyecciones](depuracion/perdices20261007/PROYECCIONES_MATRICES_H.md)
excluye el caso escalar y la primera coordenada aislada.
[Soportes y rectas](depuracion/perdices20261007/SOPORTES_MATRICES_H.md) añade
14 teoremas Lean: recta natural común excluida, incluso con conexiones en
ambos sentidos; diez soportes mínimos de aporte izquierdo. Cotejo de
16.384 soportes. Aporte positivo no equivale a descenso; árticas indecisas
y **persistencia abierta**.

**Siguiente:** estudiar diferencias completas de constantes y reglas
estáticas en matrices con ruta activa y sin recta natural común.
No exigir un circuito sin prueba. Cierre solicitado el 12-10.

## Evidencia y conservación

**Arca reconstruida:** [mapa básico](depuracion/mapa20261011/MapaDependenciasBasic.html)
y [completo](depuracion/mapa20261011/MapaDependenciasComplex.html): 70 nombres,
123 piezas, nueve ramas. Incluye recuperados y alias; distingue historia,
dependencias e hipótesis. [Auditoría](depuracion/mapa20261011/RECONSTRUCCION.md):
68 revisiones de Git; 331 afirmaciones conservadas y dos nuevas, SQLite y navegación sin red.

Lean 4.32.2, Mathlib fijado; `leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Registro: 333 afirmaciones: 220 demostradas, 92 medidas, 13 conjeturadas
y ocho refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar históricos.

Histórico: [recuperación del 05-10](depuracion/casa20261005_recuperada/RECUPERACION.md)
y [conciliación](depuracion/jinetas20261010/CONCILIACION.md). Dos huellas antiguas
requieren revisión; no se usan sus cachés. Históricos y zootheorem intactos.
