# Gemma3-Powered LocalLLM for Retrieval Augmented Generation (RAG)

Gemma is a lightweight, family of models from Google built on Gemini technology. The Gemma 3 models are multimodal — processing both text and images. Gemma3 has been benchmarked to outperform DeepSeek-V3 while requiring less computional resources.

RAG is a technique for enhancing the accuracy and reliability of generative AI models (Large Language Models) with information from specific and relevant data sources, often available on on-prem or local machines.

This repository enables standing up a local LLM service with Gemma3 that indexes local and remote files and emails to provide comprehensive responses for specific research and administrative tasks.

- eg: Summarise all papers on satellite derived bathymetry - and prepare a white paper on pros and cons of each methodology.
- eg: When is Nick's contract due?
- eg: Prepare an executive summary of all communications and paperwork for RFP 34424.
- eg: What is SPC's policy on airline club membership?

There is zero-leakage to the internet post-setup, and this tool can be used without any internet connectivity.

### Setup Ollama

Download Ollama and install from ollama.com

In your terminal, get Gemma3 with Tooling support -

`ollama pull ebdm/gemma3-enhanced:12b`

### Setup uv - a Rust-based tooling for Python Projects

https://docs.astral.sh/uv/getting-started/installation/

### Clone the Repository

`git clone https://github.com/sopac/gemma-rag-agent.git`

`cd gemma-rag-agent`

### Install Python and Dependecies

Prior installation of a Python 3.13 environment is not required. Within your terminal run -

`uv sync`

### Update Local Sources

Edit `sources.txt` and update the list of folders to index 

### Index Local Sources

Within your terminal run -

`uv run index.py`

This process will take several hours, so best to let it run overnight.

### Start LocalLLM

`ollama serve`

### Query 
Within your terminal run -

`uv run main.py`

Exit the query tool with `\q`. There is a context mechanism present, so you can ask follow up questions to drill down previous answers further.

### System Requirements

16Gb+ RAM
