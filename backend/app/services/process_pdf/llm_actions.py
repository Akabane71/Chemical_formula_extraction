import json
import re
from app.clients.openai_client import get_async_openai_client
from app.core.config import azure_openai_settings


LLM_PROMPT_TEMPLATE = """
你是一个专业的化学专家助手，擅长从文本中提取化学式和相关数据。
请从下面的页面信息中提取所有化学式，并输出 JSON 数组。
每条记录的字段固定为：
- name: 化学式名称
- image_url: 化学式图片 URL（如无对应图片可留空字符串）
- function: 功能
- description: 描述

页面信息（JSON）：
{pages_json}
"""


def _extract_json(text: str):
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\])", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    raise ValueError("LLM 返回结果无法解析为 JSON")


async def llm_process_pdf_action(extracted_pages: list[dict]) -> list[dict]:
    pages_json = json.dumps(extracted_pages, ensure_ascii=False)
    prompt = LLM_PROMPT_TEMPLATE.format(pages_json=pages_json)
    client = await get_async_openai_client()
    response = await client.chat.completions.create(
        model=azure_openai_settings.AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "输出只允许 JSON 数组，不要包含其他文本。"},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or ""
    return _extract_json(content)
