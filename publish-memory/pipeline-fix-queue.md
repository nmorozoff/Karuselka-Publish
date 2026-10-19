# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260907-001

status: open
run_at: 2026-09-07T08:02:30.601810+00:00
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

## INC-20260907-001

status: open
run_at: 2026-09-07T08:02:43.693925+00:00
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

## INC-20260907-001

status: open
run_at: 2026-09-07T08:05:01.283052+00:00
pair: pair2
stage: publish
carousel: crsl_20260903_0809_909

### Error
```
Zernio tiktok error: {'post': {'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, '_id': '6a9e7012e8d9bc677f962a61', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Правда, которую тупо нужно принять — без розовых очков.', 'mediaItems': [{'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/o6mreo22q2qwc46gacwb7/slide-01.png?rlkey=45wmeinauaa59s2lctvg7nioh&dl=1', '_id': '6a9e7012e8d9bc677f962a62'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/4i0qvsd6xwtrct5i0uimd/slide-02.png?rlkey=txcy9jxxkkrardzgdvoe6snr4&dl=1', '_id': '6a9e7012e8d9bc677f962a63'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/6ki0odpivf7hac1alqn1j/slide-03.png?rlkey=ez4t97k9yzuve6pktnphhv7us&dl=1', '_id': '6a9e7012e8d9bc677f962a64'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/xwookw21bi1zr4m8ykgqx/slide-04.png?rlkey=amunoeswokf5r46if72pdxj4n&dl=1', '_id': '6a9e7012e8d9bc677f962a65'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/vgxzfzxumzsonrm1olhoj/slide-05.png?rlkey=cto7nguazlu7o2bmwjl7qin5j&dl=1', '_id': '6a9e7012e8d9bc677f962a66'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/tddrgjhun5gckvd0rp9sk/slide-06.png?rlkey=fptcwwy1q8xhrc9g2fqv8w4nm&dl=1', '_id': '6a9e7012e8d9bc677f962a67'}], 'platforms': [{'platform': 'tiktok', 'accountId': {'_id': '6a6a3bf5df17280d93d66feb', 'platform': 'tiktok', 'profileId': '6a6a3b62bbbe9621ca350a53', 'displayName': 'Психолог Морозова Наталья', 'isActive': True, 'profilePicture': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=c6cb7d94&x-expires=1788926400&x-signature=GW99G5Um%2BQfu9HXRiX1j6egmHmI%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my2', 'username': 'natalyamorozovapsy'}, 'profileId': '6a6a3b62bbbe9621ca350a53', 'customMedia': [], 'scheduledFor': '2026-09-07T08:04:27.643Z', 'platformSpecificData': {'tiktokSettings': {'privacy_level': 'PUBLIC_TO_EVERYONE', 'allow_comment': True, 'media_type': 'photo', 'photo_cover_index': 0, 'description': 'Чем больше стараемся понравиться — тем меньше нравимся. Другой чувствует: от него хотят функции, а не контакта. Мы боимся не того, что не получится — а того, что получится. Успех, близость, ответственность. «Хорошая» без спонтанности никому не нужна. И человек меняется только если сам захочет — сколько бы вы ни вкладывались. В отношениях мужчина усиливает то, что вы реально о себе думаете. «Меня бросят» — и вы найдёте того, кто подтвердит. Мнение о себе часто — это страхи значимых взрослых из детства. А кризисы будут всегда. Вопрос — научимся ли мы их выдерживать. Запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля (morozovanatalia.ru) #отношения #самооценка #психология #эмдр', 'auto_add_music': True, 'content_preview_confirmed': True, 'express_consent_given': True}}, 'status': 'failed', 'publishAttempts': 0, 'contentHash': '2fabc2ceed0e9765d37d69aaa6aa4584', '_id': '6a9e7012e8d9bc677f962a68', 'errorCategory': 'user_abuse', 'errorMessage': 'TikTok detected potential spam content. Please review content guidelines.', 'errorSource': 'user'}], 'scheduledFor': '2026-09-07T08:04:27.643Z', 'timezone': 'UTC', 'status': 'failed', 'tags': [], 'hashtags': [], 'mentions': [], 'visibility': 'public', 'crosspostingEnabled': True, 'metadata': {'usageCounted': True, 'usageRefunded': True}, 'publishAttempts': 0, 'createdAt': '2026-09-07T08:04:34.407Z', 'updatedAt': '2026-09-07T08:04:57.853Z', '__v': 0, 'publishingClaimedAt': '2026-09-07T08:04:34.478Z'}, 'message': 'Post created but publishing failed', 'error': 'All platforms failed', 'platformResults': [{'platform': 'tiktok', 'status': 'failed', 'error': 'TikTok detected potential spam content. Please review content guidelines.'}]}
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
