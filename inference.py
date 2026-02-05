import json
import requests
import os
from openai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client()


def get_product(product_no):
    return requests.get(f"http://127.0.0.1:8000/products/{product_no}").json()


def get_order(order_no):
    return requests.get(f"http://127.0.0.1:8000/orders/{order_no}").json()


def get_shipping(order_no, order_seq):
    return requests.get(f"http://127.0.0.1:8000/shipping/{order_no}/{order_seq}").json()


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Get the product by product_no",
            "parameters": {
                "type": "object",
                "required": ["product_no"],
                "properties": {
                    "product_no": {"type": "number", "description": "상품번호"}
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_shipping",
            "description": "Get the shipping info by order_no, order_seq",
            "parameters": {
                "type": "object",
                "required": ["order_no", "order_seq"],
                "properties": {
                    "order_no": {"type": "number", "description": "주문번호"},
                    "order_seq": {"type": "number", "description": "주문순번"},
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get the order by order_no",
            "parameters": {
                "type": "object",
                "required": ["order_no"],
                "properties": {
                    "order_no": {"type": "number", "description": "주문번호"}
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

system_prompt = """
아래 말투 예시를 참고해서 최대한 정중한 말투로 답변하세요.

example1: 안녕하세요.
example2: 궁금한 게 있으시면 무엇이든 물어보세요.
example3: 주문이 미뤄지고 있습니다.
example4: 오늘 제일 핫한 이 상품을 확인해보세요.
example5: 잠시만 기다려주세요.
example6: 이 상품은 어떤가요?
example7: 확인해보겠습니다.
example8: 무슨 일 있나요?
example9: 난 온라인 쇼핑을 즐겨합니다.
example10: 좋아하시는 음식 있나요?
"""


def inference(message):
    # 1) 먼저 gpt한테 물어보기: tool 필요하면 tool_calls로 돌아옴
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0,
        tools=tools,
    )
    if response.choices[0].finish_reason == "tool_calls":
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_args = response.choices[0].message.tool_calls[0].function.arguments
        tool_args = json.loads(tool_args)
        #     if tool_name == "get_product":
        #         result = get_product(tool_args["product_no"])
        #     elif tool_name == "get_order":
        #         result = get_order(tool_args["order_no"])
        #     elif tool_name == "get_shipping":
        #         result = get_shipping(tool_args["order_no"], tool_args["order_seq"])
        result = globals()[tool_name](**tool_args)
        prompt = f"""
                context: {result}

                question: {message}
                answer:
                """
        response_answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response_answer.choices[0].message.content

    else:
        return response.choices[0].message.content
