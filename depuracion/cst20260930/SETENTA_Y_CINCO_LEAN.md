# Ocelotas: CST hasta 75 rachas, con LMN y Rozier–Terracol explícitos

03-10-2026. **Ensamblaje condicional terminado en Lean.** No se ha
certificado dentro del laboratorio la prueba trascendente de LMN ni
el resultado computacional de Rozier–Terracol. Revisión humana y
prioridad histórica pendientes.

## Enunciado

Se usa `T(n)=n/2` para n par y `(3n+1)/2` para n impar, con n>=2.
`S_j(n)` cuenta las entradas impares en los primeros j pasos.
El primer cruce finito k cumple `3^S_j>=2^j` para `1<=j<k` y
`3^S_k<2^k`. Las rachas son bloques maximales de entradas impares hasta k.
No hay ley probabilística ni condicionamiento muestral.

[OcelotasSetentaYCinco.lean](OcelotasSetentaYCinco.lean) prueba:

```text
LMN23 -> RozierTerracol54 -> n>=2 -> PrimerCruce n k -> rachas(n,k)<=75
      -> (n<=T^j(n) para todo j<k, y T^k(n)<n).
```

Los teoremas finales son `cst_condicional` y
`fallo_exige_setenta_y_seis`. Este último exige al menos 76 rachas
para un fallo **bajo ambas hipótesis externas**.

`RozierTerracol54` se define como la proposición que asegura descenso
en el primer cruce para `2<=n<=28000000000000000000`.
Se recibe como argumento de los teoremas, sin declararla como axioma
global ni darla por demostrada en Lean. Es la consecuencia empleada del
[corolario 5.4 de Rozier–Terracol, v5](https://arxiv.org/html/2502.00948v5#S5),
revisado nuevamente el 03-10. El artículo afirma igualdad del primer
descenso y el primer cruce en ese rango. Su prueba depende de resultados
computacionales externos; no se repitieron sus tablas.

El caso par está incluido. No se afirma existencia universal del primer
cruce ni llegada a 1. La ruta de [21](VEINTIUNA_LEAN.md), y la comprobación
en curso de [22](VEINTIDOS_LEAN.md), certifican su tramo finito en el
repositorio y usan LMN como único resultado externo.

## Tabla finita y cola infinita

La prueba escrita anterior está en [RACHAS_AFINADAS.md](RACHAS_AFINADAS.md)
y [RACHAS_UNILATERALES.md](RACHAS_UNILATERALES.md). Esta formalización
conserva esos antecedentes y usa una tabla más corta:

- [97 intervalos](preparacion_setenta_y_cinco.json), que cubren
  `1<=q<1361733414753853584389`, con q=S_k(n).
- Cada par de extremos tiene determinante uno. Los signos de sus formas
  logarítmicas y una cota positiva se certifican en Lean. El lema unilateral
  se aplica a todo q del intervalo, sin suponer coprimalidad.
- 91 filas remiten a una cota de semilla dentro del umbral externo;
  seis se excluyen mediante la criba afinada, con alfa=317/200 y beta=B/256.
  Las potencias se verifican con `decide +kernel`; los pisos con `norm_num`.
- [Logaritmos precisos](OcelotasLogaritmosPrecisos.lean): encierros de
  log 2 y log 3 con 55 decimales, por series con resto demostrado.
  Se usan 192 y 128 términos. Estos dos lemas no dependen de LMN.
- La [cola paramétrica](COLA_PARAMETRICA.md), con
  `R=75, A=3395059960557476, c=7, H=70`, excluye todos los fallos
  con k>=2^70. El extremo q de la tabla supera 2^70, y q<k.

Ante un supuesto fallo, la tabla obliga a n dentro del rango externo,
o la cola lo contradice. El ensamblaje convierte el contador real en
una palabra de rachas y concluye el descenso.

El cotejo exacto encuentra `2684909333528212357` como máxima cota
exclusiva de semilla entre las filas que sobreviven a la criba.
El enunciado de la tabla Lean usa directamente el umbral externo,
`n<28000000000000000001`; no se atribuye a ese enunciado la cota más
ajustada del cálculo auxiliar.

## Evidencia

[Auditoría completa](evidencia_setenta_y_cinco.json) y
[salida](evidencia_setenta_y_cinco.txt): Lean 4.32.2,
11 módulos compilados y 110 consultas de axiomas, sólo `propext`,
`Classical.choice`, `Quot.sound`, sin `sorryAx`.
Se reutilizaron 38 módulos previos con entorno, fuentes y objetos
comprobados por huellas. No es una reconstrucción limpia de todos ellos.

[Cotejo independiente](cotejo_setenta_y_cinco.json): logaritmos mediante
series racionales de atanh, determinantes, signos, cobertura, techos de
semilla, potencias y recurrencia entera de denominador 6400. Las 97 filas
y la cola coincidieron. Este cotejo no importa el generador ni verifica
el resultado externo. El censo conservado hasta 2^23 permanece intacto.

```text
python -B -X utf8 depuracion/cst20260930/preparar_setenta_y_cinco.py --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --colas depuracion/cst20260930/colas_parametricas.json --salida depuracion/cst20260930/preparacion_setenta_y_cinco.json
python -B -X utf8 depuracion/cst20260930/cotejar_setenta_y_cinco.py --certificado depuracion/cst20260930/preparacion_setenta_y_cinco.json --salida depuracion/cst20260930/cotejo_setenta_y_cinco.json
python -B -X utf8 depuracion/cst20260930/generar_setenta_y_cinco_lean.py --certificado depuracion/cst20260930/preparacion_setenta_y_cinco.json --salida depuracion/cst20260930/OcelotasSetentaYCincoTabla.lean --filas-por-modulo 16
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasSetentaYCinco --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_setenta_y_cinco.json
```

## Próxima frontera

La [exploración de 76, 77 y 80](frontera_externa_76_80.json) localiza
los intervalos que la tabla aún no descarta. No está cotejada ni
formalizada. Para R=76 queda una ventana:

```text
28000000000000000001 <= n <= 42380653296441592424,
130441933147714940 <= q < 397560349370386783.
```

El primer ensayo de 500000 nodos agotó su presupuesto y se conserva en
[prefijos_76_externo_500k.json](prefijos_76_externo_500k.json).
El [ensayo entero completo](prefijos_76_externo_5m.json) terminó en
3747781 nodos, profundidad 85, sin pendientes. La
[variante afinada](prefijos_76_afinados_5m.json) reduce la propuesta a
11225 nodos, profundidad 77, también sin pendientes. Ambas representan
14380653296441592424 semillas; no se suman sus coberturas.

El [cotejo independiente de la variante afinada](cotejo_prefijos_76_afinados.json)
coincidió en 4910 clases no vacías: órbitas directas, otro representante,
recurrencia racional, potencias y cobertura disjunta. La tabla completa
de 76 sigue siendo exploratoria y falta el certificado Lean de la
ventana. La variante afinada necesita formalizar su uso
después de un corte: extender `criba_contador` y `criba_despues_corte`
de [OcelotasPrefijos.lean](OcelotasPrefijos.lean), conectar la recurrencia
entera `(25B+10144C)/6400` con la criba real, y adaptar el verificador.
Una extensión requiere resolver estas obligaciones antes de afirmar
CST hasta 76 en esa etapa. La continuación quedó después
[cerrada en Lean por la evaluación binaria](SETENTA_Y_SEIS_LEAN.md),
con las mismas dos hipótesis externas. La descripción anterior conserva
la propuesta inicial y sus límites en el momento de prepararla.
