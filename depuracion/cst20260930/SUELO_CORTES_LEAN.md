# Ocelotas: suelo después de un corte y verificador

03-10-2026. **Conexión universal, verificador y piloto aceptados en Lean.**
Continuación de la [criba con suelo](SUELO_RACHAS_LEAN.md). No usa LMN
ni Rozier–Terracol. Se amplía esa afirmación del registro; las consultas
de axiomas y las implementaciones no se cuentan como resultados separados.

## Enunciado y derivación

Mapa: `T(n)=n/2` para n par y `(3n+1)/2` para n impar, sobre naturales.
`S_j(n)` cuenta entradas impares en los primeros j pasos; `r_j(n)` cuenta
sus bloques maximales. `PrimerCruce n k` significa que
`3^S_j >= 2^j` para `1<=j<k` y `3^S_k < 2^k`.

Sean un primer cruce finito k, un corte `i<k` que sea vacío o siga a
una entrada par, y un presupuesto `r_k<=R`. Si

```text
n >= 4095,        T^i(n) <= X,
B >= 512,        (X+1)^256 <= 2^B,
C(B,0) = 0,
C(B,j+1) = (400B + 162304 C(B,j) - 102375j) div 102400,
```

entonces

```text
S_k(n) <= S_i(n) + C(B, R-r_i(n)).
```

La resta de la recurrencia es no negativa, como ya demuestra
`OcelotasSueloNumerica`. La cota real usa `alfa=317/200`, `beta=B/256`
y `gamma=4095/4096`.

Derivación independiente del código de prefijos:

1. Antes del primer cruce global, `T^j(n)>=n`. Por ello el sufijo
   iniciado en i conserva el suelo n hasta antes de k.
2. El primer cruce acaba con una entrada par. El sufijo admite pares
   iniciales y luego una palabra de bloques impares y pares; el último
   bloque par puede quedar cortado en k.
3. Si hay pares iniciales, se eliminan sin añadir entradas impares ni
   rachas y sin aumentar el valor de arranque. Las congruencias con suelo
   acotan los bloques restantes desde `T^i(n)+1`.
4. Al cortar después de un par, los contadores se suman exactamente:
   `S_k=S_i+S_sufijo` y `r_k=r_i+r_sufijo`. La monotonía de C permite
   sustituir `r_sufijo` por `R-r_i`.

**No se supone que k-i sea un primer cruce del sufijo, ni que el valor
final sea mayor o igual que el suelo.** Tampoco se supone un fallo de CST
para la desigualdad anterior. No hay ley probabilística.

## Formalización y auditoría

- [OcelotasSueloContador.lean](OcelotasSueloContador.lean):
  `criba_contador` permite pares iniciales; `criba_real_despues_corte`
  conserva parámetros reales generales; `criba_desde_potencia` especializa
  la fórmula entera. [Auditoría](evidencia_suelo_contador.json): cinco
  módulos, uno nuevo, 23 consultas.
- [OcelotasCribaPrefijosSuelo.lean](OcelotasCribaPrefijosSuelo.lean):
  verificador por residuos con suelo `n>=4095`, corrección universal
  y certificado de descenso. Sólo aplica la criba al corte admisible
  con `B>=512`. Agotar combustible rechaza. Se conservan los verificadores
  anteriores. [Auditoría](evidencia_criba_prefijos_suelo.json): siete
  módulos reutilizados y comprobados por huellas, 28 consultas.
- [OcelotasSueloPiloto.lean](OcelotasSueloPiloto.lean): el núcleo evalúa
  el verificador con `decide +kernel`, sin tomar el JSON como premisa.
  [Auditoría final](evidencia_suelo_piloto.json): ocho módulos, dos
  compilados y seis reutilizados, 30 consultas; 27 módulos de base
  verificados por huellas.

Lean 4.32.2, commit `f3b06c705e6c85f5314019d5d3baab0fec5b580c`.
Las consultas contienen sólo axiomas estándar, sin `sorryAx`; el piloto
`acepta` usa únicamente `propext`. Son siete declaraciones consultadas
en los tres archivos nuevos; las 30 consultas incluyen dependencias.
Se conserva el [intento inicial fallido](intento_criba_prefijos_suelo_01.txt)
por transcripción de desigualdades; no es evidencia aceptada.

## Cotejos independientes y piloto

[Cotejo de cortes](cotejo_suelo_cortes.json), producido por
[órbitas directas y Fraction](cotejar_suelo_cortes.py), sin importar
generadores: todas las 4097 semillas de 4095 a 8191, 14253 pasos,
7131 cortes admisibles y 28524 cotas, sin discrepancias. Incluye
3034 cortes interiores, 3558 sufijos iniciados en par y 3083 sin
entradas impares. En 2830 semillas el primer cruce termina bajo 4095.
Se verifican dos cotas del valor actual y dos presupuestos de rachas.

Piloto: semillas `4095..8191`, `q>=60`, `R=4`, combustible 64.
La [preparación](preparar_piloto_suelo.py) conserva las hojas en
[piloto_suelo.json](piloto_suelo.json). El
[cotejador independiente](cotejar_piloto_suelo.py) reconstruye los
prefijos por órbitas directas, calcula las cotas con `Fraction` y comprueba
clases disjuntas, cobertura y motivos de todas las hojas:
[resultado](cotejo_piloto_suelo.json).

| Criba | Nodos | Hojas vacías | Hojas de descenso | Hojas de criba |
|---|---:|---:|---:|---:|
| Original afinada | 349 | 88 | 11 | 76 |
| Descuento por racha | 345 | 86 | 11 | 76 |
| Suelo | 339 | 83 | 11 | 76 |

Las tres cubren las mismas 4097 semillas, sin hojas pendientes.
La reducción frente al descuento es de seis nodos, aproximadamente
1,74 %, en este piloto. No es una comparación de tiempos ni una garantía
universal de mejora. El caso concreto con suelo está aceptado en Lean;
la tabla comparativa está cotejada independientemente en Python.

## Límite y siguiente paso

Queda disponible la criba con suelo en un verificador universal y un
piloto pequeño. Falta adaptar los certificados de árboles con testigos
para usarla en ventanas grandes; no se ha certificado con ella una
frontera nueva de rachas mediante esta criba. La cadena independiente de
[23 bajo LMN](VEINTITRES_LEAN.md) terminó el 03-10 a las 23:59:59;
también siguen vigentes 77 bajo LMN y Rozier–Terracol.
No se demuestra existencia universal del primer cruce ni llegada a 1.
Revisión humana y prioridad histórica pendientes.

## Reproducción

```powershell
python -B -X utf8 depuracion/cst20260930/cotejar_suelo_cortes.py --inicio 4095 --limite 8191 --max-pasos 4096 --salida depuracion/cst20260930/cotejo_suelo_cortes.json
python -B -X utf8 depuracion/cst20260930/preparar_piloto_suelo.py --inicio 4095 --limite 8191 --q-min 60 --rachas 4 --combustible 64 --max-nodos 10000 --salida depuracion/cst20260930/piloto_suelo.json
python -B -X utf8 depuracion/cst20260930/cotejar_piloto_suelo.py --certificado depuracion/cst20260930/piloto_suelo.json --salida depuracion/cst20260930/cotejo_piloto_suelo.json
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasSueloPiloto --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_descuento_20261003 --salida depuracion/cst20260930/evidencia_suelo_piloto.json
```

El auditor persistente comprueba fuentes, dependencias, versión de Lean,
objetos y consultas; sólo debe ejecutarse una instancia por caché.
