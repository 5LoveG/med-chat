# local
UPLOAD_FOLDER: str = "Local/uploads"  # audio file
SESSION_STORAGE_DIR: str = "Local/Sessions"  # session file

# audio
MAX_FILE_SIZE: int = 16 * 1024 * 1024  # max audio file size 16MB
WHISPER_MODEL: str = "small"  # whisper model type base/small/medium/large

# llm
# OPENAI_API_KEY: str = ""
# OPENAI_API_BASE: str = ""
MAX_TOKENS: int = 2024

# web but rag embedding need local ollama
HOST: str = "localhost"
PORT: int = 8000

# local_model if not web
LLM_MODEL_NAME: str = "qwen3:8b"
# model="deepseek-r1",
# model="deepseek-r1:1.5b",
# model="qwen3:0.6b",
