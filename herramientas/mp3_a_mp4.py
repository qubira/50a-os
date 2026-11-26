"""Mete un .mp3 dentro de un contenedor .mp4 (solo audio) sin recodificar.
Uso: python mp3_a_mp4.py entrada.mp3 salida.mp4
"""
import struct
import sys

BITRATES = {  # MPEG-1 y MPEG-2/2.5, capa III (kbps)
    1: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
    2: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
}
RATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}


def leer_cuadros(d):
    i = 0
    if d[:3] == b'ID3':
        tam = (d[6] << 21) | (d[7] << 14) | (d[8] << 7) | d[9]
        i = 10 + tam + (10 if d[5] & 0x10 else 0)
    cuadros, sr, canales = [], None, 2
    while i + 4 <= len(d):
        if d[i] != 0xFF or (d[i + 1] & 0xE0) != 0xE0:
            i += 1
            continue
        ver = (d[i + 1] >> 3) & 3
        capa = (d[i + 1] >> 1) & 3
        bri = d[i + 2] >> 4
        sri = (d[i + 2] >> 2) & 3
        pad = (d[i + 2] >> 1) & 1
        if ver == 1 or capa != 1 or bri in (0, 15) or sri == 3:
            i += 1
            continue
        br = BITRATES[1 if ver == 3 else 2][bri] * 1000
        rate = RATES[ver][sri]
        largo = (144 * br // rate + pad) if ver == 3 else (72 * br // rate + pad)
        if i + largo > len(d):
            break
        if sr is None:
            sr = rate
            canales = 1 if (d[i + 3] >> 6) == 3 else 2
            muestras = 1152 if ver == 3 else 576
        cuadros.append(d[i:i + largo])
        i += largo
    return cuadros, sr, canales, muestras


def caja(tipo, *partes):
    cuerpo = b''.join(partes)
    return struct.pack('>I', 8 + len(cuerpo)) + tipo + cuerpo


def completa(tipo, ver, flags, *partes):
    return caja(tipo, struct.pack('>I', (ver << 24) | flags), *partes)


def desc(tag, cuerpo):
    n = len(cuerpo)
    return bytes([tag, 0x80 | ((n >> 21) & 0x7F), 0x80 | ((n >> 14) & 0x7F), 0x80 | ((n >> 7) & 0x7F), n & 0x7F]) + cuerpo


def armar(cuadros, sr, canales, muestras, offset_datos):
    n = len(cuadros)
    dur = n * muestras
    tam_total = sum(len(c) for c in cuadros)
    kbps = int(tam_total * 8 / (dur / sr)) if dur else 128000
    matriz = struct.pack('>9I', 0x10000, 0, 0, 0, 0x10000, 0, 0, 0, 0x40000000)
    mvhd = completa(b'mvhd', 0, 0, struct.pack('>IIII', 0, 0, sr, dur), struct.pack('>IH', 0x10000, 0x100), b'\0' * 10, matriz, b'\0' * 24, struct.pack('>I', 2))
    tkhd = completa(b'tkhd', 0, 3, struct.pack('>IIIII', 0, 0, 1, 0, dur), b'\0' * 8, struct.pack('>HHHH', 0, 0, 0x100, 0), matriz, struct.pack('>II', 0, 0))
    mdhd = completa(b'mdhd', 0, 0, struct.pack('>IIII', 0, 0, sr, dur), struct.pack('>HH', 0x55C4, 0))
    hdlr = completa(b'hdlr', 0, 0, struct.pack('>I', 0), b'soun', b'\0' * 12, b'Sonido\0')
    smhd = completa(b'smhd', 0, 0, struct.pack('>HH', 0, 0))
    dinf = caja(b'dinf', completa(b'dref', 0, 0, struct.pack('>I', 1), completa(b'url ', 0, 1)))
    dcd = desc(0x04, bytes([0x6B, 0x15]) + (0).to_bytes(3, 'big') + struct.pack('>II', kbps, kbps))
    esd = desc(0x03, struct.pack('>HB', 0, 0) + dcd + desc(0x06, b'\x02'))
    esds = completa(b'esds', 0, 0, esd)
    mp4a = caja(b'mp4a', b'\0' * 6, struct.pack('>H', 1), b'\0' * 8, struct.pack('>HHHH', canales, 16, 0, 0), struct.pack('>I', sr << 16), esds)
    stsd = completa(b'stsd', 0, 0, struct.pack('>I', 1), mp4a)
    stts = completa(b'stts', 0, 0, struct.pack('>III', 1, n, muestras))
    stsc = completa(b'stsc', 0, 0, struct.pack('>IIII', 1, 1, n, 1))
    stsz = completa(b'stsz', 0, 0, struct.pack('>II', 0, n), b''.join(struct.pack('>I', len(c)) for c in cuadros))
    stco = completa(b'stco', 0, 0, struct.pack('>II', 1, offset_datos))
    stbl = caja(b'stbl', stsd, stts, stsc, stsz, stco)
    minf = caja(b'minf', smhd, dinf, stbl)
    trak = caja(b'trak', tkhd, caja(b'mdia', mdhd, hdlr, minf))
    return caja(b'moov', mvhd, trak)


def main(ent, sal):
    d = open(ent, 'rb').read()
    cuadros, sr, canales, muestras = leer_cuadros(d)
    assert cuadros, 'no se encontraron cuadros MP3'
    ftyp = caja(b'ftyp', b'isom', struct.pack('>I', 0x200), b'isomiso2mp41')
    moov = armar(cuadros, sr, canales, muestras, 0)
    offset = len(ftyp) + len(moov) + 8
    moov = armar(cuadros, sr, canales, muestras, offset)
    datos = b''.join(cuadros)
    with open(sal, 'wb') as f:
        f.write(ftyp + moov + struct.pack('>I', 8 + len(datos)) + b'mdat' + datos)
    print(len(cuadros), 'cuadros,', sr, 'Hz,', canales, 'canales,', round(len(cuadros) * muestras / sr), 's')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
