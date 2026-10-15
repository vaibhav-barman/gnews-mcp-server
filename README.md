# GNews MCP Server

An MCP server that provides tools for searching GNews articles and retrieving
top headlines.

## Requirements

- Python 3.14 or newer
- A GNews API key

Set the API key in the environment where the server will run:

```sh
export GNEWS_API_KEY="your-api-key"
```

Install the project and start the server over stdio:

```sh
uv sync
uv run gnews-mcp-server
```

## Tools

- `search_news`: Search by query, with optional language, country, date range,
	searched fields, sort order, result count, and page.
- `get_top_headlines`: Retrieve headlines by category, with optional query,
	language, country, date range, result count, and page.

Both tools return the GNews API response, including article data and pagination
metadata. Result counts are limited to 1-100, and paging is limited to the
first 1000 results as required by GNews.

## MCP client configuration

For an MCP client that launches local stdio servers, configure the server with
the project path and API key, for example:

```json
{
	"mcpServers": {
		"gnews": {
			"command": "uv",
			"args": ["--directory", "/path/to/gnews-mcp-server", "run", "gnews-mcp-server"],
			"env": {
				"GNEWS_API_KEY": "your-api-key"
			}
		}
	}
}
```
