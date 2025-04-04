from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request,'index.html')





def gen_pdf(request):
    if request.method == 'POST':
        coke=request.POST['coke']
        pepsi=request.POST['pepsi']
        fanta=request.POST['fanta']
        sprite=request.POST['sprite']
        dt=request.POST['dt']
        coke_rt=30
        pepsi_rt=40
        fanta_rt=43
        sprite_rt=45
        total=(int(coke)*coke_rt + int(pepsi)*pepsi_rt + int(fanta)*fanta_rt + int(sprite)*sprite_rt )
        return render(request,'pdf.html',{'coke':coke,'pepsi':pepsi,'fanta':'fanta','sprite':sprite,'dt':dt,'total':total})
    return render(request,'index.html')