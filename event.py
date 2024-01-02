import datetime


# Question/Information Data Class
class Event():

    def __init__(self,
            id: str = None,
            guild: int = None, 
            channel:int = None, 
            type: str = None, 
            header:str = None, 
            body: list[str] = [], 
            dt: datetime = None
        ) -> None:
        self.id = id
        self.guild = guild
        self.channel = channel
        self.type = type
        self.header = header
        self.body = body
        self.dt = dt

    
    def __str__(self):
        return f"guild: {self.guild},\nchannel: {self.channel},\ntype: {self.type},\nheader: {self.header},\nbody: {self.body},\ndt: {self.dt}"


    def body_to_text(self) -> str:
        return(" ".join(self.body))

    def body_from_text(self, text: str) -> None:
        self.body = text.split(" ")
