# Integration Ecosystem API Gap Survey

This document surveys major open-source Plex integrations to identify API endpoints, parameters, and authentication patterns that are commonly used but missing or poorly documented in the official Plex OpenAPI spec (`plex-api-spec.yaml`).

---

## Tautulli API usage

Tautulli (`Tautulli/Tautulli`) is a Python-based monitoring and tracking tool that interacts heavily with both the local PMS and plex.tv APIs.

### PMS Endpoints Used

| Endpoint | Method | Purpose | Status in Spec |
|---|---|---|---|
| `/status/sessions` | GET | Active play sessions | **Present** |
| `/status/sessions/terminate` | GET | Kill a session by ID | **Present** |
| `/library/metadata/{ratingKey}?includeMarkers=1` | GET | Media metadata with intro/credits markers | **Partial** (`includeMarkers` param absent) |
| `/library/metadata/{ratingKey}/children` | GET | Season episodes, album tracks | **Present** |
| `/library/metadata/{ratingKey}/allLeaves` | GET | All descendant items | **Present** |
| `/library/metadata/{ratingKey}/grandchildren` | GET | Grandchildren (e.g. episodes under a show) | **Absent** |
| `/library/sections` | GET | List libraries | **Present** |
| `/library/sections/{sectionId}/all` | GET | Library contents | **Present** |
| `/library/sections/{sectionId}/recentlyAdded` | GET | Per-library recently added | **Absent** |
| `/library/sections/{sectionId}/label` | GET | Labels for a library | **Absent** |
| `/library/recentlyAdded` | GET | Global recently added | **Absent** |
| `/hubs/home/recentlyAdded` | GET | Hub-centric recently added | **Absent** |
| `/hubs/search?query=&limit=&includeCollections=1` | GET | Search with collection results | **Partial** (`includeCollections` not documented) |
| `/hubs/metadata/{ratingKey}/related` | GET | Related items in a collection | **Present** |
| `/playlists/{ratingKey}/items` | GET | Playlist items | **Present** |
| `/sync/items/{syncId}` | GET | Sync item details | **Absent** |
| `/sync/transcodeQueue` | GET | Sync transcode queue status | **Absent** |
| `/myplex/account` | GET | Linked MyPlex account info | **Absent** |
| `/myplex/refreshReachability` | PUT | Refresh remote access port mapping | **Absent** |
| `/servers` | GET | Local server list | **Absent** |
| `/identity` | GET | Server identity / machine identifier | **Present** |
| `/:/prefs` | GET / PUT | Server preferences | **Present** |
| `/updater/check?download=0` | PUT | Trigger update check | **Present** |
| `/updater/status` | GET | Update status | **Present** |
| `/livetv/dvrs` | GET | DVR devices | **Present** |
| `/status/sessions/history/all` | GET | Play history | **Present** |
| `/activities` | GET | Background activities | **Present** |

### plex.tv Endpoints Used

| Endpoint | Method | Purpose | Status in Spec |
|---|---|---|---|
| `https://plex.tv/api/v2/pins` | POST | OAuth PIN generation | **Absent** |
| `https://plex.tv/api/v2/pins/{pin}` | GET | PIN status / token retrieval | **Absent** |
| `https://plex.tv/api/users` | GET | Friends / shared users | **Present** (`GET /users` on plex.tv) |
| `https://plex.tv/users/account` | GET | Own account details (XML) | **Absent** |
| `https://plex.tv/devices.xml` | GET | Authorized devices list | **Absent** |
| `https://plex.tv/pms/servers.xml` | GET | Published server list with timestamps | **Absent** |
| `https://plex.tv/api/resources?includeHttps=1` | GET | Server connections & discovery | **Absent** |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | GET | Per-server shared library access | **Absent** |
| `https://plex.tv/servers/{machineId}/sync_lists` | GET | Mobile sync lists | **Absent** |
| `https://plex.tv/api/downloads/{channel}.json` | GET | Plex update downloads | **Absent** |
| `https://plex.tv/api/v2/cloud_server` | GET | Plex Cloud status | **Absent** |
| `https://plex.tv/api/v2/geoip?ip_address=` | GET | GeoIP lookup | **Absent** |
| `https://plex.tv/api/v2/ping` | GET | Token validity ping | **Absent** |
| `https://plex.tv/:/ip` | GET | Public IP detection | **Absent** |

### Special Patterns

- **Websocket**: Tautulli connects to `wss://{host}/:/websockets/notifications` (or `ws://`) with `X-Plex-Token` header for real-time session and timeline events.
- **Auth**: Uses `X-Plex-Token` header; also supports per-user server tokens derived from shared_server access tokens.
- **Pagination**: Uses `X-Plex-Container-Start` and `X-Plex-Container-Size` query parameters (also used by others).

---

## Overseerr / Jellyseerr API usage

Overseerr (`sct/overseerr`) and its successor Jellyseerr (`Fallenbagel/jellyseerr`) manage Plex user access, library scanning, and watchlist integration.

### PMS Endpoints Used

| Endpoint | Method | Purpose | Status in Spec |
|---|---|---|---|
| `/library/sections` | GET | Sync libraries | **Present** |
| `/library/sections/{id}/all?includeGuids=1` | GET | Full library scan with external GUIDs | **Partial** (`includeGuids` param absent) |
| `/library/metadata/{key}` | GET | Item metadata | **Present** |
| `/library/metadata/{key}/children` | GET | Child items (seasons/episodes) | **Present** |
| `/library/sections/{id}/all?type={1|4}&sort=addedAt:desc&addedAt>>={ts}` | GET | Recently added delta scan | **Partial** (filter params not fully documented) |

### plex.tv / Provider Endpoints Used

| Endpoint | Method | Purpose | Status in Spec |
|---|---|---|---|
| `https://plex.tv/api/resources?includeHttps=1` | GET | Server discovery & connection URLs | **Absent** |
| `https://plex.tv/users/account.json` | GET | Account info (JSON) | **Absent** |
| `https://plex.tv/api/users` | GET | Friends / shared users (XML) | **Present** (`GET /users`) |
| `https://discover.provider.plex.tv/library/sections/watchlist/all` | GET | Plex Discover watchlist | **Absent** |
| `https://discover.provider.plex.tv/library/metadata/{ratingKey}` | GET | Watchlist item metadata from Discover | **Absent** |
| `https://plex.tv/api/v2/ping` | GET | Token health check | **Absent** |

### Special Patterns

- **Container headers**: Overseerr sends `X-Plex-Container-Start` and `X-Plex-Container-Size` as **HTTP headers** rather than query parameters for pagination.
- **ETag caching**: Uses `If-None-Match` with ETag for watchlist caching.
- **Authentication**: Relies on OAuth PIN flow (same missing endpoints as Tautulli) to obtain tokens.
- **Migration note**: Jellyseerr migrated watchlist from `metadata.provider.plex.tv` to `discover.provider.plex.tv` after Plex deprecated the former.

---

## Bazarr API usage

Bazarr (`morpheus65535/bazarr`) integrates with Plex primarily for subtitle management and webhook-driven automation.

### PMS Endpoints Used

Bazarr's direct PMS API usage is lighter than other tools; it primarily triggers library refreshes after subtitle changes. The exact PMS paths are abstracted behind its own internal API, but typical operations include:

- **Library item refresh** (likely `GET /library/metadata/{id}/refresh` or similar) to update subtitles.
- **Server connection testing** against `/` or `/identity`.

### plex.tv / Webhook Patterns

| Pattern | Details | Status in Spec |
|---|---|---|
| Plex Webhooks (inbound) | Bazarr receives webhooks at `/api/webhooks/plex?apikey={key}` for `media.play` / `media.resume` events to trigger subtitle search | **Absent** |
| Plex Webhook auto-registration | Bazarr can auto-create webhooks on the Plex server via the Plex Web UI mechanisms (not a formal API) | **Absent** |
| OAuth PIN flow | `POST /api/v2/pins` → `GET /api/v2/pins/{id}` for Plex auth | **Absent** |

### Special Patterns

- **Webhook payload**: Consumes standard Plex webhook JSON payloads (see Webhooks section below).
- **Added-date manipulation**: Can update `addedAt` timestamps for movies/episodes after subtitle operations (implementation-specific, not a standard API endpoint).

---

## Kometa API usage

Kometa (`kometa-team/kometa`) is a Python automation framework built on top of the `python-plexapi` library. It exercises a very broad surface of the PMS API for metadata editing, collection management, and server maintenance.

### PMS Endpoints Used (via python-plexapi)

| Endpoint / Operation | Method | Purpose | Status in Spec |
|---|---|---|---|
| `/library/sections/{id}/all` | GET | Enumerate all library items | **Present** |
| `/library/metadata/{id}` | GET | Read item metadata | **Present** |
| `/library/metadata/{id}` | PUT | Update item metadata (title, summary, etc.) | **Partial** (update body schema unclear) |
| `/library/metadata/{id}/posters` | POST | Upload custom poster image | **Absent** |
| `/library/metadata/{id}/arts` | POST | Upload custom background art | **Absent** |
| `/library/collections` | GET / POST | Create and list collections | **Partial** (creation semantics missing) |
| `/library/collections/{id}` | PUT | Edit collection metadata | **Partial** |
| `/library/sections/{id}/refresh` | GET / POST | Trigger library refresh | **Absent** |
| `/library/sections/{id}/emptyTrash` | GET / POST | Empty library trash | **Absent** |
| `/library/sections/{id}/optimize` | GET / POST | Optimize database for a library | **Absent** |
| `/library/optimize` | GET / POST | Global database optimize | **Absent** |
| `/playlists` | GET / POST | Create and list playlists | **Present** |
| `/playlists/{id}/items` | PUT / POST | Add items to playlists | **Partial** |
| `/library/metadata/{id}/unmatch` | PUT | Unmatch metadata match | **Present** |
| `/library/metadata/{id}/match` | PUT / GET | Re-match item | **Present** |
| `/library/metadata/{id}/refresh` | GET | Refresh metadata for single item | **Present** |

### Special Patterns

- **Database cache tuning**: Kometa recommends setting `db_cache` (PMS preference `DatabaseCacheSize` via `:/prefs`) before operations.
- **Label-based smart collections**: Uses `/library/sections/{id}/label` (missing from spec) to drive smart collection filters.
- **Overlays**: Performs image composition and uploads via the poster/art upload endpoints, which are not formally documented in the spec.
- **Python-plexapi abstraction**: Many of these endpoints are not called directly by Kometa's code but are abstracted through `PlexServer`, `LibrarySection`, `Movie`, `Show`, etc. objects in the `python-plexapi` library.

---

## Home Assistant Plex integration usage

The Home Assistant (`home-assistant/core`) Plex integration uses the `python-plexapi` library and a dedicated websocket wrapper (`plexwebsocket`) to monitor server state and control clients.

### PMS Endpoints Used

| Endpoint / Mechanism | Purpose | Status in Spec |
|---|---|---|
| `/` (root) | Server status / connection test | **Present** |
| `/clients` | List connected clients | **Absent** (returns `MediaContainer` of `Server`/`Player` objects) |
| `/status/sessions` | Active sessions | **Present** |
| `/library/sections` | Library discovery | **Present** |
| `systemAccounts()` (effectively `/accounts`) | Server system accounts | **Absent** |
| `playlists()` | List playlists | **Present** |
| `createToken()` | Generate temporary client token | **Absent** |

### Websocket & Real-Time

| Endpoint | Purpose | Status in Spec |
|---|---|---|
| `/:/websockets/notifications` | Real-time event stream (playing, timeline, status, reachability) | **Absent** |

The integration subscribes to:
- `playing` → `PlaySessionStateNotification` (state changes: playing, paused, stopped)
- `status` → `StatusNotification` (e.g. "Library scan complete")

### Discovery

- **GDM (UDP multicast)**: Uses `plexapi.gdm.GDM` to discover clients on `239.0.0.250:32412/32414` via UDP multicast. This is a network-layer protocol, not a REST API, but it's a critical integration mechanism absent from the spec.

### plex.tv Patterns

- `MyPlexAccount(token=...)` → `account.resources()` → server connection
- `account.users()` → shared user discovery
- `resource.connect()` → plex.direct URL resolution

---

## Webhooks & plex.tv endpoints

### Plex Webhooks

Webhooks are a **Plex Pass** feature configured via the Plex Web UI (Account → Webhooks). There is **no documented REST API** for webhook CRUD operations.

#### Events Emitted

| Event | Description |
|---|---|
| `library.on.deck` | New item added to On Deck |
| `library.new` | New item added to library |
| `media.play` | Playback started |
| `media.pause` | Playback paused |
| `media.resume` | Playback resumed |
| `media.stop` | Playback stopped |
| `media.scrobble` | Played past ~90% |
| `media.rate` | Item rated |
| `admin.database.backup` | Scheduled DB backup completed |
| `admin.database.corrupted` | DB corruption detected |
| `device.new` | New device accessed server |
| `playback.started` | Shared user started playback (admin only) |

#### Payload Structure

- **Format**: Multipart HTTP POST (`Content-Type: multipart/form-data`)
- **JSON part**: `payload` field containing `event`, `user`, `owner`, `Account`, `Server`, `Player`, `Metadata`
- **Thumbnail part**: Optional JPEG `thumb` attachment for `media.play`, `library.new`, `library.on.deck`, `media.rate`, `playback.started`

The webhook payload schema is **not present** in the OpenAPI spec.

### Additional plex.tv Endpoints (Cross-cutting)

These plex.tv endpoints are used by multiple integrations (Tautulli, Overseerr, Home Assistant, etc.) and are largely absent:

| Endpoint | Used By | Status |
|---|---|---|
| `GET https://plex.tv/api/v2/pins` | Tautulli, Overseerr, Bazarr | **Absent** |
| `GET https://plex.tv/api/v2/pins/{id}` | Tautulli, Overseerr, Bazarr | **Absent** |
| `GET https://plex.tv/api/resources?includeHttps=1` | Tautulli, Overseerr, HA | **Absent** |
| `GET https://plex.tv/users/account` / `users/account.json` | Tautulli, Overseerr | **Absent** |
| `GET https://plex.tv/devices.xml` | Tautulli | **Absent** |
| `GET https://plex.tv/pms/servers.xml` | Tautulli | **Absent** |
| `GET https://plex.tv/api/servers/{machineId}/shared_servers` | Tautulli | **Absent** |
| `GET https://plex.tv/servers/{machineId}/sync_lists` | Tautulli | **Absent** |
| `GET https://plex.tv/api/downloads/{channel}.json` | Tautulli | **Absent** |
| `GET https://plex.tv/api/v2/cloud_server` | Tautulli | **Absent** |
| `GET https://plex.tv/api/v2/geoip` | Tautulli | **Absent** |
| `GET https://plex.tv/api/v2/ping` | Tautulli, Overseerr | **Absent** |
| `GET https://plex.tv/:/ip` | Tautulli | **Absent** |
| `GET https://discover.provider.plex.tv/library/sections/watchlist/all` | Overseerr, Jellyseerr | **Absent** |
| `GET https://discover.provider.plex.tv/library/metadata/{id}` | Overseerr, Jellyseerr | **Absent** |
| `GET https://metadata.provider.plex.tv/library/metadata/{id}` | Tautulli | **Absent** |

---

## Summary table: Endpoint | Method | Used By | Status in Spec

| Endpoint | Method | Used By | Status in Spec |
|---|---|---|---|
| `/status/sessions` | GET | Tautulli, HA, many | Present |
| `/status/sessions/terminate` | GET | Tautulli | Present |
| `/library/metadata/{id}?includeMarkers=1` | GET | Tautulli | Partial |
| `/library/metadata/{id}/grandchildren` | GET | Tautulli | Absent |
| `/library/sections/{id}/recentlyAdded` | GET | Tautulli | Absent |
| `/library/recentlyAdded` | GET | Tautulli | Absent |
| `/hubs/home/recentlyAdded` | GET | Tautulli | Absent |
| `/hubs/search?includeCollections=1` | GET | Tautulli | Partial |
| `/library/sections/{id}/label` | GET | Tautulli, Kometa | Absent |
| `/sync/items/{id}` | GET | Tautulli | Absent |
| `/sync/transcodeQueue` | GET | Tautulli | Absent |
| `/myplex/account` | GET | Tautulli | Absent |
| `/myplex/refreshReachability` | PUT | Tautulli | Absent |
| `/servers` | GET | Tautulli | Absent |
| `/library/sections/{id}/all?includeGuids=1` | GET | Overseerr | Partial |
| `/library/sections/{id}/all?addedAt>>={ts}` | GET | Overseerr | Partial |
| `discover.provider.plex.tv/library/sections/watchlist/all` | GET | Overseerr, Jellyseerr | Absent |
| `discover.provider.plex.tv/library/metadata/{id}` | GET | Overseerr, Jellyseerr | Absent |
| `metadata.provider.plex.tv/library/metadata/{id}` | GET | Tautulli | Absent |
| `/library/metadata/{id}/posters` | POST | Kometa | Absent |
| `/library/metadata/{id}/arts` | POST | Kometa | Absent |
| `/library/sections/{id}/refresh` | GET/POST | Kometa | Absent |
| `/library/sections/{id}/emptyTrash` | GET/POST | Kometa | Absent |
| `/library/sections/{id}/optimize` | GET/POST | Kometa | Absent |
| `/library/optimize` | GET/POST | Kometa | Absent |
| `/clients` | GET | HA | Absent |
| `/accounts` | GET | HA (via python-plexapi) | Absent |
| `/:/websockets/notifications` | WS | Tautulli, HA | Absent |
| `plex.tv/api/v2/pins` | POST | Tautulli, Overseerr, Bazarr | Absent |
| `plex.tv/api/v2/pins/{id}` | GET | Tautulli, Overseerr, Bazarr | Absent |
| `plex.tv/api/resources?includeHttps=1` | GET | Tautulli, Overseerr, HA | Absent |
| `plex.tv/users/account` / `users/account.json` | GET | Tautulli, Overseerr | Absent |
| `plex.tv/devices.xml` | GET | Tautulli | Absent |
| `plex.tv/pms/servers.xml` | GET | Tautulli | Absent |
| `plex.tv/api/servers/{machineId}/shared_servers` | GET | Tautulli | Absent |
| `plex.tv/servers/{machineId}/sync_lists` | GET | Tautulli | Absent |
| `plex.tv/api/downloads/{channel}.json` | GET | Tautulli | Absent |
| `plex.tv/api/v2/cloud_server` | GET | Tautulli | Absent |
| `plex.tv/api/v2/geoip` | GET | Tautulli | Absent |
| `plex.tv/api/v2/ping` | GET | Tautulli, Overseerr | Absent |
| `plex.tv/:/ip` | GET | Tautulli | Absent |
| Plex Webhook payload schema | POST (inbound) | Bazarr, HA, Notifiarr | Absent |

---

## Priority gaps (most impactful missing endpoints)

### 1. plex.tv Authentication & Discovery (`CRITICAL`)
The OAuth PIN flow (`/api/v2/pins`) and server discovery (`/api/resources?includeHttps=1`) are fundamental to every modern integration. Without these, client apps cannot authenticate users or discover connection URLs. These are completely missing.

### 2. plex.tv Account & Sharing Endpoints (`HIGH`)
- `/users/account` and `/users/account.json` — required for account info, Plex Pass status, and home-user detection.
- `/api/servers/{machineId}/shared_servers` — required for understanding which libraries are shared with which users.
- `/api/users` — present in spec but only as XML; JSON variant used by some tools is not documented.

### 3. Plex Discover / Watchlist Provider (`HIGH`)
- `discover.provider.plex.tv/library/sections/watchlist/all`
- `discover.provider.plex.tv/library/metadata/{id}`
These are now the canonical endpoints for Plex Watchlist data. Overseerr/Jellyseerr depend on them. The older `metadata.provider.plex.tv` endpoint is also used by Tautulli for GUID-based metadata lookups.

### 4. Real-Time Websocket (`HIGH`)
- `/:/websockets/notifications` is the primary real-time event bus for sessions, timeline updates, and server status. Both Tautulli and Home Assistant rely on it. The spec documents SSE/EventSource but not the websocket path or its message schema (`NotificationContainer`, `PlaySessionStateNotification`, `TimelineEntry`, `ReachabilityNotification`).

### 5. Media Metadata Parameters (`MEDIUM-HIGH`)
- `includeMarkers=1` on `/library/metadata/{id}` — critical for intro/credits skip detection (used by Tautulli and many clients).
- `includeGuids=1` on `/library/sections/{id}/all` — critical for matching items to external databases (TMDB, TVDB) in Overseerr/Kometa.
- `includeCollections=1` on `/hubs/search` — affects search behavior for collection discovery.

### 6. Library & Server Maintenance Endpoints (`MEDIUM`)
- `/library/sections/{id}/refresh`, `/emptyTrash`, `/optimize`
- `/library/optimize`
- `/library/metadata/{id}/posters` and `/arts` (image upload)
These are essential for automation tools like Kometa and are well-known in the community but absent from the spec.

### 7. Webhook Schema (`MEDIUM`)
The webhook payload structure and event types are documented only in Plex support articles. A formal OpenAPI schema for the multipart JSON payload would help webhook consumers (Bazarr, Home Assistant, Notifiarr, Tautulli) validate inputs.

### 8. Local Server Utility Endpoints (`LOW-MEDIUM`)
- `/servers` — local server list
- `/library/recentlyAdded` and `/library/sections/{id}/recentlyAdded` — standard "new content" queries
- `/library/metadata/{id}/grandchildren` — useful for show→episode traversal without intermediate season fetches
- `/sync/items/{id}` and `/sync/transcodeQueue` — mobile sync management
