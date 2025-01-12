import smtplib

smtp_host = "smtp.titan.email"
smtp_port = 587
email_user = "ceo@skillsquared.com"
email_password = "Skillsquared@10"  # Replace with your password

try:
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(email_user, email_password)
    print("SMTP connection successful!")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print(f"SMTP Authentication Error: {e}")
except Exception as e:
    print(f"Error: {e}")
