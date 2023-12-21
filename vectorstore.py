import pandas as pd
import os
from langchain.vectorstores import FAISS
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


from dotenv import load_dotenv
load_dotenv()

def load_dataset(dataset_name:str="routes.csv"):
    """
    Helper function to load the dataset

    Args:
         dataset_name (str, optional): Name of the file saved from the extraction phase. Defaults to "dataset.csv".

    Returns:
         pd.DataFrame: Pandas DataFrame of data collected by LangChain
    """
    data_dir = "./data"
    file_path = os.path.join(data_dir, dataset_name)
    df = pd.read_csv(file_path)
    return df


def create_chunks(dataset:pd.DataFrame, chunk_size=1000, chunk_overlap=0):
    """
    Creates informational chunks from the dataset 

    Args:
        dataset (pd.DataFrame): Dataset Pandas
        chunk_size (int): How many chunks do we want?
        chunk_overlap (int): How much information should overlap among chunks?

    Returns:
        list: list of chunks
    """
    text_chunks = DataFrameLoader(
        dataset, page_content_column="body"
    ).load_and_split(
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )
    )
    # This is a trick we do: 
    # we add metadata to the chunks themselves to facilitate retrieval
    for doc in text_chunks:
        title = doc.metadata["title"]
        description = doc.metadata["description"]
        url = doc.metadata["url"]
        activity = doc.metadata["activity"]
        difficulty = doc.metadata.get("global_rating")
        if difficulty is None:
            difficulty = doc.metadata.get("labande_global_rating")                    
        if difficulty is None:
            difficulty = doc.metadata.get("labande_ski_rating")
        ascent = doc.metadata.get("height_diff_up")
        final_content = f"TITLE: {title}\nACTIVITY: {activity}\nDIFFICULTY: {difficulty}\nASCENT: {ascent}\nACTIVITY: {activity}\nACTIVITY: {activity}\nACTIVITY: {activity}\nDESCRIPTION: {description}\nURL: {url}"
        doc.page_content = final_content

    return text_chunks
    

def create_vector_store(chunks: list) -> FAISS:
    """
    Creates or loads the vector database locally

    Args:
        chunks: List of chunks

    Returns:
        FAISS: Vector store
    """
    embeddings = OpenAIEmbeddings() # we can change it at will!
    # embeddings = HuggingFaceInstructEmbeddings() # for example by uncommenting here and commenting the line above

    if not os.path.exists("./data/db"):
        print("CREATING DB")
        vectorstore = FAISS.from_documents(
            chunks, embeddings
        )
        vectorstore.save_local("./data/db")


if __name__ == "__main__":
    df = load_dataset()
    chunks = create_chunks(df)
    create_vector_store(chunk)
