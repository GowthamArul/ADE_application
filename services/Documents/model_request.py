from pydantic import BaseModel
from pydantic import Field
import uuid


class SourceDocument(BaseModel):
    document_id: str = Field(
        validate_default=lambda: str(uuid.uuid4()),
        description="Global Unique identifier for the document"
    )
    document_name: str
    title: str
    text:str | None = None

class ArxivDocs(SourceDocument):
    authors: str
    summary: str
    primary_category: str
    secondary_categories: str
    publication_date: str
    updated_date: str | None = None
    link: str | None = None
    

class CreateDocumentRequest(BaseModel):
    documents: list[ArxivDocs]
    user_id:str
    module: str = "Arxiv"
    model_config = {
        "json_schema_extra": {
            "examples": [
            {
        "documents": [
                        {
                        "document_id": "2203.00502v1",
                        "document_name": "2203.00502v1",
                        "title": "Sensor technologies in cancer research for new directions in diagnosis  and treatment: and exploratory analysis",
                        "authors": "Mario Coccia, Saeed Roshani, Melika Mosleh",
                        "summary": "The goal of this study is an exploratory analysis concerning main sensortechnologies applied in cancer research to detect new directions in diagnosisand treatments. The study focused on types of cancer having a high incidenceand mortality worldwide: breast, lung, colorectal and prostate. Data of the Webof Science (WOS) core collection database are used to retrieve articles relatedto sensor technologies and cancer research over 1991-2021 period. We utilizedGephi software version 0.9.2 to visualize the co-word networks of theinteraction between sensor technologies and cancers under study. Results showmain clusters of interaction per typology of cancer. Biosensor is the only typeof sensor that plays an essential role in all types of cancer: breast cancer,lung cancer, prostate cancer, and colorectal cancer. Electrochemical sensor isapplied in all types of cancer under study except lung cancer. Electrochemicalbiosensor is used in breast cancer, lung cancer, and prostate cancer researchbut not colorectal cancer. Optical sensor can also be considered one of thesensor technologies that significantly is used in breast cancer, prostatecancer, and colorectal cancer. This study shows that this type of sensor isapplied in more diversified approaches. Moreover, the oxygen sensor is mostlystudied in lung cancer and breast cancer due to the usage in breath analysisfor the treatment process. Finally, Cmos sensor is a technology used mainly inlung cancer and colorectal cancer. Results here suggest new directions for theevolution of science and technology of sensors in cancer research to supportinnovation and research policy directed to new technological trajectorieshaving a potential of accelerated growth and positive social impact fordiagnosis and treatments of cancer.",
                        "primary_category": "Signal Processing",
                        "secondary_categories": "Social and Information Networks, Medical Physics",
                        "publication_date": "2022-02-04T11:50:19Z",
                        "updated_date": "2022-02-04 11:50:19",
                        "link": "http://arxiv.org/abs/2203.00502v1"
                    }
                    ],
                    "user_id": "ag",
                    "module": "Arxiv"
                    } ]
                            }
    }

class CreateDocumentResponse(BaseModel):
    document_id_by_name: dict[str, str]
    created: int
    existing: int
    status: str