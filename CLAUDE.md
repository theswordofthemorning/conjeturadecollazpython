# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Inicio de sesión

Las reglas vigentes están en [AGENTS.md](AGENTS.md).
El único contexto de investigación necesario al arrancar es
[ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md).
Si ya están en la sesión, continuar con la tarea sin volver a cargarlos.

Leer documentación adicional por necesidad concreta, usando el índice
[RutaTeoremas.md](RutaTeoremas.md). No leer el repositorio entero.

## Encargo vigente para Claude: cerrar la barrera Lean de Perdices

El usuario prioriza Perdices. Trabaja en la rama actual; no crees otra rama ni
un worktree. El punto de partida conservado es el commit `08a5a22`.
Este encargo termina al certificar la barrera de tres cargas o al identificar
un obstáculo reproducible. No continúes J2/J3 de `RutaDeJudasIscariote.md`,
ni abras otra ruta del piloto durante esta tanda.

Lee sólo [BARRERA.md](depuracion/perdices20261007/congruencias_codex20261016/BARRERA.md)
y los archivos que necesites para estas tareas:

1. **Diagnóstico.** Comprueba `lean --version`, inspecciona los parámetros de
   `comprobar_barrera.py` y localiza el primer error concreto de compilación
   de `PerdicesBarreraTablas.lean` o `PerdicesBarreraTres.lean`. La compilación
   completa anterior consumió demasiada memoria. Prueba piezas pequeñas y
   un proceso Lean a la vez; no repitas la ejecución monolítica sin corregir
   antes su causa.
2. **Corrección.** Repara la formalización del enunciado de BARRERA §1:
   en cada tres cargas consecutivas alguna es al menos 17. Conserva el
   dominio, las hipótesis y el significado de los teoremas. Puedes dividir
   las tablas o pruebas en módulos Lean pequeños. No uses `sorry`, `admit`,
   `axiom` ni `native_decide`. Si hallas un contraejemplo o una brecha en la
   prueba escrita, detén la formalización y comunica el caso exacto.
3. **Cierre verificable.** Ejecuta `comprobar_barrera.py` completo sólo cuando
   las piezas compilen. Exige salida exitosa, `#print axioms` sin `sorryAx`
   y sólo los axiomas estándar admitidos por el verificador. Contrasta el
   enunciado con `certificado_barrera.json` y `cotejo_barrera.json`; no repitas
   censos grandes. Genera `evidencia_barrera.json` y `.txt` sólo tras éxito
   completo. Si no se cierra, informa el comando, error exacto, módulo
   alcanzado y siguiente obligación; no declares certificada la barrera.

Durante este encargo puedes editar los archivos `PerdicesBarrera*.lean`,
crear módulos `.lean` auxiliares en esa misma carpeta y ajustar
`comprobar_barrera.py`. Si la división mecánica de tablas lo exige, puedes
ajustar `certificar_barrera.py`, conservando el contenido matemático del
certificado y comprobando su igualdad después de regenerarlo. No edites
ningún `.md`, los registros, las bases de datos, la evidencia Lean previa ni
archivos de otras ramas de investigación. Si esa restricción impide terminar,
explica el cambio necesario en tu informe. No hagas commit ni push de esta
investigación sin una nueva instrucción del usuario.

Entrega final breve: resultado matemático exacto, archivos cambiados,
comandos y resultados de verificación, y pendientes reales. No cambies de
objetivo cuando aparezca una dificultad técnica.

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
