"""Prueba ambos HTML desde file://, sin red, en escritorio y móvil."""

import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# Nombre buscado -> pieza que debe quedar elegida (Focas es alias de Queltehues).
BUSQUEDAS = {'Perras': 'perras', 'Gatas': 'gatas', 'Jirafas': 'jirafas', 'Pumas': 'pumas', 'Ocelotas': 'ocelotas',
             'Perdices': 'perdices', 'Focas': 'queltehues', 'Corzas': 'corzas', 'Chinchillas': 'chinchillas',
             'Loras': 'loras', 'Ballenas': 'ballenas'}


def verificar():
    resultados = []
    with sync_playwright() as motor:
        navegador = motor.chromium.launch(headless=True)
        for modo in ('Basic', 'Complex'):
            for ancho, alto in ((1440, 1000), (390, 844)):
                contexto = navegador.new_context(viewport={'width': ancho, 'height': alto}, offline=True)
                pagina = contexto.new_page()
                errores = []
                solicitudes = []
                pagina.on('pageerror', lambda error: errores.append(str(error)))
                pagina.on('request', lambda peticion: solicitudes.append(peticion.url))
                ruta = Path(__file__).with_name('MapaDependencias' + modo + '.html')
                pagina.goto(ruta.as_uri())
                assert pagina.evaluate("cy.nodes('.pieza').length") == 123
                for nombre, pieza in BUSQUEDAS.items():
                    pagina.locator('#buscar').fill(nombre)
                    pagina.locator('#buscar').press('Enter')
                    assert pagina.evaluate('fijado') == pieza, nombre
                    assert pagina.evaluate(f"cy.getElementById('{pieza}').hasClass('elegido')"), nombre
                    titulo = pagina.evaluate(f"piezas.get('{pieza}').titulo")
                    assert titulo in pagina.locator('#panel h2').inner_text(), nombre
                # Al elegir una pieza se encienden sus apoyos y se apaga el resto.
                pagina.evaluate("elegir('hienas')")
                assert pagina.evaluate("cy.getElementById('gao_densidad').hasClass('tenue')") is False
                assert pagina.evaluate("cy.edges('.apoyo').length") >= 1
                assert pagina.evaluate("cy.nodes('.tenue').length") > 50
                pagina.locator('#ver-todo').click()
                assert pagina.evaluate("cy.nodes('.tenue').length") == 0
                pagina.locator('#ir-actual').click()
                assert 'matrices' in pagina.locator('#panel h2').inner_text()
                pagina.locator('#ver-todo').click()
                pagina.locator('[data-vista="nombres"]').click()
                assert pagina.locator('#inventario tbody tr').count() == 70
                assert pagina.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), 'Nombres desbordan'
                pagina.locator('#buscar').fill('Lurrus')
                assert pagina.locator('#inventario tbody tr').count() == 1
                pagina.locator('#buscar').fill('')
                pagina.locator('[data-vista="alarmas"]').click()
                assert pagina.locator('#vista-alarmas .tarjeta').count() >= 5
                if modo == 'Complex':
                    pagina.locator('[data-vista="afirmaciones"]').click()
                    assert pagina.locator('#lista-afirmaciones .af').count() == 333
                    assert pagina.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), 'Afirmaciones desbordan'
                    pagina.locator('#estado-af').select_option('refutado')
                    assert pagina.locator('#lista-afirmaciones .af').count() == 8
                    pagina.locator('[data-vista="correcciones"]').click()
                    assert pagina.locator('#lista-correcciones .af').count() == 85
                pagina.locator('[data-vista="arbol"]').click()
                assert not errores, errores
                assert not [url for url in solicitudes if url.startswith(('http:', 'https:'))], solicitudes
                assert pagina.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1')
                resultados.append({'modo': modo, 'ancho': ancho, 'alto': alto, 'errores': errores,
                                   'busquedas': len(BUSQUEDAS), 'inventario': 70})
                contexto.close()
        navegador.close()
    return resultados


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    argumentos = parser.parse_args()
    resultado = verificar()
    argumentos.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('OK: dos mapas, escritorio y móvil; navegación y búsquedas sin conexión.')
