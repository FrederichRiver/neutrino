#!/usr/bin/python3
import requests


class tarantula(object):
    def __init__(self):
        self.start_url = 'https://www.zhihu.com/signin?next=%2F'
        # self.start_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.session = requests.session()
        self.headers = {
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        self.login_headers = {
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            "cookie": '_zap=5aaa77ee-0605-4d02-aebf-9720e4da4579; _xsrf=fdc145b4-2e24-48fb-a855-9d67e1a2eddc; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1583756360,1584202172,1584854816; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1584978905; KLBRSID=57358d62405ef24305120316801fd92a|1584978905|1584978902; d_c0="AHCeYl0aAhGPTiXL0hmySYEt5ntUI27vW4o=|1584978905"; capsion_ticket="2|1:0|10:1584978905|14:capsion_ticket|44:OGJjYTk3OWI3M2M1NDAzZDlkNmE2ZTM0Yjk0ZjZiY2E=|a234a3824f14660a32f10c9f33172ed52395d87cba879bde979d0e53985fd22a"; _ga=GA1.2.1605611667.1584978906; _gid=GA1.2.49021677.1584978906; _gat_gtag_UA_149949619_1=1',
            "x-ab-param": 'se_click_club=0;tp_meta_card=0;se_sug=1;se_websearch=3;soc_adreadfilter=0;soc_adsort=0;zr_intervene=0;se_new_topic=0;se_ctx_rerank=1;se_webrs=1;li_tjys_ec_ab=0;zr_km_slot_style=event_card;se_cbert=0;soc_cardheight=2;top_hotcommerce=1;pf_fuceng=1;se_colorfultab=1;se_payconsult=0;zr_update_merge_size=1;se_timebox_up=0;tp_club_tab_feed=0;li_vip_no_ad_mon=0;zw_sameq_sorce=999;se_entity_model=0;zr_km_sku_thres=false;se_cate_l3=0;ug_newtag=0;soc_authormore=2;tsp_vote=2;top_test_4_liguangyi=1;ug_follow_answerer=0;se_billboardsearch=0;se_sug_term=0;tp_topic_tab=0;ug_goodcomment_0=1;ug_fw_answ_aut_1=0;se_zu_onebox=0;tp_qa_metacard_top=top;soc_update=1;zr_art_rec=base;zr_video_rank=new_rank;soc_adreadline=0;soc_iospinweight=0;pf_adjust=0;se_cbert_ab=1;soc_newfeed=2;li_se_heat=1;zr_answer_rec_cp=open;zr_search_sim=0;qap_article_like=1;se_topiclabel=1;tsp_hotlist_ui=1;soc_iosreadfilter=0;top_ebook=0;se_col_boost=0;se_p_slideshow=0;tp_club_feed=1;soc_special=0;top_universalebook=1;se_aa_base=0;se_relationship=1;se_college_cm=0;se_whitelist=0;se_rel_search=0;soc_adpinweight=0;zr_rel_search=base;se_expired_ob=0;se_college=default;se_spb309=0;tp_topic_rec=1;soc_ri_merge=0;li_query_match=0;li_se_across=0;se_highlight=0;ls_zvideo_rec=2;top_ydyq=X;zr_video_rank_nn=new_rank;li_catalog_card=1;zr_expslotpaid=1;tp_header_style=1;li_yxzl_new_style_a=1;tp_score_1=a;tp_club_qa_pic=1;qap_question_visitor= 0;soc_brdcst3=0;top_new_feed=5;ug_zero_follow_0=0;sem_up_growth=in_app;li_paid_answer_exp=0;li_ebok_chap=0;se_pek_test3=1;ug_zero_follow=0;top_v_album=1;ls_zvideo_license=1;se_qanchor=0;se_wannasearch=0;soc_zcfw_shipinshiti=1;soc_zcfw_broadcast=0;se_cardrank_2=1;soc_notification=0;se_hotmore=2;tsp_videobillboard=1;li_answer_card=0;li_answers_link=0;zr_km_sku_mix=sku_20;li_se_media_icon=1;pf_creator_card=1;tp_discover_copy=0;ug_follow_answerer_0=0;se_ffzx_jushen1=0;tp_sft_v2=d;qap_thanks=1;zr_slotpaidexp=1;se_cardrank_1=0;zw_payc_qaedit=0;se_adxtest=1;se_presearch_ab=0;soc_wonderuser_recom=2;soc_zcfw_broadcast2=1;li_answer_label=0;li_qa_btn_text=0;se_lottery=0;se_ios_spb309=0;se_pek_test=1;soc_leave_recommend=2;zr_km_feed_nlp=old;zr_rec_answer_cp=close;zr_article_new=close;se_suggest_cache=0;pf_noti_entry_num=0;zr_slot_cold_start=aver;zr_training_first=false;soc_zuichangfangwen=0;top_quality=0;ug_follow_topic_1=2;qap_ques_invite=0;se_topicfeed=0;ls_recommend_test=0;li_purchase_test=0;se_ltr_cp_new=0;top_root=0;se_prf=0;se_zu_recommend=0;soc_brdcst4=3;li_svip_tab_search=0;li_sku_bottom_bar_re=0;se_hotsearch_2=1;li_ebook_audio=0;se_famous=1;tp_club_tab=0;li_se_edu=0;se_webtimebox=0;se_ltr_dnn_cp=0;li_salt_hot=1;li_hot_score_ab=0;tp_club_header=1;li_se_section=0;zr_ans_rec=gbrank;soc_bignew=1;se_club_post=5;soc_userrec=0;se_ltr_video=0;se_movietab=1;se_likebutton=0;se_webmajorob=0;li_video_section=0;tp_club_join=0;li_ebook_read=0;li_album_liutongab=0;se_agency= 0;tp_club_pk=1;se_multianswer=0;tp_club_pic=0.6;soc_feed_intimacy=2;se_pek_test2=1;se_use_zitem=0;tp_topic_style=0;qap_question_author=0;tp_club_pic_swiper=0;soc_zcfw_badcase=0;soc_bigone=0;ls_videoad=2;li_assessment_show=1;li_pay_banner_type=6;zr_video_recall=current_recall;se_amovietab=1;soc_iosreadline=0;qap_payc_invite=0;se_entity_model_14=0;se_featured=1;se_subtext=0;soc_authormore2=2;li_android_vip=0;se_hotsearch_num=0;se_backsearch=0;tp_qa_metacard=1;tp_topic_head=0;li_search_v5=0;se_auto_syn=0;se_cardrank_3=0;tp_club_android_feed=old;tp_topic_tab_new=0-0-0;li_education_box=0;li_answer_right=0;zr_km_style=base;tp_club_qa=1;tp_discover=0;tp_sft=a;se_bert_comp=0;se_site_onebox=0;se_mobileweb=1;se_time_threshold=0;tp_topic_entry=0;li_qa_new_cover=1;se_sug_entrance=1;se_new_merger=1;se_hotsearch=0;se_search_feed=N;li_hot_voted=0;zr_slot_training=1;zr_slot_filter=false;tp_m_intro_re_topic=1;ls_fmp4=0;soc_iosintimacy=2;se_related_index=3;se_preset_tech=0;soc_stickypush=1;zr_test_aa1=0;tp_sticky_android=2;zr_km_answer=open_cvr;se_hot_timebox=0;soc_iossort=0;li_svip_cardshow=0;se_relation_1=0;se_waterfall=0;se_ad_index=10;tp_club_android_join=1;soc_yxzl_zcfw=0;pf_newguide_vertical=0;pf_foltopic_usernum=50;se_preset_label=1;se_cardrank_4=1;tp_qa_toast=1',
            "x-zse-83": '3_2.0',
            "x-zse-86": "1.0_a8Yyk69yo0OxghY8hG2qUbuBk_xfbLOyfLYBUgu0QX2p",
            "x-requested-with": 'fetch',
            "referer": 'https://www.zhihu.com/signin?next=%2F'
        }

    def run(self):
        import re
        import json
        response = self.session.get(self.start_url, headers=self.headers)
        result = response.headers
        pattern = r'_xsrf=([a-z0-9\-]+)'
        xsrf = re.findall(pattern, str(response.headers))
        print(xsrf[0])
        with open('zhihu.header', 'w') as f:
            f.write(str(response.headers))
        with open('zhihu.text', 'w') as f:
            f.write(str(response.text))
        form_data = {
            "name": ''
        }
        p2 = r'"captchaNeeded":([a-z]+)'
        cap_need = re.findall(p2, response.text)
        print(cap_need[0])
        self.captcha_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=cn"
        cap_result = self.session.post(self.captcha_url, headers=self.login_headers)
        print(cap_result)
        # self.login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
        # result = self.session.post(self.login_url)
        # print(result)


def _get_signature(self, timestamp):
    ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
    grant_type = self.login_data['grant_type']
    client_id = self.login_data['client_id']
    source = self.login_data['source']
    ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
    return ha.hexdigest()


def _get_xsrf():
    pass

"""
request_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
# "cookie": '_zap=9d5d1617-95e1-41b0-8fdc-9ebe08f532c7; d_c0="ANDXmq7i7xCPTlIkz1GioQD14MrkA-BdxWU=|1583756348"; _ga=GA1.2.750210372.1583756361; tst=r; _xsrf=lnmXFSI9tM6XUerDd72s7hBBVYaqGSUJ; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1583756360,1584202172,1584854816; _gid=GA1.2.320287222.1584854817; q_c1=de90185a939644b3aaf4b4c396b285ad|1584875523000|1584875523000; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1584877986; capsion_ticket="2|1:0|10:1584878087|14:capsion_ticket|44:YjQzYjkzZDA3NDVlNDhhMWI5YzFkYjE1NDEyYjQyNjk=|aa08a44c5c450f7b8f3402df4fdd25ad69d88701c00ddf06d4c719cde48d6eb4"; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1584878205|158487548',
headers = {
    "x-xsrftoken": 'lnmXFSI9tM6XUerDd72s7hBBVYaqGSUJ',
    "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    "content-type": 'application/x-www-form-urlencoded'
    "x-zse-83": '3_2.0'
}
form_data = None
timestamp = str(int(time.time()*1000))

resp = self.session.get(api, headers=headers)
show_captcha = re.search(r'true', resp.text)
if show_captcha:
    put_resp = self.session.put(api, headers=headers)
    img_base64 = re.findall(
        r'"img_base64":"(.+)"', put_resp.text, re.S)[0].replace(r'\n', '')
    with open('./captcha.jpg', 'wb') as f:
        f.write(base64.b64decode(img_base64))
        img = Image.open('./captcha.jpg')
"""


if __name__ == "__main__":
    event = tarantula()
    event.run()
