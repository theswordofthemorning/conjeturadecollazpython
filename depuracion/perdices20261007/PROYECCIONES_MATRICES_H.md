# Perdices: obstrucción escalar y acoplamiento matricial necesario

11-10-2026. Continúa [Matrices H](MATRICES_H.md). **Resultado:** en la
primera etapa del objetivo 57, ninguna interpretación afín natural escalar
puede eliminar una regla dinámica. En dimensión 2 es necesario que al menos
uno de los símbolos a,b,d,e,f,g tenga entrada matricial (0,1) positiva.
No se exige ninguna condición a esa entrada de c.

Es una obstrucción de una familia de órdenes, sin cota de coeficientes.
No excluye las matrices acopladas, no establece una obstrucción ártica y
no demuestra la terminación de H. No se reclama prioridad.

## 1. Dominio, composición y desigualdades

Se mantienen las reglas de [Matrices H, §1](MATRICES_H.md#1-fuente-sistema-y-alcance-de-la-reducción),
invertidas para que las dinámicas estén en la cabeza. Para cada símbolo
se considera una función de **naturales a naturales**:

```text
A(x)=αx+a, B(x)=βx+b, C(x)=χx+c, D(x)=δx+d,
E(x)=εx+e, F(x)=φx+f, G(x)=γx+g.
```

Todos los parámetros son naturales, incluido cero. `XY` significa `X∘Y`;
la letra de la derecha se aplica primero. El orden débil compara pendiente
y constante por separado. El estricto natural exige además descenso de la
constante, como el verificador de certificados. No hay ley aleatoria ni
condicionamiento orbital: se estudia una asignación algebraica a símbolos.

Bastan nueve de las doce desigualdades del sistema:

```text
DA >= D,  DBAA >= DABE,  DBBA >= DBAF,
FA >= BE, GA >= AF, EB >= BF, FB >= AG,
EC >= BC, FC >= AAC.
```

Las otras tres (`EA>=AE`, `GB>=BG`, `GC>=BAC`) no se usan en la prueba.
El resultado exige conservar las tres dinámicas: se aplica a la primera
eliminación; no se transfiere automáticamente a una etapa posterior.

## 2. Prueba escalar, incluidos los ceros

**Caso δ=0.** Las seis palabras dinámicas tienen constante d, luego
ninguna comparación puede ser estricta.

Supongamos δ>0. La pendiente de `DA>=D` obliga a α>=1. Cancelamos δ y d
en las constantes de las otras dos dinámicas:

```text
α(βe+b)+a <= β(αa+a)+b,                         (1)
β(αf+a)+b <= β(βa+b)+b.                         (3)
```

**Caso β=0.** (1) dice `αb+a<=b`. Como α>=1, se sigue `a=0` y `αb=b`.
Las constantes de cada uno de los tres pares dinámicos son iguales.
Aquí b puede ser positivo; no se descarta esa proyección constante.

Supongamos β>0. Las pendientes de `GA>=AF` y `EB>=BF` dan γ>=φ y ε>=φ.
Las de `FA>=BE` y `FB>=AG` dan

```text
βε <= φα,  αγ <= φβ.
```

**Caso φ=0.** Se obtiene ε=γ=0. En las constantes estáticas:

```text
αf+a <= g,  αg+a <= f,
βe+b <= f,  βf+b <= e.
```

Como α,β>=1, el primer par fuerza a=0 y el segundo b=0. Las constantes
izquierdas de las tres dinámicas son d; sus derechas son >=d. La orientación
débil las hace iguales.

**Caso φ>0.** Las mismas pendientes dan α>=β y β>=α. Por tanto
`α=β=t>=1` y `ε=φ=γ=s`. La pendiente de `DBAA>=DABE` impone s<=t.
Las constantes de `EC>=BC` y `FC>=AAC` implican

```text
e>=b,  f>=(t+1)a>=2a,
```

pues `s*c<=t*c<=t²*c`. Sustituyendo e>=b en (1), con `K=t²+t>=2`:

```text
K*b+a <= K*a+b  =>  b<=a.
```

Cancelando t>0 en (3), se obtiene `t*f+a<=t*a+b`. Como f>=2a y t>=1,
`b>=(t+1)a>=2a`. Así a=b=0. De nuevo las constantes izquierdas son d
y la orientación débil fuerza igualdad en los tres pares. Esto completa
todos los casos sin suponer que los coeficientes sean positivos.

## 3. Consecuencia para dimensión 2

Un símbolo es ahora `X(z)=M_X*z+v_X`, con matrices y vectores naturales.
Los índices son 0 y 1. Si `(M_X)01=0`, entonces

```text
(M_X M_Y)00 = (M_X)00 (M_Y)00,
(M_X v_Y+v_X)0 = (M_X)00 (v_Y)0+(v_X)0.
```

La proyección `X -> ((M_X)00,(v_X)0)` respeta ese producto. Si la entrada
(0,1) se anula en a,b,d,e,f,g, las nueve reglas se proyectan a las escalares
de §1. c sólo aparece como última letra en las reglas usadas; su entrada
(0,1) puede ser arbitraria. §2 fuerza igualdad de las constantes 0 en
cada par dinámico. Por contraposición, cualquier primera eliminación exige

```text
(M_a)01+(M_b)01+(M_d)01+(M_e)01+(M_f)01+(M_g)01 > 0.
```

Es una condición necesaria, no suficiente. En particular excluye matrices
diagonales y matrices triangulares inferiores en dimensión 2. El argumento
escalar también excluye la familia con primera fila aislada en cualquier
dimensión, por la misma fórmula del producto; esa extensión conserva sólo
prueba escrita, mientras la formalización matricial siguiente es 2x2.

## 4. Lean y contraste independiente

[PerdicesProyeccionesMatrices.lean](PerdicesProyeccionesMatrices.lean) contiene
diez teoremas: clasificación de pendientes, dos casos de constantes,
cancelación de amplificación, obstrucción escalar, proyección del producto
y del orden, proyección de reglas, igualdad dinámica y acoplamiento necesario.
Las estructuras `Reglas` y `ReglasDos` contienen exactamente las nueve
hipótesis de §1, con las composiciones explícitas. No se postula la
obstrucción como axioma.

Lean 4.32.2; `#print axioms` sólo usa los axiomas estándar, sin `sorryAx`.
[Evidencia](evidencia_proyecciones_matrices.json),
[salida](evidencia_proyecciones_matrices.txt),
[reproductor](comprobar_proyecciones_matrices.py). Lean certifica el
enunciado algebraico y su traducción 2x2; no certifica el buscador Python,
la equivalencia global con la dinámica de enteros ni la terminación de H.

[cotejar_proyecciones_matrices_h.py](cotejar_proyecciones_matrices_h.py)
calcula cada función evaluando las letras de derecha a izquierda en 0 y 1,
y contrasta los coeficientes con el compositor matricial independiente.
Con D(x)=x, cubre las 531.441 asignaciones de coeficientes `0..2` a los otros
seis símbolos, descartando por reglas que no dependen de c antes de variarlo.
Quedan 124 asignaciones débiles: 109 con β=0, cuatro con β>0 y φ=0, y once
con pendiente común. Ninguna tiene descenso dinámico estricto.

Se cotejan 2.976 interpretaciones y 2.048 productos 2x2 con primera fila
izquierda aislada. Un producto con entrada (0,1) positiva demuestra por
cálculo que la proyección puede dejar de respetar la composición.
[Cotejo](cotejo_proyecciones_matrices_h.json). La reducción a D(x)=x está
justificada por cancelación cuando δ>0; δ=0 se trata directamente en §2
y en Lean. Este censo finito no sustituye la prueba sin cota.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_proyecciones_matrices.py --compilados "$env:TEMP/perdices_proyecciones_matrices_20261011" --salida depuracion/perdices20261007/evidencia_proyecciones_matrices.json
python -B -X utf8 depuracion/perdices20261007/cotejar_proyecciones_matrices_h.py --cota 2 --sistema-guardado depuracion/perdices20261007/bv_objetivo57_n2_c3.json --salida depuracion/perdices20261007/cotejo_proyecciones_matrices_h.json
```

## 5. Árticas sin cota: lo que quedó indeciso

[buscar_articas_libres_h.py](buscar_articas_libres_h.py) representa menos
infinito por -1 y cada peso finito por su entero no negativo. Su producto
es `if a=-1 or b=-1 then -1 else a+b`; la suma es máximo. La composición
completa usa sólo aritmética lineal entera y condicionales, lógica QF_LIA.
No hay cota superior de pesos ni productos entre incógnitas. La primera
coordenada debe permanecer finita, igual que en los certificados anteriores.

Se guarda la fórmula SMT, con las hipótesis etiquetadas como supuestos,
y los parámetros completos. Dos llamadas de Z3 5.1.0, semilla 0, una hebra:

| Sistema | Dimensión | Límite | Resultado |
|---|---:|---:|---|
| Objetivo 57 | 2 | 45 s | [indeciso](lia_objetivo57_a2.json), motivo `canceled` |
| Control 15 | 3 | 30 s | [indeciso](lia_control15_a3.json), motivo `canceled` |

El control tiene modelos conocidos; su timeout muestra que esta llamada
tampoco decide con rapidez un caso satisfacible. No se afirma UNSAT para
ninguna de las dos fórmulas sin cota. No se han repetido aumentando el tiempo.

[auditar_articas_libres_h.py](auditar_articas_libres_h.py) sí comprueba los
seis certificados árticos anteriores en la nueva codificación, tanto con
sus pesos originales como multiplicando todos los pesos finitos por 10.000.
Son doce comprobaciones, con los mismos conjuntos de reglas estrictas.
Añade las 256 asignaciones a dos símbolos escalares con valores codificados
en `{0,1,2,10001}`: menos infinito, peso cero y pesos positivos pequeños y
grandes. Coteja 2.956 interpretaciones con enteros independientes.
[Auditoría](auditoria_articas_libres_h.json). Valida esos casos concretos;
no convierte los timeouts en una conclusión matemática.

```powershell
& "$env:TEMP/perdices_sat_20261011/Scripts/python.exe" -B -X utf8 depuracion/perdices20261007/buscar_articas_libres_h.py --sistema-guardado depuracion/perdices20261007/bv_objetivo57_a2_c3.json --dimension 2 --segundos 45 --salida depuracion/perdices20261007/lia_objetivo57_a2.json
& "$env:TEMP/perdices_sat_20261011/Scripts/python.exe" -B -X utf8 depuracion/perdices20261007/auditar_articas_libres_h.py --controles depuracion/perdices20261007/sat_control15_a3_c5.json depuracion/perdices20261007/bv_control15_a3_c5.json --salida depuracion/perdices20261007/auditoria_articas_libres_h.json
```

## 6. Siguiente restricción que falta

Examinar el soporte de las matrices naturales acopladas: la entrada positiva
exigida por §3 debe intervenir en una ruta hasta la constante que disminuye.
Clasificar los soportes viables antes de asignar pesos permitiría separar
proyecciones absorbentes, rutas que terminan en la segunda constante y
circuitos entre coordenadas. La mera positividad de una entrada (0,1) no
garantiza un circuito: no se puede exigir la entrada inversa sin prueba.

**Continuación 12-10:** [Soportes y rectas](SOPORTES_MATRICES_H.md)
clasifica diez soportes mínimos de aporte izquierdo y excluye las rectas
naturales invariantes comunes. La viabilidad de pesos para el sistema
completo sigue pendiente; no se identifica un aporte con un descenso.
