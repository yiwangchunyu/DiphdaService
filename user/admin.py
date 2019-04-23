from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'openid', 'username', 'avatar', 'tags','status','ctime','mtime')

    #搜索字段
    search_fields = ('id', 'openid', 'username','tags', 'ctime')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('id',)

    # list_editable 设置默认可编辑字段
    list_editable = ['username']

    # 设置哪些字段可以点击进入编辑界面
    # list_display_links = ('id', 'caption')

    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)


# 页面标题
admin.site.site_title="Diphda"
# 登录页导航条和首页导航条标题
admin.site.site_header="Diphda Administration"
# 主页标题
admin.site.index_title="Welcome, you can manage the backstage now!"