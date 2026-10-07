# Estado para continuar — 05-10-2026

[Premisa del usuario](PREMISA_DE_INVESTIGACION.md): interpreta los resultados
acumulados como evidencia de que Collatz es verdadero y busca cerrar la
prueba universal. Esta conclusión de trabajo orienta la búsqueda, sin
servir como hipótesis de prueba.

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal; de ella la de Garner (1985) sobre rachas y la conjetura 2 de Wu
(1992). CST: Ocelotas hasta veinticuatro rachas, bajo
Laurent–Mignotte–Nesterenko. Ruta B, sin hipótesis externas: Terras (1976),
Korec (1994), el retrato del fugitivo y una potencia `N^0,969` para los
candidatos a menor contraejemplo.**

- **Gao.** `GaoEnunciado.conjetura_gao`
  ([Tejonas](depuracion/gao20260920/Tejonas.md)): con el mapa clásico, los n
  con `f^k(n)=f^k(n+1)` para algún `k<=log2 n` tienen densidad natural 1.
  Forma literal, `d̄_k -> 1` y `d(x) -> 1`: `GaoLiteral.conjetura_gao_literal`
  ([Hienas](depuracion/gao20260920/Hienas.md)). Ritmo muy lento:
  [Cigarras](depuracion/gao20260924/Cigarras.md).
- **Garner (1985).** `GarnerEnunciado.conjetura_garner`
  ([Alpacas](depuracion/garner20260926/Alpacas.md)): L+1 consecutivos, tan
  grandes como se quiera, con igual altura e igual tiempo total de parada.
- **Wu (1992).** `WuEnunciado` ([Condoras](depuracion/gao20260920/formal/Condoras.lean)):
  `lim L=∞`. La conjetura 1 equivale, dado Gao, a que casi todo n llegue a 1:
  sigue abierta. Citas leídas con la IA de CNKI; falta cotejar el original.
- **Ocelotas.** [Veinticuatro rachas en Lean](depuracion/cst20260930/VEINTICUATRO_LEAN.md):
  primer descenso = primer cruce bajo el corolario especializado de LMN
  (1995), original cotejado ([lecturas](depuracion/cst20260930/LECTURAS_20261003.md)).
  Un fallo exige **al menos 25 rachas**; el
  [cierre de 77](depuracion/cst20260930/SETENTA_Y_SIETE_LEAN.md) exige 78
  con LMN y Rozier–Terracol como hipótesis externas.

Sólo axiomas estándar en los módulos Lean. **Revisión humana pendiente.**
Salvo en las rachas construidas, nada afirma la llegada a 1.

## Revisión y publicación

[Pendientes](gaopendientes.md): revisión humana de Gao, Hienas, Garner y
Wu. Lean certifica el enunciado, no su interpretación. La
[revisión del 27-09](papers/revision20260927/REVISION.md#4-novedad) no halló
pruebas publicadas; faltan MathSciNet, Scholar y el original de Garner.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **Artículos.** [Tres `.tex`](papers/README.md), [Zenodo](papers/zenodo/LEEME.md).
  AFM rechazó los tres el 28-09 ([correos](papers/CORREOS_20261004.md)); I
  sigue en revisión técnica de [JAR](papers/jar/LEEME.md), sin noticias al
  04-10. Borrador del [IV, Ocelotas](papers/articulo_IV_ocelotas.tex), sin
  enviar. [Qeios](papers/qeios/LEEME.md): retiro confirmado.
  [Palomar](papers/palomar/LEEME.md): Gao en verificación, CI verde.
  [Zulip](papers/qeios/ZULIP_borrador.md): anuncio borrado (escrito con IA).
- **OEIS.** Aprobadas [A078441](depuracion/oeis20260917/A078441_20260930_aprobada.txt)
  y [A400486](depuracion/oeis20260917/A400486_20261004_aprobada.txt); no
  validan pruebas. A400487 sigue pendiente; si se rechaza, retirar su
  referencia en A078441 ([seguimiento](papers/oeis/RESPUESTA_20260928.md)).

## Ruta vigente y próximo bloque

Cerrados o condicionales: [Nashida](depuracion/nashida20260928/LEEME.md),
[Pandas](depuracion/pandas20260930/LEEME.md),
[Wirsching](depuracion/wirsching20260930/LEEME.md) y las
[herramientas de Ocelotas](depuracion/cst20260930/LEEME.md).

Ruta B, elegida por el usuario el 04-10
([plano de la casa](depuracion/casa20261004/LEEME.md)): Collatz equivale a
los dos muros, en Lean. Sin fuerza bruta: no se amplía a 25 rachas.
[Corzas](depuracion/casa20261004/CORZAS.md): retrato del fugitivo (órbita
no acotada, patrón nunca periódico, `≡ 3 mod 4`), densidad cero y
distribución límite de σ (Terras).
[Chinchillas](depuracion/casa20261004/CHINCHILLAS.md), 05-10: Korec
(casi todo n baja por debajo de `n^c` si `c > log 3/log 4`, barrera
2-ádica); bajo N, menos de `14,5 N^0,969` números nunca bajan (ahí estaría
el menor contraejemplo) y otros tantos fallan en CST. Bajo la forma
entera de LMN, una falla de CST `n ≥ 2^125000` cruza después de
`log₂ n + 1` pasos y el exponente baja a 0,95, la barrera del conteo.
[Perdices](depuracion/casa20261004/PERDICES.md): identidad afín
`T^k(r + 2^k t) = T^k(r) + 3^S t` en Lean; la mezcla fina de Tao (2019),
que salta la barrera, queda medida hasta `3^14`, sin prueba. Pasos 3 y 4
delimitados: lo que falta equivale a la periodicidad de Lagarias (muro B)
y a CST (muro A), abiertas. Siguiente: la ley exacta de `T^k(r) mod 3^m`
como cadena de Markov, en Lean.

## Evidencia y conservación

Lean 4.32.2, Mathlib fijado. Gao: reconstrucción del 26-09 y
`leanchecker` de 28 módulos
([evidencia](depuracion/gao20260920/evidencia_gao_lean.json),
[reproducción](depuracion/gao20260920/formal/README.md)). Casa: los diez
módulos de la ruta B desde las fuentes, sin cachés, 98 consultas
([evidencia](depuracion/casa20261004/evidencia_fugitivo.json)). Los
cálculos finitos no sustituyen las pruebas universales.

Registro: 280 afirmaciones: 174 demostradas, 87 medidas, 12 conjeturadas
y siete refutadas
([fuente versionada](depuracion/coherencia20260913/registro.json) y
`guardarafirmaciones.py`). No reconstruir conversaciones ni alterar
históricos. zootheorem permanece intacto.
