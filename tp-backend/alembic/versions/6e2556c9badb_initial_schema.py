"""Initial schema

Revision ID: 6e2556c9badb
Revises: 
Create Date: 2025-05-04 14:08:44.210011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6e2556c9badb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop tables with foreign key dependencies first
    op.drop_index('_InvoiceTasks_B_index', table_name='_InvoiceTasks')
    op.drop_table('_InvoiceTasks')
    
    # Drop HourEntry before Task since it has a foreign key to Task
    op.drop_table('HourEntry')
    
    # Drop the Task table since it's referenced by HourEntry and _InvoiceTasks
    op.drop_table('Task')
    
    # Drop Invoice before _InvoiceTasks since it has a foreign key to Invoice
    op.drop_index('Invoice_invoiceNumber_key', table_name='Invoice')
    op.drop_table('Invoice')
    
    # Drop remaining tables
    op.drop_table('ScheduleEvent')
    op.drop_table('_prisma_migrations')


def downgrade() -> None:
    """Downgrade schema."""
    # Create tables in reverse order of their dependencies
    op.create_table('_prisma_migrations',
    sa.Column('id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('checksum', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('finished_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('migration_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('logs', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('rolled_back_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('started_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('applied_steps_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='_prisma_migrations_pkey')
    )
    
    op.create_table('ScheduleEvent',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('start', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=False),
    sa.Column('end', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='ScheduleEvent_pkey')
    )
    
    # Create Task before HourEntry and _InvoiceTasks since they depend on it
    op.create_table('Task',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Task_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('title', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('completed', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('createdAt', postgresql.TIMESTAMP(precision=3), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('updatedAt', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Task_pkey'),
    postgresql_ignore_search_path=False
    )
    
    # Create Invoice before _InvoiceTasks since it depends on it
    op.create_table('Invoice',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('issuedAt', postgresql.TIMESTAMP(precision=3), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('dueDate', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=False),
    sa.Column('paid', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('clientName', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('invoiceNumber', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Invoice_pkey')
    )
    op.create_index('Invoice_invoiceNumber_key', 'Invoice', ['invoiceNumber'], unique=True)
    
    # Create HourEntry after Task since it depends on Task
    op.create_table('HourEntry',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('taskId', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=False),
    sa.Column('hours', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('notes', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['taskId'], ['Task.id'], name='HourEntry_taskId_fkey', onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name='HourEntry_pkey')
    )
    
    # Create _InvoiceTasks last since it depends on both Invoice and Task
    op.create_table('_InvoiceTasks',
    sa.Column('A', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('B', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['A'], ['Invoice.id'], name='_InvoiceTasks_A_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['B'], ['Task.id'], name='_InvoiceTasks_B_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('A', 'B', name='_InvoiceTasks_AB_pkey')
    )
    op.create_index('_InvoiceTasks_B_index', '_InvoiceTasks', ['B'], unique=False)
    # ### end Alembic commands ###
