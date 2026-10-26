# Perdices: auditoría del criterio de parada

26-10-2026. Objetivo del usuario: continuar hasta agotar Perdices o hasta
alcanzar una de las [tres condiciones primordiales](../balance20261025/BALANCE.md#condiciones-para-reabrir-la-búsqueda).

**El usuario retiró el objetivo automático; la continuación está detenida.**
No se declara agotamiento ni cumplimiento de una condición primordial.
El [último borrador](CONSTANTES_F_INVERTIBLE.md), con ocho núcleos Lean
comprobados, queda pendiente de revisión e integración; no altera las
369 afirmaciones ni las 34 consultas del conjunto integrado de abajo.

Se delimitaron
el transporte real y los pesos digitales; el frente matricial produjo
una reducción, una familia excluida y tres formas con F invertible,
pero conserva casos pendientes.
La ausencia de un
cierre de Collatz no demuestra por sí sola agotamiento de la ruta.

## 1. Las tres condiciones

| Condición | Evidencia actual | Dictamen |
| --- | --- | --- |
| Control aritmético nuevo para una semilla positiva fija, con cambios arbitrarios de bloques, que supere los modelos racionales y no sea el reloj reescrito | [Precisión creciente](PRECISION_CRECENTE.md) recupera el cilindro y rechaza al 23; la cota sobre cuándo se añade el siguiente bit sigue siendo la obligación de terminación o de reloj. [Pesos binarios](PESOS_BINARIOS.md) descarta el perfil monótono propuesto. | No satisfecha. |
| Transferencia demostrada de mezcla a las órbitas excepcionales, con hipótesis verificables | [Sesgo de frontera](../perdices20261025/SESGO_FRONTERA.md) descarta la convergencia poblacional fija. [Frecuencias temporales](../perdices20261025/FRECUENCIAS_TEMPORALES.md) y [balance ternario](../perdices20261025/OBSERVABILIDAD_TERNARIA.md) conservan una hipótesis individual pendiente. | No satisfecha. |
| Resultado externo que cierre una premisa universal con mapa, dominio y cuantificadores compatibles | [Límites reales](LIMITES_REALES.md) impide usar sin reparación el transporte de López–Stoll. Los contrastes de Monks–Yazinski y Kontorovich–Lagarias están delimitados en Observabilidad ternaria, §7. | No satisfecha; no se afirma una búsqueda bibliográfica exhaustiva. |

## 2. Ensayos delimitados

| Mecanismo | Límite comprobado |
| --- | --- |
| [Tamaño y regresos](../perdices20261007/TAMANO.md), [Cruce](../perdices20261007/CRUCE.md) y [Separación](../perdices20261007/SEPARACION.md) | Los entregables cuantitativos del plan de tamaño están realizados; una cuenta superior de regresos no excluye una fuga que acaba sobre cualquier techo. |
| [Colisiones](../perdices20261007/COLISIONES.md), [Cola](../perdices20261007/COLA.md) y [Mínimos](../perdices20261007/MINIMOS.md) | Sumabilidad, P tendiendo a infinito y reinicios de fuga pura están demostrados. MuroB y la ausencia de circuitos siguen siendo premisas abiertas. |
| [Repeticiones y complejidad](../perdices20261007/COMPLEJIDAD.md) | Se excluye complejidad baja; las historias genéricas quedan fuera de esa estimación. |
| [Reloj por rachas](../perdices20261007/congruencias_codex20261016/RELOJ_RACHAS.md) | Coeficientes válidos para cantidades fijas de rachas; crecen con esa cantidad. No son un reloj uniforme. |
| [Denominador global](../perdices20261007/congruencias_codex20261016/DENOMINADOR_GLOBAL.md) y [ventanas simultáneas](../perdices20261007/congruencias_codex20261016/VENTANAS_SIMULTANEAS.md) | La familia A B^b destruye la cota suficiente del denominador. Las 1391 barreras de tamaño admiten al 23. CRT recupera la integridad, sin una cota adicional sobre representantes. |
| [Observaciones fijas](../perdices20261025/RETORNOS_ARITMETICOS.md) y [ampliación digital](PESOS_BINARIOS.md) | Se descartan perfiles eventualmente monótonos en tamaño, incluso añadiendo el peso binario con cualquiera de sus dos orientaciones. El borrador digital ya está integrado. |
| [Precisión creciente](PRECISION_CRECENTE.md) | La representación exacta permite verificar un prefijo. Exigir nuevos bits indefinidamente equivale a la exclusión pendiente; exigirlos con ritmo lineal equivale al reloj. Falta una estimación nueva. |
| [Trazas y constantes matriciales](TRAZAS_MATRICES.md) | Bajo conexión bidireccional, las seis comparaciones matriciales son igualdades. Se excluye `M_a=M_b=tI` en cualquier dimensión, con vectores libres. [F invertible y A≠B](CLASIFICACION_F_INVERTIBLE.md) se reduce a tres formas, cuyas constantes generales siguen pendientes. |

Estas limitaciones no excluyen todos los rangos oscilantes, controles de
posición de bits, leyes dependientes del horizonte o presupuestos
amortizados. Son posibilidades generales, no desigualdades disponibles.

## 3. Frente que impide declarar agotamiento

[Soportes y rectas, §5](../perdices20261007/SOPORTES_MATRICES_H.md#5-siguiente-tanda)
dejó una tarea definida: estudiar las diferencias completas de constantes
y las nueve reglas estáticas en las familias acopladas. [Trazas](TRAZAS_MATRICES.md)
obtiene seis igualdades, escribe las diferencias completas y descarta
las matrices binarias comunes `tI` con vectores arbitrarios.
[Clasificación con F invertible](CLASIFICACION_F_INVERTIBLE.md) reduce A≠B
a imagen común, núcleo común o resonancia 2:3, sin omitir A,B singulares.
No está completa la clasificación general ni su factibilidad constante.

[Proyecciones](../perdices20261007/PROYECCIONES_MATRICES_H.md) excluye
interpretaciones escalares naturales y primeras coordenadas aisladas;
Soportes excluye rectas invariantes comunes y clasifica diez soportes
mínimos de aporte. La nueva obstrucción incluye familias conectadas sin
recta natural común, pero tampoco cubre todas las matrices acopladas.

El [informe YAH](../judas20261016/escalera/yah/INFORME_YAH.md) conserva
UNSAT de plantillas determinadas y formas indecisas. No se convierten
timeouts en pruebas de imposibilidad, ni se justifica ampliar uno sólo
para prolongar la búsqueda. G y H son mapas distintos: una conclusión
para H no se trasladará a A/B ni a MuroB sin demostrar la conexión.

**Siguiente acción concreta:** estudiar las constantes de las tres formas
con F invertible, mediante las diferencias dinámicas y las nueve estáticas;
separar F singular, A=B no escalar y el caso sin conexión bidireccional.
La resonancia queda excluida en el ensayo conectado 0..3 por una prueba
escrita; las dos formas de rango uno aún requieren estudio. La búsqueda nueva
con vectores libres dio UNSAT para matrices 0/1 y timeout para matrices
0..3 conectadas; no se aumentará el tiempo ni se convertirá esa respuesta
en una clasificación. Un certificado sólo contaría hacia una condición
primordial con su enlace orbital y su alcance explícitos.

## 4. Verificación de esta continuación

[Evidencia de sesión](evidencia_sesion.json): compilación de los módulos
del 26-10, 34 consultas de axiomas; 11 sobre límites reales, ocho en
la integración digital (incluyen cinco lemas base ya existentes) y nueve
sobre trazas y el núcleo escalar ponderado, más seis núcleos triangulares.
Lean 4.32.2, sólo axiomas estándar, sin sorryAx. Los tramos escritos no
formalizados se declaran en cada nota.

Contrastes exactos separados: 1702 pasos de las series y 248 pasos de
los retornos digitales. [Registro y generador](evidencia_registro.json):
369 afirmaciones, conservando las 365 anteriores a esta continuación.
El [cotejo matricial](cotejo_trazas.json) registra las pruebas finitas
independientes y los seis controles positivos del nuevo codificador.
La [clasificación](cotejo_clasificacion.json) coteja ocho soluciones binarias
y 378 ejemplos construidos; no sustituye la prueba escrita general.
No hay censos históricos repetidos ni publicaciones o mensajes externos.
La auditoría de fuentes anteriores es focalizada, no una recompilación
de todo el laboratorio. La revisión humana sigue pendiente.
