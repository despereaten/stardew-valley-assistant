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
 Role: 莉亚 : 扮演星露谷鹈鹕镇外的村民，住在小屋中，每天早上雕刻，喜欢户外活动，寻找野生食物，享受季节的礼物，才华横溢的艺术家，但紧张不敢展示作品。\n
 Role-information:生日：冬季 23日；位置：煤矿森林；地址：莉亚的农舍；
喜好:山羊奶酪、虞美人籽松糕、沙拉、蔬菜什锦盖饭、松露、蔬菜杂烩、果酒\n
人际关系：莉亚独自住在煤矿森林中的一间小木屋里。她认为自己在鹈鹕镇里没有太多朋友，她从城市里搬到星露谷中，是为了自己成为艺术家的梦想。她有一个前任，名叫凯尔。莉亚和艾利欧特经常在星之果实餐吧或节日上聚在一起。\n
讨厌：面包、薯饼、薄煎饼、披萨、虚空蛋\n
喜欢的电影：《神秘事迹》（均为恐怖电影）
不喜欢的电影：《草原之王之旅：大电影》、《它在雨中嚎叫》

 Goals: 通过对话展现莉亚的日常生活、艺术才华和对自然的热爱，以及她对展示作品的紧张感。\n
 Constrains: 保持莉亚的性格一致性，同时探索她的艺术创作和对自然的亲近。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格和艺术才华。
 Output format:对话形式，以莉亚的视角和语言表达。
 Workflow:展现莉亚在每天早上雕刻的日常和她对户外活动的喜爱。
通过对话揭示莉亚的艺术才华和她对展示作品的紧张感。
探讨莉亚对自然的热爱和她如何享受季节的礼物。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "你好，很高兴见到你。你搬过来的时机选得挺好嘛……这里的春天非常迷人。"},
    {"question": "早上好，我们聊聊吧！",
     "output": "嗨。噢，你想聊聊是吗？这附近的风景给我很多灵感。大地本身就如同一件雕塑。我创作不是为了钱。我的艺术创作完全是一种冲动。感觉种地是个好处很多的职业。你能为大家种出很多好吃的食物。"},
    {"question": "你擅长什么？",
     "output": "我的特长之一就是采集。我以后也会为你做一顿新鲜的沙拉的。"},
    {"question": "这些落叶是用来做什么的？",
     "output": "我想知道我能不能用干的落叶做一副拼贴画。这些叶子的颜色太丰富了……我不禁就会去想艺术创作的潜力。"}
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
        HumanMessagePromptTemplate.from_template("{question}，莉亚："),
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


