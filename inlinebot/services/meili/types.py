from dataclasses import dataclass, field
from meilisearch_python_async.models.settings import MeiliSearchSettings

@dataclass()
class MeiliIndex:
    uid: str = field(init=False)
    primary_key: str = field(init=False)
    setting: MeiliSearchSettings = field(init=False, default=None)
