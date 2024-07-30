import os
from langchain_community.chat_models import ChatZhipuAI
from langchain.chains import ConversationChain
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


os.environ["ZHIPUAI_API_KEY"] = "183575f15e77347d72c40941d6773405.N4btmxwTujCvK9IW"
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
os.environ["SERPAPI_API_KEY"] = "624e55f3f2020f6dd408be77e10d13067ee07a3e2965ce1695519feadabec772"

zhipuai_chat_model = ChatZhipuAI(
    model="glm-4",
    temperature=0.5,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

conversation = ConversationChain(llm=zhipuai_chat_model)


roles = {
    "Alex": "爱好健身，有点小骄傲和自负的体育健将",
    "Abigail": "喜欢大自然，乐观向上的小农场女孩",
    "Elliott": "热爱文学，浪漫梦幻的作家",
    "Emily": "热衷裁缝，对艺术充满热情的设计师",
    "Haley": "时尚潮流，个性独立的时尚达人",
    "Harvey": "医疗专家，温和细心的医生",
    "Leah": "艺术创作，追求独特的自由艺术家",
    "Maru": "科学研究，聪明勤奋的科技爱好者",
    "Penny": "教育工作者，温暖善良的教师",
    "Sam": "音乐才华，充满活力的年轻音乐家",
    "Sebastian": "计算机技术，冷静沉稳的程序员",
    "Shane": "厌世态度，内心敏感的孤独者"
}

questions = [
    "你通常如何度过周末？",
    "当你感到压力时，你通常会选择哪种方式来放松？",
    "你认为自己最突出的个人特质是什么？",
    "你更倾向于独处还是与朋友一起度过时间？",
    "在你的空闲时间，你更愿意做什么活动？",
    "你是否喜欢参与户外活动或自然探险？",
    "你有没有特别的爱好或兴趣，它对你来说意味着什么？",
    "你如何看待艺术和创造力在你的生活中的作用？",
]

answers = []
#
# for question in questions:
#     user_answer = input(f"{question} ")
#     answers.append(user_answer)
#
# combined_answers = " ".join(answers)
# prompt = f"根据以下回答，判断用户最适合的角色：\n\n回答：{combined_answers}\n\n角色定义：{roles}\n\n请给出用户最适合的角色并解释理由."
#
# for chunk in zhipuai_chat_model.astream(input=prompt):
#         print(chunk.content, end="|", flush=True)