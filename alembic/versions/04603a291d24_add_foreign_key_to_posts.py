"""add foreign key to posts

Revision ID: 04603a291d24
Revises: 02362694a10b
Create Date: 2025-09-08 12:33:37.428458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04603a291d24'
down_revision: Union[str, Sequence[str], None] = '02362694a10b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="cascade")


def downgrade() :
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')