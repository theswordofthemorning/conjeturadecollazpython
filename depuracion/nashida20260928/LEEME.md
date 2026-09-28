# Nashida: auditoría del puente de barrera fija

28-09-2026. Primer bloque del [plan por sesiones](../transversal20260927/PLAN_SESIONES_20260928.md).
**Resultado:** original localizado y leído; enunciado cotejado con el código;
puente condicional con Condoras demostrado en Lean local. Nashida no se ha
recompilado aquí ni se incorpora como teorema certificado por este laboratorio.
No hay nuevos barridos numéricos ni una resolución de Wu 1.

## Fuentes fijadas

- Artículo r8, 27-09-2026: [Zenodo 22986671](https://doi.org/10.5281/zenodo.22986671).
  El DOI conceptual 22986670 resuelve a esta versión.
- Código: [harappa/collatz-fixed-barrier-power-saving](https://github.com/harappa/collatz-fixed-barrier-power-saving),
  commit `976fffb160744c56f1f26912f7bd23d195fe02d2`.
- Lean externo: `v4.30.0-rc2`; versión local comprobada: `4.32.2`, commit
  `f3b06c705e6c85f5314019d5d3baab0fec5b580c`.
- PDF descargado: `collatz-fixed-barrier-power-saving-r8.pdf`, doce páginas.
  Su MD5 coincide con Zenodo. Las dieciséis copias de archivos cotejables
  descargadas para lectura coinciden con `MANIFEST.sha256`; esto comprueba
  integridad de esas copias, no corrección de las pruebas.

Copias de consulta en `fuentes/`, excluidas de Git. La evidencia reproducible
de esta sesión queda en [evidencia.json](evidencia.json) y
[lean_local.txt](lean_local.txt).

## Enunciado y correspondencia formal

Mapa clásico `C(n)=n/2` si n es par y `C(n)=3n+1` si es impar. Semillas
positivas; los tiempos son iteraciones de C, con tiempo cero incluido.
No se introduce ley aleatoria ni condicionamiento probabilístico. Definimos

$$
E(X,B)=\#\{1\le n\le X:\ \forall j\ge0,\ C^j(n)>B\}.
$$

El teorema 1.1, pp. 2 y 10, afirma que existe **una misma** constante real
K>0 tal que, para todo B entero ≥1 y X entero ≥0,

$$
E(X,B)\le K B^{-c'}X,\qquad c'=c_B/(160\log 2)>0.
$$

El exponente tiene una expresión explícita mediante la entropía binaria;
K depende de umbrales no explicitados. No se ha calculado aquí ningún
valor decimal del exponente ni una barrera efectiva.

| Punto cotejado | Resultado de la lectura del código fijado |
|---|---|
| Mapa final | `CollatzND/Core/Col.lean`, `col`: coincide con el mapa clásico del laboratorio. |
| Semillas y extremo | `Finset.Icc 1 X`; n=0 no se cuenta y X=0 da el conjunto vacío. |
| Tiempo y barrera | `∀ m, N0 < col^[m] N`: todos los tiempos, incluido cero; desigualdad estricta. |
| Cuantificadores | `nd_collatz_uniform_explicit` elige K>0 antes de B y X. |
| Hipótesis intermedia | `FixedBarrierHyp` aparece en `Uniform.lean`, pero `ShaikBridge.lean` la descarga desde `fixedBarrier_failure_count`. |
| Exponente positivo | `Explicit.lean`: `tstarExponent_eq` y `tstarExponent_pos`. |
| Cierre final | `Explicit.lean`: `nd_collatz_uniform_explicit` no conserva una hipótesis matemática explícita en su tipo. |

Enlaces permanentes al
[enunciado final](https://github.com/harappa/collatz-fixed-barrier-power-saving/blob/976fffb160744c56f1f26912f7bd23d195fe02d2/CollatzND/Core/Explicit.lean#L223),
la [barrera](https://github.com/harappa/collatz-fixed-barrier-power-saving/blob/976fffb160744c56f1f26912f7bd23d195fe02d2/CollatzND/Core/Col.lean#L17)
y la [descarga de la hipótesis](https://github.com/harappa/collatz-fixed-barrier-power-saving/blob/976fffb160744c56f1f26912f7bd23d195fe02d2/CollatzND/Core/ShaikBridge.lean#L20).

No se detectó una discrepancia entre este enunciado y el teorema del PDF.
Esto es un cotejo de especificación, no una auditoría completa de su cierre
de dependencias ni una certificación local del teorema externo.

## Prueba independiente del puente con Condoras

Supongamos B≥1 y que **cada entero de [1,B], incluido B, llega a 1**.
Para n≥1 hay entonces equivalencia exacta:

$$
n\text{ no llega a }1\quad\Longleftrightarrow\quad
\forall j\ge0,\ C^j(n)>B.
$$

Prueba: si una órbita que no termina alcanzase un m≤B, la positividad del
mapa daría m≥1; por la hipótesis, la cola desde m llegaría a 1, contradicción.
Recíprocamente, una órbita que siempre está por encima de B≥1 no visita 1.
Se usa concatenación de iteraciones; no se presupone la conjetura de Collatz.

Por tanto, para M≥2, usando exactamente la normalización de Condoras,

$$
\rho(M)=1-\frac{E(M-1,B)}{M-1}\ \ge\ 1-KB^{-c'}.
$$

Sea G(M) el número de coalescencias de Gao en [0,M), sin tope de pasos.
La desigualdad de conteos de `CondorasWu.cota_llegan` produce además

$$
d_{Wu}(M)\ge 1-KB^{-c'}-\frac{M-G(M)}{M-1}.
$$

Gao da G(M)/M→1, de modo que

$$
\liminf_{M\to\infty}d_{Wu}(M)\ge1-KB^{-c'}.
$$

No se afirma que el límite de dWu exista. Una segunda forma de obtener
la misma consecuencia usa directamente `CondorasWu.diferencia`, que
certifica ρ(M)−dWu(M)→0. Ambas vías mantienen la misma barrera fija.

### Certificado local y sus hipótesis

[CondorasBarrera.lean](CondorasBarrera.lean) importa Condoras y demuestra:

- `no_llega_iff_sobre`: la equivalencia de órbitas anterior.
- `cuenta_complementaria`: la igualdad de conteos, también para M=0 y M=1.
- `cota_rho`: la cota de la proporción que llega a 1, para M≥2.
- `cota_finita_dWu`: la desigualdad finita con el defecto de coalescencia.
- `cota_eventual_dWu`: para todo ε>0, eventualmente dWu(M)≥1−error(B)−ε.

El certificado usa un perfil arbitrario `error : ℕ → ℝ` y deja como
hipótesis `CotaBarrera error`, es decir E(X,B)≤error(B)X. Para Nashida, el
perfil sería K B^(-c'). Así el puente sirve también para otras cotas y no
requiere instalar el proyecto externo para certificar la implicación.
`Cubierta B` exige terminación para **1≤n≤B**. Estas hipótesis aparecen en
el tipo final; no quedan escondidas en un axioma.

Compilación local con código 0 en Lean 4.32.2; consultas de axiomas sin
`sorryAx`, sólo axiomas estándar. La forma eventual está formalizada; la
expresión con `liminf` de esta nota es su lectura matemática, no otro
teorema Lean denominado `liminf`. Es una extensión condicional de Condoras,
no una nueva conjetura resuelta ni una afirmación de novedad bibliográfica.

**Corrección del plan del 27-09 y de la primera evaluación del 28-09:**
allí se escribió terminación para n<B. Con la barrera estricta del original
hay que incluir B. Si se conserva la hipótesis n<B, con B≥2 corresponde
aplicar la cota a B−1 y obtener el término K(B−1)^(-c'). Se conserva el
texto histórico con esta corrección enlazada.

## Lo que impide concluir Wu 1

1. Con B fijo queda el defecto K B^(-c'); hacer M→∞ no lo elimina.
2. K no está explicitada. El lado derecho puede no mejorar siquiera la
   cota elemental dWu≥0 para una barrera concreta que sepamos cubierta.
3. Hacer B→∞ exige barreras cubiertas arbitrariamente grandes. Como
   `Cubierta B` incluye todos los enteros hasta B, disponer de ellas ya
   implica Collatz. No se obtiene ese paso aumentando un censo finito.
4. El corolario sobre descenso por debajo de f(n)→∞ no permite sustituir
   f por la constante 1. Tampoco densidad cero de excepciones es ausencia
   de excepciones.

El diagnóstico no refuta el teorema de Nashida: identifica el límite del
puente propuesto. El paso adicional debe controlar el destino, suministrar
una cota aplicable a una barrera cubierta o tratar las excepciones por otra vía.

## Herramienta que se incorpora al camino: combinar escalas

En las secciones 4–6, Nashida combina dos estimaciones para un mismo
problema de barrera; usa comparaciones demostradas al cambiar entre
conteos en intervalos y probabilidades ponderadas en ventanas.

La primera cota, normalizada en una capa de rango M y válida para
L0≤L≤M con un umbral absoluto L0, tiene la forma

$$
C(M+1)(L+1)e^{-c_B L},\qquad L=\lfloor\log_2B\rfloor.
$$

Con L fijo, empeora al aumentar M. El artículo la utiliza sólo hasta una
escala de arranque cuya magnitud logarítmica es v=e^(c_B L/2). Allí el
producto v e^(-c_B L) todavía decrece con L.

Las ventanas contienen enteros impares en [y,y^α] y llevan pesos
proporcionales a 1/n, normalizados por su suma. Ésta es la ley finita
usada en ese paso, distinta del conteo uniforme de semillas del enunciado.
Las comparaciones entre ambos objetos forman parte de la prueba.

Para avanzar a escalas mayores dispone de una recurrencia entre ventanas
con α>1 y error del tipo (log x)^(-d), con d>0. Para x0>1, en escalas
x_j=x_0^(α^j), la acumulación queda dominada por la serie geométrica

$$
\sum_{j\ge0}(\log x_j)^{-d}
=\frac{(\log x_0)^{-d}}{1-\alpha^{-d}}.
$$

Es independiente del número de ventanas recorridas. Al elegir el arranque
en función de B y convertir de nuevo a conteos, se obtiene el control
uniforme en X. No interviene una suposición de independencia de las
paridades de una órbita fija.

**La idea reutilizable es empalmar una cota de base con una propagación
cuyo error total esté controlado.** Antes de aplicarla hay que demostrar
la correspondencia de observables, el solapamiento de rangos y la suma
de errores. Sus aplicaciones candidatas y las obligaciones particulares
para Pandas, Wirsching, CST y la cadena de Gao están en el
[plan vigente](../transversal20260927/PLAN_SESIONES_20260928.md#herramienta-que-aporta-la-lectura-de-nashida-combinar-escalas).
La sección 7 del propio artículo ya discute cómo equilibrar las escalas
y mejorar el exponente; esa optimización no debe presentarse como una
nueva aportación nuestra.

## Alcance de la auditoría y decisión

Se leyó el PDF completo y se contrastaron las definiciones y los pasos
principales con `Col`, `Main`, `Bridge`, `Uniform`, `Explicit` y
`ShaikBridge`; se inspeccionó el tramo añadido de `FixedBarrier.lean`
dentro del parche. Se consultaron también `Density`, `Power`, `Defs`,
los scripts de descarga, las versiones, el manifiesto y dos registros
de verificación. Esto no es una revisión línea por línea de todo el código.

Las dependencias externas son la formalización de Mazur, commit
`ca3dd0d63920411213403092aecc6946619eb082`, y la de Shaik, commit
`7239f88d05d8262d4778f3c46f4560905052872f`, con el parche de Nashida.
No se descargó ni recompiló su cierre. Sus registros de axiomas y de
`leanchecker` son evidencia **del autor**, distinta de `lean_local.txt`.
El registro del 27-09 pertenece a su repositorio fuente, commit abreviado
`8528d93`; no es una ejecución nuestra sobre el snapshot `976fffb…`.

La diferencia de versiones Lean se ha identificado, no se ha probado una
incompatibilidad. Una reproducción externa debe hacerse aislada, con las
versiones fijadas, antes de reemplazar `CotaBarrera` por un teorema importado.
No se modificó la configuración Lean del laboratorio.

**Decisión:** el bloque inicial entrega un puente útil y certificado como
implicación, además de una técnica para revisar las demás rutas. No justifica
poner Wu 1 a plazo ni integrar ahora todo el proyecto externo. Según el
orden solicitado, el siguiente bloque es Pandas. La reproducción completa
de Nashida queda como ampliación concreta si aparece una aplicación que
necesite eliminar la hipótesis externa del certificado local.

Para reproducir sólo el puente, desde `depuracion/gao20260920/formal`:

```text
lean --version
lake env lean ../../nashida20260928/CondorasBarrera.lean
```

No se ejecutaron los experimentos históricos, cálculos de constantes ni
un nuevo barrido de semillas. Tampoco se publicó ni contactó a terceros.
