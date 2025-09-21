from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader,UnstructuredURLLoader
from langchain_groq import ChatGroq
import bs4
from Prompt import generic_prompt,final_prompt,web_prompt
import streamlit as st
import tempfile
import os

groq_key="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"


with st.sidebar:
    st.header("Navigation")
    model_name=st.selectbox("choose llm model",                            options=["openai/gpt-oss-120b","openai/gpt-oss-20b","llama-3.3-70b-versatile","moonshotai/kimi-k2-instruct-0905"])
    language=st.selectbox("language",options=["english","franch","arabic","chainis"])
    chosen_option=st.radio("Choose an option", options=["web", "documents"])

    
llm=ChatGroq(api_key=groq_key,model=model_name)

if chosen_option == "documents":
    st.header("document Processing Mode")
    st.write("Enter the pdf txt docs files you want to process.")
    file_uploader = st.file_uploader(
        "Upload your files", 
        accept_multiple_files=True
    )
    try:
        documents = []
        if file_uploader:
            
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    for uploaded_file in file_uploader:
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        
                        with open(file_path, "wb") as file:
                            file.write(uploaded_file.getvalue())
                        
                        if uploaded_file.name.endswith(".pdf"):
                            st.write("pdf mode active")
                            loader = PyPDFLoader(file_path)
                        elif uploaded_file.name.endswith(".txt"):
                            st.write("txt mode active")
                            loader = TextLoader(file_path)
                        elif uploaded_file.name.endswith(".docx"):
                            st.write("docs mode active")
                            loader = Docx2txtLoader(file_path)
                        else:
                            st.warning(f"Skipping unsupported file type: {uploaded_file.name}")
                            continue

                        files = loader.load_and_split()
                        documents.extend(files)

                st.success(f"Successfully loaded {len(documents)} pages from all files.")
                
            except Exception as e:
                st.error(f"Error loading document: {e}")
    except:
            st.info(f"load documents")


    text_spliter=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=300)
    docs=text_spliter.split_documents(documents)
    lista = []
    for doc in docs:
        if isinstance(doc.page_content, str) and doc.page_content.strip():
            lista.append(llm.get_num_tokens(doc.page_content))
        else:
            print(f"Skipping a document with invalid or empty page content: {doc.page_content}")

    with st.spinner("prossess"):    
        if sum(lista)<=5000:
            prompt=PromptTemplate(input_variables=["text"],template=generic_prompt)
            sumary_chain=load_summarize_chain(llm,
                                            chain_type="stuff",
                                            verbose=True,
                                            prompt=prompt)  
        else:
            prompt_final=PromptTemplate(input_variables=["text"],template=final_prompt)
            prompt=PromptTemplate(input_variables=["text"],template=generic_prompt)
            sumary_chain=load_summarize_chain(llm=llm,
                                            map_prompt=prompt,
                                            verbose=True,
                                            chain_type="map_reduce",
                                            combine_prompt=prompt_final)

        st.write(sumary_chain.run(input_documents=docs, language=language))
elif chosen_option == "web":
    st.header("Web Page Processing Mode")
    st.write("Enter the URL of the web page you want to process.")
    
    url_input = st.text_input("Enter URL here", "https://en.wikipedia.org/wiki/Large_language_model")

    if st.button("Process URL"):
        if url_input:
                loader=None
                try:
                    loader = UnstructuredURLLoader(urls=[url_input],
                                                       ssl_verify=True)
                    web_documents = loader.load()
                except Exception as e:
                    st.exception(f'error {e}')
    
                if web_documents:
                    with st.spinner("loading"): 
                        prompt=PromptTemplate(input_variables=["text"],template=web_prompt)
                        sumary_chain=load_summarize_chain(llm,
                                                            chain_type="stuff",
                                                            verbose=True,
                                                            prompt=prompt)
                        st.write(sumary_chain.run(input_documents=web_documents, language=language))

        else:
                st.warning("Please enter a URL to process.")

