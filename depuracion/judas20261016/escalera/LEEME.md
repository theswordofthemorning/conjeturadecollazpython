# Escalera de AProVE sobre el piloto, 17-10-2026

Corre la escalera de [§11 de la ruta](../../../RutaDeJudasIscariote.md#11-siguiente-paso-aprove)
en el equipo del usuario. **Los peldaños 1 a 4 dan YES. El 5, el piloto,
queda sin respuesta (KILLED) a 300 s y a 3600 s, y da MAYBE con dos
estrategias acotadas (§5).** No hubo ningún NO. El portafolio completo, rama
por rama, sigue en curso (§6).

## 1. Resultado

| Peldaño | Sistema | Resultado |
| --- | --- | --- |
| 1 | sólo las reglas X ([srs](peldano1_X.srs)) | YES |
| 2 | sin L ([srs](peldano2_sinL.srs)) | YES |
| 3 | rama A ([srs](peldano3_ramaA.srs)) | YES |
| 4 | rama B ([srs](peldano4_ramaB.srs)) | YES, 7,4 s con vigía |
| 5 | completo ([srs](peldano5_completo.srs)) | KILLED a 300 s y a 3600 s; MAYBE con las dos estrategias de §5 |

- `peldano5_completo.srs` es [piloto_yah.srs](../piloto_yah.srs) con comas
  entre las reglas, como en el formato SRS que lee AProVE.
- Los YES de 1 a 4 son de calibración: ya se sabía que esos sistemas terminan.
  Dicen que la instalación funciona. No se certificaron porque nada se afirma
  con ellos.
- Por la regla de §11, el KILLED y el MAYBE del peldaño 5 confirman la
  salida (b) con el presupuesto de abajo. No son una prueba ni un
  contraejemplo.

**Presupuesto.**
- Equipo: Windows 11, AMD Ryzen 5 1600 y 16 GB de RAM.
- Para AProVE: 4 núcleos (`-XX:ActiveProcessorCount=4`, afinidad 0,2,4,6),
  prioridad baja y un heap de 5 GB (`-Xmx5g`).
- Herramientas: JDK 27 con el parche de §2, Z3 5.3.1, MiniSat 2 compilado aquí
  y Yices 1 imitado por el adaptador de §2.

La medida limpia es la de 300 s: pico de Java 5,41 GB, ningún error de memoria
y ningún corte del vigía. Aun así, Java llenó su heap de 5 GB en los primeros
22 s. Ver su [vigía](vigilado/peldano5_completo.vigia.txt) y su
[salida](vigilado/peldano5_completo.salida.txt).

## 2. Lo que hubo que adaptar en Windows

AProVE está hecho para Java 25, y sus autores lo usan en Linux. Aquí hicieron
falta tres arreglos, instalados fuera del repo, en `C:\Users\Home\herramientas`.
Los guiones están copiados en [windows/](windows/).

- **Java.** Se usó el JDK 27 del equipo.
  - El jar publicado (TC-2026) trae 1753 clases compiladas para Java 26, entre
    ellas `aprove/cli/Main`. Con Java 25 no arranca.
  - AProVE corta las técnicas lentas con `Thread.stop()`, que desde Java 26 ya
    no existe. Las corridas sin parche fallaban con `NoSuchMethodError`.
  - Su código atrapa `UnsupportedOperationException`, que es lo que lanza ese
    método en Java 20 a 25, y entonces interrumpe el hilo.
  - El parche recompila tres clases del código de AProVE (commit `ae097c6`),
    entre ellas `TrackThreadCustom`, para que atrapen también
    `NoSuchMethodError`. Está en `aprove_parche_stop.jar`; el resto del jar
    es idéntico.
- **Yices 1.** AProVE no funciona con Yices 2, y Yices 1 no se instaló aquí:
  su descarga de SRI dio 403.
  - [yices_shim.py](windows/yices_shim.py) imita su interfaz: pasa el lenguaje
    nativo a Z3 y el DIMACS a MiniSat.
  - Ante lo que no sabe traducir responde `unknown`, y eso nunca deja concluir
    nada falso.
  - [yices_lanzador.c](windows/yices_lanzador.c) es el `yices.exe` que lo llama.
  - Su [registro](windows/yices_shim.log), en todas las corridas que lo usaron:
    59 respuestas (43 sat y 16 unsat), un error por un temporal ya borrado y
    ningún `unknown`.
- **Memoria.** [vigia.py](windows/vigia.py) corre la orden con prioridad baja.
  - Si un solucionador pasa de 1,5 GB, lo corta.
  - Si la RAM libre baja de 3 GB, corta el solucionador mayor. Desde §6
    también lo corta si baja el compromiso libre (RAM más archivo de
    paginación).
  - Si baja de 2 GB, corta todo.

  Cortar un solucionador sólo hace fallar la técnica que lo usaba. Al
  terminar, corta los solucionadores que su corrida dejó vivos, y sólo ésos
  desde la corrección de §5.

## 3. La corrida de una hora

Archivos `peldano5_completo_3600s.*` en [vigilado/](vigilado/): vigía, GC,
errores y salida.

- **Terminó sola** a los 3604,5 s, con KILLED. Java llegó a 5,55 GB, y hubo
  hasta 24 solucionadores a la vez, con 2,31 GB entre todos.
- **Se quedó sin memoria.**
  - Hubo 67 recolecciones completas sobre el heap de 5 GB. El registro de GC
    termina a los 1328 s.
  - Hubo 21 `OutOfMemoryError`, que mataron técnicas.
  - El vigía cortó tres MiniSat (a los 1289, 1384 y 1388 s) con la RAM libre
    bajo 3 GB, mientras Claude usaba Chrome en el mismo equipo.
  - Desde los 1330 s, Java sólo esperó a seis MiniSat.
- **Sin avance.** Abrió los mismos 49 subproblemas que la de 300 s (líneas
  `(P,Q,R)-chains`). Cerró 3 subpruebas con YES, contra 4 (cada una sale dos
  veces en la salida).
- **Lección.** En este equipo más tiempo no ayuda: el límite es la memoria.

## 4. Pendiente: el peldaño 5 en una máquina Linux

Esto es lo que falta: correrlo en una máquina con más memoria.

**Qué cambia en Linux.**
- Java sigue, porque AProVE es un programa Java.
- La imagen Docker de AProVE trae su propio jar, Java 25, Yices 1 y MiniSat.
  Con ella no hacen falta el parche ni el adaptador.
- Con 32 GB o más, el heap puede ser de 16 GB o más: el triple de aquí, o más.

**Opción A: la imagen Docker.** La página de descarga de AProVE enlaza
`jckassing/aprove`, que según ella trae AProVE con todas sus herramientas
externas.
- La versión del 23-09-2026 trae Ubuntu 24.04, OpenJDK 25 y
  `/opt/bundle/aprove.jar`.
- Su orden por defecto es su envoltorio `solver`. Para pasar nuestras opciones
  se cambia por `java`.

Esta orden, lanzada desde la carpeta de los `.srs`, no se ha probado aquí:

```sh
docker pull jckassing/aprove
docker run --rm -v "$PWD":/input --entrypoint java jckassing/aprove \
  -ea -Xmx16g -jar /opt/bundle/aprove.jar -m wst -p plain -t 60 peldano1_X.srs
```

**Opción B: instalación directa**, según la página de descarga, con dos
trampas que se vieron aquí:
- El jar de las [versiones publicadas](https://github.com/aprove-developers/aprove-open-source/releases)
  (TC-2026) no arranca con Java 25, y con Java 26 o más necesita el parche. Lo
  más simple es llevar `aprove_parche_stop.jar` desde
  `C:\Users\Home\herramientas\aprove\` y usar un JDK 26 o 27.
- La descarga de Yices 1 (la 1.0.40, primera en el `PATH`) dio 403 en SRI el
  17-10. Sin Yices 1, conviene la opción A.
- Lo demás: Z3 4.4.0 o más, con `libz3java.so` en `LD_LIBRARY_PATH`, y
  MiniSat 2, el paquete `minisat2` en Debian y Ubuntu.

**Pasos.**
1. Anotar la máquina: `uname -a`, `nproc`, `free -g` y `java -version`, o la
   fecha de la imagen.
2. Probar la instalación con el peldaño 1 a 60 s. Debe dar YES.
3. Correr el peldaño 5 con un heap de a lo sumo la mitad de la RAM, dejando
   3 GB libres o más para los solucionadores.
   - Primero a 300 s, para comparar con la de aquí.
   - Después a 3600 s o más.

   Por ejemplo, con 32 GB:

   ```sh
   java -ea -Xmx16g -Xlog:gc:file=gc.txt -jar aprove.jar -m wst -p plain \
     -t 3600 peldano5_completo.srs > salida.txt 2> errores.txt
   ```
4. Traer `salida.txt`, `errores.txt`, `gc.txt` y los datos de la máquina a
   `escalera/linux/`.
5. Correr también las estrategias de §5 con el heap mayor. En Linux el
   classpath se separa con `:` y no con `;`.

**Cómo leer el resultado**, con las reglas de §11:
- **YES:** todavía no es una prueba. Se repite con `-C ceta -p cpf`, y el
  certificado se comprueba con CeTA, o se traslada a Lean, antes de afirmar
  nada. Con eso la rama pasa a J3a.
- **NO:** sería un contraejemplo o un error en J2 §2. Se detiene todo y se
  comprueba a mano.
- **MAYBE o KILLED:** confirma (b) con el presupuesto mayor, que se anota.
- Si el peldaño 1 no da YES, el problema es de instalación.

Hay otra vía, sólo con permiso del usuario: mysolvertimesout.org. Ahí lo
prueban en máquinas grandes, pero el problema queda publicado.

## 5. Dos estrategias acotadas: MAYBE

El portafolio por omisión corre muchas técnicas a la vez y llena el heap. Las
dos estrategias de [acotada/estrategia/](acotada/estrategia/aprove/predefinedstrategies/Piloto/)
son finitas y casi en serie, para que terminen. Las dos terminaron solas con
**MAYBE**: probaron todas sus técnicas y ninguna cerró la prueba. Por §11,
confirman (b) con este presupuesto. Las dos se detienen en el mismo núcleo de
2 o 3 pares, que es G misma.

| Estrategia | Corrida | Resultado |
| --- | --- | --- |
| [A](acotada/estrategia/aprove/predefinedstrategies/Piloto/peldano5.strategy) | 2357 s, `-Xmx6g` | MAYBE |
| [B](acotada/estrategia/aprove/predefinedstrategies/Piloto/peldano5b.strategy) | 2604 s, `-Xmx6g` | MAYBE |

**Qué técnicas usan.**
- A quita reglas con KBO, polinomios y matrices naturales, durante 5 min a lo
  sumo. Sigue con pares de dependencia: cambio de tamaño, polinomios,
  matrices árticas y naturales hasta dimensión 7, y etiquetado semántico con
  2 valores. Cada técnica tiene su reloj, de 10 s a 5 min.
  - Va al derecho y al revés a la vez.
  - Si nada cierra, prueba 20 min de etiquetado de raíz.
- B usa lo que A no usa: polinomios con coeficientes negativos o racionales,
  matrices racionales, matrices naturales de rango 3 y 7, y etiquetado
  semántico con 3 valores.
- Ninguna busca no terminación. En el piloto no puede haber lazos: las reglas
  X conservan el valor y las de R lo suben, así que una palabra L…R nunca
  vuelve a sí misma.
- Antes se validaron: A da YES en los peldaños 1 a 4, y B en el 3 y el 4, en
  segundos (`acotada/prueba_*` y `acotada/pruebab_*`).

**Dónde se atasca A** ([salida](acotada/peldano5_acotada.salida.txt),
[vigía](acotada/peldano5_acotada.vigia.txt)).
- Fase 1, unos 19 min. En las dos direcciones quitó la regla 7 → 8 y cerró el
  cruce de cifras con cambio de tamaño. Quedó el núcleo, que es G misma:
  - al derecho, 3 pares en L, la cabeza que pasa las cifras ternarias a
    binarias (nodo 46 de la salida);
  - al revés, 2 pares en R, el final que hace z → 3z/2 y z → (9z+1)/8
    (nodo 24).

  Ninguna técnica del presupuesto orientó esos pares.
- Fase 2, los 20 min siguientes. El etiquetado de raíz agrandó el núcleo a
  entre 31 y 60 pares, y su reloj lo cortó sin cerrarlo.
- Memoria: Java llegó a 6,21 GB, todo su heap, sin ninguna recolección
  completa ni `OutOfMemoryError`. El vigía no cortó nada.

**B se atasca en el mismo sitio** ([salida](acotada/peldano5_acotadab.salida.txt),
[vigía](acotada/peldano5_acotadab.vigia.txt)).
- Agotó sus técnicas en las dos direcciones y terminó sola.
- Quitó la misma regla, cerró el mismo cruce y dejó el mismo núcleo: sus
  nodos 26 y 50 son los 24 y 46 de A.
- Usó poca memoria: Java llegó a 0,83 GB, sin recolecciones completas ni
  cortes.

**Cómo se lanzan.** La carpeta `estrategia/` va en el classpath, y `-s` elige
la estrategia (`aprove.Piloto.peldano5b` para B). Desde `acotada/`:

```sh
java -ea -Xmx6g -cp "C:/Users/Home/herramientas/aprove/aprove_parche_stop.jar;estrategia" aprove.Main \
  -m wst -p plain -t 5400 -s aprove.Piloto.peldano5 ../peldano5_completo.srs
```

La orden exacta de cada corrida es la primera línea de su `*.vigia.txt`.

**Corridas descartadas** ([descartada/](acotada/descartada/)).
- B se lanzó mientras A corría, y se detuvo a los 25 s para no repartir la
  memoria.
- Al cerrar, su vigía cortó también dos MiniSat de A, porque cortaba todo
  solucionador nacido durante su corrida.
- Se corrigió el [vigía](windows/vigia.py): ahora corta sólo los
  solucionadores de su corrida. Después se repitieron A y B desde cero.

## 6. El portafolio completo, por turnos (en curso)

El portafolio de AProVE para SRS (`bigqsrs`) corre cuatro ramas a la vez: dos
búsquedas de lazos (`SRSNonLoop`) y `workOnSRS` al derecho y al revés. En §1 y
§3 las cuatro compartían el heap y la RAM. Aquí corren una tras otra, cada una
con el equipo entero: se cambia tiempo por memoria.

- Las estrategias de [turnos/estrategia/](turnos/estrategia/aprove/predefinedstrategies/Turnos/)
  copian literalmente la sección SRS de `aprove.Auto.current` del jar (líneas
  318-331 y 387-572). Sólo cambia `main`:
  - `derecho`: `Solve(workOnSRS)`;
  - `reves`: `Solve(QTRSReverse:workOnSRS)`;
  - `lazos`: las dos búsquedas `SRSNonLoop` de `bigqsrs`.
- [lanzar_turnos.sh](turnos/lanzar_turnos.sh) corre derecho (8100 s), revés
  (8100 s) y lazos (1800 s) bajo el vigía, y se detiene ante un YES o un NO.
- Este portafolio no puede dar MAYBE en el piloto: la búsqueda de lazos sin
  reloj, el etiquetado de raíz recursivo (`srsrootlabloop`) y el último grupo
  de matrices de `srsRedPair` no terminan solos. Sin prueba, cada turno acaba
  KILLED.

**Calibración.**
- 6 núcleos físicos (afinidad 0,2,4,6,8,10 y `-XX:ActiveProcessorCount=6`) y
  prioridad baja.
- Heap de 5 GB en derecho y revés, para dejar unos 4 GB a los solucionadores;
  8 GB en lazos, que corre dentro de Java.
- Vigía: tope de 3 GB por solucionador, aviso a 1,8 GB y mínimos de 1,2 GB.
- Validación ([cadena.txt](turnos/cadena.txt), `turnos/prueba_*`): derecho y
  revés dan YES en los peldaños 3 y 4, y lazos da NO en `a -> a a`
  ([bucle.srs](turnos/bucle.srs)).

**Intentos descartados** ([turnos/descartada/](turnos/descartada/)).
- Con `-Xmx7g`, a los 229 s: Java se quedó con los 7 GB, y el vigía cortó un
  MiniSat de 1,72 GB por falta de RAM.
- Con `-Xmx5g`, cortado entero a los 1859 s, sin veredicto:
  - a los 877 s el vigía cortó un MiniSat de 3,23 GB, más que el tope;
  - Java hizo 89 recolecciones completas y abortó 13 técnicas por
    `OutOfMemoryError`, casi todas pares de reducción (`QDPReductionPair`) al
    pasar sus fórmulas a DIMACS;
  - al final el compromiso libre bajó a 1,10 GB con 2,07 GB de RAM libre, y la
    regla 3 cortó todo. El archivo de paginación, gestionado por Windows,
    tenía 4 GB.
- Se corrigió el [vigía](windows/vigia.py): la regla 2 corta el solucionador
  mayor también cuando baja el compromiso, y tras cada corte se vuelve a
  medir. El revés, que llevaba 121 s, se detuvo, y la cadena se relanzó desde
  derecho a las 19:40.

**La maleta del Victus.** En 16 GB no caben a la vez el heap y los
solucionadores de esta rama. [turnos/maleta/](turnos/maleta/) arma una carpeta
portátil (361 MB, fuera del repo) para repetir la cadena en un portátil de
24 GB (Ryzen 5 5600H).
- Lleva el JDK, un Python mínimo con psutil, el jar parcheado, MiniSat, Z3, el
  adaptador de Yices, el vigía y estas estrategias.
- Su `lanzar.py` reparte la RAM libre al empezar: Java, el 55 % de lo libre
  menos 2 GB; cada solucionador, hasta el 60 % del resto.
- Valida con las cinco pruebas y corre la misma cadena. Los pasos están en su
  [LEEME.txt](turnos/maleta/LEEME.txt).

## 7. Las carpetas

- [ronda1_sin_solvers/](ronda1_sin_solvers/): la primera ronda, sin los
  solucionadores en el `PATH` (`Cannot run program "yices"`). Los peldaños 1
  y 2 ya daban YES.
- Los `peldano*.salida.txt` sueltos: la segunda ronda, con solucionadores y sin
  parche.
  - Incluye el peldaño 5 a 300 s y la corrida de una hora con `-Xmx10g`.
    Claude la detuvo a los 41 min, sin veredicto, porque el equipo se
    quedaba sin memoria.
  - Las dos tienen `NoSuchMethodError`.
- [prueba_parche/](prueba_parche/): los peldaños 1 a 4 con el jar parcheado, y
  el 3 a 60 s sin solucionadores.
- [vigilado/](vigilado/): con parche y vigía. Son las medidas que valen: el
  peldaño 4, y el 5 a 300 s y a 3600 s.
- [acotada/](acotada/): las estrategias de §5, sus validaciones, sus corridas
  y las descartadas.
- [turnos/](turnos/): el portafolio por turnos de §6, con sus estrategias, el
  lanzador, la validación, los intentos descartados y la maleta.

**Cómo se lanzó en Windows.**
- Desde Bash, con `MSYS2_ARG_CONV_EXCL='*'`, porque PowerShell 5.1 parte
  `-XX:ActiveProcessorCount=4`.
- Con `herramientas/bin` en el `PATH`.
- La orden exacta de cada corrida es la primera línea de su `*.vigia.txt`.
