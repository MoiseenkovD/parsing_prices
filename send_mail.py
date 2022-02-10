import yagmail

try:
    yag = yagmail.SMTP(user='<YOUR_EMAIL>', password='<YOUR_PASSWORD>')
    yag.send(to='<TO_EMAIL>', subject='Compare prices',
             contents='Hello world!', attachments=['low-price.xlsx', 'other_prices.xlsx'])
    print("Email sent successfully")
except:
    print("Error, email was not sent")
