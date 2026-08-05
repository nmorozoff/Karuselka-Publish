# Секреты karuselka-publish

Не коммитить `*.env.local`.

## Шаблоны

```bash
cp publish-memory/airtable.env.example publish-memory/airtable.env.local
cp publish-memory/dropbox.env.example publish-memory/dropbox.env.local
cp publish-memory/zernio.env.example publish-memory/zernio.env.local
cp publish-memory/max.env.example publish-memory/max.env.local
```

## Symlink с фабрики (локальная разработка)

```bash
FACTORY="../../КАРУСЕЛЬКА/carusel-memory"
for f in airtable dropbox zernio cloud-worker; do
  ln -sf "$FACTORY/${f}.env.local" "publish-memory/${f}.env.local"
done
ln -sf "../../Посты EMDR/posts-emdr-memory/max.env.local" publish-memory/max.env.local
```

## accounts-pairs.json

Копия в `publish-memory/accounts-pairs.json`. При изменении пар в фабрике — синхронизировать вручную или symlink:

```bash
ln -sf ../../КАРУСЕЛЬКА/carusel-memory/publish/accounts-pairs.json publish-memory/accounts-pairs.json
```

## Cursor Cloud Automations

Runtime Secrets в [Cursor Dashboard](https://cursor.com/dashboard/cloud-agents) — см. `deploy/cursor-automation/CLOUD-SECRETS.md`.
