"""create users table
Revision ID: b2f58e78315d
Revises: 3fbf07bdf676
Create Date: 2026-06-22 15:08:02.005853
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b2f58e78315d'
down_revision: Union[str, Sequence[str], None] = '3fbf07bdf676'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
  op.create_table(
     "users",
     sa.Column('id', sa.Integer(), primary_key=True, nullable=False, index=True),
     sa.Column('email', sa.String(), unique=True, nullable=True, index=True),
     sa.Column('password', sa.String(), nullable=False, index=True))  

def downgrade() -> None:
    op.drop_table('users')
