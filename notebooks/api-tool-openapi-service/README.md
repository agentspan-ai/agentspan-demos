# API Tool OpenAPI Service Demo

This directory contains the full runnable companion for the Agentspan blog post on building agents on top of existing APIs.

## Contents

- `agentspan_api_tool_demo.ipynb`: the main Jupyter notebook walkthrough
- `api_tool_demo.py`: helper functions the notebook imports to list operations and run the demo agent
- `service_catalog_api.py`: the local FastAPI service that publishes the OpenAPI document used in the demo

## Quickstart

Run the notebook from this directory so the local imports resolve correctly.

```bash
cd notebooks/api-tool-openapi-service
python3 -m pip install agentspan==0.1.5 fastapi uvicorn notebook
export OPENAI_API_KEY=your-own-key
jupyter notebook agentspan_api_tool_demo.ipynb
```

The notebook starts the demo API locally on port `8010`, starts a dedicated Agentspan server on port `6770`, and then runs an agent against the published OpenAPI document.

## Notes

- The walkthrough was developed and tested against `agentspan==0.1.5`.
- The notebook assumes `OPENAI_API_KEY` is already set in the environment before you run it.
