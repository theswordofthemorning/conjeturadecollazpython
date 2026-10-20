# Plan de YAH tras el diagnóstico — 19-10-2026

## Objetivo y decisión

El diagnóstico ya terminó: calibración 4/4 QED y G_B4 sin prueba, con
11 reglas residuales. G_B5…G_B7 no se ejecutaron. G y G_A2 también quedaron
con 11 reglas; las 22 configuraciones ensayadas de dimensión ≤ 3 dieron
UNSAT en cada residuo. Evidencia y alcance en [INFORME_YAH.md](INFORME_YAH.md).

La siguiente acción es auditar Nashida sobre los residuos exactos de G_A2
y G_B4 y después buscar una medida a mano para G_B4. El puente SRS ↔ función
sigue pendiente en Lean también para G: `piloto_iff` formaliza paridades ↔
no parada de G. La formalización de ese puente y el traductor de
certificados quedan detrás de las dos tareas anteriores; hoy el traductor
sólo serviría para los QED de calibración. Detalle en [PENDIENTES.md](PENDIENTES.md).

Una corrida larga sólo se justifica si la auditoría o el argumento a mano
señala una configuración concreta: fijar sistema, residuo, tipo, dimensión,
ancho, orientación, presupuesto y condición de parada. No repetir la
cascada ni ampliar k por los mismos resultados. El perfil y los comandos
de abajo se conservan como referencia de reproducción del diagnóstico.

Mapa y dominio: z entero positivo; G(z)=3z/2 si z es par,
G(z)=(9z+1)/8 si z=7 módulo 8, y parada en las otras clases.
G_Bk añade parada cuando z=-1 módulo 2^k, con k=4,5,6,7.
Un paso es una aplicación de G; no es un paso clásico de Collatz.
Los segundos de abajo son tiempo de pared del probador.

El perfil de diagnóstico ejecuta **una sola tanda**, con cuatro
solucionadores por forma, nice 10 y las protecciones de memoria existentes.
Un bloqueo `flock`
impide superponer lanzamientos mediante la versión nueva de `lanzar.sh`.
Procesos antiguos o lanzados por otras vías requieren comprobarse aparte.

## Perfil implementado: --diagnostico

1. Calibrar los peldaños 1, 2, 3 y 4. Si cualquiera no da QED, parar.
2. Probar G_B4; sólo si da QED, seguir con G_B5, luego G_B6 y G_B7.
3. Parar en el primer sistema sin prueba, error, falta de memoria o
   agotamiento del presupuesto. No subir automáticamente a la siguiente k.

Cada sistema usa las 36 formas existentes (natural, ártica y tropical,
ambas orientaciones), **una sola pasada de 30 s por forma**. Tras una
eliminación se reinicia la cascada sobre el sistema reducido. Los UNSAT
no se repiten sobre ese mismo sistema durante la tanda.
El presupuesto **global es 1800 s**, incluidos los reinicios y las esperas
de memoria; se ajusta el tiempo de cada hijo a lo que resta. La limpieza
de procesos puede añadir unos segundos. No se prometen todas las formas
ni todos los casos dentro de ese plazo.

El perfil no incluye G, G_A2 ni otras G_Ak: G_A2 ya ofrece un primer caso
resistente. Tampoco aumenta dimensiones ni relanza topes de 900/3600 s.
Un QED en un caso débil justifica explorar el siguiente; no demuestra una
cota uniforme al variar k ni Collatz.

## Nashida: qué comprobar antes de ampliar

La clasificación estructural y la búsqueda matricial son tareas distintas.
El clasificador puede orientar qué certificado buscar; una etiqueta de
enredo no descarta por sí sola toda configuración de este lanzador.
La auditoría debe comprobar lo siguiente antes de proponer otra corrida larga:

- Fijar commit y SHA-256 del
  [repositorio de la Parte I](https://github.com/harappa/collatz-termination-certificate-dichotomy).
  Leer el código; descargar juntos `computations/classify_families.py` y
  `computations/maps_G1.tsv`. `g1check` verifica sólo los 209 mapas de G_1.
- Construir nuestros nueve mapas directamente con `GMap`, sin enumerar
  familias mediante `list k`. Usar exponente de módulo max(3,k), comprobar
  positividad y cotejar ramas con `debilitar.py`; no importar este último
  sólo para obtener las funciones sin revisar primero sus efectos.
- Guardar componentes, ciclos y ramificación como testigos exactos.
  `INF` significa enredo; `escape` no prueba divergencia. La generación usa
  coma flotante; un certificado positivo requiere comprobación entera y,
  para nuestra certificación formal, su traducción a Lean.
- Para excluir una búsqueda YAH, identificar el teorema matricial, el
  sistema residual exacto, las reglas y la orientación a los que se aplica.
  Una equivalencia de terminación entre sistemas no basta para transportar
  una barrera de certificados. Conservar las hipótesis y el tramo pendiente.

El diagnóstico breve de G_B4 ya está registrado: no repetirlo para preparar
esta auditoría. Documentar el teorema aplicable y cada hipótesis satisfecha
o pendiente; una etiqueta del clasificador no basta. No se presenta la
Parte I como no existencia comprobada en Lean.
Los detalles del clasificador están en su
[código](https://github.com/harappa/collatz-termination-certificate-dichotomy/blob/master/computations/classify_families.py).

## Reproducción del perfil en el equipo Linux, como oem

Estos comandos documentan el perfil ejecutado; no son la siguiente acción
del plan. Desde la cuenta oem (si la sesión está abierta como root, pasar
primero a `sudo -iu oem`). No ejecutar aquí las corridas en Windows.

```bash
cd ~/Desktop/conjeturadecollazpython
git status -sb
git pull --ff-only
cd depuracion/judas20261016/escalera/yah
python3 -B -X utf8 comprobar_plan.py
bash -n lanzar.sh
pgrep -a -u oem -f 'lanzar.py|prover/main.py'
```

Si Git muestra resultados locales por conservar, guardarlos antes del pull;
no usar reset ni limpiar carpetas. `pgrep` sin coincidencias devuelve 1,
lo cual es normal. Si muestra una tanda anterior, identificarla y cerrarla
con su `parar.sh` antes de continuar. La nota remota registra que estaban
paradas; no sustituye esta comprobación de procesos actuales.

Revisar herramientas instaladas (no reinstalarlas por rutina):

```bash
git -C ~/herramientas/yah/rewriting-collatz rev-parse HEAD
git -C ~/herramientas/yah/rewriting-collatz diff -- prover/sat.py
~/herramientas/yah/rewriting-collatz/.venv/bin/python --version
command -v flock systemd-inhibit
```

La instalación anterior era YAH `8a4dfda`, con el arreglo
`random.randint(0, 10**9)` en `prover/sat.py`; los detalles están en
[LEEME.txt](LEEME.txt). Conservar la versión y cualquier diferencia junto
a los resultados. La calibración es obligatoria en este perfil.

Lanzar:

```bash
bash lanzar.sh --fondo --diagnostico
```

El comando imprime una ruta nueva bajo
`~/herramientas/yah/resultados/diagnostico-XXXXXXXX/` y la orden `tail -f`
para verla. Allí quedan `consola.txt`, `resumen.json`, registros y sistemas
residuales. `resumen.json` incluye SHA-256 de los ocho sistemas de entrada,
presupuesto, trabajadores y motivo de detención cuando procede.
No se sobrescriben las carpetas históricas del repo. Tampoco se reutiliza
una carpeta con resumen o resultados de un sistema.

Para parar esta tanda (el diagnóstico se distingue de `--debilitadas`):

```bash
bash parar.sh
```

Si se prefiere observar el arranque en primer plano, omitir `--fondo`.
No combinar `--diagnostico` con los perfiles antiguos.

## Lectura y siguiente decisión

- **QED:** preservar matrices, registros y toda la cadena de eliminaciones.
  Es una salida del probador, todavía pendiente de certificación externa o
  Lean. El puente SRS ↔ función sigue sin formalizar también para G; para
  las debilitadas sólo hay cotejo finito.
- **UNSAT:** sólo descarta esa interpretación, dimensión, ancho y
  orientación sobre ese sistema residual. No descarta terminación.
- **Tope / presupuesto / sin prueba:** cerrar el diagnóstico. Informar
  reglas eliminadas, sistema residual y formas probadas; no ampliar tiempo
  automáticamente. Error o falta de memoria son incidencias, no resultados
  matemáticos.

El diagnóstico se cerró en G_B4; seguir ahora la auditoría y el trabajo a
mano de [PENDIENTES.md](PENDIENTES.md). El resultado no equipara la
dificultad de los tres mapas ni excluye todas las interpretaciones
matriciales. Guardar sólo evidencia útil al repo, excluyendo `trabajo/` y
sus CNF.

## Validación del cambio

`comprobar_plan.py` verifica sin YAH: parada por calibración fallida y por
primer resistente, progresión sólo con QED, conservación de carpetas y
resúmenes, presupuesto y espera de memoria. La ejecución real de este
perfil quedó registrada en [resultados_diagnostico/](resultados_diagnostico/).
Esta revisión documental no relanza ese control ni ninguna tanda de YAH.
