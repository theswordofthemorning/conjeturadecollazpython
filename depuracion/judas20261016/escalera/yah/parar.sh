#!/usr/bin/env bash
# Para la tanda de YAH: lanzar.py corta la corrida en curso (que va en su
# propio grupo de procesos) al recibir TERM. Lo terminado queda en resultados/.
# La de AProVE tiene la misma línea de orden: se distingue por la carpeta.
# Uso:  bash parar.sh                 (la del peldaño 5 o la calibración)
#       bash parar.sh --debilitadas   (la escalera de G debilitadas)
aqui=$(cd "$(dirname "$0")" && pwd)
pid=""
for p in $(pgrep -u oem -f "python3 -I lanzar.py"); do
  [ "$(readlink "/proc/$p/cwd")" = "$aqui" ] || continue
  if tr '\0' ' ' < "/proc/$p/cmdline" | grep -q -- "--debilitadas"; then
    [ "$1" = "--debilitadas" ] && pid=$p
  else
    [ "$1" = "--debilitadas" ] || pid=$p
  fi
done
if [ -z "$pid" ]; then
  echo "No hay ninguna tanda de YAH de ese tipo corriendo."
  exit 0
fi
echo "Paro la tanda de YAH (proceso $pid)."
kill -TERM "$pid"
sleep 5
if kill -0 "$pid" 2>/dev/null; then
  # cada corrida de YAH va en su propio grupo, colgando de lanzar.py
  for hijo in $(pgrep -P "$pid"); do pkill -KILL -g "$hijo" 2>/dev/null; done
  kill -KILL "$pid"
fi
echo "Parada."
