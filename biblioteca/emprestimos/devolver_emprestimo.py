from emprestimos.models import Emprestimo
from emprestimos.views import is_admin


from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


@login_required
@user_passes_test(is_admin)
def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.devolvido:
        messages.info(request, 'Este empréstimo já foi devolvido.')
    else:
        emprestimo.devolvido = True
        emprestimo.data_devolucao = timezone.now()
        emprestimo.livro.disponivel = True
        emprestimo.livro.save()
        emprestimo.save()
        messages.success(request, f'O livro "{emprestimo.livro.titulo}" foi devolvido.')
    return redirect('emprestimos:emprestimo_list')