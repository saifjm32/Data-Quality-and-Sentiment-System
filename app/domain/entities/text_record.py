from dataclasses import dataclass


@dataclass(frozen=True)
class TextRecord:
    record_id: str
    text: str
    source: str | None = None

    def normalized_text(self) -> str:
        return self.text.strip()

    def normalized_source(self) -> str:
        return "" if self.source is None else self.source.strip()

    def is_empty(self) -> bool:
        return self.normalized_text() == ""