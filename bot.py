import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

# ===== توکن ربات خودت رو اینجا بذار =====
BOT_TOKEN = "8676745042:AAGNoon6a_AyHNJmfE3sr9VmKx5IQxAQOxE"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# آیتم‌هایی که می‌خوایم نمایش بدیم
PRICE_ITEMS = [
    {"key": "price_dollar_rl",   "label": "💵 دلار آمریکا"},
    {"key": "price_eur",         "label": "💶 یورو"},
    {"key": "price_gbp",         "label": "💷 پوند"},
    {"key": "geram18",           "label": "🥇 طلا ۱۸ عیار (هر گرم)"},
    {"key": "sekee",             "label": "🪙 سکه امامی"},
    {"key": "sekeb",             "label": "🪙 سکه بهار آزادی"},
    {"key": "oil",               "label": "🛢️ نفت برنت (دلار)"},
    {"key": "crypto-bitcoin",    "label": "₿ بیت‌کوین (دلار)"},
    {"key": "crypto-ethereum",   "label": "⟠ اتریوم (دلار)"},
    {"key": "crypto-tether",     "label": "💲 تتر (دلار)"},
]

def get_price(key: str) -> str:
    """دریافت قیمت از API سایت tgju"""
    try:
        url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/{key}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=8)
        data = res.json()

        if data.get("data") and len(data["data"]) > 0:
            row = data["data"][0]
            price = row.get("p", "—")
            return price
        return "—"
    except Exception:
        return "خطا"


def format_number(num_str: str) -> str:
    """اضافه کردن جداکننده هزارگان به عدد"""
    try:
        num_str = num_str.replace(",", "").strip()
        num = float(num_str)
        if num >= 1:
            return f"{num:,.0f}"
        else:
            return f"{num:,.4f}"
    except Exception:
        return num_str


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر دستور /start"""
    await update.message.reply_text(
        "سلام! 👋\nبرای دریافت آخرین قیمت‌ها از دستور /price استفاده کن."
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر دستور /price - اعلام قیمت‌ها"""
    await update.message.reply_text("⏳ در حال دریافت قیمت‌ها...")

    now = datetime.now().strftime("%H:%M:%S - %Y/%m/%d")
    lines = [f"📊 *قیمت‌های لحظه‌ای بازار*\n🕐 {now}\n"]

    for item in PRICE_ITEMS:
        raw = get_price(item["key"])
        formatted = format_number(raw) if raw not in ("—", "خطا") else raw
        lines.append(f"{item['label']}:\n  `{formatted}` تومان\n")

    lines.append("\n_منبع: tgju.org_")
    message = "\n".join(lines)

    await update.message.reply_text(message, parse_mode="Markdown")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    print("✅ ربات فعال شد...")
    app.run_polling()


if __name__ == "__main__":
    main()
