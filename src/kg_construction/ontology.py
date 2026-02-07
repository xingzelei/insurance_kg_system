from enum import Enum

class EntityType(Enum):
    INSURANCE_PRODUCT = "InsuranceProduct"
    DISEASE = "Disease"
    DRUG = "Drug"
    DEPARTMENT = "Department"
    NURSING_HOME = "NursingHome"
    SERVICE = "Service"
    LOCATION = "Location"

class RelationType(Enum):
    COVERS_DISEASE = "COVERS_DISEASE"        # Insurance -> Disease
    APPLICABLE_AGE = "APPLICABLE_AGE"        # Insurance -> AgeRange (represented as property usually, but can be node)
    REQUIRES_UNDERWRITING = "REQUIRES_UNDERWRITING" # Insurance -> Disease (e.g., Hypertension needs underwriting)
    TREATS = "TREATS"                        # Drug -> Disease
    BELONGS_TO = "BELONGS_TO"                # Disease -> Department
    HAS_COMPLICATION = "HAS_COMPLICATION"    # Disease -> Disease
    LOCATED_IN = "LOCATED_IN"                # NursingHome -> Location
    PROVIDES_SERVICE = "PROVIDES_SERVICE"    # NursingHome -> Service
