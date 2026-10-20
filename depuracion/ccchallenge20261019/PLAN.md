# Plan: clasificar G con el criterio de Nashida (para el Victus)

Fecha: 19-10-2026. Se escribió en el PC de escritorio y se ejecuta en el
Victus (Linux, usuario `oem`), la máquina de las corridas largas, donde ya
están las tandas de YAH (`depuracion/judas20261016/escalera/yah/`).

## Por qué

Se leyó la lista de ccchallenge.org (API `https://ccchallenge.org/api/papers`,
389 entradas) y se cruzó con el repo; el resultado está en `cruce.json`:
78 papers citados, 62 con el apellido nombrado pero sin el año y 249 que no
se nombran nunca. Antes de 2010 casi todo es la bibliografía de Lagarias,
que ya está leída.

Lo único que cambia el rumbo son tres preprints de Nashida (2026), en
Zenodo. No estaban citados en ninguna nota de YAH ni de Judas:

| Zenodo   | Qué dice |
|----------|----------|
| 23081447 | Parte I. Un mapa de la clase 𝒢, `(A·z+b)/2^e` por restos, tiene certificado de valuación escalonado si y sólo si está «desenredado». «Enredado» quiere decir que una componente fuerte tiene a la vez un ciclo que crece y un vértice que se ramifica. |
| 23081491 | Parte II. Barreras para interpretaciones matriciales en cualquier dimensión, y los debilitamientos máximos de la conjetura 4.14 de YAH (4089 y 10913 mod 2^14). |
| 23147025 | En ninguna dimensión progresan sobre collatz-T las interpretaciones naturales (EWZ), ni las árticas sobre collatz-T y collatz-T-5or7mod8. Está comprobado en Lean. |

Esto encaja con lo que ya vimos en `escalera/yah/PENDIENTES.md`. Con cada
rama sola hay prueba (el peldaño 4 da QED en segundos), pero el peldaño 5 se
queda con 11 reglas y G_A2 resiste con 11. Lo difícil es mezclar las dos
ramas, que es justo el «enredo» de Nashida. Si G está enredado, otra tanda
de YAH con matrices o árticas está condenada de antemano. Mejor saberlo
antes de gastar horas de Victus.

Cautelas:
- Nashida trabaja con IA (Claude) y nadie lo ha revisado.
- La no existencia de la parte I no está formalizada.
- AProVE combina más técnicas que las matrices, así que estas barreras no
  lo excluyen.

## Qué está hecho

- `specs_nashida.py` escribe G y sus debilitadas G_A2…G_A5 y G_B4…G_B7 en
  el formato `r:A,b,e;...` y comprueba cada spec contra la definición
  directa en todo z < 2^12. Deja `specs_nashida.json`.
- La spec de G, con k=3, es `0:3,0,1;2:3,0,1;4:3,0,1;6:3,0,1;7:9,1,3`.
- El formato está inferido de los papers, no del código. Lo primero es
  confirmarlo (paso 2).

## Pasos en el Victus

0. `git pull` en el clon del Victus. No tocar las tandas de YAH que estén
   corriendo: el clasificador tarda segundos y sólo usa la biblioteca
   estándar, así que puede convivir con ellas.
1. **Bajar** el repo de Nashida fuera del repo nuestro, en una carpeta
   vacía. Es código de un tercero; el 19-10 el usuario pidió hacer esto en
   el Victus:
   ```
   mkdir -p /home/oem/herramientas/nashida
   cd /home/oem/herramientas/nashida
   git clone https://github.com/harappa/collatz-termination-certificate-dichotomy
   ```
   Apuntar el commit (`git rev-parse HEAD`).
2. **Leer** `computations/classify_families.py` entero antes de ejecutarlo.
   Confirmar tres cosas:
   - que no hay red ni escritura fuera de su carpeta;
   - cuál es el formato exacto de la spec (qué es `b`, si los restos que
     faltan paran);
   - cómo se pasa `k`.
   Si el formato no coincide, corregir `specs_nashida.py` y volver a
   correrlo.
3. **Autotest.** Ejecutar `g1check`, o lo que el código traiga para
   reproducir su tabla 5, y comprobar que sale igual que en el paper. Si no
   coincide, parar aquí y anotarlo.
4. **Clasificar** los 9 sistemas de `specs_nashida.json`: G, G_A2…G_A5 y
   G_B4…G_B7. Correr Python con `-I` y pasar la ruta del script como
   argumento, sin hacer `cd` dentro del clon. Guardar la salida literal en
   `clasificacion.txt`, en esta carpeta.
5. **Leer el resultado** frente a las tandas de YAH:
   - *G enredado.* Las matrices y árticas no bastan. No lanzar más formas
     de YAH sobre el peldaño 5. Mirar qué debilitadas salen desenredadas y
     si coinciden con las que YAH resolvió.
   - *G desenredado.* Nashida da un certificado escalonado: anotarlo
     entero. Es la ruta nueva y hay que pasarlo a Lean (pieza aparte, con
     su propio plan).
   - *Mezcla en la escalera* (unas sí y otras no). El corte en k dice dónde
     está la frontera. Contrastarlo con el k donde la cascada de YAH deja de
     dar QED (`resultados_debilitadas/`).
6. **Subir** con `git add -A`, commit y push, sólo si el usuario lo pide en
   esa sesión. Van `clasificacion.txt`, la nota del commit de Nashida y los
   cambios de `specs_nashida.py`. El clon de Nashida queda fuera del repo.

## Pistas secundarias de la lectura (sin prisa)

- **Rozier 2017, LBH.** No está en el repo. De Jesus 2026 prueba que
  LBH ⇒ Collatz. Hay que compararlo con MINIMOS antes de citarlo.
- **Macindoe 2026.** Interés medio para Perdices (cargas).
- **Descartados por no aportar ruta:** Velazquez, Pereira, Halemane,
  Williams, Siegel, Sterin, Monks 2013 y Capco.

## Fuera de este plan

- Responder a Rozier (19-10). Muestra interés en la coalescencia de Gao,
  Garner y Wu, y Terracol falleció. Sólo se responde con permiso para ese
  envío.
- El encargo de la barrera Lean de Perdices (CLAUDE.md) sigue sin empezar.
