#!/usr/bin/env python
# encoding: utf-8


from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, SubmitField, ValidationError, TextAreaField, SelectField
from wtforms.validators import Required, Length, Regexp, IPAddress, NumberRange, Optional
from ..models import IDC, Groups, Hosts


class EditProfileForm(Form):
    '''profile edit form'''
    realname = StringField(u'名字', validators=[Length(0, 64)])
    mobile = StringField(u'电话', validators=[Regexp('^[0-9]*$'), Length(0, 15)])
    pub_key = TextAreaField(u'公钥', validators=[Length(0, 1000)])
    pri_key= TextAreaField(u'私钥', validators=[Length(0, 2000)])
    submit = SubmitField(u'更新')


class AddIdcForm(Form):
    '''add bgp form'''
    name = StringField(u'数据中心', validators=[Required(), Length(1, 64)])
    remark = TextAreaField(u'备注', validators=[Length(0, 500)])
    submit = SubmitField(u'添加')

    def validate_name(self, field):
        if IDC.query.filter_by(name=field.data).first():
            raise ValidationError(u'机房已存在.')


class EditIdcForm(Form):
    '''idc list edit form'''
    name = StringField(u'机房', validators=[Length(0, 64)])
    remark = TextAreaField(u'备注', validators=[Length(0, 500)])
    submit = SubmitField(u'更新')

    def __init__(self, idc, *args, **kwargs):
        super(EditIdcForm, self).__init__(*args, **kwargs)
        self.idc = idc

    def validate_name(self, field):
        if field.data != self.idc.name and \
                IDC.query.filter_by(name=field.data).first():
            raise ValidationError('IDC already exist')


class AddGropuForm(Form):
    '''Business groups edit form'''
    name = StringField(u'项目组名', validators=[Required(), Length(1, 64)])
    remark = TextAreaField(u'备注', validators=[Length(0, 500)])
    submit = SubmitField(u'添加')

    def validate_name(self, field):
        if Groups.query.filter_by(name=field.data).first():
            raise ValidationError('Group already exist or input no name.')


class EditGropuForm(Form):
    '''Business groups edit form'''
    name = StringField(u'项目组名', validators=[Length(0, 64)])
    remark = TextAreaField(u'备注', validators=[Length(0,500)])
    submit = SubmitField(u'更新')

    def __init__(self, group, *args, **kwargs):
        super(EditGropuForm, self).__init__(*args, **kwargs)
        self.group = group

    def validate_name(self, field):
        if field.data != self.group.name and \
                Groups.query.filter_by(name=field.data).first():
            raise ValidationError('Group already exist.')


class AddHostForm(Form):
    '''edit host form for admin'''
    hostname = StringField(u'主机名', validators=[Required(), Length(1, 64)])
    ip = StringField(u'IP', validators=[Required(), Length(0, 64), IPAddress()])
    eip = StringField(u'公网IP', validators=[Length(0, 64), IPAddress(), Optional()])
    system = StringField(u'系统', validators=[Required(), Length(1, 64)])
    cpu = IntegerField(u'CPU', validators=[Required(), NumberRange(min=1, max=50)])
    mem = IntegerField(u'内存', validators=[Required(), NumberRange(min=1, max=100)])
    disk = IntegerField(u'磁盘', validators=[NumberRange(min=0, max=5000)])
    groups = SelectField(u'所属项目组', coerce=int)
    idc = SelectField(u'所属机房', coerce=int)
    submit = SubmitField(u'添加')

    def __init__(self, *args, **kwargs):
        super(AddHostForm, self).__init__(*args, **kwargs)
        self.groups.choices = [(groups.id, groups.name)
                               for groups in Groups.query.order_by(Groups.name).all()]
        self.idc.choices = [(idc.id, idc.name)
                            for idc in IDC.query.order_by(IDC.name).all()]

    def validate_ip(self, field):
        if Hosts.query.filter_by(ip=field.data).first():
            raise ValidationError('IP already exist.')


class EditHostForm(Form):
    '''admin edit host information'''
    hostname = StringField(u'主机名', validators=[Required(), Length(1, 64)])
    ip = StringField(u'IP', validators=[Required(), Length(0, 64), IPAddress()])
    eip = StringField(u'公网IP', validators=[Length(0, 64), IPAddress(), Optional()])
    system = StringField(u'系统', validators=[Required(), Length(1, 64)])
    cpu = IntegerField(u'CPU', validators=[Required(), NumberRange(min=1, max=50)])
    mem = IntegerField(u'内存', validators=[Required(), NumberRange(min=1, max=100)])
    disk = IntegerField(u'磁盘', validators=[NumberRange(min=0, max=5000)])
    groups = SelectField(u'所属项目组', coerce=int)
    idc = SelectField(u'所属机房', coerce=int)
    submit = SubmitField(u'更新')

    def __init__(self, host, *args, **kwargs):
        super(EditHostForm, self).__init__(*args, **kwargs)
        self.groups.choices = [(groups.id, groups.name)
                               for groups in Groups.query.order_by(Groups.name).all()]
        self.idc.choices = [(idc.id, idc.name)
                            for idc in IDC.query.order_by(IDC.name).all()]
        self.host = host

    def validate_ip(self, field):
        if field.data != self.host.ip and \
                Hosts.query.filter_by(ip=field.data).first():
            raise ValidationError('IP already exist.')

    def validate_eip(self, field):
        if field.data != self.host.eip and \
                Hosts.query.filter_by(eip=field.data).first():
            raise ValidationError('IP already bind to host.')

