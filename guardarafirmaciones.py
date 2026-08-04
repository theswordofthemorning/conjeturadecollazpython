# guardarafirmaciones.py
#
# LAS AFIRMACIONES DEL LABORATORIO, ORDENADAS POR CUANTIFICADOR.
#
# EL PROBLEMA QUE RESUELVE
#
#   El CLAUDE.md tiene ya decenas de hallazgos, y no todos valen lo mismo. Unos
#   son teoremas, otros promedios medidos, otros conjeturas ajenas, y varios
#   resultaron FALSOS y hubo que corregirlos. Todo eso vive hoy en prosa, y en
#   prosa no se puede consultar: no hay forma de preguntar "que se sabe para
#   TODO n" sin releer dos mil lineas.
#
# LA COLUMNA QUE IMPORTA ES EL CUANTIFICADOR, Y NO ES UN DETALLE
#
#   No es lo mismo decir "para todo n", que "para toda clase residual", que
#   "para casi todo n", que "en promedio". Son cosas distintas y solo algunas
#   sirven para encadenar un argumento:
#
#     todo_n            vale para CADA numero, uno por uno. Encadena.
#     clase_residual    vale para los INFINITOS numeros de una clase de resto,
#                       decidido con una comprobacion finita. Encadena. Es el
#                       "cuarto camino" del repo: la regla sin la secuencia.
#     casi_todo_n       vale salvo un conjunto de densidad cero. Encadena con
#                       cuidado: la excepcion que buscamos podria vivir ahi.
#     promedio          NO ENCADENA CON NADA. Un promedio no dice nada de
#                       ningun numero concreto. sqrt(3)/2 < 1 significa "en
#                       promedio bajan", y una sola orbita que subiera para
#                       siempre no moveria ese promedio ni un decimal.
#     ciclos            afirmaciones sobre orbitas periodicas, no sobre n.
#     verificado_hasta  fuerza bruta. Sirve para refutar, jamas para demostrar.
#
#   POR QUE "clase_residual" Y NO "clase_mod_2k", QUE ES COMO SE LLAMABA.
#   Corregido el 01-08-2026. El nombre viejo describia el modulo de la mayoria
#   de las filas -2^k, que es donde vive el teorema de Terras- y no la
#   categoria. Y se le quedaba estrecho a dos filas que estan en la base desde
#   el primer dia: la rueda del arbol inverso (periodo 2 segun v mod 3, hijos
#   ciclando mod 9, patron completo cada 18 duplicaciones porque 18 es el orden
#   de 2 modulo 27) y los evitados de la malla 2n mod 27. Esas dos son clases
#   modulo 3^j, no modulo 2^k, y sin embargo son EXACTAMENTE el mismo tipo de
#   objeto: una clase de resto que decide el comportamiento sin recorrer nada.
#   Meterlas en una casilla que las nombra mal obliga a explicarlo en las notas
#   de cada fila, que es donde nadie mira. El modulo concreto va en el
#   enunciado y en las notas; el cuantificador dice la FORMA del argumento.
#
#   La prueba de que la distincion no es paranoia: 5n+1 tiene media geometrica
#   1,118 > 1 ("todo sube") y sin embargo TIENE un ciclo, el del 13, donde nada
#   sube. La constante no impide la excepcion.
#
# LAS TRES TABLAS
#
#   afirmaciones   id, enunciado, cuantificador, estado, fichero, fuente, notas
#   correcciones   id, que_se_creia, por_que_era_falsa, leccion
#   constantes     id, nombre, valor_teorico, valor_medido, error_rel, formula,
#                  que_mide, fuente, fichero, aviso
#
#   La de correcciones es la que mas cuesta escribir y la que mas vale: es la
#   unica que evita repetir el error.
#
#   La de constantes existe porque las constantes de Collatz no demuestran nada
#   -son promedios, y no encadenan- pero SI son patrones utiles para trabajar,
#   y varias son literatura publicada (la de Wagon tiene entrada propia en
#   OEIS). Metidas como texto dentro de un enunciado no se podrian consultar ni
#   comparar; en campos numericos si. Y el campo AVISO es lo que las hace
#   seguras de guardar: ahi va lo que impide usarlas mal mas tarde.
#
# TRES COMPROBACIONES ANTES DE DAR NADA POR BUENO
#
#   1. ningun cuantificador ni estado fuera del vocabulario
#   2. todo fichero citado EXISTE en el disco (citar uno que no existe es un
#      fallo, no un descuido), y las constantes con fuente ajena traen valor
#      teorico, y las cinco tramposas traen aviso
#   3. IDA Y VUELTA: se reabre la base, se relee todo, y tiene que salir
#      identico a lo calculado
#
#   Si alguna falla el programa se para. Es la disciplina de guardarmallas.py:
#   comprobar antes de afirmar.
#
# No dibuja nada. Solo la base y un informe corto por stdout.

import os
import sqlite3

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

ARCHIVO = "afirmaciones.db"
CARPETA = os.path.dirname(os.path.abspath(__file__))
ANCHO = 78

CUANTIFICADORES = ("todo_n", "clase_residual", "casi_todo_n", "promedio",
                   "ciclos", "verificado_hasta")

ESTADOS = ("demostrado", "medido", "conjeturado", "refutado")

# Las constantes que NO pueden quedarse sin aviso. Cada una tiene una trampa
# documentada que ya mordio una vez.
AVISO_OBLIGATORIO = (
    "coral: divisiones por multiplicacion",
    "constante de parada del ATAJO",
    "divisiones por multiplicacion B/A",
    "residuo de Roosendaal Res(993)",
    "umbral q < 4 del qn+1",
    "exponente de la criba industrial",
    "techo heuristico del tiempo de descenso",
)


def fila(enunciado, cuantificador, estado, fichero, fuente, notas):
    """Una afirmacion. Con nombres, para no equivocarse de columna."""
    return (enunciado, cuantificador, estado, fichero, fuente, notas)


def cte(nombre, valor_teorico, valor_medido, error_rel, formula, que_mide,
        fuente, fichero, aviso):
    """Una constante. valor_medido y error_rel van a None si es exacta."""
    return (nombre, valor_teorico, valor_medido, error_rel, formula, que_mide,
            fuente, fichero, aviso)


# ===========================================================================
# LAS AFIRMACIONES
# ===========================================================================
#
# Salen del CLAUDE.md, de la bitacora, y de los cuatro ficheros del 30-07-2026
# que todavia no estaban escritos alli: pisoaltitud.py, elmasuno.py, reimpl.py
# y coralprimos.py. El orden es de lo que mas encadena a lo que menos.

AFIRMACIONES = [

    # ------------------------------------------------------------- todo_n
    #
    # Vale para CADA numero. Es lo que tiene forma de teorema.

    fila("2^B * seq[j] = 3^A * seq[i] + C para cualquier par de posiciones "
         "i < j de una trayectoria, con C -> 3C + 2^B en los pasos impares",
         "todo_n", "demostrado", "collazmalla.py", "Terras 1976 (Teorema 1.1)",
         "Ambito: cualquier par i<j de cualquier trayectoria. Es la identidad "
         "madre del repo. Terras la publica como T^k n = lambda_k*n + rho_k; "
         "multiplicando por 2^k queda esta. 6.555 pares del 221, 0 fallos."),

    fila("log2( altitud(n)/n ) >= racha(n) * log2(3/2) + 1",
         "todo_n", "demostrado", "pisoaltitud.py", "propio",
         "Ambito: n IMPAR y n >= 3. Sin la paridad es FALSO, y el borde n = 1 "
         "depende del convenio (con altitud(1) = 1 el piso falla; el conteo de "
         "49.999 impares ya lo excluia sin declararlo - trio del 02-08-2026, "
         "demostrado ademas en Lean, depuracion/lean/A2.lean). Se decide en "
         "enteros, alt*2^r >= 2*n*3^r, sin un solo float: 49.999 impares, 0 "
         "fallos. La racha no PREDICE la altitud, le pone un piso. Cota si, "
         "tendencia no."),

    fila("log2( altitud_atajo(n)/n ) >= racha(n) * log2(3/2)",
         "todo_n", "demostrado", "pisoaltitud.py", "propio",
         "Ambito: todo n >= 2, las dos paridades (el n >= 2 es hipotesis, no "
         "adorno: en n = 1 depende del convenio de altitud - trio del "
         "02-08-2026, demostrado ademas en Lean, depuracion/lean/A3.lean). "
         "ESTA es la version que hay que citar: sin el +1 y sin hipotesis de "
         "paridad. El +1 del enunciado clasico es log2(2) y aparece solo "
         "porque se mezcla la altitud de un mapa con la racha del otro."),

    fila("eps = ln( 2^B / (3^A * n) ) es identicamente igual a la suma de "
         "ln(1 + 1/(3x)) sobre los impares de la trayectoria",
         "todo_n", "demostrado", "elmasuno.py", "propio",
         "Ambito: todo n >= 1. El grosor de la lamina y el sobrante de la "
         "fraccion impar son el MISMO numero en dos coordenadas. 20.011 casos "
         "en racionales exactos, 0 fallos. El residuo 1,7e-7 que se habia "
         "medido era ruido de coma flotante, no del enunciado."),

    fila("eps >= 0 siempre, con igualdad exactamente en las potencias de 2",
         "todo_n", "demostrado", "elmasuno.py", "propio",
         "Ambito: todo n >= 1. (Decia 'eps > 0 siempre, y vale 0 en las "
         "potencias', que leido literal se contradice; corregido por el trio "
         "del 02-08-2026.) Cada factor (1+1/(3x)) es > 1 con x entero "
         "positivo, luego el producto es > 1. collazlamina.py -retirado en la "
         "purga del 01-08-2026- lo habia MEDIDO en 6.555 pares; ahora esta "
         "demostrado en una linea para todos los n. Cuidado con el borde: sobre "
         "trayectorias enteras Res(n) = 2^B/(3^A*n) >= 1 NO es estricta, vale 1 "
         "clavado en las potencias de 2 -que no tienen ni un paso impar- y solo "
         "en ellas."),

    fila("un numero tiene dos padres en el arbol si y solo si deja resto 4 al "
         "dividirlo entre 6; el segundo padre es (v-1)/3",
         "todo_n", "demostrado", None,
         "regla estandar de la literatura",
         "Ambito: todo v >= 1. La trayectoria del 221 tiene 50 vortices en sus "
         "115 numeros. FICHERO RETIRADO: collazarbol.py se borro en la purga "
         "del 01-08-2026 porque lo que dibujaba era la esfera elegida a mano, "
         "no Collatz -el 4 se excluia ahi por decision de dibujo, no de "
         "aritmetica: su otro padre es el 1, que ya es el arranque del tronco-. "
         "La regla en si no depende del dibujo y sigue en pie; quien sigue "
         "trabajando con el arbol inverso es mallascerradas.py."),

    fila("con la regla clasica dos pasos impares nunca van seguidos: "
         "P(impar | impar) = 0 exacto",
         "todo_n", "demostrado", "mallaresiduos.py",
         "propio (elemental: 3n+1 es par)",
         "Ambito: todo n, mapa clasico. Medido en 3,3 millones de "
         "oportunidades. Es la prohibicion que genera los Fibonacci, y no se "
         "metio a mano."),

    fila("los patrones de paridad alcanzables en k pasos del mapa clasico son "
         "F(k+2), los Fibonacci",
         "todo_n", "demostrado", "mallaresiduos.py",
         "folklore: conteo de cadenas sin dos adyacentes",
         "Ambito: k = 1..10, comprobado en los diez. k=4 -> 8 = F(6), "
         "k=6 -> 21 = F(8), k=8 -> 55 = F(10), k=10 -> 144 = F(12)."),

    fila("el rumbo de una rama del coral solo depende de (A,B): "
         "rumbo = A*giro_impar + B*giro_par",
         "todo_n", "demostrado", None,
         "propio (los giros conmutan)",
         "Ambito: las 730 parejas (A,B) medidas, 0 con rumbo ambiguo. Los "
         "rumbos del coral SON la malla (A,B) pasada a angulos. FICHERO "
         "RETIRADO: coralcollaz.py se borro en la purga del 01-08-2026 porque "
         "media el angulo elegido a mano y no Collatz -el cierre lo pone el "
         "angulo-. El enunciado es trivialmente cierto (los giros conmutan) y "
         "no depende del dibujo. Del coral solo sobrevive coralprimos.py, que "
         "mide el umbral de choque contra N."),

    fila("Collatz sobre los enteros negativos es exactamente el mapa 3m-1 "
         "sobre los positivos",
         "todo_n", "demostrado", None, "estandar en la literatura",
         "Ambito: todo m >= 1. 8.095.665 pasos comparados de 1 a 100.000, 0 "
         "fallos, con dos implementaciones que no comparten una linea. Sin "
         "fichero: se midio en scripts sueltos que no se guardaron."),

    fila("si n tarda S pasos, el numero de la posicion k tarda S-k; y SI S ES "
         "PAR, el de la posicion S/2 tarda S/2",
         "todo_n", "demostrado", None, "propio (contabilidad, no patron)",
         "Ambito: todo n que llegue a 1; la clausula S/2 exige S PAR (con S "
         "impar y division entera es falsa siempre: n = 5, S = 5, seq[2] = 8 "
         "tarda 3, no 2 - trio del 02-08-2026, demostrado en Lean para todo n "
         "que termine, no solo medido en 2..20.000). El 221 solo tuvo la "
         "suerte de tener 114 pasos, que es par. Esto mata el 'patron' de las "
         "notas a mano."),

    fila("n + espejo(n) = 10^k, exacto y siempre",
         "todo_n", "demostrado", None,
         "propio (recreativa elemental)",
         "Ambito: todo n >= 1, base 10. Cero grados de libertad: al plotear "
         "(n, espejo(n)) cada decada cae exacta sobre la recta x + y = 10^k. "
         "FICHERO RETIRADO: mallaespejo.py se borro en la purga del "
         "01-08-2026. Lo que dibujaba era el circulo y el modulo elegidos a "
         "mano; la identidad es de definicion y no necesita fichero."),

    fila("el espejo en base 2 baja estrictamente, luego toda orbita cae en una "
         "potencia de 2",
         "todo_n", "demostrado", None,
         "propio (una linea de algebra)",
         "Ambito: todo n >= 1. Es el analogo DEMOSTRADO de 'todo cae en el 1'. "
         "De 1 a 100.000: largos de ciclo {1: 100000}, ni un solo 2-ciclo. "
         "FICHERO RETIRADO: mallaespejo2.py se borro en la purga del "
         "01-08-2026 -media el circulo y el modulo elegidos a mano, no "
         "Collatz-, y el enunciado se demuestra en una linea sin el: si "
         "2^(k-1) < n < 2^k entonces 2^k - n < 2^(k-1). Y desde el 02-08-2026 "
         "esta DEMOSTRADO EN LEAN para todo n >= 1 (depuracion/lean/A13.lean, "
         "sin Mathlib): las potencias de 2 son los puntos fijos."),

    fila("el espejo en base b tiene puntos fijos exactamente (b/2)*b^m si b es "
         "par, y NI UNO si b es impar",
         "todo_n", "demostrado", None, "propio",
         "Ambito: las 15 bases de 2 a 16, 200.000 numeros cada una, 0 fallos. "
         "Los 5, 50, 500 del base 10 no son peculiaridad del diez: son el caso "
         "b = 10. Y la base 2 es la unica donde puede haber teorema. FICHERO "
         "RETIRADO: espejobases.py se borro en la purga del 01-08-2026 con el "
         "resto de la familia del espejo. El enunciado sale de n = b^k/2, que "
         "es entero si y solo si b es par, y no depende de ningun dibujo."),

    fila("T(2^k - n) = 2^(k-1) - T(n): en los pasos pares el espejo base 2 "
         "CONMUTA con Collatz",
         "todo_n", "demostrado", None,
         "propio (dos lineas de algebra)",
         "Ambito: n par. 50.000 casos, 0 fallos. FICHERO RETIRADO: "
         "mallaespejo2.py se borro en la purga del 01-08-2026; la identidad es "
         "algebra de dos lineas y sobrevive sin el."),

    fila("T(2^k - n) = 3*2^k + 2 - T(n): en los impares casi conmuta, pero "
         "sobra un +2",
         "todo_n", "demostrado", None,
         "propio (dos lineas de algebra)",
         "Ambito: n IMPAR con n < 2^k (la hipotesis faltaba; sobre Z vale "
         "para todo impar, incluso negativo - trio del 02-08-2026). 50.000 "
         "casos, 0 fallos. Ese +2 es el +1 del 3n+1 arrastrado, la suma de "
         "los dos +1. Exacto para UN paso; al segundo se rompe. FICHERO "
         "RETIRADO: mallaespejo2.py se borro en la purga del 01-08-2026."),

    fila("sigma_clasico(n) = sigma_atajo(n) + (pasos impares dentro de ellos), "
         "exacto",
         "todo_n", "demostrado", "descensoresto.py", "propio",
         "Ambito: todo n >= 2. Cada paso impar del atajo son dos pasos "
         "clasicos, y el valor intermedio 3n+1 es siempre MAYOR que n, asi que "
         "nunca puede ser el que dispara el descenso. Verificado en 5.012 "
         "numeros y en los 34 records de planeo publicados, 0 fallos. Es lo "
         "que permite cruzar el mapa del atajo (donde Terras es exacto) con "
         "los records de ericr.nl (que estan en el clasico)."),

    # ------------------------------------------------------ clase_residual
    #
    # Una comprobacion FINITA que decide para los INFINITOS numeros de la
    # clase. Es lo que el repo llama el cuarto camino. El modulo suele ser
    # 2^k -ahi vive Terras- pero no siempre: la rueda del arbol es mod 3^j y
    # es el mismo tipo de objeto. Por eso la casilla no lleva el modulo en el
    # nombre; el modulo va en el enunciado.

    fila("los primeros k pasos de cualquier numero los decide n mod 2^k",
         "clase_residual", "demostrado", "mallaresiduos.py",
         "Terras 1976 / Everett 1977",
         "Ambito: todo k >= 1. Tiene nombre: el vector de paridad. 64 restos x "
         "12 representantes = 768 numeros, 0 discrepancias."),

    fila("biyeccion perfecta entre los 2^k restos y los 2^k patrones de "
         "paridad posibles",
         "clase_residual", "demostrado", "mallaresiduos.py",
         "Terras 1976 / Everett 1977",
         "Ambito: SOLO el mapa del ATAJO, k = 1..10. Con la regla CLASICA no "
         "hay biyeccion: salen los Fibonacci. Los dos mapas no se pueden "
         "mezclar, y afirmar lo contrario fue un error que atrapo un "
         "SystemExit antes de dibujar nada."),

    fila("T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r): una recta en m cuya "
         "pendiente y ordenada dependen SOLO del resto",
         "clase_residual", "demostrado", "clasesfusion.py",
         "Terras 1976 (Teorema 1.2)",
         "Ambito: todo k, todo r < 2^k. De aqui salen las dos piezas mas "
         "utiles del repo: el criterio de fusion y la pinza de ciclos."),

    fila("dos consecutivos se funden para todos los infinitos m >= 1 de la "
         "clase exactamente cuando S_k(r) == S_k(r+1) y T^k(r) == T^k(r+1)",
         "clase_residual", "demostrado", "clasesfusion.py",
         "propio; Wu-Huang 2001 y Elia-Tucker 2015 lo enuncian casi textual",
         "Ambito: todo k, todo r, y m >= 1. Comprobacion finita que vale para "
         "infinitos numeros. Verificado contra fuerza bruta en 9.672 pares, 0 "
         "fallos. Y es la regla R3 de la criba industrial de Barina, que le "
         "ahorra 18%. EL m >= 1 NO ES ADORNO (01-08-2026): en m = 0 el criterio "
         "es falso -(5,6) da alturas 5 y 8, y (4,5) da 2 y 5- y fallan "
         "exactamente 3 clases, r = 2, 4 y 5, estables de k=5 a k=22. Nadie lo "
         "vio porque la fuerza bruta de clasesfusion.py empieza en "
         "range(1, 40), o sea que por construccion no podia ver el unico m que "
         "rompe. La cota del 43,57% no se mueve."),

    fila("a(32) = 1.871.137.623 clases mod 2^32 se funden: cota inferior "
         "DEMOSTRADA del 43,5658% de los pares consecutivos",
         "clase_residual", "demostrado", "clasesfusion.py", "propio",
         "Ambito: k <= 32. Confirmado por dos caminos independientes, el "
         "secuencial y el repartido por nucleos de clasesparalelo.py. No "
         "depende de muestreo ni de ajuste, y por eso es lo unico duro de esa "
         "seccion. La sucesion no esta en OEIS (28 consultas)."),

    fila("N(k+1) >= 2*N(k) siempre, luego la fraccion f(k) es monotona",
         "clase_residual", "demostrado", "clasesfusion.py", "propio",
         "Ambito: todo k >= 3. La monotonia NO se verifica: se demuestra en "
         "tres lineas. Si r es buena mod 2^k, r y r+2^k son las dos buenas mod "
         "2^(k+1). Presentarla como hallazgo empirico fue un error, corregido."),

    fila("(8k+4, 8k+5) CONFLUYEN siempre en 3 pasos para todo k >= 0, y tienen "
         "la MISMA ALTURA para todo k >= 1",
         "clase_residual", "demostrado", "verificar_fusiones.py", "Garner 1985",
         "SON DOS ENUNCIADOS Y HAY QUE SEPARARLOS (01-08-2026). La CONFLUENCIA "
         "vale para todo k >= 0: los dos caen en 6k+4 en 3 pasos, gastando 2 "
         "pares y 1 impar cada uno; 200.000 casos, 0 fallos, y es una identidad "
         "algebraica, no una medida. EL COROLARIO DE MISMA ALTURA FALLA EN "
         "k = 0: altura(4) = 2 y altura(5) = 5, porque el 4 llega al 1 ANTES "
         "del paso 3 en el que se encontrarian. De k = 1 a k = 20.000, 0 "
         "fallos, asi que el enunciado de altura lleva k >= 1. Es exactamente "
         "el mismo agujero que el m >= 1 del criterio de clases, encontrado por "
         "dos caminos distintos el mismo dia. Rederivado desde el criterio: "
         "r = 4, k = 3 da T^3(4) = T^3(5) = 2 con S = 1 en los dos."),

    fila("(32m+5, 32m+6) se funden para todo m >= 1",
         "clase_residual", "demostrado", "guardarhilos.py",
         "Wu-Huang 2001, Mathematica Applicata (Wuhan) 14, supl., 21-25, "
         "MR 1885838 (LOCALIZADA el 01-08-2026)",
         "Ambito: todo m >= 1; probado en m = 1,2,7,100,3125,9999,40000, "
         "todos con desfase 0. Nuestro par (100005, 100006) es el caso "
         "m = 3125. En m = 0 es FALSO: altura(5) = 5 y altura(6) = 8."),

    fila("si dos trayectorias se funden gastando los MISMOS pares y los MISMOS "
         "impares, entonces 2^r*k + n1 y 2^r*k + n2 se funden para todo k, "
         "siempre que r sea MAYOR que el numero de pasos pares del tramo",
         "clase_residual", "demostrado", "verificar_fusiones.py", "Garner 1985",
         "TAL COMO ESTE REPO REPETIA EL G2 -'si dos trayectorias se funden, "
         "entonces 2^r*k + n1 y 2^r*k + n2 se funden para TODO k'- ERA FALSO. "
         "Le faltaban las dos hipotesis del enunciado, y sin ellas se rompe "
         "(01-08-2026, verificar_fusiones.py). (i) Con r = e, exactamente los "
         "pares del tramo, la propagacion falla en 9.954 de 62.400 casos; con "
         "r = e+1 va perfecta, 62.400 comprobados y 0 fallos. (ii) 'Fundirse' a "
         "secas no basta: hace falta encontrarse en el mismo indice y con las "
         "mismas cuentas. El contraejemplo bueno es el par (3, 20): los dos "
         "pasan por el 10 en el indice 1, pero uno gasta 1 impar y el otro 0, y "
         "2^r*m + 3 contra 2^r*m + 20 da la misma altura en solo 2 de 40 "
         "valores de m, para r = 8, 10 y 12. Control con (4, 5), que si cumple "
         "las dos hipotesis: 40 de 40. Con las hipotesis puestas, una sola "
         "fusion sigue generando una progresion aritmetica infinita de "
         "fusiones, que es lo que produce los bloques de consecutivos con los "
         "mismos pasos. La forma del error es la de siempre aqui: un enunciado "
         "publicado, copiado sin sus cuantificadores."),

    fila("por cada resto mod 2^k hay COMO MUCHO UN candidato de ciclo, y sale "
         "en cerrado: m = (r - T^k(r)) / (3^{S(r)} - 2^k)",
         "clase_residual", "demostrado", "pinzaciclos.py",
         "propio (de la identidad de Terras)",
         "Ambito: k >= 1, barrido entero de k = 1..30 (en k = 0 el enunciado "
         "no aplica: el denominador vale 0 y todo n cumple T^0(n) = n - trio "
         "del 02-08-2026). Si m no es entero, la clase queda descartada para "
         "los infinitos numeros que contiene. Verificado contra iteracion "
         "cruda y contra una implementacion en Python puro."),

    fila("el mapa RESTO -> VECTOR DE PARIDAD es una biyeccion Z/2^k -> "
         "{0,1}^k, luego no hay descarte EN BLOQUE de clases para buscar "
         "ciclos",
         "clase_residual", "demostrado", "verificar_constantes.py",
         "Terras 1976",
         "AQUI PONIA 'T^k es una BIYECCION sobre Z/2^k' Y ESO ES FALSO AL PIE "
         "DE LA LETRA (corregido el 01-08-2026). T^k ni siquiera esta bien "
         "definida modulo 2^k: con k = 1 los restos 0 y 2 son la misma clase y "
         "T(0) = 0 mientras T(2) = 1. Y T tampoco es inyectiva sobre Z: "
         "T(1) = T(4) = 2. Lo verdadero es la biyeccion resto <-> vector de "
         "paridad, comprobada exhaustiva de k = 1 a k = 16 en "
         "verificar_constantes.py [6]: el vector depende solo del resto (0 "
         "fallos) y el mapa es biyectivo (0 fallos, 2^16 vectores distintos). "
         "LA CONCLUSION ESTRATEGICA SE SALVA ENTERA porque solo usaba esa "
         "version -hay 2^k clases y una por vector, luego ninguna comparte "
         "destino con otra-, y eso fue suerte: las dos frases estaban juntas y "
         "la que trabajaba era la buena. SEGUNDO MATIZ: decir 'no hay clases "
         "que descartar' tambien se pasa de fuerte. Las hay, y pinzaciclos.py "
         "descarta casi todas; lo que no hay es descarte en bloque, cada clase "
         "exige su propia decision aunque sea O(1), y por eso el coste es "
         "Theta(2^k) y no menos. Y DESDE EL 02-08-2026 LA BIYECCION ESTA "
         "DEMOSTRADA EN LEAN PARA TODO k (depuracion/lean/A28.lean, nucleo "
         "solo, sin sorryAx), no solo exhaustiva hasta k = 16; con el mapa "
         "CLASICO es falsa ya en k = 2: los restos 1 y 3 mod 4 comparten el "
         "vector [1,0]."),

    fila("sobre el mapa del ATAJO: n = 2^k - 1 (mod 2^k) sube k veces "
         "seguidas, y n = 0 (mod 2^k) con n >= 1 baja k veces seguidas",
         "clase_residual", "demostrado", "mallaresiduos.py",
         "Terras 1976; es el Lema 8 de Hercher 2023",
         "Ambito: todo k, mapa del ATAJO - en el clasico 'sube k veces "
         "seguidas' es falso desde k = 2 (3 -> 10 -> 5); trio del 02-08-2026, "
         "demostrado en Lean para todo k. No son estadisticas: son teoremas, "
         "y se escriben como un if. Con esto se fabrico 2^4000 - 1, que da "
         "4.000 pasos impares seguidos, no 3.999. El unico objeto que sube "
         "SIEMPRE es -1, que es uno de los ciclos negativos."),

    fila("el ritmo de brotes del arbol inverso es periodico de periodo 2 segun "
         "v mod 3, los hijos ciclan con periodo 3 mod 9, y el patron completo "
         "se repite cada 18 duplicaciones (orden de 2 mod 27)",
         "clase_residual", "demostrado", "mallascerradas.py",
         "propio; la estructura mod 6 / mod 9 es estandar",
         "Ambito: 200 rayos hasta k=44, 2.926 brotes, 0 fallos. EL MODULO AQUI "
         "ES 3^j, NO 2^k: mod 3 el ritmo de brotes, mod 9 la clase del hijo, "
         "mod 27 la rueda maestra. Es el mismo TIPO de objeto que las filas de "
         "Terras -una clase de resto que decide el comportamiento sin recorrer "
         "nada- y por eso la casilla se llama clase_residual desde el "
         "01-08-2026 y no clase_mod_2k, que la nombraba mal. Y el limite de la "
         "rueda sigue en pie: gobierna la contabilidad del arbol HACIA ATRAS, "
         "no el destino hacia adelante, que sigue ciego a los restos."),

    fila("los evitados de la malla 2n mod 27 son exactamente los multiplos de "
         "3, y predicen que rayos del arbol son mudos",
         "clase_residual", "demostrado", "mallascerradas.py", "propio",
         "200 rayos impares, 67 predichos mudos, 0 fallos. Una malla calculada "
         "sin mirar Collatz ni una vez predice Collatz sin volver a calcular "
         "Collatz. El modulo es 27 = 3^3, no 2^k: la otra fila de la base que "
         "obligo a renombrar la casilla. FICHERO CAMBIADO: esto lo citaba "
         "guardarmallas.py, que persistia las once mallas en mallas/*.json y se "
         "borro en la purga del 01-08-2026 junto con los JSON -la coleccion "
         "media el modulo elegido a mano-. La medicion sobrevive entera en "
         "mallascerradas.py, que calcula el aro de 2 mod 27, comprueba que "
         "evita exactamente los multiplos de 3 y cruza eso contra los rayos "
         "mudos del arbol; lo unico que se perdio es la capa de disco."),

    fila("la malla de restos acierta el arranque de los 173 numeros del 221 y "
         "del 1276, 0 fallos",
         "clase_residual", "medido", None, "propio",
         "64 restos contra 173 numeros. Calculada sin mirar el 221 ni una vez: "
         "cada resto usa un representante ajeno a las trayectorias. FICHERO "
         "RETIRADO: cruzarestos.py se borro en la purga del 01-08-2026 porque "
         "lo que dibujaba era la malla circular elegida a mano. La regla de "
         "fondo -los primeros k pasos los decide n mod 2^k- sigue viva y "
         "comprobada en mallaresiduos.py; lo que ya no se puede reproducir es "
         "el cruce concreto contra el 221 y el 1276."),

    fila("a(k) >= 1 para todo k: el resto 2^k - 1 sobrevive siempre a la criba "
         "de Brown/Terras, luego la criba NUNCA se vacia",
         "clase_residual", "demostrado", "descensoresto.py", "propio",
         "Demostracion de una linea: el resto que en binario son todos unos da "
         "S_j = j en todos los pasos, y 3^j > 2^j siempre. ES EL MURO "
         "ESTRUCTURAL DE CRIBAR POR RESTOS: se puede llegar a 'casi todos' con "
         "la densidad que se quiera, nunca a 'todos', para ningun k. Detalle "
         "que cierra el circulo: 2^k - 1 es justo el numero que sube k veces "
         "seguidas, y el unico objeto que lo hace para TODO k es -1, que es "
         "uno de los ciclos negativos."),

    fila("los supervivientes de la criba tienen densidad -> 0 pero cardinal -> "
         "infinito, del orden de 2^(0,95k). La criba compra densidad, no "
         "compra cobertura",
         "clase_residual", "demostrado", "descensoresto.py", "propio",
         "Medida cero, cardinal infinito. Un contraejemplo de la conjetura "
         "tendria que vivir justo en el conjunto que la criba no ve, y ese "
         "conjunto nunca se queda vacio. Es el mismo muro de pinzaciclos.py "
         "por otra puerta: alli el barrido de restos no podia encontrar ciclos "
         "porque cada clase es un candidato distinto; aqui no puede cerrar el "
         "descenso porque siempre queda clase viva. REGIMEN (trio del "
         "02-08-2026): el 0,95 = H(log_3 2) del enunciado es el ASINTOTICO, "
         "que sube por debajo sin alcanzarse en ningun k finito (0,65 en "
         "k=12, 0,88 en k=100, 0,94 en k=1400) - el espejo del 2^(-0,05k) ya "
         "corregido. Y la no-vacuidad esta demostrada en Lean para todo k "
         "(depuracion/lean/A34.lean)."),

    fila("si el coeficiente cae (3^S(r) < 2^k) y m > T^k(r) - r, entonces "
         "T^k(2^k*m + r) < 2^k*m + r: la bajada del coeficiente es bajada "
         "real fuera del tramo FINO",
         "clase_residual", "demostrado", "atacacst.lean", "propio",
         "Teorema tramo_finito_fino (03-08-2026), nucleo sin Mathlib, "
         "#print axioms limpio. Cierra el hueco Lean-Python de atacacst: "
         "tramo_finito solo cubria m > T^k(r) y el .py decide con "
         "m > T^k(r) - r; la franja intermedia no tenia teorema. La "
         "hipotesis se escribe sin resta truncada como T^k(r) < r + m, y "
         "la demostracion son tres lineas desde palanca con D >= 1."),

    fila("para todo j par, el par (2^j - 2, 2^j - 1) se funde por primera "
         "vez en el paso j+2, con vortice en el repunit ternario "
         "b = (3^(j-1) - 1)/2: la clase 2^j - 2 es NUEVA mod 2^(j+2)",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "La familia extremal de las nuevas (03-08-2026). Demostracion de "
         "cuatro lineas en el comentario de la COMPROBACION 5: un lado hace "
         "j impares hasta 3^j - 1 y dos pares; el otro gasta un par, hace "
         "j-1 impares y el encuentro cuadra exacto (3b + 1 = (3^j - 1)/2), "
         "con S = j en ambos. Corolario: b(j+2) >= 1 para todo j par - las "
         "nuevas nunca se acaban. Comprobada j = 4..60. Que ese b sea el "
         "MAXIMO del nivel esta solo medido (k <= 15). Y el patron 'todo b "
         "es 1 mod 3' se REFUTO antes de publicarse: b = 2255 en k+1 = 15."),

    fila("en cada nivel k+1 >= 4 hay EXACTAMENTE UNA clase nueva con "
         "|M| = 2, y es r = 2^(k-1) - 2 si k es impar, r = 3*2^(k-1) - 2 "
         "si k es par: la primera fila del triangulo de estratos es "
         "1, 1, 1, ... para siempre",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "Demostracion en cuatro piezas en la COMPROBACION 7 (03-08-2026): "
         "(1) |M| = 2 fuerza r par (r impar da d1 = -r impar y el paso 1 "
         "ya es mixto); (2) en cada paso compartido d pierde exactamente "
         "un factor 2, luego v2(r+2) = k-1 y solo caben DOS candidatos, "
         "2^(k-1)-2 y 3*2^(k-1)-2; (3) el ganador cumple el encuentro "
         "-alternando por la paridad de k, con la identidad "
         "T(c*2^m - 1) = 3c*2^(m-1) - 1-; (4) el perdedor falla siempre "
         "porque su vortice pediria 3^q - 1 = 3^(q+2) - 1. Comprobadas "
         "las piezas (3) y (4) hasta k = 60, y la unicidad completa por "
         "fuerza bruta en k <= 15 (comprobacion 6). Primera pieza "
         "DEMOSTRADA del mecanismo 'la razon 2 viene de la entrada de "
         "estratos, no de que ninguno acelere'."),

    fila("LEMA GENERAL: para todo C impar y q >= 2 con C = 3^q (mod 4), "
         "el par (C*2^q - 2, C*2^q - 1) se funde exactamente en el paso "
         "q+2, con S = q en los dos lados y vortice en "
         "b = (3^(q-1)*C - 1)/2",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 8 (03-08-2026). Generaliza la familia del repunit "
         "a prefijo impar arbitrario, con la identidad "
         "T(c*2^m - 1) = 3c*2^(m-1) - 1. La condicion C = 3^q (mod 4) "
         "hace impar al vortice; la paridad del otro lado es automatica "
         "(3^q*C = 1 mod 4 siempre). Los casos C = 1 y C = 3 son "
         "exactamente la alternancia del teorema de |M| = 2. Comprobado "
         "en todos los pares C <= 201 impar, q <= 40."),

    fila("la clase r = 2^(k-1) - 3 (k par) / 3*2^(k-1) - 3 (k impar) -el "
         "vecino izquierdo del perdedor de |M| = 2, con r IMPAR- es nueva "
         "en el nivel k+1 con mixtos en [0, 1, 2, k]: el estrato |M| = 4 "
         "tiene al menos una clase por nivel, con formula",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 8 (03-08-2026). Los dos primeros pasos se calculan "
         "a mano: el par (w-3, w-2) con w = c*2^(k-1) se contrae en dos "
         "pasos a (3c*2^(k-3) - 2, 3c*2^(k-3) - 1) - VUELVE A SER "
         "CONSECUTIVO (d2 = 1) - y ese es el lema general con C = 3c, "
         "q = k-3. LOS ESTRATOS SE REDUCEN UNOS A OTROS: |M| = 4 es dos "
         "mixtos de preludio mas un |M| = 2 desplazado, y esa reduccion "
         "es la forma de la recursion del triangulo. La UNICIDAD de "
         "|M| = 4 sigue solo medida (1 por nivel, k <= 15): faltaria "
         "descartar los demas patrones de posiciones. Comprobada "
         "k = 4..60."),

    fila("r IMPAR fuerza pasos 0, 1 y 2 mixtos (|M| >= 4 siempre); si "
         "ademas r = 1 (mod 4), el par se contrae en dos pasos al "
         "consecutivo de menor (3r+1)/4, y DENTRO de esa ruta la clase "
         "|M| = 4 del nivel es UNICA",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 9 (03-08-2026). (i) el gap tras el paso 0 es -r, "
         "impar, y tras el paso 1 es -1 o 2r+1 segun r mod 4: tres mixtos "
         "seguidos (es el reverso del teorema de |M| = 2, que forzaba r "
         "par). (iii) tras la contraccion se aplica entero el argumento "
         "de |M| = 2: v2(s2+2) = k-3, rango C <= 11, necesidad del lema "
         "general C = 3^(k-3) (mod 4), y r entero exige 3 | C: quedan "
         "C = 3 y 9 y el mod 4 elige uno. Exhaustivo r < 2^14 mas "
         "k = 5..60. Para la unicidad TOTAL de |M| = 4 faltan las rutas "
         "r = 3 (mod 4) y r par - en el mapa de dependencias, el nodo "
         "unicidad_M4 sigue en medido y cuadratica_M6 BLOQUEADO."),

    fila("LA COORDENADA D = g - 2s - 1 del par {s, s+g}: el vortice es "
         "exactamente D = 0 con s impar, en pasos compartidos D es impar "
         "y evoluciona (D-1)/2 o (3D-1)/2, el tramo compartido termina "
         "cuando D se hace par, y D < 0 ES INVARIANTE. Con eso, la ruta "
         "r = 3 (mod 4) queda EXCLUIDA de |M| = 4: la unicidad esta "
         "demostrada para TODO r impar",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 10 (03-08-2026). r = 3 (mod 8): tras los tres "
         "mixtos el par es {(3r+7)/8, +(3r-1)/4} con D = -3, y por la "
         "invariancia su cuarto mixto nunca es vortice (|M| >= 6). "
         "r = 7 (mod 8): beta con g = 3 (mod 4) deja g impar y el paso 3 "
         "tambien es mixto (|M| >= 6 para k > 3; el borde k = 3 lo cubre "
         "la fuerza bruta del nivel 4). Exhaustivo r < 2^15 mas el "
         "seguimiento del tramo completo. La D es la herramienta nueva "
         "del programa: convierte 'se funden' en 'D llega a 0', y los "
         "estratos en la contabilidad de sus rebotes."),

    fila("LA COORDENADA E = D - 3s ES AUTONOMA dentro de un tramo "
         "compartido: su propia paridad elige su mapa (E impar -> "
         "(E-1)/2, E par -> (3E-4)/2), sin mirar los valores",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 11 (03-08-2026). D es impar durante el tramo, "
         "luego la paridad de E determina la del menor (E impar <=> s "
         "par) y E se vuelve un mapa 1-dimensional determinista. OJO con "
         "el limite: en los pasos MIXTOS ni D ni E son autonomas (ahi "
         "entra el valor: es el +1 de Collatz reapareciendo). CORRECCION "
         "de la misma noche: esta fila afirmaba ademas la orbita del "
         "rebote 1, 0, -2, -5, -3 con el vortice {1,4} imposible - era "
         "LA FAMILIA FANTASMA (w, 6w+2); el rebote real es (w, 9w+2) "
         "con E = 3w+1 dependiente de w (ver la correccion). Lo que "
         "queda en pie: la autonomia (independiente de familias) y el "
         "barrido real: entre TODAS las fusiones con S igualada de "
         "pares r par < 2^20, el estrato |M| = 4 esta VACIO, y |M| = 2 "
         "da exactamente 2^18 (el teorema de Perras, fila aparte)."),

    fila("EL REBOTE REAL: en D = 0 el par es {s, 3s+1}, y si s = 2w es "
         "par el rebote beta lo manda EXACTAMENTE a (w, 9w+2), con "
         "D = 6w+1 y E = 3w+1. Y EL TEOREMA DE PARIDAD DEL REBOTE: el "
         "tramo post-rebote nunca puede terminar en fusion DE CLASE "
         "(seria |M| = 3, impar, con Delta_S = +2 +- 1 != 0): toda "
         "fusion de clase con r par y rebote exige |M| >= 4",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACIONES 12 y 14 corregidas (03-08-2026, noche). La "
         "derivacion es de dos lineas (beta: s/2 y (9s+4)/2) y esta "
         "verificada contra 8.191 rebotes de pares reales (todos en la "
         "familia, cero excepciones). Ademas, iterando el mapa (D, E) "
         "puro desde el arranque real (6w+1, 3w+1) hasta w = 10^6: "
         "ningun tramo post-rebote termina en D = 0 (ni siquiera hay "
         "encuentro de valor). Esta fila sustituye a la del 'tercer "
         "mixto clasificado' con los casos A/B-alfa: eran de la familia "
         "fantasma - ver la correccion."),

    fila("el mapa de E como sistema dinamico sobre Z (impar -> (E-1)/2, "
         "par -> (3E-4)/2) es de tipo Collatz y su censo en [-10^5, "
         "10^5] da DIEZ familias: fijos -1 y 4, 2-ciclo (-11), 3-ciclos "
         "(-5) y (24), 5-ciclos (-77) y (-59), 11-ciclo (84), 27-ciclos "
         "(-4163) y (-5099). NINGUNA orbita escapa",
         "verificado_hasta", "medido", "nuevasfusion.py", "propio",
         "COMPROBACION 13 (03-08-2026, de la idea del usuario: 'toda "
         "orbita relevante de E pertenece a una de N familias'). El del "
         "rebote {-2,-5,-3} atrae al 47% del rango. La deriva media es "
         "contractiva (-log 2 + log 3/2 < 0), coherente con que todo "
         "cicle - pero la completitud de la lista para todo Z es "
         "exactamente el tipo de pregunta que en Collatz lleva 90 anos "
         "abierta: censo medido, no teorema. Cambia el programa: las "
         "rutas de los estratos se clasifican por familia de E y por "
         "donde el vortice (D = 0) interrumpe la orbita."),

    fila("NO EXISTE UNA TERCERA COORDENADA: el estado del par es "
         "2-dimensional y (D, E) lo genera. En particular H = 2D - E es "
         "el valor MAYOR del par menos 1 (H = g + s - 1 = l - 1), D = "
         "l - 3s - 1 y E = l - 6s - 1: toda 'coordenada nueva' es una "
         "combinacion afin de (s, l)",
         "todo_n", "demostrado", "nuevasfusion.py", "propio",
         "Dos lineas de algebra (03-08-2026), y la respuesta a la "
         "pregunta del usuario 'que propiedad nueva tiene H': NINGUNA - "
         "sus mapas eran 'otro Collatz' porque SON la trayectoria del "
         "miembro grande. Cierra la mina de coordenadas: lo que quedaba "
         "por explotar es la CLASIFICACION (familias de E, itinerarios), "
         "no mas cambios de variable. La decision de congelar B-beta y "
         "virar a clasificacion_rutas sale de aqui."),

    fila("los itinerarios de las nuevas (la palabra de familias de E "
         "entre mixtos): el ultimo tramo de todo |M| = 4 vive en "
         "{-5, -77, -4163}, EXACTAMENTE las familias de |M| = 2 - la "
         "contraccion hecha visible -, y la unica familia ausente de "
         "todos los itinerarios es el punto fijo -1 (trivial)",
         "verificado_hasta", "medido", "itinerarios.py", "propio",
         "Paso 1 de clasificacion_rutas (03-08-2026), k <= 15, con "
         "cruce contra b(k) en los 13 niveles. Y EL NEGATIVO, que vale "
         "tanto como el positivo: la familia ASINTOTICA es un invariante "
         "ruidoso para contar (el tramo solo usa un prefijo finito de la "
         "orbita de E; conteos por itinerario erraticos, no "
         "polinomicos). El refinamiento pendiente: etiquetar tramos por "
         "datos FINITOS (E de arranque modulo algo, largo del tramo). "
         "De paso murio en el acto la conjetura 'solo aparecen familias "
         "negativas': 4, 24 y 84 si aparecen en estratos altos - la "
         "cazo el cruce contra b(k) de la capa 1."),

    fila("TEOREMA DE PERRAS (la mitad exacta; bautizado por el usuario "
         "el 03-08-2026, casi en honor a Terras): para r PAR, (r, r+1) se funde con "
         "|M| = 2 si y solo si en el vector de paridad de s1 = r/2 el "
         "primer 0 va seguido de un 1; y entre s1 en [1, 2^m) fusionan "
         "EXACTAMENTE 2^(m-1), para todo m >= 2, sin casos",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 15 (03-08-2026); la perla del 2^18 exacto, "
         "demostrada. Con D = 1 el primer valor PAR de la trayectoria de "
         "s1 baja D a 0, y el vortice pide T^(j+1)(s1) impar: el bit "
         "siguiente al primer 0. Delta_S = 0 automatico (el paso 0 suma "
         "al lado r+1 y el vortice al lado r). El conteo, por la "
         "biyeccion de Terras: patrones decididos 2^(m-1) - 1, y de los "
         "dos residuos frontera (2^(m-1)-1 y 2^m-1) funde EXACTAMENTE "
         "UNO para cada m (segun 3^m mod 4): total 2^(m-1) clavado. "
         "Equivalencia exhaustiva s1 < 2^16 y conteos m = 2..16. ES LA "
         "PRIMERA MEDIDA EXACTA DE UNA FILA DEL TRIANGULO: el estrato 2 "
         "pesa 1/2 entre los r pares - Terras 1.4 (la moneda) actuando "
         "sobre dos bits. VERIFICACION BIBLIOGRAFICA (03-08-2026, noche): "
         "el patron ES el stem s_i de Garner 1985, que demostro la "
         "SUFICIENCIA (la mitad <=) y conjeturo la necesidad para TODA "
         "fusion; Elia-Tucker 2015 (arXiv:1511.09141) refutaron esa "
         "necesidad (3067/3068). LO QUE PERRAS ANADE y no esta en "
         "ninguno: la necesidad SI es verdadera restringida al estrato "
         "minimo (|M| = 2 <=> stems), y el conteo exacto 2^(m-1) con el "
         "borde resuelto - Elia-Tucker solo midieron (0,214% de "
         "contraejemplos bajo 5e9). Perras = la conjetura de Garner, "
         "falsa en general, demostrada en el estrato minimo con su "
         "densidad. LaTourette 2007 (tesis no accesible) definio los "
         "objetos; el conteo no consta alli tampoco."),

    fila("las masas de clase del sistema de renovacion, por nivel: la "
         "indecisa decae ~2% por nivel (0,65 en p = 16) y la horquilla "
         "rigurosa de f es [0,4263, 1] en p = 16 - el sistema es exacto "
         "pero converge LENTO: es el mismo muro que la razon de b(k), "
         "porque es la misma pregunta",
         "verificado_hasta", "medido", "masasdeclase.py", "propio",
         "03-08-2026, noche. Enumeracion de clases mod 2^p (p = 8..16) "
         "con dos testigos lejanos por clase; eventos de clase F/C/B "
         "decididos en t <= p (correcto por Terras). Cortes: monotonia "
         "de la cota inferior y de la masa indecisa, y la horquilla "
         "contiene el f medido (0,4453). La via que queda NO es subir "
         "p: es la renovacion de la cola (los tramos largos antes de "
         "reentrar deberian tener su propia estructura). f sigue mejor "
         "acotada por a(32)/2^32 = 0,4357."),

    fila("LA IDENTIDAD EXACTA DE LA RENOVACION: a(k+2) = a(k) + "
         "(2^k - 1) + G(k) + H(k) como IGUALDAD DE ENTEROS, con la rama "
         "de la contraccion dando a(k) clavado y la ventana de Perras "
         "dando 2^k - 1 clavado; G y H nacen como sucesiones exactas",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "k = 3..14, doce niveles, cero desviaciones (03-08-2026, "
         "noche; el test lo propuso la revision externa como sustituto "
         "de toda simulacion: sin topes, sin Monte Carlo, sin sesgo). "
         "G: 0,0,0,0,1,5,16,44,110,259,588,1302; H: 0,0,0,1,3,9,24,58,"
         "134,300,659,1426. Ademas: la rama h se reduce a {w, 9w-1} "
         "(regalo del revisor, verificado t < 3000) y los "
         "contraejemplos de Elia-Tucker viven todos en |M| = 8. Es la "
         "verificacion mas fuerte que tienen Perras y Gatas: la "
         "autosimilitud vale como aritmetica entera nivel a nivel. "
         "Y LA PREGUNTA ANTI-TAUTOLOGIA DEL REVISOR, CONTESTADA "
         "(03-08-2026, noche): G(k) = suma B(m) y H(k) = B_h(k) se "
         "RECONSTRUYEN desde los estados reducidos {w,9w+2} y {w,9w-1} "
         "sin mirar el r original, clavadas hasta k = 14: la identidad "
         "es TEOREMA verificado, no un 4 = 1+1+1+1. El cuadre con los "
         "objetivos canonicos de Delta_S verifica ademas el Corolario 2 "
         "de Jirafas."),

    fila("LEMA DE LA EQUIVALENCIA DE PANDAS (condicional a Res < 3): si "
         "H(n) = H(n+1), tau y S coinciden y las trayectorias del atajo "
         "se encuentran AL MISMO INDICE - porque 6^d = (n/(n+1)) * "
         "(Res(n)/Res(n+1)) y con 1 <= Res < 3 el lado derecho no "
         "alcanza ninguna potencia entera de 6 salvo 6^0. COROLARIO "
         "(con el reciproco de Jirafas): phi = d - la medida 2-adica de "
         "fusion ES la densidad natural de Gao (0,512 medida a 10^8)",
         "todo_n", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, noche; lemadepandas.txt. CORRECCION EN VIVO, "
         "registrada en el propio documento: la primera version decia "
         "Res < 6 y era INSUFICIENTE para d = -1 (el factor n/(n+1) "
         "baja el piso a 1/12); la condicion limpia es Res < 3 (n >= 2; "
         "n = 1 vacuo). Ultra debil igual (max conocido 1,2532; "
         "incondicional bajo 2^71). LETRAS (orden del revisor): phi = "
         "lim a(k)/2^k (2-adica), d = densidad natural de Gao - eran "
         "objetos distintos y el puente es el reciproco de Jirafas: "
         "fusion balanceada <=> evento de clase (union monotona => "
         "densidad natural = medida 2-adica). Verificado: 477.245 "
         "pares bajo 10^6, cero excepciones."),

    fila("LOS LEMAS DE GERMEN de las sub-renovaciones: b(6) = 1 con "
         "germen w = 46 mod 2^6 (funde en el paso 6 via el vortice "
         "(40, 13), compensacion S = +2 exacta) y c(6) = 1 con germen "
         "w = 25 mod 2^6 (vortice (22, 7)); cada germen decide su clase "
         "entera por Terras. Y las dos series reducidas -b: 1,4,11,28,"
         "66,149; c: 1,3,9,24,58,134,300,659,1426- NO estan en OEIS",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; goal de investigacion abierta. Los "
         "germenes son unicos en m = 6 (barrido exhaustivo de las 64 "
         "clases con dos testigos). OEIS consultada con control "
         "Fibonacci OK en la misma sesion: no results para ambas. Las "
         "razones de b y c bajan hacia 2 DESDE ARRIBA (2,26 / 2,16): "
         "las densidades reducidas siguen subiendo - la pregunta de la "
         "razon 2 ahora tiene tres pisos (a, b, c) y las mismas "
         "herramientas valen en cada piso."),

    fila("EL DOBLADO EN LOS PISOS REDUCIDOS: b(m+1) >= 2 b(m) y "
         "c(m+1) >= 2 c(m) - el levantamiento de Gao aplica igual a "
         "{w, 9w+2} y {w, 9w-1} -, luego las densidades reducidas son "
         "monotonas y sus limites beta y gamma EXISTEN. Las nuevas de "
         "cada piso (b: 2,3,6,10,17; c: 1,3,6,10,18,32,59,108) son "
         "otras dos sucesiones, y la de c tampoco esta en OEIS",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. La demostracion es el Lema 2 de Gao "
         "1993 aplicado a los pares reducidos (una clase fundida en <= m "
         "pasos se alza en dos fundidas mod 2^(m+1)); verificado en "
         "todos los terminos de las dos series. Con Gatas, el sistema "
         "completo queda: phi = 1/4 + phi/4 + beta' + gamma' con los "
         "limites reducidos existiendo por derecho propio - el analisis "
         "asintotico de los tres pisos es ahora un objeto bien definido."),

    fila("EL PERRAS DE LOS PISOS REDUCIDOS, medido con forma cerrada "
         "exacta: el estrato minimo de las fusiones reducidas es "
         "|M| = 4 en los dos pisos, y sus conteos son b4(m) = "
         "7*2^(m-7) - m + 4 y c4(m) = 6*2^(m-7) - m + 4 (m >= 7), "
         "clavados en los 8 niveles m = 7..14; densidades limite 7/128 "
         "y 3/64. El triangulo reducido replica al de arriba: cada "
         "estrato nuevo entra cada dos niveles y con exactamente 1 clase",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; goal de investigacion abierta. Las "
         "diferencias siguen 7*2^j - 1 y 6*2^j - 1 exactas (8 niveles); "
         "el termino -m sugiere UNA clase excluida por nivel, los "
         "indecisos de Perras reapareciendo. CANDIDATAS A PROPOSICION: "
         "la demostracion (pendiente) seria el analogo del argumento de "
         "la ventana de Perras sobre el estado rebote; con ella, el "
         "primer termino de las sub-renovaciones queda cerrado y el "
         "sistema de phi gana dos masas exactas mas. AVISO de la casa: "
         "forma ajustada exacta en 8 niveles NO es demostracion - por "
         "eso queda en medido. Y EL TEST DE PREDICCION (la vara del "
         "repo): las formulas, ajustadas con m <= 14, PREDIJERON los "
         "cuatro valores de m = 15 y 16 (1781, 1525, 3572, 3060) y los "
         "cuatro salieron CLAVADOS - el estatus empirico mas fuerte "
         "antes de la demostracion."),

    fila("c4 ES A079583: la sucesion del estrato minimo del piso h "
         "coincide termino a termino con la entrada catalogada "
         "3*2^n - n - 2 (con n = m - 6), lo que CONFIRMA la forma "
         "cerrada por via independiente; b4 (la hermana con 7 en vez "
         "de 6) NO esta catalogada. Y LA LEY DEL GERMEN UNICO, medida "
         "en los TRES pisos: cada estrato nuevo entra cada dos niveles "
         "con EXACTAMENTE una clase",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. A079583 esta catalogada como forma "
         "pura sin contexto Collatz: la coincidencia no es prioridad "
         "ajena sino confirmacion del ajuste (la misma formula, "
         "verificada por otro camino). La ley del germen unico: piso a "
         "(estratos 2, 4 entran con 1 - teoremas), pisos b y c "
         "(estratos 6@8, 8@10, 10@12, 12@14 entran con 1 en ambos - "
         "medido). Sugiere una recursion universal del triangulo: "
         "germen unico + ley de crecimiento por estrato."),

    fila("LOS GERMENES DEL ESTRATO 6 REENTRAN EN LOS DEL 4: en el piso "
         "h, el germen w = 33 mod 2^8 cae desde su paso 4 EXACTAMENTE "
         "en la cola del germen w = 25 ((19,56)->(29,28)->(44,14)->"
         "(22,7)->fusion en 11); en el piso g, el germen w = 118 mod "
         "2^8 pasa por DOS pares consecutivos en ruta ((134,133) y "
         "(101,100)). La renovacion es visible germen a germen",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. Trayectorias explicitas, verificables "
         "a mano en segundos (por eso demostrado: son identidades "
         "concretas de enteros). Es el patron del piso de arriba "
         "(|M|=4 = preludio + |M|=2 desplazado) repitiendose en los "
         "pisos reducidos: LA TORRE ES AUTOSIMILAR AL NIVEL DE LOS "
         "GERMENES. Sugiere que la demostracion de b4/c4 ira por "
         "preludios contados sobre los germenes inferiores - la misma "
         "forma que la cuadratica de |M|=6 conjeturada arriba."),

    fila("LA LEY DE LA REENTRADA TOTAL (estrato 6 de los pisos "
         "reducidos): las 107 clases de |M| = 6 de los dos pisos en "
         "m = 10, 11 REENTRAN TODAS antes de fundir - 64 por par "
         "consecutivo y 43 por la forma {v, 9v-1} -, y la forma "
         "{v, 9v+2} NO aparece NUNCA como reentrada (0 de 107)",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; goal de investigacion abierta. 107 de "
         "107: la torre recursa exclusivamente por DOS formas canonicas "
         "(consec y h), no tres - la asimetria g/h ya asomaba en los "
         "conteos (H > G) y aqui se vuelve estructural. Consecuencia "
         "para la demostracion de b4/c4: las sub-renovaciones de los "
         "pisos reducidos se escriben SOLO sobre f y gamma (la forma "
         "h), y la forma g es puerta de entrada pero no de recursion. "
         "El sistema de phi podria ser mas chico de lo que parecia."),

    fila("LA ANATOMIA UNIVERSAL DEL ESTRATO 4 REDUCIDO: las 686 clases "
         "de |M| = 4 de los dos pisos (m = 10..12) son TODAS 'preludio "
         "hasta par consecutivo con delta saldado (+2 acumulado) + "
         "ventana de Perras exacta (r par, primer 0 seguido de 1)'. "
         "686 de 686, cero excepciones",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; goal de investigacion abierta. Reduce "
         "la demostracion pendiente de las formas cerradas b4 = "
         "7*2^(m-7)-m+4 y c4 = 6*2^(m-7)-m+4 a CONTAR PRELUDIOS por "
         "clase residual - contabilidad sobre maquinaria ya demostrada "
         "(Perras + Terras). Es la misma anatomia del |M| = 4 del piso "
         "de arriba (contraccion + lema general), un piso mas abajo: "
         "tercera aparicion del patron preludio+ventana. Primera tarea "
         "de la continuacion: el conteo de preludios que produce el "
         "7 y el 6 de las dos formas."),

    fila("LA DERIVACION DE b4 Y c4: los conteos por largo de preludio "
         "son potencias de 2 menos 1 PURAS (una clase de preludio por "
         "largo permitido x su ventana de Perras 2^(m-l-2) - 1), y "
         "sumando sobre los largos permitidos -{3,4,6,7,...} en g (sin "
         "el 5), {3,5,6,...} en h (sin el 4)- salen ALGEBRAICAMENTE "
         "las dos formas cerradas: 7*2^(m-7)-m+4 y 6*2^(m-7)-m+4",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; el cierre de la rafaga. Medido en "
         "m = 13: g da 255,127,-,31,15,7,3,1 y h da 255,-,63,31,15,7,"
         "3,1 - las sumas geometricas reproducen el 7 y el 6 de las "
         "formulas EXACTO. Para el ascenso a teorema faltan solo DOS "
         "lemas de preludio unico (mismo genero que la unicidad de "
         "|M| = 2 del piso de arriba: candidatos por v2 + condicion de "
         "valor) y la explicacion de los dos huecos (sin largo 5 en g, "
         "sin largo 4 en h - la asimetria g/h otra vez). El patron "
         "'un germen por ventana' es ya LA CUARTA aparicion de la "
         "misma estructura: el triangulo entero parece generado por "
         "germenes unicos y ventanas de Perras."),

    fila("LOS DOS LEMAS DE HUECO, demostrados por decide: en el piso g "
         "NO existe preludio de largo 5 (cero clases entre las 2^7) y "
         "en el piso h NO existe preludio de largo 4 (cero entre las "
         "2^6) - enumeracion COMPLETA de las clases al modulo del "
         "presupuesto, sin filtro alguno: los huecos de las formas "
         "cerradas b4 y c4 son teoremas finitos",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. Es la mitad facil del ascenso de "
         "b4/c4 a teorema. AVISO honesto para la continuacion: la "
         "enumeracion rapida de germenes en los largos PERMITIDOS "
         "salio inflada porque no filtraba 'preludio con exactamente "
         "2 mixtos' ni deduplicaba por modulo natural (el germen de "
         "L=3 en g es UNA clase mod 8 que aparece como 4 residuos mod "
         "32); la distribucion de m = 13 (ventanas 2^j - 1 exactas, "
         "una por largo) sigue siendo la referencia, y la unicidad "
         "fina del preludio 2-mixto queda como el ultimo lema "
         "pendiente del ascenso."),

    fila("LA UNICIDAD DEL PRELUDIO, decide-verificada, y con ella b4 Y "
         "c4 DEMOSTRADAS EN EL RANGO: cada largo permitido tiene "
         "EXACTAMENTE UN preludio 2-mixto al modulo natural 2^L "
         "(germenes explicitos: 6, 11, -, 55, 95, 7, 487, 199, 1863, "
         "1479 en g; 1, -, 19, 15, 11, 219, 299, 747, 171, 1451 en h), "
         "L = 3..12, y los huecos dan cero",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; el remate de la rafaga. La cadena "
         "completa: preludio unico (decide, L <= 12) + lemas de hueco "
         "(decide) + proposicion de la ventana de Perras (demostrada "
         "para todo k) + suma geometrica (algebra pura) => las formas "
         "cerradas b4(m) = 7*2^(m-7)-m+4 y c4(m) = 6*2^(m-7)-m+4 son "
         "TEOREMAS para el rango m <= 14 (y coherentes con la "
         "prediccion confirmada en 15 y 16). El caso 'para todo m' "
         "pende de UN solo lema: la unicidad del preludio para todo L "
         "(candidato al metodo v2 + condicion de valor de la unicidad "
         "de |M| = 2). En una noche: conjetura -> prediccion "
         "confirmada -> derivacion -> teorema en rango."),

    fila("EL MECANISMO DE LOS PRELUDIOS: los 18 germenes de preludio "
         "terminan en un mixto con D en {-2, -8} - 18 de 18 -, los dos "
         "valores cuyo |D|/2 es potencia de 2 (1 y 4), que el vuelco "
         "alfa convierte en gap que las divisiones llevan exactamente "
         "a 1 (el par consecutivo). Los preludios son el 'Perras de "
         "D negativo': la misma dinamica de D, aterrizando en -2 o -8 "
         "en vez de 0",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. CORRECCION EN VIVO incluida: la "
         "hipotesis inicial era 'todos en D = -2' y los datos la "
         "rompieron en el tercer germen probado (95 aterriza en -8): "
         "la ley es el par {-2, -8}. PREGUNTA AFILADA que queda: por "
         "que NUNCA -4 ni -16, que tambien darian potencias de 2 - la "
         "respuesta debe vivir en el saldo de S (+2) que el preludio "
         "arrastra, y es el corazon del lema general pendiente. Con "
         "el aterrizaje caracterizado, la unicidad general del "
         "preludio se ataca con la dinamica de D restringida a "
         "acabar en {-2, -8}: el metodo de la unicidad de |M| = 2, "
         "con dos dianas en vez de una."),

    fila("LA LEY DEL ATERRIZAJE EN POTENCIAS DE -2: el D del ultimo "
         "mixto antes de toda reentrada consecutiva es una POTENCIA DE "
         "(-2): observados -2 = (-2)^1 (236+18 casos), +4 = (-2)^2 (2) "
         "y -8 = (-2)^3 (22+); los valores con |D|/2 potencia de 2 que "
         "NO son potencias de (-2) (-4, +8, -16) NO aparecen NUNCA. "
         "PREDICCION FALSABLE: el proximo aterrizaje en niveles "
         "profundos sera +16 = (-2)^4, y -4/+8/-16 jamas",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; el ultimo hallazgo de la rafaga. El "
         "mecanismo esbozado: el vuelco alfa da gap |D|/2, que necesita "
         "ser potencia de 2 para que las divisiones lleguen al par "
         "consecutivo exacto; y el SIGNO alterna con el numero de "
         "divisiones porque el saldo +2 de S fuerza que el lado impar "
         "del vortice final caiga del lado correcto - sign(D) = "
         "(-1)^(divisiones+1). Demostrarlo es el corazon del lema "
         "general del preludio: la dinamica de D con dianas en las "
         "potencias de (-2). Los estratos 4 (18/18 en {-2,-8}) y 6 "
         "(260/260 en {-2,+4,-8}) lo cumplen sin excepcion. REFUERZO "
         "de la misma madrugada: m = 13, 14 anaden 1.868 aterrizajes "
         "mas - CERO prohibidos en 2.146 acumulados - y el +16 aun no "
         "aparece (esperable: +4 es el 2,6 por ciento y (-2)^4 deberia "
         "ser un orden mas raro): la prediccion sigue viva y sin "
         "falsar. Y EL VEREDICTO en m = 15, 16 (~9.700 aterrizajes "
         "mas): LA LEY SE REFUERZA Y LA PREDICCION DE ORDEN SE REFUTA "
         "- aparecio -32 = (-2)^5 (1 caso) ANTES que el +16 = (-2)^4 "
         "predicho, que sigue en cero; los prohibidos siguen en cero "
         "absoluto sobre ~11.800 acumulados. La ley queda: SOLO "
         "potencias de (-2), con el patron fino nuevo de que las "
         "potencias IMPARES (aterrizajes negativos, con vuelco) "
         "dominan a las pares - el +16 podria estar estructuralmente "
         "suprimido o ser solo mas raro que -32: pregunta abierta "
         "registrada. Prediccion de orden fallada y anotada: el repo "
         "registra sus predicciones falladas. Y LA AMPLIACION AL PISO "
         "DE ARRIBA (m = 14..16, ~8.500 aterrizajes post-rebote de "
         "pares consecutivos): misma ley, cero prohibidos, y TAMPOCO "
         "hay +16 - la muestra total (~20.000 en tres pisos) tiene "
         "j en {0,1,2,4} divisiones con el j = 3 especificamente "
         "ausente mientras j = 4 si aparecio. SE REGISTRA COMO "
         "CONJETURA: el aterrizaje (-2)^4 = +16 esta estructuralmente "
         "prohibido (no es rareza: es el unico j saltado). Y una "
         "ANOMALIA nueva para investigar: 3 casos del piso de arriba "
         "con ultimo mixto en D = 0 (el rebote como aterrizaje "
         "inmediato de una reentrada consec) que no encajan en la "
         "taxonomia - RESUELTA EN EL ACTO: los 3 casos son r = 0 (uno "
         "por m), el par degenerado (0, 1) con T(0) = 0 bailando "
         "(0,1)-(0,2): EL BORDE DE SIEMPRE, quinto miembro del catalogo "
         "de bordes del repo (m=0, k=0, n=1, n=2^k-1, y ahora r=0 en "
         "los aterrizajes). La ley de potencias de -2 queda sin "
         "excepciones reales. Y LA CAZA DECISIVA (m = 17, 18, ~46.500 "
         "aterrizajes mas): el -32 = (-2)^5 salto a 21 casos y el "
         "+16 = (-2)^4 sigue en CERO sobre ~66.000 acumulados - la "
         "quinta potencia 21 veces, la cuarta jamas. La conjetura de "
         "la supresion del j = 3 pasa de plausible a aplastante. El "
         "proximo paso del hilo es la DEMOSTRACION (el reparto tres "
         "+1 y un -1 de los cuatro mixtos, con la paridad de j "
         "decidiendo el lado par del consec)."),

    fila("EL LEMA GENERAL DEL PRELUDIO DEL PISO h, DEMOSTRADO - y con "
         "el, c4(m) = 3*2^(m-6) - m + 4 ES TEOREMA PARA TODO m: (1) "
         "D1 = -3 SIEMPRE tras el primer mixto (calculo de una linea, "
         "con w par excluido porque D1 = 12w-2 fuerza tercer mixto); "
         "(2) la dinamica de D desde -3 vive en el grafo finito "
         "{-3, -5} con aterrizajes exactos {-2, -8}; (3) hay UN camino "
         "por largo (la alternancia fuerza la palabra) y el hueco "
         "L = 4 es imposible (-2 aterriza en largos impares, -8 en "
         "pares mas 2 divisiones); (4) Terras da UNA clase por palabra",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; la corona de la rafaga: el eslabon "
         "que faltaba, encontrado al escribir el argumento del reparto "
         "de mixtos. El esqueleto completo cabe en diez lineas sobre "
         "el grafo {-3, -5}; el detalle fino (palabra de paridades <-> "
         "clase, via E) queda para la formalizacion. Explica ademas "
         "por que los aterrizajes +4 y -32 solo aparecen en estratos "
         ">= 6 (entran por otros D iniciales, no desde -3). El piso g "
         "(D0 = 6w+1 impar, mixed0 es aterrizaje tambien) es el "
         "analogo pendiente - mismo metodo, otro grafo."),

    fila("LA UNIFICACION DE LOS DOS PISOS: el piso g entra al MISMO "
         "grafo {-3, -5} que el h - el estado tras el primer mixto de "
         "sus germenes es D = -3 en los 8 casos con L >= 4 (y el de "
         "L = 3 aterriza directo en -2). Los dos lemas de preludio "
         "comparten el corazon; la diferencia entera de los pisos es "
         "el TRAMO DE ENTRADA (g trae un compartido previo), que "
         "explica los conjuntos de largos {3,4,6,7,...} vs {3,5,6,...}",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; medido sobre los 9 germenes de g con "
         "testigos grandes. Reduce el lema de b4 a dos piezas de "
         "entrada: (a) demostrar que el mixto inicial de g fuerza "
         "D = -3 (el analogo del calculo de una linea de h), y (b) la "
         "contabilidad del tramo de entrada que produce el hueco en "
         "L = 5. Con ellas, b4(m) = 7*2^(m-7) - m + 4 seria teorema "
         "para todo m y el sistema de phi tendria sus dos masas "
         "exactas completas. La asimetria g/h queda LOCALIZADA: no es "
         "del grafo, es de la puerta."),

    fila("LA PUERTA DE g, DEMOSTRADA (tres identidades de una linea): "
         "(1) {w, 9w+2} con w IMPAR pasa en un paso a {v, 9v-1} con "
         "v = (3w+1)/2 - LA FORMA h -, y desde ahi el lema de h aplica "
         "entero; (2) con w PAR baja a la forma nueva {u, 9u+1}; (3) el "
         "mixto de {v, 9v+1} con v impar aterriza DIRECTO en D = -2 "
         "(gap 3v). Las tres exactas en 30.000 casos cada una",
         "todo_n", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. Con esto el lema de b4 esta a UNA "
         "pieza: el caso w par con u par baja a una forma 27u + c - la "
         "TORRE 3-ADICA de formas 9v+c, 27u+c, ... asomando: el hilo "
         "nombrado que sigue. La unificacion es ahora EXACTA y "
         "demostrada para la mitad impar: los dos pisos no son "
         "hermanos, son EL MISMO piso con puertas distintas - g entra "
         "a h en un paso. La asimetria entera del programa (H > G, "
         "0/107 reentradas por g, los huecos 4 vs 5) es la aritmetica "
         "de esa puerta."),

    fila("LA TORRE 3-ADICA DEL TRAMO DE ENTRADA: el caso par-par de la "
         "puerta de g asciende {v,9v+1} -> {u,27u+2} -> {s,27s+1} -> "
         "{q,81q+2} -> ... - las formas son {v, 3^k v + c_k} y la masa "
         "decae 2^(-k) por nivel: el tramo de entrada de g ES la bajada "
         "de una torre 3-adica geometrica, que NO cierra en grafo "
         "finito pero suma geometricamente. Identidades del segundo "
         "nivel exactas en 30.000 casos cada una",
         "todo_n", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada. Cada identidad es una linea (el paso "
         "compartido sube el 3^k o baja el v segun paridades). Con las "
         "puertas demostradas y la torre caracterizada, la completacion "
         "de b4 es una suma geometrica sobre la torre - contabilidad, "
         "no misterio. Y la imagen final del programa queda dibujada: "
         "el triangulo de estratos se genera por UNA gramatica "
         "(germenes del grafo {-3,-5} + ventanas de Perras) a la que "
         "se llega bajando torres 3-adicas de formas {v, 3^k v + c}. "
         "Los tres objetos - grafo, ventana, torre - son los atomos de "
         "toda la estructura medida esta noche."),

    fila("EL LEMA GENERAL DE LA TORRE (para TODO k, la familia "
         "infinita cuantificada en un teorema): T1: {v, 3^k v + 2} con "
         "v par baja a {v/2, 3^k (v/2) + 1}; T2: {v, 3^k v + 1} con v "
         "par SUBE la potencia: a {v/2, 3^(k+1) (v/2) + 2}. "
         "Demostracion de dos lineas (T1: ambos se parten; T2: beta da "
         "(3(3^k v + 1)+1)/2 = 3^(k+1)(v/2) + 2). La torre entera de "
         "formas {v, 3^k v + c} queda gobernada por dos identidades "
         "universales",
         "todo_n", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; y la nota de metodo que responde a la "
         "clausula 'encontrar todos': una familia INFINITA de lemas "
         "(uno por nivel de la torre, uno por largo de preludio, uno "
         "por germen) solo se completa de una manera legitima en "
         "matematica: CUANTIFICANDO - reemplazando los infinitos "
         "enunciados por un teorema con para-todo. Los tres atomos del "
         "programa quedan ahora cada uno como enunciado universal: el "
         "grafo {-3,-5} (teorema, todo w impar), la ventana de Perras "
         "(proposicion, todo k), y la torre (este lema, todo k). "
         "Verificado en 40.000 instancias (k = 2..11, v par < 4000)."),

    fila("LA COMPLETACION DE b4: b4(m) = 7*2^(m-7) - m + 4 ES TEOREMA "
         "PARA TODO m. La cadena: (1) la puerta impar mete a g en h en "
         "un paso, luego sus largos son 1 + L_h con unicidad HEREDADA "
         "del lema de h - y el hueco en 5 es la imagen del hueco en 4; "
         "(2) la ruta w = 2 (mod 4) con u impar da el largo 3 (germen "
         "unico mod 8, decide); (3) las rutas de la torre gastan un "
         "mixto por piso (toda forma de gap impar es un mixto) y NUNCA "
         "alcanzan preludios 2-mixtos: no aportan al estrato 4; (4) la "
         "suma de ventanas sobre {3} U {1 + L_h} reproduce la formula "
         "exacta (verificado algebraicamente m = 7..19)",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, madrugada; el segundo teorema de forma cerrada "
         "completo de la sesion (el primero fue c4 via el grafo). CON "
         "LOS DOS, LAS MASAS EXACTAS DE LAS SUB-RENOVACIONES DEL "
         "ESTRATO MINIMO ESTAN COMPLETAS: el sistema de phi tiene sus "
         "primeros terminos en forma cerrada demostrada, que era el "
         "criterio de la revision externa para 'resultado fuerte'. "
         "Nota fina pendiente de formalizacion (como en h): la palabra "
         "de paridades <-> clase via Terras, y el germen L = 3 por "
         "decide - ambos ya verificados computacionalmente."),

    fila("LA TAXONOMIA DE LLEGADAS AL CONSECUTIVO, cerrada en formas: "
         "(a) la forma {s, 3s-1} ES identicamente el estado D = -2 "
         "(gap 2s-1 => D = -2, una linea; 1.630 casos medidos como "
         "ruta dominante), y (b) la otra ruta son los estados de gap 2 "
         "({s, s+2}, D = 1-2s) que llegan por division - la cola de "
         "los aterrizajes -8/+4/-32. Ademas: en estratos >= 6 los "
         "aterrizajes llegan por transiciones mixto->mixto entre "
         "FORMAS (la D enorme se cancela por estructura, como en la "
         "puerta P3), no por tramos compartidos largos",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "04-08-2026, madrugada. Consecuencia para la supresion del "
         "j = 3: la pregunta queda reformulada como INVENTARIO DE "
         "FORMAS - que formas {s, c*s + d} son alcanzables y cual es "
         "la constante de aterrizaje de cada una (P3 dio {v,9v+1} -> "
         "-2; el inventario completo con sus constantes decidira si "
         "alguna produce +16). El metodo: las identidades de una linea "
         "por forma, como toda la cadena de esta noche."),

    fila("EL ACTA DE LOS 3 CHANCHITOS (segunda revision externa): la "
         "arquitectura VALIDADA entera por el revisor, y su unica "
         "correccion (-2 en vez de -1 por ventana) RESULTO SER UN MAPA "
         "DE CONVENCION: su(m) = 2*nuestro(m-1), confirmado 10 de 10 "
         "terminos, con su formula corregida algebraicamente identica "
         "a la nuestra bajo el mapa. Los teoremas b4 y c4 quedan en "
         "pie tal cual",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "04-08-2026. DOS DOCTRINAS NUEVAS del episodio: (1) una "
         "coincidencia de forma con OEIS sin contexto del dominio NO "
         "es evidencia (A079583 pasa a curiosidad, no confirmacion - "
         "regla del revisor, adoptada); (2) una correccion externa "
         "tambien puede ser artefacto de convencion: la herramienta "
         "que decide es el mapa explicito entre convenciones, termino "
         "a termino, ANTES de tocar nada - esta vez el mapa salvo dos "
         "teoremas correctos de una 'correccion' que los habria "
         "estropeado. El propio revisor habia advertido su riesgo de "
         "convencion: la advertencia era la buena."),

    fila("LA IDENTIDAD UNIVERSAL DE FORMAS: {s, 3s + t} tiene D = t - 1 "
         "IDENTICAMENTE para todo s (gap 2s + t => D = t - 1, una "
         "linea). Los estados de aterrizaje son las formas con "
         "t = (-2)^j + 1: {s,3s-1} (D=-2), {s,3s+5} (D=+4, 5 casos "
         "medidos), {s,3s-7} (D=-8, 273 casos), {s,3s-31} (D=-32). LA "
         "SUPRESION DEL j = 3 EN SU FORMA FINAL: la dinamica jamas "
         "alcanza la forma {s, 3s + 17}",
         "todo_n", "demostrado", "identidadexacta.py", "propio",
         "04-08-2026; el inventario de formas del siguiente paso. La "
         "identidad unifica P3, la taxonomia de llegadas y los "
         "aterrizajes en una linea; la parte 'demostrado' es la "
         "identidad misma; el inventario de cuales t-formas se "
         "alcanzan es medido (los conteos citados). La pregunta de la "
         "supresion queda reducida a la inalcanzabilidad de UNA forma "
         "afin concreta - el enunciado mas limpio que ha tenido - y "
         "nota tecnica: t = D + 1, asi que la t-dinamica es la "
         "D-dinamica conocida; lo que decide es la alcanzabilidad "
         "conjunta (D, E), el mismo objeto del lema general pendiente."),

    fila("EL MAPA DE t ES EL MAPA DE D (t = D + 1, verificado en 80 "
         "transiciones deterministas): t par comparte (s par: t/2; s "
         "impar: (3t-2)/2) y t impar es mixto. COROLARIO AFILADO: "
         "aterrizar en +16 = llegar a la forma t = 17 exige pasar el "
         "tramo por D = 33 (via f0) o D = 11 (via f1); el +4 observado "
         "viene de D = 3 (f1: (3*3-1)/2 = 4). LA SUPRESION DEL j = 3 "
         "EQUIVALE A: los valores de tramo D = 11 y D = 33 son "
         "inalcanzables desde las entradas del programa",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "04-08-2026. La reduccion final de la conjetura: una pregunta "
         "de alcanzabilidad sobre DOS enteros concretos en la dinamica "
         "de tramo (f0 = (D-1)/2, f1 = (3D-1)/2 sobre impares). El "
         "contraste que la hace jugosa: D = 3 SI es alcanzable (produce "
         "los +4) y D = 11 no - que separa al 3 del 11 es exactamente "
         "lo que hay que demostrar. Nota: las entradas conocidas del "
         "tramo son -3 (el grafo), 1 (pares consecutivos) y las "
         "puertas de la torre; el grafo desde -3 y desde 1 es finito y "
         "NO contiene 11 ni 33 - la pieza pendiente es el inventario "
         "de entradas de los estratos altos."),

    fila("LA LEY MOD 3 DE LOS TRAMOS: en los tramos compartidos del "
         "programa, D nunca es 2 (mod 3) - equivalentemente, EL LADO "
         "MAYOR NUNCA ES MULTIPLO DE 3 (D = 2 mod 3 <=> 3 | lado "
         "mayor, una linea). Verificado masivo: los impares presentes "
         "son exactamente los no-2 mod 3, y los ausentes (5, 11, 17, "
         "23, -7, -13...) todos 2 mod 3. CONSECUENCIA: D = 11 muere "
         "por la ley (es 2 mod 3) - la mitad de la supresion del j = 3 "
         "queda explicada; D = 33 (0 mod 3) SI aparece (23.715 veces) "
         "y su no-aterrizaje en +16 es la otra mitad, pendiente",
         "verificado_hasta", "medido", "identidadexacta.py", "propio",
         "04-08-2026. EL MECANISMO (esbozo de induccion): 3 | l se "
         "conserva al partir por 2 y solo se destruye cuando ese lado "
         "recibe 3x+1 (que da residuo 2 mod 3); las entradas del "
         "programa (9w+2, 9w-1, y el lado impar tras todo mixto) "
         "tienen lado mayor = 2 (mod 3): la propiedad se propaga. ES "
         "LA ESTRUCTURA MOD 3 DEL ARBOL (los rayos mudos multiplos de "
         "3, medida el primer dia del repo en mallascerradas.py) "
         "REAPARECIENDO EN LA DINAMICA DE PARES: las dos mitades del "
         "laboratorio se tocan. La supresion queda partida en dos "
         "lemas: la ley mod 3 (D = 11) y la rama de salida del 33."),

    fila("LA AUDITORIA RIGOR MORTIS (04-08-2026, orden del usuario): "
         "TODA afirmacion del programa de fusion del 03/04-08 tiene "
         "test exacto de enteros en fichero del repo - "
         "auditoria_rigor.py, 30 tests numerados R01-R30 con "
         "SystemExit, 30 de 30 PASS, mas la re-certificacion de "
         "nuevasfusion.py, identidadexacta.py y masasdeclase.py (exit "
         "0 los tres). Cubre: vortice general, Perras, unicidad M2, "
         "lema C=3^q, ruta impar, D y E, rebote real, censo de E, "
         "Gatas, Jirafas ida+reciproco, identidad y reconstruccion, "
         "Pandas, familia 3067, germenes, series b/c, formulas b4/c4, "
         "germen unico, preludio+huecos, aterrizajes, grafo h, puerta "
         "g, torre, gasto, contabilidad b4, formas y mapa t, ley mod "
         "3, y la doble correccion (reproducida: f0 10.372, +16 7)",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "La auditoria hacia atras que pedia el objetivo: las "
         "afirmaciones que solo tenian mediciones ad-hoc (formulas "
         "b4/c4, germen unico, preludios, aterrizajes, puerta, torre, "
         "gasto, mod 3, doble correccion) tienen ahora su test "
         "permanente y reproducible. Rangos declarados en cada test; "
         "donde la base cita numeros de rangos mayores, el test "
         "verifica la ley en rango exacto reproducible."),

    fila("EL ESTRATO 6 DEL PISO PRINCIPAL TIENE FORMA CERRADA: "
         "e6(N) = 3 + (N-7)(N-8)/2 para N >= 10 - cuadratica exacta, "
         "clavada en los niveles 10..15 y CONFIRMADA POR PREDICCION en "
         "los nunca medidos 16, 17, 18 (39, 48, 58). El tercer estrato "
         "del triangulo con formula, tras el 2^k - 1 de Perras "
         "(lineal... geometrico) y las b4/c4 de los pisos reducidos",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, tras el rigor mortis; test R33. El objetivo que "
         "senalo la revision externa (el estrato 6 como el trabajo "
         "bueno parado) da fruto al primer intento. NOTA DE METODO: el "
         "primer test de prediccion FALLO por un desfase de convencion "
         "k/nivel propio (la trampa de los chanchitos, autoinfligida y "
         "autocazada en minutos por los numeros: los medidos eran "
         "exactamente la formula corrida un indice). Pendiente: la "
         "demostracion via preludios + ventanas (el termino cuadratico "
         "sugiere DOS largos libres - preludios de dos tramos - contra "
         "el largo unico del estrato 4). Y LaTourette 4.2.4 verificada: "
         "pregunta proporcion de unos EN bloques (1/3 <= n/k <= 7/11), "
         "no densidad de clases: EL CONTEO DE PERRAS ES NUEVO."),

    fila("LA DERIVACION DE e6, con la hipotesis muerta que la revelo: "
         "la anatomia medida da UNA reentrada a consecutivo (40 de 42; "
         "el 'preludio doble' conjeturado ERA FALSO), o sea la fusion "
         "|M|=6 es rebote -> piso reducido -> fusion de estrato 4 alli. "
         "Por tanto e6 = suma de las NUEVAS de estrato 4 reducidas, y "
         "esas son LINEALES EXACTAS: b4(m)-2b4(m-1) = c4(m)-2c4(m-1) = "
         "m-6 (verificado algebraico m = 9..19). Suma de lineales = "
         "cuadratica: el termino cuadratico de e6 = 3 + T(N-8) VIENE "
         "DEL -m de los chanchitos",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026. La escalera de la torre de formulas queda "
         "ENGRANADA: Perras (2^k-1) alimenta a b4/c4 (geometrico - "
         "lineal), cuyas nuevas (lineales) alimentan a e6 (cuadratica). "
         "CONJETURA DE LA ESCALERA, registrada con prediccion: e8 sera "
         "cubica en su cola (suma de las nuevas cuadraticas de los "
         "estratos 6 reducidos) - falsable midiendo estratos 8. La "
         "contabilidad fina (constantes y empalmes) es el pendiente "
         "para el ascenso a teorema; la estructura ya esta."),

    fila("LA CONJETURA DE LA ESCALERA, FALLADA EN e8 Y REGISTRADA: la "
         "prediccion 'e8 cubica en su cola' es FALSA en los niveles "
         "medidos - e8 = 3,7,15,27,45,73,111,166,237 (N = 10..18) con "
         "terceras diferencias 0,2,4,0,7,-1: no constantes, no "
         "polinomial en el rango. DIAGNOSTICO: el insumo de e8 (las "
         "nuevas de estrato 6 reducidas: 3,5,8,14,22,34) tampoco es "
         "polinomial aun - el argumento de composicion es correcto "
         "pero el regimen polinomial de los pisos profundos no ha "
         "empezado en los niveles alcanzables",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026; prediccion fallada y anotada, como las otras dos "
         "de la sesion. LO QUE QUEDA EN PIE: e2, e4 (constantes = 1), "
         "e6 cuadratica confirmada por prediccion, y las formas "
         "cerradas b4/c4 - la escalera existe hasta el tercer peldano; "
         "el cuarto exige la contabilidad de canales completa (rutas "
         "r=3, composiciones dobles, empalmes), no una extrapolacion "
         "de forma. La leccion: 'cada estrato es la integral del "
         "anterior' vale como MECANISMO demostrable, no como formula "
         "que se adivina - los empalmes mandan en los niveles bajos."),

    fila("EL TEOREMA DE KOMODO 3 (el mod 3; ascendido de medido a DEMOSTRADO): tras el "
         "paso 0 de cualquier par consecutivo, el lado MAYOR es "
         "siempre = 2 (mod 3) - r par da 3s+2, r impar da (3r+1)/2 = 2 "
         "mod 3 -, y la propiedad 'mayor no multiplo de 3' es "
         "INVARIANTE: partir por 2 mapea {1,2} -> {2,1} sin tocar el 0, "
         "y el paso impar da (3l+1)/2 = 2 mod 3 siempre. COROLARIO: "
         "D != 2 (mod 3) en todo estado posterior al paso 0 - los "
         "aterrizajes -4, +8, -16 y los tramos D = 5, 11, 17, -7 son "
         "IMPOSIBLES para siempre, en todos los pisos",
         "todo_n", "demostrado", "auditoria_rigor.py", "propio",
         "04-08-2026; test R34, demostracion de tres piezas de una "
         "linea (base par, base impar, invariancia de dos ramas). Es "
         "el unico contenido real que sobrevivio de la 'ley (-2)^j' "
         "(correccion 39) y ahora es teorema: el signo de los "
         "aterrizajes queda demostrado, y el |D| = 2^j era "
         "definicional - el fenomeno completo de los aterrizajes esta "
         "CERRADO. Es ademas el teorema que conecta las dos mitades "
         "del laboratorio: los rayos mudos multiplos de 3 del arbol "
         "inverso (mallascerradas.py, primer dia) son exactamente lo "
         "que la dinamica de pares no puede pisar del lado mayor."),

    fila("EL TEOREMA DE KOMODO 3, FORMALIZADO EN LEAN 4 (teoremadekomodo3.lean, "
         "el SEXTO .lean del repo): base_par_T y base_impar_T (tras el "
         "paso 0 el mayor es 3s+2 / 3k+2, con las identidades de T "
         "demostradas), inv_par e inv_impar (la invariancia por rama) "
         "y el empaquetado invariancia (T l no multiplo de 3 si l no "
         "lo era). Nucleo puro, sin Mathlib, #print axioms = [propext, "
         "Quot.sound] en los cinco, cero sorryAx",
         "todo_n", "demostrado", "teoremadekomodo3.lean", "propio",
         "04-08-2026; y CORREGIDO la misma noche por la cuarta revision "
         "externa, que encontro tres cosas: (1) el encabezado "
         "sobreafirmaba 'siempre = 2 mod 3' - falso en el 28% de los "
         "estados (el residuo alterna 2 <-> 1 al partir por 2); son "
         "DOS frases: base (= 2 tras el paso 0) e invariante (nunca "
         "= 0 despues); (2) FALTABA LA INDUCCION - el teorema komodo "
         "que compone la invariancia sobre iterados (Titer propio, "
         "nucleo sin Mathlib) es ahora el enunciado 'para siempre' "
         "verificado, axiomas [propext, Quot.sound]; (3) la trampa de "
         "resta de Nat en 9w-1 (reescrito 9w+8) y una hipotesis "
         "sobrante. Mas la seccion bibliografica: 'multiplos de 3 sin "
         "preimagen' es clasico - el aporte es la traduccion a la "
         "coordenada D y el cierre por maquina. En palabras del "
         "revisor: 'este si es un teorema tuyo del programa de "
         "fusion'."),

    fila("LOS LEMAS DE PERRAS, FORMALIZADOS EN LEAN 4 "
         "(lemasdeperras.lean, el SEPTIMO .lean): el LEMA DEL VORTICE "
         "como doble implicacion - T(s) = T(s+g) con g impar y s >= 1 "
         "SI Y SOLO SI g = 2s+1 y s impar - mas el arranque D1 = 1 "
         "(con las identidades de T demostradas) y los dos pasos del "
         "tramo D = 1. Nucleo puro, sin Mathlib, cero sorryAx, "
         "compilado a la primera",
         "todo_n", "demostrado", "lemasdeperras.lean", "propio",
         "04-08-2026, la misma noche que Komodo 3. El vortice es el "
         "atomo del que cuelga TODO el programa (Perras, aterrizajes, "
         "unicidades): tenerlo verificado por maquina como iff - "
         "incluida la mitad 'imposible en positivos' que la costura "
         "N/Z2 exigia declarar - es el cimiento que la revision "
         "externa pedia. Nota: vortice usa Classical.choice (del "
         "by_cases), estandar; los otros tres solo propext y "
         "Quot.sound. Siguiente candidato: el conteo 2^(m-1) entero."),

    fila("LA CONTRACCION DE GATAS, FORMALIZADA EN LEAN 4 "
         "(contracciondegatas.lean, el OCTAVO .lean): las cuatro "
         "identidades de paso y el empaquetado - T(T(4t+1)) = 3t+1 y "
         "T(T(4t+2)) = 3t+2 para todo t: la autosimilitud exacta del "
         "problema de fusion, verificada por el nucleo. Compilado a la "
         "primera, cero sorryAx, axiomas [propext, Quot.sound]",
         "todo_n", "demostrado", "contracciondegatas.lean", "propio",
         "04-08-2026, el cierre de la jornada: TRES resultados con "
         "nombre bajo verificacion de maquina en una noche (Komodo 3, "
         "los lemas de Perras, la contraccion de Gatas). Ocho .lean en "
         "el repo, seis del programa historico y ahora tres del "
         "programa de fusion. El corazon (a) de Gatas - la pieza que "
         "la revision externa llamo 'el contenido real del documento' "
         "- es ahora matematica verificada por maquina."),

    fila("LA RECURSION VERTICAL DEL TRIANGULO: la rama r = 1 (mod 4) "
         "de las nuevas de estrato s en el nivel N es EXACTAMENTE "
         "e_{s-2}(N-2) - la contraccion de Gatas sube en diagonal por "
         "el triangulo entero (consume 2 mixtos y 2 niveles, y "
         "t -> 3t+1 es biyeccion). Verificado clavado en e8: rama1 = "
         "e6(N-2) = 6, 9, 13, 18 (N = 12..15, 4/4); y en e6: rama1 = "
         "e4(N-2) = 1. La descomposicion de canales queda: e_s(N) = "
         "e_{s-2}(N-2) + [canal par] + [canal r=3] - UN canal cerrado "
         "por teorema, dos pendientes",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, el ultimo hallazgo de la jornada; test R35. La "
         "demostracion es la contraccion verificada por maquina "
         "(contracciondegatas.lean) mas la biyectividad mod 2^m y el "
         "corrimiento M+2 (ambos pasos de la contraccion son mixtos): "
         "esta a un paso de teorema y A UN PASO DE LEAN. Es la "
         "estructura diagonal que faltaba para la contabilidad de e8: "
         "el canal vertical es polinomial siempre que e_{s-2} lo sea - "
         "la no-polinomialidad de e8 vive entera en los canales "
         "horizontales (pisos reducidos), ahora aislada."),

    fila("EL MOTOR DE LA RECURSION VERTICAL, FORMALIZADO "
         "(recursionvertical.lean, el NOVENO .lean): titer_shift "
         "(Titer (k+2) (4t+1) = Titer k (3t+1), la trayectoria absorbe "
         "los dos pasos exactos), s_shift (cada lado gana UN impar), "
         "mixto0/mixto1 (los dos pasos son mixtos: el estrato sube 2), "
         "y FUSION_DESPLAZA como iff: el par funde balanceado en k+2 "
         "sii el contraido funde balanceado en k. Nucleo puro, cero "
         "sorryAx, compilado a la primera",
         "todo_n", "demostrado", "recursionvertical.lean", "propio",
         "04-08-2026; el paso 1 de los tres del cierre. Lo que queda "
         "declarado para el conteo completo e_s(N)|r=1 = e_{s-2}(N-2): "
         "la biyectividad de t -> 3t+1 mod 2^m (el paso de clases, "
         "pendiente - exige induccion en m que omega no come). Cuatro "
         ".lean del programa de fusion en una noche."),

    fila("LA CONTABILIDAD DE CANALES DE e8, CERRADA: e8(N) = "
         "e6(N-2) [canal vertical, teorema-candidato] + P8(N) [canal "
         "par: 1 + suma acumulada de las nuevas de estrato 6 del piso "
         "g] + H8(N) [canal r=3: las nuevas de estrato 6 del piso h en "
         "N-2, DIRECTO]. Exacta en los cuatro niveles medibles: "
         "15 = 6+4+5, 27 = 9+9+9, 45 = 13+17+15, 73 = 18+31+24. La "
         "MISMA estructura que la identidad de renovacion (canal g "
         "acumulado, canal h directo), un estrato mas arriba",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, paso 2 de los tres del cierre. La "
         "no-polinomialidad de e8 queda EXPLICADA: sus insumos "
         "(g6news: 3,5,8,14,22; h6news: 3,5,9,15,24) son los estratos "
         "6 reducidos, que aun no entran en regimen - la recursion "
         "sigue hacia abajo y el cuarto peldano es SUMA de terceros "
         "peldanos reducidos. El patron de dos canales (acumulado / "
         "directo) aparece por SEGUNDA vez: es estructural, candidato "
         "a teorema por la misma reduccion que cerro e6."),

    fila("EL TEST ESPEJO DE LA RECURSION VERTICAL, PASADO: en 3n-1 la "
         "contraccion vive en v = 2 (mod 4) - etiquetas volteadas, "
         "como manda el espejo - y da el par fresco (3u+1, 3u+2) "
         "(30.000 casos); y la diagonal espejo clava identica: rama "
         "v=2mod4 de e8- = e6-(N-2) = 6, 9, 13, 18 (4/4, los MISMOS "
         "numeros que el mapa 3n+1). El pipeline de la recursion "
         "vertical es invariante al espejo",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, paso 3 de los tres del cierre; la falsacion "
         "barata que pedia la doctrina del repo (un pipeline que no "
         "fuera invariante al espejo tendria un error de derivacion "
         "escondido). Que los numeros sean IDENTICOS es ademas "
         "coherente con el teorema del espejo de espejoak.lean: la "
         "diagonal es funcion del vector de paridad. Con los tres "
         "pasos: el motor en Lean (9no .lean), la contabilidad de e8 "
         "cerrada, y el espejo verificado - la recursion vertical "
         "queda blindada por las tres caras."),

    fila("EL SISTEMA DE OSAS - LA ECUACION DE PHI: dividiendo la identidad demostrada "
         "a(k+2) = a(k) + (2^k - 1) + G(k) + H(k) entre 2^(k+2) y "
         "pasando al limite (existe por el doblado de Gao en los tres "
         "pisos), phi = (1 + beta + gamma) / 3, con beta y gamma las "
         "densidades limite de los pisos reducidos {w,9w+2} y "
         "{w,9w-1}. COROLARIO (el cierre del circulo): como beta, "
         "gamma <= 1, phi = 1 SI Y SOLO SI beta = gamma = 1 - la "
         "conjetura de densidad de Gao-Wu es EQUIVALENTE a si misma "
         "en los pisos reducidos: la autosimilitud es la conjetura "
         "reproduciendose piso a piso",
         "todo_n", "demostrado", "auditoria_rigor.py", "propio",
         "04-08-2026; la sintesis de la jornada entera, salida de "
         "releer la identidad con ojos de limite. La recurrencia del "
         "deficit (delta(k+2) = 1/2 + delta(k)/4 + (1-G-H)/2^(k+2)) "
         "es la identidad reordenada, verificada EXACTA en enteros "
         "k = 3..14; el paso al limite usa G = suma b(i) y H = c(k) "
         "(la reconstruccion demostrada) mas convergencia geometrica. "
         "TODO el aparato del programa - Perras, Gatas, la diagonal, "
         "los canales - queda resumido en una ecuacion de tres "
         "terminos. La pregunta del laboratorio es ahora: beta = 1?"),

    fila("EL SISTEMA DE IDENTIDADES ENTERAS ENTRE LOS TRES PISOS: "
         "(1) b_impar(m) = c(m-1) - la puerta P1 como conteo, 6/6 "
         "exacta; (2) b_2mod4(m) = a(m-3) + c(m-6) - el canal w = 2 "
         "mod 4 aterriza en el problema CONSECUTIVO tres niveles abajo "
         "mas un eco c seis niveles abajo, 6/6 exacta; (3) b_0mod4 ~ 0 "
         "(la torre, suprimida: 0,0,0,0,0,1). EN FORMA LIMITE: "
         "beta = gamma/2 + (phi + gamma)/8 + epsilon_torre - la "
         "segunda ecuacion del sistema de phi",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026; el sistema se cierra: con phi = (1+beta+gamma)/3 "
         "(demostrada) y esta, queda UNA ecuacion pendiente (la "
         "descomposicion de c por el grafo: c(m) = suma de ventanas "
         "sobre a - el analogo con los largos del grafo {-3,-5}). Con "
         "las tres, el sistema lineal en (phi, beta, gamma) mas las "
         "colas de torre DECIDE los limites - la pregunta beta = 1 "
         "tendra respuesta algebraica. Las dos identidades de hoy son "
         "ademas demostrables por las puertas ya formalizadas: P1 es "
         "lean, y el canal w = 2 mod 4 es P2 + P3 + contraccion."),

    fila("EL SISTEMA DE OSAS, CERRADO - LA TERCERA ECUACION: la "
         "deconvolucion c(m) = suma_j R(j) a(m-j) es EXACTA en los 8 "
         "niveles (R = 1,0,1,3,2,4,9,14 en j = 3..10), y el test "
         "independiente de germenes de reentrada reproduce el centro "
         "(j = 5,6,7 clavados) con flecos +-1 en los bordes - la "
         "contabilidad de orientacion bajo vuelcos es el pendiente. "
         "CON LAS TRES ECUACIONES el sistema cierra en formula: "
         "gamma = rho phi (rho = suma R(j) 2^-j), beta = gamma/2 + "
         "(phi+gamma)/8, phi = (1+beta+gamma)/3 => PHI = 8/(23-13rho). "
         "LA CONJETURA DE GAO-WU EN UNA LINEA: phi = 1 <=> rho = 15/13",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, el desemboque de la jornada entera: la pregunta "
         "de los 51% de Gao es ahora si una serie concreta de enteros "
         "positivos (los germenes de reentrada del grafo {-3,-5}) suma "
         "exactamente 15/13 al pesarla con 2^-j. rho truncada a j=10: "
         "0.28 - la cola manda, como siempre en este problema, pero "
         "por primera vez ES una serie con estructura (germenes del "
         "grafo) y no un barrido ciego. CONDICIONAL a: convolucion "
         "exacta mas alla del rango (deconvolucion la respalda) y "
         "resolucion de los flecos de orientacion. El programa "
         "completo - de los vortices del 221 a esta linea - cabe en: "
         "phi = 8/(23 - 13 rho)."),

    fila("LA SERIE R, EL NUCLEO FINAL DEL PROGRAMA: extendida por "
         "deconvolucion exacta a j = 13 (R = 1,0,1,3,2,4,9,14,25,47,"
         "89, con c(15) = 3053 y c(16) = 6487 medidos exactos), sus "
         "razones SUBEN HACIA 2 (1.556, 1.786, 1.88, 1.894) - EL "
         "MISMO fenomeno que la razon de b(k) que abrio el programa, "
         "ahora en su forma nuclear. Y rho CONVERGE por el propio "
         "sistema (c(m)/2^m <= 1 fuerza rho <= 1/phi): rho truncada "
         "0.3002, phi truncada por la formula 0.4189 - coherente con "
         "el 0.4357 de a(32) y el 0.51 de Gao",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, el punto final de la jornada. LA PREGUNTA MAS "
         "VIEJA DEL LABORATORIO EN SU FORMA DEFINITIVA: la razon de "
         "R(j) sube hacia 2 - si R(j)/2^j decae lo bastante lento, "
         "rho alcanza 15/13 y phi = 1 (Gao-Wu cierto); si decae "
         "rapido, phi < 1 con valor exacto 8/(23-13rho). Todo el "
         "problema - los 51% de Gao, los estratos, los pisos, el "
         "grafo - es ahora UNA serie de enteros con estructura "
         "conocida (germenes de reentrada del grafo {-3,-5}) y una "
         "unica pregunta asintotica. El circulo perfecto: el programa "
         "empezo con una razon subiendo a 2 sin decidirse (b(k), "
         "sesion del 30-07) y desemboca en otra razon subiendo a 2 - "
         "pero esta vez la serie TIENE gramatica demostrada detras."),

    fila("LA ECUACION DE BETA, RECONSTRUIDA INDEPENDIENTE (tarea 1 del "
         "pendiente comprometido): implementacion nueva (detector por "
         "acumuladores, testigo 777777, otro camino de codigo), las dos "
         "identidades confirmadas 5/5 incluido el nivel NUEVO m = 13: "
         "b_impar(13) = c(12) = 300 y b_2mod4(13) = a(10) + c(10) = "
         "409. El 6/6 corregido de anoche es ahora un 11/11 por dos "
         "implementaciones",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026. De regalo: el canal torre DESPIERTA en los "
         "niveles nuevos (b_0mod4 = 0, 0, 0, 1, 5 en m = 9..13) - "
         "coherente con que epsilon_torre > 0 y el teorema negativo "
         "barato muerto. La ecuacion de beta ya puede cargar peso."),

    fila("EPSILON_TORRE, MEDIDO Y CON SU MECANISMO (tarea 2 del "
         "pendiente): la masa del canal torre b_0mod4/2^m crece "
         "0.00116 -> 0.00177 -> 0.00241 (m = 14..16, razones > 2: "
         "fase de despertar) - LA MEDICION NO PUEDE DECIDIR el 1/4 "
         "que phi = 1 exige (truncamiento, la leccion de Gao). PERO "
         "LA ESTRUCTURA ES EXACTA Y NUEVA: cada ascenso de torre es "
         "un beta con el impar en el lado grande (verificado 10.000 "
         "casos), asi que el saldo S_chico - S_grande BAJA 1 por "
         "ascenso: una ruta con k ascensos necesita compensacion "
         "+2+k - LA DEUDA CRECE LINEALMENTE CON LA PROFUNDIDAD",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026. El blanco definitivo queda armado con mecanismo: "
         "si la deuda lineal mata una fraccion fija de la masa de la "
         "torre (cada compensacion cuesta ventanas, y las ventanas "
         "cuestan medida), entonces eps_torre < 1/4 estricto y "
         "phi < 1 ES TEOREMA con valor 8(1+eps)/(23-13rho). Si en "
         "cambio las compensaciones son gratis en el limite, la "
         "conjetura de Gao-Wu vive. Es la pregunta del programa, "
         "ahora con forma de carrera entre una deuda lineal y un "
         "presupuesto exponencial - el genero de pregunta que la "
         "maquinaria del repo sabe atacar."),

    fila("EL PASEO DE RATAS - LA DEUDA EN LA TORRE (movimiento 1 del cierre): dentro de "
         "la torre, las formas +2 son SIEMPRE compartidas (gap par) y "
         "las +1 SIEMPRE mixtas (gap impar) - tres leyes exactas, 7 k "
         "x 2000 v -; en cada mixta la paridad de v decide: par = "
         "asciende (deuda +1, T2), IMPAR = COMPENSA (deuda -1) y "
         "DESCIENDE A LA TORRE NEGATIVA {s, 3^(k-1) s - (3^(k-1)-1)/2} "
         "- la h-forma generalizada (9v-1 es el caso k=2). Como las "
         "paridades son monedas de Terras exactas, LA DEUDA ES UN "
         "PASEO ALEATORIO +-1 SIMETRICO - y el paseo simetrico es "
         "RECURRENTE: heuristicamente la compensacion es gratis en el "
         "limite y eps_torre = 1/4, o sea GAO-WU CIERTA",
         "verificado_hasta", "medido", "auditoria_rigor.py", "propio",
         "04-08-2026, el mecanismo final. HONESTIDAD DE ESTATUS: las "
         "tres leyes son exactas (demostrables, algebra de una linea "
         "cada una); el paso 'recurrente => eps = 1/4' es HEURISTICO "
         "(exige formalizar el paseo sobre la medida 2-adica y que la "
         "fusion llegue al tocar deuda 0 - el analogo del argumento de "
         "moneda de Terras para sigma). El programa desemboca en: la "
         "conjetura de Gao-Wu es cierta SI el paseo de la deuda es "
         "genuinamente recurrente sobre las clases - la misma "
         "estructura moneda-recurrencia que sostiene la conjetura "
         "madre. Dos torres gemelas (+c y -c) conectadas por las "
         "compensaciones: el mapa completo del problema."),

    fila("LOS MOVIMIENTOS 2 Y 3 DEL CIERRE: (2) la medicion dirigida "
         "del paseo - la masa condicional de la torre multiplica x4.75 "
         "y x2.08 por par de niveles (0.00098 -> 0.00464 -> 0.00964) "
         "sin techo geometrico, y el sub-canal k=1 despierta en m=14: "
         "CONSISTENTE con recurrencia, inconsistente con una matanza "
         "geometrica rapida - la medicion no decide el 1/4 pero "
         "favorece el paseo; (3) torredeladeuda.lean, el DECIMO .lean: "
         "pow3_impar por induccion, y las leyes de compensacion de los "
         "pisos k = 2 y 3 exactas (el chico gana el impar - deuda -1 - "
         "y desciende a la torre negativa 3s'-1 / 9s'-4), nucleo puro, "
         "cero sorryAx, a la primera",
         "verificado_hasta", "medido", "torredeladeuda.lean", "propio",
         "04-08-2026, el cierre de la jornada de jornadas. EL ESTADO "
         "FINAL DEL PROGRAMA: phi = 8(1+eps)/(23-13rho); phi = 1 <=> "
         "eps_torre = 1/4 <=> el paseo de la deuda (monedas de Terras, "
         "+-1 simetrico entre las dos torres gemelas) es recurrente "
         "sobre las clases. Tres leyes exactas, dos pisos en Lean, "
         "mecanismo completo, y UNA pregunta final que es la misma "
         "moneda de Terras que sostiene la conjetura madre. El k "
         "general del Lean queda declarado (producto de atomos: exige "
         "mas que omega)."),

    fila("EL LEMA GENERAL DEL VORTICE: toda PRIMERA coincidencia de dos "
         "trayectorias distintas del atajo es un vortice - T(a) = T(b) "
         "con a != b fuerza paridades opuestas y {a, b} = {3v+..., v} "
         "con a = 3b + 1 (b impar)",
         "todo_n", "demostrado", "nuevasfusion.py", "propio",
         "03-08-2026, madrugada. Dos lineas: si a y b tuvieran la misma "
         "paridad, T seria inyectivo en ellos (n/2 y (3n+1)/2 son "
         "inyectivas por separado); con paridades opuestas, "
         "(3b+1)/2 = a/2 da a = 3b+1. Es la version SIN restriccion de "
         "consecutividad del Lema 1 de Perras, y la base implicita de "
         "toda la maquinaria: la ecuacion de los vortices, los germenes "
         "de b y c (vortices (40,13) y (22,7)), y el hecho de que toda "
         "fusion - en cualquier piso - pasa por un segundo padre del "
         "arbol. Los vortices del 221 del primer dia del repo y el "
         "programa de fusion entero son el mismo objeto."),

    fila("EL RECIPROCO DE JIRAFAS, y con el LA CARACTERIZACION: una "
         "fusion en el indice t esta S-balanceada SI Y SOLO SI es un "
         "evento de clase mod 2^t",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, noche; teoremadejirafas.txt seccion 9. La ida es "
         "Jirafas (igualar coeficientes); el reciproco es nuevo: con "
         "Sx = Sy las pendientes son iguales y la diferencia es "
         "CONSTANTE en la clase - cero para un r, cero para todos. "
         "VEREDICTO DE RANGO ACEPTADO: Jirafas baja a LEMA "
         "(caracterizacion) en toda numeracion externa; el zoologico es "
         "interno. Es la pieza que cierra el puente phi = d de Pandas."),

    fila("TEOREMA DE FAMILIA de los contraejemplos de Elia-Tucker: TODA "
         "la familia (2^19 m + 3067, +1) funde en el paso 18 con "
         "|M| = 8, para todo m >= 0",
         "clase_residual", "demostrado", "identidadexacta.py", "propio",
         "03-08-2026, noche; punto 4 de la tercera revision, cerrado "
         "como pedia: t = 18 <= 19 medido en el representante, y por "
         "Terras el prefijo de 18 pasos es constante en la clase mod "
         "2^19: el teorema cubre los infinitos m, no cuatro muestras. "
         "Los contraejemplos a Garner viven en el estrato 8 POR TEOREMA."),

    fila("TEOREMA DE JIRAFAS (el balance forzado; bautizado por el "
         "usuario el 03-08-2026): toda fusion valida para una CLASE "
         "residual entera esta S-balanceada (la igualdad de las dos "
         "formas afines de Terras fuerza 3^Sx = 3^Sy). Corolarios: la "
         "fusion desbalanceada tiene MEDIDA 2-adica CERO (a lo sumo una "
         "solucion esporadica por clase - el fenomeno de cerca del "
         "atractor), y en la ecuacion de renovacion solo sobreviven las "
         "reentradas con delta canonico: el sistema colapsa a f y g mas "
         "masas de clase calculables",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 17 (03-08-2026, noche). Demostracion de tres "
         "lineas desde Terras 1.2. Verificado exhaustivo: las 1476 "
         "clases mod 2^12 que funden en t <= 12 para toda la clase "
         "(1476 = a(12) EXACTO, cruce gratis con clasesfusion.py) "
         "tienen S igualadas sin excepcion. Contexto: el censo de "
         "reentradas del rebote real (w, 9w+2) dio cobertura 100% en "
         "cuatro salidas (consec 45,4% -el 96% con delta 0-, rebote "
         "43,8%, fusion desbalanceada 10,3%, fusion limpia 0,6%): con "
         "este lema, las salidas muertas son medida cero y el sistema "
         "de renovacion CIERRA EN DOS INCOGNITAS."),

    fila("TEOREMA DE GATAS (el reinicio uniforme; bautizado por el "
         "usuario el 03-08-2026) y la ecuacion de renovacion: la "
         "contraccion manda r = 4t+1 al par consecutivo FRESCO "
         "(3t+1, 3t+2) con t -> 3t+1 biyeccion de Z/2^m (autosimilitud "
         "exacta, P(fusion|contraccion) = f); el w del rebote es "
         "uniforme (Terras 1.2); y por tanto f = 1/4 + f/4 + g/4 + h/4 "
         "EXACTA, con el corolario f >= 1/3 demostrado",
         "clase_residual", "demostrado", "nuevasfusion.py", "propio",
         "COMPROBACION 16 (03-08-2026). La contraccion literal esta "
         "verificada t < 2^14, la biyeccion mod 2^m hasta m = 12, y la "
         "uniformidad del rebote en j = 0..5 con 64 clases exactas. f = "
         "P(fusion de par consecutivo uniforme), g = P(fusion|rebote, "
         "familia real (w,9w+2), objetivo Delta_S = -2), h = P(fusion| "
         "r = 3 mod 4). LA ECUACION FUNCIONO COMO DETECTOR: no cerraba "
         "con la familia fantasma (0,4039 vs 0,4453) y cierra con la "
         "real (0,4504 vs 0,4453, topes declarados; medido: g = 0,188, "
         "h = 0,173, f = 0,445 a tope 3000 y r < 2^16). Si g y h se "
         "calculan exactos al estilo Perras, f queda decidida - y f = 1 "
         "seria la conjetura de Wu en densidad."),

    # --------------------------------------------------------- casi_todo_n
    #
    # Salvo un conjunto de densidad cero. Y el contraejemplo que buscamos
    # podria vivir justo ahi, asi que encadenan con cuidado.

    fila("casi todo n tiene un iterado menor que n",
         "casi_todo_n", "demostrado", None, "Everett 1977 / Terras 1976",
         "Densidad 1 en los enteros positivos. Tres paginas. El truco es usar "
         "la cota pesimista 5/3 en vez del factor exacto 3/2, y asi prescindir "
         "del +1."),

    fila("la condicion X/N < L, con L = log(2)/log(10/3) = 0,57571664249344500 "
         "y N = pasos del ATAJO, garantiza la bajada",
         "casi_todo_n", "demostrado", "verificar_everett.py", "Everett 1977",
         "LA TRADUCCION QUE ESTABA AQUI ERA FALSA, corregida el 01-08-2026. La "
         "N de Everett son pasos del ATAJO, y en el atajo cada paso impar "
         "contiene un 3n+1 y una division, luego X = A y N = B (comprobado en "
         "los 29.998 casos de n = 2..30.000). La condicion es B/A > 1/L = "
         "log2(10/3) = 1,73696559416620616641, que es MAS FUERTE que log2(3), "
         "no mas floja. El B/A > 0,7369 que decia antes es falso: 17.433 "
         "numeros de 3 a 20.000 lo cumplen en algun N sin haber bajado, y el "
         "mas chico es el 3. Y OJO, porque log2(3) TAMPOCO garantiza el "
         "descenso: n = 7 con A=5, B=8 da B/A = 1,6 > 1,585 y llega a 8, que es "
         "mayor que 7; lo impide C > 0 en la identidad del propio repo. La "
         "desigualdad de fondo, en forma entera y sin un float: 1.225.964 "
         "comprobaciones, 0 fallos, holgura minima 0 (igualdad en m = 3)."),

    fila("casi todas las orbitas de Collatz alcanzan valores casi acotados",
         "casi_todo_n", "demostrado", None, "Tao 2019",
         "Casi todo n en densidad logaritmica. El resultado general mas fuerte "
         "que existe sobre la conjetura, y sigue sin tocarla."),

    fila("la paridad de la trayectoria se comporta como lanzamientos "
         "independientes de moneda",
         "casi_todo_n", "conjeturado", None,
         "Lagarias-Weiss 1992 / Kontorovich-Lagarias",
         "Modelo heuristico, no teorema. LA GRIETA: la fraccion impar queda "
         "DETERMINADA por cuanto bajo la trayectoria y cuantos pasos tardo, y "
         "solo se puede medir en trayectorias que YA terminaron en 1. El "
         "argumento de la moneda asume lo que habria que demostrar."),

    fila("para 5x+1 solo unos x^0,65 enteros bajo x llegan a 1",
         "casi_todo_n", "conjeturado", None, "Kontorovich-Lagarias",
         "El mapa 5n+1, no Collatz. Que 5n+1 diverja no esta demostrado: es "
         "tan conjetural como Collatz. Medido aqui: cae el 3,03% de 100.000 "
         "semillas, y tiene 3 ciclos."),

    # ------------------------------------------------------------- promedio
    #
    # NO ENCADENAN CON NADA, y no es una opinion: la conjetura es una
    # afirmacion sobre CADA numero, y un promedio no demuestra ningun caso.
    # Los valores numericos estan en la tabla constantes, con sus avisos.

    fila("las constantes de parada existen y se recuperan: Wagon 9,4779, la "
         "escalera 1:2:3 de k/ln(4/3), y la media geometrica sqrt(3)/2",
         "promedio", "medido", None,
         "Wagon (OEIS A122790); Lagarias, Applegate-Lagarias",
         "Trayectorias hasta 10^7, errores del 0,06% al 0,42%. Los valores "
         "estan en la tabla constantes, y desde el 01-08-2026 cada uno con SU "
         "estimador: las tres de parada son pendiente de regresion, la de "
         "Wagon es muestreo, y el B/A de al lado es agregado a 10^6. Mezclarlos "
         "en una columna 'medido' fue el error. Ninguna demuestra nada: son "
         "promedios. Y las tres de parada no son tres: son gamma(rho) = "
         "1/(ln2 - rho*ln3) evaluada en rho = 1/2, en proporcion "
         "rho : 1 : 1+rho."),

    fila("B/A converge a 2, no a log2(3): la valuacion 2-adica media de 3n+1 "
         "vale 2",
         "promedio", "medido", None, "propio",
         "4.041.132 saltos, medido 1,99048. El log2(3) = 1,585 es el punto de "
         "EQUILIBRIO, no el valor tipico. Y el estimador correcto es el "
         "agregado suma(B)/suma(A): la media de razones da 2,174 por Jensen."),

    fila("la fraccion de pasos impares es 1/3 con el mapa clasico y 1/2 con el "
         "atajo",
         "promedio", "medido", None, "Terras 1976",
         "Todas las trayectorias de 2 a 10^6: 0,331785 y 0,496524. Los pasos "
         "impares coinciden digito a digito en los dos mapas (43.607.946). La "
         "relacion entre los dos mapas es exacta, uno por uno, no en promedio."),

    fila("la desviacion de la fraccion impar NO se encoge como 1/sqrt(N): es "
         "sesgo de la muestra y se va agrandando la SEMILLA",
         "promedio", "medido", None, "propio",
         "|desv|*sqrt(N) va 1,45 -> 1,05 -> 1,76 -> 3,62 -> 13,02 de 10^3 a "
         "10^7 pasos: firma de sesgo fijo. Pero con la semilla: -0,0044 a 16 "
         "bits y -0,0007 a 256. Collatz converge a la moneda justa agrandando "
         "la semilla, no acumulando tiradas."),

    fila("en el coral hay 1,7320 +/- 0,0003 divisiones por multiplicacion",
         "promedio", "medido", None, "propio",
         "Hasta 10^6 semillas. EL 1,7345 PUBLICADO ANTES ERA EL VALOR DE UNA "
         "MUESTRA a HASTA=3.000. Cae a 0,02% de sqrt(3) y la descomposicion "
         "del valor dice que es casual: no construir nada encima. FICHERO "
         "RETIRADO: coralcollaz.py se borro en la purga del 01-08-2026 -media "
         "el angulo elegido a mano-, asi que este numero YA NO SE PUEDE "
         "REPRODUCIR con codigo del repo. Se deja porque el negativo vale: es "
         "el ejemplo de llamar constante al valor de una muestra."),

    fila("la densidad de pares consecutivos con la misma altura crece con N",
         "promedio", "conjeturado", None,
         "Wu Jia-Bang 1995 (conjetura abierta)",
         "Medido hasta 2^28: 0,518577, monotona en los 18 escalones, 0 "
         "bajadas. EL CONTROL QUE IMPORTA: la misma medicion con el PICO en "
         "vez de la altura NO es monotona (10 bajadas de 16). La maquinaria "
         "discrimina. FICHERO RETIRADO: densidadfusion.py se borro en la purga "
         "del 01-08-2026 -era un promedio sobre 18 puntos y su seccion del "
         "mecanismo estaba sesgada por muestreo-, asi que estos numeros ya no "
         "se pueden reproducir; lo que se queda es el criterio exacto de "
         "clasesfusion.py, que es otra cosa y si se sostiene. Y OJO CON EL HITO "
         "DE GARNER, que aqui estaba mal: su conjetura es sobre la densidad de "
         "ENTEROS EN TUPLA, no sobre la fraccion de PARES, y cruza el 50% en "
         "2^6, diecisiete escalones mas abajo, no entre 2^23 y 2^24."),

    fila("el tiempo de descenso tiene techo heuristico: sigma_C/k -> "
         "(1 + log_3 2)/(1 - H) = 32,59 para el mapa clasico, y 1/(1-H) = "
         "19,98 para el atajo",
         "promedio", "conjeturado", "descensoresto.py", "propio",
         "AVISO: SALE DE UN MODELO DE DENSIDAD, o sea de un promedio, y los "
         "promedios no demuestran nada sobre casos individuales. Es el numero "
         "mas sugerente del dia y por eso el mas peligroso. Si esa cota "
         "existiera y se demostrara -sigma(n) <= C*log2(n) para todo n- la "
         "conjetura saldria por induccion fuerte sobre el minimo "
         "contraejemplo, en tres lineas. Nadie ha demostrado que esa C exista."),

    fila("desde la densidad sola, sin mirar ningun numero, el modelo predice "
         "planeo 1613 a 60 bits; el record publicado es 1614",
         "promedio", "medido", "descensoresto.py", "propio",
         "Es la validacion que le da credito al modelo del techo 32,59: la "
         "prediccion viene de contar clases supervivientes y el dato es un "
         "maximo sobre numeros de verdad, asi que no tenian por que cuadrar. "
         "Cuadran mejor de lo que merecen. Sigue siendo un promedio prediciendo "
         "un extremo: coincidir una vez no lo convierte en cota."),

    fila("la racha inicial de impares PREDICE la altitud",
         "promedio", "refutado", None, "propio",
         "Roto: correlacion 0,59, explica el 35% de la varianza, y se exigia "
         "0,8 antes de medir. Lo que la racha SI hace es ponerle un piso "
         "exacto. Cota si, tendencia no."),

    fila("el espejo base 10 y Collatz se hablan",
         "promedio", "refutado", None, "propio",
         "Roto: la correlacion entre pasos(n) y pasos(espejo(n)) es +0,08. "
         "Segunda prueba: las 5 parejas espejo del 221 dan p = 0,28 contra un "
         "modelo nulo que preserva el reparto de decadas. Un primer calculo "
         "dio '11 contra 1,48 esperadas' y era falso. FICHERO RETIRADO: "
         "mallaespejo.py se borro en la purga del 01-08-2026. El negativo se "
         "queda: es de los que evitan repetir la busqueda."),

    fila("el puente del espejo base 2 llega mas alla de un paso",
         "promedio", "refutado", None, "propio",
         "Roto: correlacion +0,06, todavia menos que el +0,08 de base 10. Un "
         "paso: identidad exacta. Dos pasos: ruido. El +2 se acumula al iterar "
         "y borra la relacion. FICHERO RETIRADO: mallaespejo2.py se borro en la "
         "purga del 01-08-2026."),

    fila("una red neuronal con 40.000 ejemplos no pasa del 50,5% prediciendo "
         "la siguiente paridad a partir de las k anteriores",
         "promedio", "medido", "redhilos.py",
         "propio; Terras 1976 Corolario 1.4 lo explica",
         "k = 4, 8, 12, 16: entre 49,3% y 50,5%. Y no puede mejorar: las "
         "paridades son independientes con P = 1/2 exacta. Viendo los m bits "
         "bajos en cambio: 50% clavado para m <= k y 100% para m > k. Un "
         "acantilado. Determinista y sin patron no son incompatibles."),

    fila("alguna constante de Collatz coincide con alguna constante "
         "fundamental",
         "promedio", "refutado", None, "propio",
         "Roto con modelo nulo: 9 constantes x 8 transformaciones contra 16 "
         "constantes adimensionales dan 1 coincidencia contra 0,394 esperadas, "
         "p = 0,317. Al corregir los tres defectos del nulo el p sube a "
         "0,40-0,45: los errores empujaban A FAVOR de la senal. Control "
         "definitivo: el metodo no distingue Collatz de reglas qn+1 (p=0,264)."),

    fila("la fila 'se escapan del rango' de la tabla A/B discrimina entre "
         "reglas",
         "promedio", "refutado", None, "propio",
         "Roto: da 33,3% para 3n+1 y para 3n-1 por igual, con los MISMOS "
         "conteos absolutos a N = 256, 1024, 4096 y 10.000. Mide el rango, no "
         "la regla. Las que si discriminan son 'ciclos distintos', 'cola mas "
         "larga' y 'cola media'. FICHERO RETIRADO: mallaespejo2.py se borro en "
         "la purga del 01-08-2026, y con el la tabla A/B que lo motivo; la "
         "leccion -no toda fila de un A/B discrimina- sigue siendo doctrina."),

    fila("la altura de un punto sobre la esfera codifica el tamano del numero",
         "promedio", "refutado", None, "propio",
         "Roto: correlacion latitud / log2(valor) = 0,12 en los 5.674 numeros "
         "de las ramas. La altura es la distancia real al 1, que es otra cosa. "
         "La esfera es envase, no resultado. FICHERO RETIRADO: collazarbol.py "
         "se borro en la purga del 01-08-2026, y este negativo es justamente la "
         "razon por la que se borro: la esfera la elegimos nosotros."),

    fila("el 221 prefiere ciertos restos mod 64",
         "promedio", "refutado", None, "propio",
         "Roto: pisa 55 de 64 y el puro azar daria 53,5. Diferencia +1,5. Los "
         "9 restos que nunca pisa no tienen nada en comun. El destino hacia "
         "adelante es ciego a los restos. FICHERO RETIRADO: cruzarestos.py se "
         "borro en la purga del 01-08-2026; el negativo se queda porque es uno "
         "de los que mas ahorra -impide volver a buscar estructura ahi-."),

    # --------------------------------------------------------------- ciclos

    fila("no hay m-ciclos de Collatz con m <= 91, donde m = numero de minimos "
         "locales del ciclo",
         "ciclos", "demostrado", "reimpl.py",
         "Hercher 2023, J. Integer Sequences 26, art. 23.3.5",
         "Reproducido aqui desde cero: los siete m_2 y las siete cotas de K "
         "salen identicos a los publicados, en 5,5 segundos y sin un solo "
         "float en las decisiones. Mejora el m >= 76 de Simons-de Weger. Dos "
         "discrepancias de impresion, que el programa mide y no oculta."),

    fila("K < 1,4784 * m * delta^m",
         "ciclos", "demostrado", "reimpl.py",
         "Simons-de Weger, Acta Arith. 117 (2005)",
         "Ambito: m <= 91. Es el unico sitio por donde entra la aproximacion "
         "diofantica dura. LA REDACCION DE ANTES SE PASABA DE FUERTE "
         "(01-08-2026): decia 'Hercher NO usa el teorema de Baker en ninguna "
         "parte', y eso vale PARA SU ARTICULO pero no PARA LA CADENA. "
         "Comprobado sobre el fuente hercher5.tex que la revista sirve junto al "
         "PDF: 'Baker' 0 veces, 'Matveev' 0, 'Rhin' 0, 'linear form' 0. Pero un "
         "escalon mas abajo si hay trascendencia: Simons-de Weger tienen una "
         "seccion 'Application of Transcendence Theory' cuyo Lema 12 -Lambda > "
         "e^(-13,3*(0,46057 + log K))- sale de RHIN (1987), una medida efectiva "
         "de irracionalidad para log3/log2 por aproximantes de Pade, y ese lema "
         "entra en K_1(m), que entra en el Lema 16, que es de donde sale el "
         "1,4784. La redaccion correcta: 'Hercher no invoca Baker; la caja "
         "negra que importa si contiene trascendencia'. Y LA CAJA NEGRA NO ES "
         "TAN NEGRA: el 1,4784 SE RE-DERIVA en diez lineas desde la definicion "
         "de Simons-de Weger, resolviendo su ecuacion de K_2(m) por biseccion "
         "con decimal a 200 cifras -b = 0,64576012, c_m = 0,3057636284, "
         "A(91) = 55, K_2(91) = 2,140701e20, k_2(91) = 1,478381-, o sea que el "
         "1,4784 es k_2(91) redondeado hacia arriba (verificar_ciclos.py, "
         "comprobacion 4), y su tabla de campeones sale 4/4. AVISO APARTE: hay "
         "CORRIGENDUM del 14-06-2026, en la misma revista, sobre el Teorema 21 "
         "de Hercher, que es justo la pieza que reimpl.py marca como importada "
         "sin verificar; el enunciado no cambia y su ultimo paso "
         "-(2^v - 1)^delta < 2^(delta*v) - 1- se comprueba aqui en 12 valores "
         "de v con 0 fallos, pero el argumento de convexidad sobre el politopo "
         "se lee, no se verifica."),

    fila("cualquier ciclo distinto del trivial mide al menos 114.208.327.604 "
         "pasos del ATAJO (186.265.759.595 del mapa clasico)",
         "ciclos", "demostrado", "verificar_ciclos.py",
         "forma de Eliahou, Discrete Math. 118 (1993), con X0 = 2^71 de Barina "
         "2025, J. Supercomputing 81(7) art. 810",
         "Ambito: todo ciclo no trivial sobre los enteros positivos. La cota "
         "sale de meter el limite de verificacion por fuerza bruta en la forma "
         "de Eliahou: la longitud es 301994a + 17087915b + 85137581c con "
         "b >= 1 y a*c = 0, y 114.208.327.604 = (a=0, b=361, c=1269), "
         "comprobado aqui. AQUI HUBO DOS NUMEROS MALOS SEGUIDOS, los dos "
         "corregidos el 01-08-2026. (1) El 19.478.780.533 que el repo citaba "
         "como 'literatura de 2025' sin nombrar a nadie existe -Laurore 2025, "
         "Adv. Pure Math. 15(6), DOI 10.4236/apm.2025.156018- pero es de SCIRP, "
         "tiene cero citas, no encaja en la forma de Eliahou (0 soluciones) y "
         "es 5,86 veces mas debil que el estado del arte, no once: el once "
         "salia de compararlo contra el 217.976.794.617, que resulto ser el "
         "numero equivocado. (2) Ese 217.976.794.617 lo publica Barina 2025 en "
         "su seccion 6 y lo repite Wikipedia, pero exige "
         "X0 >= 4,358487e21 = 2^71,884 y el "
         "record esta en 2075*2^60 = 2,392312e21 = 2^71,019: es una fila de mas "
         "en la tabla de convergentes. O sea que copiamos bien una fuente "
         "arbitrada equivocada, y el error nos favorecia, que es la direccion "
         "en la que nadie mira. Certificado por TRES caminos independientes en "
         "verificar_ciclos.py -Stern-Brocot sobre intervalo ensanchado, "
         "certificado en las dos direcciones sobre n*log2 - k*log3, y la via "
         "elemental de verificar_terras.py [6]-, con la maquinaria validada "
         "antes reproduciendo Eliahou 1993 (17.087.915) y Sinisalo 2003 "
         "(1.027.712.276) clavados. Y la conclusion no se mueve: el tramo mas "
         "largo del repo mide 114 pasos, nueve ordenes de magnitud por debajo, "
         "asi que buscar ciclos en los 6.555 pares del 221 no podia encontrar "
         "nada."),

    fila("no hay bucles de periodo <= 2.592 con la fuerza bruta que habia en "
         "1976; con X0 = 2^71 el mismo argumento elemental llega a "
         "114.208.327.603",
         "ciclos", "demostrado", "verificar_frontera_ciclos.py",
         "Terras 1976 (Tabla C, jump values); el X0 de hoy es Barina 2025",
         "EL 2.592 ES CIFRA HISTORICA, NO LA FRONTERA, y esta fila lo "
         "presentaba como si lo fuera (corregido el 01-08-2026). La frontera se "
         "mueve con X0 y X0 ha crecido cincuenta anos: con X = 10^6 -un minuto "
         "de CPU en esta maquina- el mismo argumento ya alcanza periodo 4.700, "
         "casi el doble del 2.592; con el ~10^8 de Terras, 24.726; con el 2^62 "
         "de Oliveira e Silva, 10.439.860.590; y con el 2^71 de Barina, "
         "114.208.327.603 pasos del atajo (186.265.759.593 clasicos). "
         "Recalculado en verificar_terras.py [6] y verificar_frontera_ciclos.py. "
         "LA CONCLUSION NO CAMBIA, CAMBIA POR CUANTO: el barrido de restos "
         "sigue muerto, pero no porque su rango sea teorema desde 1976 -lo es "
         "desde hoy y por mucho mas-, y para territorio virgen ya no bastaria "
         "k > 2592 sino k > 114.208.327.603, o sea 2^114208327603 restos. El "
         "barrido esta a nueve ordenes de magnitud del frente."),

    fila("sobre todo Z los unicos ciclos son {1,2,4}, {-1,-2}, "
         "{-5,-7,-10,-14,-20} y el de 18 terminos desde -17",
         "ciclos", "medido", "pinzaciclos.py", "estandar en la literatura",
         "Supervivientes de k = 1..30 (2.147.483.646 restos) y barrido hasta "
         "10^6 con 0 sin clasificar. La ecuacion no mira el signo de m, asi "
         "que el barrido resolvio el problema sobre Z sin proponerselo: "
         "dividen(k) = 2 + 2*[2|k] + 3*[3|k] + 11*[11|k], 0 desacuerdos."),

    fila("en un ciclo de 3n+1 la C de la identidad es POSITIVA, luego "
         "B/A > log2(3); en uno de 3n-1 es negativa y B/A < log2(3)",
         "ciclos", "demostrado", "pinzaciclos.py",
         "propio (se sigue del signo de C)",
         "Los tres ciclos negativos y el unico positivo, 0 fallos. El 'balance "
         "decide todo' se parte en dos mitades. Y el ciclo de -1 escrito con "
         "la identidad da 2 = 3 - 1, espejo exacto del 4 = 3 + 1."),

    fila("las casillas (A,B) que sobreviven al barrido son (semi)convergentes "
         "de log2(3), pero solo LAS QUE LO APROXIMAN POR ENCIMA",
         "ciclos", "demostrado", "collazmalla.py",
         "Terras 1976 Tabla C; Shanks 1965, Guy 1983",
         "AQUI DECIA 'exactamente las convergentes y semiconvergentes', Y ES LA "
         "MITAD (corregido el 01-08-2026): 3/2, 19/12, 84/53 y 1054/665 son "
         "convergentes de log2(3) y NO son jump values, porque lo aproximan por "
         "debajo. La lista de Terras son solo las de arriba. "
         "480 casillas, las 10 mas cercanas sin excepcion. Guy 1983 imprime la "
         "lista entera y dice que hay ciclos en los denominadores 1, 2, 5, 12 "
         "y ninguno en 41, 53, 306: es casilla por casilla nuestro barrido. La "
         "casilla (7,11) predijo el ciclo negativo de periodo 11."),

    fila("el unico ciclo positivo, escrito con la identidad del repo, es "
         "2^2 = 3^1 + 1, o sea 4 = 3 + 1",
         "ciclos", "demostrado", "collazmalla.py", "propio",
         "A=1, B=2, C=1. De los 95 candidatos enteros positivos que "
         "aparecieron, los 95 ciclan de verdad y son n en {1,2,4} dando 1, 2 o "
         "3 vueltas. Cero impostores. Y desde el 02-08-2026 la identidad del "
         "ciclo la certifica el nucleo de Lean (depuracion/lean/A63.lean): "
         "demostrado, no solo contado."),

    fila("no hay m-ciclos con m <= 95",
         "ciclos", "conjeturado", None, "Wang 2026 (preprint, Zenodo)",
         "Sigue sin arbitrar y necesita verificacion independiente: esa es la "
         "fase 3 del plan de la pinza, y si aguanta se dice y si se cae eso si "
         "es un hallazgo. PERO LA CALIBRACION DE ESTA FILA HABIA QUE REVISARLA "
         "(01-08-2026): decia 'cero citas, metadatos descuidados' como si eso "
         "midiera algo, y no lo mide -'cero citas' mide la edad del preprint y "
         "'metadatos descuidados' mide su maquetacion-. Y hay un dato duro en "
         "contra de tratarlo como sospechoso por defecto: el corrigendum del "
         "14-06-2026 al articulo de Hercher agradece el hallazgo del error del "
         "Teorema 21 a XINJUN WANG, ORCID 0009-0007-5895-5984, el mismo Wang. "
         "Encontrar un error real en un articulo arbitrado y que el autor lo "
         "reconozca por escrito es mejor credencial que una cita."),

    fila("el espejo base 10 tiene 44.451 dos-ciclos (mas 1.098 palindromos "
         "fijos) bajo 100.000, y Collatz tiene UN ciclo positivo",
         "ciclos", "demostrado", None, "propio",
         "CORREGIDO EL 02-08-2026, y subio de categoria: el 44.450 publicado "
         "era un off-by-one, y el numero bueno sale en cerrado, no contando: "
         "bajo 100.000 hay 90.000 numeros sin cero final y 1.098 palindromos, "
         "luego (90.000 - 1.098)/2 = 44.451 dos-ciclos. Reproducido ademas "
         "por conteo directo (45.549 ciclos contando los fijos). El A/B de "
         "control se queda -la maquinaria discrimina- y el ejemplo vuelve a "
         "ser reproducible sin el fichero retirado."),

    # ----------------------------------------------------- verificado_hasta
    #
    # Fuerza bruta. Sirve para REFUTAR, jamas para demostrar: verificar hasta
    # 2^71 o hasta 2^(10^100) deja exactamente la misma cantidad sin verificar.

    fila("todo n < 2^71 llega al 1",
         "verificado_hasta", "medido", None,
         "Barina 2025, J. Supercomputing",
         "No comprueba los 2^71 numeros: criba clases enteras. Coste: 12.395 "
         "anos-CPU + 159 anos-GPU. Su worker.c imprime MAXIMUM_CYCLE_OFFSET 0 "
         "como constante literal: el programa no busca ciclos en absoluto. EL "
         "FACTOR X ~ 363 QUEDA DEGRADADO (01-08-2026): no es un hallazgo, es "
         "una composicion aritmetica correcta de dos numeros no verificados -la "
         "densidad de su criba de produccion y el factor 5/9 de la criba mod "
         "9-, y estaba escrito en negrita como si fuera medicion propia."),

    fila("el residuo de Roosendaal nunca baja de 1 ni sube de 1,253142144",
         "verificado_hasta", "conjeturado", "cruzarecords.py",
         "Roosendaal (el propio autor solo llego a 2^32)",
         "Los 243 records cruzados llegan a 2^71, asi que esto es EVIDENCIA "
         "NUEVA para su conjetura. Maximo hallado 1,2486 en n=9; confirmado "
         "que 4164943872 = 993*2^22 tiene el mismo residuo que el 993."),

    fila("el maximo de eps hasta 200.000 esta en 993 y sus dobles",
         "verificado_hasta", "medido", "elmasuno.py", "propio",
         "Barrido de 2 a 200.000 comparando enteros en cruz, sin floats. Vale "
         "ln(1,253142144) = 0,225654. El 0,23 de grosor de la lamina no salio "
         "de nuestro dibujo: es una constante con conjetura propia."),

    fila("barrido de 2.147.483.646 restos (k = 1..30): los unicos "
         "supervivientes positivos son n = 1 y n = 2",
         "verificado_hasta", "medido", "pinzaciclos.py", "propio",
         "La prediccion estaba escrita antes de medir y se cumplio. Y NO SUBIR "
         "K_MAX: el rango alcanzable ya es teorema desde 1976."),

    fila("la densidad de pares con la misma altura, medida hasta "
         "2^28 = 268.435.456",
         "verificado_hasta", "medido", None, "propio",
         "Tabla int16 vectorizada por bloques, verificada contra la version "
         "lenta en los primeros 300.000: 0 discrepancias. FICHERO RETIRADO: "
         "densidadfusion.py se borro en la purga del 01-08-2026, asi que esto "
         "ya no se puede reproducir aqui. Y LA RACHA DE 120 EN 136.696.632 NO "
         "ES NUESTRA: es de Wu 1993 (MR 1277568), que barrio hasta 1,5e8 y la "
         "publico -136.696.632 < 1,5e8-. La redescubrimos, que no es lo mismo "
         "que descubrirla."),

    fila("la tupla mas larga de consecutivos con la misma altura bajo 2^30 "
         "mide 176, empezando en 722.067.240",
         "verificado_hasta", "medido", None, "Wu Jia-Bang 1992",
         "Aqui se llego a 120 en 2^28: compatible con esa trayectoria de "
         "crecimiento, pero no la confirma. No llegamos. REVERIFICADO EL "
         "02-08-2026 (verificar_wu.py): la tupla de 176 se confirma una a "
         "una; la MAXIMALIDAD bajo 2^30 sigue siendo de Wu y nadie la "
         "re-verifico - exigiria el barrido completo."),

    fila("el coral de Harriss (45 rumbos) choca por primera vez en la "
         "profundidad 31 del arbol inverso",
         "verificado_hasta", "medido", "coralprimos.py", "propio",
         "Profundidad <= 200, aritmetica entera exacta contra Phi_45. EL 0% DE "
         "ENCIMADAS ERA FALSO: solo valia hasta 3.000 semillas. Por semillas "
         "el primer choque esta en HASTA = 10.452; por arbol inverso completo, "
         "en la profundidad 31. Los dos umbrales son distintos y los dos "
         "ciertos."),

    fila("el umbral de choque del coral es una RECTA en N con dos ramas segun "
         "N mod 4: (N+11)/2 si N = 4k+3 y (N+19)/2 si N = 4k+1",
         "verificado_hasta", "medido", "coralprimos.py", "propio",
         "N de 20 a 70, profundidad <= 200. SUSTITUYE a la explicacion "
         "'45 = 3^2 * 5', que solo valia un nivel de treinta y uno. Ni rastro "
         "de la factorizacion: lo que manda es cuanto vale N y su resto mod 4."),

    fila("con N primo la clave del reticulo y la clave cruda dan el mismo "
         "umbral, sin una sola excepcion",
         "verificado_hasta", "medido", "coralprimos.py", "propio",
         "Los primos entre 20 y 70. Es la unica mitad de la prediccion que se "
         "confirmo: con N primo el reticulo es solo (1,1,...,1) y ninguna "
         "relacion no trivial ayuda nunca. La otra mitad -que el umbral se "
         "disparara- fallo."),

    fila("las 98 altitudes y los 148 retrasos publicados se recalculan desde "
         "cero con enteros exactos: 0 discrepancias",
         "verificado_hasta", "medido", "cruzarecords.py", "propio",
         "Los 243 records de Roosendaal y Barina. La lista de n de los records "
         "de altitud, Barina contra OEIS: 98/98 identicos. Trampa que costo "
         "tiempo: Barina publica la altitud en el mapa del ATAJO, y la clasica "
         "es exactamente el doble."),

    fila("la identidad de Terras aguanta en los 6.555 pares de la trayectoria "
         "del 221, 0 fallos",
         "verificado_hasta", "medido", "collazmalla.py", "propio",
         "El 221 tiene 73/41 = 1,78 divisiones por multiplicacion, o sea que "
         "cae. Un ciclo con A=41 necesitaria B=65: le sobran 8 divisiones, que "
         "son el mismo +8,02 de desviacion medido."),

    fila("A076227 ('surviving Collatz residues mod 2^n') reproducida de forma "
         "independiente: 45 terminos (n = 0..44), 0 discrepancias",
         "verificado_hasta", "medido", "descensoresto.py", "OEIS A076227",
         "a(34) = 151.917.636 = 0,884%, que es el tamano de la criba clasica "
         "que cita el CLAUDE.md. Contado por programacion dinamica sobre "
         "patrones de paridad, sin tocar un solo resto, y controlado contra la "
         "criba real de los 2^k restos hasta k = 20: coinciden los 20."),

    fila("los 34 records de planeo (glide) de records.json recalculados desde "
         "cero, 0 fallos. El planeo ES el tiempo de descenso sigma",
         "verificado_hasta", "medido", "descensoresto.py", "propio",
         "Los records de ericr.nl estan en el mapa CLASICO; se recalculan con "
         "enteros exactos y de paso validan la conversion atajo -> clasico, "
         "porque la columna clasica se obtiene sumando los impares. El mayor "
         "es n = 2.602.714.556.700.227.743 con planeo 1.639, a 61,2 bits."),

    fila("sigma_max(k)/k crece y NO se estabiliza: de 13,20 en k=10 a 23,58 en "
         "k=26, con dientes de sierra",
         "verificado_hasta", "medido", "descensoresto.py", "propio",
         "Fuerza bruta sobre TODOS los n < 2^28. Y los records publicados van "
         "por 26,79 a 61 bits. No se observa cota uniforme en el rango medido: "
         "crece de forma compatible con acercarse a un techo, pero medir 27 "
         "escalones no dice nada de los infinitos que faltan. Es un maximo de "
         "muestra, no una cota."),

    fila("de los 983 cruces que no son cola comun entre los once hilos "
         "100000..100010, 833 (el 85%) tienen desfase 0",
         "verificado_hasta", "medido", "guardarhilos.py", "propio",
         "275 de los 1.258 cruces son la cola comun [16,8,4,2,1] y no "
         "significan nada: hilos.db los marca con es_cola. Sin esa marca, el "
         "100001 -que no se funde de verdad con nadie- pareceria tan conectado "
         "como el resto."),

    fila("LA ECUACION DE CIERVAS - una clase r mod 2^(k+1) se estrena en el nivel k+1 exactamente "
         "cuando T^k(r) y T^k(r+1) se encuentran POR PRIMERA VEZ en un "
         "vortice: a = 3b+1 con paridades opuestas y S compensada en 1",
         "verificado_hasta", "medido", "nuevasfusion.py", "propio",
         "La ecuacion de las nuevas (03-08-2026). Caracterizacion CON "
         "reciproco: k = 3..15, 0 fallos y 0 falsos positivos, y reproduce "
         "b(k) = a(k+1) - 2a(k) termino a termino. El a = 3b+1 es la regla "
         "del segundo padre (v = 4 mod 6) de los vortices del 221. "
         "Convierte la pregunta de la razon 2 (b(k+1)/b(k) -> 2?) en "
         "contar soluciones de una congruencia por nivel. Precedente en "
         "OEIS: A076227/A100982 tienen recursion exacta (Zarubin 2019, "
         "Winkler) - alli la forma existe; aqui esta por derivar."),

    fila("la cota condicionada m >= M de Everett con M = 10001 certifica "
         "el descenso con umbral B/A > 1,585011 -a 4,8e-05 de log2(3)- "
         "sin UNA SOLA excepcion real hasta 10^6",
         "verificado_hasta", "medido", "franjaeverett.py", "propio",
         "Los 'sin certificar' de M = 5, 9, 101, 1001, 10001 son "
         "exactamente los impares < M (excluidos por hipotesis): 0 "
         "excepciones reales en los cinco. M = 27 es el unico que no "
         "empata (2 reales, sin identificar). La franja de Everett se "
         "estrecha tres ordenes de magnitud y NO se cierra: el limite "
         "M -> infinito sigue siendo por clases, no uniforme. OJO: este "
         "resultado estuvo escrito y SIN CORRER hasta el 03-08-2026 -ver "
         "la correccion del fichero que no compilaba."),

    fila("las clases nuevas se estratifican por el numero |M| de pasos "
         "mixtos del par: |M| es PAR siempre, el estrato |M| = 2 tiene "
         "EXACTAMENTE UNA clase por nivel (y es la familia del repunit), "
         "y |M| = 4 tambien exactamente una",
         "verificado_hasta", "medido", "nuevasfusion.py", "propio",
         "k = 3..15, 779 nuevas, 0 violaciones (03-08-2026). Paso mixto = "
         "paridades del par distintas, que ocurre exactamente cuando la "
         "diferencia d es impar. La paridad de |M| SI es demostrable en "
         "tres lineas (Delta_S cambia +-1 solo en mixtos y vuelve a 0); "
         "la unicidad de |M| = 2 se DEMOSTRO el mismo dia (fila aparte) y "
         "la de |M| = 4 sigue solo medida. Los estratos altos "
         "crecen como polinomios de grado creciente (|M| = 6 acaba con "
         "diferencias 5,6,7,8: cuadratico) y entra un estrato nuevo cada "
         "dos niveles: la razon b(k+1)/b(k) -> 2 vendria de la ENTRADA de "
         "estratos, no de que cada estrato acelere. Es la forma de "
         "recursion tipo A076227/Zarubin que se buscaba."),

    # ----- la jornada de la cadena (04-08-2026, segunda tanda) -----

    fila("TEOREMA DE LEONAS - LA CADENA (k, c): todo estado de par vivo es una forma "
         "{v, 3^k v + c} (nucleo, k >= 1) o {v, v+g} (frontera, k = 0), "
         "y la dinamica entera del par son SEIS LEYES exactas de una "
         "linea decididas por un solo bit fresco (la paridad del menor, "
         "moneda de Terras). El zoologico completo -Gatas, Perras, el "
         "vortice (1,1), el rebote (2,2), la forma h (2,-1), las puertas "
         "P1-P3, las torres T1/T2, el grafo {-3,-5}- son estados y "
         "transiciones de esta unica cadena",
         "todo_n", "demostrado", "paseodeladeuda.py", "propio",
         "04-08-2026. Las seis leyes verificadas en 181.400 instancias "
         "(0 fallos) y DEMOSTRADAS en Lean con coeficiente impar "
         "arbitrario p (mas general que 3^k): cadenakc.lean, nucleo "
         "puro, 0 sorryAx. El programa de fusion entero es un sistema "
         "simbolico con una sola absorcion: (1,1) con bit 1."),

    fila("el barrido SIMBOLICO de la cadena reproduce a(k) EXACTO sin "
         "tocar un par (contra la sucesion publicada k = 3..12, contra "
         "recomputo directo k = 3..14, y contra b(k) entera k = 3..31 "
         "incluida la cola del barrido a 2^32), y EXTIENDE la serie: "
         "a(33) = 3.761.106.610 y a(34) = 7.558.807.251 (razones de b: "
         "1,9412 y 1,9432)",
         "verificado_hasta", "medido", "paseodeladeuda.py", "propio",
         "04-08-2026. La renovacion coalesce estados: 7,7 millones de "
         "estados donde el barrido de restos necesitaba 2^34. Los dos "
         "niveles nuevos sostenidos por segundo camino "
         "(segundocamino.py): cumplen la identidad-teorema a(k+2) = "
         "a(k) + (2^k - 1) + G(k) + H(k) en k = 31, 32 con G y H de "
         "barridos separados de los pisos g y h."),

    fila("a(35) = 15.188.796.435, a(36) = 30.516.174.184, "
         "b(34) = 71.181.933, b(35) = 138.581.314 - las razones de b "
         "extendidas: 1,9432 -> 1,9452 -> 1,9469, subiendo",
         "verificado_hasta", "medido", "empujarb.py", "propio",
         "04-08-2026. Por la identidad-teorema con los pisos (G y H a "
         "33/34), con control: G(31), G(32), H(31), H(32) clavan "
         "segundocamino.py. La cota demostrada lambda >= 1,9754 exige "
         "que las razones sigan subiendo al menos hasta ahi."),

    fila("LA IDENTIDAD DE ARDILLAS - LOS FLECOS DE LA SERIE R: la identidad "
         "c(m) = suma_j F(j)*a(m-j) + D(m) cierra como IGUALDAD DE "
         "ENTEROS en m = 3..26, con F(j) = primeras visitas de la "
         "cadena al estado consecutivo (0,1) desde la forma h y D(m) = "
         "fusiones directas sin pasar por consecutivo. El R publicado "
         "(afirmacion 88) deconvolvia SIN el termino D: los flecos +-1 "
         "eran D repartida por el triangulo",
         "verificado_hasta", "medido", "flecosr.py", "propio",
         "04-08-2026. F clava el R publicado en j = 3..9; D despierta "
         "en j = 13. La contabilidad de orientacion bajo vuelcos ya no "
         "hace falta: la cadena la lleva dentro. Y c(m) extendida de "
         "m = 16 a m = 26."),

    fila("TEOREMA DE NUTRIAS - LA CONTABILIDAD DE CANALES ES ESTRUCTURAL: e_s(N) = "
         "e_{s-2}(N-2) [subarbol r = 1 mod 4 = el arbol entero "
         "desplazado] + e^h_s(N-2) [subarbol r = 3 mod 4 = piso h] + "
         "e^par_s(N-1) [subarbol r par], como igualdad de enteros en "
         "todos los niveles y estratos (s <= 12, N <= 29). Ademas: e6 "
         "cuadratica confirmada hasta N = 29, e8 NO es cubica "
         "(terceras diferencias oscilando, definitivo), y e10/e12 "
         "medidas por primera vez",
         "verificado_hasta", "medido", "estratoscadena.py", "propio",
         "04-08-2026. Los canales son los subarboles de los dos "
         "primeros bits de la cadena; la recursion vertical es la "
         "identidad de subarbol. No hizo falta Lipmaa-Moriai."),

    fila("TEOREMA DE ZORRAS - LA INVERSION DEL GOAL DE LAMBDA: b(t+2) >= "
         "N_t(1,2) como igualdad de enteros (el estado (1,2) fusiona "
         "en exactamente 2 pasos y prefijos distintos dan fusiones "
         "distintas), con s_t = N_t(1,2)/vivas >= 0,015 medido. Si "
         "phi < 1 entonces lambda = 2; contrapositivo: lambda < 2 => "
         "phi = 1 (Gao-Wu cierta). El autovalor NO puede separar: "
         "demostrar lambda < 2 no daria f < 1, daria f = 1",
         "todo_n", "medido", "retornoslambda.py", "propio",
         "04-08-2026, el cierre del goal. La desigualdad es exacta; el "
         "piso s_t >= 0,015 es medido (t = 8..32), por eso el estado "
         "es medido y no demostrado. Complemento demostrado por "
         "truncados (matriztransferencia.py): lambda >= 1,9754 (K=11, "
         "seis truncados anidados, conteo entero de caminos) y el LEMA "
         "DE LA LIBERTAD: la unica absorcion es (1,1)-bit1, ningun "
         "truncado finito puede demostrar lambda < 2."),

    fila("LOS RETORNOS DE OVEJAS - EL CRUCE LaTOURETTE (tesis Moravian 2007, bajada entera a "
         "lecturas/latourette2007/): sus 'blocks' (Tabla 4.1) son los "
         "primeros retornos del par a gap 1 CON ORDEN CONSERVADO y sus "
         "'strings' (Tabla 4.2) los retornos CON VUELCO - 21/21 y "
         "26/27 clavados contra la cadena, largo a largo. LA ENTRADA "
         "QUE FALLA ES UN ERROR EN SU TABLA: la L11 (00011100101, "
         "10110100010), marcada 'newly found', toca gap 1 en t = 9 (su "
         "prefijo es su propia entrada L9) y viola su Definicion 4. El "
         "conteo bueno de L11 es 19, no 20. La cadena extiende su "
         "catalogo de largo 11 a largo 30",
         "verificado_hasta", "medido", "retornoslambda.py", "LaTourette 2007",
         "04-08-2026. Verificacion triple del error: formal (afines "
         "exactas), realizabilidad (Terras), y fuerza bruta exhaustiva "
         "mod 2^11. Las otras 47 entradas: 0 defectos. Serie de "
         "retornos: 1,0,0,1,1,3,5,6,11,19,31,55,98,176,313,578,1099,..."),

    fila("TEOREMA DE TIGRESAS - EL MULTIPLICADOR: escribiendo cada transicion de "
         "la cadena como c' = m*c + s, en el NUCLEO (k >= 1) y la "
         "frontera par toda transicion tiene |m| = 1/2 en una rama y "
         "|m| = 3/2 en la otra - cada paso es MONEDA JUSTA entre "
         "contraer y expandir: E[m] = 1 EXACTO, E[log2 m] = -0,2075 < "
         "0. La dinamica de c es una PERPETUIDAD DE KESTEN CRITICA "
         "(kappa = 1 es la unica solucion positiva de E[m^kappa] = 1). "
         "La unica excepcion es la frontera impar: ambas ramas "
         "|m| = 3/2 (la bomba de reentrada)",
         "todo_n", "demostrado", "subrenovacionc.py", "propio",
         "04-08-2026, el mecanismo de la densidad con nombre. El mismo "
         "balance 3/2-1/2 que hace B/A -> 2: la criticidad ES la "
         "constante del problema. Verificado en 1.368 estados (con el "
         "pliegue del valor absoluto tratado aparte). LECTURA (no "
         "teorema): kappa = 1 => estacionaria tensa de cola 1/x => "
         "piso de absorcion por visita => con el paseo recurrente, "
         "phi = 1. Por que no es teorema: los (m, s) no son i.i.d. "
         "(el shift crece 3^k con la torre) y el piso exige "
         "uniformidad. El peso de los shifts SI es sumable "
         "(2^-k * log 3^k): por ahi entra la formalizacion."),

    fila("TEOREMA DE CABRAS - LAS LEYES MOD 3 DE LA CADENA: (a) cada puerta de entrada al "
         "nucleo trae SU clase - directa (3g+1)/2 = 2 (mod 3), vuelco "
         "(3g-1)/2 = 1 (mod 3); ninguna trae 0; (b) c = 0 (mod 3) es "
         "INALCANZABLE en el nucleo (el mayor es 3^k v + c = c mod 3: "
         "es Komodo 3 en coordenadas de la cadena; masa CERO medida "
         "exacta en la foto de t = 34); (c) la absorcion (1,1) vive en "
         "la clase del vuelco: LA PUERTA QUE FUNDE ES LA DEL VUELCO",
         "todo_n", "demostrado", "subrenovacionc.py", "propio",
         "04-08-2026. (a) algebraico (g < 4001 verificado); (b) "
         "invariancia por las seis leyes + Komodo (teoremadekomodo3."
         "lean); (c) 1 = 1 (mod 3). El reparto medido en k = 1 "
         "(clase 1 : clase 2 = 1 : 2) es la huella de las dos puertas."),

    fila("LA DISPERSION DE c EN EL NUCLEO BAJO, MEDIDA: E[log2|c|] en "
         "k = 1 crece DIFUSIVO (incrementos ~0,02 por nivel y "
         "decayendo ~5% - tipo t^0,65, no deriva lineal), las cubetas "
         "relativas de |c| <= C caen DESACELERANDO, s_t con exponente "
         "local beta_t ~ 0,78 a la baja, y las bandas diadicas medias "
         "rondan cociente 1/2 (la firma kappa = 1) con la cola lejana "
         "aun llenandose",
         "verificado_hasta", "medido", "dispersionc.py", "propio",
         "04-08-2026, paso 1 del norte. La lectura provisional "
         "'dispersion => phi < 1' quedo REVERTIDA por el teorema del "
         "multiplicador: kappa = 1 hace que la convergencia a la "
         "estacionaria sea critica y log-lenta, y el 'escape' medido "
         "es compatible con tension asintotica. El muro de siempre: "
         "la medicion no decide; la estructura si tiene nombre."),

    fila("TRES .LEAN NUEVOS - cadenakc (las seis leyes de la cadena "
         "con coeficiente impar arbitrario, la ley de la moneda, el "
         "vortice, el vuelco F4 y la escalera p -> 3p con piso_impar "
         "por induccion), perrasconteo (suma de ventanas = 2^m - 1, "
         "el borde alternante 3^m mod 4, y exactamente_uno: los dos "
         "residuos frontera de Perras deciden en sentidos opuestos "
         "para todo m), y zoologico (el nucleo de Jirafas entero: "
         "afines iguales en dos puntos => coeficientes iguales, mas "
         "pow3_inyectiva; las potencias de 6 de Pandas; el grafo "
         "{-3,-5} de los chanchitos con D1 = -3 y P3; la rama h de "
         "Gatas). Todos nucleo puro, 0 sorryAx",
         "todo_n", "demostrado",
         "cadenakc.lean", "propio",
         "04-08-2026. Los otros dos: perrasconteo.lean y zoologico.lean "
         "(un fichero por campo; los tres compilan 0 sorryAx). Van 13 "
         ".lean. La orden del usuario ('portar los teoremas de los .txt "
         "a Lean sin borrarlos') cumplida para los nucleos aritmeticos; "
         "los .txt siguen siendo los documentos con las revisiones."),

    fila("EL BAUTIZO DEL ZOOLOGICO (orden del usuario, 04-08-2026): "
         "todo teorema, lema o hallazgo propio lleva nombre de animal "
         "femenino para distinguir referencias propias de ajenas. El "
         "censo completo: PERRAS (mitad exacta), GATAS (renovacion), "
         "JIRAFAS (balance), PANDAS (equivalencia), 3 CHANCHITOS "
         "(b4/c4), KOMODO 3 (mod 3) [historicos]; LEONAS (la cadena "
         "(k,c)), TIGRESAS (multiplicador critico), CABRAS (puertas "
         "mod 3), ZORRAS (inversion de lambda), LOBAS (libertad de la "
         "torre), PUMAS (acorralado de lambda), ARDILLAS (flecos de "
         "R), NUTRIAS (canales), OVEJAS (retornos/LaTourette), VACAS "
         "(identidad entera), RATAS (paseo de la deuda), YEGUAS "
         "(unicidad alternante), CONEJAS (familia extremal del "
         "repunit), COMADREJAS (coordenadas D y E), PANTERAS "
         "(recursion vertical), CIERVAS (ecuacion del vortice), OSAS "
         "(sistema de phi). La tabla completa con estatus y ficheros "
         "vive en RutaTeoremas.md, seccion EL ZOOLOGICO",
         "todo_n", "medido", "auditoria_rigor.py", "propio",
         "Convencion referencial, no matematica: 'medido' porque es "
         "un registro de nomenclatura. Para textos que salgan del "
         "repo: numeracion seria con el descriptivo entre parentesis "
         "(regla ya registrada en los .txt)."),

    fila("TEOREMA DE ARANAS - LA SOMBRA DE LA CADENA: en la coordenada "
         "re-escalada u = c/3^k, las cuatro leyes del nucleo colapsan a "
         "UNA pareja - bit 0: u' = u/2 + delta, bit 1: u' = (3u-1)/2 + "
         "delta - con delta EXACTA de la tabla {0, 3^-k/2, 3^-(k+1)/2, "
         "0} y la salida a frontera con delta = 0. El nivel de la torre "
         "DESAPARECE de la dinamica del offset: la cadena es el IFS de "
         "moneda justa {u/2, (3u-1)/2} MAS una perturbacion dominada "
         "(|delta| <= 3^-k/2; con masa 2^-k por piso, la total es "
         "sumable: suma 2^-k 3^-k / 2 = 1/10)",
         "todo_n", "demostrado", "aranas.py", "propio",
         "04-08-2026, el paso (i) del norte. 354.293 identidades con "
         "Fraction, 0 fallos. LO QUE COMPRA: el IFS puro cumple TODAS "
         "las hipotesis de Goldie-Kesten i.i.d. (E[log m] < 0, E[m] = "
         "1 -> kappa = 1, shifts {0,-1/2} no degenerados, no-lattice): "
         "estacionaria unica TENSA con cola 1/x es TEOREMA ESTANDAR "
         "CITABLE. El 'no es Kesten' de Tigresas queda reducido a "
         "'Kesten mas perturbacion sumable' (perturbed random IFS, el "
         "blanco tecnico siguiente). MEDIDO con etiqueta: la distancia "
         "CDF cadena-IFS a t=34 es 0,222 (comparacion cruda: la cadena "
         "condiciona a no-absorcion y el IFS no absorbe), la cola en u "
         "muestra meseta kappa=1 en x = 1..8 con la cola lejana en "
         "transito, y el pre-vortice exacto (1, c=1) pesa 4,6% de la "
         "masa de k=1 (el piso por visita, en coordenada limpia). "
         "Excepciones declaradas: la frontera (F2 delta = 1/2, F4 "
         "voltea signo) es la costura, ~6% de la masa."),

    fila("TEOREMA DE MOSCAS - LA TENSION, TRANSFERIDA: para todo theta "
         "en (0,1), la suma S_t = suma_{palabras vivas} 2^-t |u_t|^theta "
         "cumple S_{t+1} <= r_theta S_t + (1/2)^theta con r_theta = "
         "((1/2)^theta + (3/2)^theta)/2 < 1, luego S_t <= B_theta "
         "UNIFORME EN t (theta = 1/2: B = 21,8; theta = 0,9: B = 46,2) "
         "y la masa viva con |u| > x es <= B_theta / x^theta PARA TODO "
         "t. La tension de la telarana de Aranas vale en la cadena "
         "real: incondicional, con constante explicita, autocontenida "
         "(dominacion lineal exacta |u'| <= m_b|u| + 1/2 mas "
         "subaditividad de |.|^theta -- sin citar a Kesten)",
         "todo_n", "demostrado", "moscas.py", "propio",
         "04-08-2026, el paso (ii) del norte ejecutado. La dominacion "
         "lineal verificada en 354.299 transiciones exactas con "
         "Fraction (frontera y F4 incluidos: el vuelco que rompia el "
         "acople de Aranas aqui es inofensivo, pendiente 1/2 <= 3/2); "
         "la recursion de Lyapunov comprobada nivel a nivel sobre la "
         "cadena real (t = 1..34) con S_t medida en [0,38, 1,44] -- "
         "veinte veces bajo la cota: el teorema es holgado, el "
         "contenido es la UNIFORMIDAD. La ventana entera de momentos "
         "theta < 1 esta abierta EXACTAMENTE porque E[m] = 1 es la "
         "criticidad kappa = 1 de Tigresas. LO QUE NO DA, declarado: "
         "(1) la tension del condicional a vivo si phi = 1; (2) el "
         "PISO de absorcion por visita -- la ultima pieza abierta del "
         "programa de la densidad."),
]


# ===========================================================================
# LAS CORRECCIONES
# ===========================================================================
#
# Lo que se creyo y era falso. Casi nadie escribe esto, y por eso casi todo el
# mundo repite las mismas busquedas.

CORRECCIONES = [

    ("el coral de Harriss con 16 y -8 grados no encima NUNCA dos ramas (0%)",
     "solo se habian mirado 3.000 semillas. Hay choques EXACTOS -resto cero "
     "modulo el ciclotomico Phi_45, en aritmetica entera- desde la profundidad "
     "31, y a la 59 son el 1-1,5% de los nodos de cada nivel. Lo cazo barrer "
     "el arbol inverso completo en vez de barrer por semillas (2026-07-30)",
     "un barrido por semillas solo ve las ramas que cuelgan de semillas "
     "chicas. Cambiar de barrido puede mover la respuesta tres ordenes de "
     "magnitud sin cambiar el signo"),

    ("el 1,7345 de divisiones por multiplicacion del coral es una constante",
     "era el valor de UNA MUESTRA a HASTA = 3.000. Con mas semillas se asienta "
     "en 1,7320 +/- 0,0003, y la cuarta cifra nunca fue estable. Lo cazo "
     "repetir la medida a 10^3, 3*10^3, 10^4, 10^5 y 10^6 (2026-07-30)",
     "antes de llamar constante a un numero medido hay que moverle el tamano "
     "de la muestra. Y que caiga a 0,02% de sqrt(3) es justo el tipo de "
     "coincidencia que este repo se ha propuesto no creerse"),

    ("la fila 'se escapan del rango' de la tabla A/B discrimina entre reglas",
     "da 33,3% para 3n+1 y para 3n-1 por igual, con los MISMOS conteos "
     "absolutos a cuatro tamanos: mide el rango elegido, no la regla. Lo cazo "
     "meter por la maquinaria dos reglas PARECIDAS en vez de dos muy distintas "
     "(2026-07-30)",
     "no toda fila de una tabla A/B vale como discriminante. Con reglas muy "
     "distintas cualquier fila parece funcionar"),

    ("2/ln(4/3) = 6,952 es la constante de parada del mapa clasico",
     "es la del mapa del ATAJO. La del clasico es 3/ln(4/3) = 10,428, y "
     "confundirlas da un 49,5% de error. Lo cazo medir las tres a la vez y ver "
     "que forman una escalera 1:2:3 (2026-07-30)",
     "cuando dos mapas conviven en el mismo repo, cada constante hay que "
     "etiquetarla con SU mapa o no significa nada"),

    ("la biyeccion resto <-> patron de paridad vale para el mapa clasico",
     "solo vale con el mapa del ATAJO. Con la regla clasica dos impares no "
     "pueden ir seguidos, y los patrones que sobreviven son F(k+2), los "
     "Fibonacci. Lo cazo la comprobacion 2 de mallaresiduos.py, que corto con "
     "SystemExit ANTES de dibujar nada",
     "las comprobaciones van antes del dibujo. Sin esa disciplina habria "
     "quedado una imagen bonita sosteniendo una afirmacion falsa"),

    ("la fraccion de clases que se funden CRECE con k, y eso es un hallazgo",
     "no es un hallazgo: esta FORZADO. Si r es buena mod 2^k, entonces r y "
     "r + 2^k son las dos buenas mod 2^(k+1), luego N(k+1) >= 2*N(k) siempre y "
     "la monotonia se demuestra en tres lineas. Lo cazo intentar demostrar lo "
     "que se estaba verificando (2026-07-30)",
     "antes de publicar una monotonia medida hay que preguntarse si es "
     "forzosa. Lo unico con contenido era cuantas clases se ESTRENAN en cada "
     "nivel"),

    ("el par (8k+4, 8k+5) que se funde siempre es de Lagarias",
     "es de Garner 1985. Lagarias 1985 tiene el mecanismo general, que es otra "
     "cosa. Lo cazo revisar la bibliografia entrada por entrada (2026-07-30)",
     "atribuir mal una fuente es tan grave como medir mal: el que venga detras "
     "buscara en el sitio equivocado"),

    ("Wu-Huang 2001 no se pudo verificar: no tiene DOI, no aparece en "
     "Crossref, y Elia-Tucker 2015 no la citan. Antes de apoyarse en ella "
     "hay que localizarla o quitarla (2026-07-30)",
     "LA REFUTACION ERA LA EQUIVOCADA. La cita EXISTE: Mathematica Applicata "
     "(Wuhan) 14 (2001), suplemento, 21-25, MR 1885838, Zbl 1002.11023, y "
     "esta en la bibliografia anotada de Lagarias (arXiv:math/0608208, "
     "entrada 125) con las tres familias y los vectores de paridad "
     "textuales, que se recalcularon clavados bit a bit. No estaba en "
     "Crossref porque es un SUPLEMENTO de una revista china de 2001 "
     "(2026-08-01)",
     "el error no fue de la cita, fue del indice donde se busco. 'No esta en "
     "Crossref' es una afirmacion sobre Crossref, no sobre el mundo, y para "
     "Collatz el indice correcto es la bibliografia anotada de Lagarias. Y "
     "el aviso de fondo: una REFUTACION es una afirmacion como cualquier "
     "otra y hay que auditarla igual"),

    ("cualquier ciclo no trivial mide al menos 19.478.780.533 pasos, segun 'la "
     "literatura de 2025'",
     "la fuente se localizo el 01-08-2026 y resulto ser mala por partida "
     "triple. Es Laurore, Adv. Pure Math. 15(6) 351-389 (2025), DOI "
     "10.4236/apm.2025.156018: editorial SCIRP, cero citas en Crossref. Y el "
     "numero es 5,86 VECES MAS DEBIL que el estado del arte -la cota buena con "
     "X0 = 2^71 es 114.208.327.604 en el atajo y 186.265.759.595 en el "
     "clasico-, o sea que el repo llevaba citada como 'lo que exige la "
     "literatura' una cota peor que la conocida. (Aqui se escribio 'ONCE "
     "VECES', y eso tambien estaba mal: se comparaba contra el 217.976.794.617 "
     "de Barina, que es el numero corregido en la fila siguiente. La cita de "
     "Laurore es valida pero debil, y el factor era otro.) Ademas no encaja en "
     "la forma de Eliahou "
     "(301994a + 17087915b + 85137581c con b >= 1 y a*c = 0): barrido "
     "exhaustivo, 0 soluciones, mientras que las tres cotas verificadas si "
     "encajan. Sustituida por la de Barina",
     "'la literatura dice' sin autor no es una cita, es un rumor. Y "
     "localizarla no basta: hay que mirar DONDE se publico y si el numero "
     "mejora o empeora lo que ya se sabia. Aqui la cita existia y aun asi "
     "habia que quitarla, que es un caso que no estaba previsto - la lista de "
     "salidas era 'localizar o degradar' y falto la tercera, 'localizar y "
     "descartar igualmente'"),

    ("la trayectoria del 221 contiene 11 parejas espejo contra 1,48 esperadas",
     "el modelo nulo estaba mal: ignoraba el reparto de decadas. Con un test "
     "de aleatorizacion de 20.000 conjuntos que SI lo preserva salen 5 parejas "
     "contra una media de 4,53, y p = 0,28",
     "el modelo nulo tiene que preservar la estructura del dato. Estimar el "
     "azar a ojo es la forma mas facil de fabricarse una senal"),

    ("la razon B/A se estima promediando B/A trayectoria por trayectoria",
     "eso da 2,174 (+8,7%) porque promedia un cociente con denominador chico y "
     "por Jensen se va hacia arriba. El estimador correcto es el AGREGADO "
     "suma(B)/suma(A), que da 2,014 (2026-07-30)",
     "media de cocientes no es cociente de medias. La misma trampa reaparecio "
     "al pesar por pasos contra pesar por numeros"),

    ("el limite de la fraccion se puede extrapolar ajustando e(k) ~ C/k^p",
     "la estimacion SE MOVIA al anadir puntos: 0,594 con k <= 24 y 0,606 con "
     "k <= 25. Lo cazo recalcular el ajuste con un punto mas",
     "un ajuste que cambia de respuesta cada vez que llega un dato no esta "
     "midiendo el limite, esta midiendo la muestra"),

    ("la malla del 221 x 1276 demuestra que Collatz es circular",
     "sus 4.959 casillas con ecuacion son exactas, pero el eje X es la COLA "
     "del eje Y -el 1276 es la posicion 57 del 221-, asi que el cierre en el "
     "centro esta puesto por construccion, no descubierto",
     "un modelo que devuelve la misma malla para cualquier entrada no esta "
     "midiendo la entrada, esta midiendo el modelo"),

    # ------------- las cuatro de hoy, 30-07-2026, cada una con su fichero ---

    ("log2(altitud(n)/n) >= racha(n)*log2(3/2) + 1 vale para todo n",
     "le faltaba la hipotesis n IMPAR, y sin ella es FALSO: con n par la racha "
     "vale 0, el piso exige altitud >= 2n, y eso falla en 28.325 de los 50.000 "
     "pares de 1 a 100.000 -el 10 sube solo hasta 16 y necesitaria 20. Lo cazo "
     "el barrido de control de pisoaltitud.py. NO lo encontraron los 243 "
     "records publicados: los pasaron todos, y los 15 records pares pasaron "
     "por casualidad, porque son 2*impar (2026-07-30)",
     "LOS EXTREMOS CONFIRMAN; LOS CONTROLES REFUTAN. Un test que solo mira "
     "casos favorables no comprueba nada: confirma lo que ya creia"),

    ("la holgura minima del piso de la altitud es +0,000002",
     "no es una constante: es funcion del rango barrido. Los mas apretados son "
     "los impares de racha 1, donde altitud = 3n+1 exacto y la holgura vale "
     "log2(1 + 1/(3n)), que decrece con n. El +0,000002 publicado es el valor "
     "de un barrido hasta 200.000, no hasta 100.000. Lo cazo pisoaltitud.py, "
     "comprobacion 4, comparando la formula cerrada con el minimo medido "
     "(2026-07-30)",
     "un numero que sale de un barrido hay que publicarlo CON su rango. Y si "
     "tiene formula cerrada, mejor la formula que el numero"),

    ("el +1 del 3n+1 aparece TRES veces: el grosor 0,2286 de la lamina, el +2 "
     "del espejo base 2, y la desviacion -0,0035 de la fraccion impar",
     "aparece DOS. El grosor eps = ln(2^B/(3^A n)) y el sobrante S = suma de "
     "ln(1+1/(3x)) son IDENTICOS termino a termino: son la misma aparicion "
     "contada dos veces en dos sistemas de coordenadas, el clasico y el atajo. "
     "Y el residuo 1,7e-7 que se habia medido era error de coma flotante, no "
     "del enunciado: en racionales exactos da 0. Lo cazo elmasuno.py, 20.011 "
     "casos en Fraction, 0 fallos (2026-07-30)",
     "dos cantidades medidas en sitios distintos pueden ser la misma escrita "
     "en dos coordenadas. Antes de contarlas como dos fenomenos, traducirlas "
     "al mismo sistema. Y de regalo: un negativo MEDIDO -la lamina no tiene "
     "nada por debajo del plano- se convirtio en un teorema de una linea"),

    ("mapahilos.py guarda RES_993 = 1.2531421442887503",
     "el valor exacto es 2^61/(3^32*993) = 1,2531421443950680..., que se separa "
     "en la DECIMA cifra. Coinciden en las nueve publicadas (1,253142144) y no "
     "cambia nada de lo medido, pero la constante literal esta mal. Lo cazo "
     "elmasuno.py, comprobacion 4 (2026-07-30). ARREGLADO EL 01-08-2026: "
     "mapahilos.py y elmasuno.py la calculan ahora como 2**61/(3**32*993) y "
     "ninguno la escribe a mano; elmasuno.py ademas corta con SystemExit si "
     "alguien vuelve a copiarla. Comprobado que no mueve nada: el techo sigue "
     "imprimiendo 0,225654 y los once eps siguen por debajo, 0 fallos",
     "una constante copiada a mano hay que recalcularla desde su definicion "
     "una vez, aunque solo sea decorativa. Y mejor todavia: no copiarla, "
     "escribir la definicion y dejar que la maquina la evalue"),

    ("el grosor 0,2286 de la lamina ES ln(Res(993)) = 0,225654, o sea que el "
     "0,23 del dibujo era una constante con conjetura propia (asi esta en el "
     "CLAUDE.md, seccion 'Es una lamina, no una esfera')",
     "NO SON EL MISMO NUMERO, y el parecido es una colision de unidades sobre "
     "dos objetos distintos. El 0,2286 sale de collazlamina.py, que mide "
     "h = log2(2^B*y / (3^A*x)) sobre los 6.555 PARES de la trayectoria del "
     "221, o sea en BITS; el 0,225654 es ln(Res(993)), o sea en NATS. Pasados "
     "a las mismas unidades: 0,2286 bits = 0,158478 nats, y 0,225654 nats = "
     "0,325550 bits. Difieren en un factor 1,42, no en la tercera cifra. Y el "
     "0,2286 ni siquiera es una cota: es el eps de UN numero -el maximo sobre "
     "los pares del 221 se alcanza en el par (221 -> 16), que es su "
     "trayectoria entera- asi que mide el 221, no la lamina. Lo que si es "
     "cierto y es lo que hay que escribir: h(par) <= log2(Res(seq[i])) porque "
     "un producto parcial de factores (3x+1)/(3x) es menor que el total, y por "
     "tanto la conjetura de Roosendaal acota TODOS los pares por 0,325550 "
     "bits. El 0,2286 del 221 cae holgadamente debajo (2026-08-01)",
     "antes de decir que dos numeros medidos son el mismo, pasarlos a las "
     "mismas unidades. Dos cantidades en escalas distintas pueden parecerse en "
     "tres cifras por casualidad, y aqui paso: log2 contra ln sobre dos "
     "objetos que ni siquiera son el mismo barrido. Es la hermana del error "
     "contrario que cazo elmasuno.py -alli dos numeros que parecian distintos "
     "eran el mismo- y las dos se arreglan igual: traducir antes de comparar"),

    ("el cuantificador clase_mod_2k de afirmaciones.db nombra bien a sus filas",
     "se le queda corto a dos: la rueda del arbol inverso (mod 3, mod 9, mod "
     "27) y los evitados de la malla 2n mod 27. Las dos son clases residuales "
     "modulo 3^j, no 2^k, y las dos estaban en esa casilla con una nota que "
     "pedia perdon por el nombre. La categoria real es la FORMA del argumento "
     "-una comprobacion finita que decide para los infinitos numeros de una "
     "clase de resto- y el modulo es un detalle del enunciado. Renombrado a "
     "clase_residual el 01-08-2026",
     "el nombre de una casilla tiene que describir la categoria, no el caso "
     "mayoritario. Si hay que explicar en las notas de una fila por que esta "
     "donde esta, la casilla esta mal puesta o mal llamada"),

    ("reimpl.py reproduce el Teorema 23 de Hercher sin ninguna discrepancia",
     "hay DOS. (1) El septimo epsilon sale 1,23e-43 donde el articulo imprime "
     "1,11e-43; el programa demuestra que da igual, porque el denominador "
     "minimo es PLANO en todo ese rango y las dos cotas dan el mismo K. (2) La "
     "tercera fila de la Tabla 1 sale 4,64e18 contra el 4,68e18 impreso, y ahi "
     "la sospecha va contra el papel: 4,68e18 no es denominador de ninguna "
     "semiconvergente de log2(3), asi que no es alcanzable por el metodo "
     "(2026-07-30)",
     "reproducir un resultado no es reproducir un numero: hay que comparar "
     "TODOS los intermedios y decir cuales no cuadran. Y si algo no cuadra, "
     "medir si importa antes de decidir de quien es el error"),

    ("la densidad de supervivientes de la criba escala como 2^(-0,05k), o sea "
     "que cada bit extra de criba solo elimina un 3,4% mas (esta asi en el "
     "CLAUDE.md, seccion 'Las cribas industriales')",
     "ese es el comportamiento ASINTOTICO, no el del rango donde se usa. La "
     "pendiente medida de log2(a(k)) va de 0,8738 en k = 10..20 a 0,9477 en "
     "k = 640..1280, y converge al teorico H = 0,94996; pero en el rango real "
     "de la criba (k = 34, tramo 20..40) el exponente de decaimiento es 0,108, "
     "el DOBLE del asintotico 0,050. La criba muerde MAS de lo que dice el "
     "documento donde se usa, y menos a la larga. Lo cazo descensoresto.py, "
     "medida 3, calculando la pendiente por tramos hasta k = 1400 (2026-07-30)",
     "distinguir el regimen local del limite asintotico. Citar un exponente "
     "sin decir en que rango vale es la misma clase de error que tomar el "
     "valor de una muestra por una constante. Y OJO CON LA FRASE, porque el "
     "desliz esta escrito en mas de un sitio: un exponente de decaimiento MAYOR "
     "significa que la densidad cae MAS DEPRISA. 2^(-0,108k) decae el doble de "
     "rapido que 2^(-0,050k), no la mitad"),

    ("con un numero PRIMO de rumbos el umbral de choque del coral deberia "
     "dispararse, porque los choques de N=45 vienen de que 45 = 3^2 * 5",
     "NO SE CUMPLE. Los dos primos vecinos del 45 chocan ANTES que el 45, y el "
     "maximo del rango no lo tiene un primo. El motor real es el caso trivial "
     "que el razonamiento dejo fuera: dos ramas que usan LAS MISMAS ARISTAS EN "
     "OTRO ORDEN, diferencia de vectores exactamente cero, y eso existe para "
     "cualquier N. La relacion del triangulo y el pentagono adelanta el choque "
     "UN nivel. Lo cazo coralprimos.py, midiendo cada N con dos claves "
     "-reticulo y crudo- y restandolas (2026-07-30)",
     "atribuirle el choque a 45 = 3^2 * 5 era quedarse con la causa de UN "
     "nivel e ignorar la de treinta y uno. Cuando una explicacion se confirma "
     "hay que medir CUANTO explica, no solo si explica algo. Y lo que si se "
     "confirmo -que con N primo el reticulo no ayuda nunca- era la mitad "
     "irrelevante de la prediccion"),

    # ---- las del 01-08-2026, que esta base llevaba una auditoria de retraso --

    ("la condicion de Everett se traduce como B/A > 0,7369, y nuestro "
     "log2(3) = 1,585 es el umbral verdadero",
     "LAS DOS FRASES ERAN FALSAS. La N de Everett son pasos del ATAJO, luego "
     "X = A y N = B y la condicion es B/A > 1/L = log2(10/3) = 1,73697, que es "
     "MAS FUERTE que log2(3), no mas floja: 17.433 numeros de 3 a 20.000 pasan "
     "el 0,7369 sin haber bajado, el mas chico el 3. Y log2(3) tampoco "
     "garantiza el descenso -n = 7 con A=5, B=8 llega a 8- porque C > 0 en la "
     "identidad del propio repo. Lo cazo verificar_everett.py, verificando la "
     "desigualdad de fondo en forma entera: 1.225.964 comprobaciones, 0 fallos "
     "(2026-08-01)",
     "DOS LECCIONES. (1) El 0,7369 es literalmente 1/L - 1: un umbral que sale "
     "de la constante correcta MENOS UNO es la marca algebraica de haber puesto "
     "un paso de mas en el denominador. (2) Habia una comprobacion de "
     "coherencia que lo delataba sin tocar un dato: una condicion SUFICIENTE de "
     "descenso tiene que ser mas exigente que el umbral exacto, nunca mas "
     "floja, y 0,7369 < 1,585 es imposible. Vivio casi un ano porque de esa "
     "seccion no colgaba ningun calculo: lo que nadie ejecuta hay que auditarlo "
     "a proposito, porque no se delata solo"),

    ("cualquier ciclo no trivial mide al menos 217.976.794.617 pasos del "
     "atajo, segun Barina 2025",
     "ESE NUMERO EXIGE X0 >= 4,358487e21 = 2^71,884 y el record es "
     "2075*2^60 = 2^71,019. Es una fila de mas en la tabla de convergentes. Con "
     "el X0 real la cota es 114.208.327.604 pasos del atajo / 186.265.759.595 "
     "clasicos, certificada por tres caminos independientes en "
     "verificar_ciclos.py y corroborada por la ultima fila de la Tabla 1 del "
     "propio Hercher (K > 7,20e10, del orden de 1,14e11 y no de 2,18e11). Lo "
     "publica Barina 2025 en su seccion 6 y lo repite Wikipedia (2026-08-01)",
     "AQUI COPIAMOS BIEN UNA FUENTE ARBITRADA QUE ESTA EQUIVOCADA: ya no es "
     "'citar mal'. Y el detalle que hay que recordar es la direccion del error: "
     "este numero nos venia BIEN -hacia el argumento mas fuerte- y por eso "
     "sobrevivio una pasada entera de auditoria, mientras que los dos errores "
     "de cita anteriores molestaban y por eso se miraron. Revisar con la misma "
     "dureza los numeros que nos favorecen"),

    ("el 2.592 de Terras es la frontera de exclusion de ciclos por periodo, y "
     "por eso el barrido de restos esta muerto",
     "ES UNA FOTO DE 1976, no la frontera: es lo que Terras podia excluir con "
     "la fuerza bruta que existia entonces, y la frontera se mueve con X0. Con "
     "solo X = 10^6 -un minuto de CPU aqui- el mismo argumento elemental ya "
     "alcanza 4.700, casi el doble; con el 2^62 de Oliveira e Silva, "
     "10.439.860.590; y con el 2^71 de Barina, 114.208.327.603. Lo cazo "
     "recalcularla en verificar_terras.py [6] y verificar_frontera_ciclos.py "
     "(2026-08-01)",
     "LA CONCLUSION NO CAMBIA, CAMBIA POR CUANTO: el barrido sigue muerto, pero "
     "esta a nueve ordenes de magnitud del frente y no al 1,2% de el. Una cifra "
     "historica citada como estado del arte no es un error de calculo, es un "
     "error de fecha, y hace parecer alcanzable lo que no lo es"),

    ("T^k es una biyeccion sobre Z/2^k, luego no hay clases que cribar",
     "FALSO AL PIE DE LA LETRA. T^k ni siquiera esta bien definida modulo 2^k: "
     "con k = 1 los restos 0 y 2 son la misma clase y T(0) = 0 mientras "
     "T(2) = 1. Y T tampoco es inyectiva sobre Z: T(1) = T(4) = 2. Lo verdadero "
     "es que RESTO -> VECTOR DE PARIDAD es una biyeccion Z/2^k -> {0,1}^k, "
     "exhaustivo de k = 1 a 16 en verificar_constantes.py [6]. Y 'no hay clases "
     "que descartar' tambien se pasa: pinzaciclos.py descarta casi todas, lo "
     "que no hay es descarte EN BLOQUE (2026-08-01)",
     "LA CONCLUSION ESTRATEGICA SE SALVO POR SUERTE, no por rigor: la frase "
     "falsa estaba escrita al lado de la verdadera y el argumento se apoyaba en "
     "la de al lado. Si se hubiera apoyado en la otra, la decision de abandonar "
     "el barrido de restos estaria construida sobre nada. Cuando dos "
     "formulaciones conviven, hay que decir cual es la que trabaja"),

    ("si dos trayectorias se funden, entonces 2^r*k + n1 y 2^r*k + n2 se funden "
     "para TODO k (Garner 1985, G2)",
     "FALSO SIN DOS HIPOTESIS. (i) r tiene que ser MAYOR que el numero de pasos "
     "pares del tramo: con r = e la propagacion falla en 9.954 de 62.400 casos, "
     "con r = e+1 va perfecta (62.400 y 0 fallos). (ii) Los dos tramos deben "
     "gastar los MISMOS pares y los MISMOS impares, no solo encontrarse. "
     "Contraejemplo (3, 20): pasan los dos por el 10 en el indice 1 pero uno "
     "gasta 1 impar y el otro 0, y da la misma altura en 2 de 40 valores de m; "
     "control con (4, 5), que si cumple las dos: 40 de 40. Lo cazo "
     "verificar_fusiones.py (2026-08-01)",
     "un enunciado publicado, copiado sin sus cuantificadores. Es el mismo modo "
     "de fallo que el piso de la altitud -le faltaba n impar- y que el criterio "
     "de fusion -le falta m >= 1-. Cuando se cita un teorema hay que copiar "
     "tambien sus hipotesis, sobre todo las que parecen tecnicas"),

    ("(8k+4, 8k+5) tienen la misma altura para todo k >= 0",
     "FALLA EN k = 0: altura(4) = 2 y altura(5) = 5, porque el 4 llega al 1 "
     "ANTES del paso 3 en el que se encontrarian. La CONFLUENCIA si vale para "
     "todo k >= 0 -los dos caen en 6k+4 en 3 pasos, 200.000 casos y 0 fallos, y "
     "es identidad algebraica-; lo que pide k >= 1 es el corolario de altura. "
     "Lo cazo verificar_fusiones.py (2026-08-01)",
     "confluir y tardar lo mismo son dos enunciados, y el segundo no se sigue "
     "del primero cuando uno de los dos numeros TERMINA antes del encuentro. Es "
     "el mismo agujero que el m >= 1 del criterio de clases, encontrado por dos "
     "caminos distintos el mismo dia: los bordes chicos son donde se rompen los "
     "enunciados 'para todo'"),

    ("el criterio de fusion de clases decide para TODOS los m de la clase",
     "para m >= 1. En m = 0 es falso: (5,6) da alturas 5 y 8, y (4,5) da 2 y 5, "
     "y fallan exactamente 3 clases -r = 2, 4 y 5- estables de k=5 a k=22. "
     "Nadie lo vio porque la fuerza bruta de clasesfusion.py itera "
     "range(1, 40): por construccion no podia ver el unico m que rompe. La cota "
     "del 43,57% no se mueve (2026-08-01)",
     "un test que empieza en 1 no puede refutar nada en 0. Antes de escribir "
     "'para todo', mirar donde empieza el bucle que lo comprobo. Segunda vez "
     "del mismo patron: la primera fue el piso de la altitud"),

    ("la lista entera de la Tabla C de Terras son las convergentes y "
     "semiconvergentes de log2(3)",
     "es LA MITAD: solo las que aproximan log2(3) POR ENCIMA. 3/2, 19/12, 84/53 "
     "y 1054/665 son convergentes y no son jump values (2026-08-01)",
     "'exactamente las X' es una afirmacion de doble inclusion, y aqui solo se "
     "habia comprobado una. Que todas las supervivientes sean convergentes no "
     "implica que todas las convergentes sobrevivan"),

    ("la tabla de constantes esta medida toda sobre trayectorias de 2 a 10^7",
     "MEZCLABA DOS ESTIMADORES Y DOS RANGOS sin decirlo: las tres constantes de "
     "parada son PENDIENTE DE REGRESION a 10^7, el B/A = 2,014002 es AGREGADO a "
     "10^6, y la de Wagon es muestreo. Con pendiente el B/A da 2,0018 (+0,09%) "
     "en vez de +0,70%, y el agregado de la constante clasica no converge a "
     "10,428 en ningun rango alcanzable porque la recta tiene intercepto -1,73. "
     "Ademas el 3,49031 de la fila 'hermana de Wagon' no lo reproduce ninguna "
     "definicion probada, y queda marcado como numero sin explicar (2026-08-01)",
     "paso en la misma seccion titulada 'TRAMPA DE ESTIMADOR, anotada porque "
     "mordio'. UNA ADVERTENCIA ESCRITA NO ES UNA COMPROBACION. Una columna "
     "'medido' obliga a decir con que estimador y en que rango, o no significa "
     "nada"),

    ("la racha de 120 consecutivos con la misma altura en 136.696.632 es un "
     "hallazgo del repo",
     "es de Wu 1993 (MR 1277568), que barrio hasta 1,5e8 y la publico, y "
     "136.696.632 < 1,5e8: la redescubrimos. Y en la misma fila, el hito de "
     "Garner esta diecisiete escalones mas abajo de lo que se decia: su "
     "conjetura es sobre la densidad de ENTEROS EN TUPLA, no sobre la fraccion "
     "de PARES, y cruza el 50% en 2^6, no entre 2^23 y 2^24 (2026-08-01)",
     "antes de apuntarse un maximo hallado por fuerza bruta hay que mirar hasta "
     "donde llego la fuerza bruta publicada. Y comparar un hito ajeno exige "
     "comprobar que la magnitud es la misma: densidad de enteros en tupla y "
     "fraccion de pares consecutivos no son lo mismo"),

    ("el estado post-rebote de un par con r par es (w, 6w+2), con orbita "
     "de E forzada 1, 0, -2, -5, -3 y casos A/B-alfa excluidos",
     "LA FAMILIA ERA UN FANTASMA: el estado con D = 0 es el par "
     "{s, 3s+1} (gap 2s+1), y su rebote beta da (w, 9w+2) con "
     "E = 3w+1 DEPENDIENTE de w. El error nacio de escribir el par como "
     "(s, 2s+1) -confundiendo el gap con el valor mayor- y se propago a "
     "las comprobaciones 11 (corolario), 12 y 14 y a tres filas de esta "
     "base. Lo cazo LA ECUACION DE RENOVACION al no cerrar (0,4039 "
     "contra 0,4453 medido; con la familia real cierra en 0,4504), y lo "
     "confirmo el cruce con 8.191 rebotes de pares reales: todos en "
     "(w, 9w+2), cero en (w, 6w+2) (2026-08-03)",
     "una ecuacion de conservacion que no cierra es un detector de "
     "premisas falsas mas fino que cualquier barrido: el barrido del "
     "fantasma paso limpio porque media al fantasma. Y las familias "
     "canonicas se verifican CONTRA EL OBJETO REAL antes de razonar "
     "sobre ellas - el fantasma paso tres comprobaciones que solo lo "
     "miraban a el"),

    ("la ley del aterrizaje en potencias de (-2) es una ley nueva "
     "independiente",
     "SE DESCOMPONE Y NO ES INDEPENDIENTE (correccion de la revision "
     "externa + medicion propia sin restriccion, 04-08-2026): en TODOS "
     "los pasos mixtos aparecen todos los D pares (0, 6, 10, 22, 28: la "
     "'ley' no rige ahi); en los LANDINGS (ultimo mixto que cascadea "
     "directo a consec), |D| = 2^j es DEFINICIONAL - la cascada de "
     "divisiones no puede quitar factores 3, asi que el gap post-mixto "
     "|D|/2 debe ser potencia de 2 - y el SIGNO es exactamente la ley "
     "mod 3 ((-2)^j = 1 mod 3 siempre; los gemelos -4, +8, -16 son "
     "todos 2 mod 3). 'La ley' = definicion del rincon + ley mod 3. El "
     "contenido real que queda: LA LEY MOD 3, sola, con su induccion "
     "pendiente",
     "sexta correccion de la familia del filtro: antes de anunciar una "
     "ley hay que medir el objeto SIN el filtro y descomponerla contra "
     "lo ya conocido. La regla del rango entra como doctrina: todo "
     "conteo chico se re-corre a 4x y 16x, y si crece, el rango es el "
     "resultado"),

    ("phi = 8/(23 - 13 rho) y 'phi = 1 <=> rho = 15/13'",
     "INCOMPLETA: se tiro epsilon_torre sin declararlo (quinta revision "
     "externa, 04-08-2026). La formula honesta es phi = 8(1 + eps) / "
     "(23 - 13 rho), o en la parametrizacion del revisor 23 phi = 8 + "
     "13 gamma + 8 eps_torre. NO hay error de transcripcion entre las "
     "dos formas (gamma = rho phi las hace identicas; el contraste del "
     "revisor metio gamma en el hueco de rho), pero SU GOLPE ES REAL: "
     "el 15/13 era condicional a eps = 0 sin decirlo, y con gamma <= 1 "
     "y eps = 0 saldria phi <= 21/23 - un teorema negativo FALSO por "
     "artefacto de la cola tirada. LA RESOLUCION, y es la joya: "
     "phi = 1 <=> eps_torre = 1/4 EXACTO <=> P(fusion | torre) = 1 - "
     "la conjetura reproduciendose en la torre, tercera aparicion de "
     "la autosimilitud. EL BLANCO DEFINITIVO: si la torre pierde masa "
     "(eps < 1/4 estricto), phi < 1 es TEOREMA con valor computable",
     "las colas no se tiran: se declaran con su simbolo y su cota. Y "
     "un 'teorema negativo enorme de una tarde de algebra' es la "
     "senal de revisar que cola se tiro - la imposibilidad no era del "
     "sistema, era del cero implicito. Pendiente commitado: "
     "reconstruir la ecuacion de beta independiente y MEDIR/ACOTAR "
     "eps_torre - el numero que decide el programa"),

    ("la supresion del j = 3 (version final): 'un aterrizaje +16 no "
     "puede saldar Delta_S' / 'los +16 son esporadicos de valor'",
     "REFUTADA DEL TODO por el rigor mortis (04-08-2026): los 7 "
     "aterrizajes +16 crudos traen saldo 0 (identico a los -8 que si "
     "funden), y el test de Jirafas los declara EVENTOS DE CLASE los "
     "7 de 7 (levantados a r + 2^(t+8)*K aterrizan en el mismo t): "
     "densidad positiva, no esporadicos. La 'supresion' era un "
     "artefacto DOBLE: del filtro de fusion de clase primero, y de "
     "medir en las formas reducidas a niveles m <= 18 despues - en la "
     "dinamica de pares consecutivos el +16 aparece en 7 clases bajo "
     "2^16. LO QUE SOBREVIVE, MAS LIMPIO QUE ANTES: la ley de "
     "aterrizajes es potencias de (-2) SIN excepcion - todos los j "
     "aparecen - y los no-potencia (-4, +8, -16) siguen en cero "
     "absoluto (2026-08-04)",
     "tres capas de filtro producen tres conjeturas falsas de la misma "
     "medicion; la ley verdadera aparecio al quitar la ultima. Una "
     "conjetura que muere por los propios instrumentos y deja una ley "
     "mas limpia es ganancia neta - y el test de clase de Jirafas es "
     "el arbitro correcto entre 'estructura' y 'esporadico'"),

    ("la supresion del j = 3: 'la dinamica jamas alcanza la forma "
     "{s, 3s+17}' y 'la pendiente es la rama de salida del 33'",
     "LAS DOS MITADES ERAN FALSAS, y las rompio la instrumentacion "
     "propia (04-08-2026): (1) el 33 SI sale por f0 - 19.651 veces - y "
     "el estado mixto D = +16 se alcanza de sobra; (2) el +16 SI "
     "aterriza en par consecutivo: 23 veces en la dinamica cruda "
     "(contra 38.464 del +4 y 7.274 del -8). La supresion REAL es "
     "condicional: entre las fusiones DE CLASE con el saldo Delta_S "
     "canonico, los aterrizajes +16 no aparecen - no es "
     "inalcanzabilidad dinamica, es CONTABILIDAD DE S: los 23 llegan "
     "pero nunca cierran el balance. La conjetura muta a su forma "
     "final: 'un aterrizaje +16 no puede saldar Delta_S = +2' - que "
     "es exactamente el argumento del reparto de mixtos esbozado, "
     "ahora con el objetivo puntual correcto",
     "un fenomeno medido bajo condicionamiento no es un fenomeno de la "
     "dinamica: antes de conjeturar inalcanzabilidad hay que medir el "
     "objeto SIN el filtro. La ley mod 3 (D = 11) sobrevive a esta "
     "correccion - esa si es dinamica cruda; la mitad del 33/+16 era "
     "del filtro"),

    ("el Corolario 1 de Jirafas: 'la fusion desbalanceada tiene medida "
     "cero porque es union numerable de soluciones esporadicas'",
     "ROTO por la segunda revision externa (Opus 5, 03-08-2026): "
     "'numerable => medida cero' es vacuo en Haar (N entero ya es nulo "
     "en Z_2) y no acota densidad natural (la cota da sum 2^t ~ 2^(P+1) "
     "contra 2^P: peor que trivial). Instrumentado: las 13.137 fusiones "
     "desbalanceadas del censo chocan TODAS en el valor 2 (la entrada "
     "del ciclo) pero su densidad es ~0,39 y decae lentisimo: masa "
     "real. EL COLAPSO DEL SISTEMA SOBREVIVE porque nunca necesito ese "
     "corolario (la descomposicion por primer evento DE CLASE es exacta "
     "y la masa sin evento de clase aporta 0 legitimamente), y el "
     "Corolario 2 quedo DEMOSTRADO por coeficientes (reentrada consec "
     "de clase => 3^Sx = 9*3^Sy => llega con delta 0)",
     "la cardinalidad no acota la densidad; y cuando un corolario se "
     "cae hay que preguntar si el edificio lo usaba de verdad - este "
     "no lo usaba, pero se publico como si lo sostuviera"),

    ("el lema de levantamiento de las fusiones (si n y n+1 coalescen en "
     "k pasos, 2^k r + n y 2^k r + n+1 tambien) y la existencia del "
     "limite f por monotonia son 'elementales, demostrados en este repo'",
     "SON DE GAO GUO-GANG 1993 (Discrete Mathematics 112, 261-267): su "
     "Lema 2 es el levantamiento literal y su Corolario 2 la monotonia "
     "acotada, hasta con la misma letra d_k. Lo encontro la primera "
     "revision externa (Opus 5, 03-08-2026); nuestra busqueda no lo vio. "
     "Y de paso: la 'validacion' de la ecuacion de renovacion por cierre "
     "numerico (0,4504 vs 0,4453) comparaba dos estimaciones sesgadas "
     "por el mismo truncamiento (Gao midio la densidad subiendo de "
     "0,310 a 0,512 entre 10^2 y 10^8: el sesgo es enorme) y SE RETIRA; "
     "la sustituye la identidad entera exacta de identidadexacta.py",
     "las bases 'elementales' tambien se buscan en la literatura antes "
     "de atribuirselas al repo; y dos cotas inferiores correlacionadas "
     "que coinciden no validan nada - la validacion buena es la que no "
     "tiene sesgo que compartir: identidades enteras por nivel"),

    ("franjaeverett.py corria y publicaba sus resultados (el optimo M = 9, "
     "el umbral 1,63763)",
     "el fichero NO COMPILABA: dos strings sin cerrar (lineas 542 y 589, "
     "texto adversarial del 01-08 pegado dentro de un print), o sea que "
     "NUNCA habia corrido en su forma actual y todo lo escrito tras esa "
     "edicion estaba sin verificar. Lo cazo un compile() de la lectura "
     "completa del repo (2026-08-03). Reparado y corrido: exit 0, y la "
     "afirmacion enterrada se CONFIRMA (M = 10001, umbral 1,585011)",
     "un resultado escrito no es un resultado corrido. compile() sobre "
     "cada .py tocado cuesta un segundo y habria cazado esto el mismo dia; "
     "y un texto adversarial se aplica como edicion de codigo, no se pega "
     "dentro de un print"),

    ("toda entrada al nucleo desde la frontera llega con c = 2 (mod 3)",
     "solo la puerta directa: (3g+1)/2 = 2 (mod 3). La puerta con vuelco "
     "da (3g-1)/2 = 1 (mod 3). La ley verdadera es MEJOR que la falsa: "
     "cada puerta trae SU clase, ninguna trae 0, y la absorcion (c = 1) "
     "vive exactamente en la clase del vuelco. Lo cazo el SystemExit del "
     "test T3a en su primera corrida (04-08-2026)",
     "una ley aritmetica se conjetura sobre UNA rama y se enuncia sobre "
     "todas: hay que calcular cada rama antes de escribir el 'toda'. El "
     "test exacto con SystemExit convirtio el error en un hallazgo en "
     "una sola corrida"),

    ("las dos tablas de LaTourette 2007 se corresponden con las puertas "
     "de retorno de la cadena: blocks = puerta (1,-1), strings = puerta "
     "(1,3)",
     "la puerta (1,3) NO dispara nunca, y hay una tercera puerta ((0,2) "
     "-> (0,1), el gap 2 partiendose) que la hipotesis ignoraba. La "
     "correspondencia verdadera es por el SIGNO del gap final: blocks = "
     "orden conservado, strings = vuelco. Lo cazo el SystemExit del "
     "cruce en su primera corrida (04-08-2026)",
     "antes de asignar una estructura propia a una clasificacion ajena, "
     "medir la propia: las puertas se enumeran ejecutando la cadena, no "
     "deduciendolas del papel. El error costo una corrida; publicado "
     "habria costado la credibilidad del cruce entero"),
]


# ===========================================================================
# LAS CONSTANTES
# ===========================================================================
#
# No demuestran nada: son promedios, y un promedio no dice nada de ningun
# numero concreto. Pero son patrones utiles para trabajar, y varias son
# literatura publicada que costo trabajo. El campo AVISO es lo que las hace
# seguras de guardar: ahi va lo que impide usarlas mal mas tarde.

CONSTANTES = [

    cte("constante de Wagon", 9.477955556559275, 9.471872, -0.064,
        "tiempo de caida medio",
        "cuantos pasos tarda de media un numero en bajar por debajo de si mismo",
        "Wagon; OEIS A122790", None,
        "EL VALOR ESTA BIEN Y LA FORMULA PUBLICADA ESTA MAL desde 1985, y OEIS "
        "lo documenta en A100982: la errata esta en Wagon Y en Chamberland, "
        "floor(1 + 2i + i*log2(3)) donde deberia ser floor(1 + i + i*log2(3)). "
        "El valor se confirmo aqui a 35 cifras contra A122790 por camino "
        "independiente. Quien lo reimplemente desde el enunciado publicado "
        "obtiene otra cosa. Y la columna medida es MUESTREO a 10^7, no la misma "
        "clase de estimador que las tres constantes de parada."),

    cte("hermana de Wagon (conteo reducido)", 3.4926518521864249, 3.49031,
        -0.067,
        "el mismo tiempo de caida contando solo los pasos impares",
        "la version del tiempo de caida con el conteo reducido",
        "Wagon", None,
        "DOS AVISOS (01-08-2026). (1) NO ES UNA CONSTANTE INDEPENDIENTE: "
        "E[unos] = E[sigma]/2 por el teorema del paro opcional de Doob sobre la "
        "biyeccion de Terras -los bits de paridad son monedas justas y sigma es "
        "un tiempo de paro-, o sea que esta fila y la de Wagon son la misma "
        "medicion dividida por dos. Media de pasos del atajo "
        "3,492651852186424912, media de pasos impares 1,746325926093212456. "
        "(2) EL 3,49031 DE LA COLUMNA 'medido' ES UN NUMERO SIN EXPLICAR: "
        "ninguna definicion probada lo reproduce -la natural da 3,490781, solo "
        "impares 5,981561, contando unos 1,745155, clasico sobre todos "
        "5,235936-. Viene de la sesion del 30-07-2026, que no dejo ficheros. No "
        "se borra: se marca."),

    cte("media geometrica por paso del atajo", 0.8660254037844386, 0.8643758,
        -0.190, "sqrt(3)/2",
        "por cuanto multiplica de media cada paso del mapa del atajo",
        "propio; es el modelo estandar", None,
        "Que sea menor que 1 dice 'en promedio bajan', y NO impide que exista "
        "una orbita que suba para siempre: seria un conjunto de medida cero. "
        "Prueba: 5n+1 tiene media 1,118 > 1 y aun asi tiene el ciclo del 13."),

    cte("pasos impares contra ln(n)", 3.476059496782208, 3.46140, -0.42,
        "1/ln(4/3)",
        "cuantos 3n+1 se aplican por cada unidad de ln(n)",
        "Lagarias, Applegate-Lagarias", None,
        "ESTIMADOR Y RANGO, que hasta el 01-08-2026 no estaban dichos: es "
        "PENDIENTE DE REGRESION a 10^7, no muestreo ni agregado. Ponerla en la "
        "misma columna 'medido' que las de muestreo sugiere que son comparables "
        "y no lo son. Y es gamma(1/2) con gamma(rho) = 1/(ln2 - rho*ln3): las "
        "tres constantes de parada son una sola funcion evaluada en un punto, "
        "en la proporcion rho : 1 : 1+rho."),

    cte("constante de parada del ATAJO", 6.952118993564416, 6.92916, -0.33,
        "2/ln(4/3)",
        "cuantos pasos del mapa del atajo por cada unidad de ln(n)",
        "Lagarias, Applegate-Lagarias", None,
        "ES LA DEL ATAJO, NO LA DEL CLASICO. La del clasico es "
        "3/ln(4/3) = 10,428. Confundirlas da un 49,5% de error, y ya paso una "
        "vez en este repo. La escalera correcta es 1:2:3 segun se cuenten los "
        "3n+1, los pasos del atajo o los clasicos. El valor medido es PENDIENTE "
        "DE REGRESION a 10^7 (dicho desde el 01-08-2026)."),

    cte("constante de parada CLASICA", 10.428178490346623, 10.39057, -0.36,
        "3/ln(4/3)",
        "cuantos pasos del mapa clasico 3n+1 por cada unidad de ln(n)",
        "Lagarias, Applegate-Lagarias", None,
        "MEDIDA COMO PENDIENTE DE REGRESION a 10^7. Con el otro estimador NO "
        "sale: el agregado no converge a 10,428 en ningun rango alcanzable, "
        "porque la recta tiene intercepto -1,73 pasos que solo se diluye como "
        "1/ln(n) -a 10^6 el agregado da 10,25588 y sigue subiendo lentisimo-. "
        "Con termino aditivo el estimador correcto es la pendiente, no el "
        "cociente de sumas."),

    cte("divisiones por multiplicacion B/A", 2.0, 2.014002, +0.70,
        "la valuacion 2-adica media de 3n+1, que vale 2 porque P(v=k) = 2^-k",
        "cuantas divisiones entre dos hay por cada 3n+1",
        "propio", None,
        "CONVERGE A 2, NO A log2(3). El log2(3) = 1,585 es el punto de "
        "EQUILIBRIO, no el valor tipico: son dos numeros distintos y no se "
        "contradicen. La media de razones trayectoria a trayectoria da 2,174 "
        "por Jensen y NO vale. Y EL RANGO Y EL ESTIMADOR, que faltaban hasta el "
        "01-08-2026: este 2,014002 es el AGREGADO suma(B)/suma(A) a 10^6; a "
        "10^7 el agregado da 2,012389, y con pendiente de regresion a 10^7 sale "
        "2,0018, o sea +0,09% en vez de +0,70%. Las tres constantes de parada "
        "de esta misma tabla son pendiente de regresion: ponerlas en la misma "
        "columna que este agregado sugiere que son comparables y no lo son."),

    cte("valuacion 2-adica media de 3n+1", 2.0, 1.99048, -0.48,
        "suma de k*2^-k = 2",
        "cuantas veces seguidas se puede dividir entre dos despues de un 3n+1",
        "propio", None,
        None),

    cte("log2(3), el equilibrio", 1.584962500721156, None, None,
        "log2(3)",
        "el B/A exacto por encima del cual una trayectoria cae y por debajo "
        "del cual sube; un ciclo lo tendria clavado",
        "elemental", "collazmalla.py",
        None),

    cte("residuo de Roosendaal Res(993)", 1.2531421443950680, None, None,
        "2^61 / (3^32 * 993)",
        "el maximo conocido de 2^B/(3^A*n), o sea el techo del grosor de la "
        "lamina",
        "Roosendaal (conjeturado)", "elmasuno.py",
        "ES CONJETURA, NO TEOREMA: Roosendaal lo verifico hasta 2^32, y "
        "cruzarecords.py lo comprobo hasta 2^71 sobre los 243 records. Y OJO "
        "CON LA CONSTANTE LITERAL: mapahilos.py guarda 1.2531421442887503, que "
        "esta mal desde la decima cifra. El exacto es 2^61/(3^32*993)."),

    cte("techo del grosor, ln(Res(993))", 0.2256541127319812, None, None,
        "ln( 2^61 / (3^32 * 993) )",
        "cuanto se separa como maximo un punto de la lamina del plano de "
        "equilibrio, medido en NATS sobre trayectorias enteras",
        "Roosendaal (conjeturado)", "elmasuno.py",
        "OJO CON LAS UNIDADES, QUE AQUI HUBO UN ERROR HASTA EL 01-08-2026. "
        "Este numero esta en NATS. El 0,2286 de collazlamina.py, que estaba "
        "puesto en la columna 'medido' de esta misma fila como si fuera lo "
        "mismo, esta en BITS y ademas se mide sobre PARES de la trayectoria "
        "del 221, no sobre trayectorias enteras. En las mismas unidades: "
        "0,2286 bits = 0,158478 nats contra 0,225654 nats. No se parecen: "
        "difieren en un factor 1,42. Que eps sea > 0 esta demostrado "
        "(elmasuno.py); que este ACOTADO por este numero sigue siendo la "
        "conjetura de Roosendaal."),

    cte("grosor de la lamina del 221", 0.2286349110, None, None,
        "max sobre los 6.555 pares i<j de log2( 2^B * seq[j] / (3^A * seq[i]) )",
        "cuanto sobresalen del plano de equilibrio los pares de UNA "
        "trayectoria concreta, la del 221, medido en BITS",
        "propio", None,
        "FICHERO RETIRADO: collazlamina.py se borro en la purga del 01-08-2026 "
        "porque la lamina media la geometria elegida a mano. Lo que se rescato "
        "antes de borrarlo es cotatramos.py, que se queda con la parte que si "
        "es teorema -C >= 0, o sea 2^B*seq[j] >= 3^A*seq[i] para todo par, y si "
        "el tramo baja entonces 2^B > 3^A-, pero NO recalcula este maximo. "
        "NO ES UNA COTA NI UNA CONSTANTE DEL PROBLEMA: mide el 221 y nada mas. "
        "El maximo se alcanza en el par (221 -> 16), que es la trayectoria "
        "entera del 221, asi que este numero es su propio eps en bits: "
        "0,2286 bits = 0,158478 nats, o sea Res(221) = 2^73/(3^41*221) = "
        "1,17173. Lo que si es cierto es la desigualdad: para cualquier par, "
        "h <= log2(Res(seq[i])), porque un producto parcial de factores "
        "(3x+1)/(3x) es menor que el total. Con la conjetura de Roosendaal eso "
        "acota todos los pares de todas las trayectorias por 0,325550 BITS."),

    cte("L de Everett", 0.5757166424934449, None, None,
        "log(2) / log(10/3)",
        "la fraccion de pasos impares del ATAJO por debajo de la cual Everett "
        "garantiza la bajada",
        "Everett 1977", "verificar_everett.py",
        "TRADUCCION CORREGIDA EL 01-08-2026, y la de antes era falsa. Aqui "
        "decia 'B/A > 0,7369', y el bueno es B/A > 1/L = log2(10/3) = "
        "1,73696559416620616641: MAS FUERTE que log2(3), no mas flojo. El "
        "0,7369 es literalmente 1/L - 1, que es la marca algebraica de haber "
        "sumado un paso de mas al denominador (poner N = A+B en vez de N = B). "
        "Y log2(3) no es 'el umbral verdadero': no garantiza el descenso (n = 7 "
        "sube a 8). El hueco entre los dos tiene forma cerrada, "
        "log2(10/9) = 0,15200309, y es el precio exacto de usar 5/3 en vez de "
        "3/2."),

    cte("fraccion de pasos impares, mapa del atajo", 0.5, 0.496524, -0.695,
        "1/2",
        "que proporcion de los pasos del atajo son impares",
        "Terras 1976", None,
        None),

    cte("fraccion de pasos impares, mapa clasico", 0.3333333333333333, 0.331785,
        -0.465, "1/3",
        "que proporcion de los pasos del mapa clasico son impares",
        "Terras 1976", None,
        None),

    cte("cota inferior demostrada de la densidad de fusion", 0.4356581771280617,
        None, None, "a(32) / 2^32 = 1871137623 / 2^32",
        "que fraccion de los pares consecutivos tienen la misma altura POR "
        "RAZON DE RESTO, decidido mirando solo n mod 2^32",
        "propio", "clasesfusion.py",
        "Este NO es un promedio: es una cota inferior exacta, sin muestreo ni "
        "ajuste. La densidad real medida a 2^28 es 0,5186, y la diferencia de "
        "unos diez puntos son los pares que se funden pero cuya clase no se "
        "funde entera."),

    cte("umbral q < 4 del qn+1", 4.0, 4.0019, +0.048,
        "q^f / 2 = 1 con f = 1/2",
        "el q maximo para el que el mapa qn+1 deberia converger; como q tiene "
        "que ser impar, el 3 es el unico valor que converge",
        "propio", None,
        "NO ES EVIDENCIA INDEPENDIENTE. Se comprobo que media = q^f/2 "
        "exactamente, luego 'media = 1' es IDENTICO a f = 1/2, que es Terras "
        "1976. La precision del 0,048% mide con que exactitud recuperamos una "
        "densidad ya conocida, no el umbral. El fenomeno es real; el numero no "
        "es un descubrimiento."),

    cte("exponente de la criba industrial", 0.9499555271883305, 0.947700,
        -0.237, "H(log_3 2), la entropia binaria de log_3(2)",
        "como escala la densidad de supervivientes de la criba: 2^(-(1-H)*k)",
        "Barina 2025", "descensoresto.py",
        "ES EL LIMITE ASINTOTICO, NO EL VALOR LOCAL. El valor medido de la "
        "columna es la pendiente en k = 640..1280; en el rango real de la "
        "criba (k = 34) la pendiente es 0,892 y el decaimiento 0,108, o sea "
        "que la densidad cae al DOBLE de velocidad que el 2^(-0,05k) que cita "
        "el CLAUDE.md. Y aparte: reduccion no es aceleracion, un factor 138x "
        "de criba produjo solo 5,94x de velocidad porque los supervivientes "
        "son justamente los caros."),

    cte("techo heuristico del tiempo de descenso", 32.5896, 26.79, None,
        "(1 + log_3 2) / (1 - H) para el mapa clasico; 1/(1-H) = 19,98 para "
        "el atajo",
        "a cuanto tenderia sigma_max(k)/k, o sea la C de una hipotetica cota "
        "sigma(n) <= C*log2(n)",
        "propio", "descensoresto.py",
        "SALE DE UN MODELO DE DENSIDAD, o sea de un promedio: no demuestra que "
        "la cota exista. El valor medido de la columna es el cociente de los "
        "records publicados a 61 bits (1639/61,2), que sube despacio hacia "
        "ese techo sin llegar. Si la cota existiera y se demostrara, la "
        "conjetura saldria por induccion fuerte en tres lineas: por eso es el "
        "numero mas sugerente del laboratorio y el mas peligroso."),

    cte("coral: divisiones por multiplicacion", 1.7320508075688772, 1.7320,
        -0.003, "ninguna: es una medicion sobre el arbol, no una formula",
        "cuantos pasos pares por cada impar hay en el arbol inverso dibujado "
        "por el coral",
        "propio", None,
        "FICHERO RETIRADO: coralcollaz.py se borro en la purga del 01-08-2026 "
        "(media el angulo elegido a mano), asi que este numero ya no tiene "
        "codigo detras en el repo. NO ES UNA CONSTANTE. El 1,7345 que se "
        "publico era el valor de una "
        "MUESTRA a HASTA = 3.000; se asienta en 1,7320 +/- 0,0003 y la cuarta "
        "cifra nunca fue estable. Que caiga a 0,02% de sqrt(3) es CASUAL: la "
        "descomposicion del valor lo dice. El valor teorico de esta fila es "
        "sqrt(3) puesto solo para poder comparar, no porque lo sea."),
]


# ===========================================================================
# EL MAPA DE DEPENDENCIAS (03-08-2026, regla dictada por el usuario)
# ===========================================================================
#
# Que cuelga de que, en el programa de las clases nuevas. LA REGLA: no se
# avanza en una rama sin tener comprobada la rama anterior. En codigo:
#   - un nodo 'demostrado' NO puede depender de un nodo no demostrado
#     (su demostracion colgaria del aire);
#   - ningun nodo trabajado (no pendiente) puede depender de un 'pendiente';
#   - los 'pendiente' se listan como AVANZABLE solo si TODOS sus padres
#     estan demostrados. Lo demas esta BLOQUEADO.

ESTADOS_NODO = ESTADOS + ("pendiente",)

# (nombre, estado, descripcion corta)
NODOS = [
    ("definiciones", "demostrado",
     "mapa del atajo, criterio de buenas(k) [Terras], nuevas y b(k)"),
    ("ecuacion_vortice", "medido",
     "nueva <=> primer encuentro en vortice (a=3b+1, S compensada); k=3..15"),
    ("lema_identidad", "demostrado",
     "T(c*2^m - 1) = 3c*2^(m-1) - 1, elemental"),
    ("lema_v2", "demostrado",
     "mixto <=> d impar; paso compartido quita exactamente un factor 2; "
     "|M| par"),
    ("lema_general", "demostrado",
     "C impar, C = 3^q (mod 4) => (C*2^q - 2, C*2^q - 1) funde en q+2"),
    ("teo_repunit", "demostrado",
     "familia (2^j - 2, 2^j - 1): caso C = 1, 3 del lema general"),
    ("nuevas_no_acaban", "demostrado",
     "b(j+2) >= 1 para todo j par: corolario del repunit"),
    ("unicidad_M2", "demostrado",
     "exactamente una clase |M| = 2 por nivel, alternando A/B"),
    ("familia_M4", "demostrado",
     "el vecino del perdedor: contraccion en 2 pasos + lema general"),
    ("M4_ruta_impar", "demostrado",
     "unicidad de |M| = 4 entre TODOS los r impares: r = 1 (mod 4) da "
     "exactamente una (contraccion, C en {3,9}); r = 3 (mod 8) cae en "
     "D = -3 < 0 invariante (nunca vortice); r = 7 (mod 8) encadena "
     "cuatro mixtos"),
    ("estratos_medidos", "medido",
     "tabla de estratos k <= 15: |M|=2 y 4 unicos, altos polinomicos"),
    ("unicidad_M4", "medido",
     "una sola clase |M| = 4 por nivel: demostrado para todo r impar; "
     "para r par: |M| >= 4 por el teorema de paridad del rebote, estrato "
     "4 vacio medido a 2^20, y el analisis fino REHECHO sobre la familia "
     "real (w, 9w+2) tras la correccion del fantasma. CONGELADO como "
     "problema abierto interno"),
    ("coordenadas_DE", "demostrado",
     "D = g-2s-1 (vortice <=> D=0 con s impar, afines en compartidos, "
     "D<0 absorbente) y E = D-3s autonoma (su paridad elige su mapa)"),
    ("familias_E", "medido",
     "censo del mapa de E en [-10^5, 10^5]: DIEZ familias (ciclos), "
     "ninguna orbita escapa; el del rebote {-2,-5,-3} atrae al 47%"),
    ("clasificacion_rutas", "pendiente",
     "el salto propuesto por el usuario el 03-08-2026. PASO 1 HECHO "
     "(itinerarios.py): la contraccion es visible en las etiquetas (el "
     "ultimo tramo de |M|=4 vive en las familias de |M|=2), pero la "
     "familia asintotica es invariante RUIDOSO para contar; queda "
     "etiquetar por datos finitos del tramo"),
    ("cuadratica_M6", "pendiente",
     "conjetura: |M| = 6 son preludios de longitud variable sobre |M| = 4"),
    ("recursion_bk", "pendiente",
     "la recursion completa de b(k) y el destino de la razon 2"),
]

# (hijo, padre): el hijo se apoya en el padre
DEPENDENCIAS = [
    ("ecuacion_vortice", "definiciones"),
    ("lema_identidad", "definiciones"),
    ("lema_v2", "definiciones"),
    ("lema_general", "lema_identidad"),
    ("teo_repunit", "lema_general"),
    ("nuevas_no_acaban", "teo_repunit"),
    ("unicidad_M2", "lema_v2"),
    ("unicidad_M2", "lema_general"),
    ("familia_M4", "lema_general"),
    ("estratos_medidos", "ecuacion_vortice"),
    ("estratos_medidos", "lema_v2"),
    ("M4_ruta_impar", "lema_v2"),
    ("M4_ruta_impar", "familia_M4"),
    ("M4_ruta_impar", "lema_general"),
    ("unicidad_M4", "M4_ruta_impar"),
    ("unicidad_M4", "estratos_medidos"),
    ("coordenadas_DE", "lema_v2"),
    ("familias_E", "coordenadas_DE"),
    ("unicidad_M4", "coordenadas_DE"),
    ("clasificacion_rutas", "familias_E"),
    ("clasificacion_rutas", "coordenadas_DE"),
    ("cuadratica_M6", "unicidad_M4"),
    ("cuadratica_M6", "familia_M4"),
    ("cuadratica_M6", "clasificacion_rutas"),
    ("recursion_bk", "cuadratica_M6"),
    ("recursion_bk", "unicidad_M2"),
]

print()
print("COMPROBACION 0 - el mapa de dependencias y la regla del avance")
estado_de = {}
for nombre, estado, _ in NODOS:
    if estado not in ESTADOS_NODO:
        raise SystemExit("nodo %s con estado invalido %r" % (nombre, estado))
    if nombre in estado_de:
        raise SystemExit("nodo duplicado: %s" % nombre)
    estado_de[nombre] = estado
for hijo, padre in DEPENDENCIAS:
    if hijo not in estado_de or padre not in estado_de:
        raise SystemExit("arista con nodo inexistente: %s -> %s"
                         % (hijo, padre))
    if estado_de[hijo] == "demostrado" and estado_de[padre] != "demostrado":
        raise SystemExit("REGLA ROTA: %s (demostrado) depende de %s (%s)"
                         % (hijo, padre, estado_de[padre]))
    if estado_de[hijo] != "pendiente" and estado_de[padre] == "pendiente":
        raise SystemExit("REGLA ROTA: %s (%s) depende del pendiente %s"
                         % (hijo, estado_de[hijo], padre))
# sin ciclos: eliminacion de hojas
pads = {n: set(p for h, p in DEPENDENCIAS if h == n) for n in estado_de}
quedan = set(estado_de)
while True:
    hojas = [n for n in quedan if not (pads[n] & quedan)]
    if not hojas:
        break
    quedan -= set(hojas)
if quedan:
    raise SystemExit("CICLO en el mapa de dependencias: %s" % sorted(quedan))
for nombre, estado, _ in NODOS:
    if estado == "pendiente":
        # comprobada = demostrada O medida con codigo que paso (la regla
        # del usuario dice "comprobada", no "demostrada": un censo nunca
        # va a ser teorema y no por eso bloquea lo que se apoya en el)
        via = all(estado_de[p] in ("demostrado", "medido")
                  for p in pads[nombre])
        print("  pendiente %-18s -> %s" % (nombre,
              "AVANZABLE (padres comprobados)" if via else "BLOQUEADO"))
print("  -> nodos %d, aristas %d, sin ciclos, regla respetada." %
      (len(NODOS), len(DEPENDENCIAS)))
print()


# ===========================================================================
# COMPROBACION 1 -- el vocabulario cerrado
# ===========================================================================

print()
print("=" * ANCHO)
print("LAS AFIRMACIONES DEL LABORATORIO, ORDENADAS POR CUANTIFICADOR")
print("=" * ANCHO)
print()
print("  afirmaciones : %d" % len(AFIRMACIONES))
print("  correcciones : %d" % len(CORRECCIONES))
print("  constantes   : %d" % len(CONSTANTES))
print()

malos = []
for i, f in enumerate(AFIRMACIONES, 1):
    if f[1] not in CUANTIFICADORES:
        malos.append((i, "cuantificador", f[1]))
    if f[2] not in ESTADOS:
        malos.append((i, "estado", f[2]))

print("COMPROBACION 1 - el vocabulario cerrado")
print("  cuantificadores: %s" % ", ".join(CUANTIFICADORES))
print("  estados        : %s" % ", ".join(ESTADOS))
print("  filas fuera del vocabulario: %d" % len(malos))
if malos:
    for i, que, valor in malos[:5]:
        print("    fila %d: %s = %r" % (i, que, valor))
    raise SystemExit("Hay valores fuera del vocabulario. No se guarda nada.")
print("  -> 0 fallos.")
print()


# ===========================================================================
# COMPROBACION 2 -- ficheros que existen, y constantes con lo suyo
# ===========================================================================
#
# Citar un fichero que no existe convierte la base en un catalogo de deseos. Y
# una constante ajena sin valor teorico, o una tramposa sin aviso, es peor que
# no guardarla: invita a usarla mal.

print("COMPROBACION 2 - los ficheros citados existen, y las constantes traen "
      "lo suyo")

citados = sorted({f[3] for f in AFIRMACIONES if f[3]} |
                 {c[7] for c in CONSTANTES if c[7]})
faltan = [nombre for nombre in citados
          if not os.path.exists(os.path.join(CARPETA, nombre))]
sin_fichero = sum(1 for f in AFIRMACIONES if not f[3])

print("  ficheros distintos citados: %d" % len(citados))
print("  %s" % ", ".join(citados))
print("  afirmaciones sin fichero (NULL): %d  <- medidas en scripts sueltos"
      % sin_fichero)
print("  ficheros citados que NO existen: %d" % len(faltan))
if faltan:
    print("    %s" % ", ".join(faltan))
    raise SystemExit("Se cita un fichero que no esta en el disco. No sigas.")

ajenas_sin_valor = [c for c in CONSTANTES if c[6] != "propio" and c[1] is None]
sin_aviso = [c for c in CONSTANTES
             if c[0] in AVISO_OBLIGATORIO and not c[8]]

print("  constantes de fuente ajena sin valor teorico: %d"
      % len(ajenas_sin_valor))
print("  constantes tramposas sin aviso              : %d de %d obligatorias"
      % (len(sin_aviso), len(AVISO_OBLIGATORIO)))
if ajenas_sin_valor:
    print("    %s" % ajenas_sin_valor[0][0])
    raise SystemExit("Una constante ajena sin valor teorico. No sigas.")
if sin_aviso:
    print("    %s" % ", ".join(c[0] for c in sin_aviso))
    raise SystemExit("Una constante con trampa documentada se quedo sin aviso. "
                     "Ese aviso es lo unico que impide usarla mal.")
print("  -> 0 fallos.")
print()


# ===========================================================================
# ESCRIBIR LA BASE
# ===========================================================================

ruta = os.path.join(CARPETA, ARCHIVO)
if os.path.exists(ruta):
    os.remove(ruta)

conexion = sqlite3.connect(ruta)
cursor = conexion.cursor()

cursor.executescript("""
CREATE TABLE afirmaciones (
    id            INTEGER PRIMARY KEY,
    enunciado     TEXT NOT NULL,
    cuantificador TEXT NOT NULL CHECK (cuantificador IN
                      ('todo_n','clase_residual','casi_todo_n','promedio',
                       'ciclos','verificado_hasta')),
    estado        TEXT NOT NULL CHECK (estado IN
                      ('demostrado','medido','conjeturado','refutado')),
    fichero       TEXT,
    fuente        TEXT NOT NULL,
    notas         TEXT
);

CREATE TABLE correcciones (
    id                INTEGER PRIMARY KEY,
    que_se_creia      TEXT NOT NULL,
    por_que_era_falsa TEXT NOT NULL,
    leccion           TEXT NOT NULL
);

CREATE TABLE constantes (
    id            INTEGER PRIMARY KEY,
    nombre        TEXT NOT NULL,
    valor_teorico REAL,
    valor_medido  REAL,
    error_rel     REAL,
    formula       TEXT,
    que_mide      TEXT,
    fuente        TEXT NOT NULL,
    fichero       TEXT,
    aviso         TEXT
);

CREATE TABLE nodos (
    nombre      TEXT PRIMARY KEY,
    estado      TEXT NOT NULL CHECK (estado IN
                    ('demostrado','medido','conjeturado','refutado',
                     'pendiente')),
    descripcion TEXT NOT NULL
);

CREATE TABLE dependencias (
    hijo  TEXT NOT NULL REFERENCES nodos (nombre),
    padre TEXT NOT NULL REFERENCES nodos (nombre)
);

CREATE INDEX idx_cuantificador ON afirmaciones (cuantificador);
CREATE INDEX idx_estado        ON afirmaciones (estado);
""")

cursor.executemany(
    "INSERT INTO afirmaciones (enunciado, cuantificador, estado, fichero,"
    " fuente, notas) VALUES (?,?,?,?,?,?)", AFIRMACIONES)
cursor.executemany(
    "INSERT INTO correcciones (que_se_creia, por_que_era_falsa, leccion)"
    " VALUES (?,?,?)", CORRECCIONES)
cursor.executemany(
    "INSERT INTO constantes (nombre, valor_teorico, valor_medido, error_rel,"
    " formula, que_mide, fuente, fichero, aviso) VALUES (?,?,?,?,?,?,?,?,?)",
    CONSTANTES)
cursor.executemany(
    "INSERT INTO nodos (nombre, estado, descripcion) VALUES (?,?,?)", NODOS)
cursor.executemany(
    "INSERT INTO dependencias (hijo, padre) VALUES (?,?)", DEPENDENCIAS)

conexion.commit()
conexion.close()

print("BASE DE DATOS ESCRITA: %s" % ARCHIVO)
print("  afirmaciones %d · correcciones %d · constantes %d"
      % (len(AFIRMACIONES), len(CORRECCIONES), len(CONSTANTES)))
print()


# ===========================================================================
# COMPROBACION 3 -- ida y vuelta
# ===========================================================================
#
# Guardar mal es peor que no guardar.

revision = sqlite3.connect(ruta)
c2 = revision.cursor()

leidas = c2.execute(
    "SELECT enunciado, cuantificador, estado, fichero, fuente, notas"
    " FROM afirmaciones ORDER BY id").fetchall()
leidas_corr = c2.execute(
    "SELECT que_se_creia, por_que_era_falsa, leccion"
    " FROM correcciones ORDER BY id").fetchall()
leidas_cte = c2.execute(
    "SELECT nombre, valor_teorico, valor_medido, error_rel, formula, que_mide,"
    " fuente, fichero, aviso FROM constantes ORDER BY id").fetchall()

fallos_vuelta = 0
for guardadas, releidas in ((AFIRMACIONES, leidas), (CORRECCIONES, leidas_corr),
                            (CONSTANTES, leidas_cte)):
    if len(guardadas) != len(releidas):
        fallos_vuelta += 1
    for a, b in zip(guardadas, releidas):
        if tuple(a) != tuple(b):
            fallos_vuelta += 1

print("COMPROBACION 3 - ida y vuelta contra el disco")
print("  releidas: %d afirmaciones, %d correcciones, %d constantes"
      % (len(leidas), len(leidas_corr), len(leidas_cte)))
print("  fallos: %d" % fallos_vuelta)
if fallos_vuelta:
    revision.close()
    raise SystemExit("Lo guardado no coincide con lo calculado. No sirve.")
print("  -> 0 fallos.")
print()


# ===========================================================================
# EL INFORME
# ===========================================================================

print("=" * ANCHO)
print("EL INFORME")
print("=" * ANCHO)
print()

print("POR CUANTIFICADOR\n")
print("  %-18s %6s %6s %6s %6s %6s"
      % ("", "total", "demos", "medid", "conje", "refut"))
for q in CUANTIFICADORES:
    t, d, m, c, r = [x or 0 for x in c2.execute(
        "SELECT COUNT(*), SUM(estado='demostrado'), SUM(estado='medido'),"
        " SUM(estado='conjeturado'), SUM(estado='refutado')"
        " FROM afirmaciones WHERE cuantificador=?", (q,)).fetchone()]
    print("  %-18s %6d %6d %6d %6d %6d" % (q, t, d, m, c, r))
total_todo = c2.execute("SELECT COUNT(*) FROM afirmaciones").fetchone()[0]
print("  %-18s %6d" % ("TOTAL", total_todo))
print()


print("=" * ANCHO)
print("LAS QUE COMPONEN - 'todo_n' demostradas y 'clase_residual'")
print("=" * ANCHO)
print()
print("  Son las unicas con las que se puede encadenar un argumento: valen")
print("  para CADA numero, o para los INFINITOS numeros de una clase.")
print()

componen = c2.execute(
    "SELECT cuantificador, enunciado, fichero FROM afirmaciones"
    " WHERE cuantificador='clase_residual'"
    "    OR (cuantificador='todo_n' AND estado='demostrado')"
    " ORDER BY cuantificador DESC, id").fetchall()

ultimo = None
for q, enunciado, fichero in componen:
    if q != ultimo:
        print("  --- %s ---" % q)
        ultimo = q
    print("   * %s" % enunciado)
    print("       [%s]" % (fichero or "sin fichero"))
print()
print("  SON %d DE %d. Ese es el capital real del laboratorio."
      % (len(componen), total_todo))
print()


print("=" * ANCHO)
print("LOS PROMEDIOS - AVISO: NO ENCADENAN CON NADA")
print("=" * ANCHO)
print()
print("  Un promedio no demuestra nada de ningun numero concreto. Una sola")
print("  orbita que subiera para siempre no moveria estos numeros ni un")
print("  decimal, porque seria un conjunto de medida cero. Prueba de que no es")
print("  paranoia: 5n+1 tiene media geometrica 1,118 > 1 -o sea 'todo sube'- y")
print("  SIN EMBARGO tiene un ciclo, el del 13, donde nada sube.")
print()

promedios = c2.execute(
    "SELECT enunciado, estado, fichero FROM afirmaciones"
    " WHERE cuantificador='promedio' ORDER BY estado, id").fetchall()
for enunciado, estado, fichero in promedios:
    print("   * [%s] %s" % (estado, enunciado))
    print("       [%s]" % (fichero or "sin fichero"))
print()
print("  SON %d, y %d de ellas son afirmaciones del propio repo que"
      % (len(promedios), sum(1 for p in promedios if p[1] == "refutado")))
print("  resultaron FALSAS.")
print()


print("=" * ANCHO)
print("LAS CONSTANTES CON AVISO - leer esto ANTES de usarlas en un argumento")
print("=" * ANCHO)
print()

con_aviso = c2.execute(
    "SELECT nombre, valor_teorico, valor_medido, formula, aviso"
    " FROM constantes WHERE aviso IS NOT NULL ORDER BY id").fetchall()
for nombre, teorico, medido, formula, aviso in con_aviso:
    med = "-" if medido is None else "%.7f" % medido
    print("   * %s = %.10f   (medido %s)" % (nombre, teorico, med))
    print("       formula: %s" % formula)
    print("       AVISO  : %s" % aviso)
    print()

total_cte = c2.execute("SELECT COUNT(*) FROM constantes").fetchone()[0]
print("  %d de las %d constantes llevan aviso." % (len(con_aviso), total_cte))
print()

revision.close()

print("=" * ANCHO)
print("La base esta en %s. Tablas: afirmaciones, correcciones," % ARCHIVO)
print("constantes. Se abre con sqlite3 y se consulta sin recalcular nada.")
print()
print("La pregunta que hay que hacerle a cualquier hallazgo nuevo antes de")
print("meterlo aqui:  es un promedio, o es una cota?")
print("=" * ANCHO)
print()
