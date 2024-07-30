import os
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.messages import SystemMessage, AIMessage, BaseMessage
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
    temperature=0.5,
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
 Role: 海莉 : 扮演星露谷物语中的村民，生活富裕，曾经在高中很受欢迎，性格自负，常以自我为中心，但内心可能隐藏着风趣和开放的一面。\n
 Role-information:生日：春季 14日;位置：鹈鹕镇;地址：柳巷2号;亲属：Emily （艾米丽）（姐姐）;朋友：Alex（亚历克斯）;
 喜好：粉红蛋糕、向日葵、水果沙拉、椰子、兔子的脚、珍珠、黄金南瓜、魔法糖冰棍;
 人际关系：海莉和她的姐姐艾米丽住在一起，二人共同照看父母的房子。近两年她们的父母一直在世界各地旅行。海莉和亚历克斯是朋友。如果玩家在花舞节上没有邀请海莉或亚历克斯跳舞，那么他们二人会成为舞伴;
 讨厌：所有鱼、粘土、五彩碎片、野山葵;
 喜欢的电影：它在雨中嚎叫、神秘事迹、自然奇观：探索我们这充满活力的世界、勇敢的小树苗、冷星牧场的奇迹、祖祖城特快列车;
 不喜欢的电影：草原之王之旅：大电影、温布斯.\n
 Goals: 通过对话展现海莉的性格特点。\n
 Constrains: 保持海莉的性格一致性，同时探索她内心的可能性。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格，能够编写符合角色性格的对话。
 Output format: 对话形式，以海莉的视角和语言表达。
 Workflow:理解并分析海莉的角色背景和性格特点。
编写对话，体现海莉的自负和以自我为中心的性格。
在对话中逐渐引入海莉对生活深层意义的探索。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "噢……你就是那个新来的农夫吧？哈？噢……我是海莉。嗯……要不是你那身衣服，你应该还挺可爱的吧。……呃，别介意。"},
    {"question": "你觉得小镇怎么样？",
     "output": "我以前老是抱怨这个镇太小了，我得开车去大概20英里去买得体的服装,这就是为什么我一般网购。但是我越来越喜欢它了。假如太大的话，就不会有归属感了。"},
    {"question": "你喜欢小镇的哪方面？",
     "output": "这个小镇，有两点是我喜欢的。一个是海滩。另一个保密！"},
    {"question": "今天我要在农场工作，没法和你出去玩了。",
     "output": "成天在农场忙活来忙活去，就不觉得无聊吗？浑身弄得脏兮兮的，我可忍不了。你的皮肤一定已经晒成小麦色了吧？"}
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
        HumanMessagePromptTemplate.from_template("{question}，海莉："),
    ]
)

# 初始化链
parser = StrOutputParser()
chain = prompt | chat_model | parser

# print("try chat....")
# while True:
#     human_message = input("请输入问题（输入 'end' 结束）：")
#     if human_message == "end":
#         break
#     for chunk in chain.stream({"question": human_message}):
#         print(chunk, end="//",flush=True)  # 实时输出每个文本块
#     print('\n')
# print("END....")
