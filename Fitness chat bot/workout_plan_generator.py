# importing Necessary Libary 

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import openai

# API Key for OpenAI (to be replaced with your own key)


#open_ai_key = os.environ.get("OPENAI_API_KEY")
openai.api_key =OPENAI_API_KEY


 
# Function to generate program when button is click

def generate_program():
    generate_button.empty()   #Clear the generate button
    st.session_state.generate = True  # Set session state variable to trigger program generation
    
    
    
    

# Set page configuration

st.set_page_config(page_title="Fitness Chat Bot")
st.title("AI Personal Trainer")
st.header("Workout Plan Generator")
st.sidebar.title('Workout plan')



# Initialise the session state variables if they dont exist
if 'generate' not in st.session_state:
    st.session_state.generate=False
if 'currentkey' not in st.session_state:
    st.session_state.currentkey =''
if 'validate' not in st.session_state:
    st.session_state.validate= False
if 'validate_count' not in st.session_state:
    st.session_state.validate_count =0
    
# Retrieve API key from secrets (if available)   
    
try:
    st.session_state.currentkey=st.secrets['OPENAI_API_KEY']
except:
    pass




# Main content section for generating workout program
    
if st.session_state.currentkey:
    weeks =st.number_input("How Long Should The Program Be (Weeks)",min_value=1,max_value=12,step=1)
    days=st.number_input("How Many Days Per Week ?",min_value=1,max_value=7,step=1)
    accessory = st.number_input("how many accessory lifts per session",min_value=0,max_value=5,step=1)
    squat = st.number_input("1 rep max squat?",min_value=0,max_value=1000,step=1)
    bench = st.number_input("1 rep max bench press?",min_value=0,max_value=1000,step=1)
    deadlift = st.number_input("1 rep max conventional deadlift?",min_value=0,max_value=1000,step=1)
    units = st.selectbox('units',['kilograms','pounds'])
    
    
    # Button to trigger program generation
    generate_button =st.empty()
    generate_button.button("Generate Program ",type='primary',on_click=generate_program)
    
    
    
     # Generate program if button clicked
    if st.session_state.generate:
        with st.spinner("generating program"):
            output_concat=""
            
            
           # Initialize ChatOpenAI model and PromptTemplat
            
            llm= ChatOpenAI(model='gpt-3.5-turbo',temperature=0.5,openai_api_key=OPENAI_API_KEY)
            template =  """
            
            Can you create a strength training program that focuses on back squat, bench press, and conventional deadlift

            number of sessions each week: {days}

            number of weeks: {weeks} 

            back squat 1 rep max: {squat} {units}

            bench press 1 rep max: {bench} {units}

            conventional deadlift 1 rep max: {deadlift} {units}

            number of accessory exercises each session: {accessory}

            Create the first week

            
            
            """
            promp = PromptTemplate(
                input_variables=['days','weeks','squat','units','bench','deadlift','accessory'],
                template=template
            )
            
            chain = LLMChain(llm=llm,prompt=promp)
            
            # Generate workout program for first week
              
            output=  output = chain.run({'days':days,'weeks':weeks,'squat':squat,'units':units,'bench':bench,'deadlift':deadlift,'accessory':accessory})
            st.write(output)
            st.write('******************')

            output_concat = output_concat + output
            
            
            # Generate workout program for subsequent weeks if applicable
            
            week_total = int(weeks)
            if week_total > 1:
                current_week = 2
                while current_week <= week_total:
                
                    
                    llm = ChatOpenAI(model='gpt-3.5-turbo',temperature=0.5,openai_api_key=st.session_state.currentkey)
                    template = """
                    create training program for week number {current_week} given information about last weeks training:
                    {program}
                    and the following details:
                    number of sessions each week: {days}
                    back squat 1 rep max: {squat} {units}

                    bench press 1 rep max: {bench} {units}

                    conventional deadlift 1 rep max: {deadlift} {units}

                    number of accessory exercises each session: {accessory}

                    make the program more challenging than the previous week.



                    """

                    
                    promp = PromptTemplate(
                        input_variables=['program','days','squat','units','bench','deadlift','accessory','current_week'],
                        template=template
                    )

                    chain = LLMChain(llm=llm,prompt=promp)
                    
                    # Generate workout program for current week
                    
                    output = chain.run({'program':output,'days':days,'squat':squat,'units':units,'bench':bench,'deadlift':deadlift,'accessory':accessory,'current_week':current_week})
                    st.write(output)
                    st.write('******************')
                    current_week = current_week + 1
                    output_concat = output_concat + output
                    st.session_state.generate = False


        





    
    
        
    