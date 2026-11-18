from google import genai 
from dotenv import load_dotenv
import streamlit as st 
import base64 #for setting background
import time


load_dotenv()

client = genai.Client()


def set_background(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()                              #for setting background 
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
st.subheader("👉Do you want Me to select your Travel Location ")

def plan_trip():
    c_loc = st.text_input("Enter starting location")
    Des_loc = st.text_input("Enter selected location")
    passangers = st.number_input("Enter No. passangers",0,50)
    Days=st.number_input("Decided Days",0,30)
    Standard = st.selectbox(
        "Select Budget?",
        ("Luxary", "Mid-Range", "Budget"),
    )
    mode=st.selectbox(
        "Perfer Mode of transport?",
        ("Flight","Self Car","Railway","Bus"),
    )
    st.write("You selected:", mode)

    
    if st.button("Done"):
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=f"""I want to go to trip which would be of type{Standard}
to {Des_loc} and I am starting for {c_loc} I want a full trip plan of {Days} Days I would perfer my Transport as {mode} 
considering total number of passangers as {passangers} """,
            system_instruction="""Your a smart Travel assistant bot You have to plan 2 or 3 daywise trip plan starting from beginning of journey 
spots to visit on day1 afternoon launch to evening event then dinner and night stay such for all number of days that are given as per input mode of transport 
provide respective ticket links or booking link also try to put genral price of ticket/booking  """
        )
    
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(7)
        st.success("Travel plan!")
        st.button("Change input")

        st.write(interaction.output_text)
        print(interaction.output_text)
    

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

        st.text(interaction.output_text)




choice = st.radio(
    " ",
    ["YES", "NO"],
    horizontal=True,
    index=None,
)

if choice == "YES":
    Random_loc()

    st.header("⏱️Ready to plan trip")
    start= st.radio("",
    ["Ready", "Wait"],
    horizontal=True,
    index=None,
    )
    if start == "Ready":
        plan_trip()
    elif start == "Wait":
        st.text("Change inputs to decide Destination")

elif choice == "NO":
    plan_trip()
    