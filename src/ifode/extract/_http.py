"""GET sobre HTTPS com o que as fontes publicas exigem na pratica.

Duas pegadinhas, ambas descobertas contra o servidor real:

* **User-Agent.** `gov.br` devolve 403 para o `Python-urllib/3.x` padrao e 200
  para qualquer outro. Nos identificamos com o nome do projeto -- e o minimo
  para um raspador de pesquisa em portal publico.
* **gzip.** A API do IBGE responde comprimido mesmo sem `Accept-Encoding`, e o
  urllib nao descomprime sozinho.
"""

from __future__ import annotations

import gzip
import json
import logging
import urllib.request

log = logging.getLogger("ifode.extract.http")

USER_AGENT = "ifode-research/0.1 (+https://github.com/mrcsvg/yetdsp)"
TIMEOUT_PADRAO = 300


def baixar(url: str, timeout: int = TIMEOUT_PADRAO) -> bytes:
    """Corpo da resposta, ja descomprimido."""
    log.debug("GET %s", url)
    pedido = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"}
    )
    with urllib.request.urlopen(pedido, timeout=timeout) as r:  # noqa: S310
        corpo = r.read()
        comprimido = r.headers.get("Content-Encoding") == "gzip"
    if comprimido or corpo[:2] == b"\x1f\x8b":
        corpo = gzip.decompress(corpo)
    return corpo


def get_json(url: str, timeout: int = TIMEOUT_PADRAO):
    return json.loads(baixar(url, timeout).decode("utf-8"))
