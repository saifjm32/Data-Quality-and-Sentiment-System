from abc import ABC, abstractmethod

from app.domain.entities.analysis_result import AnalysisResult


class AnalysisRepository(ABC):

    @abstractmethod
    def save(self, result: AnalysisResult) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[AnalysisResult]:
        pass

    @abstractmethod
    def get_by_record_id(self, record_id: str) -> AnalysisResult | None:
        pass