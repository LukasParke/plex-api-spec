# Plex Media Server OpenAPI Specification

An open source OpenAPI 3.1 specification for the Plex Media Server API.

- **Live docs:** [plexapi.dev](https://plexapi.dev)
- **Docs repository:** [LukasParke/plex-mintlify-docs](https://github.com/LukasParke/plex-mintlify-docs)
- **Original developer docs (being consolidated):** [LukasParke/plexapi-dev-docs](https://github.com/LukasParke/plexapi-dev-docs)

## What's in this repository

| File / directory | Purpose |
|------------------|---------|
| `plex-api-spec.yaml` | Canonical OpenAPI 3.1 contract for the Plex Media Server API. |
| `docs/` | Contributor documentation: contract decisions and SDK generation strategy. |
| `scripts/` | Validation, lint, diff, and reference-generation tooling. |
| `.github/workflows/spec-validate.yml` | CI that validates the spec on every PR and push to `main`. |

## Validation

```bash
pnpm install
pnpm spec:validate
pnpm spec:lint
pnpm spec:diff
```

## SDKs

Automation and SDKs are provided by [Speakeasy](https://www.speakeasyapi.dev/).
The following community SDKs are generated from this specification:

| Language              | Repository                                        | Releases                                                                                         | Other                                                   |
| --------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| Python                | [GitHub](https://github.com/LukeHagar/plexpy)     | [PyPI](https://pypi.org/project/plex-api-client/)                                                | -                                                       |
| JavaScript/TypeScript | [GitHub](https://github.com/LukeHagar/plexjs)     | [NPM](https://www.npmjs.com/package/@lukehagar/plexjs) \ [JSR](https://jsr.io/@lukehagar/plexjs) | -                                                       |
| Go                    | [GitHub](https://github.com/LukeHagar/plexgo)     | [Releases](https://github.com/LukeHagar/plexgo/releases)                                         | [GoDoc](https://pkg.go.dev/github.com/LukeHagar/plexgo) |
| Ruby                  | [GitHub](https://github.com/LukeHagar/plexruby)   | [Releases](https://github.com/LukeHagar/plexruby/releases)                                       | -                                                       |
| Swift                 | [GitHub](https://github.com/LukeHagar/plexswift)  | [Releases](https://github.com/LukeHagar/plexswift/releases)                                      | -                                                       |
| PHP                   | [GitHub](https://github.com/LukeHagar/plexphp)    | [Releases](https://github.com/LukeHagar/plexphp/releases)                                        | -                                                       |
| Java                  | [GitHub](https://github.com/LukeHagar/plexjava)   | [Releases](https://github.com/LukeHagar/plexjava/releases)                                       | -                                                       |
| C#                    | [GitHub](https://github.com/LukeHagar/plexcsharp) | [Releases](https://github.com/LukeHagar/plexcsharp/releases)                                     | -                                                       |

## Contributing

See [docs/api-contract.md](./docs/api-contract.md) and [docs/sdk-generation-strategy.md](./docs/sdk-generation-strategy.md) for design context.

To propose changes to the spec, open a pull request. The CI check `spec:validate` must pass before merge.
