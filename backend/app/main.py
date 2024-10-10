from fastapi import FastAPI, status
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .utils.limiter import limiter
from .routes import taskRoutes, authRoutes, userRoutes

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(taskRoutes.router)
app.include_router(authRoutes.router)
app.include_router(userRoutes.router)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Root"}
