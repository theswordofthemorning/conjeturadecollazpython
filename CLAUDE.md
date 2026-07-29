# Conjetura de Collatz — laboratorio

Repo de exploración de la conjetura de Collatz (`n/2` si es par, `3n+1` si es
impar; se conjetura que todo `n ≥ 1` termina en 1).

No es una biblioteca ni un paquete. Son programas sueltos, cada uno con su
número configurable arriba del archivo, pensados para ejecutarse y mirar el
resultado. **El código se escribe simple a propósito**: nombres en castellano,
comentarios que explican lo obvio, sin type hints ni abstracciones.

## Cómo se ejecuta

Todos se ejecutan igual: se abre el archivo, se cambia el número de arriba, y se
corre (`python archivo.py`, o Ctrl+B en Sublime Text).

**Sublime Text no acepta `input()`** — el programa se cuelga esperando. Por eso
cada script trae el valor en una constante editable arriba del archivo, nunca
solo `input()`.

Los gráficos salen como `.html` que se abren solos en el navegador (zoom con la
rueda, giro con el mouse, valores al pasar el cursor). Están en `.gitignore`.

```
pip install -r requirements.txt      # numpy, matplotlib, plotly
```

## Los archivos

| Archivo | Qué hace |
|---|---|
| `collatz.py` | Motor: `secuencia`, `altitud_maxima`, `tabla_de_pasos`, `verificar`, `records` |
| `main.py` | CLI: `verificar`, `records`, `camino`, `graficar` |
| `collazejecucion.py` | Una trayectoria como línea de tiempo horizontal (matplotlib, con barra para desplazarse) |
| `collazcirculo.py` | La trayectoria dada la vuelta al globo: ida por delante (F), vuelta por detrás (B) |
| `collazcruce.py` | Dos trayectorias de igual longitud cruzándose sobre una esfera |
| `collazarbol.py` | El árbol de Collatz sobre la esfera: tronco + ramas que brotan en los vórtices |
| `collazmalla.py` | **La malla real**: cada par de puntos en coordenadas (A, B) |
| `collazlamina.py` | **La lámina**: los pares en 3D, todos sobre un plano de grosor 0,23 |
| `viz3d.py` | Vistas 3D auxiliares en matplotlib (paisaje de trayectorias, coral) |

## Lo que se estableció, con verificación

Todo lo de abajo se comprobó ejecutando código, no razonando.

**La identidad entre pares.** Para cualquier par de posiciones `i < j` de una
trayectoria, contando `A` = veces que se aplicó `3n+1` y `B` = veces que se
aplicó `n/2` en el tramo:

```
2^B · seq[j]  =  3^A · seq[i]  +  C
```

donde `C` se actualiza `C → 3C + 2^B` en cada paso impar y no cambia en los
pares. Comprobado en **los 6.555 pares** de la trayectoria del 221: **0 fallos**.

**El único ciclo es una ecuación.** El ciclo `1 → 4 → 2 → 1` escrito con esa
identidad da `A=1, B=2, C=1`, o sea **`2² = 3¹ + 1`** → **`4 = 3 + 1`**.
Buscando ciclos escondidos en los 6.555 pares aparecieron 95 candidatos enteros
positivos; los 95 ciclan de verdad y son `n ∈ {1, 2, 4}` dando 1, 2 o 3 vueltas.
Cero impostores. *(Esto no es evidencia de nada: la literatura de 2025 exige que
cualquier otro ciclo mida ≥ 19.478.780.533 pasos, y nuestro tramo más largo mide
114. La búsqueda no podía encontrar nada.)*

**Es una lámina, no una esfera.** Puestos los pares en (tamaño de salida, tamaño
de llegada, desviación del equilibrio), los 6.555 caen entre `0` y `0,2286` por
encima del plano `desviación = salida − llegada`. **Ninguno cae por debajo.**
Grosor = 1,1% del espacio. Ese grosor es exactamente la contribución de los
`+1`: con `3n` en vez de `3n+1` sería cero.

**Los vórtices.** Un número tiene dos padres si y solo si deja resto 4 al
dividirlo entre 6 (el segundo padre es `(v−1)/3`). Es la regla estándar de la
literatura. La trayectoria del 221 tiene 50 vórtices en sus 115 números.

**El balance decide todo.** El punto de equilibrio es `log₂(3) = 1,585`
divisiones por multiplicación. El 221 tiene `73/41 = 1,78` → cae. Por debajo de
1,585 subiría; justo encima giraría en círculo.

**El 221 falla por ocho.** Un ciclo con `A=41` necesitaría `B=65` (y `65/41` es
una de las mejores aproximaciones fraccionarias a `log₂(3)`). El 221 tiene 73.
Le sobran 8 divisiones, que son el mismo `+8,02` de desviación medido, que es a
su vez el logaritmo del 221.

**Dónde podrían esconderse otros ciclos.** Barriendo 480 casillas `(A,B)`, las
que quedan en pie son exactamente las **convergentes y semiconvergentes de la
fracción continua de `log₂(3)`** — comprobado en las 10 más cercanas, todas sin
excepción. Para esconder un ciclo por encima de lo verificado (2^71, Barina 2025)
haría falta que `2^B` coincidiera con `3^A` hasta la cifra 22.

## Qué es real y qué es dibujo

Importa mantenerlo separado.

**Aritmética verificada:** los números del árbol y sus conexiones; la *altura* de
cada punto en la esfera = su distancia real al 1 (comprobado en los 5.674 números
de las ramas); los vórtices; que las ramas se funden y nunca se cruzan.

**Elección de dibujo:** la esfera misma (el árbol no vive en una esfera; se mapeó
la distancia al 1 sobre media vuelta, cierra porque se hizo cerrar); la longitud
/ dirección de cada rama; el regreso "por detrás" del 1 a la semilla (la
trayectoria real no vuelve, se queda en `1-4-2`).

**Comprobado y negativo:** la altura **no** codifica el tamaño del número. La
correlación entre latitud y `log₂(valor)` es 0,12 — nula.

## Nada de esto es nuevo

Todos los resultados de arriba son matemática conocida: la identidad, la regla
del resto 4, el papel de `log₂(3)`, y que las cotas de ciclos vivan en las
convergentes de su fracción continua. Se llegó a ellos de forma independiente,
pero no son un descubrimiento.

Verificación por fuerza bruta al día: 2^71 (Barina, enero 2025). Resultado
general más fuerte: Tao 2019, "casi todas las órbitas alcanzan valores casi
acotados".

## Siguiente sesión

Construir mallas circulares con números que sí cierren entre ellos —
independientes de Collatz—, guardarlas, y cruzarlas después contra los números
que genera Collatz para buscar coincidencias de patrón.
