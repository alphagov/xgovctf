__author__ = "Collin Petty"
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumley", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"


import smtplib
from api.common import cache
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import bcrypt

import api.common
import api.user

enable_email = False

smtp_url = ''
email_username = ''
email_password = ''
from_addr = ''
from_name = ''


def send_email(recip, subject, body):
    """Send an email with the given body text and subject to the given recipient.

    Generates a MIMEMultipart message, connects to an smtp server using the credentials loaded from the configuration
    file, then sends the email.
    """
    if enable_email:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((from_name, from_addr))
        msg['To'] = recip
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)
        s = smtplib.SMTP_SSL(smtp_url)
        s.login(email_username, email_password)
        s.sendmail(from_addr, recip, msg.as_string())
        s.quit()
    else:
        print("Emailing is disabled, not sending.")


def send_email_to_list(recips, subject, body):
    """Sends an email to a list of recipients.

    If a list of recipients is passed we iterate over them and call send_email for each recipient."""
    if recips is not None:
        for recip in recips:
            print("Sending email to %s" % recip)
            send_email(recip, subject, body)


def reset_password(token, new_password):
    """Perform the password update operation.

    Gets a token and new password from a submitted form, if the token is found in a team object in the database
    the new password is hashed and set, the token is then removed and an appropriate response is returned.
    """
    db = api.common.get_conn()
    if token is None or token == '':
        return {"status": 0, "message": "Reset token cannot be emtpy."}
    if new_password is None or new_password == '':
        return {"status": 0, "message": "New password cannot be empty."}

    team = db.teams.find_one({'password_reset_token': token})
    if team is None:
        return {"status": 0, "message": "Password reset token is not valid."}
    try:
        db.teams.update({'tid': team['tid']}, {'$set': {'password_hash': bcrypt.hashpw(new_password, bcrypt.gensalt(8))}})
        db.teams.update({'tid': team['tid']}, {'$unset': {'password_reset_token': 1}})
    except:
        return {"status": 0, "message": "There was an error updating your password."}
    return {"status": 1, "message": "Your password has been reset."}


def request_password_reset(teamname):
    """Emails a user a link to reset their password.

    Checks that a teamname was submitted to the function and grabs the relevant team info from the db.
    Generates a secure token and inserts it into the team's document as 'password_reset_token'.
    A link is emailed to the registered email address with the random token in the url.  The user can go to this
    link to submit a new password, if the token submitted with the new password matches the db token the password
    is hashed and updated in the db.
    """
    db = api.common.get_conn()
    if teamname is None or teamname == '':
        return {"status": 0, "message": "Teamname cannot be emtpy."}
    team = db.teams.find_one({'teamname': teamname})
    if team is None:
        return {"status": 0, "message": "No registration found for '%s'." % teamname}
    teamEmail = team['email']
    token = api.common.sec_token()
    db.teams.update({'tid': team['tid']}, {'$set': {'password_reset_token': token}})

    msgBody = """
    We recently received a request to reset the password for the following 'CTF Platform' account:\n\n  - %s\n\n
    Our records show that this is the email address used to register the above account.  If you did not request to reset the password for the above account then you need not take any further steps.  If you did request the password reset please follow the link below to set your new password. \n\n https://example.com/passreset#%s \n\n Best of luck! \n\n ~The 'CTF Platform' Team
    """ % (teamname, token)

    send_email(teamEmail, "'CTF Platform' Password Reset", msgBody)
    return {"status": 1, "message": "A password reset link has been sent to the email address provided during registration."}


def lookup_team_names(email):
    """Get all team names associated with an email address.

    Queries db for all teams with email equal to the provided email address, sends the names of all the team names
    to the email address.
    """
    db = api.common.get_conn()
    if email == '':
        return {"status": 0, "message": "Email Address cannot be empty."}
    teams = list(db.teams.find({'email': {'$regex': email, '$options': '-i'}}))
    if len(teams) == 0:
        return {"status": 0, "message": "No teams found with that email address, please register!"}
    tnames = [str(t['teamname']) for t in teams]
    msgBody = """Hello!

    We recently received a request to lookup the team names associated with your email address.  If you did not request this information then please disregard this email.

    The following teamnames are associated with your email address (%s).\n\n""" % email
    for tname in tnames:
        msgBody += "\t- " + tname + "\n"

    msgBody += """\nIf you have any other questions, feel free to contact us at other@example.com

    Best of luck!

    ~The 'CTF Platform' team
    """
    send_email(email, "'CTF Platform' Teamname Lookup", msgBody)
    return {"status": 1, "message": "An email has been sent with your registered teamnames."}


def load_news():
    """Get news to populate the news page.

    Queries the database for all news articles, loads them into a json document and returns them ordered by their date.
    Newest articles are at the beginning of the list to appear at the top of the news page.
    """
    db = api.common.get_conn()
    news = cache.get('news')
    if news is not None:
        return json.loads(news)
    news = sorted([{'date': str(n['date']) if 'date' in n else "2000-01-01",
                    'header': n['header'] if 'header' in n else None,
                    'articlehtml': n['articlehtml' if 'articlehtml' in n else None]}
                   for n in list(db.news.find())], key=lambda k: k['date'], reverse=True)
    cache.set('news', json.dumps(news), 60 * 2)
    return news
