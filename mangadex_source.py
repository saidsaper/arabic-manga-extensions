# MangaDex Extension for Komikku
# Author: ChatGPT
# License: Apache-2.0

from extensions_lib import (
    Source,
    Manga,
    Chapter,
    Page,
    MangaListQuery,
    ChapterListQuery,
    PageListQuery,
    ClientSession,
    JSON
)

class MangaDex(Source):
    def __init__(self):
        super().__init__(
            name="MangaDex",
            base_url="https://api.mangadex.org",
            lang=["en", "ar"],
            version="1.0",
            source_id=1001
        )

    async def search_manga(self, query: MangaListQuery) -> JSON:
        params = {"title": query.title, "limit": 20}
        async with ClientSession() as session:
            res = await session.get(f"{self.base_url}/manga", params=params)
            return await res.json()

    async def parse_manga_list(self, data: JSON) -> list[Manga]:
        out = []
        for entry in data.get("data", []):
            attr = entry["attributes"]
            out.append(Manga(
                id=entry["id"],
                title=attr["title"].get("en") or attr["title"].get("ja") or "No title",
                thumbnail=f"https://uploads.mangadex.org/covers/{entry['id']}/{attr['coverArt'][0]['fileName']}" if attr.get("coverArt") else None
            ))
        return out

    async def get_chapters(self, manga: Manga) -> JSON:
        async with ClientSession() as session:
            res = await session.get(f"{self.base_url}/manga/{manga.id}/feed", params={"translatedLanguage": ["en","ar"], "order[chapter]": "asc"})
            return await res.json()

    async def parse_chapter_list(self, data: JSON) -> list[Chapter]:
        out = []
        for chap in data.get("data", []):
            out.append(Chapter(
                id=chap["id"],
                title=f"Chapter {chap['attributes'].get('chapter')}",
                number=float(chap["attributes"].get("chapter") or 0)
            ))
        return out

    async def get_page_list(self, chapter: Chapter) -> JSON:
        async with ClientSession() as session:
            res = await session.get(f"{self.base_url}/at-home/server/{chapter.id}")
            return await res.json()

    async def parse_page_list(self, data: JSON) -> list[Page]:
        base_url = data["baseUrl"]
        return [Page(f"{base_url}/{p}") for p in data.get("chapter", {}).get("data", [])]

    async def get_cover(self, manga: Manga) -> str | None:
        return manga.thumbnail
