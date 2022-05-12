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
    # res[0]["email"]
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

@app.route("/getContentLoanProgram/<company>/<category_type>/<page>", methods=["GET"])
@cross_origin()
def getContentLoanProgram( company, category_type, page ):
    data = []
    if category_type == "CONFORMING":
        data = getConformingSQL( company, page )
    elif category_type == "LIMITED_INCOME":
        data = getLimitedIncomeSQL( company, page )
    elif category_type == "AGENCY_JUMBO":
        data = getAgencyJumboSQL( company, page )
    elif category_type == "FHA":
        data = getproductByTypesSQL( company, page, 2, 3 )
    elif category_type == "USDA":
        data = getproductByTypesSQL( company, page, 2, 4 )
    elif category_type == "VA":
        data = getproductByTypesSQL( company, page, 2, 5 )
    elif category_type == "203K":
        data = getproductByTypesSQL( company, page, 2, 6 )
    elif category_type == "Reverse":
        data = getproductByTypesSQL( company, page, 2, 13 )
    elif category_type == "Non_QM":
        data = getproductByTypesSQL( company, page, 3, 7 )
    elif category_type == "Jumbo":
        data = getproductByTypesSQL( company, page, 3, 9 )
    elif category_type == "Simple":
        data = getproductByTypesSQL( company, page, 4, 11 )
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
    # context = ('server.crt', 'server.key')
    app.run( host='0.0.0.0', port=220, debug=True )
    # app.run( host='0.0.0.0', port=220, ssl_context=context )

# get url de la peticion https://stackoverflow.com/questions/15974730/how-do-i-get-the-different-parts-of-a-flask-requests-url