import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock, MagicMock

from app.api.v1.producer.producer_service import ProducerService


@pytest.fixture
def service():
    return ProducerService()


@pytest.mark.asyncio
async def test_create_producer_success(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")

    mock_repo.get_by_cpf_cnpj = AsyncMock(return_value=None)
    mock_repo.create = AsyncMock(
        return_value={
            "id": 1,
            "cpf_cnpj": "12345678901",
            "nome_produtor": "João"
        }
    )

    data = mocker.Mock(cpf_cnpj="12345678901", nome_produtor="João")

    result = await service.create(None, data)

    assert result.id == 1
    assert result.cpf_cnpj == "12345678901"
    assert result.nome_produtor == "João"

    mock_repo.get_by_cpf_cnpj.assert_called_once()
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_producer_duplicate_document(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")

    mock_repo.get_by_cpf_cnpj = AsyncMock(return_value={"id": 1})

    data = mocker.Mock(cpf_cnpj="12345678901", nome_produtor="João")

    with pytest.raises(Exception):
        await service.create(None, data)


@pytest.mark.asyncio
async def test_get_all_producers(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")

    mock_repo.get_all = AsyncMock(
        return_value=[
            {"id": 1, "cpf_cnpj": "12345678901", "nome_produtor": "João"},
            {"id": 2, "cpf_cnpj": "98765432100", "nome_produtor": "Maria"},
        ]
    )

    mock_logger = MagicMock()

    result = await service.get_all(db=None, logger=mock_logger)

    assert len(result.producers) == 2

    assert len(result.producers) == 2
    assert result.producers[0].nome_produtor == "João"
    assert result.producers[1].nome_produtor == "Maria"


@pytest.mark.asyncio
async def test_get_producer_by_id_success(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")

    mock_repo.get_by_id = AsyncMock(
        return_value={"id": 1, "cpf_cnpj": "12345678901", "nome_produtor": "João"}
    )

    result = await service.get_by_id(None, 1)

    assert result.id == 1
    assert result.nome_produtor == "João"


@pytest.mark.asyncio
async def test_get_producer_by_id_not_found(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")
    mock_repo.get_by_id = AsyncMock(return_value=None)

    with pytest.raises(Exception):
        await service.get_by_id(None, 1)


@pytest.mark.asyncio
async def test_update_producer_success(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")

    existing = {"id": 1, "cpf_cnpj": "12345678901", "nome_produtor": "João"}
    updated = {"id": 1, "cpf_cnpj": "12345678901", "nome_produtor": "João da Silva"}

    mock_repo.get_by_id = AsyncMock(return_value=existing)
    mock_repo.update = AsyncMock(return_value=updated)

    data = mocker.Mock(nome_produtor="João da Silva")

    result = await service.update(None, 1, data)

    assert result.nome_produtor == "João da Silva"


@pytest.mark.asyncio
async def test_delete_producer_success(mocker: MockerFixture, service):
    mock_repo = mocker.patch.object(service, "repository")

    producer = {"id": 1, "cpf_cnpj": "12345678901", "nome_produtor": "João"}

    mock_repo.get_by_id = AsyncMock(return_value=producer)
    mock_repo.soft_delete = AsyncMock(return_value=producer)

    result = await service.delete(None, 1, 99)

    assert result.id == 1
    assert result.nome_produtor == "João"
