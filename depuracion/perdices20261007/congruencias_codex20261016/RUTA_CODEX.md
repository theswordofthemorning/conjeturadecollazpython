# Perdices: ruta de Codex y balance de avances

Cierre documental del 18-10-2026. Este índice reúne el trabajo de la ruta;
las pruebas, programas y evidencias permanecen en las notas enlazadas.
Se conserva el nombre Perdices, sin reivindicar prioridad bibliográfica.

## Objetivo matemático y dominio

Se estudia el atajo T sobre enteros positivos: n/2 si n es par y
(3n+1)/2 si es impar. A=1 y B=110 son bloques de paridades realizadas
desde una misma semilla n; sus duraciones son uno y tres pasos T.
No se introduce una ley aleatoria ni condicionamiento probabilístico.

El objetivo concreto es demostrar constantes universales C,D>=0 con
`L<=C*ell(n)+D` para toda palabra finita real A/B,
`ell(n)=ceil(log2(n+5))`. Equivale al presupuesto uniforme P de esta
ruta, permitiendo cambiar sus constantes. **Ambos siguen abiertos.**
El objetivo excluye persistencia en esta clase; no constituye por sí
solo una demostración de Collatz. MuroB y la ausencia general de
circuitos no triviales tampoco quedan resueltos por estos avances.

## Resultados y fronteras de la prueba

| Etapa | Resultado conservado | Límite y formalización |
| --- | --- | --- |
| [Congruencias compartidas](CONGRUENCIAS.md) y [órbitas](ORBITAS.md) | Banda óptima según b módulo 6 para la parte impar compartida; transporte a la semilla original. | Congruencias y enlace orbital en Lean; realización general de las familias óptimas escrita. No se suman mínimos independientes. |
| [Ventanas conjuntas](CONJUNTAS.md) | Dos mínimos vecinos son incompatibles; exceso óptimo 72 por pareja disjunta, alcanzado en n=667. | Certificado modular y enlace en Lean; extracción de listas generales escrita. No es todavía un coste temporal. |
| [Barrera triple](BARRERA.md) | Cada tres excesos contienen uno >=17; suma k_i>=17*floor(m/3), con desigualdad ponderada desde n. | Barrera, enlace y suma formalizados; extracción general escrita. El peso puede crecer geométricamente. |
| [Reloj terminal](RELOJ_TERMINAL.md) | La carga terminal se absorbe mediante continuación real; P equivale al reloj uniforme. | Equivalencia y continuación en Lean. No se ha demostrado la existencia de ese reloj. |
| [Pendiente uno](PENDIENTE_UNO.md) | Familias reales con L-ell ilimitado: cualquier reloj uniforme exige C>1. Mínimos de palabras no multiplicativos. | Familia orbital y obstrucción a C<=1 en Lean; identificación de mínimos y cocientes escrita. No descarta C>1. |
| [Reloj por rachas](RELOJ_RACHAS.md) | L+v_fin<7*ell hasta cuatro rachas; coeficiente explícito para cada cantidad fija. | Cotas restringidas y álgebra del modelo en Lean; conexión general y fórmulas cerradas escritas. El coeficiente crece geométricamente. |
| [Defecto interior](DEFECTO_INTERIOR.md) | Tras cualquier prefijo terminado en B aparece una racha A arbitrariamente larga con defecto fijo. | Núcleo auxiliar en Lean; existencia por congruencias escrita. No impide compensaciones entre rachas. |
| [Contexto bilateral](CONTEXTO_INTERIOR.md) | También se prescribe un futuro arbitrario: U A^a B A² V, con parte impar 13 y defecto central fijo. | Empalme y altura condicionales en Lean; levantamientos, CRT y existencia general escritos. Semillas distintas, no una órbita infinita. |
| [Compensación relativa](COMPENSACION_RELATIVA.md) | En la relajación, incluso delta_i>=eta*H_i+K con eta<1 permite coste ilimitado y pérdida relativa en todas las ventanas. | Obstrucción del modelo y divisibilidad orbital AB en Lean; ventanas y límites escritos. Las órbitas reales AB excluyen esos modelos. |

La barrera triple ya tenía evidencia de compilación en el histórico;
se corrigió la indicación documental desfasada y se añadió la suma
ponderada. La divisibilidad de AB aplica el mecanismo previo de
[repetición](../COMPLEJIDAD.md): no se presenta como una solución nueva
para historias no periódicas.

## Qué debe resolver el siguiente paso

En el modelo de rachas, `H_1=ell`,
`H_(i+1)=H_i+gamma_(p_i)*d_i`, con gamma_A=10/17 y gamma_B=1/17.
Se incorpora v_fin únicamente a la última duración. Definir

```text
C([])=0, C(p::s)=1+(1+gamma_p)*C(s),
delta_i=H_i-d_i, w_i=1+gamma_(p_i)*C(cola_i),
Z=sum_i w_i*delta_i.
```

La identidad demostrada es `L+v_fin=C(lista)*ell-Z`. El reloj exigiría

```text
Z >= (C(lista)-C*)*ell-D*
```

con C*,D* independientes del número de rachas. Esta desigualdad es una
**reformulación exacta pendiente**, no un lema aritmético obtenido.

Las familias reales descartan exigir pérdidas proporcionales en cada
racha. Los modelos muestran además que reservas constantes, porcentajes
fijos del descuento máximo e incluso convergencia relativa a uno no
controlan por sí solos el residuo absoluto. Hace falta una restricción
conjunta de realización aritmética para historias no periódicas,
conservando la misma semilla y sus fronteras. El caso periódico AB
ilustra esa diferencia, pero no cubre dichas historias.

## Evidencia, conservación y reproducción

[Evidencia de sesión](evidencia_sesion.json): 139 consultas Lean únicas,
con Lean 4.32.2 y Mathlib fijados. Los módulos indicados en cada nota se
recompilaron desde fuente; sólo aparecen axiomas estándar, sin sorryAx.
Se cotejan imports directos y sus objetos, no toda la cadena transitiva
de Mathlib. La revisión humana sigue pendiente.

Los cotejos usan enteros o Fraction, implementaciones independientes,
T literal y bordes cuando corresponden. Distinguen certificados finitos
exhaustivos con prueba de cobertura de simples contrastes de ejemplos.
Ningún barrido se usa como prueba universal. No se repitió el censo de
Salidas ni el conjunto general de controles por cambios documentales.

Las [nueve altas versionadas](alta_registro.json) se integraron mediante
el generador del laboratorio: catálogo de 349 a 358 afirmaciones,
244 demostradas, 92 medidas, 13 conjeturadas y nueve refutadas.
La [verificación de conservación](evidencia_registro.json) confirma
las 357 filas anteriores a la última alta y respuestas.db intactas.
Registro, mapa y SQLite quedaron cotejados. No se reconstruyeron
conversaciones ni se modificó zootheorem.

Para comprobar enlaces, fuentes, evidencias y conservación sin repetir
los experimentos:

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/verificar_sesion.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_sesion.json
```

Cada nota temática contiene los comandos de reproducción de sus pruebas
y cotejos. El [estado breve](../../../ESTADO_INVESTIGACION.md) conserva
la obligación actual; este índice evita tener que precargar las notas.
