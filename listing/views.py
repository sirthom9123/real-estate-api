from asyncio.windows_events import NULL
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchVector
from .models import Listings
from .serializers import ListingSerializer

class ManageListingView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            
            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions to get listing'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            slug = request.query_params.get('slug')
            
            if not slug:
                listing = Listings.objects.order_by('-date_created').filter(realtor=user.email)
                # object list
                listing = ListingSerializer(listing, many=True)
                
                return Response(
                    {'listings': listing.data},
                    status=status.HTTP_200_OK
                )
            
            if not Listings.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            listing = Listings.objects.filter(realtor=user.email, slug=slug)
            # Single list
            listing = ListingSerializer(listing).data
            
            return Response(
                    {'listing': listing},
                    status=status.HTTP_200_OK
                )
            
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listing or listing detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve_values(self, data):
        title = data['title']
        slug = data['slug']
        address = data['address']
        city = data['city']
        state = data['state']
        postalcode = data['postalcode']
        description = data['description']

        price = data['price']
        try:
            price = int(price)
        except:
            return -1

        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)
        except:
            return -2

        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)
        except:
            return -3

        if bathrooms <= 0 or bathrooms >= 10:
            bathrooms = 1.0

        bathrooms = round(bathrooms, 1)

        sale_type = data['sale_type']
        
        if sale_type == 'FOR_RENT':
            sale_type = 'For Rent'
        else:
            sale_type = 'For Sale'

        home_type = data['home_type']

        if home_type == 'CONDO':
            home_type = 'Condo'
        elif home_type == 'TOWNHOUSE':
            home_type = 'Townhouse'
        else:
            home_type = 'House'
        
        main_photo = data['main_photo']
        photo_1 = data['photo_1']
        photo_2 = data['photo_2']
        photo_3 = data['photo_3']
        is_published = data['is_published']

        if is_published == 'True':
            is_published = True
        else:
            is_published = False

        data = {
            'title': title,
            'slug': slug,
            'address': address,
            'city': city,
            'state': state,
            'postalcode': postalcode,
            'description': description,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sale_type': sale_type,
            'home_type': home_type,
            'main_photo': main_photo,
            'photo_1': photo_1,
            'photo_2': photo_2,
            'photo_3': photo_3,
            'is_published': is_published
        }

        return data

    def post(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for creating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            data = self.retrieve_values(data)

            if data == -1:
                return Response(
                    {'error': 'Price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -2:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -3:
                return Response(
                    {'error': 'Bathrooms must be a floating point value'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            postalcode = data['postalcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            if Listings.objects.filter(slug=slug).exists():
                return Response(
                    {'error': 'Listing with this slug already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Listings.objects.create(
                realtor=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                postalcode=postalcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published
            )

            return Response(
                {'success': 'Listing created successfully'},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'Something went wrong when creating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for creating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            data = self.retrieve_values(data)
            if data == -1:
                return Response(
                    {'error': 'Price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -2:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -3:
                return Response(
                    {'error': 'Bathrooms must be a floating point value'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            postalcode = data['postalcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            if not Listings.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exists'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Listings.objects.filter(realtor=user.email, slug=slug).update(
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                postalcode=postalcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published
            )

            return Response(
                {'success': 'Listing updates successfully'},
                status=status.HTTP_200_OK
            )
            
        except:
            return Response(
                {'error': 'Something went wrong with updating the listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    
    def patch(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for updating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            data = request.data 
            slug = data['slug']
            
            is_published = data['is_published']
            if is_published == 'True':
                is_published = True
            else:
                is_published = False
                
            if not Listings.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exists'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            Listings.objects.filter(realtor=user.email, slug=slug).update(
                is_published=is_published
            )

            return Response(
                {'success': 'Listing publish status updated successfully'},
                status=status.HTTP_200_OK
            )       
        except:
            return Response(
                {'error': 'Something went wrong when updating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    
    def delete(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for updating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            data = request.data
            try:
                slug = data['slug']
                
            except:
                return Response(
                    {'error': 'Slus was not provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not Listings.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing you are trying to delete does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            Listings.objects.filter(realtor=user.email, slug=slug).delete()
            
            if not Listings.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'error': 'Failed to delete listing'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Something went wrong when deleting listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
            
            
class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')
            
            if not slug:
                return Response(
                    {'error': 'Must provide slug'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not Listings.objects.filter(slug=slug, is_published=True).exists():
                return Response(
                    {'error': 'Published listing with this slug does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            listing = Listings.objects.filter(slug=slug, is_published=True)
            listing = ListingSerializer(listing).data
            
            return Response(
                {'listing': listing},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listing detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class ListingsView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format=None):
        try: 
            if not Listings.objects.filter(is_published=True).exists():
                return Response(
                    {'error': 'No published listings available'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            listings = Listings.objects.filter(is_published=True).order_by('-date_created')
            listings = ListingSerializer(listings, many=True).data
            
            return Response(
                {'listings': listings},
                status=status.HTTP_200_OK
            )   
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
            
class SearchListingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            city = request.query_params('city')
            state = request.query_params('state')
            max_price = request.query_params('max_price')
            
            try:
                max_price = int(max_price)
            except:
                return Response(
                    {'error': 'Max price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            bedrooms = request.query_params('bedrooms')
            try:
                bedrooms = int(bedrooms)
            except:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            bathrooms = request.query_params('bathrooms')
            try:
                bathrooms = int(bathrooms)
            except:
                return Response(
                    {'error': 'Bathrooms must be a floating value'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if bathrooms < 0 or bathrooms >= 10:
                bathrooms = 1.0

            bathrooms = round(bathrooms, 1)

            sale_type = request.query_params.get('sale_type')
            if sale_type == 'FOR_SALE':
                sale_type = 'For Sale'
            else:
                sale_type = 'For Rent'

            home_type = request.query_params.get('home_type')
            if home_type == 'HOUSE':
                home_type = 'House'
            elif home_type == 'CONDO':
                home_type = 'Condo'
            else:
                home_type = 'Townhouse'
                
            search = request.query_params('search')
            if not search:
                return Response(
                    {'error': 'Must pass search criteria'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            vector = SearchVector('title', 'description')
            query = SearchQuery(search)
            
            if not Listings.objects.annotate(
                search=vector
            ).filter(
                search=query,
                city=city,
                state=state,
                price__lte=max_price,
                bedrooms__gte=bedrooms,
                bathrooms__gte=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                is_published=True
            ).exists():
                return Response(
                    {'error': 'No listings found with this criteria'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            listings = Listings.objects.annotate(
                            search=vector
                        ).filter(
                            search=query,
                            city=city,
                            state=state,
                            price__lte=max_price,
                            bedrooms__gte=bedrooms,
                            bathrooms__gte=bathrooms,
                            sale_type=sale_type,
                            home_type=home_type,
                            is_published=True
                        )   
            listings = ListingSerializer(listings, many=True).data
            
            return Response(
                {'listings': listings},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when searching for listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )