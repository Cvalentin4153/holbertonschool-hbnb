from app.models.__init__ import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    def validate_name(self, name):
        if not isinstance(name, str) or len(name) > 50:
            raise TypeError
        ("Amenity must be a string of 50 chartacters or less.")
        return name