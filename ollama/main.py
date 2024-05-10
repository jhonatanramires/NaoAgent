from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model

llm = Ollama(model="unclecode/tinycallama", request_timeout=100)

parser = LlamaParse.result_type="markdown"

result = llm.complete("¿who are you?")

print(result)