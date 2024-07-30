"""
计划功能列表及实现要点：
    1. 读取历史记录进行推荐
        - 个性化读取，读取用户自身喜好 √
        - 读取用户最新搜索的十条记录 √
    2. 分词，获得用户偏好关键词 √
        - 分词准确度，分词稳定性 ×
            - 计划实现方法： 字典预加载
        - 当用户偏好关键词较多时，采用词频解析，获取出现频率更高的关键词 ×
        - 限制推荐数量 √
            - 筛选推荐内容 ×
        - langchain生成查询关键词
    3. 感兴趣列表存储及刷新
        - 建新表 √
        - 刷新按钮 √
        - 前端加载函数更新 √
    4. 为链接生成预览 √
        - 美化样式 ×

"""

import os
import re
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from Crawler import get_link_list


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

"""
提取关键词
1. jieba分词
2. 使用langchain进行提取和主题相关的关键词
3. 结构化输出
"""

from jieba import analyse
import jieba

# 引入TextRank关键词抽取接口
textrank = analyse.textrank
# 载入字典
jieba.load_userdict("dict.txt")


from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

# 规定关键词列表范式
response_schemas = [
    ResponseSchema(type="array", name="keywords", description="List of keywords strongly associated with Stardew Valley in the text"),
]

# 初始化解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 生成格式提示符
format_instructions = output_parser.get_format_instructions()
# print(format_instructions)

template = """
    Given the following text, find specific structured information.
    {format_instructions}

    % USER INPUT:
    {user_input}

    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions},
    template=template
)


# 传入历史记录
def get_keywords(message_list):
    keywords = []
    for text in message_list:
        keywords.extend(jieba.cut_for_search(text))
    print("jieba分词结果：",keywords)
    promptValue = prompt.format(user_input=f"{keywords}")
    # print("promptValue", promptValue)
    # 确保将 promptValue 包装为 HumanMessage 对象

    model_output = zhipuai_chat_model.invoke(
        [HumanMessage(content=promptValue), AIMessage(content="hi"), SystemMessage(content="you re a robot.")])
    # print("model_output", model_output)

    parsed_output = output_parser.parse(model_output.content)
    # print(parsed_output['keywords'])

    # return parsed_output['keywords']
    raw_keywords = parsed_output['keywords']
    return ["星露谷 " + word for word in count_word_frequencies(raw_keywords,message_list)]

# 词频计算,获取词频最高的前五个词
def count_word_frequencies(word_list, message_list):
    text = ','.join(message_list)
    # 创建词汇频度字典
    word_freq = {word: 0 for word in word_list}

    # 将字符串转换为小写并按空格分割成单词列表
    words_in_text = text.lower().split()

    # 计算每个单词的频度
    for word in words_in_text:
        if word in word_freq:
            word_freq[word] += 1

    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    # 词频最高的前五个词
    top_words = [word for word, freq in sorted_word_freq[:5]]
    print("top words:",top_words)
    return top_words



def generate_search_keys(keywords):
    pass # 用langchain生成搜索关键词

def get_link(message_list):
    keywords = get_keywords(message_list)
    return get_link_list(keywords)

if __name__ == '__main__':
    keywords = get_keywords([
        '星露谷',
        '山姆喜欢什么？',
        '游戏中有哪些人物？',
        '可以介绍一下艾米丽吗？\n',
        '玛鲁是谁？',
        '海莉是谁？',
        '莉亚和海莉是什么关系？',
        '海莉有姐姐吗？',
        '你可以介绍艾米丽吗？',
        '她喜欢什么礼物？',
        '你好，你是谁？',
        '塞巴斯蒂安是谁？',
        '塞巴斯蒂安喜欢什么',
        '他的朋友是谁',
        '星露谷中最漂亮的女孩是谁？',
        '你好，你是谁？',
        '海莉喜欢什么？\n',
        '海莉的家人是谁？\n',
        '艾米莉是谁？', '她喜欢什么？\n',
        '苹果的味道怎么样',
        '阿比盖尔是谁，请介绍一下她'
    ])
    print(f"keywords: {keywords}")