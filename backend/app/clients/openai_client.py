from openai import AsyncAzureOpenAI, AzureOpenAI


async def get_async_openai_client() -> AsyncAzureOpenAI:
    client = AsyncAzureOpenAI(
        azure_endpoint="https://your-azure-openai-endpoint/",
        azure_deployment="your-deployment-name",
        azure_api_key="your-azure-openai-api-key",
        api_version="2024-06-01-preview",
    )
    return client


async def chat() -> str:
    client = await get_async_openai_client()
    response = await client.chat.completions.create(
        model="your-deployment-name",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    )
    return response.choices[0].message.content
    

# async_client = await get_async_openai_client()