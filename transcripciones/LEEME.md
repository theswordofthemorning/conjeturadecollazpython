# Las transcripciones crudas, respaldadas

Un `.zip` por sesion, con el `.jsonl` literal que escribe Claude Code en

```
~/.claude/projects/<slug-del-proyecto>/<id-de-sesion>.jsonl
```

## Por que existe esta carpeta

`respuestas.db` guarda el TEXTO de cada mensaje, y eso ya salvo 355 mensajes de
tres sesiones cuyo `.jsonl` **desaparecio del disco en menos de tres dias**
(`29a697f3`, `ada74998`, `c33cf2bc`). La regla funciono.

Pero el `.jsonl` tiene mas cosas que el texto: las llamadas a herramientas, sus
resultados, los ficheros que se tocaron y en que orden. Nada de eso entra en la
base. Y el 01-08-2026 se comprobo que el directorio de transcripciones **no es
un sitio duradero**: es la misma leccion que ya se cobro `lecturas/*.pdf` (que
`.gitignore` ignoraba, y que ya no existen) y el toolchain de Lean (que estaba
instalado y desaparecio el mismo dia).

**Lo que no esta en git no sobrevive.** Esta carpeta es la conclusion.

## Por que un zip por sesion y no uno solo

Un unico `.zip` con todo se reescribe entero en cada sesion, y git guardaria un
blob nuevo de varios MB cada vez. Con un fichero por sesion, cada blob se
escribe UNA vez y no se vuelve a tocar: lo unico que cambia entre commits es el
zip de la sesion en curso.

## Como se regenera

```powershell
$origen  = "$env:USERPROFILE\.claude\projects\C--Users-Home-Desktop-conjeturadecollazpython"
$destino = "C:\Users\Home\Desktop\conjeturadecollazpython\transcripciones"
foreach ($f in Get-ChildItem "$origen\*.jsonl") {
    $zip = Join-Path $destino ($f.BaseName + ".jsonl.zip")
    if (Test-Path $zip) { Remove-Item $zip -Force }
    Compress-Archive -Path $f.FullName -DestinationPath $zip -CompressionLevel Optimal
}
```

Es **idempotente**: rehace los zips de las sesiones que sigan en disco y no
borra los de las que ya no estan. Correrlo mil veces no pierde nada.

**OJO: no recupera lo perdido.** Las tres sesiones sin `.jsonl` no van a
aparecer aqui nunca. De ellas solo queda el texto, en `respuestas.db`.

## Que hacer al cerrar sesion

Las dos cosas, en este orden:

```
python guardarrespuestas.py     # el texto, a respuestas.db (append-only)
<el bloque de PowerShell de arriba>   # el crudo, a esta carpeta
```

Y conviene correrlas **tambien a mitad** de una sesion larga: la del 01-08-2026
produjo diez commits y murio sin cierre ordenado, asi que de todo ese dia solo
quedan 42 mensajes de una ventana de 21 minutos.
