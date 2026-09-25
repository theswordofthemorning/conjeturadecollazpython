# Hormigas y Gacelas: ensayo finito certificado

20-09-2026. Se certifica el riesgo de absorción de un ensayo local.
La variante global CF_F desarrollada abajo **sigue candidata**.
*25-09-2026: CF_F quedó demostrada en Lean; ver [Lagartijas](Lagartijas.md).*
Conserva el objetivo phi=1 y los presupuestos de CF_H; cambia la
duración de los ensayos y, por ello, cuántos se pueden contar.

## 1. Palabra universal de Hormigas

Para la transición entera original del mapa atajo, todo estado `(1,c)`,
c entero firmado, admite una palabra de fusión de longitud como máximo

    D(c)=16(ceil(log2(2+|c|))+1)^2.

[Hormigas.lean](formal/Hormigas.lean), `palabra_hormigas`, prueba la
existencia y la cota sobre `CadenaCompletaGao.paso`, no sobre una
relación abstracta de accesibilidad. Su derivación conserva los signos:

- Si c no es cero, bits 0 dividen el offset par hasta hacerlo impar.
  Bajo `|c|<2^m` se necesitan a lo sumo m divisiones. Un bit 1 fusiona
  si el offset es 1 o llega a un gap positivo no mayor que |c|.
  Desde c=0, la palabra 11001 fusiona en cinco pasos.
- Para un gap g>=1, un viaje llega a fusión o a un gap positivo d
  con `6d<=5g`. Si `g<2^m`, consume a lo sumo m+3 bits. Un gap par
  se divide por dos; uno impar usa vuelco, divisiones del offset
  negativo y descenso. El gap 1 usa 001.
- Cuatro viajes dan `6^4 d<=5^4 g`. Como `2*5^4<6^4`, llevan de
  `g<2^(m+1)` a `d<2^m`, salvo absorción anterior. La inducción da
  la cota de frontera `4m(m+3)+3`, suficiente para D(c).

Esto certifica la constante 16. La antigua constante 2,5 refutada
no se reutiliza.

## 2. Relevo de salida a fusión

Cada palabra de longitud d tiene peso `2^-d` bajo los bits justos
originales. La fusión es absorbente, por lo que una palabra que fusiona
en d<=D garantiza probabilidad al menos `2^-D` de fusión en cualquier
horizonte mayor o igual que D. `EnsayoGao.palabra_piso_uniforme`
formaliza también ese margen de tiempo.

Sea `premio_G` el indicador de un estado `(1,d)` con |d|<=G. La
excursión detenida conserva en su extremo el primer offset de salida.
`EnsayoGao.relevo` prueba, por inducción sobre H,

    P_z(fusion antes de H+D)
        >= 2^-D E_z[premio_G(excursion detenida en H)],

si `D>=16(ceil(log2(G+2))+1)^2`. En una rama todavía interior se
promedian los dos hijos; en una rama ya salida se aplica la palabra
con al menos D bits restantes. No se necesita sustituir un tiempo
determinista por una parada aleatoria ni condicionar bits futuros.

El evento de [VH uniforme](Ventana_conjunta.md) está contenido en
ese premio. Con los parámetros T,Q,H,G fijados por C y
`D=16(ceil(log2(G+2))+1)^2`, resulta para todo |c|<=|C|:

    P_(2,c)(sigma<=H+D) >= 2^-D/(4Q).                  (EF)

Aquí sigma es fusión, mientras tau en VH era sólo llegada a k=1.
El tiempo cuenta pasos físicos del mapa atajo. EF es el teorema
`EnsayoGao.ensayo_uniforme` en [Ensayo.lean](formal/Ensayo.lean).

## 3. Variante global CF_F, aún candidata

Usar los N,h,C_m,T_m,Q_m,H_m,G_m,D_m,p_m de
[CF_H](Ventana_armonica.md). Fijar

    W_m=H_m+D_m,
    J_F=floor((N-1)/(W_m+2)).

Empezar en una entrada de k=1 a k=2. Admitir un ensayo sólo si sigue
vivo, el offset cumple |c|<=C_m y quedan al menos W_m pasos antes del
horizonte global h. Las guardias son conocidas al inicio. Observar
W_m bits o la absorción; después buscar la primera entrada nueva admisible
estrictamente posterior al final del bloque. La búsqueda se trunca
en h: si no hay entrada, no se admite otro ensayo.

EF da piso p_m para cada ensayo admitido, condicionado sólo a su
prefijo de inicio. La probabilidad de j ensayos admitidos y fallidos
debería quedar acotada por `(1-p_m)^j` mediante inducción en el árbol
finito. No se afirma ese piso condicionado al evento bueno global E_m.

Cada bloque de W_m pasos omite a lo sumo W_m entradas. La búsqueda
posterior añade como máximo una; conservar W_m+2 como margen da
`I_(j+1)<=I_j+W_m+2`. En E_m y no absorción hasta h, C5 de CF_H
proporciona N entradas antes de h y offsets acotados por C_m.
Para j<=J_F se tiene `I_j+W_m+2<=N`. Las entradas ocurren en pasos
enteros distintos, luego

    S_N-S_(I_j) >= N-I_j >= W_m+2.

Por tanto el bloque cabe antes de S_N y su guardia temporal se cumple.
Esto propone la inclusión en el evento de J_F fallos admitidos y

    P(sigma>h) <= 3/N+66/h+1/(4h^3)+(1-p_m)^J_F.        (CF_F)

La sustitución de J_m por J_F es explícita: EF no certifica por sí
sola el protocolo de duración variable de CF_H. En esta variante,
W_m=O(m^2 log m), D_m=O(log^2 m), Q_m=O(m); por ello J_F*p_m
tendería a infinito y se conserva la ruta hacia phi=1.

Como comprobación aritmética, en m=1.000.000 se obtiene
`W_m=41372628554613904083520`, `ceil(log2(W_m+2))=76` y
`z_F=m-76-1-D_m-ceil(log2(4Q_m))=182675`. No es una enumeración
de ese horizonte ni una prueba del ensamblaje global.

## 4. Evidencia y siguiente obligación

Los dos módulos añaden 12 consultas de axiomas sin `sorryAx`:
[compilación y hashes](evidencia_ensayo_lean.json).
[verificar_ensayo.py](verificar_ensayo.py) usa reconstrucción por pares
positivos: pasaron 8.221 viajes, 2.063 bloques de cuatro viajes y
4.127 offsets, incluyendo magnitudes de unos 512 bits. El relevo se
contrastó en 147 casos con palabras explícitas de cinco bits para
los pequeños radios utilizados. No se simuló el enorme horizonte EF.
[Salida exacta](evidencia_ensayo_exacto.json).

Próximo: formalizar las guardias, búsqueda y conteo de ensayos de CF_F;
conectar el evento bueno y el reloj global con ese protocolo finito.
Después quedan el límite y el transporte a clases residuales. Gao
continúa sin resolverse; falta además cotejar el artículo primario.
