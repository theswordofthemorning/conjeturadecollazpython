# Estado para continuar — 16-10-2026

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
  Falta cotejar el original de Wu, consultado mediante CNKI AI.
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
(antecedente De Jesus). [Salidas](depuracion/perdices20261007/SALIDAS.md):
en `1/110`, `λ(n)<=3log2(n)+1` sigue conjeturado; hasta 2^50, máximo 112,
con auditoría independiente completa hasta 16 bits. Los
[empalmes H](depuracion/perdices20261007/RACHAS_H.md) transportan exactamente
el mínimo original.

[Matrices](depuracion/perdices20261007/SOPORTES_MATRICES_H.md): diez soportes;
familias excluidas, objetivo 57 sin dinámica. Árticas y persistencia abiertas.

**Piloto de recargas:** [ruta](depuracion/coherencia20260913/RUTA_339_20261012.md).
[Recargas](depuracion/perdices20261007/RECARGAS.md) refuta K=alpha*ell+beta
para alpha<=1 y beta>=0, y presupuestos de las dos valuaciones iniciales.
Prueba escrita; caso n=4591 con epsilon=1/2,K=ell certificado en Lean.
[Perfiles](depuracion/perdices20261007/PERFILES.md) excluye rangos locales
`H(x)+F(perfil)`, H no decreciente, para listas finitas de valuaciones afines:
prueba general escrita, caso x+1,x+5 formalizado.
[Transporte impar](depuracion/perdices20261007/TRANSPORTE_IMPAR.md):
encaje universal certificado en Lean; `Eeta<=2*ell(n)` con hasta un cambio,
por escrito, ell=ceil(log2(n+5)). Las partes impares no son monótonas.
La [exploración de math](depuracion/exploracionmath20261016/EXPLORACION.md)
conserva la ruta y aporta filtros. [Dos cambios](depuracion/perdices20261007/DOS_CAMBIOS.md):
**P2 probado para toda A^a B^b A^c**. [Altura BAB](depuracion/perdices20261007/ALTURA_BAB.md):
P con epsilon=7/17,K=2*ell para hasta dos cambios; fallo de P2 en BAB
exigiría calidad abc>18, sin descartarlo ni suponer abc.
[Tres cambios](depuracion/perdices20261007/TRES_CAMBIOS.md): **P probado con
epsilon=1/13,K=2*ell para hasta tres cambios**. Cierres Lean; enlaces y cotas
orbitales escritos. Con cuatro cambios, las cotas y el balance admiten un
modelo que viola incluso epsilon=0, pero una congruencia módulo 9 lo hace
irrealizable: no es un contraejemplo orbital.
**Siguiente:** control acumulativo de congruencias desde la misma semilla.
Presupuesto global y descenso abiertos. H auxiliar. **Tanda publicada en
972c111. Próxima sesión: retomar el piloto desde ese punto.** La revisión
para Rozier queda comprobada y documentada; este cierre no inicia otra tanda.

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
Scholar y Garner original. **No anunciar, enviar a OEIS ni contactar sin autorización.**

[Artículos](papers/README.md): II y III libres tras
[AFM](papers/CORREOS_20261004.md); I en [JAR](papers/jar/LEEME.md), sin noticias
al 04-10; IV sin enviar. [Qeios](papers/qeios/LEEME.md) retirado;
[Palomar](papers/palomar/LEEME.md) verifica Gao; [Zulip](papers/qeios/ZULIP_borrador.md) borrado.
OEIS A078441, A400486 y A400487 aprobadas: no validan pruebas.
[Próxima sesión OEIS](papers/oeis/PENDIENTE_20261010.md): dos correcciones y
una sucesión, sin enviar y sujetas al panel.

## Evidencia y conservación

[Arca](depuracion/mapa20261011/MapaDependenciasComplex.html): 70 nombres,
123 piezas; [auditoría](depuracion/mapa20261011/RECONSTRUCCION.md).
[Registro versionado](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`: **349 filas**, 235 demostradas, 92 medidas,
13 conjeturadas y nueve refutadas; cotejo literal con SQLite.
Incidencia histórica de la fila 71 señalada y no usada.

Lean 4.32.2 y Mathlib fijado; [reproducción](depuracion/gao20260920/formal/README.md).
[Evidencia Rozier](depuracion/cst20260930/evidencia_rozier.json): 146 consultas
Lean estándar; [cotejo exacto](depuracion/cst20260930/revision_rozier_20261016/cotejo_numeros.json).
Perdices conserva ocho cierres Lean; congruencia y enlaces orbitales escritos.
[Casa recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md) y
[conciliación](depuracion/jinetas20261010/CONCILIACION.md): dos huellas antiguas
requieren revisión; no usar sus cachés. Históricos, conversaciones y zootheorem intactos.
