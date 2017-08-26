"""empty message

Revision ID: 5cc5bd635179
Revises: None
Create Date: 2017-08-26 13:01:19.383564

"""

# revision identifiers, used by Alembic.
revision = '5cc5bd635179'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=120), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=250), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('printed_times', sa.Integer(), server_default='0', nullable=False),
    sa.Column('printed_once', sa.Boolean(), server_default='false', nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    op.drop_table('user')
    op.drop_table('category')
    ### end Alembic commands ###
