from flask import Flask, jsonify, render_template, request, send_from_directory
from flask.helpers import send_file
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import uuid
from models.sql import *

app = Flask( __name__ )
cors = CORS(app)
mail = Mail(app)

app.config['UPLOAD_FOLDER'] = 'filesCompany'
app.config['UPLOAD_FLAYER'] = 'flayersCompany'
app.config['UPLOAD_BACKGROUND'] = 'backgroundPage'

# Configuración del email
app.config['MAIL_SERVER']='mail.1smtg.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'customers@1smtg.com'
app.config['MAIL_PASSWORD'] = '1solution'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Routes --

@app.route("/")
@cross_origin()
def index():
    return {"message": "puto el que lo lea"}

@app.route("/getAllUsers/<company>/<role>/<page>", methods=["GET"])
@cross_origin()
def getAllUsers( company, role, page ):
    data = getAllUsersSQL( company, role, page )
    return data, 200

@app.route("/getBlogs/<company>/<page>")
@cross_origin()
def getBlogsEnterprise( company, page ):
    data = getInformationEnterpriseSQL( company )
    res = json.loads( data )
    blogs = getAllBlogs( res[0]["id"], page )
    return jsonify( blogs ), 200

@app.route("/getBlogById/<blog_id>")
@cross_origin()
def getBlogById( blog_id ):
    data = getBlogByIdSQL( blog_id )
    return jsonify( data ), 200

@app.route("/getUser/<user_id>", methods=["GET"])
@cross_origin()
def getUser( user_id ):
    data = getUserSQL( user_id )
    return data

@app.route("/getInformationEnterprise/<company>", methods=["GET"])
@cross_origin()
def getInformationEnterprise( company ):
    data = getInformationEnterpriseSQL( company )
    return data, 200

@app.route("/getEnterpriseColors/<company>", methods=["GET"])
@cross_origin()
def getEnterpriseColors( company ):
    data = getInformationEnterpriseSQL( company )
    res = json.loads( data )
    dataC = getEnterpriseColorsSQl( res[0]["id"] )
    return dataC, 200

@app.route("/sendEmail/<company>/<name>/<email>/<phone>/<subject>/<message>", methods=["GET"])
@cross_origin()
def sendEmail( company, name, email, phone, subject, message ):
    data = getInformationEnterpriseSQL( company )
    res = json.loads(data)

    msg = Message( subject, sender ='info@1smtg.com', recipients = [ 'info@1smtg.com' ] )
    
    imgEnterpriseHTML = f'<img src="http://1smtg.com/picture.php?name={res[0]["picture"]}" style="width: 200px; margin-bottom: 20px;">'
    messageHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">{message}</h5> </div>'
    nameHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Name:</h5> <span> {name} </span> </div>'
    emailHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Email:</h5> <span> {email} </span> </div>'
    phoneHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Phone:</h5> <span> {phone} </span> </div>'
    fotherHTML = f'<div style="background: #555; padding: 10px; font-size: 12px; text-align: center; color: #fff;">1Solution | Support | Privacy Policy<br>© 2021 Copyright: Zero 1Solution LLC, All rights reserved. 2111 West March Lane, Stockton CA 95207</div>'

    msg.html = f"{imgEnterpriseHTML} <br> {messageHTML} <br> {nameHTML} {emailHTML} {phoneHTML} <br><br> {fotherHTML}"
    mail.send(msg) 
    return {"sent": "true"}, 200

@app.route("/sendEmail/emailApply", methods=["POST"])
@cross_origin()
def sendEmailApply():
    email_lon_of = ""
    company = request.json["company"]
    if request.json["email_lon_of"] == "":
        users = json.loads( getAllUsersSQL( company, "mlo", 0 ) )
        CEO = list( filter(lambda x: x["title"] == "CEO", users) )
        data_ceo = json.loads( getUserSQL( CEO[0]["id"] ) )
        email_lon_of = data_ceo[0]["email"]
    else:
        email_lon_of = request.json["email_lon_of"]
    
    # user information
    first_name = request.json["first_name"]
    middle_name = request.json["middle_name"]
    last_name = request.json["last_name"]
    email_cli = request.json["email_cli"]
    phone_cli = request.json["phone_cli"]
    product = request.json["product"]
    # end user information

    # inputs select information
    mortgage_type = request.json["mortgage_type"]
    zip_code = request.json["zip_code"]
    purches_price = request.json["purches_price"]
    cash_out = request.json["cash_out"]
    down_payment = request.json["down_payment"]
    loan_balance = request.json["loan_balance"]
    credit_score_value = request.json["credit_score_value"]
    term = request.json["term"]
    # end inputs select information

    company_data = getInformationEnterpriseSQL( company )
    res = json.loads( company_data )

    validate_client = json.loads( isExistClient( email_cli ) )

    cli_information_portal = updateClient( validate_client[0]["id"], validate_client[0]["password"], validate_client[0]["user"] ) if ( len( validate_client ) > 0 ) else addClient( first_name, middle_name, last_name, email_cli, phone_cli, email_lon_of )

    email_lon_of = cli_information_portal["email_lon_of"] # In case that this user is register and select other lon officer diferent to he have selected

    print(validate_client)
    print(cli_information_portal)
    print(email_lon_of)

    msg = Message( "New prospect want to apply", sender ='info@1smtg.com', recipients = [ email_lon_of ] )
    
    imgEnterpriseHTML = f'<img src="http://1smtg.com/picture.php?name={res[0]["picture"]}" style="width: 200px; margin-bottom: 20px;">'
    messageHTML = f'<div style="margin-bottom: 15px;"> <h1 style="font-weight: 500;display: inline;">New prospect want to apply</h1></div>'
    nameHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Name:</h5> <span> {first_name} {middle_name} {last_name} </span> </div>'
    emailHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Email:</h5> <span> {email_cli} </span> </div>'
    phoneHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Phone:</h5> <span> {phone_cli} </span> </div>'
    productSHTML = f'<div style="margin-bottom: 15px;"> <h1 style="font-weight: 500;display: inline;">Product select</h1></div>'
    namePHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Name product:</h5> <span> {product["name"]} </span> </div>'
    rateHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Rate:</h5> <span> {product["rate"]} </span> </div>'
    aprHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Apr:</h5> <span> {product["apr"]} </span> </div>'
    closingcostHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Closing cost:</h5> <span> {product["closing_cost"]} </span> </div>'
    monthlyHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Monthly payment:</h5> <span> {product["mo_payment"]} </span> </div>'
    captureuserSHTML = f'<div style="margin-bottom: 15px;"> <h1 style="font-weight: 500;display: inline;">Data capture</h1></div>'
    mortgagetypeHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Mortgage type:</h5> <span> {mortgage_type} </span> </div>'
    zipcodeHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">ZIP code:</h5> <span> {zip_code} </span> </div>'
    purchespriceHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Purchase price:</h5> <span> {purches_price} </span> </div>'
    cashoutHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Cash-out:</h5> <span> {cash_out} </span> </div>'
    downpaymentHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Down payment:</h5> <span> {down_payment} </span> </div>'
    loanbalanceHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Loan balance:</h5> <span> {loan_balance} </span> </div>'
    creditscorevalueHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Credit score:</h5> <span> {credit_score_value} </span> </div>'
    termHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Loan term:</h5> <span> {term} </span> </div>'
    fotherHTML = f'<div style="background: #555; padding: 10px; font-size: 12px; text-align: center; color: #fff;">1Solution | Support | Privacy Policy<br>© 2021 Copyright: Zero 1Solution LLC, All rights reserved. 2111 West March Lane, Stockton CA 95207</div>'

    msg.html = f"{imgEnterpriseHTML} <br> {messageHTML} <br> {nameHTML} {emailHTML} {phoneHTML} <br> {productSHTML} <br> {namePHTML} {rateHTML} {aprHTML} {closingcostHTML} {monthlyHTML} <br> {captureuserSHTML} <br> {mortgagetypeHTML} {zipcodeHTML} {purchespriceHTML} {cashoutHTML} {downpaymentHTML} {loanbalanceHTML} {creditscorevalueHTML} {termHTML} <br><br> {fotherHTML}"
    mail.send(msg)

    msg = Message( "Response request", sender = email_lon_of, recipients = [ email_cli ] )

    messageBackHTML = f'<div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">I received your request, in one minute I will give you more information</h5></div>'
    messageBackHTML += f'<br> <div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Your password is: {cli_information_portal["password"]}</h5></div>'
    messageBackHTML += f'<br> <div style="margin-bottom: 15px;"> <h5 style="font-weight: 500;display: inline;">Please click <a href="https://1smtg.com/verify/{cli_information_portal["session_id"]}" target="_blank">here</a> to verify or on the verify button to access the portal</h5></div>'
    messageBackHTML += f'<br> <div style="margin-bottom: 15px; background: #aa1816; display: inline; padding: 10px; cursor: pointer; box-shadow: 4px 4px 8px 1px black;"> <a style="text-decoration: none; color: white; font-weight: 600;" href="https://1smtg.com/verify/{cli_information_portal["session_id"]}" target="_blank">verify email</a></div>'


    msg.html = f"{imgEnterpriseHTML} <br> {messageBackHTML}"
    mail.send(msg)
    return cli_information_portal, 200

@app.route("/getVideoById/<company>/<user_id>", methods=["GET"])
@cross_origin()
def getVideoById( company, user_id ):
    data = getInformationEnterpriseSQL( company )
    res = json.loads( data )
    data = getVideoByIdSQL( res[0]["id"], user_id )
    return data

@app.route("/uploadFiles/<company>", methods=["POST"])
@cross_origin()
def uploadFiles( company ):
    f = request.files.getlist("images[]")

    if not os.path.exists('filesCompany'):
       os.mkdir('filesCompany')

    for img in f:
        namecode = uuid.uuid4()
        filename = secure_filename(img.filename)

        root, extension = os.path.splitext(filename)

        addNewImageSQL( company, filename, f"{namecode}{extension}", namecode )

        img.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{namecode}{extension}"))

    return {"save": "yes"}, 200

@app.route("/uploadFlayers/<company>", methods=["POST"])
@cross_origin()
def uploadFlayers( company ):
    f = request.files.getlist("images[]")

    if not os.path.exists('flayersCompany'):
       os.mkdir('flayersCompany')

    for img in f:
        namecode = uuid.uuid4()
        filename = secure_filename(img.filename)

        root, extension = os.path.splitext(filename)

        addNewFlayerSQL( company, filename, f"{namecode}{extension}", namecode )

        img.save(os.path.join(app.config['UPLOAD_FLAYER'], f"{namecode}{extension}"))

    return {"save": "yes"}, 200

@app.route("/uploadBackgroundPages/<company>/<id>", methods=["POST"])
@cross_origin()
def uploadBackgroundPages( company, id ):
    f = request.files.getlist("images[]")

    if not os.path.exists('backgroundPage'):
       os.mkdir('backgroundPage')

    for img in f:
        namecode = uuid.uuid4()
        filename = secure_filename(img.filename)

        root, extension = os.path.splitext(filename)

        addNewBackgorundPageSQL( company, id, f"{namecode}{extension}" )

        img.save(os.path.join(app.config['UPLOAD_BACKGROUND'], f"{namecode}{extension}"))

    return {"save": "yes"}, 200

@app.route("/uploadBackgroundPagesVideo/<company>/<id>", methods=["POST"])
@cross_origin()
def uploadBackgroundPagesVideo( company, id ):
    f = request.files.getlist("images[]")

    if not os.path.exists('backgroundPage'):
       os.mkdir('backgroundPage')

    for img in f:
        namecode = uuid.uuid4()
        filename = secure_filename(img.filename)

        root, extension = os.path.splitext(filename)

        addNewBackgorundPageVideoSQL( company, id, f"{namecode}{extension}" )

        img.save(os.path.join(app.config['UPLOAD_BACKGROUND'], f"{namecode}{extension}"))

    return {"save": "yes"}, 200

@app.route("/getFile/<file_name>", methods=["GET"])
@cross_origin()
def getFile( file_name ):
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return os.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    return

@app.route("/getflayer/<file_name>", methods=["GET"])
@cross_origin()
def getflayer( file_name ):
    abs_path = os.path.join(app.config['UPLOAD_FLAYER'], file_name)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return os.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    return

@app.route("/getBackgroundPage/<file_name>", methods=["GET"])
@cross_origin()
def getBackgroundPage( file_name ):
    abs_path = os.path.join(app.config['UPLOAD_BACKGROUND'], file_name)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return os.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    return

@app.route("/deleteFileImgBackgrund/<name_file>", methods=["DELETE"])
@cross_origin()
def deleteFileImgBackgrund( name_file ):
    abs_path = os.path.join(app.config['UPLOAD_BACKGROUND'], name_file)
    os.remove(abs_path)
    return { "Delete": "yes" }, 200

@app.route("/deleteFileFlayers/<name_file>", methods=["DELETE"])
@cross_origin()
def deleteFileFlayers( name_file ):
    abs_path = os.path.join(app.config['UPLOAD_FLAYER'], name_file)
    os.remove(abs_path)
    return { "Delete": "yes" }, 200

@app.route("/deleteFileStamp/<name_file>", methods=["DELETE"])
@cross_origin()
def deleteFileStamp( name_file ):
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], name_file)
    os.remove(abs_path)
    return { "Delete": "yes" }, 200

@app.route("/getFooter/<company>", methods=["GET"])
@cross_origin()
def getFooter( company ):
    dataEn = getInformationEnterpriseSQL( company )
    res = json.loads( dataEn )
    data = getFooterSQL( res[0]["id"] )
    return data, 200

@app.route("/getContentLoanProgram/<company>/<product>/<page>", methods=["GET"])
@cross_origin()
def getContentLoanProgram( company, product, page ):
    data = []
    if product == "CONFORMING":
        data = getStatusProducsByCategory( company, page, product, 1 )
    elif product == "LIMITED_INCOME":
        data = getStatusProducsByCategory( company, page, product, 1 )
    elif product == "AGENCY_JUMBO":
        data = getStatusProducsByCategory( company, page, product, 1 )
    elif product == "FHA":
        data = getStatusProducsByCategory( company, page, product, 2, 3 )
    elif product == "USDA":
        data = getStatusProducsByCategory( company, page, product, 2, 4 )
    elif product == "VA":
        data = getStatusProducsByCategory( company, page, product, 2, 5 )
    elif product == "203K":
        data = getStatusProducsByCategory( company, page, product, 2, 6 )
    elif product == "Reverse":
        data = getStatusProducsByCategory( company, page, product, 2, 13 )
    elif product == "Non_QM":
        data = getStatusProducsByCategory( company, page, product, 3, 7 )
    elif product == "Jumbo":
        data = getStatusProducsByCategory( company, page, product, 3, 9 )
    elif product == "Simple":
        data = getStatusProducsByCategory( company, page, product, 4, 11 )
    return data, 200

@app.route("/getMortgagResources/<company>", methods=["GET"])
@cross_origin()
def getMortgagResources( company ):
    dataEn = getInformationEnterpriseSQL( company )
    res = json.loads( dataEn )
    data = getMortgagResourcesSQL( res[0]["id"] )
    return data, 200

@app.route("/getContentMortgagResources/<id_loan>", methods=["GET"])
@cross_origin()
def getContentMortgagResources( id_loan ):
    data = getContentMortgagResourcesSQL( id_loan )
    return data, 200

@app.route("/getFlayers/<company>", methods=["GET"])
@cross_origin()
def getFlayers( company ):
    dataEn = getInformationEnterpriseSQL( company )
    res = json.loads( dataEn )
    data = getFlayersSQL( res[0]["id"] )
    return data, 200
# Routes --

if __name__ == "__main__":
    # context = ('../1smtg.com/1smtg.com.crt', '../1smtg.com/1smtg.com.key')
    # context = ('server.crt', 'server.key')
    app.run( host='0.0.0.0', port=220, debug=True )
    # app.run( host='0.0.0.0', port=220, ssl_context=context )

# get url de la peticion https://stackoverflow.com/questions/15974730/how-do-i-get-the-different-parts-of-a-flask-requests-url