from rest_framework import generics
from .models import Webinar
from .serializers import WebinarSerializer
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import razorpay
from .models import Webinar, WebinarBooking
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


User = get_user_model()



class WebinarListView(generics.ListAPIView):
    queryset = Webinar.objects.filter(is_active=True).order_by('-date')
    serializer_class = WebinarSerializer


class WebinarDetailView(generics.RetrieveAPIView):
    queryset = Webinar.objects.filter(is_active=True)
    serializer_class = WebinarSerializer
    lookup_field = 'slug'







# @csrf_exempt
# @require_POST
# def razorpay_webhook(request):
#     data = json.loads(request.body.decode('utf-8'))

#     payment_entity = data.get('payload', {}).get('payment', {}).get('entity', {})
#     payment_id = payment_entity.get('id')
#     order_id = payment_entity.get('order_id')
#     signature = payment_entity.get('signature')

#     try:
#         booking = WebinarBooking.objects.get(razorpay_order_id=order_id)
#         booking.razorpay_payment_id = payment_id
#         booking.razorpay_signature = signature
#         booking.is_paid = True
#         booking.save()

        
#         subject = " Webinar Slot Booked Successfully!"
#         message = f"""
# Hi {booking.user.first_name or booking.user.username},

# Your slot for the webinar: "{booking.webinar.title}" has been successfully booked.

#  Date: {booking.webinar.date.strftime('%Y-%m-%d %H:%M')}
#  Link: {booking.webinar.link}

# Thank you for booking!
#         """
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[booking.user.email],
#         )

#         return JsonResponse({'message': 'Successfully booked your slot! Email sent.'})
#     except WebinarBooking.DoesNotExist:
#         return JsonResponse({'error': 'Booking not found'}, status=404)





@csrf_exempt
def create_webinar_booking(request, webinar_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            user = get_object_or_404(User, id=user_id)

            webinar = get_object_or_404(Webinar, id=webinar_id)
            amount = int(webinar.price * 100)

            # 🧪 Dummy response (not using real Razorpay)
            payment = {
                'id': f'order_dummy_{webinar_id}_{user_id}',
            }

            WebinarBooking.objects.create(
                user=user,
                webinar=webinar,
                razorpay_order_id=payment['id']
            )

            return JsonResponse({
                'order_id': payment['id'],
                'amount': amount,
                'currency': 'INR',
                'razorpay_key': "dummy_key"
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)




@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)

            return JsonResponse({"message": "User registered", "user_id": user.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)




@csrf_exempt
@require_POST
def razorpay_webhook(request):
    data = json.loads(request.body.decode('utf-8'))

    # Get user email directly from the request
    user_email = data.get('email')

    payment_entity = data.get('payload', {}).get('payment', {}).get('entity', {})
    payment_id = payment_entity.get('id')
    order_id = payment_entity.get('order_id')
    signature = payment_entity.get('signature')

    booking = WebinarBooking.objects.filter(razorpay_order_id=order_id).first()

    if not booking:
        return JsonResponse({'error': 'Booking not found'}, status=404)

    booking.razorpay_payment_id = payment_id
    booking.razorpay_signature = signature
    booking.is_paid = True
    booking.save()

    subject = "Webinar Slot Booked Successfully!"
    message = f"""
Hi {booking.user.first_name or booking.user.username},

Your slot for the webinar: "{booking.webinar.title}" has been successfully booked.

Date: {booking.webinar.date.strftime('%Y-%m-%d %H:%M')}
Link: {booking.webinar.link}

Thank you for booking!
    """

    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )

    return JsonResponse({'message': 'Successfully booked your slot! Email sent.'})
