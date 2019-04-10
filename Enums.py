from enum import Enum

class PersonClass(Enum):
    CLASS1 = 1 # 0-5 years
    CLASS2 = 2 # 6-9 years
    CLASS3 = 3 # 10-18 years
    CLASS4 = 4 # 19-35 years
    CLASS5 = 5 # 36-50 years
    CLASS6 = 6 # 51-64 years
    CLASS7 = 7 # >65 years

class Schools(Enum):
    SCH_1 = 1 # 1st to 4th grade
    SCH_2 = 2 # 5th to 6th grade
    SCH_3 = 3 # 7th to 9th grade
    SCH_SEC = 4 # 10th to 12th grade
    SCH_SUP = 5 # university