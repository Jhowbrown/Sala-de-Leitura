from django.urls import include, path
from emprestimos import views
import emprestimos.devolver_emprestimo
from . import views
from django.contrib.auth import views as auth_views



app_name = 'emprestimos'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('livros/', views.LivroListView.as_view(), name='livro_list'),
    path('livros/<int:pk>/', views.LivroDetailView.as_view(), name='livro_detail'),
    path('emprestar/<int:livro_id>/', views.emprestar_livro, name='emprestar_livro'),
    #path('meus_emprestimos/', views.meus_emprestimos, name='meus_emprestimos'),
    path('solicitar_emprestimo/<int:livro_id>/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('emprestimos/', views.EmprestimoListView.as_view(), name='emprestimo_list'),  # Para admin
    path('emprestimos/<int:pk>/devolver/', emprestimos.devolver_emprestimo.devolver_emprestimo, name='devolver_emprestimo'),
    path('adicionar/', views.adicionar_livro, name='adicionar_livro'),
    #path('', views.lista_livros, name='lista_livros'),
    #path('lista/', views.lista_livros, name='lista_livros'),
    #path('solicitar_emprestimo/<int:livro_id>/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('meus_emprestimos/', views.meus_emprestimos, name='meus_emprestimos'),
    
]
