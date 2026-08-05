Karuselka Publish — ручная настройка 9 Cursor Automations

1. Cursor → Automations → New automation (или редактируй существующую)

2. Общие поля (все 9 одинаково):
   Repository: nmorozoff/Karuselka-Publish
   Branch: main
   Compute: Cloud Agent
   Memory: Off

3. Расписание — см. instructions/SCHEDULE.txt

4. Agents Instruction — открой instructions/pair1.txt или pair2.txt или pair3.txt
   Скопируй ВЕСЬ файл целиком в поле Agents Instruction.
   Для одной пары текст одинаковый во всех трех слотах.

5. После изменений в репозитории пересобери:
   python3 deploy/cursor-automation/build-workflows.py

Файлы:
  instructions/SCHEDULE.txt  — cron и имена jobs
  instructions/pair1.txt     — промпт pair1
  instructions/pair2.txt     — промпт pair2
  instructions/pair3.txt     — промпт pair3

JSON workflows/ — только для машинного prefill, для руки не нужен.
