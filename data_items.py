from dataclasses import dataclass


@dataclass
class VectorDataItem:
    image_url: str
    relevant_text: str
    page_url: str

