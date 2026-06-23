"""add foreign-key to posts table
Revision ID: 0c7a4a968e66
Revises: b2f58e78315d
Create Date: 2026-06-22 15:29:54.876206
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0c7a4a968e66'
down_revision: Union[str, Sequence[str], None] = 'b2f58e78315d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True))

def downgrade() -> None:
    op.drop_constraint(op.f('posts_owner_id_fkey'), 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')