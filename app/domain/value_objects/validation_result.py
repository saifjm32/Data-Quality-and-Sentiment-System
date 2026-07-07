from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: list[str]

    @classmethod
    def valid(cls) -> "ValidationResult":
        return cls(is_valid=True, errors=[])

    @classmethod
    def invalid(cls, errors: list[str]) -> "ValidationResult":
        return cls(is_valid=False, errors=errors)