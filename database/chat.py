from sqlalchemy.orm import ( Mapped,
                            mapped_column, 
                            relationship)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, DateTime, ForeignKey,
                        MetaData, Table, Text, func,
                        CheckConstraint
                        )
from typing import Optional
import uuid
from configs.config import DB_SCHEMA
import datetime
import os


Base = declarative_base()

# class JarvisBase(DeclarativeBase):
#     metadata = MetaData(
#         # schema=DB_SCHEMA or "public",
#         naming_convention={
#             'ix':'ix_%(column_0_label)s',
#             'uq':'uq_%(table_name)s_%(column_0_name)s',
#             'ck':'ck%(table_name)s_`%(constraint_name)s`',
#             'fk':'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
#             'pk':'pk_%(table_name)s'

#         },

#     )
#     type_annotation_map = {str:Text, datetime.datetime: DateTime(timezone=True)}


# class JarvisBase(Base):
    # metadata = MetaData(schema=os.environ.get("JARVIS_SCHEMA") or "public")
    

collection_document_map = Table("collection_document_map",
                                Base.metadata,
                                Column("documents", ForeignKey("documents.document_id")),
                                Column("collections", ForeignKey("collections.collection_id"))
                                )


class CollectionModel(Base):
    __tablename__ = 'collections'

    collection_id: Mapped[uuid.UUID] = mapped_column(
        Text, primary_key=True, default= lambda: str(uuid.uuid4)
    )
    creation_ts: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    edit_ts: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    user_id: Mapped[str] = mapped_column(index=True)
    collection_name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
    status: Mapped[str] = mapped_column(index=True, default="ACTIVE")
    module_name: Mapped[str] = mapped_column(index=True)
    documents: Mapped[list["DocumentModel"]] = relationship(
        secondary=collection_document_map,
        back_populates="collections",
        lazy="selectin",
        order_by="DocumentModel.title"
    )
    # chat_session: Mapped[list["ChatSessionModel"]] = relationship(
    #     back_populates="collection", cascade="all, delete-orphan", lazy="selectin"
    # )

class FileModel(Base):
    __tablename__ = "files"

    file_id: Mapped[uuid.UUID] = mapped_column(
        Text, primary_key=True, default= lambda: str(uuid.uuid4)
    )
    file_name: Mapped[str] = mapped_column(index=True)
    upload_ts: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[str] = mapped_column(index=True)
    hash: Mapped[str] = mapped_column(index=True)
    documents: Mapped["DocumentModel"] = relationship(back_populates="file")


class DocumentModel(Base):
    __tablename__ = "documents"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Text, primary_key=True, default= lambda: str(uuid.uuid4)
    )
    document_name: Mapped[str] = mapped_column(index=True)
    creation_ts: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    document_type: Mapped[str] # arxiv
    title: Mapped[str]

    user_id: Mapped[str | None] = mapped_column(index=True)

    arxiv_details: Mapped[Optional["ArxivDetailModel"]] = relationship(
        back_populates="documents",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    
    file_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey(FileModel.file_id, ondelete="RESTRICT"))
    
    collections: Mapped[list["CollectionModel"]] = relationship(
        secondary=collection_document_map,
        back_populates="documents",
        lazy="selectin"
    )
    file: Mapped[FileModel | None] = relationship(back_populates="documents")
    # user_source_docs: Mapped["UserSourceModel"] = relationship(
    #     back_populates="document"
    # )
    # chat_source_docs: Mapped["ChatSourceModel"] = relationship(
    #     back_populates="document"
    # )

    def copy(self):
        return DocumentModel(
            document_id = uuid.uuid4(),
            document_name = self.document_name,
            document_type = self.document_type,
            title=self.title,
            user_id=self.user_id,
            # file_id = self.file_id,
            arxiv_details = self.arxiv_details.copy() if self.arxiv_details else None,
            collections = [x for x in self.collections]
        )
    
    def to_embeddable(self) -> str:
        if self.document_type == "arxiv":
            assert self.arxiv_details is not None
            return self.arxiv_details.summary or "N/A"
        else:
            raise ValueError(f"Unsupported document type: {self.document_type}")
        
    def to_metadata(self) -> dict[str, str]:
        metadata = {"title": self.title, "source": self.document_type}
        return metadata


class ArxivDetailModel(Base):
    __tablename__ = "arxiv_detail"

    arxiv_id : Mapped[uuid.UUID] = mapped_column(
        Text, primary_key=True, default= lambda: str(uuid.uuid4)
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(DocumentModel.document_id, ondelete="CASCADE"),
    )
    summary: Mapped[str | None]
    publication_date: Mapped[str]
    updated_date: Mapped[str]
    link: Mapped[str]
    authors: Mapped[str]
    documents: Mapped["DocumentModel"] = relationship(back_populates="arxiv_details")

    def copy(self):
        return ArxivDetailModel(
            arxiv_id = uuid.uuid4(),
            summary = self.summary,
            publication_date = self.publication_date,
            updated_date = self.updated_date,
            link = self.link,
            authors = self.authors

        )

