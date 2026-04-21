import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


def generate_insights(stats: dict) -> list[dict]:
    """
    Генерирует список инсайтов через Gemini API.
    Возвращает список dict: [{"title": ..., "text": ..., "type": "positive"|"warning"|"neutral"}]
    """
    if not GEMINI_API_KEY:
        return _fallback_insights(stats)

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Подготовка контекста
        context = _build_context(stats)

        prompt = f"""Ты опытный бизнес-аналитик. Проанализируй данные о продажах и дай конкретные рекомендации владельцу малого бизнеса на русском языке.

Данные:
{context}

Верни ТОЛЬКО JSON-массив (без markdown, без пояснений) из 5-7 инсайтов в формате:
[
  {{
    "title": "Короткий заголовок (до 8 слов)",
    "text": "Подробное объяснение и конкретная рекомендация (2-3 предложения)",
    "type": "positive" | "warning" | "neutral"
  }}
]

Будь конкретным: называй товары по именам, указывай проценты, давай actionable советы."""

        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Убираем markdown-обёртку если есть
        raw = raw.replace("```json", "").replace("```", "").strip()
        insights = json.loads(raw)
        return insights

    except Exception as e:
        print(f"LLM error: {e}")
        return _fallback_insights(stats)


def _build_context(stats: dict) -> str:
    lines = []

    lines.append(f"Общая выручка: {stats.get('total_revenue', 0):,.0f} руб")
    lines.append(f"Всего транзакций: {stats.get('total_orders', 0)}")
    lines.append(f"Уникальных товаров/категорий: {stats.get('unique_products', 0)}")
    lines.append(f"Средний чек: {stats.get('avg_order', 0):,.0f} руб")

    if stats.get("trend_pct") is not None:
        trend = stats["trend_pct"]
        direction = "вырос" if trend > 0 else "упал"
        lines.append(f"Тренд: выручка {direction} на {abs(trend):.1f}% (вторая половина периода vs первая)")

    if stats.get("best_product"):
        lines.append(f"Лучший товар: {stats['best_product']} ({stats.get('best_product_revenue', 0):,.0f} руб)")
    if stats.get("worst_product"):
        lines.append(f"Худший товар: {stats['worst_product']} ({stats.get('worst_product_revenue', 0):,.0f} руб)")

    if stats.get("best_weekday"):
        lines.append(f"Лучший день недели: {stats['best_weekday']}")
    if stats.get("worst_weekday"):
        lines.append(f"Худший день недели: {stats['worst_weekday']}")

    if stats.get("abc_a"):
        lines.append(f"Товары группы A (80% выручки): {', '.join(stats['abc_a'][:5])}")
    if stats.get("abc_c"):
        lines.append(f"Товары группы C (хвост, кандидаты на вывод): {', '.join(stats['abc_c'][:5])}")

    if stats.get("anomaly_days", 0) > 0:
        lines.append(f"Дней с аномально высокими продажами: {stats['anomaly_days']}")

    return "\n".join(lines)


def _fallback_insights(stats: dict) -> list[dict]:
    """Базовые инсайты без LLM — на случай отсутствия API ключа."""
    insights = []

    # Тренд
    trend = stats.get("trend_pct", 0)
    if trend > 10:
        insights.append({
            "title": "Выручка растёт",
            "text": f"Вторая половина периода принесла на {trend:.0f}% больше чем первая. Хороший сигнал — продолжай в том же духе и анализируй что изменилось.",
            "type": "positive"
        })
    elif trend < -10:
        insights.append({
            "title": "Выручка падает",
            "text": f"Вторая половина периода принесла на {abs(trend):.0f}% меньше чем первая. Стоит разобраться в причинах — сезонность, ассортимент или внешние факторы.",
            "type": "warning"
        })

    # Лучший/худший товар
    if stats.get("best_product"):
        insights.append({
            "title": f"Локомотив продаж — {stats['best_product']}",
            "text": f"Этот товар приносит наибольшую выручку. Убедись что он всегда в наличии, рассмотри расширение линейки на его основе.",
            "type": "positive"
        })

    if stats.get("worst_product") and stats.get("worst_product_revenue", 0) > 0:
        insights.append({
            "title": f"Аутсайдер — {stats['worst_product']}",
            "text": f"Этот товар приносит минимальную выручку ({stats['worst_product_revenue']:,.0f} руб). Оцени: стоит ли держать его в ассортименте или лучше заменить?",
            "type": "warning"
        })

    # ABC
    if stats.get("abc_c"):
        insights.append({
            "title": "Кандидаты на вывод из ассортимента",
            "text": f"Товары {', '.join(stats['abc_c'][:3])} вносят минимальный вклад в выручку. Они занимают место и отвлекают внимание. Рассмотри их замену.",
            "type": "warning"
        })

    # Дни недели
    if stats.get("best_weekday") and stats.get("worst_weekday"):
        insights.append({
            "title": f"Лучший день — {stats['best_weekday']}, худший — {stats['worst_weekday']}",
            "text": f"Планируй акции и запасы под пиковые дни. В {stats['worst_weekday']} попробуй специальные предложения чтобы поднять выручку.",
            "type": "neutral"
        })

    if not insights:
        insights.append({
            "title": "Анализ завершён",
            "text": f"Обработано {stats.get('total_orders', 0)} транзакций. Добавь GEMINI_API_KEY в переменные окружения чтобы получить AI-рекомендации.",
            "type": "neutral"
        })

    return insights