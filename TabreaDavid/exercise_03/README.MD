## How to use

1. **Clone the repository**

2. **Create virtual environment**
    ```bash
    python -m venv venv
    source .venv/bin/activate (macos/Linux)
    .\venv\Scripts\Activate
    ```
3. **Install dependencies**
    ```bsah
    pip install -r requirements.txt
    ```
4. **Create .env file**
    ```env
    DATABASE_URL=sqlite:///./db.sqlite3
    ```
5. **Start the FastAPI backend**
    ```bash
    uvicorn main:app --reload
    ```
    Available at port 8000

ingorati unele commit-uri, am schimbat folder structure-ul de cateva ori
