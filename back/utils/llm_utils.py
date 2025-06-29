import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from config import OPENAI_API_BASE, OPENAI_API_KEY, MAX_TOKENS, LLM_MODEL_NAME

from models.session_storage import FileSessionStorage


def switch_department(department):
    model = ChatOpenAI(
        model='deepseek-chat',
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_BASE,
        max_tokens=MAX_TOKENS
    )
    parser = StrOutputParser()

    system_template = (
        f"你是一位温柔的{department}医生，你需要根据患者的描述判断疾病，并给出建议。"
        "在第一次的回答的第一行直接说明可能的疾病，然后换行，开始进行专业医学回复。"
        "专业医学回复要采用一定格式，首先说出疾病的成因，然后说出症状，然后给出建议，最后建议该挂哪个科室。"
        "尝试继续与患者沟通，获得更多信息，更好的分析病情，之后的回复不必拘泥于第一次的格式。"
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', system_template),
        MessagesPlaceholder(variable_name="history"),
        ('user', '{text}')
    ])

    chain = prompt_template | model | parser
    return chain


def switch_rag(num):
    # num
    # 1 普通门诊
    # 2 专科门诊
    # 3 智能问药
    # 4 医保咨询
    model = ChatOpenAI(
        model='deepseek-chat',
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_BASE,
        max_tokens=MAX_TOKENS
    )
    parser = StrOutputParser()
    if num == 2:
        system_template = ("你是一位温柔的医生，你需要根据患者的描述判断疾病，并给出建议。"
                           "在第一次的回答的第一行直接说明可能的疾病，然后换行，开始进行专业医学回复。"
                           "专业医学回复要采用一定格式，首先说出疾病的成因，然后说出症状，然后给出建议，最后建议该挂哪个科室"
                           "尝试继续与患者沟通，获得更多信息，更好的分析病情，之后的回复不必拘泥于第一次的格式"
                           )
    elif num == 3:
        system_template = ("你是药学专家，了解各种药物。"
                           "在第一次的回答的第一行直接说明药物的名称。"
                           "开始介绍药物，分别介绍药物基本信息，用法用量，禁忌症与注意事项，不良反应，药物相互作用，患者教育与用药指导"
                           )
    elif num == 4:
        system_template = ("你是医保专家，熟练了掌握医保相关知识"
                           "对于用户的提出的医保相关问题进行答复")
    else:
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

    chain = prompt_template | model | parser
    return chain


def get_title(file_path):
    try:
        # 读取并解析JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 查找第一个assistant的content
        for entry in data:
            if entry.get('role') == 'assistant':
                content = entry.get('content', '')
                # 分割内容并取第一行（自动处理空行）
                first_line = content.split('\n', 1)[0].strip()
                return first_line

        print("no title")
        return

    except FileNotFoundError:
        return "文件不存在"
    except json.JSONDecodeError:
        return "JSON解析错误"
    except Exception as e:
        return f"发生错误：{str(e)}"


async def streaming_chain(text: str, history: list, ch):
    async for chunk in ch.astream({"text": text, "history": history}):
        yield f"data: {json.dumps({'content': chunk})}\n\n"
