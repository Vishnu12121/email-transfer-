import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import getpass  # For securely getting the email password
import logging

# Set up logging
logging.basicConfig(filename='image_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
EMAIL_ADDRESS = 'vishnu0vardhan0@gmail.com'
EMAIL_PASSWORD = "quor yaoo wqsz fwvk"  # Securely get the password
TO_EMAIL = 'vishnuvardhanvadicherla@gmail.com'

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f'New image detected: {event.src_path}')
            logging.info(f'New image detected: {event.src_path}')
            self.send_email(event.src_path)

    def send_email(self, image_path):
        # Wait until the file is available and fully written to disk
        while not os.path.exists(image_path) or os.path.getsize(image_path) == 0:
            time.sleep(1)  # Wait for 1 second before checking again

        # Attempt to send the email with the image
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = TO_EMAIL
            msg['Subject'] = 'New Image Alert'

            # Attach the image
            with open(image_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
                msg.attach(part)

            # Send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f'Email sent with image: {image_path}')
                logging.info(f'Email sent with image: {image_path}')

        except PermissionError as e:
            print(f"Permission denied: {e}")
            logging.error(f"Permission denied: {e}")
        except Exception as e:
            print(f"An error occurred while sending email: {e}")
            logging.error(f"An error occurred while sending email: {e}")

if __name__ == "__main__":
    path_to_watch = r"C:\Users\vishn\OneDrive\Pictures\Camera Roll" # Change this to your gallery path
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)

    print("Monitoring for new images...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
  
