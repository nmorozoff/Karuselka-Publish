# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260902-001

status: fixed
fix_summary: TikTok capacity (transient) — IG ok, tiktok_resume retry succeeded, cleanup ok
files_changed: scripts/lib/publish_failure.py, scripts/publish_incident.py
run_at: 2026-09-02T08:06:56.029108+00:00
pair: pair2
stage: publish
carousel: crsl_20260902_0757_284

### Error
```
PARTIAL_IG_OK|{"post": {"recycling": {"enabled": false, "gapFreq": "month", "recycleCount": 0, "contentVariations": [], "contentVariationIndex": 0}, "_id": "6a97d91e173001b343d5c083", "userId": "6a6a3b62bbbe9621ca350a43", "title": "", "content": "Тревожнику нужны люди. И после людей — как после смены без выходных.", "mediaItems": [{"type": "image", "url": "https://www.dropbox.com/scl/fi/2810cgst9qbvq5ble381j/slide-01.png?rlkey=3485g5bshrohxyykv1nityu75&dl=1", "_id": "6a97d91e173001b343d5c084"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/9usrfv5mkvzfc164emdq2/slide-02.png?rlkey=l7ctsbnqzgiq549hf1laiogn5&dl=1", "_id": "6a97d91e173001b343d5c085"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/p61tt3gnjxjcd5tofxcag/slide-03.png?rlkey=e18wtjk5ns9efipwz27iqq8dl&dl=1", "_id": "6a97d91e173001b343d5c086"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/x7jcyd611d7n41nwr9yso/slide-04.png?rlkey=agzfyjvabl0li0euqsib3duyn&dl=1", "_id": "6a97d91e173001b343d5c087"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/q8v0qs13d05dsmaem07dw/slide-05.png?rlkey=lt8lkhvuxketdtl95p4ifm8zg&dl=1", "_id": "6a97d91e173001b343d5c088"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/6qhcw2ggkwyakz3ae78t9/slide-06.png?rlkey=w2vvfkqao0v905wakr06ahlhi&dl=1", "_id": "6a97d91e173001b343d5c089"}], "platforms": [{"platform": "tiktok", "accountId": {"_id": "6a6a3bf5df17280d93d66feb", "platform": "tiktok", "profileId": "6a6a3b62bbbe9621ca350a53", "displayName": "Психолог Морозова Наталья", "isActive": true, "profilePicture": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=d21f5c22&x-expires=1788494400&x-signature=n1uTZaQKJe0F5Cuvduj87ApRTG4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=sg1", "username": "natalyamorozovapsy"}, "profileId": "6a6a3b62bbbe9621ca350a53", "customMedia": [], "scheduledFor": "2026-09-02T08:06:49.180Z", "platformSpecificData": {"tiktokSettings": {"privacy_level": "PUBLIC_TO_EVERYONE", "allow_comment": true, "media_type": "photo", "photo_cover_index": 0, "description": "Часто слышу: «Я люблю близких, но устаю от них сильнее, чем от работы». И сразу стыд — ведь «надо быть благодарным», «семья же», «я же сам выбрал встречу». Но если присмотреться — усталость не от разговора как такового. Она от того, что в контакте тело редко получает сигнал «можно выдохнуть». Психика сканирует: всё ли в порядке, не обидел ли, не сорвётся ли атмосфера. Плечи чуть подняты. Челюсть сжата. Свои чувства откладываются — «сейчас не время». Ты подстраиваешься. Сглаживаешь. Контролируешь пространство — темп, тему, тон. Аутентичные процессы как будто ставятся на паузу. И параллельно идёт невидимая работа: обслуживать чужую психику — угадывать, успокаивать, быть удобным. Это не характер «слишком чувствительного». Это хронический режим напряжения, который когда-то помогал выжить в контакте. Мозг запомнил: расслабиться = риск. Хорошая новость: контакт без истощения — не миф. Не через «меньше людей» и не через маску «мне всё равно». А через тело, границы и проработку того, где безопасность когда-то стоила постоянного контроля. В EMDR мы работаем с этим напряжением — не отрезая тебя от близости, а возвращая опору внутри неё. Запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля (morozovanatalia.ru) #тревога #психотерапия #эмдр #эмоциональноездоровье", "auto_add_music": true, "content_preview_confirmed": true, "express_consent_given": true}}, "status": "failed", "publishAttempts": 0, "contentHash": "4290b898bad07618c75571785821a5e9", "_id": "6a97d91e173001b343d5c08a", "errorCategory": "account_issue", "errorMessage": "TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, or try again in a few hours as capacity frees up.", "errorSource": "user"}], "scheduledFor": "2026-09-02T08:06:49.180Z", "timezone": "UTC", "status": "failed", "tags": [],
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
