import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import json
import openai


# API Key for OpenAI (to be replaced with your own key)
#openai_api_key = os.environ.get("OPENAI_API_KEY")



def generate_answer():
    generate_button.empty()
    st.session_state.generate = True



# Load fitness questions from a JSON file
with open('questions.json', 'r') as json_file:
    json_data = json_file.read()
    data = json.loads(json_data)
    
# Extract questions from JSON data
 
questions = data['questions']
question_list = []


#  Set page title
st.set_page_config(
    page_title="Fitness Chat Bot",
)
st.title("AI Personal Trainer")
st.header("Answering Fitness Questions")


# Initialise the session states if they dont exist
if "generate" not in st.session_state:
    st.session_state.generate = False

if 'currentkey' not in st.session_state:
     st.session_state.currentkey = ''


try:
    st.session_state.currentkey = st.secrets["OPENAI_API_KEY"]
except:
    pass










# Display fitness questions in a select box

if st.session_state.currentkey:
    question_list.append('Select a question')
    for question in questions:
        question_list.append(question['question'])

    option = st.selectbox('Select a question',question_list,placeholder='Select a question')

    if option != 'Select a question':

        
        generate_button = st.empty()
        generate_button.button("generate answer",type='primary',on_click=generate_answer)
        if st.session_state.generate:
            with st.spinner("Answering your question..."):
                llm = ChatOpenAI(model='gpt-3.5-turbo',temperature=0.5,openai_api_key=OPENAI_API_KEY)
                template = """
                {option}
                """
                promp = PromptTemplate(
                    input_variables=['option'],
                    template=template
                )
                chain = LLMChain(llm=llm, prompt=promp)
                output = chain.run({'option':option})
            st.write(output)
            st.session_state.generate = False


