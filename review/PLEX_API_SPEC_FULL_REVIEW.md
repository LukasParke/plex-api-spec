# Plex OpenAPI Specification — Full Review & Gap Analysis

**Date:** 2026-06-03  
**Spec Analyzed:** `plex-api-spec.yaml` (≈17,000 lines, OpenAPI 3.1.1)  
**Research Inputs:** 10 domain reports from Phase 1 (SDK gap analysis, integration ecosystem survey, undocumented endpoint research) and Phase 2 (domain-specific reviews).  
**Scope:** PMS local server API, plex.tv cloud API, client remote-control protocol, cloud providers, real-time event streams, and webhook payloads.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Missing Endpoints](#2-missing-endpoints)
3. [Schema Corrections](#3-schema-corrections)
4. [Parameter & Query String Corrections](#4-parameter--query-string-corrections)
5. [Response Corrections](#5-response-corrections)
6. [Security & Auth Improvements](#6-security--auth-improvements)
7. [Documentation Improvements](#7-documentation-improvements)
8. [Speakeasy / SDK Generator Improvements](#8-speakeasy--sdk-generator-improvements)
9. [Appendix: Raw Research Files](#9-appendix-raw-research-files)

---

## 1. Executive Summary

### High-Level Stats

| Metric | Count |
|--------|-------|
| **Endpoints present in spec (reviewed)** | ~235 |
| **Missing endpoints identified** | ~175 |
| **Schema components with issues** | ~32 |
| **Individual schema field/type gaps** | ~75 |
| **Parameter / query gaps** | ~80 |
| **Response / status-code issues** | ~15 |
| **Auth / security gaps** | ~18 |
| **Documentation issues (typos, missing desc, examples, tags)** | ~45 |

### Coverage by Domain

| Domain | Present | Missing | Priority |
|--------|---------|---------|----------|
| plex.tv Auth & Account | 6 | ~40 | **CRITICAL / HIGH** |
| Plex Cloud Providers (Discover, VOD, Music) | 0 | ~7 | **HIGH** |
| Server Management & System | ~35 | ~20 | MEDIUM |
| Library & Metadata | ~85 | ~35 | MEDIUM / HIGH |
| Playback & Sessions | ~25 | ~30 | HIGH |
| Live TV & DVR | ~25 | ~7 | MEDIUM |
| Devices & Download Queue | ~20 | ~10 | MEDIUM |
| Client Remote-Control | 0 | ~25 | **HIGH** |
| Webhooks & Real-Time | 1 (WS path, no schema) | ~3 | MEDIUM / HIGH |

### Key Takeaways

1. **The spec is PMS-centric and omits the entire plex.tv v2 surface.** Authentication (OAuth PIN, JWT device registration, sign-out), account management, sharing, Plex Home, and webhooks are almost entirely absent. This blocks every modern third-party integration from generating a working auth flow.
2. **Client remote control is undocumented.** The `/player/playback/*` and `/player/timeline/poll` endpoints are the backbone of Plex client control but do not appear in the spec.
3. **Cloud provider endpoints (Discover, VOD, Music) are missing.** Watchlist, search, and add/remove actions on `discover.provider.plex.tv` are now canonical but undocumented.
4. **Schema reuse is poor.** `Activity`, `ButlerTask`, `UpdaterStatus`, `DeviceChannel`, `DownloadQueue`, `DownloadQueueItem`, `DVR`, `HistoryItem`, `PlayQueue`, and others are defined inline or duplicated instead of using `$ref`.
5. **The include/exclude parameter matrix is missing.** Critical parameters such as `includeMarkers`, `includeGuids`, `includeChapters`, `includeExtras`, `includeRelated`, and `excludeFields` are mentioned only in descriptions or missing entirely.
6. **XML-first behavior is not explained.** Many fields (blur hashes, loudness ramps, sync states) only appear in XML responses and are absent from JSON unless explicitly requested.

---

## 2. Missing Endpoints

### 2.1 plex.tv Authentication & Account

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `https://plex.tv/api/v2/pins` | `POST` | **CRITICAL** | Tautulli, Overseerr, Bazarr, python-plexapi, undocumented endpoints | OAuth PIN generation — entry point for every modern integration |
| `https://plex.tv/api/v2/pins/{pinId}` | `GET` | **CRITICAL** | Tautulli, Overseerr, Bazarr, python-plexapi | Poll PIN status; returns `authToken` when claimed |
| `https://plex.tv/api/v2/pins/link` | `PUT` | **CRITICAL** | python-plexapi, undocumented endpoints | Link a PIN to an account (OAuth completion) |
| `https://clients.plex.tv/api/v2/pins` | `POST` | **CRITICAL** | python-plexapi, undocumented endpoints | Alternative PIN endpoint (clients subdomain) |
| `https://plex.tv/api/v2/users/signout` | `DELETE` | **HIGH** | python-plexapi, undocumented endpoints | Invalidate token |
| `https://plex.tv/api/v2/ping` | `GET` | **HIGH** | Tautulli, Overseerr, python-plexapi, undocumented endpoints | Token refresh / health check (no auth required) |
| `https://plex.tv/api/v2/features` | `GET` | **HIGH** | Plex Forum, undocumented endpoints | Plex Pass feature flags |
| `https://plex.tv/api/v2/friends` | `GET` | **HIGH** | Plex Forum, undocumented endpoints | Friends & shared users (v2 JSON) |
| `https://plex.tv/api/v2/home` | `GET` | **HIGH** | Plex Forum, undocumented endpoints | Plex Home user list |
| `https://plex.tv/api/v2/server` | `GET` | **HIGH** | Plex Forum, undocumented endpoints | Server association info for logged-in user |
| `https://plex.tv/api/v2/users/password` | `POST` | **HIGH** | Plex Forum, undocumented endpoints | Change / reset password |
| `https://plex.tv/api/v2/user/view_state_sync` | `PUT` | **HIGH** | python-plexapi, undocumented endpoints | Enable/disable watch-state sync consent |
| `https://plex.tv/api/v2/user/{uuid}/settings/opt_outs` | `GET` | **HIGH** | python-plexapi, undocumented endpoints | Online-media-source opt-outs |
| `https://plex.tv/users/account` | `GET` | **HIGH** | Tautulli, Overseerr, undocumented endpoints | Own account details (XML) |
| `https://plex.tv/users/account.json` | `GET` | **HIGH** | Tautulli, Overseerr | Own account details (JSON) |
| `https://plex.tv/api/v2/shared_servers` | `POST` | **HIGH** | python-plexapi, Plexopedia, undocumented endpoints | Share a server with a user |
| `https://plex.tv/api/v2/sharings/{userId}` | `PUT` | **HIGH** | python-plexapi, undocumented endpoints | Update friend filters (allowSync, filterMovies, etc.) |
| `https://plex.tv/api/v2/sharings/{userId}` | `DELETE` | **HIGH** | python-plexapi, undocumented endpoints | Remove a share / friend |
| `https://plex.tv/api/v2/home/users/restricted/{userId}` | `PUT` | **HIGH** | python-plexapi, undocumented endpoints | Update restricted (managed) home user settings |
| `https://plex.tv/api/home/users` | `GET` / `POST` | **HIGH** | python-plexapi | List / create Plex Home users |
| `https://plex.tv/api/home/users/{userId}` | `DELETE` / `PUT` | **HIGH** | python-plexapi | Remove / update home user |
| `https://plex.tv/api/home/users/{id}/switch` | `POST` | **HIGH** | python-plexapi | Switch to home user (returns new auth token) |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | `POST` | **HIGH** | python-plexapi, Tautulli, undocumented endpoints | Share library with friend (legacy v1) |
| `https://plex.tv/api/servers/{machineId}` | `GET` | **HIGH** | python-plexapi, undocumented endpoints | Server details for sharing |
| `https://plex.tv/api/claim/token.json` | `GET` | **HIGH** | python-plexapi | Claim token for new servers |
| `POST /myplex/claim` | `POST` | **HIGH** | python-plexapi, devices review | Claim server on PMS using claim token |
| `https://plex.tv/api/v2/server/access_tokens` | `GET` | **MEDIUM** | CVE-2025-34158 write-up, undocumented endpoints | List access tokens for the server |
| `https://plex.tv/api/v2/server/users/features` | `GET` | **MEDIUM** | Plex Forum, undocumented endpoints | Features enabled per shared user |
| `https://plex.tv/api/v2/cloud_server` | `GET` | **MEDIUM** | Tautulli | Plex Cloud status |
| `https://plex.tv/api/v2/geoip` | `GET` | **MEDIUM** | Tautulli | GeoIP lookup |
| `https://plex.tv/:/ip` | `GET` | **MEDIUM** | Tautulli | Public IP detection |
| `https://plex.tv/api/downloads/{channel}.json` | `GET` | **LOW** | Tautulli | Plex update downloads |
| `https://plex.tv/pins.xml` | `POST` | **LOW** | plexargod, undocumented endpoints | Legacy PIN creation (XML) |
| `https://plex.tv/pins/{pinId}` | `GET` | **LOW** | plexargod, undocumented endpoints | Legacy PIN check (XML) |
| `https://plex.tv/api/resources` | `GET` | **LOW** | plexargod, undocumented endpoints | Legacy published server connections (XML) |
| `https://plex.tv/api/users/` | `GET` | **LOW** | python-plexapi, undocumented endpoints | Legacy friends list (XML) |
| `https://clients.plex.tv/devices.xml` | `GET` | **LOW** | CVE-2025-34158 write-up, undocumented endpoints | Authorized devices with tokens (XML) |

### 2.2 JWT Device Registration (new 2025)

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `https://clients.plex.tv/api/v2/auth/jwk` | `POST` | **MEDIUM** | Plex Pro Week blog, JonnyWong16 gist | Register device public key (JWK) |
| `https://clients.plex.tv/api/v2/auth/nonce` | `GET` | **MEDIUM** | JonnyWong16 gist | Get nonce to sign in client JWT |
| `https://clients.plex.tv/api/v2/auth/token` | `POST` | **MEDIUM** | JonnyWong16 gist | Exchange signed client JWT for Plex JWT |
| `https://clients.plex.tv/api/v2/auth/keys` | `GET` | **MEDIUM** | JonnyWong16 gist | Plex public JWKs for signature verification |

### 2.3 Plex Cloud Providers (Discover, VOD, Music, Metadata)

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `https://discover.provider.plex.tv/library/search` | `GET` | **HIGH** | python-plexapi, Overseerr, Jellyseerr, undocumented endpoints | Discover search (movies & shows) |
| `https://discover.provider.plex.tv/library/sections/watchlist/all` | `GET` | **HIGH** | Overseerr, Jellyseerr, undocumented endpoints | Plex Discover watchlist |
| `https://discover.provider.plex.tv/actions/addToWatchlist` | `POST` | **HIGH** | pd_zurg, undocumented endpoints | Add to watchlist |
| `https://discover.provider.plex.tv/actions/removeFromWatchlist` | `POST` | **HIGH** | pd_zurg, undocumented endpoints | Remove from watchlist |
| `https://metadata.provider.plex.tv/library/sections/watchlist/all` *(deprecated)* | `GET` | **LOW** | Tautulli, undocumented endpoints | Legacy watchlist (deprecated Oct 2025) |
| `https://metadata.provider.plex.tv/actions/addToWatchlist` *(deprecated)* | `POST` | **LOW** | undocumented endpoints | Legacy add (deprecated) |
| `https://metadata.provider.plex.tv/actions/removeFromWatchlist` *(deprecated)* | `POST` | **LOW** | undocumented endpoints | Legacy remove (deprecated) |
| `https://vod.provider.plex.tv/hubs` | `GET` | **HIGH** | python-plexapi, Netify, undocumented endpoints | VOD hub items |
| `https://music.provider.plex.tv/hubs` | `GET` | **HIGH** | python-plexapi, undocumented endpoints | Tidal / music hub items |

### 2.4 Server Management & System

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `/library` | `GET` | **MEDIUM** | python-plexapi | Root Library object |
| `/library/sections/` | `GET` | **MEDIUM** | python-plexapi | Fallback for non-owners to list sections |
| `/servers` | `GET` | **MEDIUM** | Tautulli | Local server list |
| `/accounts` | `GET` | **MEDIUM** | python-plexapi, Home Assistant | Local system accounts |
| `/devices` | `GET` | **MEDIUM** | python-plexapi | Local system devices |
| `/clients` | `GET` | **MEDIUM** | python-plexapi, Home Assistant | Lists connected Plex clients |
| `/system/agents` | `GET` | **MEDIUM** | python-plexapi, undocumented endpoints | Lists available metadata agents |
| `/system/agents/{agentId}` | `GET` | **MEDIUM** | undocumented endpoints | Agent details & settings |
| `/system/settings` | `GET` | **MEDIUM** | undocumented endpoints | System-level settings |
| `/system/updates` | `GET` | **MEDIUM** | undocumented endpoints | Check for PMS updates |
| `/services/browse` | `GET` | **MEDIUM** | python-plexapi | Browse filesystem paths |
| `/services/browse/{base64path}` | `GET` | **MEDIUM** | python-plexapi | Browse specific filesystem path |
| `/diagnostics` | `GET` | **MEDIUM** | undocumented endpoints | Server diagnostics overview |
| `/diagnostics/databases` | `GET` | **MEDIUM** | python-plexapi | Download server DB diagnostics |
| `/diagnostics/logs` | `GET` | **MEDIUM** | python-plexapi | Download server logs bundle |
| `/statistics/bandwidth` | `GET` | **MEDIUM** | python-plexapi | Dashboard bandwidth data |
| `/statistics/resources` | `GET` | **MEDIUM** | python-plexapi | Dashboard resource data |
| `/myplex/account` | `GET` | **MEDIUM** | Tautulli | Linked MyPlex account info on PMS |
| `/myplex/refreshReachability` | `PUT` | **MEDIUM** | Tautulli | Refresh remote access port mapping |
| `/sync` | `GET` | **MEDIUM** | undocumented endpoints | Sync status overview |
| `/sync/items` | `GET` | **MEDIUM** | undocumented endpoints | Sync items list |
| `/sync/items/{syncId}` | `GET` | **MEDIUM** | Tautulli | Sync item details |
| `/sync/queue` | `GET` | **MEDIUM** | undocumented endpoints | Sync queue |
| `/sync/transcodeQueue` | `GET` | **MEDIUM** | Tautulli | Sync transcode queue status |
| `/sync/refreshSynclists` | `PUT` | **MEDIUM** | python-plexapi | Force PMS to download new SyncList from plex.tv |
| `/sync/refreshContent` | `PUT` | **MEDIUM** | python-plexapi | Force PMS to refresh content for known SyncLists |
| `/transcode/sessions` | `GET` | **MEDIUM** | undocumented endpoints, server review | Active transcode sessions |

### 2.5 Library & Metadata

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `/library/sections/{id}/onDeck` | `GET` | **MEDIUM** | client traffic, undocumented endpoints | On-deck items for this section |
| `/library/sections/{id}/unwatched` | `GET` | **MEDIUM** | client traffic | Unwatched items |
| `/library/sections/{id}/newest` | `GET` | **MEDIUM** | client traffic | Newest additions |
| `/library/sections/{id}/recentlyAdded` | `GET` | **MEDIUM** | Tautulli | Per-library recently added |
| `/library/sections/{id}/byYear` | `GET` | **LOW** | client traffic | Browse by year |
| `/library/sections/{id}/byDecade` | `GET` | **LOW** | client traffic | Browse by decade |
| `/library/sections/{id}/byContentRating` | `GET` | **LOW** | client traffic | Browse by content rating |
| `/library/sections/{id}/byResolution` | `GET` | **LOW** | client traffic | Browse by resolution |
| `/library/sections/{id}/byFolder` | `GET` | **LOW** | client traffic | Browse by folder |
| `/library/sections/{id}/agents` | `GET` | **LOW** | client traffic | Available agents for this section |
| `/library/sections/{id}/match` | `GET` | **LOW** | client traffic | Match items in section |
| `/library/sections/{id}/unmatch` | `GET` | **LOW** | client traffic | Unmatch items in section |
| `/library/sections/{id}/edit` | `GET` / `PUT` | **LOW** | client traffic | Edit section metadata |
| `/library/sections/{id}/move` | `PUT` | **LOW** | client traffic | Move section paths |
| `/library/sections/{id}/settings` | `GET` | **LOW** | client traffic | Section-specific settings |
| `/library/sections/{id}/playlists` | `GET` | **LOW** | client traffic | Playlists belonging to section |
| `/library/sections/{id}/hubs` | `GET` | **LOW** | client traffic | Hubs for this section |
| `/library/sections/{id}/timeline` | `GET` | **LOW** | client traffic | Section timeline |
| `/library/sections/{id}/search` | `GET` | **LOW** | client traffic | Section-scoped search |
| `/library/sections/{id}/tags` | `GET` | **LOW** | client traffic | Tags in section |
| `/library/sections/{id}/label` | `GET` | **MEDIUM** | Tautulli, Kometa | Labels for a library |
| `/library/sections/{id}/artists` | `GET` | **LOW** | client traffic | Artists (music) |
| `/library/sections/{id}/shows` | `GET` | **LOW** | client traffic | Shows (TV) |
| `/library/sections/{id}/episodes` | `GET` | **LOW** | client traffic | Episodes |
| `/library/sections/{id}/movies` | `GET` | **LOW** | client traffic | Movies |
| `/library/sections/{id}/clips` | `GET` | **LOW** | client traffic | Clips |
| `/library/sections/{id}/photos` | `GET` | **LOW** | client traffic | Photos |
| `/library/sections/{id}/refresh` | `GET` / `POST` | **MEDIUM** | Kometa | Trigger library refresh |
| `/library/sections/{id}/emptyTrash` | `GET` / `POST` | **MEDIUM** | Kometa | Empty library trash |
| `/library/sections/{id}/optimize` | `GET` / `POST` | **MEDIUM** | Kometa | Optimize database for a library |
| `/library/optimize` | `GET` / `POST` | **MEDIUM** | Kometa | Global database optimize |
| `/library/recentlyAdded` | `GET` | **MEDIUM** | Tautulli | Global recently added |
| `/library/metadata/{id}/children` | `GET` | **MEDIUM** | SDK, client traffic | Children of show/season/artist/album |
| `/library/metadata/{id}/grandchildren` | `GET` | **MEDIUM** | Tautulli | Grandchildren (episodes under show) |
| `/library/metadata/{id}/onDeck` | `GET` | **LOW** | client traffic | On-deck for this show/season |
| `/library/metadata/{id}/reviews` | `GET` | **LOW** | client traffic | User reviews |
| `/library/metadata/{id}/parent` | `GET` | **LOW** | client traffic | Parent metadata shortcut |
| `/library/metadata/{id}/grandparent` | `GET` | **LOW** | client traffic | Grandparent metadata shortcut |
| `/library/metadata/{id}/nearest` | `GET` | **MEDIUM** | python-plexapi | Sonically similar items |
| `/library/metadata/{id}/posters` | `POST` | **MEDIUM** | Kometa | Upload custom poster image |
| `/library/metadata/{id}/arts` | `POST` | **MEDIUM** | Kometa | Upload custom background art |
| `/library/sections/{id}/computePath` | `GET` | **MEDIUM** | python-plexapi | Sonic adventure path |
| `/hubs/home/recentlyAdded` | `GET` | **MEDIUM** | Tautulli | Hub-centric recently added |
| `/hubs/continueWatching/items` | `GET` | **MEDIUM** | python-plexapi | Direct access to Continue Watching items |

### 2.6 Playback & Sessions

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `/:/websockets/notifications` | `WS` | **HIGH** | Tautulli, Home Assistant | Real-time event bus (sessions, timeline, status) |
| `/playlists?type=42` | `GET` / `DELETE` | **MEDIUM** | python-plexapi | Optimized / Conversion items |
| `/playQueues/1` | `GET` | **MEDIUM** | python-plexapi | Conversion queue |
| `/:/progress` | `GET` | **MEDIUM** | python-plexapi | Updates watch progress |
| `/actions/removeFromContinueWatching` | `PUT` | **MEDIUM** | python-plexapi | Removes item from Continue Watching |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.m4s` | `GET` | **MEDIUM** | UnicornTranscoder, undocumented endpoints | DASH segment delivery |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.ts` | `GET` | **MEDIUM** | undocumented endpoints | HLS TS segment delivery |
| `/music/:/transcode` | `GET` | **MEDIUM** | undocumented endpoints | Audio transcode endpoint |
| `/player/timeline/poll` | `GET` | **HIGH** | python-plexapi | Poll client playback timeline |
| `/player/playback/playMedia` | `POST` | **HIGH** | python-plexapi | Play specific media on client |
| `/player/playback/setParameters` | `POST` | **HIGH** | python-plexapi | Set shuffle/repeat/volume |
| `/player/playback/setStreams` | `POST` | **HIGH** | python-plexapi | Set active audio/subtitle/video streams |
| `/player/playback/play` | `POST` | **HIGH** | undocumented endpoints | Start playback on client |
| `/player/playback/pause` | `POST` | **HIGH** | undocumented endpoints | Pause client |
| `/player/playback/stop` | `POST` | **HIGH** | undocumented endpoints | Stop client |
| `/player/playback/seek` | `POST` | **HIGH** | undocumented endpoints | Seek to time |
| `/player/playback/skipTo` | `POST` | **HIGH** | undocumented endpoints | Skip to item |
| `/player/playback/skipBy` | `POST` | **HIGH** | undocumented endpoints | Skip forward/backward |
| `/player/playback/stepForward` | `POST` | **HIGH** | undocumented endpoints | Step forward |
| `/player/playback/stepBack` | `POST` | **HIGH** | undocumented endpoints | Step back |
| `/player/playback/subtitleStream` | `POST` | **MEDIUM** | undocumented endpoints | Change subtitle stream |
| `/player/playback/audioStream` | `POST` | **MEDIUM** | undocumented endpoints | Change audio stream |
| `/player/playback/videoStream` | `POST` | **MEDIUM** | undocumented endpoints | Change video stream |
| `/player/playback/volume` | `POST` | **MEDIUM** | undocumented endpoints | Set volume |
| `/player/playback/mute` | `POST` | **MEDIUM** | undocumented endpoints | Mute |
| `/player/playback/unmute` | `POST` | **MEDIUM** | undocumented endpoints | Unmute |
| `/player/playback/setTextStream` | `POST` | **MEDIUM** | undocumented endpoints | Set text stream |
| `/player/playback/setRating` | `POST` | **MEDIUM** | undocumented endpoints | Rate item |
| `/player/playback/setViewOffset` | `POST` | **MEDIUM** | undocumented endpoints | Set resume offset |
| `/player/playback/setState` | `POST` | **MEDIUM** | undocumented endpoints | Set playback state |
| `/player/playback/refreshPlayQueue` | `POST` | **MEDIUM** | undocumented endpoints | Refresh play queue |
| `/resources` *(on client)* | `GET` | **MEDIUM** | python-plexapi | Client capabilities and device info |

### 2.7 Live TV & DVR

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| *(session creation)* | — | **MEDIUM** | live-tv review | No documented way to create/start a Live TV session |
| `/livetv/dvrs/{dvrId}` | `PUT` / `PATCH` | **LOW** | live-tv review | Update DVR (only prefs endpoint exists) |
| `/livetv/dvrs/{dvrId}/channels` | `GET` | **LOW** | live-tv review | List channels directly associated with a DVR |
| `/livetv/dvrs/{dvrId}/guide` or `/livetv/epg/guide` | `GET` | **LOW** | live-tv review | Fetch program guide / schedule |
| `/livetv/sessions/{sessionId}` | `DELETE` | **LOW** | live-tv review | Terminate a Live TV session |
| `/livetv/dvrs/{dvrId}/recordings` or `/livetv/recordings` | `GET` | **LOW** | live-tv review | List completed DVR recordings |
| `/livetv/epg/search` | `GET` | **LOW** | live-tv review | Search EPG for upcoming airings |

### 2.8 Webhooks & Real-Time

| Endpoint | Method | Priority | Source(s) | Why it matters |
|----------|--------|----------|-----------|----------------|
| `https://plex.tv/api/v2/user/webhooks` | `GET` | **MEDIUM** | python-plexapi, undocumented endpoints | List configured webhook URLs |
| `https://plex.tv/api/v2/user/webhooks` | `POST` | **MEDIUM** | python-plexapi, undocumented endpoints | Add a webhook URL |
| *(webhook payload schema)* | `POST` *(inbound)* | **MEDIUM** | Bazarr, Home Assistant, Tautulli | Standardize `multipart/form-data` JSON payload + thumbnail |
| `/:/websockets/notifications` *(plural)* | `WS` | **HIGH** | Tautulli, Home Assistant | Widely-used plural alias for WebSocket event bus |

---

## 3. Schema Corrections

### 3.1 ServerConfiguration

| Field | Current Spec | Issue | Recommended Fix |
|-------|--------------|-------|-----------------|
| `diagnostics` | `string` | SDK parses as `list` (comma-separated diagnostics modules) | Change to `array` of `string`, or document parsing rule |
| `transcoderVideoBitrates` | untyped / description only | SDK parses as `list` | Add `type: array` with `items: string` or `integer` |
| `transcoderVideoQualities` | `string` | SDK parses as `list` | Change to `array` of `string` / `integer` |
| `transcoderVideoResolutions` | description only | SDK parses as `list` | Add `type: array` of `string` |
| `ownerFeatures` | `string` (comma-separated) | SDK parses as `list` | Change to `array` of `string`, or document parsing rule |
| `offlineTranscode` | `example: 1`, no `type` | Missing type | Should be `integer` or `boolean` (BoolInt pattern) |

**Additional issue:** The root `/` endpoint is documented as returning `MediaContainerWithDirectory`, but the actual response is a `ServerConfiguration`-shaped object with a `Directory` array. Update schema to `allOf: [ServerConfiguration, { Directory: ... }]`.

### 3.2 Metadata

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

**Type-specific gap:** The `Metadata` schema is a flat union. It does not distinguish type-specific required/optional fields (e.g. `year` is optional for episodes, `parentIndex` is season number, `grandparentTitle` is show name).

### 3.3 Media

| Field | Found In | Notes |
|-------|----------|-------|
| `uuid` | `media.py` | Media instance UUID |
| `selected` | `media.py` | Whether this media version is selected |

### 3.4 Part

| Field | Found In | Notes |
|-------|----------|-------|
| `protocol` | `media.py` | Streaming protocol (e.g. `dash`, `hls`) |
| `packetLength` | `media.py` | RTP packet length |
| `requiredBandwidths` | `media.py` | Bandwidth requirements list |
| `syncItemId` | `media.py` | Mobile sync item association |
| `syncState` | `media.py` | Sync state (e.g. `pending`, `downloaded`) |
| `deepAnalysisVersion` | `media.py` | Deep analysis version |

### 3.5 Stream (Video, Audio, Subtitle, Lyric)

**AudioStream gaps**

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

**SubtitleStream gaps**

| Field | Notes |
|-------|-------|
| `providerTitle` | Subtitle provider name |
| `score` | Match confidence score |
| `sourceKey` | Source identifier |
| `transient` | Temporary/downloaded subtitle |
| `userID` | User who added subtitle |
| `perfectMatch` | Exact match flag |

**LyricStream gaps**

| Field | Notes |
|-------|-------|
| `minLines` | Minimum lines in lyric file |
| `provider` | Lyric provider |
| `timed` | Whether lyrics are timestamped |

### 3.6 Collection

**There is no dedicated `Collection` schema.** Collections reuse `Metadata` (or are returned inside `MediaContainerWithMetadata`). Missing collection-specific fields:

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

### 3.7 Playlist

Playlists are defined via `MediaContainerWithPlaylistMetadata`. Missing fields:

| Field | Notes |
|-------|-------|
| `durationInSeconds` | Total duration in seconds (redundant but present in XML) |
| `radio` | Whether this is a generated radio playlist |
| `titleSort` | Sort-friendly title |

### 3.8 PlayQueue

There is **no standalone `PlayQueue` schema.** The creation endpoint defines play-queue fields inline. All other play-queue operations reuse `MediaContainerWithPlaylistMetadata`, which is **playlist-centric** and omits play-queue fields.

| Field | Present in Creation? | Present in Retrieval? | Notes |
|-------|---------------------|----------------------|-------|
| `playQueueLastAddedItemID` | ✅ | ❌ |  |
| `playQueueSelectedItemID` | ✅ | ❌ |  |
| `playQueueSelectedItemOffset` | ✅ | ❌ |  |
| `playQueueSelectedMetadataItemID` | ✅ | ❌ | **Missing from retrieval schema** |
| `playQueueShuffled` | ✅ | ❌ |  |
| `playQueueSourceURI` | ✅ | ❌ |  |
| `playQueueTotalCount` | ✅ | ❌ |  |
| `playQueueVersion` | ✅ | ❌ |  |

**Recommendation:** Create `MediaContainerWithPlayQueue` and reference it from all play-queue endpoints.

### 3.9 Session

The `Session` schema is extremely sparse (`bandwidth`, `id`, `location`). Real session objects include `sessionKey`, `uuid`, `title`, `userID`, etc.

**Recommendation:** Expand `Session` or document that consumers should rely on embedded `Player`, `User`, and `Metadata` objects.

### 3.10 Activity, ButlerTask, UpdaterStatus

| Schema | Status | Fix |
|--------|--------|-----|
| `Activity` | Inline under `/activities` GET | Extract to `#/components/schemas/Activity` |
| `ButlerTask` | Inline under `/butler` GET | Extract to `#/components/schemas/ButlerTask` |
| `UpdaterStatus` | Inline under `/updater/status` GET | Extract to `#/components/schemas/UpdaterStatus` |
| `LogLine` | **Does not exist** | Create or document generic text/plain response |

### 3.11 History

The history response schema defines an inline object with a minimal field set. Real history items include `guid`, `index`, `parentKey`, `parentRatingKey`, `grandparentKey`, `grandparentRatingKey`, `parentThumb`, `grandparentThumb`, `content`, `viewCount`, `lastViewedAt`, etc.

**Recommendation:** Derive history items from `Metadata` (or a `HistoryItem` `allOf`) so type-specific fields are not lost.

### 3.12 Timeline Response

The `POST /:/timeline` 200 response extends `ServerConfiguration` and adds `Bandwidths`, `terminationCode`, `terminationText`. It can also include `playQueueID` when playback originates from a queue — **not documented**.

**Fix:** Add `playQueueID` (integer) to timeline response schema.

### 3.13 DVR / Live TV Schemas

| Schema | Issue | Fix |
|--------|-------|-----|
| `DVR` | Duplicated inline across **7+ endpoints** | Extract to `#/components/schemas/DVR` |
| `MediaContainerWithDevice` | Duplicates `Device` properties inline instead of `$ref` | Use `allOf: [MediaContainer, { Device: { type: array, items: { $ref: Device } } }]` |
| `DeviceChannel` | Defined inline; has useful fields (`drm`, `favorite`, `hd`, `signalQuality`, `signalStrength`) missing from main `Channel` | Extract to component or merge into `Channel` |
| `Channel` | Missing EPG fields: `favorite`, `drm`, `signalQuality`, `signalStrength` | Add missing fields |
| `MediaSubscription` | `Directory`, `Playlist`, `Video` hints are untyped (`additionalProperties: true`) | Document known hint keys |
| `Lineup` | Missing `key` and `identifier` | Add missing fields |
| `MediaContainerWithMetadata` (sessions) | Too generic for Live TV sessions | Consider `MediaContainerWithLiveTVSession` with session-specific fields |

### 3.14 Device

The `Device` schema defines only 12 properties. Missing:

| Field | Why it matters |
|-------|----------------|
| `id` | The `deviceId` path parameter is `integer`, but schema has no `id` field |
| `name` / `title` | Human-readable device name |
| `enabled` | Toggled by `PUT /media/grabbers/devices/{deviceId}` |
| `deviceIdentifier` | Distinct from `uuid` |
| `thumb` / `thumbVersion` | Referenced by thumb endpoint |
| `lineup` / `lineupType` | EPG lineup association |

### 3.15 Download Queue & Grabber

| Schema | Issue | Fix |
|--------|-------|-----|
| `DownloadQueue` | Inline in POST/GET | Extract to `#/components/schemas/DownloadQueue` |
| `DownloadQueueItem` | Inline in list/get | Extract to `#/components/schemas/DownloadQueueItem` |
| `MediaGrabber` / `Grabber` | No reusable schema exists; inline with only 3 fields | Create component with SSDP fields (`UDN`, `URLBase`, `deviceType`, `manufacturer`, `modelDescription`, `modelNumber`, etc.) |
| `TranscodeSession` | Referenced by `DownloadQueueItem` but minimal; spec admits "not yet documented" | Prioritize documentation |

### 3.16 Provider / Hub Schemas

| Schema | Issue | Fix |
|--------|-------|-----|
| `/media/providers` response | Wrongly extends `ServerConfiguration` instead of `MediaContainer` or dedicated `ProviderContainer` | Create `Provider` and `ProviderFeature` schemas |
| `ProviderFeature` | Underspecified `Feature` array; does not enumerate well-known feature types | Document known feature keys (`search`, `metadata`, `content`, `match`, `manage`, `timeline`, `rate`, `playqueue`, `playlist`, `subscribe`, `promoted`, `continuewatching`, `collection`, `actions`, `imagetranscoder`, `queryParser`, `grid`) |
| `Hub` | `additionalProperties: true` masks missing fields like `context`, `hubKey`, `reason`, `reasonTitle`, `reasonID` | Add observed fields |

### 3.17 PlexDevice

| Issue | Details |
|-------|---------|
| Contradictory required/nullable | `platform`, `platformVersion`, `device` are typed as `["null", "string"]` but also listed in `required` |

---

## 4. Parameter & Query String Corrections

### 4.1 Library Section Browsing (`/library/sections/{sectionId}/all`)

The GET method only documents `includeMeta`, `includeGuids`, `sectionId`, `mediaQuery`, `X-Plex-Container-Start`, `X-Plex-Container-Size`. Widely used but **absent** params:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | integer | Filter by metadata type (`1`=movie, `2`=show, `3`=season, `4`=episode, `8`=artist, `9`=album, `10`=track) |
| `sort` | string | Sort key and direction (e.g. `addedAt:desc`, `titleSort`) |
| `filters` | string | General filtering expression |
| `unwatched` | integer (`1`) | Filter to unwatched only |
| `genre`, `studio`, `contentRating`, `resolution`, `year`, `firstCharacter` | string / integer | Tag-based filters |
| `includeCollections` | boolean | Include collection items in results |
| `includeExternalMedia` | boolean | Include external/online media |
| `includeAdvanced` | boolean | Include advanced settings |
| `checkFiles` | boolean | Verify file existence |
| `includeRelated` | boolean | Include related items |
| `includeExtras` | boolean | Include trailers, behind-the-scenes, etc. |
| `includePopularLeaves` | boolean | Include popular episodes |
| `includeConcerts` | boolean | Include concert items |
| `includeOnDeck` | boolean | Include On Deck status |
| `includeChapters` | boolean | Include chapter markers |
| `includePreferences` | boolean | Include user preferences |
| `includeBandwidths` | boolean | Include bandwidth info |
| `includeLoudnessRamps` | boolean | Include loudness ramp data |
| `includeStations` | boolean | Include radio station data |
| `includeExternalIds` | boolean | Include external GUIDs |
| `includeReviews` | boolean | Include user reviews |
| `includeCredits` | boolean | Include full credits |
| `includeArt`, `includeThumb`, `includeBanner`, `includeTheme` | boolean | Force inclusion of artwork fields |
| `includeFields` | string | Whitelist of fields to return |
| `asyncAugmentMetadata` | boolean | Async metadata augmentation |
| `asyncRefreshLocalMediaAgent` | boolean | Async local media agent refresh |
| `nocache` | boolean | Bypass cache |
| `excludeFields` | string | Blacklist of fields to omit |
| `skipRefresh` | boolean | Skip synchronous refresh |

### 4.2 Metadata Item Detail (`/library/metadata/{ids}`)

| Parameter | Type | Description | Notes |
|-----------|------|-------------|-------|
| `includeMarkers` | boolean | Intro/credits markers | Critical for Tautulli and skip-intro clients |
| `includeChapters` | boolean | Chapter data | Missing from spec GET params |
| `includeExternalMedia` | boolean | External media | Missing |
| `includeExtras` | boolean | Extras/trailers | Missing |
| `includeRelated` | boolean | Related items | Missing |
| `includeOnDeck` | boolean | On Deck status | Missing |
| `includePopularLeaves` | boolean | Popular episodes | Missing |
| `includeReviews` | boolean | User reviews | Missing |
| `includeStations` | boolean | Radio stations | Missing |
| `includeGuids` | boolean | External GUIDs | Only documented on `/library/sections/{id}/all` |
| `excludeElements` | string | Omit elements | Mentioned only in history endpoint description |
| `excludeFields` | string | Omit fields | Mentioned only in history endpoint description |

### 4.3 Search & Hubs

| Endpoint | Missing Param | Type | Description |
|----------|---------------|------|-------------|
| `/hubs/search` | `includeCollections` | boolean | Include collection results in search hubs |
| `/hubs/search/voice` | `includeCollections` | boolean | Same gap as standard search |

### 4.4 Playlists

| Parameter | Where | Type | Description |
|-----------|-------|------|-------------|
| `type=42` | `/playlists` | integer | Optimized/conversion items |

### 4.5 History (`/status/sessions/history/all`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `includeFields` | string | Mentioned in description but not declared |
| `excludeFields` | string | Mentioned in description but not declared |
| `includeElements` | string | Mentioned in description but not declared |
| `excludeElements` | string | Mentioned in description but not declared |
| `viewedAt>` | integer | Greater-than filter (range operator) |
| `viewedAt<` | integer | Less-than filter (range operator) |
| `accountID` | integer | Filter by account |
| `deviceID` | integer | Filter by device |
| `X-Plex-Container-Start` | header / query | Pagination start (only documented as response header) |
| `X-Plex-Container-Size` | header / query | Pagination size (only documented as response header) |

### 4.6 Timeline (`POST /:/timeline`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `containerKey` | string | Groups timeline reports (e.g. `/playQueues/123`) |
| `playQueueID` | integer | Distinct from `playQueueItemID`; identifies the queue itself |
| `guid` | string | Global unique identifier for the item |
| `url` | string | Alternative to `key`/`ratingKey` (legacy) |

### 4.7 Transcoder

| Parameter | Where Missing | Type | Description |
|-----------|---------------|------|-------------|
| `maxVideoBitrate` | `/decision`, `/start.{ext}`, `/subtitles` | integer | Client-side cap |
| `videoResolution` | transcoder endpoints | string | Cap string |
| `copyts` | transcoder endpoints | boolean | Timestamp copying |
| `platform` | transcoder endpoints | string | Some clients send this in addition to headers |
| `mediaIndex` / `partIndex` | `/subtitles` | integer | Present on `/decision` and `/start`, missing on `/subtitles` |
| `sessionId` | segment delivery | string | Path param for `.m4s` / `.ts` segments |
| `segmentId` | segment delivery | string / integer | Path param for segment files |

### 4.8 Server / System

| Parameter | Where | Type | Description |
|-----------|-------|------|-------------|
| `timespan` (1–6) | `/statistics/bandwidth` | integer | Dashboard timespan |
| `accountID`, `deviceID`, `lan` | `/statistics/bandwidth` | various | Filter params |
| `includeFiles` | `/services/browse` | boolean | Include files in browse results |
| `skipRefresh` | `/library/metadata/{ids}/refresh` | boolean | Skip synchronous refresh |
| `asyncAugmentMetadata=1` | `/library/metadata/{ids}` | boolean | Async metadata augmentation |

### 4.9 Live TV & DVR

| Endpoint | Missing Param | Type | Description |
|----------|---------------|------|-------------|
| `/livetv/dvrs` | `uuid`, `lineup` | string | Filter params for managing multiple DVRs |
| `/livetv/sessions` | `dvrId`, `channel` | string / integer | Filter params |
| `/media/subscriptions` | `X-Plex-Container-Start`, `X-Plex-Container-Size` | header / query | Pagination request params |
| `/media/subscriptions/template` | `type`, `targetLibrarySectionID` | string / integer | Influences template response |
| `/media/grabbers/devices/discover` | `protocol`, `grabberIdentifier` | string | Targeted discovery |
| `/livetv/dvrs/{dvrId}/prefs` | `value` | string | Only `name` is documented; needs `value` or `name=value` clarification |
| `/media/grabbers/devices/{deviceId}/prefs` | `value` | string | Same issue as DVR prefs |

### 4.10 Devices & Download Queue

| Endpoint | Missing Param | Type | Description |
|----------|---------------|------|-------------|
| `/media/grabbers` | `protocol` enum | string | Should enumerate known protocols (`stream`, `download`, `livetv`) |
| `/media/grabbers/devices` | `uri` format | string | No validation pattern documented |
| `/media/grabbers/devices/{deviceId}/channelmap` | `channelMapping` / `channelMappingByKey` schema | object | `style: deepObject` used but no formal nested schema |
| `/media/grabbers/devices/{deviceId}/prefs` | `name` semantics | string | Should be `object` or better documented as `name=value` pairs |
| `/media/grabbers/devices/{deviceId}/scan` | `source` enum | string | Should list valid scan sources (OTA, Cable, etc.) |
| `/downloadQueue/{queueId}/add` | `keys` max length / format | array | `explode: false` array of strings |
| `/downloadQueue/{queueId}/items` | Pagination params | header / query | `X-Plex-Container-Start` / `X-Plex-Container-Size` not listed as request params |
| `/downloadQueue/{queueId}/item/{itemId}/media` | `Accept` header | header | Required for media file negotiation |
| `/security/resources` | `source` enum / examples | string | No examples of valid source identifiers |
| `/security/resources` | `refresh` behavior | boolean | Behavior not described |
| `/security/token` | Additional `type` / `scope` values | string | Only `delegation` / `all` documented |

---

## 5. Response Corrections

### 5.1 Wrong Status Codes & Missing Bodies

| Endpoint | Issue | Fix |
|----------|-------|-----|
| `GET /` | Documented as `MediaContainerWithDirectory`; actual response is `ServerConfiguration` + `Directory` array | Correct response schema |
| `GET /activities` | `Activity` defined inline; no `200` response headers documented | Extract to component; add headers |
| `GET /butler` | `ButlerTask` defined inline | Extract to component |
| `GET /updater/status` | `UpdaterStatus` / `Release` inline; `checkedAt` type unclear | Extract to component; clarify type |
| `PUT /log` / `POST /log` | No response schema; returns generic 200 | Document whether any body is returned |
| `POST /log/networked` | Undocumented response | Document response body or note empty response |
| `GET /:/eventsource/notifications` | Returns `application/octet-stream`; no SSE event schemas | Add `NotificationContainer`, `PlaySessionStateNotification`, `StatusNotification`, `ReachabilityNotification` schemas |
| `GET /:/websocket/notifications` | Returns `application/octet-stream`; no WebSocket message schemas | Add message schemas (same as above) |
| `POST /livetv/dvrs/{dvrId}/reloadGuide` | Returns `text/html` with `X-Plex-Activity` header | Verify if body is actually JSON; document known quirk if truly HTML |
| `/media/grabbers/devices/{deviceId}/thumb/{version}` | Returns "The thumbnail" but no `content` schema | Document `image/jpeg` or `image/png` |
| `GET /downloadQueue/{queueId}/item/{itemId}/media` | Returns "The raw media file" but no `content` schema | Document expected `Content-Type` (e.g. `video/mp4`, `application/octet-stream`) |
| `/security/token` | Description says "responds to all HTTP verbs but POST is preferred" | Either document all verbs or remove the note |

### 5.2 Inline Schemas That Should Be Reusable

| Current Location | Schema Name | Where Else It Should Be Reused |
|------------------|-------------|-------------------------------|
| `/activities` GET response | `Activity` | WebSocket `StatusNotification`, other activity-returning endpoints |
| `/butler` GET response | `ButlerTask` | — |
| `/updater/status` GET response | `UpdaterStatus` | — |
| `/status/sessions/background` GET | `TranscodeJob` | Other transcode-related responses |
| `/status/sessions/history/all` GET | `HistoryItem` | `/status/sessions/history/{historyId}` |
| `/livetv/dvrs` (7+ endpoints) | `DVR` | All DVR CRUD endpoints |
| `MediaContainerWithDevice` | `Device` array | Should `$ref` `#/components/schemas/Device` |
| `/media/grabbers/devices/{deviceId}/channels` GET | `DeviceChannel` | Merge into `Channel` or extract to component |
| `POST /downloadQueue` / `GET /downloadQueue/{queueId}` | `DownloadQueue` | All download-queue endpoints |
| `GET /downloadQueue/{queueId}/items` | `DownloadQueueItem` | Item detail endpoints |
| `GET /media/grabbers` | `MediaGrabber` | All grabber-related responses |
| `POST /playQueues` 200 response | `PlayQueue` | All play-queue endpoints |
| `/media/providers` response | `Provider` / `ProviderFeature` | Provider CRUD responses |

---

## 6. Security & Auth Improvements

### 6.1 Missing Auth Flows

| Flow | Status | Fix |
|------|--------|-----|
| **OAuth PIN Flow** | Not documented | Document `POST /pins` → user visits `plex.tv/link` → `GET /pins/{id}` → obtain token |
| **JWT Device Registration** | Not documented | Document Ed25519 keypair flow: `POST /auth/jwk` → `GET /auth/nonce` → `POST /auth/token` (7-day expiry) |
| **Direct Sign-In** | Partially documented | Expand `/users/signin` to describe 2FA challenge, rate limiting, `rememberMe` behavior |
| **Home User Switch** | Not documented | Document `POST /api/home/users/{id}/switch` returning new auth token |
| **Claim Flow** | Not documented | Document `GET /api/claim/token.json` → `POST /myplex/claim` on PMS |

### 6.2 Incorrect Scopes

| Endpoint | Current Scope | Correct Scope | Notes |
|----------|---------------|---------------|-------|
| `GET /user` (plex.tv) | `admin` | Any valid token | Self-introspection endpoint |
| `GET /resources` (plex.tv) | `admin` | Any valid token | Own server lookup |
| `GET /users` (plex.tv) | `admin` | Any valid token | Friend discovery works with standard user tokens |

### 6.3 Missing Security Schemes

| Scheme | Status | Fix |
|--------|--------|-----|
| `X-Plex-Token` as query parameter | Only documented as header | Add note that token may be passed as `?X-Plex-Token=...` on all endpoints |
| `X-Plex-Client-Identifier` as security scheme | Defined as parameter only | Consider adding an `apiKey` security scheme for `clientIdentifier` so PIN endpoints can declare `security: [clientIdentifier: []]` |
| JWT bearer scheme | Mentioned in description but no formal scheme | Add a `JWT` security scheme or document the JWT flow under API Info |

### 6.4 Duplicate Inline Error Schemas

`400` and `401` error responses on `/user`, `/users/signin`, `/users`, and `/resources` are copy-pasted inline instead of referencing shared `#/components/responses/BadRequest` or `#/components/responses/Unauthorized`. Extract to reusable response components.

### 6.5 Auth Documentation Gaps

- The spec is PMS-centric. Add a top-level **Plex.tv API Info** section explaining base URLs (`https://plex.tv/api/v2` vs `https://plex.tv/api`), default formats (JSON for v2, XML for v1), and required headers.
- Document rate limiting on auth endpoints (Plex Pro Week '25 blog explicitly mentions this).
- Document that `X-Plex-Client-Identifier` is **mandatory** for PIN and JWT flows.

---

## 7. Documentation Improvements

### 7.1 Typos

| Location | Issue | Correction |
|----------|-------|------------|
| `POST /livetv/dvrs` description | "after creation of a **devcie**" | "device" |
| `PUT /livetv/dvrs/{dvrId}/lineups` description | "The lineup to **delete**" (PUT = add) | "The lineup to add" |
| `PUT /livetv/dvrs/{dvrId}/prefs` description | "by name **avd** value" | "and" |
| `GET /livetv/epg/lineupchannels` summary | "Get the channels for **mulitple** lineups" | "multiple" |
| `MediaGrabOperation` description | "media grab **opration**" | "operation" |
| `/security/token` description | "responds to all HTTP verbs but POST is preferred" | Clarify or restrict to POST only |

### 7.2 Missing Descriptions & Examples

| Topic | Gap | Recommendation |
|-------|-----|----------------|
| `PUT /:/prefs` | Only documents `prefs: object` | Add example or enum of common preference keys; link to hidden settings article |
| Hidden preferences | ~40+ keys undocumented | Document known hidden keys (`aBRKeepOldTranscodes`, `allowHighOutputBitrates`, `transcoderH264Options`, etc.) or link to external reference |
| `PUT /library/metadata/{ids}` | Body schema is `args: object` (opaque) | Document editable fields (title, summary, tag locks, etc.) |
| `uri` parameter on scrobble/unscrobble | Description refers to "intro for description of URIs" | That introductory section does not exist in the spec; add it or remove the cross-reference |
| `/media/providers` proxy paths | Individual provider feature paths are undefined | Reference dynamic paths (`/{provider}/search`, `/{provider}/metadata`, etc.) in the `Provider` tag description |
| `X-Plex-Container-Start` / `X-Plex-Container-Size` | Documented as response headers only | Clarify they are also accepted as **request** headers / query parameters for pagination |

### 7.3 Tag Organization

| Issue | Recommendation |
|-------|----------------|
| Tags `Authentication`, `Users`, `Plex` are scattered | Add a `Plex.tv` tag group in `x-tagGroups` to organize all cloud endpoints |
| `/media/grabbers/operations/{operationId}` tagged under `Subscriptions` | Cross-tag with `Devices` or retag |
| `Devices` tag description conflates DVR tuners with Plex clients | Add clarifying note that this tag only covers grabber/tuner devices; client discovery is via `/clients` (missing) or `/resources` |
| `/:/scrobble` and `/:/unscrobble` appear tag-less or under implicit tag | Verify they are categorized under a domain tag |

### 7.4 XML vs JSON Notes

| Behavior | Current State | Recommendation |
|----------|---------------|----------------|
| Default format (PMS) | Not clearly stated | Add note: "Most PMS endpoints return **XML** unless `Accept: application/json` is sent" |
| Default format (plex.tv v2) | Not clearly stated | Add note: "plex.tv v2 generally returns **JSON** by default" |
| Legacy endpoints (`/pins.xml`, `/api/resources`, `/api/users/`) | Not documented | Note that these return **XML only** |
| Webhook payload | Not documented | Note: JSON wrapped in `multipart/form-data` field named `payload`; thumbnail as second file part |
| Empty responses | Some PUT/DELETE return `204 No Content` | Document where no body is expected |

### 7.5 Missing Cross-References

| From | To | Recommendation |
|------|-----|----------------|
| `Devices` tag | `DVRs`, `EPG`, `Live TV`, `Subscriptions` tags | Add cross-reference note |
| `Download Queue` tag | `Play Queue` tag | Add note explaining the distinction |
| `Provider` tag | Individual provider proxy paths | Reference dynamic paths or document them |
| `Transcoder` endpoints | Segment delivery URLs | Add note explaining that manifests reference `/session/{sessionId}/{segmentId}.{ext}` |
| `Timeline` endpoint | `terminationCode` / `terminationText` | Explain that clients must handle 200 body to detect server-side session kill |

### 7.6 Server URL Inconsistency

- `/users` points to `https://plex.tv/api` (v1)
- `/user`, `/users/signin`, `/resources` point to `https://plex.tv/api/v2`

**Recommendation:** Document *why* this split exists (v1 XML vs v2 JSON) and note the deprecation trajectory.

---

## 8. Speakeasy / SDK Generator Improvements

### 8.1 `x-speakeasy-globals` Headers

Current globals (11 parameters) are reasonably complete. Candidates for addition:

| Header | In globals? | Assessment |
|--------|-------------|------------|
| `X-Plex-Session-Identifier` | ❌ No | Correctly excluded — playback-session-specific, not global |
| `X-Plex-Client-Profile-Name` | ❌ No | **Consider adding** — used on transcoder/decision endpoints |
| `X-Plex-Client-Profile-Extra` | ❌ No | **Consider adding** — used on transcoder/decision endpoints |
| `X-Plex-Token` | ❌ No | Correctly excluded — it is a security scheme, not a global parameter |

### 8.2 Missing Reusable Components

Create or extract the following components so generated SDKs can reference them:

- `#/components/schemas/Activity`
- `#/components/schemas/ButlerTask`
- `#/components/schemas/UpdaterStatus`
- `#/components/schemas/HistoryItem`
- `#/components/schemas/PlayQueue` (or `MediaContainerWithPlayQueue`)
- `#/components/schemas/Collection`
- `#/components/schemas/DownloadQueue`
- `#/components/schemas/DownloadQueueItem`
- `#/components/schemas/DeviceChannel`
- `#/components/schemas/MediaGrabber`
- `#/components/schemas/Provider`
- `#/components/schemas/ProviderFeature`
- `#/components/schemas/WebhookPayload`
- `#/components/schemas/NotificationContainer`
- `#/components/schemas/PlaySessionStateNotification`
- `#/components/schemas/StatusNotification`
- `#/components/schemas/ReachabilityNotification`
- `#/components/schemas/TimelineEntry`

### 8.3 Globals Improvements

- Consider adding `x-speakeasy-retries` configuration for rate-limited endpoints (`plex.tv/api/v2/pins`, `clients.plex.tv/api/v2/auth/*`).
- Document `parseAs: list` hints for comma-separated fields (`diagnostics`, `ownerFeatures`, `transcoderVideoBitrates`, etc.) so generated SDKs automatically split strings into arrays.
- Add `x-speakeasy-unknown-fields: allow` or similar note on schemas that use `additionalProperties: true` heavily (`Metadata`, `Hub`, `Activity.Context`, etc.) to set consumer expectations.

---

## 9. Appendix: Raw Research Files

| File | Description |
|------|-------------|
| `review/python_plexapi_gap_analysis.md` | Phase 1 — Comprehensive gap analysis between the official OpenAPI spec and the `python-plexapi` SDK. Covers missing PMS endpoints, plex.tv cloud APIs, client remote-control protocol, schema field mismatches, parameter gaps, and auth flow differences. |
| `review/integration_ecosystem_gaps.md` | Phase 1 — Survey of major open-source Plex integrations (Tautulli, Overseerr/Jellyseerr, Bazarr, Kometa, Home Assistant). Maps API usage patterns, missing endpoints, webhook consumption, and real-time event streams against the spec. |
| `review/undocumented_endpoints_research.md` | Phase 1 — Community-researched undocumented and hidden endpoints compiled from public forums, GitHub, Gists, Reddit, CVE write-ups, and the official spec. Catalogs plex.tv v2 surface, cloud providers, player control, transcode segments, legacy endpoints, and XML/JSON quirks. |
| `review/domain_auth_account_review.md` | Phase 2 — Deep review of the Authentication & Account domain: `securitySchemes`, `security`, `x-speakeasy-globals`, and all auth/account paths. Identifies incorrect scopes, missing OAuth/JWT flows, duplicate error schemas, and documentation gaps. |
| `review/domain_server_system_review.md` | Phase 2 — Deep review of Server & System domain (General, Activities, Butler, Updater, Log, Preferences, Events, Transcoder, Status). Identifies inline schemas, missing endpoints, parameter gaps, and auth inconsistencies. |
| `review/domain_library_metadata_review.md` | Phase 2 — Deep review of Library & Metadata domain. Covers root library, sections, metadata items, collections, playlists, and all sub-endpoints. Documents extensive schema field gaps and missing query parameters. |
| `review/domain_media_provider_review.md` | Phase 2 — Deep review of Media Provider & Content domain (Provider, Content, Hubs, Search, Rate, Playlist). Documents missing cloud provider endpoints, provider proxy paths, search parameter gaps, and hub schema issues. |
| `review/domain_playback_sessions_review.md` | Phase 2 — Deep review of Playback & Sessions domain (Status, Timeline, Play Queue, Transcoder). Documents missing WebSocket plural alias, complete client remote-control protocol, transcode segment delivery, and play-queue schema mismatch. |
| `review/domain_livetv_dvr_review.md` | Phase 2 — Deep review of Live TV & DVR domain (DVRs, EPG, Subscriptions, Live TV, Grabbers/Devices). Documents missing session lifecycle endpoints, inline schema duplication, parameter gaps, and typos. |
| `review/domain_devices_download_review.md` | Phase 2 — Deep review of Devices & Download Queue domain. Documents missing PMS local endpoints, client remote-control protocol, schema gaps in `Device`, `DownloadQueue`, `DownloadQueueItem`, and `MediaGrabber`. |

---

*Report generated by the Master Synthesizer agent. All findings are derived from the 10 Phase 1 and Phase 2 research reports listed in the Appendix.*
