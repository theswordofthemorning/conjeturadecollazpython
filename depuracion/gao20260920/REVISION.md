# Revisión local del candidato del 20-09-2026

## Estado

**Hay un ensamblaje candidato; no se declara resuelta la conjetura.**
La ruta actual es [CF_F con ensayos finitos](Ensayo_finito.md), basada en
[CF_H armónica](Ventana_armonica.md), variante de
[CF y CF2](Cota_finita.md) que evita la fórmula binomial. Evita el reloj casi seguro en el
cierre y la supermartingala infinita; conservan la ley original.
La próxima acción es una segunda auditoría conjunta del enlace
palabras–clases y del protocolo de ensayos, partiendo de los enunciados
actuales. El desarrollo universal de cilindros ya está escrito en
[Cilindros.md](Cilindros.md). C1, V1–V2 de W y el máximo finito del
producto están certificados: [detalle](Control_aditivo_producto.md).
Supervivencia inferior, cola de mixtos y [reloj M6/H3](Reloj_bloques.md)
también están certificados. La [ventana VH conjunta](Ventana_conjunta.md)
queda certificada con parámetros explícitos y uniformidad en |c|<=|C|.
El enlace con Hormigas y el piso de fusión antes de H+D están certificados.
Las [guardias y el conteo](Guardias_finitas.md) tambi?n est?n certificados.
Falta la cota del evento de supervivencia con pocas entradas admisibles.
La formalización probabilística
integral y el cotejo directo del artículo de Gao siguen pendientes.
No hubo revisión externa.

## Cambio de ruta

El objetivo anterior pedía una ventana constante para W a la salida.
Esta tanda permite una ventana `O(T^5 log(T+2)^2)` con
`T=O(log(2+|c0|))`. Se paga con una palabra de accesibilidad de longitud
`O((log log(2+|c0|))^2)`. El riesgo resultante es subpolinómico en
|c0|, que sería suficiente con arranques polinómicos y ensayos separados.
No se ha demostrado ni refutado el P2 original de ventana fija.

## Deducciones escritas

1. [Reloj_global.md](Reloj_global.md): envolvente simultánea
   `|u_t|<=K_omega(t+1)^4`, estancias de frontera, reloj `S_i=O(i^4)`
   y arranques `|c_i|=O(i^16)` sobre no absorción, casi seguramente.
2. [Salida_ampliada.md](Salida_ampliada.md): salida en una ventana
   temporal explícita y offset polilogarítmico con probabilidad
   `>=1/(4sqrt(2T+3))`; cota universal escrita para la política desde k=1.
3. [Ensamblaje_candidato.md](Ensamblaje_candidato.md): selección de
   ensayos, control de índices, suma de riesgos y paso propuesto a phi=1.

## Controles ejecutados

`python -B -X utf8 depuracion/gao20260920/verificar.py --salida depuracion/gao20260920/evidencia.json`

Resultado: [evidencia.json](evidencia.json).

- 14.024 transiciones cotejadas con dos enteros positivos y el mapa T;
  desigualdad normalizada exacta con Fraction. Incluye frontera, signos,
  cero y vecinos de potencias de 2 y 3 hasta exponente 127.
- Bijección entre palabras de ancla y residuos en niveles 3..12:
  todas las `2^n` palabras aparecen una vez en cada nivel; cotejo
  simultáneo de valores, offsets y diferencias de conteos impares.
- 8.265 semillas del constructor desde k=1, incluyendo potencias y
  vecinos hasta exponente 1024: todas fusionan dentro de V4.
  Longitud máxima observada: 2.658. No es una constante universal medida.
- 910 transiciones en rachas de k=1; 4.096 palabras para la identidad
  afín, con extensión multiplicativa después de salir.
- Certificados enteros de umbrales, binomiales hasta m=499 y seis
  parámetros adversarios, incluyendo un offset de 4.097 bits.

`lean --version`: Lean 4.32.2, x86_64-w64-windows-gnu,
commit `f3b06c705e6c85f5314019d5d3baab0fec5b580c`.

`lean depuracion/gao20260920/ingredientes.lean`: termina con código 0.
Doce `#print axioms`: sólo `propext`, `Classical.choice`, `Quot.sound`
o ninguno. Sin `sorryAx`, `sorry` ni `native_decide` en el certificado.
Se certifican desigualdades racionales, paridad k=1, descenso de gaps,
la cuenta de longitud, un paso binomial y constantes del producto.
**No** certifica aún probabilidades, todos los tiempos de parada,
Borel–Cantelli, el ensamblaje de cilindros ni la conclusión de densidad.

## Puntos auditados por razonamiento

- W se prolonga multiplicativamente después de tau; congelarlo habría
  invalidado la contracción usada para V1.
- Las cotas de momento permanecen incondicionales. Su transferencia
  usa una unión finita para W y una envolvente casi segura para u.
- Las excursiones y los tramos de frontera son finitos antes de estimar
  el reloj global; no se presupone existencia de las visitas posteriores.
- La desigualdad implícita para S_n se resuelve mediante monotonía
  de `x/log(x+2)^2`, sin presuponer un soporte `n^2`.
- Las palabras de absorción se observan bajo bits originales; no se
  fuerza el camino. La siguiente prueba comienza después de terminarlas.
- La constante 2,5 de Hormigas no se reutiliza. V4 se deriva con
  un factor de contracción 5/6 y una cuenta cuadrática holgada.
- Las constantes enormes de V3 son deliberadas: en la semilla 0,
  H supera 31.000 millones. No se ejecutó ese barrido; los controles
  verifican las desigualdades de los parámetros, no ese censo.

## Obligaciones antes de elevar el candidato

1. Rehacer universalmente el transporte de medida en cada cambio de
   ancla: paridades de una pendiente impar, orientación y relación con
   la absorción balanceada. La prueba inductiva está bosquejada; los
   controles finitos apoyan, pero no reemplazan, su desarrollo completo.
2. Auditar una segunda vez el ensamblaje probabilístico como un solo
   argumento, incluyendo filtración completada tras absorción y el
   índice de la siguiente entrada si una palabra termina en k>=2.
3. Localizar y leer el enunciado primario de Gao. La bibliografía de
   Lagarias atribuye densidad uno a la fusión clásica antes de log2(n);
   no confundirlo con igualdad de alturas finitas ni con Collatz.
4. Ampliar la certificación Lean de los puentes universales que sea
   razonable formalizar; dejar explícito cualquier tramo escrito restante.

No se modificó zootheorem ni se publicaron resultados.

## Ampliación de la revisión de cilindros

Se desarrolló la inducción con `n=r+2^t*m`, pendientes `3^p,3^q`,
refinamiento `m=2*l+d` y orientación independiente de l. Se distingue
coincidencia accidental de un representante de igualdad balanceada de
las expresiones de una clase. El enlace a fusión clásica usa `n>=2^(2t)`
para cada t fijo; no intercambia límites de densidades.

`lean depuracion/gao20260920/cilindros.lean` pasó: ocho teoremas,
sólo `propext`, `Classical.choice`, `Quot.sound` o ninguno. Total de
esta tanda: veinte certificados parciales, sin `sorryAx`.
El cierre por riesgos tiene además una prueba escrita explícita por
la supermartingala `1_(ningun exito) exp(suma de riesgos)`.

## Segunda auditoría: cota finita

Se desarrolló CF para `N=2^m`, `h=N^6`, m>=10:

    P(sigma>h) <= 3/N+66/h+1/(4h^3)+(1-p_m)^J_m.

Los parámetros p_m,J_m están dados explícitamente. La deducción separa
el evento bueno futuro de las guardias conocidas al empezar cada ensayo.
La inducción de riesgos se hace sin condicionar a ese evento futuro.
Se verificó que el reloj también acota porciones todavía incompletas en h;
usar sólo tramos terminados habría dejado un hueco en la prueba finita.

Se precisó el éxito como absorción antes de la siguiente entrada elegida,
incluyendo la espera posterior a la palabra. Así la filtración de ensayos
es `G_j=F_(A_j)` y el resultado del ensayo j es medible en `G_(j+1)`.

`python -B -X utf8 depuracion/gao20260920/cota_finita.py --salida depuracion/gao20260920/evidencia_cota_finita.json`
pasó. Comprobó m=10..64 y parámetros hasta m=1.000.000, sin construir
las clases ni ejecutar las trayectorias de esos horizontes.
En m=1.000.000: `D=627264`, `b=18`, `ell=20`, `z=372697`.
La conclusión de que el término de riesgo tiende a cero usa
`D=O(log(m)^2)`; no se deduce de esas cinco evaluaciones.

`lean depuracion/gao20260920/cota_finita.lean` pasó, cinco resultados
universales sin `sorryAx`: presupuesto de frontera, presupuesto interior,
crecimiento exponencial, presupuesto global e inducción finita de riesgos.
Total local: **25 certificados parciales**. La hipótesis `hpaso` del
certificado de riesgos aún se enlaza con la cadena mediante prueba escrita.

La siguiente obligación formal concreta es enlazar C1–C7 con la cadena
original: pasar de la dominación global al momento y formalizar las
paradas guardadas; no añadir más evaluaciones enormes de parámetros
como sustituto.

## Dominación de la cadena completa, formalizada

`cadena_completa.lean` define estados, absorción, ambas fronteras y las
transiciones con división entera. `dominacion_cadena` demuestra la forma
homogénea de E1 para todos los estados y ambos bits. No recibe la
dominación como hipótesis ni se limita a una rejilla de ejemplos.
`coef_es_potencia` identifica los denominadores con `3^k`.

Compilación Lean 4.32.2: código 0, sin avisos; nueve `#print axioms`,
sólo `propext`, `Classical.choice`, `Quot.sound` o ninguno. El total de
esta tanda pasa a **34 certificados impresos**, todos sin `sorryAx`.
No se formalizan aquí los momentos, independencia en paradas ni CF.

## Búsqueda primaria de Gao en la segunda auditoría

Crossref confirmó el DOI y enlazó la API de Elsevier. OpenAlex y
Semantic Scholar devolvieron sólo el DOI como ubicación abierta,
sin otra copia PDF. La API de Elsevier entregó metadatos y declaró
archivo abierto, pero `view=FULL` respondió 401; PDF respondió 406.
La URL pública de descarga de ScienceDirect respondió 403. No se
obtuvo ni se guardó el artículo completo, ni se contactó a terceros.
La atribución del enunciado sigue basada en Lagarias y debe cotejarse.

## Momentos y máximo finito de la cadena completa

[Momentos.lean](formal/Momentos.lean) importa la transición absorbente
ya certificada, traduce su dominación a reales y demuestra

    promedio_n sqrt(tamano) <= rho^n sqrt(tamano_0)+32(1-rho^n),
    rho=31/32; tamano=|c|/3^k, cero después de absorber.

La deriva se obtiene con `sqrt(1/2)<=91/128` y
`sqrt(3/2)<=157/128`, cuyas cotas se verifican por sus cuadrados
racionales. Desde `(0,1)` el momento es <=32 para todo n.
No se asume como hipótesis una recurrencia de expectativas: se deduce
del árbol de la transición completa. `promedio_hojas` identifica su
promedio con una suma de `2^n` hojas con multiplicidades.

`alcanza` representa haber superado U en 0..n. Una marca booleana
persistente permite identificarlo con un conteo de hojas dividido
por `2^n` (`alcanza_conteo`). Markov puntual y unión finita dan
`sqrt(U)*P(maximo>U)<=32(n+1)`. Para U=h^4, h>=1,
`envolvente_cf` certifica el término <=66/h de C1.

`lake build GaoCore GaoFormal` pasó con Lean 4.32.2 y Mathlib fijada
en `905b95818eb32af7874a58b427f50c1711a5e96c`. Las trece consultas
nuevas de axiomas usan sólo `propext`, `Classical.choice`, `Quot.sound`;
no aparece `sorryAx` ni avisos en la compilación final. Total local:
**47 certificados impresos**. [Evidencia con hashes](evidencia_momentos.json)
y [reproducción](formal/README.md).

C1 queda cerrada en el modelo finito de bits. Siguen pendientes las
leyes de rachas y excursiones, el control de W y el enlace de los
ensayos guardados con la recurrencia de riesgos. El transporte a
clases de enteros continúa escrito en Cilindros.md. CF conserva su
estado de candidata y no se anuncia resolución de Gao.

## Resto afín y producto normalizado

[Resto.lean](formal/Resto.lean) enlaza la cadena completa con
`u=Pi*u0+W` para toda palabra interior hasta su último paso, incluida
la primera salida a k=1. Certifica el error aditivo <=1/2, la marca
persistente de salida, W multiplicativo posterior, V1, V2, el coste
<=1/(4Q) de la ventana elegida y la conversión a `|c_tau|<=3(R+1)`.

[Maximos.lean](formal/Maximos.lean) generaliza el conteo de cruces
sobre árboles finitos y añade la dominación por un potencial
superarmónico. [Producto.lean](formal/Producto.lean) lo aplica a
`sqrt(|Pi_t/(31/32)^t|)` y demuestra
`P(existe t en [T,T+H]: Pi_t>(31/32)^t)<=(61/62)^T` para todo T,H.
Mejora el factor 62 previo; no se cambian los parámetros de CF.

Compilación conjunta `lake build GaoCore GaoFormal`: código 0,
Lean 4.32.2, Mathlib fijada. Veinte consultas nuevas de axiomas sin
`sorryAx`; total local **67 certificados impresos** en ocho archivos.
Las cotas racionales del producto se contrastaron con Fraction.
[Alcance matemático](Control_aditivo_producto.md) y
[evidencia actual con hashes](evidencia_resto_producto.json).
La evidencia de momentos anterior conserva su configuración histórica;
el proyecto actual añade tres módulos a la misma versión de Mathlib.

El siguiente enlace pendiente es R1/G2 y la probabilidad conjunta de
V3, después los ensayos guardados de CF. Las cotas nuevas no demuestran
el P2 de ventana fija bajo condicionamiento. CF sigue candidata.

## Variante armónica: supervivencia y energía de banda

[Supervivencia.lean](formal/Supervivencia.lean) certifica
`P(tau>t)>=1/(t+1)` usando altura armónica de media 1 y crecimiento
de a lo sumo uno por paso físico. No requiere balota ni binomiales.
[Banda.lean](formal/Banda.lean) detiene la altura en 0 o L y usa
`V(x)=x(L-x)` para acotar la cantidad esperada de pasos mixtos por
L−1. Incluye el contador real de pasos, Markov, la cota 1/L de tocar
el techo y el acoplamiento con la excursión original. Resultado:
`P(M_h>=n)<=1/L+(L-1)/n`, y para n=L^2, coste <=2/L.

Las dos cotas sirven para [CF_H](Ventana_armonica.md) cambiando
Q a T+1 y recalculando G,D,p. Los presupuestos del reloj global se
conservan; la ventana sigue dando riesgos subpolinómicos. La
derivación completa sigue candidata, con M6 como próximo enlace formal.

Dieciocho consultas nuevas de axiomas sin `sorryAx`, total **85**
en diez archivos. [Compilación actual](evidencia_supervivencia_banda.json).
El [contraste independiente](verificar_armonica.py) por pares positivos
pasó 88 niveles y 4.840 comparaciones de colas, incluidos h=0 y L=1.
[Salida y parámetros](evidencia_armonica.json): en m=1.000.000,
`D=817216`, `b=32`, `ell=20`, `z=182731`; no es un censo.

Registro: 223 afirmaciones. Se añaden el control armónico demostrado
y CF_H conjeturada, manteniendo las versiones anteriores de CF.

## Rachas enteras y reloj por bloques

`RachasEnteras.lean` cuenta exactamente las palabras que realizan h
pasos compartidos; no exige que el offset final siga par. Incluye cero
y offsets negativos. `UmbralRachas.lean` prueba la valoración de
`3^k-1`, su cota logarítmica y la ampliación de umbrales.
`Reloj.lean` conserva el contador de mixtos y el invariante k<=M+2;
su inducción por bloques deterministas certifica M6. La partición del
evento de supervivencia y la cota de Banda certifican H3.

[Enunciados y derivación independiente](Reloj_bloques.md).
Las 22 consultas de axiomas de estos tres archivos no usan `sorryAx`;
total local **107** consultas en trece archivos. No se cuentan como
nuevas las once consultas del módulo histórico `rachas.lean`, importado.
[Compilación y hashes](evidencia_reloj_lean.json).

El contraste por pares positivos pasó 832 conteos de rachas, 280
casos M6, 720 H3 y 2.312 descomposiciones del evento. No se enumeraron
los horizontes enormes de CF_H. Registro: 224 afirmaciones, con M6/H3
demostradas y CF_H todavía conjeturada. Siguiente: VH conjunta y
ensayos guardados; permanecen los límites sobre cilindros y Gao primario.

## Ventana conjunta y parámetros uniformes

`Palabras.lean` identifica todos los eventos con funciones de una misma
palabra y sus promedios. `SalidaPalabras.lean` extrae la primera salida
y aplica la identidad afín a ese prefijo. `Ventana.lean` prueba la
resta conjunta sin independencia; `ParametrosVentana.lean` descarga
las condiciones exactas de T,H,L,n,a,s y el coste del producto.
`ventana_uniforme` fija los parámetros con C y sirve para todo |c|<=|C|.

[Prueba, alcance y próximo paso](Ventana_conjunta.md). Son 22 nuevas
consultas de axiomas sin `sorryAx`, total local **129** en diecisiete
archivos. [Compilación y hashes](evidencia_ventana_lean.json).
El contraste independiente pasó 3.577 palabras, 114.716 inclusiones
de eventos y 315 cotas de producto; incluye salidas en H y la
continuación multiplicativa de W. La aritmética se cotejó hasta c=2^1024,
sin enumerar sus horizontes. Registro: 225 afirmaciones; VH demostrada,
CF_H conjeturada. Próximo: acceso de Hormigas y ensayos guardados.

## Hormigas universal y ensayo de duración fija

`Hormigas.lean` certifica la palabra de absorción de longitud
`16(ceil(log2(2+|c|))+1)^2`, incluidos signos y c=0. Los cuatro viajes
reducen la escala a la mitad y se cuentan sus divisiones. `Ensayo.lean`
prueba el peso de una palabra y el relevo desde la primera salida buena:
para |c|<=|C|, fusión antes de H(C)+D(C) con piso `2^-D/(4Q)`.
La prueba usa sólo árboles finitos; no supone Markov fuerte en una salida.

[Enunciados y siguiente protocolo](Ensayo_finito.md). Doce nuevas
consultas de axiomas sin `sorryAx`, total local **141** en diecinueve
archivos. [Compilación y hashes](evidencia_ensayo_lean.json).
Pasaron 8.221 viajes, 2.063 bloques, 4.127 offsets y 147 casos de relevo
con palabras pequeñas. Registro: 227 afirmaciones. EF está demostrado;
CF_F es candidato, con `J_F=floor((N-1)/(H_m+D_m+2))` y el mismo riesgo
p_m. Se preserva CF_H; no atribuirle el protocolo fijo sin cambiar J.

## Cierre del d?a: protocolo y reducci?n global

`Repeticion.lean`, `Guardias.lean` y `ConteoEnsayos.lean` certifican
la b?squeda truncada, el evento de j fallos y su cota `(1-p)^j`.
Supervivencia con `K_C(h)>=1+j(W+2)` implica esos j fallos. Por tanto
`P(sigma>h)<=P(sigma>h y K_C(h)<1+j(W+2))+(1-p)^j`.
[Enunciado, interpretaci?n y primer paso al retomar](Guardias_finitas.md).

16 consultas nuevas sin `sorryAx`, total local **157** en 22 archivos.
[Compilaci?n y hashes](evidencia_guardias_lean.json). El contraste finito
del protocolo en una cadena auxiliar pas? 24.564 casos, 528 comparaciones
racionales y 2.659 inclusiones; no certifica el cierre de Gao.
Registro: 228 afirmaciones. CF_F sigue conjeturada: falta enlazar el
reloj global con el contador, controlar el l?mite y transportar a clases.
La investigaci?n queda pausada a petici?n del usuario al cerrar el d?a.
