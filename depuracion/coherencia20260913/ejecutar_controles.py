"""Reproduce los controles acotados de esta auditoría; guarda salidas y manifiesto.

No regenera bases ni ejecuta los barridos históricos grandes. Requiere el
repositorio zootheorem al lado y Lean instalado. Cada proceso tiene un tope
de 120 segundos; un tope excedido cuenta como fallo, nunca como teorema.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from time import monotonic

CARPETA = Path(__file__).resolve().parent
LAB = CARPETA.parents[1]
ZOO = LAB.parent / 'zootheorem'


def main():
    python = [sys.executable, '-B', '-X', 'utf8']
    trabajos = []
    for nombre in ('motor', 'registro', 'matematica'):
        trabajos.append(('auditoria_' + nombre, LAB,
                         python + [str(CARPETA / f'verificar_{nombre}.py')]))
    trabajos.append(('estratos_simbolicos', LAB, python + ['estratoscadena.py', '--prof', '20']))
    trabajos.append(('subrenovacion', LAB, python + ['subrenovacionc.py', '--prof', '20']))
    for nombre in ('invariantes', 'balance', 'obstruccion', 'rachas', 'transferencia'):
        base = f'depuracion/frente20260910/{nombre}'
        trabajos.append(('python_' + nombre, LAB, python + [base + '.py']))
        trabajos.append(('lean_' + nombre, LAB, ['lean', base + '.lean']))
    for nombre in ('cadenakc', 'cabras', 'conejas'):
        trabajos.append(('lean_' + nombre, LAB, ['lean', nombre + '.lean']))
    trabajos.append(('lean_version', LAB, ['lean', '--version']))
    trabajos.append(('lean_espejo', ZOO, ['lean', 'lean/mirror_theorem.lean']))
    for nombre in ('merging_classes', 'q_family', 'strata', 'consistency'):
        trabajos.append(('zoo_' + nombre, ZOO, python + [f'verify/verify_{nombre}.py']))

    def ejecutar(trabajo):
        nombre, cwd, comando = trabajo
        inicio = monotonic()
        try:
            salida = subprocess.run(comando, cwd=cwd, capture_output=True,
                                    text=True, encoding='utf-8', errors='replace', timeout=120)
            codigo, texto = salida.returncode, salida.stdout + salida.stderr
        except subprocess.TimeoutExpired:
            codigo, texto = -1, 'INCONCLUSO: tiempo máximo de 120 segundos excedido.\n'
        (CARPETA / (nombre + '_salida.txt')).write_text(texto, encoding='utf-8')
        axiomas_admitidos = 'sorryAx' in texto or 'declaration uses \'sorry\'' in texto
        resultado = dict(nombre=nombre, repo=cwd.name, comando=comando[1:] if comando[0] == sys.executable else comando,
                         exit_code=codigo, segundos=round(monotonic()-inicio, 3),
                         admite_sorry=axiomas_admitidos,
                         correcto=codigo == 0 and not axiomas_admitidos)
        print(nombre, 'OK' if resultado['correcto'] else 'FALLO', flush=True)
        return resultado

    resultados = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for futuro in as_completed([pool.submit(ejecutar, t) for t in trabajos]):
            resultados.append(futuro.result())
    manifiesto = dict(fecha_utc=datetime.now(timezone.utc).isoformat(),
                      resultados=sorted(resultados, key=lambda r: r['nombre']))
    (CARPETA / 'controles.json').write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if not all(r['correcto'] for r in resultados):
        raise SystemExit('Hay controles fallidos; consultar controles.json y las salidas.')
    print(f'OK: {len(resultados)} controles acotados. No es una auditoría de todas las pruebas históricas.')


if __name__ == '__main__':
    main()
