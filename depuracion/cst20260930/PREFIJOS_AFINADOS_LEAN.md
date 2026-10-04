# Ocelotas: criba afinada después de un corte, formalizada

03-10-2026. **Lemas universales y verificador booleano comprobados en
Lean**, sin LMN ni Rozier–Terracol como hipótesis. Revisión humana y
prioridad histórica pendientes. La idea procede de combinar la criba
afinada ya existente con la separación de rachas después de un par.

## Contrato matemático

T es el atajo sobre naturales: mitad para n par, `(3n+1)/2` para n impar.
`S_i(n)` cuenta las entradas impares y `r_i=rachas(n,i)` sus bloques
maximales en los primeros i pasos. No hay ley probabilística.

Sean k un primer cruce finito del coeficiente, i<k, y `rachas(n,k)<=R`.
El corte debe ser vacío (`i=0`) o seguir a una entrada par
(`T^(i-1)(n)` par). Si `T^i(n)<=X`, se define:

```text
s = X+1,
B = 0 si s<=1; en otro caso floor(log2(s^256-1))+1,
C(B,0) = 0,
C(B,j+1) = floor((25B+10144*C(B,j))/6400).
```

Entonces

```text
S_k(n) <= S_i(n) + C(B, R-r_i).
```

Así, `S_i(n)+C(B,R-r_i)<q_min` excluye cualquier fallo del intervalo
que además requiera `S_k(n)>=q_min`. El verificador aprovecha esa
exclusión para terminar un subárbol sin enumerar sus semillas.

## Por qué es válida

[OcelotasPrefijosAfinados.lean](OcelotasPrefijosAfinados.lean) demuestra:

1. **`cota_real`.** La recurrencia entera coincide exactamente con la
   criba real existente para alfa=317/200 y beta=B/256. El piso de una
   división real de naturales coincide con la división natural.
2. **`potencia_exponente`.** `s^256<=2^B`, incluidos s=0 y s=1.
   Para s>=2 se aplica el límite de `Nat.log2` a `s^256-1`.
   Esto garantiza `log s <= (B/256) log 2` cuando s>0.
3. **`criba_contador`.** La criba real admite una palabra vacía y
   entradas pares iniciales. Se eliminan esos pares por inducción;
   cuando la semilla es impar, se extrae su palabra de rachas.
4. **`criba_real_despues_corte`.** Los contadores se suman exactamente
   al cortar después de un par. La última entrada antes del primer
   cruce también es par. Se aplica la criba a la parte restante y se
   usa monotonía respecto del número de rachas disponibles.
5. **`criba_despues_corte`.** Se especializa lo anterior con la cota
   certificada `log 3<=(317/200) log 2` y la elección entera de B.

No se supone que el tramo posterior tenga su propio primer cruce en
k-i. Ese tramo sólo necesita acabar en una entrada par; esta distinción
es necesaria para aplicar correctamente la criba tras un corte.

## Verificador y certificado finito

[OcelotasCribaPrefijosAfinados.lean](OcelotasCribaPrefijosAfinados.lean)
conserva el estado de clases `n=r+m*u`, `T^i(n)=a*u+c`, junto con el
número de impares, rachas y la paridad anterior. Para semillas <=L,
el mayor valor actual de la clase es `X=a*floor((L-r)/m)+c`.

Se aceptan clases vacías, descenso en el cruce, exceso de rachas o la
exclusión anterior. Si ninguna condición sirve, se separa u par/impar.
**Agotar combustible rechaza**. `comprobar_correcto` demuestra la
corrección por inducción; `certificado_descenso` conecta la aceptación
de la raíz con una órbita concreta, incluyendo el extremo inferior.

La [auditoría](evidencia_criba_prefijos_afinados.json) y su
[salida](evidencia_criba_prefijos_afinados.txt) contienen dos módulos
compilados, ocho consultas, axiomas estándar y ningún `sorryAx`.
Lean 4.32.2; prefijo de 27 módulos reutilizado por huellas verificadas.

Para la ventana propuesta de 76 rachas, la variante entera anterior
necesitó 3747781 nodos. La variante afinada propone 11225, con
4910 clases no vacías. El [cotejo independiente](cotejo_prefijos_76_afinados.json)
reconstruye órbitas directas, comprueba otro representante, calcula B
por búsqueda binaria y C con `Fraction`, y verifica cobertura disjunta.
No sustituye la evaluación del certificado en el núcleo ni el
ensamblaje de CST hasta 76. La evidencia previa se conserva.

```text
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasCribaPrefijosAfinados --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_criba_prefijos_afinados.json
python -B -X utf8 depuracion/cst20260930/cotejar_prefijos_afinados.py --certificados depuracion/cst20260930/prefijos_76_afinados_5m.json --salida depuracion/cst20260930/cotejo_prefijos_76_afinados.json
```
