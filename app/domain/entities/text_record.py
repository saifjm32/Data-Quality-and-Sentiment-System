from dataclasses import dataclass


@dataclass(frozen=True)
class TextRecord:
    record_id: str
    text: str

    def normalized_text(self) -> str:
        return self.text.strip()

    def is_empty(self) -> bool:
        return self.normalized_text() == ""