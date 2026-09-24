# Gao, 24-09-2026 — aritmética de parámetros de CF_F

Sesión corta sobre la primera obligación de `ESTADO_INVESTIGACION.md`.
No se demuestra la cota pendiente. Lo que hay:

- [Cigarras.md](Cigarras.md): las identidades declaradas en
  `Ventana_armonica.md` §4 se confirman exactamente desde las definiciones
  de §3, y el término `3/N` sale exacto como fracción; pero el número de
  ensayos `J_F` es **cero** para todo `m <= 45`. La desigualdad pendiente
  es sustantiva en cualquier `m`; lo que queda vacío con `m=10` es el
  ensamblaje que la usa, cuyo segundo sumando `(1-p_m)^(J_F)` vale 1.
  Umbrales calculados:
  `m>=19` (CF_H con un ensayo), `m>=46` (CF_F con un ensayo),
  `m>=802923` (término de ensayos por debajo de 1).
- [parametros_cff.py](parametros_cff.py) y su
  [salida](parametros_cff_salida.txt): enteros exactos y `Fraction`.

Consecuencia práctica: al formalizar, llevar la hipótesis correcta. Una
prueba en Lean con `m>=10` compila y no dice nada.
