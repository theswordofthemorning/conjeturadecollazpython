# Estado para continuar — 12-10-2026

[Premisa](PREMISA_DE_INVESTIGACION.md): buscar la prueba universal de Collatz;
la convicción del usuario orienta la búsqueda, sin servir como hipótesis.

## Resultados y alcance

- **Gao.** [Tejonas](depuracion/gao20260920/Tejonas.md) y
  [Hienas](depuracion/gao20260920/Hienas.md): densidad natural 1 de coalescencia,
  en la forma de Lagarias y la literal de Gao (1993). No implica llegada a 1.
  [Cigarras](depuracion/gao20260924/Cigarras.md) documenta el ritmo muy lento.
- **Garner y Wu.** [Alpacas](depuracion/garner20260926/Alpacas.md): rachas de
  consecutivos arbitrariamente largas y altas con igual altura y tiempo total
  de parada. [Condoras](depuracion/gao20260920/formal/Condoras.lean): Wu 2;
  Wu 1 equivale, dado Gao, a convergencia en densidad natural 1 y sigue abierto.
  Falta cotejar el original de Wu, consultado mediante CNKI AI.
- **Ocelotas.** [24 rachas](depuracion/cst20260930/VEINTICUATRO_LEAN.md) bajo
  LMN; [77](depuracion/cst20260930/SETENTA_Y_SIETE_LEAN.md) y
  [81 con pesos](depuracion/cst20260930/PESOS_RACHAS.md), bajo LMN y
  Rozier–Terracol. Siempre se supone primer cruce finito.
  LMN original cotejado y puente `LMN23 -> LMNDebil` en Lean
  ([lecturas](depuracion/cst20260930/LECTURAS_20261003.md)).
  Sin Rozier–Terracol, censos propios como hipótesis explícitas cierran
  40/41/42/46 rachas hasta 2^36/2·10^11/3·10^11/7·10^11; 47 pendiente.
  [Calibración](depuracion/cst20260930/CICLOS_CALIBRACION.md): CST hasta R
  excluye ciclos con hasta R rachas; con 81 queda por debajo de Hercher (91).

Sólo axiomas estándar en los módulos Lean registrados. **Revisión humana
pendiente.** Salvo en las rachas construidas, nada afirma llegada a 1.

## Ruta y siguiente acción

[Colisiones](depuracion/perdices20261007/COLISIONES.md) excluye el planeador:
en una órbita positiva inyectiva, los recíprocos son sumables,
`R_k -> ξ` finito y `P_k -> infinito` (antecedente Garcia–Tal).
[Mínimos](depuracion/perdices20261007/MINIMOS.md) extrae reinicios de fuga pura
sin MuroA y demuestra `Collatz <-> MuroB y ausencia de circuitos no triviales`.
**Ambas condiciones siguen abiertas.**

[Complejidad](depuracion/perdices20261007/COMPLEJIDAD.md) restringe repeticiones
y excluye paridades sturmianas para racionales de denominador impar
(antecedente De Jesus). [Salidas](depuracion/perdices20261007/SALIDAS.md):
en `1/110`, `λ(n)<=3log2(n)+1` sigue conjeturado; hasta 2^50, máximo 112,
con auditoría independiente completa hasta 16 bits. Los
[empalmes H](depuracion/perdices20261007/RACHAS_H.md) transportan exactamente
el mínimo original.

[Matrices](depuracion/perdices20261007/SOPORTES_MATRICES_H.md): excluidos
escalares, primera coordenada aislada y recta natural común; diez soportes
mínimos de aporte. Son condiciones necesarias; ninguna dinámica del objetivo
57 eliminada. Árticas indecisas y persistencia abierta. Pendiente algebraico:
diferencias completas de constantes y reglas estáticas, sin exigir circuito.

**Lectura solicitada de las 339:**
[evaluación y ruta](depuracion/coherencia20260913/RUTA_339_20261012.md).
Ruta acordada: priorizar descenso eventual con semilla conservada y tiempos
variables; como piloto, controlar la recarga acumulada de divisibilidad al
cambiar `1/110`. El criterio propuesto no está demostrado; resolver el piloto
tampoco cerraría Collatz. Matrices H queda como ensayo auxiliar. Se localizó
un preprint sobre barreras matriciales: presentación leída, pruebas sin auditar.
No ampliar censos como sustituto de una desigualdad nueva.
[Retomar la próxima sesión](depuracion/coherencia20260913/RUTA_339_20261012.md#reanudar-la-próxima-sesión):
fijar una familia explícita de presupuestos K y estudiar (P), terminando con
prueba, contraejemplo o una obligación pendiente precisa.

## Revisión y publicación

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y Wu.
La [revisión de novedad](papers/revision20260927/REVISION.md#4-novedad) y
zbMATH por citas (11-10) no hallaron pruebas publicadas; faltan MathSciNet,
Scholar y Garner original. **No anunciar, enviar a OEIS ni contactar sin autorización.**

[Artículos](papers/README.md), [Zenodo](papers/zenodo/LEEME.md): tras los
[rechazos AFM](papers/CORREOS_20261004.md), II y III libres; I en
[JAR](papers/jar/LEEME.md), sin noticias al 04-10; IV sin enviar.
[Qeios](papers/qeios/LEEME.md) retirado;
[Palomar](papers/palomar/LEEME.md) verifica Gao, CI verde;
[Zulip](papers/qeios/ZULIP_borrador.md) borrado.
OEIS A078441, A400486 y A400487 aprobadas: no validan pruebas.
[Próxima sesión OEIS](papers/oeis/PENDIENTE_20261010.md): dos correcciones y
una sucesión, sin enviar y sujetas al panel.

## Evidencia y conservación

[Arca completa](depuracion/mapa20261011/MapaDependenciasComplex.html): 70 nombres,
123 piezas, nueve ramas; [auditoría](depuracion/mapa20261011/RECONSTRUCCION.md).
[Registro versionado](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`: **339 filas**, 226 demostradas, 92 medidas,
13 conjeturadas y ocho refutadas. Cotejo literal completo con SQLite;
la incidencia histórica de la fila 71 sigue señalada, no usada.

Lean 4.32.2 y Mathlib fijado; [reproducción](depuracion/gao20260920/formal/README.md).
[Evidencia de esta lectura](depuracion/coherencia20260913/evidencia_ruta339_20261012.json):
cinco consultas Lean y controles exactos acotados; sin reconstrucción completa
ni censos grandes. Cambios locales preexistentes conservados.
[Casa recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md) y
[conciliación](depuracion/jinetas20261010/CONCILIACION.md): dos huellas antiguas
requieren revisión; no usar sus cachés. Históricos, conversaciones y zootheorem intactos.
