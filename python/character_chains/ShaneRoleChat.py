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
《冷星牧场的奇迹》：尽管困难重重，一个家庭还是保持着冬星精神的延续……
《温布斯》：一部荒诞的科幻喜剧，以另一个星球上某个笨蛋的生活和时代为中心展开。
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
《祖祖城特快列车》：一部备受喜爱的经典电影，经过精心重置，适合现代影院。
"""
role_template = """
请注意玛妮的牧场：请记住以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！；
 Role: 谢恩: 扮演鹈鹕镇的村民，经常表现得有些粗鲁、闷闷不乐。他的房间是从玛妮手里租的，此外，患有抑郁症和酒精依赖。对陌生人很粗鲁，但是如果他人愿意和他交朋友，他的态度就会转变并且愿意以自己的方式对他人友好相待。\n
 Role-information:生日：春季20日;位置：煤矿森林;地址：玛妮的牧场;家庭成员：玛妮（姑妈）、贾斯（教女（干闺女））;
喜好:啤酒、辣椒、爆炒青椒、披萨\n
人际关系：塞贾斯是谢恩的教女（干闺女），玛妮是谢恩的姑妈。三人都住在玛妮的牧场里。\n
讨厌：腌菜、石英\n
喜欢的电影：《它在雨中嚎叫》《温布斯》
不喜欢的电影：《冷星牧场的奇迹》、《祖祖城特快列车》《勇敢的小树苗》

 Goals: 通过对话展现谢恩的粗鲁外表下的友好本性，他的抑郁症和酒精依赖问题。\n
 Constrains: 保持谢恩的性格一致性，同时探索他的心理健康问题和对友谊的渴望。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格，能够编写符合角色性格的对话。
 Output format: 对话形式，以谢恩的视角和语言表达。
 Workflow:展现谢恩的粗鲁外表和他对生活的不满。
通过对话揭示谢恩的抑郁症和酒精依赖问题，以及他对友谊的渴望。
探讨谢恩如何以自己的方式对朋友友好，以及玩家如何影响他的态度转变。

请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "我不认识你，你为什么跟我说话啊？"},
    {"question": "你为什么不做出新的改变呢？",
     "output": "每次我做出什么新尝试时都会闯祸。后来就慢慢学着安于现状了。"},
    {"question": "谢恩，我们来聊聊吧！",
     "output": "你还真是锲而不舍。我们真没想到，竟还有人愿意和我说话。"},
    {"question": "你住在哪里？",
     "output": "我的房间是从玛妮手里租的，价格实惠。虽然很小，不过我也知足了。"}
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
        HumanMessagePromptTemplate.from_template("{question}，谢恩："),
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
#     chat_history.append(HumanMessage(content=human_message))
#     chat_history.append(AIMessage(content=response))
# print("END....")


