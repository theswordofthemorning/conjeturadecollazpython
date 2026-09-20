# Ensamblaje candidato: absorción, clases y Gao

20-09-2026. **Candidato en auditoría local, no anunciar como resolución.**
La segunda auditoría añade [Cota_finita.md](Cota_finita.md), que reemplaza
el cierre casi seguro de esta nota por CF, una cota explícita a tiempo
finito. Esa es ahora la ruta preferente de revisión. Esta versión se conserva.
El objetivo no se marca completado. La revisión debe atacar en particular
la ley de bits después de cambiar el ancla, las paradas del protocolo,
la divergencia pathwise y el enlace con el enunciado original de Gao.

## 1. Dependencias

- [Reloj global](Reloj_global.md): en la no absorción, `S_i=O(i^4)` y
  `|c_(S_i)|=O(i^16)` casi seguramente.
- [Ventana ampliada](Salida_ampliada.md): V3 y palabra V4; piso V5–V6.
- Transiciones exactas y correspondencia entre palabras y clases:
  `cadenakc.lean`, Terras y la contabilidad de pendientes del laboratorio.

## 2. Ensayos sin solapamiento

Se sigue siempre la cadena original; no se fuerza una trayectoria.
Empezar el ensayo j en una entrada `S_(I_j)`, con offset x_j.
Los parámetros T,H,G se fijan por x_j antes de leer los bits siguientes.
Esperar la primera salida R_(I_j), finita casi seguramente.

Si `T<tau<=H` y `|c_R|<=G`, calcular la palabra de Hormigas desde
ese estado y observar tantos bits como su longitud. El éxito es que
coincidan todos los bits (una fusión anterior también termina el proceso).
Si no se cumple la condición de salida, el ensayo termina en R.
Si sigue vivo, el siguiente ensayo empieza en la primera nueva entrada
a k=2 después de terminar el ensayo actual.

Todos son tiempos de parada: los parámetros se conocen al empezar y
la longitud de la palabra se conoce al llegar a R. Se puede esperar
la salida incluso cuando supera H; no hay truncación oculta ni
condicionamiento de los bits que aún no se leen.

Condicionado al pasado en el inicio del ensayo, la probabilidad de
éxito es al menos f(x_j), por V3, V4 y Markov fuerte en R. No se pide
independencia entre ensayos.

## 3. Los índices seleccionados no crecen demasiado

En no absorción hay infinitos ensayos. Durante la excursión no se
salta ninguna nueva entrada a k=2 desde k=1. Durante la palabra se
saltan a lo sumo tantos inicios como bits leídos. Tras ella se busca
la siguiente entrada; si se quedó dentro de una excursión, sólo se
termina esa excursión antes de la nueva entrada. Por tanto

    I_(j+1) <= I_j + D_G(x_j)+2,
    D_G(x)=16(ceil(log2(G(x)+2))+1)^2.

Por RG, `|x_j|<=C_omega (I_j+1)^16`. Luego
`D_G(x_j)=O_omega((1+log log(I_j+3))^2)`; basta degradarlo a
`D_G(x_j)+2<=C_omega sqrt(I_j+1)`.
La desigualdad `sqrt(y+C sqrt(y))<=sqrt(y)+C/2` da
`I_j=O_omega(j^2)`. De aquí `|x_j|=O_omega(j^32)`.

V6 implica, en cada una de esas trayectorias, `f(x_j)>=j^(-1/2)`
para todo j suficientemente grande (el umbral puede depender de la
trayectoria). En consecuencia `sum_j f(x_j)=infinito` sobre la
no absorción, salvo un evento nulo.

## 4. Cierre probabilístico propuesto

Sea E_j el evento de éxito del ensayo j; después de absorber, completar
la filtración y poner E_j falso. E_j es medible antes del siguiente
ensayo, y su probabilidad condicionada al inicio satisface el piso
anterior mientras se esté vivo. El lema condicional de Borel–Cantelli
(o su prueba por supermartingala) dice que en el evento donde la suma
de esas probabilidades diverge ocurren infinitos E_j casi seguramente.
Pero puede ocurrir a lo sumo uno porque el éxito absorbe. El evento
de no absorción debe, por tanto, ser nulo.

Se puede evitar invocar el lema sin prueba. Poner `p_j=P(E_j|F_j)`,
donde F_j es el pasado al empezar el ensayo j, y `A_N` el evento de
ningún éxito en los primeros N ensayos. Entonces

    Z_N = 1_(A_N) exp(sum_(j<=N) p_j)

es una supermartingala no negativa (con la filtración al finalizar
cada ensayo), porque `(1-p)exp(p)<=1` para `0<=p<=1`. Parar en el
primer N con suma de riesgos >=M, y truncar además en N<=L, da
`P(A_N y suma>=M antes de L)<=exp(-M)`. Primero L tiende a infinito,
luego M: la probabilidad de ningún éxito y suma infinita es cero.
Los tiempos posteriores a una fusión se pueden completar como la
misma parada absorbente; en esa rama p_j=0. No se usa una ley
condicionada a «no absorber nunca» para obtener los pisos.

**Conclusión candidata:** la cadena original absorbe casi seguramente
desde `(0,1)` (y desde los dominios de arranque declarados). Este paso
necesita auditoría conjunta; no cambiar su estatus por pasar tests finitos.

## 5. Traducción que debe verificarse

Desarrollo universal añadido: [Cilindros.md](Cilindros.md), con
ingredientes de refinamiento en `cilindros.lean`.

Un prefijo de bits de ancla debe corresponder a exactamente una clase
módulo `2^t`. Inductivamente, en esa clase el ancla es `a*m+b` con a
impar; al añadir el siguiente bit, las dos paridades de m producen las
dos ramas. Cambiar el ancla al otro miembro conserva pendiente impar:
es una pendiente de Terras `3^s`. Esto debe comprobarse incluso en
los vuelcos y al reordenar el gap en k=0. No alcanza con mirar el
par menor: el bit pertenece al ancla.

La absorción es la igualdad de valores con igualdad de pendientes,
esto es, igual número de entradas impares. Por tanto su probabilidad
hasta t es `a(t)/2^t`. Absorción casi segura implicaría `phi=1` y
densidad natural uno de fusiones balanceadas por inclusión periódica.

Para el mapa clásico C, una fusión balanceada en t pasos de T y s
entradas impares es una fusión en t+s pasos de C. Para cada nivel t
fijo, todos los elementos suficientemente grandes de las clases que
ya fusionan satisfacen `t+s<=2t<=log2(n)` si `n>=2^(2t)`.
Así `phi=1` implicaría densidad uno del conjunto

    {n>=1: existe j<=log2(n), C^j(n)=C^j(n+1)}.

Esto no requiere que la cola común alcance 1. Igualdad de alturas
**finitas** sigue exigiendo convergencia, salvo que se demuestre otro puente.

## 6. Fuente y límite bibliográfico

La ficha del artículo de Gao (1993),
[DOI](https://doi.org/10.1016/0012-365X(93)90240-T), fue localizada;
el proveedor negó acceso al texto completo en esta tanda. La formulación
con `j<=log2(n)` aparece en la entrada 68 de la
[bibliografía de Lagarias](https://arxiv.org/pdf/math/0309224), p. 28 del
PDF (página impresa 28). Es una atribución secundaria, no un cotejo
del original. **Pendiente leer la formulación primaria de Gao** antes
de identificar definitivamente esta conclusión con su conjetura.

No se ha enviado, publicado ni comunicado este candidato a terceros.
