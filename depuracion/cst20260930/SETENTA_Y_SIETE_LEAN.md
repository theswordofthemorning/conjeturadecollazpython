# Ocelotas: CST hasta 77 rachas, bajo LMN y Rozier–Terracol

03-10-2026. **Cadena completa aceptada en Lean 4.32.2.** La sesión
64800 terminó con código 0. Se conservan la
[preparación y los cotejos](SETENTA_Y_SIETE_PROPUESTA.md) y el cierre
anterior de [76](SETENTA_Y_SEIS_LEAN.md).

## Enunciado y alcance

Se usa T(n)=n/2 para n par y (3n+1)/2 para n impar, n>=2. S_j cuenta
las entradas impares en los primeros j pasos. Se supone un primer
cruce finito k: 3^S_j>=2^j para 1<=j<k y 3^S_k<2^k. Las rachas son
los bloques maximales de entradas impares hasta k, contados en la órbita.

[OcelotasSetentaYSiete.cst_condicional](OcelotasSetentaYSiete.lean)
demuestra, si hay como máximo 77 rachas:

```text
T^j(n)>=n para todo j<k, y T^k(n)<n.
```

`fallo_exige_setenta_y_ocho` concluye que un fallo necesita al menos
78 rachas. Se incluye el caso par. Ambos teoremas reciben dos
hipótesis matemáticas externas explícitas:

- `LMN23`, el corolario de Laurent–Mignotte–Nesterenko especializado
  en 2 y 3; su conversión a `LMNDebil` está formalizada.
- `RozierTerracol54`, el descenso en el primer cruce para
  2<=n<=28000000000000000000, tomado del corolario 5.4 de
  Rozier–Terracol. Ese resultado finito externo no se recalculó aquí.

Son argumentos de los teoremas, no nuevos axiomas añadidos a Lean.
No se demuestra existencia universal de primer cruce, llegada a 1
ni CST sin límite de rachas. No hay ley probabilística ni nuevo censo.

## Partes de la prueba

La [tabla](OcelotasSetentaYSieteTabla.lean) cubre 97 intervalos para
q<4857481135601629720741: 91 remiten al rango externo, cinco se
excluyen por criba y uno mediante prefijos. Su cotejo independiente
usa series racionales de logaritmos, determinantes, pisos y potencias.

La ventana inclusiva de prefijos es

```text
28000000000000000001 <= n <= 42938293471394771272,
q >= 130441933147714940, rachas <= 77, combustible 256.
```

El [certificado](prefijos_77_afinados_5m.json) tiene 1420851 nodos,
574357 clases no vacías y profundidad máxima 81. Cubre exactamente
14938293471394771272 semillas, sin pendientes. El
[contraste independiente](cotejo_prefijos_77_afinados.json) reconstruye
órbitas directas, usa `Fraction` y comprueba cobertura disjunta.

El [generador](generar_testigos_prefijos_lean.py) produjo 4896
subárboles y 4895 uniones en 73 partes. Lean evalúa los subárboles
con `decide +kernel` y une sus conclusiones mediante lemas ya probados.
La cola infinita aplica el criterio paramétrico con R=77,
A=8691353499027139, c=7 y H=72.

## Auditoría y reproducción

La [evidencia completa](evidencia_setenta_y_siete.json) y su
[salida](evidencia_setenta_y_siete.txt) registran:

- 91 módulos de extensión: 85 compilados y seis reutilizados.
- 38 módulos de base reutilizados y comprobados por huellas.
- 5030 consultas `#print axioms`, todas con axiomas estándar y sin
  `sorryAx`. Son consultas, no 5030 resultados científicos distintos.
- Fuentes, objetos compilados y número de consultas cotejados
  de nuevo tras la terminación correcta.
- 6084,780 segundos de esta ejecución; no es una comparación de rendimiento.

No es una reconstrucción limpia de toda la base. Los objetos se
reutilizan sólo cuando coinciden fuentes, dependencias y entorno.

```text
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasSetentaYSiete --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_testigos_20261003 --salida depuracion/cst20260930/evidencia_setenta_y_siete.json
```

Revisión humana de la interpretación y prioridad histórica pendientes.
Este alcance no establece una mejora del teorema de Tao de 2019.
