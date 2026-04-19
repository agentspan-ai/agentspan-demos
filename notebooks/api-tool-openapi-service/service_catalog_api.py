from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Service Catalog API",
    version="1.0.0",
    openapi_version="3.0.3",
    description=(
        "A small internal operations API used to demonstrate how Agentspan "
        "discovers multiple REST operations from one OpenAPI spec."
    ),
    servers=[
        {
            "url": os.environ.get("DEMO_API_BASE_URL", "http://127.0.0.1:8010"),
            "description": "Demo service base URL",
        }
    ],
)

SERVICES = {
    "checkout-api": {
        "service_name": "checkout-api",
        "owner_team": "payments-platform",
        "tier": "tier-1",
        "summary": "Processes checkout sessions and payment authorization handoff.",
        "runbook_url": "https://runbooks.internal/checkout-api",
        "pager_rotation": "checkout-primary",
    },
    "inventory-api": {
        "service_name": "inventory-api",
        "owner_team": "commerce-core",
        "tier": "tier-1",
        "summary": "Tracks stock levels and warehouse reservation state.",
        "runbook_url": "https://runbooks.internal/inventory-api",
        "pager_rotation": "inventory-primary",
    },
    "search-api": {
        "service_name": "search-api",
        "owner_team": "search-platform",
        "tier": "tier-2",
        "summary": "Serves product search and autocomplete responses.",
        "runbook_url": "https://runbooks.internal/search-api",
        "pager_rotation": "search-primary",
    },
}

LATEST_DEPLOYMENTS = {
    "checkout-api": {
        "service_name": "checkout-api",
        "environment": "production",
        "status": "healthy",
        "version": "2026.04.17.2",
        "deployed_at": "2026-04-17T12:18:00Z",
        "change_summary": "Rolled out stricter payment timeout handling.",
    },
    "inventory-api": {
        "service_name": "inventory-api",
        "environment": "production",
        "status": "healthy",
        "version": "2026.04.16.8",
        "deployed_at": "2026-04-16T21:42:00Z",
        "change_summary": "Shipped cache invalidation fixes for warehouse sync.",
    },
    "search-api": {
        "service_name": "search-api",
        "environment": "production",
        "status": "degraded",
        "version": "2026.04.17.1",
        "deployed_at": "2026-04-17T11:07:00Z",
        "change_summary": "Enabled a partial ranking experiment for product search.",
    },
}

OPEN_INCIDENTS = [
    {
        "incident_id": "INC-4821",
        "service_name": "checkout-api",
        "severity": "sev-2",
        "summary": "Payment authorization timeouts increased after a gateway retry change.",
    },
    {
        "incident_id": "INC-4825",
        "service_name": "search-api",
        "severity": "sev-3",
        "summary": "Autocomplete latency spiked for one shard in us-east-2.",
    },
]


def require_service(service_name: str) -> dict:
    service = SERVICES.get(service_name)
    if service is None:
        raise HTTPException(status_code=404, detail=f"Unknown service: {service_name}")
    return service


@app.get("/healthz", operation_id="get_health")
def get_health() -> dict:
    return {"status": "ok"}


@app.get("/services", operation_id="list_services")
def list_services() -> dict:
    return {"services": list(SERVICES.values())}


@app.get("/service-details", operation_id="get_service_details")
def get_service_details(service_name: str) -> dict:
    return require_service(service_name)


@app.get(
    "/latest-deployment",
    operation_id="get_latest_deployment",
)
def get_latest_deployment(service_name: str) -> dict:
    require_service(service_name)
    deployment = LATEST_DEPLOYMENTS.get(service_name)
    if deployment is None:
        raise HTTPException(status_code=404, detail=f"No deployment found for {service_name}")
    return deployment


@app.get("/service-runbook", operation_id="get_service_runbook")
def get_service_runbook(service_name: str) -> dict:
    service = require_service(service_name)
    return {
        "service_name": service_name,
        "runbook_url": service["runbook_url"],
        "pager_rotation": service["pager_rotation"],
    }


@app.get("/incidents/open", operation_id="list_open_incidents")
def list_open_incidents() -> dict:
    return {"incidents": OPEN_INCIDENTS}
