import os
from typing import Any, Literal

from dotenv import load_dotenv

load_dotenv()

import httpx
from mcp.server.fastmcp import FastMCP

load_dotenv()  # type: ignore 

GNEWS_API_URL = "https://gnews.io/api/v4"

mcp = FastMCP("GNews")


def _fetch(endpoint: str, params: dict[str, str | int | None]) -> dict[str, Any]:
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        raise RuntimeError("GNEWS_API_KEY is not set")

    request_params = {key: value for key, value in params.items() if value is not None}
    request_params["apikey"] = api_key

    try:
        response = httpx.get(
            f"{GNEWS_API_URL}/{endpoint}",
            params=request_params,
            timeout=20.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"GNews API returned HTTP {error.response.status_code}"
        ) from None
    except httpx.RequestError as error:
        raise RuntimeError(
            f"Unable to reach the GNews API ({type(error).__name__})"
        ) from None

    try:
        return response.json()
    except ValueError:
        raise RuntimeError("GNews API returned an invalid JSON response") from None


def _validate_paging(max_results: int, page: int) -> None:
    if not 1 <= max_results <= 100:
        raise ValueError("max_results must be between 1 and 100")
    if page < 1 or page * max_results > 1000:
        raise ValueError("page must select results within the first 1000 articles")


def _optional_params(
    lang: str | None,
    country: str | None,
    nullable: str | None,
    from_date: str | None,
    to_date: str | None,
    page: int,
    truncate_content: bool,
) -> dict[str, str | int | None]:
    return {
        "lang": lang,
        "country": country,
        "nullable": nullable,
        "from": from_date,
        "to": to_date,
        "page": page,
        "truncate": "content" if truncate_content else None,
    }


@mcp.tool()
def search_news(
    query: str,
    lang: str | None = None,
    country: str | None = None,
    max_results: int = 10,
    search_in: str | None = None,
    nullable: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    sort_by: Literal["publishedAt", "relevance"] = "publishedAt",
    page: int = 1,
    truncate_content: bool = False,
) -> dict[str, Any]:
    """Search GNews articles by keywords and optional filters."""
    if not query.strip() or len(query) > 200:
        raise ValueError("query must contain 1 to 200 characters")
    _validate_paging(max_results, page)

    params = _optional_params(
        lang, country, nullable, from_date, to_date, page, truncate_content
    )
    params.update(
        {
            "q": query,
            "max": max_results,
            "in": search_in,
            "sortby": sort_by,
        }
    )
    return _fetch("search", params)


@mcp.tool()
def get_top_headlines(
    category: Literal[
        "general",
        "world",
        "nation",
        "business",
        "technology",
        "entertainment",
        "sports",
        "science",
        "health",
    ] = "general",
    query: str | None = None,
    lang: str | None = None,
    country: str | None = None,
    max_results: int = 10,
    nullable: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    page: int = 1,
    truncate_content: bool = False,
) -> dict[str, Any]:
    """Get GNews top headlines by category and optional filters."""
    if query is not None and (not query.strip() or len(query) > 200):
        raise ValueError("query must contain 1 to 200 characters")
    _validate_paging(max_results, page)

    params = _optional_params(
        lang, country, nullable, from_date, to_date, page, truncate_content
    )
    params.update({"category": category, "q": query, "max": max_results})
    return _fetch("top-headlines", params)


def main() -> None:
    mcp.run(transport="stdio")
