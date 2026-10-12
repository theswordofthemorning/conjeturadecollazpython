# Perdices: búsqueda de órdenes matriciales sobre dígitos

11-10-2026. Continúa [Rachas H, §7](RACHAS_H.md#7-tamaño-del-empalme-transporte-exacto-del-mínimo).
La comparación de tamaños por CRT se reduce al mínimo original. Esta ruta
ensaya órdenes sobre palabras completas de dígitos. **Resultado:** se reproduce
un control publicado con dos familias de matrices; no se resuelve el caso que
evita 5 y 7 módulo 8. No se demuestra Collatz ni la terminación de H.

## 1. Fuente, sistema y alcance de la reducción

Se utiliza el [repositorio de Yolcu–Aaronson–Heule](https://github.com/emreyolcu/rewriting-collatz),
commit `8a4dfda60f97a6d33ff0a24fdfa7a172d4bec340`, asociado a
[arXiv:2105.14697v3, §4.5](https://arxiv.org/html/2105.14697v3#S4.SS5).
Su código se conserva sin modificar en una copia temporal externa. Los
JSON guardan las huellas de los módulos usados y el commit; el repositorio
del laboratorio contiene el adaptador y el verificador independiente.

Los símbolos a,b representan las operaciones `2x`, `2x+1`; e,f,g representan
`3x`, `3x+1`, `3x+2`; c inicia en 1 y d marca el final. El sistema publicado
`collatz-T-odd-mod8.srs` tiene cinco reglas dinámicas y nueve cambios de
representación. El adaptador coteja sus identidades afines con enteros:

| Sufijo dinámico | Entrada | Regla | Rama T |
|---|---|---|---|
| ad | 2x | `ad -> d` | par |
| aabd | 8x+1 | `aabd -> ebad` | 1 mod 8 |
| abbd | 8x+3 | `abbd -> fabd` | 3 mod 8 |
| babd | 8x+5 | `babd -> gaad` | 5 mod 8 |
| bbbd | 8x+7 | `bbbd -> gbbd` | 7 mod 8 |

El **objetivo 57** elimina las dos últimas reglas. El **control 15** elimina
las ramas 1 y 5; coincide literalmente con el archivo relativo publicado
`collatz-T-1or5mod8.srs`, para el que hay prueba conocida.

Se buscan descensos de las reglas dinámicas aplicadas al final de la palabra,
mientras los cambios de representación sólo deben no aumentar el orden.
El lector de reglas invierte todas las palabras para trabajar con reglas
dinámicas en la cabeza; el verificador comprueba independientemente esa
inversión. La equivalencia global entre terminación y el problema de residuos
es la del artículo: no se formaliza aquí en Lean. La semántica afín de cada
regla sí se coteja en el adaptador.

## 2. Qué constituye un certificado

[buscar_matrices_h.py](buscar_matrices_h.py) usa el codificador publicado y
Z3 5.1.0 como SAT, con semilla 0, una hebra y elección negativa. Los alfabetos
se ordenan para evitar depender de `PYTHONHASHSEED`. Cada candidato SAT pasa
dos controles:

1. Su asignación satisface todas las cláusulas generadas.
2. [verificar_matrices_h.py](verificar_matrices_h.py), sin SAT ni NumPy,
   vuelve a componer las matrices con enteros Python y comprueba cada regla.

En el caso **natural**, cada símbolo representa `M*x+v` con entradas no
negativas. Las reglas débiles satisfacen desigualdad componente a componente;
una dinámica se elimina si además decrece estrictamente la primera componente
del vector. Esto da descenso para cualquier sufijo y cualquier vector natural.

En el caso **ártico**, se usa máximo como suma y suma como producto, con
menos infinito absorbente. El JSON codifica menos infinito por 0 y el entero
j>=0 por j+1. Cada símbolo debe preservar la finitud de la primera coordenada:
su entrada matricial (0,0) o su constante 0 ha de ser finita. El descenso
estricto exige desigualdad estricta en cada entrada, permitiendo igualdad
sólo cuando ambas son menos infinito. Esa condición evita aceptar como rango
el vector enteramente menos infinito.

Las reglas eliminadas dejan de aparecer en la etapa siguiente. El verificador
ancla la primera etapa al sistema original y comprueba toda la cadena. Un
cierre exige eliminar **todas** las reglas dinámicas.

Los cambios de representación restantes terminan por un orden sencillo en
las palabras originales: el par lexicográfico formado por el número de
símbolos ternarios y el número de pares «binario antes de ternario». Las seis
reglas de intercambio reducen la segunda cuenta en uno; las tres que empiezan
por c reducen la primera. La inversión de palabras conserva la terminación.
Por ello, un cierre relativo completo certifica la terminación del sistema
correspondiente. Es una prueba por órdenes con certificado aritmético;
**no se ha trasladado a Lean**.

## 3. Control reproducido

El control 15 cierra de dos maneras, con tres etapas en cada caso:

- [Matrices naturales](sat_control15_n2_c3.json), dimensión 2, cota codificada 3:
  se eliminan `ad`, `abbd`, `bbbd`, en ese orden.
- [Matrices árticas](sat_control15_a3_c5.json), dimensión 3, cota codificada 5:
  se eliminan `abbd`, `ad`, `bbbd`.

Son reproducciones de un resultado publicado, no hallazgos nuevos sobre
Collatz. [auditar_matrices_h.py](auditar_matrices_h.py) verifica los seis
certificados, además de rechazar ocho alteraciones: matrices nulas, cierres
prematuros, intercambio de etapas y cambio del sistema de entrada, en ambas
familias. [Auditoría](auditoria_matrices_h.json).

## 4. Resultado de la búsqueda en el objetivo 57

La cota C limita los valores **de todas las expresiones codificadas**,
incluidos productos, sumas e interpretaciones de prefijos. No es sólo una
cota sobre las matrices de los símbolos. En naturales el rango es `0..C`;
en árticos es `{-infinito,0,...,C-1}`. No se ensayan coeficientes negativos.

| Familia | Dimensión | C | Límite SAT | Resultado |
|---|---:|---:|---:|---|
| Natural | 2 | 3 | 30 s | [UNSAT](sat_objetivo57_n2_c3.json) |
| Ártica | 2 | 3 | 30 s | [UNSAT](sat_objetivo57_a2_c3.json) |
| Natural | 3 | 3 | 60 s | [UNSAT, 24,6 s](sat_objetivo57_n3_c3.json) |
| Ártica | 3 | 3 | 60 s | [UNSAT, 26,6 s](sat_objetivo57_a3_c3.json) |
| Natural | 3 | 5 | 30 s | [timeout](sat_objetivo57_n3_c5.json) |
| Ártica | 3 | 5 | 30 s | [timeout](sat_objetivo57_a3_c5.json) |
| Ártica | 4 | 3 | 60 s | [timeout](sat_objetivo57_a4_c3.json) |

UNSAT es la respuesta del solucionador para esa fórmula finita; no se guarda
un certificado formal de insatisfacibilidad. No excluye matrices mayores,
otras cotas ni otros órdenes. Los tres timeouts no deciden siquiera la
existencia de una interpretación dentro de sus cotas. No se encontró una
regla dinámica eliminable en el objetivo.

## 5. Reproducción del codificador publicado

El entorno usado es Windows, Python 3.14.5 y NumPy 2.4.4 del laboratorio,
con Z3 instalado sólo en un entorno virtual temporal. Paquete
`z3-solver==5.1.0.0`; rueda `z3_solver-5.1.0.0-py3-none-win_amd64.whl`, SHA256
`1561efd36e06f4cb7cbf11b63a2fba8fc8fdeb9c5754df90c84f9bd7a4864552`.
No se modificó el repositorio externo ni se lanzó su lote de experimentos.

Con una copia externa en el commit indicado y un Python con Z3 y NumPy:

```powershell
& "$env:TEMP/perdices_sat_20261011/Scripts/python.exe" -B -X utf8 depuracion/perdices20261007/buscar_matrices_h.py --fuente-externa "$env:TEMP/perdices_rewriting_20261011" --sistema control15 --interpretacion natural --dimension 2 --cota 3 --segundos 30 --salida depuracion/perdices20261007/sat_control15_n2_c3.json
python -B -X utf8 depuracion/perdices20261007/verificar_matrices_h.py --entrada depuracion/perdices20261007/sat_control15_n2_c3.json
```

Para repetir otro caso, cambiar sistema, interpretación, dimensión, cota,
límite de tiempo y salida según su JSON. Las comprobaciones de certificados
guardados no necesitan Z3 ni el repositorio externo.

## 6. Codificación directa y cotas de aritmética

[buscar_matrices_directas_h.py](buscar_matrices_directas_h.py) construye las
mismas desigualdades con vectores de bits de Z3. Sólo restringe a `0..C`
los coeficientes de los símbolos; los intermedios disponen del ancho que
requiere su cota matemática. Usa `QF_BV`, semilla 0 y una hebra. Importa del
adaptador anterior la lectura y comprobación semántica de las reglas, pero
no carga el codificador SAT publicado ni NumPy.

**Naturales.** Para dimensión d, agregar la fila `(0,...,0,1)` convierte
cada transformación afín en una matriz de dimensión `m=d+1`. Puesto que
C>=1, cada entrada es <=C y cada suma de fila es <=`K=mC`. Para matrices
no negativas A,B cuyas sumas de fila están acotadas por U,V,

```text
sum_j (AB)_ij = sum_k A_ik sum_j B_kj <= U V.
```

Por inducción, cada entrada de una palabra de largo p<=L es <=`K^p<=K^L`.
Cada producto individual y suma parcial es <= la entrada que forma. Elegir
`w=bit_length(K^L)` garantiza `K^L<2^w`; las operaciones relevantes se
calculan exactamente. Se incluye la identidad de la palabra vacía.

[PerdicesCotasMatrices.lean](PerdicesCotasMatrices.lean) certifica ocho lemas:
entrada frente a suma de fila, fila del producto, identidad, palabras,
coeficientes, largo acotado y cota frente a `2^w`. Lean 4.32.2, sólo
`propext`, `Classical.choice`, `Quot.sound`, sin `sorryAx`.
[Evidencia](evidencia_cotas_matrices.json), [salida](evidencia_cotas_matrices.txt),
[reproductor](comprobar_cotas_matrices.py). La construcción afín aumentada,
la correspondencia con el programa y la semántica BitVec siguen por escrito;
Lean no certifica el buscador ni los resultados UNSAT.

**Árticos.** Un coeficiente codificado <=C representa menos infinito o un
entero entre 0 y C-1. Un producto de p letras tiene valor finito <=`p(C-1)`;
el máximo no aumenta esa cota. En la codificación, cada resultado es
<=`L(C-1)+1`. Se elige su `bit_length`. La multiplicación selecciona 0 si
algún factor es 0; en el otro caso calcula `a+b-1`, sin resta negativa.
Esta cota conserva prueba escrita, sin formalización ártica.

### Controles y resultados

[auditar_codificador_directo_h.py](auditar_codificador_directo_h.py) relee
los seis certificados anteriores y coteja 1332 interpretaciones de prefijos
con enteros Python. También enfrenta todas las 162 asignaciones de
coeficientes `0..2` a dos símbolos afines de dimensión 1, en ambas familias,
con el verificador independiente. Se incluyen ceros absorbentes y compuestos
que superan la cota de entrada. [Resultado](auditoria_codificador_directo_h.json).

El control 15 vuelve a cerrar:

- [Natural, d=2, C=3](bv_control15_n2_c3.json): **dos etapas**; primero se
  elimina `ad` y luego `abbd` y `bbbd` juntas. Los máximos intermedios son
  6 y 24, respectivamente, mayores que C.
- [Ártico, d=3, C=5](bv_control15_a3_c5.json): tres etapas; máximos codificados
  9, 11 y 13. También exceden C.

Estos certificados muestran que el nuevo dominio de búsqueda es más amplio
que el anterior a igual cota C. La prueba del control sigue siendo conocida.

| Objetivo 57 | d | C | Límite | Resultado |
|---|---:|---:|---:|---|
| Natural | 2 | 3 | 30 s | [UNSAT, 20,9 s](bv_objetivo57_n2_c3.json) |
| Ártico | 2 | 3 | 30 s | [UNSAT, 7,4 s](bv_objetivo57_a2_c3.json) |
| Natural | 3 | 3 | 30 s | [timeout](bv_objetivo57_n3_c3.json) |
| Ártico | 3 | 3 | 30 s | [timeout](bv_objetivo57_a3_c3.json) |

[auditar_matrices_directas_h.py](auditar_matrices_directas_h.py) verifica
sin Z3 las seis ejecuciones y sus cinco certificados, incluida la cadena
de eliminación y sus cotas. Rechaza diez alteraciones: las cuatro clases
anteriores y una cota de coeficientes falsa, en ambas familias.
[Auditoría](auditoria_matrices_directas_h.json).

UNSAT sigue siendo un resultado del solucionador sin certificado de
insatisfacibilidad. Los timeouts no excluyen modelos. Ninguna regla dinámica
del objetivo 57 se ha eliminado, y no se demuestra terminación de H.

```powershell
& "$env:TEMP/perdices_sat_20261011/Scripts/python.exe" -B -X utf8 depuracion/perdices20261007/buscar_matrices_directas_h.py --fuente-externa "$env:TEMP/perdices_rewriting_20261011" --sistema control15 --interpretacion natural --dimension 2 --cota 3 --segundos 30 --salida depuracion/perdices20261007/bv_control15_n2_c3.json
python -B -X utf8 depuracion/perdices20261007/verificar_matrices_h.py --entrada depuracion/perdices20261007/bv_control15_n2_c3.json
python -B -X utf8 depuracion/perdices20261007/comprobar_cotas_matrices.py --compilados "$env:TEMP/perdices_cotas_matrices_20261011" --salida depuracion/perdices20261007/evidencia_cotas_matrices.json
```

## 7. Restricción sin cota y siguiente paso

[Proyecciones](PROYECCIONES_MATRICES_H.md) demuestra que una interpretación
afín natural escalar no elimina ninguna de las tres dinámicas del objetivo
57. En dimensión 2, la primera eliminación requiere una entrada (0,1)
positiva en a,b,d,e,f o g; no basta el acoplamiento de c. Se incluyen los
coeficientes cero. Prueba escrita, diez teoremas Lean y cotejo independiente
de las 531.441 asignaciones escalares con coeficientes 0..2. La familia
natural acoplada queda abierta.

La codificación ártica QF_LIA sin cota de pesos quedó indecisa a 45 segundos
en el objetivo de dimensión 2 y a 30 segundos en el control de dimensión 3.
Los seis certificados árticos conocidos sí pasan esa codificación, tanto
con sus pesos originales como escalados por 10.000. No hay un nuevo UNSAT.

Siguiente: clasificar soportes naturales acoplados y determinar cómo llega
el aporte de la segunda coordenada a la constante que disminuye. No exigir
un circuito entre coordenadas sin demostrar su necesidad. Conservar los
controles y los límites de cada ejecución.
