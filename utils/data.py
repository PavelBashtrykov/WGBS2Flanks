from dataclasses import dataclass, field
import pandas as pd

@dataclass
class FlanksData:
    flank_length: int
    data: pd.DataFrame # columns: flank, count, methylation level

@dataclass
class Storage:
    """Data storage interface for Reader
    """
    file_name: str = ""
    data: list = field(default_factory=list)

    def add(self, some_data) -> None:
        self.data.append(some_data)

@dataclass
class ComputeFlanksDataStorage(Storage):
    data: list[FlanksData] = field(default_factory=list)
