#!/usr/bin/env bash
# Lanza la tanda de AProVE (lanzar.py) sin que el equipo se suspenda mientras
# corre. La pantalla sí puede apagarse. Pasa los argumentos a lanzar.py.
# Uso:  bash lanzar.sh            (pruebas y tanda completa, unas 9 horas como mucho)
#       bash lanzar.sh --ensayo   (sólo calibra)
#       bash lanzar.sh --fondo    (lo mismo, pero sigue aunque se cierren la
#                                  terminal o Claude; se mira con
#                                  tail -f resultados/consola.txt y se para
#                                  con bash parar.sh)
# Si se abrió como root, corre como oem para que los resultados sean suyos.
cd "$(dirname "$0")" || exit 1
yo="$PWD/$(basename "$0")"
if [ "$(id -u)" = 0 ]; then
  exec sudo -u oem bash "$yo" "$@"
fi
if [ "$1" = "--fondo" ]; then
  shift
  res="${TANDA_RESULTADOS:-$PWD/resultados}"
  mkdir -p "$res"
  # Sesión propia (setsid) y sin terminal: no le llega el cierre de la ventana.
  setsid nohup bash "$yo" "$@" > "$res/consola.txt" 2>&1 < /dev/null &
  echo "La tanda corre en segundo plano."
  echo "  Verla:   tail -f $res/consola.txt"
  echo "  Pararla: bash $PWD/parar.sh"
  exit 0
fi
exec systemd-inhibit --what=sleep:handle-lid-switch --who=AProVE \
  --why="tanda del peldaño 5" python3 -I lanzar.py "$@"
