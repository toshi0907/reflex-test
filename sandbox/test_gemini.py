from google import genai
import os
import warnings

from dotenv import load_dotenv

# Interactions API は現状ベータのため警告を抑制
warnings.filterwarnings("ignore", category=UserWarning, module="google.genai")

load_dotenv()


def gemini_test(model_name: str, prompt: str, gemini_tools=None):

    # APIキーの設定（既存の環境変数名を尊重しつつフォールバック）
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        raise RuntimeError("APIキー未設定")

    client = genai.Client(api_key=gemini_api_key)

    # 質問の送信（Interactions API）
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        interaction = client.interactions.create(
            model=model_name,
            input=prompt,
            tools=gemini_tools,
        )

    # 結果の表示（テキスト出力を優先し、複数テキストを結合して表示）
    if interaction.outputs:
        text_items = [
            o.text
            for o in interaction.outputs
            if getattr(o, "type", "") == "text" and hasattr(o, "text")
        ]

        if text_items:
            print("".join(text_items))
        else:
            # フォールバック：最後の出力に text 属性があれば表示
            last = interaction.outputs[-1]
            if hasattr(last, "text"):
                print(last.text)
            else:
                # 出力タイプを簡易表示（デバッグ用途）
                print(f"出力タイプ: {getattr(last, 'type', 'unknown')}\n{last}")


_model_name = "gemini-2.5-flash"
_prompt = "git 現在のブランチ名を確認するコマンド スクリプトで使用"
_gemini_tools = [{"type": "google_search"}]
gemini_test(_model_name, _prompt, _gemini_tools)
