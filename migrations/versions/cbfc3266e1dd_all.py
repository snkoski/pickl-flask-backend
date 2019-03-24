"""all

Revision ID: cbfc3266e1dd
Revises: 
Create Date: 2019-03-24 18:58:18.117002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbfc3266e1dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('abbreviation', sa.String(length=3), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_abbreviation'), 'team', ['abbreviation'], unique=True)
    op.create_index(op.f('ix_team_city'), 'team', ['city'], unique=False)
    op.create_index(op.f('ix_team_name'), 'team', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('home_team', sa.Integer(), nullable=True),
    sa.Column('away_team', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('schedule_status', sa.String(length=64), nullable=True),
    sa.Column('original_date', sa.DateTime(), nullable=True),
    sa.Column('original_time', sa.DateTime(), nullable=True),
    sa.Column('delayed_or_postponed_reason', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['away_team'], ['team.id'], ),
    sa.ForeignKeyConstraint(['home_team'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    op.drop_table('game')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_team_name'), table_name='team')
    op.drop_index(op.f('ix_team_city'), table_name='team')
    op.drop_index(op.f('ix_team_abbreviation'), table_name='team')
    op.drop_table('team')
    # ### end Alembic commands ###
