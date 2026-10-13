# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261013-001

status: fixed
run_at: 2026-10-13T08:05:15.923770+00:00
pair: pair2
stage: publish
carousel: crsl_k3_20261013_0800_bordo_3860
fix_summary: Zernio IG reject slide-05 — PNG 1078×1348 (aspect 0.799 < 0.8), slide-06 1079×1349 mismatch. Retry slot с --pick bottom опубликовал crsl_k3_20261013_0803_typo-min_2270. Добавлена preflight validate_instagram_slides в publish_engine.
files_changed: scripts/lib/publish_slide_validate.py, scripts/lib/publish_engine.py
needs_human_factory: crsl_k3_20261013_0800_bordo_3860 — пересобрать в фабрике 1080×1350

### Error
```
Zernio instagram error: {'post': {'_id': '6acde58ae3718cbf99540638', 'userId': '6a6a3b62bbbe9621ca350a43', 'title': '', 'content': 'Твое молчание в компании — это не скромность, а старая травма.\n\nЗамечала, как это работает на уровне тела? Кто-то неудачно пошутил, и у тебя перехватывает дыхание. Кажется, будто комната стала огромной, а ты в ней — крошечной. Это не просто обида, а глубокий, животный страх изгнания из стаи. Раньше остаться одному значило погибнуть. Наш мозг до сих пор в это верит, запуская реакцию замирания, даже если собеседник просто отвел взгляд.\n\nЯ часто вижу эту картину в кабинете. Приходят взрослые люди, которые легко управляют сложными проектами, но теряются на обычном дружеском ужине. Они тратят массу энергии, чтобы судорожно сканировать лица окружающих. Понравилась ли моя шутка? Не слишком ли громко я говорю? А вдруг они решат, что я странная, и больше не позовут?\n\nПытаясь защитить себя от гипотетического отвержения, ты раз за разом отвергаешь себя сама. Добровольно выбираешь быть удобной тенью. В терапии мы не навязываем искусственную уверенность и не заставляем зубрить аффирмации. Мы идем глубже. Находим тот самый первый эпизод, когда твоя нервная система решила, что проявляться — смертельно опасно.\n\nКогда эта старая нейронная связь распадается, тебе больше не нужно мучительно контролировать каждый свой шаг и вздох. Ты просто начинаешь по-настоящему жить. Говорить громко, когда хочется сказать. И спокойно молчать только тогда, когда нечего добавить, а не от леденящего страха быть неуместной.\n\nПодпишись чтобы не потерять.\n\n#страхотвержения #emdrтерапия #социальнаятревожность #психологиятравмы #страхобщения', 'mediaItems': [{'_id': '6acde58ae3718cbf9954063a', 'url': 'https://www.dropbox.com/scl/fi/4gr9oowqmihuk40kdb2fh/slide-01.png?rlkey=07e1scz4i90iim9kmap1ckrpw&dl=1', 'type': 'image'}, {'_id': '6acde58ae3718cbf9954063b', 'url': 'https://www.dropbox.com/scl/fi/vvm7wurs0cthjw8j8hcs4/slide-02.png?rlkey=40nbu5oyz3uwu29h51x861v5a&dl=1', 'type': 'image'}, {'_id': '6acde58ae3718cbf9954063c', 'url': 'https://www.dropbox.com/scl/fi/e0unbniodw04e5maf7krz/slide-03.png?rlkey=irxj2rf00qsa0b0nmcac9npme&dl=1', 'type': 'image'}, {'_id': '6acde58ae3718cbf9954063d', 'url': 'https://www.dropbox.com/scl/fi/vo768vmc0aiq12fb8y9so/slide-04.png?rlkey=9cqolmirbo9glrrsptfrjfxt2&dl=1', 'type': 'image'}, {'_id': '6acde58ae3718cbf9954063e', 'url': 'https://www.dropbox.com/scl/fi/4ah5bniq3h4krxvep6sll/slide-05.png?rlkey=v63ixszt5ir247241eqlw71x2&dl=1', 'type': 'image'}, {'_id': '6acde58ae3718cbf9954063f', 'url': 'https://www.dropbox.com/scl/fi/p53g6ih88196f4laieyq2/slide-06.png?rlkey=zwtqp67b6d51jsybgshp2x667&dl=1', 'type': 'image'}], 'scheduledFor': '2026-10-13T08:02:11.979Z', 'timezone': 'UTC', 'status': 'failed', 'tags': [], 'hashtags': [], 'mentions': [], 'visibility': 'public', 'crosspostingEnabled': True, 'metadata': {'usageCounted': True, 'usageRefunded': True}, 'publishingClaimedAt': '2026-10-13T08:02:18.208Z', 'publishAttempts': 0, 'recycling': {'enabled': False, 'gapFreq': 'month', 'recycleCount': 0, 'contentVariations': [], 'contentVariationIndex': 0}, 'createdAt': '2026-10-13T08:02:18.063Z', 'updatedAt': '2026-10-13T08:02:30.099Z', 'platforms': [{'_id': '6acde58ae3718cbf99540637', 'platform': 'instagram', 'accountId': {'_id': '6a6a3ccadf17280d93d6828d', 'platform': 'instagram', 'username': 'natalia_morozova_psy', 'displayName': 'Морозова Наталья | Психолог', 'profilePicture': 'https://scontent-cdg4-2.cdninstagram.com/v/t51.82787-19/571653786_18063958040622853_5965052685336651068_n.jpg?stp=dst-jpg_s206x206_tt6&_nc_cat=101&ccb=7-5&_nc_sid=bf7eb4&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=fi0EFqeLteMQ7kNvwF0jsUW&_nc_oc=AdpwahcpuMyWF8Ymd2TqhmTaZLOFBPa2i4W50owkwqNNnzi0d6MZDIlgwGCJAMLC0UU&_nc_zt=24&_nc_ht=scontent-cdg4-2.cdninstagram.com&edm=AP4hL3IEAAAA&_nc_gid=xJG5580ua5x7BZsr7wKF8w&_nc_tpa=Q5bMBQLA-1PTNEdHzwISn_fZaJs3NsILDJYGNEgBC-0e5nov6mjAJhcFHPntG4ZcMW63X15NeeLBJnSM7A&oh=00_AQOLSf
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
