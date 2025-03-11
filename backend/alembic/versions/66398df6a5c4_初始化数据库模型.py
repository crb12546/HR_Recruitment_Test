"""初始化数据库模型

Revision ID: 66398df6a5c4
Revises: 
Create Date: 2025-03-11 03:29:49.006680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66398df6a5c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_requirements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position_name', sa.String(length=100), nullable=False, comment='职位名称'),
    sa.Column('department', sa.String(length=50), nullable=True, comment='部门'),
    sa.Column('responsibilities', sa.Text(), nullable=False, comment='职责描述'),
    sa.Column('requirements', sa.Text(), nullable=False, comment='职位要求'),
    sa.Column('salary_range', sa.String(length=50), nullable=True, comment='薪资范围'),
    sa.Column('location', sa.String(length=100), nullable=True, comment='工作地点'),
    sa.Column('tags', sa.JSON(), nullable=True, comment='职位标签'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_requirements_id'), 'job_requirements', ['id'], unique=False)
    op.create_table('resumes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_name', sa.String(length=50), nullable=False, comment='候选人姓名'),
    sa.Column('file_url', sa.String(length=255), nullable=False, comment='文件URL'),
    sa.Column('file_type', sa.String(length=20), nullable=False, comment='文件类型'),
    sa.Column('ocr_content', sa.Text(), nullable=True, comment='OCR识别内容'),
    sa.Column('parsed_content', sa.Text(), nullable=True, comment='解析后内容'),
    sa.Column('talent_portrait', sa.Text(), nullable=True, comment='人才画像'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False, comment='标签名称'),
    sa.Column('category', sa.String(length=20), nullable=True, comment='标签类别'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False, comment='用户名'),
    sa.Column('email', sa.String(length=100), nullable=False, comment='邮箱'),
    sa.Column('hashed_password', sa.String(length=100), nullable=False, comment='哈希密码'),
    sa.Column('full_name', sa.String(length=100), nullable=True, comment='全名'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='是否激活'),
    sa.Column('is_superuser', sa.Boolean(), nullable=True, comment='是否超级用户'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False, comment='简历ID'),
    sa.Column('job_id', sa.Integer(), nullable=False, comment='职位ID'),
    sa.Column('match_score', sa.Float(), nullable=False, comment='匹配分数'),
    sa.Column('match_explanation', sa.Text(), nullable=True, comment='匹配说明'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.ForeignKeyConstraint(['job_id'], ['job_requirements.id'], ),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_matches_id'), 'matches', ['id'], unique=False)
    op.create_table('plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False, comment='方案标题'),
    sa.Column('job_id', sa.Integer(), nullable=False, comment='职位ID'),
    sa.Column('description', sa.Text(), nullable=True, comment='方案描述'),
    sa.Column('strategy', sa.Text(), nullable=True, comment='招聘策略'),
    sa.Column('candidate_ids', sa.JSON(), nullable=True, comment='候选人ID列表'),
    sa.Column('created_by', sa.Integer(), nullable=True, comment='创建人ID'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['job_id'], ['job_requirements.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plans_id'), 'plans', ['id'], unique=False)
    op.create_table('resume_tag',
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('resume_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resume_tag')
    op.drop_index(op.f('ix_plans_id'), table_name='plans')
    op.drop_table('plans')
    op.drop_index(op.f('ix_matches_id'), table_name='matches')
    op.drop_table('matches')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_table('resumes')
    op.drop_index(op.f('ix_job_requirements_id'), table_name='job_requirements')
    op.drop_table('job_requirements')
    # ### end Alembic commands ###
