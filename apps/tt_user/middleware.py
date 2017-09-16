class GetPathMiddleware():
    def process_view(self,request,view_func,view_ars,view_kwargs):
        no_path=['/user/register/',
                 '/user/username_repeat/',
                 '/user/login/',
                 '/user/login_handle/',
                 '/user/logout/',
                 '/user/yzm/',
                 '/user/add_user/']
        if request.path not in no_path:
            request.session['url_path']=request.get_full_path()
