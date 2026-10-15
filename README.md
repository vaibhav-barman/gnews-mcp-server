# GNews MCP Server

An MCP server built with FastMCP that exposes GNews search and top-headlines
tools over stdio.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- A GNews API key

Set `GNEWS_API_KEY` in the server environment, or add it to a `.env` file in
the project directory:

```sh
export GNEWS_API_KEY="your-api-key"
```

Install dependencies and launch the server:

```sh
uv sync
uv run gnews-mcp-server
```

The server uses stdio transport and is intended to be launched by an MCP
client.

## Tools

### `search_news`

Required argument: `query` (1-200 characters).

Optional arguments:

- `lang`, `country`: Two-letter language and country codes.
- `max_results`: Number of articles, from 1 to 100 (default: 10).
- `search_in`: Comma-separated fields: `title`, `description`, and/or `content`.
- `nullable`: Comma-separated article fields allowed to be null: `description`,
	`content`, and/or `image`.
- `from_date`, `to_date`: ISO 8601 publication date bounds.
- `sort_by`: `publishedAt` (default) or `relevance`.
- `page`: Page number, default 1. Requests are limited to the first 1000 results.
- `truncate_content`: When true, ask GNews to truncate article content.

### `get_top_headlines`

Optional arguments:

- `category`: `general` (default), `world`, `nation`, `business`, `technology`,
	`entertainment`, `sports`, `science`, or `health`.
- `query`: Optional keyword query (up to 200 characters).
- `lang`, `country`: Two-letter language and country codes.
- `max_results`: Number of articles, from 1 to 100 (default: 10).
- `nullable`: Comma-separated article fields allowed to be null: `description`,
	`content`, and/or `image`.
- `from_date`, `to_date`: ISO 8601 publication date bounds.
- `page`: Page number, default 1. Requests are limited to the first 1000 results.
- `truncate_content`: When true, ask GNews to truncate article content.

Both tools return the GNews API response, including article data and pagination
metadata. API errors are reported as tool errors.

## MCP client configuration

For an MCP client that launches local stdio servers, set the project directory
and provide the API key in the server environment:

```json
{
	"mcpServers": {
		"gnews": {
			"command": "uv",
			"args": [
				"--directory",
				"/path/to/gnews-mcp-server",
				"run",
				"gnews-mcp-server"
			],
			"env": {
				"GNEWS_API_KEY": "your-api-key"
			}
		}
	}
}
```

Keep API keys out of committed configuration files.
