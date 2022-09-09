from django.http import HttpResponse
from django.shortcuts import render, redirect


from apps.owner.forms import OwnerForm
from apps.owner.models import Owner

from django.db.models import Q, F
from apps.owner.serializers import OwnerSerializer

#Segunda parte de la clase
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Serializador
from django.core import serializers as ssr

# DRF
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


def owner_list(request):
    # data_context = {'nombre_owner': 'KEVIN',
    #                 'edad': 18,
    #                 'pais': 'Perú',
    #                 'vigente': False,
    #                 'pokemones': [{
    #                                 'nombre_pokemon': "Charizard",
    #                                 'ataques': ['atq 1 Charizard', 'atq 2 Charizard','atq 3 Charizard']
    #                             },
    #                             {
    #                                 'nombre_pokemon': "New",
    #                                 'ataques': ['atq 1 New', 'atq 2 New', 'atq 3 New']
    #                             },
    #                             {
    #                                 'nombre_pokemon': "Balbasour",
    #                                 'ataques': ['atq 1 Balbasour', 'atq 2 Balbasour', 'atq 3 Balbasour']
    #                             }
    #                             ]
    #                 }

    """Crear un objeto en la Base de Datos"""
    # p = Owner(nombre="Rousmery", edad=37)
    # p.save()

    # p.nombre = "Karla"
    # p.save()

    """Obtener todos los datos de una tabla en la BD"""
    # data_context = Owner.objects.all()

    """Filtración de datos: filter()"""
    # data_context = Owner.objects.filter(nombre='Karla')

    """Filtración de datos con AND de SQL: filter()"""

    # data_context = Owner.objects.filter(nombre='Karla', edad='29')

    """Filtración de datos más preciosos con: __constains"""

    # data_context = Owner.objects.filter(nombre__contains='karla')

    """Filtración de datos más preciosos con: __endswith"""
    # data_context = Owner.objects.filter(nombre__endswith='la')

    """Ordenar por cualquier atributo en la Base de Datos"""

    """Ordenar alfabéticamente por nombre"""
    # data_context = Owner.objects.order_by('nombre')

    """Ordenar alfabéticamente por edad"""
    # data_context = Owner.objects.order_by('edad')

    """Ordenar de manera inversa por la edad"""
    data_context = Owner.objects.order_by('-edad')

    """Acortar datos: Obtener un rango de registro de una tabla en la BD"""
    # data_context = Owner.objects.all()[2:6]

    """Eliminar objetos en la BD"""
    """Eliminar el objeto con id = 31 en la BD"""
    # p = Owner.objects.get(id=11)
    # p.delete()

    """Eliminando un conjunto de datos específico"""
    # Owner.objects.filter(pais__startswith="Bra").delete()

    """Eliminar todos los objetos de la BD"""
    # p = Owner.objects.all()
    # p.delete()

    """Actualización de datos en la BD a un cierto un grupo de datos"""

    Owner.objects.filter(pais__startswith="Bra").update(edad=17)

    """Concatenar consultas"""
    # data_context = Owner.objects.filter(nombre="Karla").order_by("-edad")

    """Utilizando F expressions"""

    Owner.objects.filter(edad__gte=17).update(edad=F('edad') + 10)

    # data_context = Owner.objects.get(nombre="Karla")

    """Consultas complejas"""

    query = Q(pais__startswith='Pe') | Q(pais__startswith='Br')

    "Negar Q"
    # query = Q(pais__startswith='Pe') & ~Q(edad=37)

    # print("Query: {}".format(query))
    # Query

    # data_context = Owner.objects.filter(query)

    # query = Q(pais__startswith='Pe') | Q(pais__startswith='Br')

    # Query inválida
    "Error de consulta Q"
    # data_context = Owner.objects.filter(edad=37, query)

    # data_context = Owner.objects.filter(query, edad=37)

    return render(request, 'owner/owners.html', context={'data': data_context})


def owner_details(request):
    return render(request, 'owner/owner_detail.html', {})


def owner_search(request):
    query = request.GET.get('q', '')
    # print("query: {}".format(query))
    results = (
        Q(nombre__icontains=query)
    )
    print("resuts: {}".format(results))
    data_context = Owner.objects.filter(results).distinct()

    return render(request, 'owner/owner_search.html', context={'data': data_context, "query": query})


def owner_create(request):
    if request.method == "POST":
        form = OwnerForm(request.POST)
        if form.is_valid():
            """Guarda todos los campos que vienen desde la plantilla"""
            # nombre = form.cleaned_data['nombre']
            # print("Nombre: {}".format(nombre))
            # edad = form.cleaned_data['edad']
            # pais = form.cleaned_data['pais']
            try:
                form.save()
                return redirect('owner_list')
            except:
                pass
    else:
        form = OwnerForm()

    return render(request, 'owner/owner-create.html', {'form': form})


def owner_delete(request, id):
    owner = Owner.objects.get(id=id)
    try:
        owner.delete()
    except:
        pass
    return redirect('owner_list')


def owner_edit(request, id):
    owner = Owner.objects.get(id=id)
    form = OwnerForm(initial={'nombre': owner.nombre, 'edad': owner.edad, 'pais': owner.pais})

    if request.method == "POST":
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('owner_list')
            except Exception as e:
                pass

    return render(request, 'owner/owner_update.html', {'form': form})


# Vistas basadas en clases
class OwnerList(ListView):
    model = Owner
    template_name = 'owner/owners_vc.html'


class OwnerCreate(CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'owner/owner-create.html'
    success_url = reverse_lazy('owner_list_vc')


class OwnerUpdate(UpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'owner/owner-create.html'
    success_url = reverse_lazy('owner_list_vc')


class OwnerDelete(DeleteView):
    model = Owner
    template_name = 'owner/owner-confirm-delete.html'
    success_url = reverse_lazy('owner_list_vc')


"""Serialización"""

def ListOwnerSerializer(request):
    #query
    lista_owner = ssr.serialize('json', Owner.objects.all(), fields=['nombre', 'edad'])
    return HttpResponse(lista_owner, content_type='application/json')



"""Serialización con DJANGO"""
class OnwnerApiView(ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


"""Serialización con funciones DRF"""
@api_view(['GET', 'POST'])
def owner_api_view(request):

    if request.method == 'GET':
        queryset = Owner.objects.all()
        serializer_class = OwnerSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OwnerSerializer(data=request.data, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def owner_detail_view(request, pk):
    queryset = Owner.objects.filter(id=pk).first()
    if queryset:
        if request.method == 'GET':
            #queryset = Owner.objects.filter(id=pk).first()
            serializer_class = OwnerSerializer(queryset)

            return Response(serializer_class.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            #queryset = Owner.objects.filter(id=pk).first()
            serializer_class = OwnerSerializer(queryset, data=request.data)

            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data)
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            #queryset = Owner.objects.filter(id=pk).first()
            queryset.delete()
            #return Response('El owner ha sido eliminado satisfactoriamente')
            return Response({'message': 'Owner se ha eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado el owner que buscaba'}, status=status.HTTP_400_BAD_REQUEST)
