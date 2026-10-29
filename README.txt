Diabetes Probability Calculator - Render deployment package

Files:
- app.py: Streamlit calculator
- requirements.txt: Python dependencies

Render settings:
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0

Important:
- This package is an educational prototype and is not a validated clinical tool.
- If using a GitHub repository that already hosts another app, do not overwrite its app.py unless you intend to replace that application.
- Choose a new Render service/repository or a separate subdirectory for this calculator.
