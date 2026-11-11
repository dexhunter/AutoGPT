"""Peak memory of is_file_binary_fn on a large text file.

The function reads the whole file into one bytes object to look for a null
byte. The file is a real on-disk file: BytesIO.read() can return the buffer
the caller already holds, which would hide the copy open() performs.
"""

from __future__ import annotations

import os
import tempfile

from forge.utils.file_operations import is_file_binary_fn

from _measure import peak_bytes, run_repeated

FILE_BYTES = 16 * 1024 * 1024


def main() -> None:
    fd, path = tempfile.mkstemp(prefix="osspr-binary-", suffix=".log")
    try:
        with os.fdopen(fd, "wb") as handle:
            remaining = FILE_BYTES
            chunk = b"log line with ordinary text\n" * 1024
            while remaining:
                piece = chunk if remaining >= len(chunk) else chunk[:remaining]
                handle.write(piece)
                remaining -= len(piece)

        def check() -> bool:
            with open(path, "rb") as handle:
                return is_file_binary_fn(handle)

        run_repeated(lambda: float(peak_bytes(check)), warmup=check)
    finally:
        os.unlink(path)


if __name__ == "__main__":
    main()
