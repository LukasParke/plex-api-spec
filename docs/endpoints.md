---
title: API Endpoints
---

# API Endpoints

This page is generated from [`plex-api-spec.yaml`](./plex-api-spec.yaml).
Do not edit it by hand; run `pnpm run spec:generate-reference` to regenerate it.

## Overview

| Method | Path | Summary | Operation ID |
| ------ | ---- | ------- | ------------ |
| GET | `/` | Get PMS info | `getServerInfo` |
| GET | `/:/eventsource/notifications` | Connect to Eventsource | `getNotifications` |
| GET | `/:/prefs` | Get all preferences | `getAllPreferences` |
| PUT | `/:/prefs` | Set preferences | `setPreferences` |
| GET | `/:/prefs/get` | Get a preferences | `getPreference` |
| PUT | `/:/rate` | Rate an item | `setRating` |
| PUT | `/:/scrobble` | Mark an item as played | `markPlayed` |
| POST | `/:/timeline` | Report media timeline | `report` |
| PUT | `/:/unscrobble` | Mark an item as unplayed | `unscrobble` |
| GET | `/:/websocket/notifications` | Connect to WebSocket | `connectWebSocket` |
| GET | `/{transcodeType}/:/transcode/universal/decision` | Make a decision on media playback | `makeDecision` |
| POST | `/{transcodeType}/:/transcode/universal/fallback` | Manually trigger a transcoder fallback | `triggerFallback` |
| GET | `/{transcodeType}/:/transcode/universal/start.{extension}` | Start A Transcoding Session | `startTranscodeSession` |
| GET | `/{transcodeType}/:/transcode/universal/subtitles` | Transcode subtitles | `transcodeSubtitles` |
| GET | `/activities` | Get all activities | `listActivities` |
| DELETE | `/activities/{activityId}` | Cancel a running activity | `cancelActivity` |
| DELETE | `/butler` | Stop all Butler tasks | `stopTasks` |
| GET | `/butler` | Get all Butler tasks | `getTasks` |
| POST | `/butler` | Start all Butler tasks | `startTasks` |
| DELETE | `/butler/{butlerTask}` | Stop a single Butler task | `stopTask` |
| POST | `/butler/{butlerTask}` | Start a single Butler task | `startTask` |
| POST | `/downloadQueue` | Create download queue | `createDownloadQueue` |
| GET | `/downloadQueue/{queueId}` | Get a download queue | `getDownloadQueue` |
| POST | `/downloadQueue/{queueId}/add` | Add to download queue | `addDownloadQueueItems` |
| GET | `/downloadQueue/{queueId}/item/{itemId}/decision` | Grab download queue item decision | `getItemDecision` |
| GET | `/downloadQueue/{queueId}/item/{itemId}/media` | Grab download queue media | `getDownloadQueueMedia` |
| GET | `/downloadQueue/{queueId}/items` | Get download queue items | `listDownloadQueueItems` |
| DELETE | `/downloadQueue/{queueId}/items/{itemId}` | Delete download queue items | `removeDownloadQueueItems` |
| GET | `/downloadQueue/{queueId}/items/{itemId}` | Get download queue items | `getDownloadQueueItems` |
| POST | `/downloadQueue/{queueId}/items/{itemId}/restart` | Restart processing of items from the decision | `restartProcessingDownloadQueueItems` |
| GET | `/hubs` | Get global hubs | `getAllHubs` |
| GET | `/hubs/continueWatching` | Get the continue watching hub | `getContinueWatching` |
| GET | `/hubs/items` | Get a hub's items | `getHubItems` |
| GET | `/hubs/metadata/{metadataId}` | Get hubs for section by metadata item | `getMetadataHubs` |
| GET | `/hubs/metadata/{metadataId}/postplay` | Get postplay hubs | `getPostplayHubs` |
| GET | `/hubs/metadata/{metadataId}/related` | Get related hubs | `getRelatedHubs` |
| GET | `/hubs/promoted` | Get the hubs which are promoted | `getPromotedHubs` |
| GET | `/hubs/search` | Search Hub | `searchHubs` |
| GET | `/hubs/search/voice` | Voice Search Hub | `voiceSearchHubs` |
| GET | `/hubs/sections/{sectionId}` | Get section hubs | `getSectionHubs` |
| DELETE | `/hubs/sections/{sectionId}/manage` | Reset hubs to defaults | `resetSectionDefaults` |
| GET | `/hubs/sections/{sectionId}/manage` | Get hubs | `listHubs` |
| POST | `/hubs/sections/{sectionId}/manage` | Create a custom hub | `createCustomHub` |
| DELETE | `/hubs/sections/{sectionId}/manage/{identifier}` | Delete a custom hub | `deleteCustomHub` |
| PUT | `/hubs/sections/{sectionId}/manage/{identifier}` | Change hub visibility | `updateHubVisibility` |
| PUT | `/hubs/sections/{sectionId}/manage/move` | Move Hub | `moveHub` |
| GET | `/identity` | Get PMS identity | `getIdentity` |
| GET | `/library/all` | Get all items in library | `getLibraryItems` |
| DELETE | `/library/caches` | Delete library caches | `deleteCaches` |
| PUT | `/library/clean/bundles` | Clean bundles | `cleanBundles` |
| POST | `/library/collections` | Create collection | `createCollection` |
| GET | `/library/collections/{collectionId}/composite/{updatedAt}` | Get a collection's image | `getCollectionImage` |
| GET | `/library/collections/{collectionId}/items` | Get items in a collection | `getCollectionItems` |
| PUT | `/library/collections/{collectionId}/items` | Add items to a collection | `addCollectionItems` |
| PUT | `/library/collections/{collectionId}/items/{itemId}` | Delete an item from a collection | `deleteCollectionItem` |
| PUT | `/library/collections/{collectionId}/items/{itemId}/move` | Reorder an item in the collection | `moveCollectionItem` |
| POST | `/library/file` | Ingest a transient item | `ingestTransientItem` |
| GET | `/library/matches` | Get library matches | `getLibraryMatches` |
| GET | `/library/media/{mediaId}/chapterImages/{chapter}` | Get a chapter image | `getChapterImage` |
| DELETE | `/library/metadata/{ids}` | Delete a metadata item | `deleteMetadataItem` |
| GET | `/library/metadata/{ids}` | Get a metadata item | `getMetadataItem` |
| PUT | `/library/metadata/{ids}` | Edit a metadata item | `editMetadataItem` |
| POST | `/library/metadata/{ids}/{element}` | Set an item's artwork, theme, etc | `setItemArtwork` |
| PUT | `/library/metadata/{ids}/{element}` | Set an item's artwork, theme, etc | `updateItemArtwork` |
| GET | `/library/metadata/{ids}/{element}/{timestamp}` | Get an item's artwork, theme, etc | `getItemArtwork` |
| PUT | `/library/metadata/{ids}/addetect` | Ad-detect an item | `detectAds` |
| GET | `/library/metadata/{ids}/allLeaves` | Get the leaves of an item | `getAllItemLeaves` |
| PUT | `/library/metadata/{ids}/analyze` | Analyze an item | `analyzeMetadata` |
| PUT | `/library/metadata/{ids}/chapterThumbs` | Generate thumbs of chapters for an item | `generateThumbs` |
| PUT | `/library/metadata/{ids}/credits` | Credit detect a metadata item | `detectCredits` |
| GET | `/library/metadata/{ids}/extras` | Get an item's extras | `getExtras` |
| POST | `/library/metadata/{ids}/extras` | Add to an item's extras | `addExtras` |
| GET | `/library/metadata/{ids}/file` | Get a file from a metadata or media bundle | `getFile` |
| PUT | `/library/metadata/{ids}/index` | Start BIF generation of an item | `startBifGeneration` |
| PUT | `/library/metadata/{ids}/intro` | Intro detect an item | `detectIntros` |
| POST | `/library/metadata/{ids}/marker` | Create a marker | `createMarker` |
| DELETE | `/library/metadata/{ids}/marker/{marker}` | Delete a marker | `deleteMarker` |
| PUT | `/library/metadata/{ids}/marker/{marker}` | Edit a marker | `editMarker` |
| PUT | `/library/metadata/{ids}/match` | Match a metadata item | `matchItem` |
| PUT | `/library/metadata/{ids}/matches` | Get metadata matches for an item | `listMatches` |
| DELETE | `/library/metadata/{ids}/media/{mediaItem}` | Delete a media item | `deleteMediaItem` |
| PUT | `/library/metadata/{ids}/merge` | Merge a metadata item | `mergeItems` |
| GET | `/library/metadata/{ids}/nearest` | Get nearest tracks to metadata item | `listSonicallySimilar` |
| PUT | `/library/metadata/{ids}/prefs` | Set metadata preferences | `setItemPreferences` |
| PUT | `/library/metadata/{ids}/refresh` | Refresh a metadata item | `refreshItemsMetadata` |
| GET | `/library/metadata/{ids}/related` | Get related items | `getRelatedItems` |
| GET | `/library/metadata/{ids}/similar` | Get similar items | `listSimilar` |
| PUT | `/library/metadata/{ids}/split` | Split a metadata item | `splitItem` |
| GET | `/library/metadata/{ids}/subtitles` | Add subtitles | `addSubtitles` |
| GET | `/library/metadata/{ids}/tree` | Get metadata items as a tree | `getItemTree` |
| PUT | `/library/metadata/{ids}/unmatch` | Unmatch a metadata item | `unmatch` |
| GET | `/library/metadata/{ids}/users/top` | Get metadata top users | `listTopUsers` |
| PUT | `/library/metadata/{ids}/voiceActivity` | Detect voice activity | `detectVoiceActivity` |
| GET | `/library/metadata/augmentations/{augmentationId}` | Get augmentation status | `getAugmentationStatus` |
| PUT | `/library/optimize` | Optimize the Database | `optimizeDatabase` |
| PUT | `/library/parts/{partId}` | Set stream selection | `setStreamSelection` |
| GET | `/library/parts/{partId}/{changestamp}/{filename}` | Get a media part | `getMediaPart` |
| GET | `/library/parts/{partId}/indexes/{index}` | Get BIF index for a part | `getPartIndex` |
| GET | `/library/parts/{partId}/indexes/{index}/{offset}` | Get an image from part BIF | `getImageFromBif` |
| GET | `/library/people/{personId}` | Get person details | `getPerson` |
| GET | `/library/people/{personId}/media` | Get media for a person | `listPersonMedia` |
| GET | `/library/randomArtwork` | Get random artwork | `getRandomArtwork` |
| DELETE | `/library/sections/{sectionId}` | Delete a library section | `deleteLibrarySection` |
| GET | `/library/sections/{sectionId}` | Get a library section by id | `getLibraryDetails` |
| PUT | `/library/sections/{sectionId}` | Edit a library section | `editSection` |
| GET | `/library/sections/{sectionId}/albums` | Set section albums | `getAlbums` |
| GET | `/library/sections/{sectionId}/all` | Get items in the section | `listContent` |
| PUT | `/library/sections/{sectionId}/all` | Set the fields of the filtered items | `updateItems` |
| GET | `/library/sections/{sectionId}/allLeaves` | Set section leaves | `getAllLeaves` |
| PUT | `/library/sections/{sectionId}/analyze` | Analyze a section | `startAnalysis` |
| GET | `/library/sections/{sectionId}/arts` | Set section artwork | `getArts` |
| GET | `/library/sections/{sectionId}/autocomplete` | Get autocompletions for search | `autocomplete` |
| GET | `/library/sections/{sectionId}/categories` | Set section categories | `getCategories` |
| GET | `/library/sections/{sectionId}/cluster` | Set section clusters | `getCluster` |
| DELETE | `/library/sections/{sectionId}/collection/{collectionId}` | Delete a collection | `deleteCollection` |
| GET | `/library/sections/{sectionId}/collections` | Get collections in a section | `getCollections` |
| GET | `/library/sections/{sectionId}/common` | Get common fields for items | `getCommon` |
| GET | `/library/sections/{sectionId}/composite/{updatedAt}` | Get a section composite image | `getSectionImage` |
| GET | `/library/sections/{sectionId}/computePath` | Similar tracks to transition from one to another | `getSonicPath` |
| PUT | `/library/sections/{sectionId}/emptyTrash` | Empty section trash | `emptyTrash` |
| GET | `/library/sections/{sectionId}/filters` | Get section filters | `getSectionFilters` |
| GET | `/library/sections/{sectionId}/firstCharacters` | Get list of first characters | `getFirstCharacters` |
| DELETE | `/library/sections/{sectionId}/indexes` | Delete section indexes | `deleteIndexes` |
| DELETE | `/library/sections/{sectionId}/intros` | Delete section intro markers | `deleteIntros` |
| GET | `/library/sections/{sectionId}/location` | Get all folder locations | `getFolders` |
| GET | `/library/sections/{sectionId}/moment` | Set section moments | `listMoments` |
| GET | `/library/sections/{sectionId}/nearest` | The nearest audio tracks | `getSonicallySimilar` |
| GET | `/library/sections/{sectionId}/prefs` | Get section prefs | `getSectionPreferences` |
| PUT | `/library/sections/{sectionId}/prefs` | Set section prefs | `setSectionPreferences` |
| DELETE | `/library/sections/{sectionId}/refresh` | Cancel section refresh | `cancelRefresh` |
| POST | `/library/sections/{sectionId}/refresh` | Refresh section | `refreshSection` |
| GET | `/library/sections/{sectionId}/sorts` | Get a section sorts | `getAvailableSorts` |
| GET | `/library/sections/all` | Get library sections (main Media Provider Only) | `getSections` |
| POST | `/library/sections/all` | Add a library section | `addSection` |
| DELETE | `/library/sections/all/refresh` | Stop refresh | `stopAllRefreshes` |
| GET | `/library/sections/prefs` | Get section prefs | `getSectionsPrefs` |
| POST | `/library/sections/refresh` | Refresh all sections | `refreshSectionsMetadata` |
| DELETE | `/library/streams/{streamId}.{ext}` | Delete a stream | `deleteStream` |
| GET | `/library/streams/{streamId}.{ext}` | Get a stream | `getStream` |
| PUT | `/library/streams/{streamId}.{ext}` | Set a stream offset | `setStreamOffset` |
| GET | `/library/streams/{streamId}/levels` | Get loudness about a stream in json | `getStreamLevels` |
| GET | `/library/streams/{streamId}/loudness` | Get loudness about a stream | `getStreamLoudness` |
| GET | `/library/tags` | Get all library tags of a type | `getTags` |
| GET | `/livetv/dvrs` | Get DVRs | `listDVRs` |
| POST | `/livetv/dvrs` | Create a DVR | `createDVR` |
| DELETE | `/livetv/dvrs/{dvrId}` | Delete a single DVR | `deleteDVR` |
| GET | `/livetv/dvrs/{dvrId}` | Get a single DVR | `getDVR` |
| POST | `/livetv/dvrs/{dvrId}/channels/{channel}/tune` | Tune a channel on a DVR | `tuneChannel` |
| DELETE | `/livetv/dvrs/{dvrId}/devices/{deviceId}` | Remove a device from an existing DVR | `removeDeviceFromDVR` |
| PUT | `/livetv/dvrs/{dvrId}/devices/{deviceId}` | Add a device to an existing DVR | `addDeviceToDVR` |
| DELETE | `/livetv/dvrs/{dvrId}/lineups` | Delete a DVR Lineup | `deleteLineup` |
| PUT | `/livetv/dvrs/{dvrId}/lineups` | Add a DVR Lineup | `addLineup` |
| PUT | `/livetv/dvrs/{dvrId}/prefs` | Set DVR preferences | `setDVRPreferences` |
| DELETE | `/livetv/dvrs/{dvrId}/reloadGuide` | Tell a DVR to stop reloading program guide | `stopDVRReload` |
| POST | `/livetv/dvrs/{dvrId}/reloadGuide` | Tell a DVR to reload program guide | `reloadGuide` |
| GET | `/livetv/epg/channelmap` | Compute the best channel map | `computeChannelMap` |
| GET | `/livetv/epg/channels` | Get channels for a lineup | `getChannels` |
| GET | `/livetv/epg/countries` | Get all countries | `getCountries` |
| GET | `/livetv/epg/countries/{country}/{epgId}/lineups` | Get lineups for a country via postal code | `getCountriesLineups` |
| GET | `/livetv/epg/countries/{country}/{epgId}/regions` | Get regions for a country | `getCountryRegions` |
| GET | `/livetv/epg/countries/{country}/{epgId}/regions/{region}/lineups` | Get lineups for a region | `listLineups` |
| GET | `/livetv/epg/languages` | Get all languages | `getAllLanguages` |
| GET | `/livetv/epg/lineup` | Compute the best lineup | `getLineup` |
| GET | `/livetv/epg/lineupchannels` | Get the channels for mulitple lineups | `getLineupChannels` |
| GET | `/livetv/sessions` | Get all sessions | `getSessions` |
| GET | `/livetv/sessions/{sessionId}` | Get a single session | `getLiveTVSession` |
| GET | `/livetv/sessions/{sessionId}/{consumerId}/{segmentId}` | Get a single session segment | `getSessionSegment` |
| GET | `/livetv/sessions/{sessionId}/{consumerId}/index.m3u8` | Get a session playlist index | `getSessionPlaylistIndex` |
| POST | `/log` | Logging a multi-line message to the Plex Media Server log | `writeLog` |
| PUT | `/log` | Logging a single-line message to the Plex Media Server log | `writeMessage` |
| POST | `/log/networked` | Enabling Papertrail | `enablePapertrail` |
| GET | `/media/grabbers` | Get available grabbers | `getAvailableGrabbers` |
| GET | `/media/grabbers/devices` | Get all devices | `listDevices` |
| POST | `/media/grabbers/devices` | Add a device | `addDevice` |
| DELETE | `/media/grabbers/devices/{deviceId}` | Remove a device | `removeDevice` |
| GET | `/media/grabbers/devices/{deviceId}` | Get device details | `getDeviceDetails` |
| PUT | `/media/grabbers/devices/{deviceId}` | Enable or disable a device | `modifyDevice` |
| PUT | `/media/grabbers/devices/{deviceId}/channelmap` | Set a device's channel mapping | `setChannelmap` |
| GET | `/media/grabbers/devices/{deviceId}/channels` | Get a device's channels | `getDevicesChannels` |
| PUT | `/media/grabbers/devices/{deviceId}/prefs` | Set device preferences | `setDevicePreferences` |
| DELETE | `/media/grabbers/devices/{deviceId}/scan` | Tell a device to stop scanning for channels | `stopScan` |
| POST | `/media/grabbers/devices/{deviceId}/scan` | Tell a device to scan for channels | `scan` |
| GET | `/media/grabbers/devices/{deviceId}/thumb/{version}` | Get device thumb | `getThumb` |
| POST | `/media/grabbers/devices/discover` | Tell grabbers to discover devices | `discoverDevices` |
| DELETE | `/media/grabbers/operations/{operationId}` | Cancel an existing grab | `cancelGrab` |
| GET | `/media/providers` | Get the list of available media providers | `listProviders` |
| POST | `/media/providers` | Add a media provider | `addProvider` |
| DELETE | `/media/providers/{provider}` | Delete a media provider | `deleteMediaProvider` |
| POST | `/media/providers/refresh` | Refresh media providers | `refreshProviders` |
| GET | `/media/subscriptions` | Get all subscriptions | `getAllSubscriptions` |
| POST | `/media/subscriptions` | Create a subscription | `createSubscription` |
| DELETE | `/media/subscriptions/{subscriptionId}` | Delete a subscription | `deleteSubscription` |
| GET | `/media/subscriptions/{subscriptionId}` | Get a single subscription | `getSubscription` |
| PUT | `/media/subscriptions/{subscriptionId}` | Edit a subscription | `editSubscriptionPreferences` |
| PUT | `/media/subscriptions/{subscriptionId}/move` | Re-order a subscription | `reorderSubscription` |
| POST | `/media/subscriptions/process` | Process all subscriptions | `processSubscriptions` |
| GET | `/media/subscriptions/scheduled` | Get all scheduled recordings | `getScheduledRecordings` |
| GET | `/media/subscriptions/template` | Get the subscription template | `getTemplate` |
| GET | `/photo/:/transcode` | Transcode an image | `transcodeImage` |
| GET | `/playlists` | List playlists | `listPlaylists` |
| POST | `/playlists` | Create a Playlist | `createPlaylist` |
| DELETE | `/playlists/{playlistId}` | Delete a Playlist | `deletePlaylist` |
| GET | `/playlists/{playlistId}` | Retrieve Playlist | `getPlaylist` |
| PUT | `/playlists/{playlistId}` | Editing a Playlist | `updatePlaylist` |
| GET | `/playlists/{playlistId}/generators` | Get a playlist's generators | `getPlaylistGenerators` |
| DELETE | `/playlists/{playlistId}/items` | Clearing a playlist | `clearPlaylistItems` |
| GET | `/playlists/{playlistId}/items` | Retrieve Playlist Contents | `getPlaylistItems` |
| PUT | `/playlists/{playlistId}/items` | Adding to  a Playlist | `addPlaylistItems` |
| DELETE | `/playlists/{playlistId}/items/{generatorId}` | Delete a Generator | `deletePlaylistItem` |
| GET | `/playlists/{playlistId}/items/{generatorId}` | Get a playlist generator | `getPlaylistGenerator` |
| PUT | `/playlists/{playlistId}/items/{generatorId}` | Modify a Generator | `modifyPlaylistGenerator` |
| PUT | `/playlists/{playlistId}/items/{generatorId}/{metadataId}/{action}` | Reprocess a generator | `refreshPlaylist` |
| GET | `/playlists/{playlistId}/items/{generatorId}/items` | Get a playlist generator's items | `getPlaylistGeneratorItems` |
| PUT | `/playlists/{playlistId}/items/{playlistItemId}/move` | Moving items in a playlist | `movePlaylistItem` |
| POST | `/playlists/upload` | Upload | `uploadPlaylist` |
| POST | `/playQueues` | Create a play queue | `createPlayQueue` |
| GET | `/playQueues/{playQueueId}` | Retrieve a play queue | `getPlayQueue` |
| PUT | `/playQueues/{playQueueId}` | Add a generator or playlist to a play queue | `addToPlayQueue` |
| DELETE | `/playQueues/{playQueueId}/items` | Clear a play queue | `clearPlayQueue` |
| DELETE | `/playQueues/{playQueueId}/items/{playQueueItemId}` | Delete an item from a play queue | `deletePlayQueueItem` |
| PUT | `/playQueues/{playQueueId}/items/{playQueueItemId}/move` | Move an item in a play queue | `movePlayQueueItem` |
| PUT | `/playQueues/{playQueueId}/reset` | Reset a play queue | `resetPlayQueue` |
| PUT | `/playQueues/{playQueueId}/shuffle` | Shuffle a play queue | `shuffle` |
| PUT | `/playQueues/{playQueueId}/unshuffle` | Unshuffle a play queue | `unshuffle` |
| GET | `/resources` | Get Server Resources | `get-server-resources` |
| GET | `/security/resources` | Get Source Connection Information | `getSourceConnectionInformation` |
| POST | `/security/token` | Get Transient Tokens | `getTransientToken` |
| GET | `/services/ultrablur/colors` | Get UltraBlur Colors | `getColors` |
| GET | `/services/ultrablur/image` | Get UltraBlur Image | `getImage` |
| GET | `/status/sessions` | List Sessions | `listSessions` |
| GET | `/status/sessions/background` | Get background tasks | `getBackgroundTasks` |
| DELETE | `/status/sessions/history/{historyId}` | Delete Single History Item | `deleteHistory` |
| GET | `/status/sessions/history/{historyId}` | Get Single History Item | `getHistoryItem` |
| GET | `/status/sessions/history/all` | List Playback History | `listPlaybackHistory` |
| POST | `/status/sessions/terminate` | Terminate a session | `terminateSession` |
| PUT | `/updater/apply` | Applying updates | `applyUpdates` |
| PUT | `/updater/check` | Checking for updates | `checkUpdates` |
| GET | `/updater/status` | Querying status of updates | `getUpdatesStatus` |
| GET | `/user` | Get Token Details | `getTokenDetails` |
| GET | `/users` | Get list of all connected users | `get-users` |
| POST | `/users/signin` | Get User Sign In Data | `post-users-sign-in-data` |

## Authentication

Most endpoints require an `X-Plex-Token` header or `X-Plex-Token` query parameter.

## Response format

Responses default to XML. Request JSON by sending `Accept: application/json`.
