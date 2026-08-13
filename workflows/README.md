# Plex API Arazzo Workflows

This directory contains [Arazzo 1.0.0](https://spec.openapis.org/arazzo/latest.html) workflow documents that describe common multi-step API interactions against a Plex Media Server. These workflows are designed for testing, documentation, and automation use cases.

## Prerequisites

- A running Plex Media Server (local or remote)
- A valid `X-Plex-Token` for authentication
- The [Plex API OpenAPI specification](../plex-api-spec.yaml) in the parent directory

## Workflow Files

| Workflow | File | Description | Steps |
|----------|------|-------------|-------|
| **Server Health Check** | `server-health-check.yaml` | Verifies server identity, features, and info | 3 |
| **Browse Library** | `browse-library.yaml` | Lists library sections then items within a section | 2 |
| **Search & Discover** | `search-and-discover.yaml` | Searches hubs, Discover, and recently added | 3 |
| **Manage Playlists** | `manage-playlists.yaml` | Lists playlists, creates new ones, gets watchlist | 3 |
| **Live TV Guide** | `live-tv-guide.yaml` | Lists DVRs, searches EPG, lists recordings | 3 |
| **User Management** | `user-management.yaml` | Gets account, home users, and server resources | 3 |

## Common Inputs

All workflows accept these inputs:

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `plexToken` | `string` | Yes | X-Plex-Token for authenticated requests |
| `baseUrl` | `string` | No | Plex server base URL (default: `http://localhost:32400`) |

## Usage with Arbiter

These workflows can be executed using the [Arbiter](https://github.com/LukasParke/arbiter) proxy's replay capabilities or any Arazzo-compatible test runner:

```bash
# Example: run the health check workflow
# (requires an Arazzo-compatible test runner)
```

## Workflow Structure

Each workflow follows the Arazzo specification:

- **`sourceDescriptions`** — References the Plex API OpenAPI spec
- **`workflows`** — Array of workflow definitions
  - **`workflowId`** — Unique identifier
  - **`inputs`** — JSON Schema for workflow parameters
  - **`steps`** — Ordered sequence of API operations
    - **`operationId`** — References an operation in the OpenAPI spec
    - **`parameters`** — Maps inputs to operation parameters
    - **`successCriteria`** — Runtime expressions for validation
    - **`outputs`** — Captures response data for downstream steps
  - **`outputs`** — Final workflow results

## Extending Workflows

To create a new workflow:

1. Copy an existing workflow file as a template
2. Define your `workflowId`, `summary`, and `description`
3. Specify required `inputs`
4. Add `steps` referencing operations from the Plex API spec
5. Use `$steps.<stepId>.outputs.<name>` to pass data between steps

See the [Arazzo specification](https://spec.openapis.org/arazzo/latest.html) for full syntax details.
