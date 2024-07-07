import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import aiohttp


@api_view(['POST'])
async def generate_summary(request):
    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required to generate summary.'}, status=status.HTTP_400_BAD_REQUEST)

    api_url = 'http://localhost:127.0.0.1:11434/api/llama3/summarize'
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={'content': content}) as response:
            if response.status == 200:
                summary = await response.json().get('summary')
                return Response({'summary': summary}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to generate summary.'}, status=response.status)
