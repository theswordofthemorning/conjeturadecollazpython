# Artículos: Gao, Garner y Wu

26-09-2026. El usuario pidió tres artículos, uno por conjetura, «como si
fueran para arXiv (tal vez un día tengamos que mandarlos)», con nombres
completos y fechas, bien explicados y revisados antes. **Todavía no están
escritos.** Esta carpeta guarda el plan, los datos reunidos y lo que falta.
No se envía nada sin autorización del usuario.

## Formato elegido

LaTeX `amsart`, en inglés: un `.tex` por artículo, en `papers/`, con la
bibliografía dentro del archivo. Se compila con Tectonic 0.17.0
(portátil; el 26-09 se bajó de su GitHub oficial a la carpeta temporal y
compiló una prueba). En la próxima sesión hay que bajarlo otra vez.

**arXiv** (info.arxiv.org, leído el 26-09):
- se sube el código fuente TeX; no aceptan un PDF generado desde TeX;
- el resumen tiene como máximo 1920 caracteres, sin la palabra
  «Abstract»;
- el primer envío a math.NT necesita un *endorsement* de un autor
  establecido, y el correo gmail no da endoso automático;
- una IA no puede figurar como autora: el autor humano responde por todo,
  y el uso importante de IA se declara en el texto;
- el código Lean va como archivos auxiliares en la carpeta `anc/`;
- los moderadores rechazan trabajos sin sustento o con afirmaciones
  exageradas, y piden no subir más de tres artículos al día.

**ccchallenge.org** es otra cosa: formaliza la literatura de Collatz
artículo por artículo, en cualquier asistente de pruebas. No pide
plantilla. Exige declarar qué modelos de IA se usaron, y las auditorías
las hacen personas distintas de los autores. Allí encaja el código Lean
con referencia a Gao (1993), Garner (1985) y Wu (1992); a arXiv va el
artículo.

## Los tres artículos

| | Conjetura | Enunciado Lean | Estado |
|---|---|---|---|
| I | Guo-Gang Gao, *Discrete Math.* 112 (1993) 261–267 | `GaoEnunciado.conjetura_gao`, `GaoLiteral.conjetura_gao_literal` | demostrada; falta revisión humana |
| II | Lynn E. Garner, *Discrete Math.* 55 (1985) 57–64, conjetura (2) | `GarnerEnunciado.conjetura_garner` | demostrada con σ∞ igual; falta revisión humana |
| III | Wu Jiabang (邬家邦), *J. Huazhong Univ. Sci. Tech.* 20(5) (1992) 171–174 | `WuEnunciado.conjetura_wu_dos`, `conjetura_wu_uno` | conjetura 2 demostrada; la 1 reducida a un problema abierto |

**I. Gao.** Contenido: el mapa atajo; la cadena de pares
`{v, 3^k v + c}` (`cadena_completa.lean`, siete transiciones, fusión
desde `(1,1)` con bit 1); el transporte exacto a clases módulo `2^t`
(`TejonasGao.transporte`, `canon_modulo`, `fusion_clasica` con `k<=2t`);
la fusión casi segura, `MartasGao.martas`. Esa fusión se apoya en:
- el momento `E sqrt(|c|/3^k) <= (31/32)^n sqrt(·)+32`;
- la supervivencia `>=1/(n+1)` por la altura armónica `k-1`;
- los mixtos (Banda) y las rachas compartidas `<= 2+log2 k` (UmbralRachas);
- el reloj H3 y la ventana VH `>=1/(4Q)`;
- la palabra de Hormigas `16(ceil(log2(2+|c|))+1)^2`, de donde sale EF;
- los ensayos guardados (`supervivencia_por_entradas`) y Lagartijas.

Luego la densidad (`TejonasGao.gao`), la forma literal con el puente de
Hienas y la tabla 3 de Gao (`#guard`). Las secciones siguen
`depuracion/gao20260920`: Lagartijas.md, Martas.md, Tejonas.md, Hienas.md,
Ventana_conjunta.md, Reloj_bloques.md, Control_aditivo_producto.md y
Ensayo_finito.md.

**II. Garner.** Basado en `depuracion/garner20260926/Alpacas.md`: cota
de unión, valor común `3^a u+A` con `3∤A`, 2 raíz primitiva módulo `3^a`,
altura `t+a+m` y `σ∞=t+m`. La reseña de zbMATH (Graham Lord) mide la
altura con T, es decir σ∞; el teorema cubre ambas lecturas. Hay que
citar a Elia y Tucker (2015, arXiv:1511.09141), que refutan la
caracterización de Garner por bloques y cadenas; falta confirmar la
ficha exacta.

**III. Wu.** Las conjeturas «笔者猜想: lim d(M)=1» y «笔者猜想: lim L=∞»
se leyeron con la IA de CNKI. Contenido:
- `lim L=∞` por Garner;
- con `d(x)->1`, `lim d(M)=1` equivale a densidad 1 de los que llegan a 1
  (Condoras.lean);
- una observación escrita, no formal: si d nunca bajara, al menos un 36 %
  de los n llegaría a 1. Hoy sólo se sabe `>= x^0,84` (Krasikov y
  Lagarias, 2003).

La tabla `d(2^N)`, con N<=24, la calcula
[wu1992_densidad.py](../depuracion/garner20260926/wu1992_densidad.py). Sus valores coinciden con los cuatro que dio la IA de CNKI,
pero dos de ellos venían corridos una fila.

## Pendiente antes de escribir o enviar

1. **Autor:** nombre completo y afiliación del usuario (no se deduce del
   correo).
2. **Declaración de IA:** confirmar los modelos. Git registra Claude
   Fable 5, Claude Opus 5 y Claude Opus 5.5.
3. **Wu:** cotejar con el PDF original las dos citas y la tabla (CNKI:
   `HZLG199205041`, DOI 10.13245/j.hust.1992.05.030; el registro del
   usuario quedó bloqueado).
4. **Evidencia:** regenerar `evidencia_gao_lean.json` con
   `python -B -X utf8 depuracion/gao20260920/evidencia_gao_lean.py`, que ya
   incluye Condoras y WuEnunciado.
5. **Revisión humana** de los enunciados, antes de cualquier envío
   ([gaopendientes.md](../gaopendientes.md)).
6. **Redacción:** primero Gao, porque los otros dos lo citan. Compilar
   cada `.tex` sin avisos y comprobar que cada enunciado del texto coincida
   con el de Lean.
