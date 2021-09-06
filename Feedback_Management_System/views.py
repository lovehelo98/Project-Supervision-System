from django.shortcuts import render,redirect
from . models import *
from User_Management_System.models import Account
from .forms import descriptionform
from django.http import JsonResponse



# Create your views here.
def grid(request):
    g = markingGrids.objects.all().order_by('id')
    return render(request, 'FMS/grid.html',{'grids':g})


def criteria(request, id):
    g = markingGrids.objects.get(id=id)
    c = g.assessmentcriterias_set.all().order_by('id')
    return render(request, 'FMS/criteria.html', {'criterias':c, 'g':g})


def description(request, id):
    criteria = assessmentCriterias.objects.get(id=id)
    g = criteria.title
    d = criteria.descriptions_set.all().order_by('id') 
    form = descriptionform()
    return render(request, 'FMS/descriptions.html', {'form':form,'descriptions':d,  'g':g, 'c':criteria})


def updategrid(request, id):
    g = markingGrids.objects.get(id=id)
    if request.method == 'POST':
        g.title = request.POST.get('title')
        g.save()
        return redirect('grid') 


def deletegrid(request, id):
    g = markingGrids.objects.get(id=id)
    g.delete()
    return redirect('grid') 


def addgrid(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        g = markingGrids(title=title)
        g.save()
        return redirect('grid') 


def updatecriteria(request, id):
    c = assessmentCriterias.objects.get(id=id)
    if request.method == 'POST':
        c.criteria = request.POST.get('title')
        gid = c.title.id
        c.save()
        return criteria(request,gid)


def deletecriteria(request, id):
    c = assessmentCriterias.objects.get(id=id)
    gid = c.title.id
    c.delete()
    return criteria(request,gid)
    

def addcriteria(request, id):
    g = markingGrids.objects.get(id=id)
    if request.method == 'POST':
        addcriteria = request.POST.get('title')
        c = assessmentCriterias(title=g, criteria=addcriteria)
        c.save()
        return criteria(request,g.id)

     
def deletedescription(request,id):
    d = descriptions.objects.get(id=id)
    cid = d.criteria.id
    d.delete()
    return description(request,cid)

def editdescription(request,id,cid):
    descp = descriptions.objects.get(id=id)
    form = descriptionform(instance=descp) 
    if request.method == "POST":
        form = descriptionform(request.POST, instance=descp)  
        if form.is_valid():  
            try:  
                 
                form.save()
                model = form.instance
                return description(request,descp.criteria.id) 
            except Exception as e: 
                pass    
    return render(request,'FMS/editdescription.html',{'form':form, 'cid':cid})  

def adddescription(request,id):
    criteria = assessmentCriterias.objects.get(id=id)
    # grid = markingGrids.objects.get(id=gid)
    form = descriptionform(request.POST)
    if request.method == "POST":
      if form.is_valid():
          post = form.save(commit=False)
          post.criteria = criteria
          post.save()
    return description(request,id)

def studentmarkinggrid(request,id):
    i = Account.objects.get(id=id)
    g = markingGrids.objects.all().order_by('id')
    c = assessmentCriterias.objects.all().order_by('id')
    d = descriptions.objects.all().order_by('id')
    cmt = comments.objects.all()
    m = marks.objects.all()
    return render(request, 'FMS/usermarkinggrid.html',{'i':i,'g':g,'c':c,'d':d, 'cmt':cmt,'m':m})

def addcomment(request):
    if request.method == "POST":
        cmtid = request.POST.get("cmntid")
        std_id = request.POST.get("student")
        teacher_id = request.POST.get("teacher")
        descp_id = request.POST.get("description")
        comment = request.POST.get("comment")
        student = Account.objects.get(id=std_id)
        teacher = Account.objects.get(id=teacher_id)
        description = descriptions.objects.get(id=descp_id)
        if cmtid != '':        
            cmt , add = comments.objects.get_or_create(student=student,description=description,teacher=teacher, id=cmtid)
            cmt.comment = comment
            cmt.save()
            comet = comments.objects.get(comment=comment, description=description )
            print(comet.id)
            comet_data = [{'id':comet.id,'comment':comet.comment, "descpid":descp_id , "stdid":std_id}]
            return JsonResponse({'status':'edited', 'comet':comet_data})
        else :
            cmt = comments(student=student,description=description,teacher=teacher, comment=comment)
            cmt.save()
            comet = comments.objects.get(comment=comment, description=description )
            print(comet.id)
            comet_data = [{'id':comet.id,'comment':comet.comment, "descpid":descp_id , "stdid":std_id}]
            return JsonResponse({'status':'save', 'comet':comet_data})
    else:
        return JsonResponse({'status':0})    


def addmarks(request):
    if request.method == "POST":
        field = request.POST.get("field")
        if field == 'criteria':
            std_id = request.POST.get("std")
            crt_id = request.POST.get("id")
            m = request.POST.get("mrk")
            student = Account.objects.get(id=std_id)
            criteria = assessmentCriterias.objects.get(id=crt_id)
            mark , add = marks.objects.get_or_create(student=student, criteria=criteria)
            mark.marks = m
            mark.save()
            comet = marks.objects.get(student=student, criteria=criteria)
            comet_data = [{'id':comet.id,'criteria':comet.criteria.criteria, "marks":comet.marks}]
            return JsonResponse({'status':'0', 'comet':comet_data})
        else :
            std_id = request.POST.get("std")
            grid_id = request.POST.get("id")
            m = request.POST.get("mrk")
            student = Account.objects.get(id=std_id)
            grid = markingGrids.objects.get(id=grid_id)
            mark , add = marks.objects.get_or_create(student=student, grid=grid)
            mark.marks = m
            mark.save()
            comet = marks.objects.get(student=student, grid=grid)
            comet_data = [{'id':comet.id,'grid':comet.grid.title, "marks":comet.marks}]
            return JsonResponse({'status':'0', 'comet':comet_data})


def cmtdel(request):
    if request.method == "POST":
        cid = request.POST.get("id")
        cmnt = comments.objects.get(id=cid)
        cmnt.delete()
        return JsonResponse({"status":0})






