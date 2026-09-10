# Frente de densidad: 10-09-2026

## Estado y alcance

**Quinta tanda:** [Puente de las Gacelas](Gacelas.md). La masa h=k-1
es armonica para la cadena entera; su cambio de medida conserva Mangostas,
pero no equivale sin prueba a condicionamiento futuro o reversion.
Se obtiene POR ESCRITO un piso de orden 1/sqrt(log x) para excursiones
largas cuya parte multiplicativa es pequena, por concentracion antes de
condicionar. Falta controlar CONJUNTAMENTE W en la salida: NO es P2.
Ocho resultados Lean y controles exactos; revision externa pendiente.

**Cuarta tanda:** [Reloj de las Mangostas](Mangostas.md). La duracion
compartida a altura fija tiene ley exacta: determinista bajo A=v2(3^k-1),
y A+Geom(1/2) sobre el umbral (Geom empieza en cero). Algebra y conteo
general del automata en Lean; enlace global escrito y cruzado en Python.
Se obtiene un control O(n log n) del reloj de pasos MIXTOS con error
explicito, no del reloj de visitas al fondo. Transferencia P2 pendiente.

**Tercera tanda:** [Obstruccion de las Erizas](Erizas.md). La contraccion
con rho fijo <1/2, eventualmente en tiempo y en TODAS las escalas, es
incompatible con una cota subexponencial de colision entera, incluso
para cada semilla fija alcanzable. Demostracion escrita, ingredientes
Lean y controles exactos; formalizacion integral y revision pendientes.
Esta actualizacion retira ese objetivo uniforme de las secciones 1 y 5.

**Segunda tanda completada:** [Balance de las Castoras](Castoras.md).
La transferencia con las cuatro corrientes, paridad y supervivencia ya
esta derivada y cruzada. Hay dos contraejemplos sinteticos en Lean y
un criterio exacto para la ganancia pendiente. Ver esa nota primero.

Trabajo local, sin agentes ni revision adversarial externa. Hay un lema
comprobado por Lean, controles Python y una correccion del alcance de G5.
No se ha probado el teorema de conteo, P2, densidad uno ni Collatz.
El punto d1 de `encargorevision11.txt` ya sospechaba el cambio de operador;
esta sesion resuelve una parte concreta de esa sospecha.

**Cierre documental:** el resultado Gacelas quedo usado solo como avance
parcial. El siguiente cuello matematico sigue siendo conjunto: controlar
`W_tau` al mismo tiempo que el producto `Pi_tau` en la salida real. En paralelo,
`../zootheorem/drafts/` recibio cinco borradores OEIS de reserva para material
ya verificado (`G`, `H`, `e8`, `e10`, `e12`), excluyendo las entradas
A398792--A398795 ya aprobadas.

## 1. La obligacion que necesita el telescopio

**Actualizacion Erizas:** la condicion suficiente expuesta aqui sigue
siendo logicamente suficiente, pero es IMPOSIBLE en el dominio de todos
los m y tiempos grandes. Se conserva la derivacion para documentar la
ruta descartada. Tambien quedan excluidos los bloques fijos uniformes.

La ley de `conteoconjunto.py` empieza en `(2,c0)`, usa bits equiprobables
y se condiciona a no haber llegado a `k=1`. Llegar a esa frontera termina
una excursion: NO es, por definicion, fusion del par.

Para vivos V y conteos n(k,r), n_k = sum_r n(k,r), se usa

    e_t(m) = (1/V) sum_{k:n_k>0} [2^m sum_r n(k,r)^2 / n_k] - 1.

Una forma SUFICIENTE del objetivo es encontrar un rho fijo < 1/2 y
un tiempo T(c0), con el dominio de c0 explicitado, tales que

    e_{t+1}(m) <= rho e_t(m+1)   para todo t >= T(c0), m >= 1.

Entonces, por induccion y la cota elemental e_T(M) <= 2^M - 1,

    e_{T+n}(m) <= rho^n e_T(m+n) <= 2^m (2 rho)^n.

Hay que controlar tambien T(c0) para usar una ventana proporcional a
log(2+|c0|). Una estimacion restringida a una region escala-tiempo puede
servir, pero requiere rehacer la iteracion dentro de su dominio; no se
puede recorrer una diagonal que abandona las hipotesis.

La afirmacion puntual rho(t,m) < 1/2 NO entrega automaticamente ese rho
uniforme. Ejemplos abstractos (no datos de Collatz):

- rho_t = (t+1)/(2(t+2)): el producto de 2 rho_t hasta n-1 es 1/(n+1),
  que decae solo polinomicamente.
- rho_t = (1 - 1/(t+2)^2)/2: el producto es (n+2)/(2(n+1)), que no
  tiende a cero. Estar siempre bajo 1/2 ni siquiera basta para ese paso.

Otra forma suficiente, para un bloque fijo L, es
e_{t+L}(m) <= theta e_t(m+L) con theta < 2^(-L) uniforme.
No se ha demostrado ni ensayado aqui una mejora por bloques.

## 2. Un error de alcance resuelto

Los mapas auxiliares son tau_k(x) = 3x + (1-3^k)/2, modulo 2^m.
`correlacionafin.py` C6 une las orbitas para alturas 2,3,4,5. En cambio,
`gapmezcla.py` G3/G5 calcula productos con alturas 3 y 5 solamente.

LEMA DE LAS SURICATAS (rigidez de los invariantes comunes de alturas 2 y 3;
Lean, todo m): si f es periodica de periodo 2^m y cumple

    f(3x-4) = f(x),     f(3x-13) = f(x)    para todo entero x,

entonces f es constante. Son exactamente las invariancias para k=2 y k=3.

Bautizado el 10-09-2026 con autorizacion del usuario para nombrar los
hallazgos. Identificador formal: `invariantes_comunes_constantes`.

Demostracion escrita: tau_2 compuesta con tau_3 inversa es la traslacion
por 9. La inversa existe porque 3 es coprimo con 2^m. Una funcion
invariante bajo ambos mapas es invariante bajo esa traslacion; como 9
tambien es coprimo con 2^m, recorre todos los residuos. Luego es constante.
Lean demuestra esto con periodicidad sobre Int y aritmetica modular,
sin asumir transitividad ni inversas como hipotesis adicionales.

En cambio, chi = (1,-1,-1,1), repetido modulo 4, es invariante bajo
tau_3 y tau_5, tiene media cero y NO es invariante bajo tau_2. Estas
afirmaciones tambien estan en Lean. Python comprueba exactamente que
M2=(I+P2)/2 reduce la energia de ese testigo a la mitad.

Por tanto, G5 NO refuta la trivialidad del invariante comun de C6.
No hay un invariante oculto por cambiar del espacio directo al espectro:
se cambiaron los operadores. Un cambio de base no cambia su dimension.

## 3. Lo que este lema NO entrega

Para los operadores auxiliares M_k=(I+P_k)/2, el lema implica
norma(M2 M3) < 1 en media cero a cada escala FINITA: igualdad de norma
en cada promedio exigiria que el vector fuera fijo por ambos mapas,
y la esfera unidad es compacta. Este corolario usa algebra lineal
elemental; el archivo Lean formaliza el lema de invariantes, no las normas.

No implica un margen uniforme en m. La SVD flotante da normas
0.707107, 0.707107, 0.809017, 0.859923, 0.893467, 0.912601, 0.931140
para m=2..8. Esa ventana no determina su limite.

Tampoco identifica M2 M3 con la excursion real: esta incluye las
corrientes de ascenso y descenso, cambios de fibra, pesos y
condicionamiento a sobrevivir. La ausencia de invariantes comunes por
si sola no prueba contraccion de un promedio arbitrario de permutaciones
sin identidad. No se restaura automaticamente la propuesta completa de C6.

## 4. Verificacion y reproduccion

Desde la raiz:

```powershell
python depuracion/frente20260910/invariantes.py
lean +v4.32.2 depuracion/frente20260910/invariantes.lean
python depuracion/frente20260910/contraccion.py
python depuracion/frente20260910/contraccion.py --pasos 25 --desde 12 --m-min 5 --m-max 10 --semillas 999983 999999937 1398101
```

Lean: version instalada 4.32.2; los cinco `#print axioms` no contienen
`sorryAx`. Python: componentes comunes (3,5)=2 y (2,3)=1 en m=2..12,
8.188 identidades de traslacion exactas; SVD etiquetada como medicion.

El nuevo DP usa estados enteros sin reduccion modular, fracciones exactas
y comparacion con 1/2 SIN conversion a float ni filtro positivo. Comprueba
conservacion de masa, 5.680 pasos contra pares positivos y, por arranque,
las 256 palabras de largo 8 mediante los pares reales. Su autor ya habia
leido el codigo anterior: NO es una implementacion ciega independiente.

El barrido por defecto cubre 14 arranques, t=12..15, m=1..12: 672 celdas,
cero cruces de 1/2. La reproduccion de la ventana original cubre 234
celdas. Los registros `*_salida.txt`, `contraccion_reproduccion.txt` e
`invariantes_lean.txt` conservan la salida. Un intento de ampliar a 36
pasos se interrumpio por crecimiento del numero de estados; no cuenta
como verificacion terminada.

Ademas, el script identifica una escala M donde distintos c de la misma
fibra no coinciden modulo 2^M. Para m>=M, e_t(m)=2^m A_t-1 exactamente,
con A_t la colision condicional sobre enteros. Imprime A_{t+1}/(2 A_t),
el limite del cociente al crecer m con t FIJO; no es un limite temporal.

## 5. Siguiente pregunta

**Actualizacion Gacelas:** el reloj condicionado admite un pago explicito
sqrt(H), y la contraccion del producto puede tratarse directamente sin
trasladar el reloj V2. Formular y contrastar ahora un control conjunto
de W_tau y Pi_tau en la salida real. No identificar el h-transform hacia
delante con la ley revertida ni dar por cerrada la transferencia.

**Actualizacion Mangostas:** el ataque directo da una formula exacta
para las colas de racha y reduce los modulos necesarios a 2^A<=4k.
Revisar el enlace con el automata y contrastar su control del reloj
con P2. El condicionamiento a supervivencia FUTURA sigue pendiente.

**Sustituida por Erizas:** estimar directamente las clases especiales
de racha/recarga. Tampoco basta pedir L2 uniforme en 1<=m<=alpha*t:
Erizas excluye ese control. No continuar intentando demostrar el margen
uniforme global siguiente.

La transferencia quedo escrita en [Castoras.md](Castoras.md). Ahora se
busca una propiedad propagable de las leyes alcanzables que acote su
margen H desde abajo, con constante uniforme. Debe controlar los cruces
de corrientes de distintas alturas y la correccion de paridad R, que
puede ser negativa; el simple equilibrio par/impar no basta.

Antes de concluir P2, siguen pendientes las condiciones medidas en
`notaensamblajep2.txt`, incluida la transferencia de perturbaciones y el
control condicionado. No quedan resueltas por esta nota.

## Revision adversarial pendiente

Cuando el usuario la autorice: comprobar que los dos mapas de Lean son
los de las corrientes compartidas; atacar la traduccion de periodicidad
en Int a funciones sobre residuos; comprobar el argumento de igualdad
en la norma de M2 M3; y verificar que ninguna conclusion presume un gap
uniforme ni reemplaza la cadena real por esos operadores auxiliares.
Reproducir los conteos desde la definicion de pares, sin leer los Python
de esta tanda. La coincidencia actual no sustituye esa revision.
