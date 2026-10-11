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

**Avance del 10-10:** [Perdices: semilla](depuracion/perdices20261007/SEMILLA.md)
formaliza que fuga pura e infinitos regresos a un techo fijo exigen
`v-u>H(T^u(n)+1)^5` en toda cola, para cada H fijo. La cota superior
opuesta bastaría para excluir ese frente; sigue abierta.

Catorce lemas nuevos, veinte módulos previos auditados, 206 consultas.
Cotejo: 2047 palabras, 20481 cortes y 223 excursiones no unitarias.
Tres pares tienen igual aporte local y distinto levantamiento.
La divisibilidad es formal; la fórmula modular y la equivalencia
infinita son escritas. [Aporte](depuracion/perdices20261007/APORTE.md)
conserva su familia, con d<x: no contradice la nueva exigencia.

[Excepciones](depuracion/perdices20261007/EXCEPCIONES.md) conserva la
no acotación formal de E; su tasa escrita 7/25 sigue por formalizar.
[Balance](depuracion/perdices20261007/BALANCE.md) conserva el presupuesto
par; [Cruce](depuracion/perdices20261007/CRUCE.md), `O(K^(4/25))`.

La [casa](depuracion/casa20261004/LEEME.md) mantiene abiertos los muros
A y B. Planeador general, cohete y grieta siguen sin excluirse.
[Jinetas](depuracion/jinetas20261010/RACHAS.md) no obtuvo inducción;
la [reserva](depuracion/perdices20261007/UMBRAL.md) tiene medidas por
formalizar. [Mahler](depuracion/mahler20261007/LEEME.md) queda integrado
como vía cerrada: documenta identidades y límites de la analogía,
sin excluir al cohete. Su plan del 07-10 es un antecedente.

**Siguiente:** acotar la duración por la entrada y su congruencia
en las palabras de retorno de SEMILLA §4. Bastaría `d<=H(x+1)^5`
uniformemente en una cola. La congruencia sola no da esa cota
ni obliga a cambiar la semilla.
El [plan del 28-09](depuracion/transversal20260927/PLAN_SESIONES_20260928.md)
queda como antecedente.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; `leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Cada ficha enlaza evidencia; los cálculos finitos no prueban universalidad.

Registro: 300 afirmaciones: 194 demostradas, 86 medidas, 12 conjeturadas
y ocho refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar históricos.

Sesión del 05-10 [recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md)
con huellas verificadas: implementaciones independientes conservadas.
[Conciliación](depuracion/jinetas20261010/CONCILIACION.md): claves y alcance
cotejados; nueve altas recuperadas conservadas sin fusionar. Medición
hasta m=14 en flotantes. Nueve discrepancias de huellas se explican por
finales de línea; dos requieren revisión.
Los módulos actuales no utilizan esas cachés. Censos históricos y zootheorem intactos.
