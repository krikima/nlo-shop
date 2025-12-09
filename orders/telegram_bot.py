import requests
import re
import logging

TELEGRAM_BOT_TOKEN = '8463666520:AAEjAPMy4642gIabaNZiL22aBkiCt-xJOdM'  
TELEGRAM_CHAT_ID = '1487359914'  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def escape_markdown_v2(text):
    if not text:
        return "не указан"
    # Экранируем только _
    escaped = text.replace('_', '\\_')
    return escaped

def send_order_to_admin(order):
    logger.info("📤 Начинаем отправку заказа #%s в Telegram", order.id)
    
    # Получаемimport requests
import logging

# === ТОКЕН И ЧАТ ID ===
TELEGRAM_BOT_TOKEN = '8463666520:AAEjAPMy4642gIabaNZiL22aBkiCt-xJOdM'
TELEGRAM_CHAT_ID = '1487359914'

# === ЛОГИРОВАНИЕ ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_order_to_admin(order):
    logger.info("📤 Отправка заказа #%s в Telegram", order.id)

    # Очищаем username
    username = order.telegram_username.strip().lstrip('@') if order.telegram_username else "не указан"
    username_link = f"@{username}" if username != "не указан" else "не указан"

    # Простое текстовое сообщение — НЕТ Markdown, НЕТ спецсимволов
    message = (
        "🆕 НОВЫЙ ЗАКАЗ\n"
        "\n"
        f"Номер: #{order.id}\n"
        f"Имя: {order.first_name}\n"
        f"Телефон: {order.phone}\n"
        f"Telegram: {username_link}\n"
        f"Адрес: {order.address or 'Самовывоз'}\n"
        f"Доставка: {'Доставка (+100р)' if order.delivery_type == 'delivery' else 'Самовывоз'}\n"
        "\n"
        "Состав заказа:\n"
    )

    # Добавляем товары
    for item in order.items.all():
        message += f" • {item.product.name} x{item.quantity} → {item.price}₽\n"

    # Итог
    message += f"\n"
    message += f"Сумма: {order.total_price}₽\n"
    message += f"Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
    message += f"\n"
    message += f"nlo — вейп-магазин"

    logger.info("📝 Сообщение:\n%s", message)

    # URL
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'disable_web_page_preview': True,
        'parse_mode': None  # ← ВАЖНО: НЕТ Markdown! Только обычный текст
    }

    logger.info("📡 Отправка...")

    try:
        response = requests.post(url, data=data, timeout=10)
        logger.info("📶 Статус: %s", response.status_code)
        logger.info("📩 Ответ: %s", response.text)

        if response.status_code == 200:
            logger.info("✅ УСПЕШНО ОТПРАВЛЕНО!")
            return True
        else:
            logger.error("❌ Ошибка: %s", response.status_code)
            return False

    except Exception as e:
        logger.error("🔥 Исключение: %s", str(e), exc_info=True)
        return False