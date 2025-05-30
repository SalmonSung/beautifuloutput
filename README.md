# beautifuloutput: Force Structured Output for LLMs
>[!Note]
> Please be aware of that, currently it's a demo.

This package provides a force-structured output tool for LLMs using prompt engineering, designed as a seamless alternative to the LangChain framework for structured responses.


## Key Features

- Support all LLMs, even if it doesn't support structured output natively.
- Enforce any `pydantic.BaseModel` structure on LLM responses.
- Simple, drop-in replacement for LangChain's structured output approach.


## Example Usage

Suppose you expect the following structured output:  
```python
from pydantic import BaseModel, Field

class ResponseFormat(BaseModel):
    answer: str = Field(description="The answer to the question")
    reason: str = Field(description="The reason why you give the answer")
```

Using LangChain (for reference)
```python
from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4.1-mini")
output = llm.invoke(["You are a helpful assistant", "who is the president of Korea?"])
```

Using BeautifulOutput (Force Structure Output)
```python
from beautifuloutput import force_structure_output

output = force_structure_output(llm, ["You are a helpful assistant", "who is the president of Korea?"], ResponseFormat)
```

Now you can easily access the structured attributes:
```python
print(output.answer)
print(output.reason)
```
