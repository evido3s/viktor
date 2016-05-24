#!/usr/bin/env python
# encoding: utf-8


from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from ..models import User
from wtforms import ValidationError


class LoginForm(Form):
    username = StringField(validators=[Required(), Length(1, 64)])
    password = PasswordField(validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class AddUserForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                               Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64)])
    realname = StringField(u'姓名', validators=[Length(0, 64)])
    mobile = StringField(u'电话', validators=[Regexp('^[0-9]*$'), Length(0, 15)])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入密码不一致.')])
    password2 = PasswordField(u'再次确认', validators=[Required()])
    submit = SubmitField(u'添加')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已存在.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在.')


class EditProfileAdminForm(Form):
    '''admin profile edit form'''
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                               Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64)])
    realname = StringField(u'全名', validators=[Length(0, 64)])
    mobile = StringField(u'电话', validators=[Length(0, 11)])
    pub_key = TextAreaField(u'公钥', validators=[Length(0, 5000)])
    pri_key= TextAreaField(u'私钥', validators=[Length(0, 5000)])
    password = PasswordField(u'密码', validators=[Length(0, 128)])
    submit = SubmitField(u'更新')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exist.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist.')

    def validate_name(self, field):
        if field.data != self.user.name and \
                User.query.filter_by(name=field.data).first():
            raise ValidationError('name already exist.')


class ChangepasswordForm(Form):
    '''change password form'''
    oldpassword = PasswordField(u'旧密码', validators=[Required()])
    newpassword = PasswordField(u'新密码', validators=[Required(),
                                                          EqualTo('newpassword2',
                                                          message=u'两次输入密码不一致.')])
    newpassword2 = PasswordField(u'再次确认', validators=[Required()])
    submit = SubmitField(u'更新')
