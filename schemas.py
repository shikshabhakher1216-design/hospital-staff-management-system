from pydantic import BaseModel
# Basemodel, is used to define the structure of data and validate input data

class HospitalStaff(BaseModel):
    # class used to define structure of table 
    # BaseModel is used to validate incoming data

    id: int
    # id must be an integer

    username: str
    # username must be in string

    password: str
    # password must be in string

    role: str
    # role must be in string

    department: str
    # department must be in string


class LoginSchema(BaseModel):

    username : str

    password : str
            