from django.urls import path
from django.contrib.auth.views import LogoutView

# Importaciones específicas que ya tenías
from .views import (
    lista_pendientes,
    detalle_tarea,
    crear_tarea,
    editar_tarea,
    eliminar_tarea,
    logueo,
    pagina_registro,
    test_auth,
    calendario_view,        # ✅ Asegúrate de que esté en views.py
    eventos_api             # ✅ Necesaria para alimentar FullCalendar
)

from . import views  # Mantiene compatibilidad con views.toggle_completo

urlpatterns = [
    path('', lista_pendientes.as_view(), name='tareas'),
    path('login/', logueo.as_view(), name='login'),
    path('registro/', pagina_registro.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('tarea/<int:pk>', detalle_tarea.as_view(), name='tarea'),
    path('crear_tarea/', crear_tarea.as_view(), name='crear_tarea'),
    path('editar_tarea/<int:pk>', editar_tarea.as_view(), name='editar_tarea'),
    path('eliminar_tarea/<int:pk>', eliminar_tarea.as_view(), name='eliminar_tarea'),

    path('toggle-completo/<int:pk>/', views.toggle_completo, name='toggle_completo'),

    # 🔹 CALENDARIO
    path('calendario/', calendario_view, name='calendario'),
    path('api/eventos/', eventos_api, name='eventos_api'),

    # 🔹 TEST
    path('test-auth/', test_auth, name='test_auth'),
]
