"""users table

Revision ID: 02362694a10b
Revises: c27de0213eaf
Create Date: 2025-09-08 12:08:45.938616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02362694a10b'
down_revision: Union[str, Sequence[str], None] = 'c27de0213eaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa. Column('email', sa.String(),nullable=False),
                    sa.Column('password', sa.String(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                              sa.PrimaryKeyConstraint('id'),
                              sa.UniqueConstraint('email')
                              )
    pass


def downgrade():
    op.drop_table('users')
    pass
