# Estado para continuar — 17-10-2026

[Premisa](PREMISA_DE_INVESTIGACION.md): buscar la prueba universal de Collatz;
la convicción del usuario orienta la búsqueda, sin servir como hipótesis.

## Resultados y alcance

- **Gao.** [Tejonas](depuracion/gao20260920/Tejonas.md) y
  [Hienas](depuracion/gao20260920/Hienas.md): coalescencia en densidad 1,
  no llegada a 1. [Cigarras](depuracion/gao20260924/Cigarras.md): ritmo lento.
- **Garner y Wu.** [Alpacas](depuracion/garner20260926/Alpacas.md): consecutivos
  en rachas arbitrariamente largas y altas con igual altura y tiempo de parada.
  [Condoras](depuracion/gao20260920/formal/Condoras.lean): Wu 2;
  Wu 1 equivale, dado Gao, a convergencia en densidad natural 1 y sigue abierto.
  Garner mide la altura con T, y Wu probablemente también
  ([nota](papers/revision20260927/cnki_wu_20261017.md)).
  [AlturaT](depuracion/gao20260920/formal/AlturaT.lean) da los mismos
  resultados con T (altura T = σ∞). Falta el impreso de Wu.
- **Ocelotas.** [83 rachas](depuracion/cst20260930/revision_rozier_20261016/REVISION.md)
  en Lean bajo LMN o Rhin y cobertura externa de Roosendaal hasta
  46645791847966786687 con tiempo clásico<=2480. Puente cobertura→CST
  formalizado; primer cruce finito supuesto. LMN original cotejado;
  Rhin original p.160 cotejado: H>=2, exponente 13,3, sin factor adicional.
  Sin esa cobertura: [24 bajo LMN](depuracion/cst20260930/VEINTICUATRO_LEAN.md)
  y 40/41/42/46 con censos propios como hipótesis; 47 pendiente.

Sólo axiomas estándar en los módulos Lean registrados. **Revisión humana
pendiente.** Salvo en las rachas construidas, nada afirma llegada a 1.

## Ruta y siguiente acción

[Colisiones](depuracion/perdices20261007/COLISIONES.md): recíprocos sumables
en órbitas positivas inyectivas; `R_k -> ξ`, `P_k -> infinito` (Garcia–Tal).
[Mínimos](depuracion/perdices20261007/MINIMOS.md) extrae reinicios de fuga pura
sin MuroA y demuestra `Collatz <-> MuroB y ausencia de circuitos no triviales`.
**Ambas condiciones siguen abiertas.**

[Complejidad](depuracion/perdices20261007/COMPLEJIDAD.md) restringe repeticiones
y excluye paridades sturmianas para racionales de denominador impar
(antecedentes Dubickas 2009 y De Jesus). [Salidas](depuracion/perdices20261007/SALIDAS.md):
en `1/110`, `λ(n)<=3log2(n)+1` sigue conjeturado; hasta 2^50, máximo 112,
con auditoría independiente completa hasta 16 bits. Los
[empalmes H](depuracion/perdices20261007/RACHAS_H.md) transportan exactamente
el mínimo original.

[Matrices](depuracion/perdices20261007/SOPORTES_MATRICES_H.md): diez soportes;
familias excluidas, objetivo 57 sin dinámica. Árticas y persistencia abiertas.

**Piloto de recargas:** [ruta](depuracion/coherencia20260913/RUTA_339_20261012.md).
[Recargas](depuracion/perdices20261007/RECARGAS.md) refuta presupuestos de
pendiente<=1 y de las dos valuaciones iniciales; [Perfiles](depuracion/perdices20261007/PERFILES.md),
rangos locales con perfiles finitos. [Transporte impar](depuracion/perdices20261007/TRANSPORTE_IMPAR.md):
encaje universal Lean y `Eeta<=2*ell(n)` con hasta un cambio, por escrito;
ell=ceil(log2(n+5)). Partes impares no monótonas. [Filtros de math](depuracion/exploracionmath20261016/EXPLORACION.md).
[Dos cambios](depuracion/perdices20261007/DOS_CAMBIOS.md): P2 para ABA.
[Altura BAB](depuracion/perdices20261007/ALTURA_BAB.md): epsilon=7/17 hasta dos
cambios. [Tres cambios](depuracion/perdices20261007/TRES_CAMBIOS.md):
epsilon=1/13 hasta tres, siempre K=2*ell. Cierres Lean; enlaces orbitales
escritos. El modelo excesivo de cuatro cambios es irrealizable módulo 9.
**Perdices, ruta Codex:** [banda óptima](depuracion/perdices20261007/congruencias_codex20261016/CONGRUENCIAS.md)
`b+delta<=ell(n)`; [enlace orbital Lean](depuracion/perdices20261007/congruencias_codex20261016/ORBITAS.md).
[Ventanas conjuntas](depuracion/perdices20261007/congruencias_codex20261016/CONJUNTAS.md):
mínimos vecinos incompatibles; exceso óptimo de 72 por pareja disjunta
(n=667), para cualquier número de ventanas.
[Barrera triple](depuracion/perdices20261007/congruencias_codex20261016/BARRERA.md):
alguno de tres excesos k_i es >=17; suma k_i>=17*floor(m/3).
Prueba escrita y certificado modular independiente; **nuevo Lean pendiente**
al cierre. El peso geométrico limita la condición conjunta desde n.
**Siguiente:** completar Lean y controlar reloj o carga terminal; P abierto.
[Claude](RutaDeJudasIscariote.md): [J2](depuracion/judas20261016/J2_MECANISMOS.md)
sin mecanismo publicado. En Lean, el piloto equivale a la parada de G, entre
Mahler y la 4.14. J3b: [expediente](depuracion/judas20261016/EXPEDIENTE_REVISION.md).
[AProVE](depuracion/judas20261016/escalera/LEEME.md): KILLED por memoria con su
portafolio; MAYBE con dos estrategias acotadas, atascadas en el núcleo G.
**Siguiente:** Linux con 32 GB o más.

## Revisión y publicación

[Revisión Rozier](depuracion/cst20260930/revision_rozier_20261016/REVISION.md):
83 con dos cierres, cola Rhin 2^68 frente a LMN 2^76; cobertura externa
no reproducida. Original de Rhin obtenido; su prueba no está formalizada.
Simons (2022) es antecedente cercano, prioridad pendiente.
[Plan B](depuracion/cst20260930/revision_rozier_20261016/PLAN_RESPUESTA.md):
esperar un avance considerable y un nuevo paper; entonces responder brevemente
todas sus preguntas junto con su presentación. Gao/Wu/Garner son candidatos
por valorar. Borrador sin enviar; commit y push de esta revisión autorizados.

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y Wu;
[prioridad](papers/revision20260927/REVISION.md#4-novedad), MathSciNet,
Scholar e impreso de Wu. **No anunciar, enviar a OEIS ni contactar sin autorización.**

[Artículos](papers/README.md): II y III libres tras
AFM; I en [JAR](papers/jar/LEEME.md), sin noticias
al 04-10; IV sin enviar. [Qeios](papers/qeios/LEEME.md) retirado;
[Palomar](papers/palomar/LEEME.md) verifica Gao; Zulip borrado.
OEIS A078441, A400486 y A400487 aprobadas: no validan pruebas.
[Próxima sesión OEIS](papers/oeis/PENDIENTE_20261010.md): dos correcciones y
una sucesión, sin enviar y sujetas al panel.

## Evidencia y conservación

[Arca](depuracion/mapa20261011/MapaDependenciasComplex.html): 70 nombres,
123 piezas; [auditoría](depuracion/mapa20261011/RECONSTRUCCION.md).
[Registro versionado](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`: **349 filas**, 235 demostradas, 92 medidas,
13 conjeturadas y nueve refutadas; cotejo literal con SQLite. Tres altas
Codex validadas en copia temporal (352 filas); integración central pendiente.
Incidencia histórica de la fila 71 señalada y no usada.

Lean 4.32.2 y Mathlib fijado; [reproducción](depuracion/gao20260920/formal/README.md).
[Evidencia Rozier](depuracion/cst20260930/evidencia_rozier.json): 146 consultas
Lean estándar; [cotejo exacto](depuracion/cst20260930/revision_rozier_20261016/cotejo_numeros.json).
Perdices: 44 consultas Lean previas; barrera nueva: 18144 cadenas,
33696 ternas y 15584 casos con A vacías; formalización pendiente.
Realización de familias óptimas y cilindro terminal: prueba escrita.
[Casa recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md) y
[conciliación](depuracion/jinetas20261010/CONCILIACION.md): dos huellas antiguas
requieren revisión; no usar sus cachés. Históricos, conversaciones y zootheorem intactos.
