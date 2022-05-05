import enum
import uuid
import string
import re
import requests

from pydantic import BaseModel, validator, ValidationError
from dataclasses import dataclass
from datetime import datetime

from bin.contentctl_project.contentctl_core.domain.entities.security_content_object import SecurityContentObject
from bin.contentctl_project.contentctl_core.domain.entities.enums.enums import AnalyticsType
from bin.contentctl_project.contentctl_core.domain.entities.enums.enums import DataModel
from bin.contentctl_project.contentctl_core.domain.entities.investigation_tags import InvestigationTags
from bin.contentctl_project.contentctl_core.domain.entities.link_validator import LinkValidator


class Investigation(BaseModel, SecurityContentObject):
    # investigation spec
    name: str
    id: str
    version: int
    date: str
    author: str
    type: str
    datamodel: list
    description: str
    search: str
    how_to_implement: str
    known_false_positives: str
    check_references: bool = False #Validation is done in order, this field must be defined first
    references: list
    inputs: list = None
    tags: InvestigationTags

    # enrichment
    lowercase_name: str = None


    @validator('name')
    def name_max_length(cls, v):
        if len(v) > 75:
            raise ValueError('name is longer then 75 chars: ' + v)
        return v

    @validator('name')
    def name_invalid_chars(cls, v):
        invalidChars = set(string.punctuation.replace("-", ""))
        if any(char in invalidChars for char in v):
            raise ValueError('invalid chars used in name: ' + v)
        return v

    @validator('id')
    def id_check(cls, v, values):
        try:
            uuid.UUID(str(v))
        except:
            raise ValueError('uuid is not valid: ' + values["name"])
        return v

    @validator('date')
    def date_valid(cls, v, values):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except:
            raise ValueError('date is not in format YYYY-MM-DD: ' + values["name"])
        return v

    @validator('datamodel')
    def datamodel_valid(cls, v, values):
        for datamodel in v:
            if datamodel not in [el.name for el in DataModel]:
                raise ValueError('not valid data model: ' + values["name"])
        return v

    @validator('description', 'how_to_implement')
    def encode_error(cls, v, values, field):
        try:
            v.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('encoding error in ' + field.name + ': ' + values["name"])
        return v

    @validator('references')
    def references_check(cls, v, values):
        
        
        if 'check_references' in values and values['check_references'] is False:
            #Reference checking is NOT enabled
            return v
        elif 'check_references' not in values:
            raise(Exception("Member 'check_references' missing from Investigation!"))
        

        for reference in v:
            LinkValidator.validate_reference(reference)

    @validator('search')
    def search_validate(cls, v, values):
        # write search validator
        return v