# -*- coding: utf-8 -*-
"""LangChain Pratice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w7KAK_hHrXZmsRuRmp7DEidvTfhWONs1

reference
langchain doc: https://python.langchain.com/en/latest/
Use LangChain, GPT and Deep Lake to work with code base: https://python.langchain.com/en/latest/use_cases/code/code-analysis-deeplake.html
"""

# We need to set up keys for external services and install necessary python libraries
!python3 -m pip install --upgrade langchain deeplake openai ticktoken

import os
from getpass import getpass

# 到openai申請api key (有免費額度)
# https://platform.openai.com/account/api-keys

# Please manually enter OpenAI Key
os.environ['OPENAI_API_KEY'] = getpass('Open API key:')

# Authenticate into Deep Lake if you want to create your own dataset and publish it. 
# You can get an API key from the platform at app.activeloop.ai
os.environ['ACTIVELOOP_TOKEN'] = getpass('Activeloop Token:')

# Load all repository files. 
# Here we assume this notebook is downloaded as the part of the langchain fork and we work with the python files of the langchain repo.

from langchain.document_loaders import TextLoader

root_dir = '../../../..'

docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        if file.endswith('.py') and '/.venv/' not in dirpath:
            try: 
                loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e: 
                pass
print(f'{len(docs)}')

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
print(f"{len(texts)}")

"""Then embed chunks and upload them to the DeepLake.
This can take several minutes.
"""

from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(disallowed_special=())
embeddings

!pip install tiktoken
from langchain.vectorstores import DeepLake
import tiktoken

db = DeepLake.from_documents(texts, embeddings, dataset_path=f"hub://francescatai/langchain-code")
db