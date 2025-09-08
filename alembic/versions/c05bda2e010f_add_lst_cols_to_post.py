"""add lst cols to post

Revision ID: c05bda2e010f
Revises: 04603a291d24
Create Date: 2025-09-08 12:42:55.141843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c05bda2e010f'
down_revision: Union[str, Sequence[str], None] = '04603a291d24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),)



def downgrade() :
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')