import uvicorn
from fastapi import FastAPI

from routers import user as UserRouter


app = FastAPI()
app.include_router(UserRouter.router, prefix="/tt")
# app.include_router(tes.router, prefix="/test")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=3)
