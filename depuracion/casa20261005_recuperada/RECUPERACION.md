# Recuperación de la sesión local del 05-10-2026

Integrada el 07-10-2026 sobre `58e8f97`, dando prioridad a GitHub.
La copia local partía de `d296b3d` y contenía trabajo sin commit. GitHub
había avanzado con `f136c0e` y `58e8f97`. Se incorporaron ambos commits
por avance directo, sin reescribir su historia.

## Trabajo conservado

Esta carpeta conserva, byte por byte, los archivos de la sesión local.
Las implementaciones independientes permanecen separadas de la
[ruta vigente](../casa20261004/LEEME.md): `CasaKorec` y `CasaTerras`
usan los mismos nombres que módulos distintos del trabajo online.
No deben mezclarse sus objetos compilados ni sus rutas de importación.

- [Corzas](CORZAS.md): retrato del fugitivo, Terras y delimitación de choques.
- [Chinchillas](CHINCHILLAS.md): Korec y cotas de potencia, incluidas las condicionales bajo LMN.
- [Perdices](PERDICES.md): identidad afín, ley de la cadena módulo `3^m`
  y medición de mezcla. Incluye [CasaCadena.lean](CasaCadena.lean),
  ausente en la versión online al integrar.
- [LEEME original](LEEME.md): contexto de la sesión, no estado vigente.
- [Registro original](sesion_original/depuracion/coherencia20260913/registro.json),
  su verificador, el estado y la base SQLite: captura histórica de los
  cambios locales. Sus rutas se refieren al emplazamiento original.
  No sustituyen el registro activo ni se ejecutan desde esta subcarpeta.

El catálogo activo conserva las 278 afirmaciones de GitHub. No se suman
automáticamente las 280 de la sesión local: hay resultados solapados y
altas diferentes. La recuperación conserva sus enunciados para una
conciliación posterior por clave y contenido, sin reasignar IDs históricos.

## Validación y límites

Se verificó la conservación exacta de los 41 archivos mediante SHA-256
contra un respaldo externo anterior a la integración; el
[manifiesto](manifiesto_recuperacion.json) registra sus rutas y huellas.
Todos los archivos que ya estaban en GitHub se conservan sin cambios,
excepto el enlace de recuperación añadido al estado breve.

Las huellas de los 19 módulos y del comprobador coinciden con
[evidencia_fugitivo.json](evidencia_fugitivo.json). La evidencia histórica
registra 108 consultas de `#print axioms`, sólo con `propext`,
`Classical.choice` y `Quot.sound`. Se comprobó Lean 4.32.2 instalado.
No se repitió la compilación: esto es conservación de evidencia previa,
no una nueva certificación ni una revisión humana de los enunciados.
Los textos históricos que mencionan 98 consultas corresponden a una
etapa anterior a `CasaCadena` y se conservaron literalmente.

Se repitió el contraste independiente [cotejar_cadena.py](cotejar_cadena.py):
546 000 casos, biyección para `k <= 14` y 45 pares `(k,m)` de la ley exacta,
todos correctos y con el mismo resultado que [cotejo_cadena.json](cotejo_cadena.json).
No se repitieron los censos grandes ni la medición hasta `3^14`.
Un conteo finito no demuestra la afirmación universal.

Para reconstruir esta implementación desde la raíz, usando su propia
carpeta temporal y una salida nueva:

```text
python -B -X utf8 depuracion/casa20261005_recuperada/comprobar_fugitivo.py --salida RUTA_NUEVA/evidencia_fugitivo.json
```

Los ejemplos de comandos dentro de los documentos originales conservan
`casa20261004`; para esta implementación debe usarse
`casa20261005_recuperada`. La siguiente acción posible es conciliar las
altas recuperadas con el catálogo vigente, cotejando solapamientos y
alcance; no se declara resuelta la mezcla fina de Tao ni Collatz.
