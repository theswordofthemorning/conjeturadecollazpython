"""Tanda de YAH (Yolcu-Aaronson-Heule) sobre la escalera del piloto.

Para cada peldaño hace una cascada de quitar reglas con interpretaciones
matriciales: prueba las formas de FORMAS en orden, de la más barata a la
más cara, sobre el sistema que queda. Cada forma corre el probador de YAH
con -any (quita al menos una regla estricta por vuelta) y repite con esa
misma forma hasta quedarse sin reglas estrictas (QED) o hasta UNSAT. Lo
que queda se guarda con -out y pasa a ser el sistema actual; tras cada
avance se vuelve a la primera forma y al primer tope.

Una forma que da UNSAT sobre un sistema no tiene prueba de esa forma y no se
repite sobre ese sistema. Una que agota el tope se reintenta en la pasada
siguiente con un tope mayor (TOPES). Si se acaban las pasadas sin QED, el
peldaño queda "sin prueba": eso no es un contraejemplo ni prueba nada.

Invertir las cadenas (-rev) conserva la terminación, así que cada forma se
prueba en las dos orientaciones. El sistema que escribe -out tras una
corrida con -rev está invertido; se anota, pero no cambia nada.

Cada quitada la comprueba el propio YAH con NumPy, aparte del SAT. Un QED
del peldaño 5 hay que cotejarlo después con otra herramienta o un
certificado: esta tanda busca, no certifica.

Los peldaños 1 a 4 son de calibración (AProVE da YES en los cuatro): corren
sólo la primera pasada, con CALIBRACION segundos por forma, y su resultado
se informa sin detener la tanda.

Con --debilitadas corre en su lugar la escalera de G debilitadas de
debilitar.py (DEBILITADAS, de la más débil a la más cercana a G), con
TOPES_DEBILITADAS, y deja los resultados en resultados_debilitadas/. Usa su
propia carpeta de trabajo. lanzar.sh admite una sola tanda a la vez.

Con --diagnostico calibra y prueba G_B4..G_B7 sólo mientras haya QED:
30 s por forma, 1800 s globales y cuatro solucionadores. Guarda en una
carpeta nueva fuera del repo. Las carpetas anteriores nunca se borran.

Uso:  python3 -I lanzar.py [--solo-calibracion | --sin-calibracion | --debilitadas] [--ensayo]
Con --ensayo sólo corre el peldaño 1 con 30 s por forma, para probar el
lanzador. La variable TANDA_RESULTADOS indica otra carpeta de resultados.
"""
import datetime
import hashlib
import glob
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
YAH = "/home/oem/herramientas/yah/rewriting-collatz"
PYTHON = os.path.join(YAH, ".venv", "bin", "python")
SISTEMAS = os.path.join(AQUI, "sistemas")
RES = os.environ.get("TANDA_RESULTADOS") or os.path.join(AQUI, "resultados")
# carpeta de trabajo de YAH: ahí busca ./cadical y deja sus CNF en tmp/
TRABAJO = YAH
GB = 2 ** 30

CALIBRACION = ["peldano1_X", "peldano2_sinL", "peldano3_ramaA", "peldano4_ramaB"]
PILOTO = "peldano5_completo"
DEBILITADAS = ["G_A2", "G_B4", "G_A3", "G_B5", "G_A4", "G_B6", "G_A5", "G_B7"]

# (interpretación, dimensión, ancho del resultado), de la más barata a la más cara
FORMAS = (
    [("natural", d, rw) for d, rw in [(1, 3), (2, 3), (2, 4), (3, 3), (3, 4),
                                      (4, 4), (5, 4), (6, 4)]]
    + [("arctic", d, rw) for d, rw in [(2, 3), (2, 4), (3, 3), (3, 4), (4, 4),
                                       (5, 4), (5, 5)]]
    + [("tropical", d, rw) for d, rw in [(2, 3), (3, 3), (4, 4)]]
)
ORIENTACIONES = [False, True]   # False: tal cual; True: con -rev
TOPES = [120, 900, 3600]        # segundos por forma en cada pasada del piloto
CALIBRACION_TOPE = 60
TOPES_DEBILITADAS = [120, 900, 3600]

TRABAJADORES = 6                # solucionadores a la vez (núcleos físicos)
MEMORIA_LIBRE = 3 * GB          # espera a tener esto libre antes de cada corrida
MEMORIA_PROCESO = 6 * GB        # tope de memoria virtual de cada proceso
ESPERA_MAXIMA = 1800            # segundos esperando memoria antes de rendirse

hijo = None
limite_tanda = None


def segundos_disponibles():
    return float("inf") if limite_tanda is None else max(0, limite_tanda - time.monotonic())


def ahora():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def decir(texto):
    print(f"[{ahora()}] {texto}", flush=True)


def memoria_disponible():
    with open("/proc/meminfo") as f:
        for linea in f:
            if linea.startswith("MemAvailable:"):
                return int(linea.split()[1]) * 1024
    return 0


def esperar_memoria():
    inicio = time.time()
    avisado = False
    while memoria_disponible() < MEMORIA_LIBRE:
        if segundos_disponibles() <= 0:
            return False
        if not avisado:
            decir(f"espero memoria: libres {memoria_disponible() / GB:.1f} GB")
            avisado = True
        if time.time() - inicio > ESPERA_MAXIMA:
            return False
        time.sleep(min(10, segundos_disponibles()))
    return True


def reglas_estrictas(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as f:
        return sum(1 for linea in f
                   if " -> " in linea and not linea.lstrip().startswith("//"))


def limitar():
    import resource
    os.nice(10)
    resource.setrlimit(resource.RLIMIT_AS, (MEMORIA_PROCESO, MEMORIA_PROCESO))


def cortar_hijo(*_):
    if hijo is not None and hijo.poll() is None:
        try:
            os.killpg(hijo.pid, signal.SIGTERM)
            time.sleep(2)
            os.killpg(hijo.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def al_parar(*_):
    cortar_hijo()
    decir("parada pedida: corto la corrida en curso")
    sys.exit(130)


def correr_forma(actual, forma, rev, tope, carpeta, numero):
    """Corre una forma. Devuelve (resultado, ruta del sistema que queda o None, segundos)."""
    global hijo
    interp, d, rw = forma
    nombre = f"{numero:03d}_{interp}_d{d}_rw{rw}{'_rev' if rev else ''}"
    salida = os.path.join(carpeta, nombre + ".srs")
    registro = os.path.join(carpeta, nombre + ".log")
    orden = [PYTHON, "-W", "ignore", "-u", os.path.join(YAH, "prover", "main.py"),
             actual, "-spc", "-i", interp, "-d", str(d), "-rw", str(rw), "-any",
             "-work", str(TRABAJADORES), "-sol", "cadical", "-out", salida, "-asc"]
    if rev:
        orden.append("-rev")
    if not esperar_memoria():
        return ("presupuesto agotado" if segundos_disponibles() <= 0 else "sin memoria"), None, 0.0
    if segundos_disponibles() <= 0:
        return "presupuesto agotado", None, 0.0
    tope = min(tope, segundos_disponibles())
    inicio = time.time()
    with open(registro, "w", encoding="utf-8") as f:
        f.write("$ " + " ".join(orden) + "\n\n")
        f.flush()
        hijo = subprocess.Popen(orden, cwd=TRABAJO, stdout=f, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, start_new_session=True,
                                preexec_fn=limitar)
        try:
            codigo = hijo.wait(timeout=tope)
        except subprocess.TimeoutExpired:
            cortar_hijo()
            hijo.wait()
            codigo = None
    hijo = None
    segundos = time.time() - inicio
    # los CNF de una corrida cortada no los borra YAH
    for cnf in glob.glob(os.path.join(TRABAJO, "tmp", "tmp*")):
        try:
            if os.path.getmtime(cnf) >= inicio - 1:
                os.remove(cnf)
        except OSError:
            pass
    if codigo == 19:
        resultado = "QED"
    elif codigo == 29:
        resultado = "UNSAT"
    elif codigo is None:
        resultado = "tope"
    else:
        resultado = f"error {codigo}"
    antes = reglas_estrictas(actual)
    despues = reglas_estrictas(salida)
    if resultado != "QED" and despues is not None and despues < antes:
        return resultado + " con avance", salida, segundos
    return resultado, None, segundos


def cascada(peldano, topes, resumen):
    carpeta = os.path.join(RES, peldano)
    if os.path.exists(carpeta):
        raise FileExistsError(f"Se conserva {carpeta}; elige otro TANDA_RESULTADOS")
    os.makedirs(carpeta)
    actual = os.path.join(carpeta, "000_inicio.srs")
    shutil.copy(os.path.join(SISTEMAS, peldano + ".srs"), actual)
    invertido = False
    etapas = []
    corridas = []
    resumen[peldano] = {"etapas": etapas, "corridas": corridas, "veredicto": None}
    numero = 0
    descartadas = set()     # (forma, rev) con UNSAT sobre el sistema actual
    pasada = 0
    decir(f"== {peldano}: {reglas_estrictas(actual)} reglas estrictas")
    while pasada < len(topes):
        tope = topes[pasada]
        avance = False
        for forma in FORMAS:
            for rev in ORIENTACIONES:
                if segundos_disponibles() <= 0:
                    resumen[peldano]["veredicto"] = "parado: presupuesto agotado"
                    guardar(resumen)
                    return False
                if (forma, rev) in descartadas:
                    continue
                numero += 1
                resultado, siguiente, segundos = correr_forma(actual, forma, rev, tope,
                                                              carpeta, numero)
                fila = {"numero": numero, "forma": list(forma), "rev": rev, "tope": tope,
                        "resultado": resultado, "segundos": round(segundos, 1),
                        "reglas_antes": reglas_estrictas(actual)}
                corridas.append(fila)
                guardar(resumen)
                decir(f"{peldano} #{numero} {forma[0]} d{forma[1]} rw{forma[2]}"
                      f"{' rev' if rev else ''} tope {tope} s: {resultado} ({segundos:.0f} s)")
                if resultado in ("sin memoria", "presupuesto agotado") or resultado.startswith("error"):
                    resumen[peldano]["veredicto"] = "parado: " + resultado
                    guardar(resumen)
                    return False
                if resultado == "QED":
                    etapas.append({"numero": numero, "forma": list(forma), "rev": rev,
                                   "quedan": 0})
                    resumen[peldano]["veredicto"] = "QED"
                    guardar(resumen)
                    decir(f"== {peldano}: QED")
                    return True
                if resultado.startswith("UNSAT") and siguiente is None:
                    descartadas.add((forma, rev))
                if siguiente is not None:
                    actual = siguiente
                    invertido ^= rev
                    quedan = reglas_estrictas(actual)
                    etapas.append({"numero": numero, "forma": list(forma), "rev": rev,
                                   "quedan": quedan, "sistema": os.path.basename(actual),
                                   "invertido": invertido})
                    guardar(resumen)
                    decir(f"{peldano}: avance, quedan {quedan} reglas estrictas")
                    avance = True
                    break
            if avance:
                break
        if avance:
            descartadas = set()
            pasada = 0
        else:
            pasada += 1
    resumen[peldano]["veredicto"] = "sin prueba"
    guardar(resumen)
    decir(f"== {peldano}: sin prueba con estas formas y topes "
          f"(quedan {reglas_estrictas(actual)} reglas estrictas)")
    return False


def guardar(resumen):
    with open(os.path.join(RES, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)


def main():
    global RES, TRABAJO, TRABAJADORES, limite_tanda
    signal.signal(signal.SIGTERM, al_parar)
    signal.signal(signal.SIGINT, al_parar)
    argumentos = sys.argv[1:]
    diagnostico = "--diagnostico" in argumentos
    if diagnostico and any(a != "--diagnostico" for a in argumentos):
        raise SystemExit("--diagnostico se usa solo; no combinar con los perfiles antiguos")
    if diagnostico:
        TRABAJADORES = 4
        limite_tanda = time.monotonic() + 1800
        if not os.environ.get("TANDA_RESULTADOS"):
            base = os.path.expanduser("~/herramientas/yah/resultados")
            os.makedirs(base, exist_ok=True)
            RES = tempfile.mkdtemp(prefix="diagnostico-", dir=base)
    if "--debilitadas" in argumentos and not os.environ.get("TANDA_RESULTADOS"):
        RES = os.path.join(AQUI, "resultados_debilitadas")
    os.makedirs(RES, exist_ok=True)
    if "--debilitadas" in argumentos or diagnostico:
        # carpeta de trabajo propia, para no borrar los CNF de otra tanda a la vez
        TRABAJO = os.path.join(RES, "trabajo")
        os.makedirs(TRABAJO, exist_ok=True)
        enlace = os.path.join(TRABAJO, "cadical")
        if not os.path.exists(enlace):
            os.symlink(os.path.join(YAH, "cadical"), enlace)
    if diagnostico:
        plan = [(p, [30]) for p in CALIBRACION + ["G_B4", "G_B5", "G_B6", "G_B7"]]
    elif "--ensayo" in argumentos:
        plan = [("peldano1_X", [30])]
    elif "--debilitadas" in argumentos:
        plan = [(p, TOPES_DEBILITADAS) for p in DEBILITADAS]
    else:
        plan = []
        if "--sin-calibracion" not in argumentos:
            plan += [(p, [CALIBRACION_TOPE]) for p in CALIBRACION]
        if "--solo-calibracion" not in argumentos:
            plan.append((PILOTO, TOPES))
    # Una carpeta con evidencia nunca se reutiliza, tampoco al relanzar el perfil antiguo.
    if os.path.exists(os.path.join(RES, "resumen.json")) or any(
            os.path.exists(os.path.join(RES, p)) for p, _ in plan):
        raise SystemExit("Resultados existentes: usa un TANDA_RESULTADOS nuevo")
    huellas = {}
    for p, _ in plan:
        with open(os.path.join(SISTEMAS, p + ".srs"), "rb") as f:
            huellas[p] = hashlib.sha256(f.read()).hexdigest()
    resumen = {"inicio": ahora(), "formas": len(FORMAS) * len(ORIENTACIONES),
               "perfil": "diagnostico" if diagnostico else "historico",
               "presupuesto_segundos": 1800 if diagnostico else None,
               "sha256_sistemas": huellas,
               "trabajadores": TRABAJADORES, "plan": [[p, t] for p, t in plan]}
    decir(f"resultados: {RES}")
    guardar(resumen)
    decir(f"tanda de YAH: {len(plan)} peldaños, {resumen['formas']} formas, "
          f"{TRABAJADORES} solucionadores, libres {memoria_disponible() / GB:.1f} GB")
    for peldano, topes in plan:
        exito = cascada(peldano, topes, resumen)
        if diagnostico and not exito:
            resumen["detencion"] = f"{peldano}: {resumen[peldano]['veredicto']}"
            decir("diagnóstico detenido; revisar antes de ampliar la búsqueda")
            break
    resumen["fin"] = ahora()
    guardar(resumen)
    decir("fin de la tanda")


if __name__ == "__main__":
    main()
