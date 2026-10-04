# Ocelotas: criba que conserva un suelo de la trayectoria

03-10-2026. **Prueba universal y especialización entera aceptadas en Lean.**
Se mejora una cota auxiliar para los pasos impares. No se usa LMN ni
un censo externo. No es un cierre nuevo de CST ni una prueba de llegada
a 1. Revisión humana y prioridad histórica pendientes.

## Enunciado y dominio

Se usa T(n)=n/2 si n es par y (3n+1)/2 si es impar. Una palabra real
de r bloques contiene a_i>=1 entradas impares seguidas de b_i>=1 pares,
con índices i=0,...,r-1. A_i cuenta las entradas impares de los primeros
i bloques y x_i es el valor al comenzar el bloque i.

Supóngase x_i>=N para i<r, alfa>=3/2, beta>=2, gamma<=1,
log(3)<=alfa log(2), n+1<=s, log(s)<=beta log(2) y

```text
gamma log(2) <= log(2N+1) - log(N+1).
```

La recurrencia

```text
C_0 = 0,
C_(j+1) = floor(beta + alfa C_j - gamma j)
```

da A_r<=C_R para r<=R. Se formalizaron su monotonía y C_j>=2j.
Si gamma>=0, esta cota nunca supera la criba original que omitía
el término `-gamma*j`.

Para una palabra que termina en el primer cruce finito, todos sus
comienzos anteriores al cruce son >=n. Por ello basta N<=n.
**No se exige x_r>=N ni que falle CST.** Esta distinción evita usar
como premisa la conclusión que se intenta investigar. No hay ley
probabilística.

## Derivación independiente

En un bloque, sean x su comienzo, z el valor tras las a entradas
impares e y el valor tras las b pares. Se tienen

```text
2^a (z+1)=3^a (x+1),       z=2^b y>=2y.
```

Cuando y>=N, la identidad

```text
(N+1)(2y+1) - (2N+1)(y+1) = y-N
```

permite conservar la reducción de la parte par:

```text
(2N+1) 2^a (y+1) <= (N+1) 3^a (x+1).
```

Al encadenar hasta el comienzo del bloque i y usar
2^a_i | x_i+1, resulta

```text
(2N+1)^i 2^(A_(i+1)) <= (n+1)(N+1)^i 3^A_i.
```

Los logaritmos producen A_(i+1)<=beta+alfa A_i-gamma*i.
Tomar pisos e iterar prueba la cota. Para el último bloque sólo se
usa su comienzo, de modo que no hace falta acotar su valor final.

## Especialización numérica

[OcelotasSueloNumerica.lean](OcelotasSueloNumerica.lean) certifica

```text
2^4095 * 4096^4096 <= 8191^4096,
```

y con ella gamma=4095/4096 para N=4095. Con alfa=317/200 y beta=B/256,
B>=512, la recurrencia equivale exactamente a

```text
C(B,0)=0,
C(B,j+1)=(400B+162304 C(B,j)-102375j) div 102400.
```

Lean demuestra que el numerador no se trunca indebidamente por la
resta natural. `criba_desde_potencia` aplica esta recurrencia a una
palabra con primer cruce finito, n>=4095, n+1<=s y s^256<=2^B.

## Evidencia

- [Identidades y paso logarítmico](OcelotasSueloRachas.lean).
- [Recurrencia y enlace con el primer cruce](OcelotasSueloCriba.lean).
- [Auditoría de los dos módulos](evidencia_suelo_criba.json): diez
  consultas de axiomas estándar.
- [Auditoría con especialización](evidencia_suelo_numerica.json):
  tres módulos, dos reutilizados y uno compilado; 14 consultas estándar,
  sin `sorryAx`, en Lean 4.32.2. Fuentes y objetos cotejados por el auditor.
- [Contraste independiente](cotejo_suelo_rachas.json), mediante
  [órbitas directas y `Fraction`](cotejar_suelo_rachas.py): 30721 semillas
  impares de 4095 a 65535, hasta ocho bloques; 133694 bloques y 534231
  pasos T, sin discrepancias. Incluye 26005 bloques finales por debajo
  del suelo y comprueba los bordes N-1, N y N+1 de la desigualdad local.
- Se conserva el [primer intento de compilación](intento_suelo_rachas_01.txt),
  fallido por el nombre de un lema auxiliar; no es evidencia aceptada.

## Límite y reproducción

La [continuación tras cortes](SUELO_CORTES_LEAN.md) ya certifica la
aplicación desde un punto intermedio, su verificador por residuos y un
piloto concreto en Lean. Permite pares iniciales y no exige un primer
cruce propio del sufijo. Falta trasladar los certificados con testigos
a ventanas grandes; el piloto no constituye un cierre nuevo de CST.

```text
python -B -X utf8 depuracion/cst20260930/cotejar_suelo_rachas.py --suelo 4095 --max-semilla 65535 --max-rachas 8 --salida depuracion/cst20260930/cotejo_suelo_rachas.json
python -B -X utf8 depuracion/cst20260930/comprobar_extension_persistente.py --modulo OcelotasSueloNumerica --compilados-base C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --compilados-extension C:/Users/Home/AppData/Local/Temp/ocelotas_descuento_20261003 --salida depuracion/cst20260930/evidencia_suelo_numerica.json
```
