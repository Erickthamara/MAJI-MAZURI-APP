from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from .zdatabase import Database
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock

from datetime import datetime
import matplotlib.pyplot as plt


class SalesGraph(Screen,Database):
   
    def __init__(self, **kw):
        super().__init__(**kw)
        
        Clock.schedule_once(self.graph_data, 0)
        

    def graph_data(self,*args):

        

        self.cursor.execute("SELECT amount FROM maji_mazuri.cash_sales;")
        data=self.cursor.fetchall()
        sales=[]
        for x in data:
            sales.append(x[0])

        self.cursor.execute("SELECT entry_date FROM maji_mazuri.cash_sales;")
        data=self.cursor.fetchall()
        dates=[]
        for x in data:
            dates.append(x[0])

        actual_date=[]
        for act in dates:
            datetime.strptime(act, "%d-%m-%Y")
            actual_date.append(act)

       

        #create the graph
        fig, ax = plt.subplots()
        ax.plot(actual_date, sales)
        ax.set_xlabel('Time')
        ax.set_ylabel('Sales')
        ax.set_title('Sales over Time')

        #set the graph
        layout=self.ids.graph
        canvas = FigureCanvasKivyAgg(figure=fig)
        layout.add_widget(canvas)
        
