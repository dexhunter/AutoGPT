"""Peak memory of HTMLParser.read on a multi-megabyte HTML document.

BeautifulSoup builds a tag object for every element before get_text() copies
the text out. The input bytes are allocated before tracing, so the reported
peak is the parser's own high-water mark.
"""

from __future__ import annotations

import io

from forge.utils.file_operations import HTMLParser

from _measure import peak_bytes, run_repeated

PARAGRAPHS = 20_000


def _document() -> bytes:
    body = "".join(
        f"<p>Paragraph {index} " + ("word " * 40) + "</p>" for index in range(PARAGRAPHS)
    )
    return f"<html><body>{body}</body></html>".encode()


def main() -> None:
    html = _document()

    def read() -> str:
        return HTMLParser().read(io.BytesIO(html))

    run_repeated(lambda: float(peak_bytes(read)), warmup=read)


if __name__ == "__main__":
    main()
