from dataclasses import dataclass


@dataclass
class VectorDataItem:
    image_url: str
    relevant_text: str
    page_url: str


@dataclass
class ScrapeSiteItem:
    src_url: str
    skip_url_patterns: list[str]
    max_depth: int
