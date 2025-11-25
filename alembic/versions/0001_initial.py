"""
initial create producer/farm schema + auth tables

Autor: Ramon Veloso
Descrição: Migration inicial para criação de produtores, propriedades, safras, culturas,
usuários e blacklist de tokens.
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True, index=True, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, unique=True, index=True, nullable=False),
        sa.Column("cpf", sa.String, unique=True, index=True),
        sa.Column("cnpj", sa.String, unique=True, index=True),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean, default=False, nullable=False),
        sa.Column("reset_pin", sa.String),
        sa.Column("reset_pin_expiration", sa.DateTime),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
    )

    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.String, primary_key=True, index=True),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
    )

    op.create_table(
        "produtores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("cpf_cnpj", sa.String(20), unique=True, nullable=False),
        sa.Column("nome_produtor", sa.String(150), nullable=False),
        sa.Column(
            "criado_em", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("criado_por", sa.Integer),
        sa.Column(
            "atualizado_em",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column("atualizado_por", sa.Integer),
        sa.Column("excluido_em", sa.TIMESTAMP(timezone=True)),
        sa.Column("excluido_por", sa.Integer),
    )

    op.create_table(
        "propriedades",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "produtor_id",
            sa.Integer,
            sa.ForeignKey("produtores.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("nome_fazenda", sa.String(150), nullable=False),
        sa.Column("cidade", sa.String(120), nullable=False),
        sa.Column("estado", sa.String(2), nullable=False),
        sa.Column("area_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("area_agricultavel", sa.Numeric(12, 2), nullable=False),
        sa.Column("area_vegetacao", sa.Numeric(12, 2), nullable=False),
        sa.CheckConstraint(
            "area_agricultavel + area_vegetacao <= area_total",
            name="ck_soma_area_menor_igual_total",
        ),
        sa.Column(
            "criado_em", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("criado_por", sa.Integer),
        sa.Column(
            "atualizado_em",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column("atualizado_por", sa.Integer),
        sa.Column("excluido_em", sa.TIMESTAMP(timezone=True)),
        sa.Column("excluido_por", sa.Integer),
    )

    op.create_table(
        "safras",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(50), unique=True, nullable=False),
        sa.Column("ano", sa.Integer, nullable=False),
        sa.Column(
            "criado_em", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("criado_por", sa.Integer),
        sa.Column(
            "atualizado_em",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column("atualizado_por", sa.Integer),
        sa.Column("excluido_em", sa.TIMESTAMP(timezone=True)),
        sa.Column("excluido_por", sa.Integer),
    )

    op.create_table(
        "culturas",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(100), unique=True, nullable=False),
        sa.Column(
            "criado_em", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("criado_por", sa.Integer),
        sa.Column(
            "atualizado_em",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column("atualizado_por", sa.Integer),
        sa.Column("excluido_em", sa.TIMESTAMP(timezone=True)),
        sa.Column("excluido_por", sa.Integer),
    )

    op.create_table(
        "propriedade_safra",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "propriedade_id",
            sa.Integer,
            sa.ForeignKey("propriedades.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("safra_id", sa.Integer, sa.ForeignKey("safras.id"), nullable=False),
        sa.UniqueConstraint("propriedade_id", "safra_id", name="uq_propriedade_safra"),
        sa.Column(
            "criado_em", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("criado_por", sa.Integer),
        sa.Column(
            "atualizado_em",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column("atualizado_por", sa.Integer),
        sa.Column("excluido_em", sa.TIMESTAMP(timezone=True)),
        sa.Column("excluido_por", sa.Integer),
    )

    op.create_table(
        "cultura_plantada",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "propriedade_safra_id",
            sa.Integer,
            sa.ForeignKey("propriedade_safra.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "cultura_id", sa.Integer, sa.ForeignKey("culturas.id"), nullable=False
        ),
        sa.UniqueConstraint(
            "propriedade_safra_id", "cultura_id", name="uq_cultura_plantada"
        ),
        sa.Column(
            "criado_em", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("criado_por", sa.Integer),
        sa.Column(
            "atualizado_em",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column("atualizado_por", sa.Integer),
        sa.Column("excluido_em", sa.TIMESTAMP(timezone=True)),
        sa.Column("excluido_por", sa.Integer),
    )


def downgrade():
    op.drop_table("cultura_plantada")
    op.drop_table("propriedade_safra")
    op.drop_table("culturas")
    op.drop_table("safras")
    op.drop_table("propriedades")
    op.drop_table("produtores")
    op.drop_table("token_blacklist")
    op.drop_table("users")
