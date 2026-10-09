# Genera github/index.html (la tienda como página estática para GitHub Pages)
# a partir de index.html + css.html + js.html, que son los mismos archivos de Apps Script.
# Uso:  python construir_github.py  "https://script.google.com/macros/s/XXXX/exec"
import io, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1].strip() if len(sys.argv) > 1 else 'PEGA_AQUI_LA_URL_EXEC'
if URL != 'PEGA_AQUI_LA_URL_EXEC' and not re.match(r'^https://script\.google\.com/macros/s/[\w-]+/exec$', URL):
    sys.exit('La URL debe verse así: https://script.google.com/macros/s/XXXX/exec')

leer = lambda n: io.open(os.path.join(AQUI, n), encoding='utf-8').read()
h = leer('index.html')

h = h.replace('data-tema="<?= config.tema ?>"', 'data-tema="oscuro"')
h = h.replace('<title><?= config.tienda ?></title>',
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="theme-color" content="#09080B">\n'
    '<title>Black Box Store · Fragancias 1.1</title>\n'
    '<meta name="description" content="Fragancias línea 1.1 para hombre y mujer. Envíos a toda Colombia y pedido directo por WhatsApp.">\n'
    '<meta property="og:title" content="Black Box Store · Fragancias 1.1">\n'
    '<meta property="og:description" content="Fragancias línea 1.1 para hombre y mujer. Envíos a toda Colombia y pedido directo por WhatsApp.">\n'
    '<meta property="og:type" content="website">\n'
    '<link rel="preconnect" href="https://script.google.com">\n'
    '<link rel="preconnect" href="https://script.googleusercontent.com">')
h = h.replace("<?!= include('css') ?>", leer('css.html'))
h = h.replace("<?!= include('js') ?>", leer('js.html'))
h = re.sub(r'<script>\s*window\.__DATA__=.*?</script>',
           lambda m: "<script>window.__API__=" + repr(URL) + ";</script>", h, flags=re.S)
resto = re.findall(r'<\?[^>]*\?>', h)
if resto:
    sys.exit('Quedaron etiquetas de Apps Script sin reemplazar: %s' % resto[:3])

os.makedirs(os.path.join(AQUI, 'github'), exist_ok=True)
io.open(os.path.join(AQUI, 'github', 'index.html'), 'w', encoding='utf-8', newline='\n').write(h)
print('OK: github/index.html  (API = %s)' % URL)
