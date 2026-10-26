# Perdices: rigidez de intercambios y constantes matriciales

26-10-2026. Continúa [Soportes, §5](../perdices20261007/SOPORTES_MATRICES_H.md#5-siguiente-tanda).
**Resultado:** en dimensión dos, si los cinco símbolos interiores conectan
ambas coordenadas, las seis desigualdades de sus matrices son igualdades.
Además, en cualquier dimensión natural finita se excluye una primera
eliminación cuando las dos matrices binarias son la misma `tI`, sin cota
de coeficientes o constantes. No se clasifica el caso general ni se
demuestra la terminación de H. Revisión humana y prioridad pendientes.

## 1. Dominio y alcance

El atajo es `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, sobre enteros
positivos. El mapa parcial H es `3n/4` en `n=0 mod 4` y `(9n+1)/8` en
`n=7 mod 8`; fuera de esas clases queda indefinido. Un paso H agrupa dos
o tres pasos T. Se conserva el enlace escrito del objetivo 57 con H en
[Matrices H](../perdices20261007/MATRICES_H.md#1-fuente-sistema-y-alcance-de-la-reducción),
sin formalizarlo nuevamente ni trasladarlo al mapa G o a los bloques A/B.

El objeto probado aquí es algebraico. Cada letra minúscula se interpreta
como `z ↦ M_x z+v_x` en `ℕ^d`, incluido cero. No hay distribución aleatoria
ni condicionamiento orbital. `XY` significa `X∘Y`; actúa primero Y.
Las mayúsculas A,B,E,F,G de las fórmulas siguientes son **matrices de
letras**, no bloques de paridades ni ramas de H. Los índices 2×2 son 0,1.
El orden débil compara cada coeficiente y cada constante; una dinámica
es estricta si su constante 0 izquierda supera a la derecha.

Se mantienen las tres dinámicas de la primera etapa y las nueve estáticas:

```text
da ≥ d, dbaa ≥ dabe, dbba ≥ dbaf;
ea ≥ ae, fa ≥ be, ga ≥ af, eb ≥ bf, fb ≥ ag, gb ≥ bg;
ec ≥ bc, fc ≥ aac, gc ≥ bac.
```

La fuente archivada es [objetivo 57](../perdices20261007/bv_objetivo57_n2_c3.json),
derivada del commit `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340` de
Yolcu–Aaronson–Heule, ya cotejado en la nota anterior. Una primera
eliminación no basta para certificar toda la terminación relativa.

## 2. Las trazas anulan las holguras entre matrices acopladas

Pongamos `U=A+B`, `V=E+F+G`, `W=U+V`. Sumar las seis desigualdades
matriciales de intercambio da `K=VU-UV ≥ 0`, entrada a entrada.
Por la ciclicidad de la traza, `tr K=0`. En dimensión dos, las dos entradas
diagonales no negativas son entonces cero. También

```text
tr(KW) = tr((VU-UV)(U+V)) = 0,
K01 W10 + K10 W01 = 0.
```

La primera identidad se obtiene expandiendo los cuatro productos y
cancelando `tr(VU²)=tr(UVU)` y `tr(VUV)=tr(UV²)`. Si `W01,W10>0`, ambos
sumandos de la segunda línea son no negativos; por tanto `K01=K10=0`.
Así `VU=UV`. Cada una de las seis holguras originales es no negativa y
su suma es cero en cada entrada, luego

```text
EA=AE, FA=BE, GA=AF, EB=BF, FB=AG, GB=BG.               (1)
```

La condición de conexión sólo usa a,b,e,f,g. No se incorpora d: no figura
en los seis intercambios. Sin conexión bidireccional, se conserva la
igualdad de las entradas diagonales y la identidad cruzada, pero no se
afirma (1) completa. La prueba funciona sobre reales con las hipótesis
indicadas y, en particular, sobre los naturales del buscador.

## 3. Las constantes conservan holguras

Sean `u=v_a+v_b` y `v=v_e+v_f+v_g`. La suma de las seis diferencias
constantes es

```text
V u + 2v - U v - 3u.                                  (2)
```

No es una traza nula. Por ejemplo, sea J la matriz 2×2 llena de unos.
Tomando `A=B=J`, `E=F=G=2J`, `v_a=v_b=(1,1)` y las otras tres constantes
cero, (1) se cumple y cada diferencia constante vale `(3,3)`. El total
de (2) es `(18,18)`. Es un ejemplo de los intercambios, **no un certificado
de las doce reglas**.

Para `r` igual a la primera fila de `M_d`, las tres diferencias completas
de constantes dinámicas son

```text
Δ1 = r v_a,
Δ2 = r [(BA+B-I)v_a + (I-A)v_b - AB v_e],
Δ3 = r [(B²-B)v_a + B v_b - BA v_f].                  (3)
```

La constante exterior `v_d0` se cancela. Con matrices fijas, (2), (3) y
las nueve reglas estáticas son restricciones lineales en los vectores.
Los diez soportes anteriores describían aportes izquierdos; no bastaba
su positividad para asegurar `Δi>0`.

## 4. Una familia acoplada excluida sin cota

Supongamos ahora dimensión finita `d≥1` y `A=B=tI`, con t natural.
No se pide recta afín común y todos los vectores quedan libres.

Si t=0, la parte matricial de `da≥d` fuerza `r=0`, anulando los tres
descensos. Si t≥1, cuatro intercambios dan, cancelando t,
`F≥E`, `E≥F`, `G≥F`, `F≥G`. Por tanto `E=F=G=N`.
La parte matricial de `dbaa≥dabe` dice `t³r≥t²rN`, luego `rN≤tr`.

Definamos los escalares no negativos

```text
x=r v_a, y=r v_b, z=r v_e, w=r v_f, c=r v_c, p=rN v_c.
```

Como `v_c≥0`, se tiene `p≤tc`. Ponderar `ec≥bc` y `fc≥aac` con r da

```text
tc+y ≤ p+z,       t²c+(t+1)x ≤ p+w.
```

Se deduce `z≥y` y `w≥(t+1)x≥2x`, usando `t²c≥tc`. Las otras dos
dinámicas, tras cancelar el factor positivo t en la tercera, exigen

```text
t²z+ty+x ≤ t²x+tx+y,       x+tw ≤ tx+y.                (4)
```

La primera de (4) y `z≥y` dan `(t²+t-1)y≤(t²+t-1)x`, es decir `y≤x`.
La segunda y `w≥2x` dan `y≥(t+1)x≥2x`. Como x,y son no negativos,
`x=y=0`. Entonces (4) fuerza `z=w=0`. Los tres valores (3) son cero:
ninguna dinámica se elimina. La prueba no necesita que N sea escalar,
diagonal, invertible o esté acotada, y r puede tener entradas nulas.

Esta familia aporta casos fuera de la obstrucción de rectas naturales.
Por ejemplo, `A=B=2I`, `E=F=G=[[1,1],[1,0]]`, `r=(1,1)`, `M_c=0` y todos
los vectores cero satisfacen las doce reglas débilmente. Hay conexión
en ambos sentidos. Una recta común `(x,kx+s)` exigiría s=0 por A y
`k(k+1)=1` por E, imposible para k natural. No hay descenso estricto.

## 5. Reducciones y ensayo con constantes libres

Para buscar una primera eliminación se puede fijar `M_c=0`: c sólo aparece
al final de `ec,bc,fc,aac,gc,bac`; sus matrices pasan a cero y sus constantes
no cambian. También se puede anular la segunda fila de `M_d` y `v_d`:
d sólo encabeza las tres dinámicas, la primera fila se conserva y su
constante exterior se cancela. **No se fija `v_c=0`.** Estas reducciones
conservan cualquier candidato estricto previo.

[Buscador](buscar_constantes_libres.py): QF_LIA, matrices 2×2 con entradas
en `0..m`, vectores naturales sin cota. Cada producto de un coeficiente
desconocido por una expresión usa una selección finita de múltiplos
enteros; no hay productos entre incógnitas de QF_LIA. Las expresiones
intermedias tampoco tienen cota. Se añaden (1) sólo bajo conexión.

| Matrices | Conexión | Resultado Z3 4.15.4 | Límite |
| --- | --- | --- | --- |
| Entradas 0 o 1 | Libre | [UNSAT](lia_trazas_objetivo57_m1_libre.json) | 30 s |
| Entradas 0 o 1 | Ambos sentidos | [UNSAT](lia_trazas_objetivo57_m1.json) | 30 s |
| Entradas 0..3 | Ambos sentidos | [unknown, timeout](lia_trazas_objetivo57_m3.json) | 30 s |

Cada JSON fija fórmula SMT2, huellas, versión, semilla 0 y una hebra.
El cambio de codificador se contrastó antes de guardar estas llamadas.
UNSAT es una respuesta del solver, sin certificado Lean de insatisfacibilidad.
El timeout no decide existencia ni justifica aumentar el tiempo. Este
ensayo permite constantes arbitrarias, a diferencia de los censos antiguos.

## 6. Prueba formal y contraste independiente

[PerdicesTrazasMatrices.lean](PerdicesTrazasMatrices.lean): nueve consultas
de axiomas. Formaliza las trazas, la conmutación y las seis igualdades bajo
conexión; también el núcleo escalar de §4, con sus hipótesis explícitas.
La traducción de la familia `tI` a ese núcleo, las identidades vectoriales
(2), (3) y las reducciones de c,d conservan prueba escrita y cotejo entero.
No se formaliza el codificador, la equivalencia global con H ni la
clasificación completa de matrices. Lean 4.32.2, Mathlib fijado, axiomas
estándar, sin `sorryAx`: [evidencia](evidencia_lean_trazas.json) y
[salida](evidencia_lean_trazas.txt). Imports directos cotejados; no se
declara una auditoría transitiva nueva de todo Mathlib.

[Cotejo independiente](cotejar_trazas.py), [resultado](cotejo_trazas.json):

- 6561 pares de matrices con entradas 0..2: identidades de traza y
  conmutación en los 318 pares conectados con conmutador no negativo.
- Los 1.048.576 quintetos binarios de matrices: 8248 cumplen los seis
  intercambios débiles; los 3334 conectados cumplen las seis igualdades.
- Mil asignaciones reproducibles contrastan (2), (3) mediante evaluación
  literal de funciones. Se comprueban el ejemplo de holguras y el de Fibonacci.
- 47.500 asignaciones escalares contrastan el núcleo de §4; las siete
  admisibles tienen x=y=z=w=0.
- Los tres certificados conocidos del control 15, originales y con todos
  sus vectores multiplicados por 10.000, pasan la nueva fórmula después de
  las reducciones c,d: seis controles SAT y 132 composiciones cotejadas
  contra evaluación entera independiente.

Son controles finitos de las implementaciones, no pruebas universales.
No se repitieron los censos históricos. Z3 se instaló en un entorno virtual
temporal aislado (`z3-solver==4.15.4.0`), sin modificar la instalación global.

```powershell
python -B -X utf8 depuracion/perdices20261026/comprobar_lean.py --modulo PerdicesTrazasMatrices --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --salida depuracion/perdices20261026/evidencia_lean_trazas.json
& "$env:TEMP/perdices_trazas_20261026/Scripts/python.exe" -B -X utf8 depuracion/perdices20261026/cotejar_trazas.py --control depuracion/perdices20261007/sat_control15_n2_c3.json --objetivo depuracion/perdices20261007/bv_objetivo57_n2_c3.json --muestras 1000 --semilla 0 --salida depuracion/perdices20261026/cotejo_trazas.json
```

## 7. Qué queda abierto

La primera condición primordial pide control nuevo de una semilla positiva
fija a través de cambios arbitrarios. Aquí se restringe una familia de
certificados; no se obtiene tal control. Tampoco se demuestra transferencia
de mezcla ni se cierra una premisa mediante un resultado externo.

La familia `A=B=tI` está descartada. En el caso conectado general quedan
las seis ecuaciones (1), las tres comparaciones matriciales dinámicas y
la factibilidad de los vectores de (3) con las nueve estáticas. El caso
no conectado conserva sus holguras cruzadas permitidas. **No se declara
agotamiento de Perdices.** La continuación [con F invertible](CLASIFICACION_F_INVERTIBLE.md)
clasifica las matrices cuando A≠B en dos formas de rango uno y una
resonancia 2:3. Sus constantes, F singular y A=B no escalar quedan abiertos.
No se ampliará el timeout como sustituto de una reducción algebraica.
