# Clip-Translate-AI-for-vrchat
AI 翻译助手
一个基于 AI 的自动翻译工具，通过监控剪切板实现中-日-中的双向翻译，支持多种翻译风格。

✨ 功能特性
自动检测：监控系统剪切板，自动检测文本变化并触发翻译
双向翻译：中文→日语→中文的完整翻译流程
多风格翻译：支持正式、日常、动漫、直译等多种翻译风格
智能提示：翻译完成后播放提示音并自动复制结果到剪切板
配置灵活：支持自定义 API 配置和提示词模板
📋 环境要求
推荐Python 3.10+
Windows 系统（使用 winsound 播放提示音）
🔧 安装步骤
1. 克隆仓库
BASH
git clone https://github.com/your-username/translation-bot.git
cd translation-bot
2. 安装依赖
BASH
pip install -r requirements.txt
3. 配置文件
在项目根目录创建 config.json：

JSON
{
    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat"
}
4. 运行程序
BASH
python translation_bot.py
📁 文件结构
TEXT
translation-bot/
├── translation_bot.py        # 主程序文件
├── config.json              # API 配置文件
├── prompts.json             # 翻译风格配置文件
├── requirements.txt         # Python 依赖包
└── README.md               # 项目说明文档
🚀 使用方法
基本使用
启动程序：python translation_bot.py
复制需要翻译的中文文本到剪切板
程序自动检测并开始翻译
听到提示音后，使用 Ctrl+V 粘贴翻译结果
翻译结果格式
翻译结果包含三部分：

TEXT
原始中文文本
日语翻译结果
中文回译结果

⚙️ 配置说明
config.json
JSON
{
    "api_key": "你的 API Key",
    "base_url": "API 基础地址",
    "model": "使用的模型名称"
}

📝 注意事项
API 限制：需要有效的 AI API Key（支持 DeepSeek、OpenAI 等）
文本长度：单次翻译建议不超过 5000 字符
剪切板冲突：避免与其他剪切板工具同时使用

📄 许可证
本项目采用 MIT 许可证。

🙏 致谢
感谢 DeepSeek 贡献全部代码。
