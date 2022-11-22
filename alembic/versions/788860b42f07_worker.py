"""worker

Revision ID: 788860b42f07
Revises: c6bc1dad81e0
Create Date: 2022-11-21 20:40:12.870113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '788860b42f07'
down_revision = 'c6bc1dad81e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('specialization', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workers_id'), 'workers', ['id'], unique=False)
    op.create_index(op.f('ix_workers_name'), 'workers', ['name'], unique=True)
    op.create_index(op.f('ix_workers_user_id'), 'workers', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workers_user_id'), table_name='workers')
    op.drop_index(op.f('ix_workers_name'), table_name='workers')
    op.drop_index(op.f('ix_workers_id'), table_name='workers')
    op.drop_table('workers')
    # ### end Alembic commands ###