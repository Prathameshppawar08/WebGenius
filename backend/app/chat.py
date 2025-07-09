from langchain_perplexity import ChatPerplexity
from langchain_core.documents import Document
# from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
load_dotenv()
PPLX_API_KEY = os.getenv("PPLX_API_KEY")


def ask_question(documents: list[Document], question: str) -> str:
    try:
        # ✅ Initialize LLM
        llm = ChatPerplexity(
            pplx_api_key=PPLX_API_KEY,
            model="sonar",  # You can also try "sonar-medium-chat"
            temperature=0.2,
        )
        prompt = PromptTemplate.from_template(
        "Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}"
        )

        chain: Runnable = create_stuff_documents_chain(llm, prompt)
        result = chain.invoke({"context": documents, "question": question})

        
        # ✅ Load LangChain QA chain with the Perplexity LLM
        # chain = load_qa_chain(llm, chain_type="stuff")

        # ✅ Run QA chain
        # result = chain.run(input_documents=documents, question=question)
        return result

    except Exception as e:
        print(f"[QA Error] {e}")
        return "Sorry, could not process your question with Perplexity."


# ✅ Only for manual testing
if __name__ == "__main__":
    from langchain_community.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # ✅ Load text file scraped from webpage
    loader = TextLoader("scraped_output.txt", encoding="utf-8")
    docs = loader.load()

    # ✅ Chunk text into smaller parts
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_chunked = splitter.split_documents(docs)

    # ✅ Ask a question
    user_question = input("Ask something about the webpage: ")
    answer = ask_question(docs_chunked, user_question)

    # ✅ Print result
    print("\n📌 Answer:")
    print(answer)
