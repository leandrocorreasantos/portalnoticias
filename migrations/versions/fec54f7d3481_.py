"""empty message

Revision ID: fec54f7d3481
Revises: 50b9b4bf72ca
Create Date: 2020-06-14 05:06:15.829273

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fec54f7d3481'
down_revision = '50b9b4bf72ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('noticias', sa.Column('categoria_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'noticias', 'categorias', ['categoria_id'], ['id'], ondelete='SET NULL')
    op.drop_column('users', 'email_confirmed_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_confirmed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'noticias', type_='foreignkey')
    op.drop_column('noticias', 'categoria_id')
    # ### end Alembic commands ###
