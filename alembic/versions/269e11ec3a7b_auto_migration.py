"""Auto migration

Revision ID: 269e11ec3a7b
Revises: 3f98abb1eeb4
Create Date: 2024-07-16 20:51:49.021970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '269e11ec3a7b'
down_revision: Union[str, None] = '3f98abb1eeb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
