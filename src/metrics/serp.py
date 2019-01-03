import json
from typing import List

from dataclasses import dataclass


@dataclass
class SerpRequest:
    keywords: str
    location: str

    def get_id(self):
        return str(hash("%s%s" % (self.keywords, self.location)))


@dataclass
class SerpPosition:
    position: int
    url: str
    title: str


@dataclass
class SerpResponse:
    listing: List[SerpPosition]
    related_keywords: list

    def to_json(self):
        data = {
            'listing': [{'postion': p.position, 'url': p.url, 'title': p.title}
                        for p in self.listing],
            'related_keywords': self.related_keywords
        }
        return json.dumps(data)

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        return SerpResponse(
            [SerpPosition(p.get('postion'), p.get('url'), p.get('title'))
             for p in data.get('listing', [])],
            data.get('related_keywords'),
        )
