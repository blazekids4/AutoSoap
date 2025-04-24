# Transcription and SOAP Notes Generation  
  
This project uses Azure Cognitive Services and OpenAI to transcribe conversations and generate SOAP notes from the transcriptions. The transcription process can be stopped using a trigger phrase.  
  
## Table of Contents  
  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  
- [License](#license)  
  
## Prerequisites  
  
- Python 3.6 or higher  
- An Azure account with access to Cognitive Services  
- An OpenAI account with API access  
- Jinja2 template files: `soap_notes_prompt.jinja2` and `soap_example.jinja2`  
  
## Installation  
  
1. Clone the repository:  

    ```bash  
    git clone https://github.com/yourusername/yourrepository.git  
    cd yourrepository  
    ```  
  
2. Create a virtual environment and activate it:  

    ```bash  
    python -m venv venv  
    source venv/bin/activate  # On Windows: venv\Scripts\activate  
    ```  
  
3. Install the required packages:  

    ```bash  
    pip install -r requirements.txt  
    ```  
  
4. Create a `.env` file in the project directory and add your Azure and OpenAI credentials:  

    ```plaintext  
    SPEECH_KEY=your_azure_speech_key  
    SPEECH_REGION=your_azure_speech_region  
    AZURE_OPENAI_ENDPOINT=your_openai_endpoint  
    AZURE_OPENAI_API_KEY=your_openai_api_key  
    ```  
  
## Configuration  
  
Ensure you have the following Jinja2 template files in the project directory:  
  
- `soap_notes_prompt.jinja2`: Template for SOAP notes prompt.  
- `soap_example.jinja2`: Template for SOAP notes example.  
  
## Usage  
  
1. Run the transcription and SOAP notes generation script:  

    ```bash  
    python main.py  
    ```  
  
2. Speak into your microphone. The transcription process will start automatically.  
  
3. To stop the transcription, say the trigger phrase "stop recording".  
  
4. The transcribed text will be saved to `transcription.txt`.  
  
5. The generated SOAP notes will be printed to the terminal and saved to `soap_notes.md`.  
  
## How It Works  
  
1. **Transcription**: The script uses Azure Cognitive Services' `ConversationTranscriber` to transcribe the conversation. The transcription process can be stopped using a trigger phrase.  
  
2. **SOAP Notes Generation**: The transcribed text is passed to OpenAI's GPT-4 model to generate SOAP notes. The generated notes are saved to a markdown file and printed to the terminal.  
  
### Key Components  
  
- `recognize_from_mic()`: Captures the conversation from the microphone and transcribes it.  
- `create_soap_notes()`: Uses OpenAI to generate SOAP notes from the transcribed text.  
- `render_soap_notes_prompt()`: Renders the SOAP notes prompt template.  
- `render_soap_example()`: Renders the SOAP notes example template.  
  
## License  
  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  
