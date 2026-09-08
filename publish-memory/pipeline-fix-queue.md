# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260908-001

status: fixed
run_at: 2026-09-08T18:07:44.113752+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_1254_708
fix_summary: Instagram ✅ @natalia_morozova_psy. TikTok capacity (transient) — добавлен классификатор tiktok_capacity, улучшен отчёт Макс для PARTIAL_IG_OK. Retry: --tiktok-only --name crsl_20260908_1254_708
files_changed:
- scripts/lib/publish_failure.py
- scripts/lib/publish_engine.py

### Error
```
PARTIAL_IG_OK|{"post": {"recycling": {"enabled": false, "gapFreq": "month", "recycleCount": 0, "contentVariations": [], "contentVariationIndex": 0}, "_id": "6aa04eefcd6dbcbc1dc8800f", "userId": "6a6a3b62bbbe9621ca350a43", "title": "", "content": "Мама может обожать сына и не выносить дочь — и при этом дело не в детях.", "mediaItems": [{"type": "image", "url": "https://www.dropbox.com/scl/fi/cukzdcb43nmyvlqhk7fv3/slide-01.png?rlkey=slbdyr33ok5akpe3ls7wbz6ck&dl=1", "_id": "6aa04eefcd6dbcbc1dc88010"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/113uw81jh5kapatst9446/slide-02.png?rlkey=9cusn7frzxlnw63xjfts9hkqx&dl=1", "_id": "6aa04eefcd6dbcbc1dc88011"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/vi8m4wjmyegtxhfr1nn9r/slide-03.png?rlkey=ejseppjez4ezmq9ycl42x07m2&dl=1", "_id": "6aa04eefcd6dbcbc1dc88012"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/mclm3jw3bhuyj35vjf5vf/slide-04.png?rlkey=95p3jxc3s939cuor9ebbge5w6&dl=1", "_id": "6aa04eefcd6dbcbc1dc88013"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/zc5ftb587f8jhtmd6cefk/slide-05.png?rlkey=yvdflqmwvovq8mnh2b9cncq6o&dl=1", "_id": "6aa04eefcd6dbcbc1dc88014"}, {"type": "image", "url": "https://www.dropbox.com/scl/fi/hy7l9gnv7bhcahwxnvamc/slide-06.png?rlkey=r4cn2d8agn258el91qgdrjitu&dl=1", "_id": "6aa04eefcd6dbcbc1dc88015"}], "platforms": [{"platform": "tiktok", "accountId": {"_id": "6a6a3bf5df17280d93d66feb", "platform": "tiktok", "profileId": "6a6a3b62bbbe9621ca350a53", "displayName": "Психолог Морозова Наталья", "isActive": true, "profilePicture": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/102c44d2c5d9b8e1b8cca31730339b55~tplv-tiktokx-cropcenter:168:168.jpeg?dr=14577&refresh_token=faec7e55&x-expires=1789012800&x-signature=LCEdAVVK4keWTtFTKdTQSnPDhsU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=8aecc5ac&idc=my", "username": "natalyamorozovapsy"}, "profileId": "6a6a3b62bbbe9621ca350a53", "customMedia": [], "scheduledFor": "2026-09-08T18:07:36.602Z", "platformSpecificData": {"tiktokSettings": {"privacy_level": "PUBLIC_TO_EVERYONE", "allow_comment": true, "media_type": "photo", "photo_cover_index": 0, "description": "Вот что я замечаю в кабинете: взрослые приходят с двойной травмой, которую редко называют вслух. Дочь десятилетиями доказывает, что она «достаточно хорошая» — сдаёт экзамены, тащит отношения, подстраивается. Сын всю жизнь держит лицо любимчика и боится разочаровать, потому что его любили не за живость, а за успех рядом с мамой. Самое тяжёлое — когда понимаешь: вы не соревновались. Вы играли разные части одного семейного спектакля. Дочь отражала то, что мать в себе не приняла — право хотеть, злиться, быть видимой. Сын становился обезболивающим: пока он на пьедестале, можно не смотреть в собственную пустоту. «Может, со мной что-то не так?» — этот вопрос я слышу и от тех, кого обесценивали, и от тех, кого возводили. Но сценарий писала не детская вина — а невыносимая боль взрослой женщины, которую никто не научил удерживать самой. Это не оправдание родителю. Это освобождение для тебя. Иногда достаточно одного честного разговора с телом — не с головой — чтобы перестать автоматически сжиматься при мамином голосе или ловить себя на поиске одобрения, как будто без него ты исчезнешь. В EMDR мы не спорим с прошлым и не требуем «простить и забыть». Ищем, где нервная система до сих пор живёт в роли удобной дочери или идеального сына — и возвращаем право быть просто человеком. Подпишись, если эта тема отзывается, и запишись на бесплатную пробную сессию 30 минут — ссылка в шапке профиля. #нарциссическаямать #токсичнаясемья #emdr #психологиясемьи", "auto_add_music": true, "content_preview_confirmed": true, "express_consent_given": true}}, "status": "failed", "publishAttempts": 0, "contentHash": "c889b924ec53f457780cada67e39baef", "_id": "6aa04eefcd6dbcbc1dc88016", "errorCategory": "account_issue", "errorMessage": "TikTok direct posting is at capacity right now. Use tiktokSettings.draft: true to deliver via Creator Inbox, or
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
