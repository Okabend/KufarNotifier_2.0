from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import WebhookInfo, BotCommand
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from loguru import logger
import config

telegram_router = Router(name="telegram")


class TelegramBot:
    def __init__(self, token: str, base_url: str, webhook_path: str, secret_token: str, debug: bool = False):
        self.bot = Bot(token=token, parse_mode=ParseMode.HTML)
        self.dp = Dispatcher()
        self.router = Router(name="telegram")
        self.dp.include_router(self.router)
        self.base_url = base_url
        self.webhook_path = webhook_path
        self.secret_token = secret_token
        self.debug = debug

    async def check_webhook(self) -> WebhookInfo | None:
        try:
            webhook_info = await self.bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logger.error(f"Can't get webhook info - {e}")
            return

    async def set_webhook(self) -> None:
        current_webhook_info = await self.check_webhook()
        if self.debug:
            logger.debug(f"Current bot info: {current_webhook_info}")
        try:
            await self.bot.set_webhook(
                f"{self.base_url}{self.webhook_path}",
                secret_token=self.secret_token,
                drop_pending_updates=current_webhook_info.pending_update_count > 0,
            )
            if self.debug:
                logger.debug(f"Updated bot info: {await self.check_webhook()}")
        except Exception as e:
            logger.error(f"Can't set webhook - {e}")

    async def set_bot_commands_menu(self) -> None:
        commands = [
            BotCommand(command="/id", description="👋 Get my ID"),
        ]
        try:
            await self.bot.set_my_commands(commands)
        except Exception as e:
            logger.error(f"Can't set commands - {e}")

    async def start(self):
        await self.set_webhook()
        # await self.set_bot_commands_menu()


tg_bot = TelegramBot(token=config.TG_TOKEN,
                     base_url=config.BASE_WEBHOOK_URL,
                     webhook_path=config.TG_WEBHOOK_PATH,
                     secret_token=config.TG_MY_TOKEN,
                     debug=config.DEBUG, )


# @tg_bot.router.message(Command("id"))
# async def cmd_id(message: Message) -> None:
#     await message.answer(f"Your ID: {message.from_user.id}")


@tg_bot.router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Добавить ссылки"),
            types.KeyboardButton(text="Очистить ссылки"),
            types.KeyboardButton(text="Интервал"),
            types.KeyboardButton(text="Старт")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Добавьте ссылки и укажите интервал"
    )
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}! Нажми на соответствующую кнопку и пришли ссылку на интересующий тебя товар / укажи интервал с которым мне следует присылать тебе новые объявления", reply_markup=keyboard)


@tg_bot.router.message(F.text)
async def hello(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")
