from rest_framework.response import Response
from rest_framework import status

def success_response(data, status_code=status.HTTP_200_OK):
    return Response(data=data, status=status_code)

def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({"error": message}, status=status_code)

def not_found_response(message="Resource not found", status_code=status.HTTP_404_NOT_FOUND):
    return Response({"error": message}, status=status_code)

def created_response(data, status_code=status.HTTP_201_CREATED):
    return Response(data=data, status=status_code)

def no_content_response():
    return Response(status=status.HTTP_204_NO_CONTENT)

def accepted_response(data, status_code=status.HTTP_202_ACCEPTED):
    return Response(data=data, status=status_code)
