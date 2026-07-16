# Contributing

## How CI validates API updates

Three tiers, in order of increasing cost:

### 1. Static gate — `validate.yml` (every PR, forks included, ~3 min)

No secrets, no Docker. Blocks merge on:

- **Format** — prettier over `plex-api-spec.yaml`, `workflows/*.yaml`, `plugins/*.js`
- **OpenAPI lint** — redocly (`recommended`), speakeasy (pinned to the generator version), vacuum (pinned, checksum-verified, ratcheted `--min-score 25`)
- **Arazzo lint** — redocly structural rules plus `plex/operation-ref-resolves` (`plugins/arazzo-ref-rules.js`), which resolves every step's `operationId`/`operationPath` against `plex-api-spec.yaml` and checks path-parameter names. A dangling or typo'd reference fails here, not at runtime.

### 2. Contract tests — `contract-test.yml` (same-repo PRs and main)

Boots a throwaway PMS (docker compose) behind the Arbiter proxy with spec validation enabled, seeds a library section (`scripts/seed-library.sh`), and runs every Arazzo workflow with `redocly respect`. Fails on workflow assertion errors or Arbiter-reported spec gaps. Skipped on fork PRs (secrets unavailable) — the static gate still covers those.

### 3. Nightly discovery — `discovery.yml`

Synthetic traffic against a fresh PMS, diffed against the spec with `arbiter diff --exit-on-gap`. Undocumented endpoints/params fail the run and open-or-update a `spec-drift` issue; a clean run auto-closes it.

## Reproduce CI locally

```bash
npm ci
npm run validate   # prettier + redocly (incl. ref resolution)
npm run lint:speakeasy
```

Runtime tier locally:

```bash
export PLEX_CLAIM_TOKEN=<from https://plex.tv/claim>
docker compose up -d pms
# build arbiter from a sibling clone, then:
scripts/seed-library.sh    # needs PLEX_TOKEN
npx redocly respect workflows/server-health-check.yaml --input plexToken=... --input baseUrl=http://localhost:32400
```

## Adding an Arazzo workflow

1. Copy an existing file in `workflows/` as a template.
2. Reference operations by `operationId: $sourceDescriptions.plex-api.<operationId>` — the lint gate verifies it exists and that any `in: path` parameters match the operation's path template.
3. `npm run validate` before pushing.

## Rules of the road

- **Don't lower the bar.** Vacuum `--min-score` and the redocly ratchet rules (`operation-parameters-unique`, `no-path-trailing-slash`, currently `warn` for pre-existing issues) may only hold or improve.
- **Pinned everything.** Actions by SHA, tools by version (redocly in `package.json`, speakeasy/vacuum in `validate.yml`, Arbiter in `plex-harness/action.yml`, PMS in `docker-compose.yml`). Bumps are deliberate, via dependabot where possible.
