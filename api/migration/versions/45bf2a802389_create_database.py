"""Create database

Revision ID: 45bf2a802389
Revises: 216348e88e86
Create Date: 2024-11-25 20:58:49.130150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45bf2a802389'
down_revision: Union[str, None] = '216348e88e86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attachment', sa.Column('path', sa.String(), nullable=False))
    op.add_column('attachment', sa.Column('size', sa.Integer(), nullable=False))
    op.drop_column('attachment', 'file_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attachment', sa.Column('file_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('attachment', 'size')
    op.drop_column('attachment', 'path')
    # ### end Alembic commands ###
