"""Model-origin policy shared by every repository check.

Project rule: no Chinese-origin models or their derivatives (fine-tunes,
distillations) in the catalog, examples, or Field Guide candidates. If a
model's base is unclear, ask a maintainer before adding it. See
SCOPE_EXPANSION_PLAN.md, rule 3.5.

Keep this the only place the denylist is written down.
"""
from __future__ import annotations

import re

# Case-insensitive patterns matched against model names, base models,
# publishers, and catalog URLs. Prefer specific tokens to avoid false positives.
DENYLIST: dict[str, str] = {
    r"qwen|qwq": "Qwen family (Alibaba)",
    r"deepseek": "DeepSeek",
    r"\b01-ai\b|\byi-(?:\d|large|lightning|coder|vl)": "Yi (01.AI)",
    r"chatglm|\bglm-\d|zhipu|thudm": "GLM / ChatGLM (Zhipu / THUDM)",
    r"baichuan": "Baichuan",
    r"internlm|internvl|shanghai[-_ ]?ai[-_ ]?lab": "InternLM / InternVL (Shanghai AI Lab)",
    r"minicpm|openbmb": "MiniCPM (OpenBMB)",
    r"moonshot|\bkimi\b": "Kimi (Moonshot AI)",
    r"hunyuan": "Hunyuan (Tencent)",
    r"\bernie\b|paddlepaddle|paddlenlp": "ERNIE / PaddleNLP (Baidu)",
    r"hanlp": "HanLP",
}
# Derivatives whose names don't reveal their base. Name matching alone can't
# catch these, so record each one here once its base model is verified.
KNOWN_DERIVATIVES: dict[str, str] = {
    r"nuextract[-_ ]?2": "NuExtract 2.x (fine-tuned from Qwen2.5-VL; verified 2026-10-12)",
}
_COMPILED = [(re.compile(p, re.IGNORECASE), label)
             for p, label in {**DENYLIST, **KNOWN_DERIVATIVES}.items()]


def violations(text: str) -> list[str]:
    """Return the denylisted family labels that appear in ``text``."""
    return [label for pattern, label in _COMPILED if pattern.search(text)]
