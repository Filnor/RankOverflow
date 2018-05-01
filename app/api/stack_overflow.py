from flask import jsonify
from urllib.request import urlopen
from datetime import datetime, timedelta
from pyquery import PyQuery as pq

from app.api import bp

@bp.route('/ranks/<int:user_id>', methods=['GET'])
def get_user_rank_last_page(user_id):
    #Get user's rank and last page first
    data = {
        "week": get_rank_page_by_mode("week", user_id),
        "month": get_rank_page_by_mode("month", user_id),
        "quarter": get_rank_page_by_mode("quarter", user_id),
        "year": get_rank_page_by_mode("year", user_id),
        "alltime": get_rank_page_by_mode("alltime", user_id)
    }

    response = jsonify(data)
    response.status_code = 200
    return response

def get_rank_page_by_mode(mode, user_id):
    #First day of week (last sunday)
    week_date = datetime.today() - timedelta(days=((datetime.today().weekday() + 1) % 7))
    week = "{:%Y-%m-%d}".format(week_date)

    #First day of month, is also used for quarter
    today_date = datetime.today()
    if today_date.day > 25:
        today_date += timedelta(7)
    month = "{:%Y-%m-%d}".format(today_date)

    #Current year
    year = "{:%Y}-01-01".format(datetime.today())

    modes = {
        "week": week,
        "month": month,
        "quarter": month,
        "year": year,
        "alltime": "2008-07-31"
    }

    page = urlopen("https://stackexchange.com/leagues/1/{}/stackoverflow/{}/{}?sort=reputationchange#{}".format(mode, modes[mode], user_id, user_id))
    html = page.read().decode("utf-8")
    jQuery = pq(html)

    user_rank = None
    max_page = None
    last_rank = None

    try:
        user_rank = int(pq(pq(pq(jQuery(".highlight").children()[2]).children()[0]).children()[0]).html()[1:])
        max_page = int(pq(pq(jQuery("[rel='next']").parent().children()[jQuery("[rel='next']").parent().children().length-2]).children()[0]).html())
    except IndexError:
        return {"user_rank": user_rank, "max_page": max_page}

    page = urlopen("https://stackexchange.com/leagues/1/{}/stackoverflow/{}?sort=reputationchange&page={}".format(mode, modes[mode], max_page))
    html = page.read().decode("utf-8")
    jQuery = pq(html)

    try:
        last_rank = int(pq(pq(pq(jQuery(".league-container").children()[jQuery(".league-container").children().length-1]).children()[0]).children()[0]).html()[1:])
    except IndexError:
        pass
    return {"user_rank": user_rank, "last_rank": last_rank, "max_page": max_page}
