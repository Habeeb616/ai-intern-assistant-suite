# 🤖 AlphaTech Solutions - Advanced Intern Assistant Suite

An enterprise-grade **Retrieval-Augmented Generation (RAG)** engine and interactive intern dashboard built using **FastAPI**, **LangChain**, and **Groq** cloud hardware architecture.

## 🚀 Core Features
* **AI Knowledge Assistant:** Context-aware RAG search pipeline querying structural parameters from text context indices.
* **HR Stipend Reimbursements:** Live background simulated pipeline that formats transaction trails and logs secure audit trails to disk.
* **Emergency Leave Notice Validator:** Algorithmic verification checking if request call-out timeframes comply with corporate advance notification windows.

## 🛠️ Technology Stack
* **Backend Framework:** FastAPI & Pydantic
* **AI Framework:** LangChain & BM25 Text Retrievers
* **LLM Engine Infrastructure:** Groq Cloud LPU (`qwen/qwen3.8-27b`)
* **Storage Utilities:** Local Disk System IO File Streams & Tabular CSV Exporters

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd ai-intern-assistant-suite
   ```

2. **Install standard dependencies:**
   ```bash
   pip install fastapi uvicorn langchain langchain-groq langchain-community pydantic pypdf
   ```

3. **Configure Source Files:**
   Place your specific `document.pdf` and `knowledge.txt` configuration guidelines files directly in the root directory.

4. **Initialize the application locally:**
   ```bash
   uvicorn app:app --reload
   ```

5. **Access the Client Dashboard:**
   Open your browser and navigate to: `http://127.0.0`
