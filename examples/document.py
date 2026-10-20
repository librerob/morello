from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    path: Path
    content: str

    def excerpt(self, limit: int = 120) -> str:
        """Return a short preview of the document."""
        if limit < 1:
            raise ValueError("limit must be positive")
        text = self.content.strip()
        if len(text) <= limit:
            return text
        prefix = text[:limit].rsplit(" ", 1)[0]
        return prefix.rstrip() + "…"


def read_document(path: Path) -> Document:
    content = path.read_text(encoding="utf-8")
    return Document(path=path, content=content)
