import os
import ptbot
import pytimeparse
from dotenv import load_dotenv


load_dotenv()

TG_TOKEN = os.getenv('TELEGRAM_TOKEN')


def render_progressbar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f'{prefix} |{pbar}| {percent}% {suffix}'


def handle_message(chat_id, message):
    try:
        seconds = pytimeparse.parse(message.lower())
        if not seconds:
            raise ValueError(
                "Неверный формат времени. Пример: 5s, 1m, 2h30m"
            )

        progress = render_progressbar(
            seconds, 0, prefix='Прогресс', suffix='⌛'
        )
        message_text = (
            f"Таймер на {seconds} секунд\n\n"
            f"{progress}\n\n"
            f"Осталось: {seconds} сек."
        )
        message_id = bot.send_message(chat_id, message_text)

        bot.create_countdown(
            seconds,
            update_countdown,
            chat_id=chat_id,
            message_id=message_id,
            total_seconds=seconds
        )

        bot.create_timer(seconds, notify_end, chat_id=chat_id)

    except Exception as e:
        bot.send_message(chat_id, f"Ошибка: {str(e)}")


def update_countdown(secs_left, chat_id, message_id, total_seconds):
    elapsed = total_seconds - secs_left
    progress = render_progressbar(
        total_seconds, elapsed, prefix='Прогресс', suffix='⌛'
    )
    message_text = (
        f"Таймер на {total_seconds} секунд\n\n"
        f"{progress}\n\n"
        f"Осталось: {secs_left} сек."
    )
    bot.update_message(chat_id, message_id, message_text)


def notify_end(chat_id):
    bot.send_message(chat_id, "Время вышло!")


def main():
    global bot
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(handle_message)
    bot.run_bot()


if __name__ == '__main__':
    main()
