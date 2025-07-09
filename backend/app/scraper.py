from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def scrape_url(url: str):
    try:
        print(f"[Scraper] Fetching content from: {url}")
        loader = WebBaseLoader(url)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)
        print(f"[Scraper] Split into {len(chunks)} chunks")
        return chunks

    except Exception as e:
        print(f"[Scraper Error] {e}")
        return []


# ✅ Run manually: python scraper.py
if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Deep_sea"
    docs = scrape_url(test_url)

    if docs:
        with open("scraped_output.txt", "w", encoding="utf-8") as f:
            for i, doc in enumerate(docs):
                f.write(f"\n--- Chunk {i+1} ---\n")
                f.write(doc.page_content.strip() + "\n")
        print("[Scraper] Data successfully saved to 'scraped_output.txt'")
    else:
        print("[Scraper] No data to write.")
