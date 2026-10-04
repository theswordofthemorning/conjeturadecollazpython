# Ocelotas: descontar una entrada impar por racha

03-10-2026. **Cota universal formalizada en Lean.** No requiere LMN
ni un resultado finito externo. Su conexión con el contador y con
cortes de la trayectoria también está formalizada. No constituye un
nuevo cierre de CST; revisión humana y prioridad histórica pendientes.

## Enunciado

Mapa T(n)=n/2 si n es par y (3n+1)/2 si es impar; n>=1.
Una palabra de r bloques completos tiene a_i>=1 entradas impares
seguidas de b_i>=1 entradas pares por bloque. Sea A_i la suma de las
primeras i longitudes impares y D_i=A_i-i. Los índices empiezan en 0.

Para alfa>=1, beta>=1, log(3)<=alfa log(2), n+1<=s y
log(s)<=beta log(2), se define:

```text
C(alfa, gamma, 0) = 0
C(alfa, gamma, j+1) = floor(gamma + alfa C(alfa, gamma, j))
```

Si r<=R, el total de entradas impares cumple

```text
A_r <= R + C(alfa, beta-1, R) <= C(alfa, beta, R).
```

La última desigualdad compara universalmente con la criba anterior;
no se afirma que siempre sea estricta. No hay ley probabilística ni
condicionamiento por primer cruce en este enunciado de bloques completos.
También vale para tramos que empiezan con pares y terminan con un par.

## Derivación independiente

En un bloque, x es la entrada impar inicial, z el valor después de
las a entradas impares e y el valor después de las b entradas pares.
Las identidades exactas son

```text
2^a (z+1) = 3^a (x+1),       z = 2^b y.
```

Como b>=1 e y>=1, se tiene z>=2y y 3(y+1)<=2(z+1). Por tanto,

```text
2^(a-1) (y+1) <= 3^(a-1) (x+1).
```

Al encadenar bloques queda 2^D_i (x_i+1)<=3^D_i (n+1).
La divisibilidad 2^a_i | x_i+1 da
2^(D_(i+1)+1)<=(n+1)3^D_i. Tomar logaritmos y pisos permite iterar
D_(i+1)<=floor(beta-1+alfa D_i). Se recupera A_r=r+D_r.
La positividad se comprueba explícitamente; n=0 queda fuera del dominio.
El ciclo 1,2,1 da igualdad y está incluido.

## Después de un corte

[OcelotasDescuentoContador.lean](OcelotasDescuentoContador.lean) prueba
`criba_desde_potencia`. Sean k un primer cruce finito, i<k, n>0,
r_k<=R y T^i(n)<=X. Se permite i=0 o un corte tras una entrada par.
Para B>=256 y (X+1)^256<=2^B:

```text
S_k <= S_i + (R-r_i) + C_entero(B-256, R-r_i),
C_entero(B,0)=0,
C_entero(B,j+1)=floor((25B+10144 C_entero(B,j))/6400).
```

S cuenta entradas impares y r bloques maximales. El tramo posterior
al corte sólo necesita terminar en par; no se supone que k-i sea su
primer cruce. La demostración usa la aditividad de ambos contadores.

## Evidencia y límites prácticos

- [Teoría de bloques](OcelotasDescuentoRachas.lean): cinco consultas
  de axiomas, [auditoría inicial](evidencia_descuento_rachas.json).
- [Cadena con el contador](evidencia_descuento_contador.json): Lean
  4.32.2, tres módulos compilados y 15 consultas estándar, sin `sorryAx`;
  27 módulos de base reutilizados por huellas. Incluye los dos módulos
  nuevos y la criba afinada previa. Fuentes y consultas cotejadas.
- [Cotejo directo](cotejo_descuento_rachas.json), mediante
  [implementación independiente](cotejar_descuento_rachas.py): 32768
  semillas impares de 1 a 65535 y ocho bloques por semilla, 262144
  bloques y 1029796 pasos T, sin discrepancias. Incluye igualdades y
  recorridos posteriores al descenso. Es un contraste finito.
- En las tablas de 23 y 77 la cota mejora, pero no elimina filas
  adicionales. No se anuncia un cierre mayor por esta desigualdad.
- La [exploración con descuento](prefijos_23_alto_descuento_16m.json)
  cubre la ventana alta de 23 con 10491273 nodos frente a 12368501,
  aproximadamente un 15 % menos, sin pendientes. Su
  [cotejo independiente](cotejo_prefijos_23_alto_descuento.json) terminó
  sin discrepancias: 1861414 hojas no vacías. La medida temporal no es una comparación
  de rendimiento controlada.

## Verificador y piloto aceptados

[OcelotasCribaPrefijosDescuento.lean](OcelotasCribaPrefijosDescuento.lean)
conecta la aceptación con órbitas positivas y primer cruce finito.
[OcelotasPrefijosDescuentoTestigos.lean](OcelotasPrefijosDescuentoTestigos.lean)
permite proponer B y unir ramas; exige X>=1 en la hoja de criba para
garantizar el exponente mínimo también en estados arbitrarios.
[OcelotasCertificadosDescuento.lean](OcelotasCertificadosDescuento.lean)
demuestra que el árbol aceptado implica la aceptación del verificador.
El combustible agotado rechaza.

La [auditoría general](evidencia_certificados_descuento.json) contiene
diez módulos y 39 consultas estándar: dos compilados y ocho reutilizados
en la ejecución final; sin `sorryAx`. El primer fallo por profundidad
de elaboración se [conserva](intento_certificados_descuento_01.txt).

El [piloto de la ventana de 76](prefijos_76_descuento_1m.json) tiene
10027 nodos frente a los 11225 anteriores, y 4366 hojas no vacías;
[cotejo independiente](cotejo_prefijos_76_descuento.json) sin discrepancias.
El [generador separado](generar_testigos_descuento_lean.py) produjo
49 subárboles y 48 uniones en una parte y su ensamblaje.
La [compilación del piloto](evidencia_descuento_piloto_76.json) terminó
con código 0: dos módulos compilados, diez reutilizados y 90 consultas
estándar. Es una aplicación del resultado ya registrado, no otro cierre
de CST ni una verificación del censo externo.

Se conservan los primeros intentos de compilación fallidos:
[bloques](intento_descuento_rachas_01.txt) y
[contador](intento_descuento_contador_01.txt). Son históricos; las
evidencias aceptadas enlazadas arriba corresponden a las fuentes actuales.

## Reproducción y siguiente acción

```text
python -B -X utf8 depuracion/cst20260930/cotejar_descuento_rachas.py --max-semilla 65535 --max-rachas 8 --tablas depuracion/cst20260930/preparacion_veintitres_lean.json depuracion/cst20260930/preparacion_setenta_y_siete.json --salida depuracion/cst20260930/cotejo_descuento_rachas.json
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasDescuentoContador --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_descuento_20261003 --salida depuracion/cst20260930/evidencia_descuento_contador.json
```

El verificador y su piloto están completos. El cierre de 23 sigue la
[ruta de prefijos anterior](VEINTITRES_PROPUESTA.md), ya cotejada.
Se obtuvo además la [cota con suelo](SUELO_RACHAS_LEAN.md), todavía
sin conexión formal con un verificador de árboles.
