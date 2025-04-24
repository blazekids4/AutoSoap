# AutoSOAP

A prototype Python application that uses Azure Cognitive Services for real-time conversation transcription and Azure OpenAI (GPT-4) to generate clinical SOAP notes. Supports both a CLI and a Flask web interface.

## Features

- Real‑time transcription with Azure Speech `ConversationTranscriber` and a trigger phrase ("stop recording") to end sessions  
- Generate detailed SOAP notes (Subjective, Objective, Assessment, Plan) via Azure OpenAI  
- CLI scripts: `soap.py`, `soap_multi.py`, `whisper.py`  
- Flask web app: `soap_flask.py` with simple UI (`templates/index.html`, `templates/view_response.html`)  
- Jinja2 templates for prompts and examples: `soap_notes_prompt.jinja2`, `soap_example.jinja2`  

## Demo

<!-- GitHub strips iframes in Markdown previews; use a clickable thumbnail instead -->
[![Watch the demo video](https://img.youtube.com/vi/Zhg5XXd0FDM/0.jpg)](https://youtu.be/Zhg5XXd0FDM)

## Prerequisites

- Python 3.8 or higher  
- Azure subscription with Cognitive Services (Speech)  
- Azure OpenAI resource  
- Microphone (for live transcription)  

## Installation

1. Clone the repo:  

   ```bash
   git clone https://github.com/yourusername/AutoSoap.git
   cd AutoSoap
   ```

2. Create and activate a virtual environment:  

   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:  

   ```bash
   pip install -r requirements.txt
   ```

4. Copy and configure environment variables:  

   ```bash
   copy .env.example .env
   ```

   Edit `.env` and fill in your Azure/OpenAI keys and endpoints.

## Usage

### CLI Mode

- Live multi‑speaker transcription and SOAP notes generation:  

  ```bash
  python soap_multi.py
  ```

- Simple one‑turn transcription and note generation:  

  ```bash
  python soap.py
  ```

- Direct Whisper‑style transcription using Azure OpenAI audio endpoint:  

  ```bash
  python whisper.py
  ```

Generated files:  

- Transcribed text → `soap_notes_archive/transcription.txt`  
- SOAP notes → `soap_notes_archive/soap_notes.md` (or `soap_notes.txt` in Flask mode)  

### Flask Web Interface

1. Run the Flask app:  

   ```bash
   python soap_flask.py
   ```

2. Visit `http://localhost:5000` in your browser  
3. Click “Start Recording” to begin  
4. Say “stop recording” to finish  
5. Download your generated SOAP notes  

## Project Structure

```
.
├── soap_flask.py
├── soap_multi.py
├── soap.py
├── whisper.py
├── requirements.txt
├── .env.example
├── templates/
│   ├── index.html
│   └── view_response.html
├── soap_notes_prompt.jinja2
├── soap_example.jinja2
└── static/
    └── soap.jpg
```

## License

MIT License. See [LICENSE](LICENSE) for details.
