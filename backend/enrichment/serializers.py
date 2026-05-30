from rest_framework import serializers

class EnrichmentInputSerializer(serializers.Serializer):
    url = serializers.CharField(required=True, help_text="The company website URL to enrich.")
    website_name = serializers.CharField(required=False, allow_blank=True, default="", help_text="Optional website name.")

    def validate_url(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("URL cannot be empty.")
        # Basic parsing check
        if not value.startswith("http://") and not value.startswith("https://") and "." not in value:
            raise serializers.ValidationError("Invalid URL format.")
        return value


class EnrichedCompanySerializer(serializers.Serializer):
    website_name = serializers.CharField(allow_blank=True, default="")
    company_name = serializers.CharField(allow_blank=True, default="")
    address = serializers.CharField(allow_blank=True, default="")
    mobile_number = serializers.CharField(allow_blank=True, default="")
    mail = serializers.ListField(child=serializers.CharField(), default=list)
    core_service = serializers.CharField(allow_blank=True, default="")
    target_customer = serializers.CharField(allow_blank=True, default="")
    probable_pain_point = serializers.CharField(allow_blank=True, default="")
    outreach_opener = serializers.CharField(allow_blank=True, default="")
