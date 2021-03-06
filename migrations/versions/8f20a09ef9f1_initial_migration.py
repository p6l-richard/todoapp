"""Initial migration

Revision ID: 8f20a09ef9f1
Revises: 
Create Date: 2020-04-16 11:31:02.199129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f20a09ef9f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    todo_table = op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=280), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    print('Adding:', [{'id': i, 'title': f'{i} thing to do', 'description': f'The number {i} thing to do'} for i in range(5)])
    op.bulk_insert(todo_table,
    [{'id': i, 'title': f'{i} thing to do', 'description': f'The number {i} thing to do'} for i in range(5)]
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    # ### end Alembic commands ###
