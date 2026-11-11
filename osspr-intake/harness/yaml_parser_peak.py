"""Peak memory of YAMLParser.read on a document of repeated records.

PyYAML's safe loader composes a node for every scalar before it builds the
Python objects, so the node graph and the values are live at the same time.
The input bytes are allocated before tracing. The returned text is str() of
the loaded document, a few hundred kilobytes; the peak is tens of megabytes.
"""

from __future__ import annotations

import io

import yaml

from forge.utils.file_operations import YAMLParser

from _measure import peak_bytes, run_repeated

RECORDS = 5_000


def _document() -> bytes:
    records = [{"i": index, "t": "x" * 40} for index in range(RECORDS)]
    return yaml.safe_dump({"rows": records}).encode()


def main() -> None:
    payload = _document()

    def read() -> str:
        return YAMLParser().read(io.BytesIO(payload))

    run_repeated(lambda: float(peak_bytes(read)), warmup=read)


if __name__ == "__main__":
    main()
