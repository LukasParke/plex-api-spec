# Documentation-Only Review — Plex API Specification

**PR:** [#117](https://github.com/LukasParke/plex-api-spec/pull/117)
**Scope:** Issues we can fix in the spec itself (excludes Plex's actual API behavior)

---

## Critical (Fix Before Merge)

| # | Issue | Location | Suggested Fix |
|---|-------|----------|---------------|
| 1 | **~237 operations missing error responses** | Global (~60% of ops) | Add `$ref` to `components/responses/400`, `401`, `403`, `404` on every operation. At minimum `400` + `401` for authenticated endpoints. |
| 2 | **3 kebab-case `operationId`s** | `get-server-resources`, `get-users`, `post-users-sign-in-data` | Rename to `getServerResources`, `getUsers`, `postUsersSignInData`. |
| 3 | **5 `operationId`s contradict their HTTP method** | e.g., `GET /library/metadata/{ids}/subtitles` -> `addSubtitles` | Audit and rename to semantically correct IDs (e.g., `getSubtitles`). |
| 4 | **Malformed path parameter declaration** | `DELETE /library/streams/{streamId}.{ext}` declares `streamId}.{ext` | Correct to `{streamId}` and handle `.ext` appropriately. |
| 5 | **Response component missing `type: object`** | `components.responses.slash-get-responses-200` (~line 18657) | Add `type: object` to the schema. |
| 6 | **Schema properties missing `type`** | `MediaSubscription` properties (`Directory`, `Playlist`, `Video`) | Add `type: object` to each property. |
| 7 | **5 undefined tags in global `tags` array** | `Authentication`, `Playback`, `Playlists`, `Plex`, `Users` | Add tag definitions with descriptions to root `tags`. |
| 8 | **Duplicate global parameter declarations** | 16 transcode/timeline operations | Remove duplicate `X-Plex-*` param declarations already covered by `x-speakeasy-globals`. |

## High Priority

| # | Issue | Location | Suggested Fix |
|---|-------|----------|---------------|
| 9 | **146 error responses return `text/html` with no schema** | Global | Define a reusable `Error` schema and apply it to all `4xx`/`5xx` responses. |
| 10 | **5 unused schemas** | `Collection`, `Feature`, `PlayQueueResponse`, `ProviderFeature`, `UpdaterStatus` | Either wire them into operations via `$ref` or delete them. |
| 11 | **20 unstructured `200` responses** | e.g., `POST /auth/jwk`, `GET /geoip` | Add proper schemas (even partial ones) instead of bare `type: object` or `type: string`. |
| 12 | **Duplicate inline request body** | `PUT /pins/link` (JSON + form-urlencoded) | Extract to `components/schemas/LinkPinRequest` and `$ref` from both media types. |
| 13 | **Unnecessary single-item `allOf`** | 7 instances (e.g., `LibrarySection` date fields, `/activities`, `/updater/status`) | Replace `allOf: [{ $ref: ... }]` with direct `$ref`. |
| 14 | **18 duplicate enum sets** | `(0,1)` x14, `('lan','wan','cellular')` x4, etc. | Extract to reusable schemas (e.g., `BoolInt`, `NetworkType`, `StreamProtocol`). |
| 15 | **21 invalid examples** | e.g., `example: 135` on `type: string`, pattern mismatches | Correct example values to match schema constraints. |
| 16 | **`allOf` subschemas missing `type`** | `GET /resources` params `includeHttps`, `includeRelay`, `includeIPv6` | Add `type: integer` to inline subschemas. |
| 17 | **`PlexDateTime` unusual type syntax** | `components.schemas.PlexDateTime` | Change `type: [integer]` to `type: integer`. |
| 18 | **Tag fragmentation** | `Playlist` vs `Playlists` vs `Library Playlists`; `Collections` vs `Library Collections` | Consolidate to a single tag per domain. |
| 19 | **Path parameter naming inconsistency** | `{id}` vs `{userId}` vs `{uuid}` for same concept | Standardize per resource type (e.g., always `{userId}`). |
| 20 | **Security override inconsistency** | Some admin-only endpoints declare `security: [token: [admin]]`, others inherit global | Audit every endpoint and explicitly declare minimum required scope. |

## Medium Priority

| # | Issue | Location | Suggested Fix |
|---|-------|----------|---------------|
| 21 | **9 operations share identical summaries** | e.g., `GET` and `POST` `/library/optimize` both `"Optimize Library"` | Distinguish by HTTP method: `"Get Library Optimization Status"` / `"Optimize Library"`. |
| 22 | **`ids` path parameter has no description** | 28 paths using `{ids}` | Add description explaining it accepts comma-separated IDs. |
| 23 | **Vague one-word summaries** | `"Ping"`, `"Get Home"`, `"Upload"` | Expand to descriptive sentences. |
| 24 | **63 schemas lack descriptions** | `Activity`, `BoolInt`, `ButlerTask`, `Channel`, etc. | Add `description` to each schema for generated SDK docs. |
| 25 | **Missing `required` arrays** | 47 response schemas + 4 request bodies | Audit and add `required` for fields the server always returns/expects. |
| 26 | **`type` query parameter is a reserved word** | 15+ operations | Add `x-speakeasy-name-override` to rename in generated SDKs. |
| 27 | **`composite` parameter lacks description** | Global component parameter | Add a description explaining its purpose. |
| 28 | **Response `401` uses inline schema** | `components.responses.401` | Extract to `components.schemas.UnauthorizedErrorResponse` for consistency with `BadRequestErrorResponse`. |
| 29 | **Missing `x-speakeasy-retries` on rate-limited endpoints** | plex.tv auth endpoints (`/pins`, `/auth/token`, etc.) | Add retry config since docs warn about rate limits. |
| 30 | **Missing `x-speakeasy-pagination` metadata** | 2 operations flagged by Speakeasy | Add pagination extension where pagination is supported. |
| 31 | **786 description duplications** | Many responses use identical `"OK"` descriptions | Use `$ref` to shared response components or vary descriptions. |
| 32 | **556+ missing examples** | Pervasive across parameters and responses | Add `example` to every parameter and response media type. |

## Positive Findings

- All 154 `$ref`s resolve correctly
- All 404 `operationId`s are unique
- No `nullable: true` misuse (proper OAS 3.1 style)
- No `type: array` without `items`
- No trailing slash inconsistency
- CI passes cleanly (prettier, speakeasy, vacuum)
