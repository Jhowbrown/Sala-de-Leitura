from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from .models import Livro, Emprestimo
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import LivroForm
from .models import Livro   

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required  
from .models import Livro, Emprestimo 




# Verifica se o usuário é administrador
def is_admin(user):
    return user.is_staff

class HomeView(TemplateView):
    template_name = 'emprestimos/home.html'

class LivroListView(ListView):
    model = Livro
    template_name = 'emprestimos/livro_list.html'
    context_object_name = 'livros'

class LivroDetailView(DetailView):
    model = Livro
    template_name = 'emprestimos/livro_detail.html'
    context_object_name = 'livro'

class LoginView(TemplateView):
    template_name = 'registration/login.html'
    
@login_required
def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    if not livro.disponivel:
        messages.error(request, 'Este livro não está disponível para empréstimo.')
        return redirect('emprestimos:livro_detail', pk=livro_id)
    
    # Criar o empréstimo
    Emprestimo.objects.create(
        livro=livro,
        usuario=request.user,
        data_emprestimo=timezone.now(),
        devolvido=False
    )
    livro.disponivel = False
    livro.save()
    messages.success(request, f'Você emprestou o livro "{livro.titulo}".')
    return redirect('emprestimos:livro_detail', pk=livro_id)

class MeusEmprestimosView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'emprestimos/meus_emprestimos.html'
    context_object_name = 'emprestimos'

    def get_queryset(self):
        return Emprestimo.objects.filter(usuario=self.request.user, devolvido=False)

class EmprestimoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Emprestimo
    template_name = 'emprestimos/emprestimo_list.html'
    context_object_name = 'emprestimos'

    def test_func(self):
        return self.request.user.is_staff

@login_required
def solicitar_emprestimo(request, livro_id):
    # Buscar o livro pelo ID ou retornar um erro 404 se não for encontrado
    livro = get_object_or_404(Livro, id=livro_id)
    
    # Verificar se o livro está disponível para empréstimo
    if livro.disponivel:
        # Criar o registro de empréstimo para o usuário logado
        emprestimo = Emprestimo.objects.create(
            livro=livro,
            usuario=request.user,  # O usuário logado
            data_emprestimo=timezone.now()
        )
        # Marcar o livro como não disponível
        livro.disponivel = False
        livro.save()

        # Redirecionar o usuário para a página de seus empréstimos
        return redirect('meus_emprestimos')
    
    # Se o livro já foi emprestado, redireciona para a lista de livros
    return redirect('lista_livros')

@staff_member_required
def adicionar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = LivroForm()

    return render(request, 'emprestimos/adicionar_livro.html', {'form': form})

@login_required
def meus_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(aluno=request.user)
    return render(request, 'emprestimos/meus_emprestimos.html', {'emprestimos': emprestimos})

def login(request):
    return render(request, 'emprestimos/login.html')
    
def logout(request):
    return render(request, 'emprestimos/logout.html')
    

