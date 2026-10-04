# Ocelotas: CST hasta 76 rachas bajo LMN y Rozier–Terracol

03-10-2026. **Cierre comprobado en Lean**, bajo LMN y el corolario finito
de Rozier–Terracol como hipótesis explícitas. Quince módulos nuevos,
123 consultas de axiomas estándar y ningún `sorryAx`. Revisión humana
y prioridad histórica pendientes. Se conserva el resultado de
[75 rachas](SETENTA_Y_CINCO_LEAN.md).

## Enunciado y alcance

[OcelotasSetentaYSeisBinarios.lean](OcelotasSetentaYSeisBinarios.lean)
prueba `cst_condicional`: con el atajo T(n)=n/2 si n es par y (3n+1)/2
si es impar, n>=2, un primer cruce finito k y hasta 76 bloques maximales
de entradas impares en los primeros k pasos, el primer descenso ocurre
exactamente en k. `fallo_exige_setenta_y_siete` impone al menos 77 rachas
a un fallo, con las mismas hipótesis.

`LMN23` es el corolario especializado publicado de
Laurent–Mignotte–Nesterenko. `RozierTerracol54` supone el descenso en
el primer cruce para 2<=n<=28000000000000000000, consecuencia del
[corolario 5.4, v5](https://arxiv.org/html/2502.00948v5#S5).
Ambos son argumentos del teorema, no axiomas añadidos a Lean. El
resultado finito externo no se ha recalculado en el laboratorio.

No se afirma existencia universal del primer cruce, llegada a 1 ni
resolución general de CST. No hay ley probabilística. El censo hasta
2^23 se conserva.

## Propuesta y contraste independiente

La [preparación exacta](preparacion_setenta_y_seis.json) y los
[97 intervalos Lean](OcelotasSetentaYSeisTablaBinaria.lean) usan:

- 91 filas que remiten a n<=28000000000000000000, rango externo;
- cinco filas excluidas por la criba de rachas;
- una fila que además requiere el nuevo certificado de prefijos.

La fila resuelta por prefijos cubre 130441933147714940<=q<397560349370386783.
Su cota de semilla es
n<42380653296441592425. El [certificado propuesto](prefijos_76_afinados_5m.json)
trata el intervalo inclusivo 28000000000000000001..42380653296441592424,
con q>=130441933147714940, como máximo 76 rachas y combustible 256.
La criba afinada propone 11225 nodos, 4910 clases no vacías y profundidad
máxima 77. El [cotejo independiente](cotejo_prefijos_76_afinados.json)
comprueba las órbitas, los pisos y la cobertura disjunta.

El [cotejo de la tabla](cotejo_setenta_y_seis.json), mediante
[otro programa](cotejar_setenta_y_seis.py), comprueba cotas racionales
de logaritmos, determinantes, continuidad de intervalos, las 97 filas y
el enlace exacto con el certificado anterior. Para la cola verifica
R=76, A=5432095936891962, c=7 y H=71. El corte de tabla es
q<2389894509120846565669, superior a 2^71.

## Verificación formal y reproducción

La [evaluación por bisección](PREFIJOS_BINARIOS_LEAN.md) del
[certificado concreto](OcelotasSetentaYSeisPrefijosBinarios.lean), las
siete partes de tabla, su unión, la cola y el ensamblaje final fueron
aceptados por Lean. La [auditoría completa](evidencia_setenta_y_seis_binarios.json)
y su [salida](evidencia_setenta_y_seis_binarios.txt) registran Lean 4.32.2,
15 módulos compilados, 123 consultas y 38 módulos previos reutilizados
por huellas verificadas. Todas las fuentes actuales coinciden con las
huellas del manifiesto. No es una reconstrucción limpia de toda la base.

La primera ejecución, **31998**, continuaba evaluando la versión
[anterior del certificado](OcelotasSetentaYSeisPrefijos.lean) cuando
terminó la cadena binaria. Se conservan sus fuentes y su
[salida parcial](evidencia_setenta_y_seis.txt); esa salida no se cita
como certificado final. El intento se [interrumpió deliberadamente](interrupcion_setenta_y_seis_original.json)
para liberar memoria después de verificar el cierre binario y la
equivalencia universal de verificadores. La sesión terminó con código 1
por esa interrupción; no es un contraejemplo ni una auditoría completada.
La comprobación de [22 rachas](VEINTIDOS_LEAN.md) terminó
después, con LMN como único resultado externo.

```text
python -B -X utf8 depuracion/cst20260930/generar_setenta_y_seis_binarios_lean.py --certificado depuracion/cst20260930/preparacion_setenta_y_seis.json --directorio depuracion/cst20260930
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasSetentaYSeisBinarios --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_setenta_y_seis_binarios.json
```

## Límite y siguiente acción

La primera [exploración de 77](prefijos_77_afinados_1m.json) agotó un
millón de nodos. Con un presupuesto mayor apareció un
[certificado propuesto completo](prefijos_77_afinados_5m.json): 1420851
nodos y 574357 hojas no vacías. El [cotejo independiente](cotejo_prefijos_77_afinados.json)
comprueba todas las hojas y su cobertura, sin discrepancias. Faltan
certificación Lean, tabla y ensamblaje para 77. La continuación tiene
[ficha propia](SETENTA_Y_SIETE_PROPUESTA.md), con su tabla ya cotejada.
El siguiente trabajo es certificar esa ventana sin repetir cálculos
innecesarios dentro de cada rama.
