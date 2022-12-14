"""empty message

Revision ID: 95cb002128ff
Revises: 510d0d505a9b
Create Date: 2022-11-14 20:15:09.423730

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '95cb002128ff'
down_revision = '510d0d505a9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fav', 'user_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fav', 'user_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
