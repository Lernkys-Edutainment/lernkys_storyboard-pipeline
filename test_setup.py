from retriever.chroma_utils import get_collection

collection = get_collection()

print(collection.count())