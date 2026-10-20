#!/usr/bin/env bash
# Lanza la tanda de YAH (lanzar.py) sin que el equipo se suspenda mientras
# corre. La pantalla sí puede apagarse. Pasa los argumentos a lanzar.py.
# Uso:  bash lanzar.sh                    (calibración y peldaño 5)
#       bash lanzar.sh --ensayo           (sólo peldaño 1, 30 s por forma)
#       bash lanzar.sh --sin-calibracion  (sólo el peldaño 5)
#       bash lanzar.sh --debilitadas      (escalera de G debilitadas, en
#                                          resultados_debilitadas/)
#       bash lanzar.sh --fondo ...        (sigue aunque se cierren la terminal
#                                          o Claude; se mira con
#                                          tail -f resultados/consola.txt y se
#                                          para con bash parar.sh)
# Si se abrió como root, corre como oem para que los resultados sean suyos.
cd "$(dirname "$0")" || exit 1
yo="$PWD/$(basename "$0")"
if [ "$(id -u)" = 0 ]; then
  exec sudo -u oem --preserve-env=TANDA_RESULTADOS bash "$yo" "$@"
fi
# Un solo candado por usuario, se lance con sudo o desde el escritorio.
candado="/tmp/collatz-yah-$(id -u).lock"
if [ "$1" = "--fondo" ] && ! flock -n "$candado" true; then
  echo "Ya corre una tanda de YAH (candado $candado ocupado)." >&2
  exit 1
fi
# El perfil acotado guarda fuera del checkout y comparte la ruta con el hijo.
case " $* " in
  *" --diagnostico "*)
    if [ -z "${TANDA_RESULTADOS:-}" ]; then
      mkdir -p "$HOME/herramientas/yah/resultados" || exit 1
      TANDA_RESULTADOS=$(mktemp -d "$HOME/herramientas/yah/resultados/diagnostico-XXXXXXXX") || exit 1
      export TANDA_RESULTADOS
    fi
    ;;
esac
if [ "$1" = "--fondo" ]; then
  shift
  res="$PWD/resultados"
  case " $* " in *" --debilitadas "*) res="$PWD/resultados_debilitadas" ;; esac
  res="${TANDA_RESULTADOS:-$res}"
  if [ -e "$res/consola.txt" ] || [ -e "$res/resumen.json" ]; then
    echo "Se conservan los resultados de $res; usa una carpeta nueva." >&2
    exit 1
  fi
  mkdir -p "$res"
  setsid nohup bash "$yo" "$@" > "$res/consola.txt" 2>&1 < /dev/null &
  echo "La tanda corre en segundo plano."
  echo "  Verla:   tail -f $res/consola.txt"
  echo "  Pararla: bash $PWD/parar.sh"
  exit 0
fi
exec systemd-inhibit --what=sleep:handle-lid-switch --who=YAH \
  --why="tanda de YAH" flock -n "$candado" \
  python3 -I lanzar.py "$@"
