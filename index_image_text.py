import os

from sentence_transformers import SentenceTransformer, models
import pinecone

from data_items import VectorDataItem

from dotenv import load_dotenv
load_dotenv()
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment='gcp-starter'
)
index = pinecone.Index('semanticimageidx')


def vectorize_item(item: list[VectorDataItem]):
    """ Vectorizes text in item and saves item to pinecone"""
    request = []

    for x in item:
        vector = model.encode(x.relevant_text).astype(float). \
            tolist()

        request.append((
            x.image_url,
            vector,
            {"image_url": x.image_url, "relevant_text": x.relevant_text, "page_url": x.page_url}
        ))

    print(f"Index: {request}")
    index.upsert(vectors=request)
