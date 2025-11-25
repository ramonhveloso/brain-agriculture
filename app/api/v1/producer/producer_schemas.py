import re
from typing import List, Optional

from pydantic import BaseModel, field_validator


def validate_cpf_cnpj(value: str) -> str:
    value = re.sub(r"\D", "", value)

    if len(value) == 11:
        if value == value[0] * 11:
            raise ValueError("Invalid CPF: repeated digits.")

        def calc_digit(digs):
            s = sum(int(d) * w for d, w in zip(digs, range(len(digs) + 1, 1, -1)))
            r = 11 - (s % 11)
            return "0" if r >= 10 else str(r)

        d1 = calc_digit(value[:9])
        d2 = calc_digit(value[:10])

        if value[-2:] != d1 + d2:
            raise ValueError("Invalid CPF: check digits do not match.")

        return value

    if len(value) == 14:
        if value == value[0] * 14:
            raise ValueError("Invalid CNPJ: repeated digits.")

        def calc_digit_cnpj(digs):
            weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            weights_second = [6] + weights_first
            weights = weights_first if len(digs) == 12 else weights_second

            s = sum(int(d) * w for d, w in zip(digs, weights))
            r = s % 11
            return "0" if r < 2 else str(11 - r)

        d1 = calc_digit_cnpj(value[:12])
        d2 = calc_digit_cnpj(value[:13])

        if value[-2:] != d1 + d2:
            raise ValueError("Invalid CNPJ: check digits do not match.")

        return value

    raise ValueError("Invalid CPF/CNPJ length.")


class CreateProducerRequest(BaseModel):
    cpf_cnpj: str
    nome_produtor: str

    @field_validator("cpf_cnpj")
    def validate_document(cls, v):
        return validate_cpf_cnpj(v)

    class Config:
        from_attributes = True


class Producer(BaseModel):
    id: int
    cpf_cnpj: str
    nome_produtor: str

    class Config:
        from_attributes = True


class CreateProducerResponse(Producer):
    pass


class GetProducerResponse(Producer):
    pass


class GetProducersResponse(BaseModel):
    producers: List[Producer]

    class Config:
        from_attributes = True


class UpdateProducerRequest(BaseModel):
    cpf_cnpj: Optional[str] = None
    nome_produtor: Optional[str] = None

    @field_validator("cpf_cnpj")
    def validate_document(cls, v):
        if v is None:
            return v
        return validate_cpf_cnpj(v)

    class Config:
        from_attributes = True


class UpdateProducerResponse(Producer):
    pass


class DeleteProducerResponse(Producer):
    pass
