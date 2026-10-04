# Ocelotas: evaluación del exponente por bisección

03-10-2026. Optimización de la [criba afinada](PREFIJOS_AFINADOS_LEAN.md).
El exponente y el contrato matemático se conservan. No se atribuye novedad
histórica a la búsqueda binaria.

## Cálculo y justificación

El verificador anterior calcula el menor B con `s^256<=2^B` mediante
`log2(s^256-1)+1`, con B=0 para s<=1. En la ventana de 76, s tiene
alrededor de 67 cifras binarias y s^256 unas 17000.

[OcelotasPrefijosBinarios.lean](OcelotasPrefijosBinarios.lean) empieza
por `inferior=256*log2(s)` y `superior=inferior+256`. Si la potencia ya
cabe en el extremo inferior, devuelve ese extremo. En otro caso hace
ocho bisecciones. En cada una conserva `s^256<=2^superior`.
`buscar_cota` prueba este invariante con cualquier combustible;
`potencia_exponente` prueba la cota resultante para todo s, incluidos 0 y 1.
La regla tras un corte se obtiene de la misma criba real existente.

[OcelotasExponenteBinarioExacto.lean](OcelotasExponenteBinarioExacto.lean)
demuestra además:

- `techo_equiv`: el exponente anterior es <=b si y sólo si `s^256<=2^b`;
- `buscar_exacto`: una anchura inicial <=2^f permite recuperar el mínimo
  con f bisecciones, si el extremo inferior está estrictamente por debajo;
- `exponente_igual`: los dos procedimientos devuelven exactamente el
  mismo entero para toda entrada.

La [auditoría de esta igualdad](evidencia_exponente_binario_exacto.json)
compila tres módulos, con 12 consultas y 27 módulos anteriores
reutilizados por huellas. Lean 4.32.2, axiomas estándar, sin `sorryAx`.

[OcelotasVerificadoresEquivalentes.lean](OcelotasVerificadoresEquivalentes.lean)
prueba por inducción en el combustible que los verificadores completos
devuelven el mismo booleano para cualquier estado, incluso si no representa
una órbita. Su [auditoría](evidencia_verificadores_equivalentes.json)
contiene seis módulos nuevos, 17 consultas y el mismo prefijo de 27.

## Certificado concreto

El [verificador binario](OcelotasCribaPrefijosBinarios.lean) conserva las
transiciones de clases y demuestra otra vez `comprobar_correcto` y
`certificado_descenso`. Sólo sustituye el cálculo del exponente.

El [certificado de la ventana de 76](OcelotasSetentaYSeisPrefijosBinarios.lean)
ya fue aceptado por `decide +kernel`. Su [auditoría](evidencia_prefijos_76_binarios.json)
contiene cuatro módulos nuevos, 13 consultas y 27 módulos de base.
Su intervalo inclusivo es 28000000000000000001..42380653296441592424,
con al menos 130441933147714940 entradas impares, hasta 76 rachas
y combustible 256. Este certificado no necesita LMN ni Rozier–Terracol.

El [cotejo independiente previo](cotejo_prefijos_76_afinados.json) reconstruye
órbitas directas, usa otra búsqueda entera para B y `Fraction` para la
recurrencia. Comprueba 4910 clases no vacías y cobertura disjunta. La
igualdad universal del exponente enlaza ambas implementaciones.

La [cadena completa de 76](SETENTA_Y_SEIS_LEAN.md) requiere también tabla,
cola y las dos hipótesis externas. La evaluación original del certificado
se conserva por separado y continuaba activa cuando terminó la binaria.
Se [interrumpió después](interrupcion_setenta_y_seis_original.json) para
liberar memoria; su salida parcial no es un certificado terminado.
No se ha realizado una comparación controlada de tiempos.

## Próxima forma de presentar los certificados

[OcelotasPrefijosTestigos.lean](OcelotasPrefijosTestigos.lean) permite
proporcionar B en cada hoja, comprobar `(X+1)^256<=2^B` y comprobar la
cota entera restante. La monotonía de la recurrencia en B justifica
usar cualquier cota superior válida, aunque no sea la mínima.
`acepta_rama` sólo necesita m<=a y la aceptación de los dos hijos;
no exige volver a evaluar la criba en una rama interna. También se
certifican las hojas vacías, de descenso y de exceso de rachas.

La [auditoría](evidencia_prefijos_testigos.json) contiene cinco módulos
nuevos, 20 consultas y 27 módulos de base, con axiomas estándar y sin
`sorryAx`. Es una interfaz formalizada para generar los certificados
de [77](SETENTA_Y_SIETE_PROPUESTA.md); todavía no se ha medido su coste
en esa ventana ni sustituye su certificado concreto pendiente. La
[continuación con árboles de motivos](TESTIGOS_PREFIJOS_LEAN.md) ya
comprobó la ventana de 76 y está evaluando la de 77.

```text
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasExponenteBinarioExacto --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_exponente_binario_exacto.json
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasSetentaYSeisPrefijosBinarios --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_prefijos_76_binarios.json
```

Las primeras versiones de los lemas se corrigieron durante la compilación.
Los manifiestos citados corresponden a las fuentes finales verificadas.
La auditoría inicial `evidencia_prefijos_binarios.json` conserva una
versión anterior a quitar un nombre de variable sin uso; no es el
manifiesto de las fuentes actuales.
