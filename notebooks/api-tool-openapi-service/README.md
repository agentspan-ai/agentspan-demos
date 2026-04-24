# Agentspan Notebook Demos

This directory contains two runnable notebook demos:

- `agentspan_system_design.ipynb`: a short end-to-end walkthrough that shows one complete Agentspan workflow with an external integration, custom Python tools, multiple agents, a built-in multi-agent strategy, deploy/serve/run, and UI monitoring.
- `agentspan_api_tool_demo.ipynb`: the companion notebook for the `api_tool()` walkthrough on building agents on top of an existing OpenAPI-described API.

## Supporting files

- `service_catalog_api.py`: the local FastAPI service used by the notebooks
- `api_tool_demo.py`: helper functions used by the `api_tool()` notebook

## Quickstart

Run a notebook from this directory so the local imports and support files resolve correctly.

### End-to-end system design notebook

```bash
cd notebooks/api-tool-openapi-service
python3 -m pip install agentspan==0.1.8 fastapi uvicorn notebook requests
export OPENAI_API_KEY=your-own-key
export AGENTSPAN_LLM_MODEL=openai/gpt-4o-mini
jupyter notebook agentspan_system_design.ipynb
```

This notebook starts a small local service catalog API on port `8001`, starts a dedicated Agentspan server on port `6773`, and then runs one complete multi-agent review workflow.

### API tool notebook

```bash
cd notebooks/api-tool-openapi-service
python3 -m pip install agentspan==0.1.5 fastapi uvicorn notebook
export OPENAI_API_KEY=your-own-key
jupyter notebook agentspan_api_tool_demo.ipynb
```

This notebook starts the demo API locally on port `8010`, starts a dedicated Agentspan server on port `6770`, and then runs an agent against the published OpenAPI document.

## Notes

- `agentspan_system_design.ipynb` was developed and tested against `agentspan==0.1.8`.
- `agentspan_api_tool_demo.ipynb` was developed and tested against `agentspan==0.1.5`.
- The examples above use OpenAI for brevity, but you can replace those environment variables with any supported Agentspan provider configuration.
