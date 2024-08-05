import os

os.environ["ZHIPUAI_API_KEY"] = "d637342fa757ce4184fb81ec813e461b.rZ53MvqlIlqwUc9X"
os.environ[
    "USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

from langchain_community.chat_models import ChatZhipuAI
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from Crawler import get_link_list


# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = "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" # 这里的 your-api-key 就是上一步获得的 api key
# os.environ["LANGCHAIN_PROJECT"] = "test" # 这里输入在langsmith中创建的项目的名字

import numpy as np
from chunkdot import cosine_similarity_top_k
import timeit


chat = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
)



# response = chat.invoke([
#     AIMessage(content="Hi."),
#     SystemMessage(content="你是一个星露谷物语的小助手."),
#     HumanMessage(content=input("请输入问题："))])
chunks = []
for chunk in chat.stream("请问星露谷中的阿比盖尔喜欢什么?"):
    chunks.append(chunk)
    print(chunk.content, end="", flush=True)
# print(response.content)