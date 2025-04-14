# app/handlers/video.py
import logging
import os
import tempfile
import subprocess
from pathlib import Path
import aiofiles
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

logger = logging.getLogger(__name__)
router = Router(name="video-handler")

# Temporary directory for processing files
TEMP_DIR = Path(tempfile.gettempdir()) / "audio_extractor"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.message(F.video)
async def handle_video(message: Message):
    """Handler for video messages - extracts audio and sends it back."""
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logger.info(f"Received video from {user_name} (ID: {user_id})")
    
    # Send a processing message
    processing_msg = await message.reply("Обрабатываю видео, извлекаю аудио...")
    
    try:
        # Get the video file
        video_file = await message.bot.get_file(message.video.file_id)
        video_path = TEMP_DIR / f"{message.video.file_id}.mp4"
        audio_path = TEMP_DIR / f"{message.video.file_id}.mp3"
        
        # Download the video file
        await message.bot.download_file(video_file.file_path, destination=video_path)
        logger.info(f"Video downloaded to {video_path}")
        
        # Extract audio using FFmpeg and compress to 128kbps
        ffmpeg_cmd = [
            "ffmpeg", 
            "-i", str(video_path), 
            "-vn",  # No video
            "-acodec", "libmp3lame",  # MP3 codec
            "-ab", "128k",  # 128kbps bitrate
            "-ar", "44100",  # 44.1kHz sample rate
            "-y",  # Overwrite output file if it exists
            str(audio_path)
        ]
        
        # Run FFmpeg command
        process = subprocess.run(
            ffmpeg_cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {process.stderr.decode()}")
            await processing_msg.edit_text("Ошибка при извлечении аудио. Пожалуйста, попробуйте другое видео.")
            return
        
        logger.info(f"Audio extracted to {audio_path}")
        
        # Send the audio file back
        audio_file = FSInputFile(audio_path)
        await message.reply_audio(
            audio=audio_file,
            caption="Вот аудио из вашего видео (сжато до 128kbps)"
        )
        logger.info(f"Audio sent back to {user_name} (ID: {user_id})")
        
        # Delete the processing message
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"Error processing video for {user_id}: {e}", exc_info=True)
        await processing_msg.edit_text("Произошла ошибка при обработке видео.")
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception as e:
            logger.error(f"Error cleaning up files: {e}")