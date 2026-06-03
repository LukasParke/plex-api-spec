# Auth & Account Domain Review

**Date:** 2026-06-03  
**Scope:** `securitySchemes`, `security`, `x-speakeasy-globals`, `components/parameters`, and all auth/account paths in `plex-api-spec.yaml`.  
**Sources:** `python_plexapi_gap_analysis.md`, `integration_ecosystem_gaps.md`, `undocumented_endpoints_research.md`

---

## Endpoints Present in Spec (inventory with assessment)

| # | Path | Server | Method | Tag | Assessment |
|---|------|--------|--------|-----|------------|
| 1 | `/user` | `plex.tv/api/v2` | `GET` | Authentication | ✅ Path correct. Response uses `UserPlexAccount` schema (comprehensive). **Issue:** Security scope is `admin`; this is a self-introspection endpoint and should work with *any* valid token. No `POST`/`PUT`/`DELETE` for profile updates. |
| 2 | `/users/signin` | `plex.tv/api/v2` | `POST` | Authentication | ✅ Path correct. Form body has `login`, `password`, `rememberMe`, `verificationCode`. **Issue:** No mention of 2FA challenge flow in description. No OAuth/PIN alternatives documented. Response extends `UserPlexAccount` with `pastSubscriptions`/`trials` — handled correctly via `allOf`. |
| 3 | `/users` | `plex.tv/api` | `GET` | Users | ✅ Path correct (v1 API). Inline schema is fairly detailed (friends/shared users with `Server` sub-array). **Issue:** Only `GET` documented; no `POST` for user creation. Security scope is `admin` but this works with any valid token for friend discovery. Only JSON documented; XML variant not mentioned. |
| 4 | `/security/resources` | PMS | `GET` | General | ✅ Path correct. `source` (required) and `refresh` query params present. Response schema is basic (accessToken + Connection list). **Issue:** No `POST`/`PUT`/`DELETE`. No security scope override at path level (falls back to global `shared user`/`admin`). |
| 5 | `/security/token` | PMS | `POST` | General | ✅ Path correct. `type=delegation` and `scope=all` enums enforced. **Issue:** Description says "responds to all HTTP verbs but POST is preferred" — confusing; should either document the other verbs or remove the note. No mention of token expiration (48h / restart). |
| 6 | `/resources` | `plex.tv/api/v2` | `GET` | Plex | ✅ Path correct. Query params `includeHttps`, `includeRelay`, `includeIPv6` present with `BoolInt` + defaults. Response is `PlexDevice[]` array. **Issue:** Security scope is `admin` but should work with any valid token for self-resource lookup. No `POST`/`PUT`/`DELETE` for device management. |

### Summary of Present Endpoints
- **Only 6 endpoints** are documented in the Auth & Account domain.
- **Zero** plex.tv v2 endpoints for OAuth PIN, sign-out, ping, webhooks, sharing, Plex Home, or JWT auth.
- **Zero** legacy v1 plex.tv endpoints (pins.xml, api/resources, api/users, etc.).
- **Zero** PMS-side auth endpoints (e.g., `/myplex/claim`, `/myplex/account`).

---

## Missing Endpoints

### CRITICAL — OAuth PIN Flow
These are fundamental to every modern integration (Tautulli, Overseerr, Bazarr, Home Assistant).

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/api/v2/pins` | `POST` | **CRITICAL** | Tautulli, Overseerr, Bazarr, python-plexapi | Create a 4-char PIN for device linking |
| `https://plex.tv/api/v2/pins/{pinId}` | `GET` | **CRITICAL** | Tautulli, Overseerr, Bazarr | Poll PIN status; returns `authToken` when claimed |
| `https://plex.tv/api/v2/pins/link` | `PUT` | **CRITICAL** | python-plexapi | Link a PIN to an account (OAuth completion) |
| `https://clients.plex.tv/api/v2/pins` | `POST` | **CRITICAL** | python-plexapi | Alternative PIN endpoint (clients subdomain) |

### HIGH — Account & Token Management

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/api/v2/users/signout` | `DELETE` | **HIGH** | python-plexapi | Invalidate token |
| `https://plex.tv/api/v2/ping` | `GET` | **HIGH** | Tautulli, Overseerr, python-plexapi | Token refresh / health check (no auth required) |
| `https://plex.tv/api/v2/features` | `GET` | **HIGH** | Plex Forum | Plex Pass feature flags |
| `https://plex.tv/api/v2/friends` | `GET` | **HIGH** | Plex Forum | Friends & shared users (v2 JSON) |
| `https://plex.tv/api/v2/home` | `GET` | **HIGH** | Plex Forum | Plex Home user list |
| `https://plex.tv/api/v2/server` | `GET` | **HIGH** | Plex Forum | Server association info for logged-in user |
| `https://plex.tv/api/v2/users/password` | `POST` | **HIGH** | Plex Forum | Change / reset password |
| `https://plex.tv/api/v2/user/view_state_sync` | `PUT` | **HIGH** | python-plexapi | Enable/disable watch-state sync consent |
| `https://plex.tv/api/v2/user/{uuid}/settings/opt_outs` | `GET` | **HIGH** | python-plexapi | Online-media-source opt-outs |
| `https://plex.tv/users/account` | `GET` | **HIGH** | Tautulli, Overseerr | Own account details (XML) |
| `https://plex.tv/users/account.json` | `GET` | **HIGH** | Tautulli, Overseerr | Own account details (JSON) |

### HIGH — Sharing & Plex Home

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/api/v2/shared_servers` | `POST` | **HIGH** | python-plexapi, Plexopedia | Share a server with a user |
| `https://plex.tv/api/v2/sharings/{userId}` | `PUT` | **HIGH** | python-plexapi | Update friend filters (allowSync, filterMovies, etc.) |
| `https://plex.tv/api/v2/sharings/{userId}` | `DELETE` | **HIGH** | python-plexapi | Remove a share / friend |
| `https://plex.tv/api/v2/home/users/restricted/{userId}` | `PUT` | **HIGH** | python-plexapi | Update restricted (managed) home user settings |
| `https://plex.tv/api/home/users` | `GET` / `POST` | **HIGH** | python-plexapi | List / create Plex Home users |
| `https://plex.tv/api/home/users/{userId}` | `DELETE` / `PUT` | **HIGH** | python-plexapi | Remove / update home user |
| `https://plex.tv/api/home/users/{id}/switch` | `POST` | **HIGH** | python-plexapi | Switch to home user (returns new auth token) |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | `POST` | **HIGH** | python-plexapi, Tautulli | Share library with friend (legacy v1) |
| `https://plex.tv/api/servers/{machineId}` | `GET` | **HIGH** | python-plexapi | Server details for sharing |

### HIGH — Claim Tokens

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/api/claim/token.json` | `GET` | **HIGH** | python-plexapi | Claim token for new servers |
| `POST /myplex/claim` | `POST` | **HIGH** | python-plexapi | Claim server on PMS (uses claim token) |

### MEDIUM — Webhooks

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/api/v2/user/webhooks` | `GET` | **MEDIUM** | python-plexapi | List configured webhook URLs |
| `https://plex.tv/api/v2/user/webhooks` | `POST` | **MEDIUM** | python-plexapi | Add a webhook URL |

### MEDIUM — JWT Device Registration (new 2025)
Documented by Plex Pro Week ’25 blog and community research.

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://clients.plex.tv/api/v2/auth/jwk` | `POST` | **MEDIUM** | Plex Pro Week, JonnyWong16 gist | Register device public key (JWK) |
| `https://clients.plex.tv/api/v2/auth/nonce` | `GET` | **MEDIUM** | JonnyWong16 gist | Get nonce to sign in client JWT |
| `https://clients.plex.tv/api/v2/auth/token` | `POST` | **MEDIUM** | JonnyWong16 gist | Exchange signed client JWT for Plex JWT |
| `https://clients.plex.tv/api/v2/auth/keys` | `GET` | **MEDIUM** | JonnyWong16 gist | Plex public JWKs for signature verification |

### MEDIUM — Server/Account Utilities

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/api/v2/server/access_tokens` | `GET` | **MEDIUM** | CVE-2025-34158 write-up | List access tokens for the server |
| `https://plex.tv/api/v2/server/users/features` | `GET` | **MEDIUM** | Plex Forum | Features enabled per shared user |
| `https://plex.tv/api/v2/cloud_server` | `GET` | **MEDIUM** | Tautulli | Plex Cloud status |
| `https://plex.tv/api/v2/geoip` | `GET` | **MEDIUM** | Tautulli | GeoIP lookup |
| `https://plex.tv/:/ip` | `GET` | **MEDIUM** | Tautulli | Public IP detection |
| `https://plex.tv/api/downloads/{channel}.json` | `GET` | **LOW** | Tautulli | Plex update downloads |

### LOW — Legacy v1 plex.tv (for migration docs)

| Path | Method | Priority | Source | What it does |
|------|--------|----------|--------|--------------|
| `https://plex.tv/pins.xml` | `POST` | **LOW** | plexargod | Legacy PIN creation (XML) |
| `https://plex.tv/pins/{pinId}` | `GET` | **LOW** | plexargod | Legacy PIN check (XML) |
| `https://plex.tv/api/resources` | `GET` | **LOW** | plexargod | Legacy published server connections (XML) |
| `https://plex.tv/api/users/` | `GET` | **LOW** | python-plexapi | Legacy friends list (XML) |
| `https://plex.tv/api/servers/{machineId}` | `GET` | **LOW** | python-plexapi | Legacy server info (XML) |
| `https://plex.tv/api/servers/{machineId}/shared_servers` | `POST` | **LOW** | python-plexapi | Legacy share server (XML) |
| `https://clients.plex.tv/devices.xml` | `GET` | **LOW** | CVE-2025-34158 write-up | Authorized devices with tokens (XML) |

---

## Schema & Security Issues

### 1. JWT Auth is Mentioned but Not Formally Documented
- The `token` security scheme **description** mentions JWT (7-day expiry, ED25519, device revocation), but there is **no dedicated security scheme** for JWT, no `JWT` bearer format, and no documentation of the keypair registration flow (`/auth/jwk`, `/auth/nonce`, `/auth/token`).
- **Fix:** Add a `JWT` security scheme (or document the JWT flow under API Info) and add the four `clients.plex.tv/api/v2/auth/*` endpoints.

### 2. `clientIdentifier` is Not a Security Scheme
- `X-Plex-Client-Identifier` is defined as a **parameter**, not a security scheme. The PIN endpoints and some public endpoints (ping) require *only* `X-Plex-Client-Identifier` without a token.
- **Fix:** Consider adding an `apiKey` security scheme for `clientIdentifier` so that PIN endpoints can declare `security: [clientIdentifier: []]` cleanly.

### 3. Incorrect `admin` Scope on Self-Introspection Endpoints
- `/user` (GET token details) requires `admin` scope — incorrect. Any valid token should work.
- `/resources` (GET own servers) requires `admin` scope — incorrect. Any valid token should work.
- `/users` (GET friends) requires `admin` scope — overly restrictive; works with standard user tokens for friend discovery.
- **Fix:** Change scopes to `shared user` (or remove scope restriction) on these paths.

### 4. `X-Plex-Token` Query Param Not Supported in Spec
- The spec defines `X-Plex-Token` **only** as a header (`in: header`). Integrations (python-plexapi, Tautulli) widely pass it as a query parameter (`?X-Plex-Token=...`).
- **Fix:** Document that `X-Plex-Token` may also be passed as a query parameter on all endpoints.

### 5. Duplicate Inline Error Schemas
- `400` and `401` error responses on `/user`, `/users/signin`, `/users`, and `/resources` are **copy-pasted inline** instead of referencing a shared `#/components/responses/BadRequest` or `#/components/responses/Unauthorized`.
- **Fix:** Extract to reusable response components.

### 6. `/security/token` Verb Confusion
- Description says "responds to all HTTP verbs but POST is preferred". If GET/PUT/DELETE actually work, they should be documented; if not, the note should be removed to avoid confusion.

### 7. `/users/signin` Missing `strong` Parameter
- The v2 PIN endpoint supports a `strong` boolean parameter for longer PINs. Not applicable to signin directly, but the OAuth PIN flow docs should mention it.

---

## Parameter/Header Gaps

### `x-speakeasy-globals` Headers
Current globals (11 parameters):
```yaml
- accepts
- X-Plex-Client-Identifier
- X-Plex-Product
- X-Plex-Version
- X-Plex-Platform
- X-Plex-Platform-Version
- X-Plex-Device
- X-Plex-Model
- X-Plex-Device-Vendor
- X-Plex-Device-Name
- X-Plex-Marketplace
```

**Missing from globals (assessment):**

| Header | In globals? | Assessment |
|--------|-------------|------------|
| `X-Plex-Session-Identifier` | ❌ No | **Correctly excluded** — it is playback-session-specific, not global. Already documented on `/:/timeline`. |
| `X-Plex-Client-Profile-Name` | ❌ No | **Consider adding** — used on transcoder/decision endpoints. |
| `X-Plex-Client-Profile-Extra` | ❌ No | **Consider adding** — used on transcoder/decision endpoints. |
| `X-Plex-Token` | ❌ No | **Correctly excluded** — it is a security scheme, not a global parameter. |

**Verdict:** The `x-speakeasy-globals` list is **reasonably complete** for auth/account. The only candidates for addition are `X-Plex-Client-Profile-Name` and `X-Plex-Client-Profile-Extra`, but those are transcoder-domain headers.

### Missing Query Parameters on Present Endpoints

| Endpoint | Missing Param | Notes |
|----------|---------------|-------|
| `/resources` | `includeDLNA` | Some clients use this to filter DLNA connections. |
| `/resources` | `includeRelay` | ✅ Present. |
| `/users/signin` | `code` (2FA) | `verificationCode` is present, but some legacy flows use `code`. |

---

## Documentation Improvements

1. **Add a Plex.tv API Info section**
   - The spec is PMS-centric. A new top-level section should explain:
     - Base URL: `https://plex.tv/api/v2`
     - Legacy base URL: `https://plex.tv/api`
     - Default response format: JSON for v2, XML for v1
     - Required headers for all plex.tv calls: `X-Plex-Client-Identifier`, `X-Plex-Product`, etc.

2. **Auth flow diagram / description**
   - Document the three supported auth flows:
     1. **Direct sign-in:** `POST /users/signin` with username/password (+ 2FA).
     2. **OAuth PIN:** `POST /pins` → user visits `https://plex.tv/link` → `GET /pins/{id}` → obtain token.
     3. **JWT Device Registration:** `POST /auth/jwk` → `GET /auth/nonce` → `POST /auth/token` (ED25519 keypairs, 7-day expiry).

3. **Tag consolidation**
   - The spec has tags: `Authentication`, `Users`, `Plex`.
   - **Suggestion:** Add a `Plex.tv` tag group in `x-tagGroups` to organize all cloud endpoints together.

4. **Server URL inconsistency**
   - `/users` points to `https://plex.tv/api` (v1)
   - `/user`, `/users/signin`, `/resources` point to `https://plex.tv/api/v2`
   - Document *why* this split exists (v1 XML vs v2 JSON) and note deprecation trajectory.

5. **`/users/signin` description**
   - Expand to explicitly mention:
     - 2FA challenge behavior (401 with `verificationCode` required).
     - Rate limiting on auth endpoints.
     - `rememberMe` behavior (extends token expiry).

6. **Webhook payload schema**
   - Although webhook configuration endpoints are missing, the spec should eventually document the inbound webhook `multipart/form-data` payload schema (event types, `payload` JSON field, optional `thumb` JPEG attachment).

7. **XML vs JSON behavior**
   - Add a note that PMS endpoints default to XML unless `Accept: application/json` is sent, while plex.tv v2 defaults to JSON.

---

*End of review.*
