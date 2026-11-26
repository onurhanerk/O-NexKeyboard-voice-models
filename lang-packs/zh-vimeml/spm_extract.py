# SentencePiece .model (protobuf) → pieces.json [[parça, puan, tür], ...] (elle protobuf okuma)
import sys, struct, json
d = open(sys.argv[1], 'rb').read()
def varint(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1; r |= (c & 0x7f) << s; s += 7
        if c < 0x80: return r, i
def fields(b):
    i = 0
    while i < len(b):
        key, i = varint(b, i); f, t = key >> 3, key & 7
        if t == 0: v, i = varint(b, i)
        elif t == 1: v = b[i:i+8]; i += 8
        elif t == 2:
            n, i = varint(b, i); v = b[i:i+n]; i += n
        elif t == 5: v = b[i:i+4]; i += 4
        else: raise SystemExit('tür ' + str(t))
        yield f, t, v
pieces = []; trainer = {}
for f, t, v in fields(d):
    if f == 1:
        p = {'piece': '', 'score': 0.0, 'type': 1}
        for f2, t2, v2 in fields(v):
            if f2 == 1: p['piece'] = v2.decode('utf-8')
            elif f2 == 2: p['score'] = struct.unpack('<f', v2)[0]
            elif f2 == 3: p['type'] = v2
        pieces.append([p['piece'], p['score'], p['type']])
    elif f == 2:
        for f2, t2, v2 in fields(v):
            if t2 == 0: trainer[f2] = v2
json.dump(pieces, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
types = {}
for p in pieces: types[p[2]] = types.get(p[2], 0) + 1
print(len(pieces), 'parça; türler', types); print(pieces[:10]); print('trainer model_type(3)=', trainer.get(3), 'byte_fallback(35)=', trainer.get(35))
