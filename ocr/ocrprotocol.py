# ocr/ocr_protocol.py

from typing import Protocol, runtime_checkable

@runtime_checkable
class OCRProtocol(Protocol):

    def ocr(self, filename: str) -> str:
        ...