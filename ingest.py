import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.custom_embeddings import GoogleEmbeddings
from app.config import Config

def load_document_with_encoding(path):
    """Handle encoding issues specifically for employee_handbook.md"""
    if "employee_handbook.md" in path:
        # Try UTF-8 first, then fallback to other common encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                loader = TextLoader(path, encoding=encoding)
                return loader.load()
            except UnicodeDecodeError:
                continue
        raise RuntimeError(f"Failed to load {path} with multiple encodings")
    else:
        return TextLoader(path).load()

def ingest_data():
    embeddings = GoogleEmbeddings()
    
    departments = {
        "engineering": ["engineering_master_doc.md"],
        "finance": ["financial_summary.md", "quarterly_financial_report.md"],
        "general": ["employee_handbook.md"],
        "hr": ["hr_data.csv"],
        "marketing": [
            "marketing_report_2024.md",
            "marketing_report_q1_2024.md",
            "marketing_report_q2_2024.md",
            "marketing_report_q3_2024.md",
            "market_report_q4_2024.md"
        ]
    }
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    for dept, files in departments.items():
        docs = []
        for file in files:
            path = f"data/{dept}/{file}"
            if file.endswith('.csv'):
                loader = CSVLoader(file_path=path)
                documents = loader.load()
            elif file == "employee_handbook.md":
                # Use our special loader for this specific file
                documents = load_document_with_encoding(path)
            else:
                loader = TextLoader(path)
                documents = loader.load()
                
            docs.extend(text_splitter.split_documents(documents))
        
        Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=f"{Config.CHROMA_PATH}/{dept}"
        )
        print(f"Ingested {len(docs)} chunks for {dept}")

if __name__ == "__main__":
    ingest_data()