import asyncio
from asyncio import subprocess


async def concatenate_audios_ffmpeg(temp_file_name: str, _format='mp3') -> bytes:
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',  # Позволяет использовать абсолютные пути
        '-i', temp_file_name,
        '-f', _format,  # Указываем формат на выходе
        '-'
    ]
    process = await subprocess.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE,
                                                      stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {stderr.decode()}")

    return stdout
