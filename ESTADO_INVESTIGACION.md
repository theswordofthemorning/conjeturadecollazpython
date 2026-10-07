# Estado para continuar — 07-10-2026

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

Ruta B ([plano](depuracion/casa20261004/LEEME.md)), sin ampliar rachas:
Collatz equivale a los dos muros. En Lean, ningún fugitivo tiene
pronóstico acotado y ninguna órbita permanece en franja. Quedan el cohete,
el planeador intermitente y la grieta. Formalizados: Terras A–C, Korec
para `θ > log 3/log 4`, CST para casi todo n, rareza `x^0,95` y teorema E
de Lagarias bajo LMN. Ninguno cierra los muros.

[Perdices](depuracion/perdices20261007/LEEME.md): olvido tras m subidas;
estacionarias exactas hasta m=6; Tao cotejado. No-cruce rompe la cota
original: `1/6>1/8`, certificado.
[Reserva](depuracion/perdices20261007/UMBRAL.md): todas las continuaciones
de L pasos sobreviven exactamente cuando `P>=2^L`. Cota adaptada escrita
`TV<=G*q+(1-G)`, 20 772 contrastes; medidas sin formalizar.
[Tamaño](depuracion/perdices20261007/TAMANO.md): `R_k=T^k(n)/P_k=o(k)`
para cada fugitivo, en Lean; 14 lemas nuevos, axiomas estándar.
Prueba escrita más fuerte: `R_k^6<=n^6(S_k+1)`; implica regresos
`T^k(n)<=Cn(k+1)^(1/6)` bajo `P_k<=C`. Identidad y factor en Lean;
ordenación y telescopio pendientes. 94 397 contrastes exactos de la cota.
**Siguiente:** seguir el [plan](depuracion/perdices20261007/TAMANO.md#qué-debe-aportar-el-siguiente-paso):
certificar sexta raíz y cuenta de regresos, cruzar con casi fugitivos
y buscar una cota inferior incompatible. La fuga lenta sigue abierta.
[Cierre pedagógico](depuracion/perdices20261007/CIERRE_SESION.md).

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado; `leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Los módulos
nuevos dejan sus registros de `lake env lean`.

Cada ficha enlaza evidencia; los cálculos finitos no prueban universalidad.

Registro: 281 afirmaciones: 176 demostradas, 86 medidas, 12 conjeturadas
y siete refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar históricos.

Sesión del 05-10 [recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md)
con huellas verificadas: implementaciones independientes conservadas.
Falta conciliar sus altas históricas; sólo las extensiones nuevas de Perdices
se añadieron al registro. Su medición antigua hasta m=14 usa flotantes,
no aritmética exacta. Censos históricos y zootheorem intactos.
