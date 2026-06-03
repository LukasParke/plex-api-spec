# Library & Metadata Domain Review

**Domain:** Library, Library Collections, Library Playlists, Collections, Metadata, Media, Part, Stream  
**Date:** 2026-06-03  
**Spec file:** `plex-api-spec.yaml` (≈17k lines, OpenAPI 3.1.1)

---

## Endpoints Present in Spec (inventory with assessment)

### Root Library Endpoints

| Path | Methods | Tag | Assessment |
|------|---------|-----|------------|
| `/library/all` | GET | Library | **Partial** — only documents `mediaQuery`; missing `type`, `sort`, filters, include/exclude flags |
| `/library/caches` | DELETE | Library | ✅ Complete |
| `/library/clean/bundles` | PUT | Library | ✅ Complete |
| `/library/collections` | POST | Collections | **Partial** — creation params present but collection-specific response fields under-documented |
| `/library/file` | POST | Library | ✅ Complete |
| `/library/matches` | GET | Library | ✅ Complete |
| `/library/optimize` | PUT | Library | ✅ Complete |
| `/library/randomArtwork` | GET | Library | ✅ Complete |
| `/library/tags` | GET | Library | ✅ Complete |

### Library Sections

| Path | Methods | Tag | Assessment |
|------|---------|-----|------------|
| `/library/sections/all` | GET | Library | ✅ Complete |
| `/library/sections/all/refresh` | DELETE | Library | ✅ Complete |
| `/library/sections/prefs` | GET | Library | ✅ Complete |
| `/library/sections/refresh` | POST | Library | ✅ Complete |
| `/library/sections/{sectionId}` | GET, PUT, DELETE | Library | **Partial** — missing `edit` body schema; `PUT` params under-documented |
| `/library/sections/{sectionId}/albums` | GET | Content | ✅ Complete |
| `/library/sections/{sectionId}/all` | GET, PUT | Content | **Partial** — GET missing `type`, `sort`, tag filters, include/exclude matrix; PUT field-editing schema is descriptive only |
| `/library/sections/{sectionId}/allLeaves` | GET | Content | ✅ Complete |
| `/library/sections/{sectionId}/analyze` | POST | Library | ✅ Complete |
| `/library/sections/{sectionId}/arts` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/autocomplete` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/categories` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/cluster` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/collections` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/common` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/computePath` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/emptyTrash` | PUT | Library | ✅ Complete |
| `/library/sections/{sectionId}/filters` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/firstCharacters` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/indexes` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/intros` | POST | Library | ✅ Complete |
| `/library/sections/{sectionId}/location` | GET, POST, DELETE | Library | ✅ Complete |
| `/library/sections/{sectionId}/moment` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/nearest` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/prefs` | GET, PUT | Library | ✅ Complete |
| `/library/sections/{sectionId}/refresh` | DELETE, POST | Library | ✅ Complete |
| `/library/sections/{sectionId}/sorts` | GET | Library | ✅ Complete |
| `/library/sections/{sectionId}/collection/{collectionId}` | DELETE | Library | ✅ Complete |
| `/library/sections/{sectionId}/composite/{updatedAt}` | GET | Library | ✅ Complete |

### Metadata Items

| Path | Methods | Tag | Assessment |
|------|---------|-----|------------|
| `/library/metadata/{ids}` | GET, PUT, DELETE | Content / Library | **Partial** — GET has `checkFiles`, `skipRefresh`, `asyncAugmentMetadata` but missing `includeMarkers`, `includeChapters`, `includeExtras`, `includeRelated`, `includeOnDeck`, `includePopularLeaves`, `includeReviews`, `includeStations`, `includeExternalMedia`, `excludeElements`, `excludeFields`; PUT body schema is `args: object` (opaque) |
| `/library/metadata/{ids}/addetect` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/allLeaves` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/analyze` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/chapterThumbs` | POST | Library | ✅ Complete |
| `/library/metadata/{ids}/credits` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/extras` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/file` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/index` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/intro` | GET, PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/marker` | GET, POST | Library | ✅ Complete |
| `/library/metadata/{ids}/match` | PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/matches` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/merge` | PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/nearest` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/prefs` | GET, PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/refresh` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/related` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/similar` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/split` | PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/subtitles` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/tree` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/unmatch` | PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/users/top` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/voiceActivity` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/augmentations/{augmentationId}` | GET | Library | ✅ Complete |
| `/library/metadata/{ids}/media/{mediaItem}` | PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/marker/{marker}` | DELETE, PUT | Library | ✅ Complete |
| `/library/metadata/{ids}/{element}` | POST, PUT | Library | ✅ Complete — supports `thumb`, `art`, `clearLogo`, `banner`, `poster`, `theme` |
| `/library/metadata/{ids}/{element}/{timestamp}` | GET | Library | ✅ Complete |
| `/library/metadata/augmentations/{augmentationId}` | GET, DELETE | Library | ✅ Complete |

### Media, Parts, Streams, People

| Path | Methods | Tag | Assessment |
|------|---------|-----|------------|
| `/library/parts/{partId}` | GET, PUT | Library | ✅ Complete |
| `/library/parts/{partId}/indexes/{index}` | GET | Library | ✅ Complete |
| `/library/parts/{partId}/indexes/{index}/{offset}` | GET | Library | ✅ Complete |
| `/library/parts/{partId}/{changestamp}/{filename}` | GET | Library | ✅ Complete |
| `/library/people/{personId}` | GET | Library | ✅ Complete |
| `/library/people/{personId}/media` | GET | Library | ✅ Complete |
| `/library/streams/{streamId}/levels` | GET | Library | ✅ Complete |
| `/library/streams/{streamId}/loudness` | GET | Library | ✅ Complete |
| `/library/streams/{streamId}.{ext}` | GET | Library | ✅ Complete |
| `/library/media/{mediaId}/chapterImages/{chapter}` | GET | Library | ✅ Complete |

### Collections

| Path | Methods | Tag | Assessment |
|------|---------|-----|------------|
| `/library/collections/{collectionId}/items` | GET, PUT | Library Collections | ✅ Complete |
| `/library/collections/{collectionId}/items/{itemId}` | DELETE | Library Collections | ✅ Complete |
| `/library/collections/{collectionId}/items/{itemId}/move` | PUT | Library Collections | ✅ Complete |
| `/library/collections/{collectionId}/composite/{updatedAt}` | GET | Library Collections | ✅ Complete |

### Playlists

| Path | Methods | Tag | Assessment |
|------|---------|-----|------------|
| `/playlists` | GET, POST | Playlist / Library Playlists | **Partial** — missing `type=42` (optimized/conversion items) query param documentation |
| `/playlists/upload` | POST | Library Playlists | ✅ Complete |
| `/playlists/{playlistId}` | GET, PUT, DELETE | Playlist / Library Playlists | ✅ Complete |
| `/playlists/{playlistId}/generators` | GET | Library Playlists | ✅ Complete |
| `/playlists/{playlistId}/items` | GET, POST, DELETE | Library Playlists | ✅ Complete |
| `/playlists/{playlistId}/items/{generatorId}` | DELETE | Library Playlists | ✅ Complete |
| `/playlists/{playlistId}/items/{generatorId}/items` | GET, POST | Library Playlists | ✅ Complete |
| `/playlists/{playlistId}/items/{playlistItemId}/move` | PUT | Library Playlists | ✅ Complete |
| `/playlists/{playlistId}/items/{generatorId}/{metadataId}/{action}` | PUT | Library Playlists | ✅ Complete |

---

## Missing Endpoints

### Section Browsing & Filtering (used by official clients)

| Path | Method | Purpose | Evidence |
|------|--------|---------|----------|
| `/library/sections/{id}/onDeck` | GET | On-deck items for this section | Client traffic / community knowledge |
| `/library/sections/{id}/unwatched` | GET | Unwatched items | Client traffic |
| `/library/sections/{id}/newest` | GET | Newest additions | Client traffic |
| `/library/sections/{id}/byYear` | GET | Browse by year | Client traffic |
| `/library/sections/{id}/byDecade` | GET | Browse by decade | Client traffic |
| `/library/sections/{id}/byContentRating` | GET | Browse by content rating | Client traffic |
| `/library/sections/{id}/byResolution` | GET | Browse by resolution | Client traffic |
| `/library/sections/{id}/byFolder` | GET | Browse by folder | Client traffic |
| `/library/sections/{id}/agents` | GET | Available agents for this section | Client traffic |
| `/library/sections/{id}/match` | GET | Match items in section | Client traffic |
| `/library/sections/{id}/unmatch` | GET | Unmatch items in section | Client traffic |
| `/library/sections/{id}/edit` | GET / PUT | Edit section metadata | Client traffic |
| `/library/sections/{id}/move` | PUT | Move section paths | Client traffic |
| `/library/sections/{id}/settings` | GET | Section-specific settings | Client traffic |
| `/library/sections/{id}/playlists` | GET | Playlists belonging to section | Client traffic |
| `/library/sections/{id}/hubs` | GET | Hubs for this section | Client traffic |
| `/library/sections/{id}/timeline` | GET | Section timeline | Client traffic |
| `/library/sections/{id}/search` | GET | Section-scoped search | Client traffic |
| `/library/sections/{id}/tags` | GET | Tags in section | Client traffic |
| `/library/sections/{id}/artists` | GET | Artists (music) | Client traffic |
| `/library/sections/{id}/shows` | GET | Shows (TV) | Client traffic |
| `/library/sections/{id}/episodes` | GET | Episodes | Client traffic |
| `/library/sections/{id}/movies` | GET | Movies | Client traffic |
| `/library/sections/{id}/clips` | GET | Clips | Client traffic |
| `/library/sections/{id}/photos` | GET | Photos | Client traffic |
| `/library/sections/{id}/recentlyAdded` | GET | Per-library recently added | Tautulli |

### Global & Hub Recently Added

| Path | Method | Purpose | Evidence |
|------|--------|---------|----------|
| `/library/recentlyAdded` | GET | Global recently added | Tautulli |
| `/hubs/home/recentlyAdded` | GET | Hub-centric recently added | Tautulli |

### Metadata Sub-Endpoints

| Path | Method | Purpose | Evidence |
|------|--------|---------|----------|
| `/library/metadata/{id}/children` | GET | Children of show/season/artist/album | SDK (`key` attribute) |
| `/library/metadata/{id}/onDeck` | GET | On-deck for this show/season | Client traffic |
| `/library/metadata/{id}/reviews` | GET | User reviews | Client traffic |
| `/library/metadata/{id}/parent` | GET | Parent metadata shortcut | Client traffic |
| `/library/metadata/{id}/grandparent` | GET | Grandparent metadata shortcut | Client traffic |
| `/library/metadata/{id}/grandchildren` | GET | Grandchildren (e.g. episodes under show) | Tautulli, python-plexapi |

### Note on Poster / Art Upload

The spec documents `/library/metadata/{ids}/{element}` (POST/PUT) with `element` enum including `poster`, `art`, `thumb`, `banner`, `clearLogo`, `theme`. This covers the upload functionality Kometa uses, but **Kometa and other tools call specific paths** (`/library/metadata/{id}/posters`, `/library/metadata/{id}/arts`). The generic endpoint is present, but dedicated path aliases are not explicitly listed.

---

## Schema Corrections

### `Metadata` Schema

The `Metadata` schema (`#/components/schemas/Metadata`) is the central type for movies, shows, episodes, tracks, etc. It uses `additionalProperties: true`, which masks missing fields. The following fields are **not documented** but are parsed by `python-plexapi` from XML/JSON responses:

| Field | Found In | Notes |
|-------|----------|-------|
| `artBlurHash` | `video.py`, `audio.py` | Blur hash for background art |
| `thumbBlurHash` | `video.py`, `audio.py` | Blur hash for thumbnail |
| `lastRatedAt` | `video.py`, `audio.py` | Timestamp of last user rating |
| `editionTitle` | `video.py` (Movie) | Edition string (e.g. "Director's Cut") |
| `languageOverride` | `video.py` (Movie, Show) | Per-item language override |
| `enableCreditsMarkerGeneration` | `video.py` (Movie, Show) | Credits marker flag |
| `useOriginalTitle` | `video.py` (Movie, Show) | Display original title flag |
| `slug` | `video.py` (Movie, Show) | URL-friendly slug |
| `skipCount` | `audio.py` (Track) | Number of times skipped |
| `musicAnalysisVersion` | `audio.py` (Audio base) | Analysis version for music |
| `distance` | `audio.py` (Audio base) | Sonic similarity distance |
| `sourceURI` | `video.py`, `audio.py`, `playlist.py` | Remote/shared server item URI |
| `playlistItemID` | `base.py` (Playable) | Item ID within a playlist |
| `playQueueItemID` | `base.py` (Playable) | Item ID within a play queue |

**Type-specific gap:** The `Metadata` schema is a flat union. It does **not** distinguish type-specific required/optional fields (e.g. `year` is optional for episodes, `parentIndex` is season number, `grandparentTitle` is show name). Tools must infer field applicability by `type`.

### `Media` Schema

| Field | Found In | Notes |
|-------|----------|-------|
| `uuid` | `media.py` | Media instance UUID |
| `selected` | `media.py` | Whether this media version is selected |

*Note:* `title` is present in spec ✅.

### `Part` Schema

| Field | Found In | Notes |
|-------|----------|-------|
| `protocol` | `media.py` | Streaming protocol (e.g. `dash`, `hls`) |
| `packetLength` | `media.py` | RTP packet length |
| `requiredBandwidths` | `media.py` | Bandwidth requirements list |
| `syncItemId` | `media.py` | Mobile sync item association |
| `syncState` | `media.py` | Sync state (e.g. `pending`, `downloaded`) |
| `deepAnalysisVersion` | `media.py` | Deep analysis version |

*Note:* `decision` is present in `MediaContainerWithDecision` ✅.

### `Stream` Schema

The `Stream` schema covers video, audio, and subtitle streams. Many audio-specific loudness and subtitle-specific fields are missing:

#### AudioStream gaps

| Field | Notes |
|-------|-------|
| `bitrateMode` | e.g. `cbr`, `vbr` |
| `visualImpaired` | Audio description track flag |
| `albumGain` | ReplayGain album gain |
| `albumPeak` | ReplayGain album peak |
| `albumRange` | ReplayGain album range |
| `endRamp` | Loudness ramp end |
| `gain` | Track replay gain |
| `loudness` | Integrated loudness (LUFS) |
| `lra` | Loudness range |
| `peak` | Track peak |
| `startRamp` | Loudness ramp start |

#### SubtitleStream gaps

| Field | Notes |
|-------|-------|
| `providerTitle` | Subtitle provider name |
| `score` | Match confidence score |
| `sourceKey` | Source identifier |
| `transient` | Temporary/downloaded subtitle |
| `userID` | User who added subtitle |
| `perfectMatch` | Exact match flag |

#### LyricStream gaps

| Field | Notes |
|-------|-------|
| `minLines` | Minimum lines in lyric file |
| `provider` | Lyric provider |
| `timed` | Whether lyrics are timestamped |

### `Collection` Schema

**There is no dedicated `Collection` schema in the spec.** Collections appear to reuse `Metadata` (or are returned inside `MediaContainerWithMetadata`). The following collection-specific fields are missing:

| Field | Notes |
|-------|-------|
| `collectionFilterBasedOnUser` | Smart-collection user filter |
| `collectionMode` | Display mode (`default`, `hideItems`, `showItems`) |
| `collectionPublished` | Whether published to Plex Discover |
| `collectionSort` | Sort order for collection |
| `artBlurHash` | Blur hash for collection art |
| `thumbBlurHash` | Blur hash for collection thumb |
| `userRating` | User star rating |
| `lastRatedAt` | Rating timestamp |

### `Playlist` Schema

Playlists in the spec are defined via `MediaContainerWithPlaylistMetadata`, which extends `Metadata` with a few extra fields. Missing fields:

| Field | Notes |
|-------|-------|
| `durationInSeconds` | Total duration in seconds (redundant but present in XML) |
| `radio` | Whether this is a generated radio playlist |
| `titleSort` | Sort-friendly title |

*Note:* `librarySectionID`, `librarySectionKey`, `librarySectionTitle` are present ✅.

---

## Parameter/Query Gaps

### Missing or Under-Documented on `/library/sections/{sectionId}/all`

The GET method only documents `includeMeta`, `includeGuids`, `sectionId`, `mediaQuery`, `X-Plex-Container-Start`, `X-Plex-Container-Size`. Widely used but **absent** params:

| Parameter | Purpose |
|-----------|---------|
| `type` | Filter by metadata type (`1`=movie, `2`=show, `3`=season, `4`=episode, `8`=artist, `9`=album, `10`=track) |
| `sort` | Sort key and direction (e.g. `addedAt:desc`, `titleSort`) |
| `filters` / `unwatched` (`1`) | General filtering |
| `genre`, `studio`, `contentRating`, `resolution`, `year`, `firstCharacter` | Tag-based filters |
| `includeCollections` | Include collection items in results |
| `includeExternalMedia` | Include external/online media |
| `includeAdvanced` | Include advanced settings |
| `checkFiles` | Verify file existence |
| `includeRelated` | Include related items |
| `includeExtras` | Include trailers, behind-the-scenes, etc. |
| `includePopularLeaves` | Include popular episodes |
| `includeConcerts` | Include concert items |
| `includeOnDeck` | Include On Deck status |
| `includeChapters` | Include chapter markers |
| `includePreferences` | Include user preferences |
| `includeBandwidths` | Include bandwidth info |
| `includeLoudnessRamps` | Include loudness ramp data |
| `includeStations` | Include radio station data |
| `includeExternalIds` | Include external GUIDs |
| `includeReviews` | Include user reviews |
| `includeCredits` | Include full credits |
| `includeArt`, `includeThumb`, `includeBanner`, `includeTheme` | Force inclusion of artwork fields |
| `includeFields` | Whitelist of fields to return |
| `asyncAugmentMetadata` | Async metadata augmentation |
| `asyncRefreshLocalMediaAgent` | Async local media agent refresh |
| `nocache` | Bypass cache |
| `excludeFields` | Blacklist of fields to omit |
| `skipRefresh` | Skip synchronous refresh |

### Missing on `/library/metadata/{ids}`

| Parameter | Purpose | Notes |
|-----------|---------|-------|
| `includeMarkers` | Intro/credits markers | Critical for Tautulli and skip-intro clients |
| `includeChapters` | Chapter data | Missing from spec GET params |
| `includeExternalMedia` | External media | Missing |
| `includeExtras` | Extras/trailers | Missing |
| `includeRelated` | Related items | Missing |
| `includeOnDeck` | On Deck status | Missing |
| `includePopularLeaves` | Popular episodes | Missing |
| `includeReviews` | User reviews | Missing |
| `includeStations` | Radio stations | Missing |
| `includeGuids` | External GUIDs | Only documented on `/library/sections/{id}/all` |
| `excludeElements` | Omit elements | Mentioned only in history endpoint description |
| `excludeFields` | Omit fields | Mentioned only in history endpoint description |

### Other Parameter Gaps

| Parameter | Where It Should Be | Notes |
|-----------|-------------------|-------|
| `type=42` | `/playlists` | Optimized/conversion items (python-plexapi `optimizedItems()`, `conversions()`) |
| `includeCollections=1` | `/hubs/search` | Tautulli uses this for collection-in-search |
| `playlistType` | `/playlists` | Present ✅ |
| `sectionID` | `/playlists` | Present ✅ |
| `asyncAugmentMetadata=1` | `/library/metadata/{ids}` | Present on GET ✅ (query param `asyncAugmentMetadata`) |

---

## Documentation Improvements

1. **Dedicate a `Collection` schema.** Collections are not vanilla `Metadata` items. They carry `collectionMode`, `collectionSort`, `collectionPublished`, `collectionFilterBasedOnUser`, and blur hashes. Reusing `Metadata` with `additionalProperties: true` hides these fields from generated SDKs.

2. **Add `Playlist` schema fields.** `durationInSeconds`, `radio`, and `titleSort` are real XML attributes that python-plexapi relies on.

3. **Document blur hashes and loudness fields.** These are XML-first fields (`artBlurHash`, `thumbBlurHash`, `loudness`, `gain`, `albumGain`, etc.) that do not always appear in JSON unless requested. The spec should note XML vs JSON behavior.

4. **Expand `/library/sections/{id}/all` query parameters.** This is one of the most trafficked endpoints. Missing `type`, `sort`, tag filters, and the include/exclude matrix forces SDK users to hand-craft query strings.

5. **Document `includeMarkers=1` on metadata endpoints.** Intro/credits skip detection is a first-class feature in modern Plex. Tautulli and many clients depend on this parameter.

6. **Add missing section sub-endpoints.** `/onDeck`, `/unwatched`, `/newest`, `/byYear`, `/byDecade`, `/byContentRating`, `/byResolution`, `/byFolder`, `/recentlyAdded` are all used by official Plex clients and are well-known in the community.

7. **Add global `/library/recentlyAdded` and `/hubs/home/recentlyAdded`.** These are standard "what's new" endpoints used by Tautulli and dashboards.

8. **Add `/library/metadata/{id}/children`, `/parent`, `/grandparent`, `/grandchildren`.** These hierarchy shortcuts prevent excessive round-trips for show→season→episode traversal.

9. **Clarify `PUT /library/metadata/{ids}` body schema.** The current spec uses `args: object`, which is opaque. Document editable fields (title, summary, tag locks, etc.).

10. **Document `sourceURI` behavior.** Cross-server playlist/collection items use `sourceURI` pointing to other servers. This multi-server awareness pattern is not described.

11. **Add missing `Stream` fields.** Audio loudness (`lra`, `peak`, `gain`, `startRamp`, `endRamp`), subtitle metadata (`providerTitle`, `score`, `perfectMatch`), and lyric metadata (`minLines`, `provider`, `timed`) should be added.

12. **Add missing `Part` fields.** `protocol`, `packetLength`, `requiredBandwidths`, `syncItemId`, `syncState`, `deepAnalysisVersion` are needed for sync and transcode clients.

13. **Add missing `Media` fields.** `uuid` and `selected` are present in real responses.

14. **Document the `_INCLUDES` / `_EXCLUDES` pattern.** python-plexapi's `PlexPartialObject.reload()` uses a matrix of include/exclude parameters. A reusable parameter component (e.g. `#/components/parameters/includeExcludeMatrix`) would keep the spec DRY.
