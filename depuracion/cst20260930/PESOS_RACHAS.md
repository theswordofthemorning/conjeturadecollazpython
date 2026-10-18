# Ocelotas: pesos por racha — 81 rachas bajo LMN y Rozier–Terracol

**Actualización 16-10:** [83 rachas y revisión para Rozier](revision_rozier_20261016/REVISION.md),
con versiones Lean bajo LMN o Rhin y la cobertura actualizada de Roosendaal.
El puente desde esa cobertura a CST también quedó formalizado. Lo que sigue
conserva el resultado y los diagnósticos del 12-10 con el rango externo antiguo.

12-10-2026. Continuación de [77 rachas](SETENTA_Y_SIETE_LEAN.md). La idea
procede de releer Hercher (2023), lemas 8–12 y teorema 21, buscando qué
pasa del caso de los ciclos al primer cruce. Revisión humana y prioridad
histórica pendientes. No se ha anunciado ni enviado a nadie.

## Qué se transfiere de Hercher

| Hercher (ciclos) | Primer cruce de CST | Uso aquí |
|---|---|---|
| Lema 8: `n ≡ -1 (mod 2^k)` en una racha | Igual; ya era `congruencia_racha` | Sí |
| Observación 7: cada racha suma menos de `3/n_i` | Igual, desde la identidad del fallo | Sí, con peso por racha |
| Lema 9: fusión de `n_i` con `(n_i-1)/2` cuando `ℓ_i ≥ 2` | **No.** La fusión transmite la llegada a 1, no el tiempo de descenso. Un fallo de CST no se hereda | No |
| Lemas 11–12, corolario 13 (media `35/18`) | Sólo los casos sin fusión; el caso `ℓ_i ≥ 2` queda con peso 1 | No |
| Teorema 21: separar mínimos pequeños de rachas grandes y crecientes | **Sí.** Una racha larga obliga a un comienzo enorme y casi no pesa; una racha que empieza cerca de n reinicia el crecimiento | Núcleo de esta nota |

Las [lecturas del 03-10](LECTURAS_20261003.md) ya advertían que el lema 9
no transfiere el primer cruce. Esta nota confirma esa frontera y encuentra
la parte que sí pasa.

## Enunciado

Mapa `T(n)=n/2` si n es par y `(3n+1)/2` si es impar; n>=2; k primer cruce
finito del coeficiente; q impares y r rachas en los k primeros pasos.

**Bajo `LMN23` y `RozierTerracol54`, si r<=81, entonces `T^k(n)<n`.**
Un fallo con primer cruce finito necesita al menos 82 rachas.
Antes: 77 rachas, con un árbol de prefijos de 1 420 851 nodos.
Ahora no hay árbol de prefijos.

No se demuestra la existencia del primer cruce, la llegada a 1, Collatz
ni CST sin límite de rachas. No hay ley probabilística ni censo nuevo.

## Prueba escrita

Sean `x_0=n, x_1, …, x_(r-1)` los comienzos de las rachas, `a_i` sus
longitudes impares, `t_i` sus tiempos y `A_i` los impares anteriores.
Tómese `M=2^m` con `nsup+R<=M`. La racha i es **pesada** si `x_i+1<=M`.
`x_0=n` siempre lo es.

1. **Pesos.** De `identidad_bloque`, `pre_cruce` y `cota_afin`, por
   inducción sobre los bloques:

   ```text
   2^(t_i) x_i M <= 3^(A_i) (n M + W_i),   W_(i+1) = W_i + w_i,
   ```

   con `w_i=M` si la racha es pesada y `w_i=n+R` si es ligera. El último
   paso es estricto. Si falla el descenso, `n<=T^k(n)`, y con
   `exp(Λ)>=1+Λ`:

   ```text
   c n M < H M + (r-H)(n+R),     c <= Λ = k log 2 - q log 3,
   ```

   donde H cuenta las rachas pesadas. Cada racha ligera pesa menos de
   `(n+R)/M`; si ese peso es pequeño, hacen falta muchas pesadas.
2. **Pesadas necesarias.** Si `h0 M + (R-h0)(nsup+R) <= c ninf M`, la
   desigualdad anterior obliga a `H>=h0+1` para todo n de `[ninf,nsup]`.
3. **Segmentos.** Cada racha pesada empieza con `x+1<=2^m`. Desde ella,
   la criba de descuento ya formalizada acota los impares del tramo hasta
   la siguiente pesada por

   ```text
   g(m,j) = j + cota(256m-256, j).
   ```

   Esa cota tiene incrementos crecientes (`g_convexa`). Con H tramos, el
   peor reparto es un tramo largo y H-1 de una racha:

   ```text
   q <= g(m, r-H+1) + (H-1) m <= g(m, R-h0) + h0 m.
   ```

4. **Exclusión.** Si esa cota es menor que el q mínimo del intervalo,
   la pieza `[ninf,nsup]` no contiene fallos. Las semillas `n<=N` se
   remiten a Rozier–Terracol, y los tiempos `k>=2^75` a la cola
   paramétrica, que ya estaba formalizada para cualquier R.

Lo esencial es el reinicio. Con una sola cadena de congruencias, cada
racha puede multiplicar el exponente por `α≈1,585`. Pero una racha que
cuenta en el peso empieza cerca de n, y su sucesora vuelve a partir de
`m` bits. El fallo necesita aproximadamente `Λn` rachas pesadas, y cada
una cuesta un factor α de crecimiento.

## Certificado y cotejo

[pesos_rachas.py](pesos_rachas.py) genera [pesos_81.json](pesos_81.json)
en menos de un segundo, con aritmética racional exacta y los mismos
encierros de 55 cifras de la tabla de 77
([logaritmos_55_propuesta.json](logaritmos_55_propuesta.json)).

- 101 intervalos unilaterales para `q<38887293218019448937881`
  (`>=2^75`).
- 91 intervalos remiten a Rozier–Terracol por la cota `n<R/c`.
- 10 intervalos, desde `q>=130441933147714940`, se cierran con
  119 piezas de pesos.
- Para 82 rachas la criba falla en el intervalo
  `[397560349370386783, 4640282259296926456)`, en la pieza
  `[28000000000000000001, 28000854492187500001]`.

[cotejar_pesos.py](cotejar_pesos.py) no importa el certificador. Recalcula
log 2 y log 3 por series de atanh con cola acotada, los determinantes,
signos, contigüidad, cobertura de cada intervalo de semillas, la criba
con la recursión real `floor(beta+alfa C)` y los parámetros de la cola.
[Resultado](cotejo_pesos_81.json): coincide.

Antes del certificado se comprobaron en órbitas reales, con enteros
exactos, las cinco desigualdades usadas: 119 999 semillas y 208 782
rachas, sin discrepancias. Ese guion exploratorio quedó fuera del
repositorio y no se presenta como evidencia de cobertura.

## Lean

- [OcelotasPesos.lean](OcelotasPesos.lean): teoría universal. Palabras
  desplazadas, segmento desde un corte, convexidad de g, cadena de pesos,
  `fallo_pesos`, `pesadas_de_fallo`, `suma_por_segmentos`,
  `pieza_imposible` y `pieza_cadena`. Sin LMN ni censo.
- [OcelotasOchentaYUnoTabla.lean](OcelotasOchentaYUnoTabla.lean) y siete
  partes, generadas por [generar_ochenta_y_uno_lean.py](generar_ochenta_y_uno_lean.py).
- [OcelotasOchentaYUno.lean](OcelotasOchentaYUno.lean): `cst_condicional`
  y `fallo_exige_ochenta_y_dos`, con `LMN23` y `RozierTerracol54` como
  argumentos explícitos. `RozierTerracol54` repite literalmente la
  definición de 77, para no importar aquel árbol.

**Cadena aceptada en Lean 4.32.2.** El auditor
[comprobar_extension_persistente.py](comprobar_extension_persistente.py)
compiló 14 módulos en un almacén nuevo, sin reutilizar extensiones
anteriores, y reutilizó la base auditada por huellas. Registró 133
consultas `#print axioms`, todas con axiomas estándar y sin `sorryAx`, en
288 s. Evidencia: [evidencia_ochenta_y_uno.json](evidencia_ochenta_y_uno.json)
y [.txt](evidencia_ochenta_y_uno.txt). No es una reconstrucción limpia de
toda la base ni verifica el censo externo.

```text
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasOchentaYUno --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_pesos_auditado_20261012 --salida depuracion/cst20260930/evidencia_ochenta_y_uno.json
```

## Límites

- Sólo con LMN y el certificado interno (n<=4912740) no mejora nada:
  `Λn<1` y los pesos no fuerzan rachas pesadas. Con un censo propio
  hasta 2^36 sí: 40 rachas, y hasta 2·10^11, 41 (sección siguiente).
- El tope de 82 está en el borde `n≈N`, en un solo intervalo:
  `397560349370386783<=q<4640282259296926456` y
  `28000000000000000001<=n<=32962697863578796386` (unos 5·10^18 semillas).
  Allí `cn<5`, de modo que bastan cinco rachas pesadas, y cinco dejan
  `q<=4,43·10^17`, por encima del mínimo `3,98·10^17`. Con seis se
  excluiría. Afinar el peso de cada racha no ayuda: una racha pesada larga
  que empieza con coeficiente cercano a 1 pesa casi 1, y en ese intervalo
  los coeficientes pueden acercarse a 1 todo lo que se quiera
  (`|Aα-t|` llega a ~10^-19). Cerrar 82 exige otra herramienta en esa
  ventana, como el árbol de prefijos de 77, o un rango externo mayor.
  Ensayo del 12-10 con `explorar_prefijos_racionales.py` (R=82, criba
  afinada, combustible 256): con 5 000 000 nodos cubre
  1 715 645 481 725 793 286 semillas, un 35 % de la ventana, y se agota el
  presupuesto. Profundidad 85, 208 s. El certificado no se conserva:
  extrapolado, haría falta un árbol más de diez veces mayor que el de 77.
  También se probó, en un prototipo fuera del repositorio, una criba
  híbrida: pesos dentro de cada nodo del árbol, con las rachas pesadas y
  ligeras ya recorridas y el tramo actual. **No podó ningún nodo** en
  200 000. En esa ventana el fallo sólo necesita 4 o 5 rachas pesadas, y
  ese reinicio quita menos crecimiento del que la criba normal ya
  descuenta. Con estas herramientas, 81 es el cierre de la vía de pesos.
- Las cotas de rachas de Hercher (91, ciclos) siguen siendo mayores; su
  lema de fusión no tiene análogo aquí.
- Los caminos rojos del mapa (no divergencia y ausencia de circuitos) no
  cambian: este avance supone un primer cruce finito.

## 40 rachas sin Rozier–Terracol: LMN y un censo propio

Los pesos reducen mucho el rango externo que hace falta. N externo
necesario, con pesos y antes:

| Rachas | Con pesos | Antes |
|---|---|---|
| 30 | 3,3·10^8 | 2,5·10^9 |
| 40 | 6,62·10^10 | 4,0·10^12 |
| 41 | 1,98·10^11 | — |
| 75 | 6,6·10^16 | 2,7·10^18 |

Para 40 rachas basta `N=2^36=68719476736`. Ese rango se comprobó aquí, sin
Rozier–Terracol.

**Enunciado.** Bajo `LMN23` y `CensoPropio36` (descenso en el primer cruce
para `2<=n<=2^36`), si r<=40, entonces `T^k(n)<n`. Antes, sólo con LMN:
24 rachas. `CensoPropio36` es una **hipótesis explícita** del teorema. El
censo es un cálculo en Python y numpy, no una prueba Lean.

- **Certificado** [pesos_40.json](pesos_40.json): 64 intervalos para
  `q<2365627332311699`. 41 remiten al censo y 23 se cierran con 317 piezas
  de pesos. Cola paramétrica R=40, A=243583605, c=7, H=51.
  [Cotejo](cotejo_pesos_40.json): coincide.
- **Lean** [OcelotasCuarenta.lean](OcelotasCuarenta.lean), tabla
  [OcelotasCuarentaTabla.lean](OcelotasCuarentaTabla.lean) y 13 partes:
  `cst_condicional` y `fallo_exige_cuarenta_y_una`. Auditor persistente:
  20 módulos compilados en un almacén nuevo, 96 consultas con axiomas
  estándar y sin `sorryAx`, en 914 s. Evidencia:
  [evidencia_cuarenta.json](evidencia_cuarenta.json) y
  [.txt](evidencia_cuarenta.txt).
- **Censo** [censo_cst.py](censo_cst.py) →
  [censo_cst_2_36.json](censo_cst_2_36.json): **0 fallos**. Criba por
  residuos mod 2^24. Las 16 490 635 clases que cruzan en a lo sumo 24
  pasos cumplen `T^j(n)=(3^S n+b)/2^j` y descienden exactamente cuando
  `n(2^j-3^S)>b`; ningún miembro `n>=2` quedó por comprobar. Las 286 581
  clases sin cruce se recorrieron una a una: 1 173 835 776 semillas
  (= 286 581·4096). 65 desbordes de uint64 se resolvieron con enteros de
  Python. 2542 s.
- **Pruebas de mutación.** Con `--factor/--divisor` el censo exige
  `f·T^k(n)<g·n`. Para 4/3, 6/5 y 10/9 cuenta los mismos fallos que la
  fuerza bruta (111 927; 31 771; 11 793 y 118 051 en dos rangos). Es decir,
  detecta fallos cuando existen.
- **Cotejo independiente** [cotejar_censo.py](cotejar_censo.py), que no
  importa el censo → [cotejo_censo_2_36.json](cotejo_censo_2_36.json):
  recorrido completo sin criba de `2<=n<=2^27` y un millón de semillas al
  azar en `[2,2^36]` (semilla 20261012). Ningún fallo.

El censo no es nuevo frente a la literatura: Rozier–Terracol, y antes
otros, verificaron rangos mucho mayores. Lo que cambia es la dependencia,
porque el teorema de 40 rachas sólo pide LMN y una cuenta reproducible en
una hora con este repositorio.

### 41 rachas: censo hasta 2·10^11

Para 41 rachas basta `N=2·10^11` (con 1,8·10^11 la criba no cierra; para
42 no basta 1,98·10^11). El censo se amplió con `--desde`, de modo que sólo
se recorrió el tramo nuevo `(2^36, 2·10^11]`, en seis procesos paralelos
([censo_41/](censo_41/), unos 31 minutos cada uno): **0 fallos**.
[cubrir_tramos.py](cubrir_tramos.py) →
[cobertura.json](censo_41/cobertura.json) comprueba que los tramos son
contiguos y que cada uno recorrió exactamente las semillas de las clases sin
cruce de su rango (373 745 9xx por tramo). Ningún miembro de una clase que
cruza quedó por comprobar. [Cotejo independiente](censo_41/cotejo_tramo.json):
un millón de semillas al azar del tramo nuevo, 0 fallos. Con `--desde`, la
suma por tramos de la mutación 10/9 hasta 3·10^6 coincide con el cálculo de
una vez (48 584 + 69 467 = 118 051). El tramo `[2,2^36]` se calculó con la
versión anterior del programa (sha256 `354b89d0…`, sin `--desde`); los
tramos nuevos, con `7c79189f…`.

- **Certificado** [pesos_41.json](pesos_41.json): 64 intervalos para
  `q<2365627332311699`, 41 remiten al censo, 23 se cierran con 284 piezas;
  cola R=41, A=389733769, c=7, H=51. [Cotejo](cotejo_pesos_41.json): coincide.
- **Lean** [OcelotasCuarentaYUna.lean](OcelotasCuarentaYUna.lean) con
  hipótesis explícita `CensoPropio2e11`, tabla
  [OcelotasCuarentaYUnaTabla.lean](OcelotasCuarentaYUnaTabla.lean) y 13
  partes: `cst_condicional` y `fallo_exige_cuarenta_y_dos`. Auditor: 20
  módulos compilados en almacén nuevo
  (`%TEMP%/ocelotas_cuarenta_y_una_auditado_20261012`), 96 consultas
  estándar, sin `sorryAx`, 24 min. Evidencia:
  [evidencia_cuarenta_y_una.json](evidencia_cuarenta_y_una.json) y
  [.txt](evidencia_cuarenta_y_una.txt).

### 42 rachas: censo hasta 3·10^11

Con H=51, 42 rachas piden un censo hasta 3·10^11 (con 2,5·10^11 no
cierra). El tramo nuevo `(2·10^11, 3·10^11]` se recorrió en seis procesos
([censo_42/](censo_42/), unos 27 minutos cada uno): **0 fallos**.
[cobertura.json](censo_42/cobertura.json) da tramos contiguos y recorridos
exactos; el [cotejo independiente](censo_42/cotejo_tramo.json) de un millón
de semillas al azar, 0 fallos.

- **Certificado** [pesos_42.json](pesos_42.json): 64 intervalos, 41 remiten
  al censo, 23 se cierran con 270 piezas; cola R=42, A=623574031, c=7, H=51.
  [Cotejo](cotejo_pesos_42.json): coincide.
- **Lean** [OcelotasCuarentaYDos.lean](OcelotasCuarentaYDos.lean) con
  hipótesis explícita `CensoPropio3e11`, tabla y 13 partes: `cst_condicional`
  y `fallo_exige_cuarenta_y_tres`. Auditor: 20 módulos compilados en almacén
  nuevo, 96 consultas estándar, sin `sorryAx`, 9 min 42 s. Evidencia:
  [evidencia_cuarenta_y_dos.json](evidencia_cuarenta_y_dos.json) y
  [.txt](evidencia_cuarenta_y_dos.txt).

### 46 rachas: censo hasta 7·10^11

El tramo nuevo `(3·10^11, 7·10^11]` se recorrió en tres procesos en paralelo
([censo_46/](censo_46/), unas 1 h 55 min cada uno): **0 fallos**.
[cobertura.json](censo_46/cobertura.json) da tramos contiguos y recorridos
exactos; el [cotejo independiente](censo_46/cotejo_tramo.json), completo hasta
2^22 y con un millón de semillas al azar en el tramo nuevo, 0 fallos.

- **Certificado** [pesos_46.json](pesos_46.json): 64 intervalos, 42 remiten
  al censo, 22 se cierran con 244 piezas; cola R=46, A=4086654774, c=7, H=51.
  [Cotejo](cotejo_pesos_46.json): coincide.
- **Lean** [OcelotasCuarentaYSeis.lean](OcelotasCuarentaYSeis.lean) con
  hipótesis explícita `CensoPropio7e11`, tabla y 12 partes: `cst_condicional`
  y `fallo_exige_cuarenta_y_siete`. Auditor: 19 módulos compilados en almacén
  nuevo, 96 consultas estándar, sin `sorryAx`, 7 min 25 s. Evidencia:
  [evidencia_cuarenta_y_seis.json](evidencia_cuarenta_y_seis.json) y
  [.txt](evidencia_cuarenta_y_seis.txt).
- **Reproducción** (12-10): con los comandos de abajo, el certificado, su
  cotejo y los 13 ficheros Lean de la tabla salen idénticos byte a byte.

### 47 rachas: PENDIENTE (12-10, noche)

El umbral medido es más bajo de lo estimado: con H=51, 47 rachas **cierran
con un censo hasta 1,2·10^12** (con 1,1·10^12 no). `pesos_47.json`: 42 filas
al censo, 22 por pesos con 228 piezas; cola A=6538647640, c=7, H=51; el
cotejo coincide. El censo `(7·10^11, 1,2·10^12]` en cuatro tramos de
1,25·10^11 (unas 2 h en paralelo) se lanzó y **se canceló a pedido del
usuario**; no hay tramos terminados. Para retomar:

```text
python -B -X utf8 depuracion/cst20260930/pesos_rachas.py --rachas 47 --H 51 --externo 1200000000000 --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/pesos_47.json
python -B -X utf8 depuracion/cst20260930/cotejar_pesos.py --certificado depuracion/cst20260930/pesos_47.json --salida depuracion/cst20260930/cotejo_pesos_47.json
python -B -X utf8 depuracion/cst20260930/generar_ochenta_y_uno_lean.py --certificado depuracion/cst20260930/pesos_47.json --base OcelotasCuarentaYSieteTabla --carpeta depuracion/cst20260930
python -B -X utf8 depuracion/cst20260930/censo_cst.py --desde 700000000001 --N 825000000000 --salida depuracion/cst20260930/censo_47/tramo_1.json   # 2: 825000000001-950000000000, 3: 950000000001-1075000000000, 4: 1075000000001-1200000000000
python -B -X utf8 depuracion/cst20260930/cubrir_tramos.py --carpeta depuracion/cst20260930/censo_47 --desde 700000000001 --tramos 4
python -B -X utf8 depuracion/cst20260930/cotejar_censo.py --N 1200000000000 --desde 700000000001 --E 22 --salida depuracion/cst20260930/censo_47/cotejo_tramo.json
```

El módulo principal `OcelotasCuarentaYSiete.lean` (hipótesis
`CensoPropio12e11`, `fallo_exige_cuarenta_y_ocho`) se copió del de 46 y está
en el repo (17-10) sin auditar, igual que el certificado y la tabla generada:
nada de 47 vale como resultado hasta el censo y la auditoría. Después: auditor persistente en un almacén nuevo, instancia
de ciclos y registro. Con Rozier–Terracol la misma vía ya da 81.

Umbrales medidos el 12-10 con `pesos_rachas.py` (H=51), que corrigen la
estimación anterior de 6·10^11 para 43:

| Rachas | No cierra con | Cierra con |
|---|---|---|
| 43 | 3,95·10^11 | 4·10^11 |
| 44 | 4·10^11 | 5·10^11 |
| 45 | 5·10^11 | 6·10^11 |
| 46 | 6,5·10^11 | 7·10^11 |
| 47 | 10^12 | 2·10^12 |
| 48 y 50 | 2·10^12 | 5·10^12 |

El censo en Python crece linealmente; Rozier–Terracol
llega a 2,8·10^19 y con él la vía de pesos da 81.

```text
python -B -X utf8 depuracion/cst20260930/pesos_rachas.py --rachas 40 --H 51 --externo 68719476736 --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/pesos_40.json
python -B -X utf8 depuracion/cst20260930/cotejar_pesos.py --certificado depuracion/cst20260930/pesos_40.json --salida depuracion/cst20260930/cotejo_pesos_40.json
python -B -X utf8 depuracion/cst20260930/generar_ochenta_y_uno_lean.py --certificado depuracion/cst20260930/pesos_40.json --base OcelotasCuarentaTabla --carpeta depuracion/cst20260930
python -B -X utf8 depuracion/cst20260930/censo_cst.py --N 68719476736 --K 24 --salida depuracion/cst20260930/censo_cst_2_36.json
python -B -X utf8 depuracion/cst20260930/cotejar_censo.py --N 68719476736 --salida depuracion/cst20260930/cotejo_censo_2_36.json
python -B -X utf8 depuracion/cst20260930/pesos_rachas.py --rachas 41 --H 51 --externo 200000000000 --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/pesos_41.json
python -B -X utf8 depuracion/cst20260930/generar_ochenta_y_uno_lean.py --certificado depuracion/cst20260930/pesos_41.json --base OcelotasCuarentaYUnaTabla --carpeta depuracion/cst20260930
python -B -X utf8 depuracion/cst20260930/censo_cst.py --desde 68719476737 --N 90599563946 --salida depuracion/cst20260930/censo_41/tramo_1.json   # y así los tramos 2-6
python -B -X utf8 depuracion/cst20260930/cubrir_tramos.py --carpeta depuracion/cst20260930/censo_41 --desde 68719476737
python -B -X utf8 depuracion/cst20260930/cotejar_censo.py --N 200000000000 --desde 68719476737 --E 22 --salida depuracion/cst20260930/censo_41/cotejo_tramo.json
python -B -X utf8 depuracion/cst20260930/pesos_rachas.py --rachas 42 --H 51 --externo 300000000000 --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/pesos_42.json
python -B -X utf8 depuracion/cst20260930/generar_ochenta_y_uno_lean.py --certificado depuracion/cst20260930/pesos_42.json --base OcelotasCuarentaYDosTabla --carpeta depuracion/cst20260930
python -B -X utf8 depuracion/cst20260930/censo_cst.py --desde 200000000001 --N 216666666666 --salida depuracion/cst20260930/censo_42/tramo_1.json   # y así los tramos 2-6
python -B -X utf8 depuracion/cst20260930/cubrir_tramos.py --carpeta depuracion/cst20260930/censo_42 --desde 200000000001
python -B -X utf8 depuracion/cst20260930/cotejar_censo.py --N 300000000000 --desde 200000000001 --E 22 --salida depuracion/cst20260930/censo_42/cotejo_tramo.json
python -B -X utf8 depuracion/cst20260930/pesos_rachas.py --rachas 46 --H 51 --externo 700000000000 --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/pesos_46.json
python -B -X utf8 depuracion/cst20260930/cotejar_pesos.py --certificado depuracion/cst20260930/pesos_46.json --salida depuracion/cst20260930/cotejo_pesos_46.json
python -B -X utf8 depuracion/cst20260930/generar_ochenta_y_uno_lean.py --certificado depuracion/cst20260930/pesos_46.json --base OcelotasCuarentaYSeisTabla --carpeta depuracion/cst20260930
python -B -X utf8 depuracion/cst20260930/censo_cst.py --desde 300000000001 --N 433333333333 --salida depuracion/cst20260930/censo_46/tramo_1.json   # y así los tramos 2-3
python -B -X utf8 depuracion/cst20260930/cubrir_tramos.py --carpeta depuracion/cst20260930/censo_46 --desde 300000000001 --tramos 3
python -B -X utf8 depuracion/cst20260930/cotejar_censo.py --N 700000000000 --desde 300000000001 --E 22 --salida depuracion/cst20260930/censo_46/cotejo_tramo.json
```

## Reproducir

```text
python -B -X utf8 depuracion/cst20260930/pesos_rachas.py --rachas 81 --H 75 --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/pesos_81.json
python -B -X utf8 depuracion/cst20260930/cotejar_pesos.py --certificado depuracion/cst20260930/pesos_81.json --salida depuracion/cst20260930/cotejo_pesos_81.json
python -B -X utf8 depuracion/cst20260930/generar_ochenta_y_uno_lean.py --certificado depuracion/cst20260930/pesos_81.json --carpeta depuracion/cst20260930
```
