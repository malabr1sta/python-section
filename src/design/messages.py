import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class MessageParser(ABC):

    @abstractmethod
    def parse(self, msg: JsonMessage) -> ParsedMessage:
        raise NotImplementedError


class TelegramParser(MessageParser):

    def parse(self) -> ParsedMessage:
        pass


class MattermostParser(MessageParser):

    def parse(self) -> ParsedMessage:
        pass


class SlackParser(MessageParser):

    def parse(self) -> ParsedMessage:
        pass


class ParserFactory:

    __parsers = {}

    @classmethod
    def register_parser(cls, msg_type: MessageType, parser: MessageParser) -> None:
        cls.__parsers[msg_type] = parser

    @classmethod
    def get_parser(cls, message: JsonMessage) -> MessageParser:
        parser_cls = cls.__parsers.get(message.message_type, None)
        if parser_cls is None:
            raise ValueError(f"No parser found for: {message.message_type}")
        return parser_cls
