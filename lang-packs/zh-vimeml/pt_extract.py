# PyTorch .pt (zip) → ham float32 tensörler + index.json. Kısıtlı unpickler: yalnızca tensör
# yeniden kurma kayıtlarını ve OrderedDict'i tanır; başka hiçbir sınıf/işlev yüklenmez.
import sys, zipfile, pickle, json, collections, struct
src, outdir = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src)
names = z.namelist()
prefix = names[0].split('/')[0]
class Storage:
    def __init__(self, key, dtype): self.key, self.dtype = key, dtype
class TensorRef:
    def __init__(self, storage, offset, size, stride): self.storage, self.offset, self.size, self.stride = storage, offset, size, stride
def rebuild_tensor_v2(storage, offset, size, stride, *rest): return TensorRef(storage, offset, size, stride)
class DType:
    def __init__(self, name): self.name = name
class R(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) == ('torch._utils', '_rebuild_tensor_v2'): return rebuild_tensor_v2
        if (module, name) == ('collections', 'OrderedDict'): return collections.OrderedDict
        if module == 'torch' and name.endswith('Storage'): return name
        raise pickle.UnpicklingError(f'izin verilmeyen: {module}.{name}')
    def persistent_load(self, pid):
        # ('storage', storage_type, key, location, numel)
        return Storage(pid[2], pid[1])
state = R(z.open(f'{prefix}/data.pkl')).load()
index = {}
import os; os.makedirs(outdir, exist_ok=True)
for k, t in state.items():
    if t.storage.dtype != 'FloatStorage': raise SystemExit(f'beklenmeyen tür {k} {t.storage.dtype}')
    raw = z.read(f'{prefix}/data/{t.storage.key}')
    n = 1
    for s in t.size: n *= s
    # bitişik (contiguous) olmalı
    exp = []; acc = 1
    for s in reversed(t.size): exp.insert(0, acc); acc *= s
    if list(t.stride) != exp: raise SystemExit(f'bitişik değil {k}')
    data = raw[t.offset * 4:(t.offset + n) * 4]
    fn = k.replace('.', '_') + '.f32'
    open(f'{outdir}/{fn}', 'wb').write(data)
    index[k] = {'file': fn, 'shape': list(t.size)}
json.dump(index, open(f'{outdir}/index.json', 'w'), indent=1)
print(len(index), 'tensör'); [print(' ', k, v['shape']) for k, v in list(index.items())[:14]]
