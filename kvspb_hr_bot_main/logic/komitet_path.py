from aiogram import Router, types
from aiogram.types import FSInputFile

import texts
import logging
router = Router()

logger = logging.getLogger(__name__)
@router.callback_query(lambda msg: msg.data == texts.komitet)
async def start_instruction(callback: types.CallbackQuery):
    logger.info(f"start_instruction. user {callback.from_user.id}. data: {callback.data}")
    kb = [
        [types.InlineKeyboardButton(text="Авторизоваться", url="https://hr.gov.spb.ru/vakansii/?")],
        [types.InlineKeyboardButton(text="Я авторизовался", callback_data="auth")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)

    await callback.message.answer(
        "Для создания анкеты в комитет. Нужно зарегистрироваться или авторизоваться на сайте комитета."
        "\nПройдите пожалуйста, регистрацию или авторизацию"
        "\nЕсли вы прошли авторизацию, нажмите на кнопку 'Я авторизовался'",
        reply_markup=keyboard
    )


@router.callback_query(lambda msg: msg.data == 'auth')
async def on_auth_message(callback: types.CallbackQuery):
    logger.info(f"on_auth_message. user {callback.from_user.id}. data: {callback.data}")
    await callback.message.answer("Спасибо что зарегистрировались на сайте. Для того, чтобы откликнуться вам необходимо заполнить анкету."
                                  "Следуйте инструкция по заполнению")

    photo = FSInputFile("logic/komitet_instruct/profile.png")
    await callback.message.answer_photo(
        caption="Перейдите в свой личный кабинет выберите пункт 'Профиль'. В данном пункте, откройте графу 'Общие данные'",
        photo=photo
    )
    await callback.message.answer(
        text="""В данном окне, вам нужно заполнить все графы выделенные в красный прямоугольник"""
    )