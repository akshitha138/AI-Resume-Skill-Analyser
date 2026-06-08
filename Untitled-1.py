
import whois
from urllib.parse import urlparse
import httpx
import pickle as pk
import pandas as pd
import extractorFunctions as ef
#Function to extract features
def featureExtraction(url):
 features = []
 #Address bar based features (12)
 features.append(ef.getLength(url))
 features.append(ef.getDepth(url))
 features.append(ef.tinyURL(url))
 features.append(ef.prefixSuffix(url))
 features.append(ef.no_of_dots(url))
 features.append(ef.sensitive_word(url))
 domain_name = ''
 #Domain based features (4)
 dns = 0
 try:
 domain_name = whois.whois(urlparse(url).netloc)
 except:
 dns = 1
 features.append(1 if dns == 1 else ef.domainAge(domain_name))
 features.append(1 if dns == 1 else ef.domainEnd(domain_name))
 # HTML & Javascript based features (4)
 dom = []

 try:
 response = httpx.get(url)
 except:
 response = ""
 dom.append(ef.iframe(response))
 dom.append(ef.mouseOver(response))
 dom.append(ef.forwarding(response))

features.append(ef.has_unicode(url)+ef.haveAtSign(url)+ef.havingIP(url))
 with open('model/pca_model.pkl', 'rb') as file:
 pca = pk.load(file)
 #converting the list to dataframe
 feature_names = ['URL_Length', 'URL_Depth', 'TinyURL', 'Prefix/Suffix',
'No_Of_Dots', 'Sensitive_Words',
 'Domain_Age', 'Domain_End', 'Have_Symbol','domain_att']
 dom_pd = pd.DataFrame([dom], columns =
['iFrame','Web_Forwards','Mouse_Over'])
 features.append(pca.transform(dom_pd)[0][0])
 row = pd.DataFrame([features], columns= feature_names)
return row
from flask import Flask, request, render_template
from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model
model = load_model('model/phishingdetection')

def predict(url):
 data = featureExtraction(url)
 result = predict_model(model, data=data)
 prediction_score = result['prediction_score'][0]
 prediction_label = result['prediction_label'][0]

 return {
 'prediction_label': prediction_label,
 'prediction_score': prediction_score * 100,
 }

app = Flask(_name_)
@app.route("/", methods=["GET", "POST"])
def index():
 data = None
 if request.method == "POST":
 url = request.form["url"]
 data = predict(url)
 return render_template('index.html', url=url, data=data )
 return render_template("index.html", data=data)
if _name_ == "_main_":
app.run(debug=True)
from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model
model = load_model('model/phishingdetection')

def predict(url):
 data = featureExtraction(url)
 result = predict_model(model, data=data)

 # Get the prediction score for the positive class (Phishing)
 prediction_score = result['prediction_score'][0]
 prediction_label = result['prediction_label'][0]
 # domain_age = result['Domain_Age'][0]
 # print('Result -> ', url)

 return {
 'prediction_label': prediction_label,
 'prediction_score': prediction_score * 100,
 }
if _name_ == "_main_":
 phishing_url_1 =
'https://bafybeifqd2yktzvwjw5g42l2ghvxsxn76khhsgqpkaqfdhnqf3kiuieg
w4.ipfs.dweb.link/'
 phishing_url_2 = 'http://about-ads-microsoftcom.o365.frc.skyfencenet.com'
 real_url_1 = 'https://chat.openai.com'
 real_url_2 = 'https://github.com/'


 print(predict(phishing_url_1))
 print(predict(phishing_url_2))
 print(predict(real_url_1))
 print(predict(real_url_2))
# importing required packages for Address Bar Based feature Extraction
from urllib.parse import urlparse, urlencode, unquote

import re
# importing required packages for Domain Based Feature Extraction
from datetime import datetime
# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
 ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
 match = re.search(ip_pattern, url)
 if match:
 return 1
 return 0
# 3.Checks the presence of @ in URL (Have_At)
def haveAtSign(url):
 if "@" in url:
 at = 1
 else:
 at = 0
 return at
# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
 return len(url)
# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
 s = urlparse(url).path.split('/')
 depth = 0
 for j in range(len(s)):
 if len(s[j]) != 0:
 depth = depth+1
 return depth

#listing shortening services
shortening_services =
r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.i
m|is\.gd|cli\.gs|" \

r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twur
l\.nl|snipurl\.com|" \

r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|sni
pr\.com|fic\.kr|loopt\.us|" \

r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bi
t\.do|t\.co|lnkd\.in|db\.tt|" \

r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly
|ity\.im|q\.gs|is\.gd|" \

r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.b
b|yourls\.org|x\.co|" \

r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1u
rl\.com|tweez\.me|v\.gd|" \
 r"tr\.im|link\.zip\.net"
# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
 match=re.search(shortening_services,url)
 if match:
 return 1
 else:
 return 0
# 9.Checking for Prefix or Suffix Separated by (-) in the Domain
(Prefix/Suffix)

def prefixSuffix(url):
 if '-' in urlparse(url).netloc:
 return 1 # phishing
 else:
 return 0 # legitimate
def no_of_dots(url):
 return url.count('.')
sensitiveWords = ["account", "confirm", "banking", "secure", "ebyisapi",
"webscr", "signin", "mail",
 "install", "toolbar", "backup", "paypal", "password",
"username", "verify", "update",
 "login", "support", "billing", "transaction", "security",
"payment", "verify", "online",
 "customer", "service", "accountupdate", "verification",
"important", "confidential",
 "limited", "access", "securitycheck", "verifyaccount",
"information", "change", "notice"
 "myaccount", "updateinfo", "loginsecure", "protect",
"transaction", "identity", "member"
 "personal", "actionrequired", "loginverify", "validate",
"paymentupdate", "urgent"]
def sensitive_word(url):
 domain = urlparse(url).netloc
 for i in sensitiveWords:
 if i in domain:
 return 1
 return 0
def has_unicode(url):
 # Parse the URL

 parsed_url = urlparse(url)
 # Get the netloc part of the URL
 netloc = parsed_url.netloc
 # Decode the netloc using IDNA encoding
 decoded_netloc = netloc.encode('latin1').decode('idna')
 # Unquote the decoded netloc
 unquoted_netloc = unquote(decoded_netloc)
 # Compare the unquoted netloc with the original netloc
 if unquoted_netloc != netloc:
 return 1
 return 0
# 13.Survival time of domain: The difference between termination time
and creation time (Domain_Age)
def domainAge(domain_name):
 creation_date = domain_name.creation_date
 expiration_date = domain_name.expiration_date
 if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
 try:
 creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
 expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
 except:
 return 1
 if ((expiration_date is None) or (creation_date is None)):
 return 1
 elif ((type(expiration_date) is list) or (type(creation_date) is list)):
 return 1
 else:
 ageofdomain = abs((expiration_date - creation_date).days)

 if ((ageofdomain/30) < 6):
 age = 1
 else:
 age = 0
 return age
# 14.End time of domain: The difference between termination time and
current time (Domain_End)
def domainEnd(domain_name):
 expiration_date = domain_name.expiration_date
 if isinstance(expiration_date,str):
 try:
 expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
 except:
 return 1
 if (expiration_date is None):
 return 1
 elif (type(expiration_date) is list):
 return 1
 else:
 today = datetime.now()
 end = abs((expiration_date - today).days)
 if ((end/30) < 6):
 end = 0
 else:
 end = 1
 return end
# 15. IFrame Redirection (iFrame)
def iframe(response):
 if response == "":
 return 1
 else:
 if re.findall(r"[<iframe>|<frameBorder>]", response.text):

 return 0
 else:
 return 1
# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
 if response == "" :
 return 1
 else:
 try:
 if re.findall("<script>.+onmouseover.+</script>", response.text):
 return 1
 else:
 return 0
 except:
 return 1
 # 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
 if response == "":
 return 1
 else:
 if len(response.history) <= 2:
 return 0
 else:
return