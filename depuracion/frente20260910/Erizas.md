# Obstruccion de las Erizas

10-09-2026. Concentracion entera y limite de la contraccion multiescala.
Nombre local; no se reclama novedad bibliografica de las herramientas.

## Resultado y estado de verificacion

**Continuacion:** [Mangostas](Mangostas.md) controla directamente la
duracion compartida mediante valuacion truncada, sin restaurar el
objetivo L2 descartado aqui. Ver esa nota para el frente vigente.

Para CADA semilla entera fija c0, la excursion iniciada en (2,c0), con
bits justos y salida al llegar a k=1, NO admite constantes

    0 <= rho < 1/2, T < infinito,
    e_{t+1}(m) <= rho e_t(m+1) para TODO t>=T y TODO m>=1.       (E0)

T y rho pueden depender de c0: tampoco asi existe (E0). Es una obstruccion
para las leyes ALCANZABLES, no otro testigo sintetico. Tambien excluye
bloques fijos L con factor uniforme theta < 2^(-L) en todas las escalas.

**Estado:** demostracion general escrita abajo; nueve ingredientes
algebraicos en Lean 4.32.2, sin `sorryAx`; controles Python exactos.
NO hay formalizacion integral: Lean toma las recurrencias de momentos
como hipotesis; su enlace con la cadena, las desigualdades de colas,
Cauchy y el paso asintotico se justifican aqui, no dentro de Lean.
Sin revision adversarial externa. No se declara cerrado un registro de
auditoria en `depuracion/veredictos.jsonl`.

## 1. Altura con salida absorbente

Trabajar con la probabilidad ORIGINAL de las palabras de bits, antes de
condicionar. Sea X_t=k_t-1 mientras vive y X_t=0 despues de salir. Sea
S_t=P(vive en t). Empezamos en X_0=1. En un paso:

- Si c es par, las dos ramas conservan X.
- Si c es impar, las alturas son X+1 y X-1, equiprobables. Para X=1,
  la segunda rama sale y vale cero, exactamente como exige la formula.
- Despues de salir, X permanece cero.

Por tanto, sin suponer independencia de la paridad de c y la altura,

    E X_t = 1,
    E X_t^2 <= t+1,
    E X_t^4 <= 3t^2+4t+1 = (t+1)(3t+1).                       (E1)

La segunda cota suma incrementos de a lo mas 1. La cuarta usa

    [(x+1)^4+(x-1)^4]/2 = x^4+6x^2+1

y suma 6(j+1)+1 para j=0..t-1. En los pasos inmoviles y absorbidos
estos incrementos se sustituyen por cero, por lo que las cotas siguen
siendo validas. Tambien X_t<=t+1 sobre las palabras vivas. Luego

    1 = E X_t <= (t+1) S_t,     S_t >= 1/(t+1).               (E2)

No se usa una estimacion difusiva, ni un teorema previo del laboratorio.

## 2. Tamano de la coordenada normalizada

Sea U_t=|c_t|/3^k_t si vive, y cero si salio. Es importante mantener
esa convencion: las esperanzas de esta seccion NO son condicionadas.
Escribir u=c/3^k con signo. Las dos ramas normalizadas son

    c par:   u/2,                 (3u-1+3^(-k))/2;
    c impar: u/2+1/(2*3^(k+1)),   (3u-1)/2.

En k=2 se elimina la segunda rama impar. Eliminar su valor absoluto
solo reduce la esperanza. La desigualdad triangular da

    E[U_{t+1} | estado vivo] <= |u|+1/2,
    E U_t <= |c0|/9+t/2.                                      (E3)

En la fila par basta incluso 1/4; en la impar el termino aditivo es
(1+3^(-k-1))/4 <= 1/2. No se necesita un momento fraccionario uniforme.

## 3. Una caja de cardinalidad subexponencial

Definir los ENTEROS

    h_t = techo( [4(t+1)^2(3t+1)]^(1/4) ),
    J_t = 4(t+1)(|c0|+t+1),
    L_t = J_t * 3^(h_t+1),
    D_t = h_t * (2 L_t+1).

Por (E1), (E2) y Markov, condicionando ahora a sobrevivir,

    P(X_t>h_t | vive) <= E X_t^4 / (S_t h_t^4) <= 1/4.

Por (E2), (E3) y Markov,

    P(U_t>J_t | vive) <= E U_t / (S_t J_t) <= 1/4.

Asi, al menos la mitad de la ley condicionada cumple simultaneamente
X_t<=h_t y U_t<=J_t. Esta parte esta dentro de la caja entera

    2 <= k <= h_t+1,     |c| <= L_t,

que tiene D_t estados. No se supone independencia entre X_t y U_t.
Para c0 fijo, h_t=O(t^(3/4)), J_t=O_c0((t+1)^2), y por tanto

    log D_t = O_c0(t^(3/4)+log(t+2)) = o(t).                  (E4)

Las cotas son deliberadamente holgadas. El exponente 3/4 es suficiente,
no se afirma que sea la escala verdadera de la excursion.

## 4. Colision entera: tasa exponencial cero

Sea p_t(k,c) la ley CONDICIONADA a vivir y P_t(k)=sum_c p_t(k,c).
Definir, omitiendo las fibras vacias,

    A_t = sum_k sum_c p_t(k,c)^2 / P_t(k).

Como P_t(k)<=1, A_t >= sum_{k,c} p_t(k,c)^2. Cauchy aplicado a la
mitad de masa dentro de la caja entrega

    1 >= A_t >= 1/(4D_t) > 0.                                (E5)

La cota superior usa que la colision de cada ley condicional es <=1.
De (E4), (E5) se sigue

    lim_{t -> infinito} (A_t)^(1/t) = 1.                      (E6)

Esto NO afirma que A_t tenga limite positivo, ni que A_{t+1}/A_t tenga
limite. Puede decaer; lo que se excluye es una cota geometrica de razon
fija menor que uno para todos los tiempos suficientemente grandes.

Reducir modulo 2^m solo agrega colisiones, asi que tambien, para toda m,

    e_t(m)+1 >= 2^m A_t >= 2^m/(4D_t).                       (E7)

En particular, para m>=alpha*t con alpha>0 fijo, e_t(m) crece sin cota.
Esto NO impide equidistribucion a una escala m FIJA al crecer t.

La obstruccion tambien alcanza al C2 MARGINAL de c, no solo al
condicional por altura. La misma caja deja al menos media masa marginal
en los 2L_t+1 enteros de [-L_t,L_t]. Cauchy y reduccion modular dan

    C2_marginal,t(m) >= 2^m/[4(2L_t+1)].                     (E8)

Por tanto, para cualquier alpha>0 y c0 fijo, no existe una cota constante
de C2 en TODO el rango 1<=m<=alpha*t: elegir m=piso(alpha*t) contradice
(E8) al crecer t. Esto afecta al control L2 uniforme que se pretendia
obtener en el "wedge" de P2-a en `notaensamblajep2.txt`. No refuta por
si mismo las cotas de probabilidad de las CLASES ESPECIALES de racha:
una ley concentrada puede asignar poca masa a esas clases concretas.

## 5. Por que cae la contraccion uniforme

Cada tiempo finito tiene soporte entero finito. A escala suficientemente
grande para separar los c de cada fibra, exactamente

    e_t(m) = 2^m A_t-1.

Si (E0) fuera cierta, fijar t y hacer crecer m, separando ambos soportes,
daria

    2^m A_{t+1}-1 <= rho (2^(m+1) A_t-1),
    A_{t+1} <= 2 rho A_t.

El limite aqui es SOLO de escala, con t fijo. Iterar desde T entregaria
A_{T+n} <= (2rho)^n A_T, contradiciendo (E6). Para rho=0 contradice
directamente A_{T+1}>0. Para bloques L el mismo argumento da
A_{t+L} <= 2^L theta A_t y contradice (E6) sobre la subsecuencia T+nL.

Equivalente en cuantificadores: para cualquier rho<1/2 no negativo y
cualquier T, existen t>=T y una escala FINITA m>=1 que violan (E0).
No se afirma que el cociente cruce 1/2: puede quedar debajo y perder
todo margen uniforme. Tampoco basta elegir un tiempo inicial mayor.

## Controles reproducibles

```powershell
python depuracion/frente20260910/obstruccion.py
python depuracion/frente20260910/obstruccion.py --pasos 28 --semillas 1
lean +v4.32.2 depuracion/frente20260910/obstruccion.lean
```

Python reutiliza el DP de `contraccion.py`: NO es revision ciega.
Compara con pares reales en 5.680 pasos, verifica 858 estados locales
(incluye c negativos, cero y la salida k=2), 10.000 raices cuartas
enteras y las 256 palabras de longitud 8 por arranque.

El barrido inicial controla 126 leyes: seis semillas, t=0..20.
El adicional controla 29 leyes para c0=1, t=0..28, con 590.042 estados
en el ultimo tiempo. Son ventanas superpuestas. Se comprueban momentos,
supervivencia, masa de la caja, colision y la formula modular inyectiva.
Los resultados estan en `obstruccion_salida.txt`,
`obstruccion_ampliada.txt` y `obstruccion_lean.txt`.

Para c0=1, el limite en escala del cociente pasa de aproximadamente
0,450422 (paso 19->20) a 0,469286 (27->28). Son decimales de fracciones
exactas, NO una demostracion de convergencia a 1/2; (E1)-(E6) son el
argumento general. Ningun barrido fue dejado ejecutandose.

## Consecuencia para la ruta y revision pendiente

Se retira la busqueda de un margen uniforme H>=epsilon(1-s)E para
todas las escalas de Castoras: (E0) es imposible en ese dominio. El
balance de Castoras y la rigidez de Suricatas permanecen validos.

Siguiente tarea: estimar directamente la masa de las clases especiales
de racha/recarga identificadas por `lecturaracha.lean`, sin exigir L2
uniforme de TODAS las clases en un wedge lineal. Otra posibilidad es
control a escalas sublineales y una estimacion separada del resto; una
tercera es un funcional que reste un piso entero justificado. Ninguna
alternativa queda probada aqui. No basta restringir el viejo objetivo
a 1<=m<=alpha*t: (E8) tambien descarta ese control L2 uniforme.
No hay nueva cota de densidad, ni prueba de P2 o de Collatz.

Para revision adversarial posterior: atacar la convencion absorbente
de X y U, el cambio entre expectativas originales y condicionadas,
el signo en las cuatro formulas de u, los factores S_t y 4, la
cardinalidad de la caja, Cauchy con los pesos P_t(k), y el orden de los
cuantificadores t/m. Formalizar el enlace general que Lean aun no cubre.
