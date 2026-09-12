# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260912-001

status: open
run_at: 2026-09-12T08:02:41.328030+00:00
pair: pair2
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260912-001

status: open
run_at: 2026-09-12T08:03:21.772624+00:00
pair: pair2
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260912-001

status: open
run_at: 2026-09-12T08:04:30.376382+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_0746_191

### Error
```
Zernio tiktok error: {'post': {'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, '_id': '6aa5078923da14ae1e5f3276', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Карусель', 'mediaItems': [{'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/xwinbfgd619g4nc3gy63n/slide-01.png?rlkey=u668gviv4gvrjeh1ce7skf56a&dl=1', '_id': '6aa5078923da14ae1e5f3277'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/khhv9wfs9eo96tg5fhven/slide-02.png?rlkey=tlsmhvajv4epd92qdm9s6e7o6&dl=1', '_id': '6aa5078923da14ae1e5f3278'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/mvshmj6zogd0qr5oex5se/slide-03.png?rlkey=ql6bvakpa30h82bbjkzz06uqm&dl=1', '_id': '6aa5078923da14ae1e5f3279'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/dg684z9q8qo767gtk3rbq/slide-04.png?rlkey=g1w1lkp08ty02rg7koy78j6u8&dl=1', '_id': '6aa5078923da14ae1e5f327a'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/dd9wahwnsgn1rqaw5nii8/slide-05.png?rlkey=mgx8ob5krfgyr4qp4iwakbzjp&dl=1', '_id': '6aa5078923da14ae1e5f327b'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/6xc3b6bhpbhjnp6k53f6m/slide-06.png?rlkey=le5k8ylnnzg7zbt3nbkwaeqem&dl=1', '_id': '6aa5078923da14ae1e5f327c'}], 'platforms': [{'platform': 'tiktok', 'accountId': {'_id': '6a6a3bf5df17280d93d66feb', 'platform': 'tiktok', 'profileId': '6a6a3b62bbbe9621ca350a53', 'displayName': 'Психолог Морозова Наталья', 'isActive': True, 'profilePicture': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=8c2ee812&x-expires=1789358400&x-signature=p5i2ZibT7ZFZ89r5MD%2Bg%2FuzkXPg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my', 'username': 'natalyamorozovapsy'}, 'profileId': '6a6a3b62bbbe9621ca350a53', 'customMedia': [], 'scheduledFor': '2026-09-12T08:04:19.423Z', 'platformSpecificData': {'tiktokSettings': {'privacy_level': 'PUBLIC_TO_EVERYONE', 'allow_comment': True, 'media_type': 'photo', 'photo_cover_index': 0, 'description': '', 'auto_add_music': True, 'content_preview_confirmed': True, 'express_consent_given': True}}, 'status': 'failed', 'publishAttempts': 0, 'contentHash': 'd9d8f0895401ce9b0cac786b510b3dd9', '_id': '6aa5078923da14ae1e5f327d', 'errorCategory': 'quota_exhausted', 'errorMessage': 'TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, or try again in a few hours as capacity frees up.', 'errorSource': 'platform'}], 'scheduledFor': '2026-09-12T08:04:19.423Z', 'timezone': 'UTC', 'status': 'failed', 'tags': [], 'hashtags': [], 'mentions': [], 'visibility': 'public', 'crosspostingEnabled': True, 'metadata': {'usageCounted': True, 'usageRefunded': True}, 'publishAttempts': 0, 'createdAt': '2026-09-12T08:04:26.021Z', 'updatedAt': '2026-09-12T08:04:26.901Z', '__v': 0, 'publishingClaimedAt': '2026-09-12T08:04:26.105Z'}, 'message': 'Post created but publishing failed', 'error': 'All platforms failed', 'platformResults': [{'platform': 'tiktok', 'status': 'failed', 'error': 'TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, or try again in a few hours as capacity frees up.'}]}
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---
