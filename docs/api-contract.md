# Plex API Contract

## Decision: OpenAPI 3.1

PlexAPI.dev describes the Plex Media Server HTTP API as a curated, versioned [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html) contract. This decision is aligned with the [SDK generation strategy](./sdk-generation-strategy), which calls for a single source of truth that feeds both reference documentation and SDK generation.

### Why OpenAPI 3.1

| Consideration | Rationale |
|---------------|-----------|
| **Tooling maturity** | OpenAPI 3.1 is supported by Swagger Parser, OpenAPI Generator, Spectral, and many documentation generators. |
| **JSON Schema alignment** | OpenAPI 3.1 schemas are valid JSON Schema 2020-12 drafts, making it easy to reuse models for validation and SDK types. |
| **SDK generation** | OpenAPI Generator and Microsoft Kiota both consume OpenAPI 3.1, matching the hybrid SDK strategy. |
| **Documentation generation** | Reference pages can be generated or hand-written from the same contract, keeping docs and code in sync. |

## Contract location

The canonical contract lives at:

```text
plex-api-spec.yaml
```

This file is the single source of truth for the Plex Media Server API. The [PlexAPI.dev documentation site](https://plexapi.dev) and the community SDKs consume this contract.

## Validation

The contract is validated on every change via:

```bash
pnpm install
pnpm spec:validate
pnpm spec:lint
```

## Security notes

- The contract declares `X-Plex-Token` as an `apiKey` security scheme.
- Token values are never included in the spec or generated examples.
- Examples and guides instruct users to load tokens from environment variables or secure configuration.
