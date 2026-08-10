# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260810-001

status: needs-human
fix_summary: TikTok user_abuse/spam — контент отклонён платформой, требуется правка caption/хештегов вручную

### Error
```
Zernio tiktok error: {'post': {'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, '_id': '6a79e8ee8201bc5ece0c5a40', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Тебе не «сложный характер» — тебе долго говорили, что твои чувства неправильные.', 'mediaItems': [{'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/xuywlw2tbjm2inzj0wqn8/slide-01.png?rlkey=evb8sjg0ewu17dac3tl0lnvi7&dl=1', '_id': '6a79e8ee8201bc5ece0c5a41'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/jb2wsw5wo4qklt8cin3v0/slide-02.png?rlkey=67difmprarvwlef57c8jum59d&dl=1', '_id': '6a79e8ee8201bc5ece0c5a42'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/sj2961gh5zqj09ylokdxl/slide-03.png?rlkey=y3ttmqu50zzjg2bagku4pr7lq&dl=1', '_id': '6a79e8ee8201bc5ece0c5a43'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/lfd5sn2na1jgitwaegajj/slide-04.png?rlkey=25asr84iybkyh8h30ffsn9bti&dl=1', '_id': '6a79e8ee8201bc5ece0c5a44'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/cpent36ttac015xhxa3g0/slide-05.png?rlkey=uv7kmfsmgsxosif4qk5dmi2w9&dl=1', '_id': '6a79e8ee8201bc5ece0c5a45'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/h1bvacjq4wzl3ly5082qo/slide-06.png?rlkey=o3slmbddb2z9q6xiu3b0u87x6&dl=1', '_id': '6a79e8ee8201bc5ece0c5a46'}], 'platforms': [{'platform': 'tiktok', 'accountId': {'_id': '6a6a3bf5df17280d93d66feb', 'platform': 'tiktok', 'profileId': '6a6a3b62bbbe9621ca350a53', 'displayName': 'Психолог Морозова Наталья', 'isActive': True, 'profilePicture': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=12f35411&x-expires=1786507200&x-signature=UH9CXoVrTyBpTYsu6Shym3BqA80%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my3', 'username': 'natalyamorozovapsy'}, 'profileId': '6a6a3b62bbbe9621ca350a53', 'customMedia': [], 'scheduledFor': '2026-08-10T15:05:32.909Z', 'platformSpecificData': {'tiktokSettings': {'privacy_level': 'PUBLIC_TO_EVERYONE', 'allow_comment': True, 'media_type': 'photo', 'photo_cover_index': 0, 'description': 'Фоновая вина — это когда вы извиняетесь, даже не понимая за что. Когда любое «нет» сопровождается внутренним судом. Когда успех не радует, потому что «могла бы лучше».\n\nЧасто это не про воспитание характера, а про тихое эмоциональное насилие: обесценивание, сравнения, холодность под видом «заботы». Ребёнок делает вывод: со мной что-то не так. Взрослый носит этот вывод как вторую кожу.\n\nСнять вину — не значит стать безответственной. Это значит перестать платить за чужие ожидания ценой собственной жизни. Когда тело это понимает, «сложный характер» растворяется — остаётесь вы.\n\nЗапишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля.\n\n#чувствовины #самооценка #токсичныеродители #EMDR #психотерапия', 'auto_add_music': True, 'content_preview_confirmed': True, 'express_consent_given': True}, '__platformUserIdSnapshot': '-000_sYAeqwVBNbcEsZQOygyDrPOEn7B6YbX', '__usernameSnapshot': 'natalyamorozovapsy', 'publishingStarted': None, 'lastPublishStage': 'publishing', 'tiktokPublishingStarted': None, '__debugCheckpoint': 'PRE_MEDIA_URL_PROCESSING @ 2026-08-10T15:06:48.989Z'}, 'status': 'failed', 'publishAttempts': 0, 'contentHash': 'f50316f720b3f8deb4369ea557dc242f', '_id': '6a79e8ee8201bc5ece0c5a47', 'errorCategory': 'user_abuse', 'errorMessage': 'TikTok detected potential spam content. Please review content guidelines.', 'errorSource': 'user'}], 'scheduledFor': '2026-08-10T15:05:32.909Z', 'timezone': 'UTC', 'status': 'failed', 'tags': [], 'hashtags': [], 'mentions': [], 'visibility': 'public', 'crosspostingEnabled': True, 'metadata': {'usageCounted': True, 'usageRefunded': True}, 'publishAttempts': 0, 'createdAt': '2026-08-10T15:06:22.816Z', 'updatedAt': '2026-08-10T15:07:17.433Z', '__v': 0, 'publishingClaimedAt': '2026-08-10T15:06:22.932Z'}, 'message': 'Post created but publishin
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260810-001

status: needs-human
fix_summary: TikTok spam detection — ручная правка контента карусели crsl_20260808_1347_622

### Error
```
TikTok spam detection: crsl_20260808_1347_622 - TikTok detected potential spam content
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260810-001

status: fixed
fix_summary: notify_max.py теперь читает errors[] из worker-last-run.json вместо not_attempted
files_changed: scripts/notify_max.py

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks
```

### Context
```json
{
  "instagram_status": "not_attempted",
  "tiktok_status": "not_attempted"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260810-001

status: fixed
fix_summary: http_client.urlopen пробрасывает HTTPError с телом ответа для диагностики Zernio 400
files_changed: scripts/lib/http_client.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 400: Bad Request
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260810-001

status: fixed
fix_summary: publish_incident.py --list-open работает без обязательных --pair/--stage/--error
files_changed: scripts/publish_incident.py

### Error
```
Zernio HTTP 400 on retry: crsl_20260805_1935_596
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
