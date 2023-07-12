from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidget
from kivymd.uix.pickers import MDDatePicker

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,ListFlowable,ListItem
from reportlab.lib.styles import getSampleStyleSheet

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class ReportScreen(Screen,Database):
    start_date = None
    end_date = None
    dialog4=None
    dialog5=None
    dialog6=None

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.report_table, 0)
        self.pdf_filename = None
        
        

    def report_table(self,instance):
         
        # ORDERS TABLE
         self.headers=["PRODUCT","QUANTITY SOLD","TOTAL SALES","EXPECTED SALES"]
         self.cursor.execute("SELECT product,quantity_sold,total_sales,expected_sales FROM maji_mazuri.report2")
         myresult = self.cursor.fetchall()
         self.rows = [] 
         for row in myresult:
            self.rows.append(row)
 
         self.mytable_order=MDDataTable(
            size_hint=(.9,.5),
            pos_hint= {'center_x':0.5, 'center_y':0.44},
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",
            background_color_header="#65275d",
            background_color_selected_cell="#c7a7db",

            column_data=[(header, dp(30)) for header in self.headers],
            row_data=self.rows

        )
        
        
         float_layout = self.ids.reports_layout
         #Here we bind the oncheck press to this table
        # self.mytable_order.bind(on_check_press=self.on_check_press)
        # self.mytable.bind(on_row_press=self.on_row_press)
         #float_layout.add_widget(self.mytable_order)

    def table_update(self):
        #first grab the new total sales
        total_sales=self.grab_total_sales()
        self.cursor.execute(f"UPDATE maji_mazuri.report2 SET total_sales = {total_sales} WHERE report_id =1")
        self.connection.commit() 

        # remove then recall the catalogue table
        layout=self.ids.reports_layout
        
        layout.remove_widget(self.mytable_order)

        # Catalogue TABLE
        self.report_table(instance=None)



    
    def download_report(self):
        self.start_date=self.ids.start_date_field.text.strip()
        self.end_date=self.ids.end_date_field.text.strip()

        if  self.start_date and self.end_date:
        
            self.date=dt.datetime.now().strftime('%d-%m-%Y')
            self.time=dt.datetime.now().strftime('%I-%M-%S %p')
            total_sales=self.grab_total_sales()

            app_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(app_dir)
            reports_dir = os.path.join(root_dir, "reports")
            os.makedirs(reports_dir, exist_ok=True)  # Create the "reports" directory if it doesn't exist

            self.pdf_filename = os.path.join(reports_dir, f"Report on {self.date} at {self.time}.pdf")  # Save the report in the "reports" directory

            doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)
            elements=[] #to store all elements in the report

            report_heading = Paragraph(f"<u><b>MAJI MAZURI SALES Report generated on {self.date}</b></u>", getSampleStyleSheet()["Heading2"])
            elements.append(report_heading)

            table_heading = Paragraph(f"<b>MAJI MAZURI Sasles Report showng total sales between {self.start_date} and {self.end_date} </b>", getSampleStyleSheet()["Heading2"])
            elements.append(table_heading)
            rows=[]
            headers = ["Cash Sales", "Online Sales","Total sales"]
            total_cash_sales=self.grab_total_sales()
            total_online_sales=self.grab_online_sales()
            rows.append([total_cash_sales, total_online_sales, total_cash_sales + total_online_sales])

            table = Table([headers] + rows)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
            ]))

            elements.append(table)

            additional_heading = Paragraph("<u><b>ADDITIONAL INFORMATION</b></u>", getSampleStyleSheet()["Heading2"])
            elements.append(additional_heading)

            highlighted_points = [
                f"Your total sales in the period entered were {total_sales}.",
                f"The toatal number of new customers gained during that same period is 50.",
                f"Additional point 3",
            ]

            styles = getSampleStyleSheet()

            point_list = ListFlowable(
                [
                    ListItem(Paragraph(point, getSampleStyleSheet()["BodyText"]))
                    for point in highlighted_points
                ],
                bulletType="bullet"  # Set to "bullet" for bullet points or "number" for numbered points
            )

            elements.append(point_list)


            doc.build(elements)

            self.download_dialog()
            doc=None
        else:
            self.enter_dates()

    def send_email(self):
        start_date=self.ids.start_date_field.text.strip()
        end_date=self.ids.end_date_field.text.strip()
        if not start_date or not end_date:
            self.enter_dates()
            return
        if not self.pdf_filename:
         self.email_dialog2()
         return
        
        if start_date and end_date:
            # Email configuration
            sender_email = "allantham897@gmail.com"  # Replace with your Gmail email address
            receiver_email = "erickthamara9@gmail.com"  # Replace with the recipient's email address
            subject = "PDF Report"
            body = "Please find the attached PDF report. From MAJI MAZURI, Regards."

            # Create a multipart message and set the email headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Add the email body
            message.attach(MIMEText(body, "plain"))

            # Open the PDF file in binary mode
            with open(self.pdf_filename, "rb") as attachment:
                # Add the PDF file as an attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode the file in ASCII characters to send by email
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {self.pdf_filename}",
            )

            # Add the attachment to the message
            message.attach(part)

            # Convert the message to a string and send the email
            text = message.as_string()

            # SMTP configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587  # Use 465 for SSL/TLS connection

            # Start the SMTP session
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Enable TLS encryption
                server.login(sender_email, "nmrfycjjqjjgbihw")  # Replace with your Gmail password or APP password
                server.sendmail(sender_email, receiver_email, text)
                self.email_dialog()
        else:
            self.enter_dates()

    def show_date_picker(self,text_field_id):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, date_range: self.on_save(text_field_id, value, date_range), on_cancel=self.on_cancel)
        date_dialog.open()
    
    def on_save(self, text_field_id, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        selected_date = value

        

        # Perform logic with the selected date
        #print("Selected Date:", selected_date)
        start_date_field = self.ids['start_date_field']
        start_date_str = start_date_field.text

        if text_field_id == 'end_date_field':
            if not start_date_str:
                # Handle the case where the start date is not specified
                self.wrong_dates_end()
                return

            start_date = dt.datetime.strptime(start_date_str, '%d-%m-%Y').date()

            if selected_date < start_date:
                # Display an error message or handle the invalid selection as needed
                self.wrong_dates_end()
                self.ids.end_date_field.text=""
                return
            

        formatted_date = selected_date.strftime('%d-%m-%Y')


        
        # Update the respective text field with the selected date
        text_field = self.ids[text_field_id]
        text_field.text = str(formatted_date)
        #print(instance, value, date_range)

        if text_field_id == 'end_date_field':
         self.table_update()
        

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    

    def grab_total_sales(self):
       
        #collect start and end dates
        start_date=self.ids.start_date_field.text.strip()
        end_date=self.ids.end_date_field.text.strip()

         #create a query for selecting all data from the START_DATE till END_DATE
        query="SELECT amount FROM maji_mazuri.cash_sales WHERE entry_date BETWEEN %s AND %s;"
        self.cursor.execute(query,(start_date,end_date))
        data_rows=self.cursor.fetchall()

        #find sales total
        sales_total=0
        for row in data_rows:
            sale=float(row[0]) #convert the string data into float
            #print(sale)
            sales_total+=sale
        
        #print(sales_total)
        return sales_total
    def grab_online_sales(self):
       
        #collect start and end dates
        start_date=self.ids.start_date_field.text.strip()
        end_date=self.ids.end_date_field.text.strip()

        self.cursor.execute("SELECT amount FROM maji_mazuri.order")
        rows = self.cursor.fetchall()

        # Calculate the total amount
        total_amount = 0
        for row in rows:
            amount = float(row[0])  # Convert the amount to a float
            total_amount += amount

        return total_amount
    
    def download_dialog(self):
          
          if not self.dialog6:
                self.dialog6= MDDialog(
                    title=f"Report downloaded successfully!",
                    radius=[20,7,20,7],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_press=self.dismiss_email_dialog6,   
                        ),
                    ],
                )
          self.dialog6.open()

    def dismiss_email_dialog6(self, instance):
        self.dialog6.dismiss()

        
    def email_dialog(self):
          
          if not self.dialog4:
                self.dialog4= MDDialog(
                    title="EMAIL SENT SUCCESSFULLY!!",
                    radius=[20,7,20,7],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_press=self.dismiss_email_dialog3,   
                        ),
                    ],
                )
          self.dialog4.open()

    def dismiss_email_dialog3(self, instance):
        self.dialog4.dismiss()

    def email_dialog2(self):
          
          if not self.dialog5:
                self.dialog5= MDDialog(
                    title="Please download the report before sending the email.",
                    radius=[20,7,20,7],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_press=self.dismiss_email_dialog5,   
                        ),
                    ],
                )
          self.dialog5.open()

    def dismiss_email_dialog5(self, instance):
        self.dialog5.dismiss()
    
    def enter_dates(self):
      snackbar=Snackbar(
          text="Enter Start Date and End Date",
          snackbar_x="10dp",
          snackbar_y="10dp",
          pos_hint={'center_x': 0.5, 'center_y': 0.5},
          #bg_color=(1,0,0,1),
          radius=[20,7,20,7],
          duration=3,
          auto_dismiss=True

      )
      snackbar.buttons=[
          MDFlatButton(text="OK",
          text_color=(1,0,0,1),
          on_release=snackbar.dismiss
            )
        ]
      snackbar.open()

    def wrong_dates_end(self):
      snackbar=Snackbar(
          text="Invalid selection. End date cannot be before the start date.",
          snackbar_x="10dp",
          snackbar_y="10dp",
          pos_hint={'center_x': 0.5, 'center_y': 0.5},
          #bg_color=(1,0,0,1),
          radius=[20,7,20,7],
          duration=3,
          auto_dismiss=True

      )
      snackbar.buttons=[
          MDFlatButton(text="OK",
          text_color=(1,0,0,1),
          on_release=snackbar.dismiss
            )
        ]
      snackbar.open()

    def wrong_dates_start(self):
      snackbar=Snackbar(
          text="Start date is not specified.",
          snackbar_x="10dp",
          snackbar_y="10dp",
          pos_hint={'center_x': 0.5, 'center_y': 0.5},
          #bg_color=(1,0,0,1),
          radius=[20,7,20,7],
          duration=3,
          auto_dismiss=True

      )
      snackbar.buttons=[
          MDFlatButton(text="OK",
          text_color=(1,0,0,1),
          on_release=snackbar.dismiss
            )
        ]
      snackbar.open()
    
    def download_catalogue(self):
        self.headers=["PRODUCT","QUANTITY SOLD","AMOUNT GENERATED"]
        self.cursor.execute("SELECT size,remaining,quantity FROM maji_mazuri.catalogue")
        myresult = self.cursor.fetchall()
        self.rows = [] 
        for row in myresult:
            self.rows.append(row)

        app_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(app_dir)
        reports_dir = os.path.join(root_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)  # Create the "reports" directory if it doesn't exist

        self.pdf_filename = os.path.join(reports_dir, f"Report on {self.date} at {self.time}.pdf")  # Save the report in the "reports" directory

        doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)
        elements=[] #to store all elements in the report

        report_heading = Paragraph(f"<u><b>MAJI MAZURI SALES Report generated on {self.date}</b></u>", getSampleStyleSheet()["Heading2"])
        elements.append(report_heading)

        table_heading = Paragraph(f"<b>MAJI MAZURI Sasles Report showng total sales between {self.start_date} and {self.end_date} </b>", getSampleStyleSheet()["Heading2"])
        elements.append(table_heading)
        rows=[]
        headers = ["Cash Sales", "Online Sales","Total sales"]
        total_cash_sales=self.grab_total_sales()
        total_online_sales=self.grab_online_sales()
        rows.append([total_cash_sales, total_online_sales, total_cash_sales + total_online_sales])

        table = Table([self.headers] + self.rows)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
        ]))

        elements.append(table)

        additional_heading = Paragraph("<u><b>ADDITIONAL INFORMATION</b></u>", getSampleStyleSheet()["Heading2"])
        elements.append(additional_heading)

        highlighted_points = [
            f"Your total sales in the period entered were .",
            f"The toatal number of new customers gained during that same period is 50.",
            f"Additional point 3",
        ]

        styles = getSampleStyleSheet()

        point_list = ListFlowable(
            [
                ListItem(Paragraph(point, getSampleStyleSheet()["BodyText"]))
                for point in highlighted_points
            ],
            bulletType="bullet"  # Set to "bullet" for bullet points or "number" for numbered points
        )

        elements.append(point_list)


        doc.build(elements)

        self.download_dialog()
        doc=None
    def customers(self):
        date=dt.datetime.now().strftime('%d-%m-%Y')
        time=dt.datetime.now().strftime('%I-%M-%S %p')
        start_date=self.ids.start_date_field.text.strip()
        end_date=self.ids.end_date_field.text.strip()

        app_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(app_dir)
        reports_dir = os.path.join(root_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)  # Create the "reports" directory if it doesn't exist

        self.pdf_filename = os.path.join(reports_dir, f"MAJI MAZURI Customer Report on {date} at {time}.pdf")  # Save the report in the "reports" directory

        doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)
        elements=[] #to store all elements in the report

        report_heading = Paragraph(f"<u><b>MAJI MAZURI Customers Report generated on {date}</b></u>", getSampleStyleSheet()["Heading2"])
        elements.append(report_heading)

        table_heading = Paragraph(f"<b>MAJI MAZURI Customers Report showng total number of customers between {start_date} and {end_date} </b>", getSampleStyleSheet()["Heading2"])
        elements.append(table_heading)
        rows=[]
        headers = ["New Customers", "Total Customers",]
        total_customers="170"
        new_customers="20"
        rows.append([new_customers,total_customers])

        table = Table([headers] + rows)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
        ]))

        elements.append(table)

        additional_heading = Paragraph("<u><b>ADDITIONAL INFORMATION</b></u>", getSampleStyleSheet()["Heading2"])
        elements.append(additional_heading)

        highlighted_points = [
            f"Your total number of new customers gained in the period entered were {new_customers}.",
            f"The toatal number of customers registered to your account are {total_customers}.",
            f"Additional point 3",
        ]

        styles = getSampleStyleSheet()

        point_list = ListFlowable(
            [
                ListItem(Paragraph(point, getSampleStyleSheet()["BodyText"]))
                for point in highlighted_points
            ],
            #bulletType="bullet"  # Set to "bullet" for bullet points or "number" for numbered points
        )

        elements.append(point_list)


        doc.build(elements)

        self.download_dialog()
        doc=None