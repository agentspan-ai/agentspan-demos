from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path

from agentspan.agents import Agent, AgentRuntime, api_tool


def fetch_spec(base_url: str) -> dict:
    spec_url = base_url if base_url.rstrip("/").endswith(("openapi.json", "swagger.json")) else f"{base_url.rstrip('/')}/openapi.json"
    with urllib.request.urlopen(spec_url) as response:
        return json.load(response)


def list_operations(base_url: str) -> None:
    spec = fetch_spec(base_url)
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            print(
                f"{operation['operationId']:>24}  "
                f"{method.upper():<6}  {path}"
            )


def build_agent(base_url: str, max_tools: int, tool_names: list[str] | None) -> Agent:
    support_api = api_tool(
        url=base_url,
        max_tools=max_tools,
        tool_names=tool_names,
    )
    return Agent(
        name="service_ops_assistant",
        model=os.environ.get("AGENTSPAN_LLM_MODEL", "openai/gpt-4o-mini"),
        instructions=(
            "You are an engineering support assistant. Use the API tools to answer "
            "questions about service ownership, incidents, deployments, and runbooks. "
            "Prefer concrete facts from the API over general advice."
        ),
        tools=[support_api],
    )


def run_demo(
    base_url: str,
    prompt: str,
    max_tools: int,
    tool_names: list[str] | None,
    execution_id_file: Path | None,
) -> None:
    agent = build_agent(base_url, max_tools=max_tools, tool_names=tool_names)
    with AgentRuntime() as runtime:
        result = runtime.run(agent, prompt)

    result.print_result()
    if execution_id_file is not None:
        execution_id_file.write_text(result.execution_id)
        print(f"execution_id_file={execution_id_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default=os.environ.get("DEMO_API_SPEC_URL", "http://127.0.0.1:8010/openapi.json"),
    )
    parser.add_argument(
        "--prompt",
        default=(
            "A checkout incident is open. Tell me who owns checkout-api, what the "
            "latest production deployment changed, and which runbook I should open first."
        ),
    )
    parser.add_argument("--max-tools", type=int, default=8)
    parser.add_argument(
        "--tool-name",
        action="append",
        dest="tool_names",
        default=[
            "get_service_details",
            "get_latest_deployment",
            "get_service_runbook",
        ],
    )
    parser.add_argument("--list-ops", action="store_true")
    parser.add_argument(
        "--execution-id-file",
        type=Path,
        default=Path("/tmp/agentspan_api_tool.execution_id"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_ops:
        list_operations(args.base_url)
        return 0
    run_demo(
        base_url=args.base_url,
        prompt=args.prompt,
        max_tools=args.max_tools,
        tool_names=args.tool_names,
        execution_id_file=args.execution_id_file,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
