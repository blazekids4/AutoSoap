import azure.cognitiveservices.speech as speechsdk  
from openai import AzureOpenAI  
import os  
import time  
from jinja2 import Environment, FileSystemLoader  
  
# Global variables  
transcribing_stop = False  
trigger_phrase = "stop recording"  
transcribed_text = ""  
  
def conversation_transcriber_recognition_canceled_cb(evt: speechsdk.SessionEventArgs):  
    print('Canceled event')  
  
def conversation_transcriber_session_stopped_cb(evt: speechsdk.SessionEventArgs):  
    print('SessionStopped event')  
  
def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):  
    global transcribing_stop, transcribed_text  
    print('TRANSCRIBED:')  
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:  
        print('\tText={}'.format(evt.result.text))  
        print('\tSpeaker ID={}'.format(evt.result.speaker_id))  
        transcribed_text += evt.result.text + " "  # Append recognized text to the transcribed_text  
        if trigger_phrase in evt.result.text.lower():  # Check if the trigger phrase is in the recognized text  
            print('Trigger phrase detected. Stopping transcription.')  
            transcribing_stop = True  
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:  
        print('\tNOMATCH: Speech could not be TRANSCRIBED: {}'.format(evt.result.no_match_details))  
  
def conversation_transcriber_session_started_cb(evt: speechsdk.SessionEventArgs):  
    print('SessionStarted event')  
  
def recognize_from_mic():  
    global transcribing_stop, transcribed_text  
    speech_key = os.getenv("SPEECH_KEY")  
    service_region = os.getenv("SPEECH_REGION")  
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)  
    speech_config.speech_recognition_language = "en-US"  
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)  
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)  
    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(speech_config=speech_config, audio_config=audio_config)  
  
    def stop_cb(evt: speechsdk.SessionEventArgs):  
        global transcribing_stop  
        print('CLOSING on {}'.format(evt))  
        transcribing_stop = True  
  
    # Connect callbacks to the events fired by the conversation transcriber  
    conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)  
    conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)  
    conversation_transcriber.session_stopped.connect(conversation_transcriber_session_stopped_cb)  
    conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)  
    # Stop transcribing on either session stopped or canceled events  
    conversation_transcriber.session_stopped.connect(stop_cb)  
    conversation_transcriber.canceled.connect(stop_cb)  
    conversation_transcriber.start_transcribing_async()  
  
    # Waits for completion.  
    while not transcribing_stop:  
        time.sleep(.5)  
  
    conversation_transcriber.stop_transcribing_async()  
  
    if transcribed_text:  
        print("Final Transcription: {}".format(transcribed_text))  
        with open('transcription.txt', 'w') as file:  
            file.write(transcribed_text)  
        return transcribed_text  # Return the transcribed text  
    else:  
        print("No speech could be recognized.")  
        return ""  # Return an empty string if no speech is recognized  
  
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
            {"role": "system", "content": f"you are an expert writing medical SOAP notes.  you will take the transcribed note provided by the doctor and you will create a detailed SOAP formatted report.  because this is a prototype application, you will insert reasonable assumptions into areas of your report you do not have the full context.  you will not add any additional notes or commentary to your response other than your SOAP formatted report. You will reference these notes on writing SOAP reports: {soap_notes_prompt}. You will also reference this example: {soap_example} Now the user will provide you the Doctors notes."},  
            {"role": "user", "content": result},  
        ],  
    )  
    soap_note = completion.choices[0].message.content  
    with open('soap_notes.md', 'w') as md_file:  
        md_file.write(soap_note)  
    print(soap_note)  # Print the generated SOAP notes to the terminal  
    return soap_note  
  
# Generate the soap_notes_prompt and soap_example  
soap_notes_prompt = render_soap_notes_prompt()  
soap_example = render_soap_example()  
  
# Now call create_soap_notes with all required arguments  
recognized_text = recognize_from_mic()  
if recognized_text:  
    create_soap_notes(recognized_text, soap_notes_prompt, soap_example)  
