from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from config import OPENAI_API_BASE, OPENAI_API_KEY, MAX_TOKENS, LLM_MODEL_NAME

from models.session_storage import FileSessionStorage

# llm
session_storage = FileSessionStorage()

system_template = ("你是一位温柔的医生，你需要根据患者的描述判断疾病，并给出建议。"
                   "在第一次的回答的第一行直接说明可能的疾病，然后换行，开始进行专业医学回复。"
                   "专业医学回复要采用一定格式，首先说出疾病的成因，然后说出症状，然后给出建议，最后建议该挂哪个科室"
                   "尝试继续与患者沟通，获得更多信息，更好的分析病情，之后的回复不必拘泥于第一次的格式"
                   )
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    MessagesPlaceholder(variable_name="history"),
    ('user', '{text}')
])

model = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_API_BASE,
    max_tokens=MAX_TOKENS
)

'''llm = ChatOllama(
    model=LLM_MODEL_NAME,
    temperature=0,
)'''

parser = StrOutputParser()

# web
chain = prompt_template | model | parser

# local
# chain = prompt_template | llm | parser

system_template2 = ("你是一位专业的医生，能够根据分析检查报告的内容")
prompt_template2 = ChatPromptTemplate.from_messages([
    ('system', system_template2),
    MessagesPlaceholder(variable_name="history"),
    ('user', '{text}')
])

chain2 = prompt_template2 | model | parser

system_template3 = ("你是医院的导诊人员，熟悉各个科室的位置，可以给用户指路。但只能详细的指路，并不能带着用户过去.")
prompt_template3 = ChatPromptTemplate.from_messages([
    ('system', system_template3),
    MessagesPlaceholder(variable_name="history"),
    ('user', '{text}')
])
chain3 = prompt_template3 | model | parser
