# Playback & Sessions Domain Review

**Date:** 2026-06-03  
**Spec file:** `plex-api-spec.yaml` (≈17 k lines)  
**Review scope:** Tags `Status`, `Timeline`, `Play Queue`, `Transcoder`; paths `/status/sessions/*`, `/:/timeline`, `/:/scrobble`, `/:/unscrobble`, `/playQueues/*`, `/{transcodeType}/:/transcode/universal/*`, `/photo/:/transcode`.

---

## Endpoints Present in Spec

| Path | Method | Tag | Notes |
|------|--------|-----|-------|
| `POST /playQueues` | POST | Play Queue | Creates a queue. Inline response schema contains play-queue fields. |
| `GET /playQueues/{playQueueId}` | GET | Play Queue | Retrieves a queue window. |
| `PUT /playQueues/{playQueueId}` | PUT | Play Queue | Add generator / playlist to queue. |
| `DELETE /playQueues/{playQueueId}/items` | DELETE | Play Queue | Clear all items. |
| `PUT /playQueues/{playQueueId}/reset` | PUT | Play Queue | Reset to first item. |
| `PUT /playQueues/{playQueueId}/shuffle` | PUT | Play Queue | Shuffle (no Up Next). |
| `PUT /playQueues/{playQueueId}/unshuffle` | PUT | Play Queue | Restore natural order. |
| `DELETE /playQueues/{playQueueId}/items/{playQueueItemId}` | DELETE | Play Queue | Delete single item. |
| `PUT /playQueues/{playQueueId}/items/{playQueueItemId}/move` | PUT | Play Queue | Move item after another. |
| `GET /status/sessions` | GET | Status | Lists active sessions (admin only). |
| `GET /status/sessions/background` | GET | Status | Lists background transcode jobs. |
| `GET /status/sessions/history/all` | GET | Status | Lists playback history. |
| `GET /status/sessions/history/{historyId}` | GET | Status | Get single history item. |
| `DELETE /status/sessions/history/{historyId}` | DELETE | Status | Delete single history item. |
| `POST /status/sessions/terminate` | POST | Status | Kill a session by ID. |
| `POST /:/timeline` | POST | Timeline | **Only POST is documented.** Report playback state / progress. |
| `PUT /:/scrobble` | PUT | Timeline | Mark item as played (no view history created). |
| `PUT /:/unscrobble` | PUT | Timeline | Mark item as unplayed. |
| `GET /photo/:/transcode` | GET | Transcoder | Image resize/format transcode. |
| `GET /{transcodeType}/:/transcode/universal/decision` | GET | Transcoder | Playback decision (MDE). |
| `POST /{transcodeType}/:/transcode/universal/fallback` | POST | Transcoder | Force transcoder fallback. |
| `GET /{transcodeType}/:/transcode/universal/subtitles` | GET | Transcoder | Subtitle-only transcode. |
| `GET /{transcodeType}/:/transcode/universal/start.{extension}` | GET | Transcoder | Start session (`m3u8` or `mpd`). |
| `GET /:/websocket/notifications` | GET | Events | **Singular** `websocket` path. Returns binary stream. |

**Observations**
- `/:/timeline` is documented as **POST only**. There is no `GET /:/timeline` in the spec. Client timeline polling is done via `/player/timeline/poll` (missing).
- `/:/scrobble` and `/:/unscrobble` are documented as **PUT only**, with a note that they respond to GET but should not be used.
- `/playQueues/{playQueueId}` (GET) and most play-queue mutators reuse response reference `#/components/responses/slash-post-responses-200`, which resolves to `MediaContainerWithPlaylistMetadata`. That schema is playlist-centric and does **not** contain play-queue top-level fields (`playQueueID`, `playQueueSelectedItemID`, etc.).

---

## Missing Endpoints

### WebSocket / Real-Time Events
| Missing Path | Why it matters |
|--------------|----------------|
| `GET /:/websockets/notifications` (plural) | Tautulli and Home Assistant connect to this **plural** path for real-time session & timeline events. The spec documents the singular `/:/websocket/notifications` under `Events`, but the plural path is the one widely used in the wild. Both should be documented, or at minimum the plural path should be noted as an alias. |

### Client Remote-Control Protocol
The Plex Client Control Protocol is entirely absent from the spec. These endpoints are proxied through PMS via `X-Plex-Target-Client-Identifier`.

| Missing Path | Purpose |
|--------------|---------|
| `GET /resources` | Client capabilities / device info (used by `PlexClient` discovery). |
| `GET /player/timeline/poll` | Poll a client’s local playback timeline. |
| `POST /player/playback/play` | Start playback on client. |
| `POST /player/playback/pause` | Pause client. |
| `POST /player/playback/stop` | Stop client. |
| `POST /player/playback/seek` | Seek to time. |
| `POST /player/playback/skipTo` | Skip to item. |
| `POST /player/playback/skipBy` | Skip forward/backward. |
| `POST /player/playback/stepForward` | Step forward. |
| `POST /player/playback/stepBack` | Step back. |
| `POST /player/playback/setParameters` | Set shuffle/repeat/volume. |
| `POST /player/playback/subtitleStream` | Change subtitle stream. |
| `POST /player/playback/audioStream` | Change audio stream. |
| `POST /player/playback/videoStream` | Change video stream. |
| `POST /player/playback/volume` | Set volume. |
| `POST /player/playback/mute` | Mute. |
| `POST /player/playback/unmute` | Unmute. |
| `POST /player/playback/setTextStream` | Set text stream. |
| `POST /player/playback/setRating` | Rate item. |
| `POST /player/playback/setViewOffset` | Set resume offset. |
| `POST /player/playback/setState` | Set playback state. |
| `POST /player/playback/refreshPlayQueue` | Refresh play queue. |
| `POST /player/playback/playMedia` | Play specific media on client. |

### Transcode Sessions & Segment Delivery
| Missing Path | Purpose |
|--------------|---------|
| `GET /{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.m4s` | DASH segment delivery. |
| `GET /{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.ts` | HLS TS segment delivery. |
| `GET /music/:/transcode` | Audio transcode endpoint (distinct from universal video transcoder). |

---

## Schema Corrections

### PlayQueue
- **Missing shared schema:** There is no standalone `PlayQueue` schema. The creation endpoint (`POST /playQueues`) defines play-queue fields (`playQueueID`, `playQueueLastAddedItemID`, `playQueueSelectedItemID`, `playQueueSelectedItemOffset`, `playQueueSelectedMetadataItemID`, `playQueueShuffled`, `playQueueSourceURI`, `playQueueTotalCount`, `playQueueVersion`) inline in its 200 response.
- **Reuse mismatch:** All other play-queue operations (GET, shuffle, unshuffle, reset, move, delete item, clear) return `#/components/schemas/MediaContainerWithPlaylistMetadata`. That schema contains **playlist** fields (`playlistType`, `smart`, `composite`, `leafCount`, etc.) and **omits** every play-queue field listed above.
- **Gap:** `playQueueSelectedMetadataItemID` is present in the creation response, but absent from `MediaContainerWithPlaylistMetadata`. Because the spec reuses the playlist schema for play-queue responses, generated SDKs will not expose play-queue properties on retrieval.
- **Recommendation:** Create a proper `MediaContainerWithPlayQueue` schema that includes both the queue metadata fields and the `Metadata` item array, and reference it from all play-queue endpoints.

### Session
- The `Session` schema (line 15863) is extremely sparse:
  ```yaml
  Session:
    properties:
      bandwidth: integer
      id: string
      location: string  # enum: [lan, wan]
  ```
- Real session objects returned in `/status/sessions` include additional fields such as `sessionKey`, `uuid`, `title`, `userID`, etc. The current schema does not model these.
- **Recommendation:** Expand `Session` or document that the object is intentionally minimal and that consumers should rely on the embedded `Player`, `User`, and `Metadata` objects.

### History
- The history response schema (`/status/sessions/history/all`, line 3770+) defines an inline object with:
  `accountID`, `deviceID`, `historyKey`, `key`, `librarySectionID`, `originallyAvailableAt`, `ratingKey`, `thumb`, `title`, `type`, `viewedAt`.
- Real history items include fields like `guid`, `index`, `parentKey`, `parentRatingKey`, `grandparentKey`, `grandparentRatingKey`, `parentThumb`, `grandparentThumb`, `content`, `viewCount`, `lastViewedAt`, etc., depending on metadata type.
- **Recommendation:** Derive history items from `Metadata` (or a `HistoryItem` allOf) so that type-specific fields are not lost.

### Timeline Response
- The `POST /:/timeline` 200 response schema extends `ServerConfiguration` and adds `Bandwidths`, `terminationCode`, `terminationText`.
- This is reasonable, but the response can also include a `playQueueID` when playback originates from a queue, which is not documented.
- **Recommendation:** Add `playQueueID` (integer) to the timeline response schema.

---

## Parameter / Query Gaps

### `POST /:/timeline`
The spec documents: `key`, `ratingKey`, `state`, `playQueueItemID`, `time`, `duration`, `continuing`, `updated`, `offline`, `timeToFirstFrame`, `timeStalled`, `bandwidth`, `bufferedTime`, `bufferedSize`, plus `X-Plex-Client-Identifier` and `X-Plex-Session-Identifier` headers.

**Missing / under-documented:**

| Parameter | Where observed | Gap |
|-----------|----------------|-----|
| `containerKey` | Official Plex clients | Used to group timeline reports (e.g., `/playQueues/123`). Not in spec. |
| `playQueueID` | Official Plex clients | Distinct from `playQueueItemID`; identifies the queue itself. Not in spec. |
| `guid` | Client traffic | Global unique identifier for the item being reported. Not in spec. |
| `url` | Legacy clients | Alternative to `key`/`ratingKey`. Mentioned in `scrobble` description but absent from timeline. |

Also, the `state` enum is `stopped | buffering | playing | paused`. This matches common usage, but some clients also send `ready` — verify if this is still current.

### `GET /status/sessions/history/all`
- The description mentions `includeFields`, `excludeFields`, `includeElements`, and `excludeElements`, but these are **not declared as formal query parameters**.
- Pagination is described in text, but `X-Plex-Container-Start` and `X-Plex-Container-Size` are only documented as **response headers**, not request parameters. Many clients send them as query parameters or headers for pagination.
- Missing filter parameters observed in SDK usage: `viewedAt>` (greater-than), `viewedAt<` (less-than), `accountID`, `deviceID`, `metadataItemID` (the latter three are present, but range operators on `viewedAt` are not formally described).

### `GET /status/sessions`
- No query parameters are listed. Real usage sometimes includes `X-Plex-Container-Start` / `X-Plex-Container-Size` for large session lists, though this is rare.

### `POST /status/sessions/terminate`
- `sessionId` and `reason` are present. Looks complete for the documented surface.

### Scrobble / Unscrobble (`PUT /:/scrobble`, `PUT /:/unscrobble`)
- Parameters: `identifier`, `key`, `uri`.
- `identifier` is documented as required; `key` and `uri` are optional (one must be provided).
- No gaps here, but the description of `uri` refers to "See intro for description of the URIs" — the spec does not actually contain that introductory URI section.

### Transcoder (`/decision`, `/start.{extension}`, `/subtitles`, `/fallback`)
- Heavily parameterized; the spec is fairly comprehensive.
- **Missing** from all transcoder endpoints:
  - `maxVideoBitrate` (client-side cap, distinct from `videoBitrate` / `peakBitrate`)
  - `videoResolution` (cap string)
  - `copyts` (boolean for timestamp copying)
  - `mediaIndex` / `partIndex` are present on `/decision` and `/start`, but not on `/subtitles`
  - `platform` query param (some clients send this in addition to headers)

### Play Queue Creation (`POST /playQueues`)
- Missing parameter observed in SDKs: `limit` (to cap initial window size). Not documented.
- Missing parameter: `next` is documented on `PUT /playQueues/{playQueueId}` (add to queue) but a `next` semantic on creation is not addressed.

---

## Documentation Improvements

1. **Clarify HTTP verbs for scrobble/unscrobble**
   - The spec notes these "respond to GET but applications should use PUT". This anti-pattern should be deprecated in documentation; only PUT should be shown in examples.

2. **Timeline polling frequency**
   - The `POST /:/timeline` description states "generally every 10 seconds on LAN/WAN, every 20 seconds over cellular." This is good, but should also mention that the server may reply with `terminationCode` / `terminationText` when a session is killed, and that clients must handle the 200 response body to detect server-side termination.

3. **Play Queue "Up Next" semantics**
   - The tag description (line 134) contains a lengthy explanation of the Up Next region, sliding window, and shuffle restrictions. This should be summarized or cross-linked in the operation descriptions for `POST /playQueues`, `PUT /playQueues/{playQueueId}/shuffle`, and `PUT /playQueues/{playQueueId}/unshuffle` so that consumers do not have to read the tag essay to understand why shuffle fails.

4. **History pagination**
   - The `listPlaybackHistory` description mentions pagination but does not declare `X-Plex-Container-Start` / `X-Plex-Container-Size` as request parameters. Add them explicitly (as headers or query params) and provide an example.

5. **Transcoder segment flow**
   - The spec documents `/start.{extension}` but does not explain that the returned manifest references segments under `/session/{sessionId}/{segmentId}.{ext}`. A short sequence diagram or note would help implementers understand the full playback flow.

6. **WebSocket path discrepancy**
   - Document that both `/:/websocket/notifications` (singular, in spec) and `/:/websockets/notifications` (plural, used by Tautulli/HA) exist, or add the plural path as a separate operation. Describe the `NotificationContainer`, `PlaySessionStateNotification`, `TimelineEntry`, and `StatusNotification` message shapes, which are currently absent.

7. **Client remote control proxy pattern**
   - Add a section explaining that `/player/*` endpoints can be invoked directly against a client or proxied through PMS using `X-Plex-Target-Client-Identifier`. This is a fundamental Plex architecture pattern that is missing from the spec entirely.

---

## Quick-Reference: Priority Matrix

| Gap | Impact | Effort |
|-----|--------|--------|
| Create `MediaContainerWithPlayQueue` schema and apply to all PQ endpoints | **High** | Medium |
| Add `/:/websockets/notifications` (plural) and message schemas | **High** | Medium |
| Add `/player/playback/*` and `/player/timeline/poll` endpoints | **High** | Large |
| Add `/resources` endpoint | **Medium** | Small |
| Add transcode segment delivery paths | **Medium** | Small |
| Expand `Session` schema | **Medium** | Small |
| Expand history inline schema | **Medium** | Medium |
| Add missing timeline query params (`containerKey`, `playQueueID`, `guid`) | **Medium** | Small |
| Declare `includeFields` / `excludeFields` / `includeElements` / `excludeElements` on history | **Low** | Small |
| Add `X-Plex-Container-Start` / `X-Plex-Container-Size` as request params on paginated endpoints | **Low** | Small |
