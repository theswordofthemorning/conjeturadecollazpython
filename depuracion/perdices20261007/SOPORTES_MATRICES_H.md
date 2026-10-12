# Perdices: soportes activos y rectas invariantes

12-10-2026. Continúa [Proyecciones](PROYECCIONES_MATRICES_H.md).
**Resultado:** se excluyen, sin cota de coeficientes, las interpretaciones
naturales 2×2 cuyas seis letras interiores conservan una misma recta
`(x,kx+t)`, con k,t naturales. La exclusión admite conexiones en ambos
sentidos. Además se clasifican los diez soportes mínimos que alimentan
las constantes izquierdas de las reglas dinámicas.

Esto restringe los candidatos a un certificado. **No clasifica todos los
soportes que orientan el sistema**, ni demuestra la terminación de H.
No se reclama prioridad. Revisión humana pendiente.

## 1. Dominio y convenciones

Cada letra X es `z ↦ M_X z + v_X` sobre `ℕ²`, incluido cero. Índices 0,1;
todos los coeficientes son enteros naturales sin cota superior. `XY` es
`X∘Y`: primero se aplica Y. No hay ley aleatoria ni condicionamiento orbital.
El orden débil compara las cuatro entradas matriciales y las dos constantes.
Una dinámica se elimina si, además, su constante 0 izquierda es mayor.

Se conserva el objetivo 57 invertido de [Matrices H](MATRICES_H.md#1-fuente-sistema-y-alcance-de-la-reducción).
Como en la obstrucción escalar, bastan nueve reglas:

```text
DA ≥ D, DBAA ≥ DABE, DBBA ≥ DBAF,
FA ≥ BE, GA ≥ AF, EB ≥ BF, FB ≥ AG, EC ≥ BC, FC ≥ AAC.
```

La prueba por rectas exige **las tres dinámicas presentes**, por lo que
trata la primera eliminación. No se aplica automáticamente tras retirar reglas.

## 2. Una recta común vuelve a dar una interpretación escalar

Fijados `k,t∈ℕ`, sea `L(x)=(x,kx+t)`, x natural. La letra X conserva ese
rayo discreto si y sólo si

```text
M_X10 + k M_X11 = k (M_X00 + k M_X01),
t M_X11 + v_X1 = k (t M_X01 + v_X0) + t.
```

En ese caso `X(L(x))=L(α_X x+β_X)`, donde

```text
α_X=M_X00+k M_X01,    β_X=t M_X01+v_X0.
```

Ambos coeficientes son naturales. Supongamos que **a,b,c,e,f,g** conservan
la misma L; **d puede ser arbitraria**. La composición conserva L. Además,
la primera coordenada de `X∘Y` restringida a L coincide con la composición
de sus proyecciones escalares siempre que **Y** conserve L. Esto alcanza
todos los productos de las nueve reglas, incluidos los encabezados por d.

El orden débil se conserva al proyectar: las nuevas pendientes y constantes
son sumas con pesos no negativos. La obstrucción escalar previa fuerza
igualdad de las constantes proyectadas en los tres pares dinámicos.
Para cualquiera de ellos, izquierda U y derecha V, esa igualdad dice

```text
t M_U01 + v_U0 = t M_V01 + v_V0.
```

La orientación débil ya impone `M_U01≥M_V01` y `v_U0≥v_V0`. Por tanto
`v_U0=v_V0`: **ninguna dinámica es estricta**. La prueba no usa que las
matrices sean triangulares ni que sus entradas estén acotadas.

### Dos consecuencias concretas

- **Segunda coordenada inactiva.** Si `M_X10=v_X1=0` para
  X en a,b,c,e,f,g, sirve `k=t=0`. Las entradas (0,1) pueden ser positivas;
  d sigue libre. Esas conexiones no bastan para obtener descenso.
- **Coordenadas que coinciden en la diagonal.** Si cada una de esas seis
  letras tiene iguales sumas de fila y `v_X1=v_X0`, sirve `k=1,t=0`.
  Se excluye esta familia incluso con ambas entradas cruzadas positivas.

Combinado con la obstrucción anterior, un candidato estricto debe tener
alguna entrada (0,1) positiva entre a,b,d,e,f,g y, además, alguna entrada
(1,0) o constante 1 positiva entre a,b,c,e,f,g. **No se deduce que deba
existir un circuito:** la segunda alternativa permite una constante positiva.
Tampoco basta con dibujar un circuito; puede conservar la diagonal excluida.

## 3. Qué soportes alimentan los lados izquierdos

Escribamos `r=(d00,d01)`, primera fila de M_d, `u=v_a`, `w=v_b`.
Al restar la constante exterior `v_d0`, los tres lados izquierdos aportan

```text
DA:   r u,
DBAA: r (M_b M_a u + M_b u + w),
DBBA: r (M_b² u + M_b w + w).
```

Todos los sumandos son no negativos. Sea Q la suma de estos tres aportes.
Como los lados derechos también tienen constante 0 al menos `v_d0`,
cualquier descenso estricto exige `Q>0`, incluso sin usar las reglas estáticas.

Expandir los productos y eliminar conjuntos de factores que contienen otro
ya suficiente da esta equivalencia exacta: **Q>0 si y sólo si al menos
uno de estos diez productos es positivo**.

| Ruta | Producto |
|---|---|
| 1 | `d00 va0` |
| 2 | `d01 va1` |
| 3 | `d00 vb0` |
| 4 | `d01 vb1` |
| 5 | `d00 b01 va1` |
| 6 | `d01 b10 va0` |
| 7 | `d00 b01 vb1` |
| 8 | `d01 b10 vb0` |
| 9 | `d00 b00 a01 va1` |
| 10 | `d01 b11 a10 va0` |

Son soportes mínimos: asignar 1 exactamente a los factores de una fila y
0 al resto activa Q; quitar cualquiera de esos factores lo anula. Las
entradas a00 y a11 pueden alterar la magnitud, pero no añaden un soporte
mínimo. Las constantes de e,f,g afectan los lados derechos y las reglas
estáticas; no aparecen en este filtro de los lados izquierdos.

**Este aporte no es todavía la diferencia entre ambos lados.** Tampoco se
ha demostrado que la conexión exigida por la obstrucción escalar deba estar
en la misma ruta activa: las letras e,f,g intervienen en otras desigualdades.
No se añade esa hipótesis al buscador.

El ejemplo `d01=va1=1`, con las demás entradas relevantes cero, activa DA
sin ninguna entrada inversa. No orienta siquiera la parte matricial de
`DA≥D`, por lo que **no es un certificado**. Sirve para comprobar que un
aporte puede recorrer un camino abierto. Como control distinto, tomar
M_a=M_b=M_d=M_e=M_f=M_g con todas sus entradas 1, M_c=0 y todos los
vectores cero orienta las doce reglas débilmente, conserva la diagonal
y no elimina ninguna dinámica.

## 4. Formalización y cálculo independiente

[PerdicesSoportesMatrices.lean](PerdicesSoportesMatrices.lean): **14 teoremas
nuevos**, 24 con la base escalar. Incluye producto y orden proyectados,
conservación de la recta, proyección de las nueve reglas, igualdad de las
constantes originales, ambos corolarios y equivalencia de los diez soportes.
La minimalidad de la lista se justifica por los testigos anteriores; no tiene
un teorema Lean separado.

Lean 4.32.2, Mathlib fijado; `#print axioms` sólo da axiomas estándar,
sin `sorryAx` ni avisos. [Evidencia](evidencia_soportes_matrices.json),
[salida](evidencia_soportes_matrices.txt),
[reproductor](comprobar_soportes_matrices.py). La dependencia escalar se
audita por huellas de fuentes y objeto. No se formaliza el programa Python
ni la equivalencia global entre el sistema de palabras y H.

[Cotejo independiente](cotejar_soportes_matrices_h.py): evalúa funciones de
derecha a izquierda y expande polinomios sin usar el compositor matricial.
Después contrasta con el compositor entero anterior:

- Los **16.384 soportes binarios** de las 14 entradas relevantes:
  10.880 con Q positivo y 5.504 sin aporte; diez soportes mínimos exactos.
- 2.000 asignaciones reproducibles con entradas de `{0,1,2,17,10000}`.
- 21.760 productos proyectados, con factor izquierdo arbitrario binario;
  17.878 composiciones de letras que conservan una recta. Se toman k,t y
  coeficientes de las letras conservadoras en `0..2`.
- Los dos controles de camino abierto y de sistema débil conectado.

[Resultados y parámetros](cotejo_soportes_matrices_h.json). Los censos
cotejan implementaciones; la equivalencia de soportes y la obstrucción
sin cota descansan en la prueba escrita y Lean.

[Conservación del catálogo](conservacion_soportes_20261012.json): las 331
afirmaciones anteriores permanecen literales; se añaden dos. Se conservan
las 85 correcciones, 20 constantes, 63 nodos y 96 dependencias anteriores.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_soportes_matrices.py --compilados "$env:TEMP/perdices_proyecciones_matrices_20261011" --salida depuracion/perdices20261007/evidencia_soportes_matrices.json
python -B -X utf8 depuracion/perdices20261007/cotejar_soportes_matrices_h.py --cota-rectas 2 --muestras-grandes 2000 --semilla 0 --sistema-guardado depuracion/perdices20261007/bv_objetivo57_n2_c3.json --salida depuracion/perdices20261007/cotejo_soportes_matrices_h.json
```

## 5. Siguiente tanda

Aplicar estos filtros a candidatos acoplados: ruta activa y ausencia de
recta natural común. Estudiar la **diferencia completa** de constantes y
las nueve reglas estáticas en las familias restantes. La clasificación
de todos los soportes realizables por pesos naturales sigue pendiente.
No ampliar un timeout ni exigir un circuito por intuición. La persistencia
de una misma semilla en H continúa abierta.
