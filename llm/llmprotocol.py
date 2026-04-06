from typing import Protocol,runtime_checkable
@runtime_checkable
class LLMPROTOCOL(Protocol):

    def chat(self, system_instruction:str, user_content:str)->str:
        ...
        