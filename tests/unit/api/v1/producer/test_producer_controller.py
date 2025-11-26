import pytest
from pydantic import ValidationError

from app.api.v1.producer.producer_schemas import CreateProducerRequest


def test_invalid_cpf_raises_validation_error():
    with pytest.raises(ValidationError):
        CreateProducerRequest(cpf_cnpj="123", nome_produtor="João")


def test_invalid_cnpj_raises_validation_error():
    with pytest.raises(ValidationError):
        CreateProducerRequest(cpf_cnpj="11111111111111", nome_produtor="João")


def test_valid_cpf_passes():
    valid_cpf = "39053344705"
    obj = CreateProducerRequest(cpf_cnpj=valid_cpf, nome_produtor="João")
    assert obj.cpf_cnpj == valid_cpf
