""" adding content column to posts table 

Revision ID: c27de0213eaf
Revises: bfef5a6bc7e0
Create Date: 2025-09-08 11:11:36.059286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c27de0213eaf'
down_revision: Union[str, Sequence[str], None] = 'bfef5a6bc7e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
     op.drop_column('posts', 'content')
     pass
