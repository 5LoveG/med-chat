from config import WHISPER_MODEL
import whisper

audio_model = whisper.load_model(WHISPER_MODEL)  # 可选 base/small/medium/large
