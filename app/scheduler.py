from rocketry import Rocketry

app = Rocketry(execution="async")


@app.task('every 5 seconds')
async def ping():
    print("PONG")
