"""Tests for CustomerService."""
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.services.customer_service import CustomerService


class TestCustomerServiceCreateCustomer:
    """TC-CUST-S-001: Create customer."""

    @pytest.mark.asyncio
    async def test_create_customer_success(self, mock_db_session):
        """Create customer should succeed."""
        customer_repo = AsyncMock()
        customer_repo.create.return_value = MagicMock(
            id=1,
            name="Test Customer",
            industry="Technology",
            gmt_create=datetime.utcnow(),
        )

        service = CustomerService(mock_db_session, customer_repo)
        result = await service.create_customer(
            name="Test Customer",
            industry="Technology",
        )

        assert result.name == "Test Customer"
        customer_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_customer_empty_name_raises(self, mock_db_session):
        """Create customer should reject empty name."""
        customer_repo = AsyncMock()
        service = CustomerService(mock_db_session, customer_repo)

        with pytest.raises(ValueError):
            await service.create_customer(name="")


class TestCustomerServiceListCustomers:
    """TC-CUST-S-002: List customers."""

    @pytest.mark.asyncio
    async def test_list_customers_success(self, mock_db_session):
        """List customers should return paginated results."""
        customer_repo = AsyncMock()
        customer_repo.list.return_value = ([MagicMock(id=1)], 1)

        service = CustomerService(mock_db_session, customer_repo)
        customers, total = await service.list_customers()

        assert total == 1

    @pytest.mark.asyncio
    async def test_list_customers_with_keyword(self, mock_db_session):
        """List customers should filter by keyword."""
        customer_repo = AsyncMock()
        customer_repo.list.return_value = ([], 0)

        service = CustomerService(mock_db_session, customer_repo)
        await service.list_customers(keyword="test")

        call_kwargs = customer_repo.list.call_args[1]
        assert call_kwargs["keyword"] == "test"


class TestCustomerServiceUpdateCustomer:
    """TC-CUST-S-003: Update customer."""

    @pytest.mark.asyncio
    async def test_update_customer_success(self, mock_db_session):
        """Update customer should succeed."""
        customer_repo = AsyncMock()
        customer_repo.get.return_value = MagicMock(
            id=1, name="Old Name",
            gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
        )

        service = CustomerService(mock_db_session, customer_repo)
        result = await service.update_customer(
            customer_id=1, name="New Name"
        )

        assert result.name == "New Name"

    @pytest.mark.asyncio
    async def test_update_customer_not_found_raises(self, mock_db_session):
        """Update customer should raise for non-existent customer."""
        customer_repo = AsyncMock()
        customer_repo.get.return_value = None

        service = CustomerService(mock_db_session, customer_repo)

        with pytest.raises(Exception):
            await service.update_customer(customer_id=999, name="New Name")


class TestCustomerServiceDeleteCustomer:
    """TC-CUST-S-004: Soft delete customer."""

    @pytest.mark.asyncio
    async def test_delete_customer_success(self, mock_db_session):
        """Delete customer should soft-delete."""
        customer_repo = AsyncMock()
        customer_repo.get.return_value = MagicMock(
            id=1, name="Customer",
            gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
        )

        service = CustomerService(mock_db_session, customer_repo)
        await service.delete_customer(customer_id=1)

        customer_repo.soft_delete.assert_called_once()
