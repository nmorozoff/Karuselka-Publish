# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260909-001

status: fixed
run_at: 2026-09-09T18:05:52.188508+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_1522_743
fix_summary: IG @natalia_morozova_psy ok; TikTok capacity (transient). Добавлен классификатор tiktok_capacity + читаемый Max-отчёт для PARTIAL_IG_OK. Retry TikTok: --tiktok-only --name crsl_20260908_1522_743 --retry-failed
files_changed:
- scripts/lib/publish_failure.py
- scripts/lib/publish_engine.py

### Error
```
PARTIAL_IG_OK|{"post": {"recycling": {"enabled": false, "gapFreq": "month", "recycleCount": 0, "contentVariations": [], "contentVariationIndex": 0}, "_id": "6aa19fff6ac254f5ab962c99", "userId": "6a6a3b62bbbe9621ca350a43", "title": "", "content": "Мама может обожать сына и не выносить дочь — и при этом дело не в детях.", "mediaItems": [{"type": "image", "url": "https://www.dropbox.com/scl/fi/dsdt623egr8kf7gt0mpvs/slide-01.png?rlkey=gowdf72zbyvjhvcq5gxvkq007&dl=1", "_id": "6aa19fff6ac254f5ab962c9a"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/zoak5hi75s53a6lnfxrct/slide-02.png?rlkey=9jpexny7olg3hske3ycp5qjbh&dl=1", "_id": "6aa19fff6ac254f5ab962c9b"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/5elhgl8fnaamlvkvfocpa/slide-03.png?rlkey=5h0fsr2z3f7phmbd1ptvt8txs&dl=1", "_id": "6aa19fff6ac254f5ab962c9c"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/2b69nw832pejmftwt5yzc/slide-04.png?rlkey=2ylbuw6c35jnsxre4kst2phbx&dl=1", "_id": "6aa19fff6ac254f5ab962c9d"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/yni5h5hb1whw1jcw8h5qf/slide-05.png?rlkey=ekkxzkokwi8wdza3a7vegjujo&dl=1", "_id": "6aa19fff6ac254f5ab962c9e"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/uqcgsg2x8fxdayiennll1/slide-06.png?rlkey=4xstxigdba2lfasjjswmkupao&dl=1", "_id": "6aa19fff6ac254f5ab962c9f"}], "platforms": [{"platform": "tiktok", "accountId": {"_id": "6a6a3bf5df17280d93d66feb", "platform": "tiktok", "profileId": "6a6a3b62bbbe9621ca350a53", "displayName": "Психолог Морозова Наталья", "isActive": true, "profilePicture": "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=54c66941&x-expires=1789099200&x-signature=b0KL9dXyDlMyXJ86GqCk9b457sk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my2", "username": "natalyamorozovapsy"}, "profileId": "6a6a3b62bbbe9621ca350a53", "customMedia": [], "scheduledFor": "2026-09-09T18:05:44.685Z", "platformSpecificData": {"tiktokSettings": {"privacy_level": "PUBLIC_TO_EVERYONE", "allow_comment": true, "media_type": "photo", "photo_cover_index": 0, "description": "Вот что я замечаю в кабинете: взрослые приходят с двойной травмой, которую редко называют вслух. Дочь десятилетиями доказывает, что она «достаточно хорошая» — сдаёт экзамены, тащит отношения, подстраивается. Сын всю жизнь держит лицо любимчика и боится разочаровать, потому что его любили не за живость, а за успех рядом с мамой. Самое тяжёлое — когда понимаешь: вы не соревновались. Вы играли разные части одного семейного спектакля. Дочь отражала то, что мать в себе не приняла — право хотеть, злиться, быть видимой. Сын становился обезболивающим: пока он на пьедестале, можно не смотреть в собственную пустоту. «Может, со мной что-то не так?» — этот вопрос я слышу и от тех, кого обесценивали, и от тех, кого возводили. Но сценарий писала не детская вина — а невыносимая боль взрослой женщины, которую никто не научил удерживать самой. Это не оправдание родителю. Это освобождение для тебя. Иногда достаточно одного честного разговора с телом — не с головой — чтобы перестать автоматически сжиматься при мамином голосе или ловить себя на поиске одобрения, как будто без него ты исчезнешь. В EMDR мы не спорим с прошлым и не требуем «простить и забыть». Ищем, где нервная система до сих пор живёт в роли удобной дочери или идеального сына — и возвращаем право быть просто человеком. Подпишись, если эта тема отзывается, и запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля. #нарциссическаямать #токсичнаясемья #emdr #психологиясемьи", "auto_add_music": true, "content_preview_confirmed": true, "express_consent_given": true}}, "status": "failed", "publishAttempts": 0, "contentHash": "11ecb2c3e8411ec9eb75ec81ec7550ef", "_id": "6aa19fff6ac254f5ab962ca0", "errorCategory": "account_issue", "errorMessage": "TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, o
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

## INC-20260909-001

status: open
run_at: 2026-09-09T18:06:42.579455+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_1522_743

### Error
```
Zernio tiktok error: {'post': {'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, '_id': '6aa1a02c82a69c8c0f1c5901', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Мама может обожать сына и не выносить дочь — и при этом дело не в детях.', 'mediaItems': [{'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/dsdt623egr8kf7gt0mpvs/slide-01.png?rlkey=gowdf72zbyvjhvcq5gxvkq007&dl=1', '_id': '6aa1a02c82a69c8c0f1c5902'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/zoak5hi75s53a6lnfxrct/slide-02.png?rlkey=9jpexny7olg3hske3ycp5qjbh&dl=1', '_id': '6aa1a02c82a69c8c0f1c5903'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/5elhgl8fnaamlvkvfocpa/slide-03.png?rlkey=5h0fsr2z3f7phmbd1ptvt8txs&dl=1', '_id': '6aa1a02c82a69c8c0f1c5904'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/2b69nw832pejmftwt5yzc/slide-04.png?rlkey=2ylbuw6c35jnsxre4kst2phbx&dl=1', '_id': '6aa1a02c82a69c8c0f1c5905'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/yni5h5hb1whw1jcw8h5qf/slide-05.png?rlkey=ekkxzkokwi8wdza3a7vegjujo&dl=1', '_id': '6aa1a02c82a69c8c0f1c5906'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/uqcgsg2x8fxdayiennll1/slide-06.png?rlkey=4xstxigdba2lfasjjswmkupao&dl=1', '_id': '6aa1a02c82a69c8c0f1c5907'}], 'platforms': [{'platform': 'tiktok', 'accountId': {'_id': '6a6a3bf5df17280d93d66feb', 'platform': 'tiktok', 'profileId': '6a6a3b62bbbe9621ca350a53', 'displayName': 'Психолог Морозова Наталья', 'isActive': True, 'profilePicture': 'https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=54c66941&x-expires=1789099200&x-signature=b0KL9dXyDlMyXJ86GqCk9b457sk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my2', 'username': 'natalyamorozovapsy'}, 'profileId': '6a6a3b62bbbe9621ca350a53', 'customMedia': [], 'scheduledFor': '2026-09-09T18:06:29.880Z', 'platformSpecificData': {'tiktokSettings': {'privacy_level': 'PUBLIC_TO_EVERYONE', 'allow_comment': True, 'media_type': 'photo', 'photo_cover_index': 0, 'description': 'Вот что я замечаю в кабинете: взрослые приходят с двойной травмой, которую редко называют вслух. Дочь десятилетиями доказывает, что она «достаточно хорошая» — сдаёт экзамены, тащит отношения, подстраивается. Сын всю жизнь держит лицо любимчика и боится разочаровать, потому что его любили не за живость, а за успех рядом с мамой. Самое тяжёлое — когда понимаешь: вы не соревновались. Вы играли разные части одного семейного спектакля. Дочь отражала то, что мать в себе не приняла — право хотеть, злиться, быть видимой. Сын становился обезболивающим: пока он на пьедестале, можно не смотреть в собственную пустоту. «Может, со мной что-то не так?» — этот вопрос я слышу и от тех, кого обесценивали, и от тех, кого возводили. Но сценарий писала не детская вина — а невыносимая боль взрослой женщины, которую никто не научил удерживать самой. Это не оправдание родителю. Это освобождение для тебя. Иногда достаточно одного честного разговора с телом — не с головой — чтобы перестать автоматически сжиматься при мамином голосе или ловить себя на поиске одобрения, как будто без него ты исчезнешь. В EMDR мы не спорим с прошлым и не требуем «простить и забыть». Ищем, где нервная система до сих пор живёт в роли удобной дочери или идеального сына — и возвращаем право быть просто человеком. Подпишись, если эта тема отзывается, и запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля. #нарциссическаямать #токсичнаясемья #emdr #психологиясемьи', 'auto_add_music': True, 'content_preview_confirmed': True, 'express_consent_given': True}}, 'status': 'failed', 'publishAttempts': 0, 'contentHash': '11ecb2c3e8411ec9eb75ec81ec7550ef', '_id': '6aa1a02c82a69c8c0f1c5908', 'errorCategory': 'account_issue', 'errorMessage': 'TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator I
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
