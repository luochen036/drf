from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# 抽象类
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        abstract = True


# 用户表
class UserInfo(BaseModel):
    class Meta:
        db_table = "user-info"  # 数据库表名
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    # 用户名
    username = models.CharField(max_length=32, verbose_name="用户名")
    # 密码
    password = models.CharField(max_length=32, verbose_name="密码")
    # 手机号
    phone = models.CharField(max_length=11, verbose_name="手机号",null=True,blank=True)
    # token
    token = models.CharField(max_length=256, verbose_name="token")
    # token 过期时间
    token_expire = models.DateTimeField(null=True, blank=True, verbose_name="token 过期时间")
    # 状态
    status_choices = [
        (1, "正常"),
        (0, "禁用"),
    ]
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")


# 话题表
class Topic(BaseModel):
    class Meta:
        db_table = "topic"  # 数据库表名
        verbose_name = "话题"
        verbose_name_plural = verbose_name

    # 话题名称
    name = models.CharField(max_length=32, verbose_name="话题名称")
    # 是否热门
    is_hot = models.BooleanField(default=False, verbose_name="是否热门")

    # 一个用户可以创建多个话题
    # 外键关联用户表
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户")


# 咨询表
class News(BaseModel):
    class Meta:
        db_table = "news"  # 数据库表名
        verbose_name = "咨询"
        verbose_name_plural = verbose_name

    # 咨询标题
    title = models.CharField(max_length=32, verbose_name="咨询标题")
    # 咨询图片
    image = models.TextField(null=True, blank=True, verbose_name="咨询图片")
    # 咨询链接
    url = models.CharField(max_length=256, null=True, blank=True, verbose_name="咨询链接")
    # 审核状态
    status_choices = [
        (0, "待审核"),
        (1, "审核通过"),
        (2, "审核拒绝"),
    ]
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="咨询状态")

    # 一个话题对应多个咨询
    # 外键关联话题表
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, verbose_name="话题")
    # 一个用户可以创建多个咨询
    # 外键关联用户表
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户")

    # 收藏数
    collect_count = models.IntegerField(default=0, verbose_name="收藏数")
    # 评论数
    comment_count = models.IntegerField(default=0, verbose_name="评论数")
    # 推荐数
    recommend_count = models.IntegerField(default=0, verbose_name="推荐数")

# 推荐表
class Recommend(models.Model):
    class Meta:
        db_table = "recommend"  # 数据库表名
        verbose_name = "推荐"
        verbose_name_plural = verbose_name

    # 推荐咨询
    news = models.ForeignKey(to=News, on_delete=models.CASCADE, verbose_name="咨询")
    # 推荐用户
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户")
    # 推荐时间
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="推荐时间")

# 收藏表
class Collect(models.Model):
    class Meta:
        db_table = "collect"  # 数据库表名
        verbose_name = "收藏"
        verbose_name_plural = verbose_name

    # 收藏咨询
    news = models.ForeignKey(to=News, on_delete=models.CASCADE, verbose_name="咨询")
    # 收藏用户
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户")
    # 收藏时间
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="收藏时间")

# 评论表
class Comment(models.Model):
    class Meta:
        db_table = "comment"  # 数据库表名
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    # 评论咨询
    news = models.ForeignKey(to=News, on_delete=models.CASCADE, verbose_name="咨询")
    # 评论用户
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户")
    # 评论内容
    content = models.TextField(verbose_name="评论内容")
    # 评论时间
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="评论时间")
    # 评论回复
    #根评论
    root_comment = models.ForeignKey(related_name="roots", to="self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="根评论")
    # 父评论
    parent_comment = models.ForeignKey(related_name="parents", to="self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父评论")
    # 评论深度
    depth = models.IntegerField(default=0, verbose_name="评论深度")
    # 最后评论时间
    last_comment_time = models.DateTimeField(null=True, blank=True, verbose_name="最后评论时间")
