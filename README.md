# O-NexKeyboard Voice Models

OBoard (O-NexKeyboard) uygulamasının sesli yazma özelliği için sherpa-onnx streaming ASR model dosyaları.
Bu depo sadece ikili model dosyalarını barındırır, kaynak kod içermez.

## Dil paketleri (`lang-packs/`)

- `ja-zenz-v3.1-small.gguf` — Japonca gelişmiş kana → kanji dönüşümü (OBoard "Gelişmiş dönüşüm").
  Kaynak: [Miwa-Keita/zenz-v3.1-small-gguf](https://huggingface.co/Miwa-Keita/zenz-v3.1-small-gguf)
  (`ggml-model-Q5_K_M.gguf`), lisans **CC BY-SA 4.0**. Değişiklik: resmi llama.cpp'nin yükleyebilmesi
  için GGUF meta verisindeki `tokenizer.ggml.pre` değeri `gpt2-small-japanese-char` → `gpt-2` yapıldı;
  ağırlıklar aynı.
- `zh-vimeml-tiny-v1.bin` — Çince pinyin adaylarını bağlama göre yeniden sıralama (OBoard "Gelişmiş dönüşüm").
  Kaynak: [Voltline/vimeml-tiny-zh-v1](https://huggingface.co/Voltline/vimeml-tiny-zh-v1)
  (`inference/weights.pt`, `inference/tokenizer.model`), lisans **GPL-3.0-or-later** + uygulama mağazası istisnası
  (`lang-packs/zh-vimeml/LICENSE`, `LICENSE-EXCEPTION`); eğitim verisi atfı `lang-packs/zh-vimeml/NOTICE.md`.
  Değişiklik: FP32 ağırlıklar fp16'ya yuvarlanıp SentencePiece parçalarıyla tek dosyada birleştirildi.
  Karşılık gelen kaynak: özgün ağırlıklar (yukarıdaki bağlantı) + bu klasördeki dönüştürme betikleri
  (`pt_extract.py` → `spm_extract.py` → `build_vime_pack.py`).

### Parçalar (`lang-packs/parts/`)

Aynı dosyaların 19 MB'lık parçaları (`split -b 19922944 -d -a 2`; `cat *.part* >` ile birleşir, bayt bayt aynı).
GitHub'a erişilemeyen yerlerde (ör. Çin) uygulama bunları jsDelivr üzerinden indirir; jsDelivr tek dosyada
20 MB üstünü vermiyor.
