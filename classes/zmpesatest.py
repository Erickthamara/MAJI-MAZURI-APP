from .zmpesa3 import MpesaClient
import reportlab

obj=MpesaClient()
result=obj.main("254796892684",1)
print(result)