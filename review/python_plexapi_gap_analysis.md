# python-plexapi Gap Analysis

**Date:** 2026-06-03  
**SDK Version Analyzed:** master (pkkid/python-plexapi)  
**OpenAPI Spec:** plex-api-spec.yaml (local)

---

## 1. Endpoints in SDK but Missing from Spec

### PMS Endpoints (Local Server)

| Path | Method | Source File | What it does |
|------|--------|-------------|--------------|
| `/library` | GET | `server.py` | Returns the root `Library` object (used by `PlexServer.library`) |
| `/library/sections/` | GET | `server.py` | Fallback for non-owners to list sections (used when `/library` throws `BadRequest`) |
| `/clients` | GET | `server.py` | Lists connected `PlexClient` objects (`PlexServer.clients()`) |
| `/system/agents` | GET | `server.py` | Lists available metadata agents (`PlexServer.agents()`) |
| `/accounts` | GET | `server.py` | Lists local system accounts (`PlexServer.systemAccounts()`) |
| `/devices` | GET | `server.py` | Lists local system devices (`PlexServer.systemDevices()`) |
| `/services/browse` | GET | `server.py` | Browses filesystem paths (`PlexServer.browse()`) |
| `/services/browse/{base64path}` | GET | `server.py` | Browses a specific filesystem path |
| `/diagnostics/databases` | GET | `server.py` | Downloads server DB diagnostics (`PlexServer.downloadDatabases()`) |
| `/diagnostics/logs` | GET | `server.py` | Downloads server logs (`PlexServer.downloadLogs()`) |
| `/statistics/bandwidth` | GET | `server.py` | Dashboard bandwidth data (`PlexServer.bandwidth()`) |
| `/statistics/resources` | GET | `server.py` | Dashboard resource data (`PlexServer.resources()`) |
| `/sync/refreshSynclists` | PUT | `server.py` | Forces PMS to download new SyncList from plex.tv |
| `/sync/refreshContent` | PUT | `server.py` | Forces PMS to refresh content for known SyncLists |
| `/playlists?type=42` | GET / DELETE | `server.py` | Optimized/Conversion items (`optimizedItems()`, `conversions()`) |
| `/playQueues/1` | GET | `server.py` | Conversion queue (`PlexServer.conversions()`) |
| `/hubs/continueWatching/items` | GET | `server.py` | Continue Watching hub items (`PlexServer.continueWatching()`) |
| `/:/progress` | GET | `base.py` | Updates watch progress (`Playable.updateProgress()`) |
| `/actions/removeFromContinueWatching` | PUT | `video.py` | Removes item from Continue Watching (`Movie.removeFromContinueWatching()`) |
| `/library/metadata/{id}/nearest` | GET | `audio.py` | Sonically similar items (`Audio.sonicallySimilar()`) |
| `/library/sections/{id}/computePath` | GET | `library.py` | Sonic adventure path (`MusicSection.sonicAdventure()`) |

### Plex.tv / MyPlex Endpoints (Cloud Auth)

The spec is PMS-centric and does **not** document any plex.tv cloud APIs. python-plexapi relies heavily on these for authentication, sharing, and sync.

| Path | Method | Source File | What it does |
|------|--------|-------------|--------------|
| `https://plex.tv/api/v2/user` | GET | `myplex.py` | MyPlex account profile |
| `https://plex.tv/api/v2/users/signin` | POST | `myplex.py` | Username/password sign-in (supports 2FA) |
| `https://plex.tv/api/v2/users/signout` | DELETE | `myplex.py` | Invalidate token |
| `https://plex.tv/api/v2/ping` | GET | `myplex.py` | Token refresh ping |
| `https://plex.tv/api/v2/user/webhooks` | GET / POST | `myplex.py` | Webhook management |
| `https://plex.tv/api/v2/user/{uuid}/settings/opt_outs` | GET | `myplex.py` | Online media source opt-outs |
| `https://plex.tv/api/v2/pins/link` | PUT | `myplex.py` | PIN-based linking |
| `https://plex.tv/api/v2/user/view_state_sync` | PUT | `myplex.py` | View state sync |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | POST | `myplex.py` | Share library with friend |
| `https://plex.tv/api/home/users` | GET / POST | `myplex.py` | Plex Home user list / creation |
| `https://plex.tv/api/home/users/{userId}` | DELETE / PUT | `myplex.py` | Remove / update home user |
| `https://plex.tv/api/v2/home/users/restricted/{userId}` | PUT | `myplex.py` | Managed user restrictions |
| `https://plex.tv/api/servers/{machineId}` | GET | `myplex.py` | Server details for sharing |
| `https://plex.tv/api/v2/sharings/{userId}` | PUT / DELETE | `myplex.py` | Update/remove friend share |
| `https://plex.tv/api/claim/token.json` | GET | `myplex.py` | Claim token for new servers |
| `https://sonos.plex.tv/resources` | GET | `myplex.py` | Sonos speaker discovery |
| `https://vod.provider.plex.tv/hubs` | GET | `myplex.py` | VOD hub items |
| `https://music.provider.plex.tv/hubs` | GET | `myplex.py` | Tidal hub items |
| `https://plex.tv/devices/{clientId}/sync_items` | GET / POST | `sync.py` | Mobile sync item list / creation |

### Client Remote-Control Endpoints

The spec does not cover the Plex Client Control Protocol (used by `PlexClient`).

| Path Prefix | Methods | Source File | What it does |
|-------------|---------|-------------|--------------|
| `/player/{command}` | GET (via proxy) | `client.py` | Playback/navigation remote control (pause, play, seek, etc.) |
| `/player/playback/playMedia` | GET (via proxy) | `client.py` | Start playback of a media item on a client |
| `/player/playback/setParameters` | GET (via proxy) | `client.py` | Set shuffle/repeat/volume |
| `/player/playback/setStreams` | GET (via proxy) | `client.py` | Set active audio/subtitle/video streams |
| `/player/timeline/poll` | GET (via proxy) | `client.py` | Poll client playback timeline |
| `/resources` | GET | `client.py` | Client capabilities and device info |

---

## 2. Schema Field Mismatches

Fields that python-plexapi parses from XML responses but which are **not documented** in the corresponding OpenAPI schemas.

### `ServerConfiguration` (root `/`)

| SDK Field | Spec Status | Notes |
|-----------|-------------|-------|
| `diagnostics` | **Type mismatch** | Spec: `string`. SDK parses as `list` (comma-separated diagnostics modules). |
| `transcoderVideoBitrates` | **Type mismatch** | Spec: untyped / description only. SDK parses as `list`. |
| `transcoderVideoQualities` | **Type mismatch** | Spec: `string`. SDK parses as `list`. |
| `transcoderVideoResolutions` | **Type mismatch** | Spec: description only. SDK parses as `list`. |
| `ownerFeatures` | **Type mismatch** | Spec: `string` (comma-separated). SDK parses as `list`. |

### `Metadata` (Movies, Shows, Episodes, Tracks, etc.)

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `artBlurHash` | `video.py`, `audio.py` | **Missing** from `Metadata` schema |
| `thumbBlurHash` | `video.py`, `audio.py` | **Missing** from `Metadata` schema |
| `lastRatedAt` | `video.py`, `audio.py` | **Missing** from `Metadata` schema |
| `editionTitle` | `video.py` (Movie) | **Missing** |
| `languageOverride` | `video.py` (Movie, Show) | **Missing** |
| `enableCreditsMarkerGeneration` | `video.py` (Movie, Show) | **Missing** |
| `useOriginalTitle` | `video.py` (Movie, Show) | **Missing** |
| `slug` | `video.py` (Movie, Show) | **Missing** |
| `skipCount` | `audio.py` (Track) | **Missing** |
| `musicAnalysisVersion` | `audio.py` (Audio base) | **Missing** |
| `distance` | `audio.py` (Audio base) | **Missing** (sonic distance) |
| `sourceURI` | `video.py`, `audio.py`, `playlist.py` | **Missing** (remote/shared server items) |
| `playlistItemID` | `base.py` (Playable) | **Missing** |
| `playQueueItemID` | `base.py` (Playable) | **Missing** |

### `Media`

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `uuid` | `media.py` | **Missing** from `Media` schema |
| `selected` | `media.py` | **Missing** |
| `title` | `media.py` | Present in spec ✅ |

### `Part`

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `protocol` | `media.py` | **Missing** |
| `packetLength` | `media.py` | **Missing** |
| `requiredBandwidths` | `media.py` | **Missing** |
| `syncItemId` | `media.py` | **Missing** |
| `syncState` | `media.py` | **Missing** |
| `deepAnalysisVersion` | `media.py` | **Missing** |
| `decision` | `media.py` | Present in `MediaContainerWithDecision` ✅ |

### `Stream` (Video, Audio, Subtitle, Lyric)

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `bitrateMode` | `media.py` (AudioStream) | **Missing** |
| `visualImpaired` | `media.py` (AudioStream) | **Missing** |
| `albumGain` | `media.py` (AudioStream) | **Missing** (track-only loudness) |
| `albumPeak` | `media.py` (AudioStream) | **Missing** |
| `albumRange` | `media.py` (AudioStream) | **Missing** |
| `endRamp` | `media.py` (AudioStream) | **Missing** |
| `gain` | `media.py` (AudioStream) | **Missing** |
| `loudness` | `media.py` (AudioStream) | **Missing** |
| `lra` | `media.py` (AudioStream) | **Missing** |
| `peak` | `media.py` (AudioStream) | **Missing** |
| `startRamp` | `media.py` (AudioStream) | **Missing** |
| `providerTitle` | `media.py` (SubtitleStream) | **Missing** |
| `score` | `media.py` (SubtitleStream) | **Missing** |
| `sourceKey` | `media.py` (SubtitleStream) | **Missing** |
| `transient` | `media.py` (SubtitleStream) | **Missing** |
| `userID` | `media.py` (SubtitleStream) | **Missing** |
| `minLines` | `media.py` (LyricStream) | **Missing** |
| `provider` | `media.py` (LyricStream) | **Missing** |
| `timed` | `media.py` (LyricStream) | **Missing** |
| `extendedDisplayTitle` | `media.py` (MediaPartStream) | Present in spec ✅ |
| `languageTag` | `media.py` (MediaPartStream) | Present in spec ✅ |
| `streamIdentifier` | `media.py` (MediaPartStream) | Present in spec ✅ |
| `perfectMatch` | `media.py` (SubtitleStream) | **Missing** |

### `Collection`

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `collectionFilterBasedOnUser` | `collection.py` | **Missing** |
| `collectionMode` | `collection.py` | **Missing** |
| `collectionPublished` | `collection.py` | **Missing** |
| `collectionSort` | `collection.py` | **Missing** |
| `artBlurHash` | `collection.py` | **Missing** |
| `thumbBlurHash` | `collection.py` | **Missing** |
| `userRating` | `collection.py` | **Missing** |
| `lastRatedAt` | `collection.py` | **Missing** |

### `Playlist`

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `durationInSeconds` | `playlist.py` | **Missing** |
| `radio` | `playlist.py` | **Missing** |
| `titleSort` | `playlist.py` | **Missing** |
| `librarySectionID` | `playlist.py` | Present in spec ✅ |
| `librarySectionKey` | `playlist.py` | Present in spec ✅ |
| `librarySectionTitle` | `playlist.py` | Present in spec ✅ |

### `PlayQueue`

| SDK Field | Found In | Spec Status |
|-----------|----------|-------------|
| `playQueueLastAddedItemID` | `playqueue.py` | Present in spec ✅ |
| `playQueueSelectedItemID` | `playqueue.py` | Present in spec ✅ |
| `playQueueSelectedItemOffset` | `playqueue.py` | Present in spec ✅ |
| `playQueueSelectedMetadataItemID` | `playqueue.py` | **Missing** |
| `playQueueShuffled` | `playqueue.py` | Present in spec ✅ |
| `playQueueSourceURI` | `playqueue.py` | Present in spec ✅ |
| `playQueueTotalCount` | `playqueue.py` | Present in spec ✅ |
| `playQueueVersion` | `playqueue.py` | Present in spec ✅ |

---

## 3. Parameter / Query Gaps

### Missing or Under-Documented Query Parameters

| Parameter | Where Used | Spec Status |
|-----------|------------|-------------|
| `includeGuids` | Virtually every `fetchItems`/`fetchItem` call in SDK | Only documented on `/library/sections/{sectionId}/all` |
| `checkFiles` | `_INCLUDES` in `base.py` (`PlexPartialObject.reload()`) | Mentioned in description but not a formal parameter on most metadata endpoints |
| `includeMarkers` | `_INCLUDES` in `base.py` | Not formally documented on `/library/metadata/{ids}` |
| `includeChapters` | `_INCLUDES` in `base.py` | Not formally documented on most endpoints |
| `includeExternalMedia` | `_INCLUDES` in `base.py` | Missing from most endpoints |
| `includeExtras` | `_INCLUDES` in `base.py` | Missing from most endpoints |
| `includeRelated` | `_INCLUDES` in `base.py` | Missing from most endpoints |
| `includeOnDeck` | `_INCLUDES` in `base.py` | Missing |
| `includePopularLeaves` | `_INCLUDES` in `base.py` | Missing |
| `includeReviews` | `_INCLUDES` in `base.py` | Missing |
| `includeStations` | `_INCLUDES` in `base.py` | Missing |
| `includeAllConcerts` | `_INCLUDES` in `base.py` | Missing |
| `includeConcerts` | `_INCLUDES` in `base.py` | Missing |
| `includeBandwidths` | `_INCLUDES` in `base.py` | Missing |
| `includeLoudnessRamps` | `_INCLUDES` in `base.py` | Missing |
| `includeGeolocation` | `_INCLUDES` in `base.py` | Missing |
| `includeChildren` | `_INCLUDES` in `base.py` | Missing |
| `includeFields` | `_INCLUDES` in `base.py` | Mentioned in `/status/sessions/history/all` description only |
| `excludeElements` | `_EXCLUDES` in `base.py` | Mentioned in history description only |
| `excludeFields` | `_EXCLUDES` in `base.py` | Mentioned in history description only |
| `skipRefresh` | `_EXCLUDES` in `base.py` | Mentioned on `/library/metadata/{ids}/refresh` |
| `asyncAugmentMetadata=1` | `video.py` (`Video.augmentation()`) | **Missing** |
| `includeFiles` | `server.py` (`PlexServer.browse()`) | **Missing** (endpoint itself is missing) |
| `type=42` | `server.py` (`optimizedItems()`, `conversions()`) | **Missing** from `/playlists` schema |
| `timespan` (values: 1-6) | `server.py` (`bandwidth()`) | **Missing** from `/statistics/bandwidth` (endpoint missing) |
| `accountID`, `deviceID`, `lan` | `server.py` (`bandwidth()`) | **Missing** |
| `playlistType` | `server.py` (`playlists()`) | Present on `/playlists` ✅ |
| `sectionID` | `server.py` (`playlists()`) | Present on `/playlists` ✅ |
| `metadataItemID` | `server.py` (`history()`) | Present on `/status/sessions/history/all` ✅ |
| `viewedAt>` | `server.py` (`history()`) | Present ✅ |

### Header Usage Differences

| Header | SDK Usage | Spec Status |
|--------|-----------|-------------|
| `X-Plex-Container-Start` | Sent on every batched `fetchItems` call | Documented as response header; not always listed as request header |
| `X-Plex-Container-Size` | Sent on every batched `fetchItems` call | Documented as response header; not always listed as request header |
| `X-Plex-Session-Identifier` | Sent on timeline posts | Documented on `/:/timeline` ✅ |

---

## 4. Auth Flow Differences

| Aspect | python-plexapi | OpenAPI Spec |
|--------|----------------|--------------|
| **PMS Auth** | `X-Plex-Token` header (or `X-Plex-Token` query param via `url()`) | `token` security scheme (header-based) ✅ |
| **Plex.tv Sign-In** | `POST https://plex.tv/api/v2/users/signin` with form data (`login`, `password`, `rememberMe`, `verificationCode`) | **Not documented** (spec is PMS-only) |
| **JWT Auth** | `MyPlexJWTLogin` uses Ed25519 keypairs to sign JWTs for auth | **Not documented** |
| **Claim Flow** | `MyPlexAccount.claimToken()` fetches token from `plex.tv/api/claim/token.json`, then `POST /myplex/claim` on PMS | Claim endpoint on PMS is **missing** from spec |
| **Home User Switch** | `POST https://plex.tv/api/home/users/{id}/switch` returns new auth token | **Not documented** |
| **Token Scope** | `PlexServer.createToken(type='delegation', scope='all')` | `/security/token` is present ✅ |
| **User Switching** | `PlexServer.switchUser()` uses admin token to fetch user token, then creates new `PlexServer` instance | Not documented as a formal flow |

---

## 5. Notes on Implementation Patterns

### XML-First Parsing
- The SDK parses **XML** responses, not JSON. All object attributes are read from XML element attributes (`data.attrib.get('...')`).
- The SDK uses **camelCase** throughout to match Plex's XML attribute names exactly.
- The OpenAPI spec describes JSON schemas, but many fields only appear in XML responses (e.g. `artBlurHash`, `thumbBlurHash`).

### Partial Object Auto-Reload
- `PlexPartialObject` implements lazy loading: accessing a `None` attribute triggers `_reload()` with `_INCLUDES`/`_EXCLUDES` parameters.
- This means the SDK relies heavily on metadata detail endpoints with optional include/exclude parameters that are not fully documented in the spec.

### Client-Side Filtering
- `fetchItems()` supports client-side operators (`__gt`, `__contains`, `__regex`, etc.) applied to XML attributes after the server response.
- These operators are **not** server-side query parameters; they are post-processing filters in Python.

### Batched Pagination
- `fetchItems()` automatically paginates using `X-Plex-Container-Start` and `X-Plex-Container-Size` headers.
- The SDK does not use traditional `offset`/`limit` query parameters for pagination; it uses Plex's header-based pagination protocol.

### Multi-Server Awareness
- Playlist items can have `sourceURI` pointing to a different server. The SDK resolves these by looking up the server via `myPlexAccount().resource(serverID).connect()`.
- This cross-server item resolution is not described in the spec.

### Playback & Sync URIs
- The SDK constructs custom `library://` and `server://` URIs for playlists, collections, and sync items.
- These URI schemes are internal to Plex and are used as `uri` parameters when creating playlists, collections, and sync items.

### Client Proxy Pattern
- `PlexClient` can send commands directly to the client device **or** proxy them through the PMS using `X-Plex-Target-Client-Identifier`.
- The proxied client commands are sent to `/player/{command}` on the PMS, which forwards them to the client. This proxy path is not documented in the spec.

---

## Summary

The python-plexapi SDK covers a **significantly broader surface area** than the current OpenAPI spec, particularly in these areas:

1. **Plex.tv cloud APIs** (auth, sharing, sync, home users, webhooks)
2. **Local PMS management endpoints** (diagnostics, statistics, browsing, agents, devices, accounts)
3. **Client remote control protocol** (navigation, playback, timeline polling)
4. **Fine-grained metadata include/exclude parameters** (the `_INCLUDES` / `_EXCLUDES` matrix)
5. **XML-specific fields** (blur hashes, loudness ramps, sync states, on-demand subtitle metadata)

The spec is strongest on core media provider APIs (`/library/metadata`, `/library/sections`, `/playlists`, `/playQueues`, `/transcode`) but lacks many operational and administrative endpoints that the SDK uses daily.
