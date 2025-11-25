import pytest
from pytest_mock import MockerFixture

from app.api.v1.culture.culture_service import CultureService


@pytest.fixture
def service():
    return CultureService(repository=None)


@pytest.mark.asyncio
async def test_get_all(service: CultureService, mocker: MockerFixture):
    service.repository = mocker.Mock()
    service.repository.get_all = mocker.AsyncMock(
        return_value=[{"id": 1, "nome": "Soja"}]
    )

    result = await service.get_all(db=None)

    assert len(result.cultures) == 1
    assert result.cultures[0].id == 1
    assert result.cultures[0].nome == "Soja"
    service.repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id(service: CultureService, mocker: MockerFixture):
    service.repository = mocker.Mock()
    service.repository.get_by_id = mocker.AsyncMock(
        return_value={"id": 1, "nome": "Milho"}
    )

    result = await service.get_by_id(db=None, culture_id=1)

    assert result.id == 1
    assert result.nome == "Milho"
    service.repository.get_by_id.assert_called_once_with(None, 1)


@pytest.mark.asyncio
async def test_get_by_id_not_found(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_id = mocker.AsyncMock(return_value=None)

    with pytest.raises(Exception) as exc:
        await service.get_by_id(db=None, culture_id=999)

    assert "Culture not found" in str(exc.value)


@pytest.mark.asyncio
async def test_create(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_name = mocker.AsyncMock(return_value=None)
    service.repository.create = mocker.AsyncMock(
        return_value={"id": 1, "nome": "Trigo"}
    )

    payload = type("Obj", (), {"nome": "Trigo"})()

    result = await service.create(db=None, data=payload)

    assert result.id == 1
    assert result.nome == "Trigo"
    service.repository.get_by_name.assert_called_once()
    service.repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_already_exists(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_name = mocker.AsyncMock(return_value={"id": 1})

    payload = type("Obj", (), {"nome": "Soja"})()

    with pytest.raises(Exception) as exc:
        await service.create(db=None, data=payload)

    assert "Culture already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_update(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_id = mocker.AsyncMock(return_value={"id": 1, "nome": "Soja"})
    service.repository.update = mocker.AsyncMock(return_value={"id": 1, "nome": "Milho"})

    payload = type("Obj", (), {"nome": "Milho"})()

    result = await service.update(db=None, culture_id=1, data=payload)

    assert result.id == 1
    assert result.nome == "Milho"
    service.repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_id = mocker.AsyncMock(return_value=None)

    payload = type("Obj", (), {"nome": "Milho"})()

    with pytest.raises(Exception) as exc:
        await service.update(db=None, culture_id=999, data=payload)

    assert "Culture not found" in str(exc.value)


@pytest.mark.asyncio
async def test_delete(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_id = mocker.AsyncMock(return_value={"id": 1, "nome": "Soja"})
    service.repository.delete = mocker.AsyncMock(return_value={"id": 1, "nome": "Soja"})

    result = await service.delete(db=None, culture_id=1)

    assert result.id == 1
    assert result.nome == "Soja"
    service.repository.delete.assert_called_once()


@pytest.mark.asyncio
async def test_delete_not_found(service: CultureService, mocker):
    service.repository = mocker.Mock()
    service.repository.get_by_id = mocker.AsyncMock(return_value=None)

    with pytest.raises(Exception) as exc:
        await service.delete(db=None, culture_id=999)

    assert "Culture not found" in str(exc.value)
