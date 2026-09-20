# Continuidad después de compactar — 20-09-2026

## Petición y situación de la sesión

El usuario pidió analizar primero el laboratorio y después `zootheorem`.
Ambos análisis están terminados. **La última autorización es sólo análisis**;
la fase de investigación comenzará cuando el usuario la indique. No interpretar
los antiguos pedidos de commit/push o edición OEIS como una tarea actual.
El usuario ejecutará `/compact`; no se ha forzado una compactación desde herramientas.

Informes: [laboratorio](ANALISIS.md), [publicación](ANALISIS_ZOOTHEOREM.md).
Evidencia: [laboratorio](evidencia.json), [publicación](evidencia_zootheorem.json).
Se escribieron únicamente notas de análisis y el estado breve del laboratorio;
los programas, bases, datos, papers y drafts conservan sus contenidos.

## Entradas mínimas y repositorios

- Laboratorio: `C:/Users/Home/Desktop/conjeturadecollazpython`.
  Abrir [ESTADO_INVESTIGACION.md](../../ESTADO_INVESTIGACION.md) tras sus reglas.
- Publicación: `C:/Users/Home/Desktop/zootheorem`.
  Abrir [PLAN_INVESTIGACION.md](../../../zootheorem/PLAN_INVESTIGACION.md).
- Son repositorios Git separados. Bases revisadas: laboratorio `a0bf045`,
  publicación `5e03432`. No se hicieron commits ni push. `zootheorem` quedó
  limpio; las notas y la actualización de estado permanecen locales en el laboratorio.
- Trabajar sin subagentes salvo petición expresa. No precargar históricos,
  conversaciones o bases completas, ni importar experimentos sin revisar su entrada.

## Objeto y distinciones que no se pueden perder

Objetivo matemático: `phi=lim a(n)/2^n=1`. Mapa de investigación:
`T(x)=x/2` si par y `(3x+1)/2` si impar; el CLI usa el clásico.
`a(n)` cuenta clases balanceadas hasta n, y nuevas en n son
`a(n)-2*a(n-1)`. OEIS A398793 usa `b(n)=a(n+1)-2*a(n)`.

Para su unión F sólo está establecida `densidad inferior(F)>=phi`.
Fusión balanceada no da por sí sola alturas finitas iguales ni convergencia.
En la cadena `{v,3^k*v+c}`, el bit es paridad del ancla; c conserva su signo.
La excursión parte de `(2,c0)` con bits justos independientes; tau es primera
llegada a k=1, no absorción del par. El estado `(1,1)` con bit 1 sí funde.

## Ruta matemática al recibir autorización para investigar

1. **P1 primero:** abrir [Matematica.md, §3](../coherencia20260913/Matematica.md#3-corolario-del-reloj-de-mangostas-y-gacelas).
   Mangostas/Gacelas dan la cola interior uniforme
   `P(tau>t)<=C sqrt(log(t+2)/(t+1))`. Falta integrar frontera k=0,1:
   declarar entradas, salidas, reinicios y dependencia del estado inicial.
   Contrastar con `cadenakc.lean` y `estratoscadena.py:transicion`.
2. **P2 después:** en la misma nota, §4, `u_tau=Pi_tau*u0+W_tau`, u0=c0/9.
   Pi está controlado. Falta M finito y p>0 uniformes con
   `P(|W_tau|<=M | tau>T(c0))>=p` para un horizonte logarítmico declarado,
   o una familia que refute esa uniformidad. Probar signos, bordes y semillas
   adversarias; distinguir supervivencia, salida y censura.
3. **P3:** arranques reales y divergencia de riesgos condicionales; justificar
   Markov fuerte y Borel–Cantelli sin asumir la recurrencia buscada.

No adoptar el reloj O(n) medido de la revisión 12. Erizas descarta contracción
uniforme en todas las escalas, no toda estrategia de escala fija. El paper 03
controla momentos a tiempo fijo: no trasladarlos a salida condicionada sin prueba.

## Verificaciones y pendientes ajenos al cierre matemático

Laboratorio: 210 Python y 34 JSON válidos; ocho controles Python y ocho Lean
pasaron. Publicación: cuatro verificadores y el espejo Lean pasaron; programas
OEIS contrastados hasta 13. Lean 4.32.2, sin `sorryAx` en las salidas revisadas.

Riesgos documentados, aún sin reparar: borrado previo de `hilos.db`, barridos al
importar y desbordamiento NumPy en k=40; en publicación, comentario excesivo
sobre ciclos, dos verificadores sin guardia y errata decimal menor. No confundir
estos mantenimientos con los obstáculos P1–P3.

OEIS: conservar el estado fechado del 17-09; no se revisó en vivo ahora.
Hay correcciones preparadas y tres propuestas en el último registro. Publicar
requiere una tarea posterior, no forma parte de esta entrega de análisis.
