import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8676745042:AAGNoon6a_AyHNJmfE3sr9VmKx5IQxAQOxE"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

PRICE_ITEMS = [
    {"key": "price_dollar_rl",   "label": "💵 دلار آمریکا"},
    {"key": "price_eur",         "label": "💶 یورو"},
    {"key": "price_gbp",         "label": "💷 پوند"},
    {"key": "geram18",           "label": "🥇 طلا ۱۸ عیار (هر گرم)"},
    {"key": "sekee",             "label": "🪙 سکه امامی"},
    {"key": "sekeb",             "label": "🪙 سکه بهار آزادی"},
    {"key": "crypto-bitcoin",    "label": "₿ بیت‌کوین (دلار)"},
    {"key": "crypto-ethereum",   "label": "⟠ اتریوم (دلار)"},
    {"key": "crypto-tether",     "label": "💲 تتر (دلار)"},
]

def get_price(key):
    try:
        url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/{key}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=8)
        data = res.json()
        if data.get("data") and len(data["data"]) > 0:
            return data["data"][0].get("p", "—")
        return "—"
    except Exception:
        return "خطا"

def format_number(num_str):
    try:
        num = float(num_str.replace(",", "").strip())
        return f"{num:,.0f}" if num >= 1 else f"{num:,.4f}"
    except Exception:
        return num_str

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\nبرای دریافت آخرین قیمت‌ها از دستور /price استفاده کن."
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ در حال دریافت قیمت‌ها...")
    now = datetime.now().strftime("%H:%M:%S - %Y/%m/%d")
    lines = [f"📊 *قیمت‌های لحظه‌ای بازار*\n🕐 {now}\n"]
    for item in PRICE_ITEMS:
        raw = get_price(item["key"])
        formatted = format_number(raw) if raw not in ("—", "خطا") else raw
        lines.append(f"{item['label']}:\n  `{formatted}`\n")
    lines.append("\n_منبع: tgju.org_")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    print("✅ ربات فعال شد...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
