import logging, asyncio
from aiogram import Bot, Dispatcher, Router
from app.handlers import router
from config import TOKEN
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import State, StatesGroup
from app.handlers import userReg
from app.bot_instance import bot, dp







logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = bot
dp =dp
router1 = Router()


    








async def main():
    dp.include_routers(router, router1)
    

    polling = asyncio.create_task(dp.start_polling(bot))
    
    await asyncio.gather(polling)

# @router1.callback_query(userReg.sending_file, ContentType.DOCUMENT)
# async def waiting_file(call: CallbackQuery, state: FSMContext):
#     try:
        

#         file_info = await bot.get_file(call.message.document.file_id)
#         downloaded_file = await bot.download_file(file_info.file_path)

#         src = 'software:/home' + call.message.document.file_name;
#         async with open(src, 'wb') as new_file:
#             new_file.write(downloaded_file)
#         await state.clear()
#         await call.message.answer("Происходит обработка файла, пожалуйста подождите")
#     except Exception as e:
#         bot.reply_to(call.message, e)

if __name__ == '__main__':
    try:

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Bot stopped')  