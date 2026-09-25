# Martas: el lado derecho de CF_F tiende a cero

25-09-2026. **Demostrado en Lean** ([Martas.lean](formal/Martas.lean), 7
consultas de axiomas, sólo `propext`, `Classical.choice`, `Quot.sound`).

## Enunciado

Cadena absorbente original desde `(0,1)`, bits iid justos:

    para todo eps>0 existe h0 tal que P(sigma>h)<=eps para todo h>=h0.   (martas)

Es decir, la fusión es casi segura; en el lenguaje de
[Cilindros](Cilindros.md), `P(absorción eventual)=1`.

## Prueba

1. **Parámetros por potencias de dos.** Con `T=tiempo(C_m)<=1024m` y
   `L=floor(log2 T)`: `cantidad T<=2^(2L+10)`, `umbral<=2L+12`,
   `margen<=6L+33`, `horizonte<=2^(3L+16)`, `duracion_palabra<=16(8L+53)^2`
   y `W+2<=2^(3L+17)` (`duracion_cota`, `tiempo_cota`).
2. **Ensayos.** `J_F=floor((2^m-1)/(W+2))>=2^(m-3L-18)` y
   `p>=2^-(16(8L+53)^2+L+3)`. Si
   `m>=K+4l+62+16(8l+133)^2` con `l=floor(log2 m)`, entonces `J_F*p>=2^K`
   (`ensayos_grandes`).
3. **Cola.** `(1-p)^J<=1/(1+J*p)` por Bernoulli, luego
   `(1-p_m)^(J_F)<=2^-K` (`cola_ensayos`).
4. **Existencia de m.** Con `m=2^max(22,K+2)` la condición anterior se
   cumple, porque `2(4l+62+16(8l+133)^2)<=2^l` desde l=22 (`polilog`,
   `existe_m`).
5. **Monotonía y cierre.** `P(fusión hasta h)` crece con h
   (`fusion_monotona`). Con [CF_F](Lagartijas.md) en `h=2^(6m)`, los cuatro
   términos quedan bajo `2^-K` y su suma bajo eps (`martas`).

## Alcance

El ritmo es pésimo: por [Cigarras](../gao20260924/Cigarras.md), `J_F*p_m>1`
sólo desde m=802923. El teorema da el límite, no una velocidad útil. El
paso a clases de enteros y a la conjetura de Gao está en [Tejonas](Tejonas.md).
