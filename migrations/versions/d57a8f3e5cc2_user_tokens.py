"""user tokens

Revision ID: d57a8f3e5cc2
Revises: 0a051555cb72
Create Date: 2019-04-16 17:56:34.590025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd57a8f3e5cc2'
down_revision = '0a051555cb72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_game_date'), 'game', ['date'], unique=False)
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    op.drop_index(op.f('ix_game_date'), table_name='game')
    # ### end Alembic commands ###
