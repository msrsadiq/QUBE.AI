"""Add LLM configuration tables

Revision ID: 003_add_llm_config
Revises: 002_add_projects
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_add_llm_config'
down_revision = '002_add_projects'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create LLMConfig table
    op.create_table(
        'llm_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('config_name', sa.String(255), nullable=False),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('model_name', sa.String(255), nullable=False),
        sa.Column('api_base_url', sa.String(500), nullable=True),
        sa.Column('api_key', sa.String(500), nullable=True),
        sa.Column('temperature', sa.String(10), server_default='0.7'),
        sa.Column('max_tokens', sa.Integer(), server_default='2048'),
        sa.Column('top_p', sa.String(10), server_default='1.0'),
        sa.Column('provider_specific_params', postgresql.JSON(), server_default='{}'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('is_validated', sa.Boolean(), server_default='false'),
        sa.Column('validation_status', sa.String(50), server_default='pending'),
        sa.Column('validation_message', sa.Text(), nullable=True),
        sa.Column('last_validated_at', sa.DateTime(), nullable=True),
        sa.Column('is_default', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_llm_configs_id'), 'llm_configs', ['id'], unique=False)
    op.create_index(op.f('ix_llm_configs_project_id'), 'llm_configs', ['project_id'], unique=False)

    # Create AgentLLMMapping table
    op.create_table(
        'agent_llm_mappings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('agent_type', sa.String(50), nullable=False),
        sa.Column('llm_config_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['llm_config_id'], ['llm_configs.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_llm_mappings_id'), 'agent_llm_mappings', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_agent_llm_mappings_id'), table_name='agent_llm_mappings')
    op.drop_table('agent_llm_mappings')
    op.drop_index(op.f('ix_llm_configs_project_id'), table_name='llm_configs')
    op.drop_index(op.f('ix_llm_configs_id'), table_name='llm_configs')
    op.drop_table('llm_configs')