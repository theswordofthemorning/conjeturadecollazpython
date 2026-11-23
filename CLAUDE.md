# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Inicio de sesión

Las reglas vigentes están en [AGENTS.md](AGENTS.md).
El único contexto de investigación necesario al arrancar es
[ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md).
Si ya están en la sesión, continuar con la tarea sin volver a cargarlos.

Leer documentación adicional por necesidad concreta, usando el índice
[RutaTeoremas.md](RutaTeoremas.md). No leer el repositorio entero.

## Encargo vigente

Ninguno. El encargo anterior, cerrar la barrera Lean de tres cargas de
Perdices, quedó cumplido el 16-10 (commit `6b01e8b`). Las constantes con F
invertible se integraron en el registro el 22-11. La siguiente acción, si
el usuario retoma Perdices, está en `ESTADO_INVESTIGACION.md`. No abras una
ruta nueva ni hagas commit o push sin instrucción del usuario.

## Comandos

No hay build, linter ni CI centralizados. Los `.lean` de la raíz se
comprueban sueltos; la formalización de Gao es un proyecto Lake (Lean 4.32.2,
Mathlib fijada) en `depuracion/gao20260920/formal/`, con `.lake/` fuera de Git.

```
pip install -r requirements.txt
python -B -X utf8 main.py verificar --limite 1000000     # también: records, camino 27
python -B -X utf8 depuracion/coherencia20260913/ejecutar_controles.py
lean cabras.lean                                         # un fichero Lean suelto
python -B -X utf8 depuracion/frente20260910/rachas.py    # un solo verificador

# desde depuracion/gao20260920/formal/ (primera vez: lake exe cache get ..., ver README)
lake build GaoCore GaoFormal
lake env lean Momentos.lean                              # un solo módulo
```

`ejecutar_controles.py` necesita `../zootheorem/` y Lean en el `PATH`;
escribe `controles.json` y `*_salida.txt` en su carpeta, y un fallo por
tiempo (120 s) o por `sorry` cuenta como FALLO, nunca como teorema.
`afirmaciones.db` se regenera con `guardarafirmaciones.py`, que aplica el
registro versionado `depuracion/coherencia20260913/registro.json` vía
`registroafirmaciones.py`; las correcciones van al registro, no a la base.

En la copia Linux (`/home/oem/Desktop/conjeturadecollazpython`), Lean se
instaló con elan en `~/.elan`, sin tocar el `PATH`: antes de `lake`, ejecutar
`export PATH=$HOME/.elan/bin:$PATH`. La caché de Mathlib ya está en el
`.lake/` de Gao. `../zootheorem` está clonado en `~/Desktop/zootheorem`.
`respuestas.db` no existe en esta copia; `verificar_alta.py` lo tolera.

La versión extensa anterior se conserva literalmente en
[archivo/contexto_20260913/CLAUDE.md.txt](archivo/contexto_20260913/CLAUDE.md.txt).
Sus reglas antiguas y estados fechados son historia, no órdenes actuales.
