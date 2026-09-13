# Archivo de contexto — 13-09-2026

Copias **literales** anteriores a la reducción documental. No son contexto
de arranque ni instrucciones actuales. Mandan [AGENTS.md](../../AGENTS.md)
y [ESTADO_INVESTIGACION.md](../../ESTADO_INVESTIGACION.md).

`fuentes.json` identifica origen, tamaño y SHA-256 de cada copia.
`indice.tsv` localiza títulos y fichas con líneas desde/hasta. Por ejemplo,
desde la raíz del laboratorio:

```powershell
rg -n -m 8 'D-01|CABRAS' archivo/contexto_20260913/indice.tsv
Get-Content -Encoding utf8 archivo/contexto_20260913/derivados.md.txt | Select-Object -Skip 25 -First 60
```

Leer sólo el tramo requerido, ampliándolo si hace falta. Los enlaces
relativos escritos dentro de las copias conservan como base el directorio
del archivo **original** indicado en `fuentes.json`.
La extensión `.txt` evita confundir el archivo con documentación de arranque.
Para trabajo nuevo, usar notas temáticas y enlazarlas desde el estado breve.
