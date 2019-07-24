from django.shortcuts import render_to_response


# def bad_request(request, exception, template_name='errors/page_400.html'):
#     return render(request, template_name)
#
#
# def permission_denied(request, exception, template_name='errors/page_403.html'):
#     return render(request, template_name)


def page_not_found(request, exception):
    return render_to_response('errors/errors_404.html')

# def server_error(request, exception, template_name='errors/page_500.html'):
#     return render(request, template_name)
