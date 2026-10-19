#!/usr/bin/env bash
# Para la tanda de YAH: lanzar.py corta la corrida en curso (que va en su
# propio grupo de procesos) al recibir TERM. Lo terminado queda en resultados/.
# La de AProVE tiene la misma línea de orden: se distingue por la carpeta.
aqui=$(cd "$(dirname "$0")" && pwd)
pid=""
for p in $(pgrep -u oem -f "python3 -I lanzar.py"); do
  if [ "$(readlink "/proc/$p/cwd")" = "$aqui" ]; then pid=$p; fi
done
if [ -z "$pid" ]; then
  echo "No hay ninguna tanda de YAH corriendo."
  exit 0
fi
echo "Paro la tanda de YAH (proceso $pid)."
kill -TERM "$pid"
sleep 5
if kill -0 "$pid" 2>/dev/null; then
  pkill -KILL -u oem -f "rewriting-collatz/prover/main.py"
  kill -KILL "$pid"
fi
echo "Parada."
