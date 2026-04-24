# Salytic 📊

> AI-анализ продаж для малого бизнеса. Загрузи CSV — получи инсайты за 30 секунд.

![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red?style=flat-square)
![Gemini](https://img.shields.io/badge/gemini-1.5_flash-orange?style=flat-square)

---

## Демо 

![Главный экран](screenshots/screenshot_main.png)
![AI-рекомендации](screenshots/screenshot_insights.png)

**Как выглядит:** загрузка CSV → KPI-карточки (выручка, средний чек, количество транзакций) → графики динамики и топ товаров → AI-рекомендации на русском → скачиваемый HTML-отчёт.

---

## Что умеет

- Автоопределение колонок (дата, товар, количество, сумма) — работает с любым CSV
- KPI: выручка, средний чек, количество транзакций, уникальные товары
- Динамика выручки по неделям с трендом
- Топ и аутсайдеры по выручке
- ABC-анализ ассортимента
- Продажи по дням недели
- AI-рекомендации на русском через Gemini 2.5 Flash
- Скачиваемый HTML-отчёт

---

## Стек

| |                  |
|---|------------------|
| UI | Streamlit        |
| Аналитика | pandas, numpy    |
| Графики | Plotly           |
| AI | Gemini 2.5 Flash |

---

## Структура

```
salytic/
├── app.py          # UI и роутинг
├── analyzer.py     # аналитика, ABC, тренды
├── llm.py          # Gemini API, fallback без ключа
├── report.py       # генерация HTML-отчёта
├── requirements.txt
├── .env.example    # шаблон переменных окружения
└── screenshots/           # скрины для README
```

---

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env        # создай .env и вставь ключ
streamlit run app.py
```

Ключ Gemini API — бесплатно на [aistudio.google.com](https://aistudio.google.com/apikey).

---

## Формат CSV

Колонки определяются автоматически. Нужны любые 2–4 из них:

`дата` · `товар / наименование` · `количество` · `сумма / выручка`

Поддерживаемые разделители: `,` `;` `Tab` `|`
Кодировка: UTF-8, Windows-1251, Latin-1.

## 📞 Контакт

Telegram: @flufer_20
