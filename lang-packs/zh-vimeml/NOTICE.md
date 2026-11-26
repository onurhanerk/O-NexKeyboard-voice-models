# Licensing and attribution

vimeml-tiny-zh-v1 weights, tokenizer, Core ML packages and the included VimeML code are licensed under the GNU General Public License version 3 or (at your option) any later version, with the additional permission in `LICENSE-EXCEPTION` for conveyance through application distribution services such as the App Store. The License text is in `LICENSE`.

## Training data attribution

Applications that bundle this model must show the model license and the following attribution. The terms of each corpus are independent of the model license. This repository contains no training text.

| Source | Terms | Link |
| --- | --- | --- |
| FineWeb2 `cmn_Hani` (Hugging Face; derived from Common Crawl) | ODC-By 1.0, also subject to the Common Crawl Terms of Use | https://huggingface.co/datasets/HuggingFaceFW/fineweb-2 |
| LCCC-base (thu-coai; Yida Wang, Pei Ke, Yinhe Zheng, Kaili Huang, Yong Jiang, Xiaoyan Zhu, Minlie Huang, *A Large-Scale Chinese Short-Text Conversation Dataset*, NLPCC 2020) | MIT (repository license and dataset card). The repository README additionally states that the dataset and pretrained dialogue models are provided for research purposes. | https://github.com/thu-coai/CDial-GPT |

## Evaluation-only sources

CrossWOZ (Apache-2.0), RiSAWOZ (MIT), KdConv (Apache-2.0) and CPED (Apache-2.0 repository license) were used for evaluation only. They do not enter the weights; this repository distributes aggregate metrics, not their text.

## Third-party software

SentencePiece and other runtime dependencies are installed separately and keep their upstream licenses. `source/` is the unchanged snapshot of the recorded source commit.
