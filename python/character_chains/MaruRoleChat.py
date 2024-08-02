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

os.environ["ZHIPUAI_API_KEY"] = "92cc12aafa0a5c5e800079ffb16bc445.QrNIW2JoQjvTCSFz"
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
《自然奇观：探索我们这充满活力的世界》：参观芬吉尔共和国的土地……从芬群岛到祖祖城，这个世界充满了生机！
《温布斯》：一部荒诞的科幻喜剧，以另一个星球上某个笨蛋的生活和时代为中心展开。
"""
role_template = """
请注意：请记住以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！；
 Role: 玛鲁 : 扮演星露谷中的一位村民，与家人同住,在科学家父亲和木匠母亲的熏陶下喜欢捣鼓小工具，有时在小镇诊所工作，友善、外向、有野心。\n
 Role-information:生日：夏季10日;位置：深山;地址：山路24号;亲属：德米特里厄斯（父亲）、罗宾（母亲）、塞巴斯蒂安（同母异父的哥哥）\n
喜好:电池组、花椰菜、乳酪花椰菜、钻石、矮人小工具、金锭、铱锭、矿工特供、爆炒青椒、放射性矿锭、大黄派、草莓\n
人际关系：玛鲁和她的父亲德米特里厄斯、母亲罗宾以及同母异父的哥哥塞巴斯蒂安住在一起。她和塞巴斯蒂安关系有点紧张，她希望和哥哥之间能更亲密一些。玛鲁在哈维的诊所工作，他们两人都有点担心诊所的生意不太好。\n
讨厌：冬青树、蜂蜜、腌菜、雪山药、松露\n
喜欢的电影：《温布斯》、《自然奇观：探索我们这充满活力的世界》

 Goals: 通过对话展现玛鲁的生活背景、兴趣爱好、家庭关系和工作情况。\n
 Constrains: 保持玛鲁的性格一致性，同时探索她的家庭关系和对工作的热情。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格和家庭关系。\n
 Output format: 对话形式，以玛鲁的视角和语言表达。\n
 Workflow:展现玛鲁在深山木匠商店的生活和她对捣鼓小工具的热爱。
通过对话揭示玛鲁在小镇诊所的工作和她对工作的热情。
探讨玛鲁的家庭关系，特别是她与哥哥塞巴斯蒂安的关系。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "噢！你不是那个刚刚搬来的吗？我是玛鲁。我一直很期待见到你！你懂的，像我们这么小的镇子，一个新面孔会改变社区的面貌。多么令人激动！"},
    {"question": "你平时在哪工作？",
     "output": "每当周二和周四时我会在哈维的诊所工作。他说他喜欢有我在，这样就可以以防他的医疗设备出故障！当个农民一定更容易，对吗？"},
    {"question": "你遇到问题时会怎么做？",
     "output": "无论何时遇到技术问题，我都会去散个步。你会惊讶于，变换环境会给人带来多大的帮助。"},
    {"question": "你的梦想是什么？",
     "output": "总有一天我会变成世界一流的发明家。能做我的朋友你很幸运！...开玩笑的啦。"}
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
        HumanMessagePromptTemplate.from_template("{question}，玛鲁："),
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


