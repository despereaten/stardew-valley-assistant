import os



os.environ["ZHIPUAI_API_KEY"] = "d637342fa757ce4184fb81ec813e461b.rZ53MvqlIlqwUc9X"
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

os.environ["COHERE_API_KEY"] = "zXiZIOuAtK8envjHFvrN6nIKCAB2ULmBkPL2IrL7"

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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" # 这里的 your-api-key 就是上一步获得的 api key
os.environ["LANGCHAIN_PROJECT"] = "stardew-valley" # 这里输入在langsmith中创建的项目的名字

from langchain_community.chat_models import ChatZhipuAI


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader,PyPDFLoader, Docx2txtLoader

base_dir = "..\\mydocuments"  # 文档存放目录
documents = []

for filename in os.listdir(base_dir):
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

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
texts = text_splitter.split_documents(documents)
print("==============分词^==============")

# 加载分词和向量化模型
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name=r"C:\Users\20991\PycharmProjects\lang-chain-demo\models\m3e-base",
                                   model_kwargs={'device': EMBEDDING_DEVICE})
print("=============加载分词和向量化模型============")

# 建立索引：将词向量存储到向量数据库
from langchain_community.vectorstores import FAISS

vector = FAISS.from_documents(documents=texts, embedding=embeddings)
print("==============词向量^==============")

# 保存FAISS索引到磁盘
vector.save_local("faiss_test_cohere")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name= r"C:\Users\20991\PycharmProjects\lang-chain-demo\models\m3e-base",
                                   model_kwargs={'device': EMBEDDING_DEVICE})

vector = FAISS.load_local(r"C:\Users\20991\Desktop\stardew-valley-assistant\python\faiss_test_cohere",
                          embeddings, allow_dangerous_deserialization=True)
print("=============== 加载向量 =================")
# 将向量数据库转换为检索器

retriever = vector.as_retriever(
    search_kwargs={"k": 5}
)
print("==============检索器包装^==============")

from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


llm = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
    streaming = True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

# compressor = CohereRerank(model="rerank-english-v3.0")
compressor = CohereRerank(model="rerank-multilingual-v3.0")
compression_retriever = ContextualCompressionRetriever(
    base_compressor = compressor,base_retriever = retriever
)

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate

# 生成搜索查询，以便在有上下文的情况下检索相关信息
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user",
     "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])

# 用于生成搜索查询并从外部检索信息
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

# 用于生成最终回答，以便基于检索到的文档内容和对话历史回答用户问题，content为搜索到的文档内容
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])

from langchain.chains.combine_documents import create_stuff_documents_chain

# 基于检索到的文档内容生成回答
document_chain = create_stuff_documents_chain(llm, prompt)

from langchain.chains.retrieval import create_retrieval_chain

# 是一个组合链，用于整合 retriever_chain 和 document_chain
# 首先使用 retriever_chain 生成搜索查询并检索相关信息。
# 然后使用 document_chain 基于检索到的信息生成回答。
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)



def generate(input,chat_history):
    for chunk in retrieval_chain.stream({"chat_history": chat_history, "input": input}):
        # delta_content = chunk.choices[0].delta.input
        delta_content = chunk.get("answer")
        if delta_content:
            yield f"{delta_content}".encode('utf-8')

if __name__ == "__main__":
    while True:
        user_input = input("请提问：")
        if user_input == "end":
            print("结束...")
            break
        else:
            chunks = []
            for chunk in retrieval_chain.invoke(user_input):
                # chunks.append(chunk)
                # delta_content = chunk.get("result")
                # if delta_content:
                #     print(delta_content, end="", flush=True)
                print(chunk.content,end="",flush=True)
            # result = generate(user_input)
            # print(result['result'])