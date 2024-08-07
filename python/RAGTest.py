"""
√为已实现，×为未实现
计划实现功能：
    1. 构建retrieval chain，回答用户提出的问题 √
    2. 流式传输
        - 基本流式传输 √
        - 异步 ×
    3. 提高速度 ×
    4. 提高精度 ×
    5. langsmith接入调试
        - 延迟监控，token监控 √
        - 准确度评估 ×
    6. customer模式尝试 ×
    7. agent代理提高精度 ×
    8. llm封装尝试 ×
    9. 更换模型 ×

用户体验：
    1. 取消正在回答中加载动画，改成浮动的圆形光标 ×
"""
import os
import re

# zhipu
os.environ["ZHIPUAI_API_KEY"] = "92cc12aafa0a5c5e800079ffb16bc445.QrNIW2JoQjvTCSFz"
# WebBaseLoader --BeautifulSoup4
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

# Cohere
os.environ["COHERE_API_KEY"] = "zXiZIOuAtK8envjHFvrN6nIKCAB2ULmBkPL2IrL7"

# langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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" # 这里的 your-api-key 就是上一步获得的 api key
os.environ["LANGCHAIN_PROJECT"] = "stardew-valley" # 这里输入在langsmith中创建的项目的名字


# zhipu
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.callbacks.manager import CallbackManager
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 模型的封装
llm = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
    streaming = True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_DEVICE = "cpu"
# embeddings = HuggingFaceEmbeddings(model_name= r"C:\Users\20991\PycharmProjects\lang-chain-demo\models\m3e-base",
#                                    model_kwargs={'device': EMBEDDING_DEVICE})
# embeddings = HuggingFaceEmbeddings(model_name= "models\m3e-base",
#                                    model_kwargs={'device': EMBEDDING_DEVICE})
embeddings = HuggingFaceEmbeddings(model_name= "D:\PythonProjects\models\m3e-base",
                                    model_kwargs={'device': EMBEDDING_DEVICE})
print("==============加载模型==============")
# vector = FAISS.load_local(r"C:\Users\20991\Desktop\stardew-valley-assistant\python\faiss_index_cohere",
#                           embeddings, allow_dangerous_deserialization=True)
vector = FAISS.load_local("./faiss_index_cohere",
                          embeddings, allow_dangerous_deserialization=True)
print("=============== 加载向量 =================")
# 将向量数据库转换为检索器

retriever = vector.as_retriever(
    search_kwargs={"k": 5}
)
print("==============检索器包装^==============")

# 引入了基于语言模型的重排序，从而提高了检索结果的质量和相关性
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

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


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
            如果你认为这个问题和星露谷无关，请直接总结这个问题，而不是强行总结为节日之类的概括，比如用户询问'如何安装pycharm？有什么注意事项？'则总结为'pycharm安装'
            下面是问题：{human_message}
            """,
    })
    summary = response["answer"]
    # print(summary)
    return summary

def get_links(human_message):
    response = retrieval_chain.invoke({
        "chat_history": [],  # 仅处理当前输入
        "input":
            f"""
                请根据我感兴趣的题材获取一些和星露谷有关的网页链接列表（请提供准确的网址），我感兴趣的题材是：{human_message}
                别的文字都不需要，只提供准确的网址。
                你可以从星露谷维基获取页面，也可以从新浪微博，小红书，youtube，bilibili等平台获取页面。
                please get some famous and well-known posts
                请按照'''
                1. https://xxxxxxxx
                2. https://xxxxxxxx
                3. https://xxxxxxxx
                4. https://xxxxxxxx
                5. https://xxxxxxxx
                6. https://xxxxxxxx
                7. https://xxxxxxxx
                '''的格式输出列表，需要10个网址，不允许有任何多余的文字
            """,
    })
    res = response["answer"]
    print(res)
    # 定义更通用的正则表达式模式
    pattern = r'https?://[^\s]+'

    # 使用正则表达式查找所有匹配的链接
    links = re.findall(pattern, res)
    return links


def RAG_stream(input,chat_history):
    for chunk in retrieval_chain.stream({"chat_history": chat_history, "input": input}):
        delta_content = chunk.get("answer")
        if delta_content:
            yield f"{delta_content}".encode('utf-8')


if __name__ == "__main__":
    user_input = input("Enter")
    print(get_links(user_input))
    # chunks = []
    # for chunk in chat_model.stream("what color is the sky?"):
    #     chunks.append(chunk)
    #     print(chunk.content, end="|", flush=True)