# instructions
cd mining-maintenance-agent

pip install uv 

uv sync

source .venv/bin/activate

uv add -r requirements.txt

streamlit run app.py