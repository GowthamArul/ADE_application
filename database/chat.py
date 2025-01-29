from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship)
from sqlalchemy import (Column, DateTime, ForeignKey,
                        MetaData, Table, Text, func,
                        CheckConstraint
                        )
import uuid
from sqlalchemy.dialects.sqlite import UUID
from configs.config import DB_SCHEMA
import datetime



class JarvisBase(DeclarativeBase):
    metadata = MetaData(
        schema=DB_SCHEMA or "public",
        naming_convention={
            'ix':'ix_%(column_0_label)s',
            'uq':'uq_%(table_name)s_%(column_0_name)s',
            'ck':'ck%(table_name)s_`%(constraint_name)s`',
            'fk':'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk':'pk_%(table_name)s'

        },

    )
    type_annotation_map = {str:Text, datetime.datetime: DateTime(timezone=True)}


class Patient_Info(JarvisBase):
    __tablename__ = 'patient_information'

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_name: Mapped[str] = mapped_column(index=True)
    patient_address: Mapped[str] = mapped_column(index=True)
    patient_age: Mapped[int] = mapped_column(index=True)

class Patient_Conditions(JarvisBase):
    Conditions_id: Mapped[uuid.UUID] = mapped_column(
        
    )