# Exploración de `openai/math`: mecanismos que podrían servir a Perdices

16-10-2026. Exploración solicitada antes de iniciar nuevos cálculos.
**Decisión:** conservar la ruta de descenso eventual y el piloto `1/110`.
La lectura aporta dos posibles mecanismos de investigación, no un lema que
cierre el piloto: incompatibilidad aritmética entre varios colapsos de partes
impares y presupuestos de información sobre una trayectoria fija.

## 1. Material examinado y alcance

Se trabajó directamente en `C:/Users/Home/Desktop/math`. Su HEAD es
`1581d4cbdd69a0faf34b2089614fe2a814316a6a`. El README y el catálogo locales
contienen **719 manuscritos en 372 familias**. La historia explica la retirada
de tres manuscritos y correcciones de otros. El catálogo declara 300/719
resultados principales formalizados; esa cifra no es una verificación nuestra.

Se recorrieron los títulos de las 372 familias; se seleccionaron descripciones
y títulos de 22; se leyeron secciones técnicas de 11 familias y tramos de cuatro
resúmenes de razonamiento. No se leyeron ni auditaron íntegramente 719 pruebas.
La búsqueda textual de Collatz, Syracuse, hailstone y FRACTRAN no encontró
coincidencias en el catálogo ni en los `.tex` y `.md` buscados de preprints y
resúmenes. Esto no certifica ausencia de toda conexión indirecta.

Familias cribadas: 007, 012, 017, 020, 021, 028, 029, 056, 082, 104, 143,
148, 149, 153, 154, 159, 179, 220, 242, 245, 362 y 376. Lectura técnica:
007, 017, 028, 056, 104, 143, 149, 153, 159, 245 y 362. Los resúmenes
consultados pertenecen a 007, 017, 159 y 362; son publicaciones de sus autores,
no memoria propia del sistema que realizó esta exploración.

Fuentes generales: [README][readme], [catálogo][catalogo],
[correcciones][historia] y [anuncio oficial](https://openai.com/index/sharing-ai-progress-in-mathematics/).
El anuncio confirma la publicación; no sustituye la revisión matemática.
Los diez resúmenes incluyen algunos extractos de los problemas originales:
la afirmación antigua de que no se publicaron materiales de razonamiento ya
no describe esta copia.

Los enlaces a math fijan la revisión pública examinada para que la nota sea
consultable desde GitHub. El inventario conserva las rutas dentro de la copia
local, sus huellas y el cotejo de contenido con ese commit.

## 2. El punto de partida del laboratorio estaba más avanzado

El `fetch` obligatorio previo a editar encontró `origin/main` un commit por
delante. Se incorporó mediante avance rápido `a4c8302`, conservando los cambios
locales previos. Ese avance del 14 de octubre contiene resultados que impiden
recomendar como nuevas varias ideas inicialmente sugeridas por el catálogo:

- [Recargas](../perdices20261007/RECARGAS.md) ya refuta el presupuesto
  `epsilon=1/2, K=ell`, y familias más amplias. No basta ajustar una constante
  aditiva a `K=ell`.
- [Perfiles](../perdices20261007/PERFILES.md) excluye rangos locales
  `H(x)+F(v2(u_1*x+v_1),...,v2(u_m*x+v_m))`, con H no decreciente y lista
  finita fija de formas afines de coeficientes naturales. La barrera general
  tiene prueba escrita; el caso `x+1,x+5` está formalizado.
- [Transporte impar](../perdices20261007/TRANSPORTE_IMPAR.md) ya controla el
  producto de cambios de potencial. No queda allí una pérdida proporcional al
  tiempo que podamos eliminar por una mejor telescopía.
- La misma nota prueba por escrito el presupuesto con hasta un cambio y
  exhibe `A^a B` con parte impar final 9 y parte impar inicial no acotada.
  Una monotonía ingenua de la parte impar es falsa.

Por ello, **«encontrar un potencial» sólo sería una propuesta útil si describe
una estructura que escape a esas barreras**. La clasificación anterior no
excluye todo potencial posible, toda memoria de la trayectoria ni toda
estimación global; sí excluye una amplia receta local concreta.

## 3. Qué patrones de prueba aparecen realmente

La coincidencia «para todo» es demasiado amplia. La conexión útil es la
forma del obstáculo: una hipotética excepción infinita produce repetidamente
una exigencia que alguna estructura finita o acotada no puede satisfacer.
El trabajo está en demostrar esa exigencia y su coste acumulable. Los
manuscritos siguientes ofrecen versiones diferentes de esa organización.

| Familia y lectura | Mecanismo examinado | Transferencia posible y límite |
| --- | --- | --- |
| **[056, terminación de programas de modelos mínimos][m056]**; introducción y dificultad | Un contador firmado incluye correcciones locales; un argumento geométrico paga sus déficits y prueba no negatividad. Las pérdidas estrictas se cuentan después. | Es la analogía más cercana a «pagar las recargas». Aquí falta identificar el recurso aritmético que paga; llamar dificultad a la suma actual no lo construye. |
| **[104, juegos de ganancia media][m104]**; estrategia, rango y créditos | El algoritmo combina dos progresos: disminuye anchura o disminuye un presupuesto de masas. La suma de rangos enteros termina la recursión. | Sugiere varios recursos y obligaciones simultáneas. El rango controla su algoritmo sobre un juego finito, no directamente una órbita de Collatz. Falta una representación fiel; un grafo de residuos puede introducir trayectorias falsas. |
| **[159, progresiones aritméticas][m159]**; iteración triangular | Una capa sólo recibe recursos de capas superiores, cuya capacidad ya está acotada. Reiniciar un test no reinicia el presupuesto. | Es pertinente si se descubre una jerarquía aritmética finita o bien fundada. Dos cuentas que se repongan mutuamente sin límite no satisfacen esta condición. El resultado sobre conjuntos de suma recíproca divergente no se aplica a nuestras órbitas inyectivas de suma convergente. |
| **[028, caminatas entre primos gaussianos][m028]**; muestreo, cobertura y telescopio | Se fija una caminata determinista. Sólo se aleatorizan tiempos y pruebas auxiliares; las cargas de información usan una misma ley y condicionamientos anidados. | Aporta una forma de estudiar cada trayectoria sin postular paridades aleatorias. La demostración usa incrementos espaciales acotados, geometría y muchos primos. Esas hipótesis no están dadas para Collatz. |
| **[017, exponente de irracionalidad de pi][m017]**; interpolación y determinante | Varias aproximaciones excepcionales producen un determinante no nulo; se comparan una cota aritmética inferior y una analítica superior incompatibles. | Sugiere estudiar varias recargas extremas enlazadas, en vez de acotar una sola. Faltan el objeto no nulo y las dos cotas; el conteo de ecuaciones por sí solo no prueba rango. |
| **[149, redes de reacciones][m149]**; funciones afines activas y conjuntos absorbentes | Una familia de funciones controla todas las ramas activas, incluidos los empates. La reversibilidad del grafo paga flujos desfavorables. | Enseña cómo tratar cambios de régimen sin perder los bordes. No convierte T en una red débilmente reversible; tomar mínimos de funciones no sortea por sí solo la barrera de Perfiles. |
| **[362, Vlasov–Maxwell][m362]**; impulso firmado y cierre | Se conserva el signo antes de sumar; un supuesto provisional se mejora estrictamente, con constantes independientes del horizonte que se quiere extender. | Útil para organizar estimaciones y evitar circularidad. Su conclusión excluye explosión en tiempo finito; una fuga de Collatz en infinitos pasos no contradice eso. |
| **[007, correlaciones multiplicativas][m007]**; signos, dependencias y rango | Se conservan factores durante la integración y se distingue entre muchas restricciones independientes y patrones de dependencia. | Herramientas para contar dependencias, no un permiso para considerar independientes los cambios de una órbita. Cancelación en promedios, incluso a toda escala, puede dejar excepciones individuales. |
| **143, ciclos límite; 153, convoluciones de Bernoulli; 245, normalización** | Respectivamente: cierre de una clase de objetos bajo operaciones necesarias; cuidado del orden de cuantificadores; transporte entre expresiones con hipótesis sobre el sistema entero. | Son controles de diseño. No proporcionan un puente inmediato a T. La normalización débil universal que exige 245 tampoco está disponible gratuitamente al codificar Collatz. |

Las fuentes técnicas precisas y sus rangos están en
[el inventario de lectura](inventario_lectura.json). Se han distinguido
descripciones del mecanismo de las pretensiones principales de cada paper:
no se adoptan estas últimas como teoremas nuevos del laboratorio.

## 4. Primera transferencia: relacionar varios colapsos de la parte impar

Dominio: enteros positivos; mapa atajo T; bloques reales A=1 y B=110;
longitud L en pasos de T, S entradas impares. Se conserva una semilla n.
Las valuaciones y partes impares son las de Transporte impar, §1.
No hay ley probabilística.

El candidato actual sigue siendo `epsilon=1/2, K=2*ell(n)`, con
`ell(n)=ceil(log2(n+5))`. La obligación ya documentada es

```text
L + 2*v_fin <= 2*v_in + 4*ell(n).                       (P2)
```

La nota de transporte proporciona el encaje

```text
3^S*(n+1) <= 2^(L+v_fin)*q_fin <= 3^S*(n+5).
```

Un valor pequeño de `q_fin` corresponde, en este encaje, a una extracción
grande de potencias de dos. Puede ocurrir en una transición: la familia con
`q_fin=9` obliga a aceptarlo. La pregunta útil es si **muchos colapsos
enlazados desde la misma semilla** pueden seguir pagando ese coste.

La transferencia de 017 consiste en buscar una obstrucción entre varios
episodios, no en trasladar su teorema sobre pi. Un posible esquema de trabajo:

1. Elegir fronteras de grandes recargas por un criterio explícito que no
   presuponga salida. Conservar las identidades afines de todos esos prefijos.
2. Eliminar la semilla común entre algunas de las identidades. La posible
   ganancia debe proceder del acoplamiento entre episodios, no de tratarlos
   como congruencias independientes.
3. Buscar una combinación entera o un menor **demostrablemente no nulo**
   cuya divisibilidad forzada exceda una cota superior de tamaño.
4. Tratar separadamente la degeneración: que el menor sea cero debe dar una
   estructura controlable, no descartarse por ser «atípico».

No tenemos aún ese menor ni las cotas incompatibles. La evidencia que haría
valiosa la propuesta sería un lema para cadenas con dos cambios, con todos
sus exponentes y semillas admisibles, que no resulte del transporte ya conocido.
Los dominios mínimos son `A^a B^b A^c` y `B^a A^b B^c`, a,b,c positivos.
También serviría una obstrucción exacta que descarte esta construcción.

Esto aprovecha el punto más específico de T: la interacción entre las
potencias de 2, las de 3, la suma de 1 y la integridad de toda la historia.
No se ofrece como prueba ni como afirmación de novedad bibliográfica.

## 5. Segunda transferencia: información de una órbita, sin azar supuesto

El punto aprovechable de 028 es el **orden de los cuantificadores**. Primero
se fija cualquier trayectoria que supuestamente evita el objetivo. Después se
elige una distribución finita de tiempos de observación sobre esa trayectoria.
No se sortea una semilla ni se atribuye independencia a sus símbolos.

El lema de coste compartido allí examinado es elemental: para un vector finito
de observaciones X y un registro auxiliar Z,

```text
H(X | Z) >= H(X) - H(Z).
```

Su prueba se obtiene de las dos expresiones de H(X,Z) y de H(Z|X)>=0.
El coste de Z se paga una vez sobre el vector conjunto. Esto no autoriza a
sumar sin más costes calculados bajo leyes o condicionamientos diferentes.
El paper construye precisamente la ley común y la compatibilidad necesarias.

Para trasladarlo hacen falta tres piezas nuevas:

- observaciones finitas del historial aritmético de **una misma** órbita;
- un coste positivo demostrable de persistir o recargar, después de todos los
  condicionamientos anteriores;
- una desigualdad global que permita acumular esos costes sin que crezca al
  mismo ritmo el presupuesto disponible.

Ninguna de las tres viene dada por llamar entropía a la longitud binaria de n.
Una semilla finita puede generar una secuencia determinista infinita. Tampoco
basta que A/B tenga dos símbolos: eso acota entropía por símbolo, pero no
garantiza que evitar la salida consuma información nueva en cada escala.

La caminata gaussiana tiene incrementos en un conjunto finito de vectores;
los incrementos de T son no acotados. Aunque el alfabeto A/B sea finito, no
reemplaza automáticamente esa hipótesis geométrica. Además, las congruencias
módulo potencias de dos están anidadas: no son nuevas coordenadas primas
independientes. Estas son obligaciones concretas de transferencia.

## 6. Qué no conviene importar

1. **Una supuesta ley histórica de éxito.** El repositorio selecciona resultados
   entre miles de intentos; no permite inferir que las fórmulas simples fallen
   pronto ni que cierta apariencia de conjetura prediga su verdad.
2. **Densidad como eliminación de excepciones.** 007, 012, 148 y 154 no cierran
   por su sola forma la órbita individual que falta en Collatz.
3. **Una criba finita sin prueba de fidelidad.** Cancelaciones, §5, ya muestra
   que toda historia finita de etiquetas del piloto tiene representantes
   positivos. Excluir un historial por mero patrón finito chocaría con ello.
4. **Compacidad en el espacio equivocado.** Prolongaciones compatibles en los
   2-ádicos no garantizan una semilla natural positiva; Repeticiones, §5, ya
   construye historias reales que satisfacen cotas de crecimiento sin las
   paridades enteras requeridas.
5. **Indecidibilidad como prohibición de técnicas generales.** La
   indecidibilidad de una familia de sistemas no excluye criterios uniformes
   suficientes ni teoremas para subclases. Exige especificar el dominio de
   cada resultado, no concluir que toda herramienta compartida sea inútil.
6. **Una cota proporcional al tiempo como único tipo de solución.** (P2) es
   un candidato suficiente. Si aparece un descenso bien fundado de otra
   clase, habrá que demostrar su conexión con salida; la ausencia de un
   epsilon uniforme no refutaría por sí sola el objetivo de descenso eventual.

## 7. Formalización y verificaciones de esta sesión

Se leyeron ocho notas de alcance Lean (007, 017, 028, 104, 143, 149, 245,
362), tres configuraciones Comparator y los enunciados y entradas de solución
de GaussianMoat y MassAction. Las configuraciones examinadas sólo permiten
`propext`, `Quot.sound` y `Classical.choice`.

Los `sorry` en `ComparatorChallenges` son huecos deliberados del enunciado de
comparación; las soluciones se señalan en `solution_module`. Su presencia no
es por sí sola evidencia de que la solución use `sorryAx`. A la inversa, leer
la configuración tampoco certifica que la ejecución pase.

El repositorio math pide Lean 4.34.1 y no tiene `.lake` en esta copia. El Lean
del laboratorio reportó 4.32.2. No se instalaron dependencias, no se compilaron
las pruebas de math y no se ejecutó `#print axioms` sobre ellas. No se declara
una auditoría formal propia. En particular, 143 formaliza la afirmación sobre
Liénard quíntico, no por ello el resultado general de Hilbert 16; 104 distingue
su algoritmo aleatorio del artículo determinista; 149 distingue el resultado
previo por estado inicial del nuevo conjunto absorbente común por clase.

No se ejecutaron experimentos de Collatz. Los programas de esta sesión sólo
leyeron texto, PDF y metadatos o verificaron la documentación. No se importaron
experimentos antiguos ni se añadieron afirmaciones al registro versionado.
La sincronización incorporó el registro de 343 filas ya publicado en el commit
remoto; esta exploración no altera su contenido. Durante la lectura inicial
no se modificó math ni se publicaron cambios. La autorización posterior para
commit y push de la documentación se recoge en §10.

## 8. Filtro de admisión de una nueva vía

Antes de desarrollar o ejecutar una propuesta, dejar explícitas estas seis
respuestas. El filtro es una herramienta de selección; no demuestra que una
propuesta que lo supere vaya a funcionar.

1. **Obligación precisa.** Qué desigualdad o excepción aborda y qué puente
   tendría hacia (P2), salida del piloto o descenso universal. Identificar el
   dominio y los cuantificadores; no confundir esos tres objetivos.
2. **Semilla y dependencias.** Qué permanece fijo, qué puede variar y de qué
   dependen las constantes. El presupuesto no puede usar una salida aún no
   probada ni reiniciarse gratuitamente con el valor de una frontera nueva.
3. **Compatibilidad con las barreras conocidas.** Explicar por qué no cae en
   la familia de Perfiles, cómo admite la familia con q_fin=9 y por qué no
   contradice la realizabilidad de todas las historias finitas de etiquetas.
4. **Coste acumulable.** Identificar qué paga cada recuperación y por qué no
   se reutiliza indefinidamente. Conservar signos. Si se usa información,
   declarar ley, condicionamientos y dependencias sobre una órbita fija.
5. **Ganancia matemática nueva.** Señalar el paso que no se deduce ya de (R)
   o del transporte impar. En la vía aritmética, exigir no nulidad y cotas
   incompatibles; en una representación abstracta, justificar su fidelidad
   a enteros positivos y a las paridades reales.
6. **Cierre verificable.** Fijar qué constituiría prueba, contraejemplo a la
   plantilla o una obligación pendiente precisa. Los controles finitos sirven
   para contrastar; una formalización útil debe declarar alcance y axiomas.

Una idea que falle un punto puede conservarse como exploratoria, indicando
exactamente la carencia. No merece un barrido mayor sólo por parecer análoga
a un resultado del catálogo.

## 9. Siguiente entrega propuesta, antes de un barrido

Mantener los cuatro puntos de la ruta oficial, con el conocimiento del día 14.
La siguiente nota debe formular **un lema de acoplamiento entre varias
alternancias**, declarar cómo evita la barrera de Perfiles y explicar por qué
implicaría (P2), o una condición suficiente de salida más débil. Primera
prioridad: divisibilidad frente a tamaño de varias identidades enlazadas.
Segunda: una contabilidad jerárquica o informacional con un coste nuevo probado.

El entregable debe acabar en prueba con dominio, contraejemplo exacto a la
plantilla o el lema preciso que falta. Una nueva notación para la misma
identidad, una estimación promedio o una cota reiniciada en cada frontera no
cumplen ese requisito. La extensión desde el piloto a bloques arbitrarios y
al descenso universal continúa como obligación separada.

## 10. Cierre documental y espera de arranque

El usuario pidió el 16-10 conservar esta exploración en los Markdown,
incluido su filtro y las rutas candidatas, y hacer commit y push. Ratificó
que la conversación continúa antes de iniciar nuevos desarrollos. El anuncio
de un futuro objetivo para avanzar hasta el cierre de sesión no lo activa:
este intercambio sólo cierra y publica la documentación solicitada.

Se enlaza desde el estado breve y desde la sección de reanudación de la
[ruta oficial](../coherencia20260913/RUTA_339_20261012.md). La ejecución de la
investigación queda en espera de una nueva indicación del usuario.

[readme]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/README.md
[catalogo]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/CONTENTS.md
[historia]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/history.md
[m056]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Termination-for-projective-log-canonical-fourfolds-with-rational-boundary-September-24-2026/paper.pdf
[m104]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Deterministic-quasipolynomial-time-mean-payoff-games-September-25-2026/paper.pdf
[m159]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quasipolynomial-Bounds-for-Arithmetic-Progressions-September-23-2026/paper.pdf
[m028]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Bounded-Step-Walks-on-Gaussian-Primes-September-26-2026/paper.pdf
[m017]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/paper.pdf
[m149]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/permanence.pdf
[m362]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/paper.pdf
[m007]: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Ordinary-two-point-correlations-of-multiplicative-functions-September-24-2026/final.pdf
