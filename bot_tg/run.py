import logging, asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN

from app.handlers import router




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(router)
    

    polling = asyncio.create_task(dp.start_polling(bot))
    
    await asyncio.gather(polling)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Bot stopped')  