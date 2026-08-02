# Подсказка: gcloud и системный proxy macOS

Если `gcloud` падает с `127.0.0.1:12334 Connection refused`:

1. Временно отключите системный proxy (Wi‑Fi → HTTP/HTTPS proxy), **или**
2. Запустите VPN/прокси-клиент, который слушает `127.0.0.1:12334`, **или**
3. Деплой с отключением proxy на время:

```bash
networksetup -setwebproxystate Wi-Fi off
networksetup -setsecurewebproxystate Wi-Fi off
./deploy/cloud-worker/setup-cloud-automation.sh
networksetup -setwebproxystate Wi-Fi on   # вернуть, если был включён
```

Скрипты deploy уже делают `unset HTTP_PROXY` — но macOS system proxy gcloud всё равно может подхватить.
