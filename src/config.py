
class Config:
    INCIDENT_ID_COLUMN_NAME = 'IncidentId'
    # FROM P360 INPUT TABLE
    L1_RC_COLUMN_NAME = 'RootCauseL1'
    L2_RC_COLUMN_NAME = 'RootCauseL2'
    L3_RC_COLUMN_NAME = 'RootCauseL3'
    L4_RC_COLUMN_NAME = 'RootCauseL4'
    L5_RC_COLUMN_NAME = 'RootCauseL5'
    L6_RC_COLUMN_NAME = 'RootCauseL6Current'
    # MAIN DATA COLS
    TITLE_COLUMN_NAME = 'Title'
    RESOLUTION_COLUMN_NAME = 'Resolutiontxt'
    CAUSE_COLUMN_NAME = 'Causetxt'
    SYMPTOMS_COLUMN_NAME = 'Symptomstxt'
    RES_CAUS_SYM_UNION = 'Res_Caus_Sym_union_txt'
    ISSUEDESCR_COLUMN_NAME = 'IssueDescription'
    CONCAT_TEXT_COLUMN_NAME = 'concat_text'  # raw input ready for preprocessing
    INPUT_TEXT_COLUMN_NAME = 'Processed_Text'  # input to model
    INCIDENTS_CLOSED_TIME_COLUMN_NAME = 'Incidents_ClosedTime'

    IS_ENGLISH_COLUMN_NAME = 'isEnglish'  # key from atlm package
