from typing import Protocol,runtime_checkable,List
@runtime_checkable

class EMBEDDINGPROTOCOL(Protocol):
    def embed(self,text:str)->List[float]:
        ...
        