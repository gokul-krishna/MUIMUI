from flask import render_template, jsonify
from app import app
import random
from flask import send_from_directory
from sqlalchemy import desc
import os
from ..models import (db, User, InstaPost, UserInfluencerMap,
                      Products, InstaInfluencer)
from flask.ext.login import login_user, logout_user, login_required
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from flask.ext.bootstrap import Bootstrap
from tempfile import NamedTemporaryFile
import sys
import os
sys.path.insert(0, os.path.abspath('../model/'))
root_dir = os.path.dirname(os.getcwd()) + '/webapp/app/'

from inference import get_nn




bootstrap = Bootstrap(app)


class UploadFileForm(FlaskForm):
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')


@app.route('/js/<path:filename>')
def serve_js(filename):
    ''' Serve JS script given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'js'), filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    ''' Return images given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'images_2'), filename)


@app.route('/images_2/<path:filename>')
def serve_images_2(filename):
    ''' Return images given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'images_2'), filename)


@app.route('/tmp/<path:filename>')
def serve_tmp(filename):
    ''' Return images given a file name '''
    return send_from_directory('/tmp/', filename)


@app.route('/plugins/<path:filename>')
def serve_plugins(filename):
    ''' Return plugins given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'plugins'), filename)


@app.route('/styles/<path:filename>')
def serve_styles(filename):
    ''' Return styles given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'styles'), filename)


@app.route('/css/<path:filename>')
def serve_css(filename):
    ''' Return css given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'css'), filename)


@app.route('/')
@app.route('/index')
def index():
    ''' Return index template '''
    recent_posts = InstaPost.query.order_by(desc(InstaPost.post_date)
                                            ).limit(6).all()
    post_links = [i.post_link for i in recent_posts]
    return render_template('index_2.html',
                           authenticated=current_user.is_authenticated,
                           post_links=post_links)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ''' Return upload template '''
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file_selector.data
        file.seek(0)
        ftemp = NamedTemporaryFile(delete=False)
        file.save(ftemp)
        links = get_nn(ftemp.name)
        products = Products.query.filter(Products.id.in_(tuple(links))).all()
        products = products[1:]
        return render_template('discovery.html', products=products,
                               tmpfile=ftemp.name)

    return render_template('upload2.html', form=form)


@app.route('/product')
@login_required
def product():
    ''' Return template for maps '''
    # user_email = current_user.email
    # influencers = UserInfluencerMap.query.
    # filter_by(user_email=user_email).all()
    # influencers = [i.influencer_id for i in influencers]
    # influencers = InstaInfluencer.query\
    #                 .filter(InstaInfluencer.id.
    # in_(tuple(influencers))).all()
    # influencers = [i.user_name for i in influencers]
    # insta_urls = InstaPost.query.filter
    # (InstaPost.user_name.in_(tuple(influencers))
    #          ).order_by(desc(InstaPost.post_date))\
    #                                     .limit(5).all()
    insta_ids = [1, 2, 3, 4, 5]
    insta_urls = InstaPost.query.filter(InstaPost.id.in_(tuple(insta_ids)))
    insta_urls = [i.post_link + '/' for i in insta_urls]
    insta_urls = ["https://www.instagram.com/p/BuzBUyBnNfE/",
                  "https://www.instagram.com/p/BwVbhAaA69n/",
                  "https://www.instagram.com/p/BouFBEBn9X_/",
                  "https://www.instagram.com/p/BwhOFKbhgca/",
                  "https://www.instagram.com/p/BwQS0a5h5yZ/"]
    insta_filenames = ["../webapp/app/static/images/img_1.jpg", "../webapp/app/static/images/img_2.jpg",
                       "../webapp/app/static/images/img_3.jpg", "../webapp/app/static/images/img_4.jpg",
                       "../webapp/app/static/images/img_5.jpg"]
    # prod_ids = [get_nn(fname) for fname in insta_filenames]



    # one loop to get nn IDs for each of those 5 imgs
    # for id
    prod_ids = [[i for i in range(1, 5)] for i in range(5)]
    prod_list = [Products.query.filter(Products.id.in_(tuple(id)))
                for id in prod_ids]
    prices = [[str(p.price) for p in prod]for prod in prod_list]
    brand_names = [[p.brand for p in prod]for prod in prod_list]
    image_links = [[p.image_link for p in prod]for prod in prod_list]
    image_links = [["https://slimages.macysassets.com/is/image/MCY/products/8/optimized/12145238_fpx.tif?op_sharpen=1&wid=402&hei=489&fit=fit,1&$filtersm$&fmt=webp",
                    "https://slimages.macysassets.com/is/image/MCY/products/6/optimized/11950306_fpx.tif?op_sharpen=1&wid=402&hei=489&fit=fit,1&$filtersm$&fmt=webp",
                    "https://slimages.macysassets.com/is/image/MCY/products/7/optimized/11936317_fpx.tif?op_sharpen=1&wid=402&hei=489&fit=fit,1&$filtersm$&fmt=webp",
                    "https://slimages.macysassets.com/is/image/MCY/products/6/optimized/11485936_fpx.tif?op_sharpen=1&wid=402&hei=489&fit=fit,1&$filtersm$&fmt=webp"],
                    ["https://slimages.macysassets.com/is/image/MCY/products/2/optimized/11758882_fpx.tif?op_sharpen=1&wid=402&hei=489&fit=fit,1&$filtersm$&fmt=webp",
                    "https://slimages.macysassets.com/is/image/MCY/products/3/optimized/11471063_fpx.tif?op_sharpen=1&wid=402&hei=489&fit=fit,1&$filtersm$&fmt=webp",
                    "https://images.topshop.com/i/TopShop/TS10N09QBLS_M_1.jpg?$w1300$&fmt.jpeg.interlaced=true",
                    "https://lp2.hm.com/hmgoepprod?set=source[/09/25/0925bf2e8bd8d25618c68f1c48671d222b4fe67c.jpg],origin[dam],category[ladies_dresses_maxidresses],type[LOOKBOOK],res[m],res[s],hmver[1]&call=url[file:/product/main"],
                    ["https://slimages.macysassets.com/is/image/MCY/products/1/optimized/11567241_fpx.tif?op_sharpen=1&wid=1230&hei=1500&fit=fit,1&$filterxlrg$",
                    "https://s7d5.scene7.com/is/image/UrbanOutfitters/48376370_009_b?$xlarge$&hei=900&qlt=80&fit=constrain",
                    "https://images.topshop.com/i/TopShop/TS14P03QPNK_M_1.jpg?$Zoom$",
                    "https://www.forever21.com/images/1_front_750/00321430-03.jpg"] ,
                    ["https://www.forever21.com/images/2_side_750/00297044-01.jpg",
                    "https://www.forever21.com/images/1_front_750/00346568-02.jpg",
                    "https://images.asos-media.com/products/asos-design-maxi-dress-with-cape-back-and-dipped-hem-in-light-floral-print/11566990-1-lightfloralprint",
                    "https://lp2.hm.com/hmgoepprod?set=source[/02/72/0272c29eedad300c3644d1b9e717a21c5095b22d.jpg],origin[dam],category[ladies_dresses_shortdresses],type[LOOKBOOK],res[m],res[s],hmver[1]&call=url[file:/product/main"]
                    ]
    page_links = [[p.page_link for p in prod]for prod in prod_list]
    page_links[0] = ["https://www.macys.com/shop/product/i.n.c.-embroidered-wrap-top-created-for-macys?ID=8254928&tdp=cm_app~zMCOM-NAVAPP~xcm_zone~zSEARCH_ZONE_A~xcm_choiceId~zcidM88MGO-98d3b662-e929-4223-b02a-b083cef3a998%40H96%40Inspired%2Bby%2Byour%2Bbrowsing%2Bhistory%24%248254928~xcm_pos~zPos6~xcm_srcCatID~z255",
                     "https://www.macys.com/shop/product/i.n.c.-lace-wrap-top-created-for-macys?ID=8226833&CategoryID=255#fn=sp%3D1%26spc%3D305%26ruleId%3D78%7CREPLACE%20SAVED%20SET%26kws%3Dlace%20tops%26searchPass%3DmatchAll%26slotId%3D54",
                     "https://www.macys.com/shop/product/style-co-lace-yoke-handkerchief-hem-top-created-for-macys?ID=6339970&CategoryID=72085&swatchColor=Bright%20White#fn=sp%3D1%26spc%3D480%26ruleId%3D78%26searchPass%3DmatchNone%26slotId%3D6",
                     "https://www.macys.com/shop/product/free-people-kiss-kiss-embroidered-lace-tunic?ID=7996870&CategoryID=72085&swatchColor=Ivory#fn=sp%3D1%26spc%3D480%26ruleId%3D78%26searchPass%3DmatchNone%26slotId%3D2"]

    page_links[1] = ["https://www.macys.com/shop/product/b-darlin-juniors-lace-wrap-dress?ID=8150897&pla_country=US&CAGPSPN=pla&CAWELAID=120156340033818016&CAAGID=66531881240&CATCI=aud-302288356980:pla-674013357759&cm_mmc=Google_Womens_PLA-_-RTW_Womens_Women%27s_Dresses_-_GS_B_Darlin-_-319761262057-_-pg1051468570_c_kclickid_c8bad234-1880-4250-9c34-91d6ac2b3dbe_KID_EMPTY_202344541_66531881240_319761262057_aud-302288356980:pla-674013357759_886542949652USA__c_KID_&trackingid=424x1051468570&m_sc=sem&m_sb=Google&m_tp=PLA&m_ac=Google_Womens_PLA&m_ag=BDarlin&m_cn=RTW_Womens_Women%27s_Dresses_-_GS&m_pi=go_cmp-202344541_adg-66531881240_ad-319761262057_aud-302288356980:pla-674013357759_dev-c_ext-_prd-886542949652USA&catargetid=120156340034688989&cadevice=c&gclid=Cj0KCQjw2IrmBRCJARIsAJZDdxDYtLjtxiZ46cMIrCX1CbrZGuZHFiOaoKgA37r7dCT5rWXvlOsNHIYaAvIHEALw_wcB",
                     "https://www.macys.com/shop/product/speechless-juniors-flutter-sleeve-fit-flare-dress?ID=7924463&tdp=cm_app~zMCOM-NAVAPP~xcm_zone~zPDP_ZONE_A~xcm_choiceId~zcidM05MDR-52590779-2385-48e2-8d93-1bede34552ee%40H7%40customers%2Balso%2Bshopped%245449%247924463~xcm_pos~zPos3~xcm_srcCatID~z18109",
                     "https://www.topshop.com/en/tsuk/product/clothing-427/dresses-442/buckle-wrap-mini-dress-8514603",
                     "https://www2.hm.com/en_us/productpage.0646676002.html?gclid=Cj0KCQjw2IrmBRCJARIsAJZDdxA8ReEPtRRvkyuIF9jLvsiK0RT5ZGSkOQ61mmbYkyKEGU1cvoXZSToaAv_2EALw_wcB&CAWELAID=120032800000156036&ef_id=Cj0KCQjw2IrmBRCJARIsAJZDdxA8ReEPtRRvkyuIF9jLvsiK0RT5ZGSkOQ61mmbYkyKEGU1cvoXZSToaAv_2EALw_wcB:G:s&s_kwcid=AL!860!3!336559326893!!!g!652378893109"]
    page_links[2] = ["https://www.macys.com/shop/product/bcbgmaxazria-ruffled-open-back-romper?ID=8224632&tdp=cm_app~zMCOM-NAVAPP~xcm_zone~zPDP_ZONE_B~xcm_choiceId~zcidM06MAU-6b93c713-cb04-42f8-ab21-132d8fca8236%40H8%40customers%2Balso%2Bloved%24181942%248224632~xcm_pos~zPos2~xcm_srcCatID~z181942",
                     "https://www.urbanoutfitters.com/shop/uo-elaine-floral-off-the-shoulder-mini-dress",
                     "http://us.topshop.com/en/tsus/product/clothing-70483/rompers-jumpsuits-4107634/pink-gingham-bardot-playsuit-8618112",
                     "https://www.forever21.com/us/shop/catalog/product/f21/dress_romper/2000321430"]
    page_links[3] = ["http://us.topshop.com/en/tsus/product/clothing-70483/trend-polkadot-7639579/horse-coin-midi-8353647",
                     "https://www.urbanoutfitters.com/shop/uo-elaine-floral-off-the-shoulder-mini-dress",
                     "http://us.topshop.com/en/tsus/product/clothing-70483/rompers-jumpsuits-4107634/pink-gingham-bardot-playsuit-8618112",
                     "https://www.forever21.com/us/shop/catalog/product/f21/dress_romper/2000321430"]

    prices[0] = ['$89.50','$79.50','$54.50', '$128.00']
    brand_names[0] = ['INC International Concepts','INC International Concepts','Style & Co','Free People']
    description[0] = ["I.N.C. International Concepts takes the wrap top to new heights with this delicately embroidered volume-sleeve style, finished with an oversized tie at the side.",
                      "Get your hands on this gorgeous lace top from I.N.C. International Concepts, in a flattering wrap style with a tie at the side waist.",
                      "Lightweight and airy, this flowing top by Style & Co features lace detailing at the yoke and front placket as well as a handkerchief hemline for plenty of boho flair.",
                      "Pretty touches of embroidery and lace detail a flowy silhouette with this beautiful pullover tunic from Free People. "]

    description = [[p.description for p in prod]for prod in prod_list]

    # prices = [['$'+str(i) for i in range(1,5)] for i in range(5)]
    # brand_names = [['A','B','C','D'], ['A','B','C','D'], ['A','B','C','D'],
    #           ['A','B','C','D'], ['A','B','C','D']]
    # descp = "blah blah blah"
    # description = [[descp for i in range(4)] for i in range(5)]
    # image_links = [[hrefs for i in range(4)] for i in range(5)]
    # brand_name = Products.query.filter_by(Products.brands)

    return render_template('product.html', insta_url=insta_urls,
                           brand_names=brand_names, prices=prices,
                           description=description, image_links=image_links,
                           page_links=page_links)


@app.route('/contact')
def contact():
    ''' Return template for contacts '''
    return render_template('contact.html', title='Contact')


@app.route('/about')
def about():
    ''' Return template for contacts '''
    return render_template('aboutus.html', title='Contact')
