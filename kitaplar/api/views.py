from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from kitaplar.api.permissons import IsAdminUserOrReadOnly, IsYorumSahibiOrReadOnly
from kitaplar.api.pagination import SmallPagination, LargePagination

from kitaplar.api.serializers import KitapSerializer, YorumSerializer
from kitaplar.models import Kitap, Yorum

from rest_framework.renderers import JSONRenderer

from rest_framework.filters import SearchFilter  #filtreleme



#concrete view
class KitapListCreateAPIView(generics.ListCreateAPIView):

    # renderer_classes = [JSONRenderer] # view'da json formatında api verilerini almak için

    queryset = Kitap.objects.prefetch_related('yorumlar').order_by('-id')
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = SmallPagination
    filter_backends = [SearchFilter] # filtreleme
    search_fields = ['isim'] # filtreleme için belirlenen kolon-field



class KitapDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    renderer_classes = [JSONRenderer] # view'da json formatında api verilerini almak için
     
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class YorumCreateAPIView(generics.CreateAPIView):
    gueryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # path('kitaplar/<int:kitap_pk>/yorum_yap', api_views.YorumCreateAPIView.as_view(), name='yorum-yap')
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        kullanici = self.request.user
        yorumlar = Yorum.objects.filter(kitap=kitap, yorum_sahibi = kullanici)
        if yorumlar.exists():
            raise ValidationError('Bir kitaba sadece bir yorum yapabilirsiniz.')
        serializer.save(kitap=kitap, yorum_sahibi=kullanici)


class YorumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [IsYorumSahibiOrReadOnly]


# class KitapListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    
#     queryset = Kitap.objects.all()
#     serializer_class = KitapSerializer

#     #listeleme
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


#     #KitapYaratma
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
