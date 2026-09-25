# Lagartijas: pocas entradas es improbable, y CF_F queda formal

25-09-2026. **Demostrado en Lean** ([Lagartijas.lean](formal/Lagartijas.lean),
19 consultas de axiomas sin `sorryAx`). Cierra el enlace finito que
[Guardias_finitas.md](Guardias_finitas.md) dejaba como primer paso.
**Gao no se declara resuelta**: faltan el límite de CF_F y el transporte
formal a clases.

## Enunciados

Cadena absorbente original `CadenaCompletaGao.paso` desde `((0,1),false)`,
bits iid justos que dan la paridad del ancla, tiempo en pasos físicos del
mapa atajo. `K_C(h)` es el contador de `ConteoEnsayos.lean`: posiciones
0..h con marca de entrada 1→2 y estado `(2,c)`, `|c|<=C`. Para m>=10,
`N=2^m`, `h=N^6`, `C=9h^4`:

    P(sigma>h y K_C(h)<N) <= 3/N+66/h+1/(4h^3).          (lagartijas)

Con `supervivencia_por_entradas`, para todo J con `1+J(W+2)<=N`, donde
`W=duracion C=H+D` y `p=riesgo C=2^-D/(4Q)` son los parámetros de EF:

    P(sigma>h) <= 3/N+66/h+1/(4h^3)+(1-p)^J.             (cf_f)

`ensayos_caben` muestra que `J_F=floor((N-1)/(W+2))` cumple la condición.
Es exactamente CF_F de [Ensayo_finito.md](Ensayo_finito.md), ahora teorema.

## La prueba no sigue el reloj escrito

[Cota_finita.md](Cota_finita.md) §2–3 usaba uniones sobre todos los inicios
t<=h (C2) y una contabilidad de rachas de frontera. Aquí no hacen falta.
Se sigue un autómata aumentado: número i de entradas guardadas y edad a
del hueco desde la última (o desde 0), más una marca de magnitud `<=U=h^4`.

1. **Reloj determinista.** Si ningún hueco con i<N alcanza edad G, la
   magnitud no cruza U y la cadena vive en h, entonces `t<=i*G+a` en todo
   t. Con `N*G<=h` resulta `K_C(h)>=N` (`reloj_determinista`,
   `muchas_entradas`). Bajo la marca, toda entrada tiene `|c|<=9U=C`.
2. **Potencial por huecos.** Sea `R_n` la probabilidad de seguir n pasos
   sin entrada guardada, vivo y acotado. `V=(N-1-i)q+R_(G-a)` es
   superarmónico y vale al menos 1 en el objetivo, así que
   `cruce_dominado` da `P(objetivo)<=V(inicio)=(N-1)q+R_G(inicio)`. La unión
   recorre los N huecos, no los h instantes.
3. **Hueco desde una entrada.** `R_(d+B+1)(2,c)<=P(tau>d)+beta` por una
   supersolución que suma la cola H3 (`RelojGao.cola_excursion`) con
   `d=N^4(10m+3)`: `P(tau>d)<=3/N^2` para todo c (`riesgo_entrada`,
   `cola_parametros`).
4. **Frontera.** Con `V=24m` y `theta=1+1/(4(V+3))`, el peso vale
   `2 theta^(v2(g)+1)` en k=0 y 2 o `theta^(V+2)` en k=1 según la paridad
   de c. Cumple `theta*E[w']<=w` fuera de las entradas (`deriva_frontera`),
   luego `R_r<=w/theta^r` (`riesgo_frontera`) y `beta=2/theta^B`. Una
   entrada sin guardia tiene `|c|>C`, magnitud mayor que U, y sale del evento.
5. **Parámetros.** `B=(96m+12)(19m+3)`, `G=d+B+1`, `N*G<=h`
   (`presupuesto_lagartijas`). Bernoulli da `theta^B>=2^(19m+3)`, luego
   `N*beta<=1/(4h^3)`; `(N-1)*3/N^2<=3/N`; C1 es `envolvente_cf`.

## Contrastes independientes

[verificar_lagartijas.py](verificar_lagartijas.py) reimplementa la
transición y calcula por enumeración o distribución exacta, sin las
recursiones de la prueba ([salida](evidencia_lagartijas_exacta.json)):
inclusión en todas las palabras (65.536 con 18.108 vivas con pocas
entradas; otro juego 17.445), frontera con 144 comparaciones (130 con cota
menor que 1) y excursión 19 de 19 no triviales, sin fallos. La cota global
es trivial a esa escala (`beta>1`), como advertía
[Cigarras](../gao20260924/Cigarras.md).

[verificar_lagartijas_pares.py](verificar_lagartijas_pares.py) usa pares
reales `(n,n+1)`, `n` en `[2^18,2^19)`, bajo T
([salida](evidencia_lagartijas_pares.json)). En los 262.144 pares, `(k,c)`
reconstruido de los enteros coincide con la cadena en los 19 instantes;
las palabras recorren cada clase módulo `2^18` una vez; las fusiones hasta
t son exactamente `2^18*P(fusión hasta t)`; la inclusión vale en los 72.432
pares vivos con pocas entradas. Controles finitos: el certificado universal
es Lean ([compilación](evidencia_lagartijas_lean.json)).

## Lo que no es, y lo que vino después

Por sí sola no da el límite ni la densidad. Ambos quedaron demostrados el
mismo día: [Martas](Martas.md) prueba `P(sigma>h)->0` y [Tejonas](Tejonas.md)
transporta a pares reales y cierra la conjetura de Gao en su forma de
Lagarias, pendiente de revisión humana y del cotejo del artículo primario.
