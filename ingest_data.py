import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf(file_path):
    # Load the PDF file
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print (f"Loaded {len(documents)} pages from the PDF file.")

    # configure text splitter. chunk size (100-150 words). chunk overlap context between chunks boundary
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,length_function=len)

    #Split the documents into smaller chunks.
    chunks = text_splitter.split_documents(documents)
    print(f"Split the document into {len(chunks)} chunks.")

    # lets see the very fast preview of the first chunk to see what it looks like
    if chunks:
        print("\n--- Preview of the first chunk:")
        print(f"Page content length: {len(chunks[0].page_content)} characters")
        print(f"source: {chunks[0].metadata.get('page')}")
        print(f"Preview of the first chunk: {chunks[0].page_content[:300]}...")  # Print first 500 characters of the first chunk

    return chunks


if __name__ == "__main__":
    # Example usage
    pdf_file_path = os.path.join("C:\\Projects\\RAG_Project\\data", "TCS_annual-report-2025-2026.pdf")  # Replace with your PDF file path
    if os.path.exists(pdf_file_path):
        process_pdf(pdf_file_path)
    else:
        print(f"File not found: {pdf_file_path}")