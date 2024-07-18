# Speech to SOAP Note Generator

This project utilizes Azure Cognitive Services and OpenAI to recognize speech from a microphone, transcribe it, and generate a SOAP (Subjective, Objective, Assessment, and Plan) note in markdown format.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Speech Recognition**: Recognizes speech using Azure Cognitive Services.
- **Transcription**: Saves the recognized speech to a text file.
- **SOAP Note Generation**: Utilizes OpenAI to generate a SOAP note based on the recognized speech.
- **Template Rendering**: Uses Jinja2 to render the SOAP note prompt and example.

## Setup

### Prerequisites

- Python 3.7+
- Azure subscription with the Cognitive Services and OpenAI APIs enabled.
- Required Python packages:
  - `azure-cognitiveservices-speech`
  - `openai`
  - `jinja2`
  - `python-dotenv`

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your_repo/speech-to-soap-note.git
    cd speech-to-soap-note
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file with your Azure and OpenAI credentials:

    ```ini
    SPEECH_KEY=your_azure_speech_key
    SPEECH_REGION=your_azure_speech_region
    AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key
    ```

## Usage

1. Ensure your templates for the SOAP notes prompt and example are in the project directory:

    - `soap_notes_prompt.jinja2`
    - `soap_example.jinja2`

2. Run the script:

    ```sh
    python script.py
    ```

3. Follow the on-screen prompts to speak into your microphone.

4. The transcribed text will be saved to `transcription.txt` and the generated SOAP note will be saved to `soap_notes.md`.

## Script Overview

### `recognize_from_mic()`

Recognizes speech from the microphone, saves the transcription to `transcription.txt`, and returns the recognized text.

### `render_soap_notes_prompt()`

Renders the SOAP notes prompt using the `soap_notes_prompt.jinja2` template and returns the rendered prompt.

### `render_soap_example()`

Renders an example SOAP note using the `soap_example.jinja2` template and returns the rendered example.

### `create_soap_notes(result, soap_notes_prompt, soap_example)`

Uses OpenAI to create a SOAP note based on the transcribed text, prompt, and example. The generated note is saved to `soap_notes.md`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
