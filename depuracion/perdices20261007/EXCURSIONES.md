# Perdices: cierre formal de las rachas entre regresos

10-10-2026. Continuación de [Separación](SEPARACION.md).

**Resultado:** bajo una misma fuga pura, infinitos regresos por debajo
de un techo fijo exigen excursiones con un número de rachas impares
no acotado en toda cola. El enlace orbital completo ya está en Lean,
incluida la construcción de los regresos consecutivos. No se afirma
que exista esa fuga ni que todas las excursiones tengan cada vez más rachas.

## 1. Enunciado exacto y dominio

Trabajamos en los naturales con el atajo `T(n)=n/2` para n par y
`T(n)=(3n+1)/2` para n impar. `x_j=T^j(n)` y `S_j` cuenta las entradas
impares entre los índices `0≤i<j`. El coeficiente es `P_j=3^S_j/2^j`.
El tiempo se mide en pasos del atajo; una racha es una secuencia
consecutiva de entradas impares, contada una sola vez por su inicio.
No hay ley aleatoria ni hipótesis de independencia.

Las hipótesis son `FugaPura n`, es decir `P_j≥1` para todo j, y un
natural c **fijo** con infinitos índices `P_j≤C=3^c`. La fuga pura
ya fuerza n≥2. En el módulo:

- `Bajo n c j` expresa `3^S_j≤3^c·2^j` mediante enteros.
- `Consecutivos n c u v` exige u<v, ambos extremos bajos y ningún
  índice bajo estrictamente entre ellos.
- `InfinitosRegresos n c` significa `∀U, ∃j>U, Bajo n c j`.
- `rachas (T^[u] n) (v-u)` es el contador canónico de
  [OcelotasContador](../cst20260930/OcelotasContador.lean), aplicado a
  las entradas del intervalo `[u,v)`. Cuenta una racha inicial impar
  aunque haya comenzado antes de u en la órbita global.

El teorema `infinitos_exigen_rachas` de
[PerdicesExcursiones.lean](PerdicesExcursiones.lean) dice:

```text
FugaPura n ∧ InfinitosRegresos n c
  ⇒ ∀H U, ∃u v, U<u ∧ Consecutivos n c u v
                    ∧ H<rachas(T^u(n), v-u).
```

La semilla n y el techo C se mantienen durante toda la demostración.
No se supone una lista de regresos como hipótesis del teorema final:
se construye el siguiente regreso mediante el mínimo natural.

## 2. Extracción de la excursión real

Si u+1<v, el primer paso tiene entrada impar: una entrada par desde
P_u≤C daría P_(u+1)=P_u/2≤C, un regreso interior. El último paso
tiene entrada par: uno impar desde P_(v−1)>C daría P_v=3P_(v−1)/2>C.
Estos argumentos se certifican con `salida_impar` y `llegada_par`.

`palabra_excursion` aplica `extraer_palabra` de Ocelotas y obtiene
una palabra real `1^a0 0^b0 ... 1^a(h−1) 0^b(h−1)`, con todas las
longitudes positivas, exactamente h rachas y duración v−u. La última
racha par puede estar truncada en v. Para v=u+1 se usa un caso
separado: no se fuerza esa forma de palabra.

## 3. Cierre entero: de pocas rachas al reloj cuadrático

La derivación logarítmica de [Separación, §4](SEPARACION.md#4-enlace-escrito-las-excursiones-necesitan-rachas-no-acotadas)
sigue siendo válida. Para formalizar su conclusión basta una vía
más sencilla, con cotas menos ajustadas y sin raíces ni logaritmos.

Fijemos un supuesto tope H de rachas. Definimos constantes enteras

```text
E=(C n)^6,
K_H=2(2^H+c)+1,
D_H=4 K_H^2 E+1.
```

En un regreso u, con x=x_u, la sexta raíz y `S_u≤u` dan

```text
x^6≤E(u+1),
(x+1)^2≤4x^2≤4x^6≤4E(u+1).                         (1)
```

Aquí x≥1; `entrada_cuadrado` prueba (1) desde la fuga pura.
En la cota por rachas de Separación podemos elegir L=x+1, pues
`x+1≤2^(x+1)`. Para una excursión no unitaria con h≤H,

```text
d≤2((2^h−1)(x+1)+c)≤K_H(x+1),
d^2≤4 K_H^2 E(u+1)≤D_H(u+1).                       (2)
```

El término +1 de D_H incorpora también d=1. `duracion_cuadrado`
formaliza (2) para todos los pares consecutivos, sin excepciones.
Esta relajación de L sirve para cerrar la contradicción; la cota
logarítmica previa conserva mejores constantes.

El lema abstracto `reloj_cuadratico` prueba, para cualquier lista
monótona t de naturales, sin suponer que sea una órbita:

```text
(t_(i+1)−t_i)^2≤D(t_i+1) para todo i
  ⇒ t_i+1≤(D+t_0+1)(i+1)^2 para todo i.             (3)
```

Prueba independiente por inducción: sea B=D+t_0+1. El caso i=0
es inmediato. Si `t_i+1≤B(i+1)^2`, entonces
`d_i^2≤D B(i+1)^2≤B^2(i+1)^2`, y por positividad
`d_i≤B(i+1)`. Sumando, `t_(i+1)+1≤B(i+1)^2+B(i+1)≤B(i+2)^2`.
La prueba cubre D=0 y t_0>0.

Una lista infinita de regresos consecutivos es estrictamente
creciente. Si h≤H en todos sus intervalos, (2) y (3) dan un reloj
cuadrático, por tanto también un reloj séxtico. Lo contradice
`reloj_sextico_imposible` de Separación. La misma prueba vale en
cualquier cola (`rachas_grandes_tarde`). Finalmente se elige un
regreso posterior a U y se itera el mínimo siguiente; así se elimina
la lista auxiliar del enunciado final.

## 4. Formalización y contraste

Diez lemas nuevos, con diez consultas `#print axioms`, en
[PerdicesExcursiones.lean](PerdicesExcursiones.lean). El cierre incluye
extracción orbital, cotas enteras, inducción del reloj, exclusión de
H fijo en toda cola y construcción de la enumeración. Sólo aparecen
`propext`, `Classical.choice` y `Quot.sound`; no hay pruebas incompletas
ni hipótesis externas de LMN o Rhin en estos enunciados.
Lean certifica esos enunciados; la revisión humana sigue pendiente.

[comprobar_excursiones.py](comprobar_excursiones.py) compila el módulo
nuevo con Lean 4.32.2. Audita fuentes, objetos, dependencias, evidencia
y entorno de los quince módulos previos, **sin recompilarlos**.
Resultado: dieciséis módulos y 142 consultas contando el cierre previo.
[Evidencia JSON](evidencia_excursiones.json), [salida de Lean](evidencia_excursiones.txt).

[cotejar_excursiones.py](cotejar_excursiones.py) es un contraste entero
independiente: órbitas directas, contador por transiciones, agrupación
de bits y comprobación de las identidades afines de cada bloque.
Revisa semillas 2..512, hasta 256 pasos y techos c=0..4, restringiendo
cada órbita al prefijo anterior a su primer cruce. El
[resultado](cotejo_excursiones.json) contiene:

- 7292 entradas y 4737 intervalos consecutivos: 4514 unitarios y
  223 no unitarios, con hasta trece rachas en un intervalo.
- 3717 pares que omiten un regreso, rechazados como consecutivos.
- 10289 cotas del reloj orbital sobre 3575 colas, conservando n.
- 42405 controles de la recurrencia abstracta, usando el mayor salto
  permitido calculado con `isqrt`, D=0..32 y cinco tiempos iniciales.

Son controles finitos de extracción y desigualdades. Ningún prefijo
certifica una fuga pura ni infinitos regresos; la afirmación universal
condicional procede de la prueba, no de este barrido.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_excursiones.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_excursiones.json
python -B -X utf8 depuracion/perdices20261007/cotejar_excursiones.py --n-max 512 --pasos 256 --nivel-max 4 --d-max 32 --salida depuracion/perdices20261007/cotejo_excursiones.json
```

Si faltan los objetos anteriores, seguir primero la
[reproducción de Separación](SEPARACION.md#6-certificación-y-reproducción).
La familia modular general de Separación conserva prueba escrita y
cotejo finito; no se ha formalizado en este módulo.

## 5. Límite y siguiente acción

Se cierra el pendiente formal de la ruta existente, sin reclamar
prioridad bibliográfica. No se excluye un planeador con rachas no
acotadas, ni el cohete ni la grieta; Collatz sigue abierto.

**Continuación:** [Ritmo](RITMO.md) reduce `2^h` a `(8/5)^h` y obtiene
una condición formal más fuerte: `(8/5)^(6h)/(u+1)^4` es no acotado en
toda cola. Conserva la misma semilla y el mismo techo. Añade una tasa
logarítmica más fina y una identidad con todas las longitudes pares,
ambas con prueba escrita. El siguiente trabajo estudia si las
congruencias de los bloques fuerzan un balance par suficiente.
