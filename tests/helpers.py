from __future__ import annotations

import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


@contextmanager
def project_tmp_dir(prefix: str = "test") -> Iterator[Path]:
    """Create a writable temp directory inside the repository workspace."""
    root = Path(__file__).resolve().parents[1] / ".test_tmp"
    root.mkdir(exist_ok=True)
    path = root / f"{prefix}_{uuid.uuid4().hex}"
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
