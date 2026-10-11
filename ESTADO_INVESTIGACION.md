# Estado para continuar — 10-10-2026

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

- **Artículos.** [Índice](papers/README.md), [Zenodo](papers/zenodo/LEEME.md).
  [Rechazos AFM](papers/CORREOS_20261004.md): II y III libres;
  I en [JAR](papers/jar/LEEME.md), sin noticias al 04-10;
  [IV](papers/articulo_IV_ocelotas.tex), sin enviar.
  [Qeios](papers/qeios/LEEME.md): retirado.
  [Palomar](papers/palomar/LEEME.md): verificando Gao, CI verde.
  [Zulip](papers/qeios/ZULIP_borrador.md): anuncio borrado.
- **OEIS.** Aprobadas [A078441](depuracion/oeis20260917/A078441_20260930_aprobada.txt)
  (30-09) y [A400486](depuracion/oeis20260917/A400486_20261004_aprobada.txt)
  (04-10); no validan pruebas. A400487 sigue
  pendiente, con `more`. Si se rechaza, retirar su referencia en A078441:
  [seguimiento](papers/oeis/RESPUESTA_20260928.md).

## Ruta vigente y próximo bloque

**Conservado:** [Colisiones](depuracion/perdices20261007/COLISIONES.md)
excluye al planeador. Atajo T, n>0 e inyectividad orbital:
`sum 1/T^j(n)<=3*2^100`, `R_k->ξ` finito y `P_k->infinito`.
Formalizado; antecedente Garcia–Tal (1999), sin reclamar prioridad.

[Mínimos futuros](depuracion/perdices20261007/MINIMOS.md) formaliza
la cota exponencial de cola y los reinicios grandes de fuga pura,
sin MuroA. También `Collatz <-> MuroB y ausencia de circuitos no
triviales`. **Ambas condiciones siguen abiertas.** La anchura
`O(n^(99/100))` conserva sólo prueba escrita.

**Cierre del 10-10:** [Cancelaciones](depuracion/perdices20261007/CANCELACIONES.md),
continuación de [Repeticiones](depuracion/perdices20261007/REPETICIONES.md).
En `1`/`110`, persistir bajo G exige `3 | v2(z+1)`;
si falla, hay salida en a lo sumo `floor(v2(z+1)/3)` pasos G.
El mapa F entre cambios cumple `8F(h)>=13h` y sus salidas tienen
valuación 3-ádica par. Veinte lemas nuevos en Lean, 26 módulos
previos auditados, 329 consultas; sólo axiomas estándar.

Prueba escrita: inversa y realización de cualquier historia finita
con semillas variables. Cotejo: 512 entradas G, 2048 semillas F y 820
historias. **La persistencia infinita de una misma semilla sigue abierta**;
resolver esta clase restringida tampoco resolvería todo MuroB.
La [cola](depuracion/perdices20261007/COLA.md) conserva su alcance y
la precaución bibliográfica sobre López–Stoll (2021).

[Novena](depuracion/perdices20261007/NOVENA.md),
[Semilla](depuracion/perdices20261007/SEMILLA.md) y
[Aporte](depuracion/perdices20261007/APORTE.md): conservados; fuga pura
ya excluye infinitos regresos.

La [casa](depuracion/casa20261004/LEEME.md) conserva abiertos A y B;
Collatz sigue abierto. [Mahler](depuracion/mahler20261007/LEEME.md)
incorpora ξ finito, sin excluir al cohete.

**Siguiente sesión:** acotar el crecimiento de representantes en historias
no periódicas de una misma semilla, primero en F y luego entre mínimos
futuros. Perfil inverso y resonancia no son restricciones independientes;
los cortes finitos no bastan.
El [plan del 28-09](depuracion/transversal20260927/PLAN_SESIONES_20260928.md)
queda como antecedente.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; `leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Cada ficha enlaza evidencia; los cálculos finitos no prueban universalidad.

Registro: 314 afirmaciones: 208 demostradas, 86 medidas, 12 conjeturadas
y ocho refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar históricos.

Histórico: [recuperación del 05-10](depuracion/casa20261005_recuperada/RECUPERACION.md)
y [conciliación](depuracion/jinetas20261010/CONCILIACION.md). Se conservan
implementaciones y nueve altas independientes. Dos huellas antiguas
requieren revisión; no se usan sus cachés. Censos y zootheorem intactos.
