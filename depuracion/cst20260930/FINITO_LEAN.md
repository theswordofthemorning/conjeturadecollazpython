# Ocelotas: descenso finito y enlace con la criba — 30-09-2026

**Nueva pieza formalizada:** [OcelotasFinito.lean](OcelotasFinito.lean)
certifica, para cada **2<=n<=11214**, que existe un primer cruce k<=105
y que en él hay descenso. Este resultado **no usa Rhin ni limita el número
de rachas**. Esta tanda dejó la extensión universal a diez rachas sujeta
a una comprobación aritmética explícita. El [cierre posterior](CIERRE_LEAN.md)
ya la demuestra y aplica al ensamblaje para palabras reales `Palabra`.

Continúa la [reducción desde las trayectorias](TRAYECTORIAS_LEAN.md).
Se conserva el nombre Ocelotas y el alcance de la
[prueba escrita condicional](REVISION_RACHAS.md).

## Enunciados certificados

Se usa el atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar, sobre
naturales. Un índice cuenta un paso de este atajo. `S k n` cuenta los pasos
impares anteriores a k; `PrimerCruce n k` exige `3^(S k n)<2^k` y
coeficiente al menos uno en cada prefijo anterior. No hay ley
probabilística ni hipótesis de distribución.

```lean
theorem existe_descenso_finito {n : ℕ} (hn : 2 ≤ n) (hnmax : n ≤ 11214) :
    ∃ k, k ≤ 105 ∧ PrimerCruce n k ∧ T^[k] n < n

theorem descenso_finito {n k : ℕ} (hn : 2 ≤ n) (hnmax : n ≤ 11214)
    (hk : PrimerCruce n k) : T^[k] n < n
```

El segundo enunciado no impone un tope a k: `primer_cruce_unico` demuestra
que coincide con el testigo del primero. Es un teorema exacto sobre un
intervalo finito, no CST para todos los naturales ni la llegada a 1.

## Verificador y corrección

`comprobar n x p d combustible` transporta el valor de la órbita y el
numerador y denominador del coeficiente. Al visitar un índice i:

- Si p<d, acepta exactamente cuando x<n.
- Si todavía p>=d, aplica T, multiplica p por 3 cuando x es impar y
  duplica d.
- Si no queda combustible, rechaza.

`numerador_siguiente` enlaza esa actualización con la definición original
de S. `comprobar_correcto` prueba por inducción los invariantes
`x=T^i(n)`, `p=3^(S i n)`, `d=2^i` y todos los prefijos. La aceptación
produce un k con `i<=k<i+combustible`, primer cruce y descenso.

`semilla n` empieza en i=0 con `(x,p,d)=(n,1,1)` y combustible 106:
visita los índices 0,...,105. El corte no se presupone suficiente;
la aceptación exhaustiva lo demuestra. `intervalo` divide en mitades el
intervalo semiabierto `[inicio,inicio+cantidad)`, y `intervalo_correcto`
demuestra que la aceptación cubre cada elemento. Finalmente:

```lean
theorem intervalo_comprobado : intervalo 2 11213 = true := by
  decide +kernel
```

El núcleo comprueba las 11213 semillas. El recorrido y la prueba de
cobertura no dependen de un listado Python. Se comprueban también el
rechazo de 0 y 1, el rechazo de n=3 con combustible 4, su aceptación con
5 y el extremo superior 11214.

## Obligación aritmética restante

`exponente_acotado` prueba que `k<131072` y `3^q<2^k` implican
**q<=82696**, usando la comparación exacta
`2^131071<=3^82697`. Para las palabras reales de r>0, la ventana estricta
ya formalizada determina `k=Nat.log2(3^q)+1` y q>=1.

Se simplifica la interfaz del cierre. Sean

```text
P = 3^q, k = Nat.log2(P)+1, Delta = 2^k-P, m = (q-1)/182.
CertificadoAritmetico q :=
  10P <= 11215 Delta  o  11P <= 2^m Delta.
```

La división de m es natural. En la primera rama, el control aditivo de un
fallo daría `Delta*n<rP<=10P<=11215 Delta`, luego n<=11214 y contradicción
con `descenso_finito`. En la segunda, `criba_fallo` y `cota_diez_lineal`
darían `q<=cota 10 m<=182m<q`.

`diez_de_certificado` formaliza exactamente este ensamblaje. Además de
`RhinEntera`, recibe **explícitamente**:

```lean
hcriba : ∀ q, 1 ≤ q → q ≤ 82696 → CertificadoAritmetico q
```

Su conclusión es el descenso para `n>=2`, `Palabra n a b r`, `0<r<=10`
y primer cruce en `tiempo a b r`. **Aquí no se demuestra hcriba.** Su
ausencia de `#print axioms` no elimina el argumento del enunciado.
Tampoco se demuestra Rhin. Este ensamblaje recibe `Palabra`; su extracción
desde el número de rachas se demuestra en la [tanda posterior](CONTADOR_LEAN.md).

## Cotejo y reproducción

[cotejar_finito_lean.py](cotejar_finito_lean.py) es independiente de los
otros verificadores: usa el mapa clásico agrupado y `Fraction` para el
coeficiente. Recorre las 11213 semillas, con tope 105, y obtiene la misma
huella de filas `(n,k,q,valor)` que el certificado anterior:

```text
864d42e2d564c80b43055e67eabcc9dca50e07a3609ba2fb03ccfbedf27f7918
```

El primer testigo del máximo k=105 es n=10087: un tope 104 se rechaza y
105 basta. Se cotejan los bordes n=2,3,39,11214. El programa también
comprueba la nueva obligación aritmética por potencias sucesivas, sin
logaritmos: **82593 exponentes** se resuelven por la cota de semilla y
**103** por la criba lineal. Esto último es cálculo exacto Python, todavía
fuera de Lean. No se amplía ningún intervalo.
[Salida y huellas](cotejo_finito_lean.json).

[comprobar_rachas_lean.py](comprobar_rachas_lean.py) reconstruye los cuatro
módulos en un directorio temporal y exige las auditorías de axiomas.
Lean 4.32.2; código 0. Los nuevos resultados de descenso usan únicamente
`propext` y `Quot.sound`; el ensamblaje añade `Classical.choice`. Sin
`sorryAx` ni evaluación nativa como sustituto del núcleo.
[Compilación y huellas](lean_finito.txt).

Desde la raíz:

```text
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_finito.txt
python -B -X utf8 depuracion/cst20260930/cotejar_finito_lean.py --certificado depuracion/cst20260930/certificado_10_rachas.json --max-pasos 105 --salida depuracion/cst20260930/cotejo_finito_lean.json
```

El estado y la entrada existente del registro se actualizan, sin aumentar
las 246 afirmaciones. Se ejecuta el generador habitual y se conservan
los registros históricos ([controles](registro_finito.txt)).
La obligación `hcriba` se resolvió y aplicó en el [cierre](CIERRE_LEAN.md).
La interfaz del contador se cerró en [CONTADOR_LEAN.md](CONTADOR_LEAN.md).
Siguen la auditoría de Rhin y la revisión humana.
