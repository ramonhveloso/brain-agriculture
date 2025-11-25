from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Response(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostSignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostSignUpResponse(BaseModel):
    username: str
    email: EmailStr
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostLoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostLoginResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostLogoutResponse(Response):
    pass


class PostForgotPasswordRequest(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostForgotPasswordResponse(Response):
    pass


class PostResetPasswordRequest(BaseModel):
    email: str
    pin: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PostResetPasswordResponse(Response):
    pass


class PutChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class PutChangePasswordResponse(Response):
    pass


class GetMeRequest(BaseModel):
    token: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)


class GetAuthMeResponse(BaseModel):
    username: str
    email: EmailStr
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            data = data.model_dump()
        return cls(**data)
