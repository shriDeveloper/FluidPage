from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from slugify import slugify
from .models import Product,Subscriber,Maker

def homepage(request):
    list = []
    email = ''
    if request.method == 'POST':
        email = request.POST.get('product_maker')
        if Maker.objects.filter(email = email).count() > 0:
            return render(request,'HomePage/HomePage.html',{'ERROR':"Email Already exists!"})
        list = [{'theme_id':'1','theme':'ThemeOne.gif'},{'theme_id':'2','theme':'ThemeTwo.gif'},{'theme_id':'3','theme':'ThemeThree.gif'}]
    return render(request,'HomePage/HomePage.html',{'themes':list,'email':email})
@xframe_options_exempt
def build(request,build):
    product_name=''
    product_maker=''
    product_summary=''
    rendered = render_to_string('Theme/'+build+'.html',{'NAME':'SSPACE','SUMMARY':'THIS IS THE BEST PRODUCT','MAKER':'shriniketDeshmukh','THEME_ID':build})
    if request.method == "POST":
        #load the template here db on build id
        product_name = request.POST.get('product_name')
        product_summary = request.POST.get('product_summary')
        product_maker = request.POST.get('product_maker')
        rendered = render_to_string('Theme/'+build+'.html',{'NAME':product_name,'SUMMARY':product_summary,'MAKER':product_maker,'THEME_ID':build})
        return render(request,'Dashboard/Dashboard.html',{'SAVE_STATUS':True,'HTML':rendered , 'NAME':product_name,'SUMMARY':product_summary,'MAKER':product_maker,'THEME_ID':build})
    return render(request,'Dashboard/Dashboard.html',{'HTML':rendered , 'NAME':product_name,'SUMMARY':product_summary,'MAKER':product_maker,'THEME_ID':build})

@xframe_options_exempt
def template(request,launch_id):
    try:
        page = Product.objects.get(slug = launch_id)
    except:
        return render(request,'Theme/Theme.html',{'ERROR':'Product Page Does Not Exist !'})
    if request.method == 'POST':
        #add new subsriber
        new_subsriber = request.POST.get('subscriber')
        subscriber = Subscriber(email = new_subsriber , product = launch_id)
        subscriber.save() 
        #ends here
        rendered = render_to_string('Theme/'+page.theme+'.html',{'NAME':page.name,'SUMMARY':page.summary,'MAKER':page.maker,'SUBSCRIBED':'Thanks a lot for subscribing !'},request=request)
        return render(request,'Theme/Theme.html',{'HTML':rendered })
    else:
        rendered = render_to_string('Theme/'+page.theme+'.html',{'NAME':page.name,'SUMMARY':page.summary,'MAKER':page.maker},request=request)
    return render(request,'Theme/Theme.html',{'HTML':rendered })

def publish(request):
    product_name = request.POST.get('NAME')
    product_slug = slugify(product_name)
    product_summary = request.POST.get('SUMMARY')
    product_maker = request.POST.get('MAKER')
    product_theme = request.POST.get('THEME')
    product_email = request.POST.get('EMAIL')


    try:
        product = Product.objects.get(name = product_name)
        product.maker = product_maker
        product.summary = product_summary
        product.slug = product_slug
        product.theme = product_theme
        
    except Product.DoesNotExist:
        product = Product(name=product_name,maker=product_maker,summary= product_summary, slug = product_slug , theme = product_theme )
    product.save()

    #add maker here
    maker = Maker(email = product_email , product = product_slug )
    maker.save()
    #add the entry here
    print(product_name)
    return JsonResponse({'launch_name':product_slug},safe=False)
def dashboard(request,launch_id):
    if request.method == 'POST':
        email = request.POST.get('u_mail')
        page = Maker.objects.get(product = launch_id)
        subscribers = Subscriber.objects.filter(product = launch_id)
        if email == page.email:
            return render(request,'Admin/Admin.html',{'VERIFIED':True,'SUBSCRIBERS':subscribers})
        else:
            print("UN Verified EMail: "+page.email)
    return render(request,'Admin/Admin.html')