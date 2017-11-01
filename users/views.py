from django.shortcuts import render,redirect,render_to_response
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from random import choice
import string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .permissions import check_permission
from .forms import RegisterForm,UserListForm
from .models import User,BeautyUsers


def index(request):
    return render(request,'index.html')


def register(request):
    redirect_to = request.POST.get('next',request.GET.get('next',''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form':form,'next':redirect_to})


def sendemail(request):
    emailaddress = request.POST['email']
    if User.objects.filter(email=emailaddress):
        for i in User.objects.filter(email=emailaddress):
            nametemp = i.username
            idtemp = i.id

            def GenPassword(length=8,chars=string.ascii_letters+string.digits):
                return ''.join([choice(chars) for i in range(length)])
            pawdtemp = GenPassword(8)
            User.objects.filter(email=emailaddress).delete()
            User.objects.create_user(id=idtemp, username=nametemp, password=pawdtemp, email=emailaddress)
            send_mail(
                subject=u"这是新的密码,请使用新的密码登录", message=pawdtemp,
                from_email='luyufeng@163.com', recipient_list=[emailaddress, ], fail_silently=False,
            )
            return HttpResponse("新的密码已经发到您的邮箱,请去您的邮箱查收并使用新的密码登录,有问题请联系站长")
    else:
        return HttpResponse("您的邮箱的账户注册信息没有找到")


def add_user(request):
    if request.method == 'POST':
        user = request.user
        print(user)
        user_id = request.POST['user_id']
        print(user_id)
        nickname = request.POST['nickname']
        try:
            BeautyUsers.objects.create(user_id=user_id, nickname=nickname,add_people=user)
        except Exception as e:
            return HttpResponse("数据重复或者数据格式不正确，具体原因：" + str(e))
    user_list = BeautyUsers.objects.all()
    return render(request, 'query/api/add_user_test.html', context={'user_list': user_list})


def userlist(request):
        user_list = BeautyUsers.objects.all()
        paginator = Paginator(user_list, 2, 2)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        return render(request, 'query/userlist.html', {"user_list": customer})


# @check_permission
def userInfo(request,user_id):
    user_obj = BeautyUsers.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserListForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return HttpResponse('保存成功！')
        else:
            print
            form.errors
    else:
        form = UserListForm(instance=user_obj)
    return render(request, 'query/userinfo.html', {'user_info': form})

# @login_required(login_url='/kucun/login')
# def add_goods(request):
#     if request.method == 'POST':
#         uf = UserListForm(request.POST)
#         if uf.is_valid():
#             user = request.user
#             user_id = uf.cleaned_data['user_id']
#             nickname = uf.cleaned_data['nickname']
#
#             adduser = BeautyUsers()
#             adduser.add_people = user
#             adduser.user_id = user_id
#             adduser.nickname = nickname
#             adduser.save()
#             return HttpResponseRedirect(reverse('addsuccess'))
#     else:
#         uf = UserListForm()
#     return render_to_response('query/api/add_user.html',{'uf':uf})


# def order_manage(request):
#     orders = Order.objects.all().filter(is_delete=False).order_by('-date')[:100]
#     return render_to_response('order_manage.html',
#                               {'request': request, 'orders': orders, 'header': '订单管理', 'title': '订单管理'})
#
#
# def api_change_arrears(request):
#     user = request.user
#     today = datetime.date.today()
#     if request.method == 'POST':
#         sell_record_id = request.POST['sell_record_id']
#         record = GoodsSellRecord.objects.get(id=sell_record_id)  # sell_record已经被之前的一个函数使用了
#         record.is_arrears = not record.is_arrears
#         record.save()
#         if record.is_arrears:
#             arrears = '是'
#             refund_records = RefundRecord.objects.filter(sell_record=record, date__year=today.year,
#                                                          date__month=today.month,
#                                                          date__day=today.day)
#             if refund_records:
#                 for record in refund_records:
#                     record.delete()
#         else:
#             arrears = '否'
#             refund_record = RefundRecord(sell_record=record, updater=user)
#             refund_record.save()
#         return HttpResponse(arrears)