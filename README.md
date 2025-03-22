<h1 align="center">
📖 LangChain-Streamlit-Docker App
</h1>
💻 Running Locally

1. Clone the repository📂

```bash
git clone https://github.com/OGTAGRAM/ChatAI.git
```

2. Install dependencies with [uv](https://docs.astral.sh/uv/) and activate virtual environment🔨

```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

if you are using remote machines like WSL2, to optimise lcoal developments, follow

```
deactivate
python3 -m venv ~/Gemini-04/new_venv
source ~/Gemini-04/new_venv/bin/activate
pip install streamlit langchain langchain-google-genai
pip install -U langchain-community
```

> You can name the environment.


3. Run the Streamlit server🚀

```bash
streamlit run demo_app/main.py 
```
