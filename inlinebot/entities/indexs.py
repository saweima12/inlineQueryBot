from dataclasses import dataclass
from inlinebot.services.meili import MeiliIndex
from meilisearch_python_async.models.settings import MeiliSearchSettings

@dataclass
class ConfigIndex(MeiliIndex):

    uid: str = "config"
    primary_key: str = "uid"

    setting = MeiliSearchSettings(
        searchable_attributes=["uid"],
        filterable_attributes=["uid"]
    )

@dataclass
class CheckedMediaIndex(MeiliIndex):

    uid = "checked"
    primary_key = "uid"

    setting = MeiliSearchSettings(
        searchable_attributes=["keywords", "uid"],
        filterable_attributes=["keywords", "uid"]
    )

@dataclass
class UnCheckedMediaIndex(MeiliIndex):
    
    uid = "unchecked"
    primary_key = "uid"
    setting = MeiliSearchSettings(
        searchable_attributes=["keywords", "media_type", "attach", "uid"],
        filterable_attributes=["keywords", "media_type", "attach", "uid"]
    )