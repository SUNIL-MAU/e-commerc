from django.shortcuts import redirect

def auth_middleware(get_response):
    
    
    def middleware(request):
        # returnUrl = request.META['PATH_INFO'] for url detail on headers
        if not request.session.get('customer'):
            return redirect('login')
        
        
        response = get_response(request)
        return response
    return middleware