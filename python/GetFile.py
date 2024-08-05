# # 本文档仅需运行一次，获得faiss_index即可
# import time
# from langchain_core.documents import Document
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import re
#
# # The base URL of the site to crawl
# base_url = "https://zh.stardewvalleywiki.com/%E6%9D%91%E6%B0%91"
#
#
# # Function to get all unique URLs containing the base URL
# def get_unique_urls(base_url):
#     response = requests.get(base_url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Find all links in the page
#     links = soup.find_all('a', href=True)
#
#     # Extract and normalize URLs
#     urls = set()
#     for link in links:
#         href = link['href']
#         full_url = urljoin(base_url, href)
#         if re.match(r'https://zh\.stardewvalleywiki\.com/%', full_url):
#             urls.add(full_url)
#
#     return urls
#
#
# # Fetch the unique URLs
# unique_urls = get_unique_urls(base_url)
#
#
# def fetch_page_content(url):
#     try:
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         response.raise_for_status()
#         return response.text
#     except requests.RequestException as e:
#         print(f"Failed to fetch {url}: {e}")
#         return None
#
#
# documents = []
#
# for url in unique_urls:
#     content = fetch_page_content(url)
#     if content:
#         soup = BeautifulSoup(content, 'html.parser')
#         text = soup.get_text()
#         documents.append({"url": url, "text": text})
#         time.sleep(1)  # 避免过于频繁的请求
#
# print("========爬取文本数据=========")
#
# import mysql.connector
#
# #1. 在MySQL中创建schemas（我命名为：stardew）
# # CREATE TABLE IF NOT EXISTS data (
# #     id INT AUTO_INCREMENT PRIMARY KEY,
# #     url VARCHAR(255) UNIQUE,
# #     content TEXT
# # )
#
# # 连接到 MySQL 数据库
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="wyx360124632",  # 更改为自己的密码
#     database="stardew"  # schema的名称
# )
#
# cursor = connection.cursor(dictionary=True)
#
# # 将文档插入到数据库中
# for doc in documents:
#     try:
#         cursor.execute("INSERT INTO data (url, content) VALUES (%s, %s)", (doc['url'], doc['text']))
#     except mysql.connector.IntegrityError as e:
#         continue
#     # 提交事务
#     connection.commit()
#
# # 提交事务
# connection.commit()
#
# # 关闭连接
# cursor.close()
# connection.close()
#
# # 从 MySQL 加载数据
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="wyx360124632",
#     database="stardew"
# )
#
# cursor = connection.cursor(dictionary=True)
# cursor.execute("SELECT content FROM data")
# rows = cursor.fetchall()
#
# documents = [Document(page_content=row['content']) for row in rows]
#
# # 关闭数据库连接
# cursor.close()
# connection.close()
# print("=======存储到MySQL数据库^===========")
#
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

# 1-1 遍历文件夹，逐一加载并累积所有文档
base_dir = "..\\mydocuments"  # 文档存放目录
documents = []

for filename in os.listdir(base_dir):
    # 构建完整文件名
    file_path = os.path.join(base_dir, filename)
    # 分别加载不同文件
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif filename.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
    elif filename.endswith(".txt"):
        loader = TextLoader(file_path, encoding='utf-8')  # 指定编码
        documents.extend(loader.load())

# 3.分词和向量化
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 分词
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
split_documents = text_splitter.split_documents(documents=documents)
print(split_documents)
print("==============分词^==============")

# 加载分词和向量化模型
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name=r"C:\Users\20991\PycharmProjects\lang-chain-demo\models\m3e-base",
                                   model_kwargs={'device': EMBEDDING_DEVICE})
print("=============加载分词和向量化模型============")

# 建立索引：将词向量存储到向量数据库
from langchain_community.vectorstores import FAISS

vector = FAISS.from_documents(documents=split_documents, embedding=embeddings)
print("==============词向量^==============")

# 保存FAISS索引到磁盘
vector.save_local("faiss_index")

# 4: 加载FAISS索引和检索数据
from langchain_community.vectorstores import FAISS

# 从磁盘加载FAISS索引
vector = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vector.as_retriever()
