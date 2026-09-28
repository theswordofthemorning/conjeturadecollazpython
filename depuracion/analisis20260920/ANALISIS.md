# Diagn?stico hist?rico del laboratorio ? 20-09-2026

Informe original, conservado [?ntegro](../../archivo/contexto_20260928/analisis20260920_ANALISIS.md.txt), con su [evidencia](evidencia.json). Se revis? el commit a0bf045; las cifras y pendientes de esa fecha no describen por s? solos el estado actual. Para continuar la investigaci?n, abrir [ESTADO_INVESTIGACION.md](../../ESTADO_INVESTIGACION.md) y el [plan vigente](../transversal20260927/PLAN_SESIONES_20260928.md).

El diagn?stico detect? tres riesgos operativos: guardarhilos.py eliminaba la base antes de reconstruirla; algunos m?dulos lanzaban barridos al importarse; clasesparalelo.py pod?a desbordar np.int64 al ampliar el rango a k=40. El informe ?ntegro contiene testigos, l?mites de las verificaciones y rutas de reparaci?n. No se ha reexaminado aqu? si esos riesgos siguen abiertos.
