# -*- coding: utf-8 -*-

import os
import json
import gazu
from logger import Logger


class LogIn(object):

    def __init__(self):
        self._host = None
        self._user = None
        self._user_id = None
        self._user_pw = None
        self._valid_host = False
        self._valid_user = False
        self._auto_login_setting = False

        self.logging = Logger()
        self.dir_path = os.path.dirname(os.path.abspath(__file__)) + '/.config'
        self.user_path = os.path.join(self.dir_path, 'user.json')
        self.logging.set_logger()

    @property
    def host(self):
        """
        현재 호스트의 URL을 반환하는 속성입니다.
        """
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def user(self):
        """
        현재 로그인한 사용자의 사용자 사전을 반환합니다.
        """
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def user_id(self):
        """
        현재 로그인한 사용자의 id를 반환합니다.
        """
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def user_pw(self):
        """
        현재 로그인한 사용자의 password를 반환합니다.
        """
        return self._user_pw

    @user_pw.setter
    def user_pw(self, value):
        self._user_pw = value

    @property
    def valid_host(self):
        """
        현재 호스트 연결의 유효성을 반환하는 속성입니다.
        """
        return self._valid_host

    @valid_host.setter
    def valid_host(self, value):
        self._valid_host = value

    @property
    def valid_user(self):
        """
        현재 사용자 로그인의 유효성을 반환하는 속성입니다.
        """
        return self._valid_user

    @valid_user.setter
    def valid_user(self, value):
        self._valid_user = value

    @property
    def auto_login_setting(self):
        """
        현재 로그인한 사용자가 자동 로그인을 선택하였는지의 여부를 반환합니다.
        """
        return self._auto_login_setting

    @auto_login_setting.setter
    def auto_login_setting(self, value):
        self._auto_login_setting = value

    def connect_host(self):
    # connect_host
        try:
            gazu.client.set_host(self.host)
            self.valid_host = True
            self.logging.connect_log(self.host)

    # connect_host fail
        except gazu.AuthFailedException:
            self.logging.failed_log()
            self.errormassage = '호스트 URL이 잘못되었습니다.'
            print(self.errormassage)


    def log_in(self):
    # log_in
        try:
            log_in = gazu.log_in(self.user_id, self.user_pw)
            self.user = log_in['user']
            self.valid_user = True
            self.save_login_info()
            self.logging.enter_log(self.user["full_name"])
            return True

        # log_in fail
        except gazu.AuthFailedException:
            self.logging.failed_log()
        # email_error
            if "@" in self.user_id and "." in self.user_id:
                self.errormassage = '사용자 ID 또는 암호가 잘못 입력되었습니다.'
                print(self.errormassage)
        # other_error
            else:
                self.errormassage = '이메일 형식이 잘못되었습니다.'
                print(self.errormassage)

    def log_out(self):

        self.user = None
        self.reset_login_info()
        self.logging.logout_log()
        print("로그아웃 성공")

        return True

    def access_setting(self):

        if not os.path.exists(self.dir_path):
            try:
                os.makedirs(self.dir_path)
            except OSError:
                raise ValueError("에러 메시지 : 디렉터리를 만들지 못했습니다.")

        if not os.path.exists(self.user_path):
            try:
                self.reset_login_info()
            except OSError:
                raise ValueError("에러 메시지 : user.json 파일을 생성하지 못했습니다.")

        return True

    def load_login_info(self):

        user_dict = {}
        if os.path.exists(self.user_path):
            with open(self.user_path, 'r') as json_file:
                user_dict = json.load(json_file)
        else:
            self.access_setting()
            with open(self.user_path, 'r') as json_file:
                user_dict = json.load(json_file)

        return user_dict

    def save_login_info(self):

        user_dict = {
            'host': self.host,
            'user_id': self.user_id,
            'user_pw': self.user_pw,
            'valid_host': self.valid_host,
            'valid_user': self.valid_user,
            'auto_login': self.auto_login_setting
        }
        with open(self.user_path, 'w') as json_file:
            json.dump(user_dict, json_file)

        return user_dict

    def reset_login_info(self):
        """
        인증 설정을 기본값으로 재설정합니다.
        """
        self.host = ''
        self.user_id = ''
        self.user_pw = ''
        self.valid_host = False
        self.valid_user = False
        self.auto_login_setting = False
        self.save_login_info()

