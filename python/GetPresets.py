import os
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from GetLinks import get_keywords

# 设置环境变量
os.environ["ZHIPUAI_API_KEY"] = "d637342fa757ce4184fb81ec813e461b.rZ53MvqlIlqwUc9X"
os.environ[
    "USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

# 初始化 ChatZhipuAI 模型
zhipuai_chat_model = ChatZhipuAI(
    model="glm-4",
    temperature=0.8,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

# 规定关键词列表范式
response_schemas = [
    ResponseSchema(type="array", name="questions",
                   description="""
                    Please generate a list of questions that are closely related to Stardew Valley in a keyword list, 
                    the questions need to be in Chinese, preferably ten characters or less,
                    and here are the inputs and outputs you can refer to.
                    input:["阿比盖尔","塞巴斯蒂安","钓鱼,"]
                    output:[
                      "怎么追求阿比盖尔效率更高",
                      "塞巴斯蒂安收到礼物的偏好",
                      "星露谷鱼类大全",
                      "塞巴斯蒂安平时喜欢去哪些地方"
                    ]
                    """
    ),
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

import jieba


def get_presets(message_list):
    keywords = get_keywords(message_list)
    promptValue = prompt.format(user_input=f"{keywords}")
    # print("promptValue", promptValue)
    # 确保将 promptValue 包装为 HumanMessage 对象

    model_output = zhipuai_chat_model.invoke(
        [HumanMessage(content=promptValue), AIMessage(content="hi"), SystemMessage(content="you re a robot.")])
    # print("model_output", model_output)

    parsed_output = output_parser.parse(model_output.content)
    # print(parsed_output['keywords'])
    raw_keywords = parsed_output['questions']
    return raw_keywords[-4:]


if __name__ == '__main__':
    response = get_presets([
        "我喜欢阿比盖尔",
        "阿比盖尔喜欢什么礼物？",
        "谢恩有什么爱好？",
        "你好",
        "海莉长得好漂亮",
        "海莉是仙女吧",
        "吴昱欣平时的作息"
        "我是一个钓鱼佬，我在星露谷应该做什么"
    ])
    print(response)