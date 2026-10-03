# Ocelotas: veintiuna rachas en Lean — 03-10-2026

**Estado:** cierre completo en Lean 4.32.2, sin `sorryAx`, con tabla y
certificados de prefijos cotejados independientemente. La auditoría
acumulada cubre 76 módulos y 943 consultas de axiomas; la última
reanudación compiló 31 módulos y reutilizó 45 por huellas verificadas.
[Registro final](lean_veintiuna.txt) y [evidencia completa](evidencia_veintiuna_lean.json).
Se conserva el cierre anterior de [veinte rachas](VEINTE_LEAN.md).

## Enunciado certificado

Se usa `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, para n>=2.
`S_j(n)` cuenta las entradas impares en los primeros j pasos. Un primer
cruce k exige `3^S_j(n)>=2^j` para `1<=j<k` y `3^S_k(n)<2^k`.
`rachas n k` cuenta los bloques maximales de entradas impares; no hay
ley probabilística ni condicionamiento sobre una muestra de semillas.

El ensamblaje certificado en [OcelotasVeintiuna.lean](OcelotasVeintiuna.lean) es:

```lean
theorem cst_veintiuna_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 21) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

`LMN23` conserva como hipótesis externa el corolario publicado,
especializado en 2 y 3; su [traducción a LMNDebil](LECTURAS_20261003.md)
está formalizada. La existencia del primer cruce es otra hipótesis.
El enunciado no afirma que todo n tenga ese cruce ni que llegue a 1.
`fallo_exige_veintidos` exige al menos 22 rachas para un fallo bajo las
mismas hipótesis; el caso par está incluido.

## Cota racional del tiempo

Se conserva el mapa atajo T, n>=2, y un primer cruce finito k. Ponemos
q=S_k(n), el número de entradas impares. La ventana del primer cruce da
`2^k<=2*3^q`. Para naturales u,v con `3^v<=2^u`, elevar a v da

`2^(v*k) <= 2^v*3^(v*q) <= 2^(u*q+v)`.

La monotonía de las potencias implica `v*k<=u*q+v`. Tomando u=8 y v=5,
`3^5=243<256=2^8`, y por tanto

**`5*k<=8*q+5`.**

La prueba escrita usa sólo enteros. Su formalización está en
[OcelotasTiempoRacional.lean](OcelotasTiempoRacional.lean), compilada en
Lean 4.32.2 con axiomas estándar y sin `sorryAx`. Vale también para
q=0; no necesita LMN ni una cota de rachas.

La preparación inicial con cola desde `2^33` se detuvo: los intervalos
racionales actuales de log 2 y log 3 no certifican el signo de una nueva
pareja. No se generó una tabla con signos inciertos. La cota racional
permite mantener la tabla de 42 intervalos hasta q<4598951775 y la cola
desde k>=2^32.

## Cola de veintiuna rachas

[OcelotasVeintiunaCola.lean](OcelotasVeintiunaCola.lean) demuestra
`cota(21,M)<=32237*M`. Para t>=32, por inducción,

`8*32237*(19*(t+33)^2+6)+5 < 5*2^t`.

El factor 19 pertenece a LMN. En t=32, el margen entero entre ambos
lados es 770687699. El supuesto fallo, LMN y la criba dan
`q<=32237*(19*(t+33)^2+6)`. Junto con `5*k<=8*q+5` contradice `2^t<=k`.
Esta cola se ensambla con las obligaciones finitas certificadas abajo.

## Certificados finitos

[La tabla](preparacion_veintiuna_lean.json) tiene 42 filas: cinco se
excluyen por la criba afinada, 35 remiten al certificado conservado hasta
n=4912740 y dos exigen prefijos. [Cotejo racional independiente](cotejo_veintiuna_lean.json)
sin discrepancias.

| Intervalo inclusivo de n | q mínimo | Nodos | Profundidad máxima | Clases no vacías |
|---|---:|---:|---:|---:|
| 4912741..5730313 | 79335 | 161365 | 48 | 19624 |
| 4912741..325543668 | 190537 | 670749 | 51 | 183177 |

Combustible 128, un millón de nodos por caso, sin obligaciones pendientes.
Los certificados están condicionados a un máximo de 21 rachas y al
q mínimo señalado. Los intervalos se solapan: no sumar sus cardinalidades
817573 y 320630928. El [cotejo independiente](cotejo_prefijos_21.json)
reconstruye las órbitas de representantes, cotas y clases disjuntas.

[OcelotasVeintiunaPrefijos.lean](OcelotasVeintiunaPrefijos.lean) certifica
la evaluación en bloques a profundidad doce: 226 y 207 bloques no
terminales, con 565 y 555 nodos de ensamblaje. La primera compilación
en un único módulo se detuvo al superar 6 GB junto con otra auditoría.
Se separaron las 561 hojas en nueve módulos de hasta 64 hojas. Los seis
primeros compilaron, pero el séptimo concentraba unos 460000 nodos y
agotó casi toda la memoria disponible. Se detuvo esa segunda ejecución.
[dividir_hojas_prefijos.py](dividir_hojas_prefijos.py) subdivide ahora sus
64 raíces en 213 hojas de hasta 5000 nodos, repartidas en 25 módulos de
hasta 20000 nodos cada uno; 149 uniones conservan los nombres públicos.
Lean comprueba las partes y su ensamblaje. La estimación del coste sólo
elige la partición y no es una hipótesis matemática.

Los 35 archivos de prefijos, incluidas las partes nuevas del séptimo
módulo, se reprodujeron byte por byte en una carpeta temporal. La opción
nueva conserva también la salida original de veinte rachas cuando no se usa.

La auditoría se interrumpió brevemente durante la petición de cierre de
sesión y se reanudó después de la indicación de terminar esta tanda.
El [registro de la interrupción](lean_veintiuna_interrumpido_cierre.txt)
conserva 45 módulos aceptados; su último código no nulo corresponde al
proceso detenido. La reanudación reutilizó esos 45 módulos y comprobó
los 31 restantes, todos con código 0. No se presenta esa ejecución como una reconstrucción
limpia de los 76 módulos.

### Auditoría final y registro

La [evidencia completa](evidencia_veintiuna_lean.json) conserva las salidas
originales de los 76 módulos, incluidas las de los reutilizados. Se
verificaron las huellas SHA256 de cada fuente y objeto, la cadena de
dependencias y el comprobador. Las 943 consultas `#print axioms` coinciden
con las fuentes: 180 listas de axiomas estándar y 763 respuestas sin
axiomas; incluyen consultas repetidas, no 943 teoremas distintos.
Ninguna usa `sorryAx` ni axiomas ajenos a `propext`, `Classical.choice`
y `Quot.sound`.

El [registro versionado](../coherencia20260913/registro.json) incorpora
`ocelotas_cst_veintiuna_rachas_prefijos_lean`. La base regenerada reúne
260 afirmaciones; [controles de integridad y referencias](registro_veintiuna.txt).
La sesión se cierra a petición del usuario, terminada esta tanda.

### Ensayo de una criba más ajustada

En el intervalo alto se comparó la recurrencia entera con alfa=317/200
y beta entero ([652463 nodos](prefijos_racionales_21_alto.json)), y con
beta en múltiplos de 1/256 ([616071 nodos](prefijos_afinados_21_alto.json)).
Son propuestas exploratorias, sin nuevo cotejo independiente ni
formalización de su uso por prefijos. El ahorro frente a los 670749
nodos actuales no justifica cambiar la prueba de esta tanda.
Se conserva la implementación anterior; el ensayo racional está en
[explorar_prefijos_racionales.py](explorar_prefijos_racionales.py).

## Reproducir el cierre

```text
python -B -X utf8 depuracion/cst20260930/preparar_cierre_lean.py --rachas 21 --bits-cola 32 --tiempo-racional 8 5 --salida depuracion/cst20260930/preparacion_veintiuna_lean.json
python -B -X utf8 depuracion/cst20260930/explorar_criba_prefijos.py --inicio 4912741 --limite 5730313 --q-min 79335 --rachas 21 --combustible 128 --criba entera --max-nodos 1000000 --salida depuracion/cst20260930/prefijos_21_bajo.json
python -B -X utf8 depuracion/cst20260930/explorar_criba_prefijos.py --inicio 4912741 --limite 325543668 --q-min 190537 --rachas 21 --combustible 128 --criba entera --max-nodos 1000000 --salida depuracion/cst20260930/prefijos_21_alto.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos.py --certificados depuracion/cst20260930/prefijos_21_bajo.json depuracion/cst20260930/prefijos_21_alto.json --salida depuracion/cst20260930/cotejo_prefijos_21.json
python -B -X utf8 depuracion/cst20260930/cotejar_veintiuna_lean.py --certificado depuracion/cst20260930/preparacion_veintiuna_lean.json --salida depuracion/cst20260930/cotejo_veintiuna_lean.json
python -B -X utf8 depuracion/cst20260930/generar_prefijos_lean.py --bajo depuracion/cst20260930/prefijos_21_bajo.json --alto depuracion/cst20260930/prefijos_21_alto.json --profundidad 12 --espacio OcelotasVeintiunaPrefijos --hojas-por-modulo 64 --salida depuracion/cst20260930/OcelotasVeintiunaPrefijos.lean
python -B -X utf8 depuracion/cst20260930/dividir_hojas_prefijos.py --origen depuracion/cst20260930/OcelotasVeintiunaPrefijosHojas07.lean --salida depuracion/cst20260930/OcelotasVeintiunaPrefijosHojas07.lean --nodos-hoja 5000 --nodos-modulo 20000
python -B -X utf8 depuracion/cst20260930/generar_veintiuna_lean.py --certificado depuracion/cst20260930/preparacion_veintiuna_lean.json --salida depuracion/cst20260930/OcelotasVeintiunaTabla.lean
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_veintiuna.txt
```

Sin `--tiempo-racional`, el preparador conserva la cota anterior k<=2q
y reproduce byte por byte la propuesta de veinte rachas. La revisión
humana y la formalización de la prueba trascendente de LMN siguen
pendientes. No se amplía el censo conservado hasta `2^23`.

## Exploración siguiente: veintidós

Con las mismas parejas, las cotas exclusivas de las dos semillas pasan
a 6003187 y 341045748. El ensayo entero con combustible 128 y presupuesto
de un millón de nodos por caso produjo:

- [Caso bajo](prefijos_22_bajo.json): 339401 nodos, profundidad 55, sin
  pendientes.
- [Primer caso alto](prefijos_22_alto.json): presupuesto agotado, conservado
  como resultado incompleto. Con presupuesto posterior de cinco millones,
  el [caso alto completo](prefijos_22_alto_5m.json) cerró con 3840535 nodos
  y profundidad 57.

El [cotejo independiente](cotejo_prefijos_22.json) coincidió en 862805
clases no vacías. Se preparó una [tabla de 42 filas](preparacion_veintidos_lean.json)
con puente entre el objetivo de tabla `2^32` y la cola desde `2^33`;
su [cotejo racional](cotejo_veintidos_lean.json) pasó sin discrepancias.

La cola requiere un puente adicional. Por `2^3<3^2` y `3^q<2^k`,
se obtiene `3q<2k`. Para q>=4598951775, esto permite tratar el tramo
`2^32<=k<2^33`, usando A=51580: el margen de
`15*4598951775 - 2*(8*A*(19*65^2+6)+5)` es 2729972935.
Desde t=33, el margen de `5*2^t-(8*A*(19*(t+33)^2+6)+5)`
es 8795460155 y su crecimiento admite la inducción anterior.
[OcelotasVentanaRacional.lean](OcelotasVentanaRacional.lean) formaliza
`3q<2k` y [OcelotasVeintidosCola.lean](OcelotasVeintidosCola.lean) formaliza
el puente y la cola. Ambos compilaron con axiomas estándar, sin `sorryAx`.
Faltan generar y evaluar los certificados de prefijos en Lean, la tabla
Lean y el ensamblaje; estas piezas auxiliares no constituyen un cierre
de veintidós rachas.
