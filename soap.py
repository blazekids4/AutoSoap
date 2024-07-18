import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
import os
from jinja2 import Environment, FileSystemLoader

def recognize_from_mic():
    speech_key=os.getenv("SPEECH_KEY")
    service_region=os.getenv("SPEECH_REGION")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        with open('transcription.txt', 'w') as file:
            file.write(result.text)
        return result.text  # Return the recognized text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return ""  # Return an empty string if no speech is recognized
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return ""  # Return an empty string in case of cancellation

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
)

def render_soap_notes_prompt():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./soap_notes_prompt.jinja2')
    soap_notes_prompt = template.render()
    return soap_notes_prompt

def render_soap_example():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./soap_example.jinja2')
    soap_example = template.render()
    return soap_example

def create_soap_notes(result, soap_notes_prompt, soap_example):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"you are an expert writing medical SOAP notes.  you will take the transcribed note provided by the doctor and you will create a detailed SOAP formatted report.  because this is a prototype application, you will insert reasonable assumptions into areas of your report you do not have the full conext.  you will not add any additional notes or commentary to your response other than your SOAP formatted report. YOu will reference these notes on writing SOAP reports: {soap_notes_prompt}. You will also refernece this example: {soap_example} Now the user will provide you the Doctors notes."},
            {"role": "user", "content": result},
        ],
    )
    soap_note = completion.choices[0].message.content
    with open('soap_notes.md', 'w') as md_file:
        md_file.write(soap_note)
    return soap_note

# Generate the soap_notes_prompt and soap_example
soap_notes_prompt = render_soap_notes_prompt()
soap_example = render_soap_example()

# Now call create_soap_notes with all required arguments
print(create_soap_notes(recognize_from_mic(), soap_notes_prompt, soap_example))

recognize_from_mic()
