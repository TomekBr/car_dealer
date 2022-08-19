from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .forms import CustomUserCompleteDetails
from .models import Branch, Vehicle, Brand, Model, RentalOffer, CarRental, BranchCarAvailability, CustomUser
import datetime

User = get_user_model()


def home(request):
    vehicles = Vehicle.objects.all()
    ctx = {'vehicles': vehicles}

    return render(request, "car_rent/home.html", context=ctx)


def aboutus(request):
    return render(request, "car_rent/about_us.html")


class AccountDetails(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)

        account = [user.first_name, user.last_name, user.address, user.mobile,
                   user.tax_id, user.mobile, user.credit_card_nr]
        count = 0
        for i in account:
            print(i)
            if len(str(i)) is 0 or i is None:
                count += 1
        if count > 0:
            ctx = {'user': user, 'count': count}
        else:
            ctx = {'user': user}
        return render(self.request, "car_rent/account_details.html", context=ctx)


class AdminPanel(View):
    def get(self, request, *args, **kwargs):
        return render(request, "admin")


class ListOfBranches(View):
    def get(self, request, *args, **kwargs):
        list_of_branches = Branch.objects.all()
        ctx = {'list_of_branches': list_of_branches}
        return render(self.request, 'car_rent/list_of_branches.html', context=ctx)


class ViewBranch(View):
    def get(self, request, branch_id, *args, **kwargs):
        try:
            branch = Branch.objects.get(id=branch_id)
            ctx = {"branch": branch}
        except Branch.DoesNotExist:
            ctx = {'branch_id': id}
        return render(request, "car_rent/branch.html", context=ctx)


class ListOfRentalOffers(View):
    def get(self, request, *args, **kwargs):
        list_of_offers = RentalOffer.objects.all()
        vehicles = Vehicle.objects.all()
        user = CustomUser.objects.get(id=request.user.id)
        car_rentals = CarRental.objects.filter(customer_id=user.id)

        for customer_record in car_rentals:
            if customer_record.is_rented:
                ctx = {'list_of_offers': list_of_offers, 'rented': customer_record.rental_offer_id.id}
                return render(request, "car_rent/list_of_offers.html", context=ctx)

        ctx = {'list_of_offers': list_of_offers, 'vehicles': vehicles}
        return render(self.request, 'car_rent/list_of_offers.html', context=ctx)


class RentalOfferView(View):
    def get(self, request, rental_offer_id, *args, **kwargs):
        try:
            rental_offer = RentalOffer.objects.get(id=rental_offer_id)
            vehicles = Vehicle.objects.all()
            ctx = {"rental_offer": rental_offer, 'vehicles': vehicles}
        except RentalOffer.DoesNotExist:
            ctx = {'rental_offer_id': id}
        return render(request, "car_rent/offer.html", context=ctx)


class VehicleList(View):
    def get(self, request, *args, **kwargs):
        vehicles = Vehicle.objects.all()
        ctx = {'vehicles': vehicles}
        return render(self.request, "car_rent/vehiclelist.html", context=ctx)


class BrandList(View):
    def get(self, request, *args, **kwargs):
        brand = Brand.objects.all()
        ctx = {'brand': brand}

        return render(self.request, "car_rent/brand_list.html", context=ctx)


class ModelList(View):
    def get(self, request, *args, **kwargs):
        model = Model.objects.all()
        ctx = {'model': model}

        return render(self.request, "car_rent/model_list.html", context=ctx)


class CarRentalDetails(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        try:
            offer = RentalOffer.objects.get(id=id)
            car_availability = BranchCarAvailability.objects.get(vehicle_id=offer.Vehicle_Id)

        except RentalOffer.DoesNotExist:
            return HttpResponse()

        except BranchCarAvailability.DoesNotExist:
            return HttpResponse()

        date = datetime.date.today()
        '''Take loged user'''
        user = CustomUser.objects.get(id=request.user.id)
        '''Take all record for user who rent any car'''
        car_rentals = CarRental.objects.filter(customer_id=user.id)

        for customer_record in car_rentals:
            '''
            If the user is still renting any car then return rented is True then not have option to rent
            '''
            if customer_record.is_rented:
                ctx = {"offer": offer, "date": date, 'rented': True}
                return render(request, "car_rent/car_rental.html", context=ctx)

        ctx = {"offer": offer, "date": date}
        return render(request, "car_rent/car_rental.html", context=ctx)

    def post(self, request, id, *args, **kwargs):
        try:
            offer = RentalOffer.objects.get(id=id)
            availability = BranchCarAvailability.objects.get(vehicle_id=offer.Vehicle_Id)

        except RentalOffer.DoesNotExist:
            return HttpResponse()

        except BranchCarAvailability.DoesNotExist:
            return HttpResponse()

        user = CustomUser.objects.get(id=request.user.id)
        car_rental = CarRental.objects.create(customer_id=user, rental_offer_id=offer, is_rented=True)
        availability.availability = False

        car_rental.save()
        availability.save()

        ctx = {'offer': offer, 'user': user}
        return render(request, "car_rent/car_rental_succusfull.html", context=ctx)


class ReturnCar(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        try:
            offer = RentalOffer.objects.get(id=id)
            car_availability = BranchCarAvailability.objects.get(vehicle_id=offer.Vehicle_Id)

        except RentalOffer.DoesNotExist:
            return HttpResponse()

        except BranchCarAvailability.DoesNotExist:
            return HttpResponse()

        date = datetime.date.today()

        ctx = {"offer": offer, "date": date}
        return render(request, "car_rent/car_rental_return.html", context=ctx)

    def post(self, request, id, *args, **kwargs):
        try:
            offer = RentalOffer.objects.get(id=id)
            availability = BranchCarAvailability.objects.get(vehicle_id=offer.Vehicle_Id)

        except RentalOffer.DoesNotExist:
            return HttpResponse()

        except BranchCarAvailability.DoesNotExist:
            return HttpResponse()

        user = CustomUser.objects.get(id=request.user.id)
        car_rental = CarRental.objects.get(customer_id=user, rental_offer_id=offer, is_rented=True)
        car_rental.is_rented = False
        availability.availability = True

        car_rental.save()
        availability.save()

        ctx = {"offer": offer, 'user': user}
        return render(request, "car_rent/car_rental_return_successful.html", context=ctx)


class CompleteDetails(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        form = CustomUserCompleteDetails()
        ctx = {"form": form}
        return render(request, "car_rent/account_complete_details.html", context=ctx)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        form = CustomUserCompleteDetails(data=request.POST)
        print(form)
        if form.is_valid():

            user.address = form.cleaned_data["address"]
            user.company = form.cleaned_data["company"]
            user.credit_card_nr = form.cleaned_data["credit_card_nr"]
            user.tax_id = form.cleaned_data["tax_id"]
            user.mobile = form.cleaned_data["mobile"]

            user.save(update_fields=["address", "company",
                                     "credit_card_nr", "tax_id","mobile"])

            ctx = {"form": form, "user": user}
            return render(request, "car_rent/account_complete_details.html", context=ctx)
        return HttpResponse()
