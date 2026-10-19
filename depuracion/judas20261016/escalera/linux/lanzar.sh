#!/usr/bin/env bash
# Lanza la tanda de AProVE (lanzar.py) sin que el equipo se suspenda mientras
# corre. La pantalla sí puede apagarse. Pasa los argumentos a lanzar.py.
# Uso:  bash lanzar.sh            (pruebas y tanda completa, unas 8 horas)
#       bash lanzar.sh --ensayo   (sólo calibra)
# Si se abrió como root, corre como oem para que los resultados sean suyos.
cd "$(dirname "$0")" || exit 1
if [ "$(id -u)" = 0 ]; then
  exec sudo -u oem bash "$0" "$@"
fi
exec systemd-inhibit --what=sleep:handle-lid-switch --who=AProVE \
  --why="tanda del peldaño 5" python3 -I lanzar.py "$@"
