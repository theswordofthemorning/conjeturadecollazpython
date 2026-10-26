# Balance estratégico de Collatz — 25-10-2026

La pregunta de esta sesión es si conviene seguir buscando una prueba universal
con el programa actual. No se intenta producir otro lema ni ampliar censos.

**Recomendación: pausar temporalmente la búsqueda universal bajo los métodos
actuales.** Hay resultados parciales sustantivos y un mapa lógico del problema;
no se ha identificado un mecanismo que cierre sus dos obstáculos universales.
La recomendación no afirma que Collatz sea inaccesible, que los resultados sean
inútiles o que ninguna combinación futura pueda funcionar. Tampoco constituye
una decisión de pausa tomada por el usuario.

## Alcance de la revisión

Se inventarió el repositorio completo: 3564 archivos versionados, incluidos
1475 Lean, 483 Python y 185 Markdown. Se recorrieron las 123 piezas de las
nueve ramas del [mapa](../coherencia20260913/mapa_investigacion.json), sus
dependencias y límites, y se abrieron las notas y los enunciados decisivos.
Se contrastaron las rutas recientes de Ocelotas, Perdices, Judas/YAH y los seis
trabajos de Nashida descargados el 20-10. Se consultaron fuentes primarias
externas para las comparaciones con Tao y los anuncios de OpenAI.

Es una revisión global de la estrategia, con comprobaciones focalizadas;
**no una nueva auditoría línea por línea de las 1475 fuentes Lean**, ni una
certificación independiente completa de los artículos externos. Gran parte
del volumen son certificados y productos generados. No se precargaron
conversaciones ni toda la base SQLite, ni se repitieron censos costosos.

El registro contiene 360 filas: 246 demostradas, 92 medidas, 13 conjeturadas y
nueve refutadas. Esas filas incluyen antecedentes, reformulaciones, resultados
condicionales y entradas administrativas. No son 246 pasos independientes de
una cadena que termine en Collatz. La incidencia histórica de la fila 71 sigue
señalada; no se usa como fundamento de este balance.

## Qué está ganado y qué sigue faltando

| Rama del mapa | Aportación comprobable | Límite para la prueba universal |
|---|---|---|
| Fundamentos | Definiciones, identidades afines, cilindros de paridad y distinción entre mapas. | Codificar exactamente una órbita no demuestra que termine. |
| Fusión | Tejonas/Hienas: coalescencia de vecinos en densidad 1; Alpacas: familias de consecutivos que llegan a 1, arbitrariamente largas y altas. | La coalescencia puede compartir un futuro desconocido; construir familias no cubre una semilla arbitraria. |
| Cadena | Modelos de mezcla y resultados sobre leyes de paridad/residuos. | La continuación del 25-10 excluye la convergencia a una ley fija bajo supervivencia H_K. Falta una transferencia válida a cada semilla excepcional. |
| Transferencia | Cotas, truncaciones y diagnósticos de contracción, incluidos Pumas/Langostas/Erizas. | Cotas de sistemas truncados no dan automáticamente control global; la contracción uniforme excesiva ya tiene una obstrucción. |
| Gao | Formalización de la coalescencia literal y sus puentes; Wu 2; equivalencia útil para Wu 1. | Wu 1 y la llegada a 1 en densidad natural 1 siguen abiertas en el repositorio. |
| Descenso | Ocelotas: CST hasta 83 rachas bajo hipótesis externas precisas. | No se controla un número arbitrario de rachas ni se prueba que siempre exista el primer cruce. |
| Fuga | Reducciones Casa y restricciones de Colisiones sobre una hipotética órbita inyectiva. | Restringir la forma de una fuga no demuestra que no exista. |
| Perdices | Reinicios de fuga pura, congruencias, restricciones de repetición y análisis exacto de las relajaciones del reloj. | Falta control uniforme para una única semilla positiva a través de cambios arbitrarios de bloques. Incluso el piloto A/B no cubriría todo Collatz. |
| Otras | Pandas, Wirsching, secuencias, experimentos y conexiones. | Las hipótesis de duración o de densidad local que permitirían concluir siguen sin demostrar; OEIS no valida pruebas. |

Fuentes principales: [Tejonas](../gao20260920/Tejonas.md),
[Hienas](../gao20260920/Hienas.md), [Alpacas](../garner20260926/Alpacas.md),
[WuEnunciado](../gao20260920/formal/WuEnunciado.lean),
[matemática de los modelos](../coherencia20260913/Matematica.md),
[Erizas](../frente20260910/Erizas.md), [Pandas](../pandas20260930/LEEME.md) y
[Wirsching](../wirsching20260930/LEEME.md).

Hay dos matices importantes. Primero, Garner construye una familia infinita
real de órbitas que llegan a 1: no es sólo una medición. Pero la elección de la
semilla forma parte de la construcción, y no resuelve el caso de una semilla
impuesta de antemano. Segundo, el teorema llamado `conjetura_wu_uno` en Lean
prueba una equivalencia entre dos límites; su nombre no significa que uno de
esos límites haya quedado establecido.

En [OcelotasRozier](../cst20260930/OcelotasRozier.lean), 83 cuenta rachas
impares hasta un primer cruce finito del producto multiplicativo. No cuenta
pasos ni un porcentaje de Collatz. Se supone LMN o Rhin y la cobertura de
Roosendaal hasta 46645791847966786687 con tiempo clásico a 1 no mayor que
2480. La cobertura externa y los teoremas analíticos no se convierten en
pruebas internas sólo porque `#print axioms` muestre los axiomas estándar:
son premisas del enunciado. La [revisión](../cst20260930/revision_rozier_20261016/REVISION.md)
distingue esas obligaciones. Aumentar 83 a otra constante no elimina por sí
solo la necesidad de controlar todas las rachas.

## El obstáculo universal sí tiene una formulación precisa

Para esta sección, el dominio es el de los enteros positivos y el mapa es
el atajo `T(n)=n/2` si n es par, `(3n+1)/2` si es impar. Escribimos
`x_j=T^j(n)`, `S_k=#{j<k: x_j impar}` y `P_k=3^S_k/2^k`.
Los índices cuentan pasos de T; no hay ley aleatoria ni condicionamiento.

[Casa](../casa20261004/CasaPlano.lean) y
[Mínimos](../perdices20261007/MINIMOS.md) dejan esta reducción:

```text
Collatz  <=>  MuroB y ausencia de circuitos positivos no triviales,

MuroB: para todo n>=2 existe k tal que P_k(n)<1.
```

Ambas condiciones siguen abiertas. Colisiones permite extraer, de una
hipotética órbita positiva inyectiva, reinicios cada vez mayores en los que
P nunca baja de 1. Eso reduce el tipo de fuga que habría que excluir. No
excluye tales reinicios. Los circuitos quedan como una obligación separada.

Por tanto, decir «ni siquiera delimitamos el muro» sería injusto con lo
conseguido. Decir «tenemos una ruta clara para atravesarlo» tampoco está
respaldado. Una equivalencia puede localizar la dificultad sin reducirla
lo suficiente para que una herramienta disponible la resuelva.

## Qué ocurre al intersectar los patrones

La idea de combinar restricciones merece una prueba de compatibilidad, no
sólo una lista más larga de propiedades. Aquí aparecen tres problemas.

**1. Las conclusiones no siempre hablan del mismo objeto.** La mezcla puede
referirse a palabras elegidas uniformemente, Gao a una densidad de semillas,
Alpacas a semillas construidas y Perdices a una órbita excepcional fija.
Pasar entre esos dominios exige un teorema. Condicionar a sobrevivir puede
destruir la ley de mezcla. No se pueden multiplicar proporciones como si los
filtros fueran independientes bajo una misma ley.

**2. La pequeñez de la excepción no es su vaciedad.** Incluso una intersección
finita de conjuntos de densidad 1 puede dejar excepciones. Una cota sublineal
para su cantidad puede crecer sin límite. Un teorema válido casi seguramente
para sucesiones de paridad tampoco cubre automáticamente cada entero fijado.
Nada de esto constituye una excepción a Collatz: explica por qué falta una
implicación lógica.

**3. Varias restricciones son consecuencias de una misma identidad.**
En las ventanas de Perdices esto se puede comprobar exactamente, sin una
suposición probabilística. Se reprodujo de manera independiente el testigo de
[Ventanas simultáneas](../perdices20261007/congruencias_codex20261016/VENTANAS_SIMULTANEAS.md):

```text
W = AABAAABBAAAAAABAAAAABABAAABAAABBB, A=1, B=110.
33 bloques, 53 pasos de T.
```

| Restricciones simultáneas | Cantidad | Umbral racional exacto | Menor entero admitido |
|---|---:|---:|---:|
| Ventanas de bloques | 561 | 4247/729 | 6 |
| Ventanas expansivas entre pasos T | 1391 | 3964757/177147 | 23 |
| Paridades e integridad de toda la palabra | Un cilindro módulo 2^53 | Residuo exacto | 6416623 |

El 23 satisface todas las 1391 desigualdades de tamaño, pero tras
`23 -> 35 -> 53` el bloque B prescrito daría `241/4`. La composición racional
aceptada no es una órbita entera con esas paridades. Se cotejaron literalmente
los 53 pasos desde 6416623.

Este testigo excluye obtener `L<=3*ceil(log2(n+5))`, sin término aditivo,
únicamente combinando esas desigualdades: ya las satisface conjuntamente.
No refuta el reloj orbital ni todos los posibles coeficientes C,D; tampoco
incluye todas las ventanas contractivas ni cualquier restricción aritmética
imaginable. Su alcance es preciso y limitado.

Conservar todas las congruencias mediante CRT recupera el cilindro exacto,
pero reconstruir el residuo no proporciona todavía una cota uniforme para
su menor representante. Ése es un punto concreto donde las intersecciones
ya se estudiaron y sigue faltando una estimación nueva.

La otra diferencia decisiva es de cuantificadores: existen prefijos
arbitrariamente largos con semillas que cambian con la longitud. Eso no
produce una semilla positiva que realice una palabra infinita. La familia
de unos `n_L=2^L-1` lo ilustra: su límite 2-ádico es -1, no un natural
positivo fijo. A la inversa, refutar una familia concreta no elimina todas
las concatenaciones no periódicas posibles.

El patrón común que encuentro es éste: las estimaciones promedio dejan una
excepción; las cotas por complejidad dejan complejidad arbitraria; las cotas
de tamaño pierden información de integridad. **No hay en el repositorio un
teorema que haga incompatibles simultáneamente esas posibilidades para toda
semilla positiva.** Esto es un diagnóstico del estado de las pruebas, no una
demostración de que exista una órbita que satisfaga todas las restricciones.

## Nashida: alcance real de los seis trabajos

Se cotejaron las cabeceras remotas con las copias locales: los seis commits
siguen coincidiendo. Las versiones y sus huellas están en
[NASHIDA_ANALIZAR](../ccchallenge20261019/NASHIDA_ANALIZAR.md). Se revisaron
enunciados, hipótesis, secciones pertinentes y parte del modelo formal;
no se reconstruyeron sus proyectos Lean ni se certificaron todas sus pruebas.

| Trabajo | Qué aporta según el enunciado revisado | Qué no suministra a esta ruta |
|---|---|---|
| [Dichotomy, I, r3](https://github.com/harappa/collatz-termination-certificate-dichotomy/tree/a138adb7c7efaec8addd06722f40f015c7f2d9be) | Clasificación de certificados escalonados de valuaciones en una clase definida de mapas. La obstrucción general no está formalizada en Lean. | Ausencia de un certificado de esa clase no equivale a no terminación ni excluye toda prueba de terminación. |
| [Matrix barriers, II, r3](https://github.com/harappa/collatz-matrix-interpretation-barriers/tree/8e7d6da6319c1c1b36ce3549fe06e00d0586a025) | Barreras para formas especificadas de interpretaciones matriciales naturales y siete sistemas debilitados resueltos. | No resuelve los sistemas originales de YAH ni nuestro piloto completo. |
| [Arctic barriers, III, r5](https://github.com/harappa/collatz-arctic-interpretation-barriers/tree/de961be6671b2084ae0189a3572b674c60788456) | Barreras para interpretaciones EWZ concretas: naturales en T y árticas en T, H, R_H y reversos correspondientes. | No cubre automáticamente G, reglas eliminadas, toda cadena de procesadores ni otros órdenes. |
| [Terras bound, r7](https://github.com/harappa/collatz-terras-bound-improvement/tree/84de3b5dda58f6b8f37bebb9d96f488bdb7f813d) | Mejora de un exponente de conteo excepcional, bajo una hipótesis analítica explícita de Bugeaud. | Una mejora de exponente no convierte el conjunto excepcional en vacío. |
| [Fixed barrier, r8](https://github.com/harappa/collatz-fixed-barrier-power-saving/tree/976fffb160744c56f1f26912f7bd23d195fe02d2) | Cota uniforme `E(X,B)<=K*B^(-c')*X`, con K inefectiva, para órbitas que nunca bajan hasta B. | Para un B fijo ya verificado deja un término positivo. Mandar B a infinito usando cobertura de todos esos B presupone lo que falta demostrar. |
| [Generalized density, r5](https://github.com/harappa/collatz-generalized-natural-density/tree/a390df858b5433039c7fbaeb6e8713d6ac247d8d) | Resultados de densidad para mapas generalizados; la versión natural incorpora una hipótesis de Matveev. | Los resultados de mínimos en densidad no excluyen por sí solos todos los ciclos ni toda órbita excepcional. |

El [puente local de barrera fija](../nashida20260928/LEEME.md) ya distinguía
la cota externa, la cobertura finita y el objetivo Wu 1. Sigue faltando
ese cierre. Como control conceptual, la clase generalizada admite el mapa
con rama impar `3n-1`, que tiene el ciclo `5,14,7,20,10,5`; se cotejó con
enteros. No es un contraejemplo a `3n+1` ni al teorema de densidad: muestra
por qué la conclusión de éste no es una afirmación universal de llegada a 1.

Hay además una diferencia verificable para trasladar la parte III al piloto.
Nuestro G usa `3z/2` para z par y `(9z+1)/8` para `z=7 mod 8`; fuera de
esas ramas para. El H del artículo usa otra rama par. El modelo genérico de
III, definición 7.1 y `CollatzProof/Arctic/Gen/Model.lean`, fija bloques con
pares (bits consumidos, factores de 3) iguales a (8,5) y (11,7).
Una concatenación de a ramas A y b ramas B de G tendría
`m=a+3b`, `s=a+2b`, de donde `a=3s-2m`. Ambos pares exigirían `a=-1`.
Por tanto, esos bloques no se trasladan por sustitución directa de palabras
de ramas de G. Esto no descarta otra codificación o una generalización
demostrada del argumento.

El [plan del 19-10](../ccchallenge20261019/PLAN.md) contiene extrapolaciones
demasiado amplias desde «enredado» hacia matrices/árticas en general. Debe
leerse con estas restricciones y con las observaciones del 20-10, no como
un teorema de imposibilidad de toda esa familia de métodos.

En [Judas/YAH](../judas20261016/escalera/yah/INFORME_YAH.md), los UNSAT se
refieren a plantillas y dimensiones ensayadas; no se conservaron certificados
UNSAT. Los MAYBE, límites de tiempo y memoria de AProVE no prueban
imposibilidad. Tampoco aportan un motivo matemático para repetir búsquedas
mayores sin cambiar el mecanismo. La equivalencia paridades ↔ no parada de G
está formalizada; el puente SRS ↔ G conserva prueba escrita, no formalización
completa.

Mi valoración de Nashida es, por tanto: trabajo pertinente para precisar
límites y estudiar densidades, cuya revisión independiente completa sigue
pendiente. No encontré en estos seis trabajos un puente universal listo para
incorporar, ni fundamento para considerarlo una vía de probabilidad alta.

## Probabilidades, Tao y decisiones de recursos

No existe aquí una muestra calibrada de programas de investigación comparables
que permita estimar una probabilidad de resolver Collatz con estas herramientas
y este presupuesto. Las pruebas realizadas tampoco son ensayos independientes
de «éxito de la estrategia». Asignar 50 %, 10 % o 1 % sería presentar una
intuición como estadística. La probabilidad no está estimada; eso no significa
ni cero ni cincuenta por ciento.

Separar tres preguntas evita una confusión: que Collatz sea verdadero, que
una ruta sea lógicamente suficiente y que podamos demostrar sus premisas
pendientes con los medios disponibles. Mucha evidencia favorable a la primera
no cuantifica la tercera. Más secuencias, lemas o casos finitos tampoco son
un porcentaje completado de una demostración universal.

[Tao](https://arxiv.org/abs/1909.03562) prueba que, para cualquier función
f(n) que tienda a infinito, casi toda órbita baja de f(n), en densidad
logarítmica. Gao estudia coalescencia; Garner construye familias convergentes.
Son conclusiones distintas. No hay una escala matemática que permita afirmar
que estamos «casi igual» o «más cerca» por compartir vocabulario y técnicas.
La metáfora de la ciudad y el barrio no sirve como medida de proximidad.

El [anuncio oficial de OpenAI sobre Navier–Stokes](https://openai.com/index/navier-stokes-solution/)
existe y describe una prueba con forzamiento, formalización Lean y un sistema
interno de investigación. No se auditó esa prueba en esta sesión. El anuncio
no calibra las posibilidades de este repositorio; no se estimaron ni
compararon recursos computacionales.

La decisión se apoya en las obligaciones que faltan y en la ausencia de un
mecanismo nuevo identificado, no en una probabilidad ficticia ni en competir
en cómputo. Las últimas extensiones han mejorado límites, formalización y
conocimiento de obstrucciones. Su aportación marginal al cierre universal
no demuestra una tendencia que justifique continuar por inercia.

## Condiciones para reabrir la búsqueda

Recomiendo conservar los resultados y pausar las sesiones abiertas cuyo éxito
sea «encontrar otra combinación que quizá resuelva Collatz». La revisión
humana o publicación de los resultados parciales puede tener valor propio,
si el usuario decide dedicarle recursos, sin presentarla como acercamiento
automático a la conjetura universal.

Una reanudación tendría fundamento si aparece al menos una propuesta concreta:

- Un control aritmético nuevo para una semilla positiva fija a través de
  cambios de bloques arbitrarios, que supere los testigos racionales y no
  sea simplemente el reloj reescrito.
- Una transferencia demostrada desde una ley de mezcla a las órbitas
  excepcionales que realmente se necesita excluir, con hipótesis verificables.
- Un resultado externo que cierre una premisa universal pendiente y cuyo
  mapa, dominio y cuantificadores coincidan con los nuestros.

Para decidir una reapertura, la propuesta debería especificar el enunciado,
la implicación hacia MuroB o la exclusión de circuitos, qué hipótesis nueva
puede verificarse y un criterio de descarte acotado. No basta con mejorar
otra constante, renombrar una equivalencia o sumar un nuevo barrido.

El punto aritmético de los representantes de cilindros es el lugar más
concreto donde concentraría una futura idea externa. Hoy sigue siendo un
problema identificado, no un método disponible. No lo recomiendo como
otra promesa para prolongar inmediatamente el trabajo.

## Continuación autorizada de Perdices

Después del balance, el usuario pidió retomar Perdices durante la sesión.
Los tres puntos anteriores son criterios para justificar una vía universal;
no eran promesas de que Perdices los resolvería ni un requisito que impidiera
esa exploración autorizada.

La continuación produjo [una cota de población protegida](../perdices20261025/PROTEGIDOS.md)
y una [prueba de no convergencia de la ley bajo H_K](../perdices20261025/SESGO_FRONTERA.md),
ya módulo 3. Esto descarta una premisa concreta de mezcla. Se obtuvo además
un [criterio temporal condicional](../perdices20261025/FRECUENCIAS_TEMPORALES.md)
y su [balance ternario general](../perdices20261025/OBSERVABILIDAD_TERNARIA.md).
La hipótesis de frecuencias para una órbita excepcional sigue pendiente;
los balances modulares admiten todavía el testigo racional de 23.
Los [retornos aritméticos](../perdices20261025/RETORNOS_ARITMETICOS.md)
añaden una obstrucción con órbitas enteras: no funcionan los rangos
eventualmente monótonos en tamaño dentro de una lista fija de residuos
y valoraciones polinómicas. No se excluyen otras plantillas.

Por tanto, **no se ha satisfecho ninguno de los tres criterios de reapertura
de la vía universal**.
Sí cambió el conocimiento de una ruta: una convergencia que estaba abierta
queda descartada por la prueba escrita, con núcleo combinatorio formalizado.
Esto no demuestra agotamiento de Perdices ni aporta una probabilidad de éxito.
La [evidencia de esta continuación](../perdices20261025/evidencia_sesion.json)
registra cinco altas y 71 consultas Lean, con los tramos pendientes explícitos.

### Continuación del 26-10: comprobación de una fuente candidata

El usuario reactivó el objetivo de Perdices, manteniendo los tres criterios
anteriores. [Límites reales](../perdices20261026/LIMITES_REALES.md) construye
palabras A/B aperiódicas cuyas series inversas convergen en los reales a
-3/2 y a -2. Para esta última, el límite 2-ádico es impar y distinto de -2.
Esto concreta dentro del lenguaje estudiado el defecto del transporte de
racionalidad advertido en Cola: el límite real no hereda la integridad
2-ádica de sus sumas parciales, y una pseudotrayectoria racional acotada
puede ganar denominadores sin ser una órbita racional de T.

La convergencia real universal de la construcción está formalizada; la
aperiodicidad tiene prueba escrita. Se contrastaron los §§2 y 6 de
López–Stoll (2021). **No se refuta su teorema principal ni se incorpora
como premisa demostrada.** Ninguno de los tres criterios queda satisfecho.
Se agota ese transporte automático, no toda la ruta Perdices.

La continuación [digital](../perdices20261026/PESOS_BINARIOS.md) demuestra
variaciones de peso binario ilimitadas en ambos sentidos dentro de una
misma clase de retornos enteros; descarta las dos monotonías del perfil
propuesto. El [examen de precisión](../perdices20261026/PRECISION_CRECENTE.md)
conserva la obligación del reloj. La [auditoría de parada](../perdices20261026/AUDITORIA_RUTA.md)
no permite cerrar el objetivo: sigue pendiente una clasificación concreta
de matrices acopladas H. Ninguno de los tres criterios se ha satisfecho.

[Trazas y constantes](../perdices20261026/TRAZAS_MATRICES.md) avanza ese
frente: conexión bidireccional implica igualdad de los seis intercambios
matriciales; se excluye la familia binaria `M_a=M_b=tI` con constantes
libres, en cualquier dimensión. Nueve consultas Lean cubren las trazas y
el núcleo escalar, con traducciones pendientes declaradas. Las matrices
generales siguen sin clasificar. La búsqueda nueva con constantes sin
cota da UNSAT para matrices 0/1 y timeout para 0..3 conectadas; no son
una prueba general. Ninguna condición primordial queda satisfecha.

La [clasificación con F invertible](../perdices20261026/CLASIFICACION_F_INVERTIBLE.md)
reduce A≠B a dos formas de rango uno y una resonancia 2:3. Trata los
bordes singulares mediante prueba escrita; Lean certifica seis núcleos
algebraicos. La factibilidad de sus constantes, F singular y A=B no
escalar siguen pendientes. Esto tampoco satisface una condición primordial.

## Verificación de la fase inicial de auditoría y conservación

- `git fetch origin` y estado inicial: main coincide con origin/main;
  se preservó `.claude/` sin versionar. No se hizo commit ni publicación.
- Lean 4.32.2: recompilación focalizada de `GaoLiteral.lean`,
  `GarnerEnunciado.lean` y `WuEnunciado.lean`, con dependencias ya compiladas.
  Las cinco consultas `#print axioms` sólo dieron `propext`,
  `Classical.choice`, `Quot.sound`; ninguna dio `sorryAx`. No fue una
  reconstrucción limpia de toda la cadena ni una revisión humana del enunciado.
- Cálculo independiente con enteros/Fraction del testigo de 53 pasos,
  sus 561/1391 ventanas y el residuo mínimo. Comprobación de los pares de
  bloques de Nashida y del ciclo del otro mapa indicado arriba.
- Coincidencia SHA-256 normalizada a LF de las 48 entradas del manifiesto
  de Mínimos y las 94 del balance Codex de Perdices. Son comprobaciones de
  conservación, no una nueva compilación de esos módulos.
- Evidencia histórica de Ocelotas/Perdices/YAH conservada y distinguida de
  los controles nuevos. No se relanzó el conjunto general de controles.
- En esa fase inicial se mantuvieron sin cambios `afirmaciones.db`,
  `respuestas.db`, el registro versionado y los repositorios vecinos.
  La continuación posterior sí añadió cinco afirmaciones por el generador,
  conservando literalmente las 360 anteriores y sin modificar `respuestas.db`.

Los resultados de los controles y los commits externos consultados quedan
en [evidencia.json](evidencia.json), correspondiente a la auditoría inicial.
La revisión humana, la prioridad y la
correspondencia exacta con los originales históricos siguen pendientes.
