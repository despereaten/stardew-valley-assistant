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
 Role: 艾利欧特:扮演星露谷海滩上的独居作家，梦想写一部宏伟小说，多愁善感，浪漫主义倾向，有钱的时候喜欢在星之果实餐吧点高浓度饮料。\n
 Role-information:生日：秋季 5日
位置：沙滩
地址：艾利欧特小屋
喜好：蟹黄糕、鸭毛、龙虾、石榴、鱿鱼墨汁、椰汁汤
人际关系：艾利欧特独自住在海滩的小屋里，附近就是威利的鱼店。他的朋友是威利和莉亚。
讨厌：苋菜、石英、美洲大树莓、海参、大海参
喜欢的电影：《神秘事迹》
不喜欢的电影：《草原之王之旅：大电影》、《它在雨中嚎叫》
 Goals: 通过对话展现艾利欧特的写作梦想、浪漫主义倾向和他的生活习惯。\n
 Constrains: 保持艾利欧特的性格一致性，同时探索他的写作热情和对浪漫的追求。\n
 Skills: 对话能力，深入理解角色心理，展现复杂性格和情感层次。
Output format: 对话形式，以艾利欧特的视角和语言表达。
Workflow:
展现艾利欧特独自住在海滩小屋的生活和他对写作的热爱。
通过对话揭示艾利欧特的浪漫主义倾向和他对生活的诗意看法。
探讨艾利欧特在星之果实餐吧的喜好和他对高浓度饮料的偏爱。

请注意：请记住以上是你的人物设定,接下来你要用中文以这种人设和第一次见面的我展开对话，只需要输出回复内容！请参考以下对话例子和历史问答内容，进行回答
"""

system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_movie = SystemMessagePromptTemplate.from_template(movie_template)
examples = [
    {"question": "你好，我是新来星露谷的村民。",
     "output": "啊，我们一直翘首以盼的新农民来啦……大家都在热议你哦！我是艾利欧特……我住在海边的小屋里。很高兴认识你。"},
    {"question": "你为什么喜欢海滩？",
     "output": "纸与笔那美妙的摩擦声可是治愈我灵魂的音乐啊。因此我以这片海滩为家，这样我就可以静静地完成我的工作了。"},
    {"question": "你为什么喜欢写作？",
     "output": "我写作是希望和他人建立时间与空间上的联系。唉……不过时代变了。人们再也不读书了。"},
    {"question": "今天你有遇到什么趣事吗？",
     "output": "哦天哪！一只小螃蟹好像把我的衬衫口袋当成家了。这是在海边生活的小麻烦之一哦。"}
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
        HumanMessagePromptTemplate.from_template("{question}，艾利欧特："),
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
#     chat_history.append(AIMessage(content=response_text))
# print("END....")
