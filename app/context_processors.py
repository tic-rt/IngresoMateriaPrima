
def grupos_usuario(request):
    if request.user.is_authenticated:
        grupos = list(request.user.groups.values_list('name', flat=True))
    else:
        grupos = []
    return {'grupos_usuario': grupos}