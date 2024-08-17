"""Changed folder_name to repo_name

Revision ID: 563409e4f995
Revises: 745a4f121281
Create Date: 2024-08-17 05:27:32.151214

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '563409e4f995'
down_revision = '745a4f121281'
branch_labels = None
depends_on = None

def upgrade():
    # Rename the column from folder_name to repo_name
    op.alter_column('users', 'folder_name', new_column_name='repo_name', existing_type=sa.String(length=255), nullable=False)

def downgrade():
    # Rename the column back from repo_name to folder_name
    op.alter_column('users', 'repo_name', new_column_name='folder_name', existing_type=sa.String(length=255), nullable=False)