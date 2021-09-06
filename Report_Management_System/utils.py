from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import zipfile
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    buffer = BytesIO()
    p = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), buffer)
    pdf = buffer.getvalue()
    buffer.close()
    if not p.err:
        return pdf#HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()