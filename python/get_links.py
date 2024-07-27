import os
import re
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage

# 设置环境变量
os.environ["ZHIPUAI_API_KEY"] = "183575f15e77347d72c40941d6773405.N4btmxwTujCvK9IW"
os.environ[
    "USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

# 初始化 ChatZhipuAI 模型
zhipuai_chat_model = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)


def get_links(human_message):
    response = zhipuai_chat_model.invoke([HumanMessage(content=f"""
        请根据我感兴趣的题材获取一些和星露谷有关的网页链接列表（请提供准确的网址），我感兴趣的题材是：{human_message}
        别的文字都不需要，只提供准确的网址。
        你可以从星露谷维基获取页面，也可以从新浪微博，小红书，youtube，bilibili等平台获取页面。
        请按照'''
        1. https://xxxxxxxx
        2. https://xxxxxxxx
        3. https://xxxxxxxx
        4. https://xxxxxxxx
        5. https://xxxxxxxx
        6. https://xxxxxxxx
        7. https://xxxxxxxx
        8. https://xxxxxxxx
        9. https://xxxxxxxx
        10. https://xxxxxxxx
        '''的格式输出列表，不允许有任何多余的文字
    """)])

    # 获取 AIMessage 对象的内容
    res = response.content

    # 输出返回的完整响应，便于调试
    print(res)

    # 定义更通用的正则表达式模式
    pattern = r'https?://[^\s]+'

    # 使用正则表达式查找所有匹配的链接
    links = re.findall(pattern, res)
    return links


if __name__ == '__main__':
    user_input = input("请输入感兴趣的关键词: ")
    links = get_links(user_input)
    print(links)
