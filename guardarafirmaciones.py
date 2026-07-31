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
#   No es lo mismo decir "para todo n", que "para toda clase mod 2^k", que
#   "para casi todo n", que "en promedio". Son cosas distintas y solo algunas
#   sirven para encadenar un argumento:
#
#     todo_n            vale para CADA numero, uno por uno. Encadena.
#     clase_mod_2k      vale para los INFINITOS numeros de una clase, decidido
#                       con una comprobacion finita. Encadena. Es el "cuarto
#                       camino" del repo: la regla sin la secuencia.
#     casi_todo_n       vale salvo un conjunto de densidad cero. Encadena con
#                       cuidado: la excepcion que buscamos podria vivir ahi.
#     promedio          NO ENCADENA CON NADA. Un promedio no dice nada de
#                       ningun numero concreto. sqrt(3)/2 < 1 significa "en
#                       promedio bajan", y una sola orbita que subiera para
#                       siempre no moveria ese promedio ni un decimal.
#     ciclos            afirmaciones sobre orbitas periodicas, no sobre n.
#     verificado_hasta  fuerza bruta. Sirve para refutar, jamas para demostrar.
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

CUANTIFICADORES = ("todo_n", "clase_mod_2k", "casi_todo_n", "promedio",
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
         "Ambito: n IMPAR. Sin esa hipotesis es FALSO. Se decide en enteros, "
         "alt*2^r >= 2*n*3^r, sin un solo float: 99.999 casos, 0 fallos. La "
         "racha no PREDICE la altitud, le pone un piso. Cota si, tendencia no."),

    fila("log2( altitud_atajo(n)/n ) >= racha(n) * log2(3/2)",
         "todo_n", "demostrado", "pisoaltitud.py", "propio",
         "Ambito: todo n >= 2, las dos paridades. ESTA es la version que hay "
         "que citar: sin el +1 y sin hipotesis de paridad. El +1 del enunciado "
         "clasico es log2(2) y aparece solo porque se mezcla la altitud de un "
         "mapa con la racha del otro."),

    fila("eps = ln( 2^B / (3^A * n) ) es identicamente igual a la suma de "
         "ln(1 + 1/(3x)) sobre los impares de la trayectoria",
         "todo_n", "demostrado", "elmasuno.py", "propio",
         "Ambito: todo n >= 1. El grosor de la lamina y el sobrante de la "
         "fraccion impar son el MISMO numero en dos coordenadas. 20.011 casos "
         "en racionales exactos, 0 fallos. El residuo 1,7e-7 que se habia "
         "medido era ruido de coma flotante, no del enunciado."),

    fila("eps > 0 siempre, y vale 0 exactamente en las potencias de 2",
         "todo_n", "demostrado", "elmasuno.py", "propio",
         "Ambito: todo n >= 1. Cada factor (1+1/(3x)) es > 1 con x entero "
         "positivo, luego el producto es > 1. collazlamina.py lo habia MEDIDO "
         "en 6.555 pares; ahora esta demostrado en una linea para todos los n."),

    fila("un numero tiene dos padres en el arbol si y solo si deja resto 4 al "
         "dividirlo entre 6; el segundo padre es (v-1)/3",
         "todo_n", "demostrado", "collazarbol.py",
         "regla estandar de la literatura",
         "Ambito: todo v >= 1. La trayectoria del 221 tiene 50 vortices en sus "
         "115 numeros. En el dibujo el 4 se excluye a mano: su otro padre es "
         "el 1, que ya es el arranque del tronco."),

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
         "todo_n", "demostrado", "coralcollaz.py",
         "propio (los giros conmutan)",
         "Ambito: las 730 parejas (A,B) medidas, 0 con rumbo ambiguo. Los "
         "rumbos del coral SON la malla (A,B) pasada a angulos."),

    fila("Collatz sobre los enteros negativos es exactamente el mapa 3m-1 "
         "sobre los positivos",
         "todo_n", "demostrado", None, "estandar en la literatura",
         "Ambito: todo m >= 1. 8.095.665 pasos comparados de 1 a 100.000, 0 "
         "fallos, con dos implementaciones que no comparten una linea. Sin "
         "fichero: se midio en scripts sueltos que no se guardaron."),

    fila("si n tarda S pasos, el numero de la posicion k tarda S-k; luego el "
         "de la posicion S/2 tarda S/2",
         "todo_n", "demostrado", None, "propio (contabilidad, no patron)",
         "Ambito: todo n con cantidad par de pasos. 10.011 numeros del 2 al "
         "20.000, 0 excepciones. El 221 solo tuvo la suerte de tener 114 "
         "pasos, que es par. Esto mata el 'patron' de las notas a mano."),

    fila("n + espejo(n) = 10^k, exacto y siempre",
         "todo_n", "demostrado", "mallaespejo.py",
         "propio (recreativa elemental)",
         "Ambito: todo n >= 1, base 10. Cero grados de libertad: al plotear "
         "(n, espejo(n)) cada decada cae exacta sobre la recta x + y = 10^k."),

    fila("el espejo en base 2 baja estrictamente, luego toda orbita cae en una "
         "potencia de 2",
         "todo_n", "demostrado", "mallaespejo2.py",
         "propio (una linea de algebra)",
         "Ambito: todo n >= 1. Es el analogo DEMOSTRADO de 'todo cae en el 1'. "
         "De 1 a 100.000: largos de ciclo {1: 100000}, ni un solo 2-ciclo."),

    fila("el espejo en base b tiene puntos fijos exactamente (b/2)*b^m si b es "
         "par, y NI UNO si b es impar",
         "todo_n", "demostrado", "espejobases.py", "propio",
         "Ambito: las 15 bases de 2 a 16, 200.000 numeros cada una, 0 fallos. "
         "Los 5, 50, 500 del base 10 no son peculiaridad del diez: son el caso "
         "b = 10. Y la base 2 es la unica donde puede haber teorema."),

    fila("T(2^k - n) = 2^(k-1) - T(n): en los pasos pares el espejo base 2 "
         "CONMUTA con Collatz",
         "todo_n", "demostrado", "mallaespejo2.py",
         "propio (dos lineas de algebra)",
         "Ambito: n par. 50.000 casos, 0 fallos."),

    fila("T(2^k - n) = 3*2^k + 2 - T(n): en los impares casi conmuta, pero "
         "sobra un +2",
         "todo_n", "demostrado", "mallaespejo2.py",
         "propio (dos lineas de algebra)",
         "Ambito: n impar, 50.000 casos, 0 fallos. Ese +2 es el +1 del 3n+1 "
         "arrastrado. Exacto para UN paso; al segundo se rompe."),

    fila("sigma_clasico(n) = sigma_atajo(n) + (pasos impares dentro de ellos), "
         "exacto",
         "todo_n", "demostrado", "descensoresto.py", "propio",
         "Ambito: todo n >= 2. Cada paso impar del atajo son dos pasos "
         "clasicos, y el valor intermedio 3n+1 es siempre MAYOR que n, asi que "
         "nunca puede ser el que dispara el descenso. Verificado en 5.012 "
         "numeros y en los 34 records de planeo publicados, 0 fallos. Es lo "
         "que permite cruzar el mapa del atajo (donde Terras es exacto) con "
         "los records de ericr.nl (que estan en el clasico)."),

    # -------------------------------------------------------- clase_mod_2k
    #
    # Una comprobacion FINITA que decide para los INFINITOS numeros de la
    # clase. Es lo que el repo llama el cuarto camino.

    fila("los primeros k pasos de cualquier numero los decide n mod 2^k",
         "clase_mod_2k", "demostrado", "mallaresiduos.py",
         "Terras 1976 / Everett 1977",
         "Ambito: todo k >= 1. Tiene nombre: el vector de paridad. 64 restos x "
         "12 representantes = 768 numeros, 0 discrepancias."),

    fila("biyeccion perfecta entre los 2^k restos y los 2^k patrones de "
         "paridad posibles",
         "clase_mod_2k", "demostrado", "mallaresiduos.py",
         "Terras 1976 / Everett 1977",
         "Ambito: SOLO el mapa del ATAJO, k = 1..10. Con la regla CLASICA no "
         "hay biyeccion: salen los Fibonacci. Los dos mapas no se pueden "
         "mezclar, y afirmar lo contrario fue un error que atrapo un "
         "SystemExit antes de dibujar nada."),

    fila("T^k(2^k*m + r) = 3^{S_k(r)} * m + T^k(r): una recta en m cuya "
         "pendiente y ordenada dependen SOLO del resto",
         "clase_mod_2k", "demostrado", "clasesfusion.py",
         "Terras 1976 (Teorema 1.2)",
         "Ambito: todo k, todo r < 2^k. De aqui salen las dos piezas mas "
         "utiles del repo: el criterio de fusion y la pinza de ciclos."),

    fila("dos consecutivos se funden para TODOS los infinitos m de la clase "
         "exactamente cuando S_k(r) == S_k(r+1) y T^k(r) == T^k(r+1)",
         "clase_mod_2k", "demostrado", "clasesfusion.py",
         "propio; Wu-Huang 2001 y Elia-Tucker 2015 lo enuncian casi textual",
         "Ambito: todo k, todo r. Comprobacion finita que vale para infinitos "
         "numeros. Verificado contra fuerza bruta en 9.672 pares, 0 fallos. Y "
         "es la regla R3 de la criba industrial de Barina, que le ahorra 18%."),

    fila("a(32) = 1.871.137.623 clases mod 2^32 se funden: cota inferior "
         "DEMOSTRADA del 43,5658% de los pares consecutivos",
         "clase_mod_2k", "demostrado", "clasesfusion.py", "propio",
         "Ambito: k <= 32. Confirmado por dos caminos independientes, el "
         "secuencial y el repartido por nucleos de clasesparalelo.py. No "
         "depende de muestreo ni de ajuste, y por eso es lo unico duro de esa "
         "seccion. La sucesion no esta en OEIS (28 consultas)."),

    fila("N(k+1) >= 2*N(k) siempre, luego la fraccion f(k) es monotona",
         "clase_mod_2k", "demostrado", "clasesfusion.py", "propio",
         "Ambito: todo k >= 3. La monotonia NO se verifica: se demuestra en "
         "tres lineas. Si r es buena mod 2^k, r y r+2^k son las dos buenas mod "
         "2^(k+1). Presentarla como hallazgo empirico fue un error, corregido."),

    fila("(8k+4, 8k+5) se funden siempre, en 3 pasos",
         "clase_mod_2k", "demostrado", "guardarhilos.py", "Garner 1985",
         "Ambito: todo k >= 0. Rederivado desde el criterio: r=4, k=3 da "
         "T^3(4) = T^3(5) = 2 con S = 1 en los dos. Tasa 1,0000."),

    fila("(32m+5, 32m+6) se funden para todo m",
         "clase_mod_2k", "demostrado", "guardarhilos.py",
         "Wu-Huang 2001 (CITA SIN VERIFICAR: sin DOI, no esta en Crossref)",
         "Ambito: todo m; probado en m = 0,1,2,7,100,3125,9999,40000, todos "
         "con desfase 0. Nuestro par (100005, 100006) es el caso m = 3125. El "
         "HECHO si esta verificado porque el criterio lo rederiva; lo que no "
         "se pudo verificar es la referencia."),

    fila("si dos trayectorias se funden, entonces 2^r*k + n1 y 2^r*k + n2 se "
         "funden para TODO k",
         "clase_mod_2k", "demostrado", "guardarhilos.py", "Garner 1985",
         "Una sola fusion genera una progresion aritmetica infinita de "
         "fusiones. Eso es lo que produce los bloques de numeros consecutivos "
         "con los mismos pasos."),

    fila("por cada resto mod 2^k hay COMO MUCHO UN candidato de ciclo, y sale "
         "en cerrado: m = (r - T^k(r)) / (3^{S(r)} - 2^k)",
         "clase_mod_2k", "demostrado", "pinzaciclos.py",
         "propio (de la identidad de Terras)",
         "Ambito: barrido entero de k = 1..30. Si m no es entero, la clase "
         "queda descartada para los infinitos numeros que contiene. Verificado "
         "contra iteracion cruda y contra una implementacion en Python puro."),

    fila("T^k es una BIYECCION sobre Z/2^k, luego no hay clases que cribar "
         "para buscar ciclos",
         "clase_mod_2k", "demostrado", "pinzaciclos.py", "Terras 1976",
         "Es la razon ESTRUCTURAL de que el barrido de restos este muerto: "
         "cada vector de paridad es una clase unica, hay tantos candidatos "
         "como vectores, y una criba necesita que muchas clases compartan "
         "destino."),

    fila("n = 2^k - 1 (mod 2^k) sube k veces seguidas; n = 0 (mod 2^k) baja k "
         "veces seguidas",
         "clase_mod_2k", "demostrado", "mallaresiduos.py",
         "Terras 1976; es el Lema 8 de Hercher 2023",
         "Ambito: todo k. No son estadisticas: son teoremas, y se escriben "
         "como un if. Con esto se fabrico 2^4000 - 1, que da 3.999 pasos "
         "impares seguidos. El unico objeto que sube SIEMPRE es -1, que es uno "
         "de los ciclos negativos."),

    fila("el ritmo de brotes del arbol inverso es periodico de periodo 2 segun "
         "v mod 3, los hijos ciclan con periodo 3 mod 9, y el patron completo "
         "se repite cada 18 duplicaciones (orden de 2 mod 27)",
         "clase_mod_2k", "demostrado", "mallascerradas.py",
         "propio; la estructura mod 6 / mod 9 es estandar",
         "Ambito: 200 rayos hasta k=44, 2.926 brotes, 0 fallos. OJO CON LA "
         "CASILLA: aqui el modulo es 3^j, no 2^k. Es el mismo TIPO de objeto "
         "-una clase residual que decide el comportamiento sin recorrer nada- "
         "pero el nombre del cuantificador se le queda estrecho."),

    fila("los evitados de la malla 2n mod 27 son exactamente los multiplos de "
         "3, y predicen que rayos del arbol son mudos",
         "clase_mod_2k", "demostrado", "guardarmallas.py", "propio",
         "200 rayos impares, 67 predichos mudos, 0 fallos. Una malla guardada "
         "en disco, calculada sin mirar Collatz ni una vez, predice Collatz "
         "sin volver a calcular Collatz."),

    fila("la malla de restos acierta el arranque de los 173 numeros del 221 y "
         "del 1276, 0 fallos",
         "clase_mod_2k", "medido", "cruzarestos.py", "propio",
         "64 restos contra 173 numeros. Calculada sin mirar el 221 ni una vez: "
         "cada resto usa un representante ajeno a las trayectorias."),

    fila("a(k) >= 1 para todo k: el resto 2^k - 1 sobrevive siempre a la criba "
         "de Brown/Terras, luego la criba NUNCA se vacia",
         "clase_mod_2k", "demostrado", "descensoresto.py", "propio",
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
         "clase_mod_2k", "demostrado", "descensoresto.py", "propio",
         "Medida cero, cardinal infinito. Un contraejemplo de la conjetura "
         "tendria que vivir justo en el conjunto que la criba no ve, y ese "
         "conjunto nunca se queda vacio. Es el mismo muro de pinzaciclos.py "
         "por otra puerta: alli el barrido de restos no podia encontrar ciclos "
         "porque cada clase es un candidato distinto; aqui no puede cerrar el "
         "descenso porque siempre queda clase viva."),

    # --------------------------------------------------------- casi_todo_n
    #
    # Salvo un conjunto de densidad cero. Y el contraejemplo que buscamos
    # podria vivir justo ahi, asi que encadenan con cuidado.

    fila("casi todo n tiene un iterado menor que n",
         "casi_todo_n", "demostrado", None, "Everett 1977 / Terras 1976",
         "Densidad 1 en los enteros positivos. Tres paginas. El truco es usar "
         "la cota pesimista 5/3 en vez del factor exacto 3/2, y asi prescindir "
         "del +1."),

    fila("la condicion X/N < L, con L = log2/log(10/3) = 0,5757, garantiza la "
         "bajada",
         "casi_todo_n", "demostrado", None, "Everett 1977",
         "Traducido a coordenadas del repo: B/A > 0,7369. Es mas flojo A "
         "PROPOSITO. Nuestro 1,585 = log2(3) es el umbral verdadero; el 0,7369 "
         "es el umbral que se SABE demostrar. Esa distancia es el precio de no "
         "tener agujeros."),

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
         "Wagon (OEIS); Lagarias, Applegate-Lagarias",
         "Trayectorias de 2 a 10^7, errores del 0,06% al 0,35%. Los valores "
         "estan en la tabla constantes. Ninguna demuestra nada: son promedios."),

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
         "promedio", "medido", "coralcollaz.py", "propio",
         "Hasta 10^6 semillas. EL 1,7345 PUBLICADO ANTES ERA EL VALOR DE UNA "
         "MUESTRA a HASTA=3.000. Cae a 0,02% de sqrt(3) y la descomposicion "
         "del valor dice que es casual: no construir nada encima."),

    fila("la densidad de pares consecutivos con la misma altura crece con N",
         "promedio", "conjeturado", "densidadfusion.py",
         "Wu Jia-Bang 1995 (conjetura abierta)",
         "Medido hasta 2^28: 0,518577, monotona en los 18 escalones, 0 "
         "bajadas. EL CONTROL QUE IMPORTA: la misma medicion con el PICO en "
         "vez de la altura NO es monotona (10 bajadas de 16). La maquinaria "
         "discrimina. Cruza el 50% entre 2^23 y 2^24: el hito de Garner 1985."),

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
         "promedio", "refutado", "mallaespejo.py", "propio",
         "Roto: la correlacion entre pasos(n) y pasos(espejo(n)) es +0,08. "
         "Segunda prueba: las 5 parejas espejo del 221 dan p = 0,28 contra un "
         "modelo nulo que preserva el reparto de decadas. Un primer calculo "
         "dio '11 contra 1,48 esperadas' y era falso."),

    fila("el puente del espejo base 2 llega mas alla de un paso",
         "promedio", "refutado", "mallaespejo2.py", "propio",
         "Roto: correlacion +0,06, todavia menos que el +0,08 de base 10. Un "
         "paso: identidad exacta. Dos pasos: ruido. El +2 se acumula al iterar "
         "y borra la relacion."),

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
         "promedio", "refutado", "mallaespejo2.py", "propio",
         "Roto: da 33,3% para 3n+1 y para 3n-1 por igual, con los MISMOS "
         "conteos absolutos a N = 256, 1024, 4096 y 10.000. Mide el rango, no "
         "la regla. Las que si discriminan son 'ciclos distintos', 'cola mas "
         "larga' y 'cola media'."),

    fila("la altura de un punto sobre la esfera codifica el tamano del numero",
         "promedio", "refutado", "collazarbol.py", "propio",
         "Roto: correlacion latitud / log2(valor) = 0,12 en los 5.674 numeros "
         "de las ramas. La altura es la distancia real al 1, que es otra cosa. "
         "La esfera es envase, no resultado."),

    fila("el 221 prefiere ciertos restos mod 64",
         "promedio", "refutado", "cruzarestos.py", "propio",
         "Roto: pisa 55 de 64 y el puro azar daria 53,5. Diferencia +1,5. Los "
         "9 restos que nunca pisa no tienen nada en comun. El destino hacia "
         "adelante es ciego a los restos."),

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
         "Ambito: m <= 91. CAJA NEGRA: es el unico sitio por donde entra la "
         "aproximacion diofantica dura. Hallazgo del estudio: Hercher NO usa "
         "el teorema de Baker en ninguna parte, toda la maquinaria pesada "
         "entra como este unico numero importado."),

    fila("cualquier ciclo distinto del trivial mide al menos 19.478.780.533 "
         "pasos",
         "ciclos", "demostrado", None, "literatura 2025",
         "Por eso buscar ciclos escondidos en los 6.555 pares del 221 no podia "
         "encontrar nada: el tramo mas largo mide 114 pasos. La busqueda no "
         "era evidencia de nada."),

    fila("no hay bucles de periodo <= 2.592",
         "ciclos", "demostrado", None, "Terras 1976 (Tabla C, jump values)",
         "ES LA RAZON DE QUE EL BARRIDO DE RESTOS ESTE MUERTO: nuestro k ES "
         "ese periodo, luego todo el rango que un barrido puede alcanzar ya "
         "esta demostrado vacio desde hace cincuenta anos. Para territorio "
         "virgen harian falta 2^2592 restos: un numero de 781 cifras."),

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

    fila("las casillas (A,B) que sobreviven al barrido son exactamente las "
         "convergentes y semiconvergentes de la fraccion continua de log2(3)",
         "ciclos", "demostrado", "collazmalla.py",
         "Terras 1976 Tabla C; Shanks 1965, Guy 1983",
         "480 casillas, las 10 mas cercanas sin excepcion. Guy 1983 imprime la "
         "lista entera y dice que hay ciclos en los denominadores 1, 2, 5, 12 "
         "y ninguno en 41, 53, 306: es casilla por casilla nuestro barrido. La "
         "casilla (7,11) predijo el ciclo negativo de periodo 11."),

    fila("el unico ciclo positivo, escrito con la identidad del repo, es "
         "2^2 = 3^1 + 1, o sea 4 = 3 + 1",
         "ciclos", "demostrado", "collazmalla.py", "propio",
         "A=1, B=2, C=1. De los 95 candidatos enteros positivos que "
         "aparecieron, los 95 ciclan de verdad y son n en {1,2,4} dando 1, 2 o "
         "3 vueltas. Cero impostores."),

    fila("no hay m-ciclos con m <= 95",
         "ciclos", "conjeturado", None, "Wang 2026 (preprint, Zenodo)",
         "Sin arbitrar, cero citas, metadatos descuidados, dos dias de vida. "
         "VERIFICARLO es la fase 3 del plan de la pinza: si aguanta se dice, y "
         "si se cae eso si es un hallazgo."),

    fila("el espejo base 10 tiene 44.450 ciclos distintos bajo 100.000, y "
         "Collatz tiene UNO",
         "ciclos", "medido", "mallaespejo.py", "propio",
         "El A/B de control, y su valor es justo que salgan distintos: la "
         "maquinaria discrimina. Lo que dibuja depende de lo que se le mete, "
         "no de como dibuja."),

    # ----------------------------------------------------- verificado_hasta
    #
    # Fuerza bruta. Sirve para REFUTAR, jamas para demostrar: verificar hasta
    # 2^71 o hasta 2^(10^100) deja exactamente la misma cantidad sin verificar.

    fila("todo n < 2^71 llega al 1",
         "verificado_hasta", "medido", None,
         "Barina 2025, J. Supercomputing",
         "No comprueba los 2^71 numeros: criba clases enteras, con un factor "
         "de reduccion X ~ 363, o sea 1 de cada 363. Coste: 12.395 anos-CPU + "
         "159 anos-GPU. Su worker.c imprime MAXIMUM_CYCLE_OFFSET 0 como "
         "constante literal: el programa no busca ciclos en absoluto."),

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
         "verificado_hasta", "medido", "densidadfusion.py", "propio",
         "Tabla int16 vectorizada por bloques, verificada contra la version "
         "lenta en los primeros 300.000: 0 discrepancias. La racha mas larga "
         "hallada es de 120, en 136.696.632."),

    fila("la tupla mas larga de consecutivos con la misma altura bajo 2^30 "
         "mide 176, empezando en 722.067.240",
         "verificado_hasta", "medido", None, "Wu Jia-Bang 1992",
         "Aqui se llego a 120 en 2^28: compatible con esa trayectoria de "
         "crecimiento, pero no la confirma. No llegamos."),

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

    ("Wu-Huang 2001 es una referencia solida en la que apoyarse",
     "no se pudo verificar: no tiene DOI, no aparece en Crossref, y "
     "Elia-Tucker 2015 no la citan -su bibliografia entera son cuatro "
     "entradas. El HECHO si esta verificado, porque el criterio lo rederiva "
     "(2026-07-30)",
     "una cita copiada de otro sitio no es una cita comprobada. Hay que "
     "separar 'el hecho es cierto' de 'la fuente existe'"),

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
     "elmasuno.py, comprobacion 4 (2026-07-30)",
     "una constante copiada a mano hay que recalcularla desde su definicion "
     "una vez, aunque solo sea decorativa"),

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

    cte("constante de Wagon", 9.4779555565593, 9.471872, -0.064,
        "tiempo de caida medio",
        "cuantos pasos tarda de media un numero en bajar por debajo de si mismo",
        "Wagon; tiene entrada propia en OEIS", None,
        None),

    cte("hermana de Wagon (conteo reducido)", 3.4926518521864, 3.49031, -0.067,
        "el mismo tiempo de caida contando solo los pasos impares",
        "la version del tiempo de caida con el conteo reducido",
        "Wagon", None,
        None),

    cte("media geometrica por paso del atajo", 0.8660254037844386, 0.8643758,
        -0.190, "sqrt(3)/2",
        "por cuanto multiplica de media cada paso del mapa del atajo",
        "propio; es el modelo estandar", None,
        "Que sea menor que 1 dice 'en promedio bajan', y NO impide que exista "
        "una orbita que suba para siempre: seria un conjunto de medida cero. "
        "Prueba: 5n+1 tiene media 1,118 > 1 y aun asi tiene el ciclo del 13."),

    cte("pasos impares contra ln(n)", 3.476059496782208, 3.46363, -0.35,
        "1/ln(4/3)",
        "cuantos 3n+1 se aplican por cada unidad de ln(n)",
        "Lagarias, Applegate-Lagarias", None,
        None),

    cte("constante de parada del ATAJO", 6.952118993564416, 6.93247, -0.28,
        "2/ln(4/3)",
        "cuantos pasos del mapa del atajo por cada unidad de ln(n)",
        "Lagarias, Applegate-Lagarias", None,
        "ES LA DEL ATAJO, NO LA DEL CLASICO. La del clasico es "
        "3/ln(4/3) = 10,428. Confundirlas da un 49,5% de error, y ya paso una "
        "vez en este repo. La escalera correcta es 1:2:3 segun se cuenten los "
        "3n+1, los pasos del atajo o los clasicos."),

    cte("constante de parada CLASICA", 10.428178490346623, 10.3961, -0.31,
        "3/ln(4/3)",
        "cuantos pasos del mapa clasico 3n+1 por cada unidad de ln(n)",
        "Lagarias, Applegate-Lagarias", None,
        None),

    cte("divisiones por multiplicacion B/A", 2.0, 2.014002, +0.70,
        "la valuacion 2-adica media de 3n+1, que vale 2 porque P(v=k) = 2^-k",
        "cuantas divisiones entre dos hay por cada 3n+1",
        "propio", None,
        "CONVERGE A 2, NO A log2(3). El log2(3) = 1,585 es el punto de "
        "EQUILIBRIO, no el valor tipico: son dos numeros distintos y no se "
        "contradicen. Y el estimador correcto es el AGREGADO suma(B)/suma(A): "
        "la media de razones trayectoria a trayectoria da 2,174 por Jensen."),

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

    cte("grosor de la lamina, ln(Res(993))", 0.2256541127319812, 0.2286, None,
        "ln( 2^61 / (3^32 * 993) )",
        "cuanto se separa como maximo un punto de la lamina del plano de "
        "equilibrio",
        "Roosendaal (conjeturado)", "elmasuno.py",
        "El 0,2286 medido en collazlamina.py es sobre PARES de una trayectoria "
        "y el 0,225654 es sobre trayectorias enteras: no son el mismo barrido. "
        "Que eps sea > 0 esta demostrado; que este ACOTADO por este numero "
        "sigue siendo la conjetura de Roosendaal."),

    cte("L de Everett", 0.5757166424934449, None, None,
        "log(2) / log(10/3)",
        "la fraccion de pasos impares por debajo de la cual Everett garantiza "
        "la bajada",
        "Everett 1977", None,
        "Es el umbral que se SABE demostrar, no el verdadero. Traducido: "
        "B/A > 0,7369, mientras que el exacto es B/A > log2(3) = 1,585. La "
        "distancia entre los dos es el precio de una demostracion sin "
        "agujeros."),

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
        "propio", "coralcollaz.py",
        "NO ES UNA CONSTANTE. El 1,7345 que se publico era el valor de una "
        "MUESTRA a HASTA = 3.000; se asienta en 1,7320 +/- 0,0003 y la cuarta "
        "cifra nunca fue estable. Que caiga a 0,02% de sqrt(3) es CASUAL: la "
        "descomposicion del valor lo dice. El valor teorico de esta fila es "
        "sqrt(3) puesto solo para poder comparar, no porque lo sea."),
]


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
                      ('todo_n','clase_mod_2k','casi_todo_n','promedio',
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
print("LAS QUE COMPONEN - 'todo_n' demostradas y 'clase_mod_2k'")
print("=" * ANCHO)
print()
print("  Son las unicas con las que se puede encadenar un argumento: valen")
print("  para CADA numero, o para los INFINITOS numeros de una clase.")
print()

componen = c2.execute(
    "SELECT cuantificador, enunciado, fichero FROM afirmaciones"
    " WHERE cuantificador='clase_mod_2k'"
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
