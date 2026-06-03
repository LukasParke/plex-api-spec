# Plex API Spec — Remaining Gaps & Phased Implementation Plan

**Date:** 2026-06-03  
**Source:** 11 review documents (~3,777 lines of analysis) from agent swarm review  
**Current Spec State:** 267 paths, 91 schemas, 315 operations, 0 speakeasy errors, 0 vacuum errors  
**Goal:** 100% documentation parity — absolute source of truth for all things Plex API

---

## Executive Summary

| Category | Review Recs | Done | Remaining | Coverage |
|----------|-------------|------|-----------|----------|
| Missing endpoints | ~175 | ~71 | ~104 | 41% |
| Schema extractions | ~18 | ~18 | 0 | 100% |
| Schema field gaps | ~75 | ~5 | ~70 | 7% |
| Query param gaps | ~80 | ~8 | ~72 | 10% |
| Response/status fixes | ~15 | ~5 | ~10 | 33% |
| Auth/security gaps | ~18 | ~6 | ~12 | 33% |
| Documentation issues | ~45 | ~10 | ~35 | 22% |

**What this PR accomplished:** All CRITICAL priorities (OAuth PIN, cloud providers, client remote-control, schema deduplication, CI tooling).  
**What remains:** Primarily MEDIUM-priority plex.tv social endpoints, deep schema field coverage, query parameter completeness, and documentation polish.

---

## Phase 4: Plex.tv v2 Account, Social & Sharing
**Priority: HIGH** | **Estimated Effort: 3–4 days** | **Target: ~25 new endpoints**

This is the largest remaining functional gap. The spec is still PMS-centric; the entire plex.tv v2 social surface is missing.

### 4.1 Auth & Account Completion
| Endpoint | Method | Source |
|----------|--------|--------|
| `/api/v2/users/signout` | `DELETE` | python-plexapi |
| `/api/v2/ping` | `GET` | Tautulli, Overseerr |
| `/api/v2/features` | `GET` | Plex Forum |
| `/api/v2/friends` | `GET` | Plex Forum |
| `/api/v2/home` | `GET` | Plex Forum |
| `/api/v2/server` | `GET` | Plex Forum |
| `/api/v2/users/password` | `POST` | Plex Forum |
| `/api/v2/user/view_state_sync` | `PUT` | python-plexapi |
| `/api/v2/user/{uuid}/settings/opt_outs` | `GET` | python-plexapi |
| `/users/account` | `GET` | Tautulli, Overseerr |
| `/users/account.json` | `GET` | Tautulli, Overseerr |

### 4.2 Server Sharing & Plex Home
| Endpoint | Method | Source |
|----------|--------|--------|
| `/api/v2/shared_servers` | `POST` | python-plexapi, Plexopedia |
| `/api/v2/sharings/{userId}` | `PUT` | python-plexapi |
| `/api/v2/sharings/{userId}` | `DELETE` | python-plexapi |
| `/api/v2/home/users/restricted/{userId}` | `PUT` | python-plexapi |
| `/api/home/users` | `GET` / `POST` | python-plexapi |
| `/api/home/users/{userId}` | `DELETE` / `PUT` | python-plexapi |
| `/api/home/users/{id}/switch` | `POST` | python-plexapi |
| `/api/servers/{machineId}/shared_servers` | `POST` | python-plexapi, Tautulli |
| `/api/servers/{machineId}` | `GET` | python-plexapi |
| `/api/claim/token.json` | `GET` | python-plexapi |
| `POST /myplex/claim` | `POST` | python-plexapi |

### 4.3 Webhooks
| Endpoint | Method | Source |
|----------|--------|--------|
| `/api/v2/user/webhooks` | `GET` | python-plexapi |
| `/api/v2/user/webhooks` | `POST` | python-plexapi |
| *Webhook payload schema* | inbound | Bazarr, Home Assistant, Tautulli |

### 4.4 Utility Endpoints
| Endpoint | Method | Source |
|----------|--------|--------|
| `/api/v2/server/access_tokens` | `GET` | CVE-2025-34158 write-up |
| `/api/v2/server/users/features` | `GET` | Plex Forum |
| `/api/v2/cloud_server` | `GET` | Tautulli |
| `/api/v2/geoip` | `GET` | Tautulli |
| `/:/ip` | `GET` | Tautulli |
| `/api/downloads/{channel}.json` | `GET` | Tautulli |

### 4.5 Security & Auth Documentation
- [ ] Add JWT bearer security scheme (documented but not formalized)
- [ ] Document rate limiting on auth endpoints
- [ ] Add note that `X-Plex-Token` may be passed as query parameter on all endpoints
- [ ] Document `X-Plex-Client-Identifier` as mandatory for PIN and JWT flows
- [ ] Document v1 vs v2 base URL split and deprecation trajectory

### Validation Gates
- [ ] `speakeasy lint` = 0 errors
- [ ] `vacuum lint` = 0 errors
- [ ] `prettier --check` passes
- [ ] All new plex.tv endpoints use correct `servers:` override
- [ ] All new endpoints have `operationId`, `summary`, `description`

---

## Phase 5: Schema Depth & Completeness
**Priority: MEDIUM** | **Estimated Effort: 2–3 days** | **Target: ~40 new fields, 5 new schemas**

Deep field-level coverage is the biggest contributor to SDK quality. Generated SDKs cannot expose fields that are not in the spec.

### 5.1 Metadata Fields
Add to `Metadata` schema (or type-specific sub-schemas):

| Field | Type | Source |
|-------|------|--------|
| `artBlurHash` | string | video.py, audio.py |
| `thumbBlurHash` | string | video.py, audio.py |
| `lastRatedAt` | integer (timestamp) | video.py, audio.py |
| `editionTitle` | string | video.py (Movie) |
| `languageOverride` | string | video.py (Movie, Show) |
| `enableCreditsMarkerGeneration` | boolean | video.py (Movie, Show) |
| `useOriginalTitle` | boolean | video.py (Movie, Show) |
| `slug` | string | video.py (Movie, Show) |
| `skipCount` | integer | audio.py (Track) |
| `musicAnalysisVersion` | integer | audio.py (Audio base) |
| `sourceURI` | string | video.py, audio.py, playlist.py |
| `playlistItemID` | integer | base.py (Playable) |

### 5.2 Media Fields
Add to `Media` schema:

| Field | Type | Source |
|-------|------|--------|
| `uuid` | string | media.py |
| `selected` | boolean | media.py |

### 5.3 Part Fields
Add to `Part` schema:

| Field | Type | Source |
|-------|------|--------|
| `protocol` | string (dash, hls) | media.py |
| `packetLength` | integer | media.py |
| `requiredBandwidths` | string (list) | media.py |
| `syncItemId` | integer | media.py |
| `syncState` | string | media.py |
| `deepAnalysisVersion` | integer | media.py |

### 5.4 Stream Fields
**AudioStream:**
| Field | Type | Source |
|-------|------|--------|
| `bitrateMode` | string (cbr, vbr) | media.py |
| `visualImpaired` | boolean | media.py |
| `albumGain` | number | media.py |
| `albumPeak` | number | media.py |
| `albumRange` | number | media.py |
| `endRamp` | string | media.py |
| `gain` | number | media.py |
| `loudness` | number | media.py |
| `lra` | number | media.py |
| `peak` | number | media.py |
| `startRamp` | string | media.py |

**SubtitleStream:**
| Field | Type | Source |
|-------|------|--------|
| `providerTitle` | string | media.py |
| `score` | number | media.py |
| `sourceKey` | string | media.py |
| `transient` | boolean | media.py |
| `userID` | integer | media.py |
| `perfectMatch` | boolean | media.py |

**LyricStream:**
| Field | Type | Source |
|-------|------|--------|
| `minLines` | integer | media.py |
| `provider` | string | media.py |
| `timed` | boolean | media.py |

### 5.5 New Standalone Schemas
- [ ] `Collection` — collection-specific fields (`collectionMode`, `collectionPublished`, `collectionSort`, `collectionFilterBasedOnUser`, `artBlurHash`, `thumbBlurHash`, `userRating`, `lastRatedAt`)
- [ ] `Provider` / `ProviderFeature` — extract from `/media/providers` response
- [ ] `MediaContainerWithPlayQueue` — distinct from playlist schema; includes `playQueueLastAddedItemID`, `playQueueSelectedItemID`, `playQueueSelectedItemOffset`, `playQueueSelectedMetadataItemID`, `playQueueShuffled`, `playQueueSourceURI`, `playQueueTotalCount`, `playQueueVersion`
- [ ] `WebhookPayload` — `multipart/form-data` JSON payload + thumbnail
- [ ] `Session` expansion — add `sessionKey`, `uuid`, `title`, `userID`, or document that consumers rely on embedded `Player`/`User`/`Metadata`

### 5.6 DVR / Live TV Schema Cleanup
- [ ] `Channel` — add missing EPG fields: `favorite`, `drm`, `signalQuality`, `signalStrength`
- [ ] `Lineup` — add `key`, `identifier`
- [ ] `MediaSubscription` — document known hint keys instead of `additionalProperties: true`
- [ ] `Device` — add `id`, `name`/`title`, `enabled`, `deviceIdentifier`, `thumb`/`thumbVersion`, `lineup`/`lineupType`

### Validation Gates
- [ ] `speakeasy lint` = 0 errors
- [ ] `vacuum lint` = 0 errors
- [ ] `prettier --check` passes
- [ ] All new fields have `description` and `example` where possible
- [ ] No duplicate property names introduced

---

## Phase 6: Library, Playback & Query Parameter Completeness
**Priority: MEDIUM** | **Estimated Effort: 2–3 days** | **Target: ~35 endpoints, ~30 query params**

### 6.1 Missing Library Endpoints
| Endpoint | Method | Priority |
|----------|--------|----------|
| `/library/sections/{id}/onDeck` | `GET` | MEDIUM |
| `/library/sections/{id}/unwatched` | `GET` | MEDIUM |
| `/library/sections/{id}/newest` | `GET` | MEDIUM |
| `/library/sections/{id}/recentlyAdded` | `GET` | MEDIUM |
| `/library/sections/{id}/byYear` | `GET` | LOW |
| `/library/sections/{id}/byDecade` | `GET` | LOW |
| `/library/sections/{id}/byContentRating` | `GET` | LOW |
| `/library/sections/{id}/byResolution` | `GET` | LOW |
| `/library/sections/{id}/byFolder` | `GET` | LOW |
| `/library/sections/{id}/agents` | `GET` | LOW |
| `/library/sections/{id}/match` | `GET` | LOW |
| `/library/sections/{id}/unmatch` | `GET` | LOW |
| `/library/sections/{id}/edit` | `GET` / `PUT` | LOW |
| `/library/sections/{id}/move` | `PUT` | LOW |
| `/library/sections/{id}/settings` | `GET` | LOW |
| `/library/sections/{id}/playlists` | `GET` | LOW |
| `/library/sections/{id}/hubs` | `GET` | LOW |
| `/library/sections/{id}/timeline` | `GET` | LOW |
| `/library/sections/{id}/search` | `GET` | LOW |
| `/library/sections/{id}/tags` | `GET` | LOW |
| `/library/sections/{id}/label` | `GET` | MEDIUM |
| `/library/sections/{id}/refresh` | `GET` / `POST` | MEDIUM |
| `/library/sections/{id}/emptyTrash` | `GET` / `POST` | MEDIUM |
| `/library/sections/{id}/optimize` | `GET` / `POST` | MEDIUM |
| `/library/optimize` | `GET` / `POST` | MEDIUM |
| `/library/recentlyAdded` | `GET` | MEDIUM |
| `/library/metadata/{id}/children` | `GET` | MEDIUM |
| `/library/metadata/{id}/grandchildren` | `GET` | MEDIUM |
| `/library/metadata/{id}/posters` | `POST` | MEDIUM |
| `/library/metadata/{id}/arts` | `POST` | MEDIUM |
| `/library/metadata/{id}/nearest` | `GET` | MEDIUM |
| `/library/metadata/{id}/computePath` | `GET` | MEDIUM |
| `/hubs/home/recentlyAdded` | `GET` | MEDIUM |
| `/hubs/continueWatching/items` | `GET` | MEDIUM |

### 6.2 Missing Playback Endpoints
| Endpoint | Method | Priority |
|----------|--------|----------|
| `/playlists?type=42` | `GET` / `DELETE` | MEDIUM |
| `/playQueues/1` | `GET` | MEDIUM |
| `/:/progress` | `GET` | MEDIUM |
| `/actions/removeFromContinueWatching` | `PUT` | MEDIUM |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.m4s` | `GET` | MEDIUM |
| `/{transcodeType}/:/transcode/universal/session/{sessionId}/{segmentId}.ts` | `GET` | MEDIUM |
| `/music/:/transcode` | `GET` | MEDIUM |
| `/resources` (on client) | `GET` | MEDIUM |

### 6.3 Missing Live TV Endpoints
| Endpoint | Method | Priority |
|----------|--------|----------|
| `/livetv/dvrs/{dvrId}` | `PUT` / `PATCH` | LOW |
| `/livetv/dvrs/{dvrId}/channels` | `GET` | LOW |
| `/livetv/dvrs/{dvrId}/guide` or `/livetv/epg/guide` | `GET` | LOW |
| `/livetv/sessions/{sessionId}` | `DELETE` | LOW |
| `/livetv/dvrs/{dvrId}/recordings` or `/livetv/recordings` | `GET` | LOW |
| `/livetv/epg/search` | `GET` | LOW |

### 6.4 Query Parameters — Library Section Browsing
Add to `/library/sections/{sectionId}/all` and other browse endpoints:

| Parameter | Type |
|-----------|------|
| `type` | integer |
| `sort` | string |
| `filters` | string |
| `unwatched` | integer (1) |
| `genre`, `studio`, `contentRating`, `resolution`, `year`, `firstCharacter` | string / integer |
| `includeCollections` | boolean |
| `includeExternalMedia` | boolean |
| `includeAdvanced` | boolean |
| `checkFiles` | boolean |
| `includeRelated` | boolean |
| `includeExtras` | boolean |
| `includePopularLeaves` | boolean |
| `includeConcerts` | boolean |
| `includeOnDeck` | boolean |
| `includeChapters` | boolean |
| `includePreferences` | boolean |
| `includeBandwidths` | boolean |
| `includeLoudnessRamps` | boolean |
| `includeStations` | boolean |
| `includeExternalIds` | boolean |
| `includeReviews` | boolean |
| `includeCredits` | boolean |
| `includeArt`, `includeThumb`, `includeBanner`, `includeTheme` | boolean |
| `includeFields` | string |
| `asyncAugmentMetadata` | boolean |
| `asyncRefreshLocalMediaAgent` | boolean |
| `nocache` | boolean |
| `excludeFields` | string |
| `skipRefresh` | boolean |

### 6.5 Query Parameters — Metadata Detail
Add to `/library/metadata/{ids}`:
- [ ] `includeMarkers` — already done in PR, verify coverage on all metadata GETs
- [ ] `includeChapters`, `includeExternalMedia`, `includeExtras`, `includeRelated`, `includeOnDeck`, `includePopularLeaves`, `includeReviews`, `includeStations` — add where missing

### 6.6 Query Parameters — Search & Hubs
- [ ] `/hubs/search` — `includeCollections`
- [ ] `/hubs/search/voice` — `includeCollections`

### 6.7 Query Parameters — History
- [ ] `/status/sessions/history/all` — `includeFields`, `excludeFields`, `includeElements`, `excludeElements`
- [ ] `viewedAt>`, `viewedAt<`, `accountID`, `deviceID`
- [ ] `X-Plex-Container-Start`, `X-Plex-Container-Size` as request params (not just response headers)

### 6.8 Query Parameters — Transcoder
- [ ] `maxVideoBitrate`, `videoResolution`, `copyts`, `platform`
- [ ] `mediaIndex`, `partIndex` on `/subtitles`

### 6.9 Query Parameters — Server / System
- [ ] `/statistics/bandwidth` — `timespan` (1–6), `accountID`, `deviceID`, `lan`
- [ ] `/services/browse` — `includeFiles`
- [ ] `/library/metadata/{ids}/refresh` — `skipRefresh`
- [ ] `/library/metadata/{ids}` — `asyncAugmentMetadata=1`

### Validation Gates
- [ ] `speakeasy lint` = 0 errors
- [ ] `vacuum lint` = 0 errors
- [ ] `prettier --check` passes
- [ ] Arbiter diff against live PMS shows 0 gaps for added endpoints

---

## Phase 7: Documentation Polish, Typos & SDK Generator
**Priority: LOW–MEDIUM** | **Estimated Effort: 1–2 days** | **Target: ~35 doc issues**

### 7.1 Fix Typos
| Location | Typo | Correction |
|----------|------|------------|
| `POST /livetv/dvrs` description | "devcie" | "device" |
| `GET /livetv/epg/lineupchannels` summary | "mulitple" | "multiple" |
| `PUT /livetv/dvrs/{dvrId}/prefs` description | "avd" | "and" |
| `MediaGrabOperation` description | "opration" | "operation" |

### 7.2 Missing Descriptions & Examples
- [ ] `PUT /:/prefs` — add example or enum of common preference keys; link to hidden settings reference
- [ ] `PUT /library/metadata/{ids}` — document editable fields (title, summary, tag locks)
- [ ] `uri` parameter on scrobble/unscrobble — remove broken cross-reference or add URI intro section
- [ ] `/media/providers` proxy paths — reference dynamic paths in `Provider` tag description
- [ ] `X-Plex-Container-Start` / `X-Plex-Container-Size` — clarify they are accepted as request headers/query params

### 7.3 XML vs JSON Notes
- [ ] Add note: "Most PMS endpoints return XML unless `Accept: application/json` is sent"
- [ ] Add note: "plex.tv v2 generally returns JSON by default"
- [ ] Note legacy endpoints (`/pins.xml`, `/api/resources`, `/api/users/`) return XML only
- [ ] Webhook payload: JSON wrapped in `multipart/form-data` field named `payload`; thumbnail as second file part
- [ ] Document where PUT/DELETE return `204 No Content`

### 7.4 Tag Organization
- [ ] Add `Plex.tv` tag group in `x-tagGroups` to organize cloud endpoints
- [ ] Retag `/media/grabbers/operations/{operationId}` from `Subscriptions` to `Devices`
- [ ] `Devices` tag description — clarify this covers grabber/tuner devices only; client discovery is via `/clients` or `/resources`
- [ ] Verify `/:/scrobble` and `/:/unscrobble` are categorized under a domain tag

### 7.5 Cross-References
- [ ] `Devices` → `DVRs`, `EPG`, `Live TV`, `Subscriptions`
- [ ] `Download Queue` → `Play Queue` (explain distinction)
- [ ] `Provider` → dynamic proxy paths
- [ ] `Transcoder` → segment delivery URLs
- [ ] `Timeline` → `terminationCode` / `terminationText` session kill behavior

### 7.6 Speakeasy / SDK Improvements
- [ ] Add `x-speakeasy-retries` for rate-limited endpoints (`/pins`, `/auth/*`)
- [ ] Add `x-speakeasy-unknown-fields: allow` note on heavily `additionalProperties` schemas
- [ ] Consider adding `X-Plex-Client-Profile-Name` and `X-Plex-Client-Profile-Extra` to `x-speakeasy-globals`
- [ ] Remove or use orphaned components: `Title`, `Type`, `UpdaterRelease`, `X-Plex-Client-Profile-Extra`, `X-Plex-Client-Profile-Name`, `X-Plex-Session-Identifier`, `500` response

### Validation Gates
- [ ] `prettier --check` passes
- [ ] `speakeasy lint` = 0 errors
- [ ] `vacuum lint` = 0 errors
- [ ] All typos verified fixed via grep

---

## Phase 8: JWT Device Registration & Legacy Endpoints
**Priority: MEDIUM** | **Estimated Effort: 1 day** | **Target: 4 endpoints + legacy coverage**

### 8.1 JWT Device Registration (2025)
| Endpoint | Method | Source |
|----------|--------|--------|
| `/api/v2/auth/jwk` | `POST` | Plex Pro Week blog, JonnyWong16 gist |
| `/api/v2/auth/nonce` | `GET` | JonnyWong16 gist |
| `/api/v2/auth/token` | `POST` | JonnyWong16 gist |
| `/api/v2/auth/keys` | `GET` | JonnyWong16 gist |

### 8.2 Legacy plex.tv Endpoints (XML-first)
| Endpoint | Method | Notes |
|----------|--------|-------|
| `/pins.xml` | `POST` | Legacy PIN (XML) |
| `/pins/{pinId}` | `GET` | Legacy PIN check (XML) |
| `/api/resources` | `GET` | Legacy published server connections |
| `/api/users/` | `GET` | Legacy friends list |
| `/devices.xml` | `GET` | Authorized devices with tokens |

### 8.3 Documentation
- [ ] Document JWT flow: `POST /auth/jwk` → `GET /auth/nonce` → `POST /auth/token` (7-day expiry)
- [ ] Document Ed25519 keypair requirement
- [ ] Note XML-only responses for legacy endpoints

---

## Phase 9: Discovery Pipeline Hardening
**Priority: MEDIUM** | **Estimated Effort: 2–3 days** | **Ongoing**

### 9.1 Arbiter Enhancements
- [ ] Add `diff-against` auto-fix mode — suggest YAML patches for gaps
- [ ] Add coverage dashboard — % of observed paths documented vs undocumented
- [ ] Add schema inference from live traffic — auto-suggest response schemas
- [ ] Support plex.tv traffic capture (not just PMS)

### 9.2 CI Improvements
- [ ] Run discovery on PRs with `exit-on-gap: false` and post gap report as PR comment
- [ ] Add vacuum quality score gate (currently 25/100 — set target 50/100)
- [ ] Auto-open issue when nightly discovery finds new undocumented endpoints

### 9.3 Continuous Validation
- [ ] Weekly diff review — human-in-the-loop for inferred schema changes
- [ ] Monthly full Arbiter run against staging PMS with all features enabled

---

## Appendix A: Priority Triage Matrix

| Priority | Count | Effort | Impact | Recommendation |
|----------|-------|--------|--------|----------------|
| CRITICAL | 0 | — | — | All addressed in current PR ✅ |
| HIGH | ~25 endpoints | 3–4 days | Blocks modern integrations | Phase 4 immediately |
| MEDIUM | ~100 endpoints/fields/params | 5–7 days | SDK completeness | Phases 5–6 next |
| LOW | ~35 doc/typos/SDK | 1–2 days | Polish & trust | Phase 7 |
| ONGOING | Pipeline | 2–3 days setup | Sustainability | Phase 9 |

## Appendix B: Source Document Mapping

| Review Document | Key Sections | Covered by Phase |
|-----------------|--------------|------------------|
| `PLEX_API_SPEC_FULL_REVIEW.md` | All | 4–8 |
| `python_plexapi_gap_analysis.md` | Endpoints, schemas, params | 4–6 |
| `integration_ecosystem_gaps.md` | Webhooks, WS, auth | 4, 6, 8 |
| `undocumented_endpoints_research.md` | Hidden endpoints, XML quirks | 4, 6, 8 |
| `domain_auth_account_review.md` | Security, scopes, OAuth, JWT | 4, 8 |
| `domain_server_system_review.md` | Activities, butler, updater, logs | 5 (schema depth) |
| `domain_library_metadata_review.md` | Metadata fields, library endpoints | 5, 6 |
| `domain_media_provider_review.md` | Providers, hubs, search | 5, 6 |
| `domain_playback_sessions_review.md` | Remote control, transcoder, WS | 6 (remaining endpoints) |
| `domain_livetv_dvr_review.md` | DVRs, EPG, sessions | 5, 6 |
| `domain_devices_download_review.md` | Devices, download queue | 5 |

## Appendix C: Validation Gates (All Phases)

Every phase must pass:
1. `prettier --check plex-api-spec.yaml`
2. `speakeasy lint openapi -s plex-api-spec.yaml` → 0 errors
3. `vacuum lint plex-api-spec.yaml` → 0 errors
4. Arbiter diff against live PMS → 0 new gaps for added endpoints (where testable)
5. PR review by CodeRabbit or equivalent automated review
