import io as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import context
from django.http import HttpResponse

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    
    html  = template.render(context_dict)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors')