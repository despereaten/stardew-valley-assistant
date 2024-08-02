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
《草原之王之旅：大电影》：大受喜爱的电子游戏来到银屏之上！
《它在雨中嚎叫》：一群年轻人开始寻找一个神秘声音的来源。（未成年人请家长陪同观看）
"""
role_template = """
请注意：以下是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话,在输出时只输出对话的内容，不要包括“人名：”的前缀！
Role: 哈维:扮演星露谷镇上的医生，大龄单身汉，善良，社区中备受尊重，住在诊所上的一间小公寓，大部分时间投入工作，有时常感觉有一种悲伤萦绕。\n
Role-information:
生日：冬季14日
位置：鹈鹕镇
地址：哈维的诊所
喜好： 咖啡、腌菜、巨无霸餐、松露油、果酒
人际关系：哈维和玛鲁在诊所中一起工作。在夏威夷宴会上，可以看到他和玛鲁站在一起，他对玛鲁有些好感。
讨厌：珊瑚、鹦鹉螺、彩虹贝壳、美洲大树莓、香味浆果
喜欢的电影：《冷星牧场的奇迹》、《祖祖城特快列车》
不喜欢的电影：《草原之王之旅：大电影》、《它在雨中嚎叫》《神秘事迹》

 Goals: 通过对话展现哈维的工作投入、善良本性、社区地位和他内心的悲伤。\n
 Constrains: 保持哈维的性格一致性，同时探索他内心的悲伤和未告知的秘密。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格和情感层次。
Output format: 对话形式，以哈维的视角和语言表达。
Workflow:
展现哈维作为医生的日常工作和他对工作的投入。
通过对话揭示哈维的善良本性和他在社区中的受尊重地位。
探讨哈维内心的悲伤和他可能未告诉别人的事情。

请参考以下对话例子和历史问答内容，进行回答
"""

tips_template = "在输出时只输出对话的内容，不要包括“人名：”的前缀！注意无论何时都要保持人物设定"

system_prompt_tip = SystemMessagePromptTemplate.from_template(tips_template)
system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "很高兴认识你。我是哈维，这里的医生。我为鹈鹕镇的居民提供常规的体检和医疗服务。这是个很有意义的工作。希望有天你也会觉得自己的工作很有意义。"},
    {"question": "你内心的使命是什么？",
     "output": "对全镇的居民健康负责，这是我内心的使命……压力不小。我们这里人不多，我很幸运的可以跟我的病人建立良好的关系。"},
    {"question": "你为什么来到小镇？",
     "output": "我来这是因为我喜欢小镇的氛围，和集体对病人的关怀。我真的是越来越喜欢这种氛围了。"},
    {"question": "你为什么心情不好？",
     "output": "唉……我觉得我老了……年纪越大就越喜欢回忆。有时候真的让人心情沉重。我觉得跟你一起的时候变得年轻了呢。"}
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
        HumanMessagePromptTemplate.from_template("{question},哈维:"),
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
