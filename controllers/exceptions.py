
class ControllerTokenException(Exception):
     def __init__(self,*args,**kwargs):
        Exception.__init__(self,"Unauthorized token")