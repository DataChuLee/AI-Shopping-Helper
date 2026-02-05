import os
import json
import streamlit as st
from inference import system_prompt, tools, get_order, get_product, get_shipping
from openai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client()

st.title("AI Shopping Helper")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("무엇이든 물어보세요!")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

with st.chat_message("assistant"):
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = st.session_state.messages,
        temperature = 0,
        tools = tools
    )
    if response.choices[0].finish_reason == "tool_calls":
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_args = response.choices[0].message.tool_calls[0].function.arguments
        tool_args = json.loads(tool_args)
        result = globals()[tool_name](**tool_args)
        prompt = f"""
                context: {result}

                question: {message}
                answer:
                """
        response_answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = st.session_state.messages[:-1] + 
            [{"role": "user", "content": prompt}],
            temperature=0,
        )
        answer = response_answer.choices[0].message.content
    else:
        answer = response.choices[0].message.content
    st.markdown(answer)


st.session_state.messages.append(
    {"role": "assistant", "content": answer}
) 

for message in st.session_state.messages:
    print(message)
print()