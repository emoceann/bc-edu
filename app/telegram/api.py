import app.telegram.handler
from .services import app


@app.get("/")
async def test():
    pass
