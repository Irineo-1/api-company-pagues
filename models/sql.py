import re
from jinja2 import Undefined
from pandas.io import sql
import json
from models.conection import getConnection
import pandas as pd

def getAllUsersSQL( company, role, page ):
    page_int = int(page)
    page_mtp = page_int * 20
    conn = getConnection()
    sql = f"SELECT us.id, us.name, us.picture, us.role, us.title, us.nmls_id FROM users us INNER JOIN companies cp ON cp.id = us.company WHERE us.role = '{role}' AND cp.domain = '{company}' AND us.status = 'active' ORDER BY id ASC LIMIT {page_mtp}, 20"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getUserSQL( user_id ):
    conn = getConnection()
    sql = f"SELECT aboutme, name, picture, facebook, instagram, twitter, messenger, email, phone, nmls_id, title, branch FROM users WHERE id = '{user_id}'"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    return jsn

def getInformationEnterpriseSQL( company ):
    conn = getConnection()
    sql = f"SELECT * FROM companies WHERE domain = '{company}'"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getEnterpriseColorsSQl( company ):
    conn = getConnection()
    sql = f"SELECT color_head, color_text, color_footer, color_background_user, color_border_user, color_name, color_info_user, img_background, video_background FROM config_colors_page_company WHERE company = '{company}'"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getAllBlogs( company_id, page ):
    page_int = int( page )
    page_mtp = page_int * 10
    conn = getConnection()
    sql = f"SELECT id, title, sub_title, picture, date FROM blogs_company WHERE company = '{ company_id }' ORDER BY id ASC LIMIT {page_mtp}, 10"
    df = pd.read_sql( sql, conn )
    # df['date'] = pd.to_datetime( df['date'], errors='coerce' )
    # df['date'] = df['date'].dt.strftime('%m-%d-%Y')
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getBlogByIdSQL( blog_id ):
    conn = getConnection()
    sql = f"SELECT title, picture, body, date FROM blogs_company WHERE id = '{blog_id}'"
    df = pd.read_sql( sql, conn )
    # df['date'] = pd.to_datetime( df['date'], errors='coerce' )
    # df['date'] = df['date'].dt.strftime('%m-%d-%Y')
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getVideoByIdSQL( company, user_id ):
    conn = getConnection()
    sql = f"SELECT title, nameFile, linkVideo, nameUserCreate FROM video_messaging WHERE userid = '{ user_id }' AND company = '{ company }'"
    df = pd.read_sql( sql,conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def addNewImageSQL( company, fileName, nameCode, code ):
    conn = getConnection()
    cursor = conn.cursor()

    sql = f"INSERT INTO stamp_companies ( company, name_file, name_code, code ) VALUES ( %s, %s, %s, %s )"
    val = ( company, fileName, nameCode, code )

    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    return

def addNewBackgorundPageSQL( company, id, img_background ):
    conn = getConnection()
    cursor = conn.cursor()

    if( id ):
        sql = f"UPDATE config_colors_page_company SET img_background = '{img_background}' WHERE id = '{id}'"
        cursor.execute(sql)
    else:
        sql = f"INSERT INTO config_colors_page_company ( company, img_background ) VALUES ( %s, %s )"
        val = ( company, img_background )
        cursor.execute(sql, val)

    conn.commit()
    conn.close()
    return

def addNewBackgorundPageVideoSQL( company, id, video_background ):
    conn = getConnection()
    cursor = conn.cursor()

    if( id ):
        sql = f"UPDATE config_colors_page_company SET video_background = '{video_background}' WHERE id = '{id}'"
        cursor.execute(sql)
    else:
        sql = f"INSERT INTO config_colors_page_company ( company, video_background ) VALUES ( %s, %s )"
        val = ( company, video_background )
        cursor.execute(sql, val)

    conn.commit()
    conn.close()
    return

def getFooterSQL( company ):
    conn = getConnection()
    sql = f"SELECT * FROM stamp_companies WHERE company = '{ company }'"
    df = pd.read_sql( sql,conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getConformingSQL( company, page ):
    # conn = getConnection()
    # res_regex = re.search('[0-9]', page)
    # if( res_regex == None ): return {"response": f"incorrect page, you send: {page}"}
    # page_int = int(page)
    # limit_reg = page_int * 10
    # sql = "SELECT pr.name, pr.lender, pr.fixed, pr.arm, pr.fixed_30, pr.fixed_25, pr.fixed_20, pr.fixed_15, pr.fixed_10, pr.fixed_5, pr.arm_15y, pr.arm_10y, pr.arm_7y, pr.arm_5y, pr.arm_3y, pr.arm_1y, pr.arm_6m, pr.lp_purchase, pr.lp_rt, pr.lp_cashout, pr.adj_section, pr.term FROM products pr "
    # sql += "INNER JOIN lenders ld ON ld.id = pr.lender "
    # sql += "WHERE pr.active = 'yes' "
    # sql += "AND pr.category_type = 1 "
    # sql += "AND pr.limited_income <> 'yes' "
    # sql += "AND pr.high_balance <> 'yes' "
    # sql += "AND pr.ft_buyer <> 'yes' "
    # sql += "AND pr.down_payment <> 'yes' "
    # sql += f"ORDER BY NAME ASC LIMIT {limit_reg}, 20"
    # df = pd.read_sql( sql, conn )
    # jsn = pd.DataFrame.to_json( df, orient="records" )
    # conn.commit()
    # conn.close()

    # list_jsn = json.loads( jsn )
    fixed_list = getListFixed( 1, "CONFORMING" )
    arm_list = getListArm( 1, "CONFORMING" )
    list_compleate = fixed_list + arm_list
    return json.dumps(list_compleate)

def getLimitedIncomeSQL( company, page ):
    conn = getConnection()
    res_regex = re.search('[0-9]', page)
    if( res_regex == None ): return {"response": f"incorrect page, you send: {page}"}
    page_int = int(page)
    limit_reg = page_int * 10
    sql = "SELECT products.name, products.lender, products.fixed, products.arm, products.fixed_30, products.fixed_25, products.fixed_20, products.fixed_15, products.fixed_10, products.fixed_5, products.arm_15y, products.arm_10y, products.arm_7y, products.arm_5y, products.arm_3y, products.arm_1y, products.arm_6m, products.lp_purchase, products.lp_rt, products.lp_cashout, products.lp_purchase, products.limited_income, products.high_balance, products.ft_buyer, products.lp_rt, products.lp_cashout, products.adj_section, products.term FROM products "
    sql += "INNER JOIN lenders ON lenders.id = products.lender "
    sql += "WHERE products.active = 'yes' "
    sql += "AND category_type = 1 "
    sql += "AND products.limited_income = 'yes' "
    sql += F"ORDER BY NAME ASC LIMIT {limit_reg}, 20"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    
    list_jsn = json.loads( jsn )

    return list_jsn

def getAgencyJumboSQL( company, page ):
    conn = getConnection()
    res_regex = re.search('[0-9]', page)
    if( res_regex == None ): return {"response": f"incorrect page, you send: {page}"}
    page_int = int(page)
    limit_reg = page_int * 10
    sql = "SELECT products.name, products.lender, products.fixed, products.arm, products.fixed_30, products.fixed_25, products.fixed_20, products.fixed_15, products.fixed_10, products.fixed_5, products.arm_15y, products.arm_10y, products.arm_7y, products.arm_5y, products.arm_3y, products.arm_1y, products.arm_6m, products.limited_income, products.high_balance, products.ft_buyer, products.lp_rt, products.lp_cashout, products.lp_purchase, products.adj_section, products.term FROM products "
    sql += "INNER JOIN lenders ON lenders.id = products.lender "
    sql += "WHERE products.active = 'yes' "
    sql += "AND category_type = 1 "
    sql += "AND products.high_balance = 'yes' "
    sql += f"ORDER BY NAME ASC LIMIT {limit_reg}, 20"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()

    list_jsn = json.loads( jsn )

    return list_jsn

def getFXorARyear( type_f_a, c_type, lp, c_sql ):
    conn = getConnection()
    sql = f"SELECT COUNT(*) FROM products WHERE 'yes' IN "
    sql += f"(SELECT p.{lp} FROM products p "
    sql += f"WHERE p.{type_f_a} = 'yes' "
    sql += f"AND p.active = 'yes' "
    sql += f"AND p.category_type = {c_type} "
    if c_sql == "CONFORMING":
        sql += f"AND p.limited_income <> 'yes' "
        sql += f"AND p.high_balance <> 'yes' "
        sql += f"AND p.ft_buyer <> 'yes' "
        sql += f"AND p.down_payment <> 'yes') "
    elif c_sql == "LIMITED_INCOME":
        sql += "AND p.limited_income = 'yes') "
    elif c_sql == "AGENCY_JUMBO":
        sql += f"AND p.high_balance = 'yes') "
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    return jsn

def getLTVSQL( type_f_a, adj_type ):
    conn = getConnection()
    sql = "SELECT MIN( ltv0_60 ) AS ltv0_60, MIN( ltv60_70 ) AS ltv60_70, MIN( ltv70_75 ) AS ltv70_75, MIN( ltv75_80 ) AS ltv75_80, MIN( ltv80_85 ) AS ltv80_85, MIN( ltv85_90 ) AS ltv85_90, MIN( ltv90_95 ) AS ltv90_95, MIN( ltv95_97 ) AS ltv95_97, MIN( ltv97_more ) AS ltv97_more "
    sql += "FROM ms_adjustments msa "
    sql += "WHERE msa.adj_section IN "
    sql += "(SELECT adj_section FROM products WHERE "
    sql += f"{type_f_a} = 'yes' GROUP BY adj_section) "
    sql += f"AND (adj_type = '{adj_type}') "
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    return jsn

def getproductByTypesSQL( company, page, c_type, c_id ):
    conn = getConnection()
    res_regex = re.search('[0-9]', page)
    if( res_regex == None ): return {"response": f"incorrect page, you send: {page}"}
    page_int = int(page)
    limit_reg = page_int * 10
    sql = "SELECT products.name, products.fixed, products.arm, products.fixed_30, products.fixed_25, products.fixed_20, products.fixed_15, products.fixed_10, products.fixed_5, products.arm_15y, products.arm_10y, products.arm_7y, products.arm_5y, products.arm_3y, products.arm_1y, products.arm_6m, products.lp_purchase, products.limited_income, products.high_balance, products.ft_buyer, products.lp_rt, products.lp_cashout, lenders.company_name, lenders.id AS lender_id, products.adj_section, products.term FROM products "
    sql += "INNER JOIN product_types ON product_types.id = products.product_type "
    sql += "INNER JOIN lenders ON lenders.id = products.lender "
    sql += "WHERE products.active = 'yes' "
    sql += f"AND product_types.category_type = {c_type} "
    sql += f"AND product_types.id = {c_id} "
    sql += f"ORDER BY lenders.company_name ASC, products.name ASC LIMIT {limit_reg}, 20"
    df = pd.read_sql( sql, conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    
    list_jsn = json.loads( jsn )
    
    fixed_30y = list( filter( lambda x : x["fixed"] == "yes" and x["fixed_30"] == "yes", list_jsn ) )
    fixed_25y = list( filter( lambda x : x["fixed"] == "yes" and x["fixed_25"] == "yes", list_jsn ) )
    fixed_20y = list( filter( lambda x : x["fixed"] == "yes" and x["fixed_20"] == "yes", list_jsn ) )
    fixed_15y = list( filter( lambda x : x["fixed"] == "yes" and x["fixed_15"] == "yes", list_jsn ) )
    fixed_10y = list( filter( lambda x : x["fixed"] == "yes" and x["fixed_10"] == "yes", list_jsn ) )
    fixed_5y = list( filter( lambda x : x["fixed"] == "yes" and x["fixed_5"] == "yes", list_jsn ) )

    arm_15y = list( filter( lambda x : x["arm"] == "yes" and x["arm_15y"] == "yes", list_jsn ) )
    arm_10y = list( filter( lambda x : x["arm"] == "yes" and x["arm_10y"] == "yes", list_jsn ) )
    arm_7y = list( filter( lambda x : x["arm"] == "yes" and x["arm_7y"] == "yes", list_jsn ) )
    arm_5y = list( filter( lambda x : x["arm"] == "yes" and x["arm_5y"] == "yes", list_jsn ) )
    arm_3y = list( filter( lambda x : x["arm"] == "yes" and x["arm_3y"] == "yes", list_jsn ) )
    arm_1y = list( filter( lambda x : x["arm"] == "yes" and x["arm_1y"] == "yes", list_jsn ) )
    arm_6m = list( filter( lambda x : x["arm"] == "yes" and x["arm_6m"] == "yes", list_jsn ) )

    fixed_list = getListFixed( fixed_30y, fixed_25y, fixed_20y, fixed_15y, fixed_10y, fixed_5y )
    arm_list = getListArm( arm_15y, arm_10y, arm_7y, arm_5y, arm_3y, arm_1y, arm_6m )
    list_compleate = fixed_list + arm_list
    return json.dumps(list_compleate)

def addNewFlayerSQL( company, fileName, nameCode, code ):
    conn = getConnection()
    cursor = conn.cursor()

    sql = f"INSERT INTO website_flayers ( company, name_file, name_code, code ) VALUES ( %s, %s, %s, %s )"
    val = ( company, fileName, nameCode, code )

    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    return

def getFlayersSQL( company ):
    conn = getConnection()
    sql = f"SELECT * FROM website_flayers WHERE company = '{ company }'"
    df = pd.read_sql( sql,conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getMortgagResourcesSQL( company ):
    conn = getConnection()
    sql = f"SELECT id, title FROM mortgage_resources WHERE company = '{ company }'"
    df = pd.read_sql( sql,conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getContentMortgagResourcesSQL( id_loan ):
    conn = getConnection()
    sql = f"SELECT title, body FROM mortgage_resources WHERE id = '{ id_loan }'"
    df = pd.read_sql( sql,conn )
    jsn = pd.DataFrame.to_json( df, orient="records" )
    conn.commit()
    conn.close()
    return jsn

def getListFixed( category_type, c_sql ):
    list_f = [{
        "name": "Fixed 30 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_30", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_30", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_30", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 25 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_25", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_25", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_25", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 20 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_20", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_20", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_20", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 15 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_15", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_15", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_15", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 10 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_10", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_10", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_10", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 5 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_5", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_5", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_5", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "3-4 Units" ) ) ),
    }]
    return list_f

def getListArm( category_type, c_sql ):
    list_a = [{
        "name": "ARM 15 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_15y", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_15y", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_15y", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 10 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_10y", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_10y", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_10y", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 7 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_7y", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_7y", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_7y", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 5 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_5y", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_5y", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_5y", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 3 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_3y", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_3y", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_3y", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 1 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_1y", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_1y", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_1y", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 6 months",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_6m", category_type, "lp_purchase", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_6m", category_type, "lp_rt", c_sql)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_6m", category_type, "lp_cashout", c_sql)))[0]["COUNT(*)"] else "no",
        "NON OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "NON-OWNER" ) ) ),
        "2ND HOME":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2ND HOME" ) ) ),
        "2 Units":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2 Units" ) ) ),
        "3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "3 Units" ) ) ),
        "4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "4 Units" ) ) ),
        "2-3 Units":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2-3 Units" ) ) ),
        "2-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2-4 Units" ) ) ),
        "3-4 Units":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "3-4 Units" ) ) ),
    }]
    return list_a

def getMinLTV( list_s ):
    try:
        min = abs(list_s[0]["ltv0_60"])
        key_max = ""
        for key in list_s[0]:
            if not abs(list_s[0][key]) == 100.0 and abs(list_s[0][key]) > min or abs(list_s[0][key]) == min:
                min = abs(list_s[0][key])
                key_max = key
        years_supp = [int(s) for s in re.findall(r'-?\d+\.?\d*', key_max)]
        return f"{years_supp[0]}-{years_supp[1]}"
    except:
        return "no"