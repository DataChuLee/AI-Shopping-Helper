# AI-Shopping-Helper

## 📌 프로젝트 개요

- 이 프로젝트는 **OpenAI GPT API의 Function Calling과 Structured Outputs 기능**을 활용하여,
사용자의 자연어 질문 의도를 파악하고 적절한 API(tool)를 호출한 뒤, 그 결과를 기반으로 **정확하고 일관된 응답을 생성하는 챗봇/에이전트 시스템**을 구현하는 것을 목표로 합니다.

- 본 저장소는 FastAPI 기반의 **배송 조회, 상품 조회, 주문 조회 API**와 이를 호출하는 **LLM 기반 에이전트**, 그리고 Streamlit UI 데모를 포함합니다.

### 1. GPT + Tools(Function Calling)

GPT는 다음과 같은 흐름으로 동작합니다:

1. 사용자 입력으로부터 **질문 의도 파악**
2. 의도에 맞는 **tool(function) 선택 및 파라미터 생성**
3. 외부 API(FastAPI 서버) 호출
4. 응답 결과를 기반으로 **자연어 답변 생성** fileciteturn0file0

예시:

* "서울 날씨 알려줘" → `get_weather(location="서울")`
* "상품번호 1234567890 찾아줘" → `get_product(product_no=1234567890)`

### 2. Structured Outputs

- Structured Outputs 기능을 사용하면 **주어진 JSON Schema를 100% 준수하는 응답**을 생성할 수 있습니다.
    - 이를 통해 파싱 오류 없이 **안정적인 API 연동**이 가능

## 🧩 데모 API 구성 (FastAPI)

### 1️⃣ 배송 조회 API

* **Endpoint**: `/shipping/{orderNo}/{orderSeq}`
* **Response 예시**:

```json
{
  "orderNo": 2024010101,
  "orderSeq": 0,
  "productNo": 1234567890,
  "deliveryStatus": "PROCESSING"
}
```

* 배송 상태

  * `PROCESSING` : 출고 준비 중
  * `IN_DELIVERY` : 배송 중
  * `DELIVERED` : 배송 완료


### 2️⃣ 상품 조회 API

* **Endpoint**: `/products/{productNo}`
* **Response 예시**:

```json
{
  "productNo": 1234567890,
  "productName": "아이폰 16 Pro",
  "productStatus": "NORMAL"
}
```

* 상품 상태

  * `NORMAL` : 정상
  * `OUT_OF_STOCK` : 품절


### 3️⃣ 주문 조회 API

* **Endpoint**: `/order/{orderNo}`
* **Response 예시**:

```json
{
  "orderNo": 2024010101,
  "orderStatus": "PROCESSING",
  "totalAmount": 50000,
  "orderList": [
    {"productNo": 1234567890, "amount": 20000},
    {"productNo": 1234567891, "amount": 30000}
  ]
}
```

* 주문 상태

  * `PROCESSING` : 주문 처리 중
  * `COMPLETED` : 주문 완료
  * `CANCELLED` : 주문 취소


## 🤖 GPT 에이전트 동작 구조

1. 사용자 질문 입력
2. GPT가 Function 호출 필요 여부 판단
3. 필요한 경우 tool 호출 (`get_product`, `get_order`, `get_shipping`)
4. API 응답을 context로 재질문
5. 최종 자연어 응답 생성

`globals()[tool_name](**arguments)` 패턴을 사용하여 **유연한 함수 호출 구조**를 구현


## 🖥 Streamlit UI 데모

* 기본 챗봇 (자유 질의 응답)
* Function Calling 챗봇 (API 연동)
* System Message를 활용한 **말투 제어**

  * 친근한 말투
  * 반말
  * 정중한 말투

이를 통해 동일한 로직에서 **응답 스타일을 제어**할 수 있습니다.

## ✨ 기대 효과

* 자연어 기반 **비즈니스 API 자동 연결**
* JSON Schema 기반 **안정적인 출력 보장**
* 챗봇 + 백엔드 API 연동 구조 학습
* 실무에서 바로 활용 가능한 **Agent 패턴 이해**
