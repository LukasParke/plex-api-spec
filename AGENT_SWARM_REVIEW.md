# Agent Swarm Review — Plex API Specification

**PR:** [#117](https://github.com/LukasParke/plex-api-spec/pull/117)  
**Branch:** `feature/arbiter-discovery-pipeline`  
**Reviewers:** 4 specialized subagents (OpenAPI Purist, SDK DevEx Critic, API Design Purist, Documentation QA Nitpicker)

---

## Executive Summary

The spec is structurally sound and CI-clean, but carries significant debt from documenting a real-world, organically-grown API. The three highest-impact issues are:

1. **~237 operations lack error responses** — SDKs get untyped errors
2. **HTTP method misuse** — GETs mutate state, RPC-style paths abound
3. **5 undefined tags + tag fragmentation** — SDKs generate broken service classes

---

## 🔴 Critical Issues (Fix Before Merge)

### 1. ~237 Operations Missing Error Responses
- **Reviewer:** OpenAPI Purist, SDK DevEx Critic
- **Problem:** ~60% of operations only define `200` success responses. No `4xx`/`5xx` coverage means generated SDKs throw generic, untyped errors.
- **Fix:** Add `$ref` to existing `components/responses/400`, `401`, `403`, `404` on every authenticated endpoint. At minimum `400` + `401`.

### 2. GET with Side Effects
- **Reviewer:** API Design Purist
- **Problem:** `GET /:/progress` updates watch progress. `GET /library/sections/{sectionId}/emptyTrash` permanently deletes items. Browsers/crawlers may prefetch these.
- **Fix:** Mark as deprecated in spec; document that clients MUST use `POST` or `DELETE`.

### 3. Malformed Path Parameter
- **Reviewer:** SDK DevEx Critic
- **Problem:** `DELETE /library/streams/{streamId}.{ext}` declares parameter as `streamId}.{ext` — broken path parsing.
- **Fix:** Correct parameter declaration to `{streamId}` and handle `.ext` as part of path or separate param.

### 4. 3 Kebab-Case `operationId`s
- **Reviewer:** SDK DevEx Critic
- **Problem:** `get-server-resources`, `get-users`, `post-users-sign-in-data` produce invalid method names in most languages.
- **Fix:** Rename to `getServerResources`, `getUsers`, `postUsersSignInData`.

### 5. 5 `operationId`s Contradict Their HTTP Method
- **Reviewer:** SDK DevEx Critic
- **Problem:** `GET /library/metadata/{ids}/subtitles` → `addSubtitles`; `PUT /library/collections/.../items/...` → `deleteCollectionItem`.
- **Fix:** Audit and rename to semantically correct IDs.

### 6. Response Component Missing Root `type`
- **Reviewer:** OpenAPI Purist
- **Problem:** `components.responses.slash-get-responses-200` declares `properties` without `type: object`.
- **Fix:** Add `type: object` at line ~18657.

### 7. Schema Properties Missing `type`
- **Reviewer:** OpenAPI Purist
- **Problem:** `MediaSubscription` properties (`Directory`, `Playlist`, `Video`) have `additionalProperties: true` but no `type: object`.
- **Fix:** Add `type: object` to each.

### 8. 5 Undefined Tags
- **Reviewer:** OpenAPI Purist, SDK DevEx Critic
- **Problem:** `Authentication`, `Playback`, `Playlists`, `Plex`, `Users` are used in operations but missing from the global `tags` array.
- **Fix:** Add tag definitions with descriptions to root `tags`.

### 9. Duplicate Global Parameters
- **Reviewer:** OpenAPI Purist
- **Problem:** 16 transcode/timeline operations redeclare `X-Plex-*` headers already injected by `x-speakeasy-globals`.
- **Fix:** Remove duplicate parameter declarations.

---

## 🟠 High-Priority Issues (Fix Soon)

### 10. RPC-Style Action Paths
- **Reviewer:** API Design Purist
- **Problem:** `/actions/addToWatchlist`, `/player/playback/mute`, `/library/sections/{id}/emptyTrash`, `/status/sessions/terminate` embed verbs in paths.
- **Note:** Inherited from Plex's architecture. Document as legacy; consider `deprecated: true` where alternatives exist.

### 11. Resource IDs in Query Parameters
- **Reviewer:** API Design Purist
- **Problem:** `DELETE /playlists?ratingKey={ratingKey}`, `POST /status/sessions/terminate?sessionId={sessionId}` pass identifiers as query params.
- **Fix:** Use path params where possible; document current behavior as legacy.

### 12. 5 Unused Schemas
- **Reviewer:** OpenAPI Purist
- **Problem:** `Collection`, `Feature`, `PlayQueueResponse`, `ProviderFeature`, `UpdaterStatus` defined but never `$ref`'d.
- **Fix:** Wire into operations or delete.

### 13. 146 Error Responses Return `text/html` with No Schema
- **Reviewer:** SDK DevEx Critic
- **Problem:** `400`, `403`, `404` responses are `text/html: {}` with no schema.
- **Fix:** Define a reusable `Error` schema and apply it to all error responses.

### 14. Inconsistent Pagination
- **Reviewer:** API Design Purist
- **Problem:** Three mechanisms: `count`, `limit`, `X-Plex-Container-Start`/`X-Plex-Container-Size`.
- **Fix:** Standardize on one pair and reuse component parameters.

### 15. `accepts` Header Defaults to XML
- **Reviewer:** SDK DevEx Critic
- **Problem:** PMS endpoints return XML by default. JSON requested via custom `accepts` param.
- **Fix:** Document clearly; consider overriding default per-operation where known.

### 16. 20 Unstructured `200` Responses
- **Reviewer:** SDK DevEx Critic
- **Problem:** Bare `type: object` or `type: string` — zero autocomplete in SDKs.
- **Fix:** Add proper schemas, even if partial.

### 17. Unnecessary Single-Item `allOf`
- **Reviewer:** OpenAPI Purist
- **Problem:** 7 instances of `allOf: [{ $ref: ... }]` — redundant indirection.
- **Fix:** Replace with direct `$ref`.

### 18. Duplicate Inline Request Body
- **Reviewer:** OpenAPI Purist, SDK DevEx Critic
- **Problem:** `PUT /pins/link` defines same `{authToken, pin}` body twice (JSON + form-urlencoded).
- **Fix:** Extract to `components/schemas/LinkPinRequest`.

### 19. 18 Duplicate Enum Sets
- **Reviewer:** OpenAPI Purist
- **Problem:** `(0, 1)` repeated 14 times, `('lan', 'wan', 'cellular')` 4 times, etc.
- **Fix:** Extract to reusable schemas.

### 20. Invalid Examples
- **Reviewer:** OpenAPI Purist
- **Problem:** 21 violations — `example: 135` on `type: string`, pattern mismatches, case mismatches.
- **Fix:** Correct to match schema constraints.

---

## 🟡 Medium-Priority Issues

### 21. Path Parameter Naming Inconsistency
- **Reviewer:** API Design Purist
- **Problem:** `{id}`, `{userId}`, `{uuid}` used for same concept across endpoints.
- **Fix:** Standardize per resource type.

### 22. Tag Fragmentation
- **Reviewer:** API Design Purist, SDK DevEx Critic
- **Problem:** `Playlist` vs `Playlists` vs `Library Playlists`; `Collections` vs `Library Collections`.
- **Fix:** Consolidate to singular consistent tags.

### 23. `type` Used as Query Parameter (15+ times)
- **Reviewer:** SDK DevEx Critic
- **Problem:** Reserved word in most languages.
- **Fix:** Add `x-speakeasy-name-override` or rename.

### 24. No 201 Created for Resource Creation
- **Reviewer:** API Design Purist
- **Problem:** Only 1 `201` in entire spec. Creation endpoints return `200`.
- **Fix:** Return `201 Created` with `Location` header.

### 25. Weak Auth Scoping
- **Reviewer:** API Design Purist
- **Problem:** Only `admin` and `shared user` scopes. Many admin-only endpoints inherit broad `[shared user, admin]`.
- **Fix:** Audit every endpoint for minimum required scope.

### 26. Missing `required` Arrays
- **Reviewer:** OpenAPI Purist
- **Problem:** 47 response schemas + 4 request bodies lack `required`.
- **Fix:** Audit and add.

### 27. 63 Schemas Lack Descriptions
- **Reviewer:** OpenAPI Purist
- **Problem:** `Activity`, `BoolInt`, `ButlerTask`, `Channel`, etc.
- **Fix:** Add descriptions for generated SDK docs.

### 28. 9 Operations Share Identical Summaries
- **Reviewer:** SDK DevEx Critic
- **Problem:** `GET` and `POST` `/library/optimize` both called `"Optimize Library"`.
- **Fix:** Distinguish by HTTP method in summary.

---

## ✅ Positive Findings

- **All 154 `$ref`s resolve** — no broken references
- **All 404 `operationId`s are unique**
- **No trailing slash inconsistency**
- **No `type: array` without `items`**
- **No `nullable: true` misuse** — correctly uses OAS 3.1 `type: ["string", "null"]`
- **Security schemes fully utilized**
- **All path parameters declared**
- **CI passes** — prettier, speakeasy, vacuum all green

---

## Recommended Fix Order

1. **P0:** Add error responses to all operations
2. **P0:** Fix 3 kebab-case `operationId`s
3. **P0:** Fix malformed path parameter
4. **P0:** Add 5 missing global tag definitions
5. **P1:** Delete/wire up 5 unused schemas
6. **P1:** Fix `type: object` omissions
7. **P1:** Remove duplicate parameters from transcode ops
8. **P2:** Flatten single-item `allOf` wrappers
9. **P2:** Extract duplicated enums to reusable schemas
10. **P2:** Fix 21 invalid examples
11. **P3:** Add `required` arrays
12. **P3:** Add descriptions to 63 schemas
