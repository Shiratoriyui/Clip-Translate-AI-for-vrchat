import json
import httpx
import pyperclip
import threading
import time
import sys
from datetime import datetime
import winsound


class TranslationBot:
    def __init__(self):
        self.config_file = "config.json"
        self.config = self.load_config()

        self.current_prompt = "请将以下中文文本翻译成日语。保持原意，使用自然的日语表达。"

        self.translation_thread = None
        self.running = True

        self.last_clipboard_content = pyperclip.paste()
        self.last_translation_result = ""
        self.clipboard_monitor_thread = None
        self.monitoring_clipboard = False
        self.translation_in_progress = False
        self.is_program_output = False
        self.clipboard_check_interval = 0.5

        print("=" * 60)
        print("AI翻译助手 - 自动检测版本")
        print("=" * 60)
        print("使用说明:")
        print("1. 复制需要翻译的文本到剪切板")
        print("2. 程序自动检测剪切板变动并开始翻译")
        print("3. 翻译完成后会播放提示音")
        print("4. 翻译结果自动复制到剪切板")
        print("5. 使用 Ctrl+V 粘贴翻译结果")
        print("=" * 60)
        print("[状态] 程序启动成功，开始监控剪切板...")
        print("[提示] 按 Ctrl+C 退出程序")
        print("=" * 60)

        self.start_clipboard_monitor()

    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[配置错误] 找不到配置文件 {self.config_file}")
            print(f"[配置提示] 请在同目录创建 {self.config_file}，格式如下：")
            print('''{
    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat"
}''')
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"[配置错误] {self.config_file} 格式不正确")
            sys.exit(1)

    def call_ai_api(self, text, prompt_type="translate_to_japanese"):
        try:
            api_key = self.config.get('api_key')
            base_url = self.config.get('base_url')
            model = self.config.get('model')

            if not api_key or not base_url or not model:
                raise ValueError("配置文件中 api_key、base_url 或 model 缺失")

            if not base_url.startswith("http"):
                base_url = "https://" + base_url.lstrip("/")

            url = base_url.rstrip("/") + "/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            if prompt_type == "translate_to_japanese":
                prompt = f"{self.current_prompt}\n\n原文：{text}\n\n以上中文翻译到日语口语，作为朋友对话尽量不添加任何敬语，只输出日语翻译结果，不要添加任何解释。"
            else:
                prompt = f"请将以下文本翻译回中文。保持原意，使用自然的中文表达。\n\n原文：{text}\n\n请只输出中文翻译结果，不要添加任何解释。"

            print(f"[API调用] 正在发送翻译请求...")
            print(f"  模型: {model}")
            print(f"  文本长度: {len(text)} 字符")

            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000
            }

            response = httpx.post(url, headers=headers, json=payload, timeout=30)

            print(f"[API响应] 状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content'].strip()
                print(f"[API结果] 请求成功，返回结果长度: {len(result)} 字符")
                return result
            else:
                print(f"[API错误] 请求失败: {response.status_code}")
                return None

        except httpx.TimeoutException:
            print("[API错误] 请求超时")
            return None
        except httpx.RequestError as e:
            print(f"[API错误] 网络请求错误: {e}")
            return None
        except Exception as e:
            print(f"[API错误] 异常: {e}")
            return None

    def translate_text(self, text):
        print(f"[翻译流程] 开始翻译，文本长度: {len(text)} 字符")

        print("[翻译步骤] 第1步: 中文 → 日语")
        japanese = self.call_ai_api(text, "translate_to_japanese")
        if not japanese:
            print("[翻译错误] 第1步翻译失败")
            return None

        print(f"[翻译结果] 第1步完成，日语翻译: {japanese[:100]}...")

        time.sleep(0.5)

        print("[翻译步骤] 第2步: 日语 → 中文")
        chinese_back = self.call_ai_api(japanese, "translate_to_chinese")
        if not chinese_back:
            print("[翻译错误] 第2步翻译失败")
            return None

        print(f"[翻译结果] 第2步完成，中文回译: {chinese_back[:100]}...")

        result = f"{text}\n{japanese}\n{chinese_back}"
        return result

    def process_translation(self, text):
        try:
            print("=" * 50)
            print("[翻译开始] 检测到剪切板内容，开始翻译处理...")

            self.translation_in_progress = True

            print(f"[剪切板检测] 获取到文本，长度: {len(text)} 字符")

            if not text:
                print("[警告] 剪切板内容为空")
                self.translation_in_progress = False
                return

            if len(text) > 5000:
                print("[错误] 文本过长（超过5000字符），请分段处理")
                self.translation_in_progress = False
                return

            if len(text) > 100:
                preview = text[:100] + "..."
            else:
                preview = text
            print(f"[原文预览] {preview}")

            result = self.translate_text(text)

            if result:
                try:
                    print("[提示音] 播放完成提示音")
                    winsound.Beep(550, 120)
                except Exception as e:
                    print(f"[警告] 无法播放提示音: {e}")
                    print("\a")

                print("[剪切板操作] 将翻译结果复制到剪切板")

                self.is_program_output = True
                pyperclip.copy(result)
                self.last_translation_result = result
                time.sleep(0.1)
                self.is_program_output = False

                print("[翻译完成] 翻译成功!")
                print(f"[完成时间] {datetime.now().strftime('%H:%M:%S')}")
                print("[使用提示] 翻译结果已复制到剪切板，请使用 Ctrl+V 粘贴")
                print("=" * 50)
            else:
                print("[翻译错误] 翻译失败")
                try:
                    winsound.Beep(200, 300)
                except:
                    pass

        except Exception as e:
            print(f"[处理错误] 翻译处理出错: {e}")
            try:
                winsound.Beep(200, 300)
            except:
                pass
        finally:
            self.translation_thread = None
            self.translation_in_progress = False
            print("[处理状态] 翻译处理结束")

    def start_translation_from_clipboard(self):
        if self.translation_in_progress:
            return

        if self.translation_thread and self.translation_thread.is_alive():
            return

        text = pyperclip.paste().strip()

        if not text:
            return

        if text == self.last_clipboard_content:
            return

        if text == self.last_translation_result:
            self.last_clipboard_content = text
            return

        lines = text.split('\n')
        if len(lines) >= 3:
            self.last_clipboard_content = text
            return

        print("[检测触发] 检测到剪切板变动，启动翻译...")
        self.last_clipboard_content = text
        self.translation_thread = threading.Thread(target=self.process_translation, args=(text,), daemon=True)
        self.translation_thread.start()

    def start_clipboard_monitor(self):
        print("[监控启动] 开始监控剪切板...")
        self.monitoring_clipboard = True
        self.clipboard_monitor_thread = threading.Thread(target=self.clipboard_monitor_loop, daemon=True)
        self.clipboard_monitor_thread.start()

    def clipboard_monitor_loop(self):
        print("[监控状态] 剪切板监控线程已启动")

        while self.running and self.monitoring_clipboard:
            try:
                current_content = pyperclip.paste()

                if self.is_program_output:
                    time.sleep(self.clipboard_check_interval)
                    continue

                if not current_content.strip():
                    time.sleep(self.clipboard_check_interval)
                    continue

                if current_content != self.last_clipboard_content:
                    time.sleep(0.2)

                    if pyperclip.paste() == current_content:
                        self.start_translation_from_clipboard()

                time.sleep(self.clipboard_check_interval)

            except Exception as e:
                print(f"[监控错误] 剪切板监控异常: {e}")
                time.sleep(1)

    def run(self):
        try:
            print("[程序状态] 程序主循环开始运行")
            print("[使用提示] 请复制文本到剪切板开始翻译")

            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n[程序退出] 收到退出信号，正在关闭...")
            self.running = False
        finally:
            self.on_closing()

    def on_closing(self):
        print("[资源清理] 正在清理资源...")
        self.running = False
        self.monitoring_clipboard = False

        if self.clipboard_monitor_thread and self.clipboard_monitor_thread.is_alive():
            self.clipboard_monitor_thread.join(timeout=1)

        if self.translation_thread and self.translation_thread.is_alive():
            self.translation_thread.join(timeout=1)

        print("[资源清理] 资源清理完成")
        print("[程序退出] 程序已正常退出")


def main():
    print("[程序启动] AI翻译助手启动中...")
    print("[配置加载] 正在加载配置文件...")

    try:
        bot = TranslationBot()
        bot.run()
    except Exception as e:
        print(f"[启动错误] 程序启动失败: {e}")
        input("按回车键退出...")


if __name__ == "__main__":
    try:
        import pyperclip
        import httpx
        import winsound
    except ImportError as e:
        print(f"[依赖错误] 缺少依赖库: {e}")
        print("[安装提示] 请安装所需库：pip install pyperclip httpx")
        input("按回车键退出...")
        sys.exit(1)

    main()
