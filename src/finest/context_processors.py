def theme_context(request):
    current_theme = request.session.get('theme', 'light')
    return {'current_theme': current_theme}