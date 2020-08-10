from django.db import models


# Create your models here.

class oldperson_info(models.Model):
    id = models.AutoField(primary_key=True)
    ORG_ID = models.IntegerField(null=True, blank=True)
    CLIENT_ID = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=5, blank=True)  # f/m
    phone = models.CharField(max_length=50, blank=True)
    id_card = models.CharField(max_length=50, blank=True)  # 身份证
    birthday = models.DateField(null=True, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_data = models.DateField(null=True, blank=True)
    imgset_dir = models.CharField(max_length=200, blank=True)
    profile_photo = models.CharField(max_length=200, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    firstguardian_name = models.CharField(max_length=50, blank=True)
    firstguardian_relationship = models.CharField(max_length=50, blank=True)
    firstguardian_phone = models.CharField(max_length=50, blank=True)
    firstguardian_wechat = models.CharField(max_length=50, blank=True)
    sceondguardian_name = models.CharField(max_length=50, blank=True)
    secondguardian_relationship = models.CharField(max_length=50, blank=True)
    secondguardian_phone = models.CharField(max_length=50, blank=True)
    secondguardian_wechat = models.CharField(max_length=50, blank=True)
    health_state = models.CharField(max_length=50, blank=True)
    DESCRIPTION = models.CharField(max_length=50, blank=True)
    ISACTIVE = models.CharField(max_length=10, blank=True)
    CREATED = models.DateTimeField(null=True, blank=True)
    CREATEBY = models.CharField(max_length=50, null=True, blank=True)
    UPDATED = models.DateTimeField(null=True, blank=True)
    UPDATEBY = models.CharField(max_length=50, null=True, blank=True)
    REMOVE = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.username


class employee_info(models.Model):
    id = models.AutoField(primary_key=True)
    ORG_ID = models.IntegerField(null=True, blank=True)
    CLIENT_ID = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=5, blank=True)  # f/m
    phone = models.CharField(max_length=50, blank=True)
    id_card = models.CharField(max_length=50, blank=True)  # 身份证
    birthday = models.DateField(null=True, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_data = models.DateField(null=True, blank=True)
    imgset_dir = models.CharField(max_length=200, blank=True)
    profile_photo = models.CharField(max_length=200, blank=True)
    DESCRIPTION = models.CharField(max_length=200, blank=True)
    ISACTIVE = models.CharField(max_length=10, blank=True)
    CREATED = models.DateTimeField(null=True, blank=True)
    CREATEBY = models.CharField(max_length=50, null=True, blank=True)
    UPDATED = models.DateTimeField(null=True, blank=True)
    UPDATEBY = models.CharField(max_length=50, null=True, blank=True)
    REMOVE = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.username


class volunteer_info(models.Model):
    id = models.AutoField(primary_key=True)
    ORG_ID = models.IntegerField(null=True, blank=True)
    CLIENT_ID = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=5, blank=True)  # f/m
    phone = models.CharField(max_length=50, blank=True)
    id_card = models.CharField(max_length=50, blank=True)  # 身份证
    birthday = models.DateField(null=True, blank=True)
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    imgset_dir = models.CharField(max_length=200, blank=True)
    profile_photo = models.CharField(max_length=200, blank=True)
    DESCRIPTION = models.CharField(max_length=200, blank=True)
    ISACTIVE = models.CharField(max_length=10, blank=True)
    CREATED = models.DateTimeField(null=True, blank=True)
    CREATEBY = models.CharField(max_length=50, null=True, blank=True)
    UPDATED = models.DateTimeField(null=True, blank=True)
    UPDATEBY = models.CharField(max_length=50, null=True, blank=True)
    REMOVE = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.username


class event_info(models.Model):
    id = models.AutoField(primary_key=True)
    event_type = models.IntegerField(null=True, blank=True)
    event_date = models.DateField(null=True,auto_now=True)
    event_location = models.CharField(max_length=200, blank=True)
    event_desc = models.CharField(max_length=200, default='')
    oldperson_id = models.ForeignKey(oldperson_info, on_delete=models.CASCADE,related_name='person',null=True,blank=True)
    img_path = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.event_desc

    @property
    def oldperson_id_name(self):
        return self.oldperson_id.username,self.oldperson_id.id


class Account(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=255)


class sys_user(models.Model):
    account = models.ForeignKey(Account, models.DO_NOTHING,primary_key=True)
    ORG_ID = models.IntegerField(null=True, blank=True)
    CLIENT_ID = models.IntegerField(null=True, blank=True)
    REAL_NAME = models.CharField(max_length=50, blank=True)
    SEX = models.CharField(max_length=20, blank=True)
    EMAIL = models.CharField(max_length=50, blank=True)
    PHONE = models.CharField(max_length=50, blank=True)
    MOBILE = models.CharField(max_length=50, blank=True)
    DESCRIPTION = models.CharField(max_length=200, blank=True)
    ISACTIVE = models.CharField(max_length=10, blank=True)
    CREATED = models.DateTimeField(null=True, blank=True)
    CREATEBY = models.CharField(max_length=50, null=True, blank=True)
    UPDATED = models.DateTimeField(null=True, blank=True)
    UPDATEBY = models.CharField(max_length=50, null=True, blank=True)
    REMOVE = models.CharField(max_length=1, blank=True)
    DATAFILTER = models.CharField(max_length=200, blank=True)
    theme = models.CharField(max_length=45, blank=True)
    defaultpage = models.CharField(max_length=45, blank=True)
    logoimage = models.CharField(max_length=45, blank=True)
    qqopenid = models.CharField(max_length=100, blank=True)
    appversion = models.CharField(max_length=10, blank=True)
    jsonauth = models.CharField(max_length=1000, blank=True)

    # def __str__(self):
    #     return self.REAL_NAME


