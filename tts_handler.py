from gtts import gTTS
import tempfile
import edge_tts
import asyncio
import os

from logger_utils import chromecast_logger

def create_audio_file_gtts(message, lang='en'):
    try:
        tts = gTTS(text=message, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        chromecast_logger.error(f"Error creating audio file: {str(e)}")
        raise

def delete_audio_file(filepath):
    global audio_files
    try:
        if os.path.exists(filepath):
            os.unlink(filepath)
        if filepath in audio_files:
            del audio_files[filepath]
        chromecast_logger.info(f"Deleted audio file: {filepath}")
    except Exception as e:
        chromecast_logger.error(f"Error deleting audio file {filepath}: {str(e)}")
        
async def create_audio_file_edge(message, voice="sv-SE-MattiasNeural", rate="+0%"):
    try:
        # Create a temporary file with .mp3 extension
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            file_path = fp.name

        # Create TTS object and generate audio
        communicate = edge_tts.Communicate(message, voice, rate=rate)
        await communicate.save(file_path)

        print(f"Audio file created successfully. Size: {os.path.getsize(file_path)} bytes")
        return file_path
    except Exception as e:
        print(f"Error creating audio file: {str(e)}")
        raise

def create_custom_audio_file_edge(message, lang):
    file_path = asyncio.run(create_audio_file_edge(message, voice=lang, rate="-5%"))
    print(f"Audio file created at: {file_path}")
    return file_path