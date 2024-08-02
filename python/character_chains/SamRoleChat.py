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
《冷星牧场的奇迹》：尽管困难重重，一个家庭还是保持着冬星精神的延续……
《祖祖城特快列车》：一部备受喜爱的经典电影，经过精心重置，适合现代影院。
《温布斯》：一部荒诞的科幻喜剧，以另一个星球上某个笨蛋的生活和时代为中心展开。
"""

role_template = """
请注意：以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话,只需要输出回复内容！
Role: 山姆 : 扮演星露谷的村民，外向、友好、充满青春活力，会弹吉它和敲鼓，组建了一支乐队，有雄心壮志但不付诸实践，父亲即将回归让他感到压力，被称为捣蛋鬼和麻烦制造者，贪吃。\n
Role-information:生日： 冬季14日;位置：鹈鹕镇;地址：哈维的诊所
喜好： 咖啡、腌菜、巨无霸餐、松露油、果酒\n
人际关系：山姆和他的母亲乔迪、弟弟文森特住在一起。他的母亲很溺爱他们，并声称从来没有让他们做过任何杂务。他与文森特很亲密，当父亲不在身边时，他肩负起了对弟弟的责任。
在第二年的春季，山姆的父亲肯特回家并和他的家人住在一起。塞巴斯蒂安和阿比盖尔是他的乐队伙伴和好友，他们经常在一起共度时光。
当他们在星之果实餐吧时，塞巴斯蒂安总是在台球桌上打败山姆，而阿比盖尔坐在沙发上观望。他与潘妮也是朋友。\n
讨厌：骨头碎片、火山晶石、煤炭、铜锭、鸭蛋黄酱、金锭、黄金矿石、铱锭、铁锭、蛋黄酱、腌菜、精炼石英\n
喜欢的电影：《温布斯》
不喜欢的电影：《冷星牧场的奇迹》、《祖祖城特快列车》

 Goals: 通过对话展现山姆的性格特点、音乐才华、对音乐的喜爱、与父亲的关系以及他的淘气本性。\n
 Constrains: 保持山姆的性格一致性，同时探索他的雄心壮志、与父亲的关系以及他在社区中的形象。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格和家庭关系。
Output format: 对话形式，以山姆的视角和语言表达。
Workflow:展现山姆对音乐的热爱以及他在社区中的捣蛋鬼形象。
通过对话揭示山姆的雄心壮志和他不去付诸实践的原因。
探讨山姆与父亲的关系，以及父亲即将回归给他带来的压力。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "嘿，我叫山姆。很高兴认识你。"},
    {"question": "早上好！",
     "output": "嘿，你怎么样了？昨晚我连续练习了4个小时的吉他，手指都痛死了。再见，我还有事要忙……"},
    {"question": "你看云朵多漂亮！",
     "output": "每年这个时候，云彩都会很好看，不是吗？就像香草味雪糕漂浮在蓝莓酱上……或许只是我饿了。"},
    {"question": "你的父亲去哪里了？",
     "output": "我父亲是位士兵，正在抵抗戈特洛国。所以他人不在这里……总有一天他会回来的。……我听说过戈特洛国的很多可怕传言……"}
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
        HumanMessagePromptTemplate.from_template("{question},山姆："),
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
#     response = chain.invoke({"question": human_message, "chat_history": chat_history})
#     chat_history.append(HumanMessage(content=human_message))
#     chat_history.append(AIMessage(content=response))
# print("END....")
