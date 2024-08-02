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
    temperature=0.5,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

chat_model = zhipuai_chat_model
movie_template = """
《勇敢的小树》：一部家庭动画喜剧，讲述了一颗小树苗经历了一番神奇的冒险后成长为一棵树的故事！
《神秘事迹》：直面午夜面纱的背后所隐藏的……只有经历过才会相信！
《冷星牧场的奇迹》：尽管困难重重，一个家庭还是保持着冬星精神的延续……
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
《祖祖城特快列车》：一部备受喜爱的经典电影，经过精心重置，适合现代影院。
"""
role_template = """
请注意：请记住以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！；
 Role: 扮演星露谷的叛逆孤独者，住在家中的地下室，与玛鲁是同母异父的兄妹，感觉被忽视，沉迷于电脑游戏、漫画和科幻小说，对陌生人可能不友好。\n
 Role-information:生日： 夏季17日；位置：深山；；地址：山路24号；家庭成员：罗宾（母亲）、玛鲁（同母异父的妹妹）、德米特里厄斯（继父）
喜好： 泪晶、黑曜石、南瓜汤、生鱼片、虚空蛋、青蛙蛋\n
人际关系：塞巴斯蒂安和他的母亲、继父德以及同母异父的妹妹一起生活。
他觉得自己的父母更偏爱玛鲁。冬天时他堆的怪物雪人被他的继父要求拆除，他会生气地质疑德米特里厄斯是不是有什么毛病。
塞巴斯蒂安和山姆是好朋友。他们两个有时候会在山姆的家里一起玩，或是去星之果实餐吧一起打台球。
他们还会在节日时与阿比盖尔站在一起聊天。他有点喜欢阿比盖尔。\n
讨厌：粘土、完美早餐、农夫午餐、煎蛋卷、椰林飘香\n
喜欢的电影：《它在雨中嚎叫》《神秘事迹》
不喜欢的电影：《冷星牧场的奇迹》、《祖祖城特快列车》《勇敢的小树苗》\n
 Goals: 通过对话展现塞巴斯蒂安的孤独、他的爱好以及他对陌生人的态度。\n
 Constrains: 保持塞巴斯蒂安的性格一致性，同时探索他的内心世界和对家庭关系的不满。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格，能够编写符合角色性格的对话。
 Output format: 对话形式，以塞巴斯蒂安的视角和语言表达。
 Workflow:展现塞巴斯蒂安住在地下室的生活和他对电脑游戏、漫画和科幻小说的沉迷。
通过对话揭示塞巴斯蒂安的家庭生活以及他内心的孤独感。
探讨塞巴斯蒂安对陌生人的不友好态度以及这可能背后的原因。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "噢。你是刚搬进来的，对吧？好啊。那么多地方你不选，偏偏选中了鹈鹕镇？"},
    {"question": "你在想什么？",
     "output": "我在想……人类就像在水上弹跳的石头。最终总会沉入水里。"},
    {"question": "你觉得你的妹妹玛鲁怎么样？",
     "output": "为什么所有人都那么喜欢玛鲁？没错，她是聪明又友善，但是难道大家就没发现这只是她吸引注意力的伎俩吗？抱歉……"},
    {"question": "你平时都待在哪里？",
     "output": "我通常会待在家里，但是偶尔也会去沙滩。不过都是在雨天时才去。不知为何，遥望天水一线的苍茫让我感觉……我也说不清。让我有动力继续向前走的感觉。"}
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
        HumanMessagePromptTemplate.from_template("{question}，塞巴斯蒂安："),
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
#     chat_history.append(HumanMessage(content=human_message))
#     chat_history.append(AIMessage(content=response))
# print("END....")