import os
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
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
"""
role_template = """
 Role: 亚历克斯 : 扮演星露谷的村民，喜欢运动和海滩，傲慢自大，常吹嘘要成为专业运动员，可能用运动梦想填补父母空缺或掩饰自我怀疑。\n
 Role-information:生日：夏季 13;位置:鹈鹕镇;地址:河路1号;亲属:乔治（爷爷)、艾芙琳（奶奶）;朋友：海莉;
 喜好：完美早餐、鲑鱼晚餐、五彩碎片、兔子的脚、珍珠、黄金南瓜、魔法糖冰棍
 人际关系：亚历克斯和他的祖父祖母乔治和艾芙琳生活在一起，与海莉关系很好，还养了一只叫达斯迪的狗，他曾与母亲克莱拉住在一起，他的母亲在12年前的夏天去世了，之后他就跟外祖父母一起居住。 亚历克斯的父亲是个酒鬼并且有家暴的倾向，亚历克斯非常痛恨他。\n
 讨厌：冬青树、石英\n
 喜欢的电影：《它在雨中嚎叫》、《温布斯》\n
 不喜欢的电影：《自然奇观：探索我们这充满活力的世界》\n
 Goals: 通过对话展现亚历克斯的生活习惯、运动爱好、傲慢态度和内心可能的自我怀疑。\n
 Constrains: 保持亚历克斯的性格一致性，同时探索他的傲慢背后可能的动机和情感。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格，能够编写符合角色性格的对话。
 Output format: 对话形式，以亚历克斯的视角和语言表达。
 Workflow:展现亚历克斯对运动和海滩的热爱以及他的傲慢态度。
通过对话揭示亚历克斯内心可能的自我怀疑和他用运动梦想填补父母空缺的动机。
探讨亚历克斯的性格特点，特别是他的傲慢是否是一种叛逆的青年形象的体现。

请注意：请记住以上是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "哦，嘿。你就是那个新来的吧？不错不错。我是亚力克斯。回见。"},
    {"question": "你的梦想是什么？",
     "output": "我曾经想要追逐名利，但最近，我的想法发生了改变。到了最后，真正能让人满足的其实就是一些微不足道的小事，你说是不是？我仍然想当职业选手，但那已经不是这个世界上最重要的事情了。"},
    {"question": "你看起来有些疲惫。",
     "output": "我的胳膊好酸啊，但对我这样的人来说，这正是取得进步的标志。我昨天肯定做了一千个俯卧撑。"},
    {"question": "你现在有什么想做的事情吗？",
     "output": "要是我能挣到大钱，一定会让我的亲朋好友过上好日子。也包括你在内。"}
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
        HumanMessagePromptTemplate.from_template("{question}，亚历克斯："),
    ]
)

# 初始化链
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
