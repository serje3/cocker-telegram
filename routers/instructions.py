from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from typing_extensions import TypedDict

from db.hooks.custom_instructions import find_instruction, insert_instruction, enable_instruction, disable_instruction
from db.models import CustomInstruction

instructions_router = Router(name=__name__)

set_instruction_command_name = "set_instruction"


class InstructionFormData(TypedDict):
    instruction: str


class InstructionForm(StatesGroup):
    instruction = State()


async def allowed_to_modify(message: Message) -> bool:
    if message.chat.type != ChatType.PRIVATE:
        if message.from_user is None:
            return False
        admins = await message.bot.get_chat_administrators(message.chat.id)
        if message.from_user.id not in [admin.user.id for admin in admins]:
            await message.answer("Это действие могут совершать только администраторы")
            return False
    return True


@instructions_router.message(Command("instruction"))
async def instruction_command(message: Message) -> None:
    instruction_doc: CustomInstruction | None = await find_instruction(message.chat.id)
    if instruction_doc is None:
        await message.reply(
            f"У вас нет кастомной инструкции. Чтобы создать используйте команду /{set_instruction_command_name}")
    else:
        if instruction_doc['enabled']:
            await message.reply("<b>Сейчас я работаю по этой инструкции</b>:\n" + instruction_doc['instruction'])
        else:
            await message.reply(
                f"<b>Сейчас я работаю по дефолтной инструкции</b>.\nНо в этом чате также указана кастомная, "
                f"которая сейчас неактивна: \n{instruction_doc['instruction']}")


@instructions_router.message(Command("instruction_enable"))
async def instruction_enable(message: Message) -> None:
    if not allowed_to_modify(message):
        return
    instruction_doc: CustomInstruction | None = await find_instruction(message.chat.id)
    if instruction_doc is None:
        await message.reply("У вас не указана инструкция")
        return

    await enable_instruction(message.chat.id)
    await message.reply("<b>Теперь используется кастомная инструкция</b>")


@instructions_router.message(Command("instruction_disable"))
async def instruction_disable(message: Message) -> None:
    if not allowed_to_modify(message):
        return
    instruction_doc: CustomInstruction | None = await find_instruction(message.chat.id)
    if instruction_doc is None:
        await message.reply("У вас не указана инструкция")
        return

    await disable_instruction(message.chat.id)
    await message.reply("<b>Кастомная инструкция отключена. Используется по умолчанию</b>")


@instructions_router.message(Command(set_instruction_command_name))
async def set_instruction_command(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    if not allowed_to_modify(message):
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
