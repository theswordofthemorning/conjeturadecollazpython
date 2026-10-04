# Ocelotas: preparación y cotejos del cierre de 77

03-10-2026. **La propuesta quedó aceptada en Lean:** véase el
[cierre de 77](SETENTA_Y_SIETE_LEAN.md), con sus hipótesis y auditoría.
Esta ficha conserva la preparación y los cotejos independientes.
El cierre anterior de [76 rachas](SETENTA_Y_SEIS_LEAN.md) se conserva.

## Alcance propuesto

Se mantienen T(n)=n/2 para n par y (3n+1)/2 para n impar, n>=2 y
primer cruce existente y finito. q cuenta las entradas impares y las
rachas son sus bloques maximales, hasta ese primer cruce. No hay ley
probabilística ni nuevo censo.

La [tabla propuesta](preparacion_setenta_y_siete.json), generada por
[preparar_setenta_y_siete.py](preparar_setenta_y_siete.py), tiene 97 filas:
91 remiten al rango externo, cinco se excluyen por criba y una requiere
el certificado de prefijos. El corte es q<4857481135601629720741.
La cola propuesta usa R=77, A=8691353499027139, c=7, H=72.

La fila 91 cubre 130441933147714940<=q<397560349370386783 y exige tratar
el intervalo inclusivo:

```text
28000000000000000001 <= n <= 42938293471394771272,
q >= 130441933147714940, rachas <= 77, combustible = 256.
```

## Evidencia finita

El primer ensayo, [limitado a un millón de nodos](prefijos_77_afinados_1m.json),
fue inconcluso. Se conserva. El [ensayo posterior](prefijos_77_afinados_5m.json)
terminó en 1420851 nodos, profundidad máxima 81, con 58 hojas de descenso,
574299 hojas de criba y 136069 clases vacías. No dejó pendientes.
Las 574357 clases no vacías cubren exactamente 14938293471394771272
semillas. La huella de hojas es
`a8711ea0246c5cf1d3ca3ff5a6b07e5cf984176e41b50bf22adde5004701aedc`.

El [cotejo de prefijos](cotejo_prefijos_77_afinados.json) reconstruye
órbitas directas, comprueba otro representante por hoja, calcula la
cota con `Fraction` y verifica cobertura disjunta. El
[cotejo de tabla](cotejo_setenta_y_siete.json), mediante
[otro programa](cotejar_setenta_y_siete.py), comprueba series racionales
de logaritmos, determinantes, continuidad, pisos, potencias, parámetros
de cola y el enlace con la ventana. Ambos terminaron sin discrepancias.

La preparación se reprodujo byte a byte en una carpeta temporal.
Estos controles finitos no sustituyen la evaluación ni la prueba
ensamblada en Lean. LMN y el rango de Rozier–Terracol seguirán siendo
hipótesis externas explícitas en el cierre aceptado.

## Construcción de los certificados y cierre

Se generaron certificados que proporcionan el exponente B en las hojas de
criba. Lean comprueba `s^256<=2^B` y la recurrencia entera. En
las ramas internas se comprueba m<=a y se unen los certificados de
ambos hijos, evitando recalcular la criba. Los seis lemas de
[OcelotasPrefijosTestigos.lean](OcelotasPrefijosTestigos.lean) ya fueron
aceptados: la [auditoría](evidencia_prefijos_testigos.json) contiene cinco
módulos nuevos, 20 consultas, axiomas estándar y ningún `sorryAx`.
Queda un aviso de simplificación redundante, sin efecto en el enunciado.
La continuación generó el [certificado de 77](OcelotasSetentaYSietePrefijos.lean)
mediante un árbol con esos motivos: 4896 subárboles y 4895 uniones,
en 73 partes. Se generaron también la
[tabla Lean](OcelotasSetentaYSieteTabla.lean) y el
[ensamblaje final](OcelotasSetentaYSiete.lean). La cadena completa terminó
con código 0, con objetos persistentes; véase la
[ficha de certificados y reanudación](TESTIGOS_PREFIJOS_LEAN.md).
La [auditoría final](evidencia_setenta_y_siete.json) acepta 91 módulos
de extensión, 85 compilados y seis reutilizados, con 5030 consultas
de axiomas estándar y sin `sorryAx`.

```text
python -B -X utf8 depuracion/cst20260930/explorar_prefijos_racionales.py --inicio 28000000000000000001 --limite 42938293471394771272 --q-min 130441933147714940 --rachas 77 --combustible 256 --criba afinada --max-nodos 5000000 --salida depuracion/cst20260930/prefijos_77_afinados_5m.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos_afinados.py --certificados depuracion/cst20260930/prefijos_77_afinados_5m.json --salida depuracion/cst20260930/cotejo_prefijos_77_afinados.json
python -B -X utf8 depuracion/cst20260930/preparar_setenta_y_siete.py --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/preparacion_setenta_y_siete.json
python -B -X utf8 depuracion/cst20260930/cotejar_setenta_y_siete.py --certificado depuracion/cst20260930/preparacion_setenta_y_siete.json --prefijos depuracion/cst20260930/prefijos_77_afinados_5m.json --cotejo-prefijos depuracion/cst20260930/cotejo_prefijos_77_afinados.json --salida depuracion/cst20260930/cotejo_setenta_y_siete.json
```
