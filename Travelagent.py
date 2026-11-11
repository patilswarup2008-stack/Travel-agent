from google import genai 
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client()
query=input("GEMINI:")
while True:
    interaction = client.interactions.create(
        model ="gemini-3.5-flash-lite",
        input= query,
        stream=True, # for stream of text genrated
        system_instruction="""Your a smart Travel assistant bot that gives replies in simple 
                               and effectives way using bullet marks 
                               paragraph writing and try help too resolue problem of user fast 
                               and quick dont add intro of your self in output
                            """, #behaviour of bot
        generation_config={
            "temperature":0.7,
            "max_output_tokens":500
        },
    )

    print("\n GEMINI Replies \n\n")
    for event in interaction:                                   #for stream of Text
        if event.event_type =="step.delta":
            if event.delta.type=="text":
                print(event.delta.text,end="",flush=True)

    query=input("\n GEMINI:")
    if (query==None) or (query=="exit"):
        break