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

**Avance del 10-10:** [Jinetas](depuracion/jinetas20261010/LEEME.md)
auditó el traslado y descartó ordenar paradojas mediante `01/10`.
El [segundo ensayo](depuracion/jinetas20261010/PREFIJOS.md) conserva
los prefijos de una misma semilla: intervalo exacto, poda persistente
y 15 enunciados Lean. En el primer cruce vuelve a CST; la monotonía
no fuerza terminar. Una rama viva con mínimos acotados equivale a
una semilla fija sin descenso. No apareció la restricción adicional:
la [ruta](depuracion/casa20261004/RUTA_20261010.md) vuelve al balance.

La [casa](depuracion/casa20261004/LEEME.md) sigue con ambos muros abiertos:
A, cruce implica descenso eventual; B, todo número tiene cruce.
Quedan cohete, planeador intermitente y grieta. Los resultados de
densidad, los tramos de CST y las cotas de regresos no los excluyen.

[Perdices](depuracion/perdices20261007/LEEME.md): el no-cruce rompe la
cota original de mezcla. [Reserva](depuracion/perdices20261007/UMBRAL.md)
tiene prueba escrita adaptada; medidas pendientes de formalización.
[Tamaño](depuracion/perdices20261007/TAMANO.md): sublinealidad en Lean;
la sexta raíz restringe los regresos. Su cierre local en Lean y Mahler
estaban sin commit al iniciar esta tarea; se conservan para integración
separada. El balance detalla evidencia y límites.

**Siguiente:** revisar la criba por prefijos de Ocelotas para buscar
una reducción de rachas propia del factor 3: regla, hipótesis, disminución
estricta y caso terminal antes de otro experimento. No ampliar tablas.
CST completo aún dejaría abierto el muro B.
El [plan del 28-09](depuracion/transversal20260927/PLAN_SESIONES_20260928.md)
queda como antecedente.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; `leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Cada ficha enlaza evidencia; los cálculos finitos no prueban universalidad.

Registro: 284 afirmaciones: 178 demostradas, 86 medidas, 12 conjeturadas
y ocho refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar históricos.

Sesión del 05-10 [recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md)
con huellas verificadas: implementaciones independientes conservadas.
[Conciliación](depuracion/jinetas20261010/CONCILIACION.md): claves y alcance
cotejados; nueve altas recuperadas conservadas sin fusionar. Medición
hasta m=14 en flotantes. Nueve discrepancias de huellas se explican por
finales de línea; dos requieren revisión.
Jinetas no utiliza esas cachés. Censos históricos y zootheorem intactos.
