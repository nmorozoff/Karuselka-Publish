# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260810-001

status: open
run_at: 2026-08-10T08:05:40.631801+00:00
pair: pair2
stage: publish
carousel: crsl_20260808_1340_265

### Error
```
Zernio tiktok error: {'post': {'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, '_id': '6a7986263921f2fe754ad549', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Ты не ленишься отдыхать — ты боишься, что без тебя всё развалится.', 'mediaItems': [{'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/8n5omg8ztj03tv5cr0yxe/slide-01.png?rlkey=hnym76mjb1iygtcvfhlud0olw&dl=1', '_id': '6a7986263921f2fe754ad54a'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/z8vk53ol8d4u8nld2ewtl/slide-02.png?rlkey=uh3bev0ux9mk1svzm1rt1t1ru&dl=1', '_id': '6a7986263921f2fe754ad54b'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/fpa587s8wspk6ojakahng/slide-03.png?rlkey=we08ndltv7x8vmzdq854bddk7&dl=1', '_id': '6a7986263921f2fe754ad54c'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/ipg8fjqjjvmj616x84t15/slide-04.png?rlkey=fn01gfunbujnsiyhxtsqcxmsw&dl=1', '_id': '6a7986263921f2fe754ad54d'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/kf0394duxdtg73wdyvrzp/slide-05.png?rlkey=8hujfsphzbly0ezt1g6flfd6q&dl=1', '_id': '6a7986263921f2fe754ad54e'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/kzdn0xren9sefxpukq0bu/slide-06.png?rlkey=l7ha5lgbdmvpkz94zp9x0hu1i&dl=1', '_id': '6a7986263921f2fe754ad54f'}], 'platforms': [{'platform': 'tiktok', 'accountId': {'_id': '6a6a3bf5df17280d93d66feb', 'platform': 'tiktok', 'profileId': '6a6a3b62bbbe9621ca350a53', 'displayName': 'Психолог Морозова Наталья', 'isActive': True, 'profilePicture': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=12f35411&x-expires=1786507200&x-signature=UH9CXoVrTyBpTYsu6Shym3BqA80%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my3', 'username': 'natalyamorozovapsy'}, 'profileId': '6a6a3b62bbbe9621ca350a53', 'customMedia': [], 'scheduledFor': '2026-08-10T08:04:46.530Z', 'platformSpecificData': {'tiktokSettings': {'privacy_level': 'PUBLIC_TO_EVERYONE', 'allow_comment': True, 'media_type': 'photo', 'photo_cover_index': 0, 'description': 'Гиперответственность часто выглядит как сила. Вас хвалят за надёжность, а внутри — хроническое напряжение и тихое раздражение на всех, кто «может позволить себе быть слабым».\n\nЭтот режим когда-то спас. В семье, где эмоции были нестабильны, ребёнок берёт на себя лишнее: успокаивает, предугадывает, контролирует. Взрослым это превращается в невозможность делегировать и в вину за отдых.\n\nПерелом начинается не с жёсткого «мне всё равно», а с телесного разрешения: я могу быть важной, даже когда не спасаю. Когда нервная система это проживает, контроль перестаёт быть единственной опорой.\n\nЗапишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля.\n\n#гиперответственность #выгорание #границы #EMDR #психологонлайн', 'auto_add_music': True, 'content_preview_confirmed': True, 'express_consent_given': True}, '__platformUserIdSnapshot': '-000_sYAeqwVBNbcEsZQOygyDrPOEn7B6YbX', '__usernameSnapshot': 'natalyamorozovapsy', 'publishingStarted': None, 'lastPublishStage': 'publishing', 'tiktokPublishingStarted': None, '__debugCheckpoint': 'PRE_MEDIA_URL_PROCESSING @ 2026-08-10T08:05:04.012Z'}, 'status': 'failed', 'publishAttempts': 0, 'contentHash': '3adf3645611e9ec080006115eec5870f', '_id': '6a7986263921f2fe754ad550', 'errorCategory': 'unknown', 'errorMessage': 'URL ownership not verified in TikTok developer portal. Please verify domain ownership at https://developers.tiktok.com/', 'errorSource': 'platform'}], 'scheduledFor': '2026-08-10T08:04:46.530Z', 'timezone': 'UTC', 'status': 'failed', 'tags': [], 'hashtags': [], 'mentions': [], 'visibility': 'public', 'crosspostingEnabled': True, 'metadata': {'usageCounted': True, 'usageRefunded': True}, 'publishAttempts': 0, 'createdAt': '2026-08-10T08:04:54.269Z', 'updatedAt': '2026-08-10T08:05:32.637Z', '__v': 0, 'publishingClaimedAt': '2026-08-10T08:04:54.405Z'},
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

status: open
run_at: 2026-08-10T08:06:54.799160+00:00
pair: pair2
stage: notify
carousel: unknown

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
