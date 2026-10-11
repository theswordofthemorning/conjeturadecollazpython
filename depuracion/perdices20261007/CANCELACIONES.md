# Perdices: resonancia y reinicios al alternar 1 y 110

10-10-2026. Continúa [Repeticiones](REPETICIONES.md). El término de
cancelación se convierte en un filtro exacto y en una transición entre
cambios de bloque. Se formalizan 20 lemas, ahora con valuaciones y la
función G explícita. No se reclama prioridad. **La clase `1`/`110` es
un ensayo restringido; su exclusión universal tampoco queda probada.**

## 1. Dominio, mapas y unidades

T es el atajo sobre naturales: n/2 para par, (3n+1)/2 para impar.
Se estudian concatenaciones de A=1 y B=110, con sus paridades reales.
En una entrada de B se escribe `x=4z-1`, con z impar positivo.
[Repeticiones, §4](REPETICIONES.md#4-el-término-que-aparece-al-cambiar-de-bloque)
dedujo la transición entre entradas consecutivas de B:

```text
v=v2(9z+1),  a=v-3,
G(z)=3^a(9z+1)/2^v,                 dominio z=7 mod 8.   (1)
```

`v2` y `v3` son valuaciones de enteros positivos. El paso G realiza
el bloque `B A^a` y termina en otra entrada de B. Salir de su dominio
significa que no se puede seguir obteniendo entradas de B de esa forma;
no es necesariamente el instante del primer bit incompatible con A/B.
Los pasos de G y de T se cuentan por separado. Todo es determinista;
no se asigna una ley aleatoria a una semilla natural fija.

En Lean, G es una función total de naturales; `Persiste z` exige
explícitamente `G^j(z)=7 mod 8` para todo j. No se usa la definición
total fuera del dominio para afirmar una trayectoria de la clase.

## 2. La valuación que se consume de tres en tres

Poner `v=v2(z+1)`. Estar en el dominio equivale a v>=3. Si v>3,
entonces `16 | z+1`, `v2(9z+1)=3`, a=0 y

```text
G(z)+1=9(z+1)/8,
v2(G(z)+1)=v-3.                                        (2)
```

La primera valuación de (1) se prueba porque `9z+1` es múltiplo de
8 pero no de 16. El factor 9 no modifica la segunda. Ambas identidades,
la equivalencia de dominio y la consecuencia infinita

```text
Persiste z => 3 divide v2(z+1)                           (3)
```

están en Lean. La prueba de (3) es inducción fuerte sobre v: cada
paso con v>3 lo reduce en tres; v=3 es el caso de cambio.

Si v no es múltiplo de tres, se sale del dominio exactamente tras
`floor(v/3)` pasos G. Lean certifica una salida **a más tardar** en
ese número de pasos; (2) demuestra por escrito que los anteriores
todavía están dentro. No se afirma que un múltiplo de tres baste
para persistir indefinidamente.

Si v=3c, c>=1, escribir `z+1=8^c q`, q impar. Tras c-1 pasos sin
cambio se alcanza `z_*+1=8*9^(c-1)q`, cuya valuación es 3. La
identidad general `G^b(z)+1=8*9^b q` cuando `z+1=8^(b+1)q`
está formalizada en `iteracion_ceros`.

## 3. F: observar solamente los cambios

En un cambio se escribe `z=8h-1`, h impar positivo, y la semilla
original de T es `x=32h-5`. Definir

```text
a=v2(9h-1)>=1,   m=(9h-1)/2^a impar,
K=3^a m+1,       k=v2(K)>=1.                            (4)
```

Se tiene `G(z)+1=K`. Si k no es múltiplo de tres, la trayectoria
sale del dominio de G después de `1+floor(k/3)` pasos desde z.
Si `k=3b`, b>=1, existe otro cambio tras b pasos G:

```text
F(h)=9^(b-1) K/2^(3b),
G^b(8h-1)+1=8 F(h).                                    (5)
```

La palabra realizada por T es `B A^a B^(b-1)`, de longitud
`a+3b` y con `a+2b` entradas impares. No se elige una semilla
nueva entre esos bloques. `carga_transicion` y
`reinicio_correspondencia` certifican (4)–(5) en Lean. Su lectura
completa como palabra de paridades conserva la derivación escrita.

En Lean, `reinicio` también es total, pero sus teoremas exigen h
positivo impar y k=3b>0. El cotejador devuelve `None` cuando no
hay un reinicio admisible; no itera F fuera de esa condición.

### Tamaño y perfil de la salida

Como a>=1, `(3/2)^a>=3/2`, de modo que
`K=(3/2)^a(9h-1)+1>=(27h-1)/2>=13h`. Además
`8F(h)=(9/8)^(b-1)K>=K`. En Lean:

```text
8F(h)>=13h,       v3(F(h))=2(b-1).                      (6)
```

La segunda igualdad usa `K=1 mod 3` y que dividir por potencias
de 2 no cambia la valuación 3-ádica. Cada reinicio aumenta h al
menos por 13/8 y su salida tiene valuación 3-ádica par.
**Es un perfil de la salida, no un filtro sobre la semilla inicial.**
Por ejemplo, h=3 tiene v3 impar y realiza el reinicio F(3)=5.

Las identidades finitas permiten escribir la equivalencia siguiente:
una trayectoria positiva infinita en la clase A/B produce, después
de un tramo finito, una sucesión infinita de reinicios admisibles F;
recíprocamente, tal sucesión produce una fuga pura de T desde
`32h-5`. La equivalencia infinita completa tiene prueba escrita:
(2) llega a un cambio en tiempo finito, (5) enlaza los siguientes,
y cada bloque A/B conserva P>=1. No se prueba que exista esa sucesión
ni que sea imposible. Tampoco se identifica esta clase con todo MuroB.

## 4. La inversa y el alcance de una condición 3-ádica

De una posible salida y se recuperan las etiquetas del reinicio:

1. y debe ser impar positivo, y `v3(y)=2c` debe ser par. Poner b=c+1.
2. Recuperar `K=8^b*y/9^c` y `a=v3(K-1)`, que debe ser >=1.
3. Poner `m=(K-1)/3^a`. Se requiere `2^a m+1=0 mod 9`.
   El único predecesor posible es `h=(2^a m+1)/9`.

Estas condiciones son suficientes: m es impar, h es impar positivo,
`v2(9h-1)=a`, y `v2(K)=3b`, porque y/9^c es impar. Sustituir en
(4)–(5) devuelve y. Por tanto F es inyectiva en su dominio admisible.
Este criterio inverso completo conserva prueba escrita y cotejo;
Lean certifica el perfil (6), no toda la inversa.

El perfil no añade una criba independiente al cálculo afín:
recupera las etiquetas que produjo la misma transición. Imponerlo
sobre todo h inicial excluiría indebidamente fuentes como h=3.

### Fuentes sin predecesor que duran cualquier corte prefijado

La rama a=b=1 equivale a `h=3 mod 32`, con
`F(h)=(27h-1)/16`. Satisface

```text
16(11F(h)-1)=27(11h-1).
```

Para cualquier r>=0, elegir por el teorema chino del resto

```text
h=11^(-1) mod 2^(4r+1),        h=3 mod 9.                (7)
```

Se obtiene h impar positivo. Para r>=1, la primera congruencia
implica h=3 mod 32; tras una aplicación se pierde exactamente
un factor 16 y queda la condición para r-1. Por inducción realiza
al menos r reinicios de la rama (1,1). Pero v3(h)=1, por lo que h
no es imagen de ningún reinicio admisible, según (6).

No hay un número uniforme de reinicios futuros que fuerce la
existencia de un predecesor. **Varía h con r**: (7) no construye
una fuente con futuro infinito. La prueba general es escrita;
se cotejó r=0..16 con F y con la palabra T `(1101)^r`.

## 5. Toda historia finita de cambios tiene un cilindro modular

Para etiquetas a,b>=1, (5) equivale a

```text
2^d h'=A h-E,
d=a+3b, A=3^(a+2b), E=9^(b-1)(3^a-2^a)>0.             (8)
```

La condición exacta de esa rama es una única clase impar:

```text
h=(E+2^d) A^(-1) mod 2^(d+1).                          (9)
```

En efecto, (9) da h' impar. Reducir (8) módulo `2^(a+1)` da
`v2(9h-1)=a`; luego (8) da `v2(K)=3b`. No falta una condición
oculta entre las etiquetas. La salida es positiva: `E/A<1/9`
y h>=1. El mismo argumento hacia atrás permite componer ramas.

Para una historia finita, componer `M h_final=A_total h-E_total`.
Exigir h_final impar deja exactamente
`h=(E_total+M) A_total^(-1) mod 2M`. Todos los enteros positivos
de esa clase realizan el historial. Esto tiene prueba escrita y
cotejo; no se formaliza toda la codificación en este módulo.

Así, un par o una historia finita de etiquetas no puede prohibirse
universalmente sólo por las congruencias. Lo pendiente sigue siendo
si los representantes de una historia **infinita** pueden estabilizarse
en un mismo natural. No se multiplican probabilidades ni se infiere
un resultado universal del tamaño de los conjuntos finitos.

## 6. Evidencia, límites y próximo paso

[PerdicesCancelaciones.lean](PerdicesCancelaciones.lean): 20 lemas,
incluidos (2), (3), la salida acotada, (5), crecimiento y perfil (6).
[comprobar_cancelaciones.py](comprobar_cancelaciones.py) audita 26
módulos previos y compila sólo el nuevo: 27 módulos propios,
329 consultas, Lean 4.32.2, sólo axiomas estándar, sin avisos ni
pruebas incompletas. Se incorpora `Mathlib.NumberTheory.Padics.PadicVal.Basic`:
fuente cotejada con la revisión fijada y huellas de fuente/objeto
registradas. [Evidencia](evidencia_cancelaciones.json) y
[salida](evidencia_cancelaciones.txt). Revisión humana pendiente.

[cotejar_cancelaciones.py](cotejar_cancelaciones.py), enteros exactos:

- z=0..4095: 512 entradas del dominio G; 219 salen por la condición
  v mod 3, y 293 llegan al siguiente cambio. Llegar no certifica persistencia.
- h impar, 1..4095: 2048 entradas; 291 reinicios admisibles y 1757
  salidas tras el cambio. Se comparan 1566 pasos de T y 128 inversas
  cuyo valor final está dentro del mismo rango.
- Cadenas desde esas 2048 semillas, corte 32: todas salen; máximo
  observado de cuatro reinicios antes del fallo, desde h=323.
  **Es medición finita**, no una cota universal. El programa cuenta
  por separado las cadenas truncadas y no las considera terminadas.
- a,b=1..3, hasta tres cambios: 820 historias, 1640 representantes,
  4716 transiciones F y 37728 pasos T, incluida la historia vacía.
- (7), r=0..16: 17 longitudes y 136 reinicios comprobados.

[Resultado](cotejo_cancelaciones.json). Los casos mínimos de CLI
incluyen corte cero para comprobar que se informa como truncamiento.
No se relanzan censos anteriores.

El [registro versionado](../coherencia20260913/registro.json) añade
`perdices_cancelaciones_resonancia` y `perdices_cancelaciones_reinicios`,
separando el alcance formal de las pruebas escritas: 314 afirmaciones,
208 demostradas, 86 medidas, 12 conjeturadas y ocho refutadas.
Se regenera `afirmaciones.db` con el generador existente; se conservan
las entradas anteriores y `respuestas.db`.

**Siguiente:** buscar una cota de crecimiento de los representantes
en historiales no periódicos de una misma semilla. El perfil inverso
y la resonancia ya son explícitos, pero no pueden tratarse como
restricciones independientes. Contrastar cualquier argumento primero
en F y después en los bloques generales entre mínimos futuros;
resolver sólo esta clase no resolvería todo MuroB.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_cancelaciones.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_cancelaciones.json
python -B -X utf8 depuracion/perdices20261007/cotejar_cancelaciones.py --zmax 4095 --hmax 4095 --corte 32 --amax 3 --bmax 3 --qmax 3 --rmax 16 --salida depuracion/perdices20261007/cotejo_cancelaciones.json
```

Si faltan objetos previos, reproducir primero [Repeticiones](REPETICIONES.md).
