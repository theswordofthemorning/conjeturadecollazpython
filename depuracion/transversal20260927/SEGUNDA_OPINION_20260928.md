# Segunda opinión: del encuentro al descenso

28-09-2026. Evaluación estratégica a petición del usuario, sin subagentes
ni nuevos experimentos numéricos. Esta nota propone trabajo: no declara
resuelta otra conjetura ni cambia el registro de afirmaciones. Conserva
como antecedente el [plan del 27-09](LEEME.md).

**Seguimiento del mismo día:** por petición del usuario, el orden de
ejecución pasa a Nashida → Pandas → Wirsching → CST, según el
[plan por sesiones](PLAN_SESIONES_20260928.md). El análisis estratégico
inicial de esta nota se conserva. La [auditoría de Nashida](../nashida20260928/LEEME.md)
ya localizó el original y certificó localmente el puente como implicación;
allí se corrige también el borde de la barrera descrito más abajo.

## Mi elección inicial

**Retomaría la conjetura del tiempo de parada del coeficiente de Terras
(CST), atacando el término aditivo y los residuos admisibles en el primer
cruce del coeficiente.** Empezaría por familias de palabras de paridad con
pocas rachas impares y longitudes sin cota. El primer objetivo candidato
es el caso de dos rachas, sujeto a cotejar antes su alcance con la
bibliografía.

La razón es concreta: el laboratorio ya tiene una identidad y una
reducción formal útiles en [atacacst.lean](../../atacacst.lean). Ese frente
pregunta cuándo una órbita baja de su propio valor inicial. Resolver CST
excluiría los ciclos positivos no triviales; dejaría pendiente la
divergencia. Es una pieza con una consecuencia identificable para el
«cerco» que propone el usuario.

No tengo evidencia para prometer que CST sea más fácil que Wu 1. La
priorizaría por la precisión del obstáculo, la infraestructura existente
y la posibilidad de obtener resultados sobre familias infinitas antes
de intentar el enunciado completo. Mi confianza es mayor en este
diagnóstico que en la viabilidad de cerrar toda CST.

## Lo que enseña el repositorio

El estado vigente registra Gao, Garner y Wu 2 como demostrados en Lean,
con revisión humana de enunciados e interpretación todavía pendiente.
Leí sus declaraciones finales y la evidencia de axiomas; esta sesión no
recompiló el proyecto. Las demostraciones producen coalescencia y rachas;
la construcción de Garner, además, proporciona rachas que sí terminan.
Eso no establece la llegada a 1 de una semilla arbitraria.

Hay dos obstáculos distintos:

1. **Destino.** Dos trayectorias pueden encontrarse sin haber determinado
   a dónde va la trayectoria común.
2. **Excepciones.** Un conjunto de densidad cero puede contener una órbita
   excepcional. Incluso demostrar llegada a 1 en densidad uno necesitaría
   otro argumento para alcanzar a todas las semillas.

Esto ya estaba advertido en el puente histórico posterior a phi, en
[RutaTeoremas histórica](../../archivo/contexto_20260913/RutaTeoremas.md.txt),
y vuelve a aparecer en el plan de ayer. Mi cambio es de prioridad.

Hay además una señal especialmente útil: [espejoak.lean](../../espejoak.lean)
transporta los conteos finitos de fusión balanceada entre los atajos
3n+1 y 3n−1. **Ese observable compartido no basta para distinguir sus
destinos.** Esto limita los argumentos que sólo usan ese conteo; no
demuestra la inutilidad de toda investigación sobre pares. Una nueva
variable que conserve valor absoluto, término aditivo o destino podría
aportar lo que allí se pierde.

También conservaría las advertencias de
[Matematica.md](../coherencia20260913/Matematica.md) sobre densidades y
de [Erizas](../frente20260910/Erizas.md) sobre la contracción uniforme
descartada. Los bits justos describen una ley exacta sobre clases en un
horizonte finito; no autorizan a tratar la órbita de cada entero fijo
como una nueva sucesión independiente.

## El obstáculo exacto de CST

Usaremos exclusivamente el atajo

$$
T(n)=\begin{cases}n/2,&n\text{ par},\\(3n+1)/2,&n\text{ impar},\end{cases}
$$

en enteros positivos. El tiempo se mide en iteraciones de T. No hay aquí
ley aleatoria ni condicionamiento probabilístico. Sea s_j(n) el número
de impares entre n y T^(j−1)(n), y definamos, con j positivo,

$$
\kappa(n)=\min\{j\ge1:3^{s_j(n)}<2^j\},\qquad
\sigma(n)=\min\{j\ge1:T^j(n)<n\}.
$$

El mínimo vale infinito si el conjunto es vacío. En esta nota sigma es
el tiempo de **descenso**, distinto de la sigma de fusión de la cadena.
CST afirma sigma(n)=kappa(n) para todo n≥2. No es el tiempo de llegada a 1.

La iteración afín da

$$
2^jT^j(n)=3^{s_j(n)}n+B_j(n),\qquad B_j(n)\ge0.
$$

El término B empieza en cero. Al añadir un paso par permanece igual;
al añadir uno impar pasa de B_j a 3B_j+2^j. Antes del primer cruce no
puede haber descenso, porque el coeficiente es al menos uno. En el
primer cruce k, lo que falta es exactamente

$$
B_k(n)<\bigl(2^k-3^{s_k(n)}\bigr)n.
$$

Decir que el coeficiente ya contrajo no prueba esta desigualdad: ése es
el problema, no un detalle que pueda eliminarse con una aproximación.

### La reducción que ya tiene el laboratorio

Sea w una palabra de paridades de longitud k, con primer cruce justo en
k: para cada prefijo propio de longitud j≥1 se cumple 3^(s_j)≥2^j, y al
final 3^s<2^k. Su realización determina una clase r módulo 2^k, con
0≤r<2^k. Escribamos

$$
A=3^s,\qquad \Delta=2^k-A>0,\qquad t=T^k(r).
$$

Aquí se extiende T a cero con T(0)=0 para poder usar representantes
residuales; las semillas del problema siguen siendo n≥2. La identidad
formalizada como `terras_1_2` dice

$$
T^k(2^kq+r)=Aq+t.
$$

Por tanto, el descenso equivale a

$$
t<r+\Delta q.
$$

Sea q_min el menor entero no negativo que hace 2^k q_min+r≥2: vale cero
si r≥2 y uno si r es cero o uno. Como Delta es positivo, **para demostrar
el descenso en toda esa clase basta, y es necesario, probarlo en su
menor semilla admisible**:

$$
t<r+\Delta q_{\min}.
$$

La equivalencia se obtiene sustituyendo la identidad afín y ordenando
los términos; no usa datos de un barrido. Su suficiencia está recogida
por `palanca`. Los lemas `tramo_finito` y `tramo_finito_fino`
garantizan descenso fuera de segmentos finitos de cada clase. **El
archivo no demuestra la desigualdad anterior para todos los primeros
cruces.** Tampoco se certificó hoy en Lean esta presentación completa con
palabras, primer cruce y representante mínimo.

Aquí cambiaría el trabajo anterior de
[atacacst.py](../../atacacst.py) y [atacacst2.py](../../atacacst2.py):
el objeto principal sería la relación entre el término aditivo y el
menor representante permitido, no el tamaño del siguiente barrido.
Tener un segmento finito por clase y por longitud deja una unión infinita
cuando la longitud es arbitraria.

## Primer objetivo y forma de avanzar

**Objetivo candidato, todavía no demostrado:** probar el descenso en el
primer cruce para todas las semillas n≥2 cuya palabra hasta ese cruce
tenga la forma

$$
w=1^a0^b1^c0^d,\qquad a,b,c,d\ge1,
$$

con los cuatro exponentes sin cota. Un uno indica un paso impar y un cero
uno par. Hay que imponer además la condición de primer cruce de todos
los prefijos. No se supone que la semilla llegue a 1.

Este objetivo excluye una forma de posible fallo de CST a cualquier
escala. Es más informativo para esta estrategia que verificar todas las
formas hasta una nueva longitud. Aun así, no puedo afirmar su novedad
ni su dificultad sin un cotejo bibliográfico específico.

Procedería así:

1. **Cerrar las definiciones y recuperar el caso conocido de una racha.**
   Rozier–Terracol tratan el caso de un máximo local en su apéndice A;
   distinguen el argumento acíclico de la exclusión conocida de
   circuitos. Lo usaría como control y antecedente, sin presentarlo como
   hallazgo propio. Su observación 5.5 propone organizar el estudio por
   número de máximos. Hay que cotejar también la literatura sobre ciclos
   con pocos máximos antes de atribuir novedad al objetivo de dos rachas.
   [Artículo, versión 5](https://arxiv.org/html/2502.00948v5).
2. **Mantener juntas congruencias y desigualdades.** Obtener para la
   familia elegida una parametrización exacta de los enteros admisibles
   y del término aditivo. Una cota para B que olvide qué r puede
   acompañarlo puede perder precisamente la información decisiva.
3. **Buscar un mecanismo que sobreviva al alargamiento de las rachas.**
   Por ejemplo, una reducción entre palabras que conserve la condición
   de primer cruce y permita comparar el margen r+Delta q_min−t,
   interpretado en los enteros. Reducir sólo el término aditivo, sin
   controlar el cambio del representante, no bastaría.
4. **Formalizar después el argumento que cierre una familia infinita.**
   Primero la prueba escrita independiente; luego las definiciones y el
   certificado Lean, con revisión de axiomas. El entregable no sería otra
   reformulación de CST ni un archivo que presuponga la desigualdad
   pendiente.
5. **Evaluar si el mecanismo se extiende a más rachas.** Cada familia
   demostrada restringiría la forma de un eventual contraejemplo. Probar
   algunos números fijos de rachas no cierra el caso arbitrario; haría
   falta una inducción o reducción uniforme adicional.

### Criterio para continuar o cambiar de frente

Continuaría si aparece una desigualdad que maneje exponentes arbitrarios,
una reducción bien fundada entre palabras o una restricción nueva y
demostrada sobre todos los posibles fallos de una familia. También una
obstrucción precisa a un mecanismo propuesto sería un resultado útil.

Cambiaría de frente si el esfuerzo sólo permite aumentar cortes finitos,
si la hipótesis necesaria equivale otra vez a toda CST, o si la familia
elegida ya está cubierta sin dejar una herramienta extensible. No hay
base para comprometer años antes de superar esta primera evaluación.

## Qué parte del cerco cerraría

La consecuencia de CST para los ciclos puede verse directamente.
En el mínimo m>1 de un supuesto ciclo no hay descenso. Pero al completar
una vuelta de longitud l la identidad afín da

$$
2^lm=3^{s_l(m)}m+B_l(m),\qquad B_l(m)>0.
$$

Un ciclo positivo tiene pasos impares, de modo que el término aditivo es
positivo y 3^(s_l(m))<2^l. Así, kappa(m) es finito y sigma(m) infinito:
contradice CST. Esta implicación también está recogida en
[Rozier–Terracol, introducción](https://arxiv.org/html/2502.00948v5).

**CST por sí sola no excluye que ambas paradas sean infinitas.** Para
deducir Collatz mediante este camino quedaría demostrar que kappa(n) es
finito para todo n≥2; con CST, la inducción fuerte cerraría la llegada a 1.
Tampoco un fallo de CST refutaría automáticamente Collatz: podría haber
descenso real más tarde.

Conviene evitar un objetivo que aparenta ser menor: la conjetura 6.1 de
Rozier–Terracol sobre ausencia de nuevas secuencias paradójicas es
explícitamente más fuerte que Collatz y CST. No la adoptaría como escalón
previo. [Sección 6](https://arxiv.org/html/2502.00948v5).

## Prioridad estratégica propuesta en la evaluación inicial

| Frente | Aporte posible | Decisión |
|---|---|---|
| CST por familias infinitas | Descenso; la versión completa excluye ciclos no triviales | Frente principal, con la evaluación inicial descrita |
| Pandas y pregunta de Gao | Relaciones entre tiempos de órbitas que llegan a 1 | Cierre complementario acotado |
| Wu 1 | Densidad natural uno de llegada a 1, dado Gao | Objetivo mayor; falta un mecanismo para controlar el destino |
| Mejor ritmo de coalescencia | Cuantifica mejor el encuentro | Trabajarlo si una aplicación nueva necesita ese ritmo |
| Puente con Nashida | Cota condicional para la proporción que termina | Lectura y auditoría antes de invertir en integración formal |
| Predecesores de Wirsching | Propagar una excepción a un conjunto grande | Segundo frente estratégico, con una dificultad aritmética diferente |

**Pandas.** [La prueba escrita](../../lemadepandas.txt) merece completarse
en Lean. Su dominio ya presupone que ambas órbitas llegan a 1. Resolver
la pregunta de Gao mediante ella sería un resultado concreto; no
eliminaría por sí mismo órbitas que nunca llegan. Tampoco convertiría
la cota global de residuos que falta en una tarea pequeña por llamarla
lema auxiliar.

**Wu 1.** [Condoras](../gao20260920/formal/Condoras.lean) identifica el
obstáculo: dado Gao, hace falta llegada a 1 en densidad natural uno.
No lo trataría como una repetición de Wu 2. Un ritmo mejor de fusión
seguiría necesitando un argumento que conecte la trayectoria común con 1.

**Nashida.** El enunciado citado ayer se refiere a una cota uniforme en
el extremo X para órbitas que permanecen sobre una barrera N0. Si se
acepta ese enunciado y se sabe que todo n<N0 termina, el puente propuesto
es lógico. Una constante inefectiva no garantiza una mejora numérica
utilizable. Una verificación hasta una barrera fija tampoco autoriza a
enviar N0 a infinito. No pude consultar el texto primario ni su código
Lean; por eso esta evaluación mantiene el puente como condicional, sin
adoptar como comprobada la descripción de ayer.
[Referencia citada](https://doi.org/10.5281/zenodo.22986670).

**Actualización posterior:** se leyó r8 y el código. Su barrera es estricta,
de modo que la condición correcta cubre `1<=n<=N0`; con `n<N0` y `N0>=2`
hay que usar `N0-1`. El [certificado local](../nashida20260928/CondorasBarrera.lean)
conserva como hipótesis la cota externa. La reproducción de todo Nashida
permanece pendiente; el diagnóstico del bloque y la técnica de combinar
escalas están en su [ficha](../nashida20260928/LEEME.md).

**Wirsching.** Su programa de 2003 tiene pasos conjeturales; no aporta
ya la densidad positiva necesaria. El objetivo original se formula para
semillas no cíclicas y no divisibles por 3, distinción relevante para el
puente con Collatz. [Artículo](https://www.aimsciences.org/article/doi/10.3934/dcds.2003.9.771),
[texto del autor](https://www.math.uni-bielefeld.de/baake/algdyn/posden.pdf).

Hay una actualización respecto de ayer: Tavares, en un preprint de
agosto de 2026, presenta pruebas de las conjeturas 1 y 3 del programa y
deja pendiente la condición (estrella 3), a la que apunta la conjetura 2.
El obstáculo restante exige control por residuos; el comportamiento del
operador límite no lo proporciona automáticamente. Leí el planteamiento
y la identificación de lo pendiente, sin auditar toda la prueba. Es una
referencia que revisar, no un resultado incorporado al laboratorio.
[Preprint y versión consultada](https://arxiv.org/html/2608.27617v1).

### Una combinación que sí corresponde a la idea del cerco

Con el resultado de Gao del repositorio, serían suficientes estas tres
piezas, **todavía abiertas en el alcance necesario**:

- CST, que excluiría ciclos positivos no triviales.
- Wu 1, que daría densidad natural uno de llegada a 1.
- Densidad inferior positiva de predecesores de cada entero positivo no
  cíclico y no divisible por 3. Para esta combinación bastaría positividad
  para cada semilla; no hace falta una misma constante para todas.

En efecto, una órbita que no llega a 1 tendría, excluidos los otros ciclos,
un punto m no cíclico y no divisible por 3: basta tomar el resultado de
un paso impar del atajo. Todos sus predecesores tampoco llegarían a 1.
La tercera pieza les daría densidad inferior positiva, contradiciendo
la segunda. Es una justificación condicional del encaje entre los frentes,
no una prueba actual de Collatz ni una estimación de cuánto falta.

Por eso mantendría Wirsching como segunda línea. Si falla la primera
evaluación de CST, estudiaría precisamente la estimación por residuos que
falta en ese programa, cotejando primero el nuevo preprint. No empezaría
reescribiendo toda su maquinaria.

## Alcance de la revisión y siguiente acción

Revisé el conjunto del repositorio mediante inventario, índices y
dependencias; profundicé en los frentes que pueden cambiar esta decisión.
No fue una auditoría línea por línea de todo el código ni una revalidación
de todas las pruebas. La lectura cubrió:

- Estado, pendientes, declaraciones finales de Gao/Garner/Wu, evidencia
  Lean y cadena Martas–Tejonas–Hienas–Alpacas–Condoras.
- Plan transversal de ayer, Pandas, sus hipótesis y el alcance descrito
  para Nashida y Wirsching.
- Palanca CST, scripts de segmentos y descenso, y la diferencia entre
  prueba universal y sus verificaciones finitas.
- Teorema espejo, rutas descartadas, restricciones de transferencia y
  pasajes históricos pertinentes. Los históricos se usaron como
  antecedentes, no como instrucciones o estados vigentes.
- Fuentes primarias externas enlazadas, consultadas al 28-09-2026; no se
  certificó exhaustivamente la novedad de los objetivos candidatos.

**Siguiente paso que propuso esta evaluación inicial:** fijar y cotejar
bibliográficamente el enunciado de dos rachas y trabajar su parametrización
simbólica. Su turno queda ahora después de los bloques más cortos del
[plan vigente](PLAN_SESIONES_20260928.md).
Todavía no necesita un nuevo censo. Las declaraciones finales ya obtenidas
y su revisión humana siguen siendo una obligación propia, independiente
de cuál sea el siguiente frente de investigación.
