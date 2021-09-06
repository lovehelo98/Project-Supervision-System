from django.shortcuts import render
from User_Management_System.models import Account
from Feedback_Management_System.models import * 
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse
from .utils import render_to_pdf , generate_zip


# Create your views here.
def report(request,id,gridtitle):
    a = Account.objects.get(id=id)
    g = markingGrids.objects.get(title=gridtitle)
    c = g.assessmentcriterias_set.all()
    d = descriptions.objects.filter(criteria_id__in=[u.id for u in c]).order_by('criteria_id')
    cmt = comments.objects.filter(description_id__in=[u.id for u in d] , student=a)
    mcrt = marks.objects.filter(student=a ,  criteria_id__in=[u.id for u in c ])
    mgrid = marks.objects.filter(student=a, grid=g)
    return render(request, 'RMS/'+gridtitle+'.html',{'a':a,'d':d,'cmt':cmt,'mgrid':mgrid, 'g':g, 'mcrt':mcrt})

# def downloadpdf(request):
# 	if request.method == 'POST':
# 		id = request.POST.get("id")
# 		id_list = id.split(",")
# 		template_list = ['Project Proposal Criteria','Professionalism Report','Project Marking Grid']
# 		print(id_list)
		
# 		topic = template_list[0]
# 		template_path = 'RMS/'+topic+'.html'
# 		a = Account.objects.get(id=id_list[0])
# 		g = markingGrids.objects.get(title=topic)   #Project Proposal Criteria Professionalism Report
# 		c = g.assessmentcriterias_set.all()
# 		d = descriptions.objects.filter(criteria_id__in=[u.id for u in c]).order_by('criteria_id')
# 		cmt = comments.objects.filter(description_id__in=[u.id for u in d] , student=a)
# 		mcrt = marks.objects.filter(student=a ,  criteria_id__in=[u.id for u in c ])
# 		mgrid = marks.objects.filter(student=a, grid=g)
# 		context = {'a':a,'d':d,'cmt':cmt,'mgrid':mgrid, 'g':g, 'mcrt':mcrt}
# 		# Create a Django response object, and specify content_type as pdf
# 		response = HttpResponse(content_type='application/pdf')
# 		response['Content-Disposition'] = 'filename='+a.fullname+"_"+g.title+".pdf"  #attachment; 
# 		# find the template and render it.
# 		template = get_template(template_path)
# 		html = template.render(context)

# 		# create a pdf
# 		pisa_status = pisa.CreatePDF(
# 		html, dest=response)

		
# 		# if error then show some funy view
# 		if pisa_status.err:
# 			return HttpResponse('We had some errors <pre>' + html + '</pre>')
# 		return response

def downloadpdf(request):
	if request.method == 'POST':
		id = request.POST.get("id")
		id_list = id.split(",")
		template_list = ['Project Proposal Criteria','Professionalism Report','Project Marking Grid']
		print(id_list)
		zip_files = []
		files = []
		for x in id_list[:-1]:
			for i in template_list:
				topic = i
				template_path = 'RMS/'+topic+'.html'
				a = Account.objects.get(id=x)
				g = markingGrids.objects.get(title=topic)   #Project Proposal Criteria Professionalism Report
				c = g.assessmentcriterias_set.all()
				d = descriptions.objects.filter(criteria_id__in=[u.id for u in c]).order_by('criteria_id')
				cmt = comments.objects.filter(description_id__in=[u.id for u in d] , student=a)
				mcrt = marks.objects.filter(student=a ,  criteria_id__in=[u.id for u in c ])
				mgrid = marks.objects.filter(student=a, grid=g)
				context = {'a':a,'d':d,'cmt':cmt,'mgrid':mgrid, 'g':g, 'mcrt':mcrt}	
				pdf = render_to_pdf(template_path, context)
				files.append ((a.fullname+"_"+g.title+".pdf", pdf))
			full_zip = generate_zip(files)
			zip_files.append((a.fullname+".zip",full_zip))
			files = []
		full_zip_in_memory = generate_zip(zip_files)
		response = HttpResponse(full_zip_in_memory, content_type='application/zip')
		response['Content-Disposition'] = 'attachment; filename="{}"'.format('Report.zip')
		return response