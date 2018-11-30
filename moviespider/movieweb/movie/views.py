from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from django.core.cache import cache
from django.core.mail import send_mail
from django.template import loader
from .models import Movie, User, Comment, Advertise

# Create your views here.
# 首页
def index(request):
    # return HttpResponse('hi')
    # return render(request, 'base.html')
    username = request.session.get('username')

    # 导航显示的视频封面图片
    carousel_list = Movie.objects.filter(is_carousel=True)
    # 推荐页面显示的视频小图（10个）
    recommend_list = Movie.objects.order_by('-mark')[:10]
    for r in recommend_list:
        r.like_count = len(r.like.all())  # 视频被收藏的总数
        # print(r.like_count)

    return render(request, 'index.html', {
                                          'recommend_list':recommend_list,
                                          'username':username,
                                        })


# 收藏/取消收藏
def like(request):
    state = request.GET.get('state')  # 收藏状态
    movie_id = request.GET.get('movie_id')  # 视频id

    username = request.session.get('username')
    currentuser = User.objects.get(username=username)  # 当前登陆的用户

    like_movie = Movie.objects.get(id=movie_id)  # 获取视频对象
    # print(like_movie.like.all())  # 该视频对应的所有收藏用户

    if state == '1':  # 取消
        like_movie.like.remove(currentuser)
    elif state == '0':  # 收藏
        like_movie.like.add(currentuser)

    return JsonResponse({'data':'success'})


def like(request):
    state = request.GET.get('state')
    movie_id = request.GET.get('movie_id')
    username = request.session.get('username')
    currentuser = User.objects.get(username=username)  # 当前登陆的用户

    like_movie = Movie.objects.get(id=movie_id)  # 获取视频对象
    # print(like_movie.like.all())  # 该视频对应的所有收藏用户

    if state == '1':  # 取消
        like_movie.like.remove(currentuser)
    elif state == '0':  # 收藏
        like_movie.like.add(currentuser)

    return JsonResponse({'data': 'success'})

# 详情页
def single(request, mid):

    username = request.session.get('username')

    single_movie = Movie.objects.get(id=mid)

    try:
        currentuser = User.objects.get(username=username)
    except User.DoesNotExist as e:
        currentuser = None

    # print(single_movie.like.all())  # 返回当前电影对应的收藏用户名称
    if currentuser != None:  # 当前用户已登陆
        if currentuser in single_movie.like.all():  # 当前登陆用户已经收藏了本电影
            is_like = 1
        else:  # 当前用户没有收藏此电影
            is_like = 0
    else:
        is_like = 3


    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[ : 3]
    for s in side_recommend:
        s.like_count = len(s.like.all())


    # 获取评论
    try:
        comment_list = Comment.objects.filter(movie_id=mid)
    except Comment.DoesNotExist as e:
        comment_list = []
    comment_list_count = len(comment_list)  # 评论总数

    return render(request, 'single.html', {'movie':single_movie,
                                           'side_recommend':side_recommend,
                                           'username':username,
                                           'is_like':is_like,
                                           'comment_list':comment_list,
                                           'comment_list_count':comment_list_count,
                                           })


# 评论
def comment(request, mid):
    comment_content = request.POST.get('comment')

    username = request.session.get('username')
    currentuser = User.objects.get(username=username)
    m = Movie.objects.get(id=mid)

    Comment.objects.create(comment_content=comment_content, movie_id=m, user_id=currentuser)

    return redirect('/single/' + mid)


# 各类视频展示及搜索页面
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def movie(request, tid):
    username = request.session.get('username')


    if tid == '2':  # 最新
        search_list = Movie.objects.order_by('-release_time')
    elif tid == '4':  # 高分
        search_list = Movie.objects.order_by('-mark')
    elif tid == '5':  # 华语
        search_list = Movie.objects.filter(country_id=3)
    elif tid == '6':  # 欧美
        search_list = Movie.objects.filter(country_id=2)
    elif tid == '7':  # 韩国
        search_list = Movie.objects.filter(country_id=1)
    elif tid == '8':  # 日本
        search_list = Movie.objects.filter(country_id=4)
    elif tid == '9':  # 更多
        search_list = Movie.objects.all()
    elif tid == '0':
        key_word = request.POST.get('keyword')
        search_list = Movie.objects.filter(name__contains=key_word)


    # 重新拼接处理封面图片的url以及出演人员的处理（默认显示3个主角）
    for s in search_list:

        s.like_count = len(s.like.all())  # 视频被收藏的总数


    paginator = Paginator(search_list, 6) # 一页显示 6 条
    page = request.GET.get('page')

        # 获取对应页面
    try:
        results = paginator.page(page)

        # 页面不是整数，返回第一页
    except PageNotAnInteger:
        results = paginator.page(1)

        # 页码越界，返回最后一页
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[: 3]
    for s in side_recommend:
        s.like_count = len(s.like.all())

    # 底部广告栏
    ad_list = Advertise.objects.all()
    import os
    for a in ad_list:
        print(a.pic)


    return render(request, 'movie.html', {'username':username,
                                          'results':results,
                                          'side_recommend':side_recommend,
                                          'ad_list':ad_list,
                                          })


# 登陆页
def login(request):
    # 将上一个页面的地址记录
    # url = request.META.get('HTTP_REFERER', '/   ')
    # print(url)
    # request.session['preUrl'] = url
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        # 查询用户是否存在
        try:
            u = User.objects.get(username=nickname)
        except User.DoesNotExist as e:
            return redirect('/login/')

        # 如果存在,验证密码是否正确
        if password != u.password:
            return redirect('/login/')

        # 登陆成功
        response = HttpResponseRedirect('/index/')

        request.session['username'] = u.username
        response.set_cookie('usernameKey', 'username')

        return response


# 注册页
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
# @csrf_protect
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 如果是ajax请求
        if request.is_ajax():
            # 验证账号是否存在
            nickname = request.POST.get('nickname')

            try:
                user = User.objects.get(username=nickname)
                # 说明账号已被使用
                return JsonResponse({'data':'1'})
            except User.DoesNotExist as e:
                # 判断邮箱是否可用
                email = request.POST.get('email')
                try:
                    email_user = User.objects.get(email=email)
                    # 说明邮箱已被占用
                    return JsonResponse({'data':'2'})
                except User.DoesNotExist as e:
                    # 邮箱可用
                    return JsonResponse({'data':'3'})
                # 说明账号可以使用
                return JsonResponse({'data':'0'})

        # 如果信息验证全部通过,注册用户
        else:
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            subscribe = request.POST.get('subscribe')

            # 用户token
            userToken = make_password(nickname)

            # 创建用户
            user = User.createuser(username=nickname, password=password, email=email, is_subscribe=subscribe, token=userToken)
            user.save()

            # 注册成功需要做状态保持,写入session,默认登陆
            request.session['username'] = nickname
            response = redirect('/index/')
            # response.set_cookie('usernameKey', 'username')
            # response.set_cookie('userToken', userToken)

            # temp = loader.get_template('/active_email.html/')
            #
            # cache.set(userToken, user.id, timeout=10 * 60)
            #
            # temp_content = temp.render(
            #     {"username": nickname, "active_url": "http://127.0.0.1:8000/useractive/?u_token=" + userToken})
            #
            # send_mail("用户激活", "", "rongjiawei1204@163.com", [email, ], html_message=temp_content)

            return response


# def user_active(request):
#     u_token = request.GET.get("u_token")
#     if not u_token:
#         return HttpResponse("激活过期，请重新激活")
#     u_id = cache.get(u_token)
#     user = User.objects.get(pk=u_id)
#     user.is_active = True
#     user.save()
#     cache.delete(u_token)
#     return HttpResponse("用户激活成功")

# 退出页
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/index/')


# 个人中心
def person(request):
    # key = request.COOKIES.get('usernameKey')
    username = request.session.get('username')

    # token = request.COOKIES.get('userToken')
    currentuser = User.objects.get(username=username).id

    results = Movie.objects.filter(like=currentuser)

    for s in results:

        s.like_count = len(s.like.all())  # 视频被收藏的总数

    paginator = Paginator(results, 6)  # 一页显示 6 条
    page = request.GET.get('page')

    # 获取对应页面
    try:
        results = paginator.page(page)

        # 页面不是整数，返回第一页
    except PageNotAnInteger:
        results = paginator.page(1)

        # 页码越界，返回最后一页
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[: 3]
    for s in side_recommend:
        s.like_count = len(s.like.all())

    # 底部广告栏
    ad_list = Advertise.objects.all()
    import os
    for a in ad_list:
        print(a.pic)

    return render(request, 'person.html', {
        'username':username,
        'side_recommend': side_recommend,
        'ad_list': ad_list,
        'results':results,
    })