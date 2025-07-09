from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.scraper import scrape_url
from app.chat import ask_question
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["chrome-extension://..."]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route 1: Scrape and save to file
@app.post("/scrape-and-download")
async def scrape_and_save(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse(content={"error": "No URL provided"}, status_code=400)

    chunks = scrape_url(url)

    if not chunks:
        return JSONResponse(content={"error": "Scraping failed"}, status_code=500)

    output_path = "scraped_output.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for i, doc in enumerate(chunks):
            f.write(f"\n--- Chunk {i+1} ---\n")
            f.write(doc.page_content.strip() + "\n")

    return JSONResponse(content={"download_url": "http://127.0.0.1:8000/download-txt"})

# ✅ Route 2: Serve the scraped file
@app.get("/download-txt")
def download_scraped_file():
    return FileResponse("scraped_output.txt", media_type='text/plain', filename="scraped_output.txt")

# ✅ Route 3: Chat - Ask questions about the scraped file
class ChatInput(BaseModel):
    question: str

@app.post("/ask-question")
async def ask(chat: ChatInput):
    try:
        loader = TextLoader("scraped_output.txt", encoding="utf-8")
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs_chunked = splitter.split_documents(docs)

        response = ask_question(docs_chunked, chat.question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
