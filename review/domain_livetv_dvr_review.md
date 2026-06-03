# Live TV & DVR Domain Review

**Date:** 2026-06-03  
**Spec File:** `plex-api-spec.yaml`  
**Domain:** Live TV & DVR (Tags: DVRs, Devices, EPG, Subscriptions, Live TV)  
**Paths Reviewed:** `/livetv/*`, `/media/subscriptions/*`, `/media/grabbers/*`

---

## Endpoints Present in Spec

### DVRs (`/livetv/dvrs`)

| Path | Methods | Tags | Notes |
|------|---------|------|-------|
| `/livetv/dvrs` | GET, POST | DVRs | `POST` requires `admin` scope |
| `/livetv/dvrs/{dvrId}` | GET, DELETE | DVRs | `DELETE` requires `admin` scope |
| `/livetv/dvrs/{dvrId}/lineups` | PUT, DELETE | DVRs | Both require `admin` scope |
| `/livetv/dvrs/{dvrId}/prefs` | PUT | DVRs | Requires `admin` scope |
| `/livetv/dvrs/{dvrId}/reloadGuide` | POST, DELETE | DVRs | Both require `admin` scope |
| `/livetv/dvrs/{dvrId}/channels/{channel}/tune` | POST | DVRs | Tunes a channel |
| `/livetv/dvrs/{dvrId}/devices/{deviceId}` | PUT, DELETE | DVRs | Add/remove device from DVR |

### EPG (`/livetv/epg`)

| Path | Methods | Tags | Notes |
|------|---------|------|-------|
| `/livetv/epg/channelmap` | GET | EPG | Compute best channel map |
| `/livetv/epg/channels` | GET | EPG | Get channels for a lineup |
| `/livetv/epg/countries` | GET | EPG | List countries with EPG data |
| `/livetv/epg/languages` | GET | EPG | List available languages |
| `/livetv/epg/lineup` | GET | EPG | Compute best lineup |
| `/livetv/epg/lineupchannels` | GET | EPG | Get channels across multiple lineups |
| `/livetv/epg/countries/{country}/{epgId}/lineups` | GET | EPG | Lineups by postal code |
| `/livetv/epg/countries/{country}/{epgId}/regions` | GET | EPG | Regions for a country |
| `/livetv/epg/countries/{country}/{epgId}/regions/{region}/lineups` | GET | EPG | Lineups for a region |

### Live TV Sessions (`/livetv/sessions`)

| Path | Methods | Tags | Notes |
|------|---------|------|-------|
| `/livetv/sessions` | GET | Live TV | List all sessions |
| `/livetv/sessions/{sessionId}` | GET | Live TV | Get single session metadata |
| `/livetv/sessions/{sessionId}/{consumerId}/index.m3u8` | GET | Live TV | HLS playlist index |
| `/livetv/sessions/{sessionId}/{consumerId}/{segmentId}` | GET | Live TV | HLS segment delivery |

### Subscriptions (`/media/subscriptions`)

| Path | Methods | Tags | Notes |
|------|---------|------|-------|
| `/media/subscriptions` | GET, POST | Subscriptions | `includeGrabs`, `includeStorage` query params |
| `/media/subscriptions/process` | POST | Subscriptions | Process all subscriptions async |
| `/media/subscriptions/scheduled` | GET | Subscriptions | Scheduled recordings across all subs |
| `/media/subscriptions/template` | GET | Subscriptions | Get subscription template for a GUID |
| `/media/subscriptions/{subscriptionId}` | GET, PUT, DELETE | Subscriptions | Single subscription CRUD |
| `/media/subscriptions/{subscriptionId}/move` | PUT | Subscriptions | Re-order subscription priority |

### Grabbers / Devices (`/media/grabbers`)

| Path | Methods | Tags | Notes |
|------|---------|------|-------|
| `/media/grabbers` | GET | Devices | `protocol` filter (e.g. `livetv`) |
| `/media/grabbers/devices` | GET, POST | Devices | List/add devices |
| `/media/grabbers/devices/discover` | POST | Devices | Trigger device discovery |
| `/media/grabbers/devices/{deviceId}` | GET, DELETE | Devices | Get/remove device |
| `/media/grabbers/devices/{deviceId}/channelmap` | PUT | Devices | Set channel mapping |
| `/media/grabbers/devices/{deviceId}/channels` | GET | Devices | Get device channels |
| `/media/grabbers/devices/{deviceId}/prefs` | PUT | Devices | Set device preferences |
| `/media/grabbers/devices/{deviceId}/scan` | POST, DELETE | Devices | Start/stop channel scan |
| `/media/grabbers/devices/{deviceId}/thumb/{version}` | GET | Devices | Device thumbnail |
| `/media/grabbers/operations/{operationId}` | DELETE | Subscriptions | Cancel an active grab/recording |

### Cross-cutting Observations

- **Plex Pass / admin requirement:** Most write operations require `admin` token scope. Read operations on subscriptions and scheduled recordings return `403` with "User cannot access DVR on this server" when the user lacks DVR privileges.
- **Client info headers:** Every endpoint repeats the full set of `X-Plex-*` client identifier headers. This is consistent with the rest of the spec but verbose.

---

## Missing Endpoints

### 1. Create / Start a Live TV Session

The spec documents `GET /livetv/sessions` and `GET /livetv/sessions/{sessionId}`, but there is **no endpoint to create or start a Live TV session**. In practice, sessions are typically initiated through the transcoder (`/video/:/transcode/universal/start.m3u8`) with a `channel` URI, but a dedicated session-creation endpoint or documentation of the flow is absent.

### 2. Update a DVR

There is no `PUT` or `PATCH` for `/livetv/dvrs/{dvrId}`. The only mutable DVR fields exposed are via `PUT /livetv/dvrs/{dvrId}/prefs` (generic preference key/value). There is no way to change the DVR's `language`, `lineup`, or associated devices in a single structured update.

### 3. List Channels for a Specific DVR

While `/livetv/epg/channels` exists (lineup-scoped), there is no `/livetv/dvrs/{dvrId}/channels` to list channels directly associated with a DVR. The only DVR-scoped channel operation is `POST .../tune`.

### 4. Get Program Guide for a DVR

There is no endpoint to fetch the actual program guide / schedule for a DVR or lineup (e.g., `/livetv/dvrs/{dvrId}/guide` or `/livetv/epg/guide`). The `reloadGuide` endpoints only trigger a background refresh.

### 5. Stop / Terminate a Live TV Session

The spec has no `DELETE` for `/livetv/sessions/{sessionId}`. Sessions appear to be read-only and segment-retrievable, but there is no documented way to tear one down.

### 6. Get DVR Recordings Directly

There is no DVR-centric path for listing completed recordings (e.g., `/livetv/dvrs/{dvrId}/recordings` or `/livetv/recordings`). Recordings are only accessible indirectly through subscription grabs or the generic `/library` metadata endpoints.

### 7. EPG Search / Program Lookup

No endpoint exists to search the EPG for upcoming airings by title, time range, or channel (e.g., `/livetv/epg/search`). This is a common client operation when setting up recording rules.

---

## Schema Corrections

### 1. Inline DVR Schema Duplication

The `DVR` object schema is duplicated inline across **at least 7 endpoints** (`/livetv/dvrs` GET, POST, `/livetv/dvrs/{dvrId}` GET, `/livetv/dvrs/{dvrId}/lineups` PUT/DELETE, `/livetv/dvrs/{dvrId}/prefs` PUT, `/livetv/dvrs/{dvrId}/devices/{deviceId}` PUT/DELETE). It should be extracted to a reusable `#/components/schemas/DVR` component.

### 2. `MediaContainerWithDevice` Duplicates `Device` Schema

`MediaContainerWithDevice` (line 14931) embeds the full `Device` property set inline instead of referencing `#/components/schemas/Device`. This creates maintenance risk if `Device` is updated.

### 3. `DeviceChannel` Not a Reusable Component

The `DeviceChannel` schema (used in `/media/grabbers/devices/{deviceId}/channels` response, line 9832) is defined inline. It has useful fields (`drm`, `favorite`, `hd`, `signalQuality`, `signalStrength`) that are **missing** from the main `Channel` schema. Consider:
- Extracting `DeviceChannel` to a component, or
- Merging these fields into the main `Channel` schema and reusing it.

### 4. `Channel` Schema Missing EPG Fields

The `Channel` schema (line 14401) only has: `title`, `callSign`, `channelVcn`, `hd`, `identifier`, `key`, `language`, `thumb`. It lacks:
- `favorite`
- `drm`
- `signalQuality`
- `signalStrength`

These fields are present in real-world EPG responses and in the inline `DeviceChannel` schema.

### 5. `MediaSubscription` Hint Schemas Are Opaque

`MediaSubscription` (line 15159) declares `Directory`, `Playlist`, and `Video` as:
```yaml
description: Media Matching Hints
additionalProperties: true
```
These are essentially untyped. At minimum, they should document the known hint keys (e.g., `ratingKey`, `title`, `guid`) that clients and the template endpoint rely on.

### 6. `MediaGrabOperation` Description Typo

Line 15125: `A media grab opration represents...` → should be `operation`.

### 7. `MediaContainerWithMetadata` for Sessions Is Too Generic

`/livetv/sessions/{sessionId}` returns `MediaContainerWithMetadata`. A session container may include session-specific fields (e.g., `sessionKey`, `sessionId`, `channel`, `dvrId`, `consumerId`) that are not present in the generic `Metadata` schema. A dedicated `MediaContainerWithLiveTVSession` schema should be considered.

### 8. `Lineup` Schema Missing `key` / `identifier`

The `Lineup` schema (line 14685) has `title`, `type`, `lineupType`, `location`, `uuid`. It does not include `key` or `identifier`, which are commonly returned when listing lineups.

---

## Parameter / Query Gaps

### 1. `/livetv/dvrs` GET — No Filter Params

The list-DVRs endpoint accepts no query parameters. In practice, clients may want to filter by `uuid` or `lineup` when managing multiple DVRs.

### 2. `/livetv/sessions` GET — No Filter Params

No filtering by `dvrId`, `channel`, or active state. For servers with many concurrent Live TV viewers, this makes client-side filtering mandatory.

### 3. `/media/subscriptions` GET — Missing Pagination Headers as Request Params

While `X-Plex-Container-Start` and `X-Plex-Container-Size` are documented as **response headers**, they are not listed as **request parameters** on this endpoint (or most others in the domain). The spec should be consistent about whether these are accepted as request headers/query params for pagination.

### 4. `/media/subscriptions/template` — Missing `type` Param

The template endpoint only documents `guid`. In practice, the type of subscription (show, season, episode, movie) likely influences the template response. A `type` or `targetLibrarySectionID` query param may be required.

### 5. `/media/grabbers/devices/discover` — No Grabber Filter

The discover endpoint takes no parameters. Clients may want to target discovery to a specific `protocol` (e.g., `livetv`) or `grabberIdentifier` to avoid unnecessary network traffic.

### 6. POST `/livetv/dvrs` — `device` Array Format Ambiguity

The `device` parameter is declared as:
```yaml
schema:
  type: array
  items:
    type: string
```
The example shows `device[]=device://tv.plex.grabbers.hdhomerun/1053C0CA`, but the spec does not declare `style: form` / `explode: true`, which may cause code generators to produce incorrect query serialization.

### 7. `/livetv/dvrs/{dvrId}/prefs` — Single `name` Param

The endpoint description says "Set DVR preferences by name and value", but only a `name` parameter is documented. There is no `value` parameter. This suggests the parameter documentation is incomplete or the API expects `name` to contain a composite `key=value` string, which should be clarified.

### 8. `/media/grabbers/devices/{deviceId}/prefs` — Same Issue

Only `name` is documented; no `value` parameter is present despite the summary saying "Set device preferences by its id".

---

## Documentation Improvements

### 1. Typos & Copy-Paste Errors

| Location | Issue | Correction |
|----------|-------|------------|
| `POST /livetv/dvrs` description | "after creation of a **devcie**" | "device" |
| `PUT /livetv/dvrs/{dvrId}/lineups` summary | "Add a DVR Lineup" ✅, but description says "The lineup to **delete**" | "The lineup to add" |
| `PUT /livetv/dvrs/{dvrId}/prefs` description | "by name **avd** value" | "and" |
| `GET /livetv/epg/lineupchannels` summary | "Get the channels for **mulitple** lineups" | "multiple" |
| `MediaGrabOperation` description | "media grab **opration**" | "operation" |

### 2. Live TV Session Lifecycle Is Undocumented

The spec documents how to **list** sessions and **retrieve HLS segments**, but does not explain:
- How sessions are created (transcoder start? tune endpoint?)
- What `sessionId` and `consumerId` represent
- How sessions expire or are terminated
- The expected content type of segments (only `application/vnd.apple.mpegurl` is documented for the index; the segment endpoint has no content-type)

### 3. `reloadGuide` Response Should Be JSON

`POST /livetv/dvrs/{dvrId}/reloadGuide` returns `text/html` with an `X-Plex-Activity` header. If the response body is actually empty or contains a status object, it should be documented as JSON. If it truly returns HTML, that should be noted as a known quirk.

### 4. Tune Endpoint Response Schema

`POST /livetv/dvrs/{dvrId}/channels/{channel}/tune` returns `MediaContainerWithMetadata`. The documentation should clarify what metadata is returned (e.g., the tuned channel's `Metadata` object, or a transcode decision).

### 5. Missing Error Response Documentation

Many endpoints only document `200` and sometimes `404`. Common errors like:
- `400` for invalid lineup / device URIs
- `403` for non-admin users
- `409` for duplicate subscriptions (only documented on `POST /media/subscriptions`)
- `500` for tuning failures (only on `/tune`)

...should be added consistently across the domain.

### 6. Plex Pass Requirement Should Be Explicit

The tag descriptions for DVRs and Subscriptions do not mention that these features require an active Plex Pass subscription and a compatible tuner device. Adding a note to the tag description would help API consumers understand why they receive `403` responses.

### 7. `Channel` Path Parameter on `/tune`

The `channel` path parameter on `/livetv/dvrs/{dvrId}/channels/{channel}/tune` has example `2.1` and type `string`. The description should clarify whether this is a `channelVcn`, a `channelKey`, or a `callSign`.

### 8. `lineupchannels` Response Headers Missing

`GET /livetv/epg/lineupchannels` returns `200` with a JSON body but does not document `X-Plex-Container-Start` / `X-Plex-Container-Total-Size` headers, even though it returns an array of channels.

---

*End of review.*
