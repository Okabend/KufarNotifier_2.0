from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import WebhookInfo, BotCommand
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from loguru import logger
import config


class KufarSearch(StatesGroup):
    setting_links = State()
    setting_interval = State()


class TelegramBot:
    def __init__(self, token: str, base_url: str, webhook_path: str, secret_token: str, debug: bool = False):
        self.bot = Bot(token=token, parse_mode=ParseMode.HTML)
        self.dp = Dispatcher(storage=MemoryStorage())
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


@tg_bot.router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Добавить ссылки"),
            types.KeyboardButton(text="Очистить ссылки")
        ],
        [
            types.KeyboardButton(text="Интервал"),
            types.KeyboardButton(text="Старт")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="Добавьте ссылки и укажите интервал"
    )
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}! Нажми на соответствующую кнопку и пришли ссылку на интересующий тебя товар / укажи интервал с которым мне следует присылать тебе новые объявления",
        reply_markup=keyboard)


@tg_bot.router.message(F.text == "Добавить ссылки")
async def hello(message: types.Message, state: FSMContext) -> None:
    try:
        await message.answer(text="Пришли мне ссылки и заметки к ним, резделяя их двойным двоеточием. Например так:\n"
                                  "товар 1::ссылка, товар 2::ссылка")
        await state.set_state(KufarSearch.setting_links)  # Устанавливаем пользователю состояние "устанавливает ссылки"

    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Что-то пошло не так, попробуйте ещё раз")


def check_links_format(links: str):
    parsed_links_dict = {}
    try:
        if links.find(','):
            separated_links = links.split(',')
            for link in separated_links:
                parsed_link = link.split('::')
                parsed_links_dict[parsed_link[0]] = parsed_link[1]

        else:
            parsed_link = links.split('::')
            parsed_links_dict[parsed_link[0]] = parsed_link[1]
    except Exception as e:
        logger.error(f"Can't parse links - {e}")
        return {}
    return parsed_links_dict


@tg_bot.router.message(KufarSearch.setting_links, F.text)
async def set_links(message: Message, state: FSMContext):
    if parsed_links_dict := check_links_format(message.text):
        logger.debug(parsed_links_dict)
        await message.answer(text="Вы успешно добавили ссылки")

    else:
        await message.answer(text="Ссылки не добавлены. Неверный формат!")
    await state.clear()


@tg_bot.router.message(F.text == "Очистить ссылки")
async def reset_links(message: Message, state: FSMContext):
    try:
        await message.answer(text="Список ссылок был успешно очищен")
    except Exception as e:
        logger.error(f"Can't send message - {e}")


@tg_bot.router.message(F.text == "Интервал")
async def set_interval(message: types.Message, state: FSMContext) -> None:
    try:
        await message.answer(text="Напиши с каким интервалом тебе присылать новые объявления (в секундах)")
        await state.set_state(KufarSearch.setting_interval)

    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Что-то пошло не так, попробуйте ещё раз")


@tg_bot.router.message(KufarSearch.setting_interval, F.text)
async def unset_interval(message: Message, state: FSMContext):
    if message.text.isdecimal() and int(message.text) > 0:
        await message.answer(text=f"Интервал установлен: {hbold(message.text)} секунд")
    else:
        await message.answer(text="Число секунд указано не верно")
    await state.clear()


@tg_bot.router.message(F.text == "Старт")
async def start(message: Message):
    try:
        await message.answer(text=hbold("Процесс поиска запущен"))
    except Exception as e:
        logger.error(f"Can't send message - {e}")
