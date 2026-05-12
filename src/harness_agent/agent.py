from agents import Agent, Runner, function_tool, set_default_openai_client, set_default_openai_api
from openai import AsyncOpenAI
import subprocess
import os

# --- 核心工具 (由 PBH 协议驱动) ---
@function_tool
def read_agents_md() -> str:
    """读取项目根目录的 AGENTS.md 文件，理解协作规则。"""
    try:
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "错误：未找到 AGENTS.md，请确认项目已由 PBH 初始化。"

@function_tool
def run_make_verify() -> str:
    """调用项目统一质量门禁，获取即时反馈。"""
    try:
        result = subprocess.run(
            ["make", "verify"],
            capture_output=True,
            timeout=30
        )
        stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ''
        stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ''
        return stdout + "\n" + stderr
    except Exception as e:
        return f"运行 make verify 时出错: {str(e)}"

# --- 配置 MiMo 自定义客户端（从环境变量读取密钥）---
mimo_api_key = os.getenv("MIMO_API_KEY")
if not mimo_api_key:
    raise RuntimeError("请先设置环境变量 MIMO_API_KEY")

mimo_client = AsyncOpenAI(
    api_key=mimo_api_key,
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

# 将 MiMo 客户端设置为全局默认，并指定使用 Chat Completions API
set_default_openai_client(mimo_client)
set_default_openai_api("chat_completions")

# 禁用 Tracing，避免超时日志污染输出
os.environ['OPENAI_AGENTS_DISABLE_TRACING'] = 'true'

# --- Architect Agent 定义 (规划者) ---
architect = Agent(
    name="Architect",
    instructions="""你是 Harness Agent 的架构师，一个基于 PBH 协议进行诊断和规划的技术专家。
你的职责是基于 AGENTS.md 中的规则，分析 CI 或 Harness-Lint 的报错。
你只负责规划，绝不修改任何代码。""",
    model="mimo-v2.5-pro",
    tools=[read_agents_md, run_make_verify]
)

# --- 运行示例 (最小可行闭环) ---
async def main():
    user_input = "Harness-Lint 刚才报告了 3 个违规。请读取 AGENTS.md 并分析可能的原因。"
    print(f"用户输入: {user_input}\n")
    result = await Runner.run(architect, user_input)
    print("Architect 分析结论:")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())