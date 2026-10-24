# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260909-001

status: fixed
run_at: 2026-09-09T08:06:10.784349+00:00
pair: pair2
stage: publish
carousel: crsl_20260902_0758_826
fix_summary: TikTok at capacity (transient, tiktok_capacity). IG ok @natalia_morozova_psy. tiktok_resume retry same run — still capacity. Resume on 18:00/21:00 MSK.
files_changed: scripts/lib/publish_failure.py

### Error
```
PARTIAL_IG_OK|{"post": {"recycling": {"enabled": false, "gapFreq": "month", "recycleCount": 0, "contentVariations": [], "contentVariationIndex": 0}, "_id": "6aa11371e14dc3fa6449f665", "userId": "6a6a3b62bbbe9621ca350a43", "title": "", "content": "Тревожнику нужны люди. И после людей — как после смены без выходных.", "mediaItems": [{"type": "image", "url": "https://www.dropbox.com/scl/fi/7xiiv8az452z0xrpoizx6/slide-01.png?rlkey=1e0zoj4abyh44bbbmi8hmicme&dl=1", "_id": "6aa11371e14dc3fa6449f666"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/6pt8ccb5k8fzmxbigy00p/slide-02.png?rlkey=rn70xpvrm9kilsi3r3s2nao09&dl=1", "_id": "6aa11371e14dc3fa6449f667"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/14u1hur49eul5bft7vfw0/slide-03.png?rlkey=gxc6wl2w53vv23zgyww0xfmyc&dl=1", "_id": "6aa11371e14dc3fa6449f668"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/2r8pey7qjsm5o99t0ura3/slide-04.png?rlkey=lbfdvp0e0kfjfj5cgdt8bl1cb&dl=1", "_id": "6aa11371e14dc3fa6449f669"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/3u0gri9kx9ka5wvviirsv/slide-05.png?rlkey=dhk1v0dzhya116em02fqb92wn&dl=1", "_id": "6aa11371e14dc3fa6449f66a"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/66nrg6kzly76lfe4382bc/slide-06.png?rlkey=zqyainc01s246md4aon6k4mxs&dl=1", "_id": "6aa11371e14dc3fa6449f66b"}], "platforms": [{"platform": "tiktok", "accountId": {"_id": "6a6a3bf5df17280d93d66feb", "platform": "tiktok", "profileId": "6a6a3b62bbbe9621ca350a53", "displayName": "Психолог Морозова Наталья", "isActive": true, "profilePicture": "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=54c66941&x-expires=1789099200&x-signature=b0KL9dXyDlMyXJ86GqCk9b457sk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my2", "username": "natalyamorozovapsy"}, "profileId": "6a6a3b62bbbe9621ca350a53", "customMedia": [], "scheduledFor": "2026-09-09T08:06:03.660Z", "platformSpecificData": {"tiktokSettings": {"privacy_level": "PUBLIC_TO_EVERYONE", "allow_comment": true, "media_type": "photo", "photo_cover_index": 0, "description": "Часто слышу: «Я люблю близких, но устаю от них сильнее, чем от работы». И сразу стыд — ведь «надо быть благодарным», «семья же», «я же сам выбрал встречу». Но если присмотреться — усталость не от разговора как такового. Она от того, что в контакте тело редко получает сигнал «можно выдохнуть». Психика сканирует: всё ли в порядке, не обидел ли, не сорвётся ли атмосфера. Плечи чуть подняты. Челюсть сжата. Свои чувства откладываются — «сейчас не время». Ты подстраиваешься. Сглаживаешь. Контролируешь пространство — темп, тему, тон. Аутентичные процессы как будто ставятся на паузу. И параллельно идёт невидимая работа: обслуживать чужую психику — угадывать, успокаивать, быть удобным. Это не характер «слишком чувствительного». Это хронический режим напряжения, который когда-то помогал выжить в контакте. Мозг запомнил: расслабиться = риск. Хорошая новость: контакт без истощения — не миф. Не через «меньше людей» и не через маску «мне всё равно». А через тело, границы и проработку того, где безопасность когда-то стоила постоянного контроля. В EMDR мы работаем с этим напряжением — не отрезая тебя от близости, а возвращая опору внутри неё. Запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля (morozovanatalia.ru) #тревога #психотерапия #эмдр #эмоциональноездоровье", "auto_add_music": true, "content_preview_confirmed": true, "express_consent_given": true}}, "status": "failed", "publishAttempts": 0, "contentHash": "5426af0e2094dc08ce9a890ca6b49cce", "_id": "6aa11371e14dc3fa6449f66c", "errorCategory": "account_issue", "errorMessage": "TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, or try again in a few hours as capacity frees up.", "errorSource": "user"}], "scheduledFor": "2026-09-09T08:06:03.660Z", "timezone": "UTC", "status": "failed", "tags": [],
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
run_at: 2026-09-09T08:07:24.189771+00:00
pair: pair2
stage: publish
carousel: crsl_20260902_0758_826

### Error
```
Zernio tiktok error: {'post': {'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, '_id': '6aa113b6ce147f37b6a32c93', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Тревожнику нужны люди. И после людей — как после смены без выходных.', 'mediaItems': [{'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/7xiiv8az452z0xrpoizx6/slide-01.png?rlkey=1e0zoj4abyh44bbbmi8hmicme&dl=1', '_id': '6aa113b6ce147f37b6a32c94'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/6pt8ccb5k8fzmxbigy00p/slide-02.png?rlkey=rn70xpvrm9kilsi3r3s2nao09&dl=1', '_id': '6aa113b6ce147f37b6a32c95'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/14u1hur49eul5bft7vfw0/slide-03.png?rlkey=gxc6wl2w53vv23zgyww0xfmyc&dl=1', '_id': '6aa113b6ce147f37b6a32c96'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/2r8pey7qjsm5o99t0ura3/slide-04.png?rlkey=lbfdvp0e0kfjfj5cgdt8bl1cb&dl=1', '_id': '6aa113b6ce147f37b6a32c97'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/3u0gri9kx9ka5wvviirsv/slide-05.png?rlkey=dhk1v0dzhya116em02fqb92wn&dl=1', '_id': '6aa113b6ce147f37b6a32c98'}, {'type': 'image', 'url': 'https://www.dropbox.com/scl/fi/66nrg6kzly76lfe4382bc/slide-06.png?rlkey=zqyainc01s246md4aon6k4mxs&dl=1', '_id': '6aa113b6ce147f37b6a32c99'}], 'platforms': [{'platform': 'tiktok', 'accountId': {'_id': '6a6a3bf5df17280d93d66feb', 'platform': 'tiktok', 'profileId': '6a6a3b62bbbe9621ca350a53', 'displayName': 'Психолог Морозова Наталья', 'isActive': True, 'profilePicture': 'https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=54c66941&x-expires=1789099200&x-signature=b0KL9dXyDlMyXJ86GqCk9b457sk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my2', 'username': 'natalyamorozovapsy'}, 'profileId': '6a6a3b62bbbe9621ca350a53', 'customMedia': [], 'scheduledFor': '2026-09-09T08:07:11.719Z', 'platformSpecificData': {'tiktokSettings': {'privacy_level': 'PUBLIC_TO_EVERYONE', 'allow_comment': True, 'media_type': 'photo', 'photo_cover_index': 0, 'description': 'Часто слышу: «Я люблю близких, но устаю от них сильнее, чем от работы». И сразу стыд — ведь «надо быть благодарным», «семья же», «я же сам выбрал встречу». Но если присмотреться — усталость не от разговора как такового. Она от того, что в контакте тело редко получает сигнал «можно выдохнуть». Психика сканирует: всё ли в порядке, не обидел ли, не сорвётся ли атмосфера. Плечи чуть подняты. Челюсть сжата. Свои чувства откладываются — «сейчас не время». Ты подстраиваешься. Сглаживаешь. Контролируешь пространство — темп, тему, тон. Аутентичные процессы как будто ставятся на паузу. И параллельно идёт невидимая работа: обслуживать чужую психику — угадывать, успокаивать, быть удобным. Это не характер «слишком чувствительного». Это хронический режим напряжения, который когда-то помогал выжить в контакте. Мозг запомнил: расслабиться = риск. Хорошая новость: контакт без истощения — не миф. Не через «меньше людей» и не через маску «мне всё равно». А через тело, границы и проработку того, где безопасность когда-то стоила постоянного контроля. В EMDR мы работаем с этим напряжением — не отрезая тебя от близости, а возвращая опору внутри неё. Запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля (morozovanatalia.ru) #тревога #психотерапия #эмдр #эмоциональноездоровье', 'auto_add_music': True, 'content_preview_confirmed': True, 'express_consent_given': True}}, 'status': 'failed', 'publishAttempts': 0, 'contentHash': '5426af0e2094dc08ce9a890ca6b49cce', '_id': '6aa113b6ce147f37b6a32c9a', 'errorCategory': 'account_issue', 'errorMessage': 'TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, or try again in a few hours as capacity frees up.', 'errorSource': 'user'}], 'scheduledFor': '2026-09-09T08:07:11.719Z', 'timezone': 'UTC', 'status': 'failed', 'tag
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
