"""'增加房屋相关表结构'

Revision ID: 3127be9a977a
Revises: b07d3696c53b
Create Date: 2019-05-12 19:34:33.292369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3127be9a977a'
down_revision = 'b07d3696c53b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('facility_info',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='状态'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False, comment='设施名称'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('house_info',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='状态'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('room_count', sa.Integer(), nullable=True),
    sa.Column('acreage', sa.Integer(), nullable=True),
    sa.Column('unit', sa.String(length=32), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('beds', sa.String(length=64), nullable=True),
    sa.Column('deposit', sa.Integer(), nullable=True),
    sa.Column('min_days', sa.Integer(), nullable=True),
    sa.Column('max_days', sa.Integer(), nullable=True),
    sa.Column('order_count', sa.Integer(), nullable=True),
    sa.Column('index_image_url', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['user_address.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('house_image',
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='状态'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False, comment='房屋'),
    sa.Column('url', sa.String(length=512), nullable=False, comment='图片链接'),
    sa.ForeignKeyConstraint(['house_id'], ['house_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('houses_facility',
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('facility_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['facility_id'], ['facility_info.id'], ),
    sa.ForeignKeyConstraint(['house_id'], ['house_info.id'], ),
    sa.PrimaryKeyConstraint('house_id', 'facility_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('houses_facility')
    op.drop_table('house_image')
    op.drop_table('house_info')
    op.drop_table('facility_info')
    # ### end Alembic commands ###
