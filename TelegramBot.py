from re import (
    search as regex_search,
    DOTALL as REGEX_DOTALL
)
from json import (
    dumps as json_encode,
    loads as json_decode
)
from requests import post, get, put

class TelegramBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token

    def __REQUEST__(self, method, data):
        try:
            response = post(
                url="https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx",
                data={
                    "UrlBox": f"https://api.telegram.org/bot{self.bot_token}/{method}",
                    "ContentTypeBox": "application/json",
                    "ContentDataBox": json_encode(data),
                    "HeadersBox": "",
                    "RefererBox": "",
                    "AgentList": "Custom...",
                    "AgentBox": "Telegram Bot SDK",
                    "VersionsList": "HTTP/1.1",
                    "MethodList": "POST"
                }
            )
            if response.status_code == 200:
                response = response.text
                response = json_decode(regex_search(r"<pre[^>]*>(.*?)</pre>", response, REGEX_DOTALL)[1].strip())
                return response["result"]
        except Exception:
            pass
        return False

    def SendMessage(self, chat_id, text):
        return self.__REQUEST__("sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "markdown"
        })