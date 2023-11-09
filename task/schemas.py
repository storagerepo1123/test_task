from pydantic import BaseModel, constr

class Contacts(BaseModel):
    phone: constr(max_length=11) # int либо так, по ситуации.
    address: str
