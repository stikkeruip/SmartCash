from django.contrib.auth import login
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .forms import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, PersonalInformationSerializer, BankLinkingSerializer


def test_api(request):
    """Simple HTML interface to test the API endpoints"""
    return render(request, 'accounts/test_api.html')


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Show registration form"""
        serializer = UserRegistrationSerializer()
        return Response(serializer.data)
    
    def post(self, request):
        """Register a new user and return authentication token."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Show login form"""
        serializer = UserLoginSerializer()
        return Response(serializer.data)
    
    def post(self, request):
        """Authenticate user with username/email and password, return token."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Logout user by deleting their authentication token."""
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({
                'message': 'Token not found'
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile information."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """Update user profile information."""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        """Delete the authenticated user's account permanently."""
        user = request.user
        username = user.username
        
        # Delete the user's token first
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        
        # Delete the user account
        user.delete()
        
        return Response({
            'message': f'Account for user "{username}" has been permanently deleted',
            'deleted_user': username
        }, status=status.HTTP_200_OK)


class PersonalInformationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's personal information (DoB, phone, address)."""
        serializer = PersonalInformationSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """Update user's personal information."""
        serializer = PersonalInformationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Personal information updated successfully',
                'personal_info': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankOptionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get available banks for linking."""
        banks = [
            {
                'bank_code': 'piraeus',
                'bank_name': 'Piraeus Bank',
                'country': 'GR',
                'supported_services': ['PSD2_AIS', 'PSD2_PIS'],
                'link_endpoint': '/api/bank/piraeus/',
                'description': 'Link your Piraeus Bank account for account information and payment services',
                'requirements': ['customer_id', 'sca_method']
            }
        ]
        
        return Response({
            'available_banks': banks,
            'total_banks': len(banks),
            'message': 'Available banks for account linking'
        }, status=status.HTTP_200_OK)


class PiraeusLinkingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current Piraeus bank linking status."""
        user = request.user
        is_linked = bool(user.piraeus_customer_id)
        
        response_data = {
            'is_linked': is_linked,
            'bank_name': 'Piraeus Bank',
            'bank_code': 'piraeus'
        }
        
        if is_linked:
            response_data.update({
                'customer_id': user.piraeus_customer_id,
                'preferred_sca_method': user.preferred_sca_method,
                'consent_status': 'active' if user.bank_consent_ids else 'none',
                'linked_services': list(user.bank_consent_ids.keys()) if user.bank_consent_ids else []
            })
        else:
            response_data['message'] = 'Piraeus Bank account not linked'
            
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Link Piraeus bank account."""
        serializer = BankLinkingSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            
            # Initialize consent tracking
            if not user.bank_consent_ids:
                user.bank_consent_ids = {
                    'account_linking': {
                        'status': 'initiated',
                        'timestamp': str(timezone.now()),
                        'customer_id': user.piraeus_customer_id
                    }
                }
                user.save()
            
            return Response({
                'message': 'Piraeus Bank account linked successfully',
                'bank_info': {
                    'customer_id': user.piraeus_customer_id,
                    'preferred_sca_method': user.preferred_sca_method,
                    'link_status': 'active',
                    'next_steps': [
                        'Verify your identity through SCA',
                        'Grant consent for account information access',
                        'Complete PSD2 authentication flow'
                    ]
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """Unlink Piraeus bank account."""
        user = request.user
        
        if not user.piraeus_customer_id:
            return Response({
                'message': 'No Piraeus Bank account is currently linked'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Store customer ID for response
        customer_id = user.piraeus_customer_id
        
        # Clear bank linking data
        user.piraeus_customer_id = None
        user.bank_consent_ids = {}
        user.preferred_sca_method = 'SMS'
        user.save()
        
        return Response({
            'message': 'Piraeus Bank account unlinked successfully',
            'unlinked_customer_id': customer_id,
            'status': 'unlinked'
        }, status=status.HTTP_200_OK)
