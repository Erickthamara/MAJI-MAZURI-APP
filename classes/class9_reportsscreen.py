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
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class ReportScreen(Screen,Database):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.order_table, 0)
        

    def order_table(self,instance):
         
        # ORDERS TABLE
         self.headers=["cutomer_id","email","phone_no","first_name","last_name","password2","password3"]
         self.cursor.execute("SELECT * FROM maji_mazuri.customer")
         myresult = self.cursor.fetchall()
         self.rows = [] 
         for row in myresult:
            self.rows.append(row)
 
         self.mytable_order=MDDataTable(
            size_hint=(.9,.5),
            pos_hint= {'center_x':0.5, 'center_y':0.5},
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
         float_layout.add_widget(self.mytable_order)
    
    def download_report(self):
        self.date=dt.datetime.now().strftime('%d-%m-%Y')
        self.time=dt.datetime.now().strftime('%I-%M-%S %p')
        
        app_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(app_dir)
        reports_dir = os.path.join(root_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)  # Create the "reports" directory if it doesn't exist

        self.pdf_filename = os.path.join(reports_dir, f"Report on {self.date} at {self.time}.pdf")  # Save the report in the "reports" directory

        doc = SimpleDocTemplate(self.pdf_filename, pagesize=letter)

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

        elements = [table]
        doc.build(elements)

        print(f"Report saved as {self.pdf_filename}")
        doc=None


    def send_email(self):
        # Email configuration
        sender_email = "allantham897@gmail.com"  # Replace with your Gmail email address
        receiver_email = "erickthamara9@gmail.com"  # Replace with the recipient's email address
        subject = "PDF Report"
        body = "Please find the attached PDF report."

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
            server.login(sender_email, "nmrfycjjqjjgbihw")  # Replace with your Gmail password
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")