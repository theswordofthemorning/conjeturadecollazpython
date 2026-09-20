# Gacelas: variante armónica de la ventana y CF_H

20-09-2026. **Candidato de ensamblaje**, no resolución de Gao.
Esta variante evita la fórmula binomial de supervivencia. Conserva
la ruta anterior en [Salida_ampliada.md](Salida_ampliada.md) y
[Cota_finita.md](Cota_finita.md); cambia explícitamente Q, G, D y p.

## 1. Cadena, ley y dos controles formales

Mapa atajo, cadena absorbente original, bits iid justos que indican
la paridad del ancla. Arranque `(2,c0)`, c0 entero firmado. Tau es la
primera llegada a k=1, no la fusión. El tiempo t cuenta pasos físicos.
Para estudiar esta primera excursión se congela la base en k=1.
Esto no modifica ningún evento anterior a tau. La extensión de W
continúa siendo multiplicativa, como en [Resto.lean](formal/Resto.lean).

Poner X_t=k_t−1 antes de salir y cero después; M_h cuenta los pasos
mixtos de los primeros h pasos físicos, incluido el que sale, y deja
de contar tras tau. No cuenta los pasos compartidos.

[Supervivencia.lean](formal/Supervivencia.lean) demuestra directamente
en la cadena que X es armónica, `E X_t=1` y
`X_t <= (t+1) 1_(tau>t)`. Por tanto

    P(tau>t) >= 1/(t+1).                                  (H1)

El promedio se identifica con un conteo de hojas entre `2^t` palabras.
H1 es más débil que G2, pero suficiente para la ventana ampliada.

[Banda.lean](formal/Banda.lean) detiene además la cadena al llegar
a altura L, para cualquier entero L>=1. En la banda 0..L,
`V(x)=x(L-x)` es no negativo; su deriva en un paso físico es −1 si
ese paso es mixto y cero si es compartido. La identidad de energía
da `E M_h_banda <= L−1`. La altura detenida conserva media 1, luego
la probabilidad de haber tocado L antes de h es <=1/L.

El archivo incluye el contador como parte del estado y demuestra
Markov para ese contador, no sólo una recurrencia de expectativas.
También acopla ambos árboles con los mismos bits: o la banda ya
tocó L, o la base y el contador coinciden con los de la excursión
original. Así, para todo h>=0, n>=1 y c0,

    P(M_h>=n) <= 1/L+(L−1)/n.                             (H2)

En particular, n=L^2 da `P(M_h>=L^2)<=2/L`. Estos resultados no
suponen que los pasos físicos tengan una probabilidad fija de ser
mixtos ni cambian la ley al observar supervivencia futura.

## 2. El enlace del reloj certificado

Sea T_n el tiempo del n-ésimo paso mixto, o tau si se sale antes.
Mangostas M6 da, con `a=2+floor(log2(n+2))`,

    P(T_n>n(a+s+1)) <= n*2^(-s).                          (M6)

Antes del n-ésimo mixto, k<=n+2; cada racha tiene umbral compartido
como máximo a. [Reloj.lean](formal/Reloj.lean) certifica M6 usando
bloques deterministas de a+s+1 pasos y el contador real de mixtos.
Cada bloque sin progreso cuesta como máximo 2^-s. La inducción
acumula n veces ese coste, bajo la ley original y sin condicionar
a supervivencia futura. [Derivación y bordes](Reloj_bloques.md).

Si H=n(a+s+1), en `{tau>H}` o bien T_n>H, o bien M_H>=n.
Aplicar M6 y H2 entrega la cota también certificada

    P(tau>H) <= 1/L+(L−1)/n+n*2^(-s).                    (H3)

No se necesita la fórmula exacta del paseo simétrico ni el muestreo
de una secuencia infinita de monedas mixtas. H3 es el teorema
`RelojGao.cola_excursion`, universal en c0 entero, n,L>=1 y s>=0.

## 3. Parámetros de la variante

Todos los logaritmos siguientes son en base 2. Para cada c0 definir

    m0=ceil(log2(2+|c0|)),    T=32 max(32,m0),
    Q=T+1,                  L=16Q,
    n=L^2=256Q^2,
    a=2+floor(log2(n+2)),    s=3 ceil(log2(n+1)),
    H=n(a+s+1),
    R=[128(H+1)Q]^2,        G=3(R+1).

Q es ahora T+1; **no** se usa el Q anterior de orden sqrt(T).
Los demás cambios de G, D y del riesgo se calculan a partir de este Q.

De H3, `2/L=1/(8Q)` y `n*2^-s<=1/n^2<=1/(8Q)`, luego
`P(tau>H)<=1/(4Q)`. El último paso se comprueba con `n^2>=8Q`.

El [producto normalizado](formal/Producto.lean) tiene coste de cruce
en T..H como máximo `(61/62)^T`. Para todo T>=1024,

    4(T+1)61^T <= 62^T,

por el cálculo entero inicial en T=1024 y la inducción
`61(T+2)<=62(T+1)` para T>=60. Por tanto su coste es <=1/(4Q).
Este paso aritmético está certificado en `ParametrosVentana.lean`;
el archivo de producto certifica la cota probabilística finita previa.

El [control de W](formal/Resto.lean) cuesta <=1/(4Q) para el R
indicado. Partir de H1 en T y restar estos tres eventos malos da

    P(T<tau<=H, |c_tau|<=G) >= 1/(4Q).                   (VH)

La conversión a offset usa `rho^T |c0|/9<=1`, `rho=31/32`, y
`|c_tau|<=3(|Pi_tau*c0/9|+|W_tau|)`. Ambas ventanas usan los mismos
bits originales; la resta no exige independencia de los eventos.
VH está certificada conjuntamente en
[ParametrosVentana.lean](formal/ParametrosVentana.lean), incluyendo
su versión uniforme para |c|<=|C| con parámetros fijados por C.
[Evento, prueba y validación](Ventana_conjunta.md).

Se conserva `T=O(log(2+|c0|))` y `H=O(T^2 log T)`, mientras
`G=O(T^6 log^2 T)`. Hormigas exige como máximo
`D=16(ceil(log2(G+2))+1)^2=O(log^2 T)` bits adicionales.
El piso de éxito es `2^-D/(4Q)`, todavía subpolinómico en |c0|.

## 4. Cota candidata CF_H

Conservar de CF, para m>=10,

    N=2^m, h=N^6, C_m=9h^4,
    r=24m+4, d=N^4(10m+3), B=(24m+5)(48m+7).

Aplicar los parámetros anteriores a c0=C_m, obteniendo T_m,H_m,Q_m,G_m.
Entonces `T_m=768m+128` y `Q_m=T_m+1`. Definir

    D_m=16(ceil(log2(G_m+2))+1)^2,
    p_m=2^(-D_m)/(4Q_m),
    J_m=floor((N−1)/(D_m+2)).

La cota candidata es

    P(sigma>h) <= 3/N+66/h+1/(4h^3)+(1-p_m)^J_m.         (CF_H)

Para las primeras N excursiones, H3 con n=N^4, L=N^2, a=4m+2
y s=6m da un coste <=`2/N^2+1/N^2=3/N^2` por excursión.
Su unión conserva el término 3/N. Los presupuestos de frontera,
porciones incompletas del reloj, guardias conocidas al inicio y
conteo de ensayos son los de CF; no se modifican sus justificaciones.
La ventana VH cambia únicamente los parámetros del riesgo.

Los parámetros son monótonos en |c0|, por lo que el piso p_m vale
para todo arranque admitido con |c0|<=C_m. Como
`D_m=O(log^2 m)` y `Q_m=O(m)`, se mantiene `J_m*p_m→infinito`.
Si CF_H se valida íntegramente, su lado derecho tiende a cero y el
puente de cilindros daría phi=1. Esa conclusión **no se declara probada**.

Los parámetros `b=ceil(log2(4Q_m))`, `ell=ceil(log2(D_m+2))`,
`z=m−ell−1−D_m−b` conservan la forma de CF2. En m=1.000.000:
`D=817216`, `b=32`, `ell=20`, `z=182731`. Es aritmética de parámetros,
no un censo ni una simulación de ese horizonte.

## 5. Evidencia y siguiente obligación

[Verificador independiente](verificar_armonica.py): 8 semillas de ambos
signos, cero y potencias; horizontes 0..10, techos 1,2,3,5,9, y 4.840
comparaciones de colas. Reconstruye dos enteros positivos y aplica T.
Comprueba conservación de la altura, balance de energía, H1 y H2.
[Salida exacta y parámetros](evidencia_armonica.json).

Los dos módulos nuevos imprimen 18 consultas de axiomas, sin `sorryAx`.
[Compilación, versiones y hashes](evidencia_supervivencia_banda.json).
La cota universal procede de Lean; los árboles pequeños son un
contraste independiente de la interpretación y la implementación.

M6 y H3 se añaden con los certificados de rachas y umbrales:
[evidencia Lean](evidencia_reloj_lean.json) y
[contraste exacto](evidencia_reloj_exacto.json).

La [ventana conjunta](Ventana_conjunta.md) descarga ahora la resta de
eventos y todas las condiciones de los parámetros, sin independencia
entre los cruces. [Compilación](evidencia_ventana_lean.json).

El [ensayo finito](Ensayo_finito.md) enlaza VH uniforme con Hormigas.
Su variante global CF_F usa bloques de H+D pasos y cambia explícitamente
el número de ensayos. Siguiente: formalizar ese protocolo guardado.
Sigue pendiente el transporte
formal a clases de enteros y el cotejo del artículo primario de Gao.
El P2 original de ventana constante bajo condicionamiento no se ha cerrado.
