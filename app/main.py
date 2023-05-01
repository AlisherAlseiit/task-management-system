from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, auth, board, list, card, comment, board_member

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(board.router)
app.include_router(list.router)
app.include_router(card.router)
app.include_router(comment.router)
app.include_router(board_member.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
