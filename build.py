"""Φτιάχνει το index.html (για το GitHub Pages) από το src/app.html."""
from pathlib import Path
root = Path(__file__).parent
head = (root / 'src/head.html').read_text()
app = (root / 'src/app.html').read_text()
(root / 'index.html').write_text(head + app + '\n</body>\n</html>\n')
print('index.html updated')
