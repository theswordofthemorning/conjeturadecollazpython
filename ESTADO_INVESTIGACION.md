# Estado para continuar — 26-10-2026

[Premisa](PREMISA_DE_INVESTIGACION.md): buscar la prueba universal de Collatz;
la convicción del usuario no sirve como hipótesis matemática.

## Decisión estratégica

**Objetivo automático retirado por el usuario; continuación autónoma detenida.**

El usuario **reactivó Perdices** hasta agotar la ruta o alcanzar una de las
[tres condiciones documentadas](depuracion/balance20261025/BALANCE.md#condiciones-para-reabrir-la-búsqueda):
control aritmético nuevo para una semilla fija con cambios arbitrarios;
transferencia de mezcla a órbitas excepcionales; o resultado externo que
cierre una premisa universal con nuestros cuantificadores. **Ninguna se ha
alcanzado.** El balance recomienda pausa con los métodos actuales; no
demuestra agotamiento ni impide esta exploración autorizada.

## Resultados y límites

- **Gao:** [Tejonas](depuracion/gao20260920/Tejonas.md) y
  [Hienas](depuracion/gao20260920/Hienas.md), coalescencia en densidad 1;
  no llegada a 1. [Cigarras](depuracion/gao20260924/Cigarras.md): ritmo lento.
- **Garner/Wu:** [Alpacas](depuracion/garner20260926/Alpacas.md), rachas
  convergentes arbitrariamente largas y altas. Wu 2 demostrado;
  [Wu 1](depuracion/gao20260920/formal/WuEnunciado.lean) equivale a
  convergencia en densidad natural 1 y sigue abierto.
  [AlturaT](depuracion/gao20260920/formal/AlturaT.lean) cubre altura T;
  falta el [impreso de Wu](papers/revision20260927/cnki_wu_20261017.md).
- **Ocelotas:** [83 rachas](depuracion/cst20260930/revision_rozier_20261016/REVISION.md)
  bajo LMN o Rhin y cobertura externa no reproducida; primer cruce
  finito supuesto. Sin ella: 24 bajo LMN; 40/41/42/46 bajo censos propios.
  No cubre rachas arbitrarias.
- **Perdices:** [Colisiones](depuracion/perdices20261007/COLISIONES.md)
  da recíprocos sumables y producto tendiendo a infinito en órbitas
  positivas inyectivas (antecedente Garcia–Tal).
  [Mínimos](depuracion/perdices20261007/MINIMOS.md) demuestra
  `Collatz <-> MuroB y ausencia de circuitos no triviales`.
  **Ambas condiciones siguen abiertas.**

Axiomas Lean estándar no eliminan las hipótesis de cada teorema.
Revisión humana y prioridad pendientes.

## Frentes abiertos

[Protegidos](depuracion/perdices20261025/PROTEGIDOS.md) limita el certificado.
[Sesgo de frontera](depuracion/perdices20261025/SESGO_FRONTERA.md) demuestra
**no convergencia poblacional a ley fija** bajo supervivencia, ya módulo 3.
Prueba escrita; Lean certifica la inyección, no todas las medidas.
[Criterio temporal](depuracion/perdices20261025/FRECUENCIAS_TEMPORALES.md):
K>=163 y TV<=1/100 módulo 9 fuerzan cruce, pero la hipótesis excepcional
sigue abierta. [Balance ternario](depuracion/perdices20261025/OBSERVABILIDAD_TERNARIA.md)
para todo m en Lean; admite todavía al testigo racional 23.
[Retornos aritméticos](depuracion/perdices20261025/RETORNOS_ARITMETICOS.md):
descartan rangos monótonos en tamaño por observaciones fijas.
[Pesos binarios](depuracion/perdices20261026/PESOS_BINARIOS.md) completa el
borrador: variaciones ilimitadas de ambos signos descartan ambas
monotonías. Prueba general escrita; caso concreto en Lean.
[Límites reales](depuracion/perdices20261026/LIMITES_REALES.md): ejemplos
-3/2 y -2 concretan el fallo de transporte de López–Stoll, sin refutar
su teorema principal. [Precisión creciente](depuracion/perdices20261026/PRECISION_CRECENTE.md)
recupera el cilindro; el control sigue siendo el reloj pendiente.
[Trazas matriciales H](depuracion/perdices20261026/TRAZAS_MATRICES.md):
conexión bidireccional fuerza seis igualdades; se excluye `M_a=M_b=tI`
con constantes libres. [F invertible, A≠B](depuracion/perdices20261026/CLASIFICACION_F_INVERTIBLE.md):
dos formas de rango uno y resonancia 2:3; prueba escrita y núcleos Lean.
Sus constantes generales siguen abiertas. UNSAT 0/1 y timeout 0..3 no
prueban imposibilidad general.

[Perdices/Codex](depuracion/perdices20261007/congruencias_codex20261016/RUTA_CODEX.md):
reloj uniforme y presupuesto P abiertos; hasta cuatro rachas hay cota,
pero el coeficiente general crece geométricamente. A/B no bastaría para
Collatz. [Ventanas simultáneas](depuracion/perdices20261007/congruencias_codex20261016/VENTANAS_SIMULTANEAS.md):
1391 barreras de tamaño aceptan 23; la menor semilla orbital es 6416623.
CRT recupera el cilindro; falta controlar sus representantes uniformemente.
[Recargas](depuracion/coherencia20260913/RUTA_339_20261012.md) y
[complejidad](depuracion/perdices20261007/COMPLEJIDAD.md) delimitan restricciones,
sin excluir concatenaciones arbitrarias.

[Judas/J2](depuracion/judas20261016/J2_MECANISMOS.md): paridades ↔ no parada
de G formalizado; SRS ↔ G escrito, sin formalización completa.
[YAH](depuracion/judas20261016/escalera/yah/INFORME_YAH.md):
G, G_A2 y G_B4 sin QED. UNSAT limitado a plantillas ensayadas;
MAYBE y tiempos agotados no prueban imposibilidad.

[Nashida](depuracion/ccchallenge20261019/NASHIDA_ANALIZAR.md): seis trabajos
revisados el 25-10, sin puente universal aplicable. G no es H.
Auditoría completa y recompilación externa pendientes.

## Revisión y publicación

[Pendientes humanos](gaopendientes.md), [prioridad](papers/revision20260927/REVISION.md#4-novedad)
y [Rozier](depuracion/cst20260930/revision_rozier_20261016/PLAN_RESPUESTA.md):
esperar avance considerable antes de responder; borrador sin enviar.
[Artículos](papers/README.md): II/III libres tras AFM;
I en [JAR](papers/jar/LEEME.md), sin noticias registradas al 04-10; IV sin enviar.
[Qeios](papers/qeios/LEEME.md) retirado;
[Palomar](papers/palomar/LEEME.md) verifica Gao; Zulip borrado.
OEIS A078441, A400486 y A400487 aprobadas no validan pruebas;
[correcciones pendientes](papers/oeis/PENDIENTE_20261010.md).
No anunciar, enviar ni contactar sin autorización.

## Evidencia y conservación

[Arca](depuracion/mapa20261011/MapaDependenciasComplex.html): 70 nombres,
123 piezas, nueve ramas. [Registro](depuracion/coherencia20260913/registro.json):
369 filas, 255 demostradas, 92 medidas, 13 conjeturadas, nueve refutadas;
incidencia histórica de fila 71 señalada y no usada.

[Controles del balance](depuracion/balance20261025/evidencia.json): auditoría focalizada.
[Evidencia Ocelotas](depuracion/cst20260930/evidencia_rozier.json) y
[Perdices](depuracion/perdices20261007/congruencias_codex20261016/evidencia_sesion.json)
conservadas. [Casa recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md)
y [conciliación](depuracion/jinetas20261010/CONCILIACION.md): dos huellas
antiguas pendientes; no usar sus cachés.
[Alta y conservación](depuracion/perdices20261026/evidencia_registro.json):
365 afirmaciones anteriores intactas; catálogo y mapa ampliados mediante
el generador. Respuestas, históricos y zootheorem intactos.

[Auditoría de parada](depuracion/perdices20261026/AUDITORIA_RUTA.md):
no declarar agotamiento. [Último borrador](depuracion/perdices20261026/CONSTANTES_F_INVERTIBLE.md):
argumento de numerales y ocho núcleos Lean comprobados, sin integrar en
el registro. Si se retoma: revisar e integrar antes de pasar a F singular,
A=B no escalar o ausencia de conexión. No ampliar timeouts.
