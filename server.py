from pydoc import text
from sre_constants import SUCCESS
from unittest import result
from awslabs.mcp_lambda_handler import MCPLambdaHandler

mcp_server = MCPLambdaHandler(name="remote_counter_MCP", version="1.0.0")


@mcp_server.tool()
def count_ja_String(text: str, characters_max: int, *, characters_min: int = 0) -> dict:
    """
    Counts the number of characters in a given Japanese sentence.
    text: string to count(str)(required)
    characters_max: Upper limit of characters to count (int)(required)
    characters_min: lower limit of characters (int)(optional, default is characters_max-10)
    """
    if characters_min == 0:
        # デフォルト: 上限-10。ただし下限は0未満にしない
        characters_min = max(0, characters_max - 10)
    # 境界チェック（任意の追加防御）
    if characters_min < 0:
        characters_min = 0
    if characters_min > characters_max:
        # エラーにする代わりに上限へ丸める（仕様に応じてエラー返却でも可）
        characters_min = characters_max
    try:
        count = len("".join(text.split()))
        is_exceed = count > characters_max
        is_below = count < characters_min
        message = (
            f"文字数が上限({characters_max})を超えています。現在の文字数: {count}"
            if is_exceed
            else f"文字数が上限内({characters_max})です。現在の文字数: {count}"
        )
        message += (
            f"\n文字数が下限({characters_min})を下回っています。"
            if is_below
            else f"\n文字数が下限({characters_min})を上回っています。"
        )
        payload = {
            "success": True,
            "message": message,
            "count": count,
            "is_exceed": is_exceed,
            "is_below": is_below,
        }
        return payload
    except Exception as e:
        return {
            "success": False,
            "message": f"文字数のカウント中にエラーが発生しました",
            "count": 0,
            "is_exceed": False,
            "is_below": False,
        }
