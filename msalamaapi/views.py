# from django.http import HttpResponse
# from django.http import JsonResponse
# from django.core.cache import cache
# from django.shortcuts import render
# from django.contrib.auth.models import User
# from vaccines.models import Vaccine, SideEffectbyVaccine
# from users.models import UserProfile, DependantProfile, UserVaccination, Doctor
#     # , Facility
# from django.core import serializers
#
# from django.core import serializers
# # from msalamapi.serializers import VaccineSerializer, SideEffectbyVaccineSerializer, UserSerializer, FacilitySerializer, DoctorUserSerializer
#
# #
# # class JSONResponse(HttpResponse):
# #     """
# #     An HttpResponse that renders its content into JSON.
# #     """
# #     def __init__(self, data, **kwargs):
# #         content = JSONRenderer().render(data)
# #         kwargs['content_type'] = 'application/json'
# #         super(JSONResponse, self).__init__(content, **kwargs)
#
# class VaccineList(generics.ListAPIView):
#     queryset = Vaccine.objects.all()
#     serializer_class = VaccineSerializer
#
#
# class SideEffectbyVaccine(generics.ListAPIView):
#     queryset = SideEffectbyVaccine.objects.all()
#     serializer_class = SideEffectbyVaccineSerializer
#
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.ListAPIView):
#     # queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         """
#         This view should return a list of all the User details
#         for the currently authenticated user.
#         """
#
#         queryset = User.objects.all()
#         username = self.kwargs['pk']
#         print username
#         if username is not None:
#             queryset = queryset.filter(id=username)
#         return queryset
#
#
# def DependantDetail(request, pk):
#         """
#         This view should return a list of all the Dependant details
#         for the currently authenticated user.
#         """
#
#         username = pk
#         ID = DependantProfile.objects.filter(Parent=pk)
#         Usaggregate= User.objects.none()
#
#         for item in ID:
#             Usaggregate= list(Usaggregate) + list(User.objects.filter(id=item.user.id))
#
#         # Userdata = list(Usaggregate)
#         Usprofiledata = list(DependantProfile.objects.filter(Parent = pk))
#
#
#
#         data= serializers.serialize('json', Usaggregate
#                                      +
#                                      Usprofiledata)
#         # return JSONResponse(data)
#         return HttpResponse(data, content_type='application/json')
#
# def VaccinationsRecieved(request, pk):
#
#     parentvaccinations=list(UserVaccination.objects.filter(patient__id = pk))
#     children = DependantProfile.objects.filter(Parent=pk)
#     allchildrenvaccions = UserVaccination.objects.none()
#     for item in children:
#         allchildrenvaccions = list(allchildrenvaccions) + list(UserVaccination.objects.filter(patient=item.user.id))
#
#
#     data = serializers.serialize('json', parentvaccinations
#                                  +
#                                  allchildrenvaccions)
#
#     return HttpResponse(data, content_type='application/json')
#
#
#
# class DoctorList(generics.ListAPIView):
#     doctors = cache.get('doctors')
#     if doctors is None:
#         doctors = list(Doctor.objects.all())
#         cache.set('doctors', doctors )
#
#     queryset = User.objects.filter(doctors__in = doctors)
#
#     serializer_class = DoctorUserSerializer
#
#
# class FacilityList(generics.ListAPIView):
#     queryset=Facility.objects.all()
#     serializer_class = FacilitySerializer
