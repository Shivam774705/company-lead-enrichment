from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import EnrichmentInputSerializer, EnrichedCompanySerializer
from .scraper import SmartScraper
from .ai_service import GroqService
from .utils import ResultsStorage, clean_url
from .constants import DEFAULT_RESPONSE_SCHEMA

@api_view(['POST'])
@permission_classes([AllowAny])
def enrich_company_api(request):
    """
    POST /api/enrich/
    Enriches a company by scraping its website and generating insights using Groq AI.
    """
    serializer = EnrichmentInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    validated_data = serializer.validated_data
    url = validated_data.get('url')
    custom_website_name = validated_data.get('website_name', '').strip()
    
    # 1. Clean the incoming URL
    target_url = clean_url(url)
    if not target_url:
        return Response({"error": "Invalid URL provided"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # 2. Run smart scraping
        scraper = SmartScraper(target_url)
        scraped_data = scraper.scrape()
        
        # 3. Call Groq AI service for enrichment
        ai_service = GroqService()
        enriched_data = ai_service.enrich_company(
            cleaned_text=scraped_data.get("combined_text", ""),
            emails=scraped_data.get("emails", []),
            phones=scraped_data.get("phones", []),
            custom_website_name=custom_website_name
        )
        
        # Add metadata for reference/caching
        enriched_data["website_url"] = target_url
        
        # 4. Store result in-memory (thread-safe + local JSON back-up)
        ResultsStorage.add(enriched_data)
        
        # 5. Return response formatted to strict schema
        response_serializer = EnrichedCompanySerializer(enriched_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Exception raised during enrichment: {e}")
        # Crash safety: return fallback schema instead of failing
        fallback_data = DEFAULT_RESPONSE_SCHEMA.copy()
        fallback_data["website_name"] = custom_website_name or "Unknown Company"
        fallback_data["website_url"] = target_url
        fallback_data["probable_pain_point"] = f"An error occurred: {str(e)}"
        
        # Add to results even if failed, for debugging/completeness
        ResultsStorage.add(fallback_data)
        
        response_serializer = EnrichedCompanySerializer(fallback_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_results_api(request):
    """
    GET /api/results/
    Returns a list of all enriched company profiles stored in memory.
    """
    try:
        results = ResultsStorage.get_all()
        serializer = EnrichedCompanySerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Exception listing results: {e}")
        return Response([], status=status.HTTP_200_OK)
