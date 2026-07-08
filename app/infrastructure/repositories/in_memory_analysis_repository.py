from app.domain.entities.analysis_result import AnalysisResult
from app.domain.repositories.analysis_repository import AnalysisRepository


class InMemoryAnalysisRepository(AnalysisRepository):
    def __init__(self):
        self._results: list[AnalysisResult] = []

    def save(self, result: AnalysisResult) -> None:
        self._results.append(result)

    def get_all(self) -> list[AnalysisResult]:
        return self._results

    def get_by_record_id(self, record_id: str) -> AnalysisResult | None:
        for result in self._results:
            if result.record_id == record_id:
                return result

        return None