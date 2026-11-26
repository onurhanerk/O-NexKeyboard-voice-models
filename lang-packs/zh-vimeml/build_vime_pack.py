# VimeML tiny zh v1 → OBoard dil paketi (zh-vimeml-tiny-v1.bin)
# Girdi: pt_extract.py çıktısı (index.json + *.f32) ve spm_extract.py çıktısı (pieces.json).
# Biçim: b'VIMEZH01' | u32 başlık uzunluğu | başlık JSON (config, tensörler, SentencePiece
# parçaları) | 64 bayta hizalı fp16 ağırlıklar. Ağırlıklar özgün FP32 tensörlerin fp16'ya
# yuvarlanmış hâlidir (başka değişiklik yok). Native okuyucu: entry/src/main/cpp/vime.cpp.
import sys, json, struct, array
raw, out = sys.argv[1], sys.argv[2]
index = json.load(open(raw + '/index.json'))
pieces = json.load(open(raw + '/pieces.json', encoding='utf-8'))
order = ['token_embedding.weight', 'position_embedding.weight']
for l in range(9):
    for n in ['attention_norm', 'attention.qkv', 'attention.projection', 'ffn_norm', 'ffn.gate', 'ffn.up', 'ffn.down']:
        order.append(f'blocks.{l}.{n}.weight')
order.append('final_norm.weight')
assert set(order) == set(index), set(index) ^ set(order)
tensors = []; blobs = []; off = 0
for k in order:
    f = array.array('f'); f.frombytes(open(raw + '/' + index[k]['file'], 'rb').read())
    h = struct.pack(f'<{len(f)}e', *f)
    tensors.append({'name': k, 'shape': index[k]['shape'], 'offset': off})
    blobs.append(h); off += len(h)
config = {'vocab': 12288, 'ctx': 128, 'd': 384, 'heads': 6, 'layers': 9, 'ff': 960, 'eps': 1e-5,
          'bos': 2, 'source': 'Voltline/vimeml-tiny-zh-v1 (GPL-3.0-or-later + LICENSE-EXCEPTION)'}
header = json.dumps({'config': config, 'tensors': tensors, 'pieces': pieces}, ensure_ascii=False).encode('utf-8')
with open(out, 'wb') as fo:
    fo.write(b'VIMEZH01'); fo.write(struct.pack('<I', len(header))); fo.write(header)
    pos = 12 + len(header); pad = (-pos) % 64; fo.write(b'\0' * pad)
    for b in blobs: fo.write(b)
print('başlık', len(header), 'veri', off, 'hizalama', pad)
