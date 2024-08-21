from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from typing_extensions import TypedDict

from db.hooks.custom_instructions import find_instruction, insert_instruction

instructions_router = Router(name=__name__)

set_instructions_command_name = "set_instructions"


class InstructionFormData(TypedDict):
    instruction: str


class InstructionForm(StatesGroup):
    instructions = State()


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
    await state.set_state(InstructionForm.instructions)
    await message.answer(
        "В следующем сообщении пришли мне новые инструкции или отмени действие /cancel",
    )


@instructions_router.message(InstructionForm.instructions, F.text.len() != 0)
async def process_instructions(message: Message, state: FSMContext) -> None:
    await state.update_data(instructions=message.text)
    data: InstructionFormData = await state.get_data()
    await state.clear()

    await insert_instruction(message.chat.id, data['instruction'])