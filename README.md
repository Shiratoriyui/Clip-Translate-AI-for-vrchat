# <h1>Clip-Translate-AI-for-vrchat</h1>    
AI 翻译助手。    <br>
把文本快速翻译到日语并译回中文对照。  <br>
一个基于 AI 的自动翻译工具，通过监控剪切板实现中-日-中的双向翻译，支持多种翻译风格。      <br>
    
<h2>✨ 功能特性   </h2> 
自动检测：监控系统剪切板，自动检测文本变化并触发翻译    <br>
双向翻译：中文→日语→中文的完整翻译流程    <br>
多风格翻译：支持正式、日常、直译等多种翻译风格    <br>
智能提示：翻译完成后播放提示音并自动复制结果到剪切板    <br>
配置灵活：支持自定义 API 配置和提示词模板    <br>
<br>
<h2>📋 环境要求  </h2>  
推荐Python 3.10+    
Windows 系统（使用 winsound 播放提示音）     
<br>
<h2>📁 文件结构    </h2>  
TEXT    <br>
Clip-Translate-AI-for-vrchat-main/    <br>
├── VRChatBox Input Chinese to Japanese Translation.py        # 主程序文件    <br>
├── config.json              # API 配置文件    <br>
└── README.md               # 项目说明文档    <br>
<br>
<h2>🚀 使用方法    </h2> 
1.启动程序 <br>
2.复制需要翻译的中文文本到剪切板    <br>
3.程序自动检测并开始翻译    <br>
4.听到提示音后，使用 Ctrl+V 粘贴翻译结果    <br>
<br>
<h2>⚙️翻译结果格式   </h2> 
翻译结果包含三部分：    <br>
    原始中文文本    <br>
    日语翻译结果    <br>
    中文回译结果    <br>
<br>
<h2>⚙️ 配置说明     </h2> 
config.json    <br>
JSON    <br>
{    <br>
    "api_key": "你的 API Key",    <br>
    "base_url": "API 基础地址",   <br> 
    "model": "使用的模型名称"    <br>
}    <br>
    <br>
<h2>📝 注意事项    </h2> 
API 限制：需要有效的 AI API Key（支持 DeepSeek、OpenAI 等）    <br>
文本长度：单次翻译建议不超过 5000 字符    <br>
剪切板冲突：避免与其他剪切板工具同时使用    <br>
    <br>
<h2>📄 许可证    </h2> 
本项目采用 MIT 许可证。    <br>
<br>
    
<h2>🙏 致谢    </h2> 
感谢 DeepSeek 贡献全部代码。   <br> 
