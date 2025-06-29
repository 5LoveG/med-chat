import uvicorn
from routers import *
from config import *
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Medical Chat API",
    version="1.0",
    description="API with session management for medical consultations"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type"]
)

# Include routers
app.include_router(audio.router)
app.include_router(chat.router)
app.include_router(picture.router)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
