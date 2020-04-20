"""Add col Lists.is_completed

Revision ID: a893e08f32e3
Revises: 8cdcb15ced6f
Create Date: 2020-04-20 19:55:50.468043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a893e08f32e3'
down_revision = '8cdcb15ced6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lists', sa.Column('is_complete', sa.Boolean(), nullable=True))
    op.execute('update lists SET is_complete = FALSE WHERE is_complete is null;')
    op.alter_column('lists', 'is_complete', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lists', 'is_complete')
    # ### end Alembic commands ###