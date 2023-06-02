import streamlit as st
from db.redis_vectordb import upload
from db.helper import process_db_data
from streamlit.runtime.uploaded_file_manager import (
    UploadedFile,
    UploadedFileRec,
    UploadedFileManager,
)
from files import file_uploader

if "chunk_size" not in st.session_state:
    st.session_state["chunk_size"] = 500
if "chunk_overlap" not in st.session_state:
    st.session_state["chunk_overlap"] = 0

def main():
    st.title("Vector Database Uploader")
    st.sidebar.title("VectorDB Uploader")
    option = st.sidebar.radio("Select an option 🌿", ("Input", "Search"))

    if option == "Input":
        file_uploader()
        show_input()
    elif option == "Search":
        show_search()
    


def show_input():
    st.header("Upload to Vector Database")
    input_text = st.text_area("", height=400)
    upload_button = st.button("Upload")
    
    if upload_button:
        st.write("Input submitted:", input_text)
        save_text_to_file(input_text)
        upload(process_db_data())
        



def save_text_to_file(text):
    with open("output.txt", "w") as file:
        file.write(text)
    st.success("Text saved to output.txt")

def show_search():
    st.header("Search Option")
    search_text = st.text_area("Enter your search query here", height=100)
    submit_button = st.button("Submit")
    
    if submit_button:
        st.write("Searching for:", search_text)

if __name__ == "__main__":
    main()
