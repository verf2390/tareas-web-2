from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms
from .models import Tarea


def test_auth(request):
    if request.user.is_authenticated:
        return HttpResponse("Estás autenticado")
    else:
        return HttpResponse("No estás autenticado")


class logueo(LoginView):
    template_name = 'base/login.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tareas')


class pagina_registro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(pagina_registro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(pagina_registro, self).get(*args, **kwargs)


def toggle_completo(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)

    # Asegurarse que el usuario es el dueño de la tarea
    if tarea.usuario != request.user:
        return redirect('tareas')  # O mostrar error si quieres

    tarea.completo = not tarea.completo
    tarea.save()
    return redirect('tareas')  # Redirige a la lista de tareas


class lista_pendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'
    template_name = 'base/tareas.html'  # corregido para incluir 'base/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tareas_usuario = self.get_queryset()

        valor_buscado = self.request.GET.get('area_buscar') or ''
        if valor_buscado:
            tareas_usuario = tareas_usuario.filter(titulo__icontains=valor_buscado)

        context['tareas'] = tareas_usuario
        context['count'] = tareas_usuario.filter(completo=False).count()
        context['valor_buscado'] = valor_buscado
        return context

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)


class detalle_tarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


# Formulario personalizado para el campo fecha_tarea con widget datetime-local
class TareaForm(forms.ModelForm):
    fecha_tarea = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label='Fecha y hora de la tarea'
    )

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'completo', 'fecha_tarea']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fecha_tarea:
            self.initial['fecha_tarea'] = self.instance.fecha_tarea.strftime('%Y-%m-%dT%H:%M')


class crear_tarea(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'base/tarea_form.html'
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class editar_tarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'base/tarea_form.html'
    success_url = reverse_lazy('tareas')


class eliminar_tarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tareas'
    template_name = 'base/tarea_confirm_delete.html'  # recomendable para DeleteView
    success_url = reverse_lazy('tareas')


@login_required
def calendario_view(request):
    return render(request, 'base/calendario.html')  # ruta correcta


@login_required
def eventos_api(request):
    tareas = Tarea.objects.filter(usuario=request.user)
    eventos = []

    for tarea in tareas:
        if tarea.fecha_tarea:
            eventos.append({
                "title": tarea.titulo,
                "start": tarea.fecha_tarea.isoformat(),
                "end": tarea.fecha_tarea.isoformat(),
                "color": "#3788d8"  # opcional
            })

    return JsonResponse(eventos, safe=False)

