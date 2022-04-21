from datetime import timedelta, datetime,timezone
import re
import time
from uuid import uuid4
from flask.sessions import SessionInterface, SessionMixin
from redis import ReadOnlyError, Redis
from pybo.exception import ExceptionError
from werkzeug.datastructures import CallbackDict
from flask import json
import pickle
import os 

SESSION_EXPIRY_MINUTES = 60
SESSION_COOKIE_NAME = "session"

def utctimestamp_by_second(utc_date_time):
    return int((utc_date_time.replace(tzinfo=timezone.utc)).timestamp())


class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(s):
            s.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class RedisSessionInterface(SessionInterface):
    #init connection
    def __init__(self, redis=None):
        print(1)
        self.redis = redis or Redis()

    def open_session(self,request):
        session_key = request.cookies.get(SESSION_COOKIE_NAME)
        if not session_key:
            return self._new_session()

        sid, expiry_timestamp = self._extract_sid_and_expiry_timestamp_from(session_key)
        if not expiry_timestamp:
            return self._new_session()

        redis_value, redis_key_ttl = self._get_redis_value_and_ttl_of(sid)
        if not redis_value:
            return self._new_session()

        if self._expiry_timestamp_not_match(expiry_timestamp, redis_key_ttl):
            return self._new_session()

        data = json.loads(redis_value.decode())
        return RedisSession(data, sid=sid)

    def save_session(self, app, session, response):
        user_id = session.get('user_id')
        response = response()
        def session_is_modified_empty():
            return not session and session.modified

        def session_is_invalid():
            return not user_id

        if session_is_modified_empty() or session_is_invalid():
            self._clean_redis_and_cookie(app, response, session)
            return

        redis_value = json.dumps(dict(session))
        expiry_duration = self._get_expiry_duration(app, session)
        expiry_date = datetime.utcnow() + expiry_duration
        expires_in_seconds = int(expiry_duration.total_seconds())
        session.sid = self._inject_user_id_in_sid(session['sid'], user_id)
        session_key = self._create_session_key(session.sid, expiry_date)
        ssd = {
			'user_id': user_id
		}
        sstr = pickle.dumps(ssd)
        #setex 적용 시 connection error 발생으로 일단 보류
        # self.redis.setex(name=session.sid,time=expires_in_seconds,value=sstr)
        # self._write_wrapper(self.redis.setex, self._redis_key(session.sid), redis_value, expires_in_seconds)
        response.set_cookie(key =SESSION_COOKIE_NAME, value = session_key, expires=expiry_date,
                            httponly=True)
        
    @staticmethod
    def _new_session():
        return RedisSession(sid=uuid4().hex, new=True)

    @staticmethod
    def _get_expiry_duration(app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(minutes=SESSION_EXPIRY_MINUTES)

    @staticmethod
    def _redis_key(sid):
        return 'sid:{}'.format(sid)

    def _write_wrapper(self, write_method, *args):
        print(*args)
        for i in range(2):
            try:
                write_method(*args)
                break
            except ReadOnlyError:
                self.redis.connection_pool.reset()
                time.sleep(1)

    def _get_redis_value_and_ttl_of(self, sid):
        redis_key = self._redis_key(sid)
        pipeline = self.redis.pipeline()
        pipeline.get(redis_key)
        pipeline.ttl(redis_key)
        results = pipeline.execute()

        return tuple(results)

    @staticmethod
    def _expiry_timestamp_not_match(expiry_timestamp, redis_key_ttl):
        datetime_from_ttl = datetime.utcnow() + timedelta(seconds=redis_key_ttl)
        timestamp_from_ttl = utctimestamp_by_second(datetime_from_ttl)

        try:
            return abs(int(expiry_timestamp) - timestamp_from_ttl) > 10
        except (ValueError, TypeError):
            return True

    @staticmethod
    def _extract_sid_and_expiry_timestamp_from(session_key):
        matched = re.match(r"^(.+)\.(\d+)$", session_key)
        if not matched:
            return session_key, None

        return matched.group(1), matched.group(2)

    @staticmethod
    def _create_session_key(sid, expiry_date):
        return "{}.{}".format(sid, utctimestamp_by_second(expiry_date))

    @staticmethod
    def _inject_user_id_in_sid(sid, user_id):
        prefix = "{}.".format(user_id)
        if not sid.startswith(prefix):
            sid = prefix + sid
        return sid

    def _clean_redis_and_cookie(self, app, response, session):
        self._write_wrapper(self.redis.delete, self._redis_key(session.sid))
        response.delete_cookie(SESSION_COOKIE_NAME, domain=self.get_cookie_domain(app))


    @staticmethod
    def _new_session():
        return RedisSession(sid=uuid4().hex, new=True)

def init_app(app):
    redis = Redis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')),
                db=int(os.environ.get('REDIS_DB')))
    app.session_interface = RedisSessionInterface(redis)