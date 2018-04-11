from django.http import JsonResponse

class AjaxMixin(object):
    success_return_code = 1
    error_return_code = 0

    def form_valid(self,form):
        if self.request.is_ajax():
            self.object = form.save()
            data = {'result':self.success_return_code}
            return JsonResponse(data)
        else:
            resp = super(AjaxMixin,self).form_valid(form)
            return resp

    def form_invalid(self,form):

        resp = super(AjaxMixin,self).form_invalid(form)
        if self.request.is_ajax():
            form.errors.update({'result':self.error_return_code})
            return JsonResponse(form.errors,status=400)
        else:
            return resp

