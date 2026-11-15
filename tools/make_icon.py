"""Φτιάχνει το εικονίδιο της εφαρμογής (δίσκος βαρών) σε PNG, χωρίς εξωτερικές βιβλιοθήκες."""
import zlib, struct, math, sys
from pathlib import Path

def hexc(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
BG, RED, RIM, STEEL, HOLE, WHITE = map(hexc, ['#14171B', '#C8102E', '#9E0C24', '#C9CED4', '#14171B', '#FFFFFF'])

def color_at(x, y):
    # x,y σε [0,1]
    dx, dy = x - .5, y - .5
    r = math.hypot(dx, dy)
    if r < .055: return HOLE
    if r < .135: return STEEL
    if r < .155: return RIM
    if r < .40:
        # λευκές ρίγες-λαβές πάνω στον δίσκο (σαν olympic plate)
        if .30 < r < .325: return RIM
        return RED
    if r < .415: return RIM
    return BG

def render(size, ss=4):
    rows = []
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            acc = [0, 0, 0]
            for sy in range(ss):
                for sx in range(ss):
                    c = color_at((px + (sx + .5) / ss) / size, (py + (sy + .5) / ss) / size)
                    acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            n = ss * ss
            row += bytes(round(v / n) for v in acc)
        rows.append(bytes(row))
    raw = b''.join(rows)
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

root = Path(__file__).resolve().parent.parent
for name, size in [('apple-touch-icon.png', 180), ('icon-512.png', 512), ('favicon.png', 64)]:
    (root / name).write_bytes(render(size, 3 if size > 200 else 4))
    print('wrote', name)
