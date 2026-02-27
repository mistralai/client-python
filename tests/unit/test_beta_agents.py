"""Tests for the BetaAgents SDK methods (CRUD, versioning, aliasing)."""

import json
from typing import Any

import httpx
import pytest
import respx

from mistralai.client.sdk import Mistral

# ---------------------------------------------------------------------------
# Minimal valid response payloads
# ---------------------------------------------------------------------------

AGENT_RESPONSE: dict[str, Any] = {
    "id": "agent-001",
    "object": "agent",
    "model": "mistral-small-latest",
    "name": "Test Agent",
    "version": 1,
    "versions": [1],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "deployment_chat": False,
    "source": "api",
    "instructions": "You are a helpful agent.",
    "description": "A test agent",
}

AGENT_ALIAS_RESPONSE: dict[str, Any] = {
    "alias": "production",
    "version": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}


# -------------------------------------------------------------------------
# 1. Create agent
# -------------------------------------------------------------------------


class TestCreateAgent:
    def test_create_agent(self, mock_router, mistral_client):
        mock_router.post("/v1/agents").mock(
            return_value=httpx.Response(200, json=AGENT_RESPONSE)
        )

        result = mistral_client.beta.agents.create(
            model="mistral-small-latest",
            name="Test Agent",
            instructions="You are a helpful agent.",
        )

        assert result.id == "agent-001"
        assert result.name == "Test Agent"
        assert result.model == "mistral-small-latest"
        assert result.object == "agent"


# -------------------------------------------------------------------------
# 2. List agents
# -------------------------------------------------------------------------


class TestListAgents:
    def test_list_agents(self, mock_router, mistral_client):
        mock_router.get("/v1/agents").mock(
            return_value=httpx.Response(200, json=[AGENT_RESPONSE])
        )

        result = mistral_client.beta.agents.list()

        assert len(result) == 1
        assert result[0].id == "agent-001"


# -------------------------------------------------------------------------
# 3. Get agent
# -------------------------------------------------------------------------


class TestGetAgent:
    def test_get_agent(self, mock_router, mistral_client):
        mock_router.get("/v1/agents/agent-001").mock(
            return_value=httpx.Response(200, json=AGENT_RESPONSE)
        )

        result = mistral_client.beta.agents.get(agent_id="agent-001")

        assert result.id == "agent-001"
        assert result.name == "Test Agent"


# -------------------------------------------------------------------------
# 4. Update agent
# -------------------------------------------------------------------------


class TestUpdateAgent:
    def test_update_agent(self, mock_router, mistral_client):
        updated = {**AGENT_RESPONSE, "name": "Updated Agent", "version": 2, "versions": [1, 2]}
        mock_router.patch("/v1/agents/agent-001").mock(
            return_value=httpx.Response(200, json=updated)
        )

        result = mistral_client.beta.agents.update(
            agent_id="agent-001",
            name="Updated Agent",
        )

        assert result.name == "Updated Agent"
        assert result.version == 2


# -------------------------------------------------------------------------
# 5. Delete agent
# -------------------------------------------------------------------------


class TestDeleteAgent:
    def test_delete_agent(self, mock_router, mistral_client):
        mock_router.delete("/v1/agents/agent-001").mock(
            return_value=httpx.Response(204)
        )

        # delete returns None on 204
        result = mistral_client.beta.agents.delete(agent_id="agent-001")
        assert result is None


# -------------------------------------------------------------------------
# 6. Update version
# -------------------------------------------------------------------------


class TestUpdateVersion:
    def test_update_version(self, mock_router, mistral_client):
        versioned = {**AGENT_RESPONSE, "version": 2}
        mock_router.patch("/v1/agents/agent-001/version").mock(
            return_value=httpx.Response(200, json=versioned)
        )

        result = mistral_client.beta.agents.update_version(
            agent_id="agent-001",
            version=2,
        )

        assert result.version == 2


# -------------------------------------------------------------------------
# 7. List versions
# -------------------------------------------------------------------------


class TestListVersions:
    def test_list_versions(self, mock_router, mistral_client):
        v1 = {**AGENT_RESPONSE, "version": 1}
        v2 = {**AGENT_RESPONSE, "version": 2, "versions": [1, 2]}
        mock_router.get("/v1/agents/agent-001/versions").mock(
            return_value=httpx.Response(200, json=[v1, v2])
        )

        result = mistral_client.beta.agents.list_versions(agent_id="agent-001")

        assert len(result) == 2
        assert result[0].version == 1
        assert result[1].version == 2


# -------------------------------------------------------------------------
# 8. Get version
# -------------------------------------------------------------------------


class TestGetVersion:
    def test_get_version(self, mock_router, mistral_client):
        mock_router.get("/v1/agents/agent-001/versions/1").mock(
            return_value=httpx.Response(200, json=AGENT_RESPONSE)
        )

        result = mistral_client.beta.agents.get_version(
            agent_id="agent-001",
            version="1",
        )

        assert result.version == 1


# -------------------------------------------------------------------------
# 9. Create version alias
# -------------------------------------------------------------------------


class TestCreateVersionAlias:
    def test_create_version_alias(self, mock_router, mistral_client):
        mock_router.put("/v1/agents/agent-001/aliases").mock(
            return_value=httpx.Response(200, json=AGENT_ALIAS_RESPONSE)
        )

        result = mistral_client.beta.agents.create_version_alias(
            agent_id="agent-001",
            alias="production",
            version=1,
        )

        assert result.alias == "production"
        assert result.version == 1


# -------------------------------------------------------------------------
# 10. List version aliases
# -------------------------------------------------------------------------


class TestListVersionAliases:
    def test_list_version_aliases(self, mock_router, mistral_client):
        mock_router.get("/v1/agents/agent-001/aliases").mock(
            return_value=httpx.Response(200, json=[AGENT_ALIAS_RESPONSE])
        )

        result = mistral_client.beta.agents.list_version_aliases(
            agent_id="agent-001",
        )

        assert len(result) == 1
        assert result[0].alias == "production"


# -------------------------------------------------------------------------
# 11. Delete version alias
# -------------------------------------------------------------------------


class TestDeleteVersionAlias:
    def test_delete_version_alias(self, mock_router, mistral_client):
        # delete_version_alias sends alias as a query param, not path segment
        mock_router.delete("/v1/agents/agent-001/aliases").mock(
            return_value=httpx.Response(204)
        )

        result = mistral_client.beta.agents.delete_version_alias(
            agent_id="agent-001",
            alias="production",
        )

        assert result is None


# -------------------------------------------------------------------------
# 12. Async create agent
# -------------------------------------------------------------------------


class TestCreateAgentAsync:
    @pytest.mark.asyncio
    async def test_create_agent_async(self, mock_router, mistral_client):
        mock_router.post("/v1/agents").mock(
            return_value=httpx.Response(200, json=AGENT_RESPONSE)
        )

        result = await mistral_client.beta.agents.create_async(
            model="mistral-small-latest",
            name="Test Agent",
            instructions="You are a helpful agent.",
        )

        assert result.id == "agent-001"
        assert result.name == "Test Agent"


# -------------------------------------------------------------------------
# 13. Async list agents
# -------------------------------------------------------------------------


class TestListAgentsAsync:
    @pytest.mark.asyncio
    async def test_list_agents_async(self, mock_router, mistral_client):
        mock_router.get("/v1/agents").mock(
            return_value=httpx.Response(200, json=[AGENT_RESPONSE])
        )

        result = await mistral_client.beta.agents.list_async()

        assert len(result) == 1
        assert result[0].id == "agent-001"


# -------------------------------------------------------------------------
# 14. Async get agent
# -------------------------------------------------------------------------


class TestGetAgentAsync:
    @pytest.mark.asyncio
    async def test_get_agent_async(self, mock_router, mistral_client):
        mock_router.get("/v1/agents/agent-001").mock(
            return_value=httpx.Response(200, json=AGENT_RESPONSE)
        )

        result = await mistral_client.beta.agents.get_async(agent_id="agent-001")

        assert result.id == "agent-001"
        assert result.name == "Test Agent"


# -------------------------------------------------------------------------
# 15. Async update agent
# -------------------------------------------------------------------------


class TestUpdateAgentAsync:
    @pytest.mark.asyncio
    async def test_update_agent_async(self, mock_router, mistral_client):
        updated = {**AGENT_RESPONSE, "name": "Updated", "version": 2, "versions": [1, 2]}
        mock_router.patch("/v1/agents/agent-001").mock(
            return_value=httpx.Response(200, json=updated)
        )

        result = await mistral_client.beta.agents.update_async(
            agent_id="agent-001",
            name="Updated",
        )

        assert result.name == "Updated"


# -------------------------------------------------------------------------
# 16. Async delete agent
# -------------------------------------------------------------------------


class TestDeleteAgentAsync:
    @pytest.mark.asyncio
    async def test_delete_agent_async(self, mock_router, mistral_client):
        mock_router.delete("/v1/agents/agent-001").mock(
            return_value=httpx.Response(204)
        )

        result = await mistral_client.beta.agents.delete_async(agent_id="agent-001")
        assert result is None


# -------------------------------------------------------------------------
# 17. Async list versions
# -------------------------------------------------------------------------


class TestListVersionsAsync:
    @pytest.mark.asyncio
    async def test_list_versions_async(self, mock_router, mistral_client):
        v1 = {**AGENT_RESPONSE, "version": 1}
        v2 = {**AGENT_RESPONSE, "version": 2, "versions": [1, 2]}
        mock_router.get("/v1/agents/agent-001/versions").mock(
            return_value=httpx.Response(200, json=[v1, v2])
        )

        result = await mistral_client.beta.agents.list_versions_async(agent_id="agent-001")

        assert len(result) == 2
        assert result[0].version == 1
        assert result[1].version == 2


# -------------------------------------------------------------------------
# 18. Async get version
# -------------------------------------------------------------------------


class TestGetVersionAsync:
    @pytest.mark.asyncio
    async def test_get_version_async(self, mock_router, mistral_client):
        mock_router.get("/v1/agents/agent-001/versions/1").mock(
            return_value=httpx.Response(200, json=AGENT_RESPONSE)
        )

        result = await mistral_client.beta.agents.get_version_async(
            agent_id="agent-001",
            version="1",
        )

        assert result.version == 1
