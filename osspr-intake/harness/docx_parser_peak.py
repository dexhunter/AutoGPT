"""Peak memory of DOCXParser.read on a long document.

python-docx turns the package into an XML element tree and a paragraph
object per paragraph, then copies the paragraph text out with no separator.
The docx bytes are allocated before tracing, so the peak is that object model
plus the returned text.
"""

from __future__ import annotations

import io

import docx

from forge.utils.file_operations import DOCXParser

from _measure import peak_bytes, run_repeated

PARAGRAPHS = 8_000
PARAGRAPH = "Paragraph body " + ("word " * 20)


def _document() -> bytes:
    document = docx.Document()
    for index in range(PARAGRAPHS):
        document.add_paragraph(f"{index} {PARAGRAPH}")
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def main() -> None:
    payload = _document()

    def read() -> str:
        return DOCXParser().read(io.BytesIO(payload))

    run_repeated(lambda: float(peak_bytes(read)), warmup=read)


if __name__ == "__main__":
    main()
