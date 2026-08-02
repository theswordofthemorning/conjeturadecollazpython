import json, io, sys, math
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
MIA = r'C:\Users\Home\AppData\Local\Temp\claude\C--Users-Home-Desktop-conjeturadecollazpython\071adcbb-695f-4c3b-9a59-7ca5d8a77d8a\scratchpad\depuracion'

# C12: el 0,2286 del 221 = log2(2^73/(3^41*221)), calculado aqui mismo
eps221 = 73 - 41 * math.log2(3) - math.log2(221)
assert abs(eps221 - 0.228634911) < 1e-8

E = ('pasada local 02-08-2026: scripts del repo (exit 0, SystemExit intactos) + consolidado '
     'propio escrito de cero + 4 .lean recompilados sin sorryAx. Salidas en scratchpad/megaB_local. '
     'SIN trio: la independencia la dan los scripts ya cruzados del repo y la re-derivacion propia.')

CONF = 'CONFIRMADA'; CORR = 'CORREGIDA'; ND = 'NO_DECIDIBLE'
V = {
 'A32': (CONF, 'malla k=6 (atajo): 0 fallos sobre los numeros del 221 y del 1276. Nota: son 115 distintos (115+58 con solape; el 1276 vive dentro de la trayectoria del 221), el 173 de la ficha cuenta las dos listas', ''),
 'A35': (CONF, 'teorema de Everett 1977 (arbitrado); su aritmetica local re-verificada en verificar_everett.py: desigualdad entera 0 fallos, la condicion correcta garantiza el descenso', ''),
 'A36': (CONF, 'verificar_everett.py: 0 fallos en enteros exactos; la condicion con N=pasos del atajo garantiza la bajada', ''),
 'A37': (ND, 'bibliografica: Tao 2019, arbitrado. No verificable localmente; ninguna parte aritmetica que re-derivar aqui', ''),
 'A38': (CONF, 'la parte finita es teorema (biyeccion resto-patron exacta k=1..10, cada patron una vez, re-derivada); como enunciado sobre trayectorias enteras sigue siendo conjetura/heuristica y asi esta etiquetada', ''),
 'A39': (ND, 'bibliografica (heuristica 5x+1); sin re-derivacion local', ''),
 'A40': (CONF, 'verificar_constantes.py exit 0: Wagon a 35 cifras contra A122790, escalera con dos estimadores, todas las comprobaciones pasaron', ''),
 'A41': (CONF, 'valuacion 2-adica media re-medida de cero: 1,99006 sobre 1.899.202 saltos (impares 3..100000); repo 1,99048', ''),
 'A42': (CONF, 'fracciones re-medidas: clasico 0,3315 (~1/3), atajo 0,4959 (~1/2), rango 2..100000', ''),
 'A43': (ND, 'mi re-medicion a 4 ventanas de semilla (10^3..10^6, 1000 seeds c/u) no reproduce una tendencia limpia (0,3311 / 0,3301 / 0,3275 / 0,3302). El enunciado viene de la sesion sin ficheros; sigue siendo un numero sin codigo detras', ''),
 'A44': (ND, 'coral: barrido caro, prohibido re-ejecutar (regla del repo). Pendiente de pasada CPU dedicada', ''),
 'A45': (CONF, 'tendencia re-medida de cero: 0,4162 a 10^4 -> 0,4502 a 10^5, crece con N', ''),
 'A46': (CONF, 'descensoresto.py exit 0 (56 s), techo heuristico consistente con la tabla', ''),
 'A47': (CONF, 'descensoresto.py exit 0: prediccion de planeo desde la densidad reproducida', ''),
 'A48': (CONF, 'corr re-medida = 0,5931 sobre 50.000 impares (repo 0,59). La refutacion de la PREDICCION se mantiene; la medicion es correcta', ''),
 'A49': (CONF, 'la refutacion aguanta: corr = 0,047 sobre 99.994 casos a 10^5 (nula). El +0,08 del repo es de otro rango no declarado - la conclusion no cambia', ''),
 'A50': (CONF, 'corr = 0,0635 a 5*10^4 (repo +0,06): ruido. La refutacion aguanta', ''),
 'A51': (CONF, 'verificado EXACTO: sobre los 2^13 residuos completos (base 2^60), la desviacion maxima de 0,5 al predecir el bit siguiente de los 8 anteriores es 0,0 - la biyeccion lo fuerza. El 50,5% de la red es instrumental. (Primer intento propio contaminaba con la cola post-convergencia: capa 1 lo cazo)', ''),
 'A52': (ND, 'irreproducible: el modelo nulo (9 constantes x 8 transformaciones x 16 fundamentales) no quedo registrado en forma ejecutable. Del pasivo "numeros sin codigo"', ''),
 'A53': (CONF, 'reproducido debil con parametrizacion distinta (techo 1000N: 0 escapes en los dos mapas - tampoco discrimina). La conclusion "la fila mide el rango, no la regla" aguanta', ''),
 'A54': (ND, 'irreproducible POR DISENO: "latitud" era coordenada de un dibujo borrado en la purga. Queda como negativo anotado, no como medicion viva', ''),
 'A55': (CONF, 'reproducido exacto: 55/64 restos pisados (azar 53,5) y los MISMOS 9 nunca pisados [0,13,21,25,26,37,45,48,51]', ''),
 'A56': (CONF, 'reimpl.py exit 0: 7/7 m2, 7/7 cotas; verificar_ciclos.py [5] segunda via identica', ''),
 'A57': (CONF, 'verificar_ciclos.py: el 1,4784 re-derivado por biseccion (k2(91)=1,478381), tabla de campeones 4/4', ''),
 'A58': (CONF, 'verificar_ciclos.py exit 0: certificada por tres caminos; el 217.976.794.617 de Barina exige X0>=2^71,884 y el record es 2^71,019', ''),
 'A59': (CONF, 'verificar_frontera_ciclos.py exit 0: frontera recalculada con el hueco entre jump values comprobado', ''),
 'A60': (CONF, 'pinza re-derivada de cero a escala k<=16: recupera exactamente {1,2} positivos y los miembros de los tres ciclos negativos (+0). El barrido k=30 completo no se re-ejecuta (regla del repo)', ''),
 'A64': (ND, 'preprint de Wang sin arbitrar (Fase 3 del plan de la pinza, pendiente). No es verificable aqui todavia', ''),
 'A65': (CORR, 'DEMOSTRACION combinatoria: bajo 100.000 hay 90.000 numeros sin cero final, 1.098 palindromos, luego (90.000-1.098)/2 = 44.451 dos-ciclos exactos (mas los 1.098 fijos = 45.549 ciclos). El 44.450 publicado tiene un off-by-one. Collatz positivo sigue teniendo 1',
          'el espejo base 10 tiene 44.451 dos-ciclos (y 1.098 palindromos fijos) bajo 100.000 - cerrado, no medido: (90.000 reversibles - 1.098 palindromos)/2. Collatz tiene UN ciclo positivo'),
 'A66': (ND, 'bibliografica (Barina 2025, arbitrado): no verificable localmente. Consistente con los records de 71 bits cruzados en cruzarecords.py', ''),
 'A67': (CONF, 'cruzarecords.py exit 0: 0 residuos fuera de [1, 1,253142144] hasta 2^71', ''),
 'A68': (CONF, 'elmasuno.py exit 0: maximo de eps en 993 y dobles, RES_993 calculado no copiado', ''),
 'A69': (CONF, 'pinza re-derivada a k<=16: supervivientes positivos exactamente {1,2}. El barrido 2^30 no se re-ejecuta (regla del repo); su salida esta registrada', ''),
 'A70': (CONF, 'tendencia re-medida (0,4162 -> 0,4502 a 10^5) consistente; el 0,5186 a 2^28 conserva la reserva ya documentada (fichero retirado, orden de magnitud)', ''),
 'A71': (CORR, 'verificar_wu.py: la tupla de 176 desde 722.067.240 se confirma entera; la MAXIMALIDAD bajo 2^30 no se re-verifica (exigiria el barrido completo) - es de Wu 1992-95',
          'hay una tupla de 176 consecutivos con la misma altura empezando en 722.067.240 (verificada una a una); que sea la mas larga bajo 2^30 es de Wu 1992-95 y no se re-verifico'),
 'A72': (ND, 'coralprimos.py esta en la lista de barridos que no se re-ejecutan. Pendiente de pasada CPU dedicada', ''),
 'A73': (ND, 'idem A72: la recta (N+11)/2 / (N+19)/2 queda medida-no-demostrada, como ya declara el CLAUDE.md', ''),
 'A74': (ND, 'idem A72', ''),
 'A75': (CONF, 'cruzarecords.py exit 0: 98 altitudes y 148 retrasos recalculados, 0 discrepancias', ''),
 'A76': (CONF, 'identidad re-derivada de cero: 6.555 pares del 221, 0 fallos', ''),
 'A77': (CONF, 'descensoresto.py exit 0: A076227 45 terminos, 0 discrepancias', ''),
 'A78': (CONF, 'descensoresto.py exit 0: 34 records de planeo recalculados', ''),
 'A79': (CONF, 'descensoresto.py exit 0: sigma_max/k crece con dientes de sierra, sin estabilizarse', ''),
 'A80': (CONF, 'consulta directa a hilos.db: 983 cruces no-cola, 833 con desfase 0 - exacto', ''),
 'C1': (CONF, 'verificar_constantes.py: Wagon confirmada a 35 cifras contra A122790 por camino independiente', ''),
 'C2': (CONF, 'la teorica es E[sigma]/2 por Doob (verificada); el 3,49031 medido sigue marcado como numero sin explicar (sesion sin ficheros)', ''),
 'C3': (CONF, 'verificar_constantes.py exit 0', ''),
 'C4': (CONF, 'verificar_constantes.py: escalera con dos estimadores, pendiente vs agregado declarados', ''),
 'C5': (CONF, 'idem C4; es la del ATAJO', ''),
 'C6': (CONF, 'idem C4; es la CLASICA (3/ln(4/3))', ''),
 'C7': (CONF, 'agregado 2,014 a 10^6 y pendiente 2,0018 a 10^7, ya con el estimador declarado; mi valuacion media independiente da 1,99006', ''),
 'C8': (CONF, 're-medida de cero: 1,99006 sobre 1,9M saltos (teorico 2 = suma k*2^-k)', ''),
 'C9': (CONF, 'constante matematica exacta (log2 3); su papel de equilibrio esta demostrado en los .lean del repo', ''),
 'C10': (CONF, 'elmasuno.py exit 0: 2^61/(3^32*993) calculado, no copiado, con SystemExit anti-errata', ''),
 'C11': (CONF, 'elmasuno.py exit 0: ln(Res(993)) = 0,225654 nats = 0,325550 bits, unidades ya corregidas en CLAUDE.md', ''),
 'C12': (CONF, 'recalculado aqui: log2(2^73/(3^41*221)) = 0,228634911 exacto - es el eps del 221 en bits, no una cota; la correccion de unidades ya esta escrita', ''),
 'C13': (CONF, 'verificar_everett.py exit 0: L y 1/L = 1,73697 con la traduccion corregida X=A, N=B', ''),
 'C14': (CONF, 're-medida: 0,4959 a 10^5 (la ficha dice 0,4965; mismo orden, estimadores por-paso)', ''),
 'C15': (CONF, 're-medida: 0,3315 a 10^5 (ficha 0,3318)', ''),
 'C16': (CONF, 'heredada del trio A22 (CONFIRMADA): a(32)=1.871.137.623 por dos caminos, fraccion exacta', ''),
 'C17': (CONF, 'el umbral q=4 es algebra exacta (q^(1/2)=2); el 4,0019 medido viene de la sesion sin ficheros y conserva esa reserva', ''),
 'C18': (CONF, 'descensoresto.py: H(log_3 2)=0,949956 asintotico, con el aviso de regimen (0,108 en k=34) ya corregido - y reconfirmado por el trio A34', ''),
 'C19': (CONF, 'descensoresto.py: techo 32,59 no alcanzado en rango (26,79 a k=26 subiendo), coherente con A79', ''),
 'C20': (ND, 'coral: no se re-ejecuta (regla del repo). El valor teorico sqrt(3) es algebra; el 1,7320+-0,0003 medido conserva su rango declarado', ''),
}
assert len(V) == 64, len(V)
ver_path = MIA + r'\veredictos.jsonl'
ya = {json.loads(l)['id'] for l in open(ver_path, encoding='utf-8') if l.strip()}
with open(ver_path, 'a', encoding='utf-8') as fh:
    for iid, (v, resumen, corr) in V.items():
        assert iid not in ya, iid
        tabla = 'constantes' if iid.startswith('C') else 'afirmaciones'
        fila = {'lote': 'megaBCD-local', 'id': iid, 'tabla': tabla, 'metodo': E,
                'lean': None, 'python': None,
                'comparador': {'veredicto': v, 'resumen': resumen, 'correccion_exacta': corr}}
        fh.write(json.dumps(fila, ensure_ascii=False) + '\n')
filas = [json.loads(l) for l in open(ver_path, encoding='utf-8') if l.strip()]
cnt = Counter((f.get('comparador') or {}).get('veredicto', '?') for f in filas)
print('MARCADOR FINAL:', len(filas), 'de 100:', dict(cnt))
