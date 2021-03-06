from django.contrib import admin

from user.models import User, Tag


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'openid', 'username', 'gender','avatar', 'tags','contact_type','contact','status','ctime','mtime')

    #搜索字段
    search_fields = ('id', 'openid', 'username','tags','contact_type','contact', 'ctime')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('id',)

    # list_editable 设置默认可编辑字段
    list_editable = ['username']

    # 设置哪些字段可以点击进入编辑界面
    # list_display_links = ('id', 'caption')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'name','status','ctime','mtime')

    #搜索字段
    search_fields = ('id', 'name')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('id',)

    # list_editable 设置默认可编辑字段
    list_editable = ['name']

    # 设置哪些字段可以点击进入编辑界面
    # list_display_links = ('id', 'caption')
