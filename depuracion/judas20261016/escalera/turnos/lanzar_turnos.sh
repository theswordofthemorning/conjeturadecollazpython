#!/usr/bin/env bash
# Portafolio por turnos sobre el peldaño 5 (LEEME de la escalera, §6).
# Uso, desde Git Bash:  bash lanzar_turnos.sh validar   (unos minutos)
#                       bash lanzar_turnos.sh largo     (unas 5 horas)
# Cada corrida pasa por el vigía. La cadena se detiene ante un YES o un NO
# del piloto, como pide §11 de la ruta: el YES se certifica y el NO se
# comprueba a mano antes de seguir.
set -u
AQUI=/c/Users/Home/Desktop/conjeturadecollazpython/depuracion/judas20261016/escalera/turnos
HERR=/c/Users/Home/herramientas
JAVA="C:/Program Files/Java/jdk-27/bin/java.exe"
CP="C:/Users/Home/herramientas/aprove/aprove_parche_stop.jar;C:/Users/Home/Desktop/conjeturadecollazpython/depuracion/judas20261016/escalera/turnos/estrategia"
export PATH="$HERR/bin:$HERR/z3/z3-5.3.1-x64-win/bin:$PATH"
export MSYS2_ARG_CONV_EXCL='*'
cd "$AQUI" || exit 1

# Seis núcleos físicos, uno por núcleo; los hermanos quedan para Windows.
NUCLEOS=0,2,4,6,8,10
# Topes del vigía para un equipo que no hace otra cosa (por omisión: 1,5, 3, 2 y 1,5).
MEMORIA="--tope-hijo-gb 3 --aviso-gb 1.8 --libre-min-gb 1.2 --compromiso-min-gb 1.2"

# correr NOMBRE ESTRATEGIA SEGUNDOS HEAP ENTRADA
correr() {
  local n=$1 s=$2 t=$3 x=$4 e=$5
  python -I "C:/Users/Home/herramientas/bin/vigia.py" --salida "$n.salida.txt" --errores "$n.errores.txt" \
    --registro "$n.vigia.txt" --nucleos "$NUCLEOS" --tiempo-max $((t + 240)) \
    --tmp "C:/Users/Home/herramientas/aprove/tmp" $MEMORIA -- \
    "$JAVA" -ea "-Xmx$x" -XX:ActiveProcessorCount=6 "-Xlog:gc:file=$n.gc.txt" -cp "$CP" \
    aprove.Main -m wst -p plain -t "$t" -s "aprove.Turnos.$s" "$e"
  veredicto=$(head -1 "$n.salida.txt" | tr -d '\r')
  echo "$(date '+%d-%m %H:%M:%S') $n: ${veredicto:-sin salida}" | tee -a cadena.txt
}

case "${1:-}" in
  validar)
    correr prueba_derecho_peldano3 derecho 120 2g ../peldano3_ramaA.srs
    correr prueba_derecho_peldano4 derecho 120 2g ../peldano4_ramaB.srs
    correr prueba_reves_peldano3 reves 120 2g ../peldano3_ramaA.srs
    correr prueba_reves_peldano4 reves 120 2g ../peldano4_ramaB.srs
    correr prueba_lazos_bucle lazos 60 2g bucle.srs
    ;;
  largo)
    # Heap por turno: los solucionadores de los turnos de terminación necesitan
    # unos 3-4 GB propios; la búsqueda de lazos corre dentro de Java.
    for turno in derecho:8100:5g reves:8100:5g lazos:1800:8g; do
      IFS=: read -r s t x <<< "$turno"
      correr "$s" "$s" "$t" "$x" ../peldano5_completo.srs
      case "$veredicto" in
        YES|NO) echo "$(date '+%d-%m %H:%M:%S') cadena detenida por $veredicto" | tee -a cadena.txt
                exit 0 ;;
      esac
    done
    ;;
  *) echo "uso: bash lanzar_turnos.sh validar|largo"; exit 2 ;;
esac
