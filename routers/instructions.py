from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from typing_extensions import TypedDict

from db.hooks.custom_instructions import find_instruction, insert_instruction

instructions_router = Router(name=__name__)

set_instructions_command_name = "set_instruction"


class InstructionFormData(TypedDict):
    instruction: str


class InstructionForm(StatesGroup):
    instruction = State()


@instructions_router.message(Command("instruction"))
async def instruction_command(message: Message) -> None:
    instruction: str | None = await find_instruction(message.chat.id)
    if instruction is None:
        await message.reply(
            f"У вас нет кастомной инструкции. Чтобы создать используйте команду /{set_instructions_command_name}")
    else:
        await message.reply("<b>Сейчас я работаю по этой инструкции</b>:\n" + instruction)


@instructions_router.message(Command(set_instructions_command_name))
async def set_instructions_command(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    if message.chat.type != ChatType.PRIVATE:
        if message.from_user is None:
            return
        admins = await message.bot.get_chat_administrators(message.chat.id)
        if message.from_user.id not in [admin.user.id for admin in admins]:
            await message.answer("Это действие могут совершать только администраторы")
            return
    await state.set_state(InstructionForm.instruction)
    await message.answer(
        "В следующем сообщении пришли мне новые инструкции или отмени действие /cancel",
    )


@instructions_router.message(InstructionForm.instruction, F.text.len() != 0)
async def process_instructions(message: Message, state: FSMContext) -> None:
    await state.update_data(instruction=message.text)
    data: InstructionFormData = await state.get_data()
    await state.clear()
    print(data)
    if 'instruction' in data:
        await insert_instruction(message.chat.id, data['instruction'])
        await message.reply("Сохранено: \n" + data['instruction'])
    else:
        await message.reply("чета не получилась)))))")
