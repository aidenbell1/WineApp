"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2025-01-08 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create restaurants table
    op.create_table(
        'restaurants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(50), nullable=True),
        sa.Column('zip_code', sa.String(10), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('subscription_tier', sa.String(50), default='trial'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    
    # Create wines table
    op.create_table(
        'wines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('restaurant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('restaurants.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('producer', sa.String(255), nullable=True),
        sa.Column('vintage', sa.Integer(), nullable=True),
        sa.Column('varietal', sa.String(100), nullable=True),
        sa.Column('region', sa.String(255), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('wine_type', sa.String(20), nullable=True),
        sa.Column('body', sa.String(20), nullable=True),
        sa.Column('sweetness', sa.Integer(), nullable=True),
        sa.Column('acidity', sa.Integer(), nullable=True),
        sa.Column('tannin', sa.Integer(), nullable=True),
        sa.Column('alcohol_content', sa.Numeric(4, 2), nullable=True),
        sa.Column('cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('inventory_count', sa.Integer(), default=0),
        sa.Column('tasting_notes', sa.Text(), nullable=True),
        sa.Column('bottle_size', sa.String(20), default='750ml'),
        sa.Column('sku', sa.String(100), nullable=True),
        sa.Column('times_sold', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_wines_restaurant_id', 'wines', ['restaurant_id'])
    op.create_index('ix_wines_name', 'wines', ['name'])
    
    # Create sales table
    op.create_table(
        'sales',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('restaurant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('restaurants.id'), nullable=False),
        sa.Column('wine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('wines.id'), nullable=False),
        sa.Column('sale_date', sa.Date(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('total_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('unit_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('server_name', sa.String(100), nullable=True),
        sa.Column('table_number', sa.String(20), nullable=True),
        sa.Column('notes', sa.String(500), nullable=True),
        sa.Column('pos_transaction_id', sa.String(100), nullable=True, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_sales_restaurant_id', 'sales', ['restaurant_id'])
    op.create_index('ix_sales_wine_id', 'sales', ['wine_id'])
    op.create_index('ix_sales_sale_date', 'sales', ['sale_date'])
    
    # Create dishes table
    op.create_table(
        'dishes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('restaurant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('restaurants.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=True),
        sa.Column('main_protein', sa.String(100), nullable=True),
        sa.Column('preparation_method', sa.String(100), nullable=True),
        sa.Column('sauce_type', sa.String(100), nullable=True),
        sa.Column('spice_level', sa.String(20), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('seasonal', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_dishes_restaurant_id', 'dishes', ['restaurant_id'])


def downgrade() -> None:
    op.drop_table('dishes')
    op.drop_table('sales')
    op.drop_table('wines')
    op.drop_table('restaurants')
