from openai import AsyncAzureOpenAI, AzureOpenAI
from app.core.config import azure_openai_settings

async def get_async_openai_client() -> AsyncAzureOpenAI:
    client = AsyncAzureOpenAI(
        azure_endpoint=azure_openai_settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=azure_openai_settings.AZURE_OPENAI_DEPLOYMENT,
        api_key=azure_openai_settings.AZURE_OPENAI_API_KEY,
        api_version=azure_openai_settings.AZURE_OPENAI_API_VERSION,
    )
    return client


async def chat() -> str:
    client = await get_async_openai_client()
    response = await client.chat.completions.create(
        model=azure_openai_settings.AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": "Hello!"},
        ],
    )
    return response.choices[0].message.content