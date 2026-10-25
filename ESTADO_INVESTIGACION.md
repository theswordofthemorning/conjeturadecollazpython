# Estado para continuar — 25-10-2026

[Premisa](PREMISA_DE_INVESTIGACION.md): buscar la prueba universal de Collatz;
la convicción del usuario no sirve como hipótesis matemática.

## Decisión estratégica

El usuario **retiró el objetivo de Perdices**; la investigación quedó detenida.
El [balance global](depuracion/balance20261025/BALANCE.md) recomienda pausar
la búsqueda universal con los métodos actuales; no es decisión del usuario
ni prueba de agotamiento. Se ensayan propuestas acotadas. Sin mecanismo
de cierre identificado ni probabilidad de éxito estimada.

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
  bajo LMN o Rhin y cobertura externa hasta 46645791847966786687 con
  tiempo clásico <=2480. Primer cruce finito supuesto; cobertura no
  reproducida. Sin ella: 24 bajo LMN; 40/41/42/46 bajo censos propios.
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

[Perdices/protegidos](depuracion/perdices20261025/PROTEGIDOS.md) acota G y
limita el certificado de mezcla. Después,
[Sesgo de frontera](depuracion/perdices20261025/SESGO_FRONTERA.md) demuestra
que la ley final bajo supervivencia en todos los prefijos **no converge
a ninguna ley fija**, ya módulo 3; TV>=1/36864 en una proporción positiva
de horizontes. Es ley poblacional, no temporal de una semilla.
Prueba escrita y contrastes exactos; Lean certifica la inyección completa
de palabras y su cardinalidad. Cuentas orbitales, densidad de horizontes
y conclusión de medidas siguen sin formalización completa.
[Criterio temporal](depuracion/perdices20261025/FRECUENCIAS_TEMPORALES.md):
K>=163 y TV<=1/100 para las frecuencias de una misma órbita módulo 9
fuerzan cruce; implicación desde tres cotas marginales formalizada.
La hipótesis excepcional sigue abierta y el balance admite el testigo
racional 23. [Extensión ternaria](depuracion/perdices20261025/OBSERVABILIDAD_TERNARIA.md):
balance orbital para todo m en Lean; ambigüedad exacta de flujos escrita.
[Retornos aritméticos](depuracion/perdices20261025/RETORNOS_ARITMETICOS.md):
tramos enteros crecientes conservan observaciones fijas; descartan rangos
monótonos en tamaño dentro de ellas. Caso 231->391 en Lean; CRT general
escrito. Siguiente: control individual que supere esas plantillas.
La [ampliación digital](depuracion/perdices20261025/borradores/LEEME.md)
queda como borrador sin integrar.

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

[Nashida](depuracion/ccchallenge20261019/NASHIDA_ANALIZAR.md): lectura
estratégica de seis trabajos realizada el 25-10, commits remotos cotejados.
Barreras específicas y densidad; sin puente universal aplicable.
El [balance](depuracion/balance20261025/BALANCE.md) corrige extrapolaciones:
G no es H. Auditoría completa y recompilación externa pendientes.

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
365 filas, 251 demostradas, 92 medidas, 13 conjeturadas, nueve refutadas;
incidencia histórica de fila 71 señalada y no usada.

[Controles del balance](depuracion/balance20261025/evidencia.json):
GaoLiteral, GarnerEnunciado y WuEnunciado recompilados; cinco consultas
sin sorryAx. Ventanas recalculadas; manifiestos de 48/94 entradas cotejados.
Sin censos ni reconstrucción completa de dependencias.
[Evidencia Ocelotas](depuracion/cst20260930/evidencia_rozier.json) y
[Perdices](depuracion/perdices20261007/congruencias_codex20261016/evidencia_sesion.json)
conservadas. [Casa recuperada](depuracion/casa20261005_recuperada/RECUPERACION.md)
y [conciliación](depuracion/jinetas20261010/CONCILIACION.md): dos huellas
antiguas pendientes; no usar sus cachés.
[Cinco altas y conservación](depuracion/perdices20261025/evidencia_registro.json):
360 afirmaciones anteriores intactas; catálogo y mapa ampliados mediante
el generador. Respuestas, históricos y zootheorem intactos.
