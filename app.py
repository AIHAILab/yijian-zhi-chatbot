from typing import cast

import chainlit as cl
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore

from index import get_vector_store


@cl.on_chat_start
async def on_chat_start():
    vector_store = get_vector_store()
    cl.user_session.set("vector_store", vector_store)
    model = ChatOpenAI(streaming=True, model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是個研究文史學者，擅長回答文史相關問題，尤其對於南宋洪邁著的《夷堅志》有非常深入的研究，請你嘗試回答使用者的疑問並遵守以下原則:\n\
                1. 只回答與使用者提問相關的內容，若使用者問題與《夷堅志》無關或是無法理解，請你告訴使用者。\n\
                2. 請盡可能提供詳細的答案。\n\
                3. 只回答你知道的內容，若你不知道的內容，請你告訴使用者你不知道。\n\
                以下是一些可能對於回答問題有幫助的參考資料：{context}\n\
                請自行判斷這些參考資料是否能幫助回答問題，若不能的話請嘗試利用你對《夷堅志》的了解回答使用者問題，若還是無法回答，請你明確告知使用者無法回答。",
            ),
            (
                "human",
                "{question}",
            ),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable
    vector_store = cast(QdrantVectorStore, cl.user_session.get("vector_store"))
    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content, "context": vector_store.similarity_search(message.content, k=10)},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()


@cl.on_chat_end
def on_chat_end():
    vector_store = cast(QdrantVectorStore, cl.user_session.get("vector_store"))
    vector_store.client.close()
