# Estado para continuar ? 20-09-2026, cierre del d?a

**Investigaci?n pausada a petici?n del usuario.** Objetivo conservado:
resolver Gao o avanzar hasta donde sea posible. **No se declara resuelta.**
La ruta actual es [CF_F](depuracion/gao20260920/Ensayo_finito.md), basada
en CF_H. Est?n certificados los ingredientes locales, las guardias y el
conteo de ensayos. Falta conectar el reloj global con suficientes entradas
admisibles. [Punto preciso de reinicio](depuracion/gao20260920/Guardias_finitas.md).

## Objeto y ley

`T(x)=x/2` si es par, `(3x+1)/2` si es impar; C es el mapa cl?sico
del CLI. `a(t)` cuenta clases m?dulo `2^t` que fusionan balanceadas
hasta t; `phi=lim a(t)/2^t`. OEIS usa `b(t)=a(t+1)-2a(t)`.
Para F, uni?n de esas clases, `densidad inferior(F)>=phi`; phi=1
implicar?a densidad uno. Igual altura finita exige adem?s convergencia
de la cola y control de primeras llegadas a 1.

Cadena original absorbente, bits iid justos. Estado `{v,3^k*v+c}`;
bit=paridad del ancla, no del menor. En k=0, gap positivo; en torre,
c firmado. `(1,1)` con bit 1 absorbe. Desde `(2,c0)`, tau es primera
llegada a k=1; sigma es fusi?n. Tiempo en pasos f?sicos del mapa atajo.
No sustituir la ley por supervivencia condicionada o cadena rebotada.

## Certificados disponibles

- Momentos y m?ximo de magnitud de la cadena completa; desde `(0,1)`,
  coste del m?ximo hasta h acotado por `66/h`.
- Identidad af?n hasta tau, W prolongado multiplicativamente despu?s;
  producto normalizado y m?ximos. No congelar W ni sustituir tiempo
  determinista por tau dentro de una esperanza.
- Supervivencia inferior `1/(t+1)`, cola de mixtos, rachas enteras y
  [reloj M6/H3](depuracion/gao20260920/Reloj_bloques.md).
- [VH uniforme](depuracion/gao20260920/Ventana_conjunta.md): par?metros
  fijados por C para todos |c|<=|C|, salida buena con piso `1/(4Q)`.
- Hormigas: palabra de fusi?n desde `(1,c)` de longitud
  `<=16(ceil(log2(2+|c|))+1)^2`. La antigua constante 2,5 est? refutada.
- EF: con `D=16(ceil(log2(G+2))+1)^2`, `W=H+D` y `p=2^-D/(4Q)`,
  probabilidad de fusi?n antes de W al menos p, uniforme en el offset.
- Protocolo guardado: j ensayos admitidos y fallidos tienen probabilidad
  `<= (1-p)^j`. Cada bloque consume W bits y borra la marca de entrada
  al reiniciar. La b?squeda admite s?lo entradas nuevas 1->2 con
  |c|<=C y tiempo suficiente; se trunca en h.

## Primera obligaci?n al retomar

`K_C(h)` cuenta entradas admisibles entre 0 y h, incluidos extremos.
`ConteoEnsayos.lean` certifica para todos C,j,h:

    P(sigma>h) <= P(sigma>h y K_C(h)<1+j(W+2)) + (1-p)^j.

El primer t?rmino incluye supervivencia. Pr?ximo: formalizar, con
`N=2^m`, `h=N^6`, `C_m=9h^4`, m>=10,

    P(sigma>h y K_(C_m)(h)<N) <= 3/N+66/h+1/(4h^3).

**Aviso del 24-09-2026 sobre ese `m>=10`:** la desigualdad de arriba es
sustantiva en cualquier `m`, pero el ensamblaje que la usa no. Con los
parámetros declarados `J_F=0` para todo `m<=45`, luego `(1-p_m)^J_F` vale
1 y el ensamblaje no concluye nada. Umbrales exactos:
`m>=19` para que CF_H tenga un ensayo, `m>=46` para CF_F, y `m>=802923`
para que ese término baje de 1. Llevar la hipótesis correcta al
formalizar. Comprobación en [Cigarras](depuracion/gao20260924/Cigarras.md).

Usar el presupuesto del [reloj global](depuracion/gao20260920/Reloj_global.md)
y C5 de [CF_H](depuracion/gao20260920/Ventana_armonica.md): frontera,
porciones incompletas y control de offsets antes de h. Despu?s aplicar
`J_F=floor((N-1)/(W_m+2))`. CF_F sigue candidata; CF_H usaba D_m+2,
no mezclar denominadores. Quedan el l?mite `J_F*p_m -> infinito` y el
transporte a clases, escrito en [Cilindros](depuracion/gao20260920/Cilindros.md).
El P2 antiguo de ventana constante para W sigue abierto.

Falta cotejar Gao primario (1993), cuyo proveedor bloque? el acceso.
La atribuci?n secundaria de Lagarias no sustituye ese cotejo ni prueba
Collatz. No contactar personas ni enviar OEIS/papers sin autorizaci?n.

## Evidencia y conservaci?n

Lean 4.32.2, Mathlib fijado: 157 consultas locales de axiomas en 22
archivos sin `sorryAx`. [Compilaci?n y hashes](depuracion/gao20260920/evidencia_guardias_lean.json).
Contrastes exactos independientes con Fraction; el ?ltimo protocolo
pas? 24.564 casos y 528 comparaciones en una cadena auxiliar, h<=10.
Son controles finitos, no pruebas universales.
[Revisi?n completa](depuracion/gao20260920/REVISION.md).

Registro: 228 afirmaciones; protocolo demostrado, CF_F conjeturada.
Fuente versionada `depuracion/coherencia20260913/registro.json` y generador
`guardarafirmaciones.py`. No reconstruir conversaciones ni alterar hist?ricos.
Los [an?lisis previos](depuracion/analisis20260920/CONTINUIDAD.md) se conservan;
su ruta P1?P3 precede este avance. zootheorem permanece intacto.
Cierre solicitado: commit y push del laboratorio; reanudar desde la cota
anterior, sin repetir censos caros ni la compilaci?n por rutina.
