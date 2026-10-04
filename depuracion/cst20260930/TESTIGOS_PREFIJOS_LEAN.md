# Ocelotas: certificados que explicitan el motivo de cada hoja

03-10-2026. El verificador y su corrección están formalizados. La
ventana de 76 ya se evaluó con esta representación; el
[cierre de 77](SETENTA_Y_SIETE_LEAN.md) también quedó aceptado.
No se añaden hipótesis matemáticas ni se atribuye novedad
histórica a esta forma de presentar certificados.

## Contrato

Se conservan el atajo T, los contadores de entradas impares y rachas,
y el estado `n=r+m*u`, `T^i(n)=a*u+c`. El combustible cuenta pasos
restantes del atajo. La clase se restringe a semillas <=L.
El árbol de [OcelotasCertificadosTestigos.lean](OcelotasCertificadosTestigos.lean)
contiene cinco constructores:

| Motivo propuesto | Condición comprobada |
|---|---|
| Vacío | L<r |
| Descenso | a<m y c<r |
| Exceso de rachas | m<=a y R<s |
| Criba con exponente B | m<=a, entrada anterior par, `(X+1)^256<=2^B` y `q+C(B,R-s)<qmin`, con `X=a*floor((L-r)/m)+c` |
| Rama | m<=a y aceptación de ambos hijos, separando u par e impar |

El combustible cero siempre rechaza. Un exponente incorrecto, un corte
inválido o una hoja sin justificación no permiten aceptar. B puede ser
una cota superior conservadora; no es necesario que sea mínimo.

`verificar_correcto` demuestra por inducción en el combustible que
aceptar este árbol implica aceptar el verificador binario anterior,
para el mismo estado. El teorema `descenso` conecta la raíz con una
órbita concreta, bajo primer cruce finito, hasta R rachas y al menos
qmin entradas impares. No necesita LMN ni Rozier–Terracol.
La [auditoría](evidencia_certificados_testigos.json) contiene seis módulos
nuevos, 22 consultas y 27 módulos de base; axiomas estándar, sin `sorryAx`.

## Generación y división

[generar_testigos_prefijos_lean.py](generar_testigos_prefijos_lean.py)
reproduce la exploración con enteros, verifica todos los conteos y la
huella de hojas contra el certificado y su cotejo independiente, y
genera subárboles de hasta 2000 nodos. Las partes agrupan hasta 20000
nodos evaluados. Sus teoremas se obtienen con `decide +kernel` y el lema
de corrección; `acepta_rama` une las partes sin repetir sus evaluaciones.

La [prueba piloto de 76](OcelotasSetentaYSeisTestigos.lean) usa 49
subárboles y 48 uniones: los mismos 11225 nodos y la misma cobertura del
certificado ya cotejado. La [auditoría](evidencia_testigos_76.json) compila
ocho módulos nuevos, con 73 consultas. En esta ejecución la parte de
certificados tomó 54,412 segundos y la unión 19,434; hubo otros procesos
activos, por lo que no es una comparación controlada de velocidades.

La [generación de 77](generacion_OcelotasSetentaYSietePrefijos.json)
propone 4896 subárboles y 4895 uniones en 73 partes. Su suma reproduce
exactamente los 1420851 nodos y la huella del cotejo independiente.
Las fuentes generadas por sí solas no certifican su aceptación en Lean.

## Conservación de lo comprobado

[comprobar_extension_persistente.py](comprobar_extension_persistente.py)
valida el prefijo anterior y conserva cada nuevo módulo aceptado junto
con las huellas de fuente, objeto y dependencias, el entorno y la
auditoría de axiomas. Guarda el manifiesto después de cada módulo con
reemplazo atómico. Al terminar vuelve a comprobar todas las fuentes y
objetos. El manifiesto final de éxito sólo se escribe al completar la cadena.

La [prueba de reutilización](evidencia_reutilizacion_testigos_76.json)
recuperó los ocho módulos, con cero recompilaciones y 73 consultas
originales conservadas. Usar una sola ejecución por directorio de
extensiones. Este directorio es distinto del de la comprobación de 22.

La cadena de 77, sesión **64800**, terminó con código 0. La
[salida completa](evidencia_setenta_y_siete.txt) y la
[evidencia final](evidencia_setenta_y_siete.json) aceptan 91 módulos
de extensión: 85 compilados y seis reutilizados, 5030 consultas
estándar sin `sorryAx`. Las fuentes y objetos se cotejaron después.
Antes de reanudar cualquier otra cadena hay que consultar su proceso;
un manifiesto parcial no acredita por sí solo el teorema final.

```text
python -B -X utf8 depuracion/cst20260930/generar_testigos_prefijos_lean.py --certificado depuracion/cst20260930/prefijos_77_afinados_5m.json --cotejo depuracion/cst20260930/cotejo_prefijos_77_afinados.json --espacio OcelotasSetentaYSietePrefijos --directorio depuracion/cst20260930 --nodos-subarbol 2000 --nodos-modulo 20000
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasSetentaYSiete --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_testigos_20261003 --salida depuracion/cst20260930/evidencia_setenta_y_siete.json
```
