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

def getStatusProducsByCategory( company, page, product, c_type, c_id = "" ):
    fixed_list = getListFixed( c_type, product, c_id )
    arm_list = getListArm( c_type, product, c_id )
    list_compleate = fixed_list + arm_list
    return json.dumps( list_compleate )

def getFXorARyear( type_f_a, c_type, lp, c_sql, c_id ):
    conn = getConnection()
    sql = f"SELECT COUNT(*) FROM products WHERE 'yes' IN "
    sql += f"(SELECT p.{lp} FROM products p "
    if c_id:
        sql += f"INNER JOIN product_types pt ON pt.id = p.product_type "
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
    elif c_id:
        sql += f"AND pt.category_type = {c_type} "
        sql += f"AND pt.id = {c_id}) "
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

def getListFixed( category_type, c_sql, c_id ):
    list_f = [{
        "name": "Fixed 30 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_30", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_30", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_30", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "fixed_30", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 25 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_25", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_25", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_25", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "fixed_25", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 20 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_20", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_20", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_20", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "fixed_20", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 15 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_15", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_15", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_15", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "fixed_15", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 10 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_10", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_10", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_10", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "fixed_10", "3-4 Units" ) ) ),
    },
    {
        "name": "Fixed 5 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("fixed_5", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("fixed_5", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("fixed_5", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "fixed_5", "3-4 Units" ) ) ),
    }]
    return list_f

def getListArm( category_type, c_sql, c_id ):
    list_a = [{
        "name": "ARM 15 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_15y", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_15y", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_15y", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_15y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 10 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_10y", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_10y", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_10y", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_10y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 7 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_7y", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_7y", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_7y", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_7y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 5 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_5y", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_5y", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_5y", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_5y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 3 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_3y", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_3y", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_3y", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_3y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 1 years",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_1y", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_1y", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_1y", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_1y", "3-4 Units" ) ) ),
    },
    {
        "name": "ARM 6 months",
        "lp_purchase": "yes" if (json.loads(getFXorARyear("arm_6m", category_type, "lp_purchase", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_rt": "yes" if (json.loads(getFXorARyear("arm_6m", category_type, "lp_rt", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "lp_cashout": "yes" if (json.loads(getFXorARyear("arm_6m", category_type, "lp_cashout", c_sql, c_id)))[0]["COUNT(*)"] else "no",
        "NON_OWNER":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "NON-OWNER" ) ) ),
        "HOME_2ND":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2ND HOME" ) ) ),
        "Units_2":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2 Units" ) ) ),
        "Units_3":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "3 Units" ) ) ),
        "Units_4":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "4 Units" ) ) ),
        "Units_2_3":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2-3 Units" ) ) ),
        "Units_2_4":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "2-4 Units" ) ) ),
        "Units_3_4":  getMinLTV( json.loads( getLTVSQL( "arm_6m", "3-4 Units" ) ) ),
    }]
    return list_a

def getMinLTV( list_s ):
    try:
        min = abs(list_s[0][" "])
        key_max = ""
        for key in list_s[0]:
            if not abs(list_s[0][key]) == 100.0 and abs(list_s[0][key]) > min or abs(list_s[0][key]) == min:
                min = abs(list_s[0][key])
                key_max = key
        years_supp = [int(s) for s in re.findall(r'-?\d+\.?\d*', key_max)]
        return f"{years_supp[1]}"
    except:
        return "no"