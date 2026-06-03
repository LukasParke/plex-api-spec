# Media Provider & Content Domain Review

**Date:** 2026-06-03  
**Scope:** Tags `Provider`, `Content`, `Hubs`, `Search`, `Rate`, `Playlist` (partial) and paths `/media/providers/*`, `/hubs/*`, `/media/providers/refresh`, `/media/subscriptions/*`, `/playlists/*`.  
**Sources:** `plex-api-spec.yaml`, `python_plexapi_gap_analysis.md`, `integration_ecosystem_gaps.md`, `undocumented_endpoints_research.md`.

---

## Endpoints Present in Spec

### Provider

| Method | Path | Summary | Notes |
|--------|------|---------|-------|
| `GET` | `/media/providers` | List providers | Response schema inherits from `ServerConfiguration` |
| `POST` | `/media/providers` | Add a provider | Only `url` query param documented |
| `POST` | `/media/providers/refresh` | Refresh providers | — |
| `DELETE`| `/media/providers/{provider}` | Delete a provider | — |

### Content (selected representative endpoints)

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/library/metadata/{ratingKey}` | Get metadata item(s) |
| `DELETE`| `/library/metadata/{ratingKey}` | Delete metadata item(s) |
| `GET` | `/library/sections/{sectionId}/all` | List section items |
| `GET` | `/library/sections/{sectionId}/allLeaves` | All leaves |
| `GET` | `/library/sections/{sectionId}/albums` | Music albums |
| `GET` | `/library/sections/{sectionId}/categories` | Categories |
| `GET` | `/library/sections/{sectionId}/cluster` | Clusters (photos) |
| `GET` | `/library/sections/{sectionId}/computePath` | Sonic path |
| `GET` | `/library/sections/{sectionId}/nearest` | Sonically similar tracks |
| `GET` | `/library/sections/{sectionId}/location` | Folder locations |
| `GET` | `/library/sections/{sectionId}/moment` | Moments (photos) |
| `GET` | `/library/collections/{collectionId}/items` | Collection items |
| `GET` | `/library/collections/{collectionId}/composite/{updatedAt}` | Collection image |

### Hubs

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/hubs` | Global hubs |
| `GET` | `/hubs/continueWatching` | Continue watching hub |
| `GET` | `/hubs/items` | Items for a specific hub (by `identifier`) |
| `GET` | `/hubs/promoted` | Promoted hubs |
| `GET` | `/hubs/search` | Search across libraries (hub results) |
| `GET` | `/hubs/search/voice` | Voice search |
| `GET` | `/hubs/metadata/{metadataId}` | Hubs for a metadata item (music) |
| `GET` | `/hubs/metadata/{metadataId}/postplay` | Post-play hubs |
| `GET` | `/hubs/metadata/{metadataId}/related` | Related hubs |
| `GET` | `/hubs/sections/{sectionId}` | Section hubs |
| `GET` | `/hubs/sections/{sectionId}/manage` | List built-in & custom hubs |
| `DELETE`| `/hubs/sections/{sectionId}/manage` | Reset hubs to defaults |
| `PUT` | `/hubs/sections/{sectionId}/manage/move` | Re-order a hub |
| `PUT` | `/hubs/sections/{sectionId}/manage/{identifier}` | Update hub visibility |

### Search

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/hubs/search` | Standard search |
| `GET` | `/hubs/search/voice` | Voice search |

### Rate

| Method | Path | Summary |
|--------|------|---------|
| `PUT` | `/:/rate` | Rate an item (`identifier`, `key`, `rating`, `ratedAt`) |

### Playlist

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/playlists` | List playlists |
| `POST` | `/playlists` | Create playlist |
| `POST` | `/playlists/upload` | Import m3u playlist |
| `GET` | `/playlists/{playlistId}` | Retrieve playlist |
| `PUT` | `/playlists/{playlistId}` | Edit playlist metadata |
| `DELETE`| `/playlists/{playlistId}` | Delete playlist |
| `GET` | `/playlists/{playlistId}/generators` | List generators |
| `GET` | `/playlists/{playlistId}/items` | List items |
| `DELETE`| `/playlists/{playlistId}/items` | Clear playlist |
| `PUT` | `/playlists/{playlistId}/items` | Add items |
| `PUT` | `/playlists/{playlistId}/items/{generatorId}/items` | Add generator items |
| `PUT` | `/playlists/{playlistId}/items/{playlistItemId}/move` | Move item |
| `PUT` | `/playlists/{playlistId}/items/{generatorId}/{metadataId}/{action}` | Generator actions |

---

## Missing Endpoints (including cloud providers)

### Cloud / External Providers

These are used by official clients and major integrations (Overseerr, Jellyseerr, Tautulli, python-plexapi) but are **absent** from the spec.

| Provider Host | Missing Paths | Purpose |
|---------------|---------------|---------|
| `discover.provider.plex.tv` | `GET /library/search` | Discover search (movies & shows) |
| `discover.provider.plex.tv` | `GET /library/sections/watchlist/all` | Plex Discover watchlist |
| `discover.provider.plex.tv` | `POST /actions/addToWatchlist` | Add to watchlist |
| `discover.provider.plex.tv` | `POST /actions/removeFromWatchlist` | Remove from watchlist |
| `metadata.provider.plex.tv` *(deprecated)* | `GET /library/sections/watchlist/all` | Legacy watchlist |
| `metadata.provider.plex.tv` *(deprecated)* | `POST /actions/addToWatchlist` | Legacy add |
| `metadata.provider.plex.tv` *(deprecated)* | `POST /actions/removeFromWatchlist` | Legacy remove |
| `vod.provider.plex.tv` | `GET /hubs` | VOD hub items |
| `music.provider.plex.tv` | `GET /hubs` | Tidal / music hub items |

> **Note:** `metadata.provider.plex.tv` was deprecated in late 2025 in favor of `discover.provider.plex.tv`. The spec should document the current endpoints and include a deprecation notice for the old host.

### Hub Endpoints

| Missing Path | Method | Used By | Why It Matters |
|--------------|--------|---------|----------------|
| `/hubs/home/recentlyAdded` | `GET` | Tautulli, official clients | Global recently-added hub view |
| `/hubs/continueWatching/items` | `GET` | python-plexapi (`PlexServer.continueWatching()`) | Direct access to CW items without wrapping in a hub container |

### Provider Proxy Endpoints

The spec only documents `DELETE /media/providers/{provider}`. No proxy paths for the individual provider features are defined. In practice, PMS reverse-proxies the following feature paths for each registered provider:

- `/{provider}/search`
- `/{provider}/metadata`
- `/{provider}/content`
- `/{provider}/match`
- `/{provider}/manage`
- `/{provider}/timeline`
- `/{provider}/rate`
- `/{provider}/playqueue`
- `/{provider}/playlist`
- `/{provider}/subscribe`
- `/{provider}/promoted`
- `/{provider}/continuewatching`
- `/{provider}/collection`
- `/{provider}/actions`
- `/{provider}/imagetranscoder`
- `/{provider}/queryParser`
- `/{provider}/grid`

These should at minimum be referenced in the `Provider` tag description or documented as dynamic paths.

---

## Schema Corrections

### `/media/providers` Response Schema

The `GET /media/providers` response uses:

```yaml
allOf:
  - $ref: '#/components/schemas/ServerConfiguration'
  - properties:
      Feature: ...
      identifier: ...
      protocols: ...
      title: ...
      types: ...
```

**Issues:**

1. **Wrong base schema.** `ServerConfiguration` is server-global (includes `machineIdentifier`, `version`, `transcoderActiveVideoSessions`, etc.). A provider list should likely extend `MediaContainer` or a dedicated `ProviderContainer`.
2. **Underspecified `Feature` array.** Each `Feature` contains a `Directory[]` referencing the generic `Directory` schema. The spec does not enumerate the well-known feature types (`search`, `metadata`, `content`, `match`, `manage`, `timeline`, `rate`, `playqueue`, `playlist`, `subscribe`, `promoted`, `continuewatching`, `collection`, `actions`, `imagetranscoder`, `queryParser`, `grid`).
3. **Missing provider-level fields.** Real-world responses include additional fields (e.g., `icon`, `hubKey`, `featureKey`) that are not documented.

**Recommendation:** Create a `Provider` schema and a `ProviderFeature` schema that explicitly documents the known feature keys and their directory structures.

### `Hub` Schema

The `Hub` schema (`components/schemas/Hub`) is reasonably complete for the fields it documents (`hubIdentifier`, `key`, `Metadata`, `more`, `promoted`, `random`, `size`, `style`, `subtype`, `totalSize`). However:

- It sets `additionalProperties: true`, which masks the fact that several fields observed in client traffic (e.g., `context`, `hubKey`, `reason`, `reasonTitle`, `reasonID`) are not formally described.
- The `Metadata` items reference the base `Metadata` schema, which is missing fields commonly returned in hub contexts (see below).

### `Metadata` / Content Schema Gaps (hub-relevant)

Per `python_plexapi_gap_analysis.md`, the `Metadata` schema is missing fields that appear in XML/JSON hub and search responses:

- `artBlurHash`, `thumbBlurHash`
- `lastRatedAt`
- `editionTitle`, `languageOverride`, `enableCreditsMarkerGeneration`, `useOriginalTitle`, `slug`
- `sourceURI`
- `playlistItemID`, `playQueueItemID`

### `Playlist` Schema Gaps

- `durationInSeconds`, `radio`, `titleSort` are missing from the playlist metadata schema.

---

## Parameter/Query Gaps

### Search Parameters

| Endpoint | Missing / Under-documented Parameter | Impact |
|----------|--------------------------------------|--------|
| `GET /hubs/search` | `includeCollections` (boolean) | Tautulli and other clients use this to include collection results in search hubs. **Not documented.** |
| `GET /hubs/search` | Query syntax details | No documentation on field filters (e.g., `title:`, `actor:`), partial-match behavior, or spell-check heuristics. |
| `GET /hubs/search/voice` | `includeCollections` | Same gap as standard search. |

### Hub Pagination

- `X-Plex-Container-Start` and `X-Plex-Container-Size` are documented as **response headers** on hub endpoints, but they are also sent by clients as **request headers** (or query parameters) for pagination. The spec should clarify that these may be used as request headers.

### Rate Endpoint

| Endpoint | Gap |
|----------|-----|
| `PUT /:/rate` | No `DELETE` method documented. In Plex, sending `rating=0` effectively removes the rating, but this is not described. |
| `PUT /:/rate` | `rating` is typed as `number` (0–10). It should note that fractional values (e.g., `8.5`) are accepted for star ratings. |

### Provider Endpoints

- `POST /media/providers` only documents `url`. Other query parameters that may be accepted (e.g., `identifier`, `title`, `protocols`) are not listed.

---

## Documentation Improvements

1. **Provider Response Features**
   - Document the `Feature` directory types in `/media/providers` responses. Provide an enum or descriptive list for the known feature keys (`search`, `metadata`, `content`, `match`, `manage`, `timeline`, `rate`, `playqueue`, `playlist`, `subscribe`, `promoted`, `continuewatching`, `collection`, `actions`, `imagetranscoder`, `queryParser`, `grid`).

2. **Cloud Provider Deprecation & Migration**
   - Add a deprecation note for `metadata.provider.plex.tv` and document the canonical `discover.provider.plex.tv` endpoints (search, watchlist, add/remove actions).
   - Document `vod.provider.plex.tv` and `music.provider.plex.tv` base paths at a high level so SDK generators know these hosts exist.

3. **Search Query Syntax**
   - Expand the `/hubs/search` and `/hubs/search/voice` operation descriptions to explain:
     - How query strings are tokenized.
     - That partial matches and spell-check are applied.
     - The effect of `includeCollections=1`.
     - The meaning of `reason`, `reasonTitle`, and `reasonID` in search results.

4. **Pagination Clarification**
   - Add a note to all `Hub` and `Playlist` endpoints that pagination can be driven by sending `X-Plex-Container-Start` and `X-Plex-Container-Size` as **request headers** (in addition to documenting them as response headers).

5. **Rate Endpoint Semantics**
   - Clarify that `rating=0` clears the user rating.
   - Mention that the endpoint also responds to `GET` but `PUT` is the preferred verb.

6. **Missing Hub Endpoints**
   - Add `/hubs/home/recentlyAdded` and `/hubs/continueWatching/items` to the Hubs tag.

7. **Schema Field Additions**
   - Add missing `Metadata` fields (`artBlurHash`, `thumbBlurHash`, `lastRatedAt`, `sourceURI`, etc.) where they are known to appear in hub and search responses.
   - Add missing `Playlist` fields (`durationInSeconds`, `radio`, `titleSort`).

---

*End of review.*
