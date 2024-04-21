import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import openai

# API Key for OpenAI (to be replaced with your own key)

#openai_api_key = os.environ.get("OPENAI_API_KEY")

# Function to generate diet plan

def generate_program():
    generate_button.empty()
    st.session_state.generate = True
    
 
 # Set page configuration
    
st.set_page_config(page_title="Fitness Chat Bot")
st.title("AI Perosonal Nutritionists")
st.header("Diet Plan Generator")
st.sidebar.title("Customize your Diet plan")


if "generate" not in st.session_state:
    st.session_state.generate =False
    
if "currentkey" not in st.session_state:
    st.session_state.currentkey=" "

# Retrieve API key from secrets (if available)

try:
    st.session_state.currentkey =st.secrets["OPENAI_API_KEY"]
except:
    pass


# Input fields for user's fitness information
if st.session_state.currentkey:
    goal =st.selectbox(" Select  Fitness Goal ",["Lose weight" , "Gain Muscle "])
    gender =st.selectbox(" Select your Gender",["Male","Female"])
    Age =st.number_input("Enter Your Age",min_value=12,max_value=100)
    Weight =st.number_input("Enter Your Weight",min_value=10,max_value=300,)
    
    height =st.number_input("Enter your height in CM",min_value=140,max_value=180,step=1)
    Diet =st.selectbox("Select Diet Type",["veg","Non Veg","Vegan","Low Carb","Ketogenic"])
    
      # Button to generate diet plan
    generate_button = st.empty()
    generate_button.button("Generate Program", type="primary", on_click=generate_program)

    # Generate diet plan if button is clicked
    if st.session_state.generate:
        with st.spinner("generating Diet Plan"):
            output_concat=""
            
             # Initialize ChatOpenAI model
            llm= ChatOpenAI(model="gpt-3.5-turbo",temperature=0.5,openai_api_key=OPENAI_API_KEY)
              # Define template for diet plan generation
            template="""
            can you create diet plan monday to sunday and tell how many days should be fllow diet plan based on
            goal :{goal} 
            gender:{gender}
            Age:{Age}
            Weight:{Weight}
            height:{height}
            Diet:{Diet}
            
            
            """
            promp =PromptTemplate(input_variables=[ 'goal', 'gender', 'Age','Weight', 'height', 'Diet'], template=template)
            # Create LLMChain for generating diet plan
            chain=LLMChain(llm=llm,prompt=promp)
             # Run chain with user's input data
            output = chain.run({'goal':goal ,
           "gender": gender,
           "Age": Age,
           "Weight": Weight,
           "height" :height,
           'Diet':Diet})
            
            # Display generated diet plan
            st.write(output)
            st.write('******************')
            output_concat=output_concat+output
            st.session_state.generate = False
            

    
            
    
    



 