# guardarrespuestas.py
#
# EL CUADERNO DE LAS CONVERSACIONES, SACADO DE LAS TRANSCRIPCIONES DE VERDAD.
#
# Que problema resuelve. Las respuestas de Claude en consola traen observaciones,
# correcciones y lineamientos que se daban por perdidos al cerrar la sesion.
# El CLAUDE.md no puede absorberlos porque creceria sin control.
#
# NO ESTABAN PERDIDOS. Claude Code guarda la transcripcion entera de cada sesion
# en JSONL, con marca de tiempo exacta, en
#
#     ~/.claude/projects/<slug-del-proyecto>/*.jsonl
#
# donde el slug de este repo es C--Users-Home-Desktop-conjeturadecollazpython.
# Ahi esta todo: cada pregunta del usuario y cada respuesta del asistente,
# literales. Este programa las lee y las mete en sqlite para poder consultarlas.
#
# ---------------------------------------------------------------------------
# POR QUE NO SE PUDO HACER DE OTRA FORMA
# ---------------------------------------------------------------------------
#
# El texto del asistente NO pasa por stdout: no hay ningun proceso escribiendo a
# una consola que se pueda redirigir. Claude Code lo renderiza directo. Lo unico
# que existe como fichero es esta transcripcion, y por eso es la fuente.
#
# Una version anterior de este fichero reconstruia las respuestas de memoria.
# Estaba mal: existiendo lo literal, reconstruir es meter una copia peor en un
# sitio que parece un registro. La columna `origen` se queda igualmente, porque
# distingue dos cosas que no valen lo mismo:
#
#   'capturado'    salio de la transcripcion, literal, con hora exacta
#   'reconstruido' lo escribio alguien despues, de memoria
#
# ---------------------------------------------------------------------------
# ESTE FICHERO ROMPE UNA REGLA DEL REPO, Y ES A PROPOSITO
# ---------------------------------------------------------------------------
#
# guardarmallas.py y guardarhilos.py REGENERAN su base entera cada vez (el
# segundo hace os.remove del fichero). Aqui NO: respuestas.db es APPEND-ONLY.
# Un registro historico no se regenera. Si algun dia se borran las
# transcripciones viejas, esta base sera el unico sitio donde queden.
#
# Es idempotente por (sesion, orden): se puede correr mil veces sin duplicar.
#
# ---------------------------------------------------------------------------
# LAS COLUMNAS DE ANALISIS VAN VACIAS, Y ESTA BIEN
# ---------------------------------------------------------------------------
#
# resumen, tipo, hallazgos, decisiones y ficheros quedan NULL al capturar. No se
# rellenan automaticamente porque eso seria inventar. Se llenan despues, a mano
# o por un modelo que lea la fila y la clasifique. Asi el registro crudo y la
# interpretacion no se mezclan, que es la misma disciplina que el resto del repo.

import glob
import json
import os
import sqlite3

# ---------------------------------------------------------------------------
# Cambia esto aqui, guarda, y dale a Ctrl+B en Sublime.
# ---------------------------------------------------------------------------

ARCHIVO = "respuestas.db"

# El SLUG se DEDUCE del directorio en que estas, no se escribe a mano. Claude
# Code nombra la carpeta de transcripciones con la ruta del proyecto y le cambia
# cada separador por un guion: C:\Users\Pepe\Desktop\x -> C--Users-Pepe-Desktop-x
#
# Estuvo a fuego como "C--Users-Home-Desktop-conjeturadecollazpython" y por eso
# el programa no arrancaba en una maquina cuyo usuario no fuera "Home": el 01-08
# se descubrio que la regla del registro llevaba una sesion entera sin poder
# cumplirse. Si lo vuelves a fijar a mano, se rompe en la siguiente maquina.
SLUG = os.path.abspath(os.getcwd()).replace(":", "-").replace("\\", "-").replace("/", "-")
CARPETA = os.path.join(os.path.expanduser("~"), ".claude", "projects", SLUG)

# Salida de emergencia: si Claude Code cambia como arma el nombre, se busca la
# carpeta que termine igual que este proyecto en vez de rendirse.
if not os.path.isdir(CARPETA):
    raiz = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    fin = "-" + os.path.basename(os.getcwd())
    if os.path.isdir(raiz):
        cand = [d for d in os.listdir(raiz) if d.endswith(fin)]
        if len(cand) == 1:
            CARPETA = os.path.join(raiz, cand[0])
            SLUG = cand[0]

ROLES = ("usuario", "asistente", "sistema")
ORIGENES = ("capturado", "reconstruido")
TIPOS = (None, "observacion", "correccion", "lineamiento", "resultado",
         "decision", "conversacion")


# ---------------------------------------------------------------------------
# Leer las transcripciones
# ---------------------------------------------------------------------------

def texto_de(contenido):
    """Saca el texto de un contenido, que puede ser cadena o lista de bloques.

    Los bloques que no son texto (llamadas a herramienta, resultados) se
    ignoran: aqui interesa la conversacion, no la maquinaria.
    """
    if isinstance(contenido, str):
        return contenido
    if isinstance(contenido, list):
        trozos = []
        for bloque in contenido:
            if isinstance(bloque, dict) and bloque.get("type") == "text":
                trozos.append(bloque.get("text", ""))
        return "\n".join(trozos)
    return ""


def es_notificacion(texto):
    """Las notificaciones de tareas de fondo llegan como si fueran del usuario.

    No son mensajes de una persona y no hay que contarlas como tales.
    """
    cabeza = texto.lstrip()[:200]
    return ("[SYSTEM NOTIFICATION" in cabeza
            or "<task-notification>" in cabeza
            or "<command-name>" in cabeza)


def leer_transcripcion(ruta):
    """Devuelve la lista de mensajes de una sesion, en orden."""
    mensajes = []
    orden = 0
    for linea in open(ruta, encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        try:
            objeto = json.loads(linea)
        except json.JSONDecodeError:
            continue

        # los mensajes de los subagentes van marcados y no son la conversacion
        if objeto.get("isSidechain"):
            continue

        clase = objeto.get("type")
        if clase not in ("user", "assistant"):
            continue

        mensaje = objeto.get("message") or {}
        texto = texto_de(mensaje.get("content"))
        if not texto.strip():
            continue

        if clase == "user":
            rol = "sistema" if es_notificacion(texto) else "usuario"
        else:
            rol = "asistente"

        orden += 1
        mensajes.append(dict(
            orden=orden,
            fecha_hora=objeto.get("timestamp") or "",
            rol=rol,
            modelo=mensaje.get("model"),
            texto=texto,
        ))
    return mensajes


# ---------------------------------------------------------------------------
# La base
# ---------------------------------------------------------------------------

def abrir(archivo=ARCHIVO):
    """Abre la base y crea la tabla si no existe. NUNCA borra nada."""
    conexion = sqlite3.connect(archivo)
    conexion.executescript("""
    CREATE TABLE IF NOT EXISTS respuestasclaude (
        id          INTEGER PRIMARY KEY,
        sesion      TEXT    NOT NULL,
        orden       INTEGER NOT NULL,
        fecha_hora  TEXT    NOT NULL,
        rol         TEXT    NOT NULL,
        modelo      TEXT,
        texto       TEXT    NOT NULL,
        largo       INTEGER NOT NULL,
        origen      TEXT    NOT NULL,
        tipo        TEXT,
        resumen     TEXT,
        hallazgos   TEXT,
        decisiones  TEXT,
        ficheros    TEXT,
        UNIQUE (sesion, orden)
    );
    CREATE INDEX IF NOT EXISTS idx_resp_sesion ON respuestasclaude (sesion, orden);
    CREATE INDEX IF NOT EXISTS idx_resp_rol    ON respuestasclaude (rol);
    CREATE INDEX IF NOT EXISTS idx_resp_fecha  ON respuestasclaude (fecha_hora);
    CREATE INDEX IF NOT EXISTS idx_resp_tipo   ON respuestasclaude (tipo);
    """)
    return conexion


def anotar(conexion, sesion, mensaje, origen="capturado"):
    """Mete un mensaje. Si ya existe ese (sesion, orden), lo deja como estaba."""
    if mensaje["rol"] not in ROLES:
        raise SystemExit(f"rol desconocido: {mensaje['rol']}")
    if origen not in ORIGENES:
        raise SystemExit(f"origen desconocido: {origen}")
    conexion.execute(
        "INSERT OR IGNORE INTO respuestasclaude"
        " (sesion, orden, fecha_hora, rol, modelo, texto, largo, origen)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (sesion, mensaje["orden"], mensaje["fecha_hora"], mensaje["rol"],
         mensaje.get("modelo"), mensaje["texto"], len(mensaje["texto"]), origen))


# ---------------------------------------------------------------------------
# A trabajar
# ---------------------------------------------------------------------------

print("EL CUADERNO DE LAS CONVERSACIONES\n")

if not os.path.isdir(CARPETA):
    raise SystemExit(
        f"No existe la carpeta de transcripciones:\n  {CARPETA}\n"
        "Si Claude Code guarda las sesiones en otro sitio, cambia SLUG o CARPETA.")

rutas = sorted(glob.glob(os.path.join(CARPETA, "*.jsonl")))
if not rutas:
    raise SystemExit(f"No hay ningun .jsonl en {CARPETA}. Nada que capturar.")

print(f"  transcripciones encontradas: {len(rutas)}")
for ruta in rutas:
    print(f"    {os.path.basename(ruta)}   {os.path.getsize(ruta) / 1024:,.0f} KB")

existia = os.path.exists(ARCHIVO)
conexion = abrir()
antes = conexion.execute("SELECT COUNT(*) FROM respuestasclaude").fetchone()[0]

leidos = 0
for ruta in rutas:
    sesion = os.path.splitext(os.path.basename(ruta))[0]
    mensajes = leer_transcripcion(ruta)
    leidos += len(mensajes)
    for mensaje in mensajes:
        anotar(conexion, sesion, mensaje)
conexion.commit()

despues = conexion.execute("SELECT COUNT(*) FROM respuestasclaude").fetchone()[0]
print(f"\n  base: {ARCHIVO}   {'(ya existia)' if existia else '(creada ahora)'}")
print(f"  mensajes leidos de las transcripciones: {leidos:,}")
print(f"  entradas antes {antes:,}  ->  ahora {despues:,}   (nuevas: {despues - antes:,})")


# ------------------------------------- COMPROBACION 1: vocabulario cerrado

malos = conexion.execute(
    "SELECT COUNT(*) FROM respuestasclaude"
    " WHERE rol NOT IN ('usuario','asistente','sistema')").fetchone()[0]
malos += conexion.execute(
    "SELECT COUNT(*) FROM respuestasclaude"
    " WHERE origen NOT IN ('capturado','reconstruido')").fetchone()[0]
print(f"\nCOMPROBACION 1 -- vocabulario cerrado: {malos} filas fuera de rango")
if malos:
    raise SystemExit("Hay roles u origenes fuera del vocabulario. No sigas.")


# ------------------------------------- COMPROBACION 2: nada vacio ni duplicado

vacias = conexion.execute(
    "SELECT COUNT(*) FROM respuestasclaude"
    " WHERE texto IS NULL OR TRIM(texto) = ''").fetchone()[0]
duplicados = conexion.execute(
    "SELECT COUNT(*) FROM (SELECT sesion, orden FROM respuestasclaude"
    " GROUP BY 1,2 HAVING COUNT(*) > 1)").fetchone()[0]
sin_fecha = conexion.execute(
    "SELECT COUNT(*) FROM respuestasclaude WHERE fecha_hora = ''").fetchone()[0]
print(f"COMPROBACION 2 -- vacias {vacias} · (sesion,orden) repetidos {duplicados}"
      f" · sin fecha {sin_fecha}")
if vacias or duplicados:
    raise SystemExit("Hay filas vacias o duplicadas. No sigas.")


# ------------------------------------- COMPROBACION 3: ida y vuelta literal
#
# Se relee una muestra del disco y se compara caracter a caracter contra la
# transcripcion original. Si el texto no sale identico, la captura no sirve.

fallos = 0
comprobados = 0
for ruta in rutas:
    sesion = os.path.splitext(os.path.basename(ruta))[0]
    for mensaje in leer_transcripcion(ruta):
        fila = conexion.execute(
            "SELECT texto, rol, largo FROM respuestasclaude WHERE sesion=? AND orden=?",
            (sesion, mensaje["orden"])).fetchone()
        comprobados += 1
        if (fila is None or fila[0] != mensaje["texto"]
                or fila[1] != mensaje["rol"] or fila[2] != len(mensaje["texto"])):
            fallos += 1
print(f"COMPROBACION 3 -- ida y vuelta literal: {comprobados:,} mensajes, {fallos} fallos")
if fallos:
    raise SystemExit("Lo guardado no es identico a la transcripcion. No sirve.")


# ------------------------------------------------------------- el informe

print("\nQUE HAY GUARDADO\n")
print(f"  {'sesion':<10} {'de':<20} {'a':<20} {'usuario':>8} {'asistente':>10}"
      f" {'sistema':>8} {'caracteres':>12}")
print(f"  {'-'*10} {'-'*20} {'-'*20} {'-'*8} {'-'*10} {'-'*8} {'-'*12}")
for sesion, desde, hasta, u, a, s, chars in conexion.execute("""
        SELECT sesion, MIN(fecha_hora), MAX(fecha_hora),
               SUM(rol='usuario'), SUM(rol='asistente'), SUM(rol='sistema'),
               SUM(largo)
        FROM respuestasclaude GROUP BY sesion ORDER BY MIN(fecha_hora)"""):
    print(f"  {sesion[:8]:<10} {desde[:19]:<20} {hasta[:19]:<20}"
          f" {u:>8} {a:>10} {s:>8} {chars:>12,}")

total_u, total_a, total_c = conexion.execute(
    "SELECT SUM(rol='usuario'), SUM(rol='asistente'), SUM(largo)"
    " FROM respuestasclaude").fetchone()
print(f"\n  TOTAL: {total_u} preguntas · {total_a} respuestas · "
      f"{total_c:,} caracteres")

print(f"\n  Las diez respuestas mas largas (suelen ser las que traen el analisis):")
for sesion, orden, fecha, largo in conexion.execute(
        "SELECT sesion, orden, fecha_hora, largo FROM respuestasclaude"
        " WHERE rol='asistente' ORDER BY largo DESC LIMIT 10"):
    print(f"    {sesion[:8]} turno {orden:>4}  {fecha[:19]}  {largo:>7,} caracteres")

pendientes = conexion.execute(
    "SELECT COUNT(*) FROM respuestasclaude WHERE rol='asistente' AND tipo IS NULL"
).fetchone()[0]
print(f"\n  Respuestas sin clasificar (tipo IS NULL): {pendientes}")
print(f"  Las columnas tipo, resumen, hallazgos, decisiones y ficheros se llenan")
print(f"  DESPUES, leyendo la fila. No se rellenan solas: eso seria inventar.")

conexion.close()
print(f"\nLa base esta en {ARCHIVO}. Es APPEND-ONLY: correr esto otra vez no")
print(f"duplica ni borra nada, solo añade las sesiones nuevas que aparezcan.")
