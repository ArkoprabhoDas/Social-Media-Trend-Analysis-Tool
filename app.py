import streamlit as st
import os
import subprocess
import nbformat 
from nbconvert.preprocessors import ExecutePreprocessor 
import threading

# pip freeze > requirements.txt
def run_ipynb(notebook_path): 
     
    with open(notebook_path, 'r', encoding='utf-8') as nb_file: 
        notebook = nbformat.read(nb_file, as_version=4) 
 
    
    execute_preprocessor = ExecutePreprocessor(timeout=-1, kernel_name='python3') 
 
    
    try: 
        execute_preprocessor.preprocess(notebook, {'metadata': {'path': '.'}}) 
    except Exception as e: 
        raise Exception(f"Error executing the notebook: {e}") 


def showPost():
    with open("post.txt","r", encoding="utf-8") as file:
        dataList = file.readlines()
    dataList = [item.strip() for item in dataList]
    st.title("Post : ")
    for item in dataList:
        st.success(item)

def showKeyword():
    with open("postKeyword.txt","r", encoding="utf-8") as file:
        dataList = file.readlines()
    dataList = [item.strip() for item in dataList]
    st.title("Topic : ")
    for item in dataList:
        st.success(item)

def deleteFile():
    if os.path.exists("keyword.txt"):
        os.remove("keyword.txt")
    if os.path.exists("region.txt"):
        os.remove("region.txt")
    if os.path.exists("age.txt"):
        os.remove("age.txt")


st.title("Welcome")
keyword = st.text_input("Enter the keyword : ")
optionsAge = ["No age","18-24","25-34","35-44","45-49","50-54","55-64"]
optionSelected = st.selectbox("Select an age option", optionsAge)
option = st.selectbox("Select an option:",["None","Region","Country"])
if(option == "Country"):
    optionsCountry = ["United States","Canada","Italy","Spain","Germany","France","Colombia","Argentina","Mexico","Brazil"]
    option = st.selectbox("Select Country:", optionsCountry)
elif(option == "Region"):
    optionsRegion = ["Southern Europe (GR, IT, MT, PT, ES)","Germanic countries (DE, AT, CH)","Great Britain & Ireland (GB, IE)","Nordic countries (NO, FI, DK, SE)","Eastern Europe (HU, PL, RO, SK, CZ)","Hispanic LatAm (CL, CO, AR, MX)","Australasia (AU, NZ)"]
    option = st.selectbox("Select Region:", optionsRegion)
if st.button("Submit") and len(keyword) != 0:
    deleteFile()
    with open("keyword.txt","w") as file:
        file.write(keyword)
    if(optionSelected != "No age"):
        with open("age.txt","w") as file:
            file.write(optionSelected)
    if(option != "None"):
        with open("region.txt","w") as file:
            file.write(option)
    with st.spinner("Searching through social media.......") :
        notebook_path_pintrest = "pintrest.ipynb"
        thread1 = threading.Thread(target=run_ipynb, args = (notebook_path_pintrest,))
        notebook_path_facebook = "facebook.ipynb"
        thread2 = threading.Thread(target=run_ipynb, args = (notebook_path_facebook,))
        notebook_path_Reddit = "Reddit.ipynb"
        thread3 = threading.Thread(target=run_ipynb, args = (notebook_path_Reddit,))
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()
    with st.spinner("Getting relevant post and topic.......") :
        run_ipynb("dataScanning.ipynb")
    col1, col2 = st.columns(2)
    with col1:
        showPost()
    with col2:
        showKeyword()

    


 
