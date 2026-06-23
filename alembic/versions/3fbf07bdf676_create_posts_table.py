"""create posts table
Revision ID: 3fbf07bdf676
Revises: 
Create Date: 2026-06-21 22:36:59.505672
"""
# sqlalchemy.orm not needed in alembic migration
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3fbf07bdf676'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, index=True),
        sa.Column('title', sa.String(), nullable=False, index=True),
        sa.Column('content', sa.String(), nullable=False, index=True),
        sa.Column('category', sa.String(), nullable=False, index=True),
        sa.Column('published', sa.Boolean(), server_default='true', nullable=False, index=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False, index=True),
    )

def downgrade() -> None:
    op.drop_table("posts")
    
