# Ocelotas: veinte rachas en Lean — 03-10-2026

**Continuación:** cierre posterior de [veintiuna rachas](VEINTIUNA_LEAN.md).
Se conserva aquí la evidencia de la tanda de veinte.

**Cierre verificado:** reconstrucción limpia de 37 módulos, código 0,
153 consultas de axiomas (147 listas estándar y seis declaraciones
libres de axiomas), sin `sorryAx`. Se cotejaron las huellas de las fuentes,
del comprobador y de los objetos ([registro](lean_veinte.txt)).
Extiende el [cierre de diecinueve](DIECINUEVE_LEAN.md) y conserva su
verificador general de prefijos.

## Enunciado y alcance

Mapa atajo: `T(n)=n/2` para n par y `(3n+1)/2` para n impar, n>=2.
`S_j(n)` cuenta entradas impares en los primeros j pasos. Un primer
cruce k satisface `3^S_j(n)>=2^j` para `1<=j<k` y `3^S_k(n)<2^k`.
`rachas n k` cuenta bloques maximales de entradas impares. No hay
distribución probabilística ni promedio sobre semillas.

[OcelotasVeinte.lean](OcelotasVeinte.lean) prueba:

```lean
theorem cst_veinte_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 20) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

Así, el primer descenso coincide con el primer cruce para hasta veinte
rachas. Un fallo necesita **al menos veintiuna rachas**. Se incluye el
caso par. La existencia del cruce es una hipótesis: no se demuestra que
todo n tenga cruce ni que llegue a 1.

`LMN23` es el corolario 2 de Laurent–Mignotte–Nesterenko, especializado
en 2 y 3. Su traducción a `LMNDebil` está en Lean; su prueba trascendente
sigue como hipótesis externa explícita. La fórmula publicada se
[cotejó con el original](LECTURAS_20261003.md). Sólo la cola usa LMN.

## Certificados de prefijos

La [tabla de 42 intervalos](OcelotasVeinteTabla.lean) cubre
`1<=q=S_k(n)<4598951775`. Cinco filas se excluyen mediante la criba
afinada, 35 remiten al certificado finito hasta n=4912740 y dos necesitan
la criba por prefijos:

| Intervalo inclusivo de n | q mínimo | Nodos explorados | Profundidad máxima | Clases finales no vacías |
|---|---:|---:|---:|---:|
| 4912741..5457441 | 79335 | 55811 | 43 | 8548 |
| 4912741..310041588 | 190537 | 67649 | 46 | 21800 |

Ambos certificados usan combustible 96; agotarlo rechaza. Los
intervalos contienen 544701 y 305128848 semillas y se solapan; sus
cardinalidades no se suman. La afirmación para estos intervalos está
condicionada a `q>=q_min` y al máximo de veinte rachas.

El verificador conserva `n=r+m*u`, `T^i(n)=a*u+c`, el número de impares,
las rachas y la paridad anterior. En un corte posterior a una entrada
par, la cota `q_i+cota(20-s,M)<q_min` excluye un fallo. La prueba general
está en [OcelotasCribaPrefijos.lean](OcelotasCribaPrefijos.lean); su
[derivación y condiciones](DIECINUEVE_LEAN.md#reiniciar-la-criba-con-un-prefijo-real)
se conservan.

[OcelotasVeintePrefijos.lean](OcelotasVeintePrefijos.lean) divide los
árboles a profundidad diez: 64 y 50 bloques no terminales, con 181 y 171
nodos de ensamblaje, respectivamente. Cada hoja se evalúa con
`decide +kernel`. [OcelotasPrefijosBloques.lean](OcelotasPrefijosBloques.lean)
prueba la unión de dos hijos después de comprobar todas las condiciones
de la rama. Las declaraciones finales usan sólo axiomas estándar.

El [generador de bloques](generar_prefijos_lean.py) propone constantes;
Lean vuelve a comprobar las condiciones, las hojas y su unión. No se
importa como prueba la salida del explorador.

## Cola infinita y semillas pequeñas

[OcelotasVeinteCola.lean](OcelotasVeinteCola.lean) demuestra
`cota(20,M)<=20148*M`. Para t>=32, por inducción:

`40296*(19*(t+33)^2+6)<2^t`.

El coeficiente **19** dentro del paréntesis procede de LMN y no cuenta
rachas. Un fallo da `k<=40296*(19*(t+33)^2+6)` para el correspondiente
t, mientras `2^t<=k`. Como `q>=4598951775>2^32` implica k>q,
esto elimina toda la cola.

Se conserva [OcelotasResiduosFinito.lean](OcelotasResiduosFinito.lean):
para todo `2<=n<=4912740` hay primer cruce de longitud <=224 y descenso,
sin LMN ni límite de rachas. No se amplía ese certificado ni el censo
consecutivo anterior hasta `2^23`.

## Contrastes y reproducción

- [Cotejo de la tabla](cotejo_veinte_lean.json): 42 filas mediante series
  racionales de `atanh`, productos enteros y recurrencia independiente.
- [Cotejo de prefijos](cotejo_prefijos_20.json): reconstrucción por
  órbitas directas de representantes, potencias, contadores, bordes,
  desigualdades exactas y cobertura disjunta de 30348 clases no vacías.
  No importa las transiciones del explorador.
- Propuestas originales: [tabla](preparacion_veinte_lean.json),
  [caso bajo](prefijos_20_bajo.json), [caso alto](prefijos_20_alto.json).

Los generadores reprodujeron byte por byte los módulos de tabla y
prefijos en una carpeta temporal. El [registro versionado](../coherencia20260913/registro.json)
incorpora `ocelotas_cst_veinte_rachas_prefijos_lean`; la base se regeneró
con 259 afirmaciones, vocabulario, archivos e integridad correctos
([controles](registro_veinte.txt)).

Desde la raíz, con Lean 4.32.2 y el Mathlib fijado:

```text
python -B -X utf8 depuracion/cst20260930/preparar_cierre_lean.py --rachas 20 --bits-cola 32 --salida depuracion/cst20260930/preparacion_veinte_lean.json
python -B -X utf8 depuracion/cst20260930/generar_veinte_lean.py --certificado depuracion/cst20260930/preparacion_veinte_lean.json --salida depuracion/cst20260930/OcelotasVeinteTabla.lean
python -B -X utf8 depuracion/cst20260930/generar_prefijos_lean.py --bajo depuracion/cst20260930/prefijos_20_bajo.json --alto depuracion/cst20260930/prefijos_20_alto.json --profundidad 10 --espacio OcelotasVeintePrefijos --salida depuracion/cst20260930/OcelotasVeintePrefijos.lean
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_veinte.txt
python -B -X utf8 depuracion/cst20260930/cotejar_veinte_lean.py --certificado depuracion/cst20260930/preparacion_veinte_lean.json --salida depuracion/cst20260930/cotejo_veinte_lean.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos.py --certificados depuracion/cst20260930/prefijos_20_bajo.json depuracion/cst20260930/prefijos_20_alto.json --salida depuracion/cst20260930/cotejo_prefijos_20.json
```

### Compilación conservada

Por defecto, el comprobador reconstruye toda la cadena en una carpeta
temporal limpia. `--compilados RUTA` conserva los `.olean` y un manifiesto
de fuentes, objetos y auditorías; también recompila toda la cadena.
Sólo al añadir `--reutilizar` admite un prefijo ya auditado si coinciden
entorno, fuentes, objetos y todas las dependencias anteriores.
El primer desacuerdo obliga a recompilar el resto. Las auditorías
conservadas se validan otra vez y la salida distingue compilaciones de
reutilizaciones. La reutilización no se presenta como reconstrucción limpia.

[Control de rechazos](control_cache_lean.json): detecta cambios de fuente,
dependencias y objeto, axiomas ajenos, huecos y ausencia de auditoría.
La validación integral terminó: segunda ejecución con **0 compilaciones
y 37 reutilizaciones**, con cotejo de los objetos conservados
([registro](lean_veinte_reutilizado.txt)). El control corresponde al
comprobador usado en esta tanda; ampliarlo después cambia su huella.

La revisión humana y la novedad siguen pendientes. Las 75 rachas bajo
Rozier–Terracol conservan su alcance escrito y exacto, sin cierre Lean
completo.
