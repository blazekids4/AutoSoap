import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_id = "whisper" #This will correspond to the custom name you chose for your deployment when you deployed a model."
audio_test_file = "./Recording.m4a"

result = client.audio.transcriptions.create(
    file=open(audio_test_file, "rb"),            
    model=deployment_id
)

print(result)