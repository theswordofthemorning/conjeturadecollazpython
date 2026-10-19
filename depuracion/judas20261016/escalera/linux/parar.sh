#!/usr/bin/env bash
# Para la tanda de AProVE, la lanzada con --fondo o la de una terminal:
# corta lanzar.py, el vigía, Java y los solucionadores, que comparten grupo
# de procesos. Lo ya terminado queda en resultados/.
pid=$(pgrep -o -u oem -f "python3 -I lanzar.py")
if [ -z "$pid" ]; then
  echo "No hay ninguna tanda corriendo."
  exit 0
fi
grupo=$(ps -o pgid= -p "$pid" | tr -d ' ')
echo "Paro la tanda (grupo de procesos $grupo)."
kill -TERM -- "-$grupo"
sleep 3
if pgrep -g "$grupo" > /dev/null; then
  kill -KILL -- "-$grupo"
fi
# El vigía cortado ya no borra su carpeta temporal: se borra aquí.
rm -rf /home/oem/herramientas/aprove/tmp/vigia_*
echo "Parada."
