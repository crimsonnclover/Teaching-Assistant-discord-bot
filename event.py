import datetime


# Question/Information Data Class
class Event():

    def __init__(
            self, 
            guild: int = None, 
            channel:int = None, 
            type: str = None, 
            header:str = None, 
            body: list[str] = None, 
            dt: datetime = None) -> None:
        self.guild = guild
        self.channel = channel
        self.type = type
        self.header = header
        self.body = body
        self.dt = dt
        if type == "question":
            self.number_of_questions = len(body)
        else:
            self.number_of_questions = 0
