from fastapi import FastAPI

app = FastAPI(title="taxifare")

@app.get("/")
def root():
    return {"message": "Taxifare API is running"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}
