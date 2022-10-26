import uvicorn


from fastapi import FastAPI
from router import product

app = FastAPI(
    title="Shopping Cart API",
    description="This API was develpoed for teaching Fast API",
    version="v0.0.1",
    terms_of_service="http://localhost:5000",
        )

app.include_router(product.router)

@app.get("/")
def root():
    return {"Docs": "Hellow world!"}

if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
