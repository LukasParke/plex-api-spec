# Server & System Domain Review

**Date:** 2026-06-03  
**Domain:** Server & System (General, Activities, Butler, Updater, Log, Preferences, Events, UltraBlur, Transcoder, Status)  
**Spec File:** `plex-api-spec.yaml` (16,989 lines)

---

## Endpoints Present in Spec (inventory with assessment)

### General
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/` | GET | General | ⚠️ **Schema mismatch.** Returns `MediaContainerWithDirectory`, but the actual response body contains `ServerConfiguration` fields (e.g. `machineIdentifier`, `version`, `platform`, `myPlex`, etc.). The `Directory` array is present but the container itself is server config. |
| `/identity` | GET | General | ✅ Clean. Returns `claimed`, `machineIdentifier`, `version`. Unauthenticated. |

### Activities
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/activities` | GET | Activities | ⚠️ **Inline schema.** `Activity` is defined inline in the response; not a reusable component. No `200` response headers documented. Missing `X-Plex-Activity` header documented elsewhere. |
| `/activities/{activityId}` | DELETE | Activities | ✅ Clean. Path param `activityId` documented. Returns 200/400/404. |

### Butler
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/butler` | GET / DELETE / POST | Butler | ⚠️ **Inline schema.** `ButlerTask` is defined inline. `GET` returns tasks list; `DELETE` stops all; `POST` starts all. Admin-only security is correct. |
| `/butler/{butlerTask}` | DELETE / POST | Butler | ✅ Clean. Comprehensive enum of 24 task names. Admin-only. |

### Updater
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/updater/apply` | PUT | Updater | ✅ Clean. Params `tonight` and `skip` (BoolInt). Returns text/html. |
| `/updater/check` | PUT | Updater | ✅ Clean. Param `download` (BoolInt). |
| `/updater/status` | GET | Updater | ⚠️ **Inline schema.** `UpdaterStatus` / `Release` objects are inline. Missing `checkedAt` type clarity (integer timestamp). |

### Log
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/log` | PUT / POST | Log | ⚠️ **No response schema.** PUT writes a single line; POST writes multi-line plain text. No `LogLine` schema exists. Level enum (0-4) is correct. |
| `/log/networked` | POST | Log | ⚠️ **Undocumented response.** Enables Papertrail logging. Param `minutes` documented. Returns only generic 200/403. |

### Preferences
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/:/prefs` | GET / PUT | Preferences | ⚠️ **GET lacks auth?** GET has no `security` block (should likely be admin). PUT uses generic `prefs: object` query param instead of documenting known keys. Hidden preferences (~40+ keys) are not documented. |
| `/:/prefs/get` | GET | Preferences | ✅ Clean. Single preference fetch by `id`. |

### Rate / Timeline / Scrobble
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/:/rate` | PUT | Rate | ✅ Clean. Params `identifier`, `key`, `rating` (0-10), `ratedAt`. |
| `/:/timeline` | POST | Timeline | ✅ Extensive params for playback reporting. Documents `state` enum, bandwidth, buffering, etc. |
| `/:/scrobble` | GET | — | 📍 **Not in primary domain review** but related to playback progress. |
| `/:/unscrobble` | GET | — | 📍 **Not in primary domain review** but related to playback progress. |

### Events
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/:/eventsource/notifications` | GET | Events | ⚠️ **No message schema.** Returns `application/octet-stream`. Filter param documented but no SSE event schemas. |
| `/:/websocket/notifications` | GET | Events | ⚠️ **No message schema.** Returns `application/octet-stream`. Filter param documented but no WebSocket message schemas (`NotificationContainer`, `PlaySessionStateNotification`, `StatusNotification`, `ReachabilityNotification`). |

### UltraBlur
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/services/ultrablur/colors` | GET | UltraBlur | ✅ Clean. `url` param. Returns `UltraBlurColors` array. |
| `/services/ultrablur/image` | GET | UltraBlur | ✅ Clean. Color quadrant params documented. |

### Transcoder (Universal)
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/{transcodeType}/:/transcode/universal/decision` | GET | Transcoder | ✅ Extensive params for playback decision. Returns `MediaContainerWithDecision`. |
| `/{transcodeType}/:/transcode/universal/start.{extension}` | GET | Transcoder | ✅ Supports `m3u8` and `mpd`. Extensive params duplicated from `/decision`. |
| `/{transcodeType}/:/transcode/universal/fallback` | POST | Transcoder | ✅ Clean. Session-based fallback trigger. |
| `/{transcodeType}/:/transcode/universal/subtitles` | GET | Transcoder | ✅ Clean. Subtitle-only transcode params. |

### Status (Partial)
| Path | Method | Tag | Assessment |
|------|--------|-----|------------|
| `/status/sessions` | GET | Status | ✅ Clean. Returns `Metadata` with `Player`, `Session`, `User`. Admin-only. |
| `/status/sessions/background` | GET | Status | ⚠️ **Inline schema.** `TranscodeJob` is inline. Missing some fields like `generatorID` vs `generatorID` casing? (spec has `generatorID`). |
| `/status/sessions/history/all` | GET | Status | ⚠️ **Partial params.** Mentions `includeFields`, `excludeFields`, `includeElements`, `excludeElements` in description but does not formally declare them as query parameters. |
| `/status/sessions/terminate` | POST | Status | ✅ Clean. `sessionId` and `reason` params. |
| `/status/sessions/history/{historyId}` | GET | Status | 📍 Present but not primary focus of this review. |

---

## Missing Endpoints

The following endpoints are used by `python-plexapi`, Tautulli, Home Assistant, or community research but are **absent** from the spec.

### Server Discovery & Identity
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/servers` | GET | Tautulli | Local server list. |
| `/myplex/account` | GET | Tautulli | Linked MyPlex account info on PMS. |
| `/myplex/refreshReachability` | PUT | Tautulli | Refresh remote access port mapping. |

### Clients & Devices
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/clients` | GET | python-plexapi, HA | Lists connected `PlexClient` objects. Returns `MediaContainer` of `Server`/`Player` objects. |
| `/accounts` | GET | python-plexapi | Lists local system accounts (`PlexServer.systemAccounts()`). |
| `/devices` | GET | python-plexapi | Lists local system devices (`PlexServer.systemDevices()`). |

### System & Agents
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/system/agents` | GET | python-plexapi | Lists available metadata agents. |
| `/system/agents/{agentId}` | GET | Community | Agent details & settings. |
| `/system/settings` | GET | Community | System-level settings. |
| `/system/updates` | GET | Community | Check for PMS updates (alternative to `/updater/check`). |

### Diagnostics & Statistics
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/diagnostics` | GET | Community | Server diagnostics overview. |
| `/diagnostics/databases` | GET | python-plexapi | Downloads server DB diagnostics. |
| `/diagnostics/logs` | GET | python-plexapi | Downloads server logs bundle. |
| `/statistics/bandwidth` | GET | python-plexapi | Dashboard bandwidth data. Missing `timespan` (1-6), `accountID`, `deviceID`, `lan` params. |
| `/statistics/resources` | GET | python-plexapi | Dashboard resource data. |

### Sync
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/sync` | GET | Community | Sync status overview. |
| `/sync/items` | GET | Community / Tautulli | Sync items list. |
| `/sync/items/{syncId}` | GET | Tautulli | Sync item details. |
| `/sync/queue` | GET | Community | Sync queue. |
| `/sync/transcodeQueue` | GET | Tautulli | Sync transcode queue status. |
| `/sync/refreshSynclists` | PUT | python-plexapi | Forces PMS to download new SyncList from plex.tv. |
| `/sync/refreshContent` | PUT | python-plexapi | Forces PMS to refresh content for known SyncLists. |

### Browse
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/services/browse` | GET | python-plexapi | Browses filesystem paths. Missing `includeFiles` param. |
| `/services/browse/{base64path}` | GET | python-plexapi | Browses a specific filesystem path. |

### Playback Progress
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/:/progress` | GET | python-plexapi | Updates watch progress (`Playable.updateProgress()`). |

### Transcoder (Missing)
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/transcode/sessions` | GET | Community | Active transcode sessions. |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.m4s` | GET | Community | DASH segment delivery. |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.ts` | GET | Community | HLS TS segment delivery. |
| `/music/:/transcode` | GET | Community | Audio transcode endpoint. |

### Real-Time Events (Missing Schema)
| Path | Method | Source | Notes |
|------|--------|--------|-------|
| `/:/websockets/notifications` | WS | Tautulli, HA | WebSocket path is present but **message schema is absent**. |

---

## Schema Corrections

### `ServerConfiguration`
Used at `/media/providers` and in `LibrarySections` response, but **most importantly** the root `/` endpoint returns these fields. The spec incorrectly labels `/` as returning `MediaContainerWithDirectory`.

| Field | Spec Status | Issue | Recommended Fix |
|-------|-------------|-------|-----------------|
| `diagnostics` | `string` | SDK parses as `list` (comma-separated diagnostics modules). | Change to `array` of `string`, or document as comma-separated list with `parseAs: list` hint. |
| `transcoderVideoBitrates` | untyped / description only | SDK parses as `list`. | Add `type: array` with `items: string` or `integer`. |
| `transcoderVideoQualities` | `string` | SDK parses as `list`. | Change to `array` of `string` / `integer`. |
| `transcoderVideoResolutions` | description only | SDK parses as `list`. | Add `type: array` of `string`. |
| `ownerFeatures` | `string` | SDK parses as `list` (comma-separated). | Change to `array` of `string`, or document parsing rule. |

**Additional issue:** `offlineTranscode` is documented as `example: 1` but has no `type`. Should be `integer` or `boolean` (BoolInt pattern).

### `Activity`
Defined inline under `/activities` GET response (lines 728-763). Should be extracted to `#/components/schemas/Activity`.

| Field | Status | Notes |
|-------|--------|-------|
| `uuid` | Present | Good. |
| `type` | Present | Good. |
| `title` | Present | Good. |
| `subtitle` | Present | Good. |
| `progress` | Present | Good (-1 to 100). |
| `cancellable` | Present | Good. |
| `userID` | Present | Good. |
| `Context` | Present | `additionalProperties: true` is permissive but correct. |
| `Response` | Present | `additionalProperties: true` is permissive but correct. |

**Missing:** No standalone component means it cannot be reused by other endpoints that may return activities (e.g., websocket `StatusNotification`).

### `ButlerTask`
Defined inline under `/butler` GET response (lines 798-819). Should be extracted to `#/components/schemas/ButlerTask`.

| Field | Status | Notes |
|-------|--------|-------|
| `name` | Present | Good. |
| `title` | Present | Good. |
| `description` | Present | Good. |
| `enabled` | Present | Good. |
| `interval` | Present | Good (days). |
| `scheduleRandomized` | Present | Good. |

### `UpdaterStatus`
Defined inline under `/updater/status` GET response (lines 3956-3984+). Should be extracted to `#/components/schemas/UpdaterStatus`.

| Field | Status | Notes |
|-------|--------|-------|
| `autoUpdateVersion` | Present | Good. |
| `canInstall` | Present | Good. |
| `checkedAt` | Present | Good. |
| `downloadURL` | Present | Good. |
| `Release` | Present | Array with `added`, `fixed`, `downloadURL`, `key`, etc. |

### `LogLine`
**Does not exist.** The `/log` endpoints return generic `200` responses with no schema. If the endpoints ever return the logged line or a confirmation object, it should be documented.

### `MediaContainerWithDecision` (Transcoder)
Present and comprehensive. However, the `decision` enum on `Part` and `Stream` is well-defined (`directplay`, `transcode`, `copy`, `burn`, etc.). ✅

---

## Parameter / Query Gaps

### Preferences (`/:/prefs`)
- **PUT `/:/prefs`** uses a single `prefs: object` query parameter. It should document the known public keys (`FriendlyName`, `ScheduledLibraryUpdateInterval`, `sendCrashReports`, etc.) and note that hidden keys are also accepted.
- **Hidden preference keys** (~40+) are not documented anywhere in the spec. Examples:
  - `aBRKeepOldTranscodes`, `allowHighOutputBitrates`, `backgroundQueueIdlePaused`
  - `butlerTaskGarbageCollectBlobs`, `butlerTaskGenerateMediaIndexFiles`
  - `certificateVersion`, `dvrShowUnsupportedDevices`, `enableABRDebugOverlay`
  - `hardwareDevicePath`, `manualPortMappingMode`, `manualPortMappingPort`
  - `transcoderH264MinimumCRF`, `transcoderH264Options`, `transcoderH264Preset`
  - `transcoderLogLevel`, `transcoderLivePruneBuffer`
  - Source: [Python PlexAPI settings docs](https://python-plexapi.readthedocs.io/en/latest/modules/settings.html)

### History (`/status/sessions/history/all`)
- Mentions `includeFields`, `excludeFields`, `includeElements`, `excludeElements` in the **description** but does not formally declare them as query parameters. These should be added as explicit parameters.
- Also missing formal `X-Plex-Container-Start` and `X-Plex-Container-Size` **request** parameters (they are documented as response headers but used for request pagination by many clients).

### Updater
- `/updater/check` documents `download` as BoolInt. Tautulli uses `download=0`. The spec is technically correct but could note that `0` explicitly skips download.

### Transcoder Universal
- Missing segment delivery path parameters:
  - `sessionId` (path) and `segmentId` (path) for `.m4s` / `.ts` segment URLs.
- Missing audio-specific transcoder path `/music/:/transcode`.
- Some stream URL parameters are accepted but not documented on all transcoder endpoints:
  - `maxVideoBitrate`, `videoResolution`, `offset`, `copyts`, `protocol`, `mediaIndex`, `partIndex`, `platform`.

### Timeline (`/:/timeline`)
- Generally well-documented. Missing `X-Plex-Session-Identifier` as a formal parameter? It is present. ✅

### Root `/`
- Missing `X-Plex-Token` as a query parameter option. The SDK often passes token via `url()` query param, not just header.

---

## Documentation Improvements

1. **Root `/` response schema**
   - The description says "Information about this PMS setup and configuration" but the schema is `MediaContainerWithDirectory`. The actual response is a `ServerConfiguration`-shaped object with a `Directory` array. Update the schema to `allOf: [ServerConfiguration, { Directory: ... }]`.

2. **Event / WebSocket / Eventsource message schemas**
   - The spec documents the connection endpoints but provides **no schemas** for the messages that flow over them.
   - Missing: `NotificationContainer`, `PlaySessionStateNotification`, `TimelineEntry`, `StatusNotification`, `ReachabilityNotification`.
   - These are critical for Tautulli and Home Assistant integrations.

3. **Activity, ButlerTask, UpdaterStatus should be components**
   - Extract inline schemas to `#/components/schemas/` so they can be referenced by other endpoints and generated SDKs.

4. **Log endpoint responses**
   - Document whether `/log` PUT/POST returns any body, and if so, what it contains.

5. **Preference setting documentation**
   - Add an `example` or `enum` of common preference keys to the `PUT /:/prefs` operation description.
   - Add a note about hidden/advanced preference keys and link to Plex support article.

6. **Transcoder segment delivery**
   - Document the segment delivery URLs (`.../session/{sessionId}/{segmentId}.m4s` / `.ts`) even if they are primarily streaming URLs rather than REST API calls.

7. **Auth consistency**
   - `GET /:/prefs` lacks a `security` block. It should likely require `token: [admin]` like `PUT /:/prefs`.
   - `/identity` correctly allows unauthenticated access (`security: [{}]`). ✅

8. **Missing tags**
   - Some endpoints like `/:/scrobble` and `/:/unscrobble` are not tagged with a domain tag (they appear tag-less or under an implicit tag). Verify they are categorized.

---

*End of review.*
