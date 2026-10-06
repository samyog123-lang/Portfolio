from .models import PortfolioProfile


def profile_context(request):
    return {'profile': PortfolioProfile.objects.filter(pk=1).first()}