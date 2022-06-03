import csv
from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import DocumentForm
from .models import DocumentModel


class HomeView(View):

    def get(self, request):
        if not request.user.is_authenticated and request.user.status:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return redirect('incoming')


class DocumentsIncoming(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        documents = DocumentModel.objects.filter(user_to__pk=request.user.pk, archived=False)
        context = {
            'documents': documents,
        }
        return render(request, 'documents/index.html', context)


class DocumentsArchive(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=True)
        context = {
            'documents': documents,
        }
        return render(request, 'documents/archive.html', context)


class DocumentsOutcoming(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=False)
        context = {
            'documents': documents,
        }
        return render(request, 'documents/index.html', context)


class DocumetnsAdd(View):
    '''
    name = models.CharField('Название документа', max_length=255, null=True)
    theme = models.CharField('Вид документа', max_length=255, null=True)
    number = models.IntegerField('Номер договора', null=True)
    type = models.CharField('Тип документа', max_length=255, null=True)
    description = models.TextField('Краткое содержание документа', null=True)
    status = models.CharField('Статус документа', choices=DOCUMENT_STATUSES, max_length=255, default=ADDED)

    load_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    ending_date = models.DateTimeField(verbose_name='Дата окончания', null=True, default=datetime.now())
    archived = models.BooleanField('В архиве', default=False)
    user_from = models.ForeignKey(CustomUser,
                                  verbose_name='От кого',
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name='user_from')
    user_to = models.ManyToManyField(CustomUser, verbose_name='Кому', null=True, related_name='user_to')
    file = models.FileField(verbose_name='Электронный файл докуента', upload_to='documents/', null=True)
    '''

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            document = DocumentModel.objects.create(file=request.FILES['file'])
            document.name = form.cleaned_data['name']
            document.number = form.cleaned_data['number']
            document.type = form.cleaned_data['type']
            document.description = form.cleaned_data['description']
            document.theme = form.cleaned_data['theme']
            document.user_from = request.user
            document.user_to = form.cleaned_data['user_to']
            document.status = DocumentModel.ADDED
            document.action = form.cleaned_data['action']
            document.ending_date = form.cleaned_data['ending_date']
            document.save()
            return redirect('outcoming')

        context = {
            'form': form
        }
        return render(request, 'documents/add.html', context)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        form = DocumentForm(data=request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'documents/add.html', context)


class DocumentsToArchive(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        document.archived = True
        document.save()
        return redirect('outcoming')


class DocumentsSubmit(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        document.submited = True
        document.status = DocumentModel.SUBMITED
        document.save()
        return redirect('incoming')


class DocumentsTerminate(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        document.status = DocumentModel.TERMINATED
        document.save()
        return redirect('incoming')


class DocumentsRead(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        document.status = DocumentModel.READ
        document.save()
        return redirect('incoming')


class DocumentsDelete(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        document.delete()

        return redirect('documents')


class DocumentsFilter(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        choice = request.GET['choice']
        error_message = False
        if choice == 'name':
            documents = DocumentModel.objects.filter(name__icontains=request.GET['q'])
        elif choice == 'number':
            try:
                int(request.GET['q'])
                documents = DocumentModel.objects.filter(number__icontains=request.GET['q'])
            except ValueError:
                documents = DocumentModel.objects.all()
                error_message = 'Ошибка! Для поиска/фильтрации по номеру документа введите число.'
        elif choice == 'user_fio':

            first_name = request.GET['q'].split(' ')[0]
            try:
                last_name = request.GET['q'].split(' ')[1]
                documents = (
                    DocumentModel.objects
                        .filter(user__first_name__icontains=first_name)
                        .filter(user__last_name__icontains=last_name)
                )
            except IndexError:
                documents = DocumentModel.objects.filter(user__first_name__icontains=first_name)

        context = {
            'documents': documents,
        }
        if error_message:
            context['error_message'] = error_message
        return render(request, 'documents/index.html', context)


class ArchiveFilter(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        choice = request.GET['choice']
        error_message = False
        if choice == 'name':
            documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=True, name__icontains=request.GET['q'])
        elif choice == 'number':
            try:
                int(request.GET['q'])
                documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=True, number__icontains=request.GET['q'])
            except ValueError:
                documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=True)
                error_message = 'Ошибка! Для поиска/фильтрации по номеру документа введите число.'
        elif choice == 'user_fio':

            first_name = request.GET['q'].split(' ')[0]
            try:
                last_name = request.GET['q'].split(' ')[1]
                documents = (
                    DocumentModel.objects
                        .filter(user__first_name__icontains=first_name)
                        .filter(user__last_name__icontains=last_name, user_from__pk=request.user.pk, archived=True)
                )
            except IndexError:
                documents = DocumentModel.objects.filter(user__first_name__icontains=first_name, user_from__pk=request.user.pk, archived=True)

        context = {
            'documents': documents,
        }
        if error_message:
            context['error_message'] = error_message
        return render(request, 'documents/archive.html', context)


class DocumentsSort(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        choice = request.GET['choice']
        up_down = request.GET['up_down']

        if up_down == 'up':
            documents = DocumentModel.objects.all().order_by(f'{choice}')
        elif up_down == 'down':
            documents = DocumentModel.objects.all().order_by(f'-{choice}')

        context = {
            'documents': documents,
        }
        return render(request, 'documents/index.html', context)


class ArchiveSort(View):

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        choice = request.GET['choice']
        up_down = request.GET['up_down']

        if up_down == 'up':
            documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=True).order_by(f'{choice}')
        elif up_down == 'down':
            documents = DocumentModel.objects.filter(user_from__pk=request.user.pk, archived=True).order_by(f'-{choice}')

        context = {
            'documents': documents,
        }
        return render(request, 'documents/archive.html', context)


class DescriptionView(View):

    def get(self, request):
        return render(request, 'documents/description.html', {})


class CreateReport(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        date = datetime.strptime(request.GET['date'], "%Y-%m-%d")
        doc_from = DocumentModel.objects.filter(load_date__year=date.year, load_date__month=date.month,
                                                load_date__day=date.day, user_from__pk=request.user.pk)
        doc_to = DocumentModel.objects.filter(load_date__year=date.year, load_date__month=date.month,
                                              load_date__day=date.day, user_to__pk=request.user.pk)
        documents = doc_from.union(doc_to)

        if not documents:
            documents = DocumentModel.objects.all()
            error_message = 'Ошибка создания отчета. Не найдено документов за эту дату.'
            context = {
                'documents': documents,
                'error_message': error_message,
            }
            return render(request, 'documents/index.html', context)
        else:

            data = []  # Окончательный список данных, которые будут возвращены
            for row in documents:
                source_data = [row.number, row.name, row.type, row.theme,
                               f'{row.user_from.first_name} {row.user_from.last_name}',
                               f'{row.user_to.first_name} {row.user_to.last_name}',
                               f'{"да" if row.archived else "нет"}',
                               f'{row.load_date.strftime("%Y.%m.%d")}',
                               f'{row.ending_date.strftime("%Y.%m.%d")}'
                               ]
                data.append(source_data)  # Добавить каждую строку списка данных в большой список

            response = HttpResponse(content_type='text/csv')  # Определить HttpResponse, тип CSV
            response[
                'Content-Disposition'] = f"attachment; filename = {date.strftime('%Y.%m.%d')}.csv"  # Определить возвращаемую информацию, метод вложения и имя файла;
            writer = csv.writer(response, dialect=csv.excel)  # Используйте модуль csv для записи ответа
            writer.writerow([
                'Номер документа',
                'Название документа',
                'Тип документа',
                'Тема документа',
                'От кого',
                'Кому',
                'В архиве',
                'Дата создания',
                'Срок выполнения',
            ])
            for row in data:
                writer.writerow(row)  # Cycle для записи информации базы данных
        return response
