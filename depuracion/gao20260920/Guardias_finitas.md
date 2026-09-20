# Hormigas y Gacelas: repetición guardada y reducción por entradas

20-09-2026. Cierre de la sesión: protocolo finito certificado. **CF_F
sigue candidata; Gao no se declara resuelta.**

## Ley, dominio y protocolo

Se usa `CadenaCompletaGao.paso`, la cadena entera absorbente del mapa
atajo, con bits iid justos de paridad del ancla. El tiempo cuenta pasos
físicos, desde cero. Sigma es el primer instante de fusión. El estado
ampliado conserva la base y una marca de entrada reciente de k=1 a k=2.
La marca no cambia la transición de la base.

Para C natural, fijar los parámetros uniformes de
[EF](Ensayo_finito.md): `W=H(C)+D(C)>=1`, `p=2^-D(C)/(4Q(C))`.
Una entrada es admisible si la marca está activa y el estado es `(2,c)`
con `|c|<=C`. Al buscar un ensayo se exige además que queden W pasos
antes de h. Si no se cumplen las guardias, se consume un bit y se sigue
buscando. Al llegar a h, la búsqueda termina sin otro ensayo.

Un ensayo consume W bits. Si termina vivo, cuenta como fallido; se borra
la marca y se busca la primera entrada admisible estrictamente posterior
al extremo del bloque. No se vuelve a admitir la entrada del extremo.
La absorción es persistente. Todas las decisiones se conocen al inicio;
no se condiciona al evento bueno futuro del reloj.

## Certificados

- [Repeticion.lean](formal/Repeticion.lean) define la búsqueda truncada
  como promedio recursivo y como evento booleano sobre palabras. Prueba
  su igualdad y la cota `(1-p)^j` para j ensayos admitidos y fallidos,
  mediante inducción finita. No supone independencia entre ensayos.
- [Guardias.lean](formal/Guardias.lean) identifica la proyección con la
  cadena original y aplica EF a cada estado admitido. `fallos_evento`
  entrega la cota para el evento de ejecución del protocolo.
- [ConteoEnsayos.lean](formal/ConteoEnsayos.lean) cuenta las posiciones
  admisibles, incluidos los extremos 0 y h. Desde la raíz
  `((0,1),false)`, sea este número `K_C(h)`. `completa_bloques` demuestra
  que supervivencia y `K_C(h)>=1+j(W+2)` implican j fallos admitidos.

Una derivación independiente del conteo: un prefijo de W pasos consume
a lo sumo W posiciones antes de su extremo; borrar la marca pierde a lo
sumo otra posición. Si había al menos `1+(j+1)(W+2)` posiciones
admisibles, quedan al menos `1+j(W+2)` después del bloque y del reinicio.
La misma desigualdad garantiza que el primer bloque cabe. Los pasos de
búsqueda sin guardia no consumen posiciones contadas. Inducir en j y en
la longitud de la búsqueda da la inclusión, también en los extremos.

La partición por el contador produce `supervivencia_por_entradas`:

    P(sigma>h)
      <= P(sigma>h y K_C(h)<1+j(W+2)) + (1-p)^j.

El primer término **incluye supervivencia**. Reemplazarlo por una
probabilidad de pocas entradas sin esa condición incluiría las trayectorias
ya absorbidas y perdería la reducción útil. El teorema vale para todos
C,j,h naturales; las probabilidades son promedios exactos de palabras.

## Primer paso al retomar

Con los parámetros de [CF_F](Ensayo_finito.md), `N=2^m`, `h=N^6`,
`C_m=9h^4` y `J_F=floor((N-1)/(W_m+2))`, demostrar sobre esta misma cadena:

    P(sigma>h y K_(C_m)(h)<N) <= 3/N+66/h+1/(4h^3).

Partir del presupuesto del [reloj global](Reloj_global.md) y de C5 en
[CF_H](Ventana_armonica.md): formalizar frontera, porciones incompletas
y suficientes entradas antes de h con offset acotado. Como
`1+J_F(W_m+2)<=N`, esa cota cerraría el enlace finito pendiente.
Después verificar el límite `J_F*p_m -> infinito` y el transporte a
clases de [Cilindros](Cilindros.md). Falta cotejar el artículo primario
de Gao. Ninguno de estos pasos se declara completado por el protocolo.

## Evidencia del cierre

Lean 4.32.2, Mathlib fijado: `lake build GaoCore GaoFormal` correcto.
Los tres módulos nuevos añaden 16 consultas de axiomas sin `sorryAx`;
total local 157 en 22 archivos, incluidas las cuatro piezas previas fuera
de `formal/`. No se cuentan las consultas del módulo histórico importado.
[Compilación y hashes](evidencia_guardias_lean.json).

[verificar_guardias.py](verificar_guardias.py) contrasta la implementación
recursiva con un recorrido directo de palabras en una cadena auxiliar
absorbente: 24.564 casos, 528 comparaciones racionales y 2.659 inclusiones,
h<=10, anchos 1,2,3 y riesgos 1/2,1/2,5/8. Incluye h=0, j=0, arranque
sin marca y absorción inicial. Es un control finito del protocolo y del
conteo; no verifica EF en sus enormes horizontes ni prueba CF_F.
[Resultado exacto](evidencia_guardias_exacta.json).
