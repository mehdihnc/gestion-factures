from django.utils.deprecation import MiddlewareMixin
from .models import FactureLog, Facture

class FactureLogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.view_name = view_func.__name__
        return None

    def process_response(self, request, response):
        if request.method == 'POST' and 'facture' in request.path.lower():
            if response.status_code in [200, 201, 302]:
                try:
                    facture = Facture.objects.latest('date_creation')
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

                    FactureLog.objects.create(
                        facture=facture,
                        utilisateur=request.user if request.user.is_authenticated else None,
                        action='creation',
                        ip_address=ip,
                        details={
                            'methode': request.method,
                            'path': request.path,
                            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                            'view': getattr(request, 'view_name', 'unknown'),
                            'referer': request.META.get('HTTP_REFERER', ''),
                        }
                    )
                except Exception as e:
                    print(f"Erreur lors de la création du log : {e}")
        return response
