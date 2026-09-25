# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Inicio de sesión

Las reglas vigentes están en [AGENTS.md](AGENTS.md).
El único contexto de investigación necesario al arrancar es
[ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md).
Si ya están en la sesión, continuar con la tarea sin volver a cargarlos.

Leer documentación adicional por necesidad concreta, usando el índice
[RutaTeoremas.md](RutaTeoremas.md). No leer el repositorio entero.

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

La versión extensa anterior se conserva literalmente en
[archivo/contexto_20260913/CLAUDE.md.txt](archivo/contexto_20260913/CLAUDE.md.txt).
Sus reglas antiguas y estados fechados son historia, no órdenes actuales.
