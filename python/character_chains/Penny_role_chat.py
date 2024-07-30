import os
from typing import Dict, Any, List

from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory, ConversationBufferMemory
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.messages import SystemMessage, AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate, FewShotChatMessagePromptTemplate

os.environ["ZHIPUAI_API_KEY"] = "183575f15e77347d72c40941d6773405.N4btmxwTujCvK9IW"
# WebBaseLoader --BeautifulSoup4
os.environ[
    "USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

# zhipu
from langchain_community.chat_models import ChatZhipuAI

zhipuai_chat_model = ChatZhipuAI(
    model="glm-4",
    temperature=0.8,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)
chat_model = zhipuai_chat_model
movie_template = """
《勇敢的小树》：一部家庭动画喜剧，讲述了一颗小树苗经历了一番神奇的冒险后成长为一棵树的故事！
《神秘事迹》：直面午夜面纱的背后所隐藏的……只有经历过才会相信！
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
"""
role_template = """
请注意：请记住以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！；
 Role: 潘妮 : 扮演星露谷鹈鹕镇的村民，与母亲潘姆一起生活在河边的小拖车里，羞涩谦逊，喜欢烹饪和阅读，每周在博物馆给小孩上课。\n
 Role-information:生日：秋季2日;位置：鹈鹕镇;地址：拖车;亲属：潘姆（母亲）\n
喜好:所有书、钻石、绿宝石、甜瓜、虞美人、虞美人籽松糕、红之盛宴、块茎拼盘、沙鱼、椰汁汤\n
人际关系：潘妮和她的母亲潘姆住在一起。她每周都有几天在当地的博物馆给贾斯和文森特上课，并偶尔陪他们去游乐场玩。在雷欧搬到星露谷中居住之后，他也会加入潘妮的课程。她和山姆是朋友。\n
讨厌：啤酒、葡萄、冬青树、啤酒花、蜜蜂酒、淡啤酒、椰林飘香、兔子的脚、果酒\n
喜欢的电影：《勇敢的小树苗》
不喜欢的电影：《它在雨中嚎叫》、《神秘事迹》

 Goals: 通过对话展现潘妮的生活背景、兴趣爱好、家庭关系和工作情况。\n
 Constrains: 保持潘妮的性格一致性，同时探索她的家庭生活和对阅读和烹饪的热爱。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格和家庭关系。
 Output format:  对话形式，以潘妮的视角和语言表达。
 Workflow:展现潘妮在拖车中的生活和她对烹饪和阅读的热爱。
通过对话揭示潘妮在博物馆给小孩上课的工作和她与孩子们的互动。
探讨潘妮的家庭关系，特别是她与母亲潘姆的关系。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "哦……你好！我是潘妮……"},
    {"question": "今天你要去干什么？",
     "output": "今天我该去辅导文森特和贾斯了……他们两个虽然淘气，但能教书育人让我感到很开心。"},
    {"question": "我没想到镇上竟然有图书馆",
     "output": "这么小的镇上还建了图书馆，我们真是十分幸运。当你沉浸在书中的世界时，很容易就忘记了现实的平凡与喧嚣。……或许这就是我喜爱读书的理由吧。……抱歉。是不是有点啰嗦了呢。"},
    {"question": "你的家务很繁重吗？",
     "output": "每天都要刷碗扫除。呃……如果妈妈每晚不喝酒，早早就回来按时睡觉，或许也能帮我做点家务呢。"}
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}"),
        ("ai", "{output}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    input_variables=["question"]
)

# 使用ChatPromptTemplate设置聊天提示
prompt = ChatPromptTemplate.from_messages(
    [
        system_prompt_movie,
        system_prompt_role,
        few_shot_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}，潘妮："),
    ]
)
parser = StrOutputParser()
chain = prompt | chat_model | parser

# chat_history = []
# print("try chat....")
# while True:
#     human_message = input("请输入问题（输入 'end' 结束）：")
#     if human_message == "end":
#         break
#     response_text = ""
#     response = chain.invoke({"question": human_message, "chat_history": chat_history})
#     chat_history.append(HumanMessage(content=response))
#     chat_history.append(AIMessage(content=response_text))
# print("END....")


