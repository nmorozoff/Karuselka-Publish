# Аналитическая справка: фабрика Каруселька → Publish без failed

Документ для репозитория **Karuselka-emdr** / плагин `carusel`.  
Цель: устранить повторяющиеся причины `failed` в `karuselka-publish` (35 инцидентов на 10.08.2026).

## 1. Сводка инцидентов (август 2026)

| Категория | Кол-во | Retry? | Ответственность |
|-----------|--------|--------|-----------------|
| `instagram_format` (aspect 0.75) | 6 | ❌ | **Фабрика** — размер слайдов |
| `rate_limit` (Zernio 429) | 8 | ✅ | Publish — 1 карусель/run, пауза IG→TT |
| `tiktok_spam` | 4 | ❌ | **Фабрика** — тексты TikTok |
| `bad_request` (HTTP 400) | ~15 | ❌ | Фабрика + legacy бандлы |
| `tiktok_url_ownership` | 1+ | ❌ | **Ручная** — TikTok Developer Portal |
| `transient` | 2 | ✅ | Publish retry |

**Главный блокер фабрики:** PNG **3:4 (0.75)** не проходят Instagram Carousel API через Zernio.

## 2. Обязательный формат слайдов

### Instagram (через Zernio mixed carousel)

| Параметр | Требование | Сейчас (ошибка) |
|----------|------------|-----------------|
| Соотношение сторон PNG | **4:5 … 1.91:1** (Meta Carousel) | 3:4 = **0.75** → reject |
| Рекомендуемый размер | **1080×1350 px** (4:5) | 1080×1440 (3:4 Kie grid) |
| Альтернатива | 1080×1080 (1:1) | — |
| Количество PNG | **6** (`slide-01` … `slide-06`) | OK |
| Hook | `slide-01.mp4` (5s loop) | OK |
| Mixed IG | video `slide-01.mp4` + images `slide-02..06.png` | OK |

**Действие в фабрике:** после slice из Kie 3×3 master — **ресайз каждого PNG в 1080×1350** (crop/pad из 3:4 без искажения текста) **до** `export_publish_bundle.py`.

### TikTok (photo carousel)

| Параметр | Требование |
|----------|------------|
| Слайды | все **6 PNG** (`slide-01..06`) |
| Видео hook | **не отправляется** в TikTok |
| Заголовок | `TikTok заголовок` ≤ **90** символов |
| Описание | `TikTok описание`, без spam-триггеров |
| auto_add_music | true (на стороне publish) |

### Проверка перед export

```bash
# В Karuselka-emdr после slice, до export:
python scripts/validate_publish_slides.py carusel-memory/output/slides/
# Ожидание: PASS, aspect 0.8–1.91, 6 PNG, optional slide-01.mp4
```

Минимальная логика валидатора (добавить в фабрику):

```python
from PIL import Image
MIN_RATIO, MAX_RATIO = 0.8, 1.91  # width/height
for path in slides:
    w, h = Image.open(path).size
    ratio = w / h
    assert MIN_RATIO <= ratio <= MAX_RATIO, f"{path}: ratio {ratio:.2f}"
```

## 3. Airtable — поля без 422

| Поле | Правило |
|------|---------|
| `Name` | `crsl_YYYYMMDD_HHMM_XXX` — совпадает с папкой Dropbox |
| `Описание карусели` | IG caption, ≤2200 символов |
| `TikTok заголовок` | ≤90 символов, без CAPS-spam, без «подпишись/лайк/переходи» пачками |
| `TikTok описание` | нейтральный тон, без повторов хештегов |
| `Dropbox Path` | **не заполнять** при create (422); publish резолвит путь сам |

## 4. Dropbox bundle

```
/Content_Plan/Pair{N}/{Name}/
  slide-01.mp4      # hook IG
  slide-01.png … slide-06.png
  caption.txt       # справочно
  manifest.json     # контракт export
```

`manifest.json`:

```json
{
  "name": "crsl_20260810_1200_001",
  "slides": 6,
  "image_size": [1080, 1350],
  "aspect_ratio": "4:5",
  "publish": {
    "instagram": { "mode": "mixed", "slide1": "slide-01.mp4", "slides2n": "slide-02..06.png" },
    "tiktok": { "mode": "photo_carousel", "slides": "slide-01..06.png" }
  }
}
```

## 5. TikTok spam — правила копирайта

Отклонения `user_abuse` / content guidelines (4 карусели):

- Не дублировать один и тот же CTA на заголовке и описании.
- Избегать: «ЖМИ», «ПОДПИШИСЬ СЕЙЧАС», цепочки эмодзи, медицинские обещания «100% излечение».
- Один хук — одна мысль; описание раскрывает, не кричит.
- **Checklist copywriter:** `tiktok_title_len ≤ 90`, `tiktok_spam_lint: pass` перед export.

## 6. TikTok URL ownership (pair2+)

Ошибка: `URL ownership not verified in TikTok developer portal`.

**Не фабрика.** В [TikTok Developer Portal](https://developers.tiktok.com/) для приложения Zernio:

1. Verify domain для хоста **Dropbox shared links** (или CDN, если Zernio проксирует media).
2. После верификации — retry одной карусели:  
   `publish_worker.py --pair pair2 --name crsl_... --retry-failed --tiktok-only`

**Важно:** `manage_failed_queue.py reconcile` **не удаляет** `tiktok_url_ownership` — только снимает блокировку вручную после fix портала.

## 7. Rate limit 429 — не фабрика

Причина: несколько каруселей и IG+TT без паузы в одном automation run.

**Уже в publish (Aug 2026):**

- `ZERNIO_PLATFORM_GAP_SEC=45` между IG и TT
- `ZERNIO_POST_RETRIES=3`, backoff 90s
- Automation: **limit 1**, не `--retry-failed` пачкой при 429

## 8. Legacy / bad_request 400

Карусели `crsl_202606*` и бандлы без 6 валидных слайдов — **не retry**, purge из очереди.

Причины 400:

- битый payload (старый формат);
- невалидные shared URLs;
- отсутствие файлов в Dropbox.

**Gate export:** не писать в Airtable, если `validate_publish_slides.py` ≠ PASS.

## 9. Чеклист фабрики перед Airtable

- [ ] 6 PNG, каждый **1080×1350** (или 1080×1080), ratio 0.8–1.91
- [ ] `slide-01.mp4` существует, 5s, вертикаль
- [ ] `manifest.json` с `image_size` и `aspect_ratio`
- [ ] TikTok заголовок ≤90, spam-lint pass
- [ ] Папка `Pair1|2|3` соответствует аккаунту
- [ ] Dry-run publish: `publish_worker.py --pair pairN --name ... --dry-run` → 6 images, hook ok

## 10. Связь с publish-репозиторием

| Артефакт publish | Назначение |
|------------------|------------|
| `shared/queue-contract.md` | контракт полей и путей |
| `scripts/manage_failed_queue.py reconcile` | purge junk + unlock retryable |
| `scripts/lib/publish_failure.py` | категории failed |
| `deploy/cursor-automation/instructions/pair*.txt` | 1 карусель/run |

---

**Версия:** 2026-08-10  
**Источник данных:** worker-state Dropbox, 35 failed, логи Zernio automations 03–10.08.2026
