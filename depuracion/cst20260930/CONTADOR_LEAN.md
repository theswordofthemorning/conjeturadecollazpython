# Ocelotas: contador canónico y primer descenso — 30-09-2026

**Resultado:** `OcelotasContador.cst_contador` demuestra en Lean que el
primer descenso real coincide con el primer cruce del coeficiente cuando
el contador directo de rachas impares es como máximo diez, bajo
`RhinEntera`. La representación `Palabra` se construye en la prueba.
Se cierra la interfaz que quedó pendiente en el [cierre aritmético](CIERRE_LEAN.md).

## Enunciado y convenciones

```lean
theorem cst_contador (hR : RhinEntera) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 10) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

Se mantiene el atajo `T(n)=n/2` para n par, `(3n+1)/2` para n impar.
El dominio del descenso es n>=2; k y j cuentan pasos de ese atajo.
El prefijo de longitud k contiene las entradas `T^j(n)` para **0<=j<k**;
no incluye la paridad de la salida `T^k(n)`. No hay ley probabilística.
`PrimerCruce n k` conserva su significado: `3^(S k n)<2^k` por primera vez.

El contador es computable y se define independientemente de `Palabra`:

```text
R(n,0) = 0
R(n,k+1) = R(n,k) + [T^k(n) es impar y
                     (k=0 o T^(k-1)(n) es par)].
```

`rachas_eq_card` identifica R con la cardinalidad del conjunto de índices
que satisfacen esa condición. Cuenta cada racha maximal impar una sola vez,
incluida una racha abierta al final del prefijo. Para n par y su primer
cruce k=1, R=0; el teorema también cubre ese caso.

## Extracción y lectura matemática

[OcelotasContador.lean](OcelotasContador.lean) desarrolla estas piezas:

1. `leer_prefijo`: para n impar, todo prefijo no vacío se escribe como r
   bloques completos `1^a 0^b`, seguidos de `1^u 0^v`, con u>0 y v>=0.
   La longitud coincide con el prefijo y el contador vale r+1. Al leer
   otro símbolo, se prolonga el tramo par, se prolonga el impar si v=0,
   o se cierra el bloque y se inicia otro si llega un impar con v>0.
2. `extraer_palabra`: si además la última entrada del prefijo es par,
   entonces v>0. Se cierra el último bloque y se obtiene una `Palabra`
   con exactamente R(n,k) bloques y tiempo total k. La prueba vale para
   cualquier prefijo con esos extremos, sin Rhin ni primer cruce.
3. `cruce_termina_par`: un primer cruce necesariamente termina con
   entrada par. Si la última entrada fuera impar, `3^S` se multiplicaría
   por 3 mientras `2^k` sólo lo hace por 2; el coeficiente previo >=1
   no podría pasar a ser <1. `palabra_del_cruce` une las dos piezas.
4. `descenso_contador` aplica `ocelotas_diez` a la palabra extraída y
   resuelve n par mediante `descenso_par`. Su contraposición,
   `fallo_contador_exige_once`, exige R(n,k)>=11 ante un fallo.
5. `cota_inferior` prueba por inducción
   `3^(S j n)*n <= 2^j*T^j(n)`. El término aditivo de cada paso es
   no negativo. Antes del primer cruce, `2^j<=3^(S j n)`, luego
   `n<=T^j(n)`. `no_desciende_antes` y el descenso en k dan `cst_contador`.

Estas son pruebas universales de los enunciados indicados. La construcción
no supone que exista primer cruce para toda semilla ni que las longitudes
de las rachas estén acotadas.

## Bordes, contraste y evidencia

El [cotejo independiente](cotejar_contador.py) compara los inicios 0->1
con `itertools.groupby` y con una lectura de bloques abiertos. Comprueba
**8191 palabras binarias**, todas las de longitudes 0,...,12: una vacía,
4095 con inicio par, 2048 con inicio impar y final impar, y 2047 con
inicio impar y final par. También verifica **33024 prefijos de órbita**,
n=0,...,255 y k=0,...,128; 8120 admiten la extracción completa impar-par.
Todos los primeros cruces de esas 256 semillas aparecen en ese horizonte.
El coeficiente se compone con `Fraction` y se coteja con las potencias
exactas; se comprueba la cota inferior y el descenso en los casos de
hasta diez rachas con n>=2. Es evidencia finita, distinta de la prueba.

Casos concretos, con unidades del atajo:

| n | Primer cruce k | R(n,k) | T^k(n) |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 2 | 1 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 4 | 1 | 2 |
| 7 | 7 | 2 | 5 |
| 27 | 59 | 15 | 23 |
| 10087 | 105 | 25 | 7688 |

n=0 y n=1 muestran por qué el descenso estricto exige n>=2. Las dos
últimas filas comprueban el contador fuera del alcance de diez rachas;
no amplían ese alcance. Lean comprueba con el núcleo los ejemplos de
prefijo vacío, racha abierta, n par y los primeros cruces de 1,3,7,27.
[Resultados, parámetros y huellas](cotejo_contador.json).

Reconstrucción limpia de **ocho módulos**, Lean 4.32.2, código 0.
Las consultas `#print axioms` sólo muestran subconjuntos de `propext`,
`Classical.choice`, `Quot.sound`; sin `sorryAx`, axiomas propios ni
evaluación nativa. [Compilación y huellas](lean_contador.txt).
Los siete módulos matemáticos anteriores y sus registros se conservan.

Desde la raíz:

```text
python -B -X utf8 depuracion/cst20260930/cotejar_contador.py --longitud-binaria 12 --hasta 255 --max-pasos 128 --salida depuracion/cst20260930/cotejo_contador.json
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_contador.txt
```

Se actualiza la entrada existente del registro, manteniendo 246 afirmaciones
y regenerando SQLite mediante el generador habitual
([controles y huellas](registro_contador.txt)).

## Límite y siguiente acción

`RhinEntera` sigue siendo una hipótesis externa explícita; su ausencia
de la lista de axiomas no la descarga. No se demuestra existencia
universal del primer cruce, CST para un número arbitrario de rachas,
ni Collatz. No se certifica novedad bibliográfica.

La interfaz del contador está cerrada. Sigue auditar el rango y las
constantes de Rhin contra su fuente original, y estudiar la descarga
de esa hipótesis en Lean. La revisión humana del enunciado sigue pendiente.
No se amplían los censos anteriores.
