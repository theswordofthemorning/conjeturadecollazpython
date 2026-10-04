# Ocelotas: CST hasta veintidós rachas en Lean bajo LMN

03-10-2026. **Cierre Lean completo.** El tramo finito se certifica en
el repositorio y LMN es el único resultado externo. Se conserva el
cierre de [veintiuna rachas](VEINTIUNA_LEAN.md). El de
[76](SETENTA_Y_SEIS_LEAN.md) asume además el resultado finito de
Rozier–Terracol. Revisión humana y prioridad histórica pendientes.

## Enunciado y alcance

[OcelotasVeintidos.lean](OcelotasVeintidos.lean) prueba
`cst_veintidos_corolario`: para T(n)=n/2 si n es par y (3n+1)/2 si es
impar, n>=2 y primer cruce finito k, bajo `LMN23`, si los primeros k
pasos contienen como máximo 22 bloques maximales de entradas impares,
no hay descenso antes de k y T^k(n)<n. El caso par está incluido.
`fallo_exige_veintitres` exige al menos 23 rachas a un fallo, desde
`LMNDebil`; `LMN23` implica esa hipótesis mediante la traducción formal.

LMN permanece como argumento explícito del teorema. No se demuestra
la existencia universal del primer cruce, la llegada a 1 ni CST general.
No hay ley probabilística ni ampliación del censo hasta 2^23.

## Piezas y contrastes

Se conservan la [tabla propuesta](preparacion_veintidos_lean.json), su
[cotejo racional](cotejo_veintidos_lean.json), los certificados
[bajo](prefijos_22_bajo.json) y [alto](prefijos_22_alto_5m.json), y el
[contraste independiente de 862805 clases](cotejo_prefijos_22.json).
Los intervalos se solapan; no se suman sus cardinalidades.

Se comprobaron:

- [Tabla Lean](OcelotasVeintidosTabla.lean): 42 intervalos;
  [generador](generar_veintidos_lean.py).
- [Prefijos](OcelotasVeintidosPrefijos.lean): intervalos inclusivos
  4912741..6003186 con q>=79335 y 4912741..341045747 con q>=190537,
  rachas<=22 y combustible 128.
- 230 módulos de evaluación, hasta 5000 nodos por hoja y 20000 por
  módulo; 1896 hojas y 1330 uniones internas adicionales.
- [Ensamblaje](OcelotasVeintidos.lean) desde el contador real,
  con LMN externo y primer cruce finito.

La [cola](OcelotasVeintidosCola.lean) prueba `cota(22,m)<=51580*m` y
excluye fallos para k>=2^33 por una desigualdad entera e inducción.
El [puente temporal](OcelotasVentanaRacional.lean) trata la ventana
2^32<=k<2^33 que queda después del corte q>=4598951775.
La tabla de 42 intervalos tiene 35 filas que remiten a n<=4912740,
cinco exclusiones por criba y dos ventanas de prefijos.

Los cotejos independientes comprueban las 42 filas por aritmética
racional y las 862805 hojas no vacías por órbitas directas y cobertura
disjunta. Los certificados bajo y alto tienen 339401 y 3840535 nodos,
con profundidades máximas 55 y 57. Sus intervalos se solapan.

## Auditoría

La ejecución **88825 terminó con código 0**. El
[registro final](lean_veintidos.txt) y la
[evidencia archivada](evidencia_veintidos_lean.json) conservan:

- Lean 4.32.2 y las huellas del comprobador y del registro;
- 312 módulos: 236 compilados en esta ejecución y 76 reutilizados;
- 3420 consultas: 317 con listas de axiomas estándar y 3103 sin axiomas;
- las auditorías originales de todos los módulos reutilizados;
- cotejo de fuentes, objetos, cadena de prefijos y número de consultas.

No aparece `sorryAx`. Las consultas no son necesariamente declaraciones
distintas. Es una auditoría acumulada, no una reconstrucción limpia de
los 312 módulos. El manifiesto completo se conserva dentro de la evidencia.

## Reproducción

```text
python -B -X utf8 depuracion/cst20260930/generar_prefijos_lean.py --bajo depuracion/cst20260930/prefijos_22_bajo.json --alto depuracion/cst20260930/prefijos_22_alto_5m.json --profundidad 12 --espacio OcelotasVeintidosPrefijos --hojas-por-modulo 10000 --salida depuracion/cst20260930/OcelotasVeintidosPrefijos.lean
python -B -X utf8 depuracion/cst20260930/dividir_hojas_prefijos.py --origen depuracion/cst20260930/OcelotasVeintidosPrefijosHojas01.lean --salida depuracion/cst20260930/OcelotasVeintidosPrefijosHojas01.lean --nodos-hoja 5000 --nodos-modulo 20000
python -B -X utf8 depuracion/cst20260930/generar_veintidos_lean.py --certificado depuracion/cst20260930/preparacion_veintidos_lean.json --salida depuracion/cst20260930/OcelotasVeintidosTabla.lean
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --hasta 22 --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --reutilizar --salida depuracion/cst20260930/lean_veintidos.txt
```

La siguiente frontera de esta vía es 23 rachas; no queda resuelta por
este cierre. En la vía que usa además Rozier–Terracol está en curso la
[comprobación de 77](SETENTA_Y_SIETE_PROPUESTA.md). La
[cota general](COTA_GENERAL.md) se conserva como resultado independiente
de los certificados finitos de esta tanda.
