"""empty message

Revision ID: 46b2cf2d2d5e
Revises: 
Create Date: 2022-01-20 14:20:12.672425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46b2cf2d2d5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content_master', sa.Column('ref_stored_filename', sa.String(length=500), nullable=True, comment='참조하는 파일 이름'))
    op.alter_column('content_master', 'description',
               existing_type=sa.VARCHAR(length=500),
               comment='설명',
               existing_comment='컨텐츠 설명',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('content_master', 'description',
               existing_type=sa.VARCHAR(length=500),
               comment='컨텐츠 설명',
               existing_comment='설명',
               existing_nullable=True)
    op.drop_column('content_master', 'ref_stored_filename')
    # ### end Alembic commands ###
