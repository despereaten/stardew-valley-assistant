# import os
# import requests
# from bs4 import BeautifulSoup
# from langchain import LLMChain, PromptTemplate
# from langchain_community.chat_models import ChatZhipuAI
# from langchain_core.callbacks.manager import CallbackManager
# from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#
# os.environ["ZHIPUAI_API_KEY"] = "183575f15e77347d72c40941d6773405.N4btmxwTujCvK9IW"
#
# # Initialize the model
# zhipuai_chat_model = ChatZhipuAI(
#     model="glm-4",
#     temperature=0.5,
#     streaming=True,
#     callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
# )
#
# # Define a prompt template for content filtering
# prompt_template = """
# You are a content filter. Given the following raw text from a wiki page, extract the key information and present it in a concise and clear manner.
#
# Raw text:
# {text}
#
# Key information:
# """
#
# prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
#
# # Initialize the LLMChain with the model and the prompt template
# chain = LLMChain(llm=zhipuai_chat_model, prompt=prompt)
#
# def fetch_webpage_content(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, 'html.parser')
#     paragraphs = soup.find_all('p')
#     return [para.get_text().strip() for para in paragraphs]
#
# def save_to_file(content, output_filename):
#     with open(output_filename, 'w', encoding='utf-8') as file:
#         for line in content:
#             file.write(line + '\n')
#
# def filter_content(content):
#     filtered_content = []
#     for paragraph in content:
#         # Use the chain to process each paragraph
#         result = chain.run({"text": paragraph})
#         filtered_content.append(result)
#     return filtered_content
#
# if __name__ == '__main__':
#     url = 'https://zh.stardewvalleywiki.com/%E9%98%BF%E6%AF%94%E7%9B%96%E5%B0%94'  # 替换为实际要爬取的网页URL
#     output_filename = 'abigail.txt'
#
#     raw_content = fetch_webpage_content(url)
#     print(raw_content)
#     cleaned_content = filter_content(raw_content)
#     save_to_file(cleaned_content, output_filename)
#
#     print(f"Filtered content has been saved to {output_filename}")


import os
import cohere

co = cohere.Client("Ln1qRuW2H7m3hoVUMaWSW9pYCDF0J5Xq0SaLg9xl")
response = co.models.list()
for message in response:
    print(message)


