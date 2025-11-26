import pytest
from decimal import Decimal
from unittest.mock import Mock

from app.api.v1.property.property_repository import PropertyRepository
from app.database.models.property import Property


@pytest.mark.asyncio
async def test_update_property_invalid_area():
    repo = PropertyRepository()

    mock_db = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    entity = Property(
        id=1,
        produtor_id=1,
        nome_fazenda="Fazenda A",
        cidade="Cidade X",
        estado="SP",
        area_total=Decimal("100"),
        area_agricultavel=Decimal("60"),
        area_vegetacao=Decimal("30"),
    )

    data = Mock(
        nome_fazenda=None,
        cidade=None,
        estado=None,
        area_total=None,
        area_agricultavel=Decimal("80"),
        area_vegetacao=Decimal("30"),
    )

    with pytest.raises(ValueError):
        await repo.update(mock_db, entity, data)
