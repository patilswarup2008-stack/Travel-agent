from google import genai 
from dotenv import load_dotenv
import streamlit as st 
import base64 #for setting background
import time


load_dotenv()

client = genai.Client()


def set_background(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    "<style>[data-testid='stMarkdownContainer'] p { text-align: justify; }</style>",  #for justifying st.write
    unsafe_allow_html=True,
)

st.title(":violet[🌏TRAVEL ASSISTANT]",text_alignment="center")
set_background("other\image.jpg")
st.header("Hello this is your Travel Assistant Lets plan your trip together",text_alignment="center")
st.text("👉Do you want Me to select your Travel Location ",text_alignment="center")

def Random_loc():
    st.text("📍 selecting location with some info")
    c_loc = st.text_input("Enter Current city")
    dis = st.slider("Enter parameter of trip", 0, 1000, 50)
    st.write("Your Range is", dis, "KM")
    Days = st.number_input("Enter Days of trip", 0, 30)

    if st.button("Show options"):
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=f"""I want to go to trip for {Days} days
my current city is {c_loc}
find some best in range of {dis} Km
suggest all famous and important spot in that range""",
            stream=True,
            system_instruction="""Your a smart Travel assistant bot that gives replies in simple
and effective way using bullet marks with proper block arrangement,
paragraph writing put text in bracket in same line only, give roman number to place and try help too resolve problem of user fast
and quick dont add intro of your self in output """,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500,
            },
        )
    
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(5)
        st.success("Let's select")
        st.button("Change input")

        for event in interaction:                                   #for stream of Text
            if event.event_type =="step.delta":
                if event.delta.type=="text":
                    st.write(event.delta.text)
        plan_trip()

def plan_trip():
    st.text_input("Enter selected location")
    st.number_input("Enter No. passangers",0,50)
    Standard = st.selectbox(
        "Select Budget?",
        ("Luxary", "Mid-Range", "Budget"),
    )
    st.write("You selected:", Standard)
    




choice = st.radio(
    "Do you want me to select your travel location?",
    ["YES", "NO"],
    horizontal=True,
    index=None,
)

if choice == "YES":
    Random_loc()
    choice = st.radio("⏱️Ready to plan trip",
    ["Ready", "Wait"],
    horizontal=True,
    index=None,
    )
    if choice == "Ready":
        plan_trip()


elif choice == "NO":
    plan_trip()
    










# query=input("GEMINI:")
# id=None                                              #dummy variable to store history
# while True:
#     interaction = client.interactions.create(
#         model ="gemini-3.5-flash-lite",
#         input= query,
#         stream=True, # for stream of text genrated
#         system_instruction="""Your a smart Travel assistant bot that gives replies in simple 
#                                and effectives way using bullet marks with proper arrangement, 
#                                paragraph writing and try help too resolue problem of user fast 
#                                and quick dont add intro of your self in output
#                             """, #behaviour of bot
#         generation_config={
#             "temperature":0.7,
#             "max_output_tokens":500
#         },
#         previous_interaction_id=id                              # chat history
#     )

#     print("\n GEMINI Replies \n\n")
#     for event in interaction:                                   #for stream of Text
#         if event.event_type =="step.delta":
#             if event.delta.type=="text":
#                 print(event.delta.text,end="",flush=True)

#     id = event.interaction.id
#     query=input("\n GEMINI:")
#     if (query==None) or (query=="exit"):
#         break