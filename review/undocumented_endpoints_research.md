# Undocumented & Hidden Plex API Endpoints

> **Research date:** 2026-06-03  
> **Scope:** Public forums, GitHub, Gists, Reddit, CVE write-ups, and the official `plex-api-spec.yaml` (≈17k lines).  
> **Goal:** Catalog endpoints, patterns, auth quirks, and XML/JSON behaviors that are **not** present in the current OpenAPI spec.

---

## How to read this document

* **In spec?** = Already documented in `plex-api-spec.yaml`.
* **Not in spec** = Missing from the current spec and should be considered for addition.
* Sources are URLs where the endpoint or behavior was observed in the wild.

---

## plex.tv API v2 (Account, Auth, Devices, Webhooks)

The current spec only documents three `plex.tv/api/v2` paths (`/user`, `/users/signin`, `/resources`). The v2 surface is much larger.

### Account & User

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://plex.tv/api/v2/user` | `GET` | Full account object (authToken, home, subscription, etc.) | `X-Plex-Token` | ✅ Yes | — |
| `https://plex.tv/api/v2/users/signin` | `POST` | Username/password sign-in | Basic / form | ✅ Yes | — |
| `https://plex.tv/api/v2/users/signout` | `DELETE` | Invalidate token | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/features` | `GET` | Plex Pass feature flags for the account | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/plex-v2-api-documentation/444928) |
| `https://plex.tv/api/v2/friends` | `GET` | List of friends & shared users | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/plex-v2-api-documentation/444928) |
| `https://plex.tv/api/v2/home` | `GET` | Plex Home user list | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/plex-v2-api-documentation/444928) |
| `https://plex.tv/api/v2/server` | `GET` | Server association info for the logged-in user | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/plex-v2-api-documentation/444928) |
| `https://plex.tv/api/v2/users/password` | `POST` | Change/reset password | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/plex-v2-api-documentation/444928) |
| `https://plex.tv/api/v2/ping` | `GET` | Health / latency check | None | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/user/view_state_sync` | `PUT` | Enable/disable watch-state sync consent | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/user/{userUUID}/settings/opt_outs` | `GET` | Online-media-source opt-outs (e.g. `opt_in`, `opt_out`, `opt_out_managed`) | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |

### Sharing & Invites

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://plex.tv/api/v2/shared_servers` | `POST` | Share a server with a user (managed or friend) | `X-Plex-Token` + `X-Plex-Client-Identifier` | ❌ No | [Plexopedia](https://www.plexopedia.com/plex-media-server/api-plextv/share-server/) |
| `https://plex.tv/api/v2/sharings/{userId}` | `PUT` | Update friend filters (allowSync, allowCameraUpload, filterMovies, etc.) | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/sharings/{userId}` | `DELETE` | Remove a share / friend | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/home/users/restricted/{userId}` | `PUT` | Update restricted (managed) home user settings | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/server/access_tokens` | `GET` | List access tokens for the server (server-device token only) | `X-Plex-Token` | ❌ No | [CVE-2025-34158 write-up](https://github.com/lufinkey/vulnerability-research/blob/main/CVE-2025-34158/README.md) |
| `https://plex.tv/api/v2/server/users/features` | `GET` | Features enabled per shared user | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/request-for-admin-expert-review-server-claimed-but-all-tokens-return-403-forbidden/932522) |

### PIN & OAuth

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://plex.tv/api/v2/pins` | `POST` | Create a 4-character PIN for device linking | `X-Plex-Client-Identifier` | ❌ No | [python-plexapi docs](https://python-plexapi.readthedocs.io/en/latest/modules/myplex.html) |
| `https://plex.tv/api/v2/pins/{pinId}` | `GET` | Poll PIN status; returns `authToken` when claimed | `X-Plex-Client-Identifier` | ❌ No | [plexargod repo](https://github.com/danielewood/plexargod) |
| `https://plex.tv/api/v2/pins/link` | `PUT` | Link a PIN to an account (used by OAuth flow) | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://clients.plex.tv/api/v2/pins` | `POST` | Alternative PIN endpoint (clients subdomain) | `X-Plex-Client-Identifier` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |

### JWT Device Registration (new as of 2025)

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://clients.plex.tv/api/v2/auth/jwk` | `POST` | Register device public key (JWK) | `X-Plex-Token` + `X-Plex-Client-Identifier` | ❌ No | [Plex Pro Week blog](https://www.plex.tv/blog/plex-pro-week-25-api-unlocked/), [JonnyWong16 gist](https://gist.github.com/JonnyWong16/6720b9d9edc5686c72957d94b0d5b381) |
| `https://clients.plex.tv/api/v2/auth/nonce` | `GET` | Get a nonce to sign in the client JWT | `X-Plex-Client-Identifier` | ❌ No | [JonnyWong16 gist](https://gist.github.com/JonnyWong16/6720b9d9edc5686c72957d94b0d5b381) |
| `https://clients.plex.tv/api/v2/auth/token` | `POST` | Exchange signed client JWT for a Plex JWT | `X-Plex-Client-Identifier` | ❌ No | [JonnyWong16 gist](https://gist.github.com/JonnyWong16/6720b9d9edc5686c72957d94b0d5b381) |
| `https://clients.plex.tv/api/v2/auth/keys` | `GET` | Plex public JWKs for signature verification | None | ❌ No | [JonnyWong16 gist](https://gist.github.com/JonnyWong16/6720b9d9edc5686c72957d94b0d5b381) |

**JWT quirks**
* Tokens expire after **7 days**.
* Must be refreshed via the keypair flow.
* Scope list: `username`, `email`, `friendly_name`, `restricted`, `anonymous`, `joinedAt`.
* Plex mentions **rate limiting** is active on these endpoints.

### Webhooks Configuration

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://plex.tv/api/v2/user/webhooks` | `GET` | List configured webhook URLs | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/v2/user/webhooks` | `POST` | Add a webhook URL | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |

### Device Certificate (used during server claim)

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://plex.tv/api/v2/devices/{deviceId}/certificate/subject` | `GET` | Get cert subject | `X-Plex-Token` | ❌ No | [Plex Forum logs](https://forums.plex.tv/t/fresh-install-unable-to-claim-ubuntu/853466) |
| `https://plex.tv/api/v2/devices/{deviceId}/certificate/csr` | `PUT` | Upload CSR | `X-Plex-Token` | ❌ No | [Plex Forum logs](https://forums.plex.tv/t/fresh-install-unable-to-claim-ubuntu/853466) |
| `https://plex.tv/api/v2/devices/{deviceId}/certificate/download` | `GET` | Download signed cert (may 202 / retry) | `X-Plex-Token` | ❌ No | [Plex Forum logs](https://forums.plex.tv/t/fresh-install-unable-to-claim-ubuntu/853466) |
| `https://plex.tv/api/v2/release_channels` | `GET` | Release channel info (seen during claim) | `X-Plex-Token` | ❌ No | [Plex Forum](https://forums.plex.tv/t/unable-to-set-my-claim-token/922072) |

### Legacy v1 plex.tv endpoints still in use

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://plex.tv/pins.xml` | `POST` | Legacy PIN creation (returns XML) | `X-Plex-Client-Identifier` | ❌ No | [plexargod repo](https://github.com/danielewood/plexargod) |
| `https://plex.tv/pins/{pinId}` | `GET` | Legacy PIN check (returns XML) | `X-Plex-Client-Identifier` | ❌ No | [plexargod repo](https://github.com/danielewood/plexargod) |
| `https://plex.tv/api/resources` | `GET` | Published server connections (XML) | `X-Plex-Token` | ❌ No | [plexargod repo](https://github.com/danielewood/plexargod) |
| `https://plex.tv/api/users/` | `GET` | Friends list (XML) | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/servers/{machineId}` | `GET` | Server info (XML) | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | `POST` | Share server (XML) | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://clients.plex.tv/devices.xml` | `GET` | Authorized devices with tokens (XML) | `X-Plex-Token` | ❌ No | [CVE-2025-34158 write-up](https://github.com/lufinkey/vulnerability-research/blob/main/CVE-2025-34158/README.md) |

---

## Cloud Provider Endpoints (`tv.plex.provider.*`)

These are **not** in the spec at all. They are used by Plex clients for watchlists, search, and streaming metadata.

### `metadata.provider.plex.tv` — **Deprecated** (moved to `discover.provider.plex.tv`)

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://metadata.provider.plex.tv/library/sections/watchlist/all` | `GET` | Fetch user watchlist | `X-Plex-Token` | ❌ No | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |
| `https://metadata.provider.plex.tv/actions/removeFromWatchlist` | `POST` | Remove from watchlist | `X-Plex-Token` | ❌ No | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |
| `https://metadata.provider.plex.tv/actions/addToWatchlist` | `POST` | Add to watchlist | `X-Plex-Token` | ❌ No | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |

### `discover.provider.plex.tv` — **Current**

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `https://discover.provider.plex.tv/library/search` | `GET` | Search movies & shows in Discover | `X-Plex-Token` | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://discover.provider.plex.tv/library/sections/watchlist/all` | `GET` | New watchlist endpoint | `X-Plex-Token` | ❌ No | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |
| `https://discover.provider.plex.tv/actions/removeFromWatchlist` | `POST` | New remove-from-watchlist | `X-Plex-Token` | ❌ No | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |
| `https://discover.provider.plex.tv/actions/addToWatchlist` | `POST` | New add-to-watchlist | `X-Plex-Token` | ❌ No | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |

**Search query params** (from `searchDiscover`):
* `query`, `limit`, `searchTypes` (`movies,tv` or `movie` or `show`), `searchProviders` (`discover`, `discover,PLEXAVOD`, `discover,PLEXAVOD,PLEXTVOD`), `includeMetadata=1`
* Requires header `Accept: application/json`.

### Other provider hostnames observed

| Hostname | Purpose | In spec? | Source |
|----------|---------|----------|--------|
| `https://vod.provider.plex.tv` | VOD streaming / metadata | ❌ No | [Netify](https://www.netify.ai/resources/hostnames/vod.provider.plex.tv), [python-plexapi](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://music.provider.plex.tv` | Music provider | ❌ No | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `tv.plex.provider.vod` | VOD provider identifier | ❌ No | [Plex Pro Week blog](https://www.plex.tv/blog/plex-pro-week-25-api-unlocked/) |
| `tv.plex.provider.music` | Music provider identifier | ❌ No | [Plex Pro Week blog](https://www.plex.tv/blog/plex-pro-week-25-api-unlocked/) |
| `tv.plex.provider.discover` | Discover provider identifier | ❌ No | [Plex Pro Week blog](https://www.plex.tv/blog/plex-pro-week-25-api-unlocked/) |
| `tv.plex.provider.metadata` | Metadata provider identifier | ❌ No | [Plex Pro Week blog](https://www.plex.tv/blog/plex-pro-week-25-api-unlocked/) |

---

## Server Management (undiscovered preferences, system endpoints)

### System & Diagnostics

| Path | Method | What it does | Auth | In spec? | Source |
|------|--------|--------------|------|----------|--------|
| `GET /system/agents` | `GET` | List metadata agents | `X-Plex-Token` (admin) | ❌ No | Unofficial wiki / community knowledge |
| `GET /system/agents/{agentId}` | `GET` | Agent details & settings | `X-Plex-Token` (admin) | ❌ No | Unofficial wiki / community knowledge |
| `GET /system/settings` | `GET` | System-level settings | `X-Plex-Token` (admin) | ❌ No | Unofficial wiki / community knowledge |
| `GET /system/updates` | `GET` | Check for PMS updates | `X-Plex-Token` (admin) | ❌ No | Unofficial wiki / community knowledge |
| `GET /diagnostics` | `GET` | Server diagnostics | `X-Plex-Token` (admin) | ❌ No | Unofficial wiki / community knowledge |
| `GET /sync` | `GET` | Sync status overview | `X-Plex-Token` | ❌ No | Unofficial wiki / community knowledge |
| `GET /sync/items` | `GET` | Sync items list | `X-Plex-Token` | ❌ No | Unofficial wiki / community knowledge |
| `GET /sync/queue` | `GET` | Sync queue | `X-Plex-Token` | ❌ No | Unofficial wiki / community knowledge |
| `GET /transcode/sessions` | `GET` | Active transcode sessions | `X-Plex-Token` (admin) | ❌ No | Unofficial wiki / community knowledge |

### Preferences (`/:/prefs` is in spec, but many hidden settings are not)

The spec documents `GET /:/prefs`, `GET /:/prefs/get`, and `PUT /:/prefs`.  
What is **not** documented are the ~40+ *hidden* preference keys that can be read/written via the same endpoint:

* `aBRKeepOldTranscodes`, `allowHighOutputBitrates`, `backgroundQueueIdlePaused`
* `butlerTaskGarbageCollectBlobs`, `butlerTaskGenerateMediaIndexFiles`
* `certificateVersion`, `dvrShowUnsupportedDevices`, `enableABRDebugOverlay`
* `enableAirplay`, `eyeQUser`, `forceAutoAdjustQuality`
* `generateIndexFilesDuringAnalysis`, `gracenoteUser`
* `hardwareDevicePath` (default `/dev/dri/renderD128`)
* `manualPortMappingMode`, `manualPortMappingPort`
* `minimumProgressTime`, `plexMetricsUrl`, `plexOnlineMail`, `plexOnlineUrl`
* `syncMyPlexLoginGCDeferral`, `syncPagingItemsLimit`
* `systemAudioCodecs`, `transcoderH264MinimumCRF`, `transcoderH264Options`
* `transcoderH264OptionsOverride`, `transcoderH264Preset`
* `transcoderLivePruneBuffer`, `transcoderLogLevel`

Source: [Python PlexAPI settings docs](https://python-plexapi.readthedocs.io/en/latest/modules/settings.html), [Plex hidden settings article](https://support.plex.tv/articles/201105343-advanced-hidden-server-settings/)

---

## Media Library (hidden params, extra endpoints)

### Missing sub-endpoints under `/library/sections/{sectionId}`

The spec documents `/library/sections/{sectionId}/all`, `/albums`, `/allLeaves`, `/analyze`, `/arts`, `/autocomplete`, `/categories`, `/cluster`, `/collections`, `/common`, `/computePath`, `/emptyTrash`, `/filters`, `/firstCharacters`, `/indexes`, `/intros`, `/location`, `/moment`, `/nearest`, `/prefs`, `/refresh`, `/sorts`, `/collection/{collectionId}`, `/composite/{updatedAt}`.

**Not documented:**

| Path | Method | Purpose | In spec? | Source |
|------|--------|---------|----------|--------|
| `/library/sections/{sectionId}/onDeck` | `GET` | On-deck items for this section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/unwatched` | `GET` | Unwatched items | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/newest` | `GET` | Newest additions | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/byYear` | `GET` | Browse by year | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/byDecade` | `GET` | Browse by decade | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/byContentRating` | `GET` | Browse by content rating | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/byResolution` | `GET` | Browse by resolution | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/byFolder` | `GET` | Browse by folder | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/agents` | `GET` | Available agents for this section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/match` | `GET` | Match items in section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/unmatch` | `GET` | Unmatch items in section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/edit` | `GET/PUT` | Edit section metadata | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/delete` | `DELETE` | Delete the section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/move` | `PUT` | Move section paths | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/settings` | `GET` | Section-specific settings | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/playlists` | `GET` | Playlists belonging to section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/hubs` | `GET` | Hubs for this section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/timeline` | `GET` | Section timeline | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/search` | `GET` | Section-scoped search | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/tags` | `GET` | Tags in section | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/artists` | `GET` | Artists (music) | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/shows` | `GET` | Shows (TV) | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/episodes` | `GET` | Episodes | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/movies` | `GET` | Movies | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/clips` | `GET` | Clips | ❌ No | Community knowledge / client traffic |
| `/library/sections/{sectionId}/photos` | `GET` | Photos | ❌ No | Community knowledge / client traffic |

### Missing sub-endpoints under `/library/metadata/{ratingKey}`

The spec documents many (`/credits`, `/extras`, `/file`, `/index`, `/intro`, `/marker`, `/match`, `/matches`, `/merge`, `/nearest`, `/prefs`, `/refresh`, `/related`, `/similar`, `/split`, `/subtitles`, `/tree`, `/unmatch`, `/users/top`, `/voiceActivity`, `/augmentations/{augmentationId}`, `/media/{mediaItem}`, `/marker/{marker}`, `/nearest`, `/file`, `/parts/{partId}`, etc.).

**Not documented:**

| Path | Method | Purpose | In spec? | Source |
|------|--------|---------|----------|--------|
| `/library/metadata/{ratingKey}/children` | `GET` | Children of a show/season/artist/album | ❌ No | Client `key` attribute in metadata responses |
| `/library/metadata/{ratingKey}/onDeck` | `GET` | On-deck for this show/season | ❌ No | Client traffic |
| `/library/metadata/{ratingKey}/reviews` | `GET` | User reviews | ❌ No | Client traffic |
| `/library/metadata/{ratingKey}/parent` | `GET` | Parent metadata shortcut | ❌ No | Client traffic |
| `/library/metadata/{ratingKey}/grandparent` | `GET` | Grandparent metadata shortcut | ❌ No | Client traffic |

### Undocumented query parameters for `/library/sections/{sectionId}/all`

The spec only lists `includeMeta`, `includeGuids`, `sectionId`, `mediaQuery`, `X-Plex-Container-Start`, `X-Plex-Container-Size`.  
The following params are widely used by official clients but **absent** from the spec:

* **Type filtering:** `type` (`1`=movie, `2`=show, `3`=season, `4`=episode, `8`=artist, `9`=album, `10`=track, …)
* **Sorting:** `sort` (e.g. `titleSort`, `year`, `addedAt`, `lastViewedAt`, `viewCount`, `rating`)
* **Filters:** `filters`, `unwatched` (`1`)
* **Tag filters:** `genre`, `studio`, `contentRating`, `resolution`, `year`, `firstCharacter`
* **Include flags:** `includeCollections`, `includeExternalMedia`, `includeAdvanced`, `includeMeta`, `checkFiles`, `includeRelated`, `includeExtras`, `includePopularLeaves`, `includeConcerts`, `includeOnDeck`, `includeChapters`, `includePreferences`, `includeBandwidths`, `includeLoudnessRamps`, `includeStations`, `includeExternalIds`, `includeReviews`, `includeCredits`, `includeArt`, `includeThumb`, `includeBanner`, `includeTheme`, `includeFields`
* **Async flags:** `asyncAugmentMetadata`, `asyncRefreshLocalMediaAgent`, `nocache`, `excludeFields`, `skipRefresh`

---

## Playback & Transcoder (hidden tuning params)

### Player control endpoints (missing from spec entirely)

The Plex Web app uses these to remotely control clients. They are **not** in the spec.

| Path | Method | Purpose |
|------|--------|---------|
| `/player/playback/play` | `POST` | Start playback |
| `/player/playback/pause` | `POST` | Pause |
| `/player/playback/stop` | `POST` | Stop |
| `/player/playback/seek` | `POST` | Seek to time |
| `/player/playback/skipTo` | `POST` | Skip to item |
| `/player/playback/skipBy` | `POST` | Skip forward/backward |
| `/player/playback/stepForward` | `POST` | Step forward |
| `/player/playback/stepBack` | `POST` | Step back |
| `/player/playback/setParameters` | `POST` | Set playback params |
| `/player/playback/subtitleStream` | `POST` | Change subtitle stream |
| `/player/playback/audioStream` | `POST` | Change audio stream |
| `/player/playback/videoStream` | `POST` | Change video stream |
| `/player/playback/volume` | `POST` | Set volume |
| `/player/playback/mute` | `POST` | Mute |
| `/player/playback/unmute` | `POST` | Unmute |
| `/player/playback/setTextStream` | `POST` | Set text stream |
| `/player/playback/setRating` | `POST` | Rate item |
| `/player/playback/setViewOffset` | `POST` | Set resume offset |
| `/player/playback/setState` | `POST` | Set playback state |
| `/player/playback/refreshPlayQueue` | `POST` | Refresh play queue |
| `/player/playback/playMedia` | `POST` | Play specific media |

**Auth:** Usually requires a `X-Plex-Target-Client-Identifier` header plus the controlling user’s `X-Plex-Token`.

### Transcode session segments

The spec documents `/{transcodeType}/:/transcode/universal/start.{extension}`, `/decision`, `/fallback`, `/subtitles`.  
What is missing:

| Path | Purpose | In spec? | Source |
|------|---------|----------|--------|
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.m4s` | DASH/HLS segment delivery | ❌ No | [UnicornTranscoder issue #136](https://github.com/UnicornTranscoder/UnicornTranscoder/issues/136) |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.ts` | HLS TS segment delivery | ❌ No | Community knowledge |
| `/music/:/transcode` | Audio transcode endpoint | ❌ No | Community knowledge |

### Stream URL hidden parameters

When requesting a direct-play or transcode stream URL, these query params are accepted but undocumented in the spec:

* `maxVideoBitrate`, `videoResolution`
* `offset`, `copyts`, `protocol`
* `mediaIndex`, `partIndex`
* `platform`, `X-Plex-Token`

Source: [Python PlexAPI base docs](https://python-plexapi.readthedocs.io/en/latest/modules/base.html)

---

## Webhooks & Events

### Configuration

* `GET https://plex.tv/api/v2/user/webhooks` — list URLs.
* `POST https://plex.tv/api/v2/user/webhooks` — add a URL (body likely JSON with `url` field).

### Payload format

* **Content-Type:** `multipart/form-data` (not pure JSON).
* **Fields:**
  * `payload` — JSON string containing `event`, `user`, `owner`, `Account`, `Server`, `Player`, `Metadata`.
  * `thumb` — JPEG thumbnail (only for `media.play` and `media.rate`).
* **Events:** `media.play`, `media.pause`, `media.resume`, `media.stop`, `media.scrobble`, `media.rate`, `library.new`.

Source: [Plex Support – Webhooks](https://support.plex.tv/articles/115002267687-webhooks/)

### Sonos integration

* `https://sonos.plex.tv` — Plex-to-Sonos control gateway. Routes through Plex remote access. Not in spec.
* Requires Plex Pass + linked Sonos account + remote access enabled.

Source: [Python PlexAPI docs](https://python-plexapi.readthedocs.io/en/latest/introduction.html)

---

## Legacy / Deprecated endpoints

| Path | Status | Replacement | Source |
|------|--------|-------------|--------|
| `https://plex.tv/pins.xml` | Legacy XML PIN API | `https://plex.tv/api/v2/pins` | [plexargod repo](https://github.com/danielewood/plexargod) |
| `https://plex.tv/api/resources` | Legacy XML resources | `https://plex.tv/api/v2/resources` | [plexargod repo](https://github.com/danielewood/plexargod) |
| `https://plex.tv/api/users/` | Legacy XML friends | `https://plex.tv/api/v2/friends` | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | Legacy XML sharing | `https://plex.tv/api/v2/shared_servers` | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |
| `https://clients.plex.tv/devices.xml` | Legacy XML devices | `https://plex.tv/api/v2/resources` or JWT flow | [CVE-2025-34158 write-up](https://github.com/lufinkey/vulnerability-research/blob/main/CVE-2025-34158/README.md) |
| `https://metadata.provider.plex.tv/...` | Deprecated Oct 2025 | `https://discover.provider.plex.tv/...` | [pd_zurg issue #98](https://github.com/I-am-PUID-0/pd_zurg/issues/98) |

---

## XML vs JSON quirks

| Behavior | Details |
|----------|---------|
| **Default format** | Most PMS endpoints return **XML** unless `Accept: application/json` is sent. |
| **plex.tv v2** | Generally returns **JSON** by default. |
| **Legacy endpoints** (`/pins.xml`, `/api/resources`, `/api/users/`) | Return **XML** only. |
| **Webhook payload** | JSON wrapped in a `multipart/form-data` field named `payload`; thumbnail delivered as a second file part. |
| **Empty responses** | Some `PUT`/`DELETE` endpoints return `204 No Content` with no body. |

---

## Rate Limiting & Special Headers

| Topic | Details |
|-------|---------|
| **JWT / Auth rate limits** | Plex Pro Week ’25 blog explicitly mentions built-in rate limiting on auth endpoints to prevent abuse. | [Plex Pro Week blog](https://www.plex.tv/blog/plex-pro-week-25-api-unlocked/) |
| **Claim loops** | `POST https://plex.tv/servers.xml` can return `429 Too Many Requests` if retried too aggressively. | [Plex Forum](https://forums.plex.tv/t/fresh-install-unable-to-claim-ubuntu/853466) |
| **Provider timeouts** | Custom metadata providers may be timed out by PMS if responses are slow; no documented timeout value. | [Plex Forum – Custom Metadata Providers](https://forums.plex.tv/t/announcement-custom-metadata-providers/934384?page=2) |
| **Required headers** | `X-Plex-Client-Identifier` is **mandatory** for PIN and JWT flows. `X-Plex-Token` can be passed as header or query param. | Community knowledge |
| **Client info headers** | `X-Plex-Product`, `X-Plex-Version`, `X-Plex-Platform`, `X-Plex-Platform-Version`, `X-Plex-Device`, `X-Plex-Model`, `X-Plex-Device-Vendor`, `X-Plex-Device-Name`, `X-Plex-Marketplace` are expected by most plex.tv endpoints. | [python-plexapi source](https://python-plexapi.readthedocs.io/en/latest/_modules/plexapi/myplex.html) |

---

## Summary: What should be added to the spec

### High priority (missing blocks)

1. **plex.tv API v2 surface**
   * `/features`, `/friends`, `/home`, `/server`, `/users/signout`, `/users/password`
   * `/pins`, `/pins/link`, `/ping`
   * `/shared_servers`, `/sharings/{userId}`, `/home/users/restricted/{userId}`
   * `/user/webhooks`, `/user/view_state_sync`, `/user/{uuid}/settings/opt_outs`
   * `/server/access_tokens`, `/server/users/features`
   * `/devices/{id}/certificate/*`, `/release_channels`
   * **JWT auth sub-tree:** `clients.plex.tv/api/v2/auth/jwk`, `/nonce`, `/token`, `/keys`

2. **Cloud providers**
   * `discover.provider.plex.tv/library/search`
   * `discover.provider.plex.tv/library/sections/watchlist/all`
   * `discover.provider.plex.tv/actions/addToWatchlist` & `removeFromWatchlist`
   * `vod.provider.plex.tv` & `music.provider.plex.tv` base paths
   * Deprecated but historically important: `metadata.provider.plex.tv` watchlist endpoints (for migration docs)

3. **Player control API**
   * All `/player/playback/*` endpoints (play, pause, stop, seek, volume, stream selection, etc.)

4. **Transcode segments**
   * `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.m4s` / `.ts`
   * `/music/:/transcode`

5. **Missing library section sub-endpoints**
   * `/onDeck`, `/unwatched`, `/newest`, `/byYear`, `/byDecade`, `/byContentRating`, `/byResolution`, `/byFolder`
   * `/agents`, `/match`, `/unmatch`, `/edit`, `/delete`, `/move`, `/settings`
   * `/playlists`, `/hubs`, `/timeline`, `/search`, `/tags`
   * `/artists`, `/shows`, `/episodes`, `/movies`, `/clips`, `/photos`

6. **Missing metadata sub-endpoints**
   * `/library/metadata/{id}/children`, `/onDeck`, `/reviews`, `/parent`, `/grandparent`

7. **System & diagnostics**
   * `/system/agents`, `/system/agents/{id}`, `/system/settings`, `/system/updates`
   * `/diagnostics`, `/sync`, `/sync/items`, `/sync/queue`, `/transcode/sessions`

### Medium priority (query params & schemas)

8. **Expand `/library/sections/{sectionId}/all` parameters**
   * `type`, `sort`, `filters`, `unwatched`, `genre`, `studio`, `contentRating`, `resolution`, `year`, `firstCharacter`
   * `includeCollections`, `includeExternalMedia`, `includeAdvanced`, `checkFiles`, `includeRelated`, `includeExtras`, `includePopularLeaves`, `includeConcerts`, `includeOnDeck`, `includeChapters`, `includePreferences`, `includeBandwidths`, `includeLoudnessRamps`, `includeStations`, `includeExternalIds`, `includeReviews`, `includeCredits`, `includeArt`, `includeThumb`, `includeBanner`, `includeTheme`, `includeFields`
   * `asyncAugmentMetadata`, `asyncRefreshLocalMediaAgent`, `nocache`, `excludeFields`, `skipRefresh`

9. **Webhook schema**
   * Document the `multipart/form-data` payload, event enum, and thumbnail attachment behavior.

10. **Hidden preferences schema**
    * Document the hidden `BoolInt` / `text` preferences accessible via `/:/prefs`.

### Low priority (legacy / reference)

11. **Legacy v1 endpoints**
    * `POST /pins.xml`, `GET /pins/{id}`, `GET /api/resources`, `GET /api/users/`, `GET /api/servers/{machineId}`, `POST /api/servers/{machineId}/shared_servers`, `GET /clients.plex.tv/devices.xml`
    * Useful for migration guides and backwards-compatibility notes.

---

*End of research.*
