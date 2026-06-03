# Devices & Download Queue Domain Review

**Date:** 2026-06-03  
**Scope:** Tags `Devices`, `Download Queue`, plus `/security/*`, `/resources`, `/user`, and related schemas.  
**Sources:** `plex-api-spec.yaml`, `python_plexapi_gap_analysis.md`, `integration_ecosystem_gaps.md`, `undocumented_endpoints_research.md`

---

## Endpoints Present in Spec

### Devices (Media Grabbers / DVR Tuners)

| Path | Method | OperationId | Notes |
|------|--------|-------------|-------|
| `/media/grabbers` | `GET` | `getAvailableGrabbers` | Lists grabber protocols. |
| `/media/grabbers/devices` | `GET` | `listDevices` | Lists all discovered grabber devices. **Admin only.** |
| `/media/grabbers/devices` | `POST` | `addDevice` | Adds a device by URI to an existing grabber. **Admin only.** |
| `/media/grabbers/devices/discover` | `POST` | `discoverDevices` | Triggers SSDP/network discovery. **Admin only.** |
| `/media/grabbers/devices/{deviceId}` | `DELETE` | `removeDevice` | Removes device + channel mappings. **Admin only.** |
| `/media/grabbers/devices/{deviceId}` | `GET` | `getDeviceDetails` | Returns `MediaContainerWithDevice`. **Admin only.** |
| `/media/grabbers/devices/{deviceId}` | `PUT` | `modifyDevice` | Enable/disable device. **Admin only.** |
| `/media/grabbers/devices/{deviceId}/channelmap` | `PUT` | `setChannelmap` | Maps device channels to lineup VCNs/keys. **Admin only.** |
| `/media/grabbers/devices/{deviceId}/channels` | `GET` | `getDevicesChannels` | Returns `DeviceChannel` array. **Admin only.** |
| `/media/grabbers/devices/{deviceId}/prefs` | `PUT` | `setDevicePreferences` | Sets device preferences by name. **Admin only.** |
| `/media/grabbers/devices/{deviceId}/scan` | `DELETE` | `stopScan` | Stops channel scan. |
| `/media/grabbers/devices/{deviceId}/scan` | `POST` | `scan` | Starts channel scan (returns `X-Plex-Activity`). |
| `/media/grabbers/devices/{deviceId}/thumb/{version}` | `GET` | `getThumb` | Device thumbnail image. |
| `/media/grabbers/operations/{operationId}` | `DELETE` | `cancelGrab` | Cancels an active recording/grab. Tagged under `Subscriptions`. |

### Download Queue

| Path | Method | OperationId | Notes |
|------|--------|-------------|-------|
| `/downloadQueue` | `POST` | `createDownloadQueue` | Creates or returns existing queue for client+user. |
| `/downloadQueue/{queueId}` | `GET` | `getDownloadQueue` | Returns queue metadata (`id`, `itemCount`, `status`). |
| `/downloadQueue/{queueId}/add` | `POST` | `addDownloadQueueItems` | Adds items by `keys` array. Reuses many transcoding query params. |
| `/downloadQueue/{queueId}/items` | `GET` | `listDownloadQueueItems` | Lists items with `DecisionResult` + `TranscodeSession`. |
| `/downloadQueue/{queueId}/items/{itemId}` | `DELETE` | `removeDownloadQueueItems` | `itemId` is an array (supports batch delete). |
| `/downloadQueue/{queueId}/items/{itemId}` | `GET` | `getDownloadQueueItems` | Same schema as `listDownloadQueueItems`. |
| `/downloadQueue/{queueId}/items/{itemId}/restart` | `POST` | `restartProcessingDownloadQueueItems` | Reprocess with previous decision params. |
| `/downloadQueue/{queueId}/item/{itemId}/decision` | `GET` | `getItemDecision` | Returns `MediaContainerWithDecision`. |
| `/downloadQueue/{queueId}/item/{itemId}/media` | `GET` | `getDownloadQueueMedia` | Returns raw media file when transcoding complete; `503`+`Retry-After` if not ready. |

### Security / Token / Resources

| Path | Method | OperationId | Tag | Notes |
|------|--------|-------------|-----|-------|
| `/security/resources` | `GET` | `getSourceConnectionInformation` | `General` | Returns connection details + transient token for a source. |
| `/security/token` | `POST` | `getTransientToken` | `General` | Generates delegation token (`type=delegation`, `scope=all`). |
| `/resources` | `GET` | `get-server-resources` | `Plex` | plex.tv API v2. Returns `PlexDevice[]` (servers & clients). |
| `/user` | `GET` | `getTokenDetails` | `Authentication` | plex.tv API v2. Returns `UserPlexAccount`. |

---

## Missing Endpoints

### PMS Local Endpoints (High Impact)

| Path | Method | Used By | Description |
|------|--------|---------|-------------|
| `/clients` | `GET` | python-plexapi, Home Assistant | Lists connected Plex clients (`MediaContainer` of `Server`/`Player` objects). |
| `/accounts` | `GET` | python-plexapi | Lists local system accounts. |
| `/devices` | `GET` | python-plexapi | Lists local system devices (distinct from grabber devices). |
| `/sync/refreshSynclists` | `PUT` | python-plexapi | Forces PMS to download new SyncList from plex.tv. |
| `/sync/refreshContent` | `PUT` | python-plexapi | Forces PMS to refresh content for known SyncLists. |
| `/sync/items/{syncId}` | `GET` | Tautulli | Sync item details. |
| `/sync/transcodeQueue` | `GET` | Tautulli | Sync transcode queue status. |
| `/myplex/claim` | `POST` | python-plexapi | Claims server using plex.tv claim token. |

### Client Remote-Control Protocol (High Impact)

The Plex Client Control Protocol is entirely absent. Proxied via PMS using `X-Plex-Target-Client-Identifier`.

| Path Prefix | Methods | Description |
|-------------|---------|-------------|
| `/player/playback/play` | `POST` | Start playback |
| `/player/playback/pause` | `POST` | Pause |
| `/player/playback/stop` | `POST` | Stop |
| `/player/playback/seek` | `POST` | Seek to time |
| `/player/playback/skipTo` | `POST` | Skip to item |
| `/player/playback/skipBy` | `POST` | Skip forward/backward |
| `/player/playback/stepForward` | `POST` | Step forward |
| `/player/playback/stepBack` | `POST` | Step back |
| `/player/playback/setParameters` | `POST` | Set shuffle/repeat/volume |
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
| `/player/playback/playMedia` | `POST` | Play specific media on client |
| `/player/timeline/poll` | `GET` | Poll client playback timeline |
| `/resources` (on client) | `GET` | Client capabilities and device info |

### plex.tv Cloud Endpoints (Out-of-scope for PMS spec, but referenced)

| Path | Method | Description |
|------|--------|-------------|
| `https://plex.tv/api/v2/devices/{deviceId}/certificate/subject` | `GET` | Device certificate subject (used during claim). |
| `https://plex.tv/api/v2/devices/{deviceId}/certificate/csr` | `PUT` | Upload CSR. |
| `https://plex.tv/api/v2/devices/{deviceId}/certificate/download` | `GET` | Download signed cert. |
| `https://plex.tv/api/v2/release_channels` | `GET` | Release channel info. |
| `https://sonos.plex.tv/resources` | `GET` | Sonos speaker discovery. |

### Real-Time / Websocket

| Path | Description |
|------|-------------|
| `/:/websockets/notifications` | WebSocket event bus for sessions, timeline, status. Used by Tautulli and Home Assistant. Spec documents SSE/EventSource only. |

---

## Schema Corrections

### `Device` Schema (reusable component)

**Current state:** The `Device` schema (`#/components/schemas/Device`) defines only 12 properties:

- `ChannelMapping`, `key`, `lastSeenAt`, `make`, `model`, `modelNumber`, `protocol`, `sources`, `state`, `status`, `tuners`, `uri`, `uuid`

**Issues:**
- **Missing `id`:** The `deviceId` path parameter is typed as `integer`, but the schema has no `id` field.
- **Missing `name` / `title`:** No human-readable device name.
- **Missing `enabled`:** The `PUT /media/grabbers/devices/{deviceId}` endpoint toggles this, but it is not in the schema.
- **Missing `deviceIdentifier`:** Not distinguished from `uuid`.
- **Missing `thumb` / `thumbVersion`:** Referenced by `/media/grabbers/devices/{deviceId}/thumb/{version}`.
- **Missing `lineup` / `lineupType`:** EPG lineup association is absent.
- **No `$ref` usage in responses:** `MediaContainerWithDevice` duplicates the `Device` properties inline instead of referencing `#/components/schemas/Device`. This means fixes must be applied in two places.

### `MediaContainerWithDevice` Schema

**Issue:** Duplicates `Device` properties verbatim instead of using `allOf` + `$ref: '#/components/schemas/Device'`. Should be:

```yaml
MediaContainerWithDevice:
  type: object
  properties:
    MediaContainer:
      allOf:
        - $ref: '#/components/schemas/MediaContainer'
        - type: object
          properties:
            Device:
              type: array
              items:
                $ref: '#/components/schemas/Device'
```

### `Grabber` / `MediaGrabber` Schema

**Issue:** No reusable schema exists. The `GET /media/grabbers` response defines `MediaGrabber` inline with only:
- `identifier`, `protocol`, `title`

**Likely missing fields:**
- `id`, `type`, `deviceType`, `urlBase`, `modelDescription`, `modelNumber`, `modelURL`, `UDN`, `manufacturer`, `manufacturerURL`, `protocols` (array), `features`.

### `DownloadQueue` Schema

**Issue:** Not a reusable component. Defined inline in `POST /downloadQueue` and `GET /downloadQueue/{queueId}`.

**Current fields:** `id`, `itemCount`, `status`

**Likely missing fields:**
- `createdAt`, `updatedAt`, `clientIdentifier`, `userID`, `totalSize`, `identifier`.

### `DownloadQueueItem` Schema

**Issue:** Not a reusable component. Defined inline in `GET /downloadQueue/{queueId}/items` and `GET /downloadQueue/{queueId}/items/{itemId}`.

**Current fields:** `DecisionResult`, `error`, `id`, `key`, `queueId`, `status`, `transcode`, `TranscodeSession`

**Likely missing fields:**
- `createdAt`, `updatedAt`, `downloadUrl`, `metadata` (`Metadata` object), `mediaIndex`, `partIndex`, `optimizedForStreaming`, `videoResolution`, `audioCodec`, `videoCodec`, `container`.

### `PlexDevice` Schema

**Status:** Well-defined reusable schema (`#/components/schemas/PlexDevice`) with 25+ fields. Used by `/resources`.

**Minor issue:** `platform`, `platformVersion`, and `device` are typed as `["null", "string"]` which is correct for optional nullable fields, but the `required` list includes them. This is contradictory — either remove from `required` or remove `null` from type.

### `ServerConfiguration` Schema (cross-domain)

**Issues noted in gap analysis:**
- `diagnostics`: Spec types as `string`; SDK parses as `list` (comma-separated).
- `transcoderVideoBitrates`: Untyped / description only; SDK parses as `list`.
- `transcoderVideoQualities`: Spec types as `string`; SDK parses as `list`.
- `transcoderVideoResolutions`: Description only; SDK parses as `list`.
- `ownerFeatures`: Spec types as `string` (comma-separated); SDK parses as `list`.

---

## Parameter/Query Gaps

### Devices

| Endpoint | Gap | Details |
|----------|-----|---------|
| `GET /media/grabbers` | `protocol` query param | Only documented as `string` with example `livetv`. Should enumerate known protocols (`stream`, `download`, `livetv`). |
| `POST /media/grabbers/devices` | `uri` query param | No format/validation pattern documented. |
| `PUT /media/grabbers/devices/{deviceId}/channelmap` | `channelMapping` / `channelMappingByKey` | `style: deepObject` is used but no formal schema for the nested map keys. |
| `PUT /media/grabbers/devices/{deviceId}/prefs` | `name` query param | Description says "preference names and values" but schema is just `string`. Should be `object` or better documented as `name=value` pairs. |
| `POST /media/grabbers/devices/{deviceId}/scan` | `source` query param | Only example `Cable` given; should list valid scan sources (OTA, Cable, etc.). |

### Download Queue

| Endpoint | Gap | Details |
|----------|-----|---------|
| `POST /downloadQueue/{queueId}/add` | `keys` parameter | `explode: false` array of strings. No max length or format documented. |
| `POST /downloadQueue/{queueId}/add` | Transcoding params | Re-uses ~25 transcoding parameters (e.g., `videoBitrate`, `audioChannelCount`, `subtitles`). These are well-documented individually but the interaction with download-queue transcoding is not described. |
| `GET /downloadQueue/{queueId}/items` | Pagination | No `offset` / `limit` query parameters; relies on `X-Plex-Container-Start` / `X-Plex-Container-Size` headers which are not listed as request parameters. |
| `GET /downloadQueue/{queueId}/item/{itemId}/media` | `Accept` header | Should document required `Accept` header for media file negotiation. |

### Security / Resources

| Endpoint | Gap | Details |
|----------|-----|---------|
| `GET /security/resources` | `source` query param | Required but no enum or example of valid source identifiers. |
| `GET /security/resources` | `refresh` query param | Boolean (`BoolInt`) but behavior is not described. |
| `POST /security/token` | `type` / `scope` | Only `delegation` / `all` are documented. No note on whether additional scopes are planned. |
| `GET /resources` | `includeHttps` / `includeRelay` / `includeIPv6` | Defaults are `0`; should clarify that omitting them is equivalent to `0`. |

---

## Documentation Improvements

### Tag Clarity
1. **Devices tag description** conflates "media grabber devices" (DVR tuners) with "Plex clients/devices". A clarifying note should be added that this tag **only** covers DVR/network tuner devices discovered via SSDP, and that client discovery is handled via `/clients` (missing) or `/resources`.
2. **`/media/grabbers/operations/{operationId}`** is tagged under `Subscriptions` rather than `Devices`. While logically related to subscription recordings, it operates on grabber operations and could be cross-tagged.

### Endpoint Descriptions
1. **`/security/token`** description states "responds to all HTTP verbs but POST is preferred." The spec only documents `POST`. Either document all verbs or restrict the description to `POST` only.
2. **Download Queue endpoints** all carry an `Available: 0.2.0` note with no context. If this refers to an internal API version, it should be documented in the tag description or removed if not actionable for consumers.
3. **`GET /downloadQueue/{queueId}/item/{itemId}/media`** returns `200` with "The raw media file" but has no `content` schema. Should document expected `Content-Type` (e.g., `video/mp4`, `application/octet-stream`) and note that the actual type depends on the transcode decision.
4. **`GET /media/grabbers/devices/{deviceId}/thumb/{version}`** returns `200` with "The thumbnail for the device" but has no `content` schema. Should document `image/jpeg` or `image/png` response type.

### Schema Documentation
1. **`Device` schema** should be expanded and referenced consistently. The SSDP example in the tag description lists fields (`UDN`, `URLBase`, `deviceType`, `serviceType`, `serviceId`, `friendlyName`, `manufacturer`, `modelDescription`, `modelName`, `modelNumber`) that do not appear in the `Device` schema at all.
2. **`MediaGrabber` inline schema** should become a reusable component with complete fields.
3. **`DownloadQueue` and `DownloadQueueItem` inline schemas** should be promoted to reusable components under `#/components/schemas/`.
4. **`TranscodeSession` schema** is referenced by `DownloadQueueItem` but is minimal. The comment in the spec admits it is "not yet documented." This is a known gap but should be prioritized.

### Cross-References
1. Add a note in the `Devices` tag pointing to the `DVRs`, `EPG`, `Live TV`, and `Subscriptions` tags, since grabber devices are tightly coupled with DVR functionality.
2. Add a note in the `Download Queue` tag explaining that this is the **server-side sync/optimization queue** (used for mobile sync and optimized versions), distinct from the client-side `Play Queue`.
