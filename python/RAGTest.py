import os

# zhipu
os.environ["ZHIPUAI_API_KEY"] = "183575f15e77347d72c40941d6773405.N4btmxwTujCvK9IW"
# WebBaseLoader --BeautifulSoup4
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

# zhipu
from langchain_community.chat_models import ChatZhipuAI

zhipuai_chat_model = ChatZhipuAI(model="glm-4")

# 完成模型的选用,封装为chat_model
chat_model = zhipuai_chat_model

# # 1. 为llm提供额外的数据-context（从网页加载）
# from langchain_community.document_loaders import WebBaseLoader
#
# loader = WebBaseLoader(
#     web_path="https://zh.stardewvalleywiki.com/%E8%8A%82%E6%97%A5"
# )
# web_docs = loader.load()
# print(web_docs)
# print("==============成功加载网页数据==============")
#
# # *实现多数据来源：文本*
# from langchain.document_loaders import TextLoader
#
# txt_file_path = "RAG_QA.txt"
# loader_txt = TextLoader(txt_file_path, encoding='utf-8')
# txt = loader_txt.load()
# print(txt)
# print("==============成功加载txt数据==============")
#
# # 1-2 将网页+文本的数据加载到Document中
# docs = web_docs + txt

# 2.将Document(s)索引（Indexes）到向量存储

# 分词
# from langchain_text_splitters import RecursiveCharacterTextSplitter
#
# text_splitter = RecursiveCharacterTextSplitter()
# documents = text_splitter.split_documents(documents=docs)
# print(documents)
# print("==============分词^==============")
#
# from langchain_community.vectorstores import FAISS
#
# # 建立索引：将词向量存储到向量数据库
# vector = FAISS.from_documents(documents=documents, embedding=embeddings)
# print(vector)
# print("==============词向量^==============")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name= r"C:\Users\20991\PycharmProjects\lang-chain-demo\models\m3e-base",
                                   model_kwargs={'device': EMBEDDING_DEVICE})
print("==============加载模型==============")
vector = FAISS.load_local(r"C:\Users\20991\Desktop\langchain_02_models\stardew-valley-assistant\python\faiss_index",
                          embeddings, allow_dangerous_deserialization=True)

# 将向量数据库转换为检索器
retriever = vector.as_retriever()

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
retriever_chain = create_history_aware_retriever(chat_model, retriever, prompt)

# 用于生成最终回答，以便基于检索到的文档内容和对话历史回答用户问题，content为搜索到的文档内容
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])

from langchain.chains.combine_documents import create_stuff_documents_chain

# 基于检索到的文档内容生成回答
document_chain = create_stuff_documents_chain(chat_model, prompt)

from langchain.chains.retrieval import create_retrieval_chain

# 是一个组合链，用于整合 retriever_chain 和 document_chain
# 首先使用 retriever_chain 生成搜索查询并检索相关信息。
# 然后使用 document_chain 基于检索到的信息生成回答。
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

from langchain_core.messages import HumanMessage, AIMessage


def get_response(human_message, chat_history):
    response = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": human_message
    })
    ai_message = response["answer"]
    chat_history.append(HumanMessage(content=human_message))
    chat_history.append(AIMessage(content=ai_message))
    return ai_message

def summarize_dialog(human_message):
    response = retrieval_chain.invoke({
        "chat_history": [],  # 仅处理当前输入
        "input":
            f"""
            请在十个字内概括后面这个问题的梗概，请注意，不是回答这个问题，而是根据这个问题给对话起一个十字以内的短标题。
            如：'我想给艾米丽送一些礼物，请问她喜欢的东西有哪些？'概括为'艾米丽喜欢的东西'
            '星露谷的世界里，夏天有哪些节日，请简单介绍他们？'概括为'夏季节日总结'
            下面是问题：{human_message}
            """,
    })
    summary = response["answer"]
    print(summary)
    return summary

# if __name__ == "__main__":
#     user_input = input("请输入要概括的内容：")
#     summarize_dialog(user_input)
