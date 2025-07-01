from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from flask import (
    Blueprint, g, render_template, request
)
from pytz import timezone
from werkzeug.exceptions import abort

from flask_app.auth import editor_required
from flask_app.db import get_db


utc = timezone('UTC')
central = timezone('US/Central')


bp = Blueprint('opportunities', __name__)


def get_opportunities():
    '''Gets all active opportunities plus those that have occured in the last
    45 days.

    Includes recurring opportunities and anytime opportunities that either don't
    have an expiration_date or have one that is greater than the current date.

    Returns:
        opportunities(arr): An array of opportunity dicts.
    '''
    opportunities = []
    with get_db() as cursor:
        cursor.execute(
            """SELECT
                    id,
                    owner,
                    title,
                    body,
                    anywhere,
                    anytime,
                    location,
                    city,
                    event_start,
                    event_end,
                    expiration_date,
                    category,
                    project_id,
                    recurring_weekly,
                    recurring_monthly,
                    link,
                    just_show_up
                FROM opportunities
                WHERE (event_start >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 45 DAY) AND (expiration_date IS NULL OR expiration_date >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 45 DAY)))
                    OR (anytime IS TRUE AND (expiration_date IS NULL OR expiration_date >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 45 DAY)))
                    OR (recurring_weekly IS TRUE AND (expiration_date IS NULL OR expiration_date >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 45 DAY)))
                    OR (recurring_monthly IS NOT NULL AND (expiration_date IS NULL OR expiration_date >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 45 DAY)))"""
        )
        db_opportunities = cursor.fetchall()

    for opp in db_opportunities:
        opportunities.append({
            'id': opp[0],
            'owner': opp[1],
            'title': opp[2],
            'body': opp[3],
            'anywhere': opp[4] == 1,
            'anytime': opp[5] == 1,
            'location': opp[6],
            'city': opp[7],
            'event_start': utc.localize(opp[8]) if opp[8] else None,
            'event_end': utc.localize(opp[9]) if opp[9] else None,
            'expiration_date': utc.localize(opp[10]) if opp[10] else None,
            'category': opp[11],
            'project_id': opp[12],
            'recurring_weekly': opp[13] == 1,
            'recurring_monthly': opp[14],
            'link': opp[15],
            'just_show_up': opp[16] == 1
        })

    return opportunities


def convert_to_local_time(opp, day=None, original_hour=None):
    '''Converts opp(dict)'s event_start, event_end, and expiration_date from utc
    to YYYY-MM-DD HH:mm local time.'''
    if opp.get('expiration_date'):
        opp['expiration_date'] = opp['expiration_date'].astimezone(central).strftime('%Y-%m-%d %H:%M')
    if opp.get('event_start'):
        event_length = timedelta(seconds=3600)
        if opp.get('event_end'):
            event_length = opp['event_end'] - opp['event_start']
        if day:
            opp['event_start'] = day
        localized_start = opp['event_start'].astimezone(central)
        if original_hour and localized_start.hour != original_hour:
            localized_start = localized_start.replace(hour=original_hour)
        opp['event_start'] = localized_start.strftime('%Y-%m-%d %H:%M')
        opp['event_end'] = (localized_start + event_length).strftime('%Y-%m-%d %H:%M')


def find_recurring(opportunities):
    '''Adds all opportunity recurrences to opportunities array.

    Parameters:
    opportunities (arr): a list of opportunity dicts with expiration_date,
        event_start, event_end, recurring_weekly, and recurring_monthly

    Returns:
    all_opportunities (arr): a list of opportunity dicts that inlcudes all
        occurences of recurring events from 45 days back to 3 months in the
        future.
    '''
    # TODO refactor maybe at some point.
    all_opportunities = []
    now = datetime.now(tz=utc)
    six_months_out = now + relativedelta(months=6)
    fortyfive_days_ago = now - timedelta(days=45)
    for opp in opportunities:
        expiration_date = None
        if opp['expiration_date']:
            expiration_date = opp['expiration_date']
        if opp['recurring_weekly']:
            # adds opp every 7 days for 3 months out (accounting for expiration_date).
            day = opp['event_start']
            original_hour = day.astimezone(central).hour
            while day < fortyfive_days_ago:
                day += timedelta(days=7)
            while day <= six_months_out and (not expiration_date or day <= expiration_date):
                new_opp = opp.copy()
                convert_to_local_time(new_opp, day, original_hour)
                all_opportunities.append(new_opp)
                day += timedelta(days=7)
        elif opp['recurring_monthly']:
            # adds opp every month for 3 months out (accounting for expiration_date).
            day = opp['event_start']
            original_hour = day.astimezone(central).hour
            at_least_date = (opp['recurring_monthly'] - 1) * 7
            while day < fortyfive_days_ago or day.day <= at_least_date:
                day += timedelta(days=7)
            while day <= six_months_out and (not expiration_date or day <= expiration_date):
                new_opp = opp.copy()
                convert_to_local_time(new_opp, day, original_hour)
                all_opportunities.append(new_opp)
                current_month = day.month
                while day.month == current_month or day.day <= at_least_date:
                    day += timedelta(days=7)
        else:
            # adds non-recurring opps as-is.
            convert_to_local_time(opp)
            all_opportunities.append(opp)

    return all_opportunities

def clean_city(city):
    '''Capitalizes each letter in city(str)'''
    if city:
        return city.title()
    else:
        return None

def clean_date(dt):
    '''Deals with am/pm input and converts to utc datetime object'''
    if dt:
        pm = "pm" in dt
        dt = dt[:-3]
        dat = central.localize(datetime.strptime(dt, '%Y-%m-%d %H:%M'))
        # don't add 12 hours to 12pm
        if pm and dat.hour != 12:
            dat += timedelta(hours=12)
        return dat.astimezone(utc)
    else:
        return None


def get_opportunity(id):
    '''Fetches opportunity from database by id.'''
    opportunity = None
    with get_db() as cursor:
        cursor.execute(
            """SELECT id, owner, title, body, anywhere, anytime, location, city,
                        event_start,
                        event_end,
                        expiration_date,
                        category, project_id, recurring_weekly,
                        recurring_monthly, link, just_show_up
                FROM opportunities
                WHERE id = %(id)s""",
            {'id': id}
        )
        opportunity = cursor.fetchone()

    if opportunity is None:
        abort(404, f"Post id {id} doesn't exist.")

    return opportunity


def convert_to_readable_local(dt):
    '''Converts UTC datetime to central YYYY-MM-DD HH:mm'''
    return utc.localize(dt).astimezone(central).strftime('%Y-%m-%d %H:%M') if dt else None


@bp.route('/api/opportunities')
def list():
    return find_recurring(get_opportunities())


@bp.route('/api/create', methods=['POST'])
@editor_required
def create():
    with get_db() as cursor:
        try:
            cursor.execute(
                """INSERT INTO opportunities (owner, title, body, anywhere,
                            anytime, location, city, event_start, event_end,
                            expiration_date, category, project_id,
                            recurring_weekly, recurring_monthly, link,
                            just_show_up)
                    VALUES (%(owner)s, %(title)s, %(body)s, %(anywhere)s,
                            %(anytime)s, %(location)s, %(city)s,
                            %(event_start)s, %(event_end)s, %(expiration_date)s,
                            %(category)s, %(project_id)s,
                            %(recurring_weekly)s, %(recurring_monthly)s,
                            %(link)s, %(just_show_up)s)""",
                {
                    'owner': g.user['id'],
                    'title': request.form['title'],
                    'body': request.form['body'],
                    'anywhere': 1 if request.form.get('anywhere') == 'true' else 0,
                    'anytime': 1 if request.form.get('anytime') == 'true' else 0,
                    'location': request.form.get('location') or None,
                    'city': clean_city(request.form.get('city')),
                    'event_start': clean_date(request.form.get('event_start')),
                    'event_end': clean_date(request.form.get('event_end')),
                    'expiration_date': clean_date(request.form.get('expiration_date')),
                    'category': request.form['category'],
                    'project_id': request.form['at_category'] if request.form['category'] == 'AT' else request.form.get('project_id'),
                    'recurring_weekly': 1 if request.form.get('recurring_weekly') == 'true' else 0,
                    'recurring_monthly': request.form.get('recurring_monthly') or None,
                    'link': request.form.get('link') or None,
                    'just_show_up': 1 if request.form.get('just_show_up') == 'true' else 0,
                }
            )
        except Exception as e:
            return { 'error': str(e) }, 400
    return { 'success': True }


@bp.route('/api/update/<int:id>', methods=['POST'])
@editor_required
def update(id):
    try:
        with get_db() as cursor:
            cursor.execute(
                """SELECT owner
                    FROM opportunities
                    WHERE id = %(id)s""",
                { 'id': id }
            )
            owner = cursor.fetchone()[0]
            if not g.user['admin'] and g.user['id'] != owner:
                return { 'error': 'User does not have permission' }, 400
            cursor.execute(
                """UPDATE opportunities
                    SET
                        title = %(title)s,
                        body = %(body)s,
                        anywhere = %(anywhere)s,
                        anytime = %(anytime)s,
                        location = %(location)s,
                        city = %(city)s,
                        event_start = %(event_start)s,
                        event_end = %(event_end)s,
                        expiration_date = %(expiration_date)s,
                        category = %(category)s,
                        project_id = %(project_id)s,
                        recurring_weekly = %(recurring_weekly)s,
                        recurring_monthly = %(recurring_monthly)s,
                        link = %(link)s,
                        just_show_up = %(just_show_up)s
                    WHERE id = %(id)s""",
                {
                    'id': id,
                    'title': request.form['title'],
                    'body': request.form['body'],
                    'anywhere': 1 if request.form.get('anywhere') == 'true' else 0,
                    'anytime': 1 if request.form.get('anytime') == 'true' else 0,
                    'location': request.form.get('location') or None,
                    'city': clean_city(request.form.get('city')),
                    'event_start': clean_date(request.form.get('event_start')),
                    'event_end': clean_date(request.form.get('event_end')),
                    'expiration_date': clean_date(request.form.get('expiration_date')),
                    'category': request.form['category'],
                    'project_id': request.form['at_category'] if request.form['category'] == 'AT' else request.form.get('project_id'),
                    'recurring_weekly': 1 if request.form.get('recurring_weekly') == 'true' else 0,
                    'recurring_monthly': request.form.get('recurring_monthly') or None,
                    'link': request.form.get('link') or None,
                    'just_show_up': 1 if request.form.get('just_show_up') == 'true' else 0,
                }
            )
    except Exception as e:
        return { 'error': str(e) }, 400

    return { 'success': True }


@bp.route('/api/opportunities/<int:id>')
def opportunity_object(id):
    opp = get_opportunity(id)
    return {
        'id': opp[0],
        'owner': opp[1],
        'title': opp[2],
        'body': opp[3],
        'anywhere': opp[4] == 1,
        'anytime': opp[5] == 1,
        'location': opp[6],
        'city': opp[7],
        'event_start': convert_to_readable_local(opp[8]),
        'event_end': convert_to_readable_local(opp[9]),
        'expiration_date': convert_to_readable_local(opp[10]),
        'category': opp[11],
        'project_id': opp[12],
        'recurring_weekly': opp[13] == 1,
        'recurring_monthly': opp[14],
        'link': opp[15],
        'just_show_up': opp[16] == 1
    }


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def index(path):
    '''Serves the single page app.'''
    return render_template('opportunities/index.html')
