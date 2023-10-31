"""empty message

Revision ID: 53e489e1d710
Revises: f7de24bf5bd8
Create Date: 2023-10-30 16:57:11.760074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53e489e1d710'
down_revision: Union[str, None] = 'f7de24bf5bd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maxLineCnt',
    sa.Column('seq', sa.Integer(), nullable=False),
    sa.Column('cnt', sa.Integer(), nullable=True),
    sa.Column('regDt', sa.DateTime(), nullable=True),
    sa.Column('updDt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('seq')
    )
    op.drop_table('sqlite_sequence')
    op.alter_column('scheduleHistory', 'seq',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('scheduleManager', 'seq',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('scheduleState', 'seq',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('scheduleState', 'seq',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.alter_column('scheduleManager', 'seq',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.alter_column('scheduleHistory', 'seq',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    op.drop_table('maxLineCnt')
    # ### end Alembic commands ###
