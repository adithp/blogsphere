


def login_details(request):
    user_session = request.session.get('cuuser', {})
    return {
        'cuuser':user_session
    }
