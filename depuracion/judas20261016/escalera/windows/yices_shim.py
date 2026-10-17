"""Adaptador: imita la interfaz de Yices 1 que usa AProVE y resuelve con Z3/MiniSat.

Modos que llama AProVE:
  yices -e FICHERO        lenguaje nativo de Yices 1 (define/assert/check)
  yices -d -e FICHERO     CNF en DIMACS
  yices -smt ...          SMT-LIB 1 (no soportado: responde unknown)
Ante cualquier construccion no traducida responde "unknown" y lo apunta en
yices_shim.log; "unknown" nunca permite a AProVE concluir nada falso.
"""
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
Z3 = r"C:\Users\Home\herramientas\z3\z3-5.3.1-x64-win\bin\z3.exe"
MINISAT = os.path.join(AQUI, "minisat2.exe")
LOG = os.path.join(AQUI, "yices_shim.log")


class NoSoportado(Exception):
    pass


def apuntar(msg):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%H:%M:%S ") + msg.replace("\n", " ")[:400] + "\n")
    except OSError:
        pass


def tokens(texto):
    out, i, n = [], 0, len(texto)
    while i < n:
        c = texto[i]
        if c in "()":
            out.append(c)
            i += 1
        elif c.isspace():
            i += 1
        elif c == ";":
            while i < n and texto[i] != "\n":
                i += 1
        else:
            j = i
            while j < n and not texto[j].isspace() and texto[j] not in "();":
                j += 1
            out.append(texto[i:j])
            i = j
    return out


def arbol(toks):
    pila, actual = [], []
    for t in toks:
        if t == "(":
            pila.append(actual)
            actual = []
        elif t == ")":
            hecho = actual
            actual = pila.pop()
            actual.append(hecho)
        else:
            actual.append(t)
    if pila:
        raise NoSoportado("parentesis desequilibrados")
    return actual


def tipo(t):
    if isinstance(t, str):
        base = {"int": "Int", "bool": "Bool", "real": "Real", "nat": "Int"}
        if t in base:
            return base[t]
        raise NoSoportado("tipo " + t)
    if t and t[0] == "->":
        raise NoSoportado("tipo funcion anidado")
    raise NoSoportado("tipo " + repr(t))


def nombre_y_tipo(partes):
    """De ['x::int'] o ['x::', T] o ['x', '::', T] saca (nombre, T, resto)."""
    a = partes[0]
    if not isinstance(a, str):
        raise NoSoportado("define sin nombre")
    if "::" in a and not a.endswith("::"):
        n, t = a.split("::", 1)
        return n, t, partes[1:]
    if a.endswith("::"):
        return a[:-2], partes[1], partes[2:]
    if len(partes) > 2 and partes[1] == "::":
        return a, partes[2], partes[3:]
    raise NoSoportado("define sin tipo " + a)


OPS = {"+": "+", "-": "-", "*": "*", "<": "<", "<=": "<=", "=": "=", ">": ">",
       ">=": ">=", "and": "and", "or": "or", "not": "not", "ite": "ite",
       "if": "ite", "=>": "=>", "/=": "distinct", "div": "div", "mod": "mod"}


def atomo(a):
    if a in ("true", "false"):
        return a
    if a.lstrip("-").isdigit():
        return a if not a.startswith("-") else "(- %s)" % a[1:]
    if "/" in a and a.replace("/", "").lstrip("-").isdigit():
        p, q = a.split("/")
        num = p if not p.startswith("-") else "(- %s)" % p[1:]
        return "(/ %s %s)" % (num, q)
    return "|%s|" % a


def expr(e):
    if isinstance(e, str):
        return atomo(e)
    if not e:
        raise NoSoportado("lista vacia")
    cab = e[0]
    if not isinstance(cab, str):
        raise NoSoportado("cabeza compuesta")
    if cab in OPS:
        if cab == "-" and len(e) == 2:
            return "(- %s)" % expr(e[1])
        return "(%s %s)" % (OPS[cab], " ".join(expr(x) for x in e[1:]))
    if cab in FUNCIONES:
        return "(|%s| %s)" % (cab, " ".join(expr(x) for x in e[1:]))
    raise NoSoportado("operador " + cab)


FUNCIONES = set()


def traducir(texto):
    FUNCIONES.clear()
    lineas, consts = [], []
    for cmd in arbol(tokens(texto)):
        if isinstance(cmd, str) or not cmd:
            raise NoSoportado("orden suelta")
        cab = cmd[0]
        if cab == "define":
            n, t, resto = nombre_y_tipo(cmd[1:])
            if isinstance(t, list) and t and t[0] == "->":
                args = [tipo(x) for x in t[1:-1]]
                ret = tipo(t[-1])
                if not resto:
                    lineas.append("(declare-fun |%s| (%s) %s)" % (n, " ".join(args), ret))
                else:
                    lam = resto[0]
                    if not (isinstance(lam, list) and lam and lam[0] == "lambda"):
                        raise NoSoportado("funcion definida sin lambda")
                    params = []
                    for p in lam[1]:
                        if not isinstance(p, str) or "::" not in p:
                            raise NoSoportado("parametro lambda")
                        pn, pt = p.split("::", 1)
                        params.append("(|%s| %s)" % (pn, tipo(pt)))
                    lineas.append("(define-fun |%s| (%s) %s %s)" % (n, " ".join(params), ret, expr(lam[2])))
                FUNCIONES.add(n)
            else:
                T = tipo(t)
                if resto:
                    lineas.append("(define-fun |%s| () %s %s)" % (n, T, expr(resto[0])))
                else:
                    lineas.append("(declare-const |%s| %s)" % (n, T))
                    consts.append(n)
        elif cab == "assert":
            lineas.append("(assert %s)" % expr(cmd[1]))
        elif cab == "check":
            break
        elif cab in ("set-evidence!", "set-verbosity!", "echo"):
            continue
        else:
            raise NoSoportado("orden " + cab)
    return lineas, consts


def valor(v):
    if isinstance(v, str):
        return v
    if v[0] == "-" and len(v) == 2:
        return "-" + valor(v[1])
    if v[0] == "/" and len(v) == 3:
        return valor(v[1]) + "/" + valor(v[2])
    raise NoSoportado("valor " + repr(v))


def modo_nativo(fichero):
    with open(fichero, encoding="utf-8", errors="replace") as f:
        texto = f.read()
    lineas, consts = traducir(texto)
    entrada = "\n".join(lineas) + "\n(check-sat)\n"
    if consts:
        entrada += "(get-value (%s))\n" % " ".join("|%s|" % c for c in consts)
    r = subprocess.run([Z3, "-in", "-smt2"], input=entrada, capture_output=True, text=True)
    salida = r.stdout.strip()
    primera, _, resto = salida.partition("\n")
    primera = primera.strip()
    if primera == "unsat":
        return "unsat\n"
    if primera != "sat":
        raise NoSoportado("z3 dijo: " + salida[:300])
    out = ["sat"]
    if consts:
        pares = arbol(tokens(resto))[0]
        for par in pares:
            nom = par[0]
            if nom.startswith("|") and nom.endswith("|"):
                nom = nom[1:-1]
            out.append("(= %s %s)" % (nom, valor(par[1])))
    return "\n".join(out) + "\n"


def modo_dimacs(fichero):
    import tempfile
    fd, res = tempfile.mkstemp(suffix=".res")
    os.close(fd)
    try:
        subprocess.run([MINISAT, "-verb=0", fichero, res], capture_output=True)
        with open(res) as f:
            partes = f.read().split()
    finally:
        os.remove(res)
    if not partes:
        raise NoSoportado("minisat sin resultado")
    if partes[0] == "UNSAT":
        return "unsat\n"
    if partes[0] != "SAT":
        raise NoSoportado("minisat dijo " + partes[0])
    lits = [x for x in partes[1:] if x != "0"]
    return "sat\n" + " ".join(lits) + "\n"


def main(argv):
    args = argv[1:]
    fichero = args[-1] if args else None
    try:
        if "-smt" in args:
            raise NoSoportado("modo -smt (SMT-LIB 1)")
        if fichero is None:
            raise NoSoportado("sin fichero")
        inicio = time.time()
        if "-d" in args:
            respuesta = modo_dimacs(fichero)
        else:
            respuesta = modo_nativo(fichero)
        sys.stdout.write(respuesta)
        apuntar("ok %s %.2fs %s" % (respuesta.split("\n", 1)[0], time.time() - inicio,
                                    "-d" if "-d" in args else "-e"))
    except NoSoportado as e:
        apuntar("unknown: %s | %s" % (e, " ".join(args)))
        sys.stdout.write("unknown\n")
    except Exception as e:  # nunca romper a AProVE
        apuntar("error: %r | %s" % (e, " ".join(args)))
        sys.stdout.write("unknown\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv)
