import csv
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import DocumentForm
from .models import DocumentModel


class DocumentsView(View):

    def get(self, request):
        documents = DocumentModel.objects.all()
        context = {
            'documents': documents,
        }
        return render(request, 'documents/index.html', context)


class DocumetnsAdd(View):

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            document = DocumentModel.objects.create(file=request.FILES['file'])
            document.name = form.cleaned_data['name']
            document.number = form.cleaned_data['number']
            document.user = request.user
            document.save()
            return redirect('documents')

        context = {
            'form': form
        }
        return render(request, 'documents/add.html', context)

    def get(self, request):
        form = DocumentForm(data=request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'documents/add.html', context)


class DocumentsChange(View):

    def post(self, request, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            document = DocumentModel.objects.get(pk=kwargs['pk'])
            document.name = form.cleaned_data['name']
            document.number = form.cleaned_data['number']
            document.user = request.user
            document.file = request.FILES['file']
            document.save()
            return redirect('documents')

        context = {
            'form': form
        }
        return render(request, 'documents/add.html', context)

    def get(self, request, **kwargs):
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        form = DocumentForm(instance=document)
        context = {
            'form': form,
        }
        return render(request, 'documents/add.html', context)


class DocumentsDelete(View):

    def get(self, request, **kwargs):
        document = DocumentModel.objects.get(pk=kwargs['pk'])
        document.delete()

        return redirect('documents')


class DocumentsFilter(View):

    def get(self, request, **kwargs):

        choice = request.GET['choice']
        if choice == 'name':
            documents = DocumentModel.objects.filter(name__icontains=request.GET['q'])
        elif choice == 'number':
            documents = DocumentModel.objects.filter(number__icontains=request.GET['q'])
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
        return render(request, 'documents/index.html', context)


class DocumentsSort(View):

    def get(self, request, **kwargs):

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


class DescriptionView(View):

    def get(self, request):
        return render(request, 'documents/description.html', {})


class CreateReport(View):

    def get(self, request):

        date = datetime.strptime(request.GET['date'], "%Y-%m-%d")
        documents = DocumentModel.objects.filter(change_date__year=date.year, change_date__month=date.month,
                                                 change_date__day=date.day)

        if not documents:
            documents = DocumentModel.objects.all()
            error_message = 'Ошибка создания отчета. Не найдено документов за эту дату.'
            context = {
                'documents': documents,
                'error_message': error_message,
            }
            return render(request, 'documents/index.html', context)
        else:
            '''
                number = models.IntegerField('Номер договора')
                name = models.CharField('Название договора', max_length=255)
                type = models.CharField('Тип документа', max_length=255, null=True)
                author = models.CharField('Автор документа', max_length=255, null=True)
                doc_from = models.CharField('Отдел откуда документ', max_length=255, null=True)
                description = models.TextField('Краткое описание документа', null=True)
                theme = models.CharField('Тема документа', max_length=255, null=True)
                user = models.ForeignKey(CustomUser, verbose_name='Кто добавил', on_delete=models.CASCADE, null=True)
                load_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
                change_date = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
                file = models.FileField(verbose_name='Электронный файл договора', upload_to='documents/')
            '''
            data = []  # Окончательный список данных, которые будут возвращены
            for row in documents:
                source_data = [row.number, row.name, row.type, row.author, row.doc_from, row.theme,
                               f'{row.user.first_name} {row.user.last_name}', f'{row.change_date.strftime("%Y.%m.%d")}'
                               ]
                data.append(source_data)  # Добавить каждую строку списка данных в большой список

            response = HttpResponse(content_type='text/csv')  # Определить HttpResponse, тип CSV
            response[
                'Content-Disposition'] = f"attachment; filename = {date.strftime('%Y.%m.%d')}.csv"  # Определить возвращаемую информацию, метод вложения и имя файла;
            writer = csv.writer(response)  # Используйте модуль csv для записи ответа
            writer.writerow([
                'Номер документа',
                'Название документа',
                'Тип документа',
                'Автор документа',
                'Отдел откуда документ',
                'Тема документа',
                'ФИО добавил',
                'Дата добавления/изменения',
            ])
            for row in data:
                writer.writerow(row)  # Cycle для записи информации базы данных
            return response
