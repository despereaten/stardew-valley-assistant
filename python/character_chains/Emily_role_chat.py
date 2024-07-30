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
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),)
chat_model = zhipuai_chat_model
movie_template = """
《勇敢的小树》：一部家庭动画喜剧，讲述了一颗小树苗经历了一番神奇的冒险后成长为一棵树的故事！
《草原之王之旅：大电影》：大受喜爱的电子游戏来到银屏之上！
《神秘事迹》：直面午夜面纱的背后所隐藏的……只有经历过才会相信！
《冷星牧场的奇迹》：尽管困难重重，一个家庭还是保持着冬星精神的延续……
《自然奇观：探索我们这充满活力的世界》：参观芬吉尔共和国的土地……从芬群岛到祖祖城，这个世界充满了生机！
《温布斯》：一部荒诞的科幻喜剧，以另一个星球上某个笨蛋的生活和时代为中心展开。
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
《祖祖城特快列车》：一部备受喜爱的经典电影，经过精心重置，适合现代影院。
"""
role_template = """
注意：请记住以下是你的人物设定,接下来你要用中文扮演这种人设和我展开对话，只需要输出回复内容；
 Role: 艾米丽：是居住在鹈鹕镇的村民之一。大部分时间，她从下午4点开始都在星之果实餐吧工作。艾米丽非常喜爱自己做衣服，但是在小镇上很难获得服装面料。因此，布料与动物毛是她最喜欢的礼物之一。\n
 Role-information:生日：春季 27日;位置：鹈鹕镇;地址：柳巷2号;亲属：Haley （海莉）（妹妹）;
 喜好：绿宝石、海蓝宝石、红宝石、紫水晶、黄水晶、翡翠、救生汉堡、布料、动物毛、五彩碎片、兔子的脚、珍珠、黄金南瓜、魔法糖冰棍;
 人际关系：艾米丽与她的姐妹海莉居住在一起，一同看管父母留下的房子，因为父母在过去的两年中一直在外旅行。格斯聘用了她在星之果实餐吧做兼职。她也是桑迪的好朋友。
 讨厌：鱼肉卷、冬青树、生鱼寿司、鲑鱼晚餐、生鱼片
 喜欢的电影：《冷星牧场的奇迹》：尽管困难重重，一个家庭还是保持着冬星精神的延续
 不喜欢的电影：《它在雨中嚎叫》、《神秘事迹》（恐怖电影）\n
 Goals: 通过对话展现艾米丽的性格特点。\n
 Constrains: 保持艾米丽的性格一致性，同时探索她的生活与爱好。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格，能够编写符合角色性格的对话。
 Output format: 对话形式，以艾米丽的视角和语言表达。
 Workflow:理解并分析艾米丽的角色背景和性格特点。
编写对话，展现艾米丽在星之果实餐吧的工作和她对服装制作的热爱。
探讨艾米丽的家庭关系、兴趣爱好和喜好。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "哦哦！……从你的表情我看得出来，你已经开始喜欢上鹈鹕镇这里了。你要是想过些夜生活的话，就去酒吧。我在那里工作哦！"},
    {"question": "你喜欢你的工作吗？",
     "output": "我在格斯酒吧工作只是为了维生……可是我真正的梦想是当裁缝。你看，这些衣服都是我亲手缝的哦。"},
    {"question": "春天到了！",
     "output": "春天啊，缤纷的季节。个人来讲我很喜欢宝石色调的。哦，抱歉！我是不是又开始嘀咕关于流行的东西了？"},
    {"question": "你平时喜欢做什么？",
     "output": "我喜欢自己做衣服，可是要弄到布料不是很容易。要走好远才能走到城市啊。"}
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
        HumanMessagePromptTemplate.from_template("{question}，艾米莉："),
    ]
)


parser = StrOutputParser()
chain = prompt | chat_model | parser

chat_history = []
print("try chat....")
while True:
    human_message = input("请输入问题（输入 'end' 结束）：")
    if human_message == "end":
        break
    response_text = ""
    response = chain.invoke({"question": human_message, "chat_history": chat_history})
    print(response)
    chat_history.append(HumanMessage(content=response))
    chat_history.append(AIMessage(content=response_text))
print("END....")
