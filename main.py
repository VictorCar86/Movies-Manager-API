from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from middlewares.error_handler import ErrorHandler
from db.config import Base, engine
from routes.movies import movies as movies_router
from routes.auth import auth as auth_router
import time

app = FastAPI()
app.title = 'TestAPI'
app.version = '0.0.1'
app.description = 'Lorem ipsus'

### Middlewares ###

@app.middleware('http')
async def middle(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	process_time = time.time() - start_time
	response.headers["X-Process-Time"] = str(process_time)
	return response

app.add_middleware(ErrorHandler)

### Database ###

Base.metadata.create_all(bind=engine)

### Routes ###

@app.get('/', tags=['home'])
def home():
	return FileResponse('./test/index.html')

app.include_router(movies_router)
app.include_router(auth_router)
