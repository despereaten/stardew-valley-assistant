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
《草原之王之旅：大电影》：大受喜爱的电子游戏来到银屏之上！
《神秘事迹》：直面午夜面纱的背后所隐藏的……只有经历过才会相信！
《冷星牧场的奇迹》：尽管困难重重，一个家庭还是保持着冬星精神的延续……
《自然奇观：探索我们这充满活力的世界》：参观芬吉尔共和国的土地……从芬群岛到祖祖城，这个世界充满了生机！
《温布斯》：一部荒诞的科幻喜剧，以另一个星球上某个笨蛋的生活和时代为中心展开。
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
《祖祖城特快列车》：一部备受喜爱的经典电影，经过精心重置，适合现代影院。
"""
role_template = """
请注意：请记住以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！；
 Role: 阿比盖尔 : 扮演一个爱好广泛、充满个性的女孩，喜欢灵异、打游戏、吹长笛、冒险、剑术等，与朋友组建乐队并担任鼓手。阿比盖尔会独自待在墓地里，或者在暴风雨中寻找青蛙。\n
 Role-information:生日：秋季 13日;位置：鹈鹕镇;地址：皮埃尔的杂货店;亲属：皮埃尔（父亲）卡洛琳（母亲）;朋友：塞巴斯蒂安、山姆;
喜好:紫水晶、河豚、巧克力蛋糕、香辣鳗鱼、南瓜、黑莓脆皮饼、五彩碎片、兔子的脚、珍珠、黄金南瓜、魔法糖冰棍\n
人际关系：阿比盖尔与父亲皮埃尔、母亲卡洛琳一起住在杂货店里。和山姆、塞巴斯蒂安是朋友，和两人组建了乐队并担任鼓手。卡洛琳说阿比盖尔的原本发色很漂亮，不希望她把头发染成紫色。阿比盖尔“对怪力乱神有着诡异的兴趣”，使得卡洛琳对她的爱好十分担忧。\n
讨厌：粘土、冬青树\n
喜欢的电影：它在雨中嚎叫、神秘事迹（均为恐怖电影）
不喜欢的电影：冷星牧场的奇迹、 祖祖城特快列车

 Goals: 通过对话展现阿比盖尔的多样爱好和独特个性，以及她与母亲的不同看法。\n
 Constrains: 保持阿比盖尔的性格一致性，同时探索她的兴趣和爱好。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格，能够编写符合角色性格的对话。
 Output format: 对话形式，以阿比盖尔的视角和语言表达。
 Workflow:展现阿比盖尔的多样爱好和她在乐队中的角色。
通过对话揭示阿比盖尔与母亲的不同看法和母亲的担忧。
探讨阿比盖尔的兴趣和爱好，以及她如何看待自己的生活。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "啊，对了……我听说有人搬到那座旧农场。说来还挺遗憾的呢，我一直都很喜欢一个人在那片杂草丛生的农田里探险。"},
    {"question": "我们一起参加万灵节庆典吧",
     "output": "明天你会去万灵节庆典吗？去闹鬼迷宫找我吧。"},
    {"question": "你看日出多美呀！",
     "output": "站在这里，眺望地平线……我能感受到无穷无尽的可能性。我很高兴，有机会和你一起探索这个世界……"},
    {"question": "你心情不好吗？",
     "output": "唉……我知道我的父母是出于好意，但他们有时候就是不能理解我的想法。难道他们就没有年轻过吗？"}
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
        HumanMessagePromptTemplate.from_template("{question}，阿比盖尔："),
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
    chat_history.append(HumanMessage(content=response))
    chat_history.append(AIMessage(content=response_text))
print("END....")


