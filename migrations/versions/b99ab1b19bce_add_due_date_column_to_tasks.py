"""Add due_date column to tasks

Revision ID: b99ab1b19bce
Revises: 0ec5693d8178
Create Date: 2025-03-21 23:18:51.532757

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b99ab1b19bce'
down_revision = '0ec5693d8178'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.VARCHAR(length=36), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('password_hash', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('role', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('refresh_token', mysql.TEXT(), nullable=True),
    sa.Column('access_token', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tasks',
    sa.Column('id', mysql.VARCHAR(length=36), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('user_id', mysql.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='tasks_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
