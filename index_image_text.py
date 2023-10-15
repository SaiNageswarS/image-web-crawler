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


def vectorize_item(item: VectorDataItem):
    """ Vectorizes text in item and saves item to pinecone"""
    vector = model.encode(item.relevant_text).astype(float)
    index.upsert(vectors=[
        (
            item.image_url,
            vector,
            {"image_url": item.image_url, "relevant_text": item.relevant_text, "page_url": item.page_url}
        )
    ])
