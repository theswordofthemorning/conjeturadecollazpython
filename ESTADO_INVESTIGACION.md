# Estado para continuar — 19-10-2026

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
  Altura con T en Garner, probablemente también en Wu
  ([nota](papers/revision20260927/cnki_wu_20261017.md)).
  [AlturaT](depuracion/gao20260920/formal/AlturaT.lean): mismos resultados
  con altura T = σ∞; falta el impreso de Wu.
- **Ocelotas.** [83 rachas](depuracion/cst20260930/revision_rozier_20261016/REVISION.md)
  en Lean bajo LMN o Rhin y cobertura externa de Roosendaal hasta
  46645791847966786687 con tiempo clásico<=2480. Puente cobertura→CST
  formalizado; primer cruce finito supuesto. Originales LMN/Rhin cotejados;
  Rhin p.160: H>=2, exponente 13,3, sin factor adicional.
  Sin esa cobertura: [24 bajo LMN](depuracion/cst20260930/VEINTICUATRO_LEAN.md)
  y 40/41/42/46 con censos propios como hipótesis; 47 pendiente.

Axiomas Lean estándar; **revisión humana pendiente**. Llegada a 1 sólo
en las rachas construidas.

## Ruta y siguiente acción

[Colisiones](depuracion/perdices20261007/COLISIONES.md): recíprocos sumables
en órbitas positivas inyectivas; `R_k -> ξ`, `P_k -> infinito` (Garcia–Tal).
[Mínimos](depuracion/perdices20261007/MINIMOS.md) extrae reinicios de fuga pura
sin MuroA y demuestra `Collatz <-> MuroB y ausencia de circuitos no triviales`.
**Ambas abiertas.**

[Complejidad](depuracion/perdices20261007/COMPLEJIDAD.md) restringe repeticiones
y excluye paridades sturmianas para racionales de denominador impar
(antecedentes Dubickas 2009 y De Jesus). [Salidas](depuracion/perdices20261007/SALIDAS.md):
en `1/110`, `λ(n)<=3log2(n)+1` conjeturado; hasta 2^50, máximo 112;
auditoría independiente hasta 16 bits. Los
[empalmes H](depuracion/perdices20261007/RACHAS_H.md) transportan exactamente
el mínimo original.

**Recargas:** [ruta](depuracion/coherencia20260913/RUTA_339_20261012.md).
[Recargas](depuracion/perdices20261007/RECARGAS.md) y
[perfiles](depuracion/perdices20261007/PERFILES.md): refutadas pendiente<=1,
dependencia de valuaciones iniciales y rangos locales finitos.
[Transporte](depuracion/perdices20261007/TRANSPORTE_IMPAR.md): encaje Lean;
ell=ceil(log2(n+5)). [Filtros](depuracion/exploracionmath20261016/EXPLORACION.md).
[ABA](depuracion/perdices20261007/DOS_CAMBIOS.md) y
[BAB](depuracion/perdices20261007/ALTURA_BAB.md): epsilon=7/17 hasta dos cambios;
[tres](depuracion/perdices20261007/TRES_CAMBIOS.md): 1/13; K=2*ell.
Cierres Lean, enlaces escritos. Modelo excesivo de cuatro cambios
irrealizable módulo 9.
**Perdices, Codex:** [ruta y balance](depuracion/perdices20261007/congruencias_codex20261016/RUTA_CODEX.md).
P equivale al reloj uniforme; C>1 necesario. Hasta cuatro rachas,
L+v_fin<7*ell; coeficiente general geométrico. Bandas, defectos y límites
de las relajaciones conservados en la ruta; no contraejemplos orbitales.
[Ensayo global](depuracion/perdices20261007/congruencias_codex20261016/DENOMINADOR_GLOBAL.md):
2^L|q*n+r exacto; su barrera pierde utilidad en A B^b.
[Ventanas simultáneas](depuracion/perdices20261007/congruencias_codex20261016/VENTANAS_SIMULTANEAS.md):
óptimo conjunto desde la misma semilla. Un testigo de 53 pasos admite
n=23 en 1391 barreras expansivas; mínimo orbital 6416623. Falla la
integridad. Control: A B^b satisface L<=ell+1. CRT reconstruye exactamente
el cilindro. **Pendiente:** acotar uniformemente sus representantes,
excluyendo recorridos racionales; las mismas barreras no bastan.
Reloj y P abiertos; A/B no bastaría para Collatz. Sin mecanismo nuevo,
no lanzar otra corrida larga.
[Claude](RutaDeJudasIscariote.md): [J2](depuracion/judas20261016/J2_MECANISMOS.md)
sin mecanismo publicado. En Lean, el piloto equivale a la parada de G, entre
Mahler y la 4.14. [Mensaje YAH](depuracion/judas20261016/escalera/yah/PENDIENTES.md)
del 19-10: mezcla resistente, no prueba de imposibilidad; tandas según
esa nota, sin intervenirlas.

## Revisión y publicación

[Revisión Rozier](depuracion/cst20260930/revision_rozier_20261016/REVISION.md):
83 con dos cierres, cola Rhin 2^68 frente a LMN 2^76; cobertura externa
no reproducida. Rhin original cotejado, prueba sin formalizar.
Simons (2022) es antecedente cercano, prioridad pendiente.
[Plan B](depuracion/cst20260930/revision_rozier_20261016/PLAN_RESPUESTA.md):
esperar avance considerable y nuevo paper; luego responder todas sus preguntas.
Gao/Wu/Garner por valorar. Borrador sin enviar; commit/push de esa revisión autorizados.

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y Wu;
[prioridad](papers/revision20260927/REVISION.md#4-novedad), MathSciNet,
Scholar e impreso de Wu. **No anunciar, enviar a OEIS ni contactar sin autorización.**

[Artículos](papers/README.md): II y III libres tras
AFM; I en [JAR](papers/jar/LEEME.md), sin noticias
al 04-10; IV sin enviar. [Qeios](papers/qeios/LEEME.md) retirado;
[Palomar](papers/palomar/LEEME.md) verifica Gao; Zulip borrado.
OEIS A078441, A400486 y A400487 aprobadas: no validan pruebas.
[Próxima sesión OEIS](papers/oeis/PENDIENTE_20261010.md): dos correcciones y
una sucesión, pendientes del panel.

## Evidencia y conservación

[Arca](depuracion/mapa20261011/MapaDependenciasComplex.html): 70 nombres,
123 piezas; [auditoría](depuracion/mapa20261011/RECONSTRUCCION.md).
[Registro versionado](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`: **360 filas**, 246 demostradas, 92 medidas,
13 conjeturadas y nueve refutadas; undécima alta Codex integrada,
359 previas conservadas literalmente; SQLite cotejado.
Incidencia histórica de la fila 71 señalada y no usada.

Lean 4.32.2/Mathlib fijados: [reproducción](depuracion/gao20260920/formal/README.md).
[Evidencia Rozier](depuracion/cst20260930/evidencia_rozier.json) y
[cotejo](depuracion/cst20260930/revision_rozier_20261016/cotejo_numeros.json).
Perdices: [152 consultas Lean únicas](depuracion/perdices20261007/congruencias_codex20261016/evidencia_sesion.json).
Ventanas: 1023 palabras, 33 miembros y 34 testigos; 10954 cortes CRT
cotejados, censo sin repetir. Extracción general y CRT escritos.
[Casa recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md) y
[conciliación](depuracion/jinetas20261010/CONCILIACION.md): dos huellas antiguas
por revisar; no usar sus cachés. Históricos, conversaciones y zootheorem intactos.
